"""
clock.py — injectable Clock (issue #1 PR 1).

MEDS_FAKE_NOW must only take effect under MEDS_TEST=1, so a stray env var
can never shift a real run's clock.
"""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from clock import Clock, FakeClock, get_clock, parse_instant
from tests.conftest import TZ

UTC = timezone.utc


# ── SystemClock: aware UTC now ────────────────────────────────────────────────

def test_system_clock_now_utc_is_aware_and_close():
    before = datetime.now(tz=UTC)
    now = Clock().now_utc()
    after = datetime.now(tz=UTC)
    assert now.tzinfo is not None
    assert before <= now <= after


def test_now_in_converts_to_wall_time():
    now = Clock().now_in(TZ)
    assert now.tzinfo is not None
    assert now.utcoffset() == TZ.utcoffset(now)


# ── FakeClock: frozen, sleep advances ─────────────────────────────────────────

def test_fake_clock_is_frozen():
    start = datetime(2026, 4, 21, 15, 0, tzinfo=UTC)
    c = FakeClock(start)
    assert c.now_utc() == start
    assert c.now_utc() == start  # not moving


def test_fake_clock_sleep_advances():
    start = datetime(2026, 4, 21, 15, 0, tzinfo=UTC)
    c = FakeClock(start)
    c.sleep(90)
    assert c.now_utc() == start + timedelta(seconds=90)


def test_fake_clock_accepts_local_time_converts_to_utc():
    from tests.conftest import local_dt
    c = FakeClock(local_dt(8, 0))                 # 08:00 PDT
    assert c.now_utc() == datetime(2026, 4, 21, 15, 0, tzinfo=UTC)
    assert c.now_in(TZ).hour == 8


# ── get_clock: MEDS_FAKE_NOW gated by MEDS_TEST ───────────────────────────────

def test_get_clock_honors_fake_now_only_under_meds_test(monkeypatch):
    fake = "2026-04-21T08:00:00-07:00"

    monkeypatch.setenv("MEDS_TEST", "1")
    monkeypatch.setenv("MEDS_FAKE_NOW", fake)
    c = get_clock()
    assert isinstance(c, FakeClock)
    assert c.now_utc() == datetime(2026, 4, 21, 15, 0, tzinfo=UTC)

    # Same MEDS_FAKE_NOW but no MEDS_TEST → real clock, never shifted
    monkeypatch.delenv("MEDS_TEST")
    assert not isinstance(get_clock(), FakeClock)

    monkeypatch.setenv("MEDS_TEST", "0")
    assert not isinstance(get_clock(), FakeClock)


def test_get_clock_without_fake_now_is_system(monkeypatch):
    monkeypatch.setenv("MEDS_TEST", "1")
    monkeypatch.delenv("MEDS_FAKE_NOW", raising=False)
    assert not isinstance(get_clock(), FakeClock)


# ── parse_instant ─────────────────────────────────────────────────────────────

def test_parse_instant_tolerates_z_and_naive():
    assert parse_instant("2026-04-21T15:00:00Z") == datetime(2026, 4, 21, 15, 0, tzinfo=UTC)
    assert parse_instant("2026-04-21T15:00:00").tzinfo is UTC
    assert parse_instant("2026-04-21T08:00:00-07:00") == datetime(2026, 4, 21, 15, 0, tzinfo=UTC)
