#!/usr/bin/env python3
"""
HK URBTIX Events Skill
Intelligent query of URBTIX event batch data with security hardening.
"""

import os
import sys
import json
import re
import datetime
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

# Configuration
WORKSPACE = os.environ.get("OPENCLAW_WORKSPACE", "/home/node/.openclaw/workspace")
CACHE_DIR = Path(WORKSPACE) / "urbtix_cache"
CACHE_DIR.mkdir(exist_ok=True)

# Official URBTIX batch XML distribution (cloud host)
BASE_URL = "https://fs-open-1304240968.cos.ap-hongkong.myqcloud.com/prod/gprd"
XML_PREFIX = "URBTIX_eventBatch_"
XML_SUFFIX = ".xml"

# HK timezone offset (GMT+8)
HK_OFFSET = datetime.timedelta(hours=8)

def get_hk_now():
    """Current time in Hong Kong (GMT+8)"""
    return datetime.datetime.utcnow() + HK_OFFSET

def parse_date_from_question(question):
    """Extract a date from the question. Returns datetime.date or defaults to today."""
    patterns = [
        r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})',
        r'(\d{4})(\d{2})(\d{2})',
    ]
    for pat in patterns:
        match = re.search(pat, question)
        if match:
            try:
                year = int(match.group(1))
                month = int(match.group(2))
                day = int(match.group(3))
                return datetime.date(year, month, day)
            except:
                pass
    return get_hk_now().date()

def format_date_for_xml(dt):
    """Format date as YYYYMMDD"""
    return dt.strftime("%Y%m%d")

def build_xml_filename(target_date):
    """Build filename like URBTIX_eventBatch_20260326.xml"""
    date_str = format_date_for_xml(target_date)
    return f"{XML_PREFIX}{date_str}{XML_SUFFIX}"

def build_url(target_date):
    filename = build_xml_filename(target_date)
    return f"{BASE_URL}/{filename}"

def get_cache_path(filename):
    return CACHE_DIR / filename

# Rate limiting: lock files per date
DOWNLOAD_LOCK_DIR = CACHE_DIR / ".locks"
DOWNLOAD_LOCK_DIR.mkdir(exist_ok=True)

def get_download_lock_path(date_str):
    return DOWNLOAD_LOCK_DIR / f"download_{date_str}.lock"

def has_downloaded_today(date_str):
    """Check if we've already attempted a download for this date within the same HK day."""
    lock_path = get_download_lock_path(date_str)
    if lock_path.exists():
        try:
            lock_date_str = lock_path.stem.split('_')[1]
            lock_date = datetime.datetime.strptime(lock_date_str, "%Y%m%d").date()
            hk_today = get_hk_now().date()
            if lock_date == hk_today:
                return True
        except:
            pass
    return False

def record_download_attempt(date_str):
    """Create a lock file to record that we attempted a download for this date today."""
    lock_path = get_download_lock_path(date_str)
    lock_path.touch(exist_ok=True)

def download_xml(url, filename, max_retries=2):
    """
    Download XML with strict rate limiting: at most one download per date per HK day.
    Also prevents downloading dates prior to today.
    Returns True on success, False on failure.
    """
    # Extract date from filename
    date_str = filename.replace(XML_PREFIX, '').replace(XML_SUFFIX, '')
    try:
        file_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except ValueError:
        return False  # Invalid filename format

    # Don't download dates in the past (unless forced via cache bypass logic elsewhere)
    if file_date < get_hk_now().date():
        return False

    # Rate limit: only one download attempt per HK day
    if has_downloaded_today(date_str):
        return False

    # Create lock before network call to prevent concurrent downloads
    record_download_attempt(date_str)

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-urbtix-skill/1.0.2'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status != 200:
                    continue
                data = resp.read()
                # Validate that this is URBTIX XML
                if b'<BATCH>' not in data or b'URBTIX' not in data:
                    # Invalid or unexpected content
                    return False
                cache_path = get_cache_path(filename)
                cache_path.write_bytes(data)
                return True
        except Exception as e:
            if attempt == max_retries:
                return False
    return False
    try:
        date_str = filename.split('_')[-1].split('.')[0]
        file_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
    except:
        print(f"Invalid filename format: {filename}", file=sys.stderr)
        return False

    # Reject dates before today
    hk_today = get_hk_now().date()
    if file_date < hk_today:
        print(f"Refusing to download past date: {date_str} (today is {format_date_for_xml(hk_today)})", file=sys.stderr)
        return False

    # Check if we've already downloaded/attempted today
    if has_downloaded_today(date_str):
        print(f"Rate limit: already attempted download for {date_str} today", file=sys.stderr)
        cache_path = get_cache_path(filename)
        if cache_path.exists():
            return True
        return False

    cache_path = get_cache_path(filename)
    temp_path = cache_path.with_suffix('.tmp')

    for attempt in range(max_retries + 1):
        try:
            if cache_path.exists():
                record_download_attempt(date_str)
                return True
            if temp_path.exists():
                temp_path.unlink()

            req = urllib.request.Request(url, headers={'User-Agent': 'OpenClaw-URBTIX-Skill/1.0'})
            with urllib.request.urlopen(req, timeout=30) as resp, open(temp_path, 'wb') as out:
                out.write(resp.read())

            # Validate
            try:
                tree = ET.parse(temp_path)
                root = tree.getroot()

                # Verify source authenticity: must contain <SYSTEM>URBTIX</SYSTEM>
                system_el = root.find('SYSTEM')
                if system_el is None or system_el.text.strip().upper() != 'URBTIX':
                    print(f"Validation failed: XML does not appear to be from URBTIX (SYSTEM tag missing or not 'URBTIX')", file=sys.stderr)
                    temp_path.unlink()
                    return False

                send_date_el = root.find('SEND_DATE')
                if send_date_el is not None:
                    send_date = send_date_el.text.strip()
                    expected_date = filename.split('_')[-1].split('.')[0]
                    if send_date != expected_date:
                        print(f"Validation failed: SEND_DATE {send_date} != expected {expected_date}", file=sys.stderr)
                        temp_path.unlink()
                        return False
                total_el = root.find('TOTAL')
                if total_el is not None:
                    try:
                        expected_total = int(total_el.text.strip())
                        events = root.findall('.//EVENT')
                        actual_total = len(events)
                        if expected_total != actual_total:
                            print(f"Validation failed: TOTAL {expected_total} != actual {actual_total}", file=sys.stderr)
                            temp_path.unlink()
                            return False
                    except:
                        pass
                temp_path.rename(cache_path)
                record_download_attempt(date_str)
                return True
            except ET.ParseError as e:
                print(f"XML parse error: {e}", file=sys.stderr)
                if temp_path.exists():
                    temp_path.unlink()
                if attempt < max_retries:
                    continue
                return False

        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"XML not found: {url}", file=sys.stderr)
                return False
            print(f"HTTP error {e.code} on attempt {attempt+1}", file=sys.stderr)
        except Exception as e:
            print(f"Download error on attempt {attempt+1}: {e}", file=sys.stderr)

        if attempt < max_retries:
            import time
            time.sleep(2)

    if temp_path.exists():
        temp_path.unlink()
    return False

def load_xml(filename):
    cache_path = get_cache_path(filename)
    if not cache_path.exists():
        return None
    try:
        return ET.parse(cache_path)
    except ET.ParseError as e:
        print(f"Cache parse error: {e}", file=sys.stderr)
        return None

def purge_old_cache():
    """
    Background task: purge cached XML files older than 7 days.
    Runs silently without user notification.
    """
    hk_now = get_hk_now()
    cutoff_date = hk_now - datetime.timedelta(days=7)
    purged_count = 0
    
    for cache_file in CACHE_DIR.glob("URBTIX_eventBatch_*.xml"):
        try:
            date_str = cache_file.stem.split('_')[-1]
            file_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
            if file_date < cutoff_date.date():
                cache_file.unlink()
                purged_count += 1
        except Exception as e:
            print(f"Error purging {cache_file}: {e}", file=sys.stderr)
    
    # Also clean up old lock files (keep only today's)
    for lock_file in DOWNLOAD_LOCK_DIR.glob("download_*.lock"):
        try:
            lock_date_str = lock_file.stem.split('_')[1]
            lock_date = datetime.datetime.strptime(lock_date_str, "%Y%m%d").date()
            if lock_date < hk_now.date():
                lock_file.unlink()
        except:
            pass
    
    return purged_count

def list_available_batches():
    """Return list of (date, path) for valid cached XML batches, sorted newest first."""
    batches = []
    for cache_file in CACHE_DIR.glob("URBTIX_eventBatch_*.xml"):
        try:
            date_str = cache_file.stem.split('_')[-1]
            batch_date = datetime.datetime.strptime(date_str, "%Y%m%d").date()
            ET.parse(cache_file)  # validate
            batches.append((batch_date, cache_file))
        except Exception as e:
            print(f"Skipping corrupt cache {cache_file}: {e}", file=sys.stderr)
    batches.sort(reverse=True)
    return batches

def get_batch_xml(target_date, force_refresh=False):
    """
    Get an XML batch covering target_date.
    - Won't download if target_date is in the past (unless force_refresh with valid cache)
    - At most one download attempt per date per HK day
    - Falls back to most recent cached batch if download fails
    Returns (tree, filename, was_fallback) or (None, None, True) on failure.
    """
    filename = build_xml_filename(target_date)
    hk_today = get_hk_now().date()
    
    # Reject downloading batches for past dates (unless we already have it cached)
    if target_date < hk_today:
        # Check cache first
        cached = load_xml(filename)
        if cached is not None:
            return cached, filename, False
        # Can't download past dates
        print(f"Cannot download batch for past date {target_date}", file=sys.stderr)
        return None, None, True
    
    if not force_refresh:
        cached = load_xml(filename)
        if cached is not None:
            return cached, filename, False
    
    url = build_url(target_date)
    success = download_xml(url, filename)
    if success:
        tree = load_xml(filename)
        if tree is not None:
            return tree, filename, False
    
    # Fallback to most recent cached batch
    available = list_available_batches()
    if available:
        latest_date, latest_path = available[0]
        print(f"Batch for {target_date} not available; using {latest_date} batch as fallback", file=sys.stderr)
        try:
            tree = ET.parse(latest_path)
            return tree, latest_path.name, True
        except:
            pass
    
    # Try downloading today's batch as last resort (if target_date is not today)
    if target_date != hk_today:
        today_filename = build_xml_filename(hk_today)
        if not get_cache_path(today_filename).exists():
            today_url = build_url(hk_today)
            today_success = download_xml(today_url, today_filename)
            if today_success:
                today_tree = load_xml(today_filename)
                if today_tree is not None:
                    return today_tree, today_filename, True
    
    return None, None, True

def search_events(tree, name_keywords=None, venue_keywords=None, date_filter=None):
    """Search events in the XML tree. Returns list of matching performance entries."""
    root = tree.getroot()
    events = root.findall('.//EVENT')
    matches = []

    for event in events:
        event_eg = event.find('EVENT_EG')
        event_tc = event.find('EVENT_TC')
        venue_el = event.find('LOCATION/VENUE_EG')
        venue_tc_el = event.find('LOCATION/VENUE_TC')
        start_date = event.find('ST_DATE')
        end_date = event.find('ED_DATE')

        event_name_en = event_eg.text if event_eg is not None else ""
        event_name_tc = event_tc.text if event_tc is not None else ""
        venue = venue_el.text if venue_el is not None else ""
        venue_tc = venue_tc_el.text if venue_tc_el is not None else ""
        st_date = start_date.text if start_date is not None else ""
        ed_date = end_date.text if end_date is not None else ""

        # Date range filter
        if date_filter:
            filter_str = format_date_for_xml(date_filter)
            if not (st_date <= filter_str <= ed_date):
                continue

        # Name keywords
        if name_keywords:
            text_to_search = (event_name_en + " " + event_name_tc).lower()
            if not any(kw.lower() in text_to_search for kw in name_keywords):
                continue

        # Venue keywords
        if venue_keywords:
            venue_text = (venue + " " + venue_tc).lower()
            if not any(kw.lower() in venue_text for kw in venue_keywords):
                continue

        # Collect performances
        performances_el = event.find('PERFORMANCES')
        if performances_el is not None:
            for perf in performances_el.findall('PERFORMANCE'):
                ref_no = perf.find('REF_NO')
                perf_dt = perf.find('PERFORMANCE_DATETIME')
                title_eg = perf.find('TITLE_EG')
                title_tc = perf.find('TITLE_TC')
                link = perf.find('REFERENCE_LINK')

                if perf_dt is not None:
                    perf_datetime = perf_dt.text.strip()
                    parts = perf_datetime.split(' ')
                    if len(parts) >= 2:
                        perf_date = parts[0]
                        perf_time = parts[1]
                    else:
                        perf_date = perf_datetime
                        perf_time = ""
                else:
                    perf_date = ""
                    perf_time = ""

                # If a date filter is set, only include performances on that exact date
                if date_filter:
                    filter_str = format_date_for_xml(date_filter)  # YYYYMMDD
                    # Normalize perf_date from YYYY-MM-DD to YYYYMMDD for comparison
                    try:
                        perf_normalized = perf_date.replace('-', '')
                    except:
                        perf_normalized = perf_date
                    if perf_normalized != filter_str:
                        continue  # skip performances not on the target date

                match = {
                    "event_name_en": title_eg.text if title_eg is not None else event_name_en,
                    "event_name_tc": title_tc.text if title_tc is not None else event_name_tc,
                    "venue": venue,
                    "venue_tc": venue_tc,
                    "date": perf_date,
                    "time": perf_time,
                    "reference_link": link.text if link is not None else ""
                }
                matches.append(match)

    return matches

def format_answer(matches, total_found, clarification=None):
    if clarification:
        return {"answer": clarification, "matches": [], "clarification_needed": clarification}

    if not matches:
        return {
            "answer": "抱歉，在指定日期/條件下找不到相關演出。請嘗試提供更多細節（例如完整節目名稱、不同日期或場地）。",
            "matches": [],
            "clarification_needed": "無法匹配任何演出，請提供更多細節（完整名稱、日期、場地）"
        }

    unique = {}
    for m in matches:
        key = (m['event_name_tc'] or m['event_name_en'], m['date'], m['time'], m['venue_tc'] or m['venue'])
        if key not in unique:
            unique[key] = m

    # Build markdown table
    events = list(unique.values())
    events.sort(key=lambda x: x['time'])

    header = "| 時間 | 節目 | 場地 | 購票連結 |\n|------|------|------|----------|"
    rows = []
    for e in events:
        name = e['event_name_tc'] or e['event_name_en'] or "未提供"
        venue = e['venue_tc'] or e['venue'] or "未提供"
        time = e['time'] or "待定"
        link = e['reference_link']
        if link:
            link_cell = f"[購票]({link})"
        else:
            link_cell = "N/A"
        # Escape pipes in name/venue
        name = name.replace('|', '\\|')
        venue = venue.replace('|', '\\|')
        rows.append(f"| {time} | {name} | {venue} | {link_cell} |")

    answer = f"找到 {len(events)} 場演出：\n\n{header}\n" + "\n".join(rows)
    return {"answer": answer, "matches": events, "clarification_needed": None}

def query_events(question, force_refresh=False):
    """Main entry point."""
    # Run background cleanup silently
    purge_old_cache()
    
    target_date, name_keywords, venue_keywords = parse_question(question)
    tree, used_filename, was_fallback = get_batch_xml(target_date, force_refresh)
    if tree is None:
        return {
            "answer": f"無法獲取URBTIX資料。請稍後再試或確認日期是否正確。",
            "matches": [],
            "clarification_needed": "XML下載失敗，請稍後重試或提供不同日期"
        }

    matches = search_events(tree, name_keywords=name_keywords, venue_keywords=venue_keywords, date_filter=target_date)

    if not matches and was_fallback:
        # Search without date filter to see if there are any matches at all
        all_matches = search_events(tree, name_keywords=name_keywords, venue_keywords=venue_keywords, date_filter=None)
        if all_matches:
            return {
                "answer": f"在{target_date.strftime('%Y-%m-%d')}沒有找到相關演出。但以下日期有演出：",
                "matches": all_matches[:10],
                "clarification_needed": f"指定的日期沒有演出，但其他日期有。請確認是否查詢其他日期？"
            }
        else:
            return {
                "answer": "在可獲得的資料中找不到符合條件的演出。請嘗試提供更多細節。",
                "matches": [],
                "clarification_needed": "無法匹配任何演出，請提供更多細節（完整名稱、日期、場地）"
            }

    return format_answer(matches, len(matches))

def parse_question(question):
    """Parse question to extract date, event name keywords, and venue keywords."""
    hk_today = get_hk_now().date()
    target_date = parse_date_from_question(question)
    
    q_low = question.lower()

    venues = {
        "香港文化中心": ["香港文化中心", "hkc cultural centre", "hkcc"],
        "高山劇場": ["高山劇場", "ko shan theatre"],
        "香港演藝學院": ["香港演藝學院", "hkap"],
        "中環展城館": ["中環展城館"],
        "荃灣大會堂": ["荃灣大會堂", "tsuen wan town hall"],
    }

    venue_keywords = []
    for venue_name, aliases in venues.items():
        if any(alias in q_low for alias in aliases):
            venue_keywords.append(venue_name)
            for alias in aliases:
                q_low = q_low.replace(alias, '')

    q_clean = re.sub(r'\b(when|where|what|is|are|the|for|on|in|at|show|performance|ticket|book|find|tell me|about|event|events)\b', '', q_low)
    q_clean = re.sub(r'\d{4}[-/]\d{1,2}[-/]\d{1,2}', '', q_clean)
    q_clean = re.sub(r'\s+', ' ', q_clean).strip()

    name_keywords = [word for word in q_clean.split(' ') if len(word) > 1]
    if not name_keywords:
        name_keywords = None

    return target_date, name_keywords, venue_keywords

def main():
    try:
        payload = json.load(sys.stdin)
        question = payload.get("question", "")
        force_refresh = payload.get("force_refresh", False)

        if not question:
            print(json.dumps({"error": "Missing 'question' parameter"}, ensure_ascii=False))
            sys.exit(1)

        result = query_events(question, force_refresh)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e), "answer": f"執行錯誤：{e}"}, ensure_ascii=False))
        sys.exit(1)

if __name__ == "__main__":
    main()