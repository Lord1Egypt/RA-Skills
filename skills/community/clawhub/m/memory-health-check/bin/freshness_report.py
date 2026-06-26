#!/usr/bin/env python3
"""Freshness report — entry age distribution."""
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config
from file_scanner import FileScanner
from health_models import DimResult
from log_utils import get_logger

logger = get_logger("memory-health-check.freshness_report")


def get_file_age_distribution(
    base_dir: Path,
    reference_date: datetime = None,
) -> dict:
    """Compute age distribution of memory files.
    
    Args:
        base_dir: Memory directory
        reference_date: Reference for "now" (default: now)
        
    Returns:
        dict: {
            "total": int,
            "by_category": {"<7d": n, "7-30d": n, "30-90d": n, ">90d": n},
            "by_percentage": dict[str, float],
        }
    """
    if reference_date is None:
        reference_date = datetime.now(tz=timezone.utc)
    
    week_ago = reference_date - timedelta(days=7)
    month_ago = reference_date - timedelta(days=30)
    quarter_ago = reference_date - timedelta(days=90)
    
    scanner = FileScanner(base_dir)
    
    dist = {"<7d": 0, "7-30d": 0, "30-90d": 0, ">90d": 0, "total": 0}
    
    for _, mtime in scanner.get_file_ages():
        dist["total"] += 1
        if mtime >= week_ago:
            dist["<7d"] += 1
        elif mtime >= month_ago:
            dist["7-30d"] += 1
        elif mtime >= quarter_ago:
            dist["30-90d"] += 1
        else:
            dist[">90d"] += 1
    
    # Compute percentages
    pct = {}
    for k, v in dist.items():
        if k != "total" and dist["total"] > 0:
            pct[k] = round(v / dist["total"] * 100, 2)
    
    return {
        "total": dist["total"],
        "by_category": {k: v for k, v in dist.items() if k != "total"},
        "by_percentage": pct,
    }


def freshness_report(
    base_dir: Path = None,
    reference_date: datetime = None,
) -> dict:
    """Generate freshness report for memory entries.
    
    Args:
        base_dir: Memory directory
        reference_date: Reference for "now" (default: now)
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "recent_7d": int,
            "recent_30d": int,
            "recent_90d": int,
            "stale": int,
            "total": int,
            "freshness_rate": float,
            "age_distribution": dict,
        }
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    
    if not base_dir.exists():
        return {
            "score": 100,
            "status": "healthy",
            "recent_7d": 0,
            "recent_30d": 0,
            "recent_90d": 0,
            "stale": 0,
            "total": 0,
            "freshness_rate": 100.0,
            "age_distribution": {"<7d": 0, "7-30d": 0, "30-90d": 0, ">90d": 0},
        }
    
    if reference_date is None:
        reference_date = datetime.now(tz=timezone.utc)
    
    config = load_config()
    thresholds = config.get("thresholds", {}).get("freshness_rate", {})
    
    dist = get_file_age_distribution(base_dir, reference_date)
    
    recent_7d = dist["by_category"]["<7d"]
    recent_30d = dist["by_category"]["7-30d"]
    recent_90d = dist["by_category"]["30-90d"]
    stale = dist["by_category"][">90d"]
    total = dist["total"]
    
    freshness_rate = (dist["by_category"]["<7d"] + dist["by_category"]["7-30d"]) / max(total, 1)
    
    healthy_rate = thresholds.get("healthy", 0.70)
    warning_rate = thresholds.get("warning", 0.40)
    
    if freshness_rate >= healthy_rate:
        score = 100
        status = "healthy"
    elif freshness_rate >= warning_rate:
        score = 60
        status = "warning"
    else:
        score = 20
        status = "critical"
    
    return {
        "score": score,
        "status": status,
        "recent_7d": recent_7d,
        "recent_30d": recent_30d,
        "recent_90d": recent_90d,
        "stale": stale,
        "total": total,
        "freshness_rate": round(freshness_rate * 100, 2),
        "age_distribution": dist["by_category"],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate freshness report")
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)
    
    result = freshness_report(base_dir=args.base_dir)
    
    print(f"[freshness_report] Status: {result['status']}, Freshness: {result['freshness_rate']}%, Score: {result['score']}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
