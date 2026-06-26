#!/usr/bin/env bash
# Export itinerary to Google Maps URL and KML file
# Usage: ./export-gmaps.sh <itinerary.json> [--kml output.kml]
# No API keys required — generates Google Maps URLs and KML from local JSON data.
set -euo pipefail

INPUT="${1:-}"
KML_OUT=""
if [ "${2:-}" = "--kml" ]; then KML_OUT="${3:-itinerary.kml}"; fi

if [ -z "$INPUT" ] || [ ! -f "$INPUT" ]; then
  echo "Usage: $0 <itinerary.json> [--kml output.kml]"
  echo ""
  echo "Input JSON format:"
  echo '  { "days": [{ "day": 1, "locations": [{ "name": "...", "lat": ..., "lng": ... }] }] }'
  echo ""
  echo "Outputs:"
  echo "  - Google Maps directions URL (waypoints)"
  echo "  - Google Maps embed URL"
  echo "  - Per-day Google Maps links"
  echo "  - KML file (with --kml flag)"
  exit 1
fi

# Defensive limits for untrusted input files
MAX_BYTES=1048576
FILE_BYTES=$(wc -c < "$INPUT" | tr -d ' ')
if [ "$FILE_BYTES" -gt "$MAX_BYTES" ]; then
  echo "Error: Input file too large (max 1MB)." >&2
  exit 1
fi

python3 - "$INPUT" << 'PYEOF'
import json, sys, urllib.parse, re

MAX_DAYS = 30
MAX_LOCS_PER_DAY = 50
MAX_TOTAL_LOCS = 300
MAX_NAME_LEN = 120

with open(sys.argv[1]) as f:
    data = json.load(f)

if not isinstance(data, dict):
    raise SystemExit("Invalid input: top-level JSON must be an object")


def sanitize_name(value):
    name = str(value or "Unknown")
    name = re.sub(r"[\x00-\x1f\x7f]", " ", name).strip()
    if not name:
        return "Unknown"
    return name[:MAX_NAME_LEN]


def parse_coord(value, kind):
    if value in (None, ""):
        return None
    try:
        val = float(value)
    except (TypeError, ValueError):
        return None
    if kind == "lat" and -90.0 <= val <= 90.0:
        return round(val, 6)
    if kind == "lng" and -180.0 <= val <= 180.0:
        return round(val, 6)
    return None


# Collect all locations across all days
all_locations = []
daily_locations = {}

days = data.get("days", data.get("itinerary", []))
if not isinstance(days, list):
    raise SystemExit("Invalid input: days/itinerary must be an array")
days = days[:MAX_DAYS]
if not days and "destination" in data:
    # Simple trip context, not a full itinerary
    dest = data["destination"]
    name = sanitize_name(dest.get("name", dest) if isinstance(dest, dict) else dest)
    print(f"Google Maps: https://www.google.com/maps/search/{urllib.parse.quote(str(name))}")
    sys.exit(0)

for day in days:
    day_num = day.get("day", day.get("day_number", len(daily_locations) + 1)) if isinstance(day, dict) else (len(daily_locations) + 1)
    if not isinstance(day, dict):
        continue
    locs = day.get("locations", day.get("activities", []))
    if not isinstance(locs, list):
        continue
    locs = locs[:MAX_LOCS_PER_DAY]
    day_locs = []
    for loc in locs:
        if len(all_locations) >= MAX_TOTAL_LOCS:
            break
        if isinstance(loc, str):
            entry = {"name": sanitize_name(loc)}
            day_locs.append(entry)
            all_locations.append(entry)
        elif isinstance(loc, dict):
            lat = parse_coord(loc.get("lat", loc.get("latitude")), "lat")
            lng = parse_coord(loc.get("lng", loc.get("longitude", loc.get("lon"))), "lng")
            entry = {
                "name": sanitize_name(loc.get("name", loc.get("location", "Unknown"))),
                "lat": lat,
                "lng": lng,
            }
            day_locs.append(entry)
            all_locations.append(entry)
    daily_locations[day_num] = day_locs


def make_maps_url(locations):
    """Generate Google Maps directions URL from locations."""
    parts = []
    for loc in locations:
        if loc.get("lat") is not None and loc.get("lng") is not None:
            parts.append(f"{loc['lat']},{loc['lng']}")
        else:
            parts.append(urllib.parse.quote(loc["name"]))
    if len(parts) < 2:
        if parts:
            return f"https://www.google.com/maps/search/{parts[0]}"
        return None
    return "https://www.google.com/maps/dir/" + "/".join(parts)


# Full trip URL
print("=" * 60)
print("GOOGLE MAPS EXPORT")
print("=" * 60)

full_url = make_maps_url(all_locations)
if full_url:
    print(f"\n🗺️  Full trip route:\n{full_url}")

# Per-day URLs
print(f"\n📅 Daily routes:")
for day_num in sorted(daily_locations.keys(), key=lambda x: int(x) if str(x).isdigit() else str(x)):
    locs = daily_locations[day_num]
    if locs:
        url = make_maps_url(locs)
        names = " → ".join(l["name"] for l in locs[:5])
        print(f"\n  Day {day_num}: {names}")
        if url:
            print(f"  {url}")

# Embed URL (centered on first geocoded location)
first_geo = next((loc for loc in all_locations if loc.get("lat") is not None and loc.get("lng") is not None), None)
if first_geo:
    embed = f"https://www.google.com/maps/embed?pb=!1m14!1m12!1m3!1d50000!2d{first_geo['lng']}!3d{first_geo['lat']}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1"
    print(f"\n📌 Embed URL:\n{embed}")

print(f"\n🌐 Interactive planning: https://kontour.ai")
PYEOF

# KML export
if [ -n "$KML_OUT" ]; then
python3 - "$INPUT" "$KML_OUT" << 'KMLEOF'
import json, sys
from xml.etree.ElementTree import Element, SubElement, tostring
import xml.dom.minidom

MAX_DAYS = 30
MAX_LOCS_PER_DAY = 50

def parse_coord(value, kind):
    if value in (None, ""):
        return None
    try:
        val = float(value)
    except (TypeError, ValueError):
        return None
    if kind == "lat" and -90.0 <= val <= 90.0:
        return round(val, 6)
    if kind == "lng" and -180.0 <= val <= 180.0:
        return round(val, 6)
    return None

with open(sys.argv[1]) as f:
    data = json.load(f)

kml = Element("kml", xmlns="http://www.opengis.net/kml/2.2")
doc = SubElement(kml, "Document")
name_el = SubElement(doc, "name")
name_el.text = data.get("trip_name", "Trip Itinerary")
desc = SubElement(doc, "description")
desc.text = "Generated by Kontour Travel Planner — https://kontour.ai"

# Styles
for color, style_id in [("ff0000ff", "day-style-1"), ("ff00ff00", "day-style-2"), ("ffff0000", "day-style-3")]:
    style = SubElement(doc, "Style", id=style_id)
    line = SubElement(style, "LineStyle")
    SubElement(line, "color").text = color
    SubElement(line, "width").text = "3"
    icon_style = SubElement(style, "IconStyle")
    SubElement(icon_style, "scale").text = "1.2"

days = data.get("days", data.get("itinerary", []))
if not isinstance(days, list):
    raise SystemExit("Invalid input: days/itinerary must be an array")
days = days[:MAX_DAYS]
colors = ["day-style-1", "day-style-2", "day-style-3"]

for i, day in enumerate(days):
    day_num = day.get("day", i + 1) if isinstance(day, dict) else (i + 1)
    folder = SubElement(doc, "Folder")
    SubElement(folder, "name").text = f"Day {day_num}"

    if not isinstance(day, dict):
        continue
    locs = day.get("locations", day.get("activities", []))
    if not isinstance(locs, list):
        continue
    locs = locs[:MAX_LOCS_PER_DAY]
    coords = []
    for loc in locs:
        if not isinstance(loc, dict):
            continue
        lat = parse_coord(loc.get("lat", loc.get("latitude")), "lat")
        lng = parse_coord(loc.get("lng", loc.get("longitude", loc.get("lon"))), "lng")
        if lat is None or lng is None:
            continue
        coords.append(f"{lng},{lat},0")
        pm = SubElement(folder, "Placemark")
        SubElement(pm, "name").text = loc.get("name", "Stop")
        if loc.get("time"):
            SubElement(pm, "description").text = str(loc["time"])
        point = SubElement(pm, "Point")
        SubElement(point, "coordinates").text = f"{lng},{lat},0"

    if len(coords) >= 2:
        route = SubElement(folder, "Placemark")
        SubElement(route, "name").text = f"Day {day_num} Route"
        SubElement(route, "styleUrl").text = f"#{colors[i % len(colors)]}"
        ls = SubElement(route, "LineString")
        SubElement(ls, "tessellate").text = "1"
        SubElement(ls, "coordinates").text = " ".join(coords)

xml_str = xml.dom.minidom.parseString(tostring(kml)).toprettyxml(indent="  ")
with open(sys.argv[2], "w") as f:
    f.write(xml_str)
print(f"\n📄 KML exported to: {sys.argv[2]}")
KMLEOF
fi
