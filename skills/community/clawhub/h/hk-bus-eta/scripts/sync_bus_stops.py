#!/usr/bin/env python3
"""
Hong Kong Bus Stops Sync Script
Version: 1.0.2

Created: 2026-03-13
- Syncs TD JSON data
- Pre-builds CTB coordinate cache (FULL CACHE)
- Data Dictionary compliant (stopPickDrop, routeSeq)

Updated: 2026-03-14 (v1.0.2)
- Full CTB cache: all routes, all stops (no more limits)
- Increased parallelism for faster sync
"""
import json, sqlite3, os, time, concurrent.futures
from urllib.request import urlopen, Request
from datetime import datetime, timezone, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bus_stops.db")
CTB_CACHE = os.path.join(BASE_DIR, "ctb_stops.json")
JSON_URL = "https://static.data.gov.hk/td/routes-fares-geojson/JSON_BUS.json"

def fetch(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urlopen(req, timeout=120) as r: return json.loads(r.read().decode('utf-8-sig'))
    except: return None

def build_ctb_cache(log=print):
    """Pre-build FULL CTB stop coordinate cache by calling CTB route-stop API."""
    log(f"[{datetime.now().strftime('%H:%M:%S')}] Building FULL CTB stop cache...")
    
    # Get all CTB routes from DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT DISTINCT route FROM routes WHERE company = 'CTB'")
    ctb_routes = [r[0] for r in c.fetchall()]
    conn.close()
    
    log(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(ctb_routes)} CTB routes")
    
    ctb_stops = {}
    seen_stop_ids = set()
    
    def fetch_route_stops(route):
        """Fetch stop IDs for a route (both directions)."""
        stops = []
        for direction in ['outbound', 'inbound']:
            url = f"https://rt.data.gov.hk/v2/transport/citybus/route-stop/CTB/{route}/{direction}"
            res = fetch(url)
            if res and 'data' in res:
                for s in res['data']:
                    stops.append(s.get('stop'))
        return stops
    
    def fetch_stop_info(stop_id):
        """Fetch stop coordinates."""
        url = f"https://rt.data.gov.hk/v2/transport/citybus/stop/{stop_id}"
        res = fetch(url)
        if res and 'data' in res:
            d = res['data']
            lat, lon = float(d.get('lat', 0)), float(d.get('long', 0))
            if lat and lon:
                return stop_id, lat, lon, d.get('name_en', '')
        return None
    
    # Process ALL routes in parallel (no limit)
    log(f"[{datetime.now().strftime('%H:%M:%S')}] Fetching route-stop mappings...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        route_results = list(executor.map(fetch_route_stops, ctb_routes))
    
    # Collect all unique stop IDs
    for stops in route_results:
        for sid in stops:
            if sid and sid not in seen_stop_ids:
                seen_stop_ids.add(sid)
    
    all_stop_ids = list(seen_stop_ids)
    log(f"[{datetime.now().strftime('%H:%M:%S')}] Found {len(all_stop_ids)} unique CTB stops, fetching coordinates...")
    
    # Fetch ALL stop info in parallel (no limit)
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        stop_infos = list(executor.map(fetch_stop_info, all_stop_ids))
    
    for info in stop_infos:
        if info:
            sid, lat, lon, name = info
            ctb_stops[sid] = {'lat': lat, 'lon': lon, 'name_en': name}
    
    # Save cache
    json.dump({'ts': time.time(), 'stops': ctb_stops}, open(CTB_CACHE, 'w'))
    log(f"[{datetime.now().strftime('%H:%M:%S')}] CTB cache built: {len(ctb_stops)} stops")

def sync(log=print):
    log(f"[{datetime.now().strftime('%H:%M:%S')}] Downloading JSON_BUS.json...")
    data = fetch(JSON_URL)
    if not data: log("Error downloading"); return
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.executescript('''
        DROP TABLE IF EXISTS routes;
        DROP TABLE IF EXISTS stops;
        DROP TABLE IF EXISTS stop_names;
        CREATE TABLE routes (
            id INTEGER PRIMARY KEY, company TEXT, route TEXT, route_dir INTEGER,
            orig_tc TEXT, orig_en TEXT, dest_tc TEXT, dest_en TEXT
        );
        CREATE TABLE stops (
            stop_id INTEGER, stop_seq INTEGER, route_id INTEGER,
            name_tc TEXT, name_en TEXT, lat REAL, lon REAL, 
            pick_drop INTEGER, fare REAL
        );
        CREATE TABLE stop_names (
            name TEXT, stop_id INTEGER, company TEXT, route TEXT,
            PRIMARY KEY (name, stop_id, company, route)
        );
    ''')
    
    features = data.get('features', [])
    log(f"[{datetime.now().strftime('%H:%M:%S')}] Processing {len(features)} features...")
    
    route_map = {}
    for f in features:
        p = f.get('properties', {})
        if p.get('routeType') != 1: continue
        
        comp, rt, d = p.get('companyCode'), str(p.get('routeNameE')), p.get('routeSeq')
        rk = (comp, rt, d)
        if rk not in route_map:
            c.execute('INSERT INTO routes (company, route, route_dir, orig_tc, orig_en, dest_tc, dest_en) VALUES (?,?,?,?,?,?,?)',
                     (comp, rt, d, p.get('locStartNameC'), p.get('locStartNameE'), p.get('locEndNameC'), p.get('locEndNameE')))
            route_map[rk] = c.lastrowid
        
        coords = f.get('geometry', {}).get('coordinates', [0,0])
        c.execute('INSERT INTO stops VALUES (?,?,?,?,?,?,?,?,?)',
                 (p.get('stopId'), p.get('stopSeq'), route_map[rk], p.get('stopNameC'), p.get('stopNameE'), coords[1], coords[0], p.get('stopPickDrop'), p.get('fullFare')))
    
    c.execute('INSERT OR IGNORE INTO stop_names SELECT DISTINCT LOWER(name_tc), stop_id, company, route FROM stops s JOIN routes r ON s.route_id=r.id')
    c.execute('INSERT OR IGNORE INTO stop_names SELECT DISTINCT LOWER(name_en), stop_id, company, route FROM stops s JOIN routes r ON s.route_id=r.id')
    c.execute('CREATE INDEX idx_rt_num ON routes(route)')
    c.execute('CREATE INDEX idx_st_name ON stop_names(name)')
    
    conn.commit()
    conn.close()
    log(f"[{datetime.now().strftime('%H:%M:%S')}] DB sync complete: {os.path.getsize(DB_PATH)/1024/1024:.2f} MB")
    
    # Build CTB cache
    build_ctb_cache(log=log)

if __name__ == "__main__": sync()