#!/usr/bin/env python3
"""Coverage helpers for apply-stage reporting."""

from __future__ import annotations

from collections import Counter

from modeio_redact.core.models import ApplyReport, PlanSpan, RedactionPlan


def summarize_apply_coverage(output_text: str, plan: RedactionPlan) -> ApplyReport:
    """Summarize expected vs found placeholders for strict coverage checks."""
    expected_by_placeholder = Counter(span.placeholder for span in plan.spans)
    found_by_placeholder = {
        placeholder: output_text.count(placeholder)
        for placeholder in expected_by_placeholder
    }

    applied_count = 0
    found_count = 0
    missing_by_placeholder = {}
    for placeholder, expected_count in expected_by_placeholder.items():
        found = found_by_placeholder.get(placeholder, 0)
        found_count += found
        covered = min(found, expected_count)
        applied_count += covered
        missing = expected_count - covered
        if missing > 0:
            missing_by_placeholder[placeholder] = missing

    missed_spans = []
    if missing_by_placeholder:
        for span in plan.spans:
            remaining = missing_by_placeholder.get(span.placeholder, 0)
            if remaining <= 0:
                continue
            missed_spans.append(span)
            missing_by_placeholder[span.placeholder] = remaining - 1

    warnings = list(plan.warnings)
    if found_count > plan.expected_count:
        warnings.append(
            "Found more placeholders in output than expected canonical spans; this may indicate duplicate placeholders."
        )

    return ApplyReport(
        expected_count=plan.expected_count,
        found_count=found_count,
        applied_count=applied_count,
        missed_spans=tuple(missed_spans),
        warnings=warnings,
    )


def summarize_redaction_removal_coverage(output_text: str, plan: RedactionPlan) -> ApplyReport:
    """Summarize coverage when redaction removes originals instead of inserting placeholders."""
    expected_by_original = Counter(span.original for span in plan.spans)
    remaining_by_original = {
        original: output_text.count(original)
        for original in expected_by_original
    }

    applied_count = 0
    found_count = 0
    missed_by_original = {}
    for original, expected_count in expected_by_original.items():
        remaining = min(remaining_by_original.get(original, 0), expected_count)
        applied = expected_count - remaining
        applied_count += applied
        found_count += applied
        if remaining > 0:
            missed_by_original[original] = remaining

    missed_spans = []
    if missed_by_original:
        for span in plan.spans:
            remaining = missed_by_original.get(span.original, 0)
            if remaining <= 0:
                continue
            missed_spans.append(span)
            missed_by_original[span.original] = remaining - 1

    return ApplyReport(
        expected_count=plan.expected_count,
        found_count=found_count,
        applied_count=applied_count,
        missed_spans=tuple(missed_spans),
        warnings=list(plan.warnings),
    )
