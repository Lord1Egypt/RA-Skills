#!/usr/bin/env python3
"""Text-file adapter for pipeline extraction/apply/verify."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from modeio_redact.adapters.coverage import summarize_apply_coverage
from modeio_redact.assurance.verifier import verify_content_against_plan
from modeio_redact.core.models import ApplyReport, ExtractionBundle, InputSource, RedactionPlan, VerificationReport
from modeio_redact.workflow.file_workflow import embed_map_marker, write_output_file


class TextAdapter:
    """Adapter for plain text-like formats handled as UTF-8 text."""

    key = "text"

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
        output_content = anonymized_content
        if map_id:
            output_content = embed_map_marker(
                content=output_content,
                map_id=map_id,
                suffix=output_path.suffix.lower(),
            )
        write_output_file(output_path, output_content)
        return summarize_apply_coverage(output_content, plan)

    def verify(self, source: InputSource, output_path: Path, plan: RedactionPlan) -> VerificationReport:
        output_text = output_path.read_text(encoding="utf-8")
        return verify_content_against_plan(output_text, plan=plan, part_id="text-output")
