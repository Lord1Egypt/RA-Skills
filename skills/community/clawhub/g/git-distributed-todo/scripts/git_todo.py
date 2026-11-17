#!/usr/bin/env python3
"""Git-backed distributed Todo coordination for independent AI agents.

The repository is the coordination plane. Each task has its own JSON file and
notification receipts live separately, reducing cross-host merge conflicts.
No third-party Python packages are required.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import socket
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any


VALID_AGENT = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
VALID_STATES = {"todo", "doing", "done", "cancelled"}
VALID_PRIORITIES = {"low", "normal", "high", "urgent"}


class TodoError(RuntimeError):
    pass


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_utc(value: dt.datetime | None = None) -> str:
    value = value or now_utc()
    return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> dt.datetime:
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(raw)
    except ValueError as exc:
        raise TodoError(f"invalid ISO-8601 timestamp: {value}") from exc
    if parsed.tzinfo is None:
        raise TodoError("timestamp must include a UTC offset or Z suffix")
    return parsed.astimezone(dt.timezone.utc)


def output(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or "git command failed"
        raise TodoError(message)
    return proc


def repo_path(value: str | None) -> Path:
    raw = (
        value
        or os.environ.get("AGENT_TODO_REPO")
        or os.environ.get("HERMES_TODO_REPO")
    )
    if not raw:
        raise TodoError("set AGENT_TODO_REPO or pass --repo")
    repo = Path(raw).expanduser().resolve()
    if not repo.is_dir():
        raise TodoError(f"repository directory does not exist: {repo}")
    if git(repo, "rev-parse", "--is-inside-work-tree", check=False).returncode != 0:
        raise TodoError(f"not a Git working tree: {repo}")
    return repo


def agent_name(value: str | None, repo: Path | None = None) -> str:
    name = (
        value
        or os.environ.get("AGENT_TODO_ID")
        or os.environ.get("HERMES_TODO_AGENT")
        or ""
    ).strip().lower()
    if not name and repo is not None:
        schema = repo / ".git-distributed-todo.json"
        if schema.is_file():
            name = str(read_json(schema).get("default_agent", "")).strip().lower()
    if not VALID_AGENT.fullmatch(name):
        raise TodoError(
            "set AGENT_TODO_ID or pass --agent (or run `setup` to record a default agent id)"
        )
    return name


def clean_managed_dirs(repo: Path) -> None:
    for name in ("tasks", "receipts"):
        (repo / name).mkdir(parents=True, exist_ok=True)


def current_branch(repo: Path) -> str:
    branch = git(repo, "branch", "--show-current").stdout.strip()
    if not branch:
        raise TodoError("detached HEAD is not supported; check out a branch first")
    return branch


def ensure_no_uncommitted(repo: Path) -> None:
    dirty = git(repo, "status", "--porcelain").stdout.strip()
    if dirty:
        raise TodoError(
            "working tree has uncommitted changes; commit/stash them before distributed-todo sync"
        )


def sync(repo: Path) -> None:
    ensure_no_uncommitted(repo)
    branch = current_branch(repo)
    remote = git(repo, "remote", "get-url", "origin", check=False)
    if remote.returncode != 0:
        raise TodoError("no git remote 'origin' configured; run `setup` to configure one")
    fetch = git(repo, "fetch", "origin", branch, check=False)
    if fetch.returncode != 0:
        detail = fetch.stderr.strip()
        hint = (
            "the branch was never pushed to origin; run `setup` or `git push -u origin main` first"
            if "couldn't find remote ref" in detail
            else "check the remote URL (`git remote -v`) and your network/credentials"
        )
        raise TodoError(f"cannot fetch from origin: {detail}\nhint: {hint}")
    rebased = git(repo, "rebase", f"origin/{branch}", check=False)
    if rebased.returncode != 0:
        git(repo, "rebase", "--abort", check=False)
        raise TodoError(
            "Git conflict while synchronizing. Rebase was aborted; resolve manually and retry."
        )


def commit_and_push(repo: Path, paths: list[Path], message: str) -> None:
    relpaths = [str(path.relative_to(repo)) for path in paths]
    git(repo, "add", "--", *relpaths)
    staged = git(repo, "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        return
    git(repo, "commit", "-m", message)
    branch = current_branch(repo)
    for attempt in range(3):
        pushed = git(repo, "push", "-u", "origin", branch, check=False)
        if pushed.returncode == 0:
            return
        fetch = git(repo, "fetch", "origin", branch, check=False)
        if fetch.returncode != 0:
            # A failed fetch means the remote itself is unreachable or the
            # branch never existed there — this is NOT a push race, so report
            # the real reason instead of a misleading "conflict".
            raise TodoError(
                f"cannot publish to origin: {pushed.stderr.strip()}\n"
                f"fetch after failed push also failed: {fetch.stderr.strip()}\n"
                "hint: check the remote URL (`git remote -v`) and your network/credentials"
            )
        rebased = git(repo, "rebase", f"origin/{branch}", check=False)
        if rebased.returncode != 0:
            git(repo, "rebase", "--abort", check=False)
            raise TodoError(
                "Git conflict while synchronizing. Rebase was aborted; resolve manually and retry."
            )
        if attempt == 2:
            message_text = pushed.stderr.strip() or pushed.stdout.strip()
            raise TodoError(f"push failed after 3 attempts: {message_text}")


def ensure_origin_ref(repo: Path) -> None:
    """Make sure origin exists and the current branch is published there.

    Fixes the trap where bootstrap reports success while origin has no branch
    ref yet, leaving every later sync/commit failing with
    "couldn't find remote ref main".
    """
    branch = current_branch(repo)
    remote = git(repo, "remote", "get-url", "origin", check=False)
    if remote.returncode != 0:
        raise TodoError(
            "no git remote 'origin' configured; run `setup` or `git remote add origin <url>`"
        )
    ls = git(repo, "ls-remote", "--exit-code", "origin", f"refs/heads/{branch}", check=False)
    if ls.returncode == 0:
        return
    head = git(repo, "rev-parse", "--verify", "-q", "HEAD", check=False)
    if head.returncode != 0:
        raise TodoError("no commits yet; create the initial commit before bootstrap")
    pushed = git(repo, "push", "-u", "origin", branch, check=False)
    if pushed.returncode != 0:
        raise TodoError(
            f"cannot publish initial commit to origin: {pushed.stderr.strip()}\n"
            "hint: fix the remote (`git remote -v`) then push manually: git push -u origin main"
        )


def read_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise TodoError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise TodoError(f"expected JSON object in {path}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    temp.replace(path)


def task_path(repo: Path, task_id: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{32}", task_id):
        raise TodoError("invalid task id")
    path = repo / "tasks" / f"{task_id}.json"
    if not path.is_file():
        raise TodoError(f"task not found: {task_id}")
    return path


def notification_key(task: dict[str, Any]) -> str:
    fields = [
        str(task.get("title", "")),
        str(task.get("executor", "")),
        str(task.get("priority", "normal")),
        str(task.get("due_at", "")),
    ]
    return "\x1f".join(fields)


def maybe_sync(repo: Path, no_sync: bool) -> None:
    clean_managed_dirs(repo)
    if not no_sync:
        sync(repo)


def cmd_bootstrap(args: argparse.Namespace) -> None:
    repo = repo_path(args.repo)
    ensure_no_uncommitted(repo)
    clean_managed_dirs(repo)
    schema = repo / ".git-distributed-todo.json"
    if not schema.exists():
        write_json(schema, {"schema": 1, "format": "git-distributed-todo"})
    keepers: list[Path] = [schema]
    for directory in (repo / "tasks", repo / "receipts"):
        keeper = directory / ".gitkeep"
        keeper.touch(exist_ok=True)
        keepers.append(keeper)
    commit_and_push(repo, keepers, "Initialize distributed Todo repository")
    ensure_origin_ref(repo)
    output({"ok": True, "repo": str(repo), "schema": 1})


def init_repo(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q", check=False)
    branch = git(repo, "branch", "--show-current", check=False).stdout.strip()
    if branch != "main":
        has_main = git(repo, "rev-parse", "--verify", "-q", "main", check=False).returncode == 0
        if not has_main:
            git(repo, "checkout", "-q", "-b", "main", check=False)


def init_bare(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        ["git", "init", "--bare", "-q", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise TodoError(proc.stderr.strip() or "git init --bare failed")
    # Point HEAD at main so a later clone checks out the right branch
    # instead of warning "remote HEAD refers to nonexistent ref".
    head = subprocess.run(
        ["git", "--git-dir", str(path), "symbolic-ref", "HEAD", "refs/heads/main"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if head.returncode != 0:
        raise TodoError(head.stderr.strip() or "cannot set bare repository HEAD")


def default_agent_id() -> str:
    host = (socket.gethostname() or "agent").strip().lower()
    ident = re.sub(r"[^a-z0-9._-]", "-", host)[:64].strip(".-")
    if not VALID_AGENT.fullmatch(ident):
        ident = "agent"
    return ident


def prompt(label: str, default: str | None = None, yes: bool = False) -> str | None:
    if yes:
        return default
    if not sys.stdin.isatty():
        if default is not None:
            return default
        raise TodoError(
            "interactive input unavailable (non-TTY); pass the value explicitly "
            "(--repo/--remote/--agent) or --yes to accept defaults"
        )
    suffix = f" [{default}]" if default is not None else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def cmd_setup(args: argparse.Namespace) -> None:
    """One-shot init wizard: repo location, remote URL, agent id."""
    # 1. Repo location
    if args.repo:
        repo_raw = args.repo
    elif os.environ.get("AGENT_TODO_REPO"):
        repo_raw = os.environ["AGENT_TODO_REPO"]
    else:
        repo_raw = prompt("Todo repo location", "~/shared-todo", args.yes)
    if not repo_raw:
        raise TodoError("no repo location given; pass --repo")
    repo = Path(repo_raw).expanduser().resolve()

    # 2. Agent id — resolve before any writes so invalid input fails fast
    if args.agent:
        agent_raw = args.agent
    elif os.environ.get("AGENT_TODO_ID"):
        agent_raw = os.environ["AGENT_TODO_ID"]
    else:
        agent_raw = prompt("Agent ID", default_agent_id(), args.yes) or default_agent_id()
    agent = agent_raw.strip().lower()
    if not VALID_AGENT.fullmatch(agent):
        raise TodoError(f"invalid agent id: {agent!r} (must match {VALID_AGENT.pattern})")

    # 3. Prepare the working tree
    created = False
    if repo.is_dir():
        if git(repo, "rev-parse", "--is-inside-work-tree", check=False).returncode != 0:
            raise TodoError(f"exists but is not a Git working tree: {repo}")
        dirty = git(repo, "status", "--porcelain").stdout.strip()
        if dirty:
            raise TodoError(
                "working tree has uncommitted changes; commit or stash them before setup:\n" + dirty
            )
    else:
        if not sys.stdin.isatty() and not args.yes and args.repo is None:
            raise TodoError(
                "non-interactive: the repo does not exist yet; pass --repo (and --yes) explicitly"
            )
        init_repo(repo)
        created = True

    # 4. Remote — explicit URL wins, then existing origin, then local bare
    existing = git(repo, "remote", "get-url", "origin", check=False)
    if args.remote:
        if existing.returncode == 0:
            git(repo, "remote", "set-url", "origin", args.remote)
        else:
            git(repo, "remote", "add", "origin", args.remote)
        remote_url = args.remote
        local_bare = False
    elif existing.returncode == 0:
        remote_url = existing.stdout.strip()
        local_bare = False
    else:
        ask_remote = sys.stdin.isatty() and not args.yes
        remote_url = prompt(
            "Remote URL (blank = local bare repo for single-host)", None, args.yes
        ) if ask_remote else None
        if not remote_url:
            bare = repo.parent / (repo.name + ".git")
            init_bare(bare)
            git(repo, "remote", "add", "origin", str(bare))
            remote_url = str(bare)
            local_bare = True
        else:
            git(repo, "remote", "add", "origin", remote_url)
            local_bare = False

    # 5. Bootstrap files + record the default agent id
    clean_managed_dirs(repo)
    schema = repo / ".git-distributed-todo.json"
    data = read_json(schema) if schema.exists() else {"schema": 1, "format": "git-distributed-todo"}
    data["default_agent"] = agent
    write_json(schema, data)
    keepers: list[Path] = [schema]
    for directory in (repo / "tasks", repo / "receipts"):
        keeper = directory / ".gitkeep"
        keeper.touch(exist_ok=True)
        keepers.append(keeper)
    commit_and_push(repo, keepers, "Initialize distributed Todo repository")
    ensure_origin_ref(repo)

    output(
        {
            "ok": True,
            "repo": str(repo),
            "remote": remote_url,
            "agent_id": agent,
            "local_bare": local_bare,
            "created": created,
            "next_steps": [
                f'export AGENT_TODO_REPO="{repo}"',
                f'export AGENT_TODO_ID="{agent}"',
                "Hermes: put the two exports above in ~/.hermes/.env (loaded at startup); "
                "other shells: append them to your shell profile",
                f"Other hosts: git clone {remote_url} and run "
                f"setup --repo <clone-path> --agent <their-id>",
            ],
        }
    )


def cmd_sync(args: argparse.Namespace) -> None:
    repo = repo_path(args.repo)
    clean_managed_dirs(repo)
    sync(repo)
    output({"ok": True, "repo": str(repo), "head": git(repo, "rev-parse", "HEAD").stdout.strip()})


def cmd_create(args: argparse.Namespace) -> None:
    repo = repo_path(args.repo)
    creator = agent_name(args.agent, repo)
    executor = (args.executor or creator).strip().lower()
    if not VALID_AGENT.fullmatch(executor):
        raise TodoError("executor must be a stable lowercase agent id")
    if args.priority not in VALID_PRIORITIES:
        raise TodoError(f"invalid priority: {args.priority}")
    due_at = iso_utc(parse_time(args.due_at)) if args.due_at else None
    maybe_sync(repo, args.no_sync)
    task_id = uuid.uuid4().hex
    timestamp = iso_utc()
    task = {
        "id": task_id,
        "title": args.title.strip(),
        "description": (args.description or "").strip(),
        "created_by": creator,
        "executor": executor,
        "status": "todo",
        "priority": args.priority,
        "created_at": timestamp,
        "updated_at": timestamp,
        "due_at": due_at,
        "notify": not args.no_notify,
        "result": None,
    }
    if not task["title"]:
        raise TodoError("title cannot be empty")
    path = repo / "tasks" / f"{task_id}.json"
    write_json(path, task)
    commit_and_push(repo, [path], f"Todo create {task_id}: {task['title'][:60]}")
    output({"ok": True, "task": task})


def load_tasks(repo: Path) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for path in sorted((repo / "tasks").glob("*.json")):
        task = read_json(path)
        if task.get("id"):
            tasks.append(task)
    return tasks


def cmd_list(args: argparse.Namespace) -> None:
    repo = repo_path(args.repo)
    maybe_sync(repo, args.no_sync)
    wanted_states = None
    if args.status:
        wanted_states = {item.strip() for item in args.status.split(",") if item.strip()}
        unknown = wanted_states - VALID_STATES
        if unknown:
            raise TodoError(f"unknown states: {', '.join(sorted(unknown))}")
    tasks = load_tasks(repo)
    if args.executor:
        tasks = [task for task in tasks if task.get("executor") == args.executor]
    if wanted_states is not None:
        tasks = [task for task in tasks if task.get("status") in wanted_states]
    output({"ok": True, "count": len(tasks), "tasks": tasks})


def lifecycle_write(
    repo: Path,
    task_id: str,
    actor: str,
    new_state: str,
    result: str | None = None,
) -> dict[str, Any]:
    path = task_path(repo, task_id)
    task = read_json(path)
    if task.get("executor") != actor:
        raise TodoError(
            f"task belongs to executor {task.get('executor')!r}; current agent is {actor!r}"
        )
    old_state = task.get("status")
    allowed = {
        "todo": {"doing", "done", "cancelled"},
        "doing": {"done", "cancelled"},
        "done": set(),
        "cancelled": set(),
    }
    if new_state not in allowed.get(str(old_state), set()):
        raise TodoError(f"invalid task transition: {old_state} -> {new_state}")
    task["status"] = new_state
    task["updated_at"] = iso_utc()
    if new_state == "done":
        task["completed_at"] = task["updated_at"]
        task["result"] = (result or "").strip() or None
    if new_state == "cancelled":
        task["cancelled_at"] = task["updated_at"]
    write_json(path, task)
    return task


def cmd_lifecycle(args: argparse.Namespace, state: str) -> None:
    repo = repo_path(args.repo)
    actor = agent_name(args.agent, repo)
    maybe_sync(repo, args.no_sync)
    result = getattr(args, "result", None)
    task = lifecycle_write(repo, args.task_id, actor, state, result=result)
    path = repo / "tasks" / f"{args.task_id}.json"
    commit_and_push(repo, [path], f"Todo {state} {args.task_id}")
    output({"ok": True, "task": task})


def cmd_due(args: argparse.Namespace) -> None:
    repo = repo_path(args.repo)
    notifier = agent_name(args.notifier, repo)
    maybe_sync(repo, args.no_sync)
    cutoff = parse_time(args.at) if args.at else now_utc()
    due: list[dict[str, Any]] = []
    for task in load_tasks(repo):
        if task.get("status") not in {"todo", "doing"} or not task.get("notify", True):
            continue
        raw_due = task.get("due_at")
        if not raw_due or parse_time(str(raw_due)) > cutoff:
            continue
        receipt_path = repo / "receipts" / notifier / f"{task['id']}.json"
        if receipt_path.is_file():
            receipt = read_json(receipt_path)
            if receipt.get("notification_key") == notification_key(task):
                continue
        due.append(task)
    order = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
    due.sort(key=lambda task: (order.get(str(task.get("priority")), 9), str(task.get("due_at"))))
    output({"ok": True, "notifier": notifier, "count": len(due), "tasks": due})


def cmd_mark_notified(args: argparse.Namespace) -> None:
    repo = repo_path(args.repo)
    notifier = agent_name(args.notifier)
    maybe_sync(repo, args.no_sync)
    receipts: list[dict[str, Any]] = []
    paths: list[Path] = []
    for task_id in args.task_ids:
        task = read_json(task_path(repo, task_id))
        receipt = {
            "task_id": task_id,
            "notifier": notifier,
            "notified_at": iso_utc(),
            "notification_key": notification_key(task),
        }
        path = repo / "receipts" / notifier / f"{task_id}.json"
        write_json(path, receipt)
        receipts.append(receipt)
        paths.append(path)
    commit_and_push(repo, paths, f"Todo notified {len(receipts)} task(s) by {notifier}")
    output({"ok": True, "count": len(receipts), "receipts": receipts})


def common_repo(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--repo", help="Todo repository; defaults to AGENT_TODO_REPO")


def common_agent(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--agent", help="Current agent id; defaults to AGENT_TODO_ID")


def common_no_sync(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--no-sync", action="store_true", help="Use cached local state without fetching")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("bootstrap", help="Initialize task directories in an existing Git repository")
    common_repo(p)
    p.set_defaults(func=cmd_bootstrap)

    p = sub.add_parser(
        "setup",
        help="One-shot init wizard: repo location, remote URL, agent id (interactive or flags)",
    )
    common_repo(p)
    p.add_argument(
        "--remote",
        help="Git remote URL; blank/omitted → local bare repo next to the working tree (single-host mode)",
    )
    p.add_argument(
        "--agent", help="Agent id; defaults to AGENT_TODO_ID or a hostname-derived id"
    )
    p.add_argument("--yes", action="store_true", help="Non-interactive: use defaults, never prompt")
    p.set_defaults(func=cmd_setup)

    p = sub.add_parser("sync", help="Fetch and rebase the shared repository")
    common_repo(p)
    p.set_defaults(func=cmd_sync)

    p = sub.add_parser("create", help="Create and publish a Todo")
    common_repo(p)
    common_agent(p)
    common_no_sync(p)
    p.add_argument("--title", required=True)
    p.add_argument("--description")
    p.add_argument("--executor")
    p.add_argument("--due-at", help="ISO-8601 timestamp with timezone")
    p.add_argument("--priority", choices=sorted(VALID_PRIORITIES), default="normal")
    p.add_argument("--no-notify", action="store_true")
    p.set_defaults(func=cmd_create)

    p = sub.add_parser("list", help="List Todo records")
    common_repo(p)
    common_no_sync(p)
    p.add_argument("--executor")
    p.add_argument("--status", help="Comma-separated states")
    p.set_defaults(func=cmd_list)

    for command, help_text, state in (
        ("start", "Move an assigned Todo from todo to doing", "doing"),
        ("cancel", "Cancel an assigned Todo", "cancelled"),
    ):
        p = sub.add_parser(command, help=help_text)
        common_repo(p)
        common_agent(p)
        common_no_sync(p)
        p.add_argument("task_id")
        p.set_defaults(func=lambda args, s=state: cmd_lifecycle(args, s))

    p = sub.add_parser("complete", help="Complete an assigned Todo")
    common_repo(p)
    common_agent(p)
    common_no_sync(p)
    p.add_argument("task_id")
    p.add_argument("--result")
    p.set_defaults(func=lambda args: cmd_lifecycle(args, "done"))

    p = sub.add_parser("due", help="List due and not-yet-notified Todo records")
    common_repo(p)
    common_no_sync(p)
    p.add_argument("--notifier", required=True)
    p.add_argument("--at", help="ISO-8601 cutoff; defaults to now")
    p.set_defaults(func=cmd_due)

    p = sub.add_parser("mark-notified", help="Record successful delivery without modifying the task")
    common_repo(p)
    common_no_sync(p)
    p.add_argument("task_ids", nargs="+")
    p.add_argument("--notifier", required=True)
    p.set_defaults(func=cmd_mark_notified)

    return parser


def main() -> int:
    try:
        args = build_parser().parse_args()
        args.func(args)
        return 0
    except TodoError as exc:
        output({"ok": False, "error": str(exc)})
        return 2
    except FileNotFoundError as exc:
        output({"ok": False, "error": f"required executable not found: {exc.filename}"})
        return 2


if __name__ == "__main__":
    sys.exit(main())
