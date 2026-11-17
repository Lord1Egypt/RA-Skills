#!/usr/bin/env python3
"""Thread-safe and process-safe queue appending for kb-queue.json via fcntl flock."""
import fcntl, json, os, pathlib, re


def _parse_markdown_entry(entry_line: str):
    """Parse markdown-style queue entry into structured record."""
    m = re.match(
        r'- \[(.*?)\]\((.*?)\)(?:\s*-\s*(\S+))?(?:\s*-\s*(.+))?(?:\s*-\s*\d{4}-\d{2}-\d{2})?',
        entry_line.strip(),
    )
    if m:
        title = m.group(1).strip()
        url = m.group(2).strip()
        item_type = m.group(3).strip() if m.group(3) else "unknown"
        source = m.group(4).strip() if m.group(4) else ""
    else:
        title = entry_line.strip()
        url = ""
        item_type = "unknown"
        source = ""
    return {
        "type": "url",
        "url": url,
        "title": title,
        "source": source or item_type,
    }


def append_to_queue(entry_line: str, queue_path=None):
    """Append a structured record to kb-queue.json with file locking."""
    if queue_path is None:
        queue_path = (
            pathlib.Path.home()
            / ".openclaw"
            / "workspace"
            / "memory"
            / "kb-queue.json"
        )
    queue_path = pathlib.Path(queue_path)
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    record = _parse_markdown_entry(entry_line)

    with open(queue_path, "a+", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        f.seek(0)
        try:
            content = f.read()
            data = json.loads(content) if content.strip() else []
        except json.JSONDecodeError:
            data = []
        data.append(record)
        f.seek(0)
        f.truncate()
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)

    return {"pendingPath": str(queue_path), "entry": record}
