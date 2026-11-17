"""Normalize WGS84 coordinates and report validation or swap warnings."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils import normalize_vertices, validate_coordinates


def locate_country(vertices):
    """Validate coordinates while leaving country selection to confirmed context."""
    normalized, parse_errors = normalize_vertices(vertices)
    per_vertex = []
    warnings = []

    for index, (lon, lat) in enumerate(normalized):
        swapped = False
        if abs(lat) > 90 and abs(lon) <= 90 and abs(lat) <= 180:
            lon, lat = lat, lon
            swapped = True
            warnings.append(f"Vertex {index}: latitude/longitude order was swapped")
        per_vertex.append(
            {
                "index": index,
                "lon": lon,
                "lat": lat,
                "swapped": swapped,
                "country_code": None,
                "country_name": None,
                "method": "pending_confirmation",
            }
        )

    normalized_pairs = [[item["lon"], item["lat"]] for item in per_vertex]
    errors = parse_errors + validate_coordinates(normalized_pairs)
    return {
        "country_code": None,
        "country_name": None,
        "method": "pending_confirmation",
        "normalized_vertices": normalized_pairs,
        "per_vertex": per_vertex,
        "country_code_counts": {},
        "warnings": warnings,
        "errors": errors,
        "valid": not errors,
    }


def main():
    input_data = json.load(sys.stdin)
    if isinstance(input_data, list):
        vertices = input_data
    elif isinstance(input_data, dict) and "vertices" in input_data:
        vertices = input_data["vertices"]
    else:
        raise SystemExit("Expected a JSON list or an object containing 'vertices'")

    result = locate_country(vertices)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    if not result["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
