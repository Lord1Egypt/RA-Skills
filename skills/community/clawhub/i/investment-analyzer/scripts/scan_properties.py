#!/usr/bin/env python3
import json
import sys
import re
import requests
from datetime import datetime

try:
    from bs4 import BeautifulSoup
except ImportError:
    print(json.dumps({"success": False, "error": "beautifulsoup4 not installed. Run: pip install beautifulsoup4"}))
    sys.exit(1)

CENTRIS_BASE = "https://www.centris.ca"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "fr-CA,fr;q=0.9",
    "X-Requested-With": "XMLHttpRequest",
}

RENT_BY_UNITS = {1: 900, 2: 1800, 3: 2700, 4: 3400}
TAX_RATE = 0.011
MAINTENANCE_RATIO = 0.01
INSURANCE_MONTHLY = 150
VACANCY_RATE = 0.05
MORTGAGE_RATE = 0.035
DOWN_PAYMENT = 0.20
AMORT = 25


def mortgage_payment(principal):
    r = MORTGAGE_RATE / 12
    n = AMORT * 12
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


def analyze_quick(price, units):
    rent = RENT_BY_UNITS.get(units, units * 900)
    down = price * DOWN_PAYMENT
    loan = price - down
    eff_rent = rent * (1 - VACANCY_RATE)
    monthly_tax = price * TAX_RATE / 12
    maintenance = price * MAINTENANCE_RATIO / 12
    payment = mortgage_payment(loan)
    expenses = payment + monthly_tax + maintenance + INSURANCE_MONTHLY
    cash_flow = eff_rent - expenses
    noi = (eff_rent - monthly_tax - maintenance - INSURANCE_MONTHLY) * 12
    cap_rate = noi / price
    coc = (cash_flow * 12) / (down + price * TAX_RATE * 0.5)
    grm = price / (rent * 12)
    if cash_flow > 0 and cap_rate >= 0.045 and grm < 20:
        verdict = "✅ BUY"
    elif cap_rate >= 0.045 and grm < 20:
        verdict = "⚠️ INVESTIGATE"
    else:
        verdict = "❌ PASS"
    return {
        "monthly_cash_flow": round(cash_flow),
        "cap_rate_pct": round(cap_rate * 100, 2),
        "cash_on_cash_pct": round(coc * 100, 2),
        "grm": round(grm, 1),
        "estimated_rent": rent,
        "verdict": verdict,
    }


def extract_price(text):
    cleaned = re.sub(r"[^\d]", "", text)
    return int(cleaned) if cleaned else None


def extract_units(text):
    m = re.search(r"(\d)\s*log", text, re.IGNORECASE)
    if m:
        return int(m.group(1))
    for word, n in [("quadruplex", 4), ("triplex", 3), ("duplex", 2)]:
        if word in text.lower():
            return n
    return None


def fetch_listings(city="sherbrooke", min_price=280000, max_price=550000):
    session = requests.Session()
    session.headers.update(HEADERS)
    try:
        session.get(f"{CENTRIS_BASE}/fr/plex~a-vendre~{city}", timeout=15)
        update_resp = session.post(
            f"{CENTRIS_BASE}/Property/UpdateQuery",
            json={"query": {"Filters": [
                {"MetadataId": "MinPrice", "Values": [str(min_price)]},
                {"MetadataId": "MaxPrice", "Values": [str(max_price)]},
            ], "OperationType": "LISTINGS", "Paging": {"StartPosition": 0}}},
            timeout=15,
        )
        insc_resp = session.post(
            f"{CENTRIS_BASE}/Property/GetInscriptions",
            json={"startPosition": 0},
            timeout=15,
        )
        data = insc_resp.json()
        html = data.get("d", {}).get("Result", {}).get("html", "")
        if not html:
            html = data.get("d", {}).get("html", "")
        return html
    except Exception as e:
        return None, str(e)


def parse_listings(html):
    soup = BeautifulSoup(html, "html.parser")
    results = []
    cards = soup.find_all("div", class_=re.compile(r"property-thumbnail-summary", re.I))
    if not cards:
        cards = soup.find_all("div", class_=re.compile(r"col-12 col-sm-6", re.I))
    for card in cards:
        price_el = card.find(class_=re.compile(r"price", re.I))
        addr_el = card.find(class_=re.compile(r"address|civic", re.I))
        desc_el = card.find(class_=re.compile(r"description|category", re.I))
        link_el = card.find("a", href=True)
        price = extract_price(price_el.get_text()) if price_el else None
        address = addr_el.get_text(strip=True) if addr_el else "N/A"
        desc = desc_el.get_text(strip=True) if desc_el else ""
        units = extract_units(desc) or extract_units(card.get_text())
        url = (CENTRIS_BASE + link_el["href"]) if link_el else None
        if price and units:
            results.append({"price": price, "address": address, "units": units, "description": desc, "url": url})
    return results


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--city", default="sherbrooke")
    parser.add_argument("--min-price", type=int, default=280000)
    parser.add_argument("--max-price", type=int, default=550000)
    parser.add_argument("--verdict", default=None, help="Filter: BUY, INVESTIGATE, or all")
    args = parser.parse_args()

    html = fetch_listings(args.city, args.min_price, args.max_price)
    if not html:
        print(json.dumps({"success": False, "error": "Failed to fetch Centris listings. Site may have changed or network issue."}))
        sys.exit(1)

    listings = parse_listings(html)
    output = []
    for l in listings:
        analysis = analyze_quick(l["price"], l["units"])
        entry = {**l, **analysis}
        if args.verdict:
            if args.verdict.upper() not in analysis["verdict"]:
                continue
        output.append(entry)

    output.sort(key=lambda x: x["monthly_cash_flow"], reverse=True)
    print(json.dumps({
        "success": True,
        "scanned_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "city": args.city,
        "total_scanned": len(listings),
        "total_matching": len(output),
        "listings": output,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

