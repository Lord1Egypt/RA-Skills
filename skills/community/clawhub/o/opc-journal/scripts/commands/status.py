"""Journal command: status."""
import glob
import os
from datetime import datetime
from pathlib import Path

from utils.storage import build_customer_dir
from scripts.commands._meta import read_meta


def _parse_md_date(basename: str) -> str:
    m = __import__("re").search(r"(\d{2}-\d{2}-\d{2})\.md$", basename)
    if m:
        return m.group(1)
    return "00-00-00"


def run(customer_id: str, args: dict) -> dict:
    """Return raw journal statistics. Message generation is left to the caller (LLM)."""
    base = os.path.expanduser(build_customer_dir(customer_id))
    memory_dir = os.path.join(base, "memory")
    entry_count = 0
    first_entry_date = None
    latest = None

    if os.path.exists(memory_dir):
        files = glob.glob(os.path.join(memory_dir, "*.md"))
        files.sort(key=lambda f: _parse_md_date(os.path.basename(f)), reverse=True)
        for f in files:
            content = Path(f).read_text(encoding="utf-8")
            if "type: entry" in content:
                entry_count += 1
                date_str = _parse_md_date(os.path.basename(f))
                if latest is None:
                    latest = date_str
                # Since files are sorted reverse (newest first), keep updating first_entry_date
                # until we reach the oldest file with an entry.
                first_entry_date = date_str

    meta = read_meta(customer_id) or {}
    started_day = meta.get("started_day", 1)

    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "started_day": started_day,
            "total_entries": entry_count,
            "first_entry_date": first_entry_date or "N/A",
            "latest_entry_date": latest or "N/A",
            "journal_active": entry_count > 0,
        },
        "message": f"Status retrieved for {customer_id}",
    }
