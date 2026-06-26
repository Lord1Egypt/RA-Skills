#!/usr/bin/env python3
"""
Nex Life Logger - Headless Activity Collector
MIT-0 License - Copyright 2026 Nex AI (Kevin Blancaflor)

Runs as a background service to collect browser history, active window info,
and YouTube transcripts. No GUI dependencies.

Usage:
    python collector_headless.py              # Run continuously (default 30s interval)
    python collector_headless.py --once       # Collect once and exit
    python collector_headless.py --interval 60  # Custom interval in seconds
"""
import json
import os
import shutil
import signal
import sqlite3
import sys
import tempfile
import datetime as dt
import platform
import logging
import time
import argparse
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Add lib directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import (
    BROWSER_PATHS, POLL_INTERVAL,
    MAX_URL_LENGTH, MAX_TITLE_LENGTH, DATA_DIR,
)
import user_filters
from chat_filter import is_chat_url, is_chat_window
from content_filter import is_productive
from youtube_transcript import fetch_transcript
from storage import insert_activities, get_sync_ts, set_sync_ts, save_keywords, init_db
from keyword_extractor import extract_from_activities

log = logging.getLogger("life-logger.collector")

_shutdown = False


def _handle_signal(signum, frame):
    global _shutdown
    log.info("Received signal %d, shutting down gracefully...", signum)
    _shutdown = True


def _sanitize_url(url):
    if not url:
        return ""
    url = "".join(c for c in url if ord(c) >= 32)
    return url[:MAX_URL_LENGTH]


def _sanitize_title(title):
    if not title:
        return ""
    title = "".join(c for c in title if ord(c) >= 32)
    return title[:MAX_TITLE_LENGTH]


def _secure_delete_temp(tmp_path):
    try:
        if tmp_path.exists():
            size = tmp_path.stat().st_size
            with open(tmp_path, "wb") as f:
                f.write(os.urandom(size))
                f.flush()
                os.fsync(f.fileno())
            tmp_path.unlink()
    except Exception:
        tmp_path.unlink(missing_ok=True)


def _is_sensitive_window(title):
    if not title:
        return False
    lower = title.lower()
    sensitive_keywords = user_filters.get("sensitive_window_keywords")
    return any(kw in lower for kw in sensitive_keywords)


def _chrome_epoch_to_iso(chrome_ts):
    epoch_diff = 11644473600
    ts_seconds = chrome_ts / 1_000_000 - epoch_diff
    return dt.datetime.fromtimestamp(ts_seconds, tz=dt.timezone.utc).isoformat()


def _classify_url(url):
    host = urlparse(url).hostname or ""
    path = urlparse(url).path or ""
    if "youtube.com" in host or "youtu.be" in host:
        if "/watch" in path or "/shorts" in path:
            return "youtube"
        elif "/results" in path:
            return "search"
        return "url"
    search_engines = ["google.", "bing.com", "duckduckgo.com", "search.yahoo", "ecosia.org", "startpage.com"]
    if any(se in host for se in search_engines):
        qs = parse_qs(urlparse(url).query)
        if "q" in qs or "p" in qs or "search_query" in qs:
            return "search"
    return "url"


def _extract_extra(url, kind):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if kind == "search":
        query = qs.get("q") or qs.get("p") or qs.get("search_query") or []
        return {"search_query": query[0] if query else ""}
    if kind == "youtube":
        video_id = qs.get("v", [""])[0]
        return {"video_id": video_id}
    return {}


def _read_chromium_history(browser, db_path, since_ts):
    if not db_path.exists():
        return []
    tmp = Path(tempfile.mkdtemp()) / "History"
    try:
        shutil.copy2(db_path, tmp)
    except (PermissionError, OSError) as e:
        log.warning("%s: can't copy history file: %s", browser, e)
        return []
    rows = []
    try:
        conn = sqlite3.connect(str(tmp), timeout=5)
        conn.row_factory = sqlite3.Row
        query = "SELECT url, title, last_visit_time FROM urls WHERE last_visit_time > 0"
        params = []
        if since_ts:
            query += " AND last_visit_time > ?"
            d = dt.datetime.fromisoformat(since_ts)
            epoch_diff = 11644473600
            chrome_ts = int((d.timestamp() + epoch_diff) * 1_000_000)
            params.append(chrome_ts)
        query += " ORDER BY last_visit_time ASC"
        for r in conn.execute(query, params).fetchall():
            url = _sanitize_url(r["url"] or "")
            title = _sanitize_title(r["title"] or "")
            if not url:
                continue
            if is_chat_url(url):
                continue
            iso_ts = _chrome_epoch_to_iso(r["last_visit_time"])
            kind = _classify_url(url)
            extra = _extract_extra(url, kind)
            transcript = None
            if kind == "youtube":
                video_id = extra.get("video_id", "")
                if video_id:
                    try:
                        transcript = fetch_transcript(video_id, title=title)
                        if transcript:
                            extra["has_transcript"] = True
                            log.info("%s: transcript captured for '%s' (%s)", browser, title, video_id)
                    except Exception as e:
                        log.warning("%s: transcript fetch error for '%s' (%s): %s", browser, title, video_id, e)
            if not is_productive(url, title, transcript):
                continue
            rows.append({
                "timestamp": iso_ts,
                "source": browser,
                "kind": kind,
                "title": title,
                "url": url,
                "extra": json.dumps(extra),
            })
        conn.close()
    except Exception as e:
        log.error("%s: error reading history: %s", browser, e)
    finally:
        _secure_delete_temp(tmp)
        try:
            tmp.parent.rmdir()
        except Exception:
            pass
    return rows


def _firefox_ts_to_iso(ts):
    return dt.datetime.fromtimestamp(ts / 1_000_000, tz=dt.timezone.utc).isoformat()


def _find_firefox_db():
    ff_dir = BROWSER_PATHS.get("firefox_dir")
    if ff_dir is None or not ff_dir.exists():
        return None
    for profile in ff_dir.iterdir():
        places = profile / "places.sqlite"
        if places.exists():
            return places
    return None


def _read_firefox_history(since_ts):
    db_path = _find_firefox_db()
    if db_path is None:
        return []
    tmp = Path(tempfile.mkdtemp()) / "places.sqlite"
    try:
        shutil.copy2(db_path, tmp)
    except (PermissionError, OSError) as e:
        log.warning("firefox: can't copy places: %s", e)
        return []
    rows = []
    try:
        conn = sqlite3.connect(str(tmp), timeout=5)
        conn.row_factory = sqlite3.Row
        query = "SELECT url, title, last_visit_date FROM moz_places WHERE last_visit_date IS NOT NULL"
        params = []
        if since_ts:
            d = dt.datetime.fromisoformat(since_ts)
            params.append(int(d.timestamp() * 1_000_000))
            query += " AND last_visit_date > ?"
        query += " ORDER BY last_visit_date ASC"
        for r in conn.execute(query, params).fetchall():
            url = _sanitize_url(r["url"] or "")
            title = _sanitize_title(r["title"] or "")
            if not url:
                continue
            if is_chat_url(url):
                continue
            iso_ts = _firefox_ts_to_iso(r["last_visit_date"])
            kind = _classify_url(url)
            extra = _extract_extra(url, kind)
            transcript = None
            if kind == "youtube":
                video_id = extra.get("video_id", "")
                if video_id:
                    try:
                        transcript = fetch_transcript(video_id, title=title)
                        if transcript:
                            extra["has_transcript"] = True
                            log.info("firefox: transcript captured for '%s' (%s)", title, video_id)
                    except Exception as e:
                        log.warning("firefox: transcript fetch error for '%s' (%s): %s", title, video_id, e)
            if not is_productive(url, title, transcript):
                continue
            rows.append({
                "timestamp": iso_ts,
                "source": "firefox",
                "kind": kind,
                "title": title,
                "url": url,
                "extra": json.dumps(extra),
            })
        conn.close()
    except Exception as e:
        log.error("firefox: error reading history: %s", e)
    finally:
        _secure_delete_temp(tmp)
        try:
            tmp.parent.rmdir()
        except Exception:
            pass
    return rows


def get_active_window():
    system = platform.system()
    title = ""
    process = ""
    try:
        if system == "Windows":
            import ctypes
            from ctypes import wintypes
            user32 = ctypes.windll.user32
            hwnd = user32.GetForegroundWindow()
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            title = buf.value
            import psutil
            pid = wintypes.DWORD()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            try:
                proc = psutil.Process(pid.value)
                process = proc.name()
            except Exception:
                pass
        elif system == "Darwin":
            import subprocess
            script = '''
            tell application "System Events"
                set frontApp to first application process whose frontmost is true
                set appName to name of frontApp
                set winTitle to ""
                try
                    set winTitle to name of front window of frontApp
                end try
                return appName & "|" & winTitle
            end tell
            '''
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                parts = result.stdout.strip().split("|", 1)
                process = parts[0] if parts else ""
                title = parts[1] if len(parts) > 1 else ""
        else:
            import subprocess
            result = subprocess.run(["xdotool", "getactivewindow", "getwindowname"],
                                    capture_output=True, text=True, timeout=5)
            title = result.stdout.strip() if result.returncode == 0 else ""
            try:
                pid_result = subprocess.run(["xdotool", "getactivewindow", "getwindowpid"],
                                            capture_output=True, text=True, timeout=5)
                if pid_result.returncode == 0:
                    import psutil
                    proc = psutil.Process(int(pid_result.stdout.strip()))
                    process = proc.name()
            except Exception:
                pass
    except Exception as e:
        log.debug("Active window detection failed: %s", e)
        return None
    if not title and not process:
        return None
    if is_chat_window(title) or is_chat_window(process):
        return None
    if _is_sensitive_window(title):
        return None
    title = _sanitize_title(title)
    return {
        "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": "window",
        "kind": "app_focus",
        "title": title,
        "url": "",
        "extra": json.dumps({"process": _sanitize_title(process)}),
    }


def collect_all():
    all_rows = []
    for browser in ("chrome", "edge", "brave"):
        path = BROWSER_PATHS.get(browser)
        if path:
            since = get_sync_ts(browser)
            rows = _read_chromium_history(browser, path, since)
            if rows:
                all_rows.extend(rows)
                set_sync_ts(browser, rows[-1]["timestamp"])
    since = get_sync_ts("firefox")
    ff_rows = _read_firefox_history(since)
    if ff_rows:
        all_rows.extend(ff_rows)
        set_sync_ts("firefox", ff_rows[-1]["timestamp"])
    win = get_active_window()
    if win:
        all_rows.append(win)
    if all_rows:
        insert_activities(all_rows)
        log.info("Collected %d activities", len(all_rows))
        try:
            keywords = extract_from_activities(all_rows)
            if keywords:
                save_keywords(keywords)
                log.info("Extracted %d keywords from activities", len(keywords))
        except Exception as e:
            log.warning("Keyword extraction failed: %s", e)
    return len(all_rows)


def main():
    parser = argparse.ArgumentParser(
        description="Nex Life Logger - Background Activity Collector"
    )
    parser.add_argument(
        "--once", action="store_true",
        help="Collect once and exit (useful for timer-based scheduling)"
    )
    parser.add_argument(
        "--interval", type=int, default=POLL_INTERVAL,
        help="Collection interval in seconds (default: %d)" % POLL_INTERVAL
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        stream=sys.stdout,
    )

    signal.signal(signal.SIGTERM, _handle_signal)
    signal.signal(signal.SIGINT, _handle_signal)

    init_db()
    user_filters.init(DATA_DIR)

    if args.once:
        log.info("Running single collection cycle")
        count = collect_all()
        log.info("Done. Collected %d activities.", count)
        return

    log.info("Nex Life Logger collector starting (interval: %ds)", args.interval)
    log.info("Data directory: %s", DATA_DIR)

    while not _shutdown:
        try:
            collect_all()
        except Exception as e:
            log.error("Collection cycle failed: %s", e)
        for _ in range(args.interval):
            if _shutdown:
                break
            time.sleep(1)

    log.info("Nex Life Logger collector stopped.")


if __name__ == "__main__":
    main()
