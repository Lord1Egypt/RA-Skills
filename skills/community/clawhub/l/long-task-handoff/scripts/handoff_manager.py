#!/usr/bin/env python3
"""Create, update, find, recover, suggest, and validate long-task handoffs.

This script holds the deterministic parts of the long-task-handoff skill so
agent behavior is consistent across models and runtimes.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from check_handoff import extract_sections, read_text, validate_file


DEFAULT_AGENT = "unknown"
HANDOFF_DIR = "handoffs"
MAX_FIELD_CHARS = 1200


def now_local() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M local")


def slugify(value: str) -> str:
    cleaned = []
    for char in value.lower():
        if char.isalnum():
            cleaned.append(char)
        elif char in {" ", "-", "_"}:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug[:48] or "task"


def load_payload(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    if path == "-":
        return json.load(sys.stdin)
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sanitize_text(value: Any) -> str:
    text = str(value).replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("```", "'''")
    text = " / ".join(line.strip() for line in text.splitlines() if line.strip())
    if len(text) > MAX_FIELD_CHARS:
        text = text[:MAX_FIELD_CHARS].rstrip() + " ... [truncated]"
    return text


def field(value: Any, fallback: str = "") -> str:
    if value is None:
        return fallback
    text = sanitize_text(value)
    return text if text else fallback


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [sanitize_text(item) for item in value if sanitize_text(item)]
    if isinstance(value, str) and value.strip():
        return [sanitize_text(value)]
    return []


def merge_cli_payload(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_payload(getattr(args, "input_json", None))
    for key, attr in [
        ("completed_this_turn", "completed"),
        ("current_test_results", "test_result"),
        ("key_files", "key_file"),
        ("unfinished_items", "unfinished"),
        ("next_actions", "next_action"),
        ("known_risks", "risk"),
        ("do_not_do", "do_not_do"),
        ("files_and_artifacts", "artifact"),
        ("commands_and_verification", "command"),
        ("decisions_and_constraints", "decision"),
        ("fact_sources", "source"),
    ]:
        values = as_list(getattr(args, attr, None))
        if values:
            payload[key] = values
    if getattr(args, "goal", None):
        payload["current_goal"] = args.goal
    return payload


def run_git(workspace: Path, *parts: str) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(workspace), *parts],
            text=True,
            capture_output=True,
            timeout=10,
        )
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def git_state(workspace: Path) -> dict[str, str]:
    branch = run_git(workspace, "rev-parse", "--abbrev-ref", "HEAD")
    commit = run_git(workspace, "rev-parse", "--short", "HEAD")
    status = run_git(workspace, "status", "--short")
    if branch is None or commit is None:
        return {
            "branch": "not a git repo or unknown",
            "commit": "unknown",
            "working_tree": "unknown",
            "source": "git unavailable",
        }
    working_tree = "clean" if not status else "dirty: " + "; ".join(status.splitlines()[:12])
    return {
        "branch": branch,
        "commit": commit,
        "working_tree": working_tree,
        "source": "git rev-parse/status",
    }


def handoff_dir(workspace: Path) -> Path:
    return workspace / HANDOFF_DIR


def active_pointer(workspace: Path) -> Path:
    return handoff_dir(workspace) / "ACTIVE.md"


def parse_latest_from_active(active: Path) -> Path | None:
    if not active.exists():
        return None
    for line in read_text(active).splitlines():
        if line.lower().startswith("latest:"):
            value = line.split(":", 1)[1].strip()
            candidate = Path(value)
            if not candidate.is_absolute():
                candidate = active.parent / candidate
            if candidate.exists():
                return candidate
    return None


def find_handoff(workspace: Path) -> Path | None:
    active_target = parse_latest_from_active(active_pointer(workspace))
    if active_target:
        return active_target
    candidates = sorted(handoff_dir(workspace).glob("session-handoff-*.md"))
    return candidates[-1] if candidates else None


def bullets(items: list[str], fallback: str = "none") -> list[str]:
    values = items or [fallback]
    return [f"- {sanitize_text(item)}" for item in values]


def numbered(items: list[str], fallback: str = "Verify workspace state and continue from the current goal.") -> list[str]:
    values = items or [fallback]
    return [f"{index}. {sanitize_text(item)}" for index, item in enumerate(values, start=1)]


def risk_lines(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [
            f"- High: {field(value.get('high'), 'none')}",
            f"- Medium: {field(value.get('medium'), 'none')}",
            f"- Low: {field(value.get('low'), 'none')}",
        ]
    values = as_list(value)
    if not values:
        return ["- High: none", "- Medium: none", "- Low: none"]
    return [f"- {item}" for item in values]


def section(title: str, lines: list[str]) -> list[str]:
    return [f"## {title}", "", *lines, ""]


def build_handoff_text(
    *,
    task: str,
    workspace: Path,
    agent: str,
    trigger: str,
    supersedes: str,
    authoritative: str,
    payload: dict[str, Any],
    delta: list[str],
) -> str:
    state = git_state(workspace)
    task = field(task, "Current task")
    agent = field(agent, DEFAULT_AGENT)
    trigger = field(trigger, "unknown")
    supersedes = field(supersedes, "none")
    authoritative = field(authoritative, "yes")
    current_goal = field(payload.get("current_goal"), f"Continue task: {task}.")
    key_files = as_list(payload.get("key_files"))
    artifacts = as_list(payload.get("files_and_artifacts")) or key_files
    fact_sources = as_list(payload.get("fact_sources")) or [
        f"Branch/commit state: {state['source']}",
        "Test results: provided by current agent or marked not run",
        "File state: git status and agent inspection",
        "User constraints: current conversation and repo instructions",
    ]

    lines: list[str] = [
        f"# Session Handoff: {task}",
        "",
        f"Updated: {now_local()}",
        f"Supersedes: {supersedes}",
        f"Authoritative: {authoritative}",
        f"Workspace: {workspace}",
        f"Current agent: {agent}",
        f"Trigger: {trigger}",
        "",
        "## Restart Instruction",
        "",
        f"Continue this task by reading this handoff file first: {active_pointer(workspace)}.",
        'A short user prompt such as "continue this task" should be enough.',
        "",
    ]
    lines += section("Current Goal", [current_goal])
    lines += section(
        "Branch And Commit State",
        [
            f"- Current branch: {state['branch']}",
            f"- Current commit: {state['commit']}",
            f"- Working tree: {state['working_tree']}",
        ],
    )
    lines += section("Completed This Turn", bullets(as_list(payload.get("completed_this_turn"))))
    lines += section("Delta Since Last Update", bullets(delta))
    lines += section("Current Test Results", bullets(as_list(payload.get("current_test_results")), "not run or not recorded"))
    lines += section("Key Files", bullets(key_files, "none recorded"))
    lines += section(
        "Handoff Scope Boundary",
        bullets(
            [
                "This handoff contains only restart-critical state.",
                *as_list(payload.get("durable_docs")),
                *[f"Candidate repo doc update: {item}" for item in as_list(payload.get("candidate_repo_doc_updates"))],
            ]
        ),
    )
    lines += section("Current State", bullets(as_list(payload.get("current_state")), "current state not separately recorded"))
    lines += section("Unfinished Items", bullets(as_list(payload.get("unfinished_items")), "none recorded"))
    lines += section("Next Actions", numbered(as_list(payload.get("next_actions"))))
    lines += section("Files And Artifacts", bullets(artifacts, "none recorded"))
    lines += section("Commands And Verification", bullets(as_list(payload.get("commands_and_verification")), "not recorded"))
    lines += section("Fact Sources", bullets(fact_sources))
    lines += section("Decisions And Constraints", bullets(as_list(payload.get("decisions_and_constraints")), "none recorded"))
    lines += section("Blockers, Risks, And Open Questions", bullets(as_list(payload.get("blockers")), "none recorded"))
    lines += section("Known Risks", risk_lines(payload.get("known_risks")))
    lines += section("Do Not Redo", bullets(as_list(payload.get("do_not_redo")), "do not append stale mini-handoffs"))
    lines += section("Do Not Do", bullets(as_list(payload.get("do_not_do")), "do not include secrets, stale plans, or unverified guesses"))
    lines += section("Suggested Skills Or Tools", bullets(as_list(payload.get("suggested_skills")), "long-task-handoff"))
    lines += section(
        "Sensitive Information Handling",
        bullets(
            [
                "Secrets included in this handoff: none.",
                "Redactions made: none unless listed above.",
            ]
        ),
    )
    return "\n".join(lines).rstrip() + "\n"


def changed_sections(before: str, after: str) -> list[str]:
    old = extract_sections(before) if before else {}
    new = extract_sections(after)
    changed = [heading for heading, text in new.items() if old.get(heading) != text]
    return [heading for heading in changed if heading != "Delta Since Last Update"]


def write_active(workspace: Path, target: Path, task: str) -> None:
    active = active_pointer(workspace)
    active.parent.mkdir(parents=True, exist_ok=True)
    active.write_text(
        "\n".join(
            [
                "# Active Handoff",
                f"Updated: {now_local()}",
                f"Latest: {target.resolve()}",
                f"Task: {task}",
                f"Restart Instruction: Continue this task by reading {target.resolve()} first.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_handoff(args: argparse.Namespace, *, update: bool) -> int:
    workspace = Path(args.workspace).resolve()
    payload = merge_cli_payload(args)
    task = field(args.task or payload.get("task_name"), "Current task")
    trigger = field(args.event or ("context_compaction" if update else "manual_create"))
    agent = field(args.agent or payload.get("agent"), DEFAULT_AGENT)

    handoffs = handoff_dir(workspace)
    handoffs.mkdir(parents=True, exist_ok=True)

    previous = find_handoff(workspace)
    if update and previous:
        target = previous
        supersedes = payload.get("supersedes") or "previous revision of this file"
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        target = handoffs / f"session-handoff-{stamp}-{slugify(task)}.md"
        supersedes = payload.get("supersedes") or (str(previous.resolve()) if previous else "none")

    previous_text = read_text(target) if target.exists() else ""
    provisional = build_handoff_text(
        task=task,
        workspace=workspace,
        agent=agent,
        trigger=trigger,
        supersedes=supersedes,
        authoritative="yes, referenced by ACTIVE.md",
        payload=payload,
        delta=["pending"],
    )
    changed = changed_sections(previous_text, provisional)
    delta = as_list(payload.get("delta_since_last_update")) or [
        f"Updated sections: {', '.join(changed) if changed else 'metadata only'}",
        "Removed stale handoff content: replaced prior active snapshot; no append-only history preserved",
        "Conflicts resolved against previous handoff: none recorded",
    ]
    text = build_handoff_text(
        task=task,
        workspace=workspace,
        agent=agent,
        trigger=trigger,
        supersedes=supersedes,
        authoritative="yes, referenced by ACTIVE.md",
        payload=payload,
        delta=delta,
    )
    target.write_text(text, encoding="utf-8")
    write_active(workspace, target, task)

    errors = validate_file(target)
    result = {
        "path": str(target.resolve()),
        "active": str(active_pointer(workspace).resolve()),
        "valid": not errors,
        "errors": errors,
        "recommendation": restart_recommendation(args.compaction_count),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


def restart_recommendation(compaction_count: int | None) -> str:
    if compaction_count is None:
        return "continue"
    if compaction_count >= 4:
        return "restart_strongly_recommended"
    if compaction_count >= 3:
        return "restart_advisable"
    return "continue"


def cmd_find(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    found = find_handoff(workspace)
    result = {"path": str(found.resolve()) if found else None, "active": str(active_pointer(workspace).resolve())}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif found:
        print(found.resolve())
    return 0 if found else 1


def cmd_recover(args: argparse.Namespace) -> int:
    workspace = Path(args.workspace).resolve()
    found = find_handoff(workspace)
    if not found:
        print(json.dumps({"found": False, "path": None, "errors": ["No handoff found"]}, ensure_ascii=False, indent=2))
        return 1
    errors = validate_file(found)
    print(
        json.dumps(
            {
                "found": True,
                "path": str(found.resolve()),
                "valid": not errors,
                "errors": errors,
                "instruction": f"Read {found.resolve()} and continue from Next Actions after freshness checks.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if not errors else 1


def cmd_suggest(args: argparse.Namespace) -> int:
    result = {
        "compaction_count": args.compaction_count,
        "recommendation": restart_recommendation(args.compaction_count),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result["recommendation"])
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_file(Path(args.handoff))
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {args.handoff}")
        return 1
    print(f"PASS: {args.handoff}")
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace", default=".", help="Workspace root. Default: current directory")
    parser.add_argument("--task", help="Short task name")
    parser.add_argument("--goal", help="Current goal sentence")
    parser.add_argument("--agent", help="Current agent name")
    parser.add_argument("--event", help="Trigger event name")
    parser.add_argument("--compaction-count", type=int, help="Visible context compaction count")
    parser.add_argument("--input-json", help="JSON payload path, or '-' for stdin")
    parser.add_argument("--completed", action="append", help="Completed work item")
    parser.add_argument("--test-result", action="append", help="Current test result")
    parser.add_argument("--key-file", action="append", help="Key file entry")
    parser.add_argument("--unfinished", action="append", help="Unfinished item")
    parser.add_argument("--next-action", action="append", help="Next action")
    parser.add_argument("--risk", action="append", help="Known risk")
    parser.add_argument("--do-not-do", action="append", help="Action to avoid")
    parser.add_argument("--artifact", action="append", help="File/artifact entry")
    parser.add_argument("--command", action="append", help="Command or verification entry")
    parser.add_argument("--decision", action="append", help="Decision or constraint")
    parser.add_argument("--source", action="append", help="Fact source")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage long-task handoff files.")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Create a new timestamped handoff")
    add_common(create)
    create.set_defaults(func=lambda args: write_handoff(args, update=False))

    update = sub.add_parser("update", help="Update active handoff, or create one if missing")
    add_common(update)
    update.set_defaults(func=lambda args: write_handoff(args, update=True))

    find = sub.add_parser("find", help="Find the active or latest handoff")
    find.add_argument("--workspace", default=".")
    find.add_argument("--json", action="store_true")
    find.set_defaults(func=cmd_find)

    recover = sub.add_parser("recover", help="Find and validate handoff for a fresh continuation session")
    recover.add_argument("--workspace", default=".")
    recover.set_defaults(func=cmd_recover)

    suggest = sub.add_parser("suggest", help="Suggest whether to restart based on compaction count")
    suggest.add_argument("--compaction-count", type=int, required=True)
    suggest.add_argument("--json", action="store_true")
    suggest.set_defaults(func=cmd_suggest)

    validate = sub.add_parser("validate", help="Validate a handoff file")
    validate.add_argument("handoff")
    validate.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
