"""Tests for GtfsSystem.fetch_alerts parsing.

Constructs a real gtfs_realtime_pb2 FeedMessage so we exercise the full parse
path (HTML stripping, translation fallback, agency matching, dedup).
Skipped if gtfs-realtime-bindings is not installed.
"""
from unittest.mock import patch

import pytest

pytest.importorskip("google.transit.gtfs_realtime_pb2")

from google.transit import gtfs_realtime_pb2
from gtfs import GtfsSystem


def _make_alert(feed, header, desc="", agency_id="MTA LIRR", route_id=""):
    entity = feed.entity.add()
    entity.id = f"alert-{len(feed.entity)}"
    a = entity.alert
    ie = a.informed_entity.add()
    if agency_id:
        ie.agency_id = agency_id
    if route_id:
        ie.route_id = route_id
    t = a.header_text.translation.add()
    t.language = "en"
    t.text = header
    if desc:
        dt = a.description_text.translation.add()
        dt.language = "en"
        dt.text = desc
    return entity


def _encode(feed):
    return feed.SerializeToString()


@pytest.fixture
def system(tmp_path):
    return GtfsSystem(
        key="lirr", name="LIRR", short_name="LIRR",
        gtfs_url="http://x", cache_dir=tmp_path,
        alerts_url="http://alerts.example/feed",
        alerts_agency_id="MTA LIRR",
    )


class _FakeResp:
    def __init__(self, data):
        self._data = data
    def read(self):
        return self._data


class TestFetchAlerts:
    def test_parses_basic_alert(self, system):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        _make_alert(feed, "Signal problems at Jamaica",
                    "Expect 15 min delays on Port Jeff branch")
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        assert len(alerts) == 1
        assert alerts[0]["header"] == "Signal problems at Jamaica"
        assert "15 min delays" in alerts[0]["description"]

    def test_strips_html(self, system):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        _make_alert(feed, "<b>Track work</b> this weekend",
                    "See <a href='x'>schedule</a> for details")
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        assert alerts[0]["header"] == "Track work this weekend"
        assert alerts[0]["description"] == "See schedule for details"

    def test_filters_by_agency(self, system):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        _make_alert(feed, "LIRR issue", agency_id="MTA LIRR")
        _make_alert(feed, "MNR issue", agency_id="MTA MNR")
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        headers = [a["header"] for a in alerts]
        assert "LIRR issue" in headers
        assert "MNR issue" not in headers

    def test_matches_by_route_id_prefix(self, system):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        # No agency_id, but route_id starts with the agency id
        _make_alert(feed, "Route-scoped alert", agency_id="",
                    route_id="MTA LIRR-Port Jefferson")
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        assert len(alerts) == 1
        assert alerts[0]["header"] == "Route-scoped alert"

    def test_dedups_identical_headers(self, system):
        """Same header repeated across entities should collapse to one."""
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        _make_alert(feed, "Elevator out", "East side entrance")
        _make_alert(feed, "Switch failure", "Between A and B")
        _make_alert(feed, "Elevator out", "East side entrance")  # duplicate
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        headers = [a["header"] for a in alerts]
        assert headers.count("Elevator out") == 1
        assert "Switch failure" in headers

    def test_dedups_non_consecutive_duplicates(self, system):
        """Regression for earlier bug: dedup must work even when duplicates
        aren't adjacent in the feed."""
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        _make_alert(feed, "Delay alert", "reason 1")
        _make_alert(feed, "Other alert", "unrelated")
        _make_alert(feed, "Third alert", "also unrelated")
        _make_alert(feed, "Delay alert", "reason 2")  # non-adjacent dup
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        headers = [a["header"] for a in alerts]
        assert headers.count("Delay alert") == 1

    def test_skips_empty_header(self, system):
        feed = gtfs_realtime_pb2.FeedMessage()
        feed.header.gtfs_realtime_version = "2.0"
        _make_alert(feed, "")  # empty header should be skipped
        _make_alert(feed, "Real alert")
        with patch("gtfs.urlopen", return_value=_FakeResp(_encode(feed))):
            alerts = system.fetch_alerts()
        assert len(alerts) == 1
        assert alerts[0]["header"] == "Real alert"

    def test_empty_when_no_url(self, tmp_path):
        system = GtfsSystem(
            key="x", name="X", short_name="X",
            gtfs_url="http://x", cache_dir=tmp_path,
        )
        assert system.fetch_alerts() == []

    def test_handles_network_error(self, system):
        with patch("gtfs.urlopen", side_effect=OSError("connection refused")):
            assert system.fetch_alerts() == []
