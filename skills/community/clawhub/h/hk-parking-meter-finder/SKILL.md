---
name: hk-parking-meter-finder
description: Find Hong Kong roadside parking meter (咪錶) locations and live vacancy using official Transport Department / DATA.GOV.HK datasets. Use when the user asks in Cantonese, Chinese, or English things like「大埔富善街附近有冇咪錶位？」「火炭站附近有冇路邊錶位」「幫我搵銅鑼灣咪錶空位」「尖沙咀 parking meter vacancy」or any request to locate nearby Hong Kong metered street parking by street, area, district, landmark, or available-space intent.
---

# HK Parking Meter Finder

Use the bundled script to search the official Transport Department metered parking space inventory together with the live occupancy feed.

## Quick start

Run the bundled script from the skill directory:

```bash
python3 scripts/hk_metered_parking.py <street-or-area-keywords>
```

Or use an absolute path rooted at the installed skill folder if needed.

Examples:

```bash
python3 scripts/hk_metered_parking.py 富善街 大埔
python3 scripts/hk_metered_parking.py 廣福坊
python3 scripts/hk_metered_parking.py 火炭站 --vacant-only
python3 scripts/hk_metered_parking.py 銅鑼灣 怡和街 --json
```

## Workflow

1. Extract the place keyword first.
   - Accept street names, districts, sub-districts, estates, landmarks, station names, or short area phrases.
   - Examples: `富善街 大埔`, `火炭站`, `廣福坊`, `Causeway Bay`, `中環 咪錶`.
2. Run the script with the user's place words.
3. Read the top returned clusters.
   - Each cluster groups nearby parking-meter spaces by district / sub-district / street / street-section / vehicle type.
4. Prefer clusters with vacant spaces when the user asks for `空位`, `vacancy`, `available`, or `有冇位`.
   - Use `--vacant-only` if that helps cut noise.
5. Include the Google Maps link when it helps the user navigate quickly.
6. If the exact street is absent from the official metered-space feed, say so and report the nearest likely street clusters instead of pretending there is an exact match.
7. Summarize clearly with vacant vs occupied counts and mention the best-matching street names.

## Reporting guidance

- Keep the answer practical: which nearby street clusters have vacant spaces right now.
- Include the Google Maps link for each recommended cluster when useful.
- If there are several plausible matches, list the top few instead of guessing.
- If the user gave a broad district only, mention that the result is area-level and may need a more specific street.
- Use `--json` only when structured follow-up processing is useful.

## Data sources

The script joins these official datasets:

- `parkingspaces.csv` — static metered-space inventory from Transport Department / DATA.GOV.HK.
- `occupancystatus.csv` — live occupancy status for sensor-equipped / new meter spaces from Transport Department / DATA.GOV.HK.

## Scope and limitations

- This skill covers roadside metered parking spaces only, not car parks, private parking, or non-metered kerbside spaces.
- Live occupancy is only as complete as the official occupancy feed. Some metered spaces may exist in the inventory but not have live occupancy records.
- Matching is keyword-based and fuzzy; it is good for nearby / likely street matches, not turn-by-turn navigation.
- The script reports approximate cluster centres from official coordinates, but it does not geocode arbitrary addresses.
- Queries like `附近` without any place anchor are too vague; provide a street, district, station, or landmark.

## scripts/

- `scripts/hk_metered_parking.py` — search official Hong Kong metered parking spaces and live occupancy by street / area keyword.
