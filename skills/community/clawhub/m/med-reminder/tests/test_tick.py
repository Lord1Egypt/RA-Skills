"""
Tick engine tests (issue #1 §3, PR 2 — testing-plan rows 4-6: AC 7, 12,
14-22 minus the send-lease ACs, which live in test_send_leases.py).

One state file + the fake sender per test via make_tick_env. Time comes
from FakeClock; every comparison normalizes to UTC.
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

import event_store
import tick
from occurrence import at_local, at_utc
from tests.conftest import iso, local_dt, make_med, make_state, make_tick_env, TZ, utc

import datetime as dtmod

TUE = dtmod.date(2026, 4, 21)    # Tue
MON = dtmod.date(2026, 4, 20)    # Mon
SUN = dtmod.date(2026, 4, 19)    # Sun


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


def once_daily(times=("08:00",), **kw):
    return make_med(frequency="once_daily", times=list(times), **kw)


def occ(hhmm, day=TUE, index=0):
    return at_local(day, hhmm, TZ, index)


def snoozed_event(med_id, occurrence, until, ts, gen=0):
    return event_store.new_event(
        med_id, "snoozed", ts, occurrence=occurrence, generation=gen,
        ref=until.isoformat())


def undone_event(med_id, occurrence, ts, ref="taken"):
    return event_store.new_event(
        med_id, "undone", ts, occurrence=occurrence, ref=ref)


# ── AC 7/8: the reminder, and idempotency ────────────────────────────────────

def test_ac8_reminder_fires_at_first_tick_after_dose_time(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 0))                 # pre-dose: quiet-adjacent, nothing due
    assert env.sent() == []
    env.run(local_dt(8, 5))
    msgs = env.sent()
    assert len(msgs) == 1 and "Metformin 500mg" in msgs[0] and "Reminder" in msgs[0]
    assert env.events("send_intent")[0]["stage"] == "reminder"


def test_ac7_running_tick_twice_same_now_is_a_noop(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    before_events = env.events()
    before_sent = env.sent()
    env.run(local_dt(8, 5))
    assert env.events() == before_events
    assert env.sent() == before_sent
    assert len(env.sent()) == 1


def test_nothing_due_tick_writes_no_state(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(8, 5))                 # reminder + digest day starts here
    before = env.state_file.read_text(encoding="utf-8")
    env.run(local_dt(12, 0))                # mid-day, nothing due
    assert env.state_file.read_text(encoding="utf-8") == before, \
        "state (and .bak) must not be rewritten when no events occur"
    hb = env.heartbeat()
    assert hb["watermark_utc"] == utc(local_dt(12, 0)).isoformat()


def test_heartbeat_written_every_run(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(8, 5))
    hb1 = env.heartbeat()
    env.run(local_dt(8, 10))
    hb2 = env.heartbeat()
    assert hb1["started_utc"] < hb2["started_utc"]
    assert hb2["errors"] == 0
    assert (env.state_file.parent / "tick-heartbeat.json").exists()


def test_watermark_trails_a_pending_escalation(env):
    # regression: the watermark may not pass an unresolved occurrence, or
    # later ticks never see it again and the nudge/missed stages are lost
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))                 # reminder sent, escalation pending
    wm = utc(parse_hb(env.heartbeat()["watermark_utc"]))
    assert wm <= utc(local_dt(8, 0))
    env.run(local_dt(8, 40))                # nudge still fires
    assert env.sent_count("Late:") == 1
    env.run(local_dt(19, 0))                # nudging continues all day (#11)
    assert env.sent_count("Late:") == 2
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))   # next dose closes it
    assert len(env.events("missed")) == 1


def parse_hb(raw):
    from clock import parse_instant
    return parse_instant(raw)


# ── Stages: only the highest due stage acts ──────────────────────────────────

def test_nudge_at_T_plus_late(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))                 # reminder
    env.run(local_dt(8, 40))                # late=30 → nudge due 08:30
    assert env.sent_count("Late: Metformin") == 1
    evs = [e for e in env.events() if e["event"] == "send_intent"]
    assert {e["stage"] for e in evs} >= {"reminder", "nudge"}


def test_machine_off_through_nudge_sends_nudge_only(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 0))                 # last tick before the machine "slept"
    env.run(local_dt(8, 40))                # first tick after T: nudge is highest
    msgs = env.sent()
    assert len(msgs) == 1 and "Late:" in msgs[0]
    assert not any("Reminder" in m for m in msgs)


def test_missed_logged_silently_when_next_dose_arrives(env):
    # #11: an unresolved dose stays open (nudged) until the next dose is due,
    # then closes as missed — silently; the next dose's reminder goes out
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    env.run(local_dt(8, 40))
    env.run(local_dt(23, 55))
    assert env.events("missed") == []       # old T+90 deadline is gone
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    assert env.sent_count("Missed:") == 0
    missed = env.events("missed")
    assert len(missed) == 1 and missed[0]["occurrence_key"] == "2026-04-21T08:00#0"
    assert env.sent_count("Reminder") == 2  # today's and tomorrow's
    assert env.med_state()["missed_count"] == 1
    # next_due rolls past the missed dose (legacy field; compare instants)
    from clock import parse_instant
    assert parse_instant(env.med_state()["next_due"]) ==         occ("08:00", TUE + dtmod.timedelta(days=1)).utc


def test_taken_suppresses_all_stages(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    taken = event_store.new_event("med-001", "taken", local_dt(8, 10),
                                  occurrence=occ("08:00"))
    env.seed([taken])
    env.run(local_dt(8, 5))
    env.run(local_dt(9, 40))
    assert env.sent() == []
    assert env.events("missed") == []


def test_skipped_suppresses_all_stages(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    skipped = event_store.new_event("med-001", "skipped", local_dt(8, 0),
                                    occurrence=occ("08:00"))
    env.seed([skipped])
    env.run(local_dt(9, 40))
    assert env.sent() == []
    assert env.events("missed") == []


# ── AC 14: catch-up consolidation ─────────────────────────────────────────────

def four_meds_two_doses():
    meds = []
    for i in range(1, 5):
        meds.append(make_med(med_id=f"med-{i:03d}", name=f"Med{i}",
                             frequency="twice_daily", times=["08:00", "20:00"]))
    return meds


def test_ac14_catchup_one_consolidated_message(env):
    env.write(meds=four_meds_two_doses())
    env.run(local_dt(7, 0))                 # last tick before the gap
    env.run(local_dt(21, 0))                # machine "off" 07:00–21:00: the 08:00
    msgs = env.sent()                       # doses closed at 20:00 while it was off
    consolidated = [m for m in msgs if "wasn't logged" in m]
    assert len(consolidated) == 1, f"exactly one consolidated message, got {msgs}"
    for i in range(1, 5):
        assert f"Med{i} 8:00am" in consolidated[0]
    missed = env.events("missed")
    assert len(missed) == 4                 # silent misses, one per med
    # digest (08:00) folded in — no separate digest message at 12:00
    assert not any("Meds for" in m for m in msgs)


def test_catchup_line_mentions_the_reply_hint(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 0))
    env.run(local_dt(9, 0) + dtmod.timedelta(days=1))   # 08:00 dose closed at
                                                        # 08:00 tomorrow, while off
    m = [x for x in env.sent() if "wasn't logged" in x][0]
    assert "took metformin at 8" in m
    assert "check your med's instructions" in m


# ── AC 12: interval meds ──────────────────────────────────────────────────────

def test_ac12_interval_reminds_nudges_and_misses(env):
    med = make_med(frequency="interval", interval_hours=8)
    med["active_since_utc"] = utc(local_dt(8, 0)).isoformat()
    env.write(meds=[med])
    env.run(local_dt(8, 5))
    assert env.sent_count("Reminder") == 1
    env.run(local_dt(8, 40))
    assert env.sent_count("Late:") == 1
    env.run(local_dt(16, 5))                # next interval dose closes 08:00
    assert env.sent_count("Missed:") == 0
    assert env.sent_count("Reminder") == 2
    # anchor keyed by UTC instant
    assert env.events("missed")[0]["occurrence_key"] == "2026-04-21T15:00:00Z"


def test_ac12_interval_null_next_due_initialized_from_active_since(env):
    med = make_med(frequency="interval", interval_hours=8)
    med["active_since_utc"] = utc(local_dt(8, 0)).isoformat()
    env.write(meds=[med])
    env.run(local_dt(9, 0))
    assert env.med_state()["next_due"] == utc(local_dt(8, 0)).isoformat()


def test_interval_anchor_inited_to_quiet_end_when_active_since_is_quiet(env):
    med = make_med(frequency="interval", interval_hours=8)
    med["active_since_utc"] = utc(local_dt(23, 0)).isoformat()   # inside 22:00–07:00
    env.write(meds=[med])
    env.run(local_dt(23, 5))
    # next quiet end is 07:00 tomorrow
    assert env.med_state()["next_due"] == utc(local_dt(7, 0) + dtmod.timedelta(days=1)).isoformat()


def test_ac12_interval_20h_gap_produces_exactly_one_message(env):
    med = make_med(frequency="interval", interval_hours=8)
    med["active_since_utc"] = utc(datetime(2026, 4, 20, 8, 0, tzinfo=TZ)).isoformat()
    env.write(meds=[med])
    # ticks while the machine is "on", then a 20h gap
    env.run(datetime(2026, 4, 20, 8, 5, tzinfo=TZ))  # anchor init → reminder
    env.run(datetime(2026, 4, 20, 8, 40, tzinfo=TZ))
    env.sent_file.write_text("", encoding="utf-8")
    env.run(datetime(2026, 4, 21, 8, 0, tzinfo=TZ))   # 20h later
    # overdue and never confirmed: 08:00 d1 (closed 16:00) and 16:00 d1
    # (closed 00:00) closed while the machine was off → one consolidated
    # message; 00:00 d2 closes right now as 08:00 d2 arrives (fresh, so
    # silent) and 08:00 d2's reminder is due as well
    msgs = [m for m in env.sent() if "wasn't logged" in m]
    assert len(msgs) == 1
    assert "8:00am" in msgs[0] and "4:00pm" in msgs[0] and "12:00am" not in msgs[0]
    assert len(env.events("missed")) == 3
    assert env.sent_count("Reminder") == 1


def test_interval_occurrences_keyed_by_utc_instant_no_dst_collision(env):
    # covered fully in test_dst.py; here: distinct keys across a 1h chain
    med = make_med(frequency="interval", interval_hours=1)
    med["active_since_utc"] = utc(local_dt(10, 0)).isoformat()
    env.write(meds=[med])
    env.run(local_dt(13, 0))
    keys = {e["occurrence_key"] for e in env.events()
            if e.get("med_id") == "med-001" and e.get("occurrence_key")}
    # 10:00 (missed), 11:00 (missed), 12:00 (nudge), 13:00 (reminder)
    assert len(keys) == 4


# ── AC 22: double-dose guard ──────────────────────────────────────────────────

def test_ac22_reminder_includes_double_dose_warning(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.seed([event_store.new_event(
        "med-001", "taken", local_dt(3, 30),
        occurrence=at_utc(utc(local_dt(2, 30)), TZ),
        taken_at_utc=utc(local_dt(2, 30)).isoformat())])
    # gap is 12h; the 02:30 taken is 5.5h before T=08:00 → within the gap
    env.run(local_dt(8, 5))
    msg = env.sent()[0]
    assert "You logged Metformin today at 2:30am" in msg
    assert "Don't take another unless your prescriber says so" in msg


def test_double_dose_warning_absent_outside_gap(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.seed([event_store.new_event(
        "med-001", "taken", local_dt(12, 0) - dtmod.timedelta(days=1),
        occurrence=occ("08:00", MON - dtmod.timedelta(days=1)),
        taken_at_utc=utc(local_dt(12, 0) - dtmod.timedelta(days=1)).isoformat())])
    env.run(local_dt(8, 5))
    assert "Don't take another" not in env.sent()[0]


# ── AC 19/20/21: snooze, skip, undo (stage side; commands land in PR 4) ───────

def test_ac19_snooze_stages(env):
    env.write(meds=[once_daily()])
    env.seed([snoozed_event("med-001", occ("08:00"), utc(local_dt(8, 35)),
                            local_dt(8, 5))])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 36))
    msgs = env.sent()
    assert len(msgs) == 1 and "snoozed" in msgs[0]
    env.run(local_dt(9, 6))                 # nudge at until+30
    assert env.sent_count("Late:") == 1
    env.run(local_dt(9, 31))                # no new slot yet (next is 09:35)
    assert env.sent_count("Late:") == 1
    env.run(local_dt(9, 36))                # cadence re-anchored on the wake
    assert env.sent_count("Late:") == 2
    assert {e["stage"] for e in env.events("send_intent")} >= {"nudge-65", "nudge-95"}
    assert env.events("missed") == []
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    assert len(env.events("missed")) == 1


def test_snooze_never_misses_before_its_reminder(env):
    env.write(meds=[once_daily()])
    env.seed([snoozed_event("med-001", occ("08:00"), utc(local_dt(10, 0)),
                            local_dt(8, 5))])
    env.run(local_dt(7, 55))
    env.run(local_dt(9, 59))
    assert env.events("missed") == []
    assert env.sent_count("Missed:") == 0


def test_ac21_undo_bumps_generation_and_re_reminds(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.seed([
        event_store.new_event("med-001", "taken", local_dt(8, 10),
                              occurrence=occ("08:00")),
        undone_event("med-001", occ("08:00"), local_dt(8, 20)),
    ])
    env.run(local_dt(8, 25))                # before T+late → re-remind, new gen
    msgs = env.sent()
    assert len(msgs) == 1 and "Reminder" in msgs[0]
    assert env.events("send_intent")[0]["generation"] == 1


def test_ac21_undo_reopens_the_dose_until_the_next_one(env):
    # #11: an undone dose is open again — nudged on the cadence — and closes
    # silently as missed when the next dose arrives
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.seed([
        event_store.new_event("med-001", "taken", local_dt(8, 10),
                              occurrence=occ("08:00")),
        undone_event("med-001", occ("08:00"), local_dt(11, 0)),
    ])
    env.run(local_dt(11, 5))
    assert env.sent_count("Late:") == 1
    assert env.events("send_intent")[0]["generation"] == 1
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    assert len(env.events("missed")) == 1
    assert env.events("missed")[0]["generation"] == 1
    assert env.sent_count("wasn't logged") == 0


# ── Quiet hours (AC 28 + message suppression) ─────────────────────────────────

def test_reminder_is_quiet_exempt(env):
    env.write(meds=[once_daily(times=("23:30",))])
    env.run(local_dt(23, 25))
    env.run(local_dt(23, 35))               # inside 22:00–07:00
    assert env.sent_count("Reminder") == 1


def test_ac28_nudge_sent_in_first_30min_of_quiet_hours(env):
    env.write(meds=[once_daily(times=("21:30",))])   # late 30 → nudge due 22:00
    env.run(local_dt(21, 25))
    env.run(local_dt(21, 35))               # reminder first
    env.run(local_dt(22, 0))
    assert env.sent_count("Late:") == 1


def test_nudge_muted_mid_quiet_hours(env):
    env.write(meds=[once_daily(times=("20:00",))])
    state = env.state()
    state["meds"][0]["escalation"]["late_threshold_minutes"] = 210   # slots 23:30, 03:00, 06:30, 10:00
    env.state_file.write_text(json.dumps(state), encoding="utf-8")
    env.run(local_dt(19, 55))
    env.run(local_dt(20, 5))                # reminder
    env.run(local_dt(23, 55))
    assert env.sent_count("Late:") == 0     # nudge muted mid-quiet
    env.run(local_dt(3, 5) + dtmod.timedelta(days=1))
    env.run(local_dt(7, 5) + dtmod.timedelta(days=1))
    assert env.sent_count("Late:") == 0     # 03:00 and 06:30 muted, no burst at 07:00
    env.run(local_dt(10, 5) + dtmod.timedelta(days=1))
    assert env.sent_count("Late:") == 1     # first slot after quiet hours


def night_dose_closed_in_quiet_hours(env):
    """23:30 daily dose never taken: it closes as missed when the next
    night's 23:30 dose arrives — inside quiet hours."""
    env.write(meds=[once_daily(times=("23:30",))])
    env.run(local_dt(23, 25))
    env.run(local_dt(23, 35))               # reminder (quiet-exempt)
    env.run(local_dt(23, 35) + dtmod.timedelta(days=1))  # closes, quiet


def test_missed_event_logged_without_message_in_quiet_hours(env):
    night_dose_closed_in_quiet_hours(env)
    assert len(env.events("missed")) == 1
    assert env.sent_count("Missed:") == 0
    assert env.sent_count("wasn't logged") == 0


def test_ac28_overnight_summary_after_quiet_hours_end(env):
    night_dose_closed_in_quiet_hours(env)
    env.run(local_dt(7, 5) + dtmod.timedelta(days=2))    # first tick after 07:00
    summary = [m for m in env.sent() if "While you slept" in m]
    assert len(summary) == 1
    assert "Metformin (11:30pm)" in summary[0]
    # once per local date
    env.run(local_dt(7, 10) + dtmod.timedelta(days=2))
    assert len([m for m in env.sent() if "While you slept" in m]) == 1


def test_overnight_skipped_when_more_than_4h_late(env):
    night_dose_closed_in_quiet_hours(env)
    env.run(local_dt(12, 0) + dtmod.timedelta(days=2))   # way past 07:00+4h
    assert env.sent_count("While you slept") == 0


# ── AC 15/17/18: watermark, active_since, clock anomaly ───────────────────────

def test_ac17_migration_day_no_phantom_actions(env):
    # dose confirmed under old code at 08:05 (legacy state), first tick 10:00
    med = make_med(frequency="once_daily", times=["08:00"],
                   status="confirmed",
                   last_taken=iso(local_dt(8, 5)),
                   confirmed_dose=iso(local_dt(8, 0)),
                   history=[{"timestamp": iso(local_dt(8, 5)), "event": "taken",
                             "dose_prescribed": "500mg"}])
    env.write(meds=[med])
    env.run(local_dt(10, 0))
    assert env.sent() == []
    assert env.events("missed") == []
    assert env.events("nudge") == []
    # migration recorded the taken dose keyed to the 08:00 occurrence
    assert any(e["event"] == "taken" and e.get("occurrence_key") == "2026-04-21T08:00#0"
               for e in env.events())


def test_ac18_virgin_state_yields_zero_misses(env):
    env.write(meds=[once_daily()])          # no watermark, no active_since
    env.run(local_dt(15, 0))                # first-ever tick mid-afternoon
    assert env.events("missed") == []
    assert env.sent_count("wasn't logged") == 0
    # and the next day's dose reminds normally
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    assert env.sent_count("Reminder") == 1


def test_ac18_active_since_gates_enumeration(env):
    med = once_daily()
    med["active_since_utc"] = utc(local_dt(15, 0)).isoformat()   # "added at 15:00"
    env.write(meds=[med])
    env.run(local_dt(15, 5))
    assert env.events("missed") == [] and env.sent() == []
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    assert env.sent_count("Reminder") == 1


def test_ac15_clock_jump_forward_and_back(env):
    env.write(meds=[once_daily(times=("20:00",))])
    real_now = local_dt(12, 0)
    env.run(real_now)
    env.run(real_now + dtmod.timedelta(hours=24))        # forward 24h
    forward_missed = env.events("missed")
    env.run(real_now + dtmod.timedelta(minutes=10))      # back — anomaly
    anomalies = env.events("clock_anomaly")
    assert len(anomalies) == 1
    # occurrences actually in the future: their missed events were stamped
    # with the jumped-forward clock, so a tick at restored real time ignores
    # them (ts_utc later than now + 5min) — zero effective misses
    restored = utc(real_now + dtmod.timedelta(minutes=10))
    from clock import parse_instant
    effective = [e for e in forward_missed
                 if parse_instant(e["ts_utc"]) <= restored + dtmod.timedelta(minutes=5)]
    assert effective == []
    # the anomaly tick itself wrote nothing but the anomaly and sent nothing
    assert env.sent_count("Reminder") + env.sent_count("Missed:") == 0


def test_clock_anomaly_dedupes_within_an_hour(env):
    env.write(meds=[once_daily(times=("20:00",))])
    now = local_dt(12, 0)
    env.run(now)
    env.run(now + dtmod.timedelta(hours=24))
    env.run(now + dtmod.timedelta(minutes=1))
    env.run(now + dtmod.timedelta(minutes=2))
    assert len(env.events("clock_anomaly")) == 1


def test_72h_cap_sends_away_message_and_limits_catchup(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(12, 0) - dtmod.timedelta(days=5))   # last tick 5 days ago
    before = len(env.sent())
    env.run(local_dt(12, 0))
    away = [m for m in env.sent()[before:] if "Were you away?" in m]
    assert len(away) == 1
    assert "over 3 days" in away[0]
    # 5 days of once-daily doses, capped at 72h: the window at 12:00 covers
    # Apr 18 12:00 → Apr 21 12:00, so the doses on 19/20/21 are enumerated.
    # 19 and 20 closed when the next dose arrived (silent + one consolidated
    # message); today's 08:00 is still open, so it is nudged instead (#11)
    assert len(env.events("missed")) == 2
    assert env.sent_count("wasn't logged") == 1
    assert env.sent_count("Late:") == 1


def test_72h_cap_backfills_at_most_three_days(env):
    env.write(meds=[once_daily()])
    env.run(local_dt(12, 0) - dtmod.timedelta(days=5))
    env.run(local_dt(12, 0))
    keys = sorted(e["occurrence_key"] for e in env.events("missed"))
    assert keys == ["2026-04-19T08:00#0", "2026-04-20T08:00#0"]


# ── AC 16: fault isolation ────────────────────────────────────────────────────

def broken_and_healthy():
    return [make_med(med_id="med-001", name="Broken", frequency="once_daily",
                     times=["08:00"]),
            make_med(med_id="med-002", name="Healthy", frequency="once_daily",
                     times=["08:00"])]


@pytest.fixture
def broken_med001(monkeypatch):
    """Inject a processing failure for med-001 only (valid state, failing logic)."""
    real = tick._process_occurrence

    def flaky(plan, state, med, occ, *a, **kw):
        if med["id"] == "med-001":
            raise ValueError("schedule blew up")
        return real(plan, state, med, occ, *a, **kw)

    monkeypatch.setattr(tick, "_process_occurrence", flaky)


def test_ac16_broken_med_does_not_stop_others(env, broken_med001):
    env.write(meds=broken_and_healthy())
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    assert env.sent_count("Reminder") == 1
    assert "Healthy" in [m for m in env.sent() if "Reminder" in m][0]
    alerts = [m for m in env.sent() if "run doctor" in m]
    assert alerts == ["Can't process Broken's schedule — run doctor."]
    assert env.heartbeat()["errors"] == 1


def test_ac16_one_alert_per_day(env, broken_med001):
    env.write(meds=broken_and_healthy())
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    env.run(local_dt(9, 5))
    env.run(local_dt(10, 5))
    assert len([m for m in env.sent() if "run doctor" in m]) == 1


def test_bad_timezone_falls_back_with_alert(env):
    env.write(meds=[make_med(frequency="once_daily", times=["08:00"])])
    env.run(local_dt(7, 55))
    st = env.state()
    st["global"]["timezone"] = "Not/AZone"
    env.state_file.write_text(json.dumps(st), encoding="utf-8")
    code = env.run(local_dt(8, 5))
    assert code == 0
    assert len([m for m in env.sent() if "Timezone" in m]) == 1
    # last-good tz was never set → falls back to UTC; 08:00 UTC = 01:00 PDT,
    # so nothing reminds yet — but the tick survived and heartbeated
    assert env.heartbeat()["errors"] == 0


def test_bad_timezone_uses_last_good_cache(env):
    env.write(meds=[make_med(frequency="once_daily", times=["08:00"])])
    env.run(local_dt(7, 0))                 # good tz cached
    st = env.state()
    st["global"]["timezone"] = "Not/AZone"
    env.state_file.write_text(json.dumps(st), encoding="utf-8")
    env.run(local_dt(8, 5))
    assert env.sent_count("Reminder") == 1  # still on America/Los_Angeles


# ── Paused ────────────────────────────────────────────────────────────────────

def test_globally_paused_tick_sends_nothing(env):
    env.write(meds=[once_daily()], paused=True)
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5))
    assert env.sent() == []
    assert env.events("missed") == []


def test_paused_med_skipped(env):
    env.write(meds=[make_med(frequency="once_daily", times=["08:00"], paused=True)])
    env.run(local_dt(7, 55))
    env.run(local_dt(9, 40))
    assert env.sent() == [] and env.events("missed") == []


# ── Dry run ───────────────────────────────────────────────────────────────────

def test_dry_run_prints_and_writes_nothing(env, capsys):
    env.write(meds=[once_daily()])
    env.run(local_dt(7, 55))
    env.run(local_dt(8, 5), dry_run=True)
    assert env.sent() == []
    assert env.events() == []
    out = capsys.readouterr().out
    assert "Would send" in out and "Reminder" in out
