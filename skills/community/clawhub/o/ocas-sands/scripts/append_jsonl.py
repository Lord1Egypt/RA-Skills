#!/usr/bin/env python3
"""
Safe JSONL append helper for Sands.

Usage:
    python3 append_jsonl.py <jsonl_path> '<json_record>'

Example:
    python3 append_jsonl.py evidence.jsonl '{"timestamp":"2026-06-05T07:00:00-07:00","command":"sands.schedule.conflicts"}'

Reads the existing file, appends the new record, writes the full file back,
and verifies line count increased by 1.
"""
import json
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 append_jsonl.py")
    sys.exit(0)


def append_jsonl(path: str, record: dict) -> int:
    """Append a record to a JSONL file. Returns new line count."""
    with open(path, 'r') as f:
        lines = [l for l in f.readlines() if l.strip()]

    original_count = len(lines)
    lines.append(json.dumps(record) + '\n')

    with open(path, 'w') as f:
        f.writelines(lines)

    assert len(lines) == original_count + 1, (
        f"Line count mismatch: expected {original_count + 1}, got {len(lines)}"
    )
    return len(lines)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <jsonl_path> '<json_record>'")
        sys.exit(1)

    path = sys.argv[1]
    record = json.loads(sys.argv[2])
    new_count = append_jsonl(path, record)
    print(f"Appended. File now has {new_count} records.")
