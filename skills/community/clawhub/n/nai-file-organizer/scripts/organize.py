#!/usr/bin/env python3
"""
organize.py — Generate (and optionally execute) a file organization plan.

SAFETY: This script NEVER deletes files. It only moves them.
        Default mode is --dry-run. Pass --execute to apply the plan.

Usage:
    # Generate plan from existing scan JSON
    python3 organize.py <scan.json> [options]

    # Scan and plan in one step
    python3 organize.py --directory <dir> [options]

Options:
    --dry-run           Show what would happen without moving anything (DEFAULT)
    --execute           Actually move files (requires explicit confirmation)
    --categories <file> Path to categories.md (default: ../references/categories.md)
    --dest <dir>        Destination root for organized files (default: <scan_dir>/Organized)
    --flat              Don't preserve subdirectory structure — move all files to category root
    --output <file>     Write move plan JSON to file
    --yes               Skip interactive confirmation when using --execute

Output JSON (move plan):
    {
        "scan_dir": "/path",
        "dest_dir": "/path/Organized",
        "generated_at": "...",
        "dry_run": true,
        "moves": [
            {
                "source": "/path/to/file.jpg",
                "dest": "/path/Organized/Images/file.jpg",
                "category": "Images",
                "size": 102400,
                "conflict": false
            },
            ...
        ],
        "skipped": [...],
        "summary": { "by_category": {...}, "total_moves": 42, "total_bytes": ... }
    }
"""

import os
import sys
import json
import shutil
import argparse
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ---------------------------------------------------------------------------
# Category loading
# ---------------------------------------------------------------------------

def load_categories(categories_path: Path) -> dict[str, str]:
    """
    Parse categories.md and return a dict mapping lowercase extension → folder name.
    Handles compound extensions like .tar.gz.
    """
    if not categories_path.exists():
        print(f"WARNING: categories.md not found at {categories_path}, using built-in defaults", file=sys.stderr)
        return _builtin_categories()

    ext_to_folder = {}
    current_folder = None

    for line in categories_path.read_text().splitlines():
        line = line.strip()
        # Section header: ### Images  or  ## Images
        header = re.match(r"^#{1,4}\s+(.+)$", line)
        if header:
            current_folder = header.group(1).strip()
            continue

        # Extension line: `.jpg` `.jpeg` ... → Folder  OR just a list of `.ext`
        if current_folder and line:
            # Find all extensions in the line (including compound like .tar.gz)
            exts = re.findall(r"`(\.[a-z0-9]+(?:\.[a-z0-9]+)*)`", line)
            for ext in exts:
                ext_lower = ext.lower()
                ext_to_folder[ext_lower] = current_folder

    return ext_to_folder if ext_to_folder else _builtin_categories()


def _builtin_categories() -> dict[str, str]:
    """Minimal built-in fallback if categories.md is missing."""
    return {
        ".jpg": "Images", ".jpeg": "Images", ".png": "Images", ".gif": "Images",
        ".bmp": "Images", ".webp": "Images", ".heic": "Images", ".svg": "Images",
        ".mp4": "Videos", ".mov": "Videos", ".avi": "Videos", ".mkv": "Videos",
        ".mp3": "Audio", ".wav": "Audio", ".flac": "Audio", ".aac": "Audio", ".m4a": "Audio",
        ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents", ".txt": "Documents",
        ".xls": "Spreadsheets", ".xlsx": "Spreadsheets", ".csv": "Spreadsheets",
        ".zip": "Archives", ".tar": "Archives", ".gz": "Archives", ".7z": "Archives",
        ".py": "Code", ".js": "Code", ".ts": "Code", ".html": "Code", ".css": "Code",
        ".tar.gz": "Archives", ".tar.bz2": "Archives",
    }


def categorize_file(file: dict, ext_to_folder: dict) -> str:
    """Return the category folder name for a file."""
    ext = file.get("ext", "").lower()
    return ext_to_folder.get(ext, "Other")


# ---------------------------------------------------------------------------
# Plan generation
# ---------------------------------------------------------------------------

def generate_plan(
    scan_data: dict,
    dest_root: Path,
    ext_to_folder: dict,
    flat: bool = False,
) -> dict:
    """Build the move plan from scan data."""
    scan_dir = Path(scan_data["scan_dir"])
    files = scan_data.get("files", [])

    moves = []
    skipped = []
    dest_names: set[str] = set()  # Track dest paths to detect conflicts

    for f in files:
        # Skip symlinks — don't move them
        if f.get("is_symlink"):
            skipped.append({**f, "reason": "symlink"})
            continue

        abs_src = Path(f["abs_path"])
        category = categorize_file(f, ext_to_folder)

        # Build destination path
        if flat:
            dest_path = dest_root / category / f["name"]
        else:
            # Preserve subdirectory structure relative to scan root
            rel = Path(f["path"])
            if len(rel.parts) > 1:
                # File is in a subdirectory — preserve the subpath
                dest_path = dest_root / category / rel
            else:
                dest_path = dest_root / category / f["name"]

        # Detect name conflicts: if dest already used, add a suffix
        dest_str = str(dest_path)
        if dest_str in dest_names:
            stem = dest_path.stem
            suffix = dest_path.suffix
            counter = 1
            while dest_str in dest_names:
                dest_path = dest_path.parent / f"{stem}_{counter}{suffix}"
                dest_str = str(dest_path)
                counter += 1

        # Check if source would overwrite itself (already in dest)
        try:
            if abs_src.resolve() == dest_path.resolve():
                skipped.append({**f, "reason": "already_at_destination"})
                continue
        except OSError:
            pass

        dest_names.add(dest_str)

        # Check for pre-existing file at dest
        conflict = dest_path.exists()

        moves.append(
            {
                "source": str(abs_src),
                "source_rel": f["path"],
                "dest": dest_str,
                "category": category,
                "size": f["size"],
                "conflict": conflict,
                "name": f["name"],
            }
        )

    # Summary by category
    by_category: dict[str, dict] = defaultdict(lambda: {"count": 0, "bytes": 0})
    for m in moves:
        cat = m["category"]
        by_category[cat]["count"] += 1
        by_category[cat]["bytes"] += m["size"]

    total_bytes = sum(m["size"] for m in moves)
    conflicts = [m for m in moves if m["conflict"]]

    return {
        "scan_dir": str(scan_dir),
        "dest_dir": str(dest_root),
        "generated_at": datetime.now().isoformat(),
        "total_moves": len(moves),
        "total_bytes": total_bytes,
        "conflicts": len(conflicts),
        "skipped": len(skipped),
        "moves": moves,
        "skipped_files": skipped,
        "summary": {
            "by_category": {k: v for k, v in sorted(by_category.items())},
            "total_moves": len(moves),
            "total_bytes": total_bytes,
            "conflicts": len(conflicts),
        },
    }


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------

def execute_plan(plan: dict, yes: bool = False) -> dict:
    """
    Execute the move plan. NEVER deletes files.
    Returns a result dict with success/failure counts.
    """
    moves = plan["moves"]
    conflicts = [m for m in moves if m["conflict"]]

    if conflicts and not yes:
        print(f"\nWARNING: {len(conflicts)} destination file(s) already exist and will be skipped.", file=sys.stderr)
        print("Re-run with --yes to overwrite existing destinations.", file=sys.stderr)

    if not yes:
        print("\nThis will move the following files:")
        _print_plan_summary(plan)
        answer = input("\nProceed? [y/N] ").strip().lower()
        if answer not in ("y", "yes"):
            print("Aborted. No files were moved.")
            sys.exit(0)

    succeeded = 0
    failed = 0
    skipped_conflicts = 0
    errors = []

    for move in moves:
        src = Path(move["source"])
        dst = Path(move["dest"])

        # Safety: never delete — skip if dest exists and not overwriting
        if dst.exists() and not yes:
            skipped_conflicts += 1
            errors.append({"source": move["source"], "dest": move["dest"], "error": "destination_exists"})
            continue

        try:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dst))
            succeeded += 1
        except (PermissionError, OSError, shutil.Error) as e:
            failed += 1
            errors.append({"source": move["source"], "dest": move["dest"], "error": str(e)})
            print(f"ERROR: Could not move {src.name}: {e}", file=sys.stderr)

    return {
        "executed_at": datetime.now().isoformat(),
        "succeeded": succeeded,
        "failed": failed,
        "skipped_conflicts": skipped_conflicts,
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def format_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def _print_plan_summary(plan: dict):
    print(f"\n{'='*60}")
    print(f"  Organization Plan {'(DRY RUN)' if plan.get('dry_run') else ''}")
    print(f"{'='*60}")
    print(f"  Source:      {plan['scan_dir']}")
    print(f"  Destination: {plan['dest_dir']}")
    print(f"  Files:       {plan['total_moves']} moves ({format_bytes(plan['total_bytes'])})")
    if plan.get("conflicts", 0) > 0:
        print(f"  Conflicts:   {plan['conflicts']} (destinations already exist)")
    print(f"\n  By category:")
    for cat, stats in sorted(plan["summary"]["by_category"].items()):
        print(f"    {cat:<20} {stats['count']:>4} files  ({format_bytes(stats['bytes'])})")

    if plan.get("total_moves", 0) <= 30:
        print(f"\n  Planned moves:")
        for m in plan["moves"]:
            conflict_tag = " ⚠️  CONFLICT" if m["conflict"] else ""
            print(f"    {m['source_rel']}")
            print(f"      → {m['dest']}{conflict_tag}")
    else:
        print(f"\n  (Showing first 10 of {plan['total_moves']} moves)")
        for m in plan["moves"][:10]:
            conflict_tag = " ⚠️  CONFLICT" if m["conflict"] else ""
            print(f"    {m['source_rel']}")
            print(f"      → {m['dest']}{conflict_tag}")
        print(f"    ... and {plan['total_moves'] - 10} more.")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate and optionally execute a file organization plan. "
            "SAFETY: Never deletes files. Dry-run by default."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("scan_json", nargs="?", help="JSON file produced by scan.py")
    group.add_argument("--directory", "-d", help="Scan this directory directly")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,
        help="Show plan without executing (default)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        default=False,
        help="Actually move files (shows plan first, then confirms)",
    )
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        default=False,
        help="Skip confirmation prompt when using --execute",
    )
    parser.add_argument(
        "--dest",
        default=None,
        help="Destination root directory (default: <scan_dir>/Organized)",
    )
    parser.add_argument(
        "--categories",
        default=None,
        help="Path to categories.md (default: ../references/categories.md relative to this script)",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        default=False,
        help="Move all files to category root, don't preserve subdirectory structure",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write move plan JSON to this file",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        default=False,
        help="Include hidden files when scanning directly",
    )
    args = parser.parse_args()

    # --execute overrides --dry-run
    dry_run = not args.execute

    # Load scan data
    if args.directory:
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))
        from scan import scan_directory

        target = Path(args.directory).expanduser().resolve()
        print(f"Scanning {target}...", file=sys.stderr)
        scan_data = scan_directory(target, include_hidden=args.include_hidden)
    else:
        scan_path = Path(args.scan_json)
        if not scan_path.exists():
            print(f"ERROR: File not found: {scan_path}", file=sys.stderr)
            sys.exit(1)
        try:
            scan_data = json.loads(scan_path.read_text())
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Resolve categories file
    if args.categories:
        categories_path = Path(args.categories).expanduser().resolve()
    else:
        # Default: ../references/categories.md relative to this script
        categories_path = Path(__file__).parent.parent / "references" / "categories.md"

    ext_to_folder = load_categories(categories_path)
    print(f"Loaded {len(ext_to_folder)} extension mappings from categories", file=sys.stderr)

    # Resolve destination
    scan_dir = Path(scan_data["scan_dir"])
    if args.dest:
        dest_root = Path(args.dest).expanduser().resolve()
    else:
        dest_root = scan_dir / "Organized"

    # Generate plan
    plan = generate_plan(scan_data, dest_root, ext_to_folder, flat=args.flat)
    plan["dry_run"] = dry_run

    # Display plan
    _print_plan_summary(plan)

    # Write plan JSON if requested
    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(plan, indent=2))
        print(f"Plan written to: {out_path}")

    # Execute if requested
    if not dry_run:
        result = execute_plan(plan, yes=args.yes)
        plan["execution_result"] = result
        print(f"\nExecution complete:")
        print(f"  Moved:   {result['succeeded']} files")
        print(f"  Failed:  {result['failed']} files")
        if result.get("skipped_conflicts", 0) > 0:
            print(f"  Skipped: {result['skipped_conflicts']} (destination conflicts)")
        if result["errors"]:
            print(f"\nErrors:")
            for e in result["errors"][:10]:
                print(f"  {Path(e['source']).name}: {e['error']}")

        # Update plan JSON with results
        if args.output:
            Path(args.output).write_text(json.dumps(plan, indent=2))

    elif not args.output:
        # Dry run with no output file: print JSON to stdout
        print(json.dumps(plan, indent=2))
    else:
        print("Dry run complete. No files were moved.")
        print("Run with --execute to apply the plan.")


if __name__ == "__main__":
    main()
