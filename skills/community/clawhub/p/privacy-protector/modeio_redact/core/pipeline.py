#!/usr/bin/env python3
"""Shared extract/plan/apply/verify/finalize orchestration for file outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Sequence

from modeio_redact.adapters.registry import AdapterRegistry, default_adapter_registry
from modeio_redact.core.errors import ApplyError, VerificationError
from modeio_redact.core.models import (
    ApplyReport,
    InputSource,
    MapRef,
    MappingEntry,
    OutputPipelineResult,
    VerificationReport,
)
from modeio_redact.core.policy import AssurancePolicy
from modeio_redact.planning.plan_builder import build_redaction_plan
from modeio_redact.providers.local_regex_provider import LocalRegexProvider
from modeio_redact.providers.remote_api_provider import RemoteApiProvider
from modeio_redact.providers.base import ProviderResult
from modeio_redact.workflow.file_workflow import write_sidecar_map


def to_pipeline_input_source(input_source_context: Any) -> InputSource:
    """Convert existing workflow input context to shared pipeline input source."""
    return InputSource(
        content=getattr(input_source_context, "content", ""),
        input_type=getattr(input_source_context, "input_type", "text"),
        input_path=getattr(input_source_context, "input_path", None),
        extension=getattr(input_source_context, "extension", None),
        handler_key=getattr(input_source_context, "handler_key", None),
    )


class RedactionProviderPipeline:
    """Provider orchestrator for local regex and remote API modes."""

    def __init__(self, *, api_anonymize_callable):
        self._local_provider = LocalRegexProvider()
        self._remote_provider = RemoteApiProvider(api_anonymize_callable)

    def run(
        self,
        *,
        content: str,
        level: str,
        input_type: str,
        sender_code: Optional[str] = None,
        recipient_code: Optional[str] = None,
    ) -> ProviderResult:
        provider = self._local_provider if level == "lite" else self._remote_provider
        return provider.redact(
            content,
            level=level,
            input_type=input_type,
            sender_code=sender_code,
            recipient_code=recipient_code,
        )


class RedactionFilePipeline:
    """Orchestrates extract -> plan -> apply -> verify -> finalize for file outputs."""

    def __init__(
        self,
        *,
        policy: Optional[AssurancePolicy] = None,
        adapter_registry: Optional[AdapterRegistry] = None,
    ):
        self.policy = policy or AssurancePolicy.best_effort()
        self.adapter_registry = adapter_registry or default_adapter_registry()

    def run(
        self,
        *,
        source: InputSource,
        anonymized_content: str,
        mapping_entries: Sequence[MappingEntry],
        resolved_output_path: Optional[Path],
        map_ref: Optional[MapRef],
    ) -> OutputPipelineResult:
        adapter = self.adapter_registry.adapter_for_source(source)
        extraction = adapter.extract(source)
        plan = build_redaction_plan(
            canonical_text=extraction.canonical_text,
            mapping_entries=mapping_entries,
        )

        if self.policy.fail_on_coverage_mismatch and plan.mapping_entries and plan.expected_count == 0:
            raise ApplyError(
                "apply coverage mismatch: no canonical spans resolved from mapping entries"
            )

        if resolved_output_path is None:
            return OutputPipelineResult(
                output_path=None,
                sidecar_path=None,
                apply_report=ApplyReport(
                    expected_count=plan.expected_count,
                    found_count=0,
                    applied_count=0,
                    warnings=list(plan.warnings),
                ),
                verification_report=VerificationReport.skipped_report(),
            )

        if isinstance(map_ref, dict):
            map_ref = MapRef.from_dict(map_ref)

        map_id = None
        if map_ref:
            map_id = map_ref.map_id

        apply_report = adapter.apply(
            source=source,
            output_path=resolved_output_path,
            anonymized_content=anonymized_content,
            plan=plan,
            map_id=map_id,
        )

        if self.policy.fail_on_coverage_mismatch and apply_report.applied_count < apply_report.expected_count:
            raise ApplyError(
                "apply coverage mismatch: "
                f"expected={apply_report.expected_count}, applied={apply_report.applied_count}"
            )

        verification_report = VerificationReport.skipped_report()
        if self.policy.should_verify():
            verification_report = adapter.verify(
                source=source,
                output_path=resolved_output_path,
                plan=plan,
            )
            if self.policy.fail_on_residual_findings and not verification_report.passed:
                raise VerificationError(
                    "post-redaction residuals detected: "
                    f"residual_count={verification_report.residual_count}"
                )

        sidecar_path = None
        if map_ref:
            sidecar = write_sidecar_map(content_path=resolved_output_path, map_ref=map_ref)
            sidecar_path = str(sidecar)

        return OutputPipelineResult(
            output_path=str(resolved_output_path),
            sidecar_path=sidecar_path,
            apply_report=apply_report,
            verification_report=verification_report,
        )
