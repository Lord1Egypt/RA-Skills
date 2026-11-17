#!/usr/bin/env python3
"""Detect and remove restricted fragments with a tested pattern pack.

Standard library only. Generated skills import `load_pack`, `redact` and
`find` (or copy them) instead of writing their own narrower regex. A pack is
JSON with check.value (regex), redact.{replacement,collapse_spaces,examples},
must_match and must_not_match. Packs live in assets/patterns/; "@patterns/x.json"
resolves there.

    python -B scripts/redact_patterns.py --pack @patterns/cn-currency.json --verify
        run the pack's own positive, negative and redaction examples
    python -B scripts/redact_patterns.py --pack @patterns/cn-currency.json < in.txt > out.txt
        remove every restricted fragment from stdin

Apply the SAME redact() to every free-text field of every delivery view
(items, notes, lists, conflict details, reminders, reports); never narrow the
scope to one column. Exit 0 ok, 1 verify failed, 2 bad pack/input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_pack(ref: str, base: Path | None = None) -> dict:
    path = ROOT / "assets" / ref[1:] if ref.startswith("@") else (base or Path.cwd()) / ref
    pack = json.loads(path.read_text(encoding="utf-8-sig"))
    value = pack["check"]["value"]
    if pack["check"].get("type") != "not_regex" or not isinstance(value, str) or not value:
        raise ValueError("pack needs a not_regex check with a regex value")
    pack["_regex"] = re.compile(value, re.MULTILINE)
    return pack


def find(text: str, pack: dict) -> list[tuple[int, int]]:
    """Spans of restricted fragments in text."""
    return [m.span() for m in pack["_regex"].finditer(text)]


def redact(text: str, pack: dict) -> str:
    """Remove every restricted fragment; collapse leftover runs of blanks."""
    options = pack.get("redact", {})
    text = pack["_regex"].sub(options.get("replacement", ""), text)
    if options.get("collapse_spaces", True):
        text = re.sub(r"[ \t]{2,}", " ", text)
        text = "\n".join(line.strip() for line in text.split("\n"))
    return text


def verify(pack: dict) -> dict:
    missed = [i for i, t in enumerate(pack.get("must_match", [])) if not find(t, pack)]
    false_hits = [i for i, t in enumerate(pack.get("must_not_match", [])) if find(t, pack)]
    wrong = [i for i, e in enumerate(pack.get("redact", {}).get("examples", [])) if redact(e["in"], pack) != e["out"]]
    leftovers = [i for i, t in enumerate(pack.get("must_match", [])) if find(redact(t, pack), pack)]
    ok = not (missed or false_hits or wrong or leftovers)
    return {"status": "pass" if ok else "fail", "missed_positive_index": missed, "false_positive_index": false_hits,
            "wrong_redaction_index": wrong, "residual_after_redact_index": leftovers}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pack", required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    try:
        pack = load_pack(args.pack)
    except (OSError, ValueError, KeyError, re.error, json.JSONDecodeError):
        print(json.dumps({"status": "error", "error": "unreadable or invalid pattern pack"}, ensure_ascii=False))
        return 2
    if args.verify:
        result = verify(pack)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "pass" else 1
    sys.stdout.write(redact(sys.stdin.read(), pack))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
