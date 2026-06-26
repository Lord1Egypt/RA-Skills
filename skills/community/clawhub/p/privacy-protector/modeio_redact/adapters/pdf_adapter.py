#!/usr/bin/env python3
"""PDF adapter for pipeline extraction/apply/verify."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from modeio_redact.adapters.coverage import summarize_redaction_removal_coverage
from modeio_redact.assurance.verifier import verify_content_against_plan
from modeio_redact.core.models import ApplyReport, ExtractionBundle, InputSource, RedactionPlan, VerificationReport
from modeio_redact.workflow.file_handlers import (
    read_input_file,
    validate_non_text_output_extension,
    write_non_text_anonymized_file,
)


class PdfAdapter:
    """Adapter for text-layer PDF anonymization flows."""

    key = "pdf"

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

        if not source.input_path or source.extension != ".pdf":
            raise ValueError("PDF apply requires .pdf file input path.")

        validate_non_text_output_extension(source.extension, output_path)
        write_non_text_anonymized_file(
            input_path=Path(source.input_path).expanduser(),
            output_path=output_path,
            extension=source.extension,
            mapping_entries=plan.mapping_entries,
        )
        output_text = read_input_file(output_path, ".pdf")
        return summarize_redaction_removal_coverage(output_text, plan)

    def verify(self, source: InputSource, output_path: Path, plan: RedactionPlan) -> VerificationReport:
        del source
        output_text = read_input_file(output_path, ".pdf")
        return verify_content_against_plan(output_text, plan=plan, part_id="pdf-output")
