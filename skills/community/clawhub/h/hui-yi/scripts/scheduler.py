#!/usr/bin/env python3
"""Prototype scheduler for Hui-Yi custom timed recall.

This is a low-interruption selector, not a direct messaging daemon.
It reads a schedule config, filters eligible notes, and prints the best recall candidate(s).
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# Ensure the scripts directory is in sys.path before importing sibling modules.
# This is necessary when the script is invoked with an absolute path, via
# subprocess, or under certain IDE / agent runners on Windows, macOS, and Linux.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from core.signal_detect import load_context_text
from review import load_tags
from core.scoring import resurfacing_priority
from core.common import DEFAULT_MEMORY_ROOT, parse_date, read_text_fallback, repetition_signal, resolve_memory_root as common_resolve_memory_root, load_json


DEFAULT_CONFIG_PATH = DEFAULT_MEMORY_ROOT / "schedule.json"
IMPORTANCE_ORDER = {"low": 1, "medium": 2, "high": 3}


def resolve_memory_root(arg: str | None) -> Path:
    return common_resolve_memory_root(arg, default=DEFAULT_MEMORY_ROOT)


def parse_time_hhmm(value: str | None) -> tuple[int, int] | None:
    if not value or ":" not in value:
        return None
    try:
        hh, mm = value.split(":", 1)
        return int(hh), int(mm)
    except ValueError:
        return None


def schedule_matches_now(schedule: dict, now: datetime) -> bool:
    time_value = schedule.get("time")
    parsed = parse_time_hhmm(time_value)
    if parsed:
        return (now.hour, now.minute) == parsed

    cron = schedule.get("cron")
    if isinstance(cron, str):
        parts = cron.split()
        if len(parts) == 5:
            minute, hour = parts[0], parts[1]
            if minute.isdigit() and hour.isdigit():
                return now.minute == int(minute) and now.hour == int(hour)
    return False


def _iter_recent_log_datetimes(log_path: Path):
    if not log_path.exists():
        return
    for line in read_text_fallback(log_path).splitlines():
        if not line.startswith("|"):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 5:
            continue
        try:
            line_date = datetime.fromisoformat(parts[0]).date()
            yield line, datetime.combine(line_date, datetime.min.time()).astimezone()
        except Exception:
            continue


def recent_log_hits(memory_root: Path, note_name: str, hours: int) -> int:
    if hours <= 0:
        return 0
    log_path = memory_root / "retrieval-log.md"
    threshold = datetime.now().astimezone() - timedelta(hours=hours)
    hits = 0
    for line, line_dt in _iter_recent_log_datetimes(log_path):
        if note_name in line and line_dt >= threshold:
            hits += 1
    return hits


def recent_total_hits(memory_root: Path, hours: int) -> int:
    if hours <= 0:
        return 0
    log_path = memory_root / "retrieval-log.md"
    threshold = datetime.now().astimezone() - timedelta(hours=hours)
    return sum(1 for _, line_dt in _iter_recent_log_datetimes(log_path) if line_dt >= threshold)


def importance_ok(note: dict, minimum: str) -> bool:
    return IMPORTANCE_ORDER.get(note.get("importance", "low"), 0) >= IMPORTANCE_ORDER.get(minimum, 0)


def quiet_hours_active(schedule: dict, now: datetime) -> bool:
    quiet = schedule.get("quiet_hours")
    if not isinstance(quiet, dict) or not quiet.get("enabled", False):
        return False
    start = parse_time_hhmm(quiet.get("start"))
    end = parse_time_hhmm(quiet.get("end"))
    if not start or not end:
        return False
    now_minutes = now.hour * 60 + now.minute
    start_minutes = start[0] * 60 + start[1]
    end_minutes = end[0] * 60 + end[1]
    if start_minutes <= end_minutes:
        return start_minutes <= now_minutes < end_minutes
    return now_minutes >= start_minutes or now_minutes < end_minutes


def quiet_hours_mode(schedule: dict) -> str | None:
    quiet = schedule.get("quiet_hours")
    if not isinstance(quiet, dict):
        return None
    return quiet.get("delivery_mode")


def dedupe_key(note: dict, mode: str) -> str:
    if mode == "state":
        return str(note.get("state", "unknown"))
    if mode == "importance":
        return str(note.get("importance", "unknown"))
    tags = note.get("tags")
    if mode == "first_tag" and isinstance(tags, list) and tags:
        return str(tags[0])
    return str(note.get("title", "untitled"))


def select_candidates(
    memory_root: Path,
    config: dict,
    now: datetime,
    context: str | None,
    schedule_id: str | None,
    preview: bool = False,
) -> list[dict]:
    payload = load_tags(memory_root)
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    schedules = config.get("schedules", []) if isinstance(config.get("schedules"), list) else []
    matched_schedules = []

    for schedule in schedules:
        if not isinstance(schedule, dict) or not schedule.get("enabled", True):
            continue
        if schedule_id and schedule.get("id") != schedule_id:
            continue
        if schedule_id or schedule_matches_now(schedule, now):
            matched_schedules.append(schedule)

    candidates: list[dict] = []
    for schedule in matched_schedules:
        if not preview:
            recent_total = recent_total_hits(memory_root, int(schedule.get("global_cooldown_hours", 0) or 0))
            max_daily = int(schedule.get("max_total_per_day", 0) or 0)
            if max_daily > 0 and recent_total >= max_daily:
                continue

        for note in notes:
            if not preview and not importance_ok(note, schedule.get("min_importance", "low")):
                continue
            if not preview and note.get("state") not in (schedule.get("allowed_states") or ["warm", "cold"]):
                continue
            repeat_value = repetition_signal(note, now.date())
            min_repeat = float(schedule.get("min_repetition", 0.0) or 0.0)
            if not preview and schedule.get("require_due", True):
                next_review = parse_date(note.get("next_review"))
                due_by_time = bool(next_review and next_review <= now.date())
                due_by_repeat = repeat_value >= max(0.35, min_repeat)
                if not due_by_time and not due_by_repeat:
                    continue

            note_name = Path(note.get("path", "")).name
            cooldown_raw = schedule.get("cooldown_hours", 24)
            cooldown_hours = int(24 if cooldown_raw is None else cooldown_raw)
            if not preview and recent_log_hits(memory_root, note_name, cooldown_hours) > 0:
                continue

            score, meta = resurfacing_priority(note, now.date(), context)
            min_relevance = float(schedule.get("min_relevance", 0.15) or 0.15)
            if not preview and schedule.get("require_relevance", False) and meta.get("relevance_value", 0.0) < min_relevance:
                continue
            if not preview and schedule.get("context_required", False) and not context:
                continue
            if not preview and context and meta.get("relevance_value", 0.0) < min_relevance:
                continue
            if not preview and repeat_value < min_repeat:
                continue
            if score < float(schedule.get("min_priority", 0.0) or 0.0):
                continue

            delivery_mode = schedule.get("delivery_mode", "prompt")
            if not preview and quiet_hours_active(schedule, now):
                delivery_mode = quiet_hours_mode(schedule) or delivery_mode

            candidates.append(
                {
                    "schedule_id": schedule.get("id", "default"),
                    "delivery_mode": delivery_mode,
                    "score": score,
                    "meta": meta,
                    "note": note,
                    "dedupe_group": dedupe_key(note, str(schedule.get("dedupe_by", "title"))),
                    "repetition_signal": repeat_value,
                }
            )

    candidates.sort(key=lambda item: item["score"], reverse=True)

    deduped: list[dict] = []
    seen_groups: set[str] = set()
    for candidate in candidates:
        group = candidate.get("dedupe_group", "")
        if group in seen_groups:
            continue
        seen_groups.add(group)
        deduped.append(candidate)
    return deduped


def render_message(candidate: dict, templates: dict) -> str:
    note = candidate["note"]
    title = note.get("title", "untitled")
    mode = candidate.get("delivery_mode", "prompt")
    template = templates.get(mode) or templates.get("prompt") or "建议回忆：{title}"
    return template.format(title=title)


def build_json_payload(
    *,
    ok: bool,
    mode: str,
    memory_root: Path,
    config_path: Path,
    now: datetime,
    query: str | None,
    context_file: str | None,
    stdin_flag: bool,
    schedules_matched: list[str],
    candidates: list[dict],
    templates: dict,
    error: dict | None = None,
) -> dict:
    payload: dict = {
        "ok": ok,
        "mode": mode,
        "memoryRoot": str(memory_root),
        "configPath": str(config_path),
        "generatedAt": now.isoformat(timespec="seconds"),
        "context": {
            "query": query,
            "hasContextFile": bool(context_file),
            "usedStdin": stdin_flag,
        },
        "schedulesMatched": schedules_matched,
        "candidates": [],
    }
    if error is not None:
        payload["error"] = error
        return payload

    for candidate in candidates:
        note = candidate.get("note", {})
        meta = candidate.get("meta", {})
        payload["candidates"].append(
            {
                "scheduleId": candidate.get("schedule_id"),
                "deliveryMode": candidate.get("delivery_mode"),
                "title": note.get("title", "untitled"),
                "path": note.get("path"),
                "score": candidate.get("score"),
                "message": render_message(candidate, templates),
                "note": {
                    "importance": note.get("importance"),
                    "state": note.get("state"),
                    "nextReview": note.get("next_review"),
                },
                "meta": {
                    "relevance": meta.get("relevance_value", 0.0),
                    "forgettingRisk": meta.get("forgetting_risk", 0.0),
                    "overdueDays": meta.get("overdue_days", 0),
                    "memoryStrength": meta.get("memory_strength", "weak"),
                },
                "dedupeGroup": candidate.get("dedupe_group"),
                "preview": mode == "preview",
            }
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Prototype scheduler for Hui-Yi timed recall")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--config", default=None, help="schedule config path")
    parser.add_argument("--schedule-id", default=None, help="run a specific schedule regardless of clock match")
    parser.add_argument("--query", default=None, help="short current topic")
    parser.add_argument("--context-file", default=None, help="path to richer context text")
    parser.add_argument("--stdin", action="store_true", help="read additional context from stdin")
    parser.add_argument("--preview", action="store_true", help="preview candidates by bypassing due, importance, allowed_states, relevance-required, and cooldown gating for the selected schedule")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON only")
    args = parser.parse_args()

    memory_root = resolve_memory_root(args.memory_root)
    config_path = common_resolve_memory_root(args.config, default=DEFAULT_CONFIG_PATH) if args.config else DEFAULT_CONFIG_PATH
    config = load_json(config_path)
    now = datetime.now().astimezone()
    mode = "preview" if args.preview else "normal"

    schedules = config.get("schedules", []) if isinstance(config.get("schedules"), list) else []
    schedules_matched = [
        schedule.get("id", "default")
        for schedule in schedules
        if isinstance(schedule, dict)
        and schedule.get("enabled", True)
        and ((args.schedule_id and schedule.get("id") == args.schedule_id) or (not args.schedule_id and schedule_matches_now(schedule, now)))
    ]

    if not config.get("enabled", True):
        if args.json:
            print(json.dumps(build_json_payload(
                ok=True,
                mode=mode,
                memory_root=memory_root,
                config_path=config_path,
                now=now,
                query=args.query,
                context_file=args.context_file,
                stdin_flag=args.stdin,
                schedules_matched=schedules_matched,
                candidates=[],
                templates={},
            ), ensure_ascii=False, indent=2))
        else:
            print("Scheduler disabled.")
        return 0

    context = load_context_text(args.query, args.context_file, args.stdin)
    candidates = select_candidates(memory_root, config, now, context, args.schedule_id, preview=args.preview)
    templates = config.get("prompt_templates", {}) if isinstance(config.get("prompt_templates"), dict) else {}
    if args.json:
        print(json.dumps(build_json_payload(
            ok=True,
            mode=mode,
            memory_root=memory_root,
            config_path=config_path,
            now=now,
            query=args.query,
            context_file=args.context_file,
            stdin_flag=args.stdin,
            schedules_matched=schedules_matched,
            candidates=candidates,
            templates=templates,
        ), ensure_ascii=False, indent=2))
        return 0

    if not candidates:
        if args.preview:
            print("No preview candidates for this schedule.")
        else:
            print("No scheduled recall candidates right now.")
        return 0

    max_items = 1
    if candidates:
        first_schedule = candidates[0].get("schedule_id")
        for schedule in config.get("schedules", []):
            if isinstance(schedule, dict) and schedule.get("id") == first_schedule:
                max_items = int(schedule.get("max_items", 1) or 1)
                break

    print("Scheduled recall candidates:")
    for candidate in candidates[:max_items]:
        note = candidate["note"]
        meta = candidate["meta"]
        print(f"- schedule={candidate['schedule_id']} score={candidate['score']:.3f} title={note.get('title')}")
        print(
            f"  importance={note.get('importance')} state={note.get('state')} next_review={note.get('next_review')} "
            f"strength={meta.get('memory_strength', 'weak')} repetition={candidate.get('repetition_signal', 0.0):.3f} "
            f"relevance={meta.get('relevance_value', 0.0):.3f} due_pressure={meta.get('due_pressure', meta.get('forgetting_risk', 0.0)):.3f}"
        )
        print(f"  delivery_mode={candidate.get('delivery_mode')}")
        if args.preview:
            print("  preview=true")
        print(f"  message={render_message(candidate, templates)}")
        print(f"  path={note.get('path')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
