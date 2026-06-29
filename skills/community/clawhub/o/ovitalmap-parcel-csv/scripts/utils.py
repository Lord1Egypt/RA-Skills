"""
Shared utilities for ovitalmap parcel processing.
"""

import csv
import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Workspace root resolution
# ---------------------------------------------------------------------------

def get_workspace_root():
    """Resolve the actual workspace root where ovitalmap_archive/ etc. live.

    When the skill is installed under e.g. skills/ovitalmap-parcel-csv/ inside
    an OpenClaw workspace, the archive lives at the workspace root — not inside
    the skill directory.  This function walks up from the script directory until
    it finds a parent that contains ovitalmap_archive/, falling back to the
    skill root when no ancestor qualifies (local dev / standalone usage).
    """
    skill_root = Path(__file__).resolve().parent.parent
    for ancestor in [skill_root] + list(skill_root.parents):
        if (ancestor / 'ovitalmap_archive').is_dir():
            return ancestor
    return skill_root


# ---------------------------------------------------------------------------
# Boundary / coordinate helpers
# ---------------------------------------------------------------------------

def parse_boundary_coords(boundary_str):
    """Parse a boundary string 'lon,lat;lon,lat;...' into list of (lon, lat) floats."""
    if not boundary_str or not boundary_str.strip():
        return []
    pairs = boundary_str.strip().split(';')
    result = []
    for p in pairs:
        p = p.strip()
        if not p:
            continue
        parts = p.split(',')
        result.append((float(parts[0]), float(parts[1])))
    return result


def build_boundary_string(vertices, close_polygon=True):
    """Build boundary string from list of (lon, lat) tuples.
    Optionally close the polygon by repeating the first vertex at the end.
    """
    verts = list(vertices)
    if close_polygon and len(verts) > 1:
        if verts[0] != verts[-1]:
            verts.append(verts[0])
    return ';'.join(f'{lon},{lat}' for lon, lat in verts)


def normalize_boundary_sequence(vertices):
    """Normalize a vertex list to its canonical form for order-independent comparison.

    Returns the lexicographically smallest tuple across all cyclic permutations
    and reversals.  This makes equality checks order- and direction-independent.
    """
    if not vertices:
        return tuple()
    n = len(vertices)
    best = None
    # all cyclic permutations — forward direction
    for i in range(n):
        perm = tuple(vertices[i:] + vertices[:i])
        if best is None or perm < best:
            best = perm
    # all cyclic permutations — reversed direction
    rev = tuple(reversed(vertices))
    for i in range(n):
        perm = tuple(rev[i:] + rev[:i])
        if best is None or perm < best:
            best = perm
    return best


def boundaries_equal(b1, b2):
    """True if two boundary vertex sets are equal, ignoring start point & direction."""
    v1 = parse_boundary_coords(b1) if isinstance(b1, str) else list(b1)
    v2 = parse_boundary_coords(b2) if isinstance(b2, str) else list(b2)
    # Strip closing vertex if it repeats the first (closed-polygon convention)
    v1 = _strip_closing_vertex(v1)
    v2 = _strip_closing_vertex(v2)
    return normalize_boundary_sequence(v1) == normalize_boundary_sequence(v2)


def _strip_closing_vertex(vertices):
    """Remove the last vertex if it duplicates the first (closed polygon)."""
    if len(vertices) > 1 and vertices[0] == vertices[-1]:
        return vertices[:-1]
    return vertices


# ---------------------------------------------------------------------------
# DMS conversion
# ---------------------------------------------------------------------------

_DMS_RE = re.compile(
    r"""(?P<deg>[\d.]+)[° ]\s*
        (?:(?P<min>[\d.]+)['′ ]\s*)?
        (?:(?P<sec>[\d.]+)["″]\s*)?
        \s*(?P<hem>[NSEWnsew])?""",
    re.VERBOSE,
)


def dms_to_decimal(dms_str):
    """Convert a single DMS string like \"22°30'15.2\\\"N\" to decimal degrees."""
    s = dms_str.strip()
    m = _DMS_RE.search(s)
    if not m:
        raise ValueError(f'Cannot parse DMS: {dms_str!r}')
    deg = float(m.group('deg'))
    min_val = float(m.group('min')) if m.group('min') else 0.0
    sec = float(m.group('sec')) if m.group('sec') else 0.0
    decimal = deg + min_val / 60.0 + sec / 3600.0
    hem = (m.group('hem') or '').upper()
    if hem in ('S', 'W'):
        decimal = -decimal
    return decimal


# ---------------------------------------------------------------------------
# CSV I/O
# ---------------------------------------------------------------------------

def read_csv(filepath):
    """Read a CSV file.  Returns (fieldnames, list_of_dicts).
    Returns (None, []) if the file does not exist.
    """
    path = Path(filepath)
    if not path.exists():
        return None, []
    with open(path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return reader.fieldnames, list(reader)


def append_csv(filepath, headers, rows):
    """Append rows to a CSV.  Creates the file with headers if missing."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with open(path, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(h, '') for h in headers])


def write_csv(filepath, headers, rows):
    """Overwrite a CSV file with headers and rows."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow([row.get(h, '') for h in headers])


def read_json_stdin():
    """Read JSON from stdin."""
    return json.load(sys.stdin)


def write_json_stdout(data):
    """Write JSON to stdout."""
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')


# ---------------------------------------------------------------------------
# Coordinate validation
# ---------------------------------------------------------------------------

def check_duplicate_vertices(vertices):
    """Detect duplicate vertices. Returns (deduplicated_list, warnings).

    Keeps the first occurrence of each coordinate pair and reports later
    duplicates. Comparison uses a tolerance of 1e-9 for floating-point safety.
    """
    deduped = []
    warnings = []
    seen = {}
    for i, (lon, lat) in enumerate(vertices):
        key = (round(lon, 9), round(lat, 9))
        if key in seen:
            prev_i = seen[key]
            warnings.append(f'Vertex {i}: duplicate of vertex {prev_i} ({lon}, {lat}) — kept first occurrence, skipped duplicate')
        else:
            seen[key] = i
            deduped.append((lon, lat))
    return deduped, warnings


def validate_coordinates(vertices):
    """Validate a list of (lon, lat) pairs. Returns list of error messages."""
    errors = []
    for i, (lon, lat) in enumerate(vertices):
        if not (-180.0 <= lon <= 180.0):
            errors.append(f'Vertex {i}: longitude {lon} out of range [-180, 180]')
        if not (-90.0 <= lat <= 90.0):
            errors.append(f'Vertex {i}: latitude {lat} out of range [-90, 90]')
    return errors
