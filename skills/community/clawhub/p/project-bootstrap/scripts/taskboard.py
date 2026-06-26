#!/usr/bin/env python3
"""Pluggable taskboard CLI for multi-agent projects.

Backends: local (JSON file), github (GitHub Issues).
Configure via taskboard.config.json or --config flag.
"""

import argparse
import json
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

STATUSES = ["backlog", "in-progress", "review", "done", "blocked", "rejected"]
PRIORITIES = ["low", "medium", "high", "critical"]
STATUS_EMOJI = {
    "backlog": "📥", "in-progress": "🔄", "review": "👀",
    "done": "✅", "blocked": "🚫", "rejected": "❌",
}
DEFAULT_CONFIG = "taskboard.config.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ── Backend Interface ──────────────────────────────────────────────

class Backend(ABC):
    @abstractmethod
    def load(self) -> dict:
        """Return board dict with 'tasks' list and 'meta' dict."""

    @abstractmethod
    def save(self, board: dict):
        """Persist the board."""

    @abstractmethod
    def create_task(self, task: dict) -> dict:
        """Create a task, return it with any backend-assigned fields."""

    @abstractmethod
    def update_task(self, task_id: str, updates: dict) -> dict | None:
        """Update a task, return updated task or None if not found."""

    @abstractmethod
    def add_note(self, task_id: str, note: str) -> bool:
        """Add a note/comment to a task."""


# ── Local Backend ──────────────────────────────────────────────────

class LocalBackend(Backend):
    def __init__(self, config: dict):
        self.path = config.get("file", "taskboard.json")

    def load(self) -> dict:
        p = Path(self.path)
        if not p.exists():
            return {"tasks": [], "meta": {"project": "unnamed", "prefix": "TASK", "nextId": 1}}
        with open(p) as f:
            return json.load(f)

    def save(self, board: dict):
        with open(self.path, "w") as f:
            json.dump(board, f, indent=2, ensure_ascii=False)

    def create_task(self, task: dict) -> dict:
        # ID assignment handled by caller
        return task

    def update_task(self, task_id: str, updates: dict) -> dict | None:
        # Handled inline by caller for local
        return updates

    def add_note(self, task_id: str, note: str) -> bool:
        return True


# ── GitHub Backend ─────────────────────────────────────────────────

class GitHubBackend(Backend):
    """Sync tasks with GitHub Issues. Local JSON is the cache."""

    def __init__(self, config: dict):
        self.repo = config["repo"]  # "owner/repo"
        self.token = os.environ.get(config.get("token_env", "GITHUB_TOKEN"), "")
        self.label_map = config.get("label_mapping", {})
        self.assignee_map = config.get("assignee_mapping", {})
        self.cache_file = config.get("cache_file", "taskboard.json")
        if not self.token:
            print(f"⚠️  {config.get('token_env', 'GITHUB_TOKEN')} not set, GitHub sync disabled")

    def _api(self, method: str, endpoint: str, data: dict = None) -> dict | list:
        url = f"https://api.github.com/repos/{self.repo}/{endpoint}"
        body = json.dumps(data).encode() if data else None
        req = Request(url, data=body, method=method)
        req.add_header("Authorization", f"token {self.token}")
        req.add_header("Accept", "application/vnd.github.v3+json")
        if body:
            req.add_header("Content-Type", "application/json")
        try:
            with urlopen(req) as resp:
                return json.loads(resp.read())
        except HTTPError as e:
            err = e.read().decode()
            print(f"❌ GitHub API error ({e.code}): {err[:200]}")
            return {}

    def _status_to_labels(self, status: str) -> list[str]:
        label = self.label_map.get(status, f"status:{status}")
        return [label] if label else []

    def _agent_to_gh_user(self, agent: str) -> str | None:
        return self.assignee_map.get(agent)

    def load(self) -> dict:
        p = Path(self.cache_file)
        if not p.exists():
            return {"tasks": [], "meta": {"project": "unnamed", "prefix": "TASK", "nextId": 1}}
        with open(p) as f:
            return json.load(f)

    def save(self, board: dict):
        with open(self.cache_file, "w") as f:
            json.dump(board, f, indent=2, ensure_ascii=False)

    def create_task(self, task: dict) -> dict:
        if not self.token:
            return task
        labels = self._status_to_labels(task.get("status", "backlog"))
        labels += task.get("tags", [])
        body = {
            "title": task["title"],
            "body": task.get("description", ""),
            "labels": labels,
        }
        gh_user = self._agent_to_gh_user(task.get("assignee", ""))
        if gh_user:
            body["assignees"] = [gh_user]
        result = self._api("POST", "issues", body)
        if result.get("number"):
            task["github_issue"] = result["number"]
            task["github_url"] = result["html_url"]
            print(f"  🔗 GitHub Issue #{result['number']}: {result['html_url']}")
        return task

    def update_task(self, task_id: str, updates: dict) -> dict | None:
        if not self.token:
            return updates
        # Find the task to get github_issue number
        board = self.load()
        task = next((t for t in board["tasks"] if t["id"] == task_id), None)
        if not task or not task.get("github_issue"):
            return updates
        issue_num = task["github_issue"]
        body = {}
        if "status" in updates:
            new_labels = self._status_to_labels(updates["status"])
            # Get current labels, remove old status labels, add new
            current = self._api("GET", f"issues/{issue_num}")
            old_labels = [l["name"] for l in current.get("labels", [])
                          if not l["name"].startswith("status:")]
            body["labels"] = old_labels + new_labels
            if updates["status"] == "done":
                body["state"] = "closed"
            elif updates["status"] != "done" and current.get("state") == "closed":
                body["state"] = "open"
        if "assignee" in updates:
            gh_user = self._agent_to_gh_user(updates["assignee"])
            if gh_user:
                body["assignees"] = [gh_user]
        if body:
            self._api("PATCH", f"issues/{issue_num}", body)
            print(f"  🔗 GitHub Issue #{issue_num} synced")
        return updates

    def add_note(self, task_id: str, note: str) -> bool:
        if not self.token:
            return True
        board = self.load()
        task = next((t for t in board["tasks"] if t["id"] == task_id), None)
        if not task or not task.get("github_issue"):
            return True
        self._api("POST", f"issues/{task['github_issue']}/comments", {"body": note})
        print(f"  🔗 Comment synced to GitHub Issue #{task['github_issue']}")
        return True


# ── Config & Factory ───────────────────────────────────────────────

def load_config(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {"backend": "local", "local": {"file": "taskboard.json"}}
    with open(p) as f:
        return json.load(f)


def create_backend(config: dict) -> Backend:
    backend_type = config.get("backend", "local")
    if backend_type == "github":
        return GitHubBackend(config.get("github", {}))
    return LocalBackend(config.get("local", {"file": "taskboard.json"}))


# ── Commands ───────────────────────────────────────────────────────

def cmd_create(args, board: dict, backend: Backend):
    meta = board["meta"]
    task_id = f"{meta['prefix']}-{meta['nextId']:03d}"
    meta["nextId"] += 1

    task = {
        "id": task_id,
        "title": args.title,
        "description": args.description or "",
        "status": "backlog",
        "assignee": args.assignee or None,
        "priority": args.priority or "medium",
        "dependencies": args.deps.split(",") if args.deps else [],
        "tags": args.tags.split(",") if args.tags else [],
        "created": now_iso(),
        "updated": now_iso(),
        "adr": args.adr or None,
        "notes": [],
    }
    task = backend.create_task(task)
    board["tasks"].append(task)
    print(f"✅ Created {task_id}: {args.title}")
    return board


def cmd_list(args, board: dict, backend: Backend):
    tasks = board["tasks"]
    if args.status:
        tasks = [t for t in tasks if t["status"] == args.status]
    if args.assignee:
        tasks = [t for t in tasks if t.get("assignee") == args.assignee]
    if args.priority:
        tasks = [t for t in tasks if t.get("priority") == args.priority]

    if not tasks:
        print("No tasks found.")
        return board

    for t in tasks:
        emoji = STATUS_EMOJI.get(t["status"], "❓")
        pri = f" [{t.get('priority', 'medium')}]" if t.get("priority") != "medium" else ""
        assignee = f" ({t['assignee']})" if t.get("assignee") else ""
        gh = f" #{t['github_issue']}" if t.get("github_issue") else ""
        print(f"  {emoji} {t['id']}{pri} {t['title']}{assignee}{gh}")
    return board


def cmd_update(args, board: dict, backend: Backend):
    for t in board["tasks"]:
        if t["id"] == args.task_id:
            updates = {}
            if args.status:
                if args.status not in STATUSES:
                    print(f"❌ Invalid status. Choose from: {', '.join(STATUSES)}")
                    return board
                t["status"] = args.status
                updates["status"] = args.status
            if args.assignee:
                t["assignee"] = args.assignee
                updates["assignee"] = args.assignee
            if args.priority:
                t["priority"] = args.priority
                updates["priority"] = args.priority
            if args.note:
                t["notes"].append({"text": args.note, "at": now_iso()})
                backend.add_note(args.task_id, args.note)
            t["updated"] = now_iso()
            backend.update_task(args.task_id, updates)
            print(f"✅ Updated {args.task_id}")
            return board
    print(f"❌ Task {args.task_id} not found")
    return board


def cmd_assign(args, board: dict, backend: Backend):
    for t in board["tasks"]:
        if t["id"] == args.task_id:
            t["assignee"] = args.to
            t["updated"] = now_iso()
            backend.update_task(args.task_id, {"assignee": args.to})
            print(f"✅ Assigned {args.task_id} → {args.to}")
            return board
    print(f"❌ Task {args.task_id} not found")
    return board


def cmd_note(args, board: dict, backend: Backend):
    for t in board["tasks"]:
        if t["id"] == args.task_id:
            t["notes"].append({"text": args.text, "at": now_iso()})
            t["updated"] = now_iso()
            backend.add_note(args.task_id, args.text)
            print(f"✅ Note added to {args.task_id}")
            return board
    print(f"❌ Task {args.task_id} not found")
    return board


def cmd_show(args, board: dict, backend: Backend):
    for t in board["tasks"]:
        if t["id"] == args.task_id:
            print(f"{'─' * 40}")
            print(f"  ID:       {t['id']}")
            print(f"  Title:    {t['title']}")
            print(f"  Status:   {t['status']}")
            print(f"  Priority: {t.get('priority', 'medium')}")
            print(f"  Assignee: {t.get('assignee') or 'unassigned'}")
            if t.get("description"):
                print(f"  Desc:     {t['description']}")
            if t.get("dependencies"):
                print(f"  Deps:     {', '.join(t['dependencies'])}")
            if t.get("tags"):
                print(f"  Tags:     {', '.join(t['tags'])}")
            if t.get("adr"):
                print(f"  ADR:      {t['adr']}")
            if t.get("github_issue"):
                print(f"  GitHub:   #{t['github_issue']} {t.get('github_url', '')}")
            print(f"  Created:  {t['created']}")
            print(f"  Updated:  {t['updated']}")
            if t.get("notes"):
                print(f"  Notes:")
                for n in t["notes"]:
                    print(f"    [{n['at']}] {n['text']}")
            print(f"{'─' * 40}")
            return board
    print(f"❌ Task {args.task_id} not found")
    return board


def cmd_summary(args, board: dict, backend: Backend):
    tasks = board["tasks"]
    by_status = {}
    for t in tasks:
        by_status.setdefault(t["status"], []).append(t)

    project = board["meta"].get("project", "unnamed")
    print(f"📋 Project Board: {project}")
    print("━" * 30)
    for status in STATUSES:
        items = by_status.get(status, [])
        if items or status in ("backlog", "in-progress", "review", "done"):
            print(f"{STATUS_EMOJI[status]} {status.title()}: {len(items)} tasks")

    high = [t for t in tasks if t.get("priority") in ("high", "critical")
            and t["status"] not in ("done", "rejected")]
    if high:
        print(f"\n🔥 High Priority:")
        for t in high:
            assignee = f" ({t['assignee']})" if t.get("assignee") else ""
            print(f"  {t['id']} [{t['status']}] {t['title']}{assignee}")

    blocked = by_status.get("blocked", [])
    if blocked:
        print(f"\n🚫 Blocked:")
        for t in blocked:
            last_note = t["notes"][-1]["text"] if t.get("notes") else "no reason given"
            print(f"  {t['id']} {t['title']} — {last_note}")
    return board


def cmd_init(args, board: dict, backend: Backend):
    board["meta"]["project"] = args.project
    board["meta"]["prefix"] = args.prefix or args.project.upper()[:4]
    print(f"✅ Initialized board: {args.project} (prefix: {board['meta']['prefix']})")
    return board


def cmd_config_init(args, board: dict, backend: Backend):
    """Generate a starter config file."""
    config = {
        "backend": args.backend,
        "local": {"file": "taskboard.json"},
    }
    if args.backend == "github":
        config["github"] = {
            "repo": args.repo or "owner/repo",
            "token_env": "GITHUB_TOKEN",
            "cache_file": "taskboard.json",
            "label_mapping": {
                "backlog": "status:backlog",
                "in-progress": "status:in-progress",
                "review": "status:review",
                "done": "status:done",
                "blocked": "status:blocked",
            },
            "assignee_mapping": {},
        }
    path = args.output or DEFAULT_CONFIG
    with open(path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"✅ Config written to {path}")
    if args.backend == "github":
        print(f"   Edit 'repo', 'assignee_mapping', and set ${config['github']['token_env']}")
    return board


# ── Main ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Taskboard CLI (pluggable backends)")
    parser.add_argument("--config", default=DEFAULT_CONFIG, help="Config file path")
    sub = parser.add_subparsers(dest="command", required=True)

    # config-init
    p_cfg = sub.add_parser("config-init", help="Generate a config file")
    p_cfg.add_argument("--backend", choices=["local", "github"], default="local")
    p_cfg.add_argument("--repo", help="GitHub repo (owner/repo)")
    p_cfg.add_argument("--output", help="Output config file path")

    # init
    p_init = sub.add_parser("init", help="Initialize a new board")
    p_init.add_argument("project", help="Project name")
    p_init.add_argument("--prefix", help="Task ID prefix")

    # create
    p_create = sub.add_parser("create", help="Create a task")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--description")
    p_create.add_argument("--assignee")
    p_create.add_argument("--priority", choices=PRIORITIES, default="medium")
    p_create.add_argument("--deps", help="Comma-separated dependency task IDs")
    p_create.add_argument("--tags", help="Comma-separated tags")
    p_create.add_argument("--adr", help="Related ADR")

    # list
    p_list = sub.add_parser("list", help="List tasks")
    p_list.add_argument("--status", choices=STATUSES)
    p_list.add_argument("--assignee")
    p_list.add_argument("--priority", choices=PRIORITIES)

    # update
    p_update = sub.add_parser("update", help="Update a task")
    p_update.add_argument("task_id")
    p_update.add_argument("--status", choices=STATUSES)
    p_update.add_argument("--assignee")
    p_update.add_argument("--priority", choices=PRIORITIES)
    p_update.add_argument("--note")

    # assign
    p_assign = sub.add_parser("assign", help="Assign a task")
    p_assign.add_argument("task_id")
    p_assign.add_argument("--to", required=True)

    # note
    p_note = sub.add_parser("note", help="Add a note")
    p_note.add_argument("task_id")
    p_note.add_argument("text")

    # show
    p_show = sub.add_parser("show", help="Show task detail")
    p_show.add_argument("task_id")

    # summary
    sub.add_parser("summary", help="Board summary")

    args = parser.parse_args()

    # Config-init doesn't need a backend
    if args.command == "config-init":
        cmd_config_init(args, {}, None)
        return

    config = load_config(args.config)
    backend = create_backend(config)
    board = backend.load()

    commands = {
        "init": cmd_init, "create": cmd_create, "list": cmd_list,
        "update": cmd_update, "assign": cmd_assign, "note": cmd_note,
        "show": cmd_show, "summary": cmd_summary,
    }
    board = commands[args.command](args, board, backend)

    if args.command not in ("list", "show", "summary"):
        backend.save(board)


if __name__ == "__main__":
    main()
