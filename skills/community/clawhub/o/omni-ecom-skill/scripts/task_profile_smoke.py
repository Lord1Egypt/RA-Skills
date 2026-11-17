#!/usr/bin/env python3
"""Validate the supported report-task catalog and its collaboration defaults."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "config" / "task-profiles.json"
EXPECTED = {
    "store_diagnosis", "weekly_report", "monthly_report", "quarterly_report",
    "annual_report", "campaign_review", "data_quality_audit", "single_topic",
}
COMPREHENSIVE = {
    "store_diagnosis", "weekly_report", "monthly_report", "quarterly_report",
    "annual_report", "campaign_review",
}
REQUIRED_DELIVERY = {"report.json", "report.md", "report.pdf", "pdf-delivery.json"}


def main() -> int:
    try:
        payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8-sig"))
        profiles = payload.get("profiles", {})
        if payload.get("schema_version") != "1.0" or set(profiles) != EXPECTED:
            raise ValueError("task_profile_catalog_mismatch")
        if payload.get("default_task_type") not in EXPECTED:
            raise ValueError("default_task_type_invalid")
        results = []
        for task_type in sorted(EXPECTED):
            profile = profiles[task_type]
            expected_mode = "comprehensive" if task_type in COMPREHENSIVE else "single_point"
            valid = (
                profile.get("default_collaboration_mode") == expected_mode
                and int(profile.get("minimum_charts", 0)) >= 3
                and REQUIRED_DELIVERY.issubset(set(profile.get("required_delivery", [])))
                and bool(profile.get("comparison_expectation"))
                and bool(profile.get("decision_focus"))
            )
            results.append({"task_type": task_type, "status": "PASS" if valid else "FAIL"})
        failed = [item for item in results if item["status"] != "PASS"]
        print(json.dumps({
            "status": "PASS" if not failed else "FAIL",
            "total": len(results),
            "passed": len(results) - len(failed),
            "failed": len(failed),
            "results": results,
        }, ensure_ascii=False, indent=2))
        return 0 if not failed else 1
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "reason": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
