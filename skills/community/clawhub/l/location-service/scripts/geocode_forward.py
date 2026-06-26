#!/usr/bin/env python3
"""
Forward geocoding: Convert address to coordinates using Nominatim (OpenStreetMap)
"""

import sys
import requests
import json
from urllib.parse import quote

def forward_geocode(address):
    """Convert address to latitude/longitude using Nominatim"""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'format': 'json',
        'q': address,
        'limit': 1
    }
    headers = {
        'User-Agent': 'OpenClaw-Location-Service/1.0'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            result = data[0]
            lat = float(result['lat'])
            lon = float(result['lon'])
            display_name = result.get('display_name', 'Unknown location')
            return lat, lon, display_name
        else:
            return None, None, "Location not found"
            
    except requests.exceptions.RequestException as e:
        return None, None, f"Error: {str(e)}"
    except json.JSONDecodeError:
        return None, None, "Error: Invalid response from geocoding service"
    except ValueError:
        return None, None, "Error: Invalid coordinate data received"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 geocode_forward.py <address>")
        sys.exit(1)
    
    address = ' '.join(sys.argv[1:])
    lat, lon, result = forward_geocode(address)
    
    if lat is not None and lon is not None:
        print(f"{lat},{lon}")
        # Also print the display name for reference
        print(f"# {result}", file=sys.stderr)
    else:
        print(result, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()