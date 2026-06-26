#!/usr/bin/env python3
"""Aggregates all scanner results, manages issue lifecycle, produces latest_status.json.
Includes: score_history for 30-day radar chart, metadata passthrough, evidence/fix_action.
"""
import os
import json
import glob
from datetime import datetime, timedelta
from utils import get_data_dir, DIMENSION_LABELS, DIMENSION_ORDER


def calculate_score(issues):
    score = 100
    for issue in issues:
        sev = issue.get("severity", "LOW")
        if sev == "HIGH":
            score -= 15
        elif sev == "MEDIUM":
            score -= 5
        elif sev == "LOW":
            score -= 2
    return max(0, score)


def main():
    data_dir = get_data_dir()
    history_file = os.path.join(data_dir, "history.json")
    latest_file = os.path.join(data_dir, "latest_status.json")

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = {
            "stats": {"total_discovered": 0, "total_resolved": 0},
            "per_dimension_resolved": {},
            "score_history": [],
            "issues": {},
        }

    for key in ("per_dimension_resolved", "score_history"):
        if key not in history:
            history[key] = [] if key == "score_history" else {}

    current_time = datetime.now().isoformat()
    today_str = datetime.now().strftime("%Y-%m-%d")
    scan_files = glob.glob(os.path.join(data_dir, "latest_*.json"))

    dimensions = {}
    current_issues = {}

    for fpath in scan_files:
        basename = os.path.basename(fpath)
        if basename == "latest_status.json":
            continue
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            scanner = data.get("scanner", "unknown")
            status = data.get("status", "active")
            issues = data.get("issues", [])
            metadata = data.get("metadata", {})

            dim_label = DIMENSION_LABELS.get(scanner, scanner)
            resolved_count = history.get("per_dimension_resolved", {}).get(scanner, 0)

            if status == "not_applicable":
                dimensions[scanner] = {
                    "label": dim_label,
                    "status": "not_applicable",
                    "na_reason": data.get("na_reason", ""),
                    "score": None,
                    "issues": [],
                    "issue_counts": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
                    "resolved_count": resolved_count,
                    "metadata": metadata,
                    "scanned_at": data.get("scanned_at", current_time),
                }
            else:
                score = calculate_score(issues)
                issue_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
                for iss in issues:
                    sev = iss.get("severity", "LOW")
                    issue_counts[sev] = issue_counts.get(sev, 0) + 1

                dimensions[scanner] = {
                    "label": dim_label,
                    "status": "active",
                    "score": score,
                    "issues": issues,
                    "issue_counts": issue_counts,
                    "resolved_count": resolved_count,
                    "metadata": metadata,
                    "scanned_at": data.get("scanned_at", current_time),
                }

                for issue in issues:
                    current_issues[issue["id"]] = issue
                    current_issues[issue["id"]]["_scanner"] = scanner

        except Exception as e:
            print(f"Error reading {fpath}: {e}")

    # Update history & lifecycles
    active_issues = []

    for issue_id, issue_data in current_issues.items():
        if issue_id not in history["issues"]:
            history["issues"][issue_id] = {
                "id": issue_id,
                "title": issue_data["title"],
                "severity": issue_data["severity"],
                "scanner": issue_data.get("_scanner", issue_id.split("_")[0]),
                "first_seen": current_time,
                "last_seen": current_time,
                "status": "open",
            }
            history["stats"]["total_discovered"] += 1
        else:
            if history["issues"][issue_id]["status"] == "resolved":
                history["issues"][issue_id]["status"] = "open"
            history["issues"][issue_id]["last_seen"] = current_time

        first_seen = datetime.fromisoformat(history["issues"][issue_id]["first_seen"])
        days_open = (datetime.now() - first_seen).days

        active_issue = {k: v for k, v in issue_data.items() if k != "_scanner"}
        active_issue["days_open"] = days_open
        active_issue["first_seen"] = history["issues"][issue_id]["first_seen"]
        active_issue["dimension"] = DIMENSION_LABELS.get(
            history["issues"][issue_id].get("scanner", ""), ""
        )
        active_issues.append(active_issue)

    for issue_id, hist_data in history["issues"].items():
        if issue_id not in current_issues and hist_data["status"] == "open":
            hist_data["status"] = "resolved"
            hist_data["resolved_at"] = current_time
            history["stats"]["total_resolved"] += 1
            scanner_key = hist_data.get("scanner", "")
            history["per_dimension_resolved"][scanner_key] = (
                history["per_dimension_resolved"].get(scanner_key, 0) + 1
            )

    # Append score_history (one entry per day, overwrite same-day)
    current_scores = {}
    for key, dim in dimensions.items():
        if dim["status"] == "active":
            current_scores[key] = dim["score"]

    score_history = history["score_history"]
    if score_history and score_history[-1].get("date") == today_str:
        score_history[-1]["scores"] = current_scores
    else:
        score_history.append({"date": today_str, "scores": current_scores})

    # Keep only last 90 days
    cutoff = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
    history["score_history"] = [e for e in score_history if e["date"] >= cutoff]

    # Calculate 30-day averages for radar chart
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    recent_entries = [e for e in history["score_history"] if e["date"] >= thirty_days_ago]
    avg_scores = {}
    if recent_entries:
        for key in DIMENSION_ORDER:
            values = [e["scores"].get(key) for e in recent_entries if key in e.get("scores", {})]
            if values:
                avg_scores[key] = int(sum(values) / len(values))

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    active_issues.sort(key=lambda x: (
        {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x.get("severity", "LOW")],
        -x.get("days_open", 0),
    ))

    active_dims = {k: v for k, v in dimensions.items() if v["status"] == "active"}
    if active_dims:
        global_score = int(sum(d["score"] for d in active_dims.values()) / len(active_dims))
    else:
        global_score = 100

    # Calculate score delta vs previous scan
    previous_score = None
    score_delta = 0
    if len(history["score_history"]) >= 2:
        prev_entry = history["score_history"][-2]
        prev_scores = prev_entry.get("scores", {})
        if prev_scores:
            prev_active = {k: v for k, v in prev_scores.items() if v is not None}
            if prev_active:
                previous_score = int(sum(prev_active.values()) / len(prev_active))
                score_delta = global_score - previous_score

    ordered_dimensions = {}
    for key in DIMENSION_ORDER:
        if key in dimensions:
            ordered_dimensions[key] = dimensions[key]
    for key in dimensions:
        if key not in ordered_dimensions:
            ordered_dimensions[key] = dimensions[key]

    latest_status = {
        "generated_at": current_time,
        "global_score": global_score,
        "previous_score": previous_score,
        "score_delta": score_delta,
        "stats": {
            "total_discovered": history["stats"]["total_discovered"],
            "total_resolved": history["stats"]["total_resolved"],
            "current_open": len(active_issues),
        },
        "dimensions": ordered_dimensions,
        "active_issues": active_issues,
        "radar_avg_30d": avg_scores,
    }

    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump(latest_status, f, ensure_ascii=False, indent=2)

    delta_str = f" (↑+{score_delta})" if score_delta > 0 else (f" (↓{score_delta})" if score_delta < 0 else "")
    print(f"Watchdog aggregation complete. Global Score: {global_score}/100{delta_str}. Open issues: {len(active_issues)}.")


if __name__ == "__main__":
    main()
