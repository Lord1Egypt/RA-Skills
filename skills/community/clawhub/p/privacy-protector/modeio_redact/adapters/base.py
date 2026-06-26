#!/usr/bin/env python3
"""Base adapter protocol for file-type specific handling."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Protocol

from modeio_redact.core.models import ApplyReport, ExtractionBundle, InputSource, RedactionPlan, VerificationReport


class FileAdapter(Protocol):
    """Per-file-type adapter lifecycle for extract/apply/verify."""

    key: str

    def extract(self, source: InputSource) -> ExtractionBundle:
        """Build canonical text view for provider/planning stages."""

    def apply(
        self,
        source: InputSource,
        output_path: Path,
        anonymized_content: str,
        plan: RedactionPlan,
        map_id: Optional[str] = None,
    ) -> ApplyReport:
        """Apply redaction result to target file path."""

    def verify(self, source: InputSource, output_path: Path, plan: RedactionPlan) -> VerificationReport:
        """Perform post-redaction verification for target output."""
