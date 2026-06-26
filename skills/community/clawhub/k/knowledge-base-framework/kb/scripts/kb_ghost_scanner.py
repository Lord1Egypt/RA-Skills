#!/usr/bin/env python3
"""
KB Ghost Scanner – Finds new files that are not indexed in KB

Runtime: Monday-Friday 02:00 AM (via Cron)
Purpose: Find new files and add them to KB

Phase 2.3: Extended Extensions + Incremental Scanning
- Extensions: .doc, .docx, .epub added
- Recursive scanning deeper into subdirectories
- Incremental scan with cache
"""

import sqlite3
import os
import json
from pathlib import Path
from datetime import datetime
import csv

# Configuration - use KBConfig for portable paths
try:
    from kb.base.config import KBConfig
    _config = KBConfig.get_instance()
    DB_PATH = _config.db_path
    LIBRARY_PATH = _config.library_path
    OUTPUT_DIR = _config.library_path / "audit"
    CACHE_FILE = _config.ghost_cache_path
    _WORKSPACE = _config.workspace_path
except ImportError:
    from kb.framework.paths import (
        get_default_db_path, get_default_library_path,
        get_default_ghost_cache_path, get_default_workspace_path,
    )
    DB_PATH = get_default_db_path()
    LIBRARY_PATH = get_default_library_path()
    OUTPUT_DIR = LIBRARY_PATH / "audit"
    CACHE_FILE = get_default_ghost_cache_path()
    _WORKSPACE = get_default_workspace_path()

OUTPUT_FILE = OUTPUT_DIR / "ghost_files.csv"
LOG_FILE = OUTPUT_DIR / "audit_log.md"

# Directories to monitor
SCAN_DIRS = [
    LIBRARY_PATH,
    _WORKSPACE,
    LIBRARY_PATH / "Gesundheit",
]

# Phase 2.3: Extended file extensions (with warning for non-directly indexable)
INDEXABLE_EXTENSIONS = {
    # Documents (directly indexable)
    '.pdf', '.txt', '.md', '.html', '.xml',
    # Office (Indexable with warning)
    '.doc', '.docx', '.odt', '.rtf',
    # E-Books
    '.epub', '.mobi', '.azw3',
    # Images (for OCR queue)
    '.jpg', '.jpeg', '.png', '.tiff', '.webp',
    # Code
    '.py', '.sh', '.js', '.ts', '.java', '.c', '.cpp', '.go',
    # Data
    '.json', '.yaml', '.yml', '.csv', '.tsv',
    # Other
    '.log', '.rst', '.tex',
}

# Warning for these extensions (need external tools)
EXTERNAL_TOOL_EXTENSIONS = {'.doc', '.docx', '.odt', '.rtf', '.epub', '.mobi', '.azw3'}

def log(message: str):
    """Log a message"""
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {message}")

def init_output_dir():
    """Create output directory if needed"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_indexed_files() -> set:
    """Get all files indexed in KB"""
    conn = sqlite3.connect(str(DB_PATH))
    try:
        cursor = conn.execute("SELECT DISTINCT file_path FROM files WHERE file_path IS NOT NULL")
        indexed = {row[0] for row in cursor.fetchall()}
    finally:
        conn.close()
    return indexed

def load_cache() -> dict:
    """Load cached file hashes for incremental scanning"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE) as f:
                return json.load(f)
        except Exception as e:
            log(f"WARN: Failed to load cache: {e}")
    return {}

def save_cache(cache: dict):
    """Save cache"""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)

def should_scan_file(file_path: Path, cache: dict, incremental: bool) -> bool:
    """
    Check if file has changed since last scan.
    Phase 2.3: Incremental scanning.
    """
    if not incremental:
        return True
    
    key = str(file_path)
    try:
        current_mtime = file_path.stat().st_mtime
        if key not in cache or cache[key] != current_mtime:
            return True
    except OSError:
        return False

def scan_for_files(incremental: bool = True) -> list[Path]:
    """
    Scan all directories for indexable files.
    
    Phase 2.3: 
    - Recursive scanning (rglob instead of glob)
    - Incremental scanning with cache
    """
    files = []
    cache = load_cache() if incremental else {}
    new_cache = {}
    
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            log(f"WARN: Directory does not exist: {scan_dir}")
            continue
        
        # Phase 2.3: rglob for recursive scanning in subdirectories
        for ext in INDEXABLE_EXTENSIONS:
            for f in scan_dir.rglob(f"*{ext}"):  # rglob instead of glob
                # Skip if should be skipped in incremental mode
                if not should_scan_file(f, cache, incremental):
                    continue
                files.append(f)
                # Update cache
                try:
                    new_cache[str(f)] = f.stat().st_mtime
                except OSError:
                    pass
    
    # Save updated cache
    if incremental:
        save_cache(new_cache)
    
    return files

def find_ghost_files(indexed: set, files: list[Path]) -> list[dict]:
    """Find files that are not in KB"""
    ghost_files = []
    for f in files:
        str_path = str(f)
        if str_path not in indexed:
            ghost_files.append({
                'path': str_path,
                'size': f.stat().st_size,
                'modified': datetime.fromtimestamp(f.stat().st_mtime).isoformat(),
            })
    return ghost_files

def save_ghost_files(ghost_files: list[dict]):
    """Save ghost files as CSV"""
    with open(OUTPUT_FILE, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['path', 'size', 'modified'])
        writer.writeheader()
        writer.writerows(ghost_files)
    log(f"Found: {len(ghost_files)} ghost files")

def update_log(ghost_count: int):
    """Update audit log"""
    with open(LOG_FILE, 'a') as f:
        f.write(f"\n## {datetime.now():%Y-%m-%d} (Ghost-Scan)\n")
        f.write(f"- Ghost files found: {ghost_count}\n")

def main(incremental: bool = True):
    log("Start: KB Ghost Scanner")
    init_output_dir()
    
    mode = "incremental" if incremental else "full"
    log(f"Mode: {mode}")
    
    indexed = get_indexed_files()
    log(f"Indexed files in KB: {len(indexed)}")
    
    files = scan_for_files(incremental=incremental)
    log(f"Scanned files (new/changed): {len(files)}")
    
    ghost_files = find_ghost_files(indexed, files)
    
    # Check for external tool needed
    external_count = sum(1 for g in ghost_files 
                         if any(g['path'].endswith(ext) for ext in EXTERNAL_TOOL_EXTENSIONS))
    
    if ghost_files:
        save_ghost_files(ghost_files)
        update_log(len(ghost_files))
        log(f"Ghost files found: {len(ghost_files)}")
        log(f"CSV saved: {OUTPUT_FILE}")
        if external_count > 0:
            log(f"⚠️  {external_count} files need external tools (docx, epub, etc.)")
    else:
        log("No ghost files found")
    
    log("Done: KB Ghost Scanner")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='KB Ghost Scanner')
    parser.add_argument('--mode', choices=['full', 'incremental'], default='incremental',
                       help='Scan mode: full (all files) or incremental (changed only)')
    args = parser.parse_args()
    main(incremental=(args.mode == 'incremental'))
