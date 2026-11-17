"""
Multi-day weekly schedules (PR 7) — end-to-end: the tick enumerates a
Mon–Fri med with zero weekend phantoms, the digest/status labels format
day lists, and reply.py add/edit accept both day_of_week forms.

Helper-level coverage (day_indexes, occurrences_between, compute_next_due,
fmt_days) lives in tests/test_weekly.py; validator cases in
tests/test_safe_write.py; the editor's array handling in editor_check.cjs.

Fixture date 2026-04-21 is a Tuesday; the surrounding week runs
Fri Apr 17 – Mon Apr 27, so Sat/Sun are Apr 18/19.
"""
import datetime as dtmod
import json
from zoneinfo import ZoneInfo

import pytest

import dispatch
import event_store
import safe_write as sw
import tick
from clock import FakeClock, parse_instant
from occurrence import at_local
from reply import handle_add_med, handle_edit_med, handle_status
from tests.conftest import local_dt, make_med, make_state, make_tick_env, utc

TZ = ZoneInfo("America/Los_Angeles")
WEEKDAYS = ["mon", "tue", "wed", "thu", "fri"]
DAYTIME_QUIET = ("13:00", "14:00")   # parked away from every dose/nudge here


@pytest.fixture
def env(tmp_path, monkeypatch):
    return make_tick_env(tmp_path, monkeypatch)


@pytest.fixture
def state_file(tmp_path, monkeypatch):
    sf = tmp_path / "meds-state.json"
    monkeypatch.setattr(dispatch, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "STATE_FILE", sf)
    monkeypatch.setattr(sw, "LOG_FILE", tmp_path / "sw.log")
    return sf


def write_state(sf, meds=None, **kw):
    sf.write_text(json.dumps(make_state(meds=meds if meds is not None else [], **kw)),
                  encoding="utf-8")


def on_disk(sf):
    return json.loads(sf.read_text(encoding="utf-8"))


# ── Tick: Mon–Fri med, zero weekend phantoms ──────────────────────────────────

def test_tick_mon_fri_zero_weekend_phantoms(env):
    med = make_med(frequency="weekly", times=["09:00"], day_of_week=WEEKDAYS)
    med["active_since_utc"] = utc(local_dt(0, 0, day=17)).isoformat()   # Fri
    env.write(meds=[med], quiet_start=DAYTIME_QUIET[0], quiet_end=DAYTIME_QUIET[1],
              digest_time="23:59")
    env.run(local_dt(8, 55, day=17))            # Friday warm tick
    env.run(local_dt(9, 5, day=17))             # Friday reminder
    assert env.sent_count("Metformin") == 1
    env.seed([event_store.new_event(            # Friday's dose taken at 09:10
        "med-001", "taken", local_dt(9, 10, day=17),
        occurrence=at_local(dtmod.date(2026, 4, 17), "09:00", TZ, 0))])

    env.run(local_dt(9, 5, day=18))             # Saturday tick
    env.run(local_dt(9, 5, day=19))             # Sunday tick

    assert env.sent_count("Metformin") == 1     # nothing new sent
    assert env.events("missed") == []           # nothing logged missed
    weekend = [e for e in env.events()
               if str(e.get("occurrence_key", "")).startswith(("2026-04-18", "2026-04-19"))]
    assert weekend == []                        # no event keys on Sat/Sun at all

    env.run(local_dt(8, 55, day=20))            # Monday warm tick
    env.run(local_dt(9, 5, day=20))             # Monday reminder back on schedule
    assert env.sent_count("Metformin") == 2


def test_tick_tue_sat_reminds_on_both_days(env):
    med = make_med(frequency="weekly", times=["09:00"], day_of_week=["tue", "sat"])
    med["active_since_utc"] = utc(local_dt(0, 0, day=17)).isoformat()   # Fri
    env.write(meds=[med], quiet_start=DAYTIME_QUIET[0], quiet_end=DAYTIME_QUIET[1],
              digest_time="23:59")
    env.run(local_dt(8, 55, day=18))            # Saturday warm tick
    env.run(local_dt(9, 5, day=18))
    env.run(local_dt(8, 55, day=21))            # Tuesday warm tick
    env.run(local_dt(9, 5, day=21))
    assert env.sent_count("Metformin") == 2
    keys = sorted(e["occurrence_key"] for e in env.events("send_intent"))
    assert keys == ["2026-04-18T09:00#0", "2026-04-21T09:00#0"]


# ── Digest / status labels ────────────────────────────────────────────────────

def test_digest_labels_multi_day():
    state = make_state(meds=[
        make_med(frequency="weekly", times=["09:00"], day_of_week=WEEKDAYS),
        make_med(med_id="med-002", name="Methotrexate",
                 frequency="weekly", times=["09:00"], day_of_week=["tue", "sat"]),
        make_med(med_id="med-003", name="Legacy", frequency="weekly",
                 times=["09:00"], day_of_week="mon"),
    ])
    # each med is listed only on its own days, so check on Mon and on Tue
    monday = tick.digest_text(state, [], TZ, local_dt(9, 0, day=20))
    tuesday = tick.digest_text(state, [], TZ, local_dt(9, 0, day=21))
    assert "Metformin 500mg | Mon–Fri 9:00am" in monday
    assert "Legacy 500mg | Mon 9:00am" in monday     # legacy form unchanged
    assert "Methotrexate 500mg | Tue+Sat 9:00am" in tuesday


def test_status_labels_multi_day(state_file, capsys):
    write_state(state_file, meds=[
        make_med(frequency="weekly", times=["09:00"], day_of_week=["tue", "sat"]),
    ])
    handle_status()
    out = capsys.readouterr().out
    assert "Tue+Sat 9:00am" in out


# ── add-med: both forms accepted, canonical stored ────────────────────────────

def test_add_med_list_sorted_and_deduped(state_file):
    write_state(state_file, meds=[])
    handle_add_med(json.dumps(make_med(frequency="weekly", times=["09:00"],
                                       day_of_week=["sat", "tue", "sat"])),
                   dry_run=False, clock=FakeClock(local_dt(12, 0)))
    assert on_disk(state_file)["meds"][0]["schedule"]["day_of_week"] == ["tue", "sat"]


def test_add_med_single_string_stays_string(state_file):
    write_state(state_file, meds=[])
    handle_add_med(json.dumps(make_med(frequency="weekly", times=["09:00"],
                                       day_of_week="tue")),
                   dry_run=False, clock=FakeClock(local_dt(12, 0)))
    assert on_disk(state_file)["meds"][0]["schedule"]["day_of_week"] == "tue"


def test_add_med_empty_list_rejected(state_file, capsys):
    write_state(state_file, meds=[])
    with pytest.raises(SystemExit) as e:
        handle_add_med(json.dumps(make_med(frequency="weekly", times=["09:00"],
                                           day_of_week=[])),
                       dry_run=False, clock=FakeClock(local_dt(12, 0)))
    assert e.value.code != 0
    assert "empty list" in capsys.readouterr().out
    assert on_disk(state_file)["meds"] == []


def test_add_med_unknown_day_rejected(state_file, capsys):
    write_state(state_file, meds=[])
    with pytest.raises(SystemExit) as e:
        handle_add_med(json.dumps(make_med(frequency="weekly", times=["09:00"],
                                           day_of_week=["tue", "funday"])),
                       dry_run=False, clock=FakeClock(local_dt(12, 0)))
    assert e.value.code != 0
    assert "funday" in capsys.readouterr().out
    assert on_disk(state_file)["meds"] == []


# ── edit-med: canonical writes and semantic re-anchoring ──────────────────────

def test_edit_med_representation_swap_does_not_re_anchor(state_file):
    med = make_med(frequency="weekly", times=["09:00"], day_of_week="tue")
    med["active_since_utc"] = local_dt(6, 0).isoformat()
    write_state(state_file, meds=[med])

    handle_edit_med("med-001", json.dumps(make_med(frequency="weekly", times=["09:00"],
                                                   day_of_week=["tue"])),
                    dry_run=False, clock=FakeClock(local_dt(10, 0)))

    med_after = on_disk(state_file)["meds"][0]
    assert med_after["schedule"]["day_of_week"] == ["tue"]
    # 'tue' == ['tue'] — same schedule, tracking anchor untouched
    assert parse_instant(med_after["active_since_utc"]) == utc(local_dt(6, 0))


def test_edit_med_day_change_re_anchors(state_file):
    med = make_med(frequency="weekly", times=["09:00"], day_of_week=["tue", "sat"])
    med["active_since_utc"] = local_dt(6, 0).isoformat()
    write_state(state_file, meds=[med])

    handle_edit_med("med-001", json.dumps(make_med(frequency="weekly", times=["09:00"],
                                                   day_of_week=["tue"])),
                    dry_run=False, clock=FakeClock(local_dt(10, 0)))

    med_after = on_disk(state_file)["meds"][0]
    assert med_after["schedule"]["day_of_week"] == ["tue"]
    assert parse_instant(med_after["active_since_utc"]) == utc(local_dt(10, 0))


def test_edit_med_unknown_day_rejected(state_file, capsys):
    med = make_med(frequency="weekly", times=["09:00"], day_of_week="tue")
    write_state(state_file, meds=[med])
    with pytest.raises(SystemExit) as e:
        handle_edit_med("med-001", json.dumps(make_med(frequency="weekly", times=["09:00"],
                                                       day_of_week=["sonday"])),
                        dry_run=False, clock=FakeClock(local_dt(10, 0)))
    assert e.value.code != 0
    assert "sonday" in capsys.readouterr().out
    assert on_disk(state_file)["meds"][0]["schedule"]["day_of_week"] == "tue"
