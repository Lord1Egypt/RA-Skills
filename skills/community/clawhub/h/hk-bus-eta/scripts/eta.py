"""
Hong Kong Bus ETA Query Script
Version: 1.0.2
Created: 2026-03-13 (with "Mr. Usagi - Tom's Agent")

Changelog:
- 2026-03-14 (v1.0.2): Added bounded latency budgets (~5s), timeout-aware stop matching retries, and deterministic no-result fallback messages.
- 2026-03-14 (v1.0.2): Parallel API fetching with ThreadPoolExecutor, cache-first KMB stops, improved CTB cache strategy.
- 2026-03-13 (v1.0.0): First stable release. Supports KMB/CTB/LWB with smart location association, coordinate clustering, destination fuzzy merge, terminus marking, circular route handling, and auto background sync.
- 30s Golden Rule timeout enforced.
"""
import json, os, time, math, sqlite3, subprocess, sys, re
from urllib.request import urlopen, Request
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeout

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "bus_stops.db")
KMB_CACHE = os.path.join(BASE_DIR, "kmb_stops.json")
CTB_CACHE = os.path.join(BASE_DIR, "ctb_stops.json")

# Performance budgets (target: response within ~5s)
TOTAL_BUDGET_SEC = 4.8
MATCH_TIMEOUT_SEC = 1.0
RETRY_MATCH_TIMEOUT_SEC = 0.8
ETA_FETCH_TIMEOUT_SEC = 3.0

def get_dist(lat1, lon1, lat2, lon2):
    try: return 6371*2*math.asin(math.sqrt(math.sin(math.radians(lat2-lat1)/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(math.radians(lon2-lon1)/2)**2))
    except: return 9999

def fetch(url):
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        # tighter timeout to keep total query latency bounded
        with urlopen(req, timeout=2.2) as r: return json.loads(r.read().decode())
    except: return None

def cleanup_name(n): return (n or "").replace("<br>"," ").replace("<br/>"," ").strip()

def format_eta(e):
    try:
        t = datetime.fromisoformat(e.replace("Z","+00:00"))
        d = int((t - datetime.now(timezone(timedelta(hours=8)))).total_seconds()/60)
        return {"str": t.strftime('%H:%M'), "min": max(0,d), "ts": t.timestamp()}
    except: return None

def load_cache(path): 
    try: return json.load(open(path)).get('stops', {}) if os.path.exists(path) else {}
    except: return {}

def save_cache(path, data): 
    try: json.dump({'ts': time.time(), 'stops': data}, open(path,'w'))
    except: pass

def get_kmb_stops():
    """Cache-first strategy: use cached data if fresh, background refresh if stale."""
    d = load_cache(KMB_CACHE)
    cache_ts = d.pop('_ts', 0) if isinstance(d, dict) and '_ts' in d else 0
    cache_age = time.time() - cache_ts if cache_ts else float('inf')
    
    # Use cache if fresh (< 1 hour)
    if d and cache_age < 3600:
        return d
    
    # Try to refresh, but return cache if fetch fails
    r = fetch("https://data.etabus.gov.hk/v1/transport/kmb/stop")
    if r and 'data' in r:
        s = {st['stop']: st for st in r['data']}
        s['_ts'] = time.time()
        save_cache(KMB_CACHE, s)
        return s
    return d or {}

def get_ctb_route_stops_realtime(route, direction):
    url = f"https://rt.data.gov.hk/v2/transport/citybus/route-stop/CTB/{route}/{direction}"
    rs = fetch(url)
    if not rs or 'data' not in rs: return {}
    route_stops = {}
    ctb_cache = load_cache(CTB_CACHE)
    for s in rs['data']:
        stop_id = s.get('stop')
        if stop_id in ctb_cache: route_stops[stop_id] = ctb_cache[stop_id]
        else:
            info = fetch(f"https://rt.data.gov.hk/v2/transport/citybus/stop/{stop_id}")
            if info and 'data' in info:
                d = info['data']
                lat, lon = float(d.get('lat', 0)), float(d.get('long', 0))
                name = d.get('name_en', '')
                if lat and lon:
                    route_stops[stop_id] = {'lat': lat, 'lon': lon, 'name_en': name}
                    ctb_cache[stop_id] = route_stops[stop_id]
    save_cache(CTB_CACHE, ctb_cache); return route_stops

def fetch_missing_ctb_stops(stop_ids, ctb_cache, max_workers=10):
    """Fetch missing CTB stop coordinates in parallel and update cache."""
    missing = [sid for sid in stop_ids if sid not in ctb_cache]
    if not missing:
        return ctb_cache
    
    def fetch_stop(stop_id):
        url = f"https://rt.data.gov.hk/v2/transport/citybus/stop/{stop_id}"
        res = fetch(url)
        if res and 'data' in res:
            d = res['data']
            lat, lon = float(d.get('lat', 0)), float(d.get('long', 0))
            if lat and lon:
                return stop_id, {'lat': lat, 'lon': lon, 'name_en': d.get('name_en', '')}
        return None
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(fetch_stop, missing[:50]))  # Limit to 50 at a time
    
    for r in results:
        if r:
            stop_id, info = r
            ctb_cache[stop_id] = info
    
    save_cache(CTB_CACHE, ctb_cache)
    return ctb_cache

def find_stops(route, pattern, lang="tc"):
    if not os.path.exists(DB_PATH): return []
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT s.stop_id,s.name_tc,s.name_en,s.lat,s.lon,s.pick_drop,r.company,r.route_dir FROM stops s JOIN routes r ON s.route_id=r.id WHERE r.route=?', (route,))
    p = pattern.lower()
    rows = []
    for r in c.fetchall():
        tc, en = cleanup_name(r[1]), cleanup_name(r[2])
        if p in tc.lower() or p in en.lower():
            rows.append({'id':r[0],'name_tc':tc, 'name_en':en, 'lat':r[3],'lon':r[4],'pick_drop':r[5],'company':r[6],'dir':['outbound','inbound'][r[7]-1]})
    conn.close()
    return rows

def normalize_pattern(s):
    s = (s or "").strip().lower()
    # remove common stop suffix/prefix noise for faster fuzzy retries
    noise = [
        "巴士轉乘站", "轉車站", "收費廣場", "巴士總站", "總站", "巴士站", "車站", "站",
        "bus interchange", "interchange", "toll plaza", "bus terminus", "terminus", "station", "stop"
    ]
    for n in noise:
        s = s.replace(n, "")
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def find_stops_with_timeout(route, pattern, lang="tc", timeout_sec=MATCH_TIMEOUT_SEC):
    with ThreadPoolExecutor(max_workers=1) as ex:
        fut = ex.submit(find_stops, route, pattern, lang)
        try:
            return fut.result(timeout=timeout_sec)
        except FuturesTimeout:
            return []
        except:
            return []

# English translations
EN_TRANS = {
    "九巴(KMB)": "KMB",
    "城巴(CTB)": "CTB",
    "龍運(LWB)": "LWB",
    "九巴(KMB)/城巴(CTB) 聯營": "KMB/CTB Joint",
    "終點站": "Terminus",
    "循環線": "Circular",
    "往": "To",
    "地圖": "Map",
    "分鐘": "min",
}

def fetch_parallel(urls_with_keys, max_workers=10, timeout_sec=None):
    """Fetch multiple URLs in parallel, returning dict of key -> result."""
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(fetch, url): key for key, url in urls_with_keys.items()}
        try:
            iterator = as_completed(futures, timeout=timeout_sec)
            for future in iterator:
                key = futures[future]
                try:
                    results[key] = future.result()
                except:
                    results[key] = None
        except FuturesTimeout:
            # leave unfinished futures as None
            pass

        # fill missing keys as None
        for f, key in futures.items():
            if key not in results:
                results[key] = None
    return results

def main(route, pattern, lang="tc"):
    start_t = time.time()
    output = [] 
    
    if not os.path.exists(DB_PATH):
        if lang == 'en':
            output.append("🔄 First run, initializing database...")
            output.append("(About 15-20 seconds)")
        else:
            output.append("🔄 首次使用，正在初始化數據庫，請稍後......")
            output.append("（約需 15-20 秒）")
        output.append("")
        import sync_bus_stops
        sync_bus_stops.sync(log=output.append)
        output.append("")
        if lang == 'en':
            output.append("✅ Database initialized!")
        else:
            output.append("✅ 數據庫初始化完成！")
        output.append("")
    
    needs_bg_sync = False
    if os.path.exists(DB_PATH):
        file_age = time.time() - os.path.getmtime(DB_PATH)
        if file_age > 7 * 86400:
            needs_bg_sync = True
            if lang == 'en':
                output.append("🔄 Database outdated (>7 days), updating in background...")
            else:
                output.append("🔄 數據庫已超過 7 天，正在背景更新......")
            output.append("")
    
    # fast-path stop matching with timeout
    stops = find_stops_with_timeout(route, pattern, lang, MATCH_TIMEOUT_SEC)
    if not stops:
        # retry with normalized (shortened) keyword
        norm = normalize_pattern(pattern)
        if norm and norm != pattern.lower():
            stops = find_stops_with_timeout(route, norm, lang, RETRY_MATCH_TIMEOUT_SEC)

    if not stops:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT lat, lon FROM stops WHERE name_tc LIKE ? OR name_en LIKE ? LIMIT 20', (f'%{pattern}%', f'%{pattern}%'))
        locs = c.fetchall()
        if locs:
            alat, alon = sum(l[0] for l in locs)/len(locs), sum(l[1] for l in locs)/len(locs)
            c.execute('SELECT s.stop_id,s.name_tc,s.name_en,s.lat,s.lon,s.pick_drop,r.company,r.route_dir FROM stops s JOIN routes r ON s.route_id=r.id WHERE r.route=?', (route,))
            for r in c.fetchall():
                if get_dist(r[3], r[4], alat, alon) < 0.3:
                    stops.append({'id':r[0],'name_tc':cleanup_name(r[1]), 'name_en':cleanup_name(r[2]),'lat':r[3],'lon':r[4],'pick_drop':r[5],'company':r[6],'dir':['outbound','inbound'][r[7]-1]})
        if not stops:
            # no-result fallback (avoid empty response)
            if lang == 'en':
                print("Service hours have passed / No route information found")
            else:
                print("尾班車已過或未有班次資料")
            return
        conn.close()

    # Pre-detect circular route
    is_circular = False
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT dest_tc, dest_en FROM routes WHERE route=?', (route,))
        rows = c.fetchall()
        # Check for circular route in both Chinese and English
        is_circular = any('循環線' in r[0] or 'CIRCULAR' in str(r[1]).upper() for r in rows)
        conn.close()

    kmb_stops_all = get_kmb_stops()
    
    # === Phase1: Collect all API endpoints to fetch ===
    api_urls = {}  # key -> url
    
    # KMB route-stop mappings
    for d in ['outbound', 'inbound']:
        api_urls[('kmb_route_stop', d)] = f"https://data.etabus.gov.hk/v1/transport/kmb/route-stop/{route}/{d}/1"
    
    # CTB route-stop mappings (need to fetch stop coordinates)
    for d in ['outbound', 'inbound']:
        api_urls[('ctb_route_stop', d)] = f"https://rt.data.gov.hk/v2/transport/citybus/route-stop/CTB/{route}/{d}"
    
    # === Phase 2: Fetch all route-stop data in parallel ===
    route_data = fetch_parallel(api_urls, max_workers=6, timeout_sec=ETA_FETCH_TIMEOUT_SEC)
    
    # === Phase 3: Identify matching stops and collect ETA endpoints ===
    eta_urls = {}
    stop_info = {}  # (op, stop_id, direction) -> matching stop data
    ctb_cache = load_cache(CTB_CACHE)
    
    # Process KMB route-stop results
    for d in ['outbound', 'inbound']:
        rs = route_data.get(('kmb_route_stop', d))
        if rs and 'data' in rs:
            for rs_item in rs['data']:
                sid = rs_item['stop']
                info = kmb_stops_all.get(sid, {})
                alat, alon = float(info.get('lat', 999)), float(info.get('long', 999))
                if alat < 900:
                    for s in stops:
                        if s['dir'] == d and get_dist(s['lat'], s['lon'], alat, alon) < 0.15:
                            key = ('kmb_eta', sid, d)
                            eta_urls[key] = f"https://data.etabus.gov.hk/v1/transport/kmb/eta/{sid}/{route}/1"
                            stop_info[('kmb', sid, d)] = {'stop': s, 'alat': alat, 'alon': alon}
                            break
    
    # Process CTB route-stop results (also update cache)
    # First, collect all CTB stop IDs and fetch missing ones in parallel
    all_ctb_stop_ids = set()
    for d in ['outbound', 'inbound']:
        rs = route_data.get(('ctb_route_stop', d))
        if rs and 'data' in rs:
            for s_item in rs['data']:
                all_ctb_stop_ids.add(s_item.get('stop'))
    
    # Fetch missing CTB stop coordinates in parallel
    ctb_cache = fetch_missing_ctb_stops(all_ctb_stop_ids, ctb_cache, max_workers=10)
    
    # Now match stops with cached coordinates
    for d in ['outbound', 'inbound']:
        rs = route_data.get(('ctb_route_stop', d))
        if rs and 'data' in rs:
            for s_item in rs['data']:
                stop_id = s_item.get('stop')
                if stop_id in ctb_cache:
                    info = ctb_cache[stop_id]
                    alat, alon = info['lat'], info['lon']
                    for s in stops:
                        if s['dir'] == d and get_dist(s['lat'], s['lon'], alat, alon) < 0.15:
                            key = ('ctb_eta', stop_id, d)
                            eta_urls[key] = f"https://rt.data.gov.hk/v2/transport/citybus/eta/CTB/{stop_id}/{route}"
                            stop_info[('ctb', stop_id, d)] = {'stop': s, 'alat': alat, 'alon': alon}
                            break
    
    # === Phase 4: Fetch all ETAs in parallel ===
    eta_data = fetch_parallel(eta_urls, max_workers=10, timeout_sec=ETA_FETCH_TIMEOUT_SEC)
    
    # === Phase 5: Process results ===
    results = {}
    
    for key, eta_res in eta_data.items():
        if not eta_res or 'data' not in eta_res:
            continue
        
        op, sid, d = key[0].replace('_eta', ''), key[1], key[2]
        info_key = (op, sid, d)
        if info_key not in stop_info:
            continue
        
        s = stop_info[info_key]['stop']
        
        # Find or create cluster
        cluster_id = None
        for ck in results:
            clat, clon = map(float, ck.split(','))
            if get_dist(clat, clon, s['lat'], s['lon']) < 0.05:
                cluster_id = ck
                break
        if not cluster_id:
            cluster_id = f"{s['lat']},{s['lon']}"
            results[cluster_id] = {'names_tc': set([s['name_tc']]), 'names_en': set([s['name_en']]), 'lat': s['lat'], 'lon': s['lon'], 'etas': {}, 'ops': set(), 'comp': s['company']}
        results[cluster_id]['names_tc'].add(s['name_tc'])
        results[cluster_id]['names_en'].add(s['name_en'])
        results[cluster_id]['ops'].add(op)
        
        for e in eta_res['data']:
            if e.get('dir') != ('O' if d == 'outbound' else 'I'):
                continue
            f = format_eta(e.get('eta'))
            if f:
                e_seq = e.get('seq', 0)

                # Circular-route guard:
                # at origin-like stop (pick_drop=1), keep ONLY seq=1 departure ETAs;
                # this prevents destination/terminus ETAs from mixing in.
                if is_circular and s['pick_drop'] == 1 and str(e_seq) != '1':
                    continue

                dest = e.get('dest_tc' if lang == 'tc' else 'dest_en')
                if dest not in results[cluster_id]['etas']:
                    results[cluster_id]['etas'][dest] = {'data': [], 'is_terminus': False}
                if s['pick_drop'] == 1:
                    results[cluster_id]['etas'][dest]['is_terminus'] = True
                e_pd = s['pick_drop']

                # De-dup by time+seq (not just time), avoids dropping valid seq=1 records.
                if not any(x['str'] == f['str'] and str(x.get('seq', '')) == str(e_seq) for x in results[cluster_id]['etas'][dest]['data']):
                    results[cluster_id]['etas'][dest]['data'].append({**f, 'op': op, 'pick_drop': e_pd, 'seq': e_seq})
    
    # === Phase 6: Format output ===
    for r in results.values():
        # Check if this stop has any non-terminus routes (boarding routes)
        has_boarding = any(not obj['is_terminus'] and obj['data'] for obj in r['etas'].values())
        if not has_boarding:
            continue  # Skip stops that only have terminus routes
        
        c_name = r.get('comp', '')
        if lang == 'en':
            s_names = sorted(list(r.get('names_en', set())))
            p = "KMB/CTB Joint" if len(r['ops'])>1 else ("LWB" if "LWB" in c_name else ("KMB" if "kmb" in r['ops'] else "CTB"))
            header = " / ".join(s_names)
            map_label = "Map"
        else:
            s_names = sorted(list(r.get('names_tc', set())))
            p = "九巴(KMB)/城巴(CTB) 聯營" if len(r['ops'])>1 else ("龍運(LWB)" if "LWB" in c_name else ("九巴(KMB)" if "kmb" in r['ops'] else "城巴(CTB)"))
            header = " / ".join(s_names)
            map_label = "地圖"
        output.append(f"🚌 **{p} {route}** @ {header} [📍{map_label}](https://www.google.com/maps?q={r['lat']},{r['lon']})")
        
        # Get origin name for circular routes
        orig_name = ""
        if is_circular and os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            if lang == 'en':
                c.execute('SELECT DISTINCT orig_en FROM routes WHERE route=?', (route,))
            else:
                c.execute('SELECT DISTINCT orig_tc FROM routes WHERE route=?', (route,))
            row = c.fetchone()
            if row: orig_name = row[0]
            conn.close()

        merged = {}
        for dest, obj in r['etas'].items():
            if not obj['data']: continue
            key = dest.replace('(','').replace(')','').replace(' ','')[:3]
            if key not in merged: merged[key] = {'name':dest, 'data':[], 'is_terminus':False}
            merged[key]['data'].extend(obj['data'])
            if len(dest) < len(merged[key]['name']): merged[key]['name'] = dest
            if obj['is_terminus']: merged[key]['is_terminus'] = True
        
        for key, obj in merged.items():
            if is_circular:
                # For circular routes:
                # - At origin stop: filter to show only departures (seq=1)
                # - At intermediate stops: show all ETAs
                departures = [e for e in obj['data'] if str(e.get('seq', '')) == '1']
                # If no seq=1 ETAs, this is an intermediate stop - show all
                if not departures:
                    departures = obj['data']
                
                if departures:
                    times = []
                    for e in sorted(departures, key=lambda x:x['ts'])[:3]:
                        t_val = f"{e['str']} ({e['min']} min)"
                        if len(r['ops'])>1: t_val += f" [{e['op'].upper()}]"
                        times.append(t_val)
                    import re
                    # Remove circular suffix from destination name
                    dest_clean = re.sub(r'\s*\(循環線\)\s*$', '', obj['name'])
                    dest_clean = re.sub(r'\s*\(CIRCULAR\)\s*$', '', dest_clean, flags=re.IGNORECASE)
                    dest_clean = dest_clean.strip()
                    if lang == 'en':
                        output.append(f"• From {orig_name} to {dest_clean} (Circular): " + ", ".join(times))
                    else:
                        output.append(f"• {orig_name} 往 {dest_clean}(循環線): " + ", ".join(times))
            else:
                # Non-circular routes: hide terminus ETAs by default
                if obj['is_terminus']:
                    continue
                times = []
                for e in sorted(obj['data'], key=lambda x:x['ts'])[:3]:
                    t_val = f"{e['str']} ({e['min']} min)"
                    if len(r['ops'])>1: t_val += f" [{e['op'].upper()}]"
                    times.append(t_val)
                if lang == 'en':
                    output.append(f"• To {obj['name']}: " + ", ".join(times))
                else:
                    output.append(f"• 往 {obj['name']}: " + ", ".join(times))
        output.append("")
    
    # Ensure deterministic fallback when no ETA block is produced
    if not any(line.startswith("🚌") for line in output):
        if lang == 'en':
            print("Service hours have passed / No route information found")
        else:
            print("尾班車已過或未有班次資料")
        return

    print("\n".join(output))
    if needs_bg_sync:
        sync_script = os.path.join(BASE_DIR, "sync_bus_stops.py")
        try: subprocess.Popen(["python3", sync_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
        except: pass

if __name__ == "__main__":
    import sys; a = sys.argv[1:]
    if len(a)>=2: main(a[0], a[1], a[2] if len(a)>2 else "tc")
