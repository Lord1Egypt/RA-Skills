---
name: hotel
description: Local-first hotel decision engine for trip stays, hotel comparison, shortlist creation, booking readiness, and accommodation planning. Use whenever the user mentions hotels, where to stay, comparing properties, nights, location tradeoffs, budget, amenities, booking decisions, or choosing the best stay for a trip. Captures hotel options, stores trip context, scores tradeoffs, and surfaces the best-fit hotel based on budget, location, amenities, and decision confidence.
---

# Hotel: Choose the stay with less friction.

## Core Philosophy
1. Turn vague stay planning into concrete hotel decisions.
2. Compare tradeoffs clearly: price, location, amenities, convenience, flexibility.
3. Shortlist before booking.
4. Reduce booking regret by making decision criteria explicit.

## Runtime Requirements
- Python 3 must be available as `python3`
- No external packages required

## Storage
All data is stored locally only under:
- `~/.openclaw/workspace/memory/hotel/trips.json`
- `~/.openclaw/workspace/memory/hotel/hotels.json`
- `~/.openclaw/workspace/memory/hotel/preferences.json`

No external sync. No booking APIs. No credentials required.

## Core Objects
- `trip`: destination, dates, budget, purpose, constraints
- `hotel`: property candidate with price, area, amenities, refund policy, notes
- `preference`: reusable user preferences like breakfast, walkability, quiet rooms, flexible cancellation

## Key Workflows
- **Create Trip**: `add_trip.py --destination "Tokyo" --check_in 2026-04-10 --check_out 2026-04-13 --budget_total 450`
- **Add Hotel**: `add_hotel.py --trip_id TRP-XXXX --name "Hotel A" --nightly_price 120 --area "Shinjuku" --amenities wifi,breakfast`
- **Compare**: `compare_hotels.py --trip_id TRP-XXXX`
- **Shortlist**: `shortlist.py --trip_id TRP-XXXX --top 3`
- **Booking Check**: `book_ready.py --hotel_id HOT-XXXX`
- **Save Preference**: `save_preference.py --key breakfast --value required`

## Scripts
| Script | Purpose |
|---|---|
| `init_storage.py` | Initialize local storage |
| `add_trip.py` | Create a new trip |
| `add_hotel.py` | Add a hotel candidate |
| `compare_hotels.py` | Compare hotel options for a trip |
| `shortlist.py` | Surface best-fit hotels |
| `book_ready.py` | Check if a hotel is ready to book |
| `save_preference.py` | Save reusable hotel preferences |
