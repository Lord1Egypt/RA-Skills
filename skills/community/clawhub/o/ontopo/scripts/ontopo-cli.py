#!/usr/bin/env python3
"""
Ontopo CLI - Search Israeli restaurants and check table availability.

A complete, self-contained CLI for interacting with the Ontopo restaurant
booking platform API.
"""

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

try:
    import httpx
except ImportError:
    print("Error: httpx is required. Install with: pip install httpx", file=sys.stderr)
    sys.exit(1)


# =============================================================================
# CONSTANTS
# =============================================================================

BASE_URL = "https://ontopo.com/api"
WEBSITE_URL = "https://ontopo.com"
ISRAEL_DISTRIBUTOR_SLUG = "15171493"  # Required for venue search
ISRAEL_MARKETPLACE_ID = "29421469"   # Default (Tel Aviv) for batch availability search

CATEGORIES = [
    "restaurants", "bars", "fine_dining", "happy_hour",
    "brunch", "business", "kosher", "events"
]

# Authoritative city data from Ontopo SSR __INITIAL_STATE__
# Each entry: (marketplace_id, geocode_key, display_label)
# The slug (dict key) matches Ontopo's URL pattern: /he/il/{slug}/restaurants
_CITY_DATA = {
    "tel-aviv":       ("29421469", "telavivjaffa",       "תל אביב"),
    "jerusalem":      ("29384685", "jerusalem",          "ירושלים"),
    "haifa":          ("11243454", "haifa",               "חיפה"),
    "herzeliya":      ("62204663", "herzeliya",           "הרצליה"),
    "raanana":        ("71499188", "raanana",             "רעננה"),
    "ramatgan":       ("87918421", "rag-giv-area",        "רמת גן - גבעתיים"),
    "natanya":        ("19467447", "netanya_area",        "נתניה"),
    "ashdod":         ("93786391", "ashdod",              "אשדוד"),
    "beer-sheva":     ("83166822", "beer_sheva",          "באר שבע"),
    "eilat":          ("71154151", "eilat_area",          "אילת"),
    "modiin":         ("49473533", "modiin_area",         "מודיעין והסביבה"),
    "rehovot":        ("58943955", "rehovot",             "רחובות"),
    "rishon_lezion":  ("39514882", "rishon_lezion",       "ראשון לציון"),
    "petah_tikva":    ("74902764", "petah_tikva_area",    "פתח תקווה"),
    "holon":          ("60235869", "holon-batyam-area",   "חולון - בת ים"),
    "kfar_saba":      ("45164735", "kfarsaba",            "כפר סבא"),
    "hod_hasharon":   ("77097784", "hod_hasharon",        "הוד השרון"),
    "ramat_hasharon":  ("64031461", "ramat_hasharon",     "רמת השרון"),
    "caesarya":       ("86032396", "caesarea_area",        "קיסריה - חדרה והסביבה"),
    "ness_ziona":     ("47865336", "ness_ziona",          "נס ציונה"),
    "kiryat_ono":     ("29033809", "kiryat_ono_area",     "קריית אונו"),
    "kineret":        ("92127549", "golan_kineret",       "כנרת ורמת הגולן"),
    "the_north":      ("45577648", "the_north",           "אזור הצפון"),
    "south":          ("65424368", "south",               "אזור הדרום"),
    "merkaz":         ("41581793", "merkaz",              "אזור המרכז"),
    "hashfela":       ("74908782", "hashfela",            "אזור השפלה"),
    "hasharon":       ("75635900", "hasharon",            "אזור השרון"),
}

# User-friendly aliases (hyphenated → canonical slug)
_CITY_ALIASES = {
    "herzliya": "herzeliya",
    "ramat-gan": "ramatgan",
    "netanya": "natanya",
    "rishon-lezion": "rishon_lezion",
    "petah-tikva": "petah_tikva",
    "kfar-saba": "kfar_saba",
    "hod-hasharon": "hod_hasharon",
    "ramat-hasharon": "ramat_hasharon",
    "caesarea": "caesarya",
    "ness-ziona": "ness_ziona",
    "kiryat-ono": "kiryat_ono",
    "north": "the_north",
    "bat-yam": "holon",  # Same marketplace
}

def _resolve_city(city: str) -> str:
    """Resolve user input to canonical city slug."""
    city = city.lower().strip()
    return _CITY_ALIASES.get(city, city)

CITIES = sorted(_CITY_DATA.keys())
CITY_GEOCODES = {slug: data[1] for slug, data in _CITY_DATA.items()}
CITY_MARKETPLACE_IDS = {slug: data[0] for slug, data in _CITY_DATA.items()}

# Substrings matched against a venue's address to filter search results by city.
# The venue_search endpoint has no city parameter, so `search --city` is applied
# client-side. Region slugs below cover several municipalities and cannot be
# matched from an address string; they are handled separately.
_CITY_ADDRESS_TERMS = {
    "tel-aviv":       ["tel aviv", "תל אביב", "jaffa", "יפו"],
    "jerusalem":      ["jerusalem", "ירושלים"],
    "haifa":          ["haifa", "חיפה"],
    "herzeliya":      ["herzliya", "herzeliya", "הרצליה"],
    "raanana":        ["raanana", "ra'anana", "רעננה"],
    "ramatgan":       ["ramat gan", "givatayim", "רמת גן", "גבעתיים"],
    "natanya":        ["netanya", "natanya", "נתניה"],
    "ashdod":         ["ashdod", "אשדוד"],
    "beer-sheva":     ["beer sheva", "be'er sheva", "beersheba", "באר שבע"],
    "eilat":          ["eilat", "אילת"],
    "modiin":         ["modiin", "modi'in", "מודיעין"],
    "rehovot":        ["rehovot", "רחובות"],
    "rishon_lezion":  ["rishon", "ראשון לציון"],
    "petah_tikva":    ["petah tikva", "petach tikva", "פתח תקווה"],
    "holon":          ["holon", "bat yam", "חולון", "בת ים"],
    "kfar_saba":      ["kfar saba", "כפר סבא"],
    "hod_hasharon":   ["hod hasharon", "הוד השרון"],
    "ramat_hasharon": ["ramat hasharon", "רמת השרון"],
    "caesarya":       ["caesarea", "hadera", "קיסריה", "חדרה"],
    "ness_ziona":     ["ness ziona", "nes ziona", "נס ציונה"],
    "kiryat_ono":     ["kiryat ono", "קריית אונו", "קרית אונו"],
}

# Multi-municipality regions: valid for `available` (they map to a marketplace)
# but not filterable from an address string in `search`.
REGION_SLUGS = {s for s in _CITY_DATA if s not in _CITY_ADDRESS_TERMS}


def city_matches_address(city_slug: str, address: str) -> bool:
    """True if an address appears to be in the given city slug."""
    terms = _CITY_ADDRESS_TERMS.get(city_slug)
    if not terms:
        return True
    addr = (address or "").lower()
    return any(term in addr for term in terms)


# =============================================================================
# STRUCTURED OUTPUT
# =============================================================================
# Every command emits the same JSON envelope so an agent can parse one shape:
#
#   {"ok": bool, "command": str, "criteria": {...},
#    "results": [...], "count": int, "warning": str|null, "error": str|null}
#
# Venue objects are flat and always carry venue_id / name / booking_url where
# known, so a result from any command can be fed straight into any other.
# Pass --raw for the unprocessed upstream payload.

SLOT_STATUS = {"seat": "available", "standby": "waitlist"}


def make_booking_url(page_id: Any, locale: str = "en") -> Optional[str]:
    """Build the public booking URL for a page id."""
    if not page_id:
        return None
    return f"https://ontopo.com/{locale}/il/page/{page_id}"


def extract_slots(availability: Optional[Dict]) -> List[Dict]:
    """Flatten areas[].options[] into slots grouped by time and status.

    Returns [{time, status, areas: [...]}]. Grouping keeps the seating choice
    (bar vs. table vs. courtyard) while avoiding one object per area per time,
    which is where most of the upstream payload size comes from.
    """
    if not isinstance(availability, dict):
        return []

    grouped: Dict[Tuple[str, str], List[str]] = {}
    for area in availability.get("areas") or []:
        if not isinstance(area, dict):
            continue
        area_name = area.get("name") or area.get("id") or "Unknown"
        for opt in area.get("options") or []:
            if not isinstance(opt, dict):
                continue
            status = SLOT_STATUS.get(opt.get("method"))
            if not status or not opt.get("time"):
                continue
            key = (format_time_display(opt["time"]), status)
            if area_name not in grouped.setdefault(key, []):
                grouped[key].append(area_name)

    return [
        {"time": time, "status": status, "areas": areas}
        for (time, status), areas in sorted(grouped.items())
    ]


def make_envelope(
    command: str,
    criteria: Optional[Dict] = None,
    results: Optional[List] = None,
    error: Optional[str] = None,
    warning: Optional[str] = None,
    **extra: Any
) -> Dict:
    """Build the standard response envelope."""
    env = {
        "ok": error is None,
        "command": command,
        "criteria": {k: v for k, v in (criteria or {}).items() if v is not None},
        "results": results if results is not None else [],
        "count": len(results) if results is not None else 0,
    }
    env.update({k: v for k, v in extra.items() if v is not None})
    env["warning"] = warning
    env["error"] = error
    return env


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def parse_time(time_str: str) -> str:
    """
    Parse flexible time input and return HHMM format.
    Accepts: HH:MM, HHMM, "19:00", "7pm", "7:30pm", "19"
    """
    time_str = time_str.strip().lower().replace('"', '').replace("'", "")

    # Handle am/pm format
    is_pm = 'pm' in time_str
    is_am = 'am' in time_str
    time_str = time_str.replace('pm', '').replace('am', '').strip()

    # Try different patterns
    patterns = [
        (r'^(\d{1,2}):(\d{2})$', lambda m: (int(m.group(1)), int(m.group(2)))),
        (r'^(\d{4})$', lambda m: (int(m.group(1)[:2]), int(m.group(1)[2:]))),
        (r'^(\d{1,2})$', lambda m: (int(m.group(1)), 0)),
    ]

    for pattern, extractor in patterns:
        match = re.match(pattern, time_str)
        if match:
            hour, minute = extractor(match)
            break
    else:
        raise ValueError(f"Invalid time format: {time_str}. Use HH:MM, HHMM, or 7pm")

    # Apply am/pm conversion
    if is_pm and hour < 12:
        hour += 12
    elif is_am and hour == 12:
        hour = 0

    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError(f"Invalid time: {hour:02d}:{minute:02d}")

    return f"{hour:02d}{minute:02d}"


# Weekday names accepted by parse_date. "friday" means the next Friday,
# counting today as a candidate: asking for Friday on a Friday means tonight.
# Taking the name directly avoids the +N arithmetic that callers (human or
# agent) routinely get wrong by a day.
_WEEKDAYS = {name: i for i, names in enumerate([
    ("monday", "mon"), ("tuesday", "tue", "tues"), ("wednesday", "wed"),
    ("thursday", "thu", "thur", "thurs"), ("friday", "fri"),
    ("saturday", "sat"), ("sunday", "sun"),
]) for name in names}


def parse_date(date_str: str) -> str:
    """
    Parse date input (YYYY-MM-DD) and return YYYYMMDD format.
    Also accepts: today, tomorrow, relative days like +3, or a weekday name
    like friday (the next occurrence, today included).
    """
    date_str = date_str.strip().lower()

    if date_str == 'today':
        dt = datetime.now()
    elif date_str == 'tomorrow':
        dt = datetime.now() + timedelta(days=1)
    elif date_str in _WEEKDAYS:
        now = datetime.now()
        dt = now + timedelta(days=(_WEEKDAYS[date_str] - now.weekday()) % 7)
    elif date_str.startswith('+'):
        days = int(date_str[1:])
        dt = datetime.now() + timedelta(days=days)
    else:
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}. Use YYYY-MM-DD, "
                             f"today, tomorrow, +N, or a weekday name like friday")

    return dt.strftime('%Y%m%d')


def format_date_display(date_str: str) -> str:
    """Convert YYYYMMDD to readable format."""
    try:
        dt = datetime.strptime(date_str, '%Y%m%d')
        return dt.strftime('%Y-%m-%d (%A)')
    except ValueError:
        return date_str


def format_time_display(time_str: str) -> str:
    """Convert HHMM to HH:MM format."""
    if len(time_str) == 4:
        return f"{time_str[:2]}:{time_str[2:]}"
    return time_str


def format_price(price: Any) -> str:
    """Format price for display."""
    if price is None:
        return "N/A"
    try:
        return f"{float(price):.0f} ILS"
    except (ValueError, TypeError):
        return str(price)


def print_table(headers: List[str], rows: List[List[str]], min_widths: Optional[List[int]] = None) -> str:
    """Create a markdown-style table."""
    if not rows:
        return "No data to display."

    # Calculate column widths
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(str(cell)))

    if min_widths:
        for i, mw in enumerate(min_widths):
            if i < len(widths):
                widths[i] = max(widths[i], mw)

    # Build table
    lines = []

    # Header
    header_line = "| " + " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers)) + " |"
    lines.append(header_line)

    # Separator
    sep_line = "|" + "|".join("-" * (w + 2) for w in widths) + "|"
    lines.append(sep_line)

    # Rows
    for row in rows:
        row_cells = []
        for i, cell in enumerate(row):
            if i < len(widths):
                row_cells.append(str(cell).ljust(widths[i]))
        line = "| " + " | ".join(row_cells) + " |"
        lines.append(line)

    return "\n".join(lines)


# =============================================================================
# API CLIENT
# =============================================================================

class OntopoClient:
    """Async client for Ontopo API."""

    def __init__(self, locale: str = "en"):
        self.locale = locale
        self.token: Optional[str] = None
        self._venue_page_cache: Dict[str, str] = {}
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def _ensure_auth(self) -> None:
        """Ensure we have a valid JWT token."""
        if self.token:
            return

        response = await self._request("POST", "/loginAnonymously", auth_required=False)
        self.token = response.get("jwt_token")
        if not self.token:
            raise RuntimeError("Failed to obtain authentication token")

    async def _request(
        self,
        method: str,
        endpoint: str,
        body: Optional[Dict] = None,
        params: Optional[Dict] = None,
        auth_required: bool = True,
        retries: int = 3
    ) -> Any:
        """Make an API request with retry logic."""
        if auth_required:
            await self._ensure_auth()

        url = f"{BASE_URL}/{endpoint.lstrip('/')}"
        headers = {"Content-Type": "application/json"}

        if auth_required and self.token:
            headers["token"] = self.token

        for attempt in range(retries):
            try:
                if method == "GET":
                    response = await self._client.get(url, params=params, headers=headers)
                elif method == "POST":
                    response = await self._client.post(url, json=body, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                if response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = 2 ** attempt
                    await asyncio.sleep(wait_time)
                    continue

                if response.status_code == 401:
                    # Token expired - refresh and retry
                    self.token = None
                    await self._ensure_auth()
                    continue

                response.raise_for_status()

                if response.content:
                    return response.json()
                return {}

            except httpx.HTTPStatusError as e:
                if attempt == retries - 1:
                    raise RuntimeError(f"API error: {e.response.status_code} - {e.response.text}")
                await asyncio.sleep(1)
            except httpx.RequestError as e:
                if attempt == retries - 1:
                    raise RuntimeError(f"Network error: {e}")
                await asyncio.sleep(1)

        raise RuntimeError("Max retries exceeded")

    async def search_venues(self, query: str) -> List[Dict]:
        """Search for venues by query.

        The endpoint has no city parameter; callers filter by city client-side
        via city_matches_address().
        """
        params = {
            "slug": ISRAEL_DISTRIBUTOR_SLUG,
            "version": "1",
            "terms": query,
            "locale": self.locale
        }

        response = await self._request("GET", "/venue_search", params=params, auth_required=False)

        venues = response if isinstance(response, list) else response.get("venues", response.get("results", []))
        return venues if isinstance(venues, list) else []

    async def get_venue_profile(self, venue_id: str) -> Dict:
        """Get venue profile including page mappings."""
        params = {
            "slug": venue_id,
            "version": "1",
            "locale": self.locale
        }
        return await self._request("GET", "/venue_profile", params=params, auth_required=False)

    async def get_page(self, page_id: str) -> Dict:
        """Get page/venue details using slug_content API."""
        params = {
            "slug": page_id,
            "locale": self.locale
        }
        return await self._request("GET", "/slug_content", params=params, auth_required=False)

    async def resolve_page_id(self, venue_id: str, validate: bool = False) -> str:
        """Resolve venue_id to page_id for booking operations.

        With validate=True, an input that cannot be resolved through the venue
        profile is only accepted if it is itself a live page (one get_page
        call); otherwise ValueError is raised. Without validation the input is
        returned as-is - safe wherever a downstream API call rejects bad ids
        anyway (check/info), but never safe for building shareable URLs:
        ids taken from `available` output are ephemeral search-post ids, and
        pasting them into a page URL yields a dead link.
        """
        if venue_id in self._venue_page_cache:
            return self._venue_page_cache[venue_id]

        try:
            profile = await self.get_venue_profile(venue_id)
            pages = profile.get("pages", [])
            # Look for a page with content_type="reservation"
            for page in pages:
                if page.get("content_type") == "reservation":
                    page_slug = page.get("slug", page.get("id", venue_id))
                    self._venue_page_cache[venue_id] = page_slug
                    return page_slug
            # Fallback to first page if no reservation type found
            if pages:
                page_slug = pages[0].get("slug", pages[0].get("id", venue_id))
                self._venue_page_cache[venue_id] = page_slug
                return page_slug
        except Exception:
            pass

        # Fallback: the input may already be a page id (the documented
        # `url <page_id>` flow relies on this).
        if validate:
            # A live booking page identifies itself: content_type
            # "reservation" plus a slug_venue back-reference. Search-post ids
            # from `available` output also answer get_page, but as a bare
            # content_type "page" with no slug_venue - and a URL built from
            # one renders nothing. Recover those through the venue name.
            bad = ValueError(
                f"'{venue_id}' does not resolve to a booking page. "
                f"Ids from `available` output are temporary search ids - "
                f"use that output's page_slug instead, or find the venue "
                f"with: ontopo-cli.py search <name>"
            )
            try:
                page = await self.get_page(venue_id)
            except Exception:
                raise bad
            if page.get("content_type") == "reservation" and page.get("slug_venue"):
                self._venue_page_cache[venue_id] = venue_id
                return venue_id
            title = page.get("title")
            if title:
                try:
                    venue_slug = await self.resolve_venue_name(title)
                    if venue_slug != venue_id:
                        recovered = await self.resolve_page_id(venue_slug)
                        if recovered != venue_slug:
                            self._venue_page_cache[venue_id] = recovered
                            return recovered
                except Exception:
                    pass
            raise bad

        self._venue_page_cache[venue_id] = venue_id
        return venue_id

    async def resolve_venue_name(self, venue_input: str) -> str:
        """Resolve venue name or ID to a usable venue ID.

        If input is numeric, return as-is.
        If input is text (e.g., 'taizu'), search and return first match's slug.
        """
        # If it's already numeric, use directly
        if venue_input.isdigit():
            return venue_input

        # Search for the venue name
        try:
            results = await self.search_venues(venue_input)
            if results:
                # Return the first match's slug
                first = results[0]
                slug = first.get("slug", first.get("id", venue_input))
                return slug
        except Exception:
            pass

        # Fallback: return as-is and let downstream handle errors
        return venue_input

    async def create_search_token(
        self,
        date: str,
        time: str,
        size: int,
        geocodes: Optional[List[str]] = None,
        category: Optional[str] = None,
        venue_type: Optional[str] = None,
        city: Optional[str] = None
    ) -> str:
        """Create a search session for batch availability.

        Args:
            venue_type: Filter by venue tag (e.g. 'safe_zone' for מרחב מוגן,
                        'kosher', 'vegetarian', 'wine_bar', etc.)
            city: City slug for marketplace routing (each city has its own marketplace).
        """
        marketplace_id = CITY_MARKETPLACE_IDS.get(city, ISRAEL_MARKETPLACE_ID) if city else ISRAEL_MARKETPLACE_ID
        body = {
            "marketplace_id": marketplace_id,
            "criteria": {
                "date": date,
                "time": time,
                "size": str(size)  # Must be string
            },
            "locale": self.locale,
            "traits": ["reservation"],
            "analytics": {
                "distributor_id": "il",
                "platform": "web"
            }
        }
        if geocodes:
            body["geocodes"] = geocodes
        if category:
            body["primary"] = [category]
        if venue_type:
            body["venue_type"] = venue_type

        response = await self._request("POST", "/search_token", body=body)
        return response.get("search_id", response.get("token", ""))

    async def get_search_results(self, search_id: str) -> Dict:
        """Get search results with availability."""
        body = {"search_id": search_id}
        response = await self._request("POST", "/search_request", body=body)
        return response

    async def check_availability(
        self,
        venue_id: str,
        date: str,
        time: str,
        size: int
    ) -> Dict:
        """Check specific venue availability."""
        page_id = await self.resolve_page_id(venue_id)

        # The API requires specific structure:
        # - slug at top level (not 'venue')
        # - criteria object with size/date/time as STRINGS
        body = {
            "slug": page_id,
            "locale": self.locale,
            "criteria": {
                "size": str(size),  # Must be string!
                "date": date,       # YYYYMMDD format
                "time": time,       # HHMM format
            }
        }
        return await self._request("POST", "/availability_search", body=body)

    async def get_venue_info(self, venue_id: str) -> Dict:
        """Get detailed venue information."""
        page_id = await self.resolve_page_id(venue_id)
        return await self.get_page(page_id)


# =============================================================================
# COMMAND HANDLERS
# =============================================================================

class CommandHandler:
    """Handle CLI commands and format output."""

    def __init__(self, client: OntopoClient, json_output: bool = False,
                 raw_output: bool = False):
        self.client = client
        self.json_output = json_output
        self.raw_output = raw_output

    def _output(self, data: Any, markdown: str) -> None:
        """Output data in JSON or markdown format."""
        if self.json_output:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(markdown)

    async def cmd_cities(self) -> None:
        """List supported cities."""
        cities_with_labels = [
            {"slug": slug, "label": _CITY_DATA[slug][2]}
            for slug in CITIES
        ]
        aliases = {v: k for k, v in _CITY_ALIASES.items()}
        data = {"cities": [c["slug"] for c in cities_with_labels], "count": len(CITIES)}
        if self.json_output and not self.raw_output:
            self._output(make_envelope(
                "cities",
                results=[{"slug": c["slug"], "label": c["label"],
                          "is_region": c["slug"] in REGION_SLUGS}
                         for c in cities_with_labels],
            ), "")
            return

        if self.json_output:
            self._output(data, "")
        else:
            print(f"Supported Cities ({len(CITIES)}):")
            print("-" * 40)
            for i, c in enumerate(cities_with_labels, 1):
                alias = aliases.get(c["slug"])
                alias_str = f" (or: {alias})" if alias else ""
                print(f"  {i:2}. {c['slug']:20s} {c['label']}{alias_str}")

    async def cmd_categories(self) -> None:
        """List supported categories."""
        data = {"categories": CATEGORIES, "count": len(CATEGORIES)}
        if self.json_output and not self.raw_output:
            self._output(make_envelope("categories", results=list(CATEGORIES)), "")
            return

        if self.json_output:
            self._output(data, "")
        else:
            print(f"Supported Categories ({len(CATEGORIES)}):")
            print("-" * 40)
            for cat in CATEGORIES:
                print(f"  - {cat}")

    async def cmd_search(self, query: str, city: Optional[str] = None) -> None:
        """Search for venues."""
        warning = None
        if city:
            city = _resolve_city(city)
            if city not in _CITY_DATA:
                msg = (f"Unknown city '{city}'. "
                       f"Run: ontopo-cli.py cities")
                if self.json_output:
                    self._output(make_envelope(
                        "search", criteria={"query": query}, error=msg), "")
                else:
                    print(msg)
                return
            if city in REGION_SLUGS:
                warning = (f"'{city}' is a multi-city region and cannot filter search "
                           f"results; showing all matches. Use 'available --city {city}' "
                           f"for region-wide availability.")

        venues = await self.client.search_venues(query)

        if city and city not in REGION_SLUGS:
            venues = [v for v in venues
                      if city_matches_address(city, v.get("address", ""))]

        if not venues:
            msg = f"No venues found for '{query}'"
            if city:
                msg += f" in {city}"
            msg += "."
            if self.json_output:
                self._output(make_envelope(
                    "search", criteria={"query": query, "city": city},
                    results=[], warning=warning, message=msg), "")
            else:
                print(msg)
            return

        if self.json_output:
            if self.raw_output:
                self._output({"venues": venues, "count": len(venues)}, "")
            else:
                results = [{
                    "venue_id": str(v.get("slug", "")),
                    "name": v.get("title") or v.get("name") or "Unknown",
                    "address": v.get("address") or None,
                } for v in venues]
                self._output(make_envelope(
                    "search",
                    criteria={"query": query, "city": city},
                    results=results,
                    warning=warning,
                    hint="Use 'url <venue_id>' for a booking link, "
                         "'check <venue_id> <date> <time>' for availability.",
                ), "")
        else:
            print(f"Search Results for '{query}':")
            if city:
                print(f"City: {city}")
            if warning:
                print(f"Note: {warning}")
            print()

            rows = []
            for v in venues[:20]:  # Limit display
                venue_id = v.get("slug", v.get("id", v.get("venue_id", "N/A")))
                name = v.get("title", v.get("name", "Unknown"))[:40]
                address = v.get("address", "")[:30]
                rows.append([str(venue_id), name, address])

            table = print_table(
                ["Venue ID", "Name", "Address"],
                rows,
                [12, 40, 30]
            )
            print(table)

            if len(venues) > 20:
                print(f"\n... and {len(venues) - 20} more results")

    async def cmd_available(
        self,
        date: str,
        time: str,
        city: Optional[str] = None,
        party_size: int = 2,
        venue_type: Optional[str] = None
    ) -> None:
        """Search for available venues."""
        api_date = parse_date(date)
        api_time = parse_time(time)

        # Resolve city alias to canonical slug
        if city:
            city = _resolve_city(city)

        # Get geocode for city (single value, wrapped in list for API)
        geocode = CITY_GEOCODES.get(city) if city else None
        geocodes = [geocode] if geocode else None

        try:
            search_id = await self.client.create_search_token(
                api_date, api_time, party_size, geocodes,
                venue_type=venue_type, city=city
            )

            if not search_id:
                raise RuntimeError("Failed to create search session")

            response = await self.client.get_search_results(search_id)
            # Extract posts array from response
            results = response.get("posts", response.get("results", []))
            if not isinstance(results, list):
                results = []
            # Total venues matching the filter (including unavailable)
            total_venues = response.get("total")
        except Exception as e:
            if self.json_output:
                self._output(make_envelope("available", error=str(e)), "")
            else:
                print(f"Error searching availability: {e}")
            return

        # Count venues with actual bookable time slots (not just "Check venue")
        def _has_bookable_slots(venue):
            avail = venue.get("availability", {})
            for area in avail.get("areas", []):
                for opt in area.get("options", []):
                    if isinstance(opt, dict) and opt.get("method") == "seat" and opt.get("time"):
                        return True
            return False

        bookable_count = sum(1 for r in results if _has_bookable_slots(r))

        if self.json_output:
            if self.raw_output:
                self._output({
                    "date": api_date, "time": api_time,
                    "party_size": party_size, "city": city,
                    "venue_type": venue_type, "venues": results,
                    "count": len(results), "bookable_count": bookable_count,
                    "total_venues": total_venues
                }, "")
            else:
                norm = []
                for r in results:
                    post = r.get("post", r) if isinstance(r, dict) else {}
                    page_id = post.get("page_slug")
                    norm.append({
                        "venue_id": str(post.get("slug", "")),
                        "name": post.get("venue_name") or post.get("title") or "Unknown",
                        "page_id": str(page_id) if page_id else None,
                        "booking_url": make_booking_url(page_id, self.client.locale),
                        "slots": extract_slots(r.get("availability")),
                    })
                self._output(make_envelope(
                    "available",
                    criteria={
                        "date": format_date_display(api_date),
                        "time": format_time_display(api_time),
                        "party_size": party_size,
                        "city": city,
                        "venue_type": venue_type,
                    },
                    results=norm,
                    bookable_count=bookable_count,
                    total_venues=total_venues,
                    hint="Share booking_url values verbatim. venue_id is a "
                         "temporary search id - a URL built from it will not "
                         "load.",
                ), "")
        else:
            print(f"Available Venues")
            print(f"Date: {format_date_display(api_date)}")
            print(f"Time: {format_time_display(api_time)}")
            print(f"Party Size: {party_size}")
            if city:
                print(f"City: {city}")
            if venue_type:
                label = "מרחב מוגן (Safe Zone)" if venue_type == "safe_zone" else venue_type
                print(f"Filter: {label}")
                if total_venues:
                    print(f"Total venues with filter: {total_venues} ({bookable_count} with bookable slots)")
            print()

            if not results:
                print("No available venues found for this search.")
                return

            rows = []
            for r in results[:25]:
                # Structure: {"post": {...}, "availability": {...}}
                post = r.get("post", r)
                avail = r.get("availability", {})

                venue_id = post.get("page_slug", post.get("slug", "N/A"))
                name = post.get("venue_name", post.get("title", "Unknown"))[:35]

                # Get available times from areas[].options[] where method="seat"
                areas = avail.get("areas", [])
                times_set = set()
                for area in areas:
                    for opt in area.get("options", []):
                        if isinstance(opt, dict) and opt.get("method") == "seat":
                            time_val = opt.get("time", "")
                            if time_val:
                                times_set.add(format_time_display(time_val))

                slot_times = ", ".join(sorted(times_set)[:5]) if times_set else "Check venue"
                rows.append([str(venue_id), name, slot_times[:30]])

            table = print_table(
                ["ID", "Name", "Available Times"],
                rows,
                [10, 35, 30]
            )
            print(table)

    async def cmd_check(
        self,
        venue_id: str,
        date: str,
        time: Optional[str] = None,
        party_size: int = 2
    ) -> None:
        """Check availability for a specific venue."""
        # Resolve venue name to ID if needed
        resolved_id = await self.client.resolve_venue_name(venue_id)

        api_date = parse_date(date)
        api_time = parse_time(time) if time else "1900"

        try:
            result = await self.client.check_availability(
                resolved_id, api_date, api_time, party_size
            )
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                if venue_id != resolved_id:
                    error_msg = f"Venue '{venue_id}' resolved to ID {resolved_id}, but not found. Try: ontopo-cli.py search <name>"
                else:
                    error_msg = f"Venue not found: {venue_id}. Try: ontopo-cli.py search <name>"
            if self.json_output:
                self._output(make_envelope(
                    "check", criteria={"venue_input": venue_id},
                    error=error_msg), "")
            else:
                print(f"Error: {error_msg}")
            return

        data = {
            "venue_id": resolved_id,
            "venue_input": venue_id,
            "date": api_date,
            "time": api_time,
            "party_size": party_size,
            "availability": result
        }
        if self.json_output and not self.raw_output:
            # The availability response carries no page id; resolve it here so
            # the caller gets a booking link without a follow-up `url` call.
            try:
                page_id = await self.client.resolve_page_id(resolved_id)
            except Exception:
                page_id = None
            slots = extract_slots(result)
            self._output(make_envelope(
                "check",
                criteria={
                    "venue_id": resolved_id, "venue_input": venue_id,
                    "date": format_date_display(api_date),
                    "time": format_time_display(api_time),
                    "party_size": party_size,
                },
                results=[{
                    "venue_id": resolved_id,
                    "booking_url": make_booking_url(page_id, self.client.locale),
                    "available": any(sl["status"] == "available" for sl in slots),
                    "slots": slots,
                }],
            ), "")
            return

        if self.json_output:
            self._output(data, "")
        else:
            print(f"Availability Check")
            if venue_id != resolved_id:
                print(f"Venue: {venue_id} (ID: {resolved_id})")
            else:
                print(f"Venue ID: {resolved_id}")
            print(f"Date: {format_date_display(api_date)}")
            print(f"Time: {format_time_display(api_time)}")
            print(f"Party Size: {party_size}")
            print()

            # Parse areas[].options[] structure from API response
            areas = result.get("areas", [])
            has_availability = False
            rows = []

            for area in areas:
                area_name = area.get("name", area.get("id", "Unknown"))
                area_icon = area.get("icon", "")
                options = area.get("options", [])

                for opt in options:
                    method = opt.get("method", "")
                    opt_time = opt.get("time", "")

                    if method == "seat":
                        has_availability = True
                        status = "✅ Available"
                        rows.append([format_time_display(opt_time), area_name, status])
                    elif method == "standby":
                        has_availability = True
                        status = "⏳ Waitlist"
                        rows.append([format_time_display(opt_time), area_name, status])

            if rows:
                print("Available Time Slots:")
                print()
                table = print_table(["Time", "Area", "Status"], rows, [8, 30, 15])
                print(table)

                # Show recommended options if available
                recommended = result.get("recommended", [])
                if recommended:
                    print("\nRecommended:")
                    for rec in recommended[:3]:
                        rec_time = format_time_display(rec.get("time", ""))
                        rec_area = rec.get("text", rec.get("id", ""))
                        print(f"  • {rec_time} - {rec_area}")
            else:
                # Check for alternative dates
                alt_dates = result.get("dates", [])
                if alt_dates:
                    print("No availability at requested time.")
                    print("\nAlternative dates with availability:")
                    for alt in alt_dates[:5]:
                        # Format: "202602021900" -> "2026-02-02 19:00"
                        if len(alt) >= 12:
                            alt_date = f"{alt[:4]}-{alt[4:6]}-{alt[6:8]}"
                            alt_time = f"{alt[8:10]}:{alt[10:12]}"
                            print(f"  • {alt_date} at {alt_time}")
                        else:
                            print(f"  • {alt}")
                else:
                    print("No availability at the requested time.")

    async def cmd_range(
        self,
        venue_id: str,
        start_date: str,
        end_date: str,
        times: str = "19:00,20:00",
        party_size: int = 2
    ) -> None:
        """Check availability over a date range."""
        # Resolve venue name to ID if needed
        resolved_id = await self.client.resolve_venue_name(venue_id)

        start = datetime.strptime(parse_date(start_date), '%Y%m%d')
        end = datetime.strptime(parse_date(end_date), '%Y%m%d')

        time_list = [parse_time(t.strip()) for t in times.split(",")]

        results = []
        current = start

        while current <= end:
            date_str = current.strftime('%Y%m%d')
            date_results = {"date": date_str, "times": []}

            for api_time in time_list:
                try:
                    result = await self.client.check_availability(
                        resolved_id, date_str, api_time, party_size
                    )
                    # Check areas[].options[] for method="seat" or "standby" availability
                    areas = result.get("areas", [])
                    available_times = []
                    waitlist_times = []
                    for area in areas:
                        for opt in area.get("options", []):
                            method = opt.get("method", "")
                            if method == "seat":
                                available_times.append(opt.get("time", ""))
                            elif method == "standby":
                                waitlist_times.append(opt.get("time", ""))

                    available = len(available_times) > 0
                    has_waitlist = len(waitlist_times) > 0
                    date_results["times"].append({
                        "time": api_time,
                        "available": available,
                        "waitlist": has_waitlist,
                        "slots": available_times,
                        "waitlist_slots": waitlist_times
                    })
                except Exception as e:
                    date_results["times"].append({
                        "time": api_time,
                        "available": False,
                        "error": str(e)
                    })

            results.append(date_results)
            current += timedelta(days=1)

        data = {
            "venue_id": venue_id,
            "start_date": start.strftime('%Y%m%d'),
            "end_date": end.strftime('%Y%m%d'),
            "times": time_list,
            "party_size": party_size,
            "results": results
        }

        if self.json_output and not self.raw_output:
            norm = []
            for day in results:
                norm.append({
                    "date": format_date_display(day.get("date", "")),
                    "times": [{
                        "time": format_time_display(t.get("time", "")),
                        "status": ("available" if t.get("available")
                                   else "waitlist" if t.get("waitlist")
                                   else "error" if t.get("error")
                                   else "unavailable"),
                    } for t in day.get("times", [])],
                })
            try:
                page_id = await self.client.resolve_page_id(resolved_id, validate=True)
            except Exception:
                page_id = None
            self._output(make_envelope(
                "range",
                criteria={
                    "venue_id": resolved_id,
                    "venue_input": venue_id,
                    "start_date": format_date_display(start.strftime('%Y%m%d')),
                    "end_date": format_date_display(end.strftime('%Y%m%d')),
                    "party_size": party_size,
                    "booking_url": make_booking_url(page_id, self.client.locale),
                },
                results=norm,
            ), "")
        elif self.json_output:
            self._output(data, "")
        else:
            print(f"Availability Range Check")
            print(f"Venue ID: {venue_id}")
            print(f"Date Range: {start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}")
            print(f"Times: {', '.join(format_time_display(t) for t in time_list)}")
            print(f"Party Size: {party_size}")
            print()

            headers = ["Date"] + [format_time_display(t) for t in time_list]
            rows = []

            for day_result in results:
                row = [format_date_display(day_result["date"])]
                for time_result in day_result["times"]:
                    if time_result.get("available"):
                        row.append("Available")
                    elif time_result.get("waitlist"):
                        row.append("Waitlist")
                    elif time_result.get("error"):
                        row.append("Error")
                    else:
                        row.append("-")
                rows.append(row)

            table = print_table(headers, rows)
            print(table)

    async def cmd_menu(
        self,
        venue_id: str,
        section: Optional[str] = None,
        search: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> None:
        """Get venue menu."""
        # Resolve venue name to ID if needed
        resolved_id = await self.client.resolve_venue_name(venue_id)

        try:
            info = await self.client.get_venue_info(resolved_id)
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                error_msg = f"Venue not found: {venue_id}. Try: ontopo-cli.py search <name>"
            if self.json_output:
                self._output(make_envelope(
                    "info", criteria={"venue_input": venue_id},
                    error=error_msg), "")
            else:
                print(f"Error: {error_msg}")
            return

        menus = info.get("menus", info.get("menu", []))
        if isinstance(menus, dict):
            menus = [menus]

        # Flatten menu items from structure: menus[].sections[].items[]
        all_items = []
        for menu_obj in menus:
            menu_title = menu_obj.get("title", "Menu")
            sections = menu_obj.get("sections", [])

            # If no sections, try items directly
            if not sections:
                items = menu_obj.get("items", menu_obj.get("dishes", []))
                for item in items:
                    item_copy = dict(item)
                    item_copy["_section"] = menu_title
                    item_copy["_menu"] = menu_title
                    all_items.append(item_copy)
            else:
                for section_obj in sections:
                    section_name = section_obj.get("title", section_obj.get("name", ""))
                    items = section_obj.get("items", section_obj.get("dishes", []))
                    for item in items:
                        item_copy = dict(item)
                        item_copy["_section"] = section_name if section_name else menu_title
                        item_copy["_menu"] = menu_title
                        all_items.append(item_copy)

        # Apply filters
        filtered = all_items

        if section:
            section_lower = section.lower()
            filtered = [i for i in filtered if section_lower in i.get("_section", "").lower()]

        if search:
            search_lower = search.lower()
            filtered = [i for i in filtered if (
                search_lower in i.get("name", "").lower() or
                search_lower in i.get("description", "").lower()
            )]

        if min_price is not None:
            filtered = [i for i in filtered if (
                i.get("price") is not None and float(i.get("price", 0)) >= min_price
            )]

        if max_price is not None:
            filtered = [i for i in filtered if (
                i.get("price") is not None and float(i.get("price", 999999)) <= max_price
            )]

        if self.json_output and not self.raw_output:
            self._output(make_envelope(
                "menu",
                criteria={"venue_id": venue_id, "section": section,
                          "search": search, "min_price": min_price,
                          "max_price": max_price},
                results=[{
                    "name": i.get("name"),
                    "section": i.get("section"),
                    "price": i.get("price"),
                    "description": i.get("description") or None,
                } for i in filtered],
            ), "")
            return

        data = {
            "venue_id": venue_id,
            "items": filtered,
            "count": len(filtered),
            "filters": {
                "section": section,
                "search": search,
                "min_price": min_price,
                "max_price": max_price
            }
        }

        if self.json_output:
            self._output(data, "")
        else:
            venue_name = info.get("name", info.get("title", venue_id))
            print(f"Menu: {venue_name}")
            print()

            if not filtered:
                print("No menu items found matching your criteria.")
                return

            # Group by section
            sections: Dict[str, List[Dict]] = {}
            for item in filtered:
                sec = item.get("_section", "Other")
                if sec not in sections:
                    sections[sec] = []
                sections[sec].append(item)

            for sec_name, items in sections.items():
                print(f"## {sec_name}")
                print()
                rows = []
                for item in items:
                    name = item.get("name", item.get("title", ""))[:40]
                    desc = item.get("description", "")[:30]
                    price = format_price(item.get("price"))
                    rows.append([name, desc, price])

                table = print_table(["Item", "Description", "Price"], rows)
                print(table)
                print()

    async def cmd_info(self, venue_id: str) -> None:
        """Get detailed venue information."""
        # Resolve venue name to ID if needed
        resolved_id = await self.client.resolve_venue_name(venue_id)

        try:
            info = await self.client.get_venue_info(resolved_id)
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                error_msg = f"Venue not found: {venue_id}. Try: ontopo-cli.py search <name>"
            if self.json_output:
                self._output({"error": error_msg}, "")
            else:
                print(f"Error: {error_msg}")
            return

        if self.json_output and not self.raw_output:
            # Only a live booking page (content_type "reservation" with a
            # slug_venue back-reference) may contribute a booking_url. For a
            # search-post id, get_page echoes the input slug, and a URL built
            # from it renders nothing - same trap the url command guards.
            page_id = info.get("slug")
            if not (info.get("content_type") == "reservation"
                    and info.get("slug_venue")):
                page_id = None
            self._output(make_envelope(
                "info",
                criteria={"venue_input": venue_id, "venue_id": resolved_id},
                results=[{
                    "venue_id": resolved_id,
                    "page_id": str(page_id) if page_id else None,
                    "name": info.get("title") or info.get("name") or "Unknown",
                    "address": info.get("address") or None,
                    "phone": info.get("phone") or None,
                    "website": info.get("website") or None,
                    "cuisine": [t for t in (info.get("tag1"), info.get("tag2")) if t],
                    "price_level": info.get("venue_price") or None,
                    "about": info.get("about_us") or None,
                    "booking_url": make_booking_url(page_id, self.client.locale),
                }],
            ), "")
        elif self.json_output:
            self._output(info, "")
        else:
            name = info.get("name", info.get("title", "Unknown"))
            print(f"# {name}")
            print()

            details = [
                ("ID", info.get("id", venue_id)),
                ("Address", info.get("address", info.get("location", {}).get("address", "N/A"))),
                ("City", info.get("city", info.get("area", "N/A"))),
                ("Cuisine", info.get("cuisine", info.get("category", "N/A"))),
                ("Rating", info.get("rating", "N/A")),
                ("Price Range", info.get("price_range", info.get("price_level", "N/A"))),
                ("Phone", info.get("phone", info.get("telephone", "N/A"))),
                ("Website", info.get("website", info.get("url", "N/A"))),
            ]

            for label, value in details:
                if value and value != "N/A":
                    print(f"**{label}**: {value}")

            # Hours
            hours = info.get("hours", info.get("opening_hours", {}))
            if hours:
                print()
                print("## Opening Hours")
                if isinstance(hours, dict):
                    for day, time_range in hours.items():
                        print(f"  {day}: {time_range}")
                elif isinstance(hours, list):
                    for h in hours:
                        print(f"  {h}")

            # Description
            description = info.get("description", info.get("about", ""))
            if description:
                print()
                print("## About")
                print(description[:500])
                if len(description) > 500:
                    print("...")

    async def cmd_url(self, venue_id: str) -> None:
        """Get booking URL for venue."""
        # Resolve venue name to ID if needed
        resolved_id = await self.client.resolve_venue_name(venue_id)
        try:
            page_id = await self.client.resolve_page_id(resolved_id, validate=True)
        except ValueError as e:
            if self.json_output:
                self._output(make_envelope(
                    "url", criteria={"venue_input": venue_id},
                    error=str(e)), "")
            else:
                print(f"Error: {e}")
            return
        url = f"https://ontopo.com/{self.client.locale}/il/page/{page_id}"

        if self.json_output and not self.raw_output:
            self._output(make_envelope(
                "url",
                criteria={"venue_input": venue_id},
                results=[{"venue_id": resolved_id, "page_id": page_id,
                          "booking_url": url}],
            ), "")
        elif self.json_output:
            self._output({"venue_id": venue_id, "page_id": page_id, "url": url}, "")
        else:
            print(f"Booking URL: {url}")

# =============================================================================
# CLI SETUP
# =============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="ontopo-cli.py",
        description="Search Israeli restaurants on Ontopo and check table availability.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ontopo-cli.py cities                              # List supported cities
  ontopo-cli.py search "sushi" --city tel-aviv      # Search for sushi in Tel Aviv
  ontopo-cli.py available 2024-12-25 19:00          # Find available restaurants
  ontopo-cli.py check abc123 2024-12-25             # Check venue availability
  ontopo-cli.py range abc123 2024-12-20 2024-12-27  # Check availability range
  ontopo-cli.py menu abc123 --search "hummus"       # Search venue menu
  ontopo-cli.py info abc123                         # Get venue details
  ontopo-cli.py url abc123                          # Get booking URL
        """
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="With --json, emit the unprocessed upstream payload"
    )
    parser.add_argument(
        "--check-args", action="store_true",
        help=argparse.SUPPRESS  # Validate arguments and exit; used by tests.
    )

    # Accept --raw after the subcommand as well as before it. SUPPRESS keeps
    # the top-level value when the flag is not repeated on the subcommand.
    _common = argparse.ArgumentParser(add_help=False)
    _common.add_argument("--raw", action="store_true",
                         default=argparse.SUPPRESS,
                         help="With --json, emit the unprocessed upstream payload")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # cities
    cities_parser = subparsers.add_parser("cities", help="List supported cities", parents=[_common])
    cities_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # categories
    cat_parser = subparsers.add_parser("categories", help="List supported categories", parents=[_common])
    cat_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # search
    search_parser = subparsers.add_parser("search", help="Search for venues", parents=[_common])
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--city", help="Filter by city")
    search_parser.add_argument("--locale", choices=["en", "he"], default="en", help="Language")
    search_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # available
    avail_parser = subparsers.add_parser("available", help="Search available venues", parents=[_common])
    avail_parser.add_argument("date", help="Date (YYYY-MM-DD, today, tomorrow, +N)")
    avail_parser.add_argument("time", help="Time (HH:MM, HHMM, 7pm)")
    avail_parser.add_argument("--city", help="City to search in")
    avail_parser.add_argument("--party-size", type=int, default=2, help="Party size (default: 2)")
    avail_parser.add_argument("--safe-zone", "--mamad", action="store_true", help="Only show venues tagged as safe zone (מרחב מוגן) on Ontopo")
    avail_parser.add_argument("--venue-type", help="Filter by venue tag (e.g. kosher, vegetarian, wine_bar)")
    avail_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # check
    check_parser = subparsers.add_parser("check", help="Check venue availability", parents=[_common])
    check_parser.add_argument("venue_id", help="Venue ID or name (e.g., 36960535 or 'taizu')")
    check_parser.add_argument("date", help="Date (YYYY-MM-DD, today, tomorrow, +N)")
    check_parser.add_argument("time", nargs="?", default="19:00", help="Time (HH:MM, HHMM, 7pm) - default: 19:00")
    check_parser.add_argument("--party-size", type=int, default=2, help="Party size (default: 2)")
    check_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # range
    range_parser = subparsers.add_parser("range", help="Check availability over date range", parents=[_common])
    range_parser.add_argument("venue_id", help="Venue ID")
    range_parser.add_argument("start_date", help="Start date (YYYY-MM-DD)")
    range_parser.add_argument("end_date", help="End date (YYYY-MM-DD)")
    range_parser.add_argument("--times", default="19:00,20:00", help="Times to check (comma-separated)")
    range_parser.add_argument("--party-size", type=int, default=2, help="Party size (default: 2)")
    range_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # menu
    menu_parser = subparsers.add_parser("menu", help="Get venue menu", parents=[_common])
    menu_parser.add_argument("venue_id", help="Venue ID")
    menu_parser.add_argument("--section", help="Filter by section name")
    menu_parser.add_argument("--search", help="Search menu items")
    menu_parser.add_argument("--min-price", type=float, help="Minimum price")
    menu_parser.add_argument("--max-price", type=float, help="Maximum price")
    menu_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # info
    info_parser = subparsers.add_parser("info", help="Get venue details", parents=[_common])
    info_parser.add_argument("venue_id", help="Venue ID")
    info_parser.add_argument("--locale", choices=["en", "he"], default="en", help="Language")
    info_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # url
    url_parser = subparsers.add_parser("url", help="Get booking URL", parents=[_common])
    url_parser.add_argument("venue_id", help="Venue ID")
    url_parser.add_argument("--locale", choices=["en", "he"], default="en", help="Language")
    url_parser.add_argument("--json", action="store_true", help="Output as JSON")

    return parser


async def main_async(args: argparse.Namespace) -> int:
    """Main async entry point."""
    locale = getattr(args, "locale", "en")
    json_output = getattr(args, "json", False)
    raw_output = getattr(args, "raw", False)

    async with OntopoClient(locale=locale) as client:
        handler = CommandHandler(client, json_output=json_output,
                                 raw_output=raw_output)

        try:
            if args.command == "cities":
                await handler.cmd_cities()

            elif args.command == "categories":
                await handler.cmd_categories()

            elif args.command == "search":
                await handler.cmd_search(args.query, args.city)

            elif args.command == "available":
                venue_type = "safe_zone" if getattr(args, "safe_zone", False) else getattr(args, "venue_type", None)
                await handler.cmd_available(
                    args.date, args.time, args.city, args.party_size,
                    venue_type=venue_type
                )

            elif args.command == "check":
                await handler.cmd_check(
                    args.venue_id, args.date, args.time, args.party_size
                )

            elif args.command == "range":
                await handler.cmd_range(
                    args.venue_id, args.start_date, args.end_date,
                    args.times, args.party_size
                )

            elif args.command == "menu":
                await handler.cmd_menu(
                    args.venue_id, args.section, args.search,
                    args.min_price, args.max_price
                )

            elif args.command == "info":
                await handler.cmd_info(args.venue_id)

            elif args.command == "url":
                await handler.cmd_url(args.venue_id)

            else:
                return 1

            return 0

        except ValueError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1

        except RuntimeError as e:
            if json_output:
                print(json.dumps({"error": str(e)}))
            else:
                print(f"Error: {e}", file=sys.stderr)
            return 1


def main() -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Validate arguments without executing (used by the docs conformance test).
    if getattr(args, "check_args", False):
        return 0

    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
