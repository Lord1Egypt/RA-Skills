"""
Quiet-hours tests (issue #1 §3.4).

The tick-side quiet rules — reminder exempt, nudge muted except the
first 30 min of quiet hours, missed always logged with the message
muted, overnight summary after quiet end — live in tests/test_tick.py
(AC 26-28). This file keeps the in_quiet_window edit-time check that
doctor (PR 3) and add/edit (PR 4) share; the build_tasks warning tests
are gone with build_tasks itself — doctor FAILs on quiet-hours doses
now (tests/test_doctor.py).
"""
from tests.conftest import load_setup_tasks

setup_tasks = load_setup_tasks()


def test_in_quiet_window_matches():
    q = {"start": "22:00", "end": "07:00"}
    assert setup_tasks.in_quiet_window("23:00", q) is True
    assert setup_tasks.in_quiet_window("03:00", q) is True
    assert setup_tasks.in_quiet_window("22:00", q) is True    # start is quiet
    assert setup_tasks.in_quiet_window("07:00", q) is False   # end is not
    assert setup_tasks.in_quiet_window("12:00", q) is False


def test_in_quiet_window_same_day_window():
    q = {"start": "13:00", "end": "15:00"}
    assert setup_tasks.in_quiet_window("14:00", q) is True
    assert setup_tasks.in_quiet_window("12:59", q) is False
