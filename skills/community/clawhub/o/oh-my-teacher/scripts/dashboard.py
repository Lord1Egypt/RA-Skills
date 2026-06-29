#!/usr/bin/env python3
"""Oh My Teacher — terminal review dashboard.

Shows the Current Course Snapshot, SRS due topics, and a quick review
overview. Requires `rich` for the TUI; falls back to plain text.

Usage:
  python scripts/dashboard.py                    # single-course mode
  python scripts/dashboard.py --active           # active multi-course
  python scripts/dashboard.py --slug math        # specific course
  python scripts/dashboard.py --workspace /path  # custom workspace
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

HAS_RICH = True
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    from rich.progress import Progress, BarColumn, TextColumn
except ImportError:
    HAS_RICH = False


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from snapshot import parse_snapshot, state_root, single_snapshot_path, snapshot_path, active_path  # noqa: E402
from srs import read_rows, parse_date  # noqa: E402


def _today() -> str:
    return dt.date.today().isoformat()


def _load_snapshot(workspace: Path, slug: str | None) -> dict[str, str] | None:
    path = snapshot_path(workspace, slug) if slug else single_snapshot_path(workspace)
    if not path.exists():
        return None
    return parse_snapshot(path.read_text(encoding="utf-8"))


def _load_srs_rows(workspace: Path, slug: str | None) -> list:
    from srs import read_rows, srs_path
    path = srs_path(workspace, slug)
    if not path.exists():
        return []
    return read_rows(path)


def dashboard_text(workspace: Path, slug: str | None) -> str:
    """Render a plain-text dashboard."""
    snap = _load_snapshot(workspace, slug)
    srs_rows = _load_srs_rows(workspace, slug)
    today = _today()

    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  Oh My Teacher — Review Dashboard")
    lines.append("=" * 60)

    if snap:
        lines.append("")
        lines.append("  Current Course:")
        for key, val in snap.items():
            lines.append(f"    {key.replace('_', ' ').title():20s}: {val}")
    else:
        lines.append("  No snapshot found.")

    if srs_rows:
        today_obj = dt.date.fromisoformat(today)
        due = [r for r in srs_rows if parse_date(r.next_review) <= today_obj]
        lines.append("")
        lines.append(f"  SRS: {len(srs_rows)} topics tracked, {len(due)} due today")
        if due:
            lines.append("")
            lines.append("  Due topics (by priority):")
            due.sort(key=lambda r: (parse_date(r.next_review), -r.score))
            for r in due:
                days_over = (today_obj - parse_date(r.next_review)).days
                marker = "!!!" if days_over >= 3 else (" !!" if days_over >= 1 else "  !")
                leech = " [LEECH: change strategy]" if r.is_leech() else ""
                lines.append(f"    {marker} {r.topic:25s} score={r.score} streak={r.streak} "
                             f"ease={r.ease:.2f} lapses={r.lapses} next={r.next_review} (+{days_over}d overdue){leech}")
        else:
            lines.append("  No topics due today.")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  Commands: python scripts/srs.py due | python scripts/snapshot.py load")
    lines.append("  Use: python scripts/dashboard.py --active (multi-course)")
    lines.append("=" * 60)
    return "\n".join(lines)


def dashboard_rich(workspace: Path, slug: str | None) -> None:
    """Render a rich TUI dashboard."""
    console = Console()
    snap = _load_snapshot(workspace, slug)
    srs_rows = _load_srs_rows(workspace, slug)
    today = dt.date.today()

    # Header
    title = Text("Oh My Teacher — Review Dashboard", style="bold cyan")
    console.print(Panel(title, box=box.ROUNDED))

    # Snapshot panel
    if snap:
        table = Table(title="Current Course Snapshot", box=box.SIMPLE)
        table.add_column("Field", style="yellow")
        table.add_column("Value", style="white")
        for key, val in snap.items():
            table.add_row(key.replace("_", " ").title(), val)
        console.print(table)
    else:
        console.print("[red]No snapshot found.[/red]")

    # SRS panel
    if srs_rows:
        due = [r for r in srs_rows if parse_date(r.next_review) <= today]
        due_count = len(due)
        total = len(srs_rows)
        pct = int((total - due_count) / total * 100) if total else 0

        progress_table = Table(box=box.SIMPLE)
        progress_table.add_column("Metric", style="green")
        progress_table.add_column("Value")
        progress_table.add_row("Topics tracked", str(total))
        progress_table.add_row("Due today", f"[red]{due_count}[/red]" if due_count else "[green]0[/green]")
        progress_table.add_row("Review coverage", f"{pct}%")

        console.print(Panel(progress_table, title="Spaced Repetition", box=box.ROUNDED))

        if due:
            due_table = Table(title=f"Due Topics ({due_count})", box=box.SIMPLE)
            due_table.add_column("Topic", style="cyan")
            due_table.add_column("Score", justify="center")
            due_table.add_column("Streak", justify="center")
            due_table.add_column("Next Review", justify="center")
            due_table.add_column("Overdue", justify="center")
            due.sort(key=lambda r: (parse_date(r.next_review), -r.score))
            for r in due:
                days_over = (today - parse_date(r.next_review)).days
                overdue_str = f"[red]{days_over}d[/red]" if days_over > 0 else "[green]today[/green]"
                due_table.add_row(r.topic, str(r.score), str(r.streak), r.next_review, overdue_str)
            console.print(due_table)
    else:
        console.print("[yellow]No SRS data found. Use /quiz or /grade to start.[/yellow]")

    # Footer
    console.print("[dim]Commands: python scripts/srs.py due | python scripts/snapshot.py load[/dim]",
                  style="italic")


def main(argv: list[str] | None = None) -> int:
    import argparse
    import os
    parser = argparse.ArgumentParser(description="Oh My Teacher review dashboard.")
    parser.add_argument("--workspace", default=os.environ.get("OMT_WORKSPACE", "."),
                        help="Workspace root (default: $OMT_WORKSPACE or current directory).")
    parser.add_argument("--slug", help="Course slug for multi-course mode.")
    parser.add_argument("--active", action="store_true", help="Use active multi-course snapshot.")
    args = parser.parse_args(argv)

    workspace = Path(args.workspace).resolve()
    slug = args.slug
    if slug is None and args.active:
        from snapshot import active_path as snap_active_path
        active = snap_active_path(workspace)
        if active.exists():
            slug = active.read_text(encoding="utf-8").strip()
        else:
            print("No active snapshot slug is set.", file=sys.stderr)
            return 1

    if HAS_RICH:
        dashboard_rich(workspace, slug)
    else:
        print(dashboard_text(workspace, slug))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
