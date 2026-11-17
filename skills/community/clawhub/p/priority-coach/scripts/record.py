#!/usr/bin/env python3
"""Priority Coach local record management.

默认写入 ~/.openclaw/data/priority-coach/ 下的：
- records.json：用户明确保存的完整结果卡
- sessions.json：默认最小会话摘要

用法：
  python3 scripts/record.py add --data '<json>'
  python3 scripts/record.py list
  python3 scripts/record.py latest
  python3 scripts/record.py get [--date YYYY-MM-DD | --index N]
  python3 scripts/record.py delete [--date YYYY-MM-DD | --index N | --all]
  python3 scripts/record.py export

  python3 scripts/record.py session-add --data '<json>'
  python3 scripts/record.py session-list
  python3 scripts/record.py session-latest
  python3 scripts/record.py session-get [--date YYYY-MM-DD | --index N]
  python3 scripts/record.py session-delete [--date YYYY-MM-DD | --index N | --all]
  python3 scripts/record.py session-export
  python3 scripts/record.py session-weekly-summary [--days N] [--limit N]

  python3 scripts/record.py path
  python3 scripts/record.py migrate
  python3 scripts/record.py weekly-summary [--days N] [--limit N]
"""

from __future__ import annotations

import argparse
from collections import Counter
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Any

OPENCLAW_HOME = Path(os.environ.get("OPENCLAW_HOME", "~/.openclaw")).expanduser()
PRIMARY_DIR = OPENCLAW_HOME / "data" / "priority-coach"
PRIMARY_RECORDS_STORE = PRIMARY_DIR / "records.json"
PRIMARY_SESSIONS_STORE = PRIMARY_DIR / "sessions.json"

LEGACY_DIR = Path("~/.workbuddy/priority-coach").expanduser()
LEGACY_RECORDS_STORE = LEGACY_DIR / "records.json"
LEGACY_SESSIONS_STORE = LEGACY_DIR / "sessions.json"

RECORDS_SCHEMA_VERSION = 3
SESSIONS_SCHEMA_VERSION = 1

VALID_FEEDBACK_OUTCOMES = {
    "",
    "clarified_priority",
    "defined_next_step",
    "reduced_pressure",
    "not_helpful",
}

VALID_FEEDBACK_FAILURE_REASONS = {
    "",
    "too_many_questions",
    "too_abstract",
    "wrong_route",
    "not_actionable",
    "too_heavy",
    "other",
}

VALID_FAILURE_TAGS = {
    "too_many_questions",
    "too_abstract",
    "wrong_route",
    "not_actionable",
    "too_heavy",
    "low_energy_dropoff",
}

VALID_ROUTE_CONFIDENCE = {"", "high", "medium", "low"}
VALID_DROPOFF_RISK = {"", "low", "medium", "high"}
VALID_RESULT_TYPES = {
    "",
    "priority_card",
    "action_card",
    "wrap_card",
    "habit_card",
    "overwhelmed_card",
    "none",
}


def get_store_paths(kind: str) -> tuple[Path, Path]:
    if kind == "records":
        return PRIMARY_RECORDS_STORE, LEGACY_RECORDS_STORE
    if kind == "sessions":
        return PRIMARY_SESSIONS_STORE, LEGACY_SESSIONS_STORE
    raise ValueError(f"unknown store kind: {kind}")


def get_schema_version(kind: str) -> int:
    if kind == "records":
        return RECORDS_SCHEMA_VERSION
    if kind == "sessions":
        return SESSIONS_SCHEMA_VERSION
    raise ValueError(f"unknown store kind: {kind}")


def get_items_key(kind: str) -> str:
    if kind == "records":
        return "records"
    if kind == "sessions":
        return "sessions"
    raise ValueError(f"unknown store kind: {kind}")


def empty_store(kind: str) -> dict[str, Any]:
    return {"schemaVersion": get_schema_version(kind), get_items_key(kind): []}


def default_session_meta() -> dict[str, Any]:
    return {
        "sessionId": "",
        "enteredState": "",
        "endedState": "",
        "completed": False,
        "savedByUser": False,
        "feedbackOutcome": "",
        "feedbackFailureReason": "",
        "failureTags": [],
        "routeConfidence": "",
        "dropoffRisk": "",
        "nextStepChosen": "",
    }


def default_session_summary() -> dict[str, Any]:
    return {
        "schemaVersion": SESSIONS_SCHEMA_VERSION,
        "sessionId": "",
        "date": "",
        "startedAt": "",
        "endedAt": "",
        "enteredState": "",
        "endedState": "",
        "completed": False,
        "resultType": "",
        "savedResult": False,
        "feedbackOutcome": "",
        "feedbackFailureReason": "",
        "failureTags": [],
        "routeConfidence": "",
        "dropoffRisk": "",
        "nextStepChosen": "",
    }


def normalize_string(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def normalize_list(value: Any, *, limit: int | None = None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        items = [value]
    elif isinstance(value, list):
        items = value
    else:
        items = [str(value)]

    cleaned: list[str] = []
    for item in items:
        text = normalize_string(item)
        if text:
            cleaned.append(text)
    if limit is not None:
        cleaned = cleaned[:limit]
    return cleaned


def normalize_bool(value: Any, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    if value in (1, "1", "true", "True", "yes", "YES"):
        return True
    if value in (0, "0", "false", "False", "no", "NO"):
        return False
    return default


def normalize_enum(value: Any, valid: set[str], default: str = "") -> str:
    text = normalize_string(value)
    if text in valid:
        return text
    return default


def normalize_session_meta(raw: Any) -> dict[str, Any]:
    base = default_session_meta()
    if not isinstance(raw, dict):
        return base

    base["sessionId"] = normalize_string(raw.get("sessionId"))
    base["enteredState"] = normalize_string(raw.get("enteredState"))
    base["endedState"] = normalize_string(raw.get("endedState"))
    base["completed"] = normalize_bool(raw.get("completed"), default=False)
    base["savedByUser"] = normalize_bool(raw.get("savedByUser"), default=False)
    base["feedbackOutcome"] = normalize_enum(raw.get("feedbackOutcome"), VALID_FEEDBACK_OUTCOMES)
    base["feedbackFailureReason"] = normalize_enum(
        raw.get("feedbackFailureReason"),
        VALID_FEEDBACK_FAILURE_REASONS,
    )
    tags = normalize_list(raw.get("failureTags"), limit=2)
    base["failureTags"] = [tag for tag in tags if tag in VALID_FAILURE_TAGS]
    base["routeConfidence"] = normalize_enum(raw.get("routeConfidence"), VALID_ROUTE_CONFIDENCE)
    base["dropoffRisk"] = normalize_enum(raw.get("dropoffRisk"), VALID_DROPOFF_RISK)
    base["nextStepChosen"] = normalize_string(raw.get("nextStepChosen"))
    return base


def normalize_session_summary(raw: Any) -> dict[str, Any]:
    base = default_session_summary()
    if not isinstance(raw, dict):
        return base

    now = dt.datetime.now().isoformat(timespec="seconds")
    base["sessionId"] = normalize_string(raw.get("sessionId"))
    base["date"] = normalize_string(raw.get("date")) or dt.date.today().isoformat()
    base["startedAt"] = normalize_string(raw.get("startedAt")) or now
    base["endedAt"] = normalize_string(raw.get("endedAt")) or now
    base["enteredState"] = normalize_string(raw.get("enteredState"))
    base["endedState"] = normalize_string(raw.get("endedState"))
    base["completed"] = normalize_bool(raw.get("completed"), False)
    base["savedResult"] = normalize_bool(raw.get("savedResult"), False)
    base["resultType"] = normalize_enum(raw.get("resultType"), VALID_RESULT_TYPES)
    base["feedbackOutcome"] = normalize_enum(raw.get("feedbackOutcome"), VALID_FEEDBACK_OUTCOMES)
    base["feedbackFailureReason"] = normalize_enum(
        raw.get("feedbackFailureReason"),
        VALID_FEEDBACK_FAILURE_REASONS,
    )
    tags = normalize_list(raw.get("failureTags"), limit=2)
    base["failureTags"] = [tag for tag in tags if tag in VALID_FAILURE_TAGS]
    base["routeConfidence"] = normalize_enum(raw.get("routeConfidence"), VALID_ROUTE_CONFIDENCE)
    base["dropoffRisk"] = normalize_enum(raw.get("dropoffRisk"), VALID_DROPOFF_RISK)
    base["nextStepChosen"] = normalize_string(raw.get("nextStepChosen"))
    return base


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    now = dt.datetime.now().isoformat(timespec="seconds")
    record = {
        "schemaVersion": RECORDS_SCHEMA_VERSION,
        "date": normalize_string(raw.get("date")) or dt.date.today().isoformat(),
        "createdAt": normalize_string(raw.get("createdAt")) or now,
        "state": normalize_string(raw.get("state")),
        "topPriorities": normalize_list(raw.get("topPriorities"), limit=3),
        "smallestActionToday": normalize_string(raw.get("smallestActionToday")),
        "notNow": normalize_list(raw.get("notNow")),
        "candidates": normalize_list(raw.get("candidates"), limit=7),
        "weeklyFocus": normalize_list(raw.get("weeklyFocus"), limit=3),
        "energyPattern": normalize_string(raw.get("energyPattern")),
        "supportPreference": normalize_string(raw.get("supportPreference")),
        "sessionMeta": normalize_session_meta(raw.get("sessionMeta")),
    }

    raw_answers = raw.get("rawAnswers")
    if raw_answers is not None:
        record["rawAnswers"] = raw_answers

    if not record["topPriorities"]:
        raise ValueError("topPriorities 不能为空")
    if not record["smallestActionToday"]:
        raise ValueError("smallestActionToday 不能为空")
    return record


def normalize_loaded_items(kind: str, data: dict[str, Any]) -> dict[str, Any]:
    items_key = get_items_key(kind)
    items = data.get(items_key, [])
    normalized: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        merged = dict(item)
        if kind == "records":
            merged.setdefault("sessionMeta", default_session_meta())
            merged["sessionMeta"] = normalize_session_meta(merged.get("sessionMeta"))
            merged["schemaVersion"] = RECORDS_SCHEMA_VERSION
        else:
            merged = normalize_session_summary(merged)
        normalized.append(merged)
    data[items_key] = normalized
    data["schemaVersion"] = get_schema_version(kind)
    return data


def filter_recent_records(
    items: list[dict[str, Any]],
    *,
    days: int | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    filtered = items
    if days is not None:
        cutoff = dt.date.today() - dt.timedelta(days=days)
        tmp: list[dict[str, Any]] = []
        for item in filtered:
            try:
                item_date = dt.date.fromisoformat(item.get("date", ""))
            except Exception:
                continue
            if item_date >= cutoff:
                tmp.append(item)
        filtered = tmp
    if limit is not None:
        filtered = filtered[:limit]
    return filtered


def detect_existing_store(kind: str) -> Path | None:
    primary, legacy = get_store_paths(kind)
    if primary.exists():
        return primary
    if legacy.exists():
        return legacy
    return None


def load_store(kind: str) -> tuple[dict[str, Any], Path | None]:
    store_path = detect_existing_store(kind)
    if store_path is None:
        return empty_store(kind), None
    try:
        with store_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return empty_store(kind), store_path

    if not isinstance(data, dict):
        return empty_store(kind), store_path

    items_key = get_items_key(kind)
    items = data.get(items_key)
    if not isinstance(items, list):
        data[items_key] = []
    data["schemaVersion"] = get_schema_version(kind)
    return normalize_loaded_items(kind, data), store_path


def write_store(kind: str, data: dict[str, Any]) -> None:
    primary, _ = get_store_paths(kind)
    PRIMARY_DIR.mkdir(parents=True, exist_ok=True)
    data["schemaVersion"] = get_schema_version(kind)
    with primary.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def find_item(items: list[dict[str, Any]], *, date: str | None, index: int | None) -> dict[str, Any]:
    if not items:
        raise IndexError("暂无记录")
    if date:
        for item in items:
            if item.get("date") == date:
                return item
        raise IndexError(f"未找到日期 {date}")
    idx = index or 1
    if not 1 <= idx <= len(items):
        raise IndexError("索引越界")
    return items[idx - 1]


def cmd_add(args: argparse.Namespace) -> int:
    try:
        raw = json.loads(args.data)
    except Exception as exc:
        print(f"ERROR: --data 必须是合法 JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(raw, dict):
        print("ERROR: 记录必须是 JSON 对象", file=sys.stderr)
        return 1
    try:
        record = normalize_record(raw)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    data, _ = load_store("records")
    data["records"].insert(0, record)
    write_store("records", data)
    print(f"已保存。当前共 {len(data['records'])} 条记录。")
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def iter_records() -> tuple[list[dict[str, Any]], Path | None]:
    data, store_path = load_store("records")
    return data.get("records", []), store_path


def iter_sessions() -> tuple[list[dict[str, Any]], Path | None]:
    data, store_path = load_store("sessions")
    return data.get("sessions", []), store_path


def cmd_list(_: argparse.Namespace) -> int:
    records, store_path = iter_records()
    if not records:
        print("（暂无记录）")
        return 0
    print(f"当前数据源：{store_path or PRIMARY_RECORDS_STORE}")
    for idx, record in enumerate(records, start=1):
        date = record.get("date", "?")
        tops = " / ".join(record.get("topPriorities", []))
        action = record.get("smallestActionToday", "")
        meta = record.get("sessionMeta", {}) or {}
        entered = meta.get("enteredState", "")
        ended = meta.get("endedState", "")
        flow = f"{entered}->{ended}" if entered or ended else "-"
        print(f"{idx}. {date} | {flow} | {tops} | 最小行动：{action}")
    return 0


def cmd_latest(_: argparse.Namespace) -> int:
    records, _ = iter_records()
    if not records:
        print("（暂无记录）")
        return 0
    print(json.dumps(records[0], ensure_ascii=False, indent=2))
    return 0


def cmd_get(args: argparse.Namespace) -> int:
    records, _ = iter_records()
    if not records:
        print("（暂无记录）")
        return 0
    try:
        record = find_item(records, date=args.date, index=args.index)
    except IndexError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    data, _ = load_store("records")
    records = data.get("records", [])
    if not records:
        print("（暂无记录）")
        return 0

    if args.all:
        data["records"] = []
        write_store("records", data)
        print("已清空所有记录。")
        return 0

    if args.date:
        before = len(records)
        data["records"] = [record for record in records if record.get("date") != args.date]
        removed = before - len(data["records"])
        write_store("records", data)
        print(f"删除了 {removed} 条。")
        return 0

    idx = args.index or 1
    if not 1 <= idx <= len(records):
        print("索引越界", file=sys.stderr)
        return 1
    removed = records[idx - 1]
    data["records"].pop(idx - 1)
    write_store("records", data)
    print(f"已删除：{removed.get('date', '?')}")
    return 0


def cmd_export(_: argparse.Namespace) -> int:
    data, _ = load_store("records")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_session_add(args: argparse.Namespace) -> int:
    try:
        raw = json.loads(args.data)
    except Exception as exc:
        print(f"ERROR: --data 必须是合法 JSON: {exc}", file=sys.stderr)
        return 1
    if not isinstance(raw, dict):
        print("ERROR: session 必须是 JSON 对象", file=sys.stderr)
        return 1

    session = normalize_session_summary(raw)
    data, _ = load_store("sessions")
    data["sessions"].insert(0, session)
    write_store("sessions", data)
    print(f"已保存 session。当前共 {len(data['sessions'])} 条。")
    print(json.dumps(session, ensure_ascii=False, indent=2))
    return 0


def cmd_session_list(_: argparse.Namespace) -> int:
    sessions, store_path = iter_sessions()
    if not sessions:
        print("（暂无 session 记录）")
        return 0
    print(f"当前 session 数据源：{store_path or PRIMARY_SESSIONS_STORE}")
    for idx, session in enumerate(sessions, start=1):
        date = session.get("date", "?")
        entered = session.get("enteredState", "")
        ended = session.get("endedState", "")
        completed = "done" if session.get("completed") else "drop"
        result_type = session.get("resultType", "")
        print(f"{idx}. {date} | {entered}->{ended} | {completed} | {result_type}")
    return 0


def cmd_session_latest(_: argparse.Namespace) -> int:
    sessions, _ = iter_sessions()
    if not sessions:
        print("（暂无 session 记录）")
        return 0
    print(json.dumps(sessions[0], ensure_ascii=False, indent=2))
    return 0


def cmd_session_get(args: argparse.Namespace) -> int:
    sessions, _ = iter_sessions()
    if not sessions:
        print("（暂无 session 记录）")
        return 0
    try:
        session = find_item(sessions, date=args.date, index=args.index)
    except IndexError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(session, ensure_ascii=False, indent=2))
    return 0


def cmd_session_delete(args: argparse.Namespace) -> int:
    data, _ = load_store("sessions")
    sessions = data.get("sessions", [])
    if not sessions:
        print("（暂无 session 记录）")
        return 0

    if args.all:
        data["sessions"] = []
        write_store("sessions", data)
        print("已清空所有 session。")
        return 0

    if args.date:
        before = len(sessions)
        data["sessions"] = [s for s in sessions if s.get("date") != args.date]
        removed = before - len(data["sessions"])
        write_store("sessions", data)
        print(f"删除了 {removed} 条 session。")
        return 0

    idx = args.index or 1
    if not (1 <= idx <= len(sessions)):
        print("索引越界", file=sys.stderr)
        return 1
    removed = sessions[idx - 1]
    data["sessions"].pop(idx - 1)
    write_store("sessions", data)
    print(f"已删除 session：{removed.get('date', '?')}")
    return 0


def cmd_session_export(_: argparse.Namespace) -> int:
    data, _ = load_store("sessions")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


def cmd_weekly_summary(args: argparse.Namespace) -> int:
    records, _ = iter_records()
    if not records:
        print("（暂无记录）")
        return 0

    records = filter_recent_records(records, days=args.days, limit=args.limit)
    if not records:
        print("（所选范围内暂无记录）")
        return 0

    total = len(records)
    entered_counter: Counter[str] = Counter()
    ended_counter: Counter[str] = Counter()
    outcome_counter: Counter[str] = Counter()
    failure_reason_counter: Counter[str] = Counter()
    failure_tag_counter: Counter[str] = Counter()
    completed_count = 0
    saved_count = 0

    for record in records:
        meta = record.get("sessionMeta", {}) or {}
        entered_counter[meta.get("enteredState", "")] += 1
        ended_counter[meta.get("endedState", "")] += 1
        outcome_counter[meta.get("feedbackOutcome", "")] += 1
        failure_reason_counter[meta.get("feedbackFailureReason", "")] += 1
        for tag in meta.get("failureTags", []):
            failure_tag_counter[tag] += 1
        if meta.get("completed"):
            completed_count += 1
        if meta.get("savedByUser"):
            saved_count += 1

    helpful_count = (
        outcome_counter["clarified_priority"]
        + outcome_counter["defined_next_step"]
        + outcome_counter["reduced_pressure"]
    )

    print("## 本周概览")
    print(f"- 样本数：{total}")
    print(f"- 完成率：{completed_count}/{total}")
    print(f"- 保存率：{saved_count}/{total}")
    print(f"- 有帮助反馈数：{helpful_count}/{total}")

    def print_counter(title: str, counter: Counter[str]) -> None:
        print(f"\n## {title}")
        for key, count in counter.most_common(5):
            if key:
                print(f"- {key}: {count}")

    print_counter("进入状态 Top", entered_counter)
    print_counter("结束状态 Top", ended_counter)
    print_counter("失败原因 Top", failure_reason_counter)
    print_counter("失败标签 Top", failure_tag_counter)
    return 0


def cmd_session_weekly_summary(args: argparse.Namespace) -> int:
    sessions, _ = iter_sessions()
    if not sessions:
        print("（暂无 session 记录）")
        return 0

    sessions = filter_recent_records(sessions, days=args.days, limit=args.limit)
    if not sessions:
        print("（所选范围内暂无 session 记录）")
        return 0

    total = len(sessions)
    entered_counter: Counter[str] = Counter()
    ended_counter: Counter[str] = Counter()
    outcome_counter: Counter[str] = Counter()
    failure_reason_counter: Counter[str] = Counter()
    failure_tag_counter: Counter[str] = Counter()
    completed_count = 0
    saved_result_count = 0

    for session in sessions:
        entered_counter[session.get("enteredState", "")] += 1
        ended_counter[session.get("endedState", "")] += 1
        outcome_counter[session.get("feedbackOutcome", "")] += 1
        failure_reason_counter[session.get("feedbackFailureReason", "")] += 1
        for tag in session.get("failureTags", []):
            failure_tag_counter[tag] += 1
        if session.get("completed"):
            completed_count += 1
        if session.get("savedResult"):
            saved_result_count += 1

    helpful_count = (
        outcome_counter["clarified_priority"]
        + outcome_counter["defined_next_step"]
        + outcome_counter["reduced_pressure"]
    )

    print("## 本周 session 概览")
    print(f"- 样本数：{total}")
    print(f"- 完成率：{completed_count}/{total}")
    print(f"- 保存结果率：{saved_result_count}/{total}")
    print(f"- 有帮助反馈数：{helpful_count}/{total}")

    def print_counter(title: str, counter: Counter[str]) -> None:
        print(f"\n## {title}")
        for key, count in counter.most_common(5):
            if key:
                print(f"- {key}: {count}")

    print_counter("进入状态 Top", entered_counter)
    print_counter("结束状态 Top", ended_counter)
    print_counter("失败原因 Top", failure_reason_counter)
    print_counter("失败标签 Top", failure_tag_counter)
    return 0


def cmd_path(_: argparse.Namespace) -> int:
    current_records = detect_existing_store("records") or PRIMARY_RECORDS_STORE
    current_sessions = detect_existing_store("sessions") or PRIMARY_SESSIONS_STORE
    print(f"records: {current_records}")
    print(f"sessions: {current_sessions}")
    return 0


def cmd_migrate(_: argparse.Namespace) -> int:
    PRIMARY_DIR.mkdir(parents=True, exist_ok=True)

    def migrate_kind(kind: str) -> str:
        primary, legacy = get_store_paths(kind)
        items_key = get_items_key(kind)
        if primary.exists():
            return f"{kind}: 已使用新路径：{primary}"
        if not legacy.exists():
            write_store(kind, empty_store(kind))
            return f"{kind}: 未发现旧数据，已初始化新路径：{primary}"
        shutil.copy2(legacy, primary)
        data, _ = load_store(kind)
        if items_key not in data:
            data[items_key] = []
        write_store(kind, data)
        return f"{kind}: 已迁移：{legacy} -> {primary}"

    print(migrate_kind("records"))
    print(migrate_kind("sessions"))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="优先级教练本地记录")
    sub = parser.add_subparsers(dest="cmd")

    add = sub.add_parser("add")
    add.add_argument("--data", required=True)

    sub.add_parser("list")
    sub.add_parser("latest")

    get = sub.add_parser("get")
    get.add_argument("--date")
    get.add_argument("--index", type=int)

    delete = sub.add_parser("delete")
    delete.add_argument("--date")
    delete.add_argument("--index", type=int)
    delete.add_argument("--all", action="store_true")

    session_add = sub.add_parser("session-add")
    session_add.add_argument("--data", required=True)

    sub.add_parser("session-list")
    sub.add_parser("session-latest")

    session_get = sub.add_parser("session-get")
    session_get.add_argument("--date")
    session_get.add_argument("--index", type=int)

    session_delete = sub.add_parser("session-delete")
    session_delete.add_argument("--date")
    session_delete.add_argument("--index", type=int)
    session_delete.add_argument("--all", action="store_true")

    sub.add_parser("session-export")

    sub.add_parser("export")
    sub.add_parser("path")
    sub.add_parser("migrate")

    weekly = sub.add_parser("weekly-summary")
    weekly.add_argument("--days", type=int, default=7)
    weekly.add_argument("--limit", type=int)

    session_weekly = sub.add_parser("session-weekly-summary")
    session_weekly.add_argument("--days", type=int, default=7)
    session_weekly.add_argument("--limit", type=int)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd == "add":
        return cmd_add(args)
    if args.cmd == "list":
        return cmd_list(args)
    if args.cmd == "latest":
        return cmd_latest(args)
    if args.cmd == "get":
        return cmd_get(args)
    if args.cmd == "delete":
        return cmd_delete(args)

    if args.cmd == "session-add":
        return cmd_session_add(args)
    if args.cmd == "session-list":
        return cmd_session_list(args)
    if args.cmd == "session-latest":
        return cmd_session_latest(args)
    if args.cmd == "session-get":
        return cmd_session_get(args)
    if args.cmd == "session-delete":
        return cmd_session_delete(args)
    if args.cmd == "session-export":
        return cmd_session_export(args)

    if args.cmd == "export":
        return cmd_export(args)
    if args.cmd == "path":
        return cmd_path(args)
    if args.cmd == "weekly-summary":
        return cmd_weekly_summary(args)
    if args.cmd == "session-weekly-summary":
        return cmd_session_weekly_summary(args)
    if args.cmd == "migrate":
        return cmd_migrate(args)
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
