from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

todos = []

template = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Todo List</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f4f4f9; }
    .container { max-width: 600px; margin: 50px auto; background: #fff; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
    h1 { margin-top: 0; }
    form { display: flex; gap: 10px; margin-bottom: 20px; }
    input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
    button { padding: 10px 15px; border: none; background: #007bff; color: #fff; border-radius: 4px; cursor: pointer; }
    button:hover { background: #0056d6; }
    ul { list-style: none; padding: 0; }
    li { display: flex; justify-content: space-between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }
    li.done span { text-decoration: line-through; color: #888; }
    .actions { display: flex; gap: 6px; }
    .actions a { text-decoration: none; color: #007bff; }
    .actions a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Todo List</h1>
    <form method="post" action="/">
      <input type="text" name="todo" placeholder="Add a new task" autocomplete="off" required>
      <button type="submit">Add</button>
    </form>
    <ul>
      {% for idx, item in todos %}
        <li class="{% if item.done %}done{% endif %}">
          <span>{{ item.task }}</span>
          <div class="actions">
            <a href="{{ url_for('toggle', index=idx) }}">{% if item.done %}Undo{% else %}Done{% endif %}</a>
            <a href="{{ url_for('delete', index=idx) }}">Delete</a>
          </div>
        </li>
      {% endfor %}
    </ul>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("todo", "").strip()
        if task:
            todos.append({"task": task, "done": False})
        return redirect(url_for("index"))
    return render_template_string(template, todos=list(enumerate(todos)))

@app.route("/toggle/<int:index>")
def toggle(index):
    if 0 <= index < len(todos):
        todos[index]["done"] = not todos[index]["done"]
    return redirect(url_for("index"))

@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(todos):
        todos.pop(index)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

