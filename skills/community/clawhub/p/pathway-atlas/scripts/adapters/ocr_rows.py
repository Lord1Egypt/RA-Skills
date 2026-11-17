"""Normalize strict host-produced OCR row JSON without performing OCR."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
from types import MappingProxyType
from typing import Any

from . import (
    CellStatus,
    ColumnMapping,
    ExtractedCoverage,
    ExtractedRow,
    ExtractedTable,
    StructuredValidationError,
    _freeze_json,
    coerce_column_mapping,
    derive_coverage,
    read_stable_local_file,
    reject_duplicate_rows,
    validate_monotonicity,
    validate_public_locator,
)


class OcrValidationError(StructuredValidationError):
    """Raised when OCR input is ambiguous, unsafe, or internally inconsistent."""


_SAFE_ID = re.compile(r"^[A-Za-z][A-Za-z0-9._-]{0,63}$")
_MASKED = re.compile(
    r"^(?:[*—–-]+|\d+(?:\.\d+)?\s*分?\s*(?:以上|及以上|以下|及以下)|前\s*\d+(?:\.\d+)?\s*名?|由学校逐一告知)$"
)
_ROOT_KEYS = {
    "schema_version",
    "document_id",
    "total_pages",
    "covered_pages",
    "images",
    "rows",
    "anchors",
}
_IMAGE_KEYS = {"page_number", "image_id"}
_ROW_KEYS = {"page_number", "image_id", "bbox", "cropped", "cells"}
_CELL_KEYS = {"label", "bbox", "raw_text", "normalized_value", "confidence", "verified"}
_ANCHOR_KEYS = {"row_index", "label", "bbox", "raw_text", "normalized_value"}


@dataclass(frozen=True)
class OcrExtractedRow(ExtractedRow):
    cell_locations: Mapping[str, str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        super().__post_init__()
        if not isinstance(self.cell_locations, Mapping):
            raise TypeError("cell_locations must be a mapping")
        snapshot: dict[str, str] = {}
        for key, location in self.cell_locations.items():
            if key not in self.values or key in snapshot:
                raise ValueError("cell_locations must match extracted fields")
            snapshot[key] = validate_public_locator(location)
        if set(snapshot) != set(self.values):
            raise ValueError("cell_locations must match extracted fields")
        object.__setattr__(self, "cell_locations", MappingProxyType(snapshot))


@dataclass(frozen=True)
class OcrExtractedTable(ExtractedTable):
    mapping_snapshot: Mapping[str, Any] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        super().__post_init__()
        frozen = _freeze_json(self.mapping_snapshot)
        if not isinstance(frozen, Mapping):
            raise TypeError("mapping_snapshot must be a mapping")
        object.__setattr__(self, "mapping_snapshot", frozen)


def _require_keys(value: object, expected: set[str], name: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != expected:
        raise OcrValidationError(f"{name} has missing or unknown keys")
    return value


def _integer(value: object, name: str, *, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise OcrValidationError(f"{name} must be a mathematical integer")
    if isinstance(value, float) and (not math.isfinite(value) or not value.is_integer()):
        raise OcrValidationError(f"{name} must be a mathematical integer")
    result = int(value)
    if result < minimum:
        raise OcrValidationError(f"{name} is outside its allowed range")
    return result


def _finite_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise OcrValidationError(f"{name} must be a finite number")
    result = float(value)
    if not math.isfinite(result):
        raise OcrValidationError(f"{name} must be a finite number")
    return result


def _bbox(value: object, name: str) -> tuple[int | float, int | float, int | float, int | float]:
    if not isinstance(value, list) or len(value) != 4:
        raise OcrValidationError(f"{name} must contain four coordinates")
    coordinates: list[int | float] = []
    for item in value:
        number = _finite_number(item, name)
        coordinates.append(int(number) if number.is_integer() else number)
    left, top, right, bottom = coordinates
    if left < 0 or top < 0 or right <= left or bottom <= top:
        raise OcrValidationError(f"{name} is not a positive rectangle")
    return left, top, right, bottom


def _location(page_number: int, image_id: str, bbox: Sequence[int | float]) -> str:
    coordinates = ",".join(str(value) for value in bbox)
    return f"page[{page_number}]/image[{image_id}]/bbox[{coordinates}]"


def _safe_id(value: object, name: str) -> str:
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value) or value in {".", ".."}:
        raise OcrValidationError(f"{name} must be a safe logical identifier")
    return value


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise OcrValidationError("OCR JSON contains duplicate keys")
        result[key] = value
    return result


def _reject_constant(_: str) -> None:
    raise OcrValidationError("OCR JSON contains a non-finite number")


def _load_json(source: bytes) -> dict[str, Any]:
    try:
        text = source.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except OcrValidationError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise OcrValidationError("OCR input must be strict UTF-8 JSON") from None
    return _require_keys(value, _ROOT_KEYS, "OCR document")


def _score_scale(value: object) -> tuple[int, int]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)) or len(value) != 2:
        raise TypeError("score_scale must be an ordered pair")
    try:
        lower = _integer(value[0], "score_scale lower", minimum=0)
        upper = _integer(value[1], "score_scale upper", minimum=0)
    except OcrValidationError:
        raise TypeError("score_scale bounds must be mathematical integers") from None
    if lower > upper:
        raise ValueError("score_scale bounds are out of order")
    return lower, upper


def _mapping_snapshot(mapping: ColumnMapping) -> dict[str, Any]:
    return {
        "columns": {key: list(aliases) for key, aliases in mapping.items()},
        "roles": dict(mapping.roles),
        "score_scale": list(mapping.score_scale) if mapping.score_scale is not None else None,
    }


def _derive_complete_role_coverage(
    rows: list[ExtractedRow], mapping: ColumnMapping
) -> tuple[ExtractedCoverage, list[str]]:
    bounds: dict[str, int | None] = {
        "lower_score": None,
        "upper_score": None,
        "lower_rank": None,
        "upper_rank": None,
    }
    warnings: list[str] = []
    for role in ("score", "rank"):
        fields = [field for field, declared_role in mapping.roles.items() if declared_role == role]
        if not fields:
            continue
        projected = [
            ExtractedRow(
                {field: row.values[field] for field in fields},
                {field: row.cell_status[field] for field in fields},
                row.location,
                row.confidence,
                row.warnings,
            )
            for row in rows
        ]
        role_mapping = ColumnMapping(
            {field: mapping[field] for field in fields},
            roles={field: role for field in fields},
            score_scale=mapping.score_scale,
        )
        role_coverage, role_warnings = derive_coverage(projected, role_mapping)
        boundary_exact = all(
            row.cell_status[field] is CellStatus.EXACT
            for row in (rows[0], rows[-1])
            for field in fields
        )
        if boundary_exact:
            bounds[f"lower_{role}"] = getattr(role_coverage, f"lower_{role}")
            bounds[f"upper_{role}"] = getattr(role_coverage, f"upper_{role}")
        elif f"coverage-{role}-unavailable" not in role_warnings:
            role_warnings.append(f"coverage-{role}-unavailable")
        for warning in role_warnings:
            if warning not in warnings:
                warnings.append(warning)
    return ExtractedCoverage(**bounds), warnings


def _validate_anchors(payload: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    anchors = payload["anchors"]
    if not isinstance(anchors, list) or len(anchors) < 2:
        raise OcrValidationError("at least two verification anchors are required")
    references: set[tuple[int, str]] = set()
    row_positions: set[int] = set()
    spatial_positions: list[
        tuple[str, tuple[int | float, int | float, int | float, int | float]]
    ] = []
    for raw_anchor in anchors:
        anchor = _require_keys(raw_anchor, _ANCHOR_KEYS, "verification anchor")
        row_index = _integer(anchor["row_index"], "anchor row_index")
        if row_index > len(rows):
            raise OcrValidationError("verification anchor references a missing row")
        label = anchor["label"]
        if not isinstance(label, str) or not label or label != label.strip():
            raise OcrValidationError("anchor label must be a nonempty exact string")
        reference = (row_index, label)
        if reference in references:
            raise OcrValidationError("verification anchors must reference distinct cells")
        references.add(reference)
        row_positions.add(row_index)
        matches = [cell for cell in rows[row_index - 1]["cells"] if cell["label"] == label]
        if len(matches) != 1:
            raise OcrValidationError("verification anchor references an ambiguous cell")
        cell = matches[0]
        anchor_bbox = _bbox(anchor["bbox"], "anchor bbox")
        if (
            anchor_bbox != cell["bbox"]
            or anchor["raw_text"] != cell["raw_text"]
            or type(anchor["normalized_value"]) is not type(cell["normalized_value"])
            or anchor["normalized_value"] != cell["normalized_value"]
        ):
            raise OcrValidationError("verification anchor does not reproduce its cell")
        image_key = f"{rows[row_index - 1]['page_number']}:{rows[row_index - 1]['image_id']}"
        for prior_image, prior_bbox in spatial_positions:
            if prior_image != image_key:
                continue
            left = max(anchor_bbox[0], prior_bbox[0])
            top = max(anchor_bbox[1], prior_bbox[1])
            right = min(anchor_bbox[2], prior_bbox[2])
            bottom = min(anchor_bbox[3], prior_bbox[3])
            intersection = max(0, right - left) * max(0, bottom - top)
            anchor_area = (anchor_bbox[2] - anchor_bbox[0]) * (anchor_bbox[3] - anchor_bbox[1])
            prior_area = (prior_bbox[2] - prior_bbox[0]) * (prior_bbox[3] - prior_bbox[1])
            if intersection / min(anchor_area, prior_area) >= 0.9:
                raise OcrValidationError("verification anchors must be spatially distributed")
        spatial_positions.append((image_key, anchor_bbox))
    if len(row_positions) < 2:
        raise OcrValidationError("verification anchors must be spatially distributed")


def normalize_ocr_rows(
    path: str | Path,
    mapping: ColumnMapping | Mapping[str, object],
    *,
    score_scale: Sequence[object],
    min_exact_confidence: float,
) -> ExtractedTable:
    scale = _score_scale(score_scale)
    if isinstance(min_exact_confidence, bool) or not isinstance(min_exact_confidence, (int, float)):
        raise TypeError("min_exact_confidence must be a finite number")
    threshold = float(min_exact_confidence)
    if not math.isfinite(threshold) or not 0 <= threshold <= 1:
        raise ValueError("min_exact_confidence must be between zero and one")
    declared = coerce_column_mapping(mapping)
    if declared.score_scale is not None and declared.score_scale != scale:
        raise OcrValidationError("mapping score scale conflicts with the explicit score_scale")
    column_mapping = ColumnMapping(declared.columns, roles=declared.roles, score_scale=scale)
    payload = _load_json(read_stable_local_file(path, suffixes=(".json",)))
    if payload["schema_version"] != 1 or isinstance(payload["schema_version"], bool):
        raise OcrValidationError("unsupported OCR schema version")
    document_id = _safe_id(payload["document_id"], "document_id")
    total_pages = _integer(payload["total_pages"], "total_pages")
    if total_pages > 10_000:
        raise OcrValidationError("total_pages exceeds the supported limit")
    if not isinstance(payload["covered_pages"], list) or not payload["covered_pages"]:
        raise OcrValidationError("covered_pages must be a nonempty ordered list")
    covered_pages = tuple(_integer(item, "covered page") for item in payload["covered_pages"])
    if covered_pages != tuple(sorted(set(covered_pages))) or covered_pages[-1] > total_pages:
        raise OcrValidationError("covered_pages must be unique, ordered, and in range")
    partial = covered_pages != tuple(range(1, total_pages + 1))

    if not isinstance(payload["images"], list):
        raise OcrValidationError("images must be an ordered list")
    image_by_page: dict[int, str] = {}
    for raw_image in payload["images"]:
        image = _require_keys(raw_image, _IMAGE_KEYS, "image")
        page_number = _integer(image["page_number"], "image page_number")
        image_id = _safe_id(image["image_id"], "image_id")
        if page_number in image_by_page or page_number not in covered_pages or image_id in image_by_page.values():
            raise OcrValidationError("image identities must map one-to-one to covered pages")
        image_by_page[page_number] = image_id
    if set(image_by_page) != set(covered_pages):
        raise OcrValidationError("every covered page must declare one image")

    if not isinstance(payload["rows"], list) or not payload["rows"]:
        raise OcrValidationError("rows must be a nonempty ordered list")
    parsed_rows: list[dict[str, Any]] = []
    for raw_row in payload["rows"]:
        row = _require_keys(raw_row, _ROW_KEYS, "OCR row")
        page_number = _integer(row["page_number"], "row page_number")
        image_id = _safe_id(row["image_id"], "row image_id")
        if image_by_page.get(page_number) != image_id:
            raise OcrValidationError("row page and image identity are inconsistent")
        row_bbox = _bbox(row["bbox"], "row bbox")
        if not isinstance(row["cropped"], bool):
            raise OcrValidationError("cropped must be boolean")
        if not isinstance(row["cells"], list) or not row["cells"]:
            raise OcrValidationError("cells must be a nonempty ordered list")
        cells: list[dict[str, Any]] = []
        labels: set[str] = set()
        for raw_cell in row["cells"]:
            cell = _require_keys(raw_cell, _CELL_KEYS, "OCR cell")
            label = cell["label"]
            raw_text = cell["raw_text"]
            if not isinstance(label, str) or not label or label != label.strip() or label in labels:
                raise OcrValidationError("cell labels must be unique nonempty exact strings")
            if not isinstance(raw_text, str):
                raise OcrValidationError("cell raw_text must be a string")
            labels.add(label)
            cell_bbox = _bbox(cell["bbox"], "cell bbox")
            if not (
                row_bbox[0] <= cell_bbox[0] < cell_bbox[2] <= row_bbox[2]
                and row_bbox[1] <= cell_bbox[1] < cell_bbox[3] <= row_bbox[3]
            ):
                raise OcrValidationError("cell bbox must be inside its row bbox")
            confidence = _finite_number(cell["confidence"], "cell confidence")
            if not 0 <= confidence <= 1:
                raise OcrValidationError("cell confidence must be between zero and one")
            if not isinstance(cell["verified"], bool):
                raise OcrValidationError("cell verified must be boolean")
            normalized = cell["normalized_value"]
            try:
                _freeze_json(normalized)
            except (TypeError, ValueError):
                raise OcrValidationError("normalized_value must be finite JSON data") from None
            cells.append(
                {
                    **cell,
                    "bbox": cell_bbox,
                    "confidence": confidence,
                }
            )
        parsed_rows.append({**row, "page_number": page_number, "bbox": row_bbox, "cells": cells})

    _validate_anchors(payload, parsed_rows)
    extracted: list[ExtractedRow] = []
    for row in parsed_rows:
        cells_by_label = {cell["label"]: cell for cell in row["cells"]}
        values: dict[str, Any] = {}
        statuses: dict[str, CellStatus] = {}
        cell_locations: dict[str, str] = {}
        warnings: list[str] = []
        for canonical, aliases in column_mapping.items():
            matches = [cells_by_label[alias] for alias in aliases if alias in cells_by_label]
            if len(matches) != 1:
                raise OcrValidationError("mapped source label is missing or ambiguous")
            cell = matches[0]
            raw_text = cell["raw_text"].strip()
            value = cell["normalized_value"]
            if _MASKED.fullmatch(raw_text):
                value = None
                status = CellStatus.MASKED
                warnings.append(f"masked-cell:{canonical}")
            elif value is None:
                status = CellStatus.EMPTY
                warnings.append(f"empty-cell:{canonical}")
            else:
                role = column_mapping.roles.get(canonical)
                if role == "rank":
                    value = _integer(value, canonical)
                elif role == "score":
                    numeric = _finite_number(value, canonical)
                    value = int(numeric) if numeric.is_integer() else numeric
                    if not scale[0] <= value <= scale[1]:
                        raise OcrValidationError("score lies outside the explicit score scale")
                status = CellStatus.EXACT
                if cell["confidence"] < threshold:
                    status = CellStatus.UNCERTAIN
                    warnings.append(f"low-confidence-cell:{canonical}")
                if not cell["verified"]:
                    status = CellStatus.UNCERTAIN
                    warnings.append(f"unverified-cell:{canonical}")
                if row["cropped"] or partial:
                    status = CellStatus.UNCERTAIN
            values[canonical] = value
            statuses[canonical] = status
            cell_locations[canonical] = _location(row["page_number"], row["image_id"], cell["bbox"])
        if row["cropped"]:
            warnings.append("cropped-row")
        if partial:
            warnings.append("partial-page-coverage")
        extracted.append(
            OcrExtractedRow(
                values,
                statuses,
                _location(row["page_number"], row["image_id"], row["bbox"]),
                min(cell["confidence"] for cell in row["cells"]),
                warnings,
                cell_locations,
            )
        )
    try:
        reject_duplicate_rows(extracted)
        validate_monotonicity(extracted, column_mapping)
    except StructuredValidationError:
        raise OcrValidationError("OCR rows violate duplicate or monotonicity rules") from None
    coverage, coverage_warnings = _derive_complete_role_coverage(extracted, column_mapping)
    if partial:
        coverage = ExtractedCoverage()
        coverage_warnings = [
            warning
            for warning in ("coverage-score-unavailable", "coverage-rank-unavailable")
            if warning.split("-")[1] in column_mapping.roles.values()
        ]
    table_warnings: list[str] = []
    if any(CellStatus.MASKED in row.cell_status.values() for row in extracted):
        table_warnings.append("masked-cells-present")
    if any(CellStatus.UNCERTAIN in row.cell_status.values() for row in extracted):
        table_warnings.append("uncertain-cells-present")
    if partial:
        table_warnings.append("partial-page-coverage")
    table_warnings.extend(coverage_warnings)
    return OcrExtractedTable(
        document_id,
        None,
        None,
        extracted,
        coverage,
        table_warnings,
        "host-ocr-rows",
        _mapping_snapshot(column_mapping),
    )


__all__ = [
    "OcrExtractedRow",
    "OcrExtractedTable",
    "OcrValidationError",
    "normalize_ocr_rows",
]
