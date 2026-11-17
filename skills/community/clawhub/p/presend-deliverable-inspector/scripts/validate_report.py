#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED = {
    "artifact_type",
    "audience",
    "context_basis",
    "verdict",
    "must_fix",
    "additional_findings",
    "finding_overflow",
    "can_keep",
    "repair_route",
    "unverified_items",
    "confidence",
}
VERDICTS = {
    "can_send",
    "send_after_quick_fixes",
    "hold_before_send",
    "rework_before_send",
}


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_report.py <inspection.json>")
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    missing = sorted(REQUIRED - set(data))
    if missing:
        raise AssertionError(f"missing fields: {missing}")
    if data["verdict"] not in VERDICTS:
        raise AssertionError(f"bad verdict: {data['verdict']}")
    context = data["context_basis"]
    for key in (
        "recipient",
        "target_action",
        "deadline",
        "material_stage",
        "known_limits",
        "missing_context",
        "context_signals",
        "risk_weighting",
    ):
        if key not in context:
            raise AssertionError(f"context_basis missing {key}")
    if not context["context_signals"]:
        raise AssertionError("context_basis must include context_signals")
    if not context["risk_weighting"]:
        raise AssertionError("context_basis must include risk_weighting")
    for item in context["context_signals"]:
        for key in ("field", "value", "source", "impact"):
            if not item.get(key):
                raise AssertionError(f"context_signal missing {key}")
    for item in context["risk_weighting"]:
        for key in ("risk_area", "direction", "reason"):
            if not item.get(key):
                raise AssertionError(f"risk_weighting item missing {key}")
    if len(data["must_fix"]) > 7:
        raise AssertionError("must_fix must contain no more than 7 items")
    for item in [*data["must_fix"], *data["additional_findings"]]:
        for key in ("location", "error_family", "error_type", "risk", "context_reason", "evidence", "fix"):
            if not item.get(key):
                raise AssertionError(f"finding item missing {key}")
    overflow = data["finding_overflow"]
    expected_total = len(data["must_fix"]) + len(data["additional_findings"])
    if overflow.get("detected_total") != expected_total:
        raise AssertionError("finding_overflow detected_total does not match finding arrays")
    if overflow.get("displayed_total") != len(data["must_fix"]):
        raise AssertionError("finding_overflow displayed_total does not match must_fix")
    if overflow.get("omitted_total") != len(data["additional_findings"]):
        raise AssertionError("finding_overflow omitted_total does not match additional_findings")
    omitted_blockers = sum(item.get("severity") == "blocker" for item in data["additional_findings"])
    if overflow.get("omitted_blocker_count") != omitted_blockers:
        raise AssertionError("finding_overflow omitted_blocker_count does not match additional_findings")
    if len(overflow.get("omitted_locations", [])) != len(data["additional_findings"]):
        raise AssertionError("finding_overflow must list every omitted finding location")
    if not data["repair_route"]:
        raise AssertionError("repair_route must not be empty")
    print("inspection report validation passed")


if __name__ == "__main__":
    main()
