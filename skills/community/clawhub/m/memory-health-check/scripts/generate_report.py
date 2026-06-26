#!/usr/bin/env python3
"""Generate health report."""
import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
logger = logging.getLogger("generate_report")

SKILL_DIR = Path(__file__).parent.parent
SKILL_BIN = SKILL_DIR / "bin"
REPORT_DIR = Path.home() / ".openclaw" / "workspace" / "memory" / "health-reports"


def parse_json_output(output: str) -> dict:
    """Parse the last JSON object from script output (robust)."""
    depth = 0
    start = -1
    for i, ch in enumerate(output):
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and start >= 0:
                try:
                    return json.loads(output[start:i+1])
                except json.JSONDecodeError:
                    pass
    return {}


def run_script(script_name: str) -> dict:
    """Run a bin script and parse its JSON output."""
    script_path = SKILL_BIN / script_name
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), "--json"],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            parsed = parse_json_output(result.stdout)
            if parsed:
                return parsed
            logger.warning(f"No valid JSON from {script_name}: {result.stdout[:100]}")
        else:
            logger.warning(f"{script_name} exited {result.returncode}: {result.stderr[:200]}")
    except subprocess.TimeoutExpired:
        logger.warning(f"{script_name} timed out")
    except Exception as e:
        logger.warning(f"Error running {script_name}: {e}")
    return {}


def generate_recommendations(results: dict) -> list[dict]:
    """Generate actionable recommendations based on dimension scores."""
    recommendations = []

    dim_scores = results.get("dimensions", {})
    dim_status = results.get("dimension_status", {})

    for dim in ["integrity", "bloat", "orphans", "dedup", "freshness"]:
        score = dim_scores.get(dim, 100)
        status = dim_status.get(dim, "unknown")

        if status == "critical" or (isinstance(score, (int, float)) and score < 50):
            recommendations.append({
                "priority": "high",
                "dimension": dim,
                "message": f"CRITICAL: {dim} needs immediate attention (score: {score})",
            })
        elif status == "warning" or (isinstance(score, (int, float)) and score >= 50 and score < 80):
            recommendations.append({
                "priority": "medium",
                "dimension": dim,
                "message": f"WARNING: {dim} could be improved (score: {score})",
            })

    # Add bloat-specific recommendations
    if dim_scores.get("bloat", 100) < 80:
        recommendations.append({
            "priority": "medium",
            "dimension": "bloat",
            "message": "Consider running --auto-repair or manually cleaning old memory files",
        })

    return recommendations


def generate_report(verbose: bool = False) -> dict:
    """Generate a comprehensive health report."""
    if verbose:
        logger.setLevel(logging.DEBUG)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Collecting health data...")

    # Gather all dimension results
    integrity = run_script("integrity_scan.py")
    bloat = run_script("bloat_detector.py")
    orphans = run_script("orphan_finder.py")
    dedup = run_script("dedup_scanner.py")
    freshness = run_script("freshness_report.py")

    dim_scores = {
        "integrity": integrity.get("score", 0) if isinstance(integrity, dict) else 0,
        "bloat": bloat.get("score", 0) if isinstance(bloat, dict) else 0,
        "orphans": orphans.get("score", 0) if isinstance(orphans, dict) else 0,
        "dedup": dedup.get("score", 0) if isinstance(dedup, dict) else 0,
        "freshness": freshness.get("score", 0) if isinstance(freshness, dict) else 0,
    }
    dim_status = {
        "integrity": integrity.get("status", "unknown") if isinstance(integrity, dict) else "unknown",
        "bloat": bloat.get("status", "unknown") if isinstance(bloat, dict) else "unknown",
        "orphans": orphans.get("status", "unknown") if isinstance(orphans, dict) else "unknown",
        "dedup": dedup.get("status", "unknown") if isinstance(dedup, dict) else "unknown",
        "freshness": freshness.get("status", "unknown") if isinstance(freshness, dict) else "unknown",
    }

    weights = {"integrity": 0.30, "bloat": 0.20, "orphans": 0.15, "dedup": 0.15, "freshness": 0.20}
    overall = round(sum(dim_scores[k] * weights[k] for k in weights), 1)
    overall_status = "healthy" if overall >= 80 else ("warning" if overall >= 50 else "critical")

    recommendations = generate_recommendations({
        "dimensions": dim_scores,
        "dimension_status": dim_status,
    })

    report = {
        "ts": datetime.now(tz=timezone.utc).isoformat(),
        "overall_score": overall,
        "status": overall_status,
        "dimensions": {
            "integrity": {"score": dim_scores["integrity"], "status": dim_status["integrity"]},
            "bloat": {"score": dim_scores["bloat"], "status": dim_status["bloat"], "total_mb": bloat.get("total_mb", 0) if isinstance(bloat, dict) else 0},
            "orphans": {"score": dim_scores["orphans"], "status": dim_status["orphans"], "orphan_count": orphans.get("orphan_count", 0) if isinstance(orphans, dict) else 0},
            "dedup": {"score": dim_scores["dedup"], "status": dim_status["dedup"], "dup_count": dedup.get("dup_count", 0) if isinstance(dedup, dict) else 0},
            "freshness": {"score": dim_scores["freshness"], "status": dim_status["freshness"], "freshness_rate": freshness.get("freshness_rate", 0) if isinstance(freshness, dict) else 0},
        },
        "recommendations": recommendations,
    }

    # Save report
    date_str = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d_%H-%M")
    report_file = REPORT_DIR / f"health-report-{date_str}.json"
    report_file.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    logger.info(f"Report saved to {report_file}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Generate health report")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    result = generate_report(verbose=args.verbose)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"[generate_report] Overall: {result['overall_score']}/100 ({result['status']})")
        for rec in result.get("recommendations", []):
            print(f"  [{rec['priority'].upper()}] {rec['message']}")
        print(f"\nFull report saved to {REPORT_DIR}")


if __name__ == "__main__":
    main()
