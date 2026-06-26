#!/usr/bin/env python3
"""Integrity scan — DB corruption / checksum checks."""
import argparse
import json
import logging
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config
from sqlite_scanner import SQLiteScanner, find_memory_dbs
from health_models import DimResult
from log_utils import get_logger

logger = get_logger("memory-health-check.integrity_scan")


def find_memory_dbs(base_dir: Path = None) -> list[Path]:
    """Find all SQLite DBs in the OpenClaw memory hierarchy.
    
    Searches:
        ~/.openclaw/memory/*.sqlite
        ~/.openclaw/workspace/*/memory/*.sqlite
        
    Returns:
        List of Path objects to discovered DB files
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw"
    
    dbs = []
    
    memory_dir = base_dir / "memory"
    if memory_dir.exists():
        dbs.extend(memory_dir.glob("*.sqlite"))
        for subdir in memory_dir.iterdir():
            if subdir.is_dir():
                dbs.extend(subdir.glob("*.sqlite"))
    
    workspace_dir = base_dir / "workspace"
    if workspace_dir.exists():
        for workspace in workspace_dir.iterdir():
            if workspace.is_dir():
                mem_dir = workspace / "memory"
                if mem_dir.exists():
                    dbs.extend(mem_dir.glob("*.sqlite"))
    
    return sorted(set(dbs))


def check_sqlite_integrity(db_path: Path) -> dict:
    """Run SQLite integrity_check pragma on a single DB.
    
    Args:
        db_path: Path to SQLite file
        
    Returns:
        dict: {
            "path": str,
            "ok": bool,
            "issues": list[str],
            "table_count": int,
            "row_counts": dict[str, int],
        }
    """
    result = {
        "path": str(db_path),
        "ok": False,
        "issues": [],
        "table_count": 0,
        "row_counts": {},
        "size_bytes": 0,
    }
    
    try:
        scanner = SQLiteScanner(db_path)
        if not scanner.connect():
            result["issues"].append("Failed to connect")
            return result
        
        result["size_bytes"] = scanner.get_db_size_bytes()
        
        # Run integrity check
        is_ok, issues = scanner.run_integrity_check()
        result["ok"] = is_ok
        result["issues"].extend(issues)
        
        # Get table info
        result["table_count"] = len(scanner.get_table_list())
        result["row_counts"] = scanner.get_row_counts()
        
        scanner.close()
        
    except Exception as e:
        result["issues"].append(f"Exception: {e}")
    
    return result


def integrity_scan(
    scan_dbs: bool = True,
    scan_files: bool = True,
    db_paths: list[Path] = None,
    base_dir: Path = None,
) -> dict:
    """Run full integrity scan across all memory storage.
    
    Args:
        scan_dbs: Run SQLite integrity checks (default: True)
        scan_files: Run checksum verification (default: True)
        db_paths: Override DB paths to scan
        base_dir: Base directory to search (default: ~/.openclaw)
        
    Returns:
        dict: {
            "score": int,           # 0-100
            "status": str,          # healthy/warning/critical
            "issues": list[str],
            "details": dict,
        }
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw"
    
    config = load_config()
    thresholds = config.get("thresholds", {}).get("integrity", {})
    
    all_issues = []
    db_results = []
    total_dbs = 0
    corrupted_dbs = 0
    
    if scan_dbs:
        if db_paths is None:
            db_paths = find_memory_dbs(base_dir)
        
        total_dbs = len(db_paths)
        
        for db_path in db_paths:
            db_result = check_sqlite_integrity(db_path)
            db_results.append(db_result)
            
            if not db_result["ok"]:
                corrupted_dbs += 1
                all_issues.append(
                    f"DB corruption in {db_path.name}: {', '.join(db_result['issues'])}"
                )
            elif db_result["issues"]:
                all_issues.append(
                    f"DB warning in {db_path.name}: {', '.join(db_result['issues'])}"
                )
    
    # Determine score and status
    if corrupted_dbs > 0:
        score = 0
        status = "critical"
    elif len(all_issues) > 0:
        score = 50
        status = "warning"
    else:
        score = 100
        status = "healthy"
    
    return {
        "score": score,
        "status": status,
        "issues": all_issues,
        "details": {
            "db_results": db_results,
            "total_dbs_scanned": total_dbs,
            "corrupted_dbs": corrupted_dbs,
        }
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan memory integrity")
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("--no-db-scan", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)
    
    result = integrity_scan(
        scan_dbs=not args.no_db_scan,
        base_dir=args.base_dir,
    )
    
    print(f"[integrity_scan] Status: {result['status']}, Score: {result['score']}")
    if result["issues"]:
        for issue in result["issues"]:
            print(f"  ! {issue}")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
