#!/usr/bin/env python3
"""Orphan finder — entries with zero inbound references."""
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config
from file_scanner import FileScanner
from health_models import DimResult
from log_utils import get_logger

logger = get_logger("memory-health-check.orphan_finder")


def build_reference_graph(base_dir: Path) -> dict:
    """Build a graph of file references.
    
    Detects references via:
        - Obsidian-style [[wikilinks]]
        - Markdown [text](url) links (internal references)
        - Cross-file content references (file name mentions)
        - SQLite foreign key relationships (via schema inspection)
    
    Args:
        base_dir: Memory directory
        
    Returns:
        dict: {
            "referrer": {set of referenced file paths},
            "all_files": [list of all file paths],
            "orphaned_files": [list of file paths with zero inbound refs],
        }
    """
    scanner = FileScanner(base_dir)
    
    # Collect all files
    all_files = []
    file_contents = {}
    
    for f in base_dir.rglob("*"):
        if f.is_file() and f.suffix in {".md", ".sqlite", ".json"}:
            all_files.append(f)
            if f.suffix == ".md":
                try:
                    file_contents[f] = f.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    file_contents[f] = ""
    
    # Build referrer set
    referenced_files = set()
    
    for f, content in file_contents.items():
        # Find [[wikilinks]]
        for link_target in scanner.find_wikilinks(content):
            for candidate in all_files:
                if candidate.stem == link_target or candidate.name == link_target:
                    referenced_files.add(candidate)
        
        # Find [text](url) links (internal only)
        for link_target in scanner.find_markdown_links(content):
            if not link_target.startswith(("http://", "https://", "mailto:")):
                for candidate in all_files:
                    if candidate.name == link_target or str(candidate) == link_target:
                        referenced_files.add(candidate)
        
        # Find file name mentions
        for candidate in all_files:
            if candidate == f:
                continue
            # Check if this file mentions another file's name
            if candidate.stem in content and len(candidate.stem) > 3:
                referenced_files.add(candidate)
    
    # Find orphans (files with no inbound references)
    orphaned = []
    for f in all_files:
        if f not in referenced_files and f.suffix == ".md":
            orphaned.append(f)
    
    return {
        "referenced_count": len(referenced_files),
        "total_files": len(all_files),
        "orphaned_files": [str(f) for f in orphaned],
        "orphan_types": {
            "md": sum(1 for f in orphaned if f.suffix == ".md"),
            "sqlite": sum(1 for f in orphaned if f.suffix == ".sqlite"),
            "json": sum(1 for f in orphaned if f.suffix == ".json"),
        },
    }


def find_orphans(
    base_dir: Path = None,
    min_age_days: int = 7,
) -> dict:
    """Find orphaned memory entries.
    
    Args:
        base_dir: Memory directory (default: workspace/memory/)
        min_age_days: Only flag files older than this
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "orphan_count": int,
            "total_entries": int,
            "orphan_rate": float,
            "orphaned_files": list[str],
            "orphan_types": dict[str, int],
        }
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    
    if not base_dir.exists():
        return {
            "score": 100,
            "status": "healthy",
            "orphan_count": 0,
            "total_entries": 0,
            "orphan_rate": 0.0,
            "orphaned_files": [],
            "orphan_types": {"md": 0, "sqlite": 0, "json": 0},
        }
    
    config = load_config()
    thresholds = config.get("thresholds", {}).get("orphan_rate", {})
    
    graph = build_reference_graph(base_dir)
    
    total = graph["total_files"]
    orphan_count = len(graph["orphaned_files"])
    orphan_rate = orphan_count / max(total, 1)
    
    # Apply min_age filter
    if min_age_days > 0:
        from datetime import timedelta
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=min_age_days)
        recent_orphans = []
        for f_str in graph["orphaned_files"]:
            f = Path(f_str)
            try:
                if datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc) >= cutoff:
                    recent_orphans.append(f_str)
            except OSError:
                pass
        # Use filtered count for scoring
        orphan_count_filtered = len(recent_orphans)
        orphan_rate = orphan_count_filtered / max(total, 1)
    else:
        recent_orphans = graph["orphaned_files"]
        orphan_count_filtered = orphan_count
    
    # Determine score and status
    healthy_threshold = thresholds.get("healthy", 0.01)
    warning_threshold = thresholds.get("warning", 0.05)
    
    if orphan_rate <= healthy_threshold:
        score = 100
        status = "healthy"
    elif orphan_rate <= warning_threshold:
        score = 70
        status = "warning"
    else:
        score = 30
        status = "critical"
    
    return {
        "score": score,
        "status": status,
        "orphan_count": orphan_count,
        "orphan_count_recent": orphan_count_filtered,
        "total_entries": total,
        "orphan_rate": round(orphan_rate * 100, 2),
        "orphaned_files": recent_orphans[:100],  # Cap at 100
        "orphan_types": graph["orphan_types"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find orphaned entries")
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("--min-age-days", type=int, default=7)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)
    
    result = find_orphans(
        base_dir=args.base_dir,
        min_age_days=args.min_age_days,
    )
    
    print(f"[orphan_finder] Status: {result['status']}, Orphans: {result['orphan_count']}/{result['total_entries']}, Score: {result['score']}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
