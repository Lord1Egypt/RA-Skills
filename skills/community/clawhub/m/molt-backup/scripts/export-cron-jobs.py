#!/usr/bin/env python3
"""export-cron-jobs.py — Export OpenClaw cron jobs to JSON + Markdown.

Usage:
    python3 export-cron-jobs.py <output-dir>

Writes:
    <output-dir>/jobs.json     — Full job list (raw JSON)
    <output-dir>/README.md     — Human-readable summary
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def export(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Dump JSON ────────────────────────────────────────────────────────────
    jobs_path = output_dir / "jobs.json"
    try:
        result = subprocess.run(
            ["openclaw", "cron", "list", "--all", "--json"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        data = json.loads(result.stdout)
    except Exception as e:
        data = {"note": f"openclaw cron list unavailable: {e}"}

    jobs_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    # ── Generate Markdown summary ─────────────────────────────────────────────
    readme_path = output_dir / "README.md"
    jobs = data.get("jobs", [])
    lines = [
        "# Cron Jobs\n",
        f"_Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}_\n\n",
    ]

    for j in jobs:
        status = "✅ enabled" if j.get("enabled") else "⏸ disabled"
        name = j.get("name", j.get("id"))
        lines.append(f"## {name}\n\n")
        lines.append(f"**Status:** {status}  \n")

        sched = j.get("schedule", {})
        kind = sched.get("kind")
        if kind == "cron":
            lines.append(f"**Schedule:** `{sched.get('expr')}` ({sched.get('tz', 'UTC')})  \n")
        elif kind == "every":
            ms = sched.get("everyMs", 0)
            minutes = ms // 60000
            hours = minutes // 60
            if hours and minutes % 60 == 0:
                lines.append(f"**Schedule:** Every {hours}h  \n")
            else:
                lines.append(f"**Schedule:** Every {minutes}m  \n")
        elif kind == "at":
            lines.append(f"**Schedule:** One-shot at `{sched.get('at')}`  \n")

        state = j.get("state", {})
        last_run = state.get("lastRunAtMs")
        next_run = state.get("nextRunAtMs")
        last_status = state.get("lastRunStatus", "—")
        last_error = state.get("lastError", "")

        if last_run:
            ts = datetime.fromtimestamp(last_run / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            lines.append(f"**Last run:** {ts} — `{last_status}`")
            if last_error:
                lines.append(f" — _{last_error}_")
            lines.append("  \n")
        if next_run:
            ts = datetime.fromtimestamp(next_run / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            lines.append(f"**Next run:** {ts}  \n")

        payload = j.get("payload", {})
        msg = payload.get("message", "")
        if msg:
            first_line = msg.strip().split("\n")[0]
            lines.append(f"**Task:** {first_line}  \n")

        lines.append("\n")

    readme_path.write_text("".join(lines))
    print(f"  ✓ cron-jobs/ ({len(jobs)} jobs)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output-dir>")
        sys.exit(1)
    export(Path(sys.argv[1]))
