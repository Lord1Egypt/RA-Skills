#!/usr/bin/env python3
"""Adapter registry for extension/handler dispatch."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from modeio_redact.adapters.base import FileAdapter
from modeio_redact.adapters.docx_adapter import DocxAdapter
from modeio_redact.adapters.pdf_adapter import PdfAdapter
from modeio_redact.adapters.text_adapter import TextAdapter
from modeio_redact.core.models import InputSource
from modeio_redact.workflow.file_types import HANDLER_DOCX, HANDLER_PDF, HANDLER_TEXT


@dataclass
class AdapterRegistry:
    """Lookup registry for file adapters by handler key."""

    adapters_by_key: Dict[str, FileAdapter]

    def adapter_for_source(self, source: InputSource) -> FileAdapter:
        handler_key = (source.handler_key or HANDLER_TEXT).strip().lower()
        adapter = self.adapters_by_key.get(handler_key)
        if adapter is None:
            adapter = self.adapters_by_key[HANDLER_TEXT]
        return adapter


def default_adapter_registry() -> AdapterRegistry:
    return AdapterRegistry(
        adapters_by_key={
            HANDLER_TEXT: TextAdapter(),
            HANDLER_DOCX: DocxAdapter(),
            HANDLER_PDF: PdfAdapter(),
        }
    )
