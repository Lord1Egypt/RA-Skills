import pytest
import sys
import csv
import io
import zipfile
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from gtfs import parse_gtfs_time, format_time, fuzzy_match_station, GtfsSystem


# --- Utility function tests ---

class TestParseGtfsTime:
    def test_normal_time(self):
        assert parse_gtfs_time("17:22:00") == 17 * 60 + 22

    def test_midnight(self):
        assert parse_gtfs_time("00:00:00") == 0

    def test_next_day_service(self):
        # GTFS uses 25:30 for 1:30 AM next day
        assert parse_gtfs_time("25:30:00") == 25 * 60 + 30

    def test_noon(self):
        assert parse_gtfs_time("12:00:00") == 720

    def test_short_format(self):
        assert parse_gtfs_time("9:05:00") == 9 * 60 + 5


class TestFormatTime:
    def test_morning(self):
        assert format_time(9 * 60 + 30) == "9:30 AM"

    def test_afternoon(self):
        assert format_time(17 * 60 + 22) == "5:22 PM"

    def test_midnight(self):
        assert format_time(0) == "12:00 AM"

    def test_noon(self):
        assert format_time(720) == "12:00 PM"

    def test_next_day_wraps(self):
        # 25*60 = 1500 min = 1:00 AM next day
        assert format_time(25 * 60) == "1:00 AM"

    def test_pm_boundary(self):
        assert format_time(12 * 60 + 1) == "12:01 PM"

    def test_am_boundary(self):
        assert format_time(11 * 60 + 59) == "11:59 AM"


class TestFuzzyMatchStation:
    STOPS = {
        "1": {"stop_name": "Penn Station", "stop_code": "NYK"},
        "2": {"stop_name": "New Hyde Park", "stop_code": "NHP"},
        "3": {"stop_name": "Mineola", "stop_code": "MIN"},
        "4": {"stop_name": "Merillon Avenue", "stop_code": "MAV"},
        "5": {"stop_name": "Atlantic Terminal", "stop_code": "ATL"},
    }

    def test_exact_code_match(self):
        matches = fuzzy_match_station("NYK", self.STOPS)
        assert matches[0][0] == "1"
        assert matches[0][2] == 100  # score

    def test_exact_name_match(self):
        matches = fuzzy_match_station("Penn Station", self.STOPS)
        assert matches[0][0] == "1"

    def test_prefix_match(self):
        matches = fuzzy_match_station("New", self.STOPS)
        names = [m[1] for m in matches]
        assert "New Hyde Park" in names

    def test_substring_match(self):
        matches = fuzzy_match_station("hyde", self.STOPS)
        assert matches[0][1] == "New Hyde Park"

    def test_case_insensitive(self):
        matches = fuzzy_match_station("penn station", self.STOPS)
        assert matches[0][0] == "1"

    def test_no_match(self):
        matches = fuzzy_match_station("xyzzy", self.STOPS)
        assert len(matches) == 0

    def test_word_overlap_match(self):
        matches = fuzzy_match_station("atlantic", self.STOPS)
        assert any(m[1] == "Atlantic Terminal" for m in matches)

    def test_results_sorted_by_score(self):
        matches = fuzzy_match_station("min", self.STOPS)
        scores = [m[2] for m in matches]
        assert scores == sorted(scores, reverse=True)


# --- GtfsSystem tests with synthetic data ---

def _make_test_gtfs_zip(tmp_dir):
    """Create a minimal GTFS zip for testing."""
    zip_path = Path(tmp_dir) / "gtfs_test.zip"

    stops_csv = "stop_id,stop_name,stop_code,stop_lat,stop_lon\n"
    stops_csv += "10,Penn Station,NYK,40.7505,-73.9935\n"
    stops_csv += "20,New Hyde Park,NHP,40.7432,-73.6812\n"

    routes_csv = "route_id,route_short_name,route_long_name\n"
    routes_csv += "3,,Port Jefferson Branch\n"

    trips_csv = "trip_id,route_id,service_id,trip_headsign\n"
    trips_csv += "T100,3,WKDY,Huntington\n"

    stop_times_csv = "trip_id,stop_id,departure_time,arrival_time,stop_sequence\n"
    stop_times_csv += "T100,10,17:22:00,17:22:00,1\n"
    stop_times_csv += "T100,20,17:53:00,17:53:00,5\n"

    calendar_dates_csv = "service_id,date,exception_type\n"
    calendar_dates_csv += "WKDY,20260410,1\n"

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("stops.txt", stops_csv)
        zf.writestr("routes.txt", routes_csv)
        zf.writestr("trips.txt", trips_csv)
        zf.writestr("stop_times.txt", stop_times_csv)
        zf.writestr("calendar_dates.txt", calendar_dates_csv)

    return zip_path


class TestGtfsSystem:
    @pytest.fixture
    def system(self, tmp_path):
        zip_path = _make_test_gtfs_zip(tmp_path)
        sys = GtfsSystem(
            key="test",
            name="Test Railroad",
            short_name="TEST",
            gtfs_url="http://example.com/gtfs.zip",
            cache_dir=tmp_path,
        )
        sys.cache_zip = zip_path
        return sys

    def test_from_config(self, tmp_path):
        config = {
            "name": "Test Railroad",
            "short_name": "TEST",
            "gtfs_url": "http://example.com/gtfs.zip",
            "gtfs_rt_url": "http://example.com/gtfs-rt",
            "alerts_url": "http://example.com/alerts",
            "alerts_agency_id": "TST",
            "cache_dir": ".test_cache",
        }
        sys = GtfsSystem.from_config("test", config, tmp_path)
        assert sys.key == "test"
        assert sys.name == "Test Railroad"
        assert sys.short_name == "TEST"
        assert sys.gtfs_rt_url == "http://example.com/gtfs-rt"
        assert sys.alerts_agency_id == "TST"
        assert sys.cache_dir == tmp_path / ".test_cache"

    def test_load_stops(self, system):
        stops = system.load_stops()
        assert "10" in stops
        assert "20" in stops
        assert stops["10"]["stop_name"] == "Penn Station"
        assert stops["20"]["stop_code"] == "NHP"

    def test_load_routes(self, system):
        routes = system.load_routes()
        assert "3" in routes
        assert routes["3"]["route_long_name"] == "Port Jefferson Branch"

    def test_load_trips(self, system):
        trips = system.load_trips()
        assert "T100" in trips
        assert trips["T100"]["route_id"] == "3"
        assert trips["T100"]["trip_headsign"] == "Huntington"

    def test_load_stop_times(self, system):
        st = system.load_stop_times()
        assert len(st) == 2
        assert st[0]["trip_id"] == "T100"

    def test_load_active_services_calendar_dates(self, system):
        services = system.load_active_services("2026-04-10")
        assert "WKDY" in services

    def test_load_active_services_wrong_date(self, system):
        services = system.load_active_services("2026-01-01")
        assert "WKDY" not in services

    def test_find_trains(self, system):
        trains = system.find_trains("10", "20", "2026-04-10", "17:00", count=5)
        assert len(trains) == 1
        assert trains[0]["origin"] == "Penn Station"
        assert trains[0]["destination"] == "New Hyde Park"
        assert trains[0]["depart"] == 17 * 60 + 22
        assert trains[0]["arrive"] == 17 * 60 + 53
        assert trains[0]["duration"] == 31
        assert trains[0]["system"] == "test"

    def test_find_trains_time_filter(self, system):
        trains = system.find_trains("10", "20", "2026-04-10", "18:00", count=5)
        assert len(trains) == 0

    def test_find_trains_wrong_direction(self, system):
        # dest -> origin should return nothing
        trains = system.find_trains("20", "10", "2026-04-10", "17:00", count=5)
        assert len(trains) == 0

    def test_find_trains_no_active_services(self, system):
        trains = system.find_trains("10", "20", "2026-01-01", "17:00", count=5)
        assert len(trains) == 0

    def test_find_trains_output_format(self, system):
        trains = system.find_trains("10", "20", "2026-04-10", "17:00", count=5)
        t = trains[0]
        assert "trip_id" in t
        assert "route" in t
        assert "headsign" in t
        assert "depart_str" in t
        assert "arrive_str" in t
        assert "status" in t
        assert t["depart_str"] == "5:22 PM"
        assert t["arrive_str"] == "5:53 PM"

    def test_caches_extracted_txt(self, system):
        """After first load, txt files should be cached on disk."""
        system.load_stops()
        assert (system.cache_dir / "stops.txt").exists()
        # Second load should use cached file
        stops2 = system.load_stops()
        assert "10" in stops2

    def test_fetch_realtime_no_url(self, system):
        """Without a RT URL, should return empty dict."""
        rt = system.fetch_realtime()
        assert rt == {}

    def test_fetch_alerts_no_url(self, system):
        """Without alerts URL, should return empty list."""
        alerts = system.fetch_alerts()
        assert alerts == []
