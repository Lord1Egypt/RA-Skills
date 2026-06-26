#!/usr/bin/env python3
"""DOCX adapter for pipeline extraction/apply/verify."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from modeio_redact.adapters.coverage import summarize_apply_coverage
from modeio_redact.assurance.verifier import verify_content_against_plan
from modeio_redact.core.models import ApplyReport, ExtractionBundle, InputSource, RedactionPlan, VerificationReport
from modeio_redact.workflow.file_handlers import (
    read_input_file,
    validate_non_text_output_extension,
    write_non_text_anonymized_file,
)


class DocxAdapter:
    """Adapter for .docx extraction and replacement workflows."""

    key = "docx"

    def extract(self, source: InputSource) -> ExtractionBundle:
        return ExtractionBundle(adapter_key=self.key, canonical_text=source.content)

    def apply(
        self,
        source: InputSource,
        output_path: Path,
        anonymized_content: str,
        plan: RedactionPlan,
        map_id: Optional[str] = None,
    ) -> ApplyReport:
        del anonymized_content
        del map_id

        if not source.input_path or source.extension != ".docx":
            raise ValueError("DOCX apply requires .docx file input path.")

        validate_non_text_output_extension(source.extension, output_path)
        write_non_text_anonymized_file(
            input_path=Path(source.input_path).expanduser(),
            output_path=output_path,
            extension=source.extension,
            mapping_entries=plan.mapping_entries,
        )
        output_text = read_input_file(output_path, ".docx")
        return summarize_apply_coverage(output_text, plan)

    def verify(self, source: InputSource, output_path: Path, plan: RedactionPlan) -> VerificationReport:
        del source
        output_text = read_input_file(output_path, ".docx")
        return verify_content_against_plan(output_text, plan=plan, part_id="docx-output")
