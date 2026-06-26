#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = [
#     "polars>=1.0.0",
#     "duckdb>=1.0.0",
#     "pyobjc-framework-Cocoa>=10.0",
# ]
# ///
import urllib.request
import urllib.parse
import json
import os
import random
from datetime import datetime
from pathlib import Path
import importlib.util

# Load change.py for set_wallpaper_all_displays
script_dir = Path(__file__).parent
spec = importlib.util.spec_from_file_location("change_wallpaper", script_dir / "change.py")
change_wallpaper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(change_wallpaper)

# 1. Read Preferences
prefs_file = Path.home() / ".wallpaper_prefs.json"
query = "nature"
if prefs_file.exists():
    try:
        with open(prefs_file, "r") as f:
            prefs = json.load(f)
            query = prefs.get("query", "nature")
    except Exception as e:
        print(f"Error reading prefs: {e}")

# 2. Search Unsplash using NAPI
print(f"Searching Unsplash for: {query}")
encoded_query = urllib.parse.quote(query)
search_url = f"https://unsplash.com/napi/search/photos?query={encoded_query}&per_page=15"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
try:
    req = urllib.request.Request(search_url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read())
        
    results = [r for r in data.get('results', []) if not r.get('premium', False)]
    if not results:
        print("No free results found. Falling back to Bing.")
        bing_url = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
        bing_req = urllib.request.Request(bing_url, headers=headers)
        with urllib.request.urlopen(bing_req, timeout=10) as response:
            bing_data = json.loads(response.read())
            image_url = "https://www.bing.com" + bing_data['images'][0]['url']
    else:
        # Pick a random image from top results to keep it fresh everyday
        selected = random.choice(results[:10])
        image_url = selected['urls']['raw'] + "&q=85&w=3840&h=2160&fit=crop"
        
except Exception as e:
    print(f"Error fetching image: {e}")
    exit(1)

# 3. Download and Set
today = datetime.now().strftime("%Y-%m-%d")
base_dir = Path.home() / "wallpaper-daily" / today
base_dir.mkdir(parents=True, exist_ok=True)
wallpaper_path = base_dir / f"auto-{datetime.now().strftime('%H%M%S')}.jpg"

print(f"Downloading {image_url}...")
try:
    req = urllib.request.Request(image_url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as response, open(wallpaper_path, 'wb') as out_file:
        out_file.write(response.read())
        
    # Set Wallpaper
    change_wallpaper.set_wallpaper_all_displays(wallpaper_path)
    print("Wallpaper updated successfully!")
except Exception as e:
    print(f"Failed to download/set: {e}")
