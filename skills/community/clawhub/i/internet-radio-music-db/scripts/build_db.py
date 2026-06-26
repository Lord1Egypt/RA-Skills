#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_db.py - Music stream database builder from internet-radio.com.
Parses genre pages, extracts .pls playlists, resolves direct stream URLs.
"""

import json, os, re, time, urllib.request
from datetime import datetime, timezone

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(SKILL_DIR, "state.json")

BASE_URL = "https://www.internet-radio.com"
TIMEOUT = 15
DELAY = 0.1
MAX_PAGES = 10

GENRES = [
    "rock", "pop", "jazz", "classical", "electronic", "dance",
    "blues", "metal", "indie", "alternative", "ambient", "latin",
    "reggae", "folk", "soul", "punk", "funk", "disco",
    "80s", "90s", "oldies", "top-40", "news", "talk",
    "house", "techno", "trance", "country", "gospel",
]

# -- State management --

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"streams": [], "last_updated": None, "last_checked": None}

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def url_exists(state, url):
    return any(s.get("url") == url for s in state["streams"])

# -- HTTP --

def fetch_url(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            charset = "utf-8"
            ct = resp.headers.get("Content-Type", "")
            m = re.search(r"charset=([^\s;]+)", ct)
            if m:
                charset = m.group(1)
            return resp.read().decode(charset, errors="replace")
    except Exception:
        return None

# -- Playlist parsing --

def parse_pls(content):
    """Parse .pls content, return list of (url, title)."""
    results = []
    for line in content.splitlines():
        line = line.strip()
        m = re.match(r"^File\d+=(.+)", line, re.IGNORECASE)
        if m:
            results.append(m.group(1).strip())
    return results

def parse_m3u(content):
    """Parse .m3u content, return list of URLs."""
    results = []
    for line in content.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            results.append(line)
    return results

def resolve_stream_url(pls_href):
    """
    Given a playlistgenerator href, download the playlist and extract stream URL.
    Falls back to constructing URL from server address.
    """
    # Normalize &amp; -> &
    pls_href = pls_href.replace("&amp;", "&")
    
    pls_href = pls_href.replace("&amp;", "&")
    
    if pls_href.startswith("/"):
        pls_href = BASE_URL + pls_href
    
    content = fetch_url(pls_href)
    if content:
        for parser in (parse_pls, parse_m3u):
            results = parser(content)
            if results:
                return results[0]
    
    # Fallback: extract server URL and construct stream URL
    m = re.search(r"[?&]u=([^&]+)", pls_href)
    if m:
        server_url = urllib.request.unquote(m.group(1))
        # Remove playlist suffix
        base = re.sub(r"/(listen|live|stream)\.(pls|m3u|asx|ram|mp3|aac|ogg)$", "", server_url)
        base = re.sub(r"/(listen|live|stream)$", "", base)
        if not base.endswith("/stream"):
            return base + "/stream"
        return base
    return None

# -- Speed check (shared module) --
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_stream import check_stream

def check_stream_speed(url, bitrate=None):
    """Adaptive speed check using bitrate-based threshold. Returns (ok, speed_bps)."""
    ok, speed_kbs, threshold_kbs, bytes_read, elapsed = check_stream(url, bitrate_kbps=bitrate)
    return ok, speed_kbs * 1024

# -- Language detection --

def detect_language(name, genre):
    n = name.lower()
    for kw in ["\u0440\u0443\u0441", "\u0440\u043e\u0441\u0441\u0438\u044f", "\u043c\u043e\u0441\u043a\u0432\u0430", "\u0440\u0435\u0442\u0440\u043e", "\u0448\u0430\u043d\u0441\u043e\u043d", "\u043d\u0430\u0448\u0435 \u0440\u0430\u0434\u0438\u043e", "\u043c\u0430\u044f\u043a", "\u0432\u0435\u0441\u0442\u0438"]:
        if kw in n:
            return "ru"
    for kw in ["deutsch", "germany", "berlin", "bayern"]:
        if kw in n:
            return "de"
    for kw in ["france", "paris", "fran\u00e7ais", "french"]:
        if kw in n:
            return "fr"
    for kw in ["espa\u00f1a", "spanish", "latino", "mexico"]:
        if kw in n:
            return "es"
    if genre in ("latin", "reggae", "salsa", "bossa-nova", "brazilian"):
        return "es"
    return "en"

# -- Stream availability check --

def probe_stream(url, timeout=10):
    req = urllib.request.Request(url, method="HEAD", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Icy-MetaData": "1",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except Exception:
        pass
    try:
        req2 = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Icy-MetaData": "1",
            "Range": "bytes=0-1023",
        })
        with urllib.request.urlopen(req2, timeout=timeout) as resp:
            return 200 <= resp.status < 400
    except Exception:
        return False

# -- HTML parsing --

def parse_genre_page(html, genre_name):
    """Parse genre page HTML and extract station data from <tr> blocks."""
    stations = []
    
    # Decode HTML entities
    html = html.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')
    
    tr_blocks = re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.DOTALL)
    
    for tr in tr_blocks:
        # Find .pls link
        pls_match = re.search(
            r'href="(/servers/tools/playlistgenerator/\?u=[^"]+&t=\.pls)"',
            tr
        )
        if not pls_match:
            continue
        
        pls_href = pls_match.group(1)
        
        # Find station name
        name_match = re.search(
            r'<h[34][^>]*>\s*<a[^>]*href="/station/[^"]*"[^>]*>(.*?)</a>\s*</h[34]>',
            tr, re.DOTALL
        )
        if not name_match:
            continue
        
        name = re.sub(r"<[^>]+>", "", name_match.group(1)).strip()
        if not name or len(name) < 2:
            continue
        
        # Find genres
        genre_links = re.findall(r'href="/stations/([a-z0-9\-]+)/"[^>]*>([^<]{1,30})</a>', tr)
        genres = [g[1].strip() for g in genre_links if g[1].strip()]
        
        # Find bitrate
        bitrate_m = re.search(r"(\d+)\s*Kbps", tr)
        bitrate = int(bitrate_m.group(1)) if bitrate_m else None
        
        # Find listeners
        listeners_m = re.search(r"(\d+)\s*Listeners", tr)
        listeners = int(listeners_m.group(1)) if listeners_m else 0
        
        # Audio type
        audio_m = re.search(r"audio/(mpeg|aac|ogg|vorbis)", tr)
        audio_type = audio_m.group(1) if audio_m else "unknown"
        
        # Station page URL
        station_m = re.search(r'href="(/station/[^"/]+/)"', tr)
        station_href = station_m.group(1) if station_m else ""
        
        stations.append({
            "name": name,
            "pls_href": pls_href,
            "station_href": station_href,
            "genres": genres,
            "genre_main": genre_name,
            "bitrate": bitrate,
            "listeners": listeners,
            "audio_type": audio_type,
        })
    
    return stations

def collect_genre(genre_slug):
    """Collect stations from all pages of a genre."""
    all_stations = []
    for page in range(1, MAX_PAGES + 1):
        if page == 1:
            url = f"{BASE_URL}/stations/{genre_slug}/"
        else:
            url = f"{BASE_URL}/stations/{genre_slug}/?page={page}"
        
        html = fetch_url(url)
        if not html:
            print(f"    [Error] Page {page} failed to load")
            break
        
        stations = parse_genre_page(html, genre_slug)
        if not stations:
            print(f"    [Info] Page {page}: no stations found (end)")
            break
        
        all_stations.extend(stations)
        print(f"    [Page {page}] Found {len(stations)} stations")
        time.sleep(DELAY)
    
    return all_stations

# -- Main --

def main():
    import sys
    sys.stdout.reconfigure(line_buffering=True)
    print("=" * 60, flush=True)
    print("Music Stream Database Builder")
    print(f"Source: {BASE_URL}")
    print(f"Genres: {len(GENRES)}, max pages per genre: {MAX_PAGES}")
    print("=" * 60)
    
    state = load_state()
    existing = len(state["streams"])
    added = 0
    seen_urls = set(s.get("url", "") for s in state["streams"])  # dedup protection
    
    # Step 1: Collect stations (parallel: one thread per genre)
    MAX_PARALLEL_GENRES = 10
    print("\nStep 1: Collecting stations (parallel, {} threads) ...\n".format(MAX_PARALLEL_GENRES))
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    all_stations = []
    # Process genres in batches to avoid overloading the server
    for batch_start in range(0, len(GENRES), MAX_PARALLEL_GENRES):
        batch = GENRES[batch_start:batch_start + MAX_PARALLEL_GENRES]
        print(f"  Batch {batch_start // MAX_PARALLEL_GENRES + 1}: {', '.join(batch)}")
        with ThreadPoolExecutor(max_workers=MAX_PARALLEL_GENRES) as executor:
            future_to_genre = {executor.submit(collect_genre, genre): genre for genre in batch}
            for future in as_completed(future_to_genre):
                genre = future_to_genre[future]
                try:
                    stations = future.result()
                    all_stations.extend(stations)
                    print(f"    [{genre}] Collected: {len(stations)} stations")
                except Exception as e:
                    print(f"    [{genre}] ERROR: {e}")
    
    print(f"\n  Total stations collected: {len(all_stations)}")
    
    # Step 2: Resolve stream URLs (fast: construct from server address)
    print("\nStep 2: Resolving stream URLs ...\n")
    
    new_streams = []
    for i, st in enumerate(all_stations):
        # Fast path: construct URL from server address in pls_href
        stream_url = None
        m = re.search(r"[?&]u=([^&]+)", st["pls_href"])
        if m:
            server_url = urllib.request.unquote(m.group(1))
            # Remove playlist suffix
            base = re.sub(r"/(listen|live|stream)\.(pls|m3u|asx|ram|mp3|aac|ogg)$", "", server_url)
            base = re.sub(r"/(listen|live|stream)$", "", base)
            if not base.endswith("/stream"):
                stream_url = base + "/stream"
            else:
                stream_url = base
        
        if not stream_url:
            continue
        
        if stream_url in seen_urls:
            continue
        seen_urls.add(stream_url)
        
        lang = detect_language(st["name"], st["genre_main"])
        
        new_streams.append({
            "url": stream_url,
            "name": st["name"],
            "genre": st["genre_main"],
            "language": lang,
            "available": True,
            "source": "internet-radio.com",
            "station_url": BASE_URL + st["station_href"] if st["station_href"] else None,
            "bitrate": st.get("bitrate"),
            "listeners": st.get("listeners", 0),
            "audio_type": st.get("audio_type", "unknown"),
            "genres": st.get("genres", []),
            "added_at": datetime.now(timezone.utc).isoformat(),
            "last_checked": None,
            "failed_checks": 0,
        })
        
        if (i + 1) % 100 == 0:
            print(f"    Processed {i+1}/{len(all_stations)}, new: {len(new_streams)}")
    
    print(f"  New streams: {len(new_streams)}")
    
    # Step 3: Check availability with speed test (ALL new streams)
    print("\nStep 3: Speed check (all {} new streams) ...\n".format(len(new_streams)))
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    avail_count = 0
    with ThreadPoolExecutor(max_workers=60) as executor:
        future_to_stream = {
            executor.submit(check_stream_speed, stream["url"], stream.get("bitrate")): stream
            for stream in new_streams
        }
        done_count = 0
        for future in as_completed(future_to_stream):
            stream = future_to_stream[future]
            ok, speed = future.result()
            stream["available"] = ok
            stream["last_checked"] = datetime.now(timezone.utc).isoformat()
            stream["last_speed_bps"] = round(speed, 2)
            if ok:
                avail_count += 1
            else:
                stream["failed_checks"] = 1
            done_count += 1
            if done_count % 50 == 0:
                print("    Checked {}/{}, available: {}".format(done_count, len(new_streams), avail_count))
    
    print("    Checked {}/{}, available: {}".format(done_count, len(new_streams), avail_count))
    
    # Step 4: Save
    print("\nStep 4: Saving to database ...\n")
    
    for stream in new_streams:
        state["streams"].append(stream)
        added += 1
    
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    
    total = len(state["streams"])
    avail = sum(1 for s in state["streams"] if s.get("available", True))
    
    print("=" * 60)
    print("RESULTS:")
    print(f"  Was:              {existing}")
    print(f"  Stations found:   {len(all_stations)}")
    print(f"  New added:        {added}")
    print(f"  Checked:          {len(new_streams)} (available: {avail_count})")
    print(f"  Total in DB:      {total} (available: {avail})")
    print("=" * 60)

if __name__ == "__main__":
    main()
