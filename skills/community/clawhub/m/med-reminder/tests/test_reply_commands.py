"""
Reply command tests — issue #1 PR 4 §6: snooze, skip (defer's alias tests
live in test_reply_handler.py), then undo, pause/unpause, the edit-time
quiet-hours rejections, add/edit/remove/status/show-state, and --position
resolution.

Every command goes through transact and writes store events (snoozed with
the wake instant in `ref`, skipped, undone with `ref` = the undone event's
id) — the shapes tick.py already reads (PR 2).
"""
import hashlib
import json

import pytest

import dispatch
import event_store
import safe_write as sw
import tick
from clock import FakeClock, parse_instant
from reply import (
    handle_add_med,
    handle_confirm,
    handle_edit_med,
    handle_pause,
    handle_remove,
    handle_set_quiet_hours,
    handle_show_state,
    handle_skip,
    handle_snooze,
    handle_status,
    handle_undo,
    handle_unpause,
)
from tests.conftest import local_dt, make_med, make_state, make_tick_env, utc

import datetime as dtmod


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


def events(sf):
    return event_store.load_events(sw.history_file())


def on_disk(sf):
    return json.loads(sf.read_text(encoding="utf-8"))


# ── snooze ─────────────────────────────────────────────────────────────────────

def test_snooze_writes_snoozed_event_with_wake_instant(state_file):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])

    handle_snooze("med-001", 30, dry_run=False, clock=FakeClock(local_dt(8, 5)))

    evs = events(state_file)
    assert len(evs) == 1 and evs[0]["event"] == "snoozed"
    assert evs[0]["occurrence_key"] == "2026-04-21T08:00#0"
    assert evs[0]["generation"] == 0
    # the wake instant rides in `ref` — the format tick.snooze_until_for reads
    assert parse_instant(evs[0]["ref"]) == utc(local_dt(8, 35))


def test_snooze_defaults_to_120_minutes(state_file):
    # #11: the default pause is 2h (a 30-min default collided with the nudge)
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])

    handle_snooze("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))

    assert parse_instant(events(state_file)[0]["ref"]) == utc(local_dt(10, 5))


def test_snooze_default_shrinks_to_fit_before_the_next_dose(state_file):
    # 08:00/09:00 at 08:05: the dose closes at 09:00 → the default 120
    # shrinks to 54 minutes (wake at 08:59, before the close)
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "09:00"])
    write_state(state_file, meds=[med])

    handle_snooze("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 5)))

    assert parse_instant(events(state_file)[0]["ref"]) == utc(local_dt(8, 59))


@pytest.mark.parametrize("minutes", [4, 241])
def test_snooze_out_of_range_rejected(state_file, minutes):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])

    with pytest.raises(SystemExit) as e:
        handle_snooze("med-001", minutes, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert e.value.code != 0
    assert events(state_file) == []


def test_snooze_cap_refusal_and_boundary(state_file, capsys):
    # 08:00/11:00 at 08:05 → the dose closes at 11:00 → cap 174 minutes
    # (the wake must land before the close, #11)
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "11:00"])
    write_state(state_file, meds=[med])

    with pytest.raises(SystemExit) as e:
        handle_snooze("med-001", 175, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert e.value.code != 0
    out = capsys.readouterr().out
    assert "run into your next dose" in out and "skip instead?" in out
    assert events(state_file) == []

    # exactly at the cap is allowed
    handle_snooze("med-001", 174, dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert parse_instant(events(state_file)[0]["ref"]) == utc(local_dt(10, 59))


def test_snooze_before_first_tracked_dose_errors(state_file):
    # fresh install: active_since prunes yesterday's occurrence
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    med["active_since_utc"] = local_dt(7, 0).isoformat()
    write_state(state_file, meds=[med])

    with pytest.raises(SystemExit) as e:
        handle_snooze("med-001", 30, dry_run=False, clock=FakeClock(local_dt(7, 30)))
    assert e.value.code != 0
    assert events(state_file) == []


def test_snooze_already_logged_dose_errors(state_file):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    taken = event_store.new_event("med-001", "taken", local_dt(8, 10),
                                  occurrence_key="2026-04-21T08:00#0",
                                  occurrence_utc=utc(local_dt(8, 0)).isoformat())
    event_store.append_events(sw.history_file(), [taken])

    with pytest.raises(SystemExit):
        handle_snooze("med-001", 30, dry_run=False, clock=FakeClock(local_dt(8, 20)))
    assert len(events(state_file)) == 1


def test_snooze_interval_med_caps_at_half_interval(state_file):
    med = make_med(med_id="med-001", frequency="interval", interval_hours=4,
                   next_due=local_dt(8, 0).isoformat())
    write_state(state_file, meds=[med])

    # cap = 4h/2 = 120min: 240 exceeds it
    with pytest.raises(SystemExit):
        handle_snooze("med-001", 240, dry_run=False, clock=FakeClock(local_dt(8, 10)))
    handle_snooze("med-001", 120, dry_run=False, clock=FakeClock(local_dt(8, 10)))
    evs = events(state_file)
    # occurrence keyed by the UTC instant 08:00 PDT = 15:00Z
    assert evs[0]["occurrence_key"] == "2026-04-21T15:00:00Z"
    assert parse_instant(evs[0]["ref"]) == utc(local_dt(10, 10))


def test_ac19_snooze_command_then_tick_stages(tmp_path, monkeypatch):
    env = make_tick_env(tmp_path, monkeypatch)
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med])

    env.run(local_dt(7, 55))                 # watermark init before anything
    env.run(local_dt(8, 1))                  # the reminder that gets snoozed
    assert env.sent_count("Reminder") == 1
    handle_snooze("med-001", 30, dry_run=False, clock=FakeClock(local_dt(8, 5)))

    env.run(local_dt(8, 6))                  # already reminded; the snooze holds
    assert env.sent_count("Reminder") == 1 and env.sent()[-1] == env.sent()[0]
    env.run(local_dt(8, 36))                 # until → snooze reminder
    assert env.sent_count("snoozed") == 1
    env.run(local_dt(9, 6))                  # until+30 → nudge
    assert env.sent_count("Late:") == 1
    env.run(local_dt(9, 36))                 # cadence continues from the wake
    assert env.sent_count("Late:") == 2
    assert env.events("missed") == []
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))   # next dose closes it
    assert len(env.events("missed")) == 1


# ── skip (AC 20) ───────────────────────────────────────────────────────────────

def test_skip_targets_past_or_current_occurrence(state_file):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])

    handle_skip("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 10)))

    evs = events(state_file)
    assert len(evs) == 1 and evs[0]["event"] == "skipped"
    assert evs[0]["occurrence_key"] == "2026-04-21T08:00#0"


def test_skip_without_dose_never_targets_future(state_file):
    # fresh install, next dose still ahead: nothing due → refuse
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    med["active_since_utc"] = local_dt(7, 0).isoformat()
    write_state(state_file, meds=[med])

    with pytest.raises(SystemExit) as e:
        handle_skip("med-001", None, dry_run=False, clock=FakeClock(local_dt(7, 30)))
    assert e.value.code != 0
    assert events(state_file) == []


def test_skip_with_dose_pins_future_occurrence(state_file):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])

    handle_skip("med-001", "20:00", dry_run=False, clock=FakeClock(local_dt(14, 0)))

    assert events(state_file)[0]["occurrence_key"] == "2026-04-21T20:00#1"


def test_skip_with_unscheduled_dose_rejected(state_file):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])

    with pytest.raises(SystemExit) as e:
        handle_skip("med-001", "09:00", dry_run=False, clock=FakeClock(local_dt(14, 0)))
    assert e.value.code != 0
    assert events(state_file) == []


def test_ac20_skip_never_becomes_missed(tmp_path, monkeypatch):
    env = make_tick_env(tmp_path, monkeypatch)
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med])

    env.run(local_dt(7, 55))
    handle_skip("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 10)))
    env.run(local_dt(9, 0))
    env.run(local_dt(10, 31))                # past T+90

    assert env.events("skipped") and env.events("missed") == []
    assert env.sent_count("Missed:") == 0


def test_skip_already_taken_dose_refuses(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    taken = event_store.new_event("med-001", "taken", local_dt(8, 10),
                                  occurrence_key="2026-04-21T08:00#0",
                                  occurrence_utc=utc(local_dt(8, 0)).isoformat())
    event_store.append_events(sw.history_file(), [taken])

    with pytest.raises(SystemExit):
        handle_skip("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 20)))
    assert len(events(state_file)) == 1
    assert "already logged as taken" in capsys.readouterr().out


def test_skip_overrides_an_earlier_missed(state_file):
    # precedence taken > skipped > missed: a later `skipped` flips a missed dose
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    missed = event_store.new_event("med-001", "missed", local_dt(9, 30),
                                   occurrence_key="2026-04-21T08:00#0",
                                   occurrence_utc=utc(local_dt(8, 0)).isoformat())
    event_store.append_events(sw.history_file(), [missed])

    handle_skip("med-001", None, dry_run=False, clock=FakeClock(local_dt(10, 0)))

    assert event_store.outcome(events(state_file), "2026-04-21T08:00#0",
                               0, med_id="med-001") == "skipped"


# ── undo (AC 21) ───────────────────────────────────────────────────────────────

def test_undo_taken_writes_undone_with_ref(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    taken = event_store.new_event(
        "med-001", "taken", local_dt(8, 14),
        occurrence_key="2026-04-21T08:00#0",
        occurrence_utc=utc(local_dt(8, 0)).isoformat(),
        taken_at_utc=utc(local_dt(8, 14)).isoformat())
    event_store.append_events(sw.history_file(), [taken])

    handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(10, 0)))

    evs = events(state_file)
    assert [e["event"] for e in evs] == ["taken", "undone"]
    undone = evs[1]
    assert undone["ref"] == taken["id"]
    assert undone["occurrence_key"] == "2026-04-21T08:00#0"
    assert undone["generation"] == 0
    out = capsys.readouterr().out
    assert "Undid" in out and "8:00am" in out and "8:14am" in out
    # generation bumps: the occurrence is unresolved again
    from attribution import generation as occurrence_generation
    assert occurrence_generation(evs, "med-001", "2026-04-21T08:00#0") == 1


def test_undo_second_time_fails_with_nothing_to_undo(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    event_store.append_events(sw.history_file(), [
        event_store.new_event("med-001", "taken", local_dt(8, 14),
                              occurrence_key="2026-04-21T08:00#0",
                              occurrence_utc=utc(local_dt(8, 0)).isoformat())])

    handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(9, 0)))
    with pytest.raises(SystemExit) as e:
        handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(9, 5)))
    assert e.value.code != 0
    assert "nothing to undo" in capsys.readouterr().out
    assert len(events(state_file)) == 2


def test_undo_older_than_24h_refused(state_file):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    event_store.append_events(sw.history_file(), [
        event_store.new_event("med-001", "taken", local_dt(8, 14) - dtmod.timedelta(days=2),
                              occurrence_key="2026-04-19T08:00#0",
                              occurrence_utc=utc(local_dt(8, 0) - dtmod.timedelta(days=2)).isoformat())])

    with pytest.raises(SystemExit) as e:
        handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(10, 0)))
    assert e.value.code != 0
    assert len(events(state_file)) == 1


def test_undo_skipped_echoes_it(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    skipped = event_store.new_event(
        "med-001", "skipped", local_dt(8, 10),
        occurrence_key="2026-04-21T08:00#0",
        occurrence_utc=utc(local_dt(8, 0)).isoformat())
    event_store.append_events(sw.history_file(), [skipped])

    handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(9, 0)))

    evs = events(state_file)
    assert evs[1]["event"] == "undone" and evs[1]["ref"] == skipped["id"]
    assert "Undid: skipped" in capsys.readouterr().out


def test_ac21_undo_before_late_re_reminds(tmp_path, monkeypatch):
    env = make_tick_env(tmp_path, monkeypatch)
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med])

    env.run(local_dt(7, 55))                 # establish the watermark
    from reply import handle_confirm
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 10)))
    handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(8, 20)))

    env.run(local_dt(8, 25))                 # before T+late → re-remind, new gen
    msgs = env.sent()
    assert len(msgs) == 1 and "Reminder" in msgs[0]
    assert env.events("send_intent")[0]["generation"] == 1


def test_ac21_undo_reopens_the_dose(tmp_path, monkeypatch):
    # #11: an undone dose is open again — nudged — until the next dose closes it
    env = make_tick_env(tmp_path, monkeypatch)
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med])

    env.run(local_dt(7, 55))
    from reply import handle_confirm
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 10)))
    handle_undo("med-001", dry_run=False, clock=FakeClock(local_dt(11, 0)))

    env.run(local_dt(11, 5))
    assert env.sent_count("Late:") == 1
    env.run(local_dt(8, 5) + dtmod.timedelta(days=1))
    assert len(env.events("missed")) == 1
    assert env.events("missed")[0]["generation"] == 1


# ── pause / unpause ────────────────────────────────────────────────────────────

def test_pause_and_unpause(state_file):
    med = make_med(med_id="med-001")
    write_state(state_file, meds=[med])

    handle_pause("med-001", dry_run=False, clock=FakeClock(local_dt(10, 0)))
    assert on_disk(state_file)["meds"][0]["paused"] is True
    assert events(state_file) == []          # no events — state-only change

    handle_unpause("med-001", dry_run=False, clock=FakeClock(local_dt(12, 0)))
    med_disk = on_disk(state_file)["meds"][0]
    assert med_disk["paused"] is False
    # unpause re-anchors tracking: nothing during the pause is enumerated
    assert parse_instant(med_disk["active_since_utc"]) == utc(local_dt(12, 0))


def test_unpause_active_since_prevents_phantom_misses(tmp_path, monkeypatch):
    env = make_tick_env(tmp_path, monkeypatch)
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    env.write(meds=[med])

    env.run(local_dt(7, 55))
    handle_pause("med-001", dry_run=False, clock=FakeClock(local_dt(7, 58)))
    env.run(local_dt(10, 30))                # the 08:00 dose passes while paused
    handle_unpause("med-001", dry_run=False, clock=FakeClock(local_dt(11, 0)))

    env.run(local_dt(11, 30))

    assert env.events("missed") == []
    assert env.sent() == []


# ── Edit-time quiet-hours rejection (AC 27) ────────────────────────────────────

def med_json(**kw):
    return json.dumps(make_med(**kw))


def test_add_med_rejects_dose_inside_quiet(state_file, capsys):
    write_state(state_file, meds=[])            # default quiet 22:00–07:00

    with pytest.raises(SystemExit) as e:
        handle_add_med(med_json(times=["23:00"]), dry_run=False,
                       clock=FakeClock(local_dt(12, 0)))
    assert e.value.code != 0
    out = capsys.readouterr().out
    assert "23:00" in out and "inside quiet hours" in out
    assert on_disk(state_file)["meds"] == []


def test_add_med_rejects_nudge_in_muted_quiet_with_fix(state_file, capsys):
    # dose 21:00 + late 90 → nudge 22:30, past the 30-min head → muted
    with_state = make_med(times=["21:00"], late_threshold=90, missed_threshold=120)
    write_state(state_file, meds=[])

    with pytest.raises(SystemExit) as e:
        handle_add_med(json.dumps(with_state), dry_run=False,
                       clock=FakeClock(local_dt(12, 0)))
    assert e.value.code != 0
    out = capsys.readouterr().out
    assert "22:30" in out and "muted" in out and "22:30" in out
    assert on_disk(state_file)["meds"] == []


def test_add_med_accepts_nudge_in_quiet_head(state_file):
    # AC 28's blessed config: dose 21:30 + late 30 → nudge at 22:00, inside
    # the first 30 min of quiet hours, where nudges still send
    write_state(state_file, meds=[])

    handle_add_med(med_json(times=["21:30"]), dry_run=False,
                   clock=FakeClock(local_dt(12, 0)))

    meds = on_disk(state_file)["meds"]
    assert len(meds) == 1 and meds[0]["schedule"]["times"] == ["21:30"]


def test_add_med_assigns_id_and_active_since(state_file):
    write_state(state_file, meds=[])

    handle_add_med(med_json(times=["08:00"]), dry_run=False,
                   clock=FakeClock(local_dt(15, 0)))

    med = on_disk(state_file)["meds"][0]
    assert med["id"] == "med-001"
    assert parse_instant(med["active_since_utc"]) == utc(local_dt(15, 0))


def test_add_med_honors_explicit_unique_id(state_file):
    existing = make_med(med_id="med-001")
    write_state(state_file, meds=[existing])

    handle_add_med(med_json(med_id="med-042", times=["08:00"]), dry_run=False,
                   clock=FakeClock(local_dt(15, 0)))

    assert [m["id"] for m in on_disk(state_file)["meds"]] == ["med-001", "med-042"]

    with pytest.raises(SystemExit):          # duplicate id refused
        handle_add_med(med_json(med_id="med-042", times=["08:00"]), dry_run=False,
                       clock=FakeClock(local_dt(15, 1)))


def test_edit_med_rejects_dose_inside_quiet(state_file):
    write_state(state_file, meds=[make_med(times=["08:00"])])

    with pytest.raises(SystemExit) as e:
        handle_edit_med("med-001", med_json(times=["23:00"]), dry_run=False,
                        clock=FakeClock(local_dt(12, 0)))
    assert e.value.code != 0
    assert on_disk(state_file)["meds"][0]["schedule"]["times"] == ["08:00"]


def test_edit_med_preserves_state_and_unknown_fields(state_file):
    med = make_med(times=["08:00"], missed_count=3)
    med["min_gap_hours"] = 6                  # optional field passes through
    med["active_since_utc"] = local_dt(6, 0).isoformat()
    write_state(state_file, meds=[med])

    handle_edit_med("med-001", json.dumps({"name": "Metformin XR",
                                           "schedule": {"frequency": "once_daily",
                                                        "times": ["09:00"]}}),
                    dry_run=False, clock=FakeClock(local_dt(10, 0)))

    med_after = on_disk(state_file)["meds"][0]
    assert med_after["name"] == "Metformin XR"
    assert med_after["schedule"]["times"] == ["09:00"]
    assert med_after["min_gap_hours"] == 6
    assert med_after["state"]["missed_count"] == 3      # runtime state kept
    # schedule changed → tracking re-anchored from the edit instant
    assert parse_instant(med_after["active_since_utc"]) == utc(local_dt(10, 0))


def test_edit_med_rename_alone_keeps_active_since(state_file):
    med = make_med(times=["08:00"])
    med["active_since_utc"] = local_dt(6, 0).isoformat()
    write_state(state_file, meds=[med])

    handle_edit_med("med-001", json.dumps({"name": "Metformin XR"}),
                    dry_run=False, clock=FakeClock(local_dt(10, 0)))

    assert parse_instant(on_disk(state_file)["meds"][0]["active_since_utc"]) \
        == utc(local_dt(6, 0))


def test_set_quiet_hours_rejects_conflict_with_existing_meds(state_file, capsys):
    write_state(state_file, meds=[make_med(times=["08:00"])])  # nudge 08:30

    with pytest.raises(SystemExit) as e:
        handle_set_quiet_hours("07:30", "09:00", dry_run=False)
    assert e.value.code != 0
    out = capsys.readouterr().out
    assert "08:00" in out and "inside quiet hours" in out
    quiet = on_disk(state_file)["global"]["quiet_hours"]
    assert quiet == {"start": "22:00", "end": "07:00"}   # unchanged


def test_set_quiet_hours_accepts_clean_window(state_file):
    write_state(state_file, meds=[make_med(times=["23:30"])])  # dose past quiet

    handle_set_quiet_hours("22:00", "23:00", dry_run=False,
                           clock=FakeClock(local_dt(12, 0)))

    assert on_disk(state_file)["global"]["quiet_hours"] == {"start": "22:00",
                                                            "end": "23:00"}


def test_set_quiet_hours_rejects_bad_format(state_file):
    write_state(state_file, meds=[])
    with pytest.raises(SystemExit) as e:
        handle_set_quiet_hours("25:00", "07:00", dry_run=False)
    assert e.value.code != 0


# ── remove / status / show-state ───────────────────────────────────────────────

def test_remove_requires_yes(state_file):
    write_state(state_file, meds=[make_med()])
    with pytest.raises(SystemExit) as e:
        handle_remove("med-001", False, dry_run=False, clock=FakeClock(local_dt(12, 0)))
    assert e.value.code != 0
    assert len(on_disk(state_file)["meds"]) == 1


def test_remove_leaves_history_lines(state_file):
    write_state(state_file, meds=[make_med()])
    taken = event_store.new_event("med-001", "taken", local_dt(8, 14),
                                  occurrence_key="2026-04-21T08:00#0",
                                  occurrence_utc=utc(local_dt(8, 0)).isoformat())
    event_store.append_events(sw.history_file(), [taken])

    handle_remove("med-001", True, dry_run=False, clock=FakeClock(local_dt(12, 0)))

    assert on_disk(state_file)["meds"] == []
    assert events(state_file) == [taken]      # history.jsonl untouched


def test_status_lists_meds(state_file, capsys):
    m1 = make_med(med_id="med-001", name="Metformin")
    m2 = make_med(med_id="med-002", name="Lisinopril", paused=True,
                  frequency="interval", interval_hours=8)
    write_state(state_file, meds=[m1, m2])
    event_store.append_events(sw.history_file(), [
        event_store.new_event("med-001", "taken", local_dt(8, 14),
                              occurrence_key="2026-04-21T08:00#0",
                              occurrence_utc=utc(local_dt(8, 0)).isoformat())])

    handle_status()

    out = capsys.readouterr().out
    assert "Metformin" in out and "8:00am" in out and "taken" in out
    assert "Lisinopril" in out and "every 8h" in out and "[paused]" in out
    before = state_file.read_text(encoding="utf-8")
    assert state_file.read_text(encoding="utf-8") == before   # read-only


def test_show_state_prints_sha256(state_file, capsys):
    write_state(state_file, meds=[make_med()])

    handle_show_state()

    sha = capsys.readouterr().out.strip()
    assert sha == hashlib.sha256(state_file.read_bytes()).hexdigest()


# ── --position resolution (issue #1 §6) ────────────────────────────────────────

def write_state_with_digest_order(sf, meds, order, date):
    state = make_state(meds=meds)
    state["global"]["last_digest_order"] = order
    state["global"]["last_digest_date"] = date
    sf.write_text(json.dumps(state), encoding="utf-8")


def test_digest_records_order_and_date(tmp_path, monkeypatch):
    env = make_tick_env(tmp_path, monkeypatch)
    m1 = make_med(med_id="med-001", name="Metformin")
    m2 = make_med(med_id="med-002", name="Lisinopril", paused=True)
    env.write(meds=[m1, m2], digest_time="08:00")

    env.run(local_dt(8, 2))                  # digest fires

    g = env.state()["global"]
    assert g["last_digest_order"] == ["med-001"]   # paused meds aren't listed
    assert g["last_digest_date"] == "2026-04-21"


def test_position_resolves_and_echoes_name(state_file, capsys):
    m1 = make_med(med_id="med-001", name="Metformin", times=["08:00"])
    m2 = make_med(med_id="med-002", name="Lisinopril", times=["21:00"])
    write_state_with_digest_order(state_file, [m1, m2],
                                  ["med-001", "med-002"], "2026-04-21")

    handle_confirm(None, None, dry_run=False, clock=FakeClock(local_dt(21, 10)),
                   position=2)

    out = capsys.readouterr().out
    assert "Position 2: Lisinopril (med-002)." in out
    taken = events(state_file)
    assert len(taken) == 1 and taken[0]["med_id"] == "med-002"
    assert taken[0]["occurrence_key"] == "2026-04-21T21:00#0"


def test_position_refuses_previous_day(state_file, capsys):
    m1 = make_med(med_id="med-001", times=["08:00"])
    write_state_with_digest_order(state_file, [m1], ["med-001"], "2026-04-20")

    with pytest.raises(SystemExit) as e:
        handle_snooze(None, 30, dry_run=False, clock=FakeClock(local_dt(8, 5)),
                      position=1)
    assert e.value.code != 0
    assert "no digest order for today" in capsys.readouterr().out
    assert events(state_file) == []


def test_position_out_of_range(state_file):
    m1 = make_med(med_id="med-001", times=["08:00"])
    write_state_with_digest_order(state_file, [m1], ["med-001"], "2026-04-21")

    with pytest.raises(SystemExit) as e:
        handle_skip(None, None, dry_run=False, clock=FakeClock(local_dt(8, 5)),
                    position=5)
    assert e.value.code != 0


def test_position_without_any_recorded_order(state_file):
    write_state(state_file, meds=[make_med(times=["08:00"])])

    with pytest.raises(SystemExit) as e:
        handle_skip(None, None, dry_run=False, clock=FakeClock(local_dt(8, 5)),
                    position=1)
    assert e.value.code != 0
