#!/usr/bin/env python3
"""
Fetch pollen forecast from Swedish Pollenrapporten API.
Usage: python3 get_forecast.py <city-name>
Example: python3 get_forecast.py Göteborg
"""

import sys
import json
import urllib.request
from pathlib import Path

API_BASE = "https://api.pollenrapporten.se/v1"
SKILL_DIR = Path(__file__).parent.parent
REGIONS_FILE = SKILL_DIR / "references" / "regions.json"

LEVEL_NAMES = {
    0: ("None", "Inga halter"),
    1: ("Low", "Låga halter"),
    2: ("Moderate", "Måttliga halter"),
    3: ("High", "Höga halter"),
    4: ("Very High", "Mycket höga halter")
}

# Boss is hyper-allergic to grass pollen - these trigger special alerts
GRASS_POLLEN_NAMES = ["Gräs", "Grass", "gräs", "grass"]


def load_regions():
    """Load region mappings from reference file."""
    with open(REGIONS_FILE) as f:
        return json.load(f)


def find_region(city_name, data):
    """Find region ID for a given city name."""
    city = city_name.strip()
    regions = data["regions"]
    mappings = data.get("common_mappings", {})
    
    # Check direct match first
    for region in regions:
        if region["name"].lower() == city.lower():
            return region
    
    # Check common mappings
    if city in mappings:
        mapped_city = mappings[city]
        for region in regions:
            if region["name"] == mapped_city:
                return region
    
    # Try case-insensitive partial match
    for region in regions:
        if city.lower() in region["name"].lower() or region["name"].lower() in city.lower():
            return region
    
    return None


def fetch_pollen_types():
    """Fetch pollen type definitions from API."""
    url = f"{API_BASE}/pollen-types"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-PollenBot/1.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # Create ID -> detailed info mapping
            types = {}
            for item in data.get("items", []):
                name = item.get("name", item.get("swedishName", "Unknown"))
                types[item["id"]] = {
                    "name": name,
                    "thresholds": {
                        "low": item.get("thresholdLow", 0),
                        "medium": item.get("thresholdMedium", 0),
                        "high": item.get("thresholdHigh", 0),
                        "veryHigh": item.get("thresholdVeryHigh", 0)
                    }
                }
            return types
    except Exception as e:
        print(f"Warning: Could not fetch pollen types: {e}")
        return {}


def fetch_level_definitions():
    """Fetch pollen level definitions (Swedish names)."""
    url = f"{API_BASE}/pollen-level-definitions"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-PollenBot/1.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # Create level -> Swedish name mapping
            levels = {}
            for item in data.get("items", []):
                level = item.get("level")
                if level is not None:
                    levels[level] = item.get("name", LEVEL_NAMES.get(level, ("?", "?"))[1])
            return levels
    except Exception as e:
        print(f"Warning: Could not fetch level definitions: {e}")
        return {}


def fetch_forecast(region_id):
    """Fetch current forecast for a region."""
    url = f"{API_BASE}/forecasts?region_id={region_id}&current=True"
    try:
        req = urllib.request.Request(url, headers={
            "Accept": "application/json",
            "User-Agent": "OpenClaw-PollenBot/1.0"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return None


def format_forecast(data, pollen_types, level_definitions, region_name, alert_mode=False):
    """Format forecast data for display."""
    if not data or "items" not in data or not data["items"]:
        return "No forecast data available."
    
    forecast = data["items"][0]
    start_date = forecast.get("startDate", "?")
    end_date = forecast.get("endDate", "?")
    summary = forecast.get("text", "No summary available.")
    
    # Track grass pollen level for alerts
    grass_level = 0
    grass_name = "Gräs"
    
    output = []
    output.append(f"🌿 Pollen Forecast for {region_name}")
    output.append(f"📅 {start_date} to {end_date}")
    output.append("")
    output.append("📝 Summary:")
    output.append(summary)
    output.append("")
    
    # Get latest levels from levelSeries
    levels = forecast.get("levelSeries", [])
    if levels:
        output.append("📊 Current Levels:")
        # Group by pollen ID and get latest
        latest_levels = {}
        for entry in levels:
            pid = entry.get("pollenId")
            if pid:
                latest_levels[pid] = entry.get("level", 0)
        
        for pid, level in sorted(latest_levels.items()):
            p_info = pollen_types.get(pid, {"name": "Unknown"})
            pollen_name = p_info.get('name', 'Unknown')
            
            # Check if this is grass pollen
            is_grass = any(g in pollen_name for g in GRASS_POLLEN_NAMES)
            if is_grass:
                grass_level = level
                grass_name = pollen_name
            
            # Use level definitions if available, fallback to defaults
            level_sv = level_definitions.get(level, LEVEL_NAMES.get(level, ("?", "?"))[1])
            level_en = LEVEL_NAMES.get(level, ("Unknown", "?"))[0]
            
            output.append(f"• {pollen_name}: {level_en} / {level_sv}")
    
    # Add grass pollen alert for Boss (hyper-allergic)
    if alert_mode and grass_level >= 2:
        output.append("")
        output.append("⚠️ GRASS POLLEN ALERT ⚠️")
        if grass_level == 2:
            output.append(f"🌾 {grass_name} is at MODERATE levels.")
            output.append("💊 Recommendation: Start taking allergy medication.")
            output.append("😷 Consider wearing a mask if spending extended time outdoors.")
        elif grass_level == 3:
            output.append(f"🌾 {grass_name} is at HIGH levels.")
            output.append("💊 Take allergy medication now.")
            output.append("😷 Wear mask + 👓 glasses when outside.")
            output.append("🚪 Keep windows closed. Use air purifier if available.")
        elif grass_level >= 4:
            output.append(f"🌾 {grass_name} is at VERY HIGH levels!")
            output.append("🚨 HIGH ALERT for grass allergy sufferers.")
            output.append("💊 Take medication immediately.")
            output.append("😷 Mask + 👓 glasses REQUIRED outdoors.")
            output.append("🏠 Minimize outdoor exposure today.")
            output.append("🚪 Keep all windows closed. Shower after any outdoor time.")
    
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 get_forecast.py <city-name> [--alert]")
        print("Example: python3 get_forecast.py Göteborg")
        print("         python3 get_forecast.py Göteborg --alert  (for grass pollen warnings)")
        print("\nAvailable cities:")
        data = load_regions()
        for r in data["regions"]:
            print(f"  - {r['name']}")
        sys.exit(1)
    
    city = sys.argv[1]
    alert_mode = "--alert" in sys.argv
    
    # Load regions
    try:
        data = load_regions()
    except Exception as e:
        print(f"Error loading regions: {e}")
        sys.exit(1)
    
    # Find region
    region = find_region(city, data)
    if not region:
        print(f"City '{city}' not found. Available cities:")
        for r in data["regions"]:
            print(f"  - {r['name']}")
        sys.exit(1)
    
    # Fetch data
    print(f"Fetching forecast for {region['name']}...")
    
    pollen_types = fetch_pollen_types()
    level_definitions = fetch_level_definitions()
    forecast_data = fetch_forecast(region["id"])
    
    if forecast_data:
        print()
        print(format_forecast(forecast_data, pollen_types, level_definitions, region["name"], alert_mode))
    else:
        print("Failed to fetch forecast data.")
        sys.exit(1)


if __name__ == "__main__":
    main()
