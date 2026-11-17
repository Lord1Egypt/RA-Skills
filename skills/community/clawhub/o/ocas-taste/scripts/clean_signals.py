"""Garbage signal cleanup helper.

Removes signals with no real venue and deduplicates across
(venue_name, event_date, extraction_source, domain). Also filters
generic calendar meal-titles (Breakfast, Lunch, Dinner, Brunch) that
aren't real venue names. Writes the cleaned set back to the same JSONL file.

Usage:
    python scripts/clean_signals.py /path/to/signals.jsonl
"""
import sys
if __name__ == "__main__" and ("--help" in sys.argv or "-h" in sys.argv):
    print('Remove generic meal titles and deduplicate signals.jsonl.')
    print("Usage: clean_signals.py [options]")
    print("Run with no arguments for default behavior; see SKILL.md for flags.")
    print("  -h, --help  Show this help message")
    sys.exit(0)

import json
import re
import sys
from pathlib import Path

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 clean_signals.py")
    sys.exit(0)



GENERIC_MEAL_TITLES = frozenset({
    "breakfast", "lunch", "dinner", "brunch",
    "breakfast/lunch", "breakfast / lunch",
})

GENERIC_MEAL_RE = re.compile(
    r"^(breakfast|lunch|dinner|brunch)(\s+/|/\s+.*|$)",
    re.IGNORECASE,
)


def _is_generic_meal(venue_name: str) -> bool:
    """Check if venue_name is a generic calendar meal title, not a real venue."""
    name_lower = venue_name.strip().lower()
    if name_lower in GENERIC_MEAL_TITLES:
        return True
    if GENERIC_MEAL_RE.match(venue_name):
        return True
    return False


def clean(signals_path: Path) -> tuple[int, int]:
    with signals_path.open() as fh:
        signals = [json.loads(line) for line in fh if line.strip()]

    total = len(signals)
    clean_signals = [
        s for s in signals
        if s.get("venue_name") not in (None, "Unknown", "")
        and not _is_generic_meal(s.get("venue_name", ""))
    ]

    seen: set[tuple[str, str, str, str]] = set()
    unique: list[dict] = []
    for s in clean_signals:
        key = (
            s.get("venue_name", ""),
            s.get("event_date", "")[:10],
            s.get("extraction_source", ""),
            s.get("domain", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(s)

    with signals_path.open("w") as fh:
        for s in unique:
            fh.write(json.dumps(s) + "\n")

    return total, len(unique)


if __name__ == "__main__":
    path = Path(sys.argv[1])
    before, after = clean(path)
    print(f"cleaned {path}: {before} -> {after}")