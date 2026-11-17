"""Shared validation, coordinate, and CSV helpers."""

import csv
import json
import math
import os
import re
import sys
from pathlib import Path


COUNTRY_CODE_RE = re.compile(r"^[A-Z]{2}$")
DATE_TOKEN_RE = re.compile(r"^\d{6}$")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
BOUNDARY_TOLERANCE = 1e-8


def get_workspace_root():
    """Return the data workspace, never an arbitrary ancestor directory."""
    configured = os.environ.get("OVITALMAP_WORKSPACE")
    if configured:
        return Path(configured).expanduser().resolve()

    cwd = Path.cwd().resolve()
    if cwd != Path(cwd.anchor):
        return cwd
    return Path(__file__).resolve().parent.parent


def validate_country_code(country_code):
    value = str(country_code or "").strip().upper()
    if not COUNTRY_CODE_RE.fullmatch(value):
        raise ValueError("country_code must be an ISO alpha-2 code such as CN")
    return value


def validate_date_token(date_token):
    value = str(date_token or "").strip()
    if not DATE_TOKEN_RE.fullmatch(value):
        raise ValueError("date must use YYMMDD format")
    return value


def validate_identifier(value, field_name="identifier"):
    text = str(value or "").strip()
    if not SAFE_ID_RE.fullmatch(text) or text in {".", ".."}:
        raise ValueError(
            f"{field_name} must contain 1-80 letters, digits, dots, underscores, or hyphens"
        )
    return text


def normalize_vertices(vertices):
    """Convert coordinate pairs to finite floats while preserving their order."""
    normalized = []
    errors = []
    if not isinstance(vertices, (list, tuple)):
        return [], ["vertices must be a list of [longitude, latitude] pairs"]

    for index, vertex in enumerate(vertices):
        if not isinstance(vertex, (list, tuple)) or len(vertex) != 2:
            errors.append(f"Vertex {index}: expected [longitude, latitude]")
            continue
        try:
            lon, lat = float(vertex[0]), float(vertex[1])
        except (TypeError, ValueError):
            errors.append(f"Vertex {index}: longitude and latitude must be numbers")
            continue
        if not math.isfinite(lon) or not math.isfinite(lat):
            errors.append(f"Vertex {index}: coordinates must be finite numbers")
            continue
        normalized.append((lon, lat))
    return normalized, errors


def validate_coordinates(vertices, require_polygon=False):
    normalized, errors = normalize_vertices(vertices)
    for index, (lon, lat) in enumerate(normalized):
        if not -180.0 <= lon <= 180.0:
            errors.append(f"Vertex {index}: longitude {lon} out of range [-180, 180]")
        if not -90.0 <= lat <= 90.0:
            errors.append(f"Vertex {index}: latitude {lat} out of range [-90, 90]")

    open_vertices = _strip_closing_vertex(normalized)
    if require_polygon and len(open_vertices) < 3:
        errors.append("A parcel boundary requires at least three vertices")
    return errors


def check_duplicate_vertices(vertices):
    """Remove repeated points; treat the final closing point as intentional."""
    normalized, errors = normalize_vertices(vertices)
    if errors:
        return list(vertices) if isinstance(vertices, (list, tuple)) else [], errors

    closed = len(normalized) > 1 and _points_close(normalized[0], normalized[-1])
    source = list(vertices)
    candidates = normalized[:-1] if closed else normalized
    source_candidates = source[:-1] if closed else source
    deduped = []
    comparable = []
    warnings = []
    for index, (point, original) in enumerate(zip(candidates, source_candidates)):
        duplicate_index = next(
            (prior for prior, existing in enumerate(comparable) if _points_close(point, existing)),
            None,
        )
        if duplicate_index is None:
            deduped.append(tuple(original))
            comparable.append(point)
        else:
            warnings.append(
                f"Vertex {index}: duplicate of vertex {duplicate_index} "
                f"({point[0]}, {point[1]}); skipped"
            )
    return deduped, warnings


def parse_boundary_coords(boundary_str):
    if not boundary_str or not str(boundary_str).strip():
        return []
    result = []
    for item in str(boundary_str).strip().split(";"):
        if not item.strip():
            continue
        parts = item.split(",")
        if len(parts) != 2:
            raise ValueError(f"Invalid boundary coordinate: {item!r}")
        result.append((float(parts[0]), float(parts[1])))
    return result


def build_boundary_string(vertices, close_polygon=True):
    normalized, errors = normalize_vertices(vertices)
    if errors:
        raise ValueError("; ".join(errors))
    points = [tuple(point) for point in vertices]
    if close_polygon and len(points) > 1 and not _points_close(normalized[0], normalized[-1]):
        points.append(points[0])
    return ";".join(f"{lon},{lat}" for lon, lat in points)


def boundaries_equal(first, second, tolerance=BOUNDARY_TOLERANCE):
    """Compare polygon vertices independent of start point and direction."""
    left = parse_boundary_coords(first) if isinstance(first, str) else list(first)
    right = parse_boundary_coords(second) if isinstance(second, str) else list(second)
    left = _strip_closing_vertex(left)
    right = _strip_closing_vertex(right)
    if len(left) != len(right):
        return False
    if not left:
        return True

    for candidate in (right, list(reversed(right))):
        for offset in range(len(candidate)):
            rotated = candidate[offset:] + candidate[:offset]
            if all(
                _points_close(a, b, tolerance)
                for a, b in zip(left, rotated)
            ):
                return True
    return False


def _points_close(first, second, tolerance=BOUNDARY_TOLERANCE):
    return (
        math.isclose(float(first[0]), float(second[0]), abs_tol=tolerance, rel_tol=0.0)
        and math.isclose(float(first[1]), float(second[1]), abs_tol=tolerance, rel_tol=0.0)
    )


def _strip_closing_vertex(vertices):
    points = list(vertices)
    if len(points) > 1 and _points_close(points[0], points[-1]):
        return points[:-1]
    return points


_DMS_RE = re.compile(
    r"""^\s*
        (?P<sign>[+-]?)
        (?P<deg>\d+(?:\.\d+)?)\s*[°]\s*
        (?:(?P<min>\d+(?:\.\d+)?)\s*['′]\s*)?
        (?:(?P<sec>\d+(?:\.\d+)?)\s*["″]\s*)?
        (?P<hem>[NSEWnsew])?
        \s*$""",
    re.VERBOSE,
)


def dms_to_decimal(dms_str):
    match = _DMS_RE.fullmatch(str(dms_str))
    if not match:
        raise ValueError(f"Cannot parse DMS: {dms_str!r}")

    degrees = float(match.group("deg"))
    minutes = float(match.group("min") or 0)
    seconds = float(match.group("sec") or 0)
    hemisphere = (match.group("hem") or "").upper()
    if minutes >= 60 or seconds >= 60:
        raise ValueError("DMS minutes and seconds must be below 60")
    if hemisphere in {"N", "S"} and degrees > 90:
        raise ValueError("Latitude degrees must be at most 90")
    if hemisphere in {"E", "W"} and degrees > 180:
        raise ValueError("Longitude degrees must be at most 180")

    negative = match.group("sign") == "-" or hemisphere in {"S", "W"}
    if match.group("sign") == "-" and hemisphere in {"N", "E"}:
        raise ValueError("DMS sign conflicts with hemisphere")
    decimal = degrees + minutes / 60.0 + seconds / 3600.0
    return -decimal if negative else decimal


def read_csv(filepath):
    path = Path(filepath)
    if not path.exists():
        return None, []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return reader.fieldnames, list(reader)


def append_csv(filepath, headers, rows):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        if not file_exists:
            writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(header, "") for header in headers])


def write_csv(filepath, headers, rows):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(header, "") for header in headers])


def read_json_stdin():
    return json.load(sys.stdin)


def write_json_stdout(data):
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
