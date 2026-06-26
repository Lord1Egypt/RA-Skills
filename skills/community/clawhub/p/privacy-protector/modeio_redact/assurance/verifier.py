#!/usr/bin/env python3
"""Verification helpers for post-redaction checks."""

from __future__ import annotations

from modeio_redact.assurance.residual_scan import scan_for_residuals
from modeio_redact.core.models import RedactionPlan, VerificationReport
from modeio_redact.workflow.file_workflow import strip_embedded_map_marker


def verify_content_against_plan(text: str, plan: RedactionPlan, *, part_id: str) -> VerificationReport:
    """Verify no original values from plan remain in output text."""
    normalized = strip_embedded_map_marker(text)
    residuals = scan_for_residuals(normalized, plan.mapping_entries, part_id=part_id)
    return VerificationReport(
        passed=(len(residuals) == 0),
        skipped=False,
        residual_count=len(residuals),
        residuals=residuals,
        warnings=[],
    )
