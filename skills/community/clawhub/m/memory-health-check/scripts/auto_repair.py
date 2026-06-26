#!/usr/bin/env python3
"""Auto-repair - clean orphaned and temp files."""
import argparse
import json
import logging
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("auto_repair")

MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
LINK_PATTERN = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")


def get_ds_store_files(base: Path) -> list[Path]:
    """Return all .DS_Store files under base."""
    try:
        return [f for f in base.rglob(".DS_Store") if f.is_file()]
    except Exception:
        return []


def get_empty_files(base: Path) -> list[Path]:
    """Return all empty (.size == 0) markdown files under base."""
    empty = []
    for f in base.rglob("*.md"):
        try:
            if f.is_file() and f.stat().st_size == 0:
                empty.append(f)
        except Exception:
            pass
    return empty


def get_orphan_files(base: Path) -> list[Path]:
    """Return orphan files (no inbound Obsidian [[...]] references)."""
    md_files = [f for f in base.rglob("*.md") if f.is_file()]
    filename_refs: dict[str, set[str]] = {}

    for f in md_files:
        try:
            content = f.read_text(errors="ignore")
            refs = set()
            for match in LINK_PATTERN.finditer(content):
                linked_name = Path(match.group(1).strip()).stem
                refs.add(linked_name)
            filename_refs[f.stem] = refs
        except Exception:
            pass

    orphans = []
    for f in md_files:
        inbound = any(
            f.stem in refs
            for other_stem, refs in filename_refs.items()
            if other_stem != f.stem
        )
        if not inbound:
            orphans.append(f)
    return orphans


def auto_repair(
    remove_ds_store: bool = True,
    remove_empty: bool = True,
    remove_orphans: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
) -> dict:
    """Remove orphaned entries and temp files (user-approved)."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    if not MEMORY_DIR.exists():
        logger.warning("memory directory not found")
        return {"repaired": [], "errors": [], "summary": "No memory directory found"}

    repaired = []
    errors = []

    # .DS_Store cleanup
    if remove_ds_store:
        for f in get_ds_store_files(MEMORY_DIR):
            if dry_run:
                logger.info(f"[dry-run] Would remove .DS_Store: {f}")
                repaired.append(f"[dry-run] Remove: {f}")
            else:
                try:
                    f.unlink()
                    repaired.append(f"Removed .DS_Store: {f}")
                    logger.info(f"Removed: {f}")
                except Exception as e:
                    errors.append(f"Failed to remove {f}: {e}")
                    logger.error(f"Failed: {f}: {e}")

    # Empty file cleanup
    if remove_empty:
        for f in get_empty_files(MEMORY_DIR):
            if dry_run:
                repaired.append(f"[dry-run] Remove empty: {f}")
                logger.info(f"[dry-run] Would remove empty file: {f}")
            else:
                try:
                    f.unlink()
                    repaired.append(f"Removed empty: {f}")
                    logger.info(f"Removed empty file: {f}")
                except Exception as e:
                    errors.append(f"Failed to remove {f}: {e}")

    # Orphan cleanup (disabled by default - needs explicit flag)
    if remove_orphans:
        orphans = get_orphan_files(MEMORY_DIR)
        if dry_run:
            for f in orphans:
                repaired.append(f"[dry-run] Remove orphan: {f}")
                logger.info(f"[dry-run] Would remove orphan: {f}")
        else:
            for f in orphans:
                try:
                    f.unlink()
                    repaired.append(f"Removed orphan: {f}")
                    logger.info(f"Removed orphan: {f}")
                except Exception as e:
                    errors.append(f"Failed to remove orphan {f}: {e}")

    summary = f"Cleaned {len(repaired)} items, {len(errors)} errors"
    logger.info(summary)

    return {
        "repaired": repaired,
        "errors": errors,
        "summary": summary,
    }


def main():
    parser = argparse.ArgumentParser(description="Auto-repair - clean orphaned and temp files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--remove-orphans", action="store_true", help="Also remove orphan files (default: no)")
    parser.add_argument("--no-ds-store", action="store_true", help="Skip .DS_Store removal")
    parser.add_argument("--no-empty", action="store_true", help="Skip empty file removal")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    result = auto_repair(
        remove_ds_store=not args.no_ds_store,
        remove_empty=not args.no_empty,
        remove_orphans=args.remove_orphans,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"[auto_repair] {result['summary']}")
        for r in result["repaired"]:
            print(f"  ✓ {r}")
        if result["errors"]:
            print("Errors:")
            for e in result["errors"]:
                print(f"  ✗ {e}")


if __name__ == "__main__":
    main()
