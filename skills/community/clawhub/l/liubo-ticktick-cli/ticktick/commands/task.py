import json
import sys

from ..api import api, PRIORITY_MAP
from ..util import is_task_id, parse_due_date


def task_create_command(args) -> None:
    try:
        project = api.find_project_by_name(args.list)
        if not project:
            print(f"Project not found: {args.list}", file=sys.stderr)
            sys.exit(1)

        payload: dict = {"title": args.title, "projectId": project["id"]}

        if args.content:
            payload["content"] = args.content

        if args.priority:
            priority = PRIORITY_MAP.get(args.priority.lower())
            if priority is None:
                print(f"Invalid priority: {args.priority}. Use none, low, medium, or high.", file=sys.stderr)
                sys.exit(1)
            payload["priority"] = priority

        if args.due:
            payload["dueDate"] = parse_due_date(args.due)

        if args.start:
            payload["startDate"] = parse_due_date(args.start)

        if args.tag:
            payload["tags"] = args.tag

        task = api.create_task(payload)

        if args.json:
            print(json.dumps(task, indent=2))
            return

        print(f'✓ Task created: "{task["title"]}"')
        print(f'  ID: {task["id"]}')
        print(f'  Project: {project["name"]}')
        if task.get("dueDate"):
            print(f'  Due: {task["dueDate"]}')

    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def task_update_command(args) -> None:
    try:
        task_name_or_id = args.title

        if is_task_id(task_name_or_id) and not args.list:
            found = api.find_task_by_id(task_name_or_id)
        else:
            found = api.find_task_by_title(task_name_or_id, args.list)

        if not found:
            print(f"Task not found: {task_name_or_id}", file=sys.stderr)
            sys.exit(1)

        task = found["task"]
        project_id = found["projectId"]

        payload: dict = {"id": task["id"], "projectId": project_id}

        if args.new_title is not None:
            payload["title"] = args.new_title

        if args.content is not None:
            payload["content"] = args.content

        if args.priority:
            priority = PRIORITY_MAP.get(args.priority.lower())
            if priority is None:
                print(f"Invalid priority: {args.priority}. Use none, low, medium, or high.", file=sys.stderr)
                sys.exit(1)
            payload["priority"] = priority

        if args.due:
            payload["dueDate"] = parse_due_date(args.due)

        if args.start:
            payload["startDate"] = parse_due_date(args.start)

        if args.tag:
            payload["tags"] = args.tag

        updated = api.update_task(payload)

        if args.json:
            print(json.dumps(updated, indent=2))
            return

        print(f'✓ Task updated: "{updated.get("title", task["title"])}"')
        print(f'  ID: {updated.get("id", task["id"])}')

    except (RuntimeError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
