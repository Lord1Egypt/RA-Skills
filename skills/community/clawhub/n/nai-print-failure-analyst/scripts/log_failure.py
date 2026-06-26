#!/usr/bin/env python3
"""
log_failure.py — Log a 3D print failure to the failure log.

Usage:
  log_failure.py --printer "Prusa MK4" --material "PLA" --failure-type "stringing" \
      --description "Hair everywhere between towers" \
      --slicer-settings '{"temperature": 210, "retraction_distance_mm": 3.5}' \
      --fixed-by "Reduced temp to 200C, enabled wipe" \
      --notes "New spool, might be wet"
"""

import argparse
import json
import os
import sys
import uuid
from datetime import datetime

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(SKILL_DIR, "assets", "failure-log.json")

VALID_FAILURE_TYPES = [
    "stringing", "warping", "layer_adhesion", "under_extrusion", "over_extrusion",
    "elephant_foot", "layer_shifting", "bridging", "overhang", "clog",
    "pillowing", "ringing", "z_banding", "seam", "supports", "first_layer",
    "wet_filament", "spaghetti", "other",
]


# ---------------------------------------------------------------------------
# Log management
# ---------------------------------------------------------------------------

def load_log():
    """Load the failure log, creating it if absent."""
    if not os.path.exists(LOG_FILE):
        return {"failures": []}
    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
        if "failures" not in data:
            data["failures"] = []
        return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading log file: {e}", file=sys.stderr)
        sys.exit(1)


def save_log(data):
    """Save the failure log."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error writing log file: {e}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Log a 3D print failure to the failure log."
    )
    parser.add_argument("--printer", "-p", required=True, help="Printer name (e.g. 'Prusa MK4')")
    parser.add_argument("--material", "-m", required=True, help="Filament material (e.g. 'PLA', 'PETG')")
    parser.add_argument(
        "--failure-type", "-f", required=True,
        help=f"Failure type. Options: {', '.join(VALID_FAILURE_TYPES)}"
    )
    parser.add_argument("--description", "-d", required=True, help="Description of the failure")
    parser.add_argument(
        "--slicer-settings", "-s",
        help='JSON string of slicer settings used (e.g. \'{"temperature": 210, "speed": 60}\')',
    )
    parser.add_argument("--fixed-by", help="What fixed the issue (optional)")
    parser.add_argument("--notes", "-n", help="Additional notes (optional)")
    parser.add_argument("--material-brand", help="Filament brand (optional, e.g. 'Prusament')")

    args = parser.parse_args()

    # Normalize failure type
    failure_type = args.failure_type.lower().replace(" ", "_").replace("-", "_")
    if failure_type not in VALID_FAILURE_TYPES:
        print(f"Warning: '{failure_type}' is not a recognized failure type.")
        print(f"Known types: {', '.join(VALID_FAILURE_TYPES)}")
        print("Logging as 'other'.")
        failure_type = "other"

    # Parse slicer settings
    slicer_settings = {}
    if args.slicer_settings:
        try:
            slicer_settings = json.loads(args.slicer_settings)
            if not isinstance(slicer_settings, dict):
                raise ValueError("Slicer settings must be a JSON object")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error: --slicer-settings is not valid JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # Build entry
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "printer": args.printer,
        "material": args.material,
        "failure_type": failure_type,
        "description": args.description,
        "slicer_settings": slicer_settings,
    }

    if args.material_brand:
        entry["material_brand"] = args.material_brand
    if args.fixed_by:
        entry["fixed_by"] = args.fixed_by
    if args.notes:
        entry["notes"] = args.notes

    # Load, append, save
    data = load_log()
    data["failures"].append(entry)
    save_log(data)

    print(f"✓ Failure logged successfully.")
    print(f"  ID:           {entry['id']}")
    print(f"  Timestamp:    {entry['timestamp']}")
    print(f"  Printer:      {entry['printer']}")
    print(f"  Material:     {entry['material']}")
    print(f"  Failure Type: {entry['failure_type']}")
    print(f"  Log file:     {LOG_FILE}")
    print(f"  Total logged: {len(data['failures'])} failure(s)")


if __name__ == "__main__":
    main()
