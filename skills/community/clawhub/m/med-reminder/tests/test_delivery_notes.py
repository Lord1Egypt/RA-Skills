"""
#21: a message that keeps failing while other sends get through is reported
on its own ("Delivery problem: the 7:30am digest couldn't be sent …"), once.
Nothing is ever prefixed to an unrelated message, and a channel outage
(every send failing) produces no note until sends work again.

Sends take one (fake) second here, so a failure is recorded after its
intent and the retry backoff behaves as it does live.
"""
from datetime import timedelta

import pytest

import dispatch
import tick
from clock import FakeClock
from reply import handle_confirm
from tests.conftest import local_dt, make_med, make_tick_env


@pytest.fixture
def env(tmp_path, monkeypatch):
    e = make_tick_env(tmp_path, monkeypatch)
    real_send = dispatch.send_once

    def run(now, tick_minutes=5, dry_run=False):
        clock = FakeClock(now)

        def timed_send(text, timeout=None):
            try:
                return real_send(text, timeout=timeout)
            finally:
                clock.sleep(1)

        monkeypatch.setattr(dispatch, "send_once", timed_send)
        try:
            return tick.run_tick(dry_run=dry_run, clock=clock, tick_minutes=tick_minutes)
        finally:
            monkeypatch.setattr(dispatch, "send_once", real_send)

    e.run = run
    return e


def tick_every_5(env, start, end):
    t = start
    while t <= end:
        env.run(t)
        t += timedelta(minutes=5)


def notes(env):
    return [m for m in env.sent() if m.startswith("Delivery problem")]


def test_failing_digest_is_reported_once_and_nothing_is_wrapped(env):
    # dogfood 2026-10-22: the digest failed all morning while nudges went out
    env.write(meds=[make_med(times=["08:00"])], digest_time="07:30")
    env.fail_sends_containing("Meds for")
    tick_every_5(env, local_dt(7, 25), local_dt(9, 0))
    assert len(notes(env)) == 1
    note = notes(env)[0]
    assert "the 7:30am digest couldn't be sent" in note
    assert "(3 attempts, last " in note
    assert "Other messages are going through" in note
    assert not any("Delivery was down" in m for m in env.sent())
    assert "Reminder: Metformin 500mg" in env.sent()
    assert env.sent_count("Late: Metformin") >= 1
    assert all(m.startswith(("Reminder", "Late", "Delivery problem")) for m in env.sent())


def test_no_note_when_it_gets_through_on_a_retry(env):
    env.write(meds=[make_med(times=["08:00"])], digest_time="07:30")
    env.fail_sends_containing("Meds for")
    tick_every_5(env, local_dt(7, 25), local_dt(7, 35))   # 2 failed attempts
    env.heal_sends()
    tick_every_5(env, local_dt(7, 40), local_dt(8, 30))   # digest delivered
    assert env.sent_count("Meds for") == 1
    assert notes(env) == []


def test_full_outage_then_recovery_sends_plain_messages(env):
    env.write(meds=[make_med(times=["08:00"])])
    env.run(local_dt(7, 55))
    env.fail_sends()
    for hm in ((8, 5), (8, 11), (8, 22), (8, 43)):
        env.run(local_dt(*hm))
    marker = env.state_file.parent / "SENDER_DOWN"
    assert marker.exists()                       # doctor still sees the outage
    assert notes(env) == []                      # nothing gets through anyway
    env.heal_sends()
    env.run(local_dt(9, 25))
    env.run(local_dt(9, 30))
    assert env.sent()[0].startswith("Late: Metformin")    # no prefix
    # the failed reminder was superseded by a delivered nudge: not reported
    assert notes(env) == []
    assert not marker.exists()


def test_no_note_while_everything_is_failing(env):
    env.write(meds=[make_med(times=["08:00"])], digest_time="07:30")
    env.run(local_dt(7, 25))
    env.fail_sends()
    tick_every_5(env, local_dt(7, 30), local_dt(9, 0))
    assert env.sent() == []
    assert env.events("send_intent", ) and not [
        e for e in env.events("send_intent") if e["stage"] == "delivery"]


def two_meds():
    # different minutes: same-minute meds share one message (#26), and these
    # tests need Metformin's sends to fail while Lisinopril's get through
    return [make_med(med_id="med-001", name="Metformin", times=["08:00"]),
            make_med(med_id="med-002", name="Lisinopril", times=["08:01"])]


def test_failing_reminder_is_reported(env):
    # everything about Metformin fails; Lisinopril's sends prove the channel
    env.write(meds=two_meds())
    env.fail_sends_containing("Metformin 500mg")
    tick_every_5(env, local_dt(7, 55), local_dt(8, 45))
    reminder_notes = [n for n in notes(env)
                      if "the 8:00am Metformin reminder couldn't be sent" in n]
    assert len(reminder_notes) == 1
    assert env.sent_count("Lisinopril") >= 1


def test_reminder_superseded_by_a_delivered_nudge_is_not_reported(env):
    env.write(meds=two_meds())
    env.fail_sends_containing("Reminder: Metformin")     # the nudge gets through
    tick_every_5(env, local_dt(7, 55), local_dt(9, 0))
    assert env.sent_count("Late: Metformin") >= 1
    assert notes(env) == []


def test_resolved_dose_is_not_reported(env):
    env.write(meds=two_meds())
    env.run(local_dt(7, 55))
    env.fail_sends_containing("Reminder: Metformin")
    for hm in ((8, 0), (8, 5), (8, 15)):
        env.run(local_dt(*hm))
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 16)))
    env.run(local_dt(8, 20))
    assert notes(env) == []


def test_note_waits_for_quiet_hours_to_end(env):
    # digest fails from 21:55; its 3rd failure and the proof that other sends
    # work (the 22:20 nudge, inside the quiet head) both land in quiet hours
    env.write(meds=[make_med(times=["21:50"])], digest_time="21:55",
              quiet_start="22:00", quiet_end="07:00")
    env.fail_sends_containing("Meds for")
    tick_every_5(env, local_dt(21, 45), local_dt(23, 55))
    assert notes(env) == []
    env.run(local_dt(7, 5) + timedelta(days=1))
    assert len(notes(env)) == 1
