#!/usr/bin/env python3
"""
Main entry point for the Location Service skill.
Handles geocoding, distance calculation, and weather integration based on input format.
Supports Google Maps links (standard and short URLs) as coordinate input.
"""

import sys
import subprocess
import re
import urllib.request

def run_script(script_path, args):
    """Run a Python script and return its output"""
    try:
        result = subprocess.run(
            [sys.executable, script_path] + args,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return result.stdout.strip(), None
        else:
            return None, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return None, "Error: Script execution timed out"
    except Exception as e:
        return None, f"Error: {str(e)}"

def is_coordinate_pair(text):
    """Check if text looks like a coordinate pair (lat,lon)"""
    pattern = r'^-?\d+\.?\d*,\s*-?\d+\.?\d*$'
    return bool(re.match(pattern, text.strip()))

def parse_coordinates(text):
    """Parse coordinate string into lat, lon floats"""
    parts = text.split(',')
    if len(parts) != 2:
        raise ValueError("Invalid coordinate format")
    lat = float(parts[0].strip())
    lon = float(parts[1].strip())
    return lat, lon

def is_google_maps_url(text):
    """Check if text looks like a Google Maps URL (standard or short)"""
    return bool(re.match(
        r'https?://(maps\.google\.com|www\.google\.com/maps|maps\.app\.goo\.gl)',
        text.strip()
    ))

def resolve_short_url(url):
    """Follow redirects on a short URL and return the final URL"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'LocationService/1.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.url
    except Exception as e:
        raise ValueError(f"Failed to resolve short URL: {e}")

def extract_coords_from_google_maps(url):
    """
    Extract (lat, lon) from a Google Maps URL.
    Supports:
      - maps.google.com/?q=lat,lon
      - maps.google.com/?ll=lat,lon
      - google.com/maps/@lat,lon,z
      - google.com/maps/place/.../@lat,lon,z
      - maps.app.goo.gl/... (short URL, resolved first)
    Returns a 'lat,lon' string or raises ValueError.
    """
    url = url.strip()

    # Resolve short URLs first
    if 'maps.app.goo.gl' in url:
        url = resolve_short_url(url)

    coord_re = r'(-?\d+\.\d+),\s*(-?\d+\.\d+)'

    # ?q=lat,lon  or  ?ll=lat,lon
    for param in ('q', 'll'):
        m = re.search(rf'[?&]{param}=' + coord_re, url)
        if m:
            return f"{m.group(1)},{m.group(2)}"

    # /@lat,lon,z  (works for both /maps/@ and /maps/place/.../@)
    m = re.search(r'/@' + coord_re, url)
    if m:
        return f"{m.group(1)},{m.group(2)}"

    raise ValueError("No coordinates found in Google Maps URL; try using the place name directly as address input")

def resolve_location_to_coords(location_spec):
    """
    Given a location specifier (coordinates, Google Maps URL, or address),
    always return a 'lat,lon' string. Raises ValueError on failure.
    """
    location_spec = location_spec.strip()

    if is_coordinate_pair(location_spec):
        return location_spec

    if is_google_maps_url(location_spec):
        return extract_coords_from_google_maps(location_spec)

    # Address → forward geocode
    script_path = "/home/ubuntu/.openclaw/workspace/skills/location-service/scripts/geocode_forward.py"
    out, err = run_script(script_path, [location_spec])
    if err:
        raise ValueError(f"Error geocoding location: {err}")
    if out and ',' in out:
        return out.split('\n')[0].strip()
    raise ValueError(f"Could not geocode location '{location_spec}'")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 location_service.py <input>")
        print("Examples:")
        print("  python3 location_service.py '41.9028,12.4964'")
        print("  python3 location_service.py 'Colosseum, Rome'")
        print("  python3 location_service.py 'https://maps.google.com/?q=41.9028,12.4964'")
        print("  python3 location_service.py 'https://maps.app.goo.gl/AbCdEfGhIjKlMnOp'")
        print("  python3 location_service.py '41.9028,12.4964 to 40.7128,-74.0060'")
        print("  python3 location_service.py 'https://maps.google.com/?q=41.9028,12.4964 to https://maps.google.com/?q=40.7128,-74.0060'")
        print("  python3 location_service.py 'weather for 41.9028,12.4964'")
        print("  python3 location_service.py 'weather for https://maps.google.com/?q=41.9028,12.4964'")
        sys.exit(1)

    input_text = ' '.join(sys.argv[1:]).strip()

    # ── Weather query ──────────────────────────────────────────────────────────
    if input_text.lower().startswith('weather for'):
        location_spec = input_text[11:].strip()
        if not location_spec:
            print("Error: Please specify a location after 'weather for'", file=sys.stderr)
            sys.exit(1)

        try:
            coords = resolve_location_to_coords(location_spec)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        lat, lon = parse_coordinates(coords)
        print(f"Weather coordinates: {lat},{lon}")
        print("# Note: Full weather integration would call the weather skill here")

    # ── Distance calculation (contains " to ") ────────────────────────────────
    elif ' to ' in input_text.lower():
        # Split on first and last " to " to tolerate URLs containing "to"
        split_idx = input_text.lower().index(' to ')
        coord1_str = input_text[:split_idx].strip()
        coord2_str = input_text[split_idx + 4:].strip()

        try:
            coords1 = resolve_location_to_coords(coord1_str)
            coords2 = resolve_location_to_coords(coord2_str)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        lat1, lon1 = parse_coordinates(coords1)
        lat2, lon2 = parse_coordinates(coords2)

        script_path = "/home/ubuntu/.openclaw/workspace/skills/location-service/scripts/distance_calc.py"
        distance_out, distance_err = run_script(script_path, [str(lat1), str(lon1), str(lat2), str(lon2)])
        if distance_err:
            print(f"Error calculating distance: {distance_err}", file=sys.stderr)
            sys.exit(1)

        print(distance_out)

    # ── Google Maps URL (single location) ────────────────────────────────────
    elif is_google_maps_url(input_text):
        try:
            coords = extract_coords_from_google_maps(input_text)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)

        lat, lon = parse_coordinates(coords)
        script_path = "/home/ubuntu/.openclaw/workspace/skills/location-service/scripts/geocode_reverse.py"
        address_out, address_err = run_script(script_path, [str(lat), str(lon)])
        if address_err:
            print(f"Error reverse geocoding: {address_err}", file=sys.stderr)
            sys.exit(1)

        print(address_out)

    # ── Coordinate pair (reverse geocoding) ──────────────────────────────────
    elif is_coordinate_pair(input_text):
        lat, lon = parse_coordinates(input_text)
        script_path = "/home/ubuntu/.openclaw/workspace/skills/location-service/scripts/geocode_reverse.py"
        address_out, address_err = run_script(script_path, [str(lat), str(lon)])
        if address_err:
            print(f"Error reverse geocoding: {address_err}", file=sys.stderr)
            sys.exit(1)

        print(address_out)

    # ── Address string (forward geocoding) ───────────────────────────────────
    else:
        script_path = "/home/ubuntu/.openclaw/workspace/skills/location-service/scripts/geocode_forward.py"
        coords_out, coords_err = run_script(script_path, [input_text])
        if coords_err:
            print(f"Error geocoding address: {coords_err}", file=sys.stderr)
            sys.exit(1)

        if coords_out:
            print(coords_out)
        else:
            print("Error: No coordinates returned", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
