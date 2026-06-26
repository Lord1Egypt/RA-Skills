import json
import sys
from datetime import datetime, timedelta

from ..api import api

PRIORITY_LABEL = {5: "[HIGH]", 3: "[MED] ", 1: "[LOW] ", 0: "      "}


def _format_due_date(date_str: str) -> str:
    try:
        date = datetime.fromisoformat(date_str.replace("+0000", "+00:00"))
    except ValueError:
        return date_str

    now = datetime.now()
    today = now.date()
    tomorrow = (now + timedelta(days=1)).date()

    if date.date() == today:
        return "today"
    if date.date() == tomorrow:
        return "tomorrow"
    if date.date() < today:
        return f"overdue ({date.strftime('%b %-d')})"
    return date.strftime("%b %-d")


def _format_task(task: dict, show_project: bool = False) -> str:
    status = "✓" if task.get("status") == 2 else "○"
    priority = PRIORITY_LABEL.get(task.get("priority", 0), "      ")
    short_id = task["id"][:8]
    title = task.get("title", "")

    project_str = f" ({task.get('projectName', '')})" if show_project and task.get("projectName") else ""
    due_str = f" due:{_format_due_date(task['dueDate'])}" if task.get("dueDate") else ""
    tags = task.get("tags") or []
    tags_str = f" [{', '.join(tags)}]" if tags else ""

    return f"{status} {priority} [{short_id}] {title}{project_str}{due_str}{tags_str}"


def _sort_tasks(tasks: list[dict]) -> list[dict]:
    def key(t: dict):
        completed = 1 if t.get("status") == 2 else 0
        priority = -(t.get("priority") or 0)  # negate: higher priority sorts first
        due = t.get("dueDate") or "9999"
        title = t.get("title", "")
        return (completed, priority, due, title)

    return sorted(tasks, key=key)


def tasks_command(args) -> None:
    try:
        projects = api.list_projects()
        project_map = {p["id"]: p["name"] for p in projects}

        search_projects = projects
        if args.list:
            project = api.find_project_by_name(args.list)
            if not project:
                print(f"Project not found: {args.list}", file=sys.stderr)
                sys.exit(1)
            search_projects = [project]

        tasks_with_projects: list[dict] = []
        for project in search_projects:
            try:
                data = api.get_project_data(project["id"])
                for task in data.get("tasks") or []:
                    tasks_with_projects.append({
                        **task,
                        "projectName": project_map.get(task.get("projectId", ""), task.get("projectId", "")),
                    })
            except RuntimeError:
                continue

        filtered = tasks_with_projects
        if getattr(args, "status", None) == "pending":
            filtered = [t for t in tasks_with_projects if t.get("status") != 2]
        elif getattr(args, "status", None) == "completed":
            filtered = [t for t in tasks_with_projects if t.get("status") == 2]

        if args.json:
            print(json.dumps(filtered, indent=2))
            return

        if not filtered:
            print("No tasks found.")
            return

        sorted_tasks = _sort_tasks(filtered)
        print(f"\nTasks ({len(sorted_tasks)}):\n")
        for task in sorted_tasks:
            print(_format_task(task, show_project=not args.list))

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
