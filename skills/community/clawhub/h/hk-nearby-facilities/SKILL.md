---
name: hk-nearby-facilities
description: Find nearby Hong Kong public facilities by place keyword or shared live location, starting with public toilets (公廁 / washroom / restroom / toilet) using official government data. Use when the user asks in Cantonese, Chinese, or English things like「大埔墟附近有冇公廁」「沙田站最近廁所喺邊」「旺角 public toilet near me」「附近有冇洗手間」or shares coordinates / live location and wants the nearest facility. This skill currently supports public toilets first and can be extended later with other facilities such as petrol stations.
---

# HK Nearby Facilities

Use the bundled script to search Hong Kong public-facility data by place keyword.

## Current scope

- Public toilets (`toilet`) via FEHD official JSON endpoints.
- Future-friendly structure for other facility types later.

## Quick start

```bash
python3 /home/jim/.openclaw/workspace/skills/hk-nearby-facilities/scripts/hk_nearby_facilities.py toilet <place-keywords>
```

Examples:

```bash
python3 /home/jim/.openclaw/workspace/skills/hk-nearby-facilities/scripts/hk_nearby_facilities.py toilet 大埔墟
python3 /home/jim/.openclaw/workspace/skills/hk-nearby-facilities/scripts/hk_nearby_facilities.py toilet 火炭站
python3 /home/jim/.openclaw/workspace/skills/hk-nearby-facilities/scripts/hk_nearby_facilities.py toilet Central --limit 5
python3 /home/jim/.openclaw/workspace/skills/hk-nearby-facilities/scripts/hk_nearby_facilities.py toilet 旺角 --accessible-only
python3 /home/jim/.openclaw/workspace/skills/hk-nearby-facilities/scripts/hk_nearby_facilities.py toilet --lat 22.448628 --lng 114.164727 --limit 3
```

## Workflow

1. Identify the facility type from the request.
   - For now, only `toilet` is implemented.
2. Extract the place keywords.
   - Accept district names, station names, estates, landmarks, street names, or short area phrases.
3. If the user shared live location or latitude+longitude, prefer using the coordinates to rank facilities by physical distance.
4. Run the script.
5. Prefer the closest or best-matching few entries rather than a huge list.
6. Include Google Maps links when they help the user navigate.
7. If the user asks for accessible / universal toilets, use the relevant flags.
8. If there is no exact place match, say it is a nearby match instead of pretending it is exact.

## Reporting guidance

- Keep it practical: name, address, district, and map link.
- Say when the result is approximate or nearby rather than exact.
- If the query is broad, return the top few likely matches.
- Mention accessible / universal toilet status when available and relevant.

## Data source

Public toilets currently use FEHD official endpoints, including:

- `getMapData.php?type=toilet`
- `getAccessibleToilets.php?type=toilet`
- `getUniversalToilets.php?type=toilet`

## Limitations

- This version is keyword-based, not GPS turn-by-turn routing.
- It currently supports public toilets only.
- Oil stations / petrol stations are not included yet because a comparable official government location dataset has not been confirmed.

## scripts/

- `scripts/hk_nearby_facilities.py` — search nearby Hong Kong facilities by place keyword.
