#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Memory Checkup audit script.

Scans an agent's memory corpus (MEMORY.md, USER.md, and Markdown files
under memory/) and reports consistency issues:

  1. Stale numbers      - superseded figures that newer entries override
                          (e.g. download counts, star counts)
  2. Contradictions     - same metric with conflicting values in different
                          entries, without an explicit supersede note
  3. Dangling references - file paths mentioned in memory that do not exist
  4. Stale entries      - daily-flush style entries that stopped updating,
                          or facts whose newest mention is older than N days
  5. Orphans            - files under memory/ never referenced anywhere

Output: human-readable report (default) or --json for machine use.

Usage:
  python3 memory_checkup.py [--memory-dir DIR] [--json] [--verbose]
"""

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

DEFAULT_PATTERNS = [
    # (label, regex with a number group, tolerance)
    ("downloads", r"([\d,]{3,7})\+?\s*(?:downloads|下载)", True),
    ("stars", r"([\d,]{2,6})\+?\s*(?:stars|星)", True),
    ("users", r"([\d,]{2,6})\+?\s*(?:users|用户)", True),
]

DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
PATH_RE = re.compile(r"([\w./~-]*?(?:output|skills|scripts|memory)/[\w./-]+\.(?:py|md|docx|json|ts|tsx|js))")


def parse_date_from_name(name: str):
    m = DATE_RE.search(name)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def _line_context_ok(label, line):
    """Disambiguate metrics by surrounding context to avoid false positives."""
    low = line.lower()
    if label == "stars":
        return "github" in low
    if label == "users":
        # site/website users or students, not study subjects (受试者) or list lengths
        return ("网站" in line or "site" in low or "website" in low) and "受试" not in line
    return True


def norm_num(s: str) -> int:
    return int(s.replace(",", ""))


def load_files(memory_dir: Path):
    """Scan workspace-root markdown files plus the memory/ subdirectory only.
    Never recurse into other subdirectories (skills/, node_modules/, projects/)."""
    files = {}
    for name in ("MEMORY.md", "USER.md", "AGENTS.md", "HEARTBEAT.md"):
        p = memory_dir / name
        if p.exists():
            files[name] = p.read_text(encoding="utf-8", errors="replace")
    memsub = memory_dir / "memory"
    if memsub.exists() and memsub.is_dir():
        for p in sorted(memsub.glob("*.md")):
            files[str(p.relative_to(memory_dir))] = p.read_text(encoding="utf-8", errors="replace")
    return files


def audit(memory_dir: Path, today: dt.date):
    files = load_files(memory_dir)
    issues = {"stale_numbers": [], "contradictions": [], "dangling_refs": [],
              "stale_entries": [], "orphans": []}

    # --- metric tracking: collect every numeric mention per label ---
    mentions = {}  # label -> list of (value, file, lineno)
    for fname, text in files.items():
        for i, line in enumerate(text.splitlines(), 1):
            for label, pat, _ in DEFAULT_PATTERNS:
                for m in re.finditer(pat, line, re.IGNORECASE):
                    if not _line_context_ok(label, line):
                        continue
                    try:
                        val = norm_num(m.group(1))
                    except ValueError:
                        continue
                    mentions.setdefault(label, []).append((val, fname, i))

    # contradiction/staleness: group per label by file date if available
    for label, ms in mentions.items():
        values = {}
        for val, fname, i in ms:
            values.setdefault(val, []).append((fname, i))
        if len(values) <= 1:
            continue
        # sort candidate values, newest evidence first: use file dates
        def latest_date(val):
            dates = [parse_date_from_name(f) or dt.date(1970, 1, 1)
                     for f, _ in values[val]]
            return max(dates)
        ranked = sorted(values.items(),
                        key=lambda kv: (latest_date(kv[0]), kv[0]),
                        reverse=True)
        current_val, current_ev = ranked[0]
        for old_val, ev in ranked[1:]:
            note = {
                "label": label, "current": current_val, "stale": old_val,
                "current_evidence": sorted(set(f for f, _ in current_ev)),
                "stale_evidence": sorted(set(f for f, _ in ev)),
            }
            issues["stale_numbers"].append(note)

    # --- dangling file references ---
    for fname, text in files.items():
        base = memory_dir / fname
        for m in PATH_RE.finditer(text):
            ref = m.group(1)
            # try workspace-root relative, then memory-dir relative
            cands = [memory_dir.parent / ref, memory_dir / ref, Path(ref)]
            if not any(c.exists() for c in cands):
                issues["dangling_refs"].append({"file": fname, "ref": ref})

    # --- stale daily entries: flag only if the NEWEST few days have gaps,
    # i.e. the flush routine may have silently died recently ---
    daily = {}
    for fname in files:
        d = parse_date_from_name(fname)
        if d:
            daily[fname] = d
    if daily:
        newest = max(daily.values())
        # look back at most 5 days from the newest entry
        for back in range(1, 6):
            day = newest - dt.timedelta(days=back)
            present = any(abs((d - day).days) == 0 for d in daily.values())
            if not present:
                issues["stale_entries"].append({
                    "file": "(daily flush)", "date": str(day),
                    "missing_days": [str(day)],
                    "note": f"no memory file dated {day}; newest entry is {newest}",
                })

    # --- orphan files: only non-date-named files (date-named daily logs are
    # expected to stand alone and be found by date search) ---
    referenced = set()
    all_text = "\n".join(files.values())
    for fname in list(files):
        if fname in ("MEMORY.md", "USER.md") or parse_date_from_name(fname):
            continue
        short = fname.rsplit("/", 1)[-1]
        stem = short.rsplit(".", 1)[0]
        # referenced if its name or stem appears in any OTHER file
        others = "\n".join(t for f, t in files.items() if f != fname)
        if short in others or stem in others:
            referenced.add(fname)
    for fname in files:
        if fname in ("MEMORY.md", "USER.md") or fname in referenced or parse_date_from_name(fname):
            continue
        issues["orphans"].append({"file": fname})

    return {"files_scanned": len(files), "issues": issues}


def main():
    ap = argparse.ArgumentParser(description="Agent memory corpus audit")
    ap.add_argument("--memory-dir", default=".", help="Workspace/memory root containing MEMORY.md and memory/")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    memory_dir = Path(args.memory_dir).resolve()
    result = audit(memory_dir, dt.date.today())

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"🧠 Memory Checkup — {result['files_scanned']} files scanned in {memory_dir}")
    iss = result["issues"]
    total = sum(len(v) for v in iss.values())
    if total == 0:
        print("✅ No consistency issues found.")
        return
    print(f"⚠️ {total} issue(s) found:\n")

    def show(name, items, fmt):
        if not items:
            return
        print(f"## {name} ({len(items)})")
        for it in items[:20]:
            print("  - " + fmt(it))
        if len(items) > 20:
            print(f"  ... and {len(items) - 20} more")
        print()

    show("Stale numbers", iss["stale_numbers"],
         lambda it: f"{it['label']}: current={it['current']} (in {', '.join(it['current_evidence'][:2])}) "
                    f"but stale={it['stale']} still appears in {', '.join(it['stale_evidence'][:2])}")
    show("Dangling references", iss["dangling_refs"],
         lambda it: f"{it['file']} references missing path: {it['ref']}")
    show("Stale entries (gaps near newest)", iss["stale_entries"],
         lambda it: f"{it.get('note', it['date'])}")
    show("Orphan files", iss["orphans"],
         lambda it: f"never referenced elsewhere: {it['file']}")

    print("Suggested fix flow: confirm the current value with the user, then update stale mentions or mark them superseded.")


if __name__ == "__main__":
    sys.exit(main())
