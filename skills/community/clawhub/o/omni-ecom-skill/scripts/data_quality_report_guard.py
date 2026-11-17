#!/usr/bin/env python3
"""Keep BLOCKED deliveries limited to auditable data-quality facts."""

from __future__ import annotations

import re
from typing import Any


ALLOWED_METRICS = {
    "report_count", "file_count", "sheet_count", "row_count", "column_count",
    "source_count", "available_metric_count", "blocked_metric_count",
    "missing_field_count", "duplicate_row_count", "invalid_row_count",
    "parse_error_count", "coverage_rate", "completeness_rate",
    "period_coverage_rate",
}
FORBIDDEN_ACTION = re.compile(
    r"预算|加投|投放|调价|降价|提价|库存补货|发布|利润|ROAS|ROI|CPC|CAC|GMV|销售|成交|转化",
    re.I,
)


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def validate_data_quality_report(report: dict[str, Any]) -> dict[str, Any]:
    """Recheck the fail-closed report after build and again at completion."""
    if report.get("gate_status") != "BLOCKED":
        return {"status": "not_applicable"}
    require(report.get("task_type") == "data_quality_audit",
            "blocked_delivery_must_be_data_quality_audit")
    require(report.get("status") == "data_blocked", "blocked_delivery_status_invalid")
    data_gate = report.get("data_gate")
    require(isinstance(data_gate, dict) and data_gate.get("blocked_report") is True,
            "blocked_delivery_marker_missing")
    require(report.get("metrics") == [], "blocked_delivery_business_metrics_forbidden")
    require(report.get("judgments") == [], "blocked_delivery_judgments_forbidden")
    require(report.get("hypotheses") == [], "blocked_delivery_hypotheses_forbidden")
    require(bool(report.get("missing_data")), "blocked_delivery_missing_data_required")

    ledger = report.get("claim_ledger")
    require(isinstance(ledger, dict) and isinstance(ledger.get("claims"), list) and ledger["claims"],
            "blocked_delivery_quality_claims_required")
    metrics: list[str] = []
    for claim in ledger["claims"]:
        require(isinstance(claim, dict), "blocked_delivery_claim_invalid")
        metric = str(claim.get("metric") or "")
        require(metric in ALLOWED_METRICS, "blocked_delivery_business_claim_forbidden:" + metric)
        metrics.append(metric)

    for action in report.get("actions", []):
        require(isinstance(action, dict), "blocked_delivery_action_invalid")
        require(not FORBIDDEN_ACTION.search(str(action.get("action") or "")),
                "blocked_delivery_business_action_forbidden")
    return {"status": "data_quality_only_verified", "quality_claim_metrics": metrics}

