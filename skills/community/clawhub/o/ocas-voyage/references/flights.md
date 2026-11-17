# Google Flights Search (fli)

Voyage uses the `fli` Python library (installed as `flights` from PyPI) to search Google Flights data for trip planning. This covers flight search, date-based price discovery, and airport resolution.

## Installation

The `flights` package must be installed in the Hermes agent venv:

```bash
$HERMES_PY -m pip install flights
```

**Important:** The system Python (3.13) and the Hermes venv (3.11) are different. Always install into the venv. The package name on PyPI is `flights`; the import name is `fli`.

## Airport Resolution

Use `search_airports()` to resolve city names, IATA codes, or partial matches:

```python
from fli.core.airports import search_airports

# City name → multiple airports
results = search_airports("new york", limit=5)
# → JFK, LGA, EWR (score=90, city match)

# Exact IATA code
results = search_airports("LHR", limit=3)
# → LHR (score=100, iata_exact)

# Partial city name
results = search_airports("san fran", limit=5)
# → SFO, OAK, SJC (score=80, city prefix)
```

Priority cascade: `iata_exact` (100) > `city` (90) > `city prefix` (80) > `name` (≤70) > `iata_prefix` (60).

Common multi-airport cities:
- New York: JFK, LGA, EWR
- Chicago: ORD, MDW
- London: LHR, LGW, STN, LTN, LCY
- Tokyo: NRT, HND
- San Francisco: SFO, OAK, SJC
- Los Angeles: LAX, BUR, SNA, ONT, LGB

## Flight Search

### One-Way

```python
from fli.search.flights import SearchFlights
from fli.models import FlightSearchFilters, PassengerInfo
from fli.core.builders import build_flight_segments
from fli.models import Airport

segments, trip_type = build_flight_segments(
    Airport.JFK, Airport.LAX, "2026-06-15"
)
filters = FlightSearchFilters(
    trip_type=trip_type,
    passenger_info=PassengerInfo(adults=1),
    flight_segments=segments,
)
sf = SearchFlights()
results = sf.search(filters, top_n=5)
```

### Round-Trip

```python
segments, trip_type = build_flight_segments(
    Airport.JFK, Airport.LAX, "2026-06-15", return_date="2026-06-22"
)
filters = FlightSearchFilters(
    trip_type=trip_type,
    passenger_info=PassengerInfo(adults=1),
    flight_segments=segments,
)
```

### With Filters

```python
from fli.models import MaxStops, SeatType, SortBy, TripType

filters = FlightSearchFilters(
    trip_type=TripType.ONE_WAY,
    passenger_info=PassengerInfo(adults=2, children=1),
    flight_segments=segments,
    stops=MaxStops.NON_STOP,          # ANY, NON_STOP, ONE_STOP_OR_FEWER, TWO_OR_FEWER_STOPS
    seat_type=SeatType.ECONOMY,       # ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST
    sort_by=SortBy.CHEAPEST,          # TOP_FLIGHTS, BEST, CHEAPEST, DEPARTURE_TIME, etc.
    max_duration=600,                  # in minutes
)
```

### Results Structure

Each `FlightResult` has:
- `price`: float (e.g., 154.0)
- `currency`: str (e.g., "USD")
- `duration`: int (total minutes)
- `stops`: int
- `legs`: list of `FlightLeg` with airline, flight_number, departure_airport, arrival_airport, departure_datetime, arrival_datetime, duration

For round-trip searches, results are tuples of `FlightResult` (outbound, return).

## Date Search (Cheapest Dates)

Use `SearchDates` to find the cheapest dates across a range:

```python
from fli.search.dates import SearchDates
from fli.models import DateSearchFilters, PassengerInfo
from fli.core.builders import build_date_search_segments
from fli.models import Airport

segments, trip_type = build_date_search_segments(
    Airport.JFK, Airport.LAX, "2026-06-01",
    is_round_trip=False,
)
filters = DateSearchFilters(
    trip_type=trip_type,
    passenger_info=PassengerInfo(adults=1),
    flight_segments=segments,
    from_date="2026-06-01",
    to_date="2026-06-30",
)
sd = SearchDates()
results = sd.search(filters)
# → list of DatePrice(date=(datetime,), price=154.0, currency="USD")
```

For round-trip date search, pass `is_round_trip=True` and `trip_duration` (days).

**Limitations:**
- Max 61 days per search chunk (library auto-splits)
- Cannot search more than ~305 days in the future
- Round-trip date search requires `duration` parameter

## Multi-Airport Search

Pass lists of airports to `build_flight_segments`:

```python
from fli.models import Airport

segments, trip_type = build_flight_segments(
    [Airport.JFK, Airport.EWR],      # depart from either NYC airport
    [Airport.LAX, Airport.SNA],       # arrive at either LA airport
    "2026-06-15",
)
```

## Multi-City Search

```python
from fli.core.builders import build_multi_city_segments
from fli.models import Airport

segments, trip_type = build_multi_city_segments([
    (Airport.JFK, Airport.LAX, "2026-06-15"),
    (Airport.LAX, Airport.SFO, "2026-06-18"),
    (Airport.SFO, Airport.JFK, "2026-06-22"),
])
```

**Note:** Multi-city with distinct city pairs may time out. Round-trip-style multi-city (same origin/destination) works reliably.

## Execution Pattern

All flight searches run via `execute_code` with the Hermes venv Python:

```python
import sys
sys.path.insert(0, "$HERMES_INSTALL/venv/lib/python3.11/site-packages")
# ... then use fli imports
```

Or use the venv Python directly via `terminal()`:
```bash
$HERMES_PY -c "..."
```

## Failure Modes

| Mode | Symptom | Resolution |
|------|---------|------------|
| No results | `search()` returns `None` | Try nearby airports, broaden date range, or relax filters |
| Timeout | Multi-city with distinct pairs | Fall back to searching legs individually |
| Rate limit | HTTP 429 | Library auto-retries with backoff; wait and retry |
| Airport not found | `search_airports()` returns empty | Ask user for IATA code or city name clarification |
| Past date | `ValueError: Travel date cannot be in the past` | Use today or future dates only |
| pydantic_core error | `ModuleNotFoundError: pydantic_core._pydantic_core` | Reinstall in correct venv: `$HERMES_PY -m pip install flights` |
| Direct API: `SortBy.PRICE` AttributeError | `SortBy` has no `PRICE` member | Use `SortBy.CHEAPEST` instead |
| Direct API: `SearchFlights(__init__)` TypeError | `got unexpected keyword argument 'flight_search_filters'` | `SearchFlights()` takes no args; call `sf.search(filters, top_n=N)` on instance |
| Direct API: `list index out of range` in format | Airport nesting wrong in `FlightSegment` | Use `departure_airport=[[origin, origin]]` (2-element inner list), NOT `[[[origin]]]` (3-level) |
| Direct API: `'FlightResult' has no attribute 'segments'` | Wrong attribute name | Use `fr.legs` not `fr.segments` |
| 4 validation errors for `FlightSegment` | Airport passed as nested list instead of Airport enum | Ensure `Airport.SFO` enum value is used, not string "SFO"; pydantic validates `[[origin, origin]]` as list Airport |

## Integration with Voyage Workflow

1. **Trip planning**: When user provides origin/destination/dates, search flights in parallel with lodging
2. **Date optimization**: Use `SearchDates` to suggest cheaper date alternatives before locking itinerary
3. **Multi-city routing**: Search each leg individually, combine into full itinerary
4. **Budget awareness**: Surface flight costs alongside lodging in total trip cost estimate
5. **Airport context**: Use resolved airport names for activity/restaurant recommendations near arrival airport

## Presentation Rules

- Always show: price, stops, duration, airline, flight numbers, departure/arrival times
- For round-trip: show outbound and return separately with combined price
- Sort by: price (default) or user preference (fewest stops, shortest duration, specific times)
- Flag basic economy restrictions when `exclude_basic_economy=False` (default)
- Never present flight prices as guaranteed — prices change frequently
- Include "as of" timestamp with all flight data
