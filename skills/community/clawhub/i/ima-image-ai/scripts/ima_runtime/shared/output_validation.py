from __future__ import annotations

import re
import struct
from typing import Any

import requests


class OutputValidationError(RuntimeError):
    pass


ASPECT_RATIO_TOLERANCE = 0.05


def _parse_size_dims(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    normalized = value.strip().upper()
    match = re.search(r"(\d{2,5})\s*[xX×]\s*(\d{2,5})", normalized)
    if match:
        return int(match.group(1)), int(match.group(2))
    square = re.fullmatch(r"(\d{2,5})\s*PX", normalized)
    if square:
        size = int(square.group(1))
        return size, size
    return None


def _parse_aspect_ratio(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    match = re.fullmatch(r"\s*(\d{1,3})\s*:\s*(\d{1,3})\s*", value)
    if not match:
        return None
    width = int(match.group(1))
    height = int(match.group(2))
    if width <= 0 or height <= 0:
        return None
    return width, height


def _parse_png_dims(data: bytes) -> tuple[int, int] | None:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def _parse_jpeg_dims(data: bytes) -> tuple[int, int] | None:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None

    i = 2
    sof_markers = {
        0xC0,
        0xC1,
        0xC2,
        0xC3,
        0xC5,
        0xC6,
        0xC7,
        0xC9,
        0xCA,
        0xCB,
        0xCD,
        0xCE,
        0xCF,
    }
    while i + 9 <= len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        while i < len(data) and data[i] == 0xFF:
            i += 1
        if i >= len(data):
            break
        marker = data[i]
        i += 1
        if marker in (0xD8, 0xD9):
            continue
        if i + 2 > len(data):
            break
        segment_length = struct.unpack(">H", data[i : i + 2])[0]
        if segment_length < 2 or i + segment_length > len(data):
            break
        if marker in sof_markers:
            height, width = struct.unpack(">HH", data[i + 3 : i + 7])
            return width, height
        i += segment_length
    return None


def _parse_webp_dims(data: bytes) -> tuple[int, int] | None:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    return None


def fetch_image_dimensions(url: str, timeout: int = 30) -> tuple[int, int]:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    data = response.content

    for parser in (_parse_png_dims, _parse_jpeg_dims, _parse_webp_dims):
        dims = parser(data)
        if dims is not None:
            return dims
    raise RuntimeError("Unable to determine output image dimensions for validation.")


def validate_output_constraints(
    url: str,
    raw_params: dict[str, Any],
    effective_params: dict[str, Any],
) -> None:
    expected_aspect = _parse_aspect_ratio(raw_params.get("aspect_ratio"))
    explicit_size = _parse_size_dims(raw_params.get("size"))
    effective_size = _parse_size_dims(effective_params.get("size"))
    expected_size = explicit_size or effective_size

    if expected_aspect is None and expected_size is None:
        return

    width, height = fetch_image_dimensions(url)

    if expected_aspect is not None:
        expected_ratio = expected_aspect[0] / expected_aspect[1]
        actual_ratio = width / height
        relative_error = abs(actual_ratio - expected_ratio) / expected_ratio
        if relative_error > ASPECT_RATIO_TOLERANCE:
            raise OutputValidationError(
                "Output aspect ratio does not match requested "
                f"aspect_ratio={raw_params['aspect_ratio']}: got {width}x{height}."
            )

    if expected_size is not None and (width, height) != expected_size:
        raise OutputValidationError(
            f"Output dimensions do not match requested size: expected {expected_size[0]}x{expected_size[1]}, got {width}x{height}."
        )
