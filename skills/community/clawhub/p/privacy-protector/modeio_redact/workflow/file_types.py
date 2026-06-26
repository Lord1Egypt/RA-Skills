#!/usr/bin/env python3
"""
Central file-type registry for privacy-protector file workflows.

Adding support for a new text-like file type should only require one new
FileTypePolicy entry.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

MAP_MARKER_STYLE_NONE = "none"
MAP_MARKER_STYLE_HASH = "hash"
MAP_MARKER_STYLE_HTML_COMMENT = "html_comment"

HANDLER_TEXT = "text"
HANDLER_DOCX = "docx"
HANDLER_PDF = "pdf"

ALL_LEVELS: Tuple[str, ...] = ("lite", "dynamic", "strict", "crossborder")


@dataclass(frozen=True)
class FileTypePolicy:
    extension: str
    marker_style: str = MAP_MARKER_STYLE_NONE
    handler_key: str = HANDLER_TEXT
    supports_deanonymize: bool = True
    supported_levels: Tuple[str, ...] = ALL_LEVELS


_FILE_TYPE_POLICIES: Tuple[FileTypePolicy, ...] = (
    FileTypePolicy(extension=".txt", marker_style=MAP_MARKER_STYLE_HASH),
    FileTypePolicy(extension=".md", marker_style=MAP_MARKER_STYLE_HTML_COMMENT),
    FileTypePolicy(extension=".markdown", marker_style=MAP_MARKER_STYLE_HTML_COMMENT),
    FileTypePolicy(extension=".csv"),
    FileTypePolicy(extension=".tsv"),
    FileTypePolicy(extension=".json"),
    FileTypePolicy(extension=".jsonl"),
    FileTypePolicy(extension=".yaml"),
    FileTypePolicy(extension=".yml"),
    FileTypePolicy(extension=".xml"),
    FileTypePolicy(extension=".html"),
    FileTypePolicy(extension=".htm"),
    FileTypePolicy(extension=".rst"),
    FileTypePolicy(extension=".log"),
    FileTypePolicy(extension=".docx", handler_key=HANDLER_DOCX),
    FileTypePolicy(
        extension=".pdf",
        handler_key=HANDLER_PDF,
        supports_deanonymize=False,
        supported_levels=ALL_LEVELS,
    ),
)


def _build_extension_map() -> Dict[str, FileTypePolicy]:
    mapping: Dict[str, FileTypePolicy] = {}
    for policy in _FILE_TYPE_POLICIES:
        normalized = normalize_extension(policy.extension)
        if not normalized.startswith("."):
            raise ValueError(f"File extension must start with '.': {policy.extension}")
        if normalized in mapping:
            raise ValueError(f"Duplicate file extension policy: {normalized}")
        mapping[normalized] = FileTypePolicy(
            extension=normalized,
            marker_style=policy.marker_style,
            handler_key=policy.handler_key,
            supports_deanonymize=policy.supports_deanonymize,
            supported_levels=tuple(policy.supported_levels),
        )
    return mapping


def normalize_extension(extension: str) -> str:
    return (extension or "").strip().lower()


_EXTENSION_MAP = _build_extension_map()

SUPPORTED_FILE_EXTENSIONS: Tuple[str, ...] = tuple(_EXTENSION_MAP.keys())


def supported_extensions_for_display(separator: str = ", ") -> str:
    return separator.join(SUPPORTED_FILE_EXTENSIONS)


def is_supported_extension(extension: str) -> bool:
    return normalize_extension(extension) in _EXTENSION_MAP


def policy_for_extension(extension: str) -> Optional[FileTypePolicy]:
    return _EXTENSION_MAP.get(normalize_extension(extension))


def handler_key_for_extension(extension: str) -> str:
    policy = policy_for_extension(extension)
    if policy is None:
        return HANDLER_TEXT
    return policy.handler_key


def supports_deanonymize_for_extension(extension: str) -> bool:
    policy = policy_for_extension(extension)
    if policy is None:
        return False
    return policy.supports_deanonymize


def supported_levels_for_extension(extension: str) -> Tuple[str, ...]:
    policy = policy_for_extension(extension)
    if policy is None:
        return tuple()
    return policy.supported_levels


def is_level_supported_for_extension(extension: str, level: str) -> bool:
    supported_levels = supported_levels_for_extension(extension)
    if not supported_levels:
        return False
    return (level or "").strip().lower() in supported_levels


def deanonymize_supported_extensions() -> Tuple[str, ...]:
    return tuple(
        policy.extension
        for policy in _EXTENSION_MAP.values()
        if policy.supports_deanonymize
    )


def deanonymize_supported_extensions_for_display(separator: str = ", ") -> str:
    return separator.join(deanonymize_supported_extensions())


def marker_style_for_extension(extension: str) -> str:
    policy = policy_for_extension(extension)
    if policy is None:
        return MAP_MARKER_STYLE_NONE
    return policy.marker_style
