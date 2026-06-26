#!/usr/bin/env python3
"""Output and assurance helpers for anonymize CLI."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from modeio_redact.core.models import InputSource, MapRef, MappingEntry
from modeio_redact.core.pipeline import RedactionFilePipeline, to_pipeline_input_source
from modeio_redact.core.policy import AssurancePolicy
from modeio_redact.workflow.file_workflow import resolve_output_path


def append_warning(data: Dict[str, Any], code: str, message: str) -> None:
    warnings = data.get("warnings")
    if not isinstance(warnings, list):
        warnings = []
        data["warnings"] = warnings
    warnings.append({"code": code, "message": message})


def persist_output_file(
    input_path: Optional[str],
    output_arg: Optional[str],
    in_place: bool,
    output_tag: str,
) -> Optional[Path]:
    return resolve_output_path(
        input_path=input_path,
        output_path=output_arg,
        in_place=in_place,
        output_tag=output_tag,
    )


def assurance_policy_for_run(*, input_extension: Optional[str]) -> AssurancePolicy:
    extension = (input_extension or "").strip().lower()
    policy = AssurancePolicy.verified() if extension in (".docx", ".pdf") else AssurancePolicy.best_effort()
    return policy.with_coverage_enforced()


def serialize_apply_report(apply_report: Any) -> Dict[str, Any]:
    return {
        "expectedCount": apply_report.expected_count,
        "foundCount": apply_report.found_count,
        "appliedCount": apply_report.applied_count,
        "missingCount": max(apply_report.expected_count - apply_report.applied_count, 0),
        "missedSpans": [
            {
                "placeholder": span.placeholder,
                "type": span.entity_type,
                "start": span.start,
                "end": span.end,
            }
            for span in apply_report.missed_spans
        ],
        "warnings": list(apply_report.warnings),
    }


def serialize_verification_report(verification_report: Any) -> Dict[str, Any]:
    return {
        "passed": verification_report.passed,
        "skipped": verification_report.skipped,
        "residualCount": verification_report.residual_count,
        "residuals": [
            {
                "partId": finding.part_id,
                "text": finding.text,
                "evidence": finding.evidence,
            }
            for finding in verification_report.residuals
        ],
        "warnings": list(verification_report.warnings),
    }


def serialize_assurance_policy(policy: AssurancePolicy) -> Dict[str, Any]:
    return {
        "level": policy.level,
        "failOnCoverageMismatch": policy.fail_on_coverage_mismatch,
        "failOnResidualFindings": policy.fail_on_residual_findings,
    }


def run_file_pipeline(
    *,
    input_source: InputSource,
    input_path: Optional[str],
    input_extension: Optional[str],
    output_arg: Optional[str],
    in_place: bool,
    anonymized_content: str,
    entries: List[MappingEntry],
    map_ref: Optional[MapRef],
    data: Dict[str, Any],
) -> Tuple[Optional[str], Optional[str], AssurancePolicy]:
    resolved_output_path = persist_output_file(
        input_path=input_path,
        output_arg=output_arg,
        in_place=in_place,
        output_tag="redacted",
    )

    assurance_policy = assurance_policy_for_run(input_extension=input_extension)
    pipeline = RedactionFilePipeline(policy=assurance_policy)
    pipeline_result = pipeline.run(
        source=to_pipeline_input_source(input_source),
        anonymized_content=anonymized_content,
        mapping_entries=entries,
        resolved_output_path=resolved_output_path,
        map_ref=map_ref,
    )

    output_path = pipeline_result.output_path
    sidecar_path = pipeline_result.sidecar_path

    if resolved_output_path is not None:
        data["applyReport"] = serialize_apply_report(pipeline_result.apply_report)
        data["verificationReport"] = serialize_verification_report(pipeline_result.verification_report)
        data["assurancePolicy"] = serialize_assurance_policy(assurance_policy)

    if output_path:
        data["outputPath"] = output_path
        if map_ref and sidecar_path:
            map_ref_data = data.get("mapRef")
            if isinstance(map_ref_data, dict):
                map_ref_data["sidecarPath"] = sidecar_path

    return output_path, sidecar_path, assurance_policy
