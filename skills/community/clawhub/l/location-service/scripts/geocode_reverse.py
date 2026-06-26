#!/usr/bin/env python3
"""
Reverse geocoding: Convert coordinates to address using Nominatim (OpenStreetMap)
"""

import sys
import requests
import json

def reverse_geocode(lat, lon):
    """Convert latitude/longitude to address using Nominatim"""
    url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'format': 'json',
        'lat': lat,
        'lon': lon,
        'zoom': 18,
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'OpenClaw-Location-Service/1.0'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if 'display_name' in data:
            return data['display_name']
        else:
            return "Address not found"
            
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    except json.JSONDecodeError:
        return "Error: Invalid response from geocoding service"

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 geocode_reverse.py <latitude> <longitude>")
        sys.exit(1)
    
    try:
        lat = float(sys.argv[1])
        lon = float(sys.argv[2])
        
        # Validate coordinates
        if not (-90 <= lat <= 90):
            print("Error: Latitude must be between -90 and 90")
            sys.exit(1)
        if not (-180 <= lon <= 180):
            print("Error: Longitude must be between -180 and 180")
            sys.exit(1)
            
        address = reverse_geocode(lat, lon)
        print(address)
        
    except ValueError:
        print("Error: Latitude and longitude must be valid numbers")
        sys.exit(1)

if __name__ == "__main__":
    main()