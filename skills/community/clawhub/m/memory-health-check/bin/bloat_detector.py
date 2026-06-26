#!/usr/bin/env python3
"""Bloat detection — DB size, file count, growth rate."""
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
from health_models import DimResult, GrowthRate
from log_utils import get_logger

logger = get_logger("memory-health-check.bloat_detector")


def get_dir_size(path: Path, follow_symlinks: bool = False) -> int:
    """Recursively compute directory size in bytes.
    
    Args:
        path: Directory path
        follow_symlinks: Whether to follow symlinks
        
    Returns:
        Total bytes
    """
    total = 0
    try:
        for f in path.rglob("*"):
            if f.is_file() and (follow_symlinks or not f.is_symlink()):
                try:
                    total += f.stat().st_size
                except OSError:
                    pass
    except Exception:
        pass
    return total


def get_file_counts(base_dir: Path) -> dict:
    """Count files by extension/type.
    
    Returns:
        dict: {"total": int, "md": int, "sqlite": int, "json": int, "other": int}
    """
    scanner = FileScanner(base_dir)
    return scanner.get_file_counts()


def get_growth_rate(
    base_dir: Path,
    report_dir: Path = None,
    snapshots: int = 4,
    interval_days: int = 7,
) -> Optional[GrowthRate]:
    """Estimate growth rate by comparing recent health reports.
    
    Reads previous health reports to get historical sizes.
    
    Args:
        base_dir: Base directory for health reports
        report_dir: Where health reports are stored
        snapshots: Number of historical points to compare
        interval_days: Expected interval between reports
        
    Returns:
        GrowthRate dict or None if insufficient data
    """
    if report_dir is None:
        report_dir = base_dir / "memory" / "health-reports"
    
    if not report_dir.exists():
        return None
    
    # Find recent report files
    reports = sorted(report_dir.glob("health-report-*.json"), reverse=True)
    
    if len(reports) < 2:
        return None
    
    # Read size from reports
    sizes_mb = []
    dates = []
    
    for report_file in reports[:snapshots]:
        try:
            data = json.loads(report_file.read_text(encoding="utf-8"))
            # Try to find bloat info in dimensions
            if "dimensions" in data and "bloat" in data["dimensions"]:
                mb = data["dimensions"]["bloat"].get("value", {}).get("total_mb", 0)
                sizes_mb.append(mb)
                dates.append(report_file.stat().st_mtime)
        except Exception:
            pass
    
    if len(sizes_mb) < 2:
        return None
    
    # Simple linear growth estimation
    n = len(sizes_mb)
    if n < 2:
        return None
    
    # Simple linear regression
    x = list(range(n))  # [0, 1, 2, ...]
    x_mean = sum(x) / n
    y_mean = sum(sizes_mb) / n
    
    numerator = sum((x[i] - x_mean) * (sizes_mb[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        slope = 0.0
    else:
        slope = numerator / denominator
    
    growth_per_week = slope * (7 / max(interval_days, 1))
    current_size = sizes_mb[0]
    projected_90d = current_size + (growth_per_week * (90 / 7))
    
    if growth_per_week > 10:
        trend = "increasing"
    elif growth_per_week < -10:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return GrowthRate(
        growth_rate_mb_per_week=round(growth_per_week, 2),
        trend=trend,
        projected_90d_mb=round(projected_90d, 2),
        historical_points=n,
        method="linear",
    )


def bloat_detection(
    base_dir: Path = None,
    include_growth: bool = True,
) -> dict:
    """Detect memory bloat across all storage layers.
    
    Args:
        base_dir: Override base directory (default: ~/.openclaw/workspace)
        include_growth: Include growth rate projection
        
    Returns:
        dict: {
            "score": int,
            "status": str,
            "total_bytes": int,
            "total_mb": float,
            "file_counts": dict,
            "growth_rate": dict | None,
            "projected_critical_date": str | None,
        }
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw" / "workspace"
    
    config = load_config()
    thresholds = config.get("thresholds", {}).get("bloat_mb", {})
    healthy_mb = thresholds.get("healthy", 500)
    warning_mb = thresholds.get("warning", 2000)
    critical_mb = thresholds.get("critical", 5000)
    
    memory_dir = base_dir / "memory"
    
    if not memory_dir.exists():
        return {
            "score": 100,
            "status": "healthy",
            "total_bytes": 0,
            "total_mb": 0.0,
            "file_counts": {"total": 0, "md": 0, "sqlite": 0, "json": 0, "other": 0},
            "growth_rate": None,
            "projected_critical_date": None,
        }
    
    total_bytes = get_dir_size(memory_dir)
    total_mb = total_bytes / (1024 * 1024)
    file_counts = get_file_counts(memory_dir)
    
    # Determine score and status
    if total_mb < healthy_mb:
        status = "healthy"
        score = 100
    elif total_mb < warning_mb:
        status = "warning"
        score = 60
    else:
        status = "critical"
        score = 20
    
    # Growth rate analysis
    growth_rate = None
    projected_critical = None
    
    if include_growth:
        growth_rate = get_growth_rate(base_dir)
        
        if growth_rate and growth_rate.projected_90d_mb > critical_mb:
            # Project when we'll hit critical
            if growth_rate.growth_rate_mb_per_week > 0:
                weeks_to_critical = (critical_mb - total_mb) / max(growth_rate.growth_rate_mb_per_week, 0.1)
                days_to_critical = int(weeks_to_critical * 7)
                future_date = datetime.now(tz=timezone.utc) + timedelta(days=days_to_critical)
                projected_critical = future_date.strftime("%Y-%m-%d")
    
    return {
        "score": score,
        "status": status,
        "total_bytes": total_bytes,
        "total_mb": round(total_mb, 2),
        "file_counts": file_counts,
        "growth_rate": {
            "growth_rate_mb_per_week": growth_rate.growth_rate_mb_per_week if growth_rate else 0,
            "trend": growth_rate.trend if growth_rate else "unknown",
            "projected_90d_mb": growth_rate.projected_90d_mb if growth_rate else None,
            "historical_points": growth_rate.historical_points if growth_rate else 0,
        } if growth_rate else None,
        "projected_critical_date": projected_critical,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect memory bloat")
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("--no-growth", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)
    
    result = bloat_detection(
        base_dir=args.base_dir,
        include_growth=not args.no_growth,
    )
    
    print(f"[bloat_detector] Status: {result['status']}, Size: {result.get('total_mb', 0)}MB, Score: {result['score']}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
