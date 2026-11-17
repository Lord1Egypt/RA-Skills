# Flight Search Reference

## Execution

All flight searches run via `execute_code` or `terminal()` using the Hermes venv Python:
```bash
$HERMES_PY -c "..."
```

**Known limitation (2026-08-23):** `fli` queries Google Flights directly from this
server's IP, and Google **intermittently soft-blocks datacenter IPs** — searches
return an empty 95-byte payload (`None` results). One search may succeed, the next
three fail, with backoff not reliably helping. Treat `None`/0 results as "source
unavailable, retry later or use LetsFG" — not as "no flights exist". LetsFG runs
its engine server-side and is immune to this block; prefer it when fli returns empty.

## fli Library API (v0.x) — Actual Calling Convention

**IMPORTANT**: The fli library API differs from initial assumptions. Use this exact pattern:

```python
from fli.search import SearchFlights
from fli.models import (
    Airport, FlightSearchFilters, FlightSegment, PassengerInfo,
    MaxStops, SortBy, TripType, SeatType
)

def search_route(origin, dest, date, limit=5):
    filters = FlightSearchFilters(
        trip_type=TripType.ONE_WAY,
        passenger_info=PassengerInfo(adults=1),  # REQUIRED
        flight_segments=[
            FlightSegment(
                departure_airport=[[origin, origin]],  # 2-element list per option
                arrival_airport=[[dest, dest]],         # NOT 3-level nested
                travel_date=date,                       # "YYYY-MM-DD" string
            )
        ],
        stops=MaxStops.ANY,
        sort_by=SortBy.CHEAPEST,  # NOT SortBy.PRICE (doesn't exist)
        seat_type=SeatType.ECONOMY,
    )
    sf = SearchFlights()  # No init args
    results = sf.search(filters, top_n=limit)  # Returns list of FlightResult
    
    for fr in results[:limit]:
        leg = fr.legs[0]          # Attribute is .legs, NOT .segments
        print(f"{leg.airline} {leg.flight_number}: ${fr.price}, {fr.stops} stops, {fr.duration}min")
```

**Key API Details:**
- `Airport` is an enum: `Airport.SFO`, `Airport.JFK`, `Airport.LGA`, `Airport.EWR`, `Airport.IAD`, `Airport.DCA`, `Airport.BWI`
- `SearchFlights()` takes NO constructor arguments
- Call `sf.search(filters, top_n=N)` to execute
- `SortBy` enum values: `TOP_FLIGHTS`, `BEST`, `CHEAPEST`, `DEPARTURE_TIME`, `ARRIVAL_TIME`, `DURATION`, `EMISSIONS`
- `FlightResult` attributes: `.legs` (list of FlightLeg), `.price` (float), `.currency`, `.duration` (int minutes), `.stops` (int)
- `FlightLeg` attributes: `.airline`, `.flight_number`, `.departure`, `.arrival`

**Common Pitfalls (learned from usage):**
- `SortBy.PRICE` doesn't exist → use `SortBy.CHEAPEST`
- `SearchFlights(flight_search_filters=...)` doesn't work → construct `SearchFlights()` then call `.search(filters)`
- `FlightSegment(departure_airport=[[[Airport.SFO]]])` (3-level nesting) fails validation → use `[[origin, origin]]` (2-element inner list)
- `fr.segments` doesn't exist → use `fr.legs`

## Capabilities

| Search Type | Description |
|---|---|
| **One-way** | Single origin → destination on a specific date |
| **Round-trip** | Outbound + return with separate date control |
| **Multi-city** | Multiple legs with distinct city pairs (may time out for very complex routes) |
| **Date search** | Find cheapest dates across a range (up to 61 days per chunk) |
| **Multi-airport** | Search across multiple origin/destination airports simultaneously |

## Filters Available

- Stops: any, non-stop, 1 stop or fewer, 2 stops or fewer
- Cabin: economy, premium economy, business, first
- Sort: best, cheapest, departure time, arrival time, duration, emissions
- Max duration (minutes)
- Airline filter
- Bags (checked + carry-on)
- Price limit
- Time restrictions (earliest/latest departure/arrival)
- Emissions filter (less CO2)

## Airport Resolution

Use `search_airports()` to resolve city names, IATA codes, or partial matches. Common cities map to multiple airports (e.g., "new york" → JFK, LGA, EWR). Always confirm ambiguous airports with the user before searching.

## Date Search for Trip Planning

When the user has flexible dates, use `SearchDates` to find the cheapest days to fly across a range. This is especially useful for:
- Suggesting date shifts that save money
- Comparing weekday vs weekend pricing
- Finding optimal departure/return combinations

## Presentation Rules

- Always show: price, currency, stops, total duration, airline, flight numbers, departure/arrival times (local)
- For round-trip: show outbound and return separately with combined price
- For date search: show top 5-10 cheapest dates with prices
- Sort by price (default) unless user specifies otherwise
- Include "as of" timestamp — flight prices change frequently
- Never present flight prices as guaranteed or fixed
- Flag when results are limited (e.g., "showing top 5 of 50+ results")

## Failure Modes

See `references/flights.md` for detailed failure modes and troubleshooting.

Common issues:
- **No results**: Try nearby airports, broaden date range, or relax filters
- **Timeout on multi-city**: Search legs individually and combine
- **Airport not found**: Ask user for IATA code or clarify city name
- **Library not installed**: `pip install flights` in the Hermes venv
