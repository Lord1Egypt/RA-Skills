#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Memory Digest — weekly report generator for AI agent memory corpora.

Scans an agent workspace (MEMORY.md + memory/*.md) and produces a
human-readable digest of what happened in a date window:

  1. Activity timeline   - dated entries grouped by day, one-line summaries
  2. Project tracker     - which project names appear, with momentum (new/ongoing/stalled)
  3. Open threads        - "pending/to-confirm/waiting" items not marked done
  4. Numbers in motion   - metrics mentioned in the window and how they changed

Output: Markdown to stdout (default) or --out FILE. Use --days N to set the
window (default 7). Works with any corpus of date-named daily logs plus a
long-term MEMORY.md.

Usage:
  python3 memory_digest.py [--memory-dir DIR] [--days 7] [--out report.md] [--json]
"""

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

DATE_IN_NAME = re.compile(r"(?:^|/)(\d{4})-(\d{2})-(\d{2})\.md$")
HEADING = re.compile(r"^#{1,3}\s+(.*)$")
PENDING = re.compile(
    r"(待办|待确认|待定|待用户|悬|未完成|pending|to.?do|waiting|blocked|TODO)",
    re.IGNORECASE,
)
PROJECT_HINT = re.compile(
    r"(?:项目|project|仓库|repo|website|网站|平台|skill|plugin|essay|文书|论文|paper)",
    re.IGNORECASE,
)
METRIC = re.compile(
    r"(\d[\d,]{2,9})\s*(?:\+?\s*(?:downloads|下载|users|用户|stars|星|participants|受试))",
    re.IGNORECASE,
)


def parse_date_from_name(name: str):
    m = DATE_IN_NAME.search(name)
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def first_line_summary(text: str) -> str:
    """Best-effort one-line summary: first non-heading, non-empty line."""
    for line in text.splitlines():
        s = line.strip().lstrip("-*• ").strip()
        if not s or s.startswith("#") or s.startswith("```"):
            continue
        if len(s) < 6:  # skip stray fragments
            continue
        return (s[:140] + "…") if len(s) > 140 else s
    return "(empty entry)"


def collect(memory_dir: Path, start: dt.date, end: dt.date):
    entries = []  # (date, filename, text)
    memsub = memory_dir / "memory"
    candidates = []
    if memsub.is_dir():
        candidates = list(memsub.glob("*.md"))
    for p in sorted(candidates):
        d = parse_date_from_name(p.name)
        if d and start <= d <= end:
            entries.append((d, p.name, p.read_text(encoding="utf-8", errors="replace")))
    entries.sort()
    return entries


def extract_sections(text: str):
    """Return list of (heading, body_lines) preserving order."""
    sections = []
    cur_h, cur = None, []
    for line in text.splitlines():
        m = HEADING.match(line)
        if m:
            if cur_h is not None:
                sections.append((cur_h, cur))
            cur_h, cur = m.group(1).strip(), []
        else:
            cur.append(line)
    if cur_h is not None:
        sections.append((cur_h, cur))
    return sections


def build_digest(memory_dir: Path, days: int, today: dt.date):
    end = today
    start = today - dt.timedelta(days=days - 1)
    entries = collect(memory_dir, start, end)

    report = {
        "window": (str(start), str(end)),
        "days_with_entries": len(entries),
        "timeline": [],
        "projects": {},
        "open_threads": [],
        "metrics": [],
    }

    for d, fname, text in entries:
        sections = extract_sections(text)
        topics = []
        for h, body in sections:
            body_text = "\n".join(body)
            if PENDING.search(body_text):
                # capture pending lines (trimmed)
                for line in body:
                    s = line.strip().lstrip("-*• ").strip()
                    if s and PENDING.search(s):
                        report["open_threads"].append(
                            {"date": str(d), "heading": h, "item": (s[:160])}
                        )
            if PROJECT_HINT.search(h) or PROJECT_HINT.search(body_text[:200]):
                topics.append(h)
            for m in METRIC.finditer(body_text):
                report["metrics"].append(
                    {
                        "date": str(d),
                        "heading": h,
                        "value": m.group(1),
                        "raw": m.group(0)[:60],
                    }
                )
        report["timeline"].append(
            {
                "date": str(d),
                "file": fname,
                "summary": first_line_summary(text),
                "sections": len(sections),
                "topics": topics[:5],
            }
        )
        # project mentions
        for h, _ in sections:
            for token in re.findall(r"[\w\u4e00-\u9fff\-]{2,30}", h):
                if PROJECT_HINT.search(token) or re.search(r"[A-Za-z]{3,}", token):
                    key = token
                    report["projects"].setdefault(key, {"days": [], "headings": set()})
                    report["projects"][key]["days"].append(str(d))
                    report["projects"][key]["headings"].add(h)

    # momentum: last seen date per project
    for key, info in report["projects"].items():
        days_seen = sorted(set(info["days"]))
        info["last_seen"] = days_seen[-1]
        info["days_count"] = len(days_seen)
        last_delta = (end - dt.date.fromisoformat(days_seen[-1])).days
        if days_seen[-1] == days_seen[0] and info["days_count"] == 1 and last_delta <= 1:
            info["momentum"] = "new"
        elif last_delta <= 2:
            info["momentum"] = "ongoing"
        else:
            info["momentum"] = "stalled"
        info["headings"] = sorted(info["headings"])[:3]
        del info["days"]
    return report


def render_markdown(rep: dict) -> str:
    lines = []
    lines.append(f"# Agent Memory Digest")
    s, e = rep["window"]
    lines.append(f"\n**Window:** {s} → {e} ｜ **Days with entries:** {rep['days_with_entries']}\n")

    lines.append("## Activity timeline\n")
    for t in rep["timeline"]:
        topics = f" ｜ {' / '.join(t['topics'])}" if t["topics"] else ""
        lines.append(f"- **{t['date']}** ({t['sections']} sections{topics}): {t['summary']}")

    if rep["projects"]:
        lines.append("\n## Projects in motion\n")
        projs = sorted(
            rep["projects"].items(),
            key=lambda kv: (kv[1]["last_seen"], kv[1]["days_count"]),
            reverse=True,
        )
        for name, info in projs[:15]:
            icon = {"new": "🆕", "ongoing": "▶️", "stalled": "⏸️"}[info["momentum"]]
            lines.append(
                f"- {icon} **{name}** — {info['days_count']} day(s), last seen {info['last_seen']} ({info['momentum']})"
            )

    if rep["open_threads"]:
        lines.append("\n## Open threads (pending / to-confirm)\n")
        seen = set()
        for th in rep["open_threads"]:
            k = th["item"][:60]
            if k in seen:
                continue
            seen.add(k)
            lines.append(f"- [{th['date']}｜{th['heading']}] {th['item']}")

    if rep["metrics"]:
        lines.append("\n## Numbers in motion\n")
        seen = set()
        for met in rep["metrics"]:
            k = (met["heading"], met["raw"])
            if k in seen:
                continue
            seen.add(k)
            lines.append(f"- [{met['date']}｜{met['heading']}] {met['raw']}")

    if rep["days_with_entries"] == 0:
        lines.append("\n_(No dated entries in the window. If daily flushes are expected, something may be wrong._")

    lines.append("\n---\n_Generated by memory-digest. Verify pending items before acting on them._")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Agent memory weekly digest")
    ap.add_argument("--memory-dir", default=".", help="Workspace root containing memory/")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--out")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    memory_dir = Path(args.memory_dir).resolve()
    rep = build_digest(memory_dir, args.days, dt.date.today())

    if args.json:
        out = json.dumps(rep, ensure_ascii=False, indent=2)
    else:
        out = render_markdown(rep)

    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    sys.exit(main())
