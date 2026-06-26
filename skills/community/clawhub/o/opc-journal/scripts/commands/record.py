"""Journal command: record."""
import glob
import json
import os
import uuid
from pathlib import Path

from utils.storage import build_customer_dir, build_memory_path, write_memory_file
from utils.timezone import now_tz
from scripts.commands._meta import get_language, read_meta, write_meta


def generate_entry_id() -> str:
    today = now_tz().strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:6].upper()
    return f"JE-{today}-{suffix}"


def _is_first_entry(customer_id: str) -> bool:
    meta = read_meta(customer_id)
    if meta is not None and meta.get("total_entries", 0) > 0:
        return False
    # Fallback: scan files if meta is missing or corrupt
    memory_dir = os.path.expanduser(Path(build_customer_dir(customer_id)) / "memory")
    if not os.path.exists(memory_dir):
        return True
    files = [f for f in glob.glob(os.path.join(memory_dir, "*.md")) if os.path.basename(f) != "dreams.md"]
    for f in files:
        content = Path(f).read_text(encoding="utf-8")
        if "type: entry" in content:
            return False
    return True


def run(customer_id: str, args: dict) -> dict:
    """Record a journal entry. Emotional interpretation is left to the caller (LLM)."""
    content = args.get("content", "")
    lang = get_language(customer_id)
    if not content:
        return {"status": "error", "result": None, "message": "content is required"}

    entry_id = generate_entry_id()
    day = args.get("day", 1)
    metadata = args.get("metadata", {})
    today_str = now_tz().strftime("%d-%m-%y")
    iso_time = now_tz().isoformat()

    # Do NOT hardcode emotion descriptions. Accept caller-provided state or leave empty.
    emotional_state = metadata.get("emotional_state", "")

    is_first = _is_first_entry(customer_id)

    entry_text = f"""---
type: entry
date: {today_str}
day: {day}
entry_id: {entry_id}
language: {lang}
emotion: {emotional_state}
---

## Entry - {entry_id}

Day {day} | {iso_time}

{content}

### Metadata
```json
{json.dumps(metadata, indent=2, ensure_ascii=False)}
```
"""

    memory_path = build_memory_path(customer_id)
    write_result = write_memory_file(memory_path, entry_text)

    meta = read_meta(customer_id)
    if meta:
        meta["total_entries"] = meta.get("total_entries", 0) + 1
        meta["last_recorded_at"] = iso_time
        write_meta(customer_id, meta)

    if write_result["success"]:
        return {
            "status": "success",
            "result": {
                "entry_id": entry_id,
                "customer_id": customer_id,
                "day": day,
                "language": lang,
                "is_first_entry": is_first,
                "memory_path": memory_path,
                "recorded_at": iso_time,
            },
            "message": f"Entry {entry_id} recorded",
        }

    return {
        "status": "error",
        "result": None,
        "message": f"Failed to write entry: {write_result.get('error')}",
    }
