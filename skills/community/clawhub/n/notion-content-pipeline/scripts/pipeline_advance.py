#!/usr/bin/env python3
"""pipeline_advance.py — Advance a blog post through the content pipeline.

Automates the round-trip for a single blog post:
  1. Pull Nissan's edits from Notion → local markdown
  2. Humanize (mechanical patterns in Python + flags LLM pass needed)
  3. Fact-check (via skills/fact-checker/scripts/fact_check.py if available)
  4. Push humanized version back to Notion
  5. Update status in Content Pipeline DB

Usage:
  python3 pipeline_advance.py advance content/blog-post.md [--skip-humanize]
      [--skip-factcheck] [--dry-run]

Environment:
  NOTION_API_KEY        Notion integration token (required)
  NOTION_PARENT_PAGE_ID Parent page for sandbox content (required)
  NOTION_SYNC_MAP       Path to sync map JSON (default: notion_sync_map.json)
  CONTENT_DIR           Content directory (default: ./content)
  NOTION_PIPELINE_DB_ID Pipeline DB ID (falls back to hardcoded constant)
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# ── Resolve workspace root and sibling scripts ────────────────────────────────

_SCRIPTS_DIR = Path(__file__).resolve().parent
_SKILL_DIR   = _SCRIPTS_DIR.parent
_WORKSPACE   = _SKILL_DIR.parent.parent   # workspace/skills/<skill>/scripts → workspace

# Add scripts dir so we can import notion_content_sync directly
sys.path.insert(0, str(_SCRIPTS_DIR))

from notion_content_sync import (   # noqa: E402
    _get_notion_key,
    _get_parent_page_id,
    _get_sync_map_path,
    _req,
    cmd_pull,
    cmd_push,
)

# ── Constants ─────────────────────────────────────────────────────────────────

PIPELINE_DB_ID = os.environ.get(
    "NOTION_PIPELINE_DB_ID", "312c9a82-0734-81bd-81a6-e58d0365e404"
)

FACT_CHECKER_SCRIPT = _WORKSPACE / "skills" / "fact-checker" / "scripts" / "fact_check.py"
PYTHON = "/Users/loki/.pyenv/versions/3.14.3/bin/python3"

# Status machine — only these two automatic transitions are allowed
STATUS_TRANSITIONS: dict[str, str] = {
    "Draft":     "Humanized",
    "Humanized": "In Review",
}

# ── Mechanical humanizer patterns ─────────────────────────────────────────────

# (compiled_regex, replacement_string)
# Replacements are intentionally conservative — only clear one-to-one swaps.
_WORD_REPLACEMENTS: list[tuple[re.Pattern, str]] = [
    # Filler sentence openers
    (re.compile(r"^Additionally,\s+", re.MULTILINE), "Also, "),
    (re.compile(r"^Moreover,\s+",     re.MULTILINE), "Also, "),
    (re.compile(r"^Furthermore,\s+",  re.MULTILINE), "Also, "),
    # Verbose constructions
    (re.compile(r"\bIn order to\b",              re.IGNORECASE), "To"),
    (re.compile(r"\bdue to the fact that\b",     re.IGNORECASE), "because"),
    (re.compile(r"\bat this point in time\b",    re.IGNORECASE), "now"),
    (re.compile(r"[Ii]t is important to note that\s*"),           ""),
    (re.compile(r"[Ii]t's important to note that\s*"),            ""),
    # Copula avoidance
    (re.compile(r"\bserves as\b",  re.IGNORECASE), "is"),
    (re.compile(r"\bstands as\b",  re.IGNORECASE), "is"),
    # Heavy AI vocabulary (safe swaps only)
    (re.compile(r"\butilize\b",    re.IGNORECASE), "use"),
    (re.compile(r"\butilization\b",re.IGNORECASE), "use"),
    (re.compile(r"\bleverage\b(?!\s+\w+\s+(?:ratio|point|buy))",
                re.IGNORECASE),                   "use"),
    (re.compile(r"\bdelve\b",      re.IGNORECASE), "explore"),
    (re.compile(r"\bshowcase\b",   re.IGNORECASE), "show"),
    (re.compile(r"\bboasts\b",     re.IGNORECASE), "has"),
    (re.compile(r"\bboast\b",      re.IGNORECASE), "have"),
]

# Em dash → comma (but not inside code blocks)
_EM_DASH_RE = re.compile(r"\s*—\s*")

# Curly quotes → straight quotes
_CURLY_OPEN_RE  = re.compile(r"[\u201c\u2018]")
_CURLY_CLOSE_RE = re.compile(r"[\u201d\u2019]")

# Rule of three detector (flag only, not auto-fixed)
_RULE_OF_THREE_RE = re.compile(
    r"\b(?:\w[\w\s]*),\s+(?:\w[\w\s]*),\s+and\s+(?:\w[\w\s]*)\b"
)

# AI vocabulary words that appear but can't be auto-swapped safely — just flag
_AI_VOCAB_FLAG = [
    "pivotal", "crucial", "vibrant", "tapestry", "landscape",
    "testament", "underscore", "highlight", "interplay", "intricate",
    "garner", "foster", "cultivate", "encompass", "groundbreaking",
    "renowned", "breathtaking", "nestled", "enduring", "indelible",
]
_AI_VOCAB_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in _AI_VOCAB_FLAG) + r")\b",
    re.IGNORECASE,
)


def _split_code_blocks(text: str) -> list[tuple[str, bool]]:
    """Split text into (segment, is_code) pairs to skip code blocks."""
    parts: list[tuple[str, bool]] = []
    pattern = re.compile(r"(```[\s\S]*?```)", re.MULTILINE)
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            parts.append((text[last:m.start()], False))
        parts.append((m.group(0), True))
        last = m.end()
    if last < len(text):
        parts.append((text[last:], False))
    return parts


def humanize(text: str) -> tuple[str, dict]:
    """Apply mechanical humanizer fixes.

    Returns (new_text, stats) where stats contains:
      - fixes_applied: int
      - rule_of_three_count: int
      - ai_vocab_flagged: list[str]
      - llm_pass_recommended: bool
    """
    stats: dict = {
        "fixes_applied": 0,
        "rule_of_three_count": 0,
        "ai_vocab_flagged": [],
        "llm_pass_recommended": False,
    }

    segments = _split_code_blocks(text)
    new_segments: list[str] = []

    for segment, is_code in segments:
        if is_code:
            new_segments.append(segment)
            continue

        s = segment

        # Em dash → comma/space
        em_count = len(_EM_DASH_RE.findall(s))
        s = _EM_DASH_RE.sub(", ", s)
        stats["fixes_applied"] += em_count

        # Curly quotes → straight quotes
        curly = len(_CURLY_OPEN_RE.findall(s)) + len(_CURLY_CLOSE_RE.findall(s))
        s = _CURLY_OPEN_RE.sub('"', s)
        s = _CURLY_CLOSE_RE.sub('"', s)
        stats["fixes_applied"] += curly

        # Word-level replacements
        for pattern, replacement in _WORD_REPLACEMENTS:
            new_s, n = pattern.subn(replacement, s)
            if n:
                stats["fixes_applied"] += n
                s = new_s

        # Rule of three detection (flag only)
        rot = _RULE_OF_THREE_RE.findall(s)
        stats["rule_of_three_count"] += len(rot)

        # AI vocabulary flagging
        ai_found = [m.group(0).lower() for m in _AI_VOCAB_RE.finditer(s)]
        stats["ai_vocab_flagged"].extend(ai_found)

        new_segments.append(s)

    result = "".join(new_segments)

    # Deduplicate flagged vocab
    stats["ai_vocab_flagged"] = sorted(set(stats["ai_vocab_flagged"]))

    # Recommend LLM pass if there's non-mechanical work to do
    if stats["rule_of_three_count"] > 0 or stats["ai_vocab_flagged"]:
        stats["llm_pass_recommended"] = True

    return result, stats


def _make_diff(original: str, revised: str, file_label: str) -> str:
    """Produce a unified diff string."""
    diff = difflib.unified_diff(
        original.splitlines(keepends=True),
        revised.splitlines(keepends=True),
        fromfile=f"{file_label} (original)",
        tofile=f"{file_label} (humanized)",
    )
    return "".join(diff)


# ── Fact-checker ──────────────────────────────────────────────────────────────

def run_factcheck(file_path: Path) -> Optional[str]:
    """Run fact_check.py if available. Returns report string or None."""
    if not FACT_CHECKER_SCRIPT.exists():
        return None

    result = subprocess.run(
        [PYTHON, str(FACT_CHECKER_SCRIPT), str(file_path)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    output = result.stdout
    if result.stderr:
        output += f"\n[stderr]: {result.stderr[:200]}"
    return output.strip() if output.strip() else "(no output)"


def _parse_factcheck_summary(report: str) -> str:
    """Extract a one-line summary from fact-check report for the summary printout."""
    if report is None:
        return f"⚠️  Skipped (fact-checker not found at {FACT_CHECKER_SCRIPT})"
    # Try to find a summary line — fallback to first line
    for line in report.splitlines():
        if re.search(r"claim|verif|check", line, re.I):
            return line.strip()
    return report.splitlines()[0].strip() if report else "(empty report)"


# ── Pipeline DB helpers ───────────────────────────────────────────────────────

def lookup_pipeline_page(
    title: str, db_id: str, key: str
) -> tuple[Optional[str], Optional[str]]:
    """Find a pipeline DB entry by title. Returns (page_id, status) or (None, None)."""
    try:
        data = _req("post", f"/databases/{db_id}/query", key,
                    json={
                        "filter": {
                            "property": "Title",
                            "title": {"equals": title},
                        }
                    },
                    timeout=15)
    except Exception as e:
        print(f"  ⚠️  Could not query pipeline DB: {e}", file=sys.stderr)
        return None, None

    results = data.get("results", [])
    if not results:
        return None, None

    page = results[0]
    page_id = page["id"]
    status_prop = page.get("properties", {}).get("Status", {})
    status = None
    if status_prop.get("type") == "select" and status_prop.get("select"):
        status = status_prop["select"]["name"]
    return page_id, status


def update_pipeline_status(
    page_id: str, new_status: str, key: str, dry_run: bool = False
) -> None:
    """Update the Status property of a pipeline DB page."""
    if dry_run:
        print(f"  [dry-run] Would PATCH /pages/{page_id} → Status: {new_status}")
        return
    _req("patch", f"/pages/{page_id}", key,
         json={"properties": {"Status": {"select": {"name": new_status}}}},
         timeout=15)


def _derive_title(md: str, file_path: Path) -> str:
    """Derive post title from markdown H1 or filename (matches cmd_push logic)."""
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return file_path.stem.replace("-", " ").title()


# ── Main advance command ──────────────────────────────────────────────────────

def cmd_advance(
    file_path: Path,
    skip_humanize: bool = False,
    skip_factcheck: bool = False,
    dry_run: bool = False,
) -> None:
    """Full pipeline advance: pull → humanize → fact-check → push → status update."""
    key         = _get_notion_key()
    sandbox_id  = _get_parent_page_id()
    sync_map_path = _get_sync_map_path(
        os.environ.get("NOTION_SYNC_MAP",
                       str(_WORKSPACE / "scripts" / "notion_sync_map.json"))
    )

    print(f"\n📄 {file_path}")

    # ── 1. Pull ───────────────────────────────────────────────────────────────
    print("\n  [1/5] Pulling from Notion…")
    if not dry_run:
        cmd_pull(file_path, key, sync_map_path)
    else:
        print("  [dry-run] Would pull from Notion")
        if not file_path.exists():
            print(f"  [dry-run] File does not exist yet: {file_path}")
            return

    original_md = file_path.read_text(encoding="utf-8") if file_path.exists() else ""
    word_count  = len(original_md.split())
    print(f"  Pulled from Notion: {word_count:,} words")

    # Derive title for pipeline DB lookup
    title = _derive_title(original_md, file_path)

    # ── 2. Humanize ───────────────────────────────────────────────────────────
    humanizer_summary = "Skipped (--skip-humanize)"
    diff_path: Optional[Path] = None

    if not skip_humanize:
        print("\n  [2/5] Humanizing…")
        humanized_md, h_stats = humanize(original_md)
        n_fixes = h_stats["fixes_applied"]

        diff_str = _make_diff(original_md, humanized_md, str(file_path))
        if diff_str:
            diff_path = file_path.with_suffix(".humanizer.diff")
            if not dry_run:
                diff_path.write_text(diff_str, encoding="utf-8")
                file_path.write_text(humanized_md, encoding="utf-8")
            else:
                print(f"  [dry-run] Would write humanized text and diff → {diff_path}")
        else:
            humanized_md = original_md  # no changes

        # Build summary line
        parts = [f"{n_fixes} mechanical pattern{'s' if n_fixes != 1 else ''} fixed"]
        if diff_path:
            parts.append(f"diff → {diff_path.name}")
        if h_stats["rule_of_three_count"]:
            parts.append(f"{h_stats['rule_of_three_count']} rule-of-three instance(s) flagged")
        if h_stats["ai_vocab_flagged"]:
            flagged = ", ".join(h_stats["ai_vocab_flagged"][:6])
            extra = f" +{len(h_stats['ai_vocab_flagged']) - 6} more" if len(h_stats["ai_vocab_flagged"]) > 6 else ""
            parts.append(f"AI vocab flagged: {flagged}{extra}")
        if h_stats["llm_pass_recommended"]:
            parts.append("⚠️  LLM humanizer pass recommended")

        humanizer_summary = " | ".join(parts)
        print(f"  Humanizer: {humanizer_summary}")
    else:
        print("\n  [2/5] Humanize: skipped")
        humanized_md = original_md

    # ── 3. Fact-check ─────────────────────────────────────────────────────────
    factcheck_summary = "Skipped (--skip-factcheck)"

    if not skip_factcheck:
        print("\n  [3/5] Fact-checking…")
        report = run_factcheck(file_path)
        factcheck_summary = _parse_factcheck_summary(report)
        if report is None:
            print(f"  Fact-check: {factcheck_summary}")
        else:
            report_path = file_path.with_suffix(".factcheck.txt")
            if not dry_run:
                report_path.write_text(report, encoding="utf-8")
            print(f"  Fact-check: {factcheck_summary}")
            print(f"  Full report → {report_path.name}")
    else:
        print("\n  [3/5] Fact-check: skipped")

    # ── 4. Push ───────────────────────────────────────────────────────────────
    print("\n  [4/5] Pushing to Notion…")
    pushed_page_id: Optional[str] = None

    if not dry_run:
        pushed_page_id = cmd_push(file_path, key, sandbox_id, sync_map_path, overwrite=True)
        page_url = f"https://notion.so/{pushed_page_id.replace('-', '')}"
        print(f"  Pushed to Notion: page {pushed_page_id}")
        print(f"  URL: {page_url}")
    else:
        print("  [dry-run] Would push to Notion")

    # ── 5. Update status ──────────────────────────────────────────────────────
    print("\n  [5/5] Updating pipeline status…")
    pipeline_page_id, current_status = lookup_pipeline_page(title, PIPELINE_DB_ID, key)

    status_line = "N/A"
    if pipeline_page_id is None:
        print(f"  ⚠️  No pipeline DB entry found for title: '{title}'")
        print(f"      Run: python3 create_pipeline_db.py and add '{title}' manually.")
        status_line = "No pipeline entry found"
    else:
        new_status = STATUS_TRANSITIONS.get(current_status or "")
        if new_status:
            update_pipeline_status(pipeline_page_id, new_status, key, dry_run=dry_run)
            status_line = f"{current_status} → {new_status}"
            if dry_run:
                status_line += " (dry-run)"
            print(f"  Status: {status_line}")
        elif current_status == "In Review":
            print("  ℹ️  Status is already 'In Review' — Nissan's decision to advance.")
            status_line = "In Review (no change — Nissan's call)"
        else:
            print(f"  ⚠️  Unknown status '{current_status}' — no automatic transition defined.")
            status_line = f"{current_status or 'unknown'} (no transition)"

    # ── Summary ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 60)
    print(f"📄 {file_path}")
    print(f"   Pulled from Notion:  {word_count:,} words")
    print(f"   Humanizer:           {humanizer_summary}")
    print(f"   Fact-check:          {factcheck_summary}")
    if pushed_page_id:
        print(f"   Pushed to Notion:    page {pushed_page_id}")
    elif dry_run:
        print(f"   Pushed to Notion:    [dry-run]")
    print(f"   Status:              {status_line}")
    print("─" * 60)


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Advance a blog post through the content pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command")

    adv = sub.add_parser("advance", help="Pull → humanize → fact-check → push → status")
    adv.add_argument("file", help="Path to local .md file")
    adv.add_argument("--skip-humanize",  action="store_true", help="Skip humanizer step")
    adv.add_argument("--skip-factcheck", action="store_true", help="Skip fact-check step")
    adv.add_argument("--dry-run",        action="store_true",
                     help="Show what would happen without making changes")

    args = parser.parse_args()

    if args.command == "advance":
        file_path = Path(args.file)
        if not file_path.exists() and not args.dry_run:
            # Still allow dry-run even if file doesn't exist yet
            print(f"⚠️  File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        cmd_advance(
            file_path=file_path,
            skip_humanize=args.skip_humanize,
            skip_factcheck=args.skip_factcheck,
            dry_run=args.dry_run,
        )
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
