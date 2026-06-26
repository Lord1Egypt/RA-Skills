import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from geo import haversine_miles


class TestHaversine:
    def test_same_point_is_zero(self):
        assert haversine_miles(40.74, -73.68, 40.74, -73.68) == 0.0

    def test_known_distance_nhp_to_mineola(self):
        # New Hyde Park (40.7432, -73.6812) to Mineola (40.7491, -73.6406)
        # Roughly 2.1 miles
        dist = haversine_miles(40.7432, -73.6812, 40.7491, -73.6406)
        assert 1.8 < dist < 2.5

    def test_known_distance_nhp_to_merillon(self):
        # New Hyde Park (40.7432, -73.6812) to Merillon Ave (40.7465, -73.6598)
        # Roughly 1.2 miles
        dist = haversine_miles(40.7432, -73.6812, 40.7465, -73.6598)
        assert 0.5 < dist < 1.5

    def test_symmetrical(self):
        d1 = haversine_miles(40.74, -73.68, 40.75, -73.64)
        d2 = haversine_miles(40.75, -73.64, 40.74, -73.68)
        assert d1 == pytest.approx(d2)

    def test_returns_float(self):
        result = haversine_miles(40.74, -73.68, 40.75, -73.64)
        assert isinstance(result, float)


from geo import find_nearby_stations


def _make_stops():
    """Synthetic stops dict mimicking load_stops() output."""
    return {
        "1": {"stop_id": "1", "stop_name": "New Hyde Park", "stop_code": "NHP",
              "stop_lat": "40.7432", "stop_lon": "-73.6812"},
        "2": {"stop_id": "2", "stop_name": "Merillon Avenue", "stop_code": "MAV",
              "stop_lat": "40.7465", "stop_lon": "-73.6598"},
        "3": {"stop_id": "3", "stop_name": "Mineola", "stop_code": "MIN",
              "stop_lat": "40.7491", "stop_lon": "-73.6406"},
        "4": {"stop_id": "4", "stop_name": "Stewart Manor", "stop_code": "SMR",
              "stop_lat": "40.7200", "stop_lon": "-73.6850"},
        "5": {"stop_id": "5", "stop_name": "Montauk", "stop_code": "MTK",
              "stop_lat": "41.0478", "stop_lon": "-71.9542"},
    }


class TestFindNearbyStations:
    def test_finds_stations_within_radius(self):
        stops = _make_stops()
        results = find_nearby_stations(40.7432, -73.6812, stops, radius_miles=2.0)
        names = [r["stop_name"] for r in results]
        assert "New Hyde Park" in names
        assert "Merillon Avenue" in names
        assert "Montauk" not in names

    def test_sorted_by_distance(self):
        stops = _make_stops()
        results = find_nearby_stations(40.7432, -73.6812, stops, radius_miles=5.0)
        distances = [r["distance_miles"] for r in results]
        assert distances == sorted(distances)

    def test_empty_when_no_stations_in_radius(self):
        stops = _make_stops()
        results = find_nearby_stations(0.0, 0.0, stops, radius_miles=1.0)
        assert results == []

    def test_result_structure(self):
        stops = _make_stops()
        results = find_nearby_stations(40.7432, -73.6812, stops, radius_miles=2.0)
        first = results[0]
        assert "stop_id" in first
        assert "stop_name" in first
        assert "distance_miles" in first
        assert isinstance(first["distance_miles"], float)

    def test_default_radius_is_3(self):
        stops = _make_stops()
        results = find_nearby_stations(40.7432, -73.6812, stops)
        names = [r["stop_name"] for r in results]
        assert len(names) >= 3
        assert "Montauk" not in names
