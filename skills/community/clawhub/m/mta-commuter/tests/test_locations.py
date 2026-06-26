import json
import pytest

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from locations import load_locations, resolve_location, save_location, LOCATIONS_PATH


class TestLoadLocations:
    def test_returns_empty_dict_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr("locations.LOCATIONS_PATH", tmp_path / "nope.json")
        result = load_locations()
        assert result == {}

    def test_returns_empty_dict_when_corrupt(self, tmp_path, monkeypatch):
        loc_file = tmp_path / "locations.json"
        loc_file.write_text("{not valid json")
        monkeypatch.setattr("locations.LOCATIONS_PATH", loc_file)
        assert load_locations() == {}

    def test_loads_existing_file(self, tmp_path, monkeypatch):
        loc_file = tmp_path / "locations.json"
        loc_file.write_text(json.dumps({
            "home": {"address": "123 Main St", "lat": 40.74, "lon": -73.68, "label": "Home"}
        }))
        monkeypatch.setattr("locations.LOCATIONS_PATH", loc_file)
        result = load_locations()
        assert "home" in result
        assert result["home"]["lat"] == 40.74


class TestResolveLocation:
    def test_resolve_named_location(self, tmp_path, monkeypatch):
        loc_file = tmp_path / "locations.json"
        loc_file.write_text(json.dumps({
            "home": {"address": "123 Main St", "lat": 40.74, "lon": -73.68, "label": "Home"}
        }))
        monkeypatch.setattr("locations.LOCATIONS_PATH", loc_file)
        lat, lon, label = resolve_location("home")
        assert lat == 40.74
        assert lon == -73.68
        assert label == "Home"

    def test_resolve_lat_lon_string(self, tmp_path, monkeypatch):
        monkeypatch.setattr("locations.LOCATIONS_PATH", tmp_path / "nope.json")
        lat, lon, label = resolve_location("40.74,-73.68")
        assert lat == 40.74
        assert lon == -73.68
        assert label == "40.74,-73.68"

    def test_resolve_unknown_name_raises(self, tmp_path, monkeypatch):
        monkeypatch.setattr("locations.LOCATIONS_PATH", tmp_path / "nope.json")
        with pytest.raises(ValueError, match="Unknown location"):
            resolve_location("narnia")


class TestSaveLocation:
    def test_save_new_location(self, tmp_path, monkeypatch):
        loc_file = tmp_path / "locations.json"
        monkeypatch.setattr("locations.LOCATIONS_PATH", loc_file)
        save_location("office", address="456 Broadway", lat=40.71, lon=-74.01, label="Office")
        data = json.loads(loc_file.read_text())
        assert data["office"]["address"] == "456 Broadway"
        assert data["office"]["lat"] == 40.71

    def test_save_appends_to_existing(self, tmp_path, monkeypatch):
        loc_file = tmp_path / "locations.json"
        loc_file.write_text(json.dumps({
            "home": {"address": "123 Main", "lat": 40.74, "lon": -73.68, "label": "Home"}
        }))
        monkeypatch.setattr("locations.LOCATIONS_PATH", loc_file)
        save_location("work", address="456 Bway", lat=40.71, lon=-74.01, label="Work")
        data = json.loads(loc_file.read_text())
        assert "home" in data
        assert "work" in data

    def test_save_overwrites_existing_key(self, tmp_path, monkeypatch):
        loc_file = tmp_path / "locations.json"
        loc_file.write_text(json.dumps({
            "home": {"address": "old", "lat": 0, "lon": 0, "label": "Old"}
        }))
        monkeypatch.setattr("locations.LOCATIONS_PATH", loc_file)
        save_location("home", address="new addr", lat=1.0, lon=2.0, label="New Home")
        data = json.loads(loc_file.read_text())
        assert data["home"]["address"] == "new addr"
