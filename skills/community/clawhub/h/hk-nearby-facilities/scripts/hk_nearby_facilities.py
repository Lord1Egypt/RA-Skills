#!/usr/bin/env python3
import argparse
import html
import json
import math
import re
import sys
import urllib.parse
import urllib.request
from difflib import SequenceMatcher

BASE = "https://www.fehd.gov.hk/english/map"
UA = {"User-Agent": "OpenClaw/1.0"}

AREA_ALIASES = {
    "大角咀": ["大角咀", "tai kok tsui", "晏架街", "櫻桃街", "詩歌舞街", "海庭道", "大角咀道", "福全街"],
    "大埔墟": ["大埔墟", "tai po market", "港鐵大埔墟站", "大埔舊墟", "寶湖道", "北盛街", "廣福里", "富善街"],
    "富善街": ["富善街", "寶湖道", "北盛街", "同發坊", "同秀坊", "同茂坊", "廣福里"],
}

DISTRICT_URL = f"{BASE}/getDistrict.php"
TOILET_URL = f"{BASE}/getMapData.php?type=toilet"
ACCESSIBLE_URL = f"{BASE}/getAccessibleToilets.php?type=toilet"
UNIVERSAL_URL = f"{BASE}/getUniversalToilets.php?type=toilet"


def fetch_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def normalize(text):
    text = html.unescape(text or "")
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def query_terms(query):
    nq = normalize(query)
    terms = [t for t in re.split(r"\s+", nq) if t]
    if not terms and nq:
        terms = [nq]

    expanded = []
    for term in terms:
        expanded.append(term)
        for alias_key, aliases in AREA_ALIASES.items():
            if term == normalize(alias_key):
                expanded.extend(normalize(x) for x in aliases)
    seen = set()
    result = []
    for term in expanded:
        if term and term not in seen:
            seen.add(term)
            result.append(term)
    return result


def score_item(item, query):
    haystacks = [
        item.get("nameEN", ""), item.get("nameTC", ""), item.get("nameSC", ""),
        item.get("addressEN", ""), item.get("addressTC", ""), item.get("addressSC", ""),
        item.get("district_resolved_en", ""), item.get("district_resolved_tc", ""),
        item.get("districtNameEN", ""), item.get("districtNameTC", ""), item.get("districtNameSC", ""),
    ]
    joined = " | ".join(normalize(x) for x in haystacks if x)
    nq = normalize(query)
    if not joined or not nq:
        return 0.0

    score = SequenceMatcher(None, nq, joined).ratio()
    terms = query_terms(query)
    exact_hits = 0
    partial_hits = 0

    for term in terms:
        if term in joined:
            exact_hits += 1
            score += 2.0 if len(term) >= 2 else 0.2
        elif len(term) >= 4:
            score -= 1.0
        elif len(term) >= 2:
            for n in range(len(term) - 1, 1, -1):
                found = False
                for i in range(0, len(term) - n + 1):
                    sub = term[i:i + n]
                    if sub in joined:
                        partial_hits += 1
                        score += 0.15 * n
                        found = True
                        break
                if found:
                    break

    if nq in joined:
        score += 3.0
    if exact_hits == 0 and len(terms) == 1 and len(terms[0]) >= 3:
        score -= 1.5
    if exact_hits == 0 and partial_hits == 0:
        score -= 0.5
    return score


def maps_link(lat, lng):
    if lat and lng:
        return f"https://maps.google.com/?q={lat},{lng}"
    return None


def haversine_m(lat1, lng1, lat2, lng2):
    r = 6371000
    p1 = math.radians(float(lat1))
    p2 = math.radians(float(lat2))
    dlat = math.radians(float(lat2) - float(lat1))
    dlng = math.radians(float(lng2) - float(lng1))
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlng / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def split_latlng(value):
    if not value:
        return None, None
    parts = [p.strip() for p in str(value).split(",", 1)]
    if len(parts) == 2:
        return parts[0], parts[1]
    return None, None


def load_toilets():
    toilets = fetch_json(TOILET_URL)
    accessible_ids = {str(x.get("mapID")) for x in fetch_json(ACCESSIBLE_URL)}
    universal_ids = {str(x.get("mapID")) for x in fetch_json(UNIVERSAL_URL)}
    districts = {x.get("districtID"): x for x in fetch_json(DISTRICT_URL)}
    for item in toilets:
        item["accessible_unisex"] = str(item.get("mapID")) in accessible_ids
        item["universal_toilet"] = str(item.get("mapID")) in universal_ids
        district = districts.get(item.get("districtID"), {})
        item["district_resolved_tc"] = district.get("nameTC") or item.get("districtNameTC")
        item["district_resolved_en"] = district.get("nameEN") or item.get("districtNameEN")
        lat, lng = split_latlng(item.get("latitude"))
        item["lat"] = lat
        item["lng"] = lng
    return toilets


def filter_toilets(items, query, accessible_only=False, universal_only=False, limit=5, lat=None, lng=None):
    if lat is not None and lng is not None:
        ranked = []
        for item in items:
            if accessible_only and not item.get("accessible_unisex"):
                continue
            if universal_only and not item.get("universal_toilet"):
                continue
            if not item.get("lat") or not item.get("lng"):
                continue
            dist = haversine_m(lat, lng, item.get("lat"), item.get("lng"))
            item = dict(item)
            item["distance_m"] = round(dist)
            ranked.append((dist, item))
        ranked.sort(key=lambda x: x[0])
        return [item for _, item in ranked[:limit]]

    ranked = []
    terms = query_terms(query)
    primary_terms = [t for t in re.split(r"\s+", normalize(query)) if t] or [normalize(query)]

    for item in items:
        if accessible_only and not item.get("accessible_unisex"):
            continue
        if universal_only and not item.get("universal_toilet"):
            continue
        haystacks = [
            item.get("nameEN", ""), item.get("nameTC", ""), item.get("nameSC", ""),
            item.get("addressEN", ""), item.get("addressTC", ""), item.get("addressSC", ""),
            item.get("district_resolved_en", ""), item.get("district_resolved_tc", ""),
        ]
        joined = " | ".join(normalize(x) for x in haystacks if x)
        primary_coverage = sum(1 for term in primary_terms if len(term) >= 2 and term in joined)
        alias_coverage = sum(1 for term in terms if len(term) >= 2 and term in joined)
        ranked.append((primary_coverage, alias_coverage, score_item(item, query), item))

    ranked.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    full_primary_coverage = len([t for t in primary_terms if len(t) >= 2])
    if ranked and ranked[0][0] > 0 and ranked[0][0] >= full_primary_coverage:
        best_primary = ranked[0][0]
        return [item for primary, alias, score, item in ranked if primary == best_primary][:limit]
    if ranked and ranked[0][1] > 0:
        best_alias = ranked[0][1]
        return [item for primary, alias, score, item in ranked if alias == best_alias][:limit]
    if ranked and ranked[0][0] > 0:
        best_primary = ranked[0][0]
        return [item for primary, alias, score, item in ranked if primary == best_primary][:limit]
    return [item for primary, alias, score, item in ranked if score > 0][:limit]


def display_toilets(items, query):
    print(f"Nearby public toilet matches for: {query}\n")
    if not items:
        print("No likely matches found.")
        return
    for i, item in enumerate(items, 1):
        name = item.get("nameTC") or item.get("nameEN")
        district = item.get("district_resolved_tc") or item.get("district_resolved_en")
        address = item.get("addressTC") or item.get("addressEN")
        lat = item.get("lat") or item.get("latitude")
        lng = item.get("lng") or item.get("longitude")
        print(f"{i}. {name}")
        print(f"   District: {district}")
        print(f"   Address: {address}")
        if item.get("distance_m") is not None:
            print(f"   Distance: {item['distance_m']} m")
        flags = []
        if item.get("accessible_unisex"):
            flags.append("accessible unisex toilet")
        if item.get("universal_toilet"):
            flags.append("universal toilet")
        if flags:
            print(f"   Features: {', '.join(flags)}")
        link = maps_link(lat, lng)
        if link:
            print(f"   Google Maps: {link}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Find nearby Hong Kong facilities by place keyword")
    parser.add_argument("facility", choices=["toilet"], help="facility type")
    parser.add_argument("keywords", nargs="*", help="place keywords")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--lat", type=float)
    parser.add_argument("--lng", type=float)
    parser.add_argument("--accessible-only", action="store_true")
    parser.add_argument("--universal-only", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    query = " ".join(args.keywords) if args.keywords else "shared location"

    if args.facility == "toilet":
        items = load_toilets()
        results = filter_toilets(
            items,
            query,
            accessible_only=args.accessible_only,
            universal_only=args.universal_only,
            limit=args.limit,
            lat=args.lat,
            lng=args.lng,
        )
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            display_toilets(results, query)
        return

    print(f"Unsupported facility type: {args.facility}", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
