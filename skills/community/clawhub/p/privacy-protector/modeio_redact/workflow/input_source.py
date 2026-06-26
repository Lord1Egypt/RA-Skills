#!/usr/bin/env python3
"""Shared --input resolver for privacy-protector modules."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

from modeio_redact.workflow.file_handlers import read_input_file
from modeio_redact.workflow.file_types import (
    SUPPORTED_FILE_EXTENSIONS,
    handler_key_for_extension,
    is_supported_extension,
    supported_extensions_for_display,
)


@dataclass(frozen=True)
class InputSourceContext:
    content: str
    input_type: str
    input_path: Optional[str]
    extension: Optional[str]
    handler_key: Optional[str]


def resolve_input_source(input_value: str) -> Tuple[str, str]:
    """Resolve --input as literal text or supported file path."""
    source = resolve_input_source_context(input_value)
    return source.content, source.input_type


def resolve_input_source_details(input_value: str) -> Tuple[str, str, Optional[str]]:
    """Resolve --input and preserve source path when input is a file."""
    source = resolve_input_source_context(input_value)
    return source.content, source.input_type, source.input_path


def resolve_input_source_context(input_value: str) -> InputSourceContext:
    """Resolve --input into normalized content plus file metadata context."""
    raw_value = (input_value or "").strip()
    if not raw_value:
        raise ValueError("--input must not be empty.")

    expanded_path = os.path.expandvars(os.path.expanduser(raw_value))
    if os.path.isfile(expanded_path):
        extension = os.path.splitext(expanded_path)[1].lower()
        if not is_supported_extension(extension):
            allowed = supported_extensions_for_display()
            raise ValueError(
                f"Unsupported file extension '{extension or '(none)'}'. "
                f"Supported file types: {allowed}."
            )

        content = read_input_file(Path(expanded_path), extension)
        if not content.strip():
            raise ValueError("Input file must not be empty.")

        return InputSourceContext(
            content=content,
            input_type="file",
            input_path=expanded_path,
            extension=extension,
            handler_key=handler_key_for_extension(extension),
        )

    return InputSourceContext(
        content=raw_value,
        input_type="text",
        input_path=None,
        extension=None,
        handler_key=None,
    )
