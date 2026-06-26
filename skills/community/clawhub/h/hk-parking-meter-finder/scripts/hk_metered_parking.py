#!/usr/bin/env python3
import argparse
import csv
import io
import json
import math
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher

SPACEINFO_URL = "https://resource.data.one.gov.hk/td/psiparkingspaces/spaceinfo/parkingspaces.csv"
OCCUPANCY_URL = "https://resource.data.one.gov.hk/td/psiparkingspaces/occupancystatus/occupancystatus.csv"
UA = "Mozilla/5.0 (OpenClaw hk-metered-parking skill)"

VEHICLE_TYPE = {
    "A": "private car / light goods vehicle",
    "M": "motorcycle",
    "G": "goods vehicle",
    "B": "bus",
}
OCCUPANCY_LABEL = {"V": "vacant", "O": "occupied"}
METER_STATUS_LABEL = {"N": "normal", "NU": "not in use"}


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://data.gov.hk/"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8-sig", "ignore")


def load_spaceinfo():
    text = fetch_text(SPACEINFO_URL)
    lines = text.splitlines()
    as_of = lines[0].strip() if lines else ""
    rows = csv.DictReader(io.StringIO("\n".join(lines[2:])))
    data = []
    for row in rows:
        row["Latitude"] = float(row["Latitude"])
        row["Longitude"] = float(row["Longitude"])
        data.append(row)
    return as_of, data


def load_occupancy():
    text = fetch_text(OCCUPANCY_URL)
    rows = csv.DictReader(io.StringIO(text))
    return {row["ParkingSpaceId"]: row for row in rows}


def normalize(text: str) -> str:
    text = (text or "").strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str):
    base = normalize(text)
    ascii_tokens = re.findall(r"[a-z0-9]+", base)
    han_tokens = re.findall(r"[\u4e00-\u9fff]{1,}", text or "")
    tokens = set(ascii_tokens + han_tokens)
    return {t for t in tokens if t}


def haversine_m(lat1, lon1, lat2, lon2):
    r = 6371000
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def build_search_text(row):
    parts = [
        row.get("Region", ""), row.get("Region_tc", ""), row.get("Region_sc", ""),
        row.get("District", ""), row.get("District_tc", ""), row.get("District_sc", ""),
        row.get("SubDistrict", ""), row.get("SubDistrict_tc", ""), row.get("SubDistrict_sc", ""),
        row.get("Street", ""), row.get("Street_tc", ""), row.get("Street_sc", ""),
        row.get("SectionOfStreet", ""), row.get("SectionOfStreet_tc", ""), row.get("SectionOfStreet_sc", ""),
        row.get("ParkingSpaceId", ""),
    ]
    return " | ".join(p for p in parts if p)


def score_row(query, row):
    qn = normalize(query)
    qt = tokenize(query)
    text = build_search_text(row)
    tn = normalize(text)
    tt = tokenize(text)
    score = 0.0
    for token in qt:
        if token in tt:
            score += 3.0 + min(len(token), 8) * 0.1
        elif token in tn:
            score += 1.8
        else:
            best = 0.0
            for candidate in tt:
                if abs(len(candidate) - len(token)) > 4:
                    continue
                ratio = SequenceMatcher(None, token, candidate).ratio()
                if ratio > best:
                    best = ratio
            if best >= 0.72:
                score += best * 1.5
    if qn and qn in tn:
        score += 5.0
    score += SequenceMatcher(None, qn, tn[: max(len(qn), 1) * 4]).ratio()
    return score


def group_key(row):
    return (
        row.get("District_tc") or row.get("District") or "",
        row.get("SubDistrict_tc") or row.get("SubDistrict") or "",
        row.get("Street_tc") or row.get("Street") or "",
        row.get("SectionOfStreet_tc") or row.get("SectionOfStreet") or "",
        row.get("VehicleType") or "",
        row.get("OperatingPeriod") or "",
    )


def describe_group(key):
    district, subdistrict, street, section, vehicle_type, operating_period = key
    parts = [p for p in [district, subdistrict, street, section] if p]
    label = " / ".join(parts)
    extras = []
    if vehicle_type:
        extras.append(VEHICLE_TYPE.get(vehicle_type, vehicle_type))
    if operating_period:
        extras.append(f"period {operating_period}")
    if extras:
        label += f" ({', '.join(extras)})"
    return label


def join_rows(space_rows, occupancy_map):
    joined = []
    for row in space_rows:
        occ = occupancy_map.get(row["ParkingSpaceId"], {})
        merged = dict(row)
        merged["OccupancyStatus"] = occ.get("OccupancyStatus", "")
        merged["OccupancyLabel"] = OCCUPANCY_LABEL.get(occ.get("OccupancyStatus", ""), "unknown")
        merged["ParkingMeterStatus"] = occ.get("ParkingMeterStatus", "")
        merged["ParkingMeterStatusLabel"] = METER_STATUS_LABEL.get(occ.get("ParkingMeterStatus", ""), "unknown")
        merged["OccupancyDateChanged"] = occ.get("OccupancyDateChanged", "")
        joined.append(merged)
    return joined


def search(joined, query, max_groups, max_spaces, vacant_only=False, occupied_only=False):
    scored = []
    for row in joined:
        row = dict(row)
        row["_score"] = score_row(query, row)
        if row["_score"] <= 0.25:
            continue
        if vacant_only and row.get("OccupancyStatus") != "V":
            continue
        if occupied_only and row.get("OccupancyStatus") != "O":
            continue
        scored.append(row)
    scored.sort(key=lambda r: (-r["_score"], r["District_tc"], r["Street_tc"], r["ParkingSpaceId"]))

    groups = defaultdict(list)
    for row in scored:
        groups[group_key(row)].append(row)

    ranked_groups = []
    for key, rows in groups.items():
        top = rows[0]
        avg_lat = sum(r["Latitude"] for r in rows) / len(rows)
        avg_lon = sum(r["Longitude"] for r in rows) / len(rows)
        ranked_groups.append({
            "key": key,
            "label": describe_group(key),
            "score": max(r["_score"] for r in rows),
            "vacant": sum(1 for r in rows if r.get("OccupancyStatus") == "V"),
            "occupied": sum(1 for r in rows if r.get("OccupancyStatus") == "O"),
            "unknown": sum(1 for r in rows if r.get("OccupancyStatus") not in {"V", "O"}),
            "total": len(rows),
            "latitude": avg_lat,
            "longitude": avg_lon,
            "spaces": sorted(rows, key=lambda r: (r.get("OccupancyStatus") != "V", -r["_score"], r["ParkingSpaceId"]))[:max_spaces],
            "top": top,
        })
    ranked_groups.sort(key=lambda g: (-g["score"], g["label"]))
    return ranked_groups[:max_groups]


def google_maps_link(lat, lon):
    return f"https://maps.google.com/?q={lat:.6f},{lon:.6f}"



def format_text(groups, query, as_of):
    lines = []
    header = f"Metered street parking matches for: {query}"
    if as_of:
        header += f" (space info as of {as_of})"
    lines.append(header)
    if not groups:
        lines.append("No likely match found in the official metered parking datasets.")
        return "\n".join(lines)
    for i, g in enumerate(groups, 1):
        lines.append(f"\n{i}. {g['label']}")
        lines.append(f"   Vacant {g['vacant']} | Occupied {g['occupied']} | Unknown {g['unknown']} | Total {g['total']}")
        lines.append(f"   Approx centre: {g['latitude']:.6f}, {g['longitude']:.6f}")
        lines.append(f"   Google Maps: {google_maps_link(g['latitude'], g['longitude'])}")
        seen = 0
        for row in g['spaces']:
            changed = row.get('OccupancyDateChanged') or 'n/a'
            lines.append(
                f"   - {row['ParkingSpaceId']}: {row['OccupancyLabel']}, meter {row['ParkingMeterStatusLabel']}, changed {changed}"
            )
            seen += 1
        if g['total'] > seen:
            lines.append(f"   - ... {g['total'] - seen} more spaces in this cluster")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Find Hong Kong metered street parking spaces and live vacancy by street/area keyword.")
    p.add_argument('query', nargs='+', help='Street / area / district keyword, e.g. 富善街 大埔 or 廣福坊')
    p.add_argument('--limit-groups', type=int, default=5)
    p.add_argument('--limit-spaces', type=int, default=8)
    p.add_argument('--vacant-only', action='store_true')
    p.add_argument('--occupied-only', action='store_true')
    p.add_argument('--json', action='store_true')
    args = p.parse_args()

    if args.vacant_only and args.occupied_only:
        print('--vacant-only and --occupied-only cannot be used together', file=sys.stderr)
        sys.exit(2)

    query = ' '.join(args.query)
    as_of, spaces = load_spaceinfo()
    occupancy = load_occupancy()
    joined = join_rows(spaces, occupancy)
    groups = search(joined, query, args.limit_groups, args.limit_spaces, args.vacant_only, args.occupied_only)

    payload = {
        'query': query,
        'spaceInfoAsOf': as_of,
        'generatedAt': datetime.utcnow().isoformat() + 'Z',
        'groups': [
            {
                'label': g['label'],
                'score': round(g['score'], 3),
                'vacant': g['vacant'],
                'occupied': g['occupied'],
                'unknown': g['unknown'],
                'total': g['total'],
                'latitude': g['latitude'],
                'longitude': g['longitude'],
                'googleMaps': google_maps_link(g['latitude'], g['longitude']),
                'spaces': [
                    {
                        'parkingSpaceId': r['ParkingSpaceId'],
                        'districtTc': r['District_tc'],
                        'subDistrictTc': r['SubDistrict_tc'],
                        'streetTc': r['Street_tc'],
                        'sectionOfStreetTc': r['SectionOfStreet_tc'],
                        'vehicleType': r['VehicleType'],
                        'occupancyStatus': r['OccupancyStatus'],
                        'occupancyLabel': r['OccupancyLabel'],
                        'parkingMeterStatus': r['ParkingMeterStatus'],
                        'parkingMeterStatusLabel': r['ParkingMeterStatusLabel'],
                        'occupancyDateChanged': r['OccupancyDateChanged'],
                        'latitude': r['Latitude'],
                        'longitude': r['Longitude'],
                    }
                    for r in g['spaces']
                ],
            }
            for g in groups
        ],
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(format_text(groups, query, as_of))


if __name__ == '__main__':
    main()
