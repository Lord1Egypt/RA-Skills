#!/usr/bin/env python3
"""
Styx Universal Enrichment — Google Places enrichment for ALL non-financial merchant categories.

Covers: retail, service, entertainment, transport, personal_care, medical, home,
        government, housing, travel, food/restaurant (everything styx_places_enrich.py
        handles plus all the non-food categories it misses).

Skips: transfer, income, bank_fees, loan_payments, loan_disbursements
       (no physical location — pure financial plumbing).

Usage:
    python3 styx_universal_enrich.py [--limit 50] [--dry-run] [--all]

    --all    Re-enrich merchants already marked source='google_places'
    --limit  Max merchants to process (default 50, use 0 for all)
"""
import json
import os
import re
import sqlite3
import sys
import time
import urllib.error
import urllib.request

STYX_DB  = os.path.expanduser("~/.hermes/data/styx.db")
TXN_DB   = os.path.expanduser("~/.hermes/data/transactions.db")

SKIP_CATEGORIES = {
    "transfer", "transfer_in", "transfer_out",
    "income", "bank_fees", "loan_payments",
    "loan_disbursements", "rent_and_utilities",
}


def load_api_key():
    with open(os.path.expanduser("~/.hermes/secrets/plaid.env")) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                if k.strip() == "GOOGLE_PLACES_API_KEY":
                    return v.strip()
    return None


def parse_formatted_address(addr):
    """
    Parse Google Places formattedAddress → (city, state_or_region, postcode).
    US:   '525 Market St, San Francisco, CA 94105, USA' → ('San Francisco', 'CA', '94105')
    UK:   '92 Station Rd., Soham, ELY CB7 5DZ, UK'     → ('Soham', 'UK', 'CB7 5DZ')
    City: 'Berkeley, CA, USA'                            → ('Berkeley', 'CA', None)
    """
    if not addr:
        return None, None, None
    parts = [p.strip() for p in addr.split(",")]
    if len(parts) < 2:
        return None, None, None
    # US with zip
    for i, p in enumerate(parts):
        m = re.match(r"^([A-Z]{2})\s+(\d{5}(?:-\d{4})?)$", p)
        if m and i >= 1:
            city = parts[i - 1].strip()
            if re.match(r"^[A-Za-z\s\.\-\']+$", city):
                return city, m.group(1), m.group(2)
    # US city-only: 'City, ST, USA'
    if parts[-1] in ("USA", "US") and len(parts) >= 3:
        state_part = parts[-2].strip()
        if re.match(r"^[A-Z]{2}$", state_part):
            city = parts[-3].strip()
            if re.match(r"^[A-Za-z\s\.\-\']+$", city):
                return city, state_part, None
    # UK
    if parts[-1].strip() in ("UK", "United Kingdom") and len(parts) >= 3:
        region_postcode = parts[-2].strip()
        uk_m = re.match(r"^(.+?)\s+([A-Z]{1,2}\d[\dA-Z]?\s*\d[A-Z]{2})$", region_postcode)
        if uk_m and len(parts) >= 4:
            city = parts[-3].strip()
            return city, "UK", uk_m.group(2).strip()
        city = parts[-2].strip()
        if re.match(r"^[A-Za-z\s\.\-\']+$", city):
            return city, "UK", None
    # Generic international
    country = parts[-1].strip()
    if re.match(r"^[A-Za-z\s]+$", country) and len(parts) >= 2:
        city = parts[-2].strip()
        if re.match(r"^[A-Za-z\s\.\-\']+$", city) and city.lower() != country.lower():
            return city, country, None
    return None, None, None


_PREFIX_RE = re.compile(
    r"^(ABM-|TCB\*|MED\*|FSP\*|ABC\*|TST\*|DD\s+\*DOORDASH\s+|DD\s+\*|"
    r"POSH\*|AMZN\s*|TGT[*\s]|WMT[*\s]|SP\s+|MS\*|SQ\s*\*|"
    r"UBER\s+\*|LYFT\s+\*)",
    re.IGNORECASE,
)
_TRAILING_RE = re.compile(
    r"\s+(SF|LLC|INC\.?|CORP\.?|LTD\.?|CO\.?|[A-Z]{2})\s*$",
    re.IGNORECASE,
)


def clean_name(name):
    """Strip Plaid prefixes and noise suffixes before Places lookup."""
    n = _PREFIX_RE.sub("", (name or "").strip())
    # Strip truncated suffixes that look like Plaid cutoffs: CLOTHIN → Clothing
    # We just strip the trailing non-word partial word only if short (<= 4 chars)
    n = re.sub(r"\s+[A-Z]{1,4}$", "", n).strip()
    return n or name


def places_search(name, city=None, max_results=3):
    """Query Google Places API (New) for a business."""
    query = name
    if city:
        query = f"{name} {city}"

    payload = json.dumps({
        "textQuery": query,
        "maxResultCount": max_results,
        "languageCode": "en",
    }).encode()

    req = urllib.request.Request(
        "https://places.googleapis.com/v1/places:searchText",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": load_api_key(),
            "X-Goog-FieldMask": (
                "places.displayName,places.formattedAddress,places.types,"
                "places.rating,places.priceLevel,places.websiteUri"
            ),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("places", [])
    except Exception as e:
        print(f"  Places API error for {name!r}: {e}")
        return []


def get_merchants_to_enrich(conn, limit, all_merchants):
    """Return merchants that need enrichment, skipping financial categories."""
    conn.execute(f'ATTACH DATABASE "{TXN_DB}" AS txdb')

    skip_cats = ", ".join(f"'{c}'" for c in SKIP_CATEGORIES)

    where = f"(m.category IS NULL OR m.category NOT IN ({skip_cats}))"
    if not all_merchants:
        where += " AND (m.source IS NULL OR m.source != 'google_places')"

    query = f"""
        SELECT DISTINCT m.id, m.name, m.category, m.city,
               COUNT(DISTINCT tm.transaction_id) as visit_count
        FROM merchants m
        JOIN transaction_merchants tm ON m.id = tm.merchant_id
        JOIN txdb.transactions t ON tm.transaction_id = t.transaction_id
        WHERE {where} AND t.pending = 0
        GROUP BY m.id
        ORDER BY visit_count DESC
    """
    if limit:
        query += f" LIMIT {limit}"

    return conn.execute(query).fetchall()


def enrich_merchant(conn, mid, name, category, city, dry_run):
    """Look up a merchant in Google Places and update the DB."""
    # Use existing city as a search hint if it looks sane
    search_city = None
    if city and not re.search(r'\d', city):
        search_city = city

    cleaned = clean_name(name)
    places = places_search(cleaned, search_city)
    # retry without city hint if nothing found
    if not places and search_city:
        places = places_search(cleaned)
    if not places:
        return False, "no_result"

    place = places[0]
    formatted_addr = place.get("formattedAddress", "")
    display_name   = (place.get("displayName") or {}).get("text", name)
    website        = place.get("websiteUri", "")

    # Derive category from Google types
    type_to_cat = {
        "restaurant": "restaurant", "cafe": "cafe", "bar": "bar",
        "bakery": "bakery", "meal_delivery": "delivery",
        "meal_takeaway": "takeaway", "grocery_or_supermarket": "grocery",
        "supermarket": "supermarket", "convenience_store": "convenience",
        "clothing_store": "retail", "shoe_store": "retail",
        "department_store": "retail", "shopping_mall": "retail",
        "book_store": "retail", "electronics_store": "retail",
        "furniture_store": "retail", "hardware_store": "retail",
        "home_goods_store": "retail", "jewelry_store": "retail",
        "beauty_salon": "personal_care", "hair_care": "personal_care",
        "spa": "personal_care", "gym": "personal_care",
        "hospital": "medical", "doctor": "medical", "pharmacy": "medical",
        "dentist": "medical", "veterinary_care": "medical",
        "gas_station": "transport", "car_repair": "transport",
        "car_wash": "transport", "parking": "transport",
        "subway_station": "transport", "train_station": "transport",
        "lodging": "travel", "hotel": "travel",
        "movie_theater": "entertainment", "night_club": "entertainment",
        "amusement_park": "entertainment", "museum": "entertainment",
        "art_gallery": "entertainment", "bowling_alley": "entertainment",
        "bank": "bank_fees", "atm": "bank_fees",
    }
    google_types = place.get("types", [])
    derived_cat = None
    for t in google_types:
        if t in type_to_cat:
            derived_cat = type_to_cat[t]
            break

    new_city, new_state, new_zip = parse_formatted_address(formatted_addr)

    if not dry_run:
        conn.execute("""
            UPDATE merchants SET
                address   = ?,
                city      = ?,
                state     = ?,
                zip       = ?,
                website   = COALESCE(NULLIF(?, ''), website),
                category  = COALESCE(?, category),
                source    = 'google_places',
                confidence = 0.9,
                updated_at = datetime('now')
            WHERE id = ?
        """, (
            formatted_addr or None,
            new_city,
            new_state,
            new_zip,
            website,
            derived_cat,
            mid,
        ))

    return True, f"{display_name} @ {new_city or '?'}, {new_state or '?'}"


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--all", action="store_true", help="Re-enrich already-enriched merchants")
    args = parser.parse_args()

    api_key = load_api_key()
    if not api_key:
        print("ERROR: GOOGLE_PLACES_API_KEY not found in ~/.hermes/secrets/plaid.env")
        sys.exit(1)

    conn = sqlite3.connect(STYX_DB, timeout=30)
    conn.row_factory = sqlite3.Row

    limit = args.limit if args.limit > 0 else None
    merchants = get_merchants_to_enrich(conn, limit, args.all)
    total = len(merchants)
    print(f"{'DRY RUN — ' if args.dry_run else ''}Enriching {total} merchants via Google Places...\n")

    enriched = 0
    failed = 0

    for i, row in enumerate(merchants):
        mid, name, category, city, visits = row["id"], row["name"], row["category"], row["city"], row["visit_count"]
        ok, detail = enrich_merchant(conn, mid, name, category, city, args.dry_run)
        status = "✓" if ok else "✗"
        print(f"  {status} [{category or '?':15s}] {name[:35]:35s}  {visits}v  {detail}")
        if ok:
            enriched += 1
        else:
            failed += 1
        time.sleep(0.25)  # rate limit

    if not args.dry_run:
        conn.commit()

    conn.close()

    print(f"\n{'='*60}")
    print(f"Done ({'dry run' if args.dry_run else 'live'}):")
    print(f"  Enriched: {enriched}")
    print(f"  Failed:   {failed}")


if __name__ == "__main__":
    main()