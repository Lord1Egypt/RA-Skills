#!/usr/bin/env python3
"""Scrub legacy raw session identifiers from Hui-Yi metadata.

This is mainly for users upgrading from pre-1.2.9 Hui-Yi builds. Newer builds
write sha256 fingerprints by default, but older tags.json files may still have
raw session keys in last_session_key or signal_history.
"""
from __future__ import annotations

import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

import argparse
import json
from datetime import date

from core.common import load_tags_payload, normalize_signal_history, resolve_memory_root, save_json, session_fingerprint


def scrub_payload(payload: dict) -> tuple[int, int]:
    changed_notes = 0
    changed_fields = 0
    notes = payload.get("notes", []) if isinstance(payload.get("notes"), list) else []
    for note in notes:
        note_changed = False
        raw_last = note.get("last_session_key")
        if isinstance(raw_last, str) and raw_last and not raw_last.startswith("sha256:"):
            note["last_session_key"] = session_fingerprint(raw_last)
            changed_fields += 1
            note_changed = True

        raw_history = note.get("signal_history") if isinstance(note.get("signal_history"), list) else []
        normalized = normalize_signal_history(raw_history)
        deduped: list[str] = []
        seen: set[str] = set()
        for item in normalized:
            if item in seen:
                continue
            seen.add(item)
            deduped.append(item)
        deduped = deduped[-20:]
        if deduped != raw_history:
            note["signal_history"] = deduped
            changed_fields += 1
            note_changed = True

        if note_changed:
            changed_notes += 1
    return changed_notes, changed_fields


def main() -> int:
    parser = argparse.ArgumentParser(description="Scrub legacy raw Hui-Yi session metadata")
    parser.add_argument("--memory-root", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    memory_root = resolve_memory_root(args.memory_root)
    payload = load_tags_payload(memory_root)
    changed_notes, changed_fields = scrub_payload(payload)

    if changed_fields and not args.dry_run:
        payload.setdefault("_meta", {})["updated"] = date.today().isoformat()
        save_json(memory_root / "tags.json", payload)

    result = {
        "ok": True,
        "memoryRoot": str(memory_root),
        "dryRun": args.dry_run,
        "changedNotes": changed_notes,
        "changedFields": changed_fields,
        "written": bool(changed_fields and not args.dry_run),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        mode = "DRY-RUN" if args.dry_run else "APPLIED"
        print(f"{mode}: scrubbed {changed_fields} field(s) across {changed_notes} note(s). memory root: {memory_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
