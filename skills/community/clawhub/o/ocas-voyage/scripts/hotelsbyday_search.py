#!/usr/bin/env python3
"""
HotelsByDay search harness for ocas-voyage.

Supports two sub-products:
  - Day-use rooms (www.hotelsbyday.com): GET /en/search/results
    - Search via form params: query, check_in, check_out, guests
    - Autocomplete: /en/search/multy_autocomplete?query=
    - Hotel detail pages expose structured room rates via data-price, hd-room-time, etc.
    - Booking form requires CSRF token (collected server-side)

  - Night stays (night.hotelsbyday.com): Livewire-based SPA
    - GET /en/hotels/search?query=...&check_in=...&check_out=...&guests=...&stay_type=night
    - Search results loaded via Livewire wire:snapshot data
    - Currently in beta with limited inventory
    - Update endpoint: POST /en/livewire/update (requires CSRF)

Usage:
  python3 hotelsbyday_search.py search "San Francisco" 2026-08-10 2026-08-11 --guests 1 --product night
  python3 hotelsbyday_search.py autocomplete "San Fran"
  python3 hotelsbyday_search.py hotel-detail https://www.hotelsbyday.com/en/hotels/united-states/new-york/m-social-hotel-times-square?date=2026-08-10

Output: JSON to stdout.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime


DAY_BASE = "https://www.hotelsbyday.com"
NIGHT_BASE = "https://night.hotelsbyday.com"
MEDIA_BASE = "https://api.hotelsbyday.com/api/media/v1"


def fetch(url, headers=None, timeout=30):
    """Fetch a URL and return (status, body, final_url)."""
    if headers is None:
        headers = {}
    default_headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/json,*/*",
    }
    default_headers.update(headers)

    req = urllib.request.Request(url, headers=default_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return resp.status, body, resp.url
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return e.code, body, url
    except Exception as e:
        return 0, str(e), url


def autocomplete(query):
    """Query the HotelsByDay autocomplete endpoint."""
    url = f"{DAY_BASE}/en/search/multy_autocomplete?{urllib.parse.urlencode({'query': query})}"
    status, body, _ = fetch(url, headers={"Accept": "application/json"})
    if status != 200:
        return {"error": f"HTTP {status}", "body": body[:500]}

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "raw": body[:500]}

    results = []
    for hotel in data.get("hotels", []):
        results.append({
            "type": "hotel",
            "hotel_id": hotel.get("hotelid"),
            "name": hotel.get("name"),
            "location": hotel.get("location"),
        })
    for country in data.get("countries", []):
        results.append({
            "type": "country",
            "country_id": country.get("countryid"),
            "name": country.get("name"),
            "code": country.get("code"),
        })

    return {"query": query, "results": results}


def _extract_hotel_cards(html):
    """Extract hotel cards from a search results page (day-use site)."""
    hotels = []

    # Pattern: class="card-hotel" data-href="URL" > ... name ... price ...
    card_blocks = re.findall(
        r'class="card-hotel"[^>]*data-href="([^"]+)"[^>]*>(.*?)</div>\s*</div>\s*</div>\s*</div>\s*</div>',
        html,
        re.DOTALL,
    )

    for href, block in card_blocks:
        # Name
        name_match = re.search(r'class="card-hotel-name"[^>]*>(.*?)</div>', block, re.DOTALL)
        name = ""
        if name_match:
            name = re.sub(r"<[^>]+>", " ", name_match.group(1))
            name = re.sub(r"&nbsp;", " ", name)
            name = re.sub(r"\s+", " ", name).strip()

        # Rating (extract from name string like "Aloft SFO San Francisco, CA 4.2 / 5")
        rating = None
        rating_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*5", name)
        if rating_match:
            rating = float(rating_match.group(1))

        # Price
        price = re.search(r'data-price="([0-9.]+)"', block)
        currency_match = re.search(r'data-currency="([^"]+)"', block)

        # Services/amenities mentioned
        services = re.findall(
            r"(Day\s*use\s*room|Work\s*Friendly|In-room\s*Work\s*Desk|Pool\s*Pass|Gym\s*Pass|Spa\s*Pass|Food\s*&\s*Beverage|Meeting\s*Room|Cabana|Event\s*Space|Parking)",
            block,
            re.IGNORECASE,
        )
        services = list(dict.fromkeys(s.strip() for s in services))

        # Time slots
        times = re.findall(r"(\d+\s*[AP]M\s*-\s*\d+\s*[AP]M)", block, re.IGNORECASE)
        time_slots = list(dict.fromkeys(times))

        # Cancellation
        cancel = re.search(r"(Pay at property[^<]*)", block, re.DOTALL)
        cancellation = cancel.group(1).strip() if cancel else None

        # Loyalty coins
        coins = re.search(r"earn up to\s*(\d+(?:\.\d+)?)", block, re.IGNORECASE)
        loyalty_coins = float(coins.group(1)) if coins else None

        hotels.append({
            "url": href,
            "name": name,
            "rating": rating,
            "price": float(price.group(1)) if price else None,
            "currency": currency_match.group(1) if currency_match else "USD",
            "services": services,
            "time_slots": time_slots,
            "cancellation": cancellation,
            "loyalty_coins": loyalty_coins,
        })

    return hotels


def _city_page_hotels(query):
    """Try to resolve a query to a HotelsByDay city page and extract its hotels.

    The /en/search/results endpoint silently falls back to default (New York)
    results when it can't geocode a query — so before trusting it, check
    whether the query matches a known city page (e.g. .../united-states/honolulu)
    and pull that page's hotel links directly. Returns list of hotels or None.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", query.lower()).strip("-")
    if not slug:
        return None
    # Try the direct city-page URL for a handful of likely countries.
    for country in ("united-states", "canada", "united-kingdom"):
        url = f"{DAY_BASE}/en/hotels/{country}/{urllib.parse.quote(slug)}"
        status, body, _ = fetch(url)
        if status != 200:
            continue
        links = re.findall(
            r'href="(' + re.escape(url) + r'/[^"?]+)[^"]*"',
            body,
        )
        if not links:
            continue
        # Names live in title attributes on hotel links only — filter out
        # generic UI titles (search box, date picker, brand).
        alt_names = []
        for m in re.finditer(
            r'href="(' + re.escape(url) + r'/[^"?]+)[^"]*"[^>]*title="([^"]{5,90})"', body
        ):
            alt_names.append(html_module_unescape(m.group(2)).strip())
        if not alt_names:
            for m in re.finditer(
                r'title="([^"]{5,90})"[^>]*href="(' + re.escape(url) + r'/[^"?)+)[^"]*"',
                body,
            ):
                alt_names.append(html_module_unescape(m.group(1)).strip())
        names = re.findall(r'class="card-hotel-name"[^>]*>(.*?)</div>', body, re.DOTALL)
        hotels = []
        for i, href in enumerate(dict.fromkeys(links)):
            name = ""
            if i < len(names):
                name = re.sub(r"<[^>]+>", " ", names[i])
                name = re.sub(r"&nbsp;", " ", name)
                name = re.sub(r"\s+", " ", name).strip()
            if not name and i < len(alt_names):
                name = html_module_unescape(alt_names[i]).strip()
            rating_match = re.search(r"(\d+(?:\.\d+)?)\s*/\s*5", name)
            hotels.append({
                "url": href,
                "name": name,
                "rating": float(rating_match.group(1)) if rating_match else None,
            })
        if hotels:
            return hotels
    return None


def search_day(query, check_in, check_out, guests=1):
    """Search for day-use hotel rooms on the HotelsByDay day-use site."""
    params = urllib.parse.urlencode({
        "query": query,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "countryid": "",
        "stateid": "",
        "cityid": "",
        "hotelid": "",
        "coords": "",
    })
    url = f"{DAY_BASE}/en/search/results?{params}"
    status, body, final_url = fetch(url)

    if status != 200:
        return {"error": f"HTTP {status}", "body": body[:500]}

    hotels = _extract_hotel_cards(body)

    # Guard against the site's silent fallback: if the returned hotels'
    # locations don't match the query at all, prefer a resolved city page.
    q_words = set(re.findall(r"[a-z]+", query.lower()))
    matched = any(
        h.get("name") and any(w in h["name"].lower() for w in q_words)
        for h in hotels
    )
    if not matched:
        city_hotels = _city_page_hotels(query)
        if city_hotels:
            return {
                "source": "hotelsbyday-city-page",
                "query": query,
                "check_in": check_in,
                "check_out": check_out,
                "guests": guests,
                "total_hotels": len(city_hotels),
                "note": ("text search returned unrelated default results; "
                         "used resolved city page instead"),
                "hotels": city_hotels,
            }

    return {
        "source": "hotelsbyday-day",
        "query": query,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "total_hotels": len(hotels),
        "hotels": hotels,
    }


def search_night(query, check_in, check_out, guests=1):
    """Search for overnight stays on the HotelsByDay night site (currently in beta)."""
    params = urllib.parse.urlencode({
        "query": query,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "stay_type": "night",
    })
    url = f"{NIGHT_BASE}/en/hotels/search?{params}"
    status, body, _ = fetch(url)

    if status != 200:
        return {"error": f"HTTP {status}", "body": body[:500]}

    # Check if the site is in beta
    beta_msg = re.search(r"currently in Beta|beta|will be available very soon", body, re.IGNORECASE)
    is_beta = bool(beta_msg)

    # Extract Livewire snapshots for search-list component
    wire_snapshots = re.findall(r'wire:snapshot="([^"]*)"', body)
    search_list_data = None

    for ws in wire_snapshots:
        decoded = ws.replace("&quot;", '"').replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        try:
            data = json.loads(decoded)
            name = data.get("memo", {}).get("name", "")
            if "search-list" in name:
                search_list_data = data.get("data", {})
                break
        except json.JSONDecodeError:
            continue

    # Extract hotel links from HTML (day-use style fallback)
    hotel_links = re.findall(r'data-href="([^"]+hotels[^"]+)"', body)
    hotel_names = re.findall(r'class="card-hotel-name"[^>]*>(.*?)</div>', body, re.DOTALL)

    hotels = []
    for i in range(min(len(hotel_links), len(hotel_names))):
        name = re.sub(r"<[^>]+>", " ", hotel_names[i])
        name = re.sub(r"&nbsp;", " ", name)
        name = re.sub(r"\s+", " ", name).strip()
        hotels.append({"url": hotel_links[i], "name": name})

    return {
        "source": "hotelsbyday-night",
        "query": query,
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "total_hotels": len(hotels),
        "is_beta": is_beta,
        "search_list_meta": search_list_data,
        "hotels": hotels,
    }


def hotel_detail(hotel_url, check_in=None, check_out=None, guests=1):
    """Fetch hotel detail page and extract room rates."""
    status, body, _ = fetch(hotel_url)
    if status != 200:
        return {"error": f"HTTP {status}", "body": body[:500]}

    # Extract room data
    room_names = re.findall(r'<div class="hd-room-name"(?:[^>]*)>(.*?)</div>', body, re.DOTALL)
    room_times = re.findall(r'<div class="hd-room-time[^"]*"[^>]*>(.*?)</div>', body, re.DOTALL)
    room_rates = re.findall(r'data-price="([0-9.]+)"', body)
    room_cancels = re.findall(r'<div class="hd-room-cancellation"[^>]*>(.*?)</div>', body, re.DOTALL)
    room_types = re.findall(r'data-rate-type="([^"]+)"', body)

    rooms = []
    for i in range(len(room_rates)):
        name = ""
        if i < len(room_names):
            name = re.sub(r"<[^>]+>", " ", room_names[i])
            name = re.sub(r"&nbsp;", " ", name)
            name = re.sub(r"\s+", " ", name).strip()

        time_slot = ""
        if i < len(room_times):
            time_slot = re.sub(r"<[^>]+>", " ", room_times[i])
            time_slot = re.sub(r"&nbsp;", " ", time_slot)
            time_slot = re.sub(r"\s+", " ", time_slot).strip()

        cancel_text = ""
        if i < len(room_cancels):
            cancel_text = re.sub(r"<[^>]+>", " ", room_cancels[i])
            cancel_text = re.sub(r"&nbsp;", " ", cancel_text)
            cancel_text = re.sub(r"\s+", " ", cancel_text).strip()

        rate_type = room_types[i] if i < len(room_types) else "basic"

        rooms.append({
            "name": name,
            "time_slot": time_slot,
            "price": float(room_rates[i]),
            "currency": "USD",
            "rate_type": rate_type,
            "cancellation": cancel_text,
        })

    # Extract general hotel info
    title_match = re.search(r"<title>(.*?)</title>", body)
    title = html_module_unescape(title_match.group(1)) if title_match else ""

    # Extract star rating from JSON-LD if present
    json_ld = re.search(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    stars = None
    if json_ld:
        try:
            ld_data = json.loads(json_ld.group(1).strip())
            stars = ld_data.get("starRating") or ld_data.get("stars")
        except json.JSONDecodeError:
            pass

    return {
        "source": "hotelsbyday-detail",
        "url": hotel_url,
        "title": title,
        "stars": stars,
        "rooms": rooms,
    }


def html_module_unescape(text):
    """Simple HTML entity unescape."""
    return text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")


def main():
    parser = argparse.ArgumentParser(description="HotelsByDay search harness")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # autocomplete
    ap = subparsers.add_parser("autocomplete", help="Search for hotels/countries by query")
    ap.add_argument("query", help="Search term (e.g. 'San Francisco')")

    # search (day-use)
    sp = subparsers.add_parser("search", help="Search for hotels")
    sp.add_argument("query", help="Location query (e.g. 'San Francisco')")
    sp.add_argument("check_in", help="Check-in date (YYYY-MM-DD)")
    sp.add_argument("check_out", help="Check-out date (YYYY-MM-DD)")
    sp.add_argument("--guests", type=int, default=1, help="Number of guests")
    sp.add_argument("--product", choices=["day", "night"], default="day", help="Product: day (day-use) or night (overnight)")

    # hotel-detail
    dp = subparsers.add_parser("hotel-detail", help="Get room rates for a specific hotel")
    dp.add_argument("url", help="Hotel detail URL")
    dp.add_argument("--check-in", help="Check-in date (YYYY-MM-DD)")
    dp.add_argument("--check-out", help="Check-out date (YYYY-MM-DD)")
    dp.add_argument("--guests", type=int, default=1)

    args = parser.parse_args()

    if args.command == "autocomplete":
        result = autocomplete(args.query)
    elif args.command == "search":
        if args.product == "night":
            result = search_night(args.query, args.check_in, args.check_out, args.guests)
        else:
            result = search_day(args.query, args.check_in, args.check_out, args.guests)
    elif args.command == "hotel-detail":
        result = hotel_detail(args.url, args.check_in, args.check_out, args.guests)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
