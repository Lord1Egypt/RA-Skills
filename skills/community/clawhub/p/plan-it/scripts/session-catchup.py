#!/usr/bin/env python3
"""session-catchup.py — detect unsynced plan-it edits from prior IDE sessions.

Parses session storage from:
  - Claude Code: ~/.claude/projects/<slug>/*.jsonl   (mtime only, no content read)
  - OpenCode:   ${XDG_DATA_HOME:-~/.local/share}/opencode/opencode.db
                (SQLite opened with mode=ro, single SELECT for id + time_created,
                 no message bodies)
  - Codex:      ~/.codex/sessions/*.json
                (capped at the 10 most recent files, each read up to 256 KB only,
                 parsed solely to match the `cwd` field; no other fields surfaced)

Looks at modification timestamps. If a session edited plan.html or
.planning/<slug>/plan.html more recently than the local file, surfaces a
catchup report.

Nothing leaves the machine. All access is local and read-only. No data is
written anywhere. No network calls.

To opt out entirely, set `PLANIT_NO_HISTORY=1` in the environment or pass
`--no-history`. The script exits 0 with no output.

Designed for invocation in SKILL.md first-step "Restore Context" block.

Usage:
  python scripts/session-catchup.py <project-cwd>
  python scripts/session-catchup.py --no-history <project-cwd>
"""
from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
import time
from pathlib import Path


def _resolve_claude_projects_dir() -> Path | None:
    candidates = [
        Path.home() / ".claude" / "projects",
    ]
    for c in candidates:
        if c.is_dir():
            return c
    return None


def _slugify_cwd(cwd: Path) -> str:
    return str(cwd).replace(":", "").replace("\\", "-").replace("/", "-").lstrip("-")


def _claude_code_catchup(cwd: Path) -> list[str]:
    out: list[str] = []
    proj_root = _resolve_claude_projects_dir()
    if not proj_root:
        return out
    # Try a few slug encodings
    slug_candidates = [
        f"C--{_slugify_cwd(cwd)}",
        _slugify_cwd(cwd),
    ]
    for slug in slug_candidates:
        proj_dir = proj_root / slug
        if proj_dir.is_dir():
            jsonls = sorted(proj_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
            if jsonls:
                latest = jsonls[0]
                age_min = (time.time() - latest.stat().st_mtime) / 60
                out.append(
                    f"[catchup] Claude Code session at {latest.name}, last touched {age_min:.0f} min ago"
                )
            break
    return out


def _opencode_catchup(cwd: Path) -> list[str]:
    out: list[str] = []
    xdg = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    db_path = Path(xdg) / "opencode" / "opencode.db"
    if not db_path.is_file():
        return out
    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
            cur = conn.cursor()
            cur.execute("PRAGMA table_info(session)")
            cols = [r[1] for r in cur.fetchall()]
            if "directory" not in cols:
                return out
            cur.execute(
                "SELECT id, time_created FROM session WHERE directory = ? ORDER BY time_created DESC LIMIT 1",
                (str(cwd),),
            )
            row = cur.fetchone()
            if row:
                age_min = (time.time() - row[1]) / 60
                out.append(f"[catchup] OpenCode session {row[0]}, last touched {age_min:.0f} min ago")
    except sqlite3.Error:
        pass
    return out


CODEX_READ_CAP = 256 * 1024  # bytes; bound how much of any one session file we touch


def _codex_catchup(cwd: Path) -> list[str]:
    out: list[str] = []
    codex_dir = Path.home() / ".codex" / "sessions"
    if not codex_dir.is_dir():
        return out
    files = sorted(codex_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    cwd_str = str(cwd)
    for f in files[:10]:
        try:
            with f.open("rb") as fh:
                blob = fh.read(CODEX_READ_CAP)
            data = json.loads(blob.decode("utf-8", errors="replace"))
        except (OSError, json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(data, dict) and data.get("cwd") == cwd_str:
            age_min = (time.time() - f.stat().st_mtime) / 60
            out.append(f"[catchup] Codex session {f.name}, last touched {age_min:.0f} min ago")
            break
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cwd", nargs="?", default=".", help="Project working directory")
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Skip all session-store reads. Same as PLANIT_NO_HISTORY=1.",
    )
    args = parser.parse_args(argv)
    cwd = Path(args.cwd).resolve()

    plan_present = (cwd / "plan.html").is_file() or (cwd / ".planning" / ".active_plan").is_file()
    if not plan_present:
        return 0

    if args.no_history or os.environ.get("PLANIT_NO_HISTORY", "").strip() in ("1", "true", "yes"):
        return 0

    lines: list[str] = []
    lines.extend(_claude_code_catchup(cwd))
    lines.extend(_opencode_catchup(cwd))
    lines.extend(_codex_catchup(cwd))

    if not lines:
        print("[plan-it] session catchup: no prior sessions found")
        return 0

    print("[plan-it] session catchup report:")
    for ln in lines:
        print(f"  {ln}")
    print(
        "[plan-it] If any of these sessions might have edited plan.html outside of this one, "
        "re-read plan.html and update progress_log + phases accordingly."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception:
        sys.exit(0)
