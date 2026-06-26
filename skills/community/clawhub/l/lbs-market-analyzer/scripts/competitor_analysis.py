import os
from dotenv import load_dotenv
import requests
import json
import argparse

"""
Competitor Analysis Script for geo-competitor-insight skill.
Uses AMAP (Gaode) LBS API to fetch POI data.
"""

class CompetitorAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://restapi.amap.com/v3"

    def geocode(self, address):
        """Converts human-readable address to coordinates."""
        endpoint = f"{self.base_url}/geocode/geo"
        params = {"key": self.api_key, "address": address}
        try:
            response = requests.get(endpoint, params=params)
            data = response.json()
            if data['status'] == '1' and data['geocodes']:
                return data['geocodes'][0]['location']
        except Exception as e:
            return None
        return None

    def search_nearby(self, location, keywords, radius=3000):
        """Fetches POIs around a specific location."""
        endpoint = f"{self.base_url}/place/around"
        params = {
            "key": self.api_key,
            "location": location,
            "keywords": keywords,
            "radius": radius,
            "sortrule": "distance",
            "offset": 25,
            "page": 1
        }
        try:
            response = requests.get(endpoint, params=params)
            return response.json()
        except Exception as e:
            return {"status": "0", "info": str(e)}

    def run_analysis(self, address, keywords, radius=3000):
        """Workflow: Geocode -> Search -> Format."""
        coords = self.geocode(address)
        if not coords:
            return {"error": f"Address not found: {address}"}
        
        raw_data = self.search_nearby(coords, keywords, radius)
        if raw_data.get('status') != '1':
            return {"error": "AMAP API failure", "details": raw_data}
        
        pois = raw_data.get('pois', [])
        return {
            "center": address,
            "coords": coords,
            "keyword": keywords,
            "radius_m": radius,
            "count": len(pois),
            "results": [
                {
                    "name": p['name'],
                    "distance_m": p['distance'],
                    "address": p['address'],
                    "type": p['type'],
                    "rating": p.get('biz_ext', {}).get('rating', 'N/A')
                } for p in pois
            ]
        }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", required=True)
    parser.add_argument("--keywords", required=True)
    parser.add_argument("--radius", type=int, default=3000)
    args = parser.parse_args()

    # Load variables from .env file
    # Get the directory of the current script, then go up one level to the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    dotenv_path = os.path.join(project_root, ".env")
    load_dotenv(dotenv_path)

    key = os.getenv("AMAP_KEY")
    if not key:
        print(json.dumps({"error": f"Missing AMAP_KEY. Looked in {dotenv_path}"}))
    else:
        analyzer = CompetitorAnalyzer(key)
        output = analyzer.run_analysis(args.address, args.keywords, args.radius)
        print(json.dumps(output, indent=2, ensure_ascii=False))
