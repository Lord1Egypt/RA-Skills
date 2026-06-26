import pytest
import sys
import zipfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from subway import (
    get_time_bucket,
    build_station_lines,
    find_nearby_subway_stations,
    get_headway,
    estimate_subway_travel_time,
)


class TestGetTimeBucket:
    def test_peak_am(self):
        assert get_time_bucket(7) == "peak_am"
        assert get_time_bucket(9) == "peak_am"

    def test_midday(self):
        assert get_time_bucket(10) == "midday"
        assert get_time_bucket(15) == "midday"

    def test_peak_pm(self):
        assert get_time_bucket(16) == "peak_pm"
        assert get_time_bucket(18) == "peak_pm"

    def test_evening(self):
        assert get_time_bucket(19) == "evening"
        assert get_time_bucket(21) == "evening"

    def test_overnight(self):
        assert get_time_bucket(22) == "overnight"
        assert get_time_bucket(23) == "overnight"
        assert get_time_bucket(0) == "overnight"
        assert get_time_bucket(3) == "overnight"
        assert get_time_bucket(6) == "overnight"


class TestBuildStationLines:
    def _make_mock_subway(self):
        """Create a mock GtfsSystem with synthetic subway data."""
        mock = MagicMock()

        mock.load_stops.return_value = {
            # Parent stations (location_type=1)
            "P1": {"stop_name": "Times Sq-42 St", "stop_lat": "40.7559",
                    "stop_lon": "-73.9869", "location_type": "1"},
            "P2": {"stop_name": "34 St-Penn Station", "stop_lat": "40.7505",
                    "stop_lon": "-73.9935", "location_type": "1"},
            # Directional stops
            "P1N": {"stop_name": "Times Sq-42 St", "stop_lat": "40.7559",
                     "stop_lon": "-73.9869", "location_type": "0",
                     "parent_station": "P1"},
            "P1S": {"stop_name": "Times Sq-42 St", "stop_lat": "40.7559",
                     "stop_lon": "-73.9869", "location_type": "0",
                     "parent_station": "P1"},
            "P2N": {"stop_name": "34 St-Penn Station", "stop_lat": "40.7505",
                     "stop_lon": "-73.9935", "location_type": "0",
                     "parent_station": "P2"},
        }

        mock.load_routes.return_value = {
            "R1": {"route_short_name": "1"},
            "R2": {"route_short_name": "A"},
            "R3": {"route_short_name": "N"},
        }

        mock.load_trips.return_value = {
            "T1": {"route_id": "R1"},
            "T2": {"route_id": "R2"},
            "T3": {"route_id": "R3"},
        }

        mock.load_stop_times.return_value = [
            {"stop_id": "P1N", "trip_id": "T1", "departure_time": "08:00:00", "stop_sequence": "1"},
            {"stop_id": "P1S", "trip_id": "T3", "departure_time": "08:05:00", "stop_sequence": "1"},
            {"stop_id": "P2N", "trip_id": "T1", "departure_time": "08:03:00", "stop_sequence": "2"},
            {"stop_id": "P2N", "trip_id": "T2", "departure_time": "08:10:00", "stop_sequence": "1"},
        ]

        mock.ensure_cache.return_value = None
        return mock

    def test_builds_parent_station_map(self):
        mock_subway = self._make_mock_subway()
        result = build_station_lines(subway=mock_subway)
        assert "P1" in result
        assert "P2" in result
        # Directional stops should NOT be in result
        assert "P1N" not in result
        assert "P1S" not in result

    def test_aggregates_lines_to_parents(self):
        mock_subway = self._make_mock_subway()
        result = build_station_lines(subway=mock_subway)
        # P1 should have lines from P1N (1 train) and P1S (N train)
        assert "1" in result["P1"]["lines"]
        assert "N" in result["P1"]["lines"]

    def test_station_has_lat_lon(self):
        mock_subway = self._make_mock_subway()
        result = build_station_lines(subway=mock_subway)
        assert result["P1"]["lat"] == 40.7559
        assert result["P1"]["lon"] == -73.9869

    def test_lines_are_sorted(self):
        mock_subway = self._make_mock_subway()
        result = build_station_lines(subway=mock_subway)
        for station in result.values():
            assert station["lines"] == sorted(station["lines"])


class TestFindNearbySubwayStations:
    STATIONS = {
        "P1": {"name": "Times Sq-42 St", "lat": 40.7559, "lon": -73.9869,
               "lines": ["1", "2", "3", "N", "Q", "R"]},
        "P2": {"name": "34 St-Penn Station", "lat": 40.7505, "lon": -73.9935,
               "lines": ["1", "2", "3"]},
        "P3": {"name": "Coney Island", "lat": 40.5752, "lon": -73.9810,
               "lines": ["D", "F", "N", "Q"]},
    }

    def test_finds_nearby(self):
        # Near Times Square
        results = find_nearby_subway_stations(
            40.7559, -73.9869, radius_miles=1.0, station_lines=self.STATIONS
        )
        names = [r["name"] for r in results]
        assert "Times Sq-42 St" in names
        assert "34 St-Penn Station" in names
        assert "Coney Island" not in names

    def test_sorted_by_distance(self):
        results = find_nearby_subway_stations(
            40.7559, -73.9869, radius_miles=1.0, station_lines=self.STATIONS
        )
        distances = [r["distance_miles"] for r in results]
        assert distances == sorted(distances)

    def test_includes_lines(self):
        results = find_nearby_subway_stations(
            40.7559, -73.9869, radius_miles=0.1, station_lines=self.STATIONS
        )
        assert len(results) >= 1
        assert "lines" in results[0]
        assert isinstance(results[0]["lines"], list)

    def test_empty_when_none_nearby(self):
        results = find_nearby_subway_stations(
            0.0, 0.0, radius_miles=1.0, station_lines=self.STATIONS
        )
        assert results == []

    def test_result_structure(self):
        results = find_nearby_subway_stations(
            40.7559, -73.9869, radius_miles=1.0, station_lines=self.STATIONS
        )
        r = results[0]
        assert "stop_id" in r
        assert "name" in r
        assert "lines" in r
        assert "lat" in r
        assert "lon" in r
        assert "distance_miles" in r


class TestGetHeadway:
    HEADWAYS = {
        "1": {
            "P1": {"peak_am": 3.5, "midday": 6.0, "peak_pm": 4.0, "evening": 8.0},
            "P2": {"peak_am": 3.5, "midday": 6.0},
        },
        "A": {
            "P2": {"peak_am": 5.0, "midday": 8.0},
        },
    }

    def test_returns_headway(self):
        result = get_headway("1", "P1", "peak_am", self.HEADWAYS)
        assert result == 3.5

    def test_returns_none_for_missing_route(self):
        result = get_headway("Z", "P1", "peak_am", self.HEADWAYS)
        assert result is None

    def test_returns_none_for_missing_station(self):
        result = get_headway("1", "P99", "peak_am", self.HEADWAYS)
        assert result is None

    def test_returns_none_for_missing_bucket(self):
        result = get_headway("1", "P1", "overnight", self.HEADWAYS)
        assert result is None

    def test_different_routes_different_headways(self):
        h1 = get_headway("1", "P2", "peak_am", self.HEADWAYS)
        hA = get_headway("A", "P2", "peak_am", self.HEADWAYS)
        assert h1 == 3.5
        assert hA == 5.0
