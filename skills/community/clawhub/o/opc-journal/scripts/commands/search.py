"""Journal command: search - actual local file search."""
import glob
import os
import re
from pathlib import Path

from utils.storage import build_customer_dir
from utils.parsing import extract_entries
from scripts.commands._meta import get_language


def _get_context(text: str, start: int, end: int, context_len: int = 40) -> str:
    """Get context around a match."""
    context_start = max(0, start - context_len)
    context_end = min(len(text), end + context_len)
    prefix = "..." if context_start > 0 else ""
    suffix = "..." if context_end < len(text) else ""
    return prefix + text[context_start:context_end] + suffix


def run(customer_id: str, args: dict) -> dict:
    """Search journal entries locally in memory files."""
    query = args.get("query", "").strip()
    limit = args.get("limit", 10)
    case_sensitive = args.get("case_sensitive", False)

    lang = get_language(customer_id)
    base = os.path.expanduser(build_customer_dir(customer_id))
    memory_dir = os.path.join(base, "memory")

    if not os.path.exists(memory_dir):
        return {
            "status": "success",
            "result": {
                "customer_id": customer_id,
                "query": query,
                "matches": [],
                "total_matches": 0,
                "language": lang,
            },
            "message": "No memory directory found",
        }

    files = sorted(glob.glob(os.path.join(memory_dir, "*.md")))
    matches = []
    flags = 0 if case_sensitive else re.IGNORECASE

    for f in files:
        content = Path(f).read_text(encoding="utf-8")

        # Skip if query provided and not found in content
        if query and not re.search(re.escape(query), content, flags):
            continue

        # Extract entries from the file
        entries = extract_entries(content)
        for entry in entries:
            if query:
                body = entry.get("body", "")
                match_positions = []
                for m in re.finditer(re.escape(query), body, flags):
                    match_positions.append({
                        "start": m.start(),
                        "end": m.end(),
                        "context": _get_context(body, m.start(), m.end()),
                    })
                if match_positions:
                    entry["matches"] = match_positions
                    entry["file"] = f
                    matches.append(entry)
            else:
                entry["file"] = f
                matches.append(entry)

    # Sort by date (newest first) and limit results
    matches.sort(key=lambda x: x.get("date", "00-00-00"), reverse=True)
    total = len(matches)
    matches = matches[:limit]

    return {
        "status": "success",
        "result": {
            "customer_id": customer_id,
            "query": query,
            "matches": matches,
            "total_matches": total,
            "returned": len(matches),
            "language": lang,
        },
        "message": f"Found {total} match(es)" if query else f"Found {total} entries",
    }
