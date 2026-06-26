import subprocess
import sys
from pathlib import Path
import pytest

MTA_PATH = str(Path(__file__).resolve().parent.parent / "scripts" / "mta.py")


def _run(args, timeout=30):
    return subprocess.run(
        [sys.executable, MTA_PATH] + args,
        capture_output=True, text=True, timeout=timeout,
    )


class TestMtaHelp:
    def test_no_args_shows_usage(self):
        result = _run([])
        assert result.returncode == 0
        assert "lirr" in result.stdout.lower()
        assert "mnr" in result.stdout.lower()
        assert "trip" in result.stdout.lower()
        assert "alerts" in result.stdout.lower()

    def test_unknown_command(self):
        result = _run(["bogus"])
        assert result.returncode != 0


class TestMtaLirr:
    def test_lirr_help(self):
        result = _run(["lirr", "--help"])
        assert result.returncode == 0
        assert "origin" in result.stdout.lower()

    def test_lirr_stations(self):
        result = _run(["lirr", "--stations"])
        assert result.returncode == 0
        assert "Penn Station" in result.stdout or "NYK" in result.stdout

    def test_lirr_routes(self):
        result = _run(["lirr", "--routes"])
        assert result.returncode == 0
        # Should list at least one branch
        assert "Branch" in result.stdout or "branch" in result.stdout

    def test_lirr_find_station(self):
        result = _run(["lirr", "--find-station", "hyde"])
        assert result.returncode == 0
        assert "New Hyde Park" in result.stdout

    def test_lirr_schedule_lookup(self):
        result = _run(["lirr", "Penn Station", "New Hyde Park",
                        "--time", "17:00", "--no-live"])
        assert result.returncode == 0
        assert "Penn Station" in result.stdout
        assert "New Hyde Park" in result.stdout

    def test_lirr_schedule_json(self):
        result = _run(["lirr", "Penn Station", "New Hyde Park",
                        "--time", "17:00", "--no-live", "--json", "--count", "1"])
        assert result.returncode == 0
        import json
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) == 1
        assert "depart_str" in data[0]

    def test_lirr_no_origin_shows_help(self):
        result = _run(["lirr"])
        assert result.returncode == 0
        # Should show help text
        assert "usage" in result.stdout.lower() or "origin" in result.stdout.lower()


class TestMtaMnr:
    def test_mnr_stations(self):
        result = _run(["mnr", "--stations"])
        assert result.returncode == 0
        assert "Grand Central" in result.stdout or "GCT" in result.stdout

    def test_mnr_routes(self):
        result = _run(["mnr", "--routes"])
        assert result.returncode == 0

    def test_mnr_schedule_lookup(self):
        result = _run(["mnr", "Grand Central", "White Plains",
                        "--time", "17:00", "--no-live"])
        assert result.returncode == 0
        assert "Grand Central" in result.stdout

    def test_mnr_find_station(self):
        result = _run(["mnr", "--find-station", "white"])
        assert result.returncode == 0
        assert "White Plains" in result.stdout or "white" in result.stdout.lower()


class TestMtaTrip:
    def test_trip_help(self):
        result = _run(["trip", "--help"])
        assert result.returncode == 0
        assert "near-origin" in result.stdout

    def test_trip_requires_args(self):
        result = _run(["trip"])
        assert result.returncode != 0


class TestMtaStations:
    def test_stations_nearby_help(self):
        result = _run(["stations", "nearby", "--help"])
        assert result.returncode == 0
        assert "near" in result.stdout.lower()

    def test_stations_bare_shows_usage(self):
        result = _run(["stations"])
        assert result.returncode == 0
        assert "nearby" in result.stdout.lower()


class TestMtaAlerts:
    def test_alerts_help(self):
        result = _run(["alerts", "--help"])
        assert result.returncode == 0
        assert "system" in result.stdout.lower()


class TestMtaConfigErrors:
    def _run_with_feeds(self, args, feeds_path):
        stub = (
            "import sys; "
            "import mta; "
            f"mta.FEEDS_PATH = __import__('pathlib').Path({str(feeds_path)!r}); "
            f"sys.argv = ['mta.py'] + {list(args)!r}; "
            "mta.main()"
        )
        return subprocess.run(
            [sys.executable, "-c", stub],
            cwd=str(Path(MTA_PATH).parent),
            capture_output=True, text=True, timeout=10,
        )

    def test_missing_feeds_json_fails_cleanly(self, tmp_path):
        result = self._run_with_feeds(["alerts"], tmp_path / "missing.json")
        assert result.returncode == 1
        assert "missing" in result.stderr.lower()

    def test_invalid_feeds_json_fails_cleanly(self, tmp_path):
        bad = tmp_path / "feeds.json"
        bad.write_text("{not valid json")
        result = self._run_with_feeds(["alerts"], bad)
        assert result.returncode == 1
        assert "not valid json" in result.stderr.lower()
