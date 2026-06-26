"""Tests for multi-leg trip planning (commuter rail + subway connections)."""
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from trip import plan_multi_leg_trip


# --- Synthetic GTFS data for a commuter rail system ---

STOPS = {
    "10": {"stop_id": "10", "stop_name": "Penn Station", "stop_code": "NYK",
           "stop_lat": "40.7505", "stop_lon": "-73.9935"},
    "20": {"stop_id": "20", "stop_name": "New Hyde Park", "stop_code": "NHP",
           "stop_lat": "40.7432", "stop_lon": "-73.6812"},
    "30": {"stop_id": "30", "stop_name": "Mineola", "stop_code": "MIN",
           "stop_lat": "40.7491", "stop_lon": "-73.6406"},
}

ROUTES = {
    "3": {"route_id": "3", "route_long_name": "Port Jefferson Branch"},
}

TRIPS = {
    # Outbound: Penn -> NHP
    "T100": {"trip_id": "T100", "route_id": "3", "service_id": "WKDY",
             "trip_headsign": "Huntington"},
    "T101": {"trip_id": "T101", "route_id": "3", "service_id": "WKDY",
             "trip_headsign": "Huntington"},
    # Inbound: NHP -> Penn
    "T200": {"trip_id": "T200", "route_id": "3", "service_id": "WKDY",
             "trip_headsign": "Penn Station"},
    "T201": {"trip_id": "T201", "route_id": "3", "service_id": "WKDY",
             "trip_headsign": "Penn Station"},
}

STOP_TIMES = [
    # T100: Penn -> NHP (depart 7:10, arrive 7:45)
    {"trip_id": "T100", "stop_id": "10", "departure_time": "07:10:00",
     "arrival_time": "07:10:00", "stop_sequence": "1"},
    {"trip_id": "T100", "stop_id": "20", "departure_time": "07:45:00",
     "arrival_time": "07:45:00", "stop_sequence": "5"},
    # T101: Penn -> NHP (depart 7:30, arrive 8:05)
    {"trip_id": "T101", "stop_id": "10", "departure_time": "07:30:00",
     "arrival_time": "07:30:00", "stop_sequence": "1"},
    {"trip_id": "T101", "stop_id": "20", "departure_time": "08:05:00",
     "arrival_time": "08:05:00", "stop_sequence": "5"},
    # T200: NHP -> Penn (depart 7:15, arrive 7:50)
    {"trip_id": "T200", "stop_id": "20", "departure_time": "07:15:00",
     "arrival_time": "07:15:00", "stop_sequence": "1"},
    {"trip_id": "T200", "stop_id": "10", "departure_time": "07:50:00",
     "arrival_time": "07:50:00", "stop_sequence": "5"},
    # T201: NHP -> Penn (depart 7:35, arrive 8:10)
    {"trip_id": "T201", "stop_id": "20", "departure_time": "07:35:00",
     "arrival_time": "07:35:00", "stop_sequence": "1"},
    {"trip_id": "T201", "stop_id": "10", "departure_time": "08:10:00",
     "arrival_time": "08:10:00", "stop_sequence": "5"},
]

ACTIVE_SERVICES = {"WKDY"}


def _make_mock_system():
    """Create a mock GtfsSystem that returns synthetic data."""
    system = MagicMock()
    system.key = "lirr"
    system.name = "Long Island Rail Road"
    system.short_name = "LIRR"
    system.ensure_cache.return_value = None
    system.load_stops.return_value = STOPS
    system.load_routes.return_value = ROUTES
    system.load_trips.return_value = TRIPS
    system.load_stop_times.return_value = STOP_TIMES
    system.load_active_services.return_value = ACTIVE_SERVICES
    system.fetch_realtime.return_value = None
    return system


# Mock subway data
SUBWAY_STATIONS = {
    "S1": {"name": "34 St-Penn Station", "lat": 40.7505, "lon": -73.9935,
           "lines": ["1", "2", "3", "A", "C", "E"]},
    "S2": {"name": "World Trade Center", "lat": 40.7127, "lon": -74.0134,
           "lines": ["E"]},
    "S3": {"name": "Chambers St", "lat": 40.7133, "lon": -74.0028,
           "lines": ["1", "2", "3"]},
}

HEADWAYS = {
    "E": {"S1": {"peak_am": 5.0}, "S2": {"peak_am": 5.0}},
    "1": {"S1": {"peak_am": 4.0}, "S3": {"peak_am": 4.0}},
}


class TestPlanMultiLegTrip:
    @pytest.fixture(autouse=True)
    def mock_subway(self):
        """Mock subway module functions so we don't need real GTFS data."""
        with patch("subway.find_nearby_subway_stations") as mock_nearby, \
             patch("subway.build_station_lines") as mock_lines, \
             patch("subway.compute_headways") as mock_hw, \
             patch("subway.get_headway") as mock_get_hw, \
             patch("subway.estimate_subway_travel_time") as mock_travel, \
             patch("subway.get_time_bucket") as mock_bucket:

            mock_lines.return_value = SUBWAY_STATIONS
            mock_hw.return_value = HEADWAYS
            mock_get_hw.return_value = 5.0
            mock_travel.return_value = 15
            mock_bucket.return_value = "peak_am"

            def nearby_side_effect(lat, lon, radius_miles=1.0, station_lines=None):
                from geo import haversine_miles
                results = []
                stations = station_lines or SUBWAY_STATIONS
                for sid, info in stations.items():
                    dist = haversine_miles(lat, lon, info["lat"], info["lon"])
                    if dist <= radius_miles:
                        results.append({
                            "stop_id": sid,
                            "name": info["name"],
                            "lines": info["lines"],
                            "lat": info["lat"],
                            "lon": info["lon"],
                            "distance_miles": round(dist, 2),
                        })
                results.sort(key=lambda r: r["distance_miles"])
                return results

            mock_nearby.side_effect = nearby_side_effect

            yield

    def test_returns_empty_with_no_systems(self):
        result = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00", systems={},
        )
        assert result == []

    def test_direct_trip_when_dest_near_station(self):
        """When destination is near a commuter rail station, should return direct trips."""
        system = _make_mock_system()
        # Destination near New Hyde Park station
        results = plan_multi_leg_trip(
            40.7505, -73.9935,  # near Penn
            40.7432, -73.6812,  # near NHP
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        # Should have at least direct options
        assert len(results) > 0
        # Direct trips have commuter_rail + walk legs
        direct = [j for j in results if len(j["legs"]) == 2
                  and j["legs"][0]["type"] == "commuter_rail"
                  and j["legs"][1]["type"] == "walk"]
        assert len(direct) > 0

    def test_multi_leg_trip_to_manhattan(self):
        """Destination in lower Manhattan should include subway legs."""
        system = _make_mock_system()
        # Origin near NHP, destination near WTC
        results = plan_multi_leg_trip(
            40.7432, -73.6812,  # near NHP
            40.7127, -74.0134,  # near WTC
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        assert len(results) > 0
        # At least one result should have a subway leg
        subway_trips = [j for j in results
                        if any(leg["type"] == "subway" for leg in j["legs"])]
        assert len(subway_trips) > 0

    def test_multi_leg_has_correct_leg_types(self):
        """Multi-leg journey should have: commuter_rail, walk, subway, [walk]."""
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        subway_trips = [j for j in results
                        if any(leg["type"] == "subway" for leg in j["legs"])]
        if subway_trips:
            j = subway_trips[0]
            leg_types = [leg["type"] for leg in j["legs"]]
            assert leg_types[0] == "commuter_rail"
            assert "subway" in leg_types

    def test_journey_has_total_duration(self):
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        for j in results:
            assert "total_duration_min" in j
            assert j["total_duration_min"] > 0

    def test_journey_has_depart_info(self):
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        for j in results:
            assert "depart" in j
            assert "depart_str" in j

    def test_sorted_by_departure(self):
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        departures = [j["depart"] for j in results]
        assert departures == sorted(departures)

    def test_subway_leg_has_line_info(self):
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        subway_trips = [j for j in results
                        if any(leg["type"] == "subway" for leg in j["legs"])]
        if subway_trips:
            subway_leg = next(l for l in subway_trips[0]["legs"]
                             if l["type"] == "subway")
            assert "line" in subway_leg
            assert "duration" in subway_leg
            assert "headway" in subway_leg

    def test_commuter_rail_leg_has_schedule_info(self):
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            systems={"lirr": system},
        )
        if results:
            rail_leg = results[0]["legs"][0]
            assert rail_leg["type"] == "commuter_rail"
            assert "from" in rail_leg
            assert "to" in rail_leg
            assert "depart_str" in rail_leg
            assert "arrive_str" in rail_leg
            assert "route" in rail_leg
            assert "system" in rail_leg

    def test_respects_count(self):
        system = _make_mock_system()
        results = plan_multi_leg_trip(
            40.7432, -73.6812, 40.7127, -74.0134,
            "2026-04-10", "07:00",
            count=1,
            systems={"lirr": system},
        )
        assert len(results) <= 1
