#!/usr/bin/env python3
"""
Fetch myclub.fi schedules using standard library HTTP requests.

Usage:
    python3 fetch_myclub.py setup --username USER --password PASS
    python3 fetch_myclub.py discover
    python3 fetch_myclub.py fetch --account Kaarlo --period "this week"

Security manifest:
    Config accessed: ~/.myclub-config.json (read/write, mode 0600)
    External endpoints:
        - https://id.myclub.fi  (authentication: login form POST)
        - https://*.myclub.fi   (data fetch: club pages, event schedules)
    No other network calls. No telemetry. No data sent to third parties.
"""

import html as html_mod
import http.cookiejar
import json
import re
import sys
import argparse
import urllib.parse
import urllib.request
from pathlib import Path
from datetime import datetime, timedelta

CONFIG_FILE = Path.home() / ".myclub-config.json"

_quiet = False

def _print(*args, **kwargs):
    """Print to stdout unless quiet mode is enabled (JSON output)."""
    if not _quiet:
        print(*args, **kwargs)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

def load_config():
    """Load credentials from config."""
    if not CONFIG_FILE.exists():
        print("Error: No .myclub-config.json found. Run 'setup' first.", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(username: str, password: str):
    """Save credentials (accounts/clubs auto-discovered)."""
    config = {"username": username, "password": password}
    CONFIG_FILE.write_text(json.dumps(config, indent=2))
    CONFIG_FILE.chmod(0o600)
    _print(f"✓ Credentials saved to {CONFIG_FILE}")
    _print("✓ Run 'discover' to see available accounts and clubs")

# ---------------------------------------------------------------------------
# HTTP session
# ---------------------------------------------------------------------------

class MyclubSession:
    """HTTP session with cookie support for myclub.fi."""

    def __init__(self):
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            urllib.request.HTTPRedirectHandler(),
        )
        self.opener.addheaders = [
            ("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) myclub-skill/0.1"),
            ("Accept", "text/html,application/xhtml+xml"),
        ]
        self.last_url = None
        self.last_html = None

    def get(self, url: str) -> str:
        resp = self.opener.open(url, timeout=30)
        self.last_url = resp.url
        self.last_html = resp.read().decode("utf-8")
        return self.last_html

    def post(self, url: str, data: dict) -> str:
        encoded = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(url, data=encoded, method="POST")
        resp = self.opener.open(req)
        self.last_url = resp.url
        self.last_html = resp.read().decode("utf-8")
        return self.last_html

    def cookies_as_list(self) -> list:
        return [
            {"name": c.name, "value": c.value, "domain": c.domain, "path": c.path}
            for c in self.cookie_jar
        ]

# ---------------------------------------------------------------------------
# Debug
# ---------------------------------------------------------------------------

def _dump_page_debug(session: MyclubSession, prefix: str):
    """Save page state for debugging: HTML, URL, and cookies."""
    html = session.last_html or ""
    print(f"\n  DEBUG: Page state dump ({prefix})", file=sys.stderr)
    print(f"  URL: {session.last_url}", file=sys.stderr)

    Path(f"{prefix}.html").write_text(html)
    print(f"  HTML ({len(html)} chars): {prefix}.html", file=sys.stderr)

    cookies = session.cookies_as_list()
    Path(f"{prefix}-cookies.json").write_text(json.dumps(cookies, indent=2))
    print(f"  Cookies ({len(cookies)}): {prefix}-cookies.json", file=sys.stderr)

    # Structure summary
    print("  Structure summary:", file=sys.stderr)
    for pattern, label in [
        (r"data-events=", "data-events divs"),
        (r'class="[^"]*event-bar[^"]*"', "event bars"),
        (r'class="[^"]*event-container[^"]*"', "event containers"),
        (r"select_account", "account links"),
    ]:
        count = len(re.findall(pattern, html))
        if count > 0:
            print(f"    {label}: {count}", file=sys.stderr)

    # Sample data-events JSON
    events_json = _extract_data_events(html)
    if events_json:
        print(f"    data-events JSON: {len(events_json)} events", file=sys.stderr)
        print(f"    Sample event keys: {list(events_json[0].keys())}", file=sys.stderr)
        print(f"    Sample event: {json.dumps(events_json[0], indent=6, ensure_ascii=False)}", file=sys.stderr)

    # Sample event-bar
    bar_match = re.search(r'<div class="event-bar".*?</div>', html, re.DOTALL)
    if bar_match:
        print(f"    Sample event-bar HTML: {bar_match.group()[:300]}", file=sys.stderr)

    print(f"  END DEBUG\n", file=sys.stderr)

# ---------------------------------------------------------------------------
# HTML parsing helpers
# ---------------------------------------------------------------------------

def _extract_csrf_token(html: str) -> str | None:
    """Extract Rails CSRF token from hidden input or meta tag."""
    # Try hidden input first (more specific to the form)
    m = re.search(r'<input[^>]*name="authenticity_token"[^>]*value="([^"]+)"', html)
    if m:
        return m.group(1)
    # Fallback to meta tag
    m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', html)
    if not m:
        m = re.search(r'<meta\s+content="([^"]+)"\s+name="csrf-token"', html)
    return m.group(1) if m else None

def _extract_data_events(html: str) -> list:
    """Extract events JSON from data-events attribute."""
    m = re.search(r'data-events="([^"]*)"', html)
    if not m:
        return []
    raw = html_mod.unescape(m.group(1))
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []


def _extract_details_url(html: str) -> str | None:
    """Extract the event details API URL from data-url attribute."""
    m = re.search(r'data-url="([^"]*events/details[^"]*)"', html)
    return m.group(1) if m else None

def _parse_event_bars(html: str) -> dict:
    """
    Parse event-bar HTML blocks for day, time, and registration status.

    Returns: {event_id: {"day": "15.3.", "time": "12:35 - 14:30", "registration_status": "..."}}
    """
    results = {}
    # Split by event-container divs
    blocks = re.split(r'<div class="event-container">', html)
    for block in blocks[1:]:
        # Event ID from href="#event-content-NNNN"
        id_m = re.search(r'href="#event-content-(\d+)"', block)
        if not id_m:
            continue
        event_id = int(id_m.group(1))

        # Day: <span class="day"> su 15.3. </span>
        day = None
        day_m = re.search(r'<span class="day">\s*(.*?)\s*</span>', block, re.DOTALL)
        if day_m:
            parts = day_m.group(1).strip().split()
            day = parts[-1] if parts else None

        # Time: <span class="time"> 12:35 - 14:30 </span>
        time_val = None
        time_m = re.search(r'<span class="time">\s*(.*?)\s*</span>', block, re.DOTALL)
        if time_m:
            time_val = time_m.group(1).strip()

        # Registration status: <span class="registration-times"><span>...</span>
        reg_status = "unknown"
        reg_m = re.search(r'<span class="registration-times"><span>(.*?)</span>', block)
        if reg_m:
            reg_status = reg_m.group(1).strip()

        if event_id and (day or time_val):
            results[event_id] = {
                "day": day,
                "time": time_val,
                "registration_status": reg_status,
            }

    return results

# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def login(session: MyclubSession, username: str, password: str, debug: bool = False) -> bool:
    """Log in to myclub.fi via form POST."""
    _print("Logging in to myclub.fi...")

    html = session.get("https://id.myclub.fi/flow/login")

    csrf = _extract_csrf_token(html)
    if not csrf:
        print("  Error: CSRF token not found on login page", file=sys.stderr)
        if debug:
            _dump_page_debug(session, "/tmp/myclub-login")
        return False

    # Form posts to /flow/user_session (Rails resource route)
    session.post("https://id.myclub.fi/flow/user_session", {
        "utf8": "\u2713",
        "authenticity_token": csrf,
        "user_session[email]": username,
        "user_session[password]": password,
        "commit": "Kirjaudu sisään",
    })

    # Check if we landed on the home page (successful login)
    if "/flow/home" not in (session.last_url or ""):
        print("  Error: Login failed — did not reach home page", file=sys.stderr)
        if debug:
            _dump_page_debug(session, "/tmp/myclub-login-result")
        return False

    _print("  ✓ Login successful")
    return True

# ---------------------------------------------------------------------------
# Club discovery
# ---------------------------------------------------------------------------

def parse_clubs_from_html(html: str) -> dict:
    """
    Parse accounts and clubs from home page HTML.

    Link format: <a href="https://fckasiysi.myclub.fi/flow/select_account?id=889307">Kaarlo Hänninen</a>
    """
    clubs = {}
    seen_combos = set()

    links = re.findall(
        r'<a[^>]*href="(https?://([a-z0-9-]+)\.myclub\.fi/flow/select_account\?id=\d+)"[^>]*>(.*?)</a>',
        html, re.DOTALL,
    )

    for url, subdomain, raw_text in links:
        # Clean HTML tags from link text (some links contain <label>, <img>, <p> etc.)
        text = re.sub(r"<[^>]+>", "", raw_text).strip()
        if len(text) < 2:
            continue

        name_parts = text.split()
        if not name_parts:
            continue

        account_name = name_parts[0].strip()

        combo = (account_name, subdomain)
        if combo in seen_combos:
            continue
        seen_combos.add(combo)

        club_display_name = format_club_name(subdomain)

        if account_name in clubs:
            key = f"{account_name} ({subdomain})"
        else:
            key = account_name

        clubs[key] = {
            "name": club_display_name,
            "url": url,
            "subdomain": subdomain,
            "full_name": text,
        }

    if clubs:
        _print(f"  ✓ Discovered {len(clubs)} account/club combinations")
    else:
        print("  No valid account/club links found", file=sys.stderr)

    return clubs

def discover_clubs(username: str, password: str, debug: bool = False) -> dict:
    """Discover all accounts and their clubs."""
    _print("Discovering accounts and clubs...")

    session = MyclubSession()
    if not login(session, username, password, debug=debug):
        return {}

    if debug:
        _dump_page_debug(session, "/tmp/myclub-home-page")

    return parse_clubs_from_html(session.last_html)

# ---------------------------------------------------------------------------
# Event type inference
# ---------------------------------------------------------------------------

def format_club_name(subdomain: str) -> str:
    """Format club subdomain to readable name."""
    if subdomain.islower() and len(subdomain) <= 6:
        return subdomain.upper()
    return " ".join(word.capitalize() for word in subdomain.split("-"))

def infer_event_type(category: str, name: str) -> str:
    """Infer event type from category or event name."""
    cat = category.strip().lower()
    if cat == "ottelu":
        return "game"
    if cat == "turnaus":
        return "tournament"
    if cat == "harjoitus":
        return "training"
    if cat == "muu":
        return "other"

    name_lower = name.lower()
    if any(w in name_lower for w in ["harjoituspeli", "ottelu", "peli", "match", "vs"]):
        return "game"
    if any(w in name_lower for w in ["turnaus", "tournament", "cup", "liiga"]):
        return "tournament"
    if "harjoitus" in name_lower:
        return "training"
    if any(w in name_lower for w in ["info", "kokous", "palaver", "vanhempainfo"]):
        return "meeting"
    return "training"

# ---------------------------------------------------------------------------
# Schedule fetching & parsing
# ---------------------------------------------------------------------------

def _fetch_event_details(session, events_url: str, details_path: str,
                         initial_html: str, start_date: str, end_date: str,
                         debug: bool = False) -> dict:
    """Fetch event details (day/time) from the details API endpoint."""
    # Get all event IDs from data-events, filtered to the requested range
    all_events = _extract_data_events(initial_html)
    event_ids = []
    for ev in all_events:
        month_str = ev.get("month", "")
        if not month_str:
            continue
        try:
            month_parts = month_str.split("-")
            month_date = datetime(int(month_parts[0]), int(month_parts[1]), 1).date()
            month_end = (datetime(int(month_parts[0]), int(month_parts[1]), 1)
                         + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            if is_month_in_range(month_date, month_end.date(), start_date, end_date):
                event_ids.append(str(ev["id"]))
        except (ValueError, IndexError, KeyError):
            continue

    if not event_ids:
        return {}

    # Build the details URL
    parsed = urllib.parse.urlparse(events_url)
    base = f"{parsed.scheme}://{parsed.netloc}{details_path}"
    ids_str = ",".join(event_ids)
    details_url = f"{base}?ids={ids_str}"

    _print(f"  Fetching day/time for {len(event_ids)} events...")
    try:
        html = session.get(details_url)
        if debug:
            _dump_page_debug(session, "/tmp/myclub-event-details")
        return _parse_event_bars(html)
    except Exception as e:
        print(f"    Warning: could not fetch event details: {e}", file=sys.stderr)
        return {}


def fetch_schedule(username: str, password: str, account_name: str,
                   start_date: str, end_date: str, debug: bool = False) -> dict:
    """Fetch schedule from myclub.fi."""
    _print(f"Fetching schedule for {account_name}...")

    session = MyclubSession()
    if not login(session, username, password, debug=debug):
        return {"account": account_name, "club": "", "events": []}

    if debug:
        _dump_page_debug(session, "/tmp/myclub-home-page")

    clubs = parse_clubs_from_html(session.last_html)

    if account_name not in clubs:
        print(f"Error: '{account_name}' not found", file=sys.stderr)
        print(f"Available: {', '.join(clubs.keys())}", file=sys.stderr)
        return {"account": account_name, "club": "", "events": []}

    club_info = clubs[account_name]
    club_name = club_info["name"]
    club_url = club_info["url"]

    _print(f"  ✓ Found {account_name} -> {club_name}")

    # Navigate to club — select_account redirects to the events page
    session.get(club_url)
    initial_html = session.last_html
    events_url = session.last_url

    if debug:
        _dump_page_debug(session, "/tmp/myclub-events-page")

    # Collect event bars (day/time) from the page
    html_event_data = _parse_event_bars(initial_html)

    # If no event bars on initial page, fetch details via API
    if not html_event_data:
        details_path = _extract_details_url(initial_html)
        if details_path:
            html_event_data = _fetch_event_details(
                session, events_url, details_path, initial_html,
                start_date, end_date, debug=debug,
            )

    _print("  Parsing events...")
    events = parse_events_from_html(initial_html, start_date, end_date,
                                    html_event_data=html_event_data)

    return {
        "account": account_name,
        "club": club_name,
        "start_date": start_date,
        "end_date": end_date,
        "events": events,
    }

def parse_events_from_html(html: str, start_date: str, end_date: str,
                           html_event_data: dict | None = None) -> list:
    """
    Parse events from schedule page HTML.

    Data sources:
    1. data-events JSON attribute: {id, name, group, venue, month, event_category}
    2. event-bar HTML blocks: day, time, registration status
    """
    events = []

    # Step 1: Parse event-bar HTML for day/time/registration
    if html_event_data is None:
        html_event_data = _parse_event_bars(html)
    _print(f"    Found {len(html_event_data)} events with day/time in HTML")

    # Step 2: Parse data-events JSON
    events_data = _extract_data_events(html)
    _print(f"    Found {len(events_data)} events in data-events JSON")

    # Step 3: Build events from JSON, enriched with HTML data
    json_event_ids = set()
    for event_data in events_data:
        name = event_data.get("name", "").strip()
        if not name:
            continue

        event_id = event_data.get("id")
        if event_id:
            json_event_ids.add(event_id)

        month_str = event_data.get("month", "").strip()
        if not month_str:
            continue

        try:
            month_parts = month_str.split("-")
            year = int(month_parts[0])
            month = int(month_parts[1])
        except (ValueError, IndexError):
            continue

        month_date = datetime(year, month, 1).date()
        month_end = (datetime(year, month, 1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        month_end = month_end.date()

        if not is_month_in_range(month_date, month_end, start_date, end_date):
            continue

        # Merge with HTML data
        day = None
        time_val = None
        reg_status = "unknown"
        if event_id and event_id in html_event_data:
            bar = html_event_data[event_id]
            day = bar.get("day")
            time_val = bar.get("time")
            reg_status = bar.get("registration_status", "unknown")

        events.append({
            "id": event_id,
            "name": name,
            "group": event_data.get("group", "").strip(),
            "venue": event_data.get("venue", "").strip(),
            "month": month_str,
            "day": day,
            "time": time_val,
            "event_category": event_data.get("event_category", ""),
            "type": infer_event_type(event_data.get("event_category", ""), name),
            "registration_status": reg_status,
        })

    # Step 4: Add HTML-only events (not in JSON data)
    for event_id, bar_data in html_event_data.items():
        if event_id in json_event_ids:
            continue

        day = bar_data.get("day")
        time_val = bar_data.get("time")

        if day and not is_date_in_range_finnish(day, start_date, end_date):
            continue

        name = bar_data.get("name", f"Event {event_id}")
        events.append({
            "id": event_id,
            "name": name,
            "group": bar_data.get("group", ""),
            "venue": bar_data.get("venue", ""),
            "month": None,
            "day": day,
            "time": time_val,
            "event_category": None,
            "type": infer_event_type("", name),
            "registration_status": bar_data.get("registration_status", "unknown"),
        })

    # Deduplicate
    seen = set()
    unique_events = []
    for e in events:
        key = e.get("id") or (e["name"], e.get("venue"), e.get("day"))
        if key not in seen:
            seen.add(key)
            unique_events.append(e)

    # Sort by day/time, then by month
    def sort_key(e):
        if e.get("day"):
            try:
                day_str = e["day"].rstrip(".")
                day_parts = day_str.split(".")
                day_num = int(day_parts[0])
                month_num = int(day_parts[1]) if len(day_parts) > 1 else 1
                return (month_num, day_num, e.get("time", "00:00"))
            except (ValueError, IndexError):
                pass
        if e.get("month"):
            try:
                parts = e["month"].split("-")
                return (int(parts[1]), 1, e.get("name", ""))
            except (ValueError, IndexError):
                pass
        return (99, 99, "")

    unique_events.sort(key=sort_key)
    _print(f"    {len(unique_events)} unique events total")
    return unique_events

# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def is_date_in_range_finnish(date_str: str, start_date: str, end_date: str) -> bool:
    """Check if Finnish date string (e.g., "15.3." or "15.3") is within range."""
    try:
        date_clean = date_str.strip().rstrip(".")
        parts = date_clean.split(".")
        if len(parts) < 2:
            return True
        day = int(parts[0])
        month = int(parts[1])
        start_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        for year in range(start_obj.year, end_obj.year + 1):
            try:
                date_obj = datetime(year, month, day).date()
            except ValueError:
                continue
            if start_obj <= date_obj <= end_obj:
                return True
        return False
    except (ValueError, AttributeError, IndexError):
        return True

def is_month_in_range(month_start, month_end, start_date: str, end_date: str) -> bool:
    """Check if a month overlaps with the requested range."""
    try:
        start_obj = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        return not (month_end < start_obj or month_start > end_obj)
    except (ValueError, AttributeError):
        return True

def parse_period(period_str: str) -> tuple:
    """Convert period string to (start_date, end_date)."""
    today = datetime.now().date()
    next_month_first = (today.replace(day=1) + timedelta(days=32)).replace(day=1)
    period_map = {
        "this week": (today - timedelta(days=today.weekday()), today + timedelta(days=6 - today.weekday())),
        "next week": (today + timedelta(days=7 - today.weekday()), today + timedelta(days=13 - today.weekday())),
        "this month": (today.replace(day=1), (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)),
        "next month": (next_month_first, (next_month_first + timedelta(days=32)).replace(day=1) - timedelta(days=1)),
    }
    if period_str.lower() in period_map:
        start, end = period_map[period_str.lower()]
        return str(start), str(end)
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    return str(start), str(end)

# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def format_output(schedule: dict) -> str:
    """Format schedule as human-readable text."""
    account = schedule["account"]
    club = schedule["club"]
    events = schedule["events"]

    if not events:
        return f"No events found for {account} ({club}) in the requested period."

    output = f"📅 {account}'s Schedule ({club})\n"
    output += f"   {schedule['start_date']} to {schedule['end_date']}\n\n"

    for event in events:
        emoji = {
            "training": "🏃",
            "game": "⚽",
            "tournament": "🏆",
            "meeting": "👥",
            "other": "📌",
        }.get(event["type"], "📌")

        if event.get("day"):
            output += f"{emoji} {event['day']}"
            if event.get("time"):
                output += f"  {event['time']}"
            output += "\n"
        else:
            output += f"{emoji} {event['month']}\n"

        output += f"   {event['name']}\n"

        if event.get("group"):
            output += f"   👥 Group: {event['group']}\n"
        if event.get("venue"):
            output += f"   📍 {event['venue']}\n"
        if event.get("event_category"):
            output += f"   📂 {event['event_category']}\n"

        output += "\n"

    return output

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Fetch myclub.fi schedules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 fetch_myclub.py setup --username user@example.com --password pass
  python3 fetch_myclub.py discover
  python3 fetch_myclub.py fetch --account Kaarlo --period "this week"
        """,
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output (HTML dumps, cookies)")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    setup = subparsers.add_parser("setup", help="Store credentials")
    setup.add_argument("--username", required=True, help="myclub.fi email")
    setup.add_argument("--password", required=True, help="myclub.fi password")

    discover = subparsers.add_parser("discover", help="List accounts and clubs")
    discover.add_argument("--json", action="store_true", help="JSON output")

    fetch = subparsers.add_parser("fetch", help="Fetch schedule")
    fetch.add_argument("--account", required=True, help="Account name")
    fetch.add_argument("--period", default="this week", help="Period")
    fetch.add_argument("--start", help="Start date (YYYY-MM-DD)")
    fetch.add_argument("--end", help="End date (YYYY-MM-DD)")
    fetch.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if args.command == "setup":
        save_config(args.username, args.password)

    elif args.command == "discover":
        global _quiet
        _quiet = args.json
        config = load_config()
        clubs = discover_clubs(config["username"], config["password"], debug=args.debug)
        if not clubs:
            print("No clubs found", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(clubs, indent=2, ensure_ascii=False))
        else:
            _print("\n📚 Available accounts and clubs:\n")
            for account, info in clubs.items():
                _print(f"  {account}:")
                _print(f"    Club: {info['name']}")
                _print(f"    URL: {info['url']}")
                _print()

    elif args.command == "fetch":
        _quiet = args.json
        config = load_config()
        start_date, end_date = (args.start, args.end) if args.start and args.end else parse_period(args.period)
        schedule = fetch_schedule(
            config["username"], config["password"], args.account,
            start_date, end_date, debug=args.debug,
        )
        if args.json:
            print(json.dumps(schedule, indent=2, ensure_ascii=False))
        else:
            print(format_output(schedule))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
