from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from src.tz import local_to_utc, utc_to_local


def test_utc_passthrough():
    naive = datetime(2024, 1, 15, 12, 0, 0)
    out = local_to_utc(naive, "UTC")
    assert out == datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)


def test_naive_local_to_utc():
    # NY EST winter: 2024-01-15 09:00 NY == 14:00 UTC (UTC-5)
    naive = datetime(2024, 1, 15, 9, 0, 0)
    out = local_to_utc(naive, "America/New_York")
    expected = datetime(2024, 1, 15, 14, 0, 0, tzinfo=timezone.utc)
    assert out == expected


def test_dst_spring_forward():
    # NY EDT after DST started (Mar 10, 2024): 2024-06-15 09:00 NY == 13:00 UTC (UTC-4)
    naive = datetime(2024, 6, 15, 9, 0, 0)
    out = local_to_utc(naive, "America/New_York")
    expected = datetime(2024, 6, 15, 13, 0, 0, tzinfo=timezone.utc)
    assert out == expected, f"DST not handled: got {out}"


def test_utc_to_local_winter():
    # 2024-01-15 14:00 UTC -> 09:00 NY (EST)
    utc = datetime(2024, 1, 15, 14, 0, 0, tzinfo=timezone.utc)
    out = utc_to_local(utc, "America/New_York")
    # accept either tz-aware (in NY) or naive equal to local wall time
    if out.tzinfo is not None:
        out_naive = out.replace(tzinfo=None)
    else:
        out_naive = out
    assert out_naive == datetime(2024, 1, 15, 9, 0, 0)
