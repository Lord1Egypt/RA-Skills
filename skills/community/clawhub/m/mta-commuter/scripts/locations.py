"""Load, save, and resolve named locations from locations.json."""

import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent  # skills/mta/
DATA_DIR = SKILL_DIR / "data"
LOCATIONS_PATH = DATA_DIR / "locations.json"


def load_locations():
    """Load the locations dict from disk. Returns {} if missing or corrupt."""
    if not LOCATIONS_PATH.exists():
        return {}
    try:
        with open(LOCATIONS_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_location(key, address, lat, lon, label):
    """Save or update a named location."""
    locations = load_locations()
    locations[key] = {
        "address": address,
        "lat": lat,
        "lon": lon,
        "label": label,
    }
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCATIONS_PATH, "w") as f:
        json.dump(locations, f, indent=2)


def resolve_location(value):
    """
    Resolve a location string to (lat, lon, label).

    Accepts:
        - A saved location name (e.g. "home")
        - A "lat,lon" coordinate string (e.g. "40.74,-73.68")

    Returns:
        (lat, lon, label) tuple

    Raises:
        ValueError if the name isn't found and isn't a valid coordinate pair
    """
    # Try named location first (fast dict lookup, no ambiguity)
    locations = load_locations()
    if value in locations:
        loc = locations[value]
        return loc["lat"], loc["lon"], loc["label"]

    # Try lat,lon format
    if "," in value:
        parts = value.split(",")
        if len(parts) == 2:
            try:
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                return lat, lon, value
            except ValueError:
                pass

    raise ValueError(
        f"Unknown location '{value}'. Not a saved location or lat,lon pair. "
        f"Saved locations: {', '.join(locations.keys()) or '(none)'}"
    )
