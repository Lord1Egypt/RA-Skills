#!/usr/bin/env python3
"""
mena-property-listing-generator — executable (v1.0)

Usage:
  property-listing new --location "Lusail" --type "2BR Apartment" \
    --price 450000 --area 120 --bedrooms 2 --bathrooms 2 \
    --features "Balcony, Gym, Pool" --agent "Nasser" --phone "+974XXXXXXXX"
  property-listing bulk --csv properties.csv
  property-listing compare --listings "listing1.json,listing2.json"
  property-listing format --input listing.json --format "whatsapp|instagram|pdf"
  property-listing agents --add --name "Nasser" --phone "+974XXX" --agency "Halaqa"
  property-listing list

Free tier: 3 listings/month.
"""
import argparse
import csv
import json
import logging
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

__version__ = "1.0.1"
SCHEMA_VERSION = 1

logger = logging.getLogger("mena-property-listing-generator")
USER_AGENT = "MENAPropertyListing/1.0 (+https://clawhub.ai)"
DATA_DIR = Path.home() / ".openclaw" / "mena-property-listing-generator"
DATA_PATH = DATA_DIR / "listings.json"
CONFIG_PATH = DATA_DIR / "config.json"
AGENTS_PATH = DATA_DIR / "agents.json"
COUNTER_PATH = DATA_DIR / "counter.json"


def configure_logging(verbose=False, quiet=False):
    """Configure logging level based on flags / env."""
    level = logging.WARNING
    if verbose:
        level = logging.DEBUG
    elif not quiet:
        level = logging.INFO
    env_level = os.environ.get("CLAWHUB_LOG_LEVEL", "").upper()
    if env_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
        level = getattr(logging, env_level)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )


# ─── MENA Locations & Arabic ──────────────────────────────────────────────────

LUSAIL_AREAS = ["Marina", "Marina Promenade", "Fox Hills", "Al Maham", "Jozi Heights", "Lusail Hills"]
PEARL_AREAS = ["Bahrain Tower", "Costa Malaz", "Rita Star", "Qanat Quartier", "Venetian", "Porto Arabia"]
WEST_BAY_AREAS = ["City Centre", "Diplomatic Area", "Grand Hyatt", "Barcelo", " Tornado Tower"]
DOHA_AREAS = ["Al Sadd", "Al Mirqab", "Al Nasr", "Wedweel", "Al Thumama", "Doha Festival City"]
OTHER_AREAS = ["Al Khor", "Lusail", "The Pearl Qatar", "Doha Festival City", "Education City"]

ARABIC_LOCATIONS = {
    "Lusail": "لوسيل",
    "The Pearl Qatar": "حلبة اللؤلؤة",
    "West Bay": "الخليج الغربي",
    "Al Sadd": "السد",
    "Al Mirqab": "المرقاب",
    "Doha": "الدوحة",
    "Al Khor": "الخور",
    "Education City": "مدينة التعليم",
}

ARABIC_TYPES = {
    "1BR Apartment": "شقة غرفة نوم واحدة",
    "2BR Apartment": "شقة غرفتين نوم",
    "3BR Apartment": "شقة ثلاث غرف نوم",
    "4BR Apartment": "شقة أربع غرف نوم",
    "Penthouse": "بنتهاوس",
    "Villa": "فيلا",
    "Townhouse": "تاون هاوس",
    "Studio": "استوديو",
    "Office": "مكتب",
    "Retail": "محل تجاري",
}

ARABIC_FEATURES = {
    "Balcony": "شرفة",
    "Gym": "صالة رياضية",
    "Pool": "مسبح",
    "Parking": "موقف سيارات",
    "Security": "أمن",
    "Concierge": "خدمات الكونسيرج",
    "Sea View": "إطلالة بحرية",
    "City View": "إطلالة على المدينة",
    "Garden": "حديقة",
    "Furnished": "مؤثث",
    "Pet Friendly": "يسمح بالحيوانات الأليفة",
    "Elevator": "مصعد",
    "Maintenance": "صيانة",
}

def to_arabic_numeral(n):
    """Convert to Arabic numerals."""
    arabic = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    return str(n).translate(arabic)

def format_price_arabic(price):
    """Format price in Arabic."""
    return f"{to_arabic_numeral(f"{price:,}")} ر.ق"

def en_to_ar(text):
    """Basic English to Arabic for property features."""
    words = text.split(", ")
    result = []
    for w in words:
        w = w.strip()
        result.append(ARABIC_FEATURES.get(w, w))
    return "، ".join(result)

# ─── Storage ───────────────────────────────────────────────────────────────────

def load_listings():
    if not DATA_PATH.exists():
        return []
    try:
        with open(DATA_PATH) as f:
            data = json.load(f)
            if isinstance(data, dict) and "listings" in data:
                file_schema = data.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating listings schema from v{file_schema} to v{SCHEMA_VERSION}")
                return data["listings"]
            return data
    except (json.JSONDecodeError, IOError):
        return []


def save_listings(listings):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, "listings": listings}
    with open(DATA_PATH, "w") as f:
        json.dump(wrapped, f, indent=2)


def load_counter():
    if not COUNTER_PATH.exists():
        return {"month": datetime.now().strftime("%Y-%m"), "count": 0}
    try:
        with open(COUNTER_PATH) as f:
            c = json.load(f)
            c.pop("_schema_version", None)
            return c
    except (json.JSONDecodeError, IOError):
        return {"month": datetime.now().strftime("%Y-%m"), "count": 0}


def save_counter(counter):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, **counter}
    with open(COUNTER_PATH, "w") as f:
        json.dump(wrapped, f)


def check_limit():
    """Check if free tier limit is reached."""
    counter = load_counter()
    month = datetime.now().strftime("%Y-%m")
    if counter.get("month") != month:
        counter = {"month": month, "count": 0}
        save_counter(counter)
    return counter["count"], counter.get("month") == month


def increment_counter():
    counter = load_counter()
    month = datetime.now().strftime("%Y-%m")
    if counter.get("month") != month:
        counter = {"month": month, "count": 0}
    counter["count"] += 1
    save_counter(counter)
    return counter["count"]


def load_agents():
    if not AGENTS_PATH.exists():
        return []
    try:
        with open(AGENTS_PATH) as f:
            data = json.load(f)
            if isinstance(data, dict) and "agents" in data:
                file_schema = data.get("_schema_version", 0)
                if file_schema < SCHEMA_VERSION:
                    logger.info(f"Migrating agents schema from v{file_schema} to v{SCHEMA_VERSION}")
                return data["agents"]
            return data
    except (json.JSONDecodeError, IOError):
        return []


def save_agents(agents):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    wrapped = {"_schema_version": SCHEMA_VERSION, "agents": agents}
    with open(AGENTS_PATH, "w") as f:
        json.dump(wrapped, f, indent=2)


# ─── LLM ──────────────────────────────────────────────────────────────────────

# Allowed LLM hosts — prevents credential-routing to arbitrary servers (TT3 fix)
ALLOWED_LLM_HOSTS = frozenset([
    "api.minimax.chat",
    "api.minimaxi.chat",
    "api.openai.com",
    "api.anthropic.com",
    "api.deepseek.com",
])

# Hardcoded defaults per provider (credential is keyed to provider)
LLM_DEFAULTS = {
    "MINIMAX_API_KEY": "https://api.minimax.chat/v1",
    "OPENAI_API_KEY": "https://api.openai.com/v1",
    "LLM_API_KEY": "https://api.minimax.chat/v1",
}


def get_llm_api_key():
    # Scope to MINIMAX only — do not accept OPENAI_API_KEY or LLM_API_KEY.
    # Sending an unrelated API key to the wrong endpoint is a credential-scoping risk.
    key = os.environ.get("MINIMAX_API_KEY")
    if key:
        return key, "MINIMAX_API_KEY"
    return None, None


def get_validated_base_url(provider_key):
    """Return a safe base URL — no env redirect, strict host allowlist.

    TT3 fix: LLM_BASE_URL env var is only honored if its host is in
    ALLOWED_LLM_HOSTS. Otherwise falls back to the provider's known default.
    """
    default = LLM_DEFAULTS.get(provider_key, "https://api.minimax.chat/v1")
    raw = os.environ.get("LLM_BASE_URL", "").strip()
    if raw:
        # Only honor the override if the host is explicitly allowlisted
        from urllib.parse import urlparse
        try:
            parsed = urlparse(raw)
            host = parsed.netloc or parsed.path.split("/")[0]
            if host in ALLOWED_LLM_HOSTS:
                # Normalise to base path
                base = f"https://{host}/v1"
                logger.debug(f"LLM_BASE_URL validated: {base}")
                return base
            else:
                logger.warning(
                    f"LLM_BASE_URL host '{host}' not in allowlist — "
                    f"rejecting; using default for {provider_key}"
                )
        except Exception:
            logger.warning(f"Could not parse LLM_BASE_URL '{raw}' — using default")
    return default


def call_llm(prompt, max_tokens=800):
    api_key, provider_key = get_llm_api_key()
    if not api_key:
        return None
    base_url = get_validated_base_url(provider_key)
    try:
        data = json.dumps({
            "model": "minimax/MiniMax-M3",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.5,
        }).encode()
        req = urllib.request.Request(
            f"{base_url}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
            }
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read())
            return result["choices"][0]["message"]["content"].strip()
    except Exception:
        return None


# ─── Listing Generation ───────────────────────────────────────────────────────

def generate_listing_enhanced(listing, format_type="whatsapp", api_key_present=False):
    """Generate enhanced listing using LLM or template fallback."""
    location = listing.get("location", "Qatar")
    prop_type = listing.get("type", "Property")
    price = listing.get("price", 0)
    area = listing.get("area", 0)
    bedrooms = listing.get("bedrooms", 0)
    bathrooms = listing.get("bathrooms", 0)
    features = listing.get("features", "")
    agent_name = listing.get("agent_name", listing.get("agent", ""))
    agent_phone = listing.get("agent_phone", listing.get("phone", ""))

    if api_key_present:
        prompt = f"""Write a property listing in TWO formats for a Qatar property:

Property: {prop_type} in {location}
Price: QAR {price:,}
Area: {area} sqm
Bedrooms: {bedrooms}, Bathrooms: {bathrooms}
Features: {features}
Agent: {agent_name}

Format 1 — WhatsApp (max 400 chars):
Write a punchy, warm WhatsApp message. Start with an emoji + hook. Include price, bedrooms, location, and one standout feature. Add "DLD: XXXXX" at the end.

Format 2 — Instagram Caption:
Write an engaging Instagram caption. Start with a strong hook. Include all property details in the first 150 chars, then a compelling description, then 8-10 relevant hashtags (#Qatar #DohaRealEstate #LuxuryLiving etc). End with a call to action.

Format 3 — PDF Description (3-4 sentences):
Write a professional property description suitable for a PDF brochure. Highlight the lifestyle, location benefits, and unique selling points.

Return ONLY these three sections, labeled exactly: [[WHATSAPP]], [[INSTAGRAM]], [[PDF]]. Do not add any other text."""

        result = call_llm(prompt)
        if result:
            return _parse_llm_result(result, listing, format_type)

    # Fallback: template-based
    return _generate_template_listing(listing, format_type)


def _parse_llm_result(result, listing, format_type):
    """Parse LLM output into sections."""
    sections = {}
    current = None
    content = []

    for line in result.split("\n"):
        if line.strip().startswith("[[WHATSAPP]]"):
            current = "whatsapp"
            content = []
        elif line.strip().startswith("[[INSTAGRAM]]"):
            sections["whatsapp"] = "\n".join(content).strip()
            current = "instagram"
            content = []
        elif line.strip().startswith("[[PDF]]"):
            sections["instagram"] = "\n".join(content).strip()
            current = "pdf"
            content = []
        elif current:
            content.append(line)

    if current and content:
        sections[current] = "\n".join(content).strip()

    if format_type == "whatsapp":
        return sections.get("whatsapp", _generate_template_listing(listing, "whatsapp"))
    elif format_type == "instagram":
        return sections.get("instagram", _generate_template_listing(listing, "instagram"))
    elif format_type == "pdf":
        return sections.get("pdf", _generate_template_listing(listing, "pdf"))
    return sections


def _generate_template_listing(listing, format_type):
    """Fallback template-based listing generator."""
    loc = listing.get("location", "Qatar")
    prop_type = listing.get("type", "Property")
    price = listing.get("price", 0)
    area = listing.get("area", 0)
    bedrooms = listing.get("bedrooms", 0)
    bathrooms = listing.get("bathrooms", 0)
    features = listing.get("features", "")
    agent = listing.get("agent_name", listing.get("agent", ""))
    phone = listing.get("agent_phone", listing.get("phone", ""))

    loc_ar = ARABIC_LOCATIONS.get(loc, loc)
    type_ar = ARABIC_TYPES.get(prop_type, prop_type)
    price_fmt = f"QAR {price:,}"
    price_fmt_ar = format_price_arabic(price)
    area_fmt = f"{area} sqm"

    features_list = [f.strip() for f in features.split(",") if f.strip()]
    feat_bullets = " • ".join(features_list[:5]) if features_list else ""

    if format_type == "whatsapp":
        feat_part = features_list[0] if features_list else "modern finishes"
        hook = "🏠" if bedrooms and int(bedrooms) >= 2 else "🏡"
        return f"""{hook} {prop_type} in {loc} — {price_fmt}
{bedrooms}BR / {bathrooms}BA / {area_fmt}
✨ {feat_part}
📍 {loc_ar}
📞 {phone}
DLD: Ready to transfer | {agent}"""

    elif format_type == "instagram":
        hashtags = " ".join([
            "#QatarRealEstate", "#DohaLiving", f"#{loc.replace(' ', '')}RealEstate",
            "#LuxuryHomes", "#InvestmentProperty", "#QatarProperty",
            "#DohaProperties", "#RealEstateQatar", "#PropertyDoha"
        ])
        return f"""{prop_type} in {loc} — {price_fmt}
━━━━━━━━━━━━━━━━━━━━
📍 Location: {loc_ar}
🛏 Bedrooms: {bedrooms} | 🛁 Bathrooms: {bathrooms} | 📐 Area: {area_fmt}
{'• ' + ' • '.join(features_list[:4]) if features_list else ''}
━━━━━━━━━━━━━━━━━━━━
{features_list[0] if features_list else 'Modern finish, prime location, excellent investment.'}
━━━━━━━━━━━━━━━━━━━━
📞 {phone} | {agent}
{hashtags}"""

    elif format_type == "pdf":
        feat_str = features_list[:3]
        feat_ar = en_to_ar(", ".join(feat_str)) if feat_str else ""
        return f"""PROPERTY DESCRIPTION

Location: {loc}, Qatar
Type: {prop_type}
Price: {price_fmt} ({price_fmt_ar})
Area: {area_fmt}

A stunning {bedrooms}-bedroom {prop_type.lower()} situated in the heart of {loc}. This property offers {area} square meters of meticulously designed living space, perfect for those seeking a blend of modern comfort and Arabian charm.

Key Highlights:
• {bedrooms} Bedrooms | {bathrooms} Bathrooms
• {feat_bullets}
• Prime location in {loc}

This property represents an exceptional opportunity for both personal residence and investment in Qatar's thriving real estate market. Contact {agent} at {phone} for viewing arrangements.

Reference: {listing.get('id', 'N/A')}"""

    return ""


# ─── Commands ─────────────────────────────────────────────────────────────────

def cmd_new(args):
    """Create a new property listing."""
    counter_month, _ = check_limit()

    if not args.pro and counter_month >= 3:
        logger.info("Free tier limited to 3 listings/month.")
        logger.info("Use --pro for unlimited ($59 one-time).")
        sys.exit(1)

    # Validate required
    if not args.location or not args.type or not args.price:
        logger.error("ERROR: --location, --type, and --price are required.")
        sys.exit(1)

    listings = load_listings()
    api_key, _ = get_llm_api_key()

    listing_id = f"LST-{len(listings) + 1:04d}"
    today = datetime.now().date().isoformat()

    listing = {
        "id": listing_id,
        "location": args.location,
        "type": args.type,
        "price": args.price,
        "area": args.area or 0,
        "bedrooms": args.bedrooms or 0,
        "bathrooms": args.bathrooms or 0,
        "features": args.features or "",
        "agent_name": args.agent or "",
        "agent_phone": args.phone or "",
        "created_at": datetime.now().isoformat(),
        "active": True,
    }

    # Generate all formats
    enhanced = generate_listing_enhanced(listing, "whatsapp", bool(api_key))
    listing["formats"] = {
        "whatsapp": generate_listing_enhanced(listing, "whatsapp", bool(api_key)),
        "instagram": generate_listing_enhanced(listing, "instagram", bool(api_key)),
        "pdf": generate_listing_enhanced(listing, "pdf", bool(api_key)),
    }

    # Build English + Arabic listing
    loc_ar = ARABIC_LOCATIONS.get(args.location, args.location)
    type_ar = ARABIC_TYPES.get(args.type, args.type)
    price_ar = format_price_arabic(args.price)
    area_fmt = f"{args.area or 0} متر مربع"

    listing["bilingual"] = {
        "location": f"{args.location} / {loc_ar}",
        "type": f"{args.type} / {type_ar}",
        "price": f"QAR {args.price:,} / {price_ar}",
        "area": f"{(args.area or 0)} sqm / {area_fmt}",
        "bedrooms": f"{args.bedrooms or 0} / {to_arabic_numeral(args.bedrooms or 0)}",
        "bathrooms": f"{args.bathrooms or 0} / {to_arabic_numeral(args.bathrooms or 0)}",
        "features": f"{args.features or ''} / {en_to_ar(args.features or '')}",
    }

    listings.append(listing)
    save_listings(listings)
    increment_counter()

    logger.info(f"\n{'=' * 60}")
    logger.info(f"Listing {listing_id} created")
    logger.info(f"{'=' * 60}")
    logger.info(f"EN: {listing['bilingual']['type']} in {listing['bilingual']['location']}")
    logger.info(f"AR: {listing['bilingual']['type']}")
    logger.info(f"Price: {listing['bilingual']['price']}")
    print()

    if args.format:
        fmt = args.format.lower()
        if fmt in listing["formats"]:
            logger.info(f"--- {fmt.upper()} FORMAT ---")
            print(listing["formats"][fmt])
        else:
            logger.info(f"Unknown format: {fmt}. Options: whatsapp | instagram | pdf")
            for name, content in listing["formats"].items():
                logger.info(f"\n--- {name.upper()} FORMAT ---")
                print(content)
    else:
        # Show all formats
        for name, content in listing["formats"].items():
            logger.info(f"\n--- {name.upper()} FORMAT ---")
            print(content)


def cmd_bulk(args):
    """Bulk generate from CSV."""
    if not os.path.isfile(args.csv):
        logger.info(f"CSV not found: {args.csv}")
        sys.exit(1)

    rows = []
    try:
        with open(args.csv) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        logger.info(f"Failed to read CSV: {e}")
        sys.exit(1)

    logger.info(f"\nGenerating {len(rows)} listings...")
    api_key, _ = get_llm_api_key()
    listings = load_listings()
    counter = load_counter()
    month = datetime.now().strftime("%Y-%m")

    for i, row in enumerate(rows):
        # Check limit
        if counter.get("month") != month:
            counter = {"month": month, "count": 0}
        if not args.pro and counter["count"] >= 3:
            logger.info(f"Free tier limit reached (3/month). Stopped at {i} listings.")
            break

        location = row.get("location", row.get("Location", "Qatar"))
        prop_type = row.get("type", row.get("Type", "Property"))
        try:
            price = int(row.get("price", row.get("Price", 0)))
        except ValueError:
            price = 0
        area = int(row.get("area", row.get("Area", 0))) or 0
        bedrooms = int(row.get("bedrooms", row.get("Bedrooms", 0))) or 0
        bathrooms = int(row.get("bathrooms", row.get("Bathrooms", 0))) or 0
        features = row.get("features", row.get("Features", ""))
        agent = row.get("agent", row.get("Agent", ""))
        phone = row.get("phone", row.get("Phone", ""))

        listing_id = f"LST-{len(listings) + 1:04d}"

        listing = {
            "id": listing_id,
            "location": location,
            "type": prop_type,
            "price": price,
            "area": area,
            "bedrooms": bedrooms,
            "bathrooms": bathrooms,
            "features": features,
            "agent_name": agent,
            "agent_phone": phone,
            "created_at": datetime.now().isoformat(),
            "active": True,
            "formats": {
                "whatsapp": generate_listing_enhanced({
                    "location": location, "type": prop_type, "price": price,
                    "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms,
                    "features": features, "agent_name": agent, "agent_phone": phone,
                }, "whatsapp", bool(api_key)),
                "instagram": generate_listing_enhanced({
                    "location": location, "type": prop_type, "price": price,
                    "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms,
                    "features": features, "agent_name": agent, "agent_phone": phone,
                }, "instagram", bool(api_key)),
                "pdf": generate_listing_enhanced({
                    "location": location, "type": prop_type, "price": price,
                    "area": area, "bedrooms": bedrooms, "bathrooms": bathrooms,
                    "features": features, "agent_name": agent, "agent_phone": phone,
                }, "pdf", bool(api_key)),
            },
        }

        listings.append(listing)
        counter["count"] += 1
        logger.info(f"  [{i+1}/{len(rows)}] {listing_id}: {prop_type} in {location} - QAR {price:,}")

    save_listings(listings)
    save_counter(counter)
    logger.info(f"\nDone. {len(rows)} listings saved.")


def cmd_format(args):
    """Format a saved listing."""
    listings = load_listings()

    listing = None
    for lst in listings:
        if lst.get("id") == args.listing_id:
            listing = lst
            break

    if not listing:
        logger.info(f"Listing '{args.listing_id}' not found.")
        sys.exit(1)

    fmt = args.format.lower()
    if fmt not in ["whatsapp", "instagram", "pdf", "all"]:
        logger.info("Format must be: whatsapp | instagram | pdf | all")
        sys.exit(1)

    if fmt == "all":
        for name, content in listing.get("formats", {}).items():
            logger.info(f"\n{'=' * 60}")
            logger.info(f" {name.upper()} FORMAT")
            logger.info(f"{'=' * 60}")
            print(content)
    else:
        logger.info(f"{'=' * 60}")
        logger.info(f" {fmt.upper()} FORMAT")
        logger.info(f"{'=' * 60}")
        print(listing.get("formats", {}).get(fmt, "(not found)"))


def cmd_list(args):
    """List all saved listings."""
    listings = load_listings()
    counter, _ = check_limit()
    month = datetime.now().strftime("%Y-%m")

    if not listings:
        logger.info("No listings yet. Create one with:")
        logger.info("  property-listing new --location 'Lusail' --type '2BR Apartment' --price 450000 --area 120")
        return

    logger.info(f"\nProperty Listings ({len(listings)} total, {counter}/3 used this month)")
    logger.info(f"{'ID':<10} {'Location':<20} {'Type':<20} {'Price':<15} {'Created':<12}")
    logger.info("-" * 80)
    for lst in listings:
        loc = lst.get("location", "?")[:20]
        prop_type = lst.get("type", "?")[:20]
        price = f"QAR {lst.get('price', 0):,}"
        created = lst.get("created_at", "")[:10]
        status = "ACTIVE" if lst.get("active") else "SOLD"
        logger.info(f"{lst.get('id', '?'):<10} {loc:<20} {prop_type:<20} {price:<15} {created:<12} [{status}]")


def cmd_agents(args):
    """Manage agent profiles."""
    agents = load_agents()

    if args.add:
        if args.name and args.phone:
            agents.append({
                "name": args.name,
                "phone": args.phone,
                "agency": args.agency or "",
                "added_at": datetime.now().isoformat(),
            })
            save_agents(agents)
            logger.info(f"OK Agent '{args.name}' added.")
        else:
            logger.info("--name and --phone required for --add")
            sys.exit(1)
        return

    if not agents:
        logger.info("No agents yet. Add one with:")
        logger.info("  property-listing agents --add --name 'Nasser' --phone '+974XXX' --agency 'Halaqa'")
        return

    logger.info(f"\nAgents ({len(agents)}):")
    for a in agents:
        logger.info(f"  {a.get('name')} | {a.get('phone')} | {a.get('agency', '')}")


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="MENA Property Listing Generator")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress info logging")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # new
    p_new = subparsers.add_parser("new", help="Create a new property listing")
    p_new.add_argument("--location", help="Location (e.g., Lusail, The Pearl Qatar)")
    p_new.add_argument("--type", help="Property type (e.g., 2BR Apartment, Villa)")
    p_new.add_argument("--price", type=int, help="Price in QAR")
    p_new.add_argument("--area", type=int, help="Area in sqm")
    p_new.add_argument("--bedrooms", type=int, help="Number of bedrooms")
    p_new.add_argument("--bathrooms", type=int, help="Number of bathrooms")
    p_new.add_argument("--features", help="Comma-separated features")
    p_new.add_argument("--agent", help="Agent name")
    p_new.add_argument("--phone", help="Agent phone number")
    p_new.add_argument("--format", help="whatsapp | instagram | pdf (default: all)")
    p_new.add_argument("--pro", action="store_true", help="Pro tier (bypass 3/month limit)")
    p_new.set_defaults(func=cmd_new)

    # bulk
    p_bulk = subparsers.add_parser("bulk", help="Bulk generate from CSV")
    p_bulk.add_argument("--csv", required=True, help="CSV file with property data")
    p_bulk.add_argument("--pro", action="store_true", help="Pro tier")
    p_bulk.set_defaults(func=cmd_bulk)

    # format
    p_fmt = subparsers.add_parser("format", help="Format a saved listing")
    p_fmt.add_argument("--input", dest="listing_id", required=True, help="Listing ID (e.g. LST-0001)")
    p_fmt.add_argument("--format", required=True, help="whatsapp | instagram | pdf | all")
    p_fmt.set_defaults(func=cmd_format)

    # list
    p_list = subparsers.add_parser("list", help="List all saved listings")
    p_list.set_defaults(func=cmd_list)

    # agents
    p_agents = subparsers.add_parser("agents", help="Manage agent profiles")
    p_agents.add_argument("--add", action="store_true", help="Add a new agent")
    p_agents.add_argument("--name", help="Agent name")
    p_agents.add_argument("--phone", help="Agent phone")
    p_agents.add_argument("--agency", help="Agency name")
    p_agents.set_defaults(func=cmd_agents)

    args = parser.parse_args()
    configure_logging(verbose=getattr(args, "verbose", False), quiet=getattr(args, "quiet", False))
    logger.debug(f"mena-property-listing-generator v{__version__}")
    args.func(args)


if __name__ == "__main__":
    main()