"""
Normalize and validate WGS84 parcel coordinates.

This script no longer performs reverse-geocoding.  The LLM determines the
ISO 3166-1 alpha-2 country code from spatial knowledge and conversation
context.  The script's role is to catch common coordinate mistakes
(swapped lat/lon, out-of-range values) before downstream processing.

CLI usage:
    echo '[[114.13472, 22.50422], [114.13564, 22.50411]]' | python3 scripts/country_locator.py
    # {"country_code": null, "country_name": null, "method": "pending_llm"}
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def locate_country(vertices):
    """Normalize vertices and flag common errors.  Returns country_code: null.

    The LLM is responsible for determining the actual country.

    Args:
        vertices: list of [lon, lat] or [lat, lon] pairs (WGS84 decimal).
                  Will auto-detect swapped lat/lon.

    Returns:
        dict with keys: country_code (always null), country_name (always null),
        method ("pending_llm"), per_vertex (list), country_code_counts (empty dict)
    """
    if not vertices:
        return {
            'country_code': None, 'country_name': None, 'method': 'pending_llm',
            'per_vertex': [], 'country_code_counts': {},
        }

    per_vertex = []
    for i, v in enumerate(vertices):
        lon, lat = float(v[0]), float(v[1])
        if abs(lat) > 90 and abs(lon) <= 90:
            lon, lat = lat, lon

        per_vertex.append({
            'index': i, 'lon': lon, 'lat': lat,
            'country_code': None, 'country_name': None, 'method': 'pending_llm',
        })

    return {
        'country_code': None,
        'country_name': None,
        'method': 'pending_llm',
        'per_vertex': per_vertex,
        'country_code_counts': {},
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    input_data = json.load(sys.stdin)
    if isinstance(input_data, list):
        vertices = input_data
    elif isinstance(input_data, dict) and 'vertices' in input_data:
        vertices = input_data['vertices']
    else:
        print("Usage: echo '[[lon, lat], ...]' | python3 scripts/country_locator.py", file=sys.stderr)
        sys.exit(1)

    result = locate_country(vertices)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()
