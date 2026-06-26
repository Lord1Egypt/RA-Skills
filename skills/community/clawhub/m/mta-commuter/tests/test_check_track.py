"""Tests for check_track helpers (no network)."""
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

from check_track import find_train

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_track.py"


SAMPLE_ARRIVALS = {
    "arrivals": [
        {"train_num": "1582", "track": "17",
         "status": {"canceled": False, "otp": 120}},
        {"train_num": "1584", "track": None,
         "status": {"canceled": False, "otp": 0}},
        {"train_num": 1586, "track": "", "status": {"canceled": True, "otp": 0}},
    ]
}


class TestFindTrain:
    def test_matches_string(self):
        t = find_train(SAMPLE_ARRIVALS, "1582")
        assert t is not None
        assert t["track"] == "17"

    def test_matches_int(self):
        t = find_train(SAMPLE_ARRIVALS, 1586)
        assert t is not None
        assert t["status"]["canceled"] is True

    def test_no_match(self):
        assert find_train(SAMPLE_ARRIVALS, "9999") is None

    def test_empty_arrivals(self):
        assert find_train({"arrivals": []}, "1582") is None

    def test_missing_arrivals_key(self):
        assert find_train({}, "1582") is None


def _run(args, mock_data=None):
    """Run check_track.py as a subprocess with optional stubbed fetch_arrivals."""
    if mock_data is not None:
        # Inject a monkeypatched fetch_arrivals via subprocess stub.
        # Use repr() so Python literals (True/False/None) survive the eval.
        stub = (
            "import sys; "
            "import check_track; "
            f"_DATA = {mock_data!r}; "
            "check_track.fetch_arrivals = lambda s, sys='lirr': _DATA; "
            "check_track.main()"
        )
        return subprocess.run(
            [sys.executable, "-c", stub] + args,
            cwd=str(SCRIPT.parent),
            capture_output=True, text=True, timeout=10,
        )
    return subprocess.run(
        [sys.executable, str(SCRIPT)] + args,
        capture_output=True, text=True, timeout=10,
    )


class TestCheckTrackCli:
    def test_track_assigned_exits_zero(self):
        # Run with mock data providing track 17
        result = _run(
            ["--train", "1582", "--station", "NYK"],
            mock_data=SAMPLE_ARRIVALS,
        )
        assert result.returncode == 0
        assert "Track 17" in result.stdout
        assert "1582" in result.stdout

    def test_no_track_exits_one(self):
        """Train exists but no track yet -> exit 1 so cron keeps polling."""
        result = _run(
            ["--train", "1584", "--station", "NYK"],
            mock_data=SAMPLE_ARRIVALS,
        )
        assert result.returncode == 1
        assert result.stdout == ""

    def test_train_not_found_exits_one(self):
        result = _run(
            ["--train", "9999", "--station", "NYK"],
            mock_data=SAMPLE_ARRIVALS,
        )
        assert result.returncode == 1

    def test_canceled_train(self):
        result = _run(
            ["--train", "1586", "--station", "NYK"],
            mock_data=SAMPLE_ARRIVALS,
        )
        # track is empty string, so exits 1 (no track assigned yet)
        assert result.returncode == 1

    def test_json_output(self):
        import json
        result = _run(
            ["--train", "1582", "--station", "NYK", "--json"],
            mock_data=SAMPLE_ARRIVALS,
        )
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["track"] == "17"
        assert data["train"] == "1582"
        assert data["system"] == "lirr"

    def test_requires_train_arg(self):
        result = _run(["--station", "NYK"])
        assert result.returncode != 0

    def test_system_mnr_accepted(self):
        result = _run(
            ["--train", "1582", "--station", "GCT", "--system", "mnr"],
            mock_data=SAMPLE_ARRIVALS,
        )
        assert result.returncode == 0
        assert "Grand Central" in result.stdout

    def test_system_bogus_rejected(self):
        result = _run(["--train", "1582", "--system", "bogus"])
        assert result.returncode != 0
