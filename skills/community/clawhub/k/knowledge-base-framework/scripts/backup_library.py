#!/usr/bin/env python3
"""
Backup Script für kb/library/
=============================

Sichert ausschließlich Daten-Dateien aus kb/library/.
.py-Dateien und __pycache__ werden ausgeschlossen.

Usage:
    python3 scripts/backup_library.py [--output /path/to/backup]
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

def backup_library(source: Path, destination: Path, dry_run: bool = False):
    """Backup kb/library/ Data-Files only."""
    
    if not source.exists():
        print(f"Error: Source {source} does not exist")
        return False
    
    # Create timestamped backup directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = destination / f"kb-library-backup_{timestamp}"
    
    print(f"Backup source: {source}")
    print(f"Backup destination: {backup_dir}")
    
    # Files to exclude (code, cache)
    exclude_extensions = {'.py', '.pyc', '.pyo'}
    exclude_dirs = {'__pycache__', '.pytest_cache', '.git'}
    
    if dry_run:
        print("\n=== DRY RUN - Files that would be copied ===")
    
    file_count = 0
    skipped_count = 0
    
    for item in source.rglob("*"):
        # Skip directories
        if item.is_dir():
            if item.name in exclude_dirs:
                print(f"  [SKIP DIR] {item.relative_to(source)}")
                skipped_count += 1
            continue
        
        # Check file extension
        if item.suffix in exclude_extensions:
            print(f"  [SKIP FILE] {item.relative_to(source)} (.py)")
            skipped_count += 1
            continue
        
        # Calculate relative path and create destination
        rel_path = item.relative_to(source)
        dest_file = backup_dir / rel_path
        
        if dry_run:
            print(f"  [WOULD COPY] {rel_path}")
        else:
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_file)
            print(f"  [COPY] {rel_path}")
        
        file_count += 1
    
    print(f"\n=== Summary ===")
    print(f"Files copied: {file_count}")
    print(f"Files skipped: {skipped_count}")
    
    if not dry_run:
        # Create backup metadata
        meta_file = backup_dir / "backup_metadata.txt"
        meta_file.write_text(f"""KB Library Backup
================
Date: {datetime.now().isoformat()}
Source: {source}
Files backed up: {file_count}
Excluded: {skipped_count} (.py files, __pycache__, etc.)
""")
        print(f"Metadata: {meta_file}")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Backup kb/library/ (data only, no .py files)")
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path.home() / "backups",
        help="Backup destination directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without actually copying"
    )
    
    args = parser.parse_args()
    
    # Default source
    source = Path(__file__).parent.parent / "kb" / "library"
    
    # Create output directory
    args.output.mkdir(parents=True, exist_ok=True)
    
    success = backup_library(source, args.output, dry_run=args.dry_run)
    
    if success:
        print("\nBackup completed successfully!")
        sys.exit(0)
    else:
        print("\nBackup failed!", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()