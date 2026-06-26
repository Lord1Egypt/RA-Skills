import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from trip import find_trip_options


# --- Synthetic GTFS data ---

STOPS = {
    "10": {"stop_id": "10", "stop_name": "Penn Station", "stop_code": "NYK",
           "stop_lat": "40.7505", "stop_lon": "-73.9935"},
    "20": {"stop_id": "20", "stop_name": "New Hyde Park", "stop_code": "NHP",
           "stop_lat": "40.7432", "stop_lon": "-73.6812"},
    "21": {"stop_id": "21", "stop_name": "Merillon Avenue", "stop_code": "MAV",
           "stop_lat": "40.7465", "stop_lon": "-73.6598"},
    "22": {"stop_id": "22", "stop_name": "Mineola", "stop_code": "MIN",
           "stop_lat": "40.7491", "stop_lon": "-73.6406"},
    "23": {"stop_id": "23", "stop_name": "Stewart Manor", "stop_code": "SMR",
           "stop_lat": "40.7200", "stop_lon": "-73.6850"},
}

ROUTES = {
    "3": {"route_id": "3", "route_long_name": "Oyster Bay Branch"},
    "2": {"route_id": "2", "route_long_name": "Hempstead Branch"},
}

TRIPS = {
    "T100": {"trip_id": "T100", "route_id": "3", "service_id": "WKDY",
             "trip_headsign": "Oyster Bay"},
    "T101": {"trip_id": "T101", "route_id": "2", "service_id": "WKDY",
             "trip_headsign": "Hempstead"},
    "T102": {"trip_id": "T102", "route_id": "3", "service_id": "WKDY",
             "trip_headsign": "Oyster Bay"},
    "T103": {"trip_id": "T103", "route_id": "2", "service_id": "WKDY",
             "trip_headsign": "Hempstead"},
}

STOP_TIMES = [
    # T100: Penn -> NHP (depart 17:22, arrive 17:57)
    {"trip_id": "T100", "stop_id": "10", "departure_time": "17:22:00",
     "arrival_time": "17:22:00", "stop_sequence": "1"},
    {"trip_id": "T100", "stop_id": "20", "departure_time": "17:57:00",
     "arrival_time": "17:57:00", "stop_sequence": "5"},
    # T101: Penn -> Merillon Ave (depart 17:19, arrive 17:53)
    {"trip_id": "T101", "stop_id": "10", "departure_time": "17:19:00",
     "arrival_time": "17:19:00", "stop_sequence": "1"},
    {"trip_id": "T101", "stop_id": "21", "departure_time": "17:53:00",
     "arrival_time": "17:53:00", "stop_sequence": "4"},
    # T102: Penn -> Mineola (depart 17:24, arrive 17:51)
    {"trip_id": "T102", "stop_id": "10", "departure_time": "17:24:00",
     "arrival_time": "17:24:00", "stop_sequence": "1"},
    {"trip_id": "T102", "stop_id": "22", "departure_time": "17:51:00",
     "arrival_time": "17:51:00", "stop_sequence": "4"},
    # T103: Penn -> Stewart Manor (depart 17:33, arrive 18:02)
    {"trip_id": "T103", "stop_id": "10", "departure_time": "17:33:00",
     "arrival_time": "17:33:00", "stop_sequence": "1"},
    {"trip_id": "T103", "stop_id": "23", "departure_time": "18:02:00",
     "arrival_time": "18:02:00", "stop_sequence": "5"},
]

ACTIVE_SERVICES = {"WKDY"}


class TestFindTripOptions:
    def test_finds_trains_to_nearby_stations(self):
        results = find_trip_options(
            origin_lat=40.7505, origin_lon=-73.9935,
            dest_lat=40.7432, dest_lon=-73.6812,
            date_str="2026-04-08",
            time_str="17:00",
            radius_miles=3.0,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        dest_names = [r["destination"] for r in results]
        assert "New Hyde Park" in dest_names
        assert "Merillon Avenue" in dest_names

    def test_results_include_distance(self):
        results = find_trip_options(
            origin_lat=40.7505, origin_lon=-73.9935,
            dest_lat=40.7432, dest_lon=-73.6812,
            date_str="2026-04-08",
            time_str="17:00",
            radius_miles=3.0,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        for r in results:
            assert "dest_distance_miles" in r
            assert isinstance(r["dest_distance_miles"], float)
            assert "origin_distance_miles" in r

    def test_sorted_by_arrival(self):
        results = find_trip_options(
            origin_lat=40.7505, origin_lon=-73.9935,
            dest_lat=40.7432, dest_lon=-73.6812,
            date_str="2026-04-08",
            time_str="17:00",
            radius_miles=3.0,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        arrivals = [r["arrive"] for r in results]
        assert arrivals == sorted(arrivals)

    def test_filters_by_time(self):
        results = find_trip_options(
            origin_lat=40.7505, origin_lon=-73.9935,
            dest_lat=40.7432, dest_lon=-73.6812,
            date_str="2026-04-08",
            time_str="17:25",
            radius_miles=3.0,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        for r in results:
            assert r["depart"] >= 17 * 60 + 25

    def test_respects_radius(self):
        results = find_trip_options(
            origin_lat=40.7505, origin_lon=-73.9935,
            dest_lat=40.7432, dest_lon=-73.6812,
            date_str="2026-04-08",
            time_str="17:00",
            radius_miles=0.5,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        dest_names = [r["destination"] for r in results]
        assert "New Hyde Park" in dest_names
        assert "Mineola" not in dest_names

    def test_empty_when_no_matches(self):
        results = find_trip_options(
            origin_lat=0.0, origin_lon=0.0,
            dest_lat=0.0, dest_lon=0.0,
            date_str="2026-04-08",
            time_str="17:00",
            radius_miles=1.0,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        assert results == []


from trip import find_alternatives


class TestFindAlternatives:
    def test_finds_alternatives_by_train_details(self):
        results = find_alternatives(
            origin_name="Penn Station", dest_name="New Hyde Park",
            depart_time="17:22", date_str="2026-04-08",
            radius_miles=3.0, window_minutes=30,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        dest_names = [r["destination"] for r in results]
        assert "New Hyde Park" in dest_names
        assert len(results) > 1

    def test_reference_train_marked(self):
        results = find_alternatives(
            origin_name="Penn Station", dest_name="New Hyde Park",
            depart_time="17:22", date_str="2026-04-08",
            radius_miles=3.0, window_minutes=30,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        ref_trains = [r for r in results if r.get("is_reference")]
        assert len(ref_trains) == 1
        assert ref_trains[0]["destination"] == "New Hyde Park"
        assert ref_trains[0]["depart"] == 17 * 60 + 22

    def test_window_filter(self):
        results = find_alternatives(
            origin_name="Penn Station", dest_name="New Hyde Park",
            depart_time="17:22", date_str="2026-04-08",
            radius_miles=3.0, window_minutes=5,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        ref_dep = 17 * 60 + 22
        for r in results:
            assert r["depart"] >= ref_dep - 5
            assert r["depart"] <= ref_dep + 5

    def test_sorted_by_arrival(self):
        results = find_alternatives(
            origin_name="Penn Station", dest_name="New Hyde Park",
            depart_time="17:22", date_str="2026-04-08",
            radius_miles=3.0, window_minutes=30,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        arrivals = [r["arrive"] for r in results]
        assert arrivals == sorted(arrivals)

    def test_includes_distance_from_target(self):
        results = find_alternatives(
            origin_name="Penn Station", dest_name="New Hyde Park",
            depart_time="17:22", date_str="2026-04-08",
            radius_miles=3.0, window_minutes=30,
            stops=STOPS, routes=ROUTES, trips=TRIPS,
            stop_times=STOP_TIMES, active_services=ACTIVE_SERVICES,
        )
        for r in results:
            assert "dest_distance_miles" in r
