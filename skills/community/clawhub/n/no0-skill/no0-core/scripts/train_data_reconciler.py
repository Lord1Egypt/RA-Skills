#!/usr/bin/env python3
"""
Reconciler for change log records: moves labeled entries from active log to archive.
(Kept as train_data_reconciler.py for backward compatibility with existing references.)
"""
import json
from pathlib import Path
from typing import Any, Dict, List

from event_logger import _build_markdown_block

BASE_DIR = Path(__file__).resolve().parent.parent

CHANGE_LOG_JSON = BASE_DIR / "change_log.json"
CHANGE_LOG_MD = BASE_DIR / "change_log.md"

ARCHIVE_JSON = BASE_DIR / "change_log_labeled.json"
ARCHIVE_MD = BASE_DIR / "change_log_labeled.md"


def is_pending(val: Any) -> bool:
    if val is None:
        return True
    raw = str(val).strip().lower()
    return raw == "" or raw == "null"


def resolve_level(row: Dict[str, Any]) -> Any:
    return row.get("level")


def load_json(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return [x for x in data if isinstance(x, dict)] if isinstance(data, list) else []
    except Exception:
        return []


def save_json(path: Path, data: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    from datetime import datetime
    now_text = datetime.now().astimezone().isoformat(timespec="seconds")

    records = load_json(CHANGE_LOG_JSON)
    if not records:
        print("no records")
        return 0

    pending = []
    labeled = []
    for row in records:
        if not isinstance(row, dict):
            continue
        if is_pending(resolve_level(row)):
            pending.append(row)
        else:
            row.setdefault("archived_record_time", now_text)
            labeled.append(row)

    if labeled:
        existing = load_json(ARCHIVE_JSON)
        seen = {str(x.get("event_id")) for x in existing if isinstance(x, dict)}
        for row in labeled:
            event_id = str(row.get("event_id"))
            if event_id and event_id not in seen:
                existing.append(row)
                seen.add(event_id)
        save_json(ARCHIVE_JSON, existing)

    save_json(CHANGE_LOG_JSON, pending)
    print(f"archived={len(labeled)} pending={len(pending)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
