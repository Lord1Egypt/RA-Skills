from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import re
from typing import Any
from xml.etree import ElementTree as ET


URL_REF_RE = re.compile(r"url\(#([^)]+)\)")


@dataclass
class ExportIntegrityResult:
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True)
class ExportIntegrityFailure:
    requested_route: str | None
    attempted_route: str
    fallback_route: str | None
    terminal_reason: str
    errors: list[dict[str, Any]]

    def to_payload(self) -> dict[str, Any]:
        return {
            "kind": "export_integrity_failure",
            "requestedRoute": self.requested_route,
            "attemptedRoute": self.attempted_route,
            "fallbackRoute": self.fallback_route,
            "terminalReason": self.terminal_reason,
            "errors": self.errors,
        }


class ExportIntegrityError(RuntimeError):
    def __init__(self, failure: ExportIntegrityFailure):
        self.failure = failure
        super().__init__(json.dumps(failure.to_payload(), ensure_ascii=False))

    def to_payload(self) -> dict[str, Any]:
        return self.failure.to_payload()


def load_export_integrity_thresholds() -> dict[str, float]:
    default_thresholds = {
        "minLabelClearancePx": 4.0,
        "legendBottomMarginPx": 8.0,
        "legendContentGapPx": 8.0,
        "titleOverflowTolerancePx": 0.0,
        "cardTextInsetPx": 12.0,
    }
    path = Path(__file__).resolve().parent.parent / "evals" / "export-integrity-thresholds.json"
    if not path.exists():
        return default_thresholds
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {**default_thresholds, **payload}


def check_svg_definition_integrity(svg_text: str) -> ExportIntegrityResult:
    result = ExportIntegrityResult()
    refs = set(URL_REF_RE.findall(svg_text))
    if not refs:
        return result

    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError:
        result.errors.append({"kind": "svg_parse_error"})
        return result

    defined_ids = {node.attrib["id"] for node in root.iter() if "id" in node.attrib}
    for ref in sorted(refs - defined_ids):
        result.errors.append({"kind": "defs_reference_missing", "ref": ref})
    return result


def check_svg_geometry_integrity(svg_text: str) -> ExportIntegrityResult:
    result = ExportIntegrityResult()
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError:
        result.errors.append({"kind": "svg_parse_error"})
        return result

    width = _to_float(root.attrib.get("width", "0"))
    height = _to_float(root.attrib.get("height", "0"))
    max_x = 0.0
    max_y = 0.0

    for node in root.iter():
        tag = _local_name(node.tag)
        attrs = node.attrib
        if tag == "rect":
            max_x = max(max_x, _to_float(attrs.get("x")) + _to_float(attrs.get("width")))
            max_y = max(max_y, _to_float(attrs.get("y")) + _to_float(attrs.get("height")))
        elif tag == "line":
            max_x = max(max_x, _to_float(attrs.get("x1")), _to_float(attrs.get("x2")))
            max_y = max(max_y, _to_float(attrs.get("y1")), _to_float(attrs.get("y2")))
        elif tag == "circle":
            cx = _to_float(attrs.get("cx"))
            cy = _to_float(attrs.get("cy"))
            r = _to_float(attrs.get("r"))
            max_x = max(max_x, cx + r)
            max_y = max(max_y, cy + r)
        elif tag == "ellipse":
            cx = _to_float(attrs.get("cx"))
            cy = _to_float(attrs.get("cy"))
            rx = _to_float(attrs.get("rx"))
            ry = _to_float(attrs.get("ry"))
            max_x = max(max_x, cx + rx)
            max_y = max(max_y, cy + ry)
        elif tag in {"polygon", "polyline"}:
            xs, ys = _points_bounds(attrs.get("points", ""))
            max_x = max(max_x, xs)
            max_y = max(max_y, ys)

    if width and max_x > width:
        result.errors.append({"kind": "canvas_clipping", "axis": "x", "actual": max_x, "limit": width})
    if height and max_y > height:
        result.errors.append({"kind": "canvas_clipping", "axis": "y", "actual": max_y, "limit": height})
    return result


def check_svg_integrity(svg_text: str) -> ExportIntegrityResult:
    combined = ExportIntegrityResult()
    for partial in (
        check_svg_definition_integrity(svg_text),
        check_svg_geometry_integrity(svg_text),
    ):
        combined.errors.extend(partial.errors)
        combined.warnings.extend(partial.warnings)
    return combined


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _to_float(value: str | None) -> float:
    if not value:
        return 0.0
    cleaned = value.replace("px", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def _points_bounds(points: str) -> tuple[float, float]:
    max_x = 0.0
    max_y = 0.0
    for pair in points.split():
        if "," not in pair:
            continue
        x, y = pair.split(",", 1)
        max_x = max(max_x, _to_float(x))
        max_y = max(max_y, _to_float(y))
    return max_x, max_y
