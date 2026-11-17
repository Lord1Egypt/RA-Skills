"""trend_tracker.py — Track drift scores over time and warn before threshold breach.

Run after each monitor run to append scores to monitor_trend.jsonl and detect
downward trends before they cross the failure threshold.

Usage:
    python scripts/trend_tracker.py
    python scripts/trend_tracker.py --report monitor_report.json --window 5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_report(path: Path) -> dict:
    if not path.exists():
        print(f"ERROR: Report not found at {path}")
        print("Run run_monitor.py first.")
        sys.exit(1)
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Could not parse {path}: {e}")
        sys.exit(1)


def append_to_trend_log(report: dict, log_path: Path) -> None:
    """Append one row per test result from this report run."""
    timestamp = report.get("timestamp", "")
    with open(log_path, "a") as f:
        for result in report.get("results", []):
            drift = result.get("drift") or {}
            row = {
                "timestamp": timestamp,
                "test_name": result["name"],
                "provider": result["provider"],
                "model": result["model"],
                "passed": result["passed"],
                "drift_score": drift.get("score"),
                "drift_threshold": drift.get("threshold"),
                "drift_enabled": drift.get("enabled", False),
            }
            f.write(json.dumps(row) + "\n")


def load_trend_log(log_path: Path) -> dict[str, list[dict]]:
    """Load trend log and return dict of test_name -> list of rows (oldest first)."""
    history: dict[str, list[dict]] = {}
    if not log_path.exists():
        return history
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
                name = row["test_name"]
                history.setdefault(name, []).append(row)
            except Exception:
                continue
    return history


def check_trends(history: dict[str, list[dict]], window: int) -> list[str]:
    """Return list of warning messages for tests trending toward failure."""
    warnings = []
    for test_name, rows in history.items():
        # Only rows with drift enabled and a numeric score
        scored = [r for r in rows if r.get("drift_enabled") and r.get("drift_score") is not None]
        if len(scored) < 3:
            continue

        recent = scored[-window:]
        scores = [r["drift_score"] for r in recent]
        threshold = recent[-1].get("drift_threshold") or 0.80

        # Check strictly declining over the window
        declining = all(scores[i] > scores[i + 1] for i in range(len(scores) - 1))
        current = scores[-1]
        near_threshold = current < threshold + 0.10

        if declining and near_threshold:
            drop = scores[0] - current
            warnings.append(
                f"  [TREND WARNING] {test_name}: drift score declining for {len(recent)} runs "
                f"({scores[0]:.3f} -> {current:.3f}, drop of {drop:.3f}). "
                f"Threshold: {threshold}. Failure imminent if trend continues."
            )

    return warnings


def write_trend_warnings(warnings: list[str], warnings_path: Path) -> None:
    """Write trend warnings to JSON file so send_alert.py can pick them up."""
    data = {"warnings": warnings}
    with open(warnings_path, "w") as f:
        json.dump(data, f, indent=2)


def clear_trend_warnings(warnings_path: Path) -> None:
    """Remove stale warnings file when no trends are detected."""
    if warnings_path.exists():
        warnings_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Track LLM drift scores over time and warn before threshold breach."
    )
    parser.add_argument(
        "--report",
        default="monitor_report.json",
        metavar="PATH",
        help="Path to monitor_report.json (default: monitor_report.json)",
    )
    parser.add_argument(
        "--log",
        default="monitor_trend.jsonl",
        metavar="PATH",
        help="Path to trend log file (default: monitor_trend.jsonl)",
    )
    parser.add_argument(
        "--warnings-file",
        default="trend_warnings.json",
        metavar="PATH",
        help="Path to write trend warnings for send_alert.py (default: trend_warnings.json)",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=5,
        metavar="N",
        help="Number of recent runs to check for trend (default: 5)",
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check trends, do not append current report to log",
    )
    args = parser.parse_args()

    report_path = Path(args.report)
    log_path = Path(args.log)
    warnings_path = Path(args.warnings_file)

    report = load_report(report_path)

    if not args.check_only:
        append_to_trend_log(report, log_path)
        print(f"Trend log updated: {log_path}")

    history = load_trend_log(log_path)
    warnings = check_trends(history, args.window)

    if warnings:
        print("\nTrend analysis:")
        for w in warnings:
            print(w)
        print()
        write_trend_warnings(warnings, warnings_path)
        print(f"Trend warnings written to {warnings_path} — send_alert.py will include them.")
        sys.exit(2)  # Exit 2 = trend warning (not a hard failure)
    else:
        clear_trend_warnings(warnings_path)
        total_tracked = sum(
            1 for rows in history.values()
            if any(r.get("drift_enabled") and r.get("drift_score") is not None for r in rows)
        )
        print(f"Trend analysis: no declining trends detected ({total_tracked} test(s) tracked).")


if __name__ == "__main__":
    main()
