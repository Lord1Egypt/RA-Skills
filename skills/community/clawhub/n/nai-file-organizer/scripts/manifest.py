#!/usr/bin/env python3
"""
manifest.py — Generate a before/after markdown manifest from scan and organize data.

Usage:
    # Compare two scan JSONs (before and after)
    python3 manifest.py --before <before_scan.json> --after <after_scan.json> [--output <manifest.md>]

    # Generate from an organize.py plan JSON (includes execution result)
    python3 manifest.py --plan <plan.json> [--output <manifest.md>]

    # Generate a simple inventory manifest from a scan
    python3 manifest.py --scan <scan.json> [--output <manifest.md>]

Output: Clean markdown file with summary tables and file listings.
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def format_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def format_datetime(iso_str: str) -> str:
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        return iso_str or "unknown"


def files_by_category(files: list[dict], ext_map: dict[str, str] | None = None) -> dict[str, list[dict]]:
    """Group files by their category (using ext if no ext_map)."""
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for f in files:
        if ext_map:
            cat = ext_map.get(f.get("ext", "").lower(), "Other")
        else:
            ext = f.get("ext", "")
            cat = ext.lstrip(".").upper() if ext else "No Extension"
        by_cat[cat].append(f)
    return dict(sorted(by_cat.items()))


def build_scan_manifest(scan_data: dict, title: str = "File Inventory") -> str:
    """Build a markdown manifest from a single scan."""
    lines = []
    scan_dir = scan_data.get("scan_dir", "unknown")
    scanned_at = format_datetime(scan_data.get("scanned_at", ""))
    files = scan_data.get("files", [])
    total_bytes = scan_data.get("total_bytes", sum(f.get("size", 0) for f in files))

    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"**Directory:** `{scan_dir}`  ")
    lines.append(f"**Scanned:** {scanned_at}  ")
    lines.append(f"**Files:** {len(files)} ({format_bytes(total_bytes)})  ")
    if scan_data.get("skipped_hidden", 0):
        lines.append(f"**Hidden items skipped:** {scan_data['skipped_hidden']}  ")
    if scan_data.get("skipped_permission_errors", 0):
        lines.append(f"**Permission errors:** {scan_data['skipped_permission_errors']}  ")
    lines.append("")

    # Extension summary table
    ext_counts: dict[str, dict] = defaultdict(lambda: {"count": 0, "bytes": 0})
    for f in files:
        ext = f.get("ext", "") or "(none)"
        ext_counts[ext]["count"] += 1
        ext_counts[ext]["bytes"] += f.get("size", 0)

    lines.append("## By Extension")
    lines.append("")
    lines.append("| Extension | Count | Size |")
    lines.append("|-----------|------:|-----:|")
    for ext, stats in sorted(ext_counts.items(), key=lambda x: -x[1]["bytes"]):
        lines.append(f"| `{ext}` | {stats['count']} | {format_bytes(stats['bytes'])} |")
    lines.append("")

    # File listing (grouped by parent directory)
    by_dir: dict[str, list[dict]] = defaultdict(list)
    for f in files:
        parent = str(Path(f["path"]).parent) if "/" in f["path"] else "."
        by_dir[parent].append(f)

    lines.append("## File Listing")
    lines.append("")
    for directory in sorted(by_dir.keys()):
        if directory == ".":
            lines.append("### Root")
        else:
            lines.append(f"### `{directory}/`")
        lines.append("")
        for f in sorted(by_dir[directory], key=lambda x: x["name"]):
            size_str = format_bytes(f.get("size", 0))
            modified = format_datetime(f.get("modified", ""))
            symlink = " 🔗" if f.get("is_symlink") else ""
            lines.append(f"- `{f['name']}`{symlink} — {size_str} — {modified}")
        lines.append("")

    return "\n".join(lines)


def build_diff_manifest(before: dict, after: dict) -> str:
    """Build a before/after diff manifest from two scans."""
    lines = []

    before_files = {f["abs_path"]: f for f in before.get("files", [])}
    after_files = {f["abs_path"]: f for f in after.get("files", [])}

    before_paths = set(before_files.keys())
    after_paths = set(after_files.keys())

    added = after_paths - before_paths
    removed = before_paths - after_paths
    common = before_paths & after_paths

    before_bytes = before.get("total_bytes", sum(f.get("size", 0) for f in before.get("files", [])))
    after_bytes = after.get("total_bytes", sum(f.get("size", 0) for f in after.get("files", [])))

    lines.append("# Before/After File Organization Manifest")
    lines.append("")
    lines.append(f"**Generated:** {format_datetime(datetime.now().isoformat())}  ")
    lines.append(f"**Directory:** `{before.get('scan_dir', 'unknown')}`  ")
    lines.append("")

    lines.append("## Summary")
    lines.append("")
    lines.append("| | Before | After | Change |")
    lines.append("|---|------:|------:|-------:|")
    lines.append(f"| Files | {len(before_files)} | {len(after_files)} | {len(after_files) - len(before_files):+d} |")
    lines.append(f"| Size | {format_bytes(before_bytes)} | {format_bytes(after_bytes)} | — |")
    lines.append(f"| Added | — | — | {len(added)} |")
    lines.append(f"| Removed | — | — | {len(removed)} |")
    lines.append(f"| Unchanged | — | — | {len(common)} |")
    lines.append("")

    if removed:
        lines.append("## Removed / Moved Files")
        lines.append("")
        for path in sorted(removed):
            f = before_files[path]
            lines.append(f"- ~~`{f['path']}`~~ ({format_bytes(f.get('size', 0))})")
        lines.append("")

    if added:
        lines.append("## Added / Moved To")
        lines.append("")
        for path in sorted(added):
            f = after_files[path]
            lines.append(f"- `{f['path']}` ({format_bytes(f.get('size', 0))})")
        lines.append("")

    return "\n".join(lines)


def build_plan_manifest(plan: dict) -> str:
    """Build a manifest from an organize.py plan JSON."""
    lines = []
    generated_at = format_datetime(plan.get("generated_at", ""))
    scan_dir = plan.get("scan_dir", "unknown")
    dest_dir = plan.get("dest_dir", "unknown")
    moves = plan.get("moves", [])
    dry_run = plan.get("dry_run", True)
    execution = plan.get("execution_result", None)

    mode = "DRY RUN" if dry_run else "EXECUTED"
    lines.append(f"# File Organization Manifest — {mode}")
    lines.append("")
    lines.append(f"**Generated:** {generated_at}  ")
    lines.append(f"**Source:** `{scan_dir}`  ")
    lines.append(f"**Destination:** `{dest_dir}`  ")
    lines.append(f"**Mode:** {'Dry Run (no files moved)' if dry_run else 'Executed'}  ")
    lines.append("")

    summary = plan.get("summary", {})
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Total moves planned:** {summary.get('total_moves', len(moves))}")
    lines.append(f"- **Total size:** {format_bytes(summary.get('total_bytes', 0))}")
    if summary.get("conflicts", 0) > 0:
        lines.append(f"- **Destination conflicts:** {summary['conflicts']} ⚠️")
    lines.append("")

    # By-category summary
    by_cat = summary.get("by_category", {})
    if by_cat:
        lines.append("## By Category")
        lines.append("")
        lines.append("| Category | Files | Size |")
        lines.append("|----------|------:|-----:|")
        for cat, stats in sorted(by_cat.items()):
            lines.append(f"| {cat} | {stats['count']} | {format_bytes(stats['bytes'])} |")
        lines.append("")

    # Execution results (if plan was executed)
    if execution:
        lines.append("## Execution Results")
        lines.append("")
        lines.append(f"- **Moved:** {execution.get('succeeded', 0)} files")
        lines.append(f"- **Failed:** {execution.get('failed', 0)} files")
        if execution.get("skipped_conflicts", 0) > 0:
            lines.append(f"- **Skipped (conflicts):** {execution['skipped_conflicts']} files")
        if execution.get("errors"):
            lines.append("")
            lines.append("### Errors")
            lines.append("")
            for e in execution["errors"][:20]:
                lines.append(f"- `{Path(e['source']).name}`: {e['error']}")
        lines.append("")

    # Move plan table
    lines.append("## Move Plan")
    lines.append("")
    lines.append("| File | Size | Category | Destination |")
    lines.append("|------|-----:|----------|-------------|")

    conflicts = []
    for m in sorted(moves, key=lambda x: x.get("category", "")):
        conflict = " ⚠️" if m.get("conflict") else ""
        dest_rel = Path(m["dest"]).relative_to(dest_dir) if m["dest"].startswith(dest_dir) else Path(m["dest"])
        lines.append(
            f"| `{m.get('source_rel', m.get('name', '?'))}` | {format_bytes(m.get('size', 0))} "
            f"| {m.get('category', '?')} | `{dest_rel}`{conflict} |"
        )
        if m.get("conflict"):
            conflicts.append(m)

    lines.append("")

    if conflicts:
        lines.append("## ⚠️ Destination Conflicts")
        lines.append("")
        lines.append("These destinations already had a file present:")
        lines.append("")
        for m in conflicts:
            lines.append(f"- `{m.get('source_rel', '?')}` → `{m['dest']}`")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a markdown manifest from scan/organize data."
    )
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--scan", help="Single scan JSON → inventory manifest")
    mode_group.add_argument("--plan", help="organize.py plan JSON → plan manifest")
    mode_group.add_argument(
        "--before",
        help="Before scan JSON (use with --after for diff manifest)",
    )

    parser.add_argument("--after", help="After scan JSON (use with --before)")
    parser.add_argument("--output", "-o", default=None, help="Write manifest to this .md file")
    parser.add_argument("--title", default="File Inventory", help="Title for single-scan manifest")
    args = parser.parse_args()

    # Validate
    if args.before and not args.after:
        print("ERROR: --before requires --after", file=sys.stderr)
        sys.exit(1)

    def load_json(path_str: str) -> dict:
        p = Path(path_str)
        if not p.exists():
            print(f"ERROR: File not found: {p}", file=sys.stderr)
            sys.exit(1)
        try:
            return json.loads(p.read_text())
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {p}: {e}", file=sys.stderr)
            sys.exit(1)

    # Build manifest
    if args.scan:
        scan_data = load_json(args.scan)
        manifest = build_scan_manifest(scan_data, title=args.title)
    elif args.plan:
        plan_data = load_json(args.plan)
        manifest = build_plan_manifest(plan_data)
    else:
        before_data = load_json(args.before)
        after_data = load_json(args.after)
        manifest = build_diff_manifest(before_data, after_data)

    # Output
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(manifest)
        print(f"Manifest written to: {out_path}")
    else:
        print(manifest)


if __name__ == "__main__":
    main()
