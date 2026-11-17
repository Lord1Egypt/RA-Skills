#!/usr/bin/env python3
"""Regression checks for the BLOCKED data-quality-only boundary."""

import copy
import unittest

from data_quality_report_guard import validate_data_quality_report


def report():
    return {
        "gate_status": "BLOCKED", "task_type": "data_quality_audit", "status": "data_blocked",
        "data_gate": {"blocked_report": True}, "metrics": [], "judgments": [], "hypotheses": [],
        "missing_data": ["缺少推广花费字段"], "actions": [{"action": "补充原始导出并核对字段"}],
        "claim_ledger": {"claims": [
            {"claim_id": "C-files", "metric": "file_count", "value": 3},
            {"claim_id": "C-missing", "metric": "missing_field_count", "value": 1},
        ]},
    }


class DataQualityReportGuardSmoke(unittest.TestCase):
    def test_quality_only_report_passes(self):
        self.assertEqual(validate_data_quality_report(report())["status"], "data_quality_only_verified")

    def test_blocked_weekly_report_cannot_masquerade_as_quality_audit(self):
        value = report(); value["task_type"] = "weekly_report"
        with self.assertRaisesRegex(ValueError, "blocked_delivery_must_be_data_quality_audit"):
            validate_data_quality_report(value)

    def test_business_claim_is_rejected_even_when_metrics_table_is_empty(self):
        value = report(); value["claim_ledger"]["claims"][0]["metric"] = "gmv"
        with self.assertRaisesRegex(ValueError, "blocked_delivery_business_claim_forbidden"):
            validate_data_quality_report(value)

    def test_blocked_report_requires_a_real_gap(self):
        value = report(); value["missing_data"] = []
        with self.assertRaisesRegex(ValueError, "blocked_delivery_missing_data_required"):
            validate_data_quality_report(value)

    def test_business_action_is_rejected(self):
        value = report(); value["actions"] = [{"action": "提高投放预算"}]
        with self.assertRaisesRegex(ValueError, "blocked_delivery_business_action_forbidden"):
            validate_data_quality_report(value)

    def test_nonblocked_report_is_untouched(self):
        value = report(); value["gate_status"] = "PASS"
        self.assertEqual(validate_data_quality_report(value), {"status": "not_applicable"})


if __name__ == "__main__":
    unittest.main()

