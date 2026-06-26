#!/usr/bin/env python3
"""
Calculate distance between two geographic points using the Haversine formula
"""

import sys
import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    
    return c * r

def main():
    if len(sys.argv) != 5:
        print("Usage: python3 distance_calc.py <lat1> <lon1> <lat2> <lon2>")
        sys.exit(1)
    
    try:
        lat1 = float(sys.argv[1])
        lon1 = float(sys.argv[2])
        lat2 = float(sys.argv[3])
        lon2 = float(sys.argv[4])
        
        # Validate coordinates
        for lat, lon in [(lat1, lon1), (lat2, lon2)]:
            if not (-90 <= lat <= 90):
                print("Error: Latitude must be between -90 and 90")
                sys.exit(1)
            if not (-180 <= lon <= 180):
                print("Error: Longitude must be between -180 and 180")
                sys.exit(1)
        
        distance_km = haversine(lat1, lon1, lat2, lon2)
        distance_mi = distance_km * 0.621371
        
        print(f"{distance_km:.2f} km ({distance_mi:.2f} mi)")
        
    except ValueError:
        print("Error: All arguments must be valid numbers")
        sys.exit(1)

if __name__ == "__main__":
    main()