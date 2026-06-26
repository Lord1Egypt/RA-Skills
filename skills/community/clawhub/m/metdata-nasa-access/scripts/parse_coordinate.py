#!/usr/bin/env python3
"""
Coordinate parser for MetaData-NASA-Access.
Handles various coordinate input formats and converts to standard lat/lon.
"""

import re
import sys
import json
import urllib.request
import urllib.error
import urllib.parse


def parse_coordinate_input(location_input):
    """
    Parse location input and return (lat, lon).
    
    Supported formats:
    - "上海市闵行区申虹路虹桥天地3号楼" (location name)
    - "31.1932, 121.3111" (direct coordinates)
    - "东半球30°，南半球60°" (hemisphere + degrees)
    - "东经120°，北纬30°" (direction + longitude/latitude)
    """
    location_input = location_input.strip()
    
    # Check if it's a direct coordinate format
    coord_pattern = r'^(-?\d+\.?\d*)\s*[,\s]\s*(-?\d+\.?\d*)$'
    match = re.match(coord_pattern, location_input)
    if match:
        lat = float(match.group(1))
        lon = float(match.group(2))
        return lat, lon
    
    # Check for hemisphere format: "东半球30°，南半球60°"
    hemisphere_pattern = r'([东西南北半球]+)\s*(\d+\.?\d*)\s*[°度]?\s*[，,]?\s*([东西南北半球]+)\s*(\d+\.?\d*)\s*[°度]?'
    match = re.search(hemisphere_pattern, location_input)
    if match:
        lat, lon = parse_hemisphere(match.group(1), match.group(2), match.group(3), match.group(4))
        return lat, lon
    
    # Check for direction format: "东经120°，北纬30°"
    direction_pattern = r'([东西南北]+)\s*(经|纬)\s*(\d+\.?\d*)\s*[°度]?\s*[，,]?\s*([东西南北]+)\s*(经|纬)\s*(\d+\.?\d*)\s*[°度]?'
    match = re.search(direction_pattern, location_input)
    if match:
        lat, lon = parse_direction(match.group(1), match.group(2), match.group(3), 
                                   match.group(4), match.group(5), match.group(6))
        return lat, lon
    
    # Otherwise, treat as location name and geocode
    return geocode_location(location_input)


def parse_hemisphere(hemi1, deg1, hemi2, deg2):
    """Parse hemisphere format: 东半球30°，南半球60°"""
    deg1 = float(deg1)
    deg2 = float(deg2)
    
    # Determine which is latitude and which is longitude
    # Latitude: 北半球/南半球
    # Longitude: 东半球/西半球
    
    lat = None
    lon = None
    
    if '北' in hemi1 or '南' in hemi1:
        lat = deg1 if '北' in hemi1 else -deg1
        lon = deg2 if '东' in hemi2 else -deg2
    elif '东' in hemi1 or '西' in hemi1:
        lon = deg1 if '东' in hemi1 else -deg1
        lat = deg2 if '北' in hemi2 else -deg2
    
    return lat, lon


def parse_direction(dir1, type1, deg1, dir2, type2, deg2):
    """Parse direction format: 东经120°，北纬30°"""
    deg1 = float(deg1)
    deg2 = float(deg2)
    
    lat = None
    lon = None
    
    if '纬' in type1:
        lat = deg1 if '北' in dir1 else -deg1
        lon = deg2 if '东' in dir2 else -deg2
    elif '经' in type1:
        lon = deg1 if '东' in dir1 else -deg1
        lat = deg2 if '北' in dir2 else -deg2
    
    return lat, lon


def geocode_location(location_name):
    """Geocode location name using Nominatim API."""
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(location_name)}&format=json&limit=1"
    
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "MetaData-NASA-Access/1.0")
    
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        if not data:
            print(f"Error: Location '{location_name}' not found", file=sys.stderr)
            return None, None
        
        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])
        return lat, lon
    except Exception as e:
        print(f"Error geocoding location: {e}", file=sys.stderr)
        return None, None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 parse_coordinate.py <location_input>")
        print("Examples:")
        print('  python3 parse_coordinate.py "上海市闵行区申虹路虹桥天地3号楼"')
        print('  python3 parse_coordinate.py "31.1932, 121.3111"')
        print('  python3 parse_coordinate.py "东半球30°，南半球60°"')
        print('  python3 parse_coordinate.py "东经120°，北纬30°"')
        sys.exit(1)
    
    location_input = sys.argv[1]
    lat, lon = parse_coordinate_input(location_input)
    
    if lat is not None and lon is not None:
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
    else:
        print("Failed to parse coordinates", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
