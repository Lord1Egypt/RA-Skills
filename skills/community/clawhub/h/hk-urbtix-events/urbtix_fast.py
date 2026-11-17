#!/usr/bin/env python3
"""
URBTIX Fast CLI — optimized for single-query lookups.
Usage: python3 urbtix_fast.py [--lang en|zh] <search terms...>

Examples:
  python3 urbtix_fast.py Andy Lau
  python3 urbtix_fast.py --lang zh 劉德華
  python3 urbtix_fast.py Leon Lai 黎明
"""
import os, sys, datetime, urllib.request, xml.etree.ElementTree as ET
import argparse

CACHE_DIR = os.path.join(os.path.expanduser("~"), ".urbtix_cache", "urbtix_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

BASE_URL = "https://fs-open-1304240968.cos.ap-hongkong.myqcloud.com/prod/gprd"
HK_TZ = datetime.timezone(datetime.timedelta(hours=8))

def hk_now():
    return datetime.datetime.now(datetime.timezone.utc).astimezone(HK_TZ)

def today_str():
    return hk_now().strftime("%Y%m%d")

def xml_filename(date_str):
    return f"URBTIX_eventBatch_{date_str}.xml"

def cache_path(date_str):
    return os.path.join(CACHE_DIR, xml_filename(date_str))

def download_batch(date_str):
    url = f"{BASE_URL}/{xml_filename(date_str)}"
    dest = cache_path(date_str)
    if os.path.exists(dest):
        return dest
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "urbtix-fast/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status != 200:
                return None
            data = resp.read()
        if b"<BATCH>" in data and b"URBTIX" in data:
            # Use temp file for atomic write
            temp_path = dest + ".tmp"
            with open(temp_path, "wb") as f:
                f.write(data)
            os.rename(temp_path, dest)
            return dest
    except:
        pass
    return None

def search_xml(filepath, keywords):
    try:
        tree = ET.parse(filepath)
    except:
        return []
    root = tree.getroot()
    matches = []
    for event in root.findall(".//EVENT"):
        eg = event.find("EVENT_EG")
        tc = event.find("EVENT_TC")
        name_en = (eg.text or "").lower()
        name_tc = (tc.text or "").lower()
        full = name_en + " " + name_tc
        if not any(kw.lower() in full for kw in keywords):
            continue
        venue_el = event.find("LOCATION/VENUE_EG")
        venue_tc_el = event.find("LOCATION/VENUE_TC")
        venue = venue_el.text if venue_el is not None else ""
        venue_tc = venue_tc_el.text if venue_tc_el is not None else ""
        sd = event.find("ST_DATE")
        ed = event.find("ED_DATE")
        perfs = event.find("PERFORMANCES")
        if perfs is not None:
            for p in perfs.findall("PERFORMANCE"):
                dt_el = p.find("PERFORMANCE_DATETIME")
                ref = p.find("REFERENCE_LINK")
                title_eg = p.find("TITLE_EG")
                title_tc = p.find("TITLE_TC")
                if dt_el is not None and dt_el.text:
                    parts = dt_el.text.strip().split(" ", 1)
                    d = parts[0] if parts else ""
                    t = parts[1] if len(parts) > 1 else ""
                else:
                    d, t = "", ""
                matches.append({
                    "name_en": title_eg.text if title_eg is not None else (eg.text or ""),
                    "name_tc": title_tc.text if title_tc is not None else (tc.text or ""),
                    "venue": venue, "venue_tc": venue_tc,
                    "date": d, "time": t,
                    "link": ref.text if ref is not None else "",
                    "start": sd.text if sd is not None else "",
                    "end": ed.text if ed is not None else "",
                })
    return matches

def format_matches(matches, language='en'):
    """Format matches as a table in the requested language."""
    if not matches:
        return ""
    
    if language == 'zh':
        header = f"{'日期':<12} {'時間':<8} {'節目':<30} {'場地':<20} {'連結'}"
        time_label = "待定"
        name_label = "未提供"
        venue_label = "未提供"
    else:
        header = f"{'Date':<12} {'Time':<8} {'Event':<30} {'Venue':<20} {'Link'}"
        time_label = "TBD"
        name_label = "N/A"
        venue_label = "N/A"
    
    lines = [header, "-" * 90]
    for m in matches:
        name = m["name_tc"] or m["name_en"] or name_label
        venue = m["venue_tc"] or m["venue"] or venue_label
        link = m["link"] if m["link"] else "N/A"
        lines.append(f"{m['date']:<12} {m['time']:<8} {name:<30} {venue:<20} {link}")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="URBTIX Fast CLI - Search Hong Kong events")
    parser.add_argument("--lang", choices=["en", "zh"], default="en", help="Output language (default: en)")
    parser.add_argument("keywords", nargs="+", help="Search keywords (artist, event name, etc.)")
    args = parser.parse_args()
    
    keywords = args.keywords
    language = args.lang
    date_str = today_str()

    # Ensure today's batch is cached
    filepath = cache_path(date_str)
    if not os.path.exists(filepath):
        result = download_batch(date_str)
        if result:
            filepath = result

    if not filepath or not os.path.exists(filepath):
        if language == 'zh':
            print("無法獲取URBTIX資料。請稍後再試。")
        else:
            print("Unable to fetch URBTIX data. Please try again later.")
        sys.exit(1)

    matches = search_xml(filepath, keywords)

    if not matches:
        try:
            total_events = len(ET.parse(filepath).getroot().findall('.//EVENT'))
        except:
            total_events = 0
        if language == 'zh':
            print(f"找不到符合 '{' '.join(keywords)}' 的演出。")
            print(f"（已搜尋 {date_str} 批次，共 {total_events} 個節目）")
        else:
            print(f"No performances found matching '{' '.join(keywords)}'.")
            print(f"(Searched {date_str} batch, {total_events} events total)")
        return

    if language == 'zh':
        print(f"找到 {len(matches)} 場符合 '{' '.join(keywords)}' 的演出：\n")
    else:
        print(f"Found {len(matches)} performance(s) matching '{' '.join(keywords)}':\n")
    
    print(format_matches(matches, language))

if __name__ == "__main__":
    main()
