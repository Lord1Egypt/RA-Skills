#!/usr/bin/env python3
"""flight_search.py — Reusable Google Flights search script using the fli library.

Usage:
    python3 flight_search.py SFO JFK 2026-06-16 --limit 5
    python3 flight_search.py SFO LGA 2026-06-16 SFO 2026-06-18 --limit 5

Output: JSON array of flight options.

CRITICAL API PATTERN (fli v0.x):
    - SearchFlights() takes NO constructor arguments
    - Call sf.search(filters, top_n=N) on the instance
    - FlightSegment airport format: [[origin, origin]] — 2-element inner list, NOT 3-level
    - SortBy.CHEAPEST exists; SortBy.PRICE does NOT
    - FlightResult uses .legs (not .segments)
"""

import json
import sys


def search_flights(origin_iata: str, dest_iata: str, date: str, limit: int = 5) -> list[dict]:
    from fli.search import SearchFlights
    from fli.models import (
        Airport, FlightSearchFilters, FlightSegment, PassengerInfo,
        MaxStops, SortBy, TripType, SeatType
    )

    origin = getattr(Airport, origin_iata)
    dest = getattr(Airport, dest_iata)

    filters = FlightSearchFilters(
        trip_type=TripType.ONE_WAY,
        passenger_info=PassengerInfo(adults=1),
        flight_segments=[
            FlightSegment(
                departure_airport=[[origin, origin]],
                arrival_airport=[[dest, dest]],
                travel_date=date,
            )
        ],
        stops=MaxStops.ANY,
        sort_by=SortBy.CHEAPEST,
        seat_type=SeatType.ECONOMY,
    )
    sf = SearchFlights()
    results = sf.search(filters, top_n=limit)

    if not results:
        return []

    flights = []
    for fr in results[:limit]:
        leg = fr.legs[0] if fr.legs else None
        flights.append({
            "airline": str(leg.airline).split(".")[-1] if leg and leg.airline else None,
            "flight_number": leg.flight_number if leg else None,
            "price": fr.price,
            "currency": fr.currency,
            "duration_min": fr.duration,
            "stops": fr.stops,
        })
    return flights


def main():
    args = sys.argv[1:]
    if len(args) < 3:
        print("Usage: flight_search.py <origin> <dest> <date> [return_date] [--limit N]", file=sys.stderr)
        sys.exit(1)

    origin_iata = args[0].upper()
    dest_iata = args[1].upper()
    date = args[2]
    return_date = None
    limit = 5

    i = 3
    while i < len(args):
        if args[i] == "--limit" and i + 1 < len(args):
            limit = int(args[i + 1])
            i += 2
        else:
            return_date = args[i]
            i += 1

    outbound = search_flights(origin_iata, dest_iata, date, limit)
    result = {"origin": origin_iata, "destination": dest_iata, "date": date, "flights": outbound}

    if return_date:
        ret = search_flights(dest_iata, origin_iata, return_date, limit)
        result["return_date"] = return_date
        result["return_flights"] = ret

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
