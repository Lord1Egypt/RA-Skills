#!/usr/bin/env python3
"""Deterministic shell metadata helpers for kai-report-creator.

These strings should be assembled from render metadata, not improvised in prose.
The visible footer and hidden watermark intentionally carry only:

    kai-report-creator v<version> <theme>
"""

from __future__ import annotations

import html


def normalize_version(version: str) -> str:
    version = version.strip()
    if not version:
        raise ValueError("version must be non-empty")
    return version if version.startswith("v") else f"v{version}"


def footer_watermark_text(version: str, theme: str) -> str:
    theme = theme.strip()
    if not theme:
        raise ValueError("theme must be non-empty")
    return f"kai-report-creator {normalize_version(version)} {theme}"


def footer_watermark_html(version: str, theme: str) -> str:
    text = footer_watermark_text(version, theme)
    escaped = html.escape(text, quote=True)
    return (
        f'<div class="report-footer">{escaped}</div>\n'
        f'<div style="display:none;visibility:hidden;opacity:0;font-size:0;'
        f'line-height:0;height:0;overflow:hidden;" aria-hidden="true" '
        f'data-watermark="{escaped}">\n'
        f'{escaped}\n'
        f"</div>"
    )
