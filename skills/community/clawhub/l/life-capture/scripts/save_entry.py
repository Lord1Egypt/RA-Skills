#!/usr/bin/env python3
import argparse
import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

SECTION_TITLES = {
    "expense": "开销",
    "task": "任务",
    "schedule": "日程",
    "idea": "灵感",
}

TYPE_PREFIX = {
    "expense": "exp",
    "task": "task",
    "schedule": "sched",
    "idea": "idea",
}


@dataclass
class SaveResult:
    id: str
    type: str
    md_file: str
    markdown_block: str
    db_written: bool


def ensure_daily_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# {path.stem}\n\n", encoding="utf-8")


def ensure_section(text: str, title: str) -> str:
    header = f"## {title}\n"
    if header in text:
        return text
    if not text.endswith("\n"):
        text += "\n"
    return text + f"\n{header}\n"


def format_value(v: Optional[object]) -> str:
    if v is None or v == "":
        return ""
    return str(v)


def build_block(record: Dict) -> str:
    tags = " ".join(f"#{t}" for t in record.get("tags", []))
    lines = [
        f"### {record['id']}",
        f"- 时间：{format_value(record.get('time'))}",
        f"- 标签：{tags}",
        f"- 原始描述：{record.get('raw_text', '')}",
        f"- 摘要：{record.get('summary', '')}",
    ]
    payload = record.get("payload", {}) or {}
    rtype = record["type"]
    if rtype == "expense":
        lines.extend([
            f"- 金额：{format_value(payload.get('amount'))}",
            f"- 币种：{format_value(payload.get('currency'))}",
            f"- 分类：{format_value(payload.get('category'))}",
            f"- 子分类：{format_value(payload.get('subcategory'))}",
            f"- 商家：{format_value(payload.get('merchant'))}",
            f"- 支付方式：{format_value(payload.get('pay_method'))}",
        ])
    elif rtype == "task":
        lines.extend([
            f"- 状态：{format_value(payload.get('status'))}",
            f"- 优先级：{format_value(payload.get('priority'))}",
            f"- 项目：{format_value(payload.get('project'))}",
            f"- 截止日期：{format_value(payload.get('due_date'))}",
            f"- 完成时间：{format_value(payload.get('completed_at'))}",
        ])
    elif rtype == "schedule":
        lines.extend([
            f"- 日期：{format_value(payload.get('schedule_date'))}",
            f"- 开始时间：{format_value(payload.get('start_time'))}",
            f"- 结束时间：{format_value(payload.get('end_time'))}",
            f"- 地点：{format_value(payload.get('location'))}",
            f"- 状态：{format_value(payload.get('status'))}",
        ])
    elif rtype == "idea":
        lines.extend([
            f"- 类型：{format_value(payload.get('idea_type'))}",
            f"- 状态：{format_value(payload.get('status'))}",
            f"- 关联任务：{format_value(payload.get('related_task_id'))}",
        ])
    return "\n".join(lines) + "\n\n"


def upsert_entry(conn: sqlite3.Connection, record: Dict, md_file: str) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    payload_json = json.dumps(record.get("payload", {}), ensure_ascii=False)
    conn.execute(
        """
        INSERT INTO entries (
            id, type, date, time, title, raw_text, summary, source, md_file,
            md_anchor, payload_json, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            type=excluded.type,
            date=excluded.date,
            time=excluded.time,
            title=excluded.title,
            raw_text=excluded.raw_text,
            summary=excluded.summary,
            source=excluded.source,
            md_file=excluded.md_file,
            md_anchor=excluded.md_anchor,
            payload_json=excluded.payload_json,
            updated_at=excluded.updated_at
        """,
        (
            record["id"],
            record["type"],
            record["date"],
            record.get("time"),
            record.get("title"),
            record.get("raw_text", ""),
            record.get("summary"),
            record.get("source", "chat"),
            md_file,
            record["id"],
            payload_json,
            now,
            now,
        ),
    )


def replace_child(conn: sqlite3.Connection, table: str, entry_id: str, fields: Dict[str, object]) -> None:
    conn.execute(f"DELETE FROM {table} WHERE entry_id = ?", (entry_id,))
    columns = ["entry_id"] + list(fields.keys())
    values = [entry_id] + [fields[k] for k in fields.keys()]
    placeholders = ", ".join(["?"] * len(columns))
    col_sql = ", ".join(columns)
    conn.execute(f"INSERT INTO {table} ({col_sql}) VALUES ({placeholders})", values)


def sync_tags(conn: sqlite3.Connection, entry_id: str, tags: List[str]) -> None:
    conn.execute("DELETE FROM entry_tags WHERE entry_id = ?", (entry_id,))
    for tag in tags:
        conn.execute("INSERT OR IGNORE INTO tags (name) VALUES (?)", (tag,))
        tag_id = conn.execute("SELECT id FROM tags WHERE name = ?", (tag,)).fetchone()[0]
        conn.execute(
            "INSERT OR IGNORE INTO entry_tags (entry_id, tag_id) VALUES (?, ?)",
            (entry_id, tag_id),
        )


def append_markdown(root: Path, record: Dict) -> (str, str):
    daily_file = root / "daily" / f"{record['date']}.md"
    ensure_daily_file(daily_file)
    text = daily_file.read_text(encoding="utf-8")
    section = SECTION_TITLES[record["type"]]
    text = ensure_section(text, section)
    block = build_block(record)

    marker = f"### {record['id']}\n"
    if marker in text:
        start = text.index(marker)
        next_pos = text.find("\n### ", start + len(marker))
        if next_pos == -1:
            next_pos = len(text)
        text = text[:start] + block + text[next_pos:]
    else:
        header = f"## {section}\n"
        insert_at = text.index(header) + len(header)
        text = text[:insert_at] + "\n" + block + text[insert_at:]

    daily_file.write_text(text, encoding="utf-8")
    return str(daily_file), block


def save_records(root: Path, db_path: Path, records: List[Dict]) -> List[SaveResult]:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    results: List[SaveResult] = []
    try:
        for record in records:
            md_file, block = append_markdown(root, record)
            upsert_entry(conn, record, md_file)
            payload = record.get("payload", {}) or {}
            if record["type"] == "expense":
                replace_child(conn, "expenses", record["id"], {
                    "amount": payload.get("amount"),
                    "currency": payload.get("currency"),
                    "category": payload.get("category"),
                    "subcategory": payload.get("subcategory"),
                    "pay_method": payload.get("pay_method"),
                    "merchant": payload.get("merchant"),
                })
            elif record["type"] == "task":
                replace_child(conn, "tasks", record["id"], {
                    "status": payload.get("status"),
                    "priority": payload.get("priority"),
                    "project": payload.get("project"),
                    "due_date": payload.get("due_date"),
                    "completed_at": payload.get("completed_at"),
                })
            elif record["type"] == "schedule":
                replace_child(conn, "schedules", record["id"], {
                    "schedule_date": payload.get("schedule_date"),
                    "start_time": payload.get("start_time"),
                    "end_time": payload.get("end_time"),
                    "location": payload.get("location"),
                    "status": payload.get("status"),
                })
            elif record["type"] == "idea":
                replace_child(conn, "ideas", record["id"], {
                    "idea_type": payload.get("idea_type"),
                    "status": payload.get("status"),
                    "related_task_id": payload.get("related_task_id"),
                })
            sync_tags(conn, record["id"], record.get("tags", []))
            results.append(SaveResult(record["id"], record["type"], md_file, block, True))
        conn.commit()
    finally:
        conn.close()
    return results


def load_payload(args: argparse.Namespace) -> Dict:
    if args.stdin_json:
        return json.load(__import__("sys").stdin)
    if args.input:
        with open(args.input, "r", encoding="utf-8") as f:
            return json.load(f)
    raise SystemExit("provide --stdin-json or --input")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--db", required=True)
    parser.add_argument("--stdin-json", action="store_true")
    parser.add_argument("--input")
    args = parser.parse_args()

    payload = load_payload(args)
    records = payload.get("records") or []
    if not isinstance(records, list) or not records:
        raise SystemExit("payload.records must be a non-empty list")

    results = save_records(Path(args.root), Path(args.db), records)
    print(json.dumps({
        "saved": [r.__dict__ for r in results]
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
