from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

MONITORED_TOOLS = {"exec", "read", "write", "edit", "browser"}
DEFAULT_DESCRIPTION = (
    "Learned procedural memory distilled from a successful OpenClaw session. "
    "Use when a similar task needs the same command sequence, file edits, or failure avoidance logic."
)


@dataclass(slots=True)
class TraceEvent:
    tool: str
    status: str
    summary: str
    detail: str
    snippet: str = ""
    error: str = ""
    raw: dict[str, Any] | None = None

    @property
    def ok(self) -> bool:
        return self.status == "ok"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Distill a successful OpenClaw trace into a reusable learned skill."
    )
    parser.add_argument("--trace", required=True, help="Path to a trace JSON file.")
    parser.add_argument("--task", help="Explicit task summary. Overrides the trace title.")
    parser.add_argument(
        "--output-root",
        default="skills",
        help="Root directory that contains the learned skill directory.",
    )
    parser.add_argument(
        "--learned-root",
        default="learned",
        help="Directory name under output-root where learned skills are written.",
    )
    parser.add_argument(
        "--utility-score",
        type=int,
        choices=range(1, 6),
        help="1-5 utility score. Defaults to the trace value or 3.",
    )
    parser.add_argument(
        "--max-events",
        type=int,
        default=20,
        help="Maximum number of recent relevant events to inspect.",
    )
    parser.add_argument(
        "--min-tool-calls",
        type=int,
        default=5,
        help="Minimum number of relevant tool events required before distillation.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Generate output even when the trace is not marked successful or is too small.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value[:48] or "session"


def compact(text: str, limit: int = 220) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def read_trace(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {"events": data}
    if isinstance(data, dict):
        return data
    raise ValueError("Trace JSON must be either an object or an array.")


def infer_status(raw_event: dict[str, Any]) -> str:
    status = str(raw_event.get("status", "")).strip().lower()
    if status in {"ok", "success", "passed"}:
        return "ok"
    if status in {"error", "failed", "failure"}:
        return "error"
    if "ok" in raw_event:
        return "ok" if bool(raw_event["ok"]) else "error"
    if "success" in raw_event:
        return "ok" if bool(raw_event["success"]) else "error"
    if raw_event.get("error"):
        return "error"
    return "ok"


def event_summary(tool: str, raw_event: dict[str, Any]) -> tuple[str, str]:
    if tool == "exec":
        command = raw_event.get("command") or raw_event.get("cmd") or raw_event.get("input") or ""
        return compact(str(command), 140), f"Command: {compact(str(command), 400)}"
    if tool in {"read", "write", "edit"}:
        path = raw_event.get("path") or raw_event.get("file") or raw_event.get("target") or ""
        verb = "Edited" if tool == "edit" else tool.capitalize()
        return compact(f"{verb} {path}", 140), f"Path: {path}"
    if tool == "browser":
        url = raw_event.get("url") or raw_event.get("ref") or raw_event.get("query") or ""
        return compact(f"Browser {url}", 140), f"Browser target: {compact(str(url), 400)}"
    fallback = raw_event.get("summary") or raw_event.get("message") or tool
    return compact(str(fallback), 140), compact(json.dumps(raw_event, ensure_ascii=False), 400)


def event_snippet(raw_event: dict[str, Any]) -> str:
    for key in ("snippet", "content", "diff", "patch"):
        value = raw_event.get(key)
        if value:
            return compact(str(value), 400)
    return ""


def normalize_events(payload: dict[str, Any], max_events: int) -> list[TraceEvent]:
    raw_events = payload.get("events") or []
    relevant: list[TraceEvent] = []
    for raw in raw_events:
        if not isinstance(raw, dict):
            continue
        tool = str(raw.get("tool") or raw.get("type") or raw.get("kind") or "").strip().lower()
        if tool not in MONITORED_TOOLS:
            continue
        summary, detail = event_summary(tool, raw)
        relevant.append(
            TraceEvent(
                tool=tool,
                status=infer_status(raw),
                summary=summary,
                detail=detail,
                snippet=event_snippet(raw),
                error=compact(str(raw.get("error", "")), 300),
                raw=raw,
            )
        )
    return relevant[-max_events:]


def trace_succeeded(payload: dict[str, Any], events: list[TraceEvent]) -> bool:
    status = str(payload.get("status") or payload.get("task_status") or "").strip().lower()
    if status:
        return status in {"ok", "success", "passed", "done"}
    return bool(events) and any(event.ok for event in events) and events[-1].ok


def extract_success_pattern(events: list[TraceEvent]) -> list[str]:
    lines: list[str] = []
    seen: set[str] = set()
    for event in events:
        if not event.ok:
            continue
        candidate = f"- {event.summary}"
        if candidate in seen:
            continue
        seen.add(candidate)
        lines.append(candidate)
    return lines


def extract_failure_triggers(events: list[TraceEvent]) -> list[str]:
    lines: list[str] = []
    for event in events:
        if event.ok:
            continue
        detail = event.error or event.detail
        lines.append(f"- Avoid `{event.summary}` because {detail}")
    return lines or ["- No critical failed attempts were preserved in the inspected window."]


def extract_snippets(events: list[TraceEvent]) -> list[str]:
    snippets: list[str] = []
    for event in events:
        if event.snippet:
            label = event.raw.get("path") or event.raw.get("file") or event.tool
            snippets.append(f"### {label}\n```\n{event.snippet}\n```")
    return snippets[:5]


def build_learned_skill_markdown(
    name: str,
    description: str,
    task: str,
    success_pattern: list[str],
    failure_triggers: list[str],
    snippets: list[str],
    utility_score: int,
) -> str:
    sections = [
        "---",
        f"name: {name}",
        f"description: {description}",
        "---",
        "",
        f"# {task}",
        "",
        "## Success Pattern",
        *success_pattern,
        "",
        "## Failure Triggers",
        *failure_triggers,
        "",
        "## Snippets",
    ]
    if snippets:
        sections.extend(snippets)
    else:
        sections.append("No durable code or patch snippets were captured in this trace window.")
    sections.extend(
        [
            "",
            "## Utility Score",
            "```yaml",
            f"utility_score: {utility_score}",
            "scale: 1-5",
            "```",
            "",
            "## Usage Guidance",
            "Replay the preserved commands and file edits in order. Prefer this skill when the task looks materially similar, and update the utility score after future uses if the workflow proves more or less effective.",
            "",
        ]
    )
    return "\n".join(sections)


def build_openai_yaml(task: str) -> str:
    return "\n".join(
        [
            "version: 1",
            f"display_name: {compact(task, 48)}",
            "short_description: Learned procedural memory distilled from a successful OpenClaw session.",
            f"default_prompt: Reuse the learned workflow for '{compact(task, 96)}' and adapt it to the current task.",
            "",
        ]
    )


def build_memory_payload(
    task: str,
    trace_path: Path,
    utility_score: int,
    events: list[TraceEvent],
) -> dict[str, Any]:
    return {
        "task": task,
        "utility_score": utility_score,
        "generated_at": datetime.now(UTC).isoformat(),
        "source_trace": str(trace_path),
        "event_window_size": len(events),
        "event_counts": {
            "success": sum(1 for event in events if event.ok),
            "failure": sum(1 for event in events if not event.ok),
        },
        "tools": [event.tool for event in events],
    }


def ensure_output(
    output_root: Path,
    learned_root: str,
    task: str,
    markdown: str,
    memory_payload: dict[str, Any],
) -> Path:
    skill_name = f"learned-{slugify(task)}"
    destination = output_root / learned_root / skill_name
    agents_dir = destination / "agents"
    agents_dir.mkdir(parents=True, exist_ok=True)
    (destination / "SKILL.md").write_text(markdown, encoding="utf-8")
    (agents_dir / "openai.yaml").write_text(build_openai_yaml(task), encoding="utf-8")
    (destination / "memory.json").write_text(
        json.dumps(memory_payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return destination


def main() -> int:
    args = parse_args()
    trace_path = Path(args.trace)
    payload = read_trace(trace_path)
    task = args.task or payload.get("task") or payload.get("title") or "Recovered successful workflow"
    events = normalize_events(payload, args.max_events)
    if not trace_succeeded(payload, events) and not args.force:
        print("Skipped: trace is not marked successful.", file=sys.stderr)
        return 2
    if len(events) < args.min_tool_calls and not args.force:
        print(
            f"Skipped: only {len(events)} relevant tool events found; need at least {args.min_tool_calls}.",
            file=sys.stderr,
        )
        return 2

    utility_score = args.utility_score or int(payload.get("utility_score") or 3)
    learned_name = f"learned-{slugify(task)}"
    learned_description = (
        f"{DEFAULT_DESCRIPTION} Original task: {compact(task, 120)}."
    )
    success_pattern = extract_success_pattern(events)
    failure_triggers = extract_failure_triggers(events)
    snippets = extract_snippets(events)
    markdown = build_learned_skill_markdown(
        name=learned_name,
        description=learned_description,
        task=task,
        success_pattern=success_pattern,
        failure_triggers=failure_triggers,
        snippets=snippets,
        utility_score=utility_score,
    )
    memory_payload = build_memory_payload(task, trace_path, utility_score, events)
    destination = ensure_output(
        output_root=Path(args.output_root),
        learned_root=args.learned_root,
        task=task,
        markdown=markdown,
        memory_payload=memory_payload,
    )
    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
