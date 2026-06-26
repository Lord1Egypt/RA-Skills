#!/usr/bin/env python3
"""Minimal vendored PDF text extractor for simple text-stream PDFs."""

from __future__ import annotations

import re
import zlib
from typing import Any

STREAM_PATTERN = re.compile(br"stream\r?\n(.*?)\r?\nendstream", re.S)
BLOCK_PATTERN = re.compile(br"BT(.*?)(?:\r?\nET\b)", re.S)
TD_PATTERN = re.compile(br"(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+Td")
TEXT_PATTERN = re.compile(br"\(((?:\\.|[^\\()])*)\)\s*Tj")


def _decode_stream(chunk: bytes) -> bytes | None:
    candidates = (
        chunk.rstrip(b"\r\n"),
        chunk.rstrip(b"\r\n\x00"),
    )
    for candidate in candidates:
        for decoder in (lambda value: zlib.decompress(value), lambda value: zlib.decompress(value, -15)):
            try:
                return decoder(candidate)
            except Exception:
                continue
    return None


def _unescape_pdf_text(value: bytes) -> str:
    output: list[str] = []
    index = 0
    while index < len(value):
        current = value[index]
        if current == 92 and index + 1 < len(value):
            index += 1
            escaped = value[index]
            mapping = {
                110: "\n",
                114: "\r",
                116: "\t",
                98: "\b",
                102: "\f",
                40: "(",
                41: ")",
                92: "\\",
            }
            output.append(mapping.get(escaped, chr(escaped)))
        else:
            output.append(chr(current))
        index += 1
    return "".join(output)


def extract_text_blocks(pdf_bytes: bytes) -> list[dict[str, Any]]:
    """Return ordered text blocks with rough coordinates.

    This parser is intentionally small and only supports the subset of PDFs
    used by the official NBA injury report where the page text is stored in
    Flate-compressed content streams with `Td` + `Tj` operators.
    """

    blocks: list[dict[str, Any]] = []
    for page_index, stream_match in enumerate(STREAM_PATTERN.finditer(pdf_bytes)):
        decoded = _decode_stream(stream_match.group(1))
        if not decoded or b"BT" not in decoded or b"Tj" not in decoded:
            continue
        for match in BLOCK_PATTERN.finditer(decoded):
            body = match.group(1)
            coords = TD_PATTERN.search(body)
            if not coords:
                continue
            text_parts = [_unescape_pdf_text(value).strip() for value in TEXT_PATTERN.findall(body)]
            text = " ".join(part for part in text_parts if part)
            if not text:
                continue
            blocks.append(
                {
                    "page": page_index,
                    "x": float(coords.group(1)),
                    "y": float(coords.group(2)),
                    "text": text,
                }
            )
    blocks.sort(key=lambda item: (item["page"], item["y"], item["x"]))
    return blocks
