#!/usr/bin/env python3
"""Aggregate health score across all dimensions."""
import argparse
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from config_loader import load_config, get_default_weights
from health_models import DimResult, Recommendation, ReportMetadata, HealthReport
from log_utils import get_logger

logger = get_logger("memory-health-check.health_score")


# ─────────────────────────────────────────────────────────────────────────────
# Coverage Analysis (inline)
# ─────────────────────────────────────────────────────────────────────────────

def analyze_coverage(base_dir: Path = None) -> dict:
    """Analyze knowledge domain coverage.
    
    Args:
        base_dir: Memory directory
        
    Returns:
        dict: coverage score and found domains
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    
    config = load_config()
    domains = config.get("knowledge_domains", [])
    keywords = config.get("coverage_keywords", {})
    
    domain_found = {d: False for d in domains}
    
    if base_dir.exists():
        for f in base_dir.rglob("*.md"):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore").lower()
                for domain in domains:
                    domain_keywords = keywords.get(domain, [])
                    for kw in domain_keywords:
                        if kw.lower() in content:
                            domain_found[domain] = True
                            break
            except Exception:
                pass
    
    found_count = sum(domain_found.values())
    coverage_rate = found_count / max(len(domains), 1)
    
    thresholds = config.get("thresholds", {}).get("coverage_rate", {})
    healthy_rate = thresholds.get("healthy", 0.80)
    warning_rate = thresholds.get("warning", 0.50)
    
    if coverage_rate >= healthy_rate:
        score = 100
        status = "healthy"
    elif coverage_rate >= warning_rate:
        score = 60
        status = "warning"
    else:
        score = 20
        status = "critical"
    
    return {
        "score": score,
        "status": status,
        "domains_found": [d for d, found in domain_found.items() if found],
        "domains_missing": [d for d, found in domain_found.items() if not found],
        "coverage_rate": round(coverage_rate * 100, 2),
    }


# ─────────────────────────────────────────────────────────────────────────────
# Recommendations Engine
# ─────────────────────────────────────────────────────────────────────────────

def generate_recommendations(dimensions: dict[str, dict]) -> list[Recommendation]:
    """Generate actionable recommendations from dimension scores.
    
    Args:
        dimensions: Dict mapping dimension name → result dict
        
    Returns:
        list of Recommendation dataclass instances
    """
    recommendations = []
    
    for dim_name, result in dimensions.items():
        score = result.get("score", 100)
        status = result.get("status", "healthy")
        
        if score < 50 or status == "critical":
            sev = "critical"
            auto = False
            if dim_name == "integrity":
                recommendations.append(Recommendation(
                    dimension=dim_name,
                    severity=sev,
                    action="CRITICAL: Database corruption detected. Run sqlite3 .recover or restore from backup.",
                    auto_repairable=False,
                    effort="high",
                ))
            elif dim_name == "bloat":
                recommendations.append(Recommendation(
                    dimension=dim_name,
                    severity=sev,
                    action="CRITICAL: Memory bloat is severe. Run dreaming-optimizer to consolidate entries.",
                    auto_repairable=True,
                    cli_command="~/.openclaw/workspace/skills/dreaming-optimizer/bin/optimize.sh",
                    effort="medium",
                ))
            elif dim_name == "orphans":
                recommendations.append(Recommendation(
                    dimension=dim_name,
                    severity=sev,
                    action="CRITICAL: High orphan rate. Review and remove orphaned files manually.",
                    auto_repairable=False,
                    effort="medium",
                ))
            elif dim_name == "dedup":
                recommendations.append(Recommendation(
                    dimension=dim_name,
                    severity=sev,
                    action="CRITICAL: High duplicate rate. Run dreaming-optimizer dedup.",
                    auto_repairable=True,
                    cli_command="~/.openclaw/workspace/skills/dreaming-optimizer/bin/deduplicate.py",
                    effort="medium",
                ))
            elif dim_name == "freshness":
                recommendations.append(Recommendation(
                    dimension=dim_name,
                    severity=sev,
                    action="CRITICAL: Memory is stale. Add new entries to refresh memory.",
                    auto_repairable=False,
                    effort="low",
                ))
            elif dim_name == "coverage":
                recommendations.append(Recommendation(
                    dimension=dim_name,
                    severity=sev,
                    action="CRITICAL: Low knowledge coverage. Diversify memory content.",
                    auto_repairable=False,
                    effort="medium",
                ))
        elif score < 70 or status == "warning":
            recommendations.append(Recommendation(
                dimension=dim_name,
                severity="warning",
                action=f"WARNING: {dim_name} dimension needs attention (score={score})",
                auto_repairable=True,
                effort="low",
            ))
    
    return recommendations


# ─────────────────────────────────────────────────────────────────────────────
# Main Health Score Aggregator
# ─────────────────────────────────────────────────────────────────────────────

def aggregate_dimensions(
    integrity: dict,
    bloat: dict,
    orphans: dict,
    dedup: dict,
    freshness: dict,
    coverage: dict = None,
) -> dict:
    """Aggregate all dimension results into overall health score.
    
    Args:
        integrity: Result from integrity_scan()
        bloat: Result from bloat_detection()
        orphans: Result from find_orphans()
        dedup: Result from dedup_scan()
        freshness: Result from freshness_report()
        coverage: Result from analyze_coverage() (optional)
        
    Returns:
        dict: {
            "overall_score": float,
            "status": str,
            "dimensions": dict[str, int],  # name → score
            "weights": dict[str, float],
        }
    """
    config = load_config()
    weights = config.get("weights", get_default_weights())
    
    scores = {
        "integrity": integrity.get("score", 100),
        "bloat": bloat.get("score", 100),
        "orphans": orphans.get("score", 100),
        "dedup": dedup.get("score", 100),
        "freshness": freshness.get("score", 100),
    }
    
    if coverage is not None:
        scores["coverage"] = coverage.get("score", 100)
    else:
        scores["coverage"] = 100  # Default
    
    # Compute weighted average
    overall = sum(scores[k] * weights.get(k, 0) for k in scores)
    
    if overall >= 80:
        status = "healthy"
    elif overall >= 50:
        status = "warning"
    else:
        status = "critical"
    
    return {
        "overall_score": round(overall, 1),
        "status": status,
        "dimensions": scores,
        "weights": weights,
    }


def health_score(
    base_dir: Path = None,
    run_all: bool = True,
    run_dims: list[str] = None,
) -> dict:
    """Public API — run full or partial health check.
    
    Args:
        base_dir: Override base directory
        run_all: Run all 6 dimensions (default: True)
        run_dims: Specific dimensions to run (overrides run_all)
                  Options: ["integrity", "bloat", "orphans", "dedup", "freshness", "coverage"]
        
    Returns:
        Full health report dict
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw" / "workspace"
    
    memory_dir = base_dir / "memory"
    
    dims_to_run = run_dims or []
    if run_all:
        dims_to_run = ["integrity", "bloat", "orphans", "dedup", "freshness", "coverage"]
    
    results = {}
    
    start_time = datetime.now()
    
    if "integrity" in dims_to_run:
        from integrity_scan import integrity_scan
        results["integrity"] = integrity_scan(base_dir=base_dir)
    
    if "bloat" in dims_to_run:
        from bloat_detector import bloat_detection
        results["bloat"] = bloat_detection(base_dir=memory_dir)
    
    if "orphans" in dims_to_run:
        from orphan_finder import find_orphans
        results["orphans"] = find_orphans(base_dir=memory_dir)
    
    if "dedup" in dims_to_run:
        from dedup_scanner import dedup_scan
        results["dedup"] = dedup_scan(base_dir=memory_dir)
    
    if "freshness" in dims_to_run:
        from freshness_report import freshness_report
        results["freshness"] = freshness_report(base_dir=memory_dir)
    
    if "coverage" in dims_to_run:
        results["coverage"] = analyze_coverage(base_dir=memory_dir)
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    # Aggregate
    aggregated = aggregate_dimensions(
        integrity=results.get("integrity", {}),
        bloat=results.get("bloat", {}),
        orphans=results.get("orphans", {}),
        dedup=results.get("dedup", {}),
        freshness=results.get("freshness", {}),
        coverage=results.get("coverage"),
    )
    
    # Generate recommendations
    recommendations = generate_recommendations(results)
    
    # Build auto-repair plan
    auto_repair = [r.action for r in recommendations if r.auto_repairable]
    
    metadata = ReportMetadata(
        generated_at=datetime.now(tz=timezone.utc).isoformat(),
        agent_name="main",
        scan_duration_seconds=round(elapsed, 2),
        db_count=results.get("integrity", {}).get("details", {}).get("total_dbs_scanned", 0),
        file_count=results.get("bloat", {}).get("file_counts", {}).get("total", 0),
    )
    
    report = HealthReport(
        ts=metadata.generated_at,
        overall_score=aggregated["overall_score"],
        status=aggregated["status"],
        dimensions={
            k: DimResult(
                score=v.get("score", 0),
                status=v.get("status", "unknown"),
                value=v,
                details=v.get("details", {}),
                issues=v.get("issues", []),
            )
            for k, v in results.items()
        },
        recommendations=recommendations,
        auto_repair_plan=auto_repair,
        metadata=metadata,
    )
    
    return report.to_dict()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute health score")
    parser.add_argument("--base-dir", type=Path, default=None)
    parser.add_argument("--dims", type=str, default=None,
                        help="Comma-separated dims to run")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    
    if args.verbose:
        import logging
        get_logger().setLevel(logging.DEBUG)
    
    run_dims = None
    if args.dims:
        run_dims = [d.strip() for d in args.dims.split(",")]
    
    result = health_score(base_dir=args.base_dir, run_dims=run_dims)
    
    print(f"[health_score] Overall: {result['overall_score']}/100, Status: {result['status']}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
