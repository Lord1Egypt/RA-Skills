#!/usr/bin/env python3
"""Mensa: print today's canteen menu from the public OpenMensa API.

Setup is non-interactive: `--setup <city>` discovers and saves ALL canteens in
that city as aliases. The first canteen becomes the default; override with
`--default <substring>`. Subsequent runs query the default canteen, or any
saved canteen by substring (special characters are normalised, so a query like
"Otto Hahn" matches a canteen named "Mensa Otto-Hahn-Straße").

External endpoints:
  GET https://openmensa.org/api/v2/canteens?page=N
  GET https://openmensa.org/api/v2/canteens/{id}/days/{date}/meals
No credentials are sent.
"""
import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import date as _date

API = "https://openmensa.org/api/v2"
TIMEOUT = 10
VERSION = "1.1.0"
USER_AGENT = f"mensa-openclaw-skill/{VERSION} (+https://openmensa.org)"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

VEG_HINTS = ("vegan",)
VEGGIE_HINTS = ("vegetarisch", "vegetarian")
SIDE_CATEGORY_HINTS = ("beilage",)
HIDDEN_NAME_HINTS = ("restproduktion",)


def is_hidden_meal(meal: dict) -> bool:
    """True if the meal is a side (Beilage) or otherwise not a real lunch dish.

    Sides are detected via the category ('beilage' substring), the leftover/Reste
    bucket ('Tagesrestproduktion') via the name.
    """
    category = (meal.get("category") or "").lower()
    if any(hint in category for hint in SIDE_CATEGORY_HINTS):
        return True
    name = (meal.get("name") or "").lower()
    return any(hint in name for hint in HIDDEN_NAME_HINTS)


def normalize(s: str) -> str:
    """Lowercase and replace non-word characters with spaces, collapsing whitespace.

    Lets queries like "otto hahn" match canteens like "Mensa Otto-Hahn-Straße".
    """
    s = re.sub(r"\W+", " ", s.lower(), flags=re.UNICODE)
    return re.sub(r"\s+", " ", s).strip()


def http_get_json(url: str):
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": USER_AGENT},
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.load(resp)


def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    try:
        os.chmod(CONFIG_PATH, 0o600)
    except OSError:
        pass


def fetch_canteens_for_city(city: str) -> list:
    """Page through /canteens; prefer exact city match, fall back to substring."""
    exact, fuzzy, page = [], [], 1
    needle = city.strip().lower()
    while True:
        data = http_get_json(f"{API}/canteens?page={page}&limit=100")
        if not data:
            break
        for c in data:
            city_field = (c.get("city") or "").strip().lower()
            name_field = (c.get("name") or "").strip().lower()
            entry = {"id": c["id"], "name": c["name"], "city": c.get("city", "")}
            if city_field == needle:
                exact.append(entry)
            elif needle and (needle in city_field or needle in name_field):
                fuzzy.append(entry)
        if len(data) < 100:
            break
        page += 1
    return exact if exact else fuzzy[:50]


def find_canteen_by_substring(canteens: list, needle: str):
    """Return the first canteen whose normalised name contains the normalised needle."""
    if not needle:
        return None
    needle_norm = normalize(needle)
    if not needle_norm:
        return None
    for c in canteens:
        if needle_norm in normalize(c["name"]):
            return c
    return None


def list_canteens(city: str) -> int:
    print(f"Searching canteens in '{city}' via OpenMensa...")
    try:
        canteens = fetch_canteens_for_city(city)
    except Exception as e:
        print(f"API error while listing canteens: {e}")
        return 1
    if not canteens:
        print(f"No canteens found for city '{city}'. Check the spelling on openmensa.org.")
        return 1
    print(f"Found {len(canteens)} canteen(s) in {city}:")
    for c in canteens:
        print(f"- {c['name']} (id={c['id']})")
    return 0


def setup(city: str, default_substring) -> int:
    print(f"Searching canteens in '{city}' via OpenMensa...")
    try:
        canteens = fetch_canteens_for_city(city)
    except Exception as e:
        print(f"API error while listing canteens: {e}")
        return 1
    if not canteens:
        print(f"No canteens found for city '{city}'. Check the spelling on openmensa.org.")
        return 1

    # Always save all canteens as aliases — every canteen in the city stays queryable.
    aliases = {c["name"].lower(): c["id"] for c in canteens}

    # Default: --default substring match wins, otherwise the first canteen.
    default = None
    if default_substring:
        default = find_canteen_by_substring(canteens, default_substring)
        if not default:
            print(
                f"Warning: --default '{default_substring}' matched no canteen in {city}. "
                f"Using first canteen as default."
            )
    if not default:
        default = canteens[0]

    cfg = {
        "city": city,
        "default": {"id": default["id"], "name": default["name"]},
        "aliases": aliases,
    }
    save_config(cfg)
    print(
        f"Saved {len(aliases)} canteen(s) for {city}. "
        f"Default: {default['name']} (id={default['id']})."
    )
    print("All canteens in this city are now queryable by name substring.")
    return 0


def resolve_canteen_id(cfg: dict, query):
    if not cfg:
        return None
    if not query:
        d = cfg.get("default", {}).get("id")
        try:
            return int(d) if d is not None else None
        except (TypeError, ValueError):
            return None
    q_norm = normalize(query)
    if not q_norm:
        return None
    aliases = cfg.get("aliases", {})
    # 1) Exact normalised match
    for name, cid in aliases.items():
        if normalize(name) == q_norm:
            try:
                return int(cid)
            except (TypeError, ValueError):
                return None
    # 2) Substring match (normalised)
    for name, cid in aliases.items():
        if q_norm in normalize(name):
            try:
                return int(cid)
            except (TypeError, ValueError):
                return None
    return None


def format_menu(meals: list, on_date: str) -> str:
    if not meals:
        return f"No dishes listed for {on_date} (closed / weekend / holiday?)."
    lines = [f"{on_date} - Menu (student price)"]
    for m in meals:
        price = m.get("prices", {}).get("students")
        price_str = f"{price:.2f} EUR" if isinstance(price, (int, float)) else "n/a"
        notes = [n.lower() for n in m.get("notes", [])]
        tags = []
        if any(h in n for n in notes for h in VEG_HINTS):
            tags.append("vegan")
        elif any(h in n for n in notes for h in VEGGIE_HINTS):
            tags.append("vegetarian")
        tag_str = f" ({', '.join(tags)})" if tags else ""
        lines.append(f"- {m['name']} - {price_str}{tag_str}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Today's canteen menu via OpenMensa.")
    parser.add_argument(
        "query",
        nargs="*",
        help="Canteen name (substring match against saved aliases).",
    )
    parser.add_argument(
        "--list",
        dest="list_city",
        metavar="CITY",
        help="List all canteens in CITY without saving config (preview step).",
    )
    parser.add_argument(
        "--setup",
        metavar="CITY",
        help="Discover and save all canteens in CITY (non-interactive).",
    )
    parser.add_argument(
        "--default",
        metavar="SUBSTRING",
        help="With --setup: which canteen to set as default (substring match). "
        "Default: first canteen returned by OpenMensa.",
    )
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Query a specific date instead of today.",
    )
    args = parser.parse_args()

    if args.list_city:
        return list_canteens(args.list_city)

    if args.setup:
        return setup(args.setup, args.default)

    if args.default:
        print("--default has no effect without --setup. Ignoring.")

    cfg = load_config()
    if not cfg:
        print('No canteen configured yet. Run:  mensa_today.py --setup "<city>"')
        return 1

    query = " ".join(args.query) if args.query else None
    cid = resolve_canteen_id(cfg, query)
    if cid is None:
        available = ", ".join(cfg.get("aliases", {}).keys()) or "(none)"
        print(f"No canteen matched '{query}'. Available: {available}")
        return 1

    if args.date:
        try:
            on_date = _date.fromisoformat(args.date).isoformat()
        except ValueError:
            print(f"Invalid --date '{args.date}'. Expected format: YYYY-MM-DD.")
            return 1
    else:
        on_date = _date.today().isoformat()
    url = f"{API}/canteens/{cid}/days/{urllib.parse.quote(on_date)}/meals"
    try:
        meals = http_get_json(url)
    except Exception as e:
        print(f"API error: {e}")
        return 1

    meals = [m for m in meals if not is_hidden_meal(m)]
    print(format_menu(meals, on_date))
    return 0


if __name__ == "__main__":
    sys.exit(main())
