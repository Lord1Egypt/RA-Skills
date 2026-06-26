"""Tests for gtfs.apply_realtime and its midnight-wrap delay guard."""
from datetime import datetime
from zoneinfo import ZoneInfo

from gtfs import apply_realtime


_ET = ZoneInfo("America/New_York")


def _ts(hour, minute, day=10):
    """Build a unix timestamp for 2026-04-{day} at hour:minute ET.

    Anchored in ET so the tests pass regardless of host timezone — which
    is the whole point of apply_realtime converting to ET under the hood.
    """
    return datetime(2026, 4, day, hour, minute, tzinfo=_ET).timestamp()


def _entry():
    return {
        "depart": 0, "depart_str": "", "arrive": 0, "arrive_str": "",
        "duration": 0, "status": "Scheduled", "delay_min": 0,
    }


class TestApplyRealtime:
    def test_on_time(self):
        entry = _entry()
        rt = {"O": {"dep": _ts(17, 22)}, "D": {"arr": _ts(17, 53)}}
        apply_realtime(entry, rt, "O", "D", 17 * 60 + 22)
        assert entry["delay_min"] == 0
        assert entry["status"] == "On time"
        assert entry["depart_str"] == "5:22 PM"
        assert entry["arrive_str"] == "5:53 PM"
        assert entry["duration"] == 31

    def test_running_late(self):
        entry = _entry()
        rt = {"O": {"dep": _ts(17, 30)}}
        apply_realtime(entry, rt, "O", "D", 17 * 60 + 22)
        assert entry["delay_min"] == 8
        assert entry["status"] == "8min late"

    def test_running_early(self):
        entry = _entry()
        rt = {"O": {"dep": _ts(17, 18)}}
        apply_realtime(entry, rt, "O", "D", 17 * 60 + 22)
        assert entry["delay_min"] == -4
        assert entry["status"] == "4min early"

    def test_no_rt_data(self):
        entry = _entry()
        apply_realtime(entry, {}, "O", "D", 17 * 60 + 22)
        assert entry["status"] == "Scheduled"
        assert entry["delay_min"] == 0

    def test_midnight_wrap_late(self):
        """Scheduled 23:55, RT ping at 00:05 next day -> 10 min late, not -1430."""
        entry = _entry()
        rt = {"O": {"dep": _ts(0, 5, day=11)}}
        apply_realtime(entry, rt, "O", "D", 23 * 60 + 55)
        assert entry["delay_min"] == 10
        assert entry["status"] == "10min late"

    def test_midnight_wrap_early(self):
        """Scheduled 00:05, RT ping at 23:55 prev day -> 10 min early."""
        entry = _entry()
        rt = {"O": {"dep": _ts(23, 55, day=10)}}
        apply_realtime(entry, rt, "O", "D", 0 * 60 + 5)
        assert entry["delay_min"] == -10
        assert entry["status"] == "10min early"

    def test_next_day_gtfs_time(self):
        """GTFS dep_min may exceed 24h for next-day service; should still work."""
        entry = _entry()
        # Scheduled for 25:05 (= 1:05 AM next day). RT ping at 1:05 AM = on time.
        rt = {"O": {"dep": _ts(1, 5, day=11)}}
        apply_realtime(entry, rt, "O", "D", 25 * 60 + 5)
        assert entry["delay_min"] == 0

    def test_arrival_crosses_midnight(self):
        """Train departs 23:55, arrives 00:10 next day — duration stays positive."""
        entry = {"depart": 0, "arrive": 0, "duration": 0,
                 "status": "Scheduled", "delay_min": 0,
                 "depart_str": "", "arrive_str": ""}
        rt = {
            "O": {"dep": _ts(23, 55, day=10)},
            "D": {"arr": _ts(0, 10, day=11)},
        }
        apply_realtime(entry, rt, "O", "D", 23 * 60 + 55)
        assert entry["duration"] == 15
        assert entry["arrive_str"] == "12:10 AM"
