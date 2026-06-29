#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_edits.py — backfill an "我的改动-交给AI.json" (exported by the lite editor's
「导出改动给AI」 button) into the ORIGINAL source HTML file, by CONTENT match.

JSON format (produced by inject.py v3):
  {"changes": [{"orig": "<original innerHTML>", "new": "<edited innerHTML>"}, ...]}

Why content-match (not position index): the user edits a rendered copy; the only
reliable anchor is the original text itself. We locate each `orig` inside the source
and replace it with `new`. Immune to structure drift and never corrupts unrelated parts.

Usage:
  python apply_edits.py <changes.json> <source.html>
  python apply_edits.py <changes.json> <source.html> --dry-run   # report only, no write

Safety:
  - Exact match preferred. If `orig` appears exactly once -> replace.
  - If it appears multiple times (ambiguous) -> SKIP and warn (never guess).
  - If not found exactly, try a whitespace-folded match mapped back to the source.
  - Anything unmatched is reported; the source is only written if >=1 change applied.
"""
import sys, os, json, re


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def apply_changes(changes, src_path, dry_run=False):
    src = open(src_path, encoding="utf-8").read()
    applied, failed = 0, []
    for ch in changes:
        orig = ch.get("orig"); new = ch.get("new")
        if orig is None or new is None:
            failed.append("(missing orig/new)"); continue
        if norm(orig) == norm(new):
            continue
        # 1) exact, unique
        n = src.count(orig)
        if n == 1:
            src = src.replace(orig, new); applied += 1; continue
        if n > 1:
            failed.append("orig appears %d times (ambiguous): %s" % (n, norm(orig)[:50])); continue
        # 2) whitespace-folded unique match -> build a tolerant regex from orig
        flat = re.sub(r"\s+", " ", src)
        target = norm(orig)
        if target and flat.count(target) == 1:
            pat = re.sub(r"\s+", r"\\s+", re.escape(orig))
            m = re.search(pat, src)
            if m:
                src = src[:m.start()] + new + src[m.end():]; applied += 1; continue
        failed.append("orig not found in source: %s" % (norm(orig)[:50]))
    if not dry_run and applied:
        open(src_path, "w", encoding="utf-8").write(src)
    print("applied %d change(s)%s to %s" % (applied, " (dry-run, not written)" if dry_run else "", src_path))
    if failed:
        print("NOT applied (needs human check):")
        for f in failed:
            print("  -", f)
    return applied, failed


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print("usage: python apply_edits.py <changes.json> <source.html> [--dry-run]")
        sys.exit(1)
    json_path, src_path = args[0], args[1]
    if not os.path.isfile(src_path):
        print("ERROR: source not found:", src_path); sys.exit(1)
    data = json.load(open(json_path, encoding="utf-8"))
    if "changes" not in data:
        if "edits" in data or (isinstance(data, dict) and all(re.match(r"t\d+$", k) for k in data)):
            print("⚠️  Old position-index format detected — indexes may have drifted, refusing to apply.")
            print("    Re-export with the latest editable HTML (the 「导出改动给AI」 button gives the new format).")
            sys.exit(2)
        print("Unrecognized JSON structure (expected a 'changes' array)."); sys.exit(2)
    apply_changes(data["changes"], src_path, dry_run=("--dry-run" in sys.argv))


if __name__ == "__main__":
    main()
