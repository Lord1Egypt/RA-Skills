"""
Reply handler tests — reply.py confirm (rewritten for issue #1 PR 2 §4)
and defer subcommands.

Confirm now goes through transact + the event store: taken events carry
the credited occurrence key/generation and taken_at_utc; duplicates exit
3 with a single-use --force nonce; ambiguity exits 4 without writing.
"""
import json
import re
from datetime import timedelta

import pytest

import dispatch
import event_store
import safe_write as sw
from clock import FakeClock, parse_instant
from occurrence import at_local
from reply import handle_confirm, handle_confirm_all, handle_defer
from tests.conftest import make_state, make_med, iso, local_dt, utc, TZ

import datetime as dtmod

TUE = dtmod.date(2026, 4, 21)
MON = dtmod.date(2026, 4, 20)


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


# ── confirm: event, legacy fields, output ─────────────────────────────────────

def test_confirm_writes_keyed_taken_event_and_legacy_fields(state_file):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])

    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 14)))

    evs = events(state_file)
    assert len(evs) == 1 and evs[0]["event"] == "taken"
    assert evs[0]["occurrence_key"] == "2026-04-21T08:00#0"
    assert evs[0]["taken_at_utc"] is not None
    st = on_disk(state_file)["meds"][0]["state"]
    assert st["status"] == "confirmed"
    assert st["confirmed_dose"] == at_local(TUE, "08:00", TZ, 0).utc.isoformat()
    nd = at_local(TUE + dtmod.timedelta(days=1), "08:00", TZ, 0).utc
    assert parse_instant(st["next_due"]) == nd
    # rollback mirror in state.history
    assert st["history"][-1]["event"] == "taken"


def test_confirm_prints_credited_dose(state_file, capsys):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(14, 30)))
    assert "Logged as your 8:00am dose." in capsys.readouterr().out


def test_ac1_midday_confirm_keeps_evening_reminder(state_file):
    # AC 1: the 20:00 occurrence stays unresolved — the tick will still remind
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(14, 30)))
    keys = [e["occurrence_key"] for e in events(state_file)]
    assert "2026-04-21T08:00#0" in keys
    assert "2026-04-21T20:00#1" not in keys


def test_confirm_unattributed_says_so(state_file, capsys):
    med = make_med(med_id="med-001", frequency="as_needed")
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(12, 0)))
    out = capsys.readouterr().out
    assert "without a schedule slot" in out
    evs = events(state_file)
    assert evs[0]["event"] == "taken" and "occurrence_key" not in evs[0]


def test_confirm_interval_credits_anchor_and_reanchors(state_file):
    med = make_med(med_id="med-001", frequency="interval", interval_hours=8,
                   next_due=local_dt(8, 0).isoformat())
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(9, 0)))
    evs = events(state_file)
    # occurrence keyed by the UTC instant 08:00 PDT = 15:00Z
    assert evs[0]["occurrence_key"] == "2026-04-21T15:00:00Z"
    st = on_disk(state_file)["meds"][0]["state"]
    assert parse_instant(st["next_due"]) == local_dt(17, 0).astimezone(dtmod.timezone.utc)


def test_confirm_interval_without_anchor_is_unattributed_but_reanchors(state_file):
    med = make_med(med_id="med-001", frequency="interval", interval_hours=8)
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(9, 0)))
    evs = events(state_file)
    assert evs[0]["event"] == "taken" and "occurrence_key" not in evs[0]
    st = on_disk(state_file)["meds"][0]["state"]
    assert parse_instant(st["next_due"]) == local_dt(17, 0).astimezone(dtmod.timezone.utc)


def test_confirm_stores_dose_taken(state_file):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    handle_confirm("med-001", "250mg", dry_run=False, clock=FakeClock(local_dt(8, 14)))
    evs = events(state_file)
    assert evs[0]["dose_taken"] == "250mg"
    assert evs[0]["dose_prescribed"] == "500mg"


def test_confirm_skips_paused_med(state_file, capsys):
    med = make_med(med_id="med-001", paused=True)
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 14)))
    assert events(state_file) == []
    assert "paused" in capsys.readouterr().out


def test_confirm_dry_run_writes_nothing(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    before = state_file.read_text(encoding="utf-8")
    handle_confirm("med-001", None, dry_run=True, clock=FakeClock(local_dt(8, 14)))
    assert state_file.read_text(encoding="utf-8") == before
    assert events(state_file) == []


# ── AC 3/4: ambiguity and --dose ──────────────────────────────────────────────

def test_ac3_ambiguous_exits_4_and_writes_nothing(state_file, capsys):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "09:30"])
    write_state(state_file, meds=[med])
    before = state_file.read_text(encoding="utf-8")
    with pytest.raises(SystemExit) as e:
        handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(8, 40)))
    assert e.value.code == 4
    assert state_file.read_text(encoding="utf-8") == before
    assert events(state_file) == []
    out = capsys.readouterr().out
    assert "8:00am" in out and "9:30am" in out


def test_ac4_dose_pin_credits_evening_dose(state_file):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])
    handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(14, 30)),
                   dose_pin="20:00")
    assert events(state_file)[0]["occurrence_key"] == "2026-04-21T20:00#1"


def test_ac4_dose_pin_rejects_unscheduled_time(state_file):
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])
    with pytest.raises(SystemExit) as e:
        handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(14, 30)),
                       dose_pin="09:00")
    assert e.value.code != 0 and e.value.code != 4
    assert events(state_file) == []


# ── AC 5: --taken-at ──────────────────────────────────────────────────────────

def test_ac5_taken_at_records_yesterday_23(state_file):
    med = make_med(med_id="med-001", frequency="once_daily", times=["23:00"])
    write_state(state_file, meds=[med])
    # wall clock says Wed 00:30; the dose was taken Tue 23:00
    handle_confirm("med-001", None, dry_run=False,
                   clock=FakeClock(local_dt(0, 30) + dtmod.timedelta(days=1)),
                   taken_at_raw="23:00")
    evs = events(state_file)
    assert evs[0]["occurrence_key"] == "2026-04-21T23:00#0"
    assert evs[0]["taken_at_utc"] == local_dt(23, 0).astimezone(dtmod.timezone.utc).isoformat()
    # attribution used taken_at, so the credited dose is yesterday's 23:00
    st = on_disk(state_file)["meds"][0]["state"]
    assert st["last_taken"] == local_dt(23, 0).astimezone(dtmod.timezone.utc).isoformat()


def test_taken_at_bad_value_exits_nonzero(state_file):
    med = make_med(med_id="med-001")
    write_state(state_file, meds=[med])
    with pytest.raises(SystemExit) as e:
        handle_confirm("med-001", None, dry_run=False, clock=FakeClock(local_dt(12, 0)),
                       taken_at_raw="25:99")
    assert e.value.code != 0


# ── AC 6: duplicate refusal, nonce, --force ───────────────────────────────────

def confirm(med_id, now, **kw):
    handle_confirm(med_id, None, dry_run=False, clock=FakeClock(now), **kw)


def test_ac6_duplicate_exits_3_with_nonce_and_no_taken_event(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    confirm("med-001", local_dt(8, 5))
    assert len(events(state_file)) == 1

    with pytest.raises(SystemExit) as e:
        confirm("med-001", local_dt(14, 0))     # 5.75h later, gap is 12h
    assert e.value.code == 3
    out = capsys.readouterr().out
    assert "Already logged" in out and "8:05am" in out
    nonce = re.search(r"--force ([0-9a-f]+)", out).group(1)
    assert len(events(state_file)) == 1, "no taken event may be written on refusal"

    # wrong nonce still refused
    with pytest.raises(SystemExit) as e:
        confirm("med-001", local_dt(14, 2), force="deadbeef")
    assert e.value.code == 3
    capsys.readouterr()

    # right nonce succeeds once…
    confirm("med-001", local_dt(14, 4), force=nonce)
    assert len(events(state_file)) == 2

    # …and cannot be replayed
    capsys.readouterr()
    with pytest.raises(SystemExit) as e:
        confirm("med-001", local_dt(14, 6), force=nonce)
    assert e.value.code == 3


def test_ac6_nonce_expires_after_10_minutes(state_file, capsys):
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    confirm("med-001", local_dt(8, 5))
    with pytest.raises(SystemExit):
        confirm("med-001", local_dt(9, 0))      # offer created at 09:00
    nonce = re.search(r"--force ([0-9a-f]+)", capsys.readouterr().out).group(1)
    with pytest.raises(SystemExit) as e:
        confirm("med-001", local_dt(9, 30), force=nonce)   # 30 min later
    assert e.value.code == 3


def test_second_dose_outside_gap_is_logged(state_file):
    # 08:00/20:00 med, gap 6h: morning at 08:14, evening at 20:30 is fine
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])
    confirm("med-001", local_dt(8, 14))
    confirm("med-001", local_dt(20, 30))
    assert len(events(state_file)) == 2


def test_early_confirm_anchors_next_due_past_covered_dose(state_file):
    # 'all taken' at 07:32 credits the 08:00 dose; next_due is 20:00,
    # not the 08:00 just covered (regression: old code re-anchored on now)
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "20:00"])
    write_state(state_file, meds=[med])
    confirm("med-001", local_dt(7, 32))
    assert events(state_file)[0]["occurrence_key"] == "2026-04-21T08:00#0"
    st = on_disk(state_file)["meds"][0]["state"]
    assert parse_instant(st["next_due"]) == local_dt(20, 0).astimezone(dtmod.timezone.utc)


# ── confirm --all ─────────────────────────────────────────────────────────────

def test_confirm_all_marks_all_scheduled(state_file):
    m1 = make_med(med_id="med-001", name="Metformin", frequency="once_daily", times=["08:00"])
    m2 = make_med(med_id="med-002", name="Lisinopril", frequency="once_daily", times=["21:00"])
    write_state(state_file, meds=[m1, m2])
    handle_confirm_all(None, dry_run=False, clock=FakeClock(local_dt(12, 0)))
    taken = [e for e in events(state_file) if e["event"] == "taken"]
    assert {e["med_id"] for e in taken} == {"med-001", "med-002"}


def test_confirm_all_skips_paused_and_as_needed(state_file, capsys):
    active = make_med(med_id="med-001", name="Metformin", frequency="once_daily", times=["08:00"])
    paused = make_med(med_id="med-002", name="Lisinopril", paused=True,
                      frequency="once_daily", times=["08:00"])
    prn = make_med(med_id="med-003", name="Ibuprofen", frequency="as_needed")
    write_state(state_file, meds=[active, paused, prn])
    handle_confirm_all(None, dry_run=False, clock=FakeClock(local_dt(12, 0)))
    ids = {e["med_id"] for e in events(state_file)}
    assert ids == {"med-001"}
    out = capsys.readouterr().out
    assert "Lisinopril" in out and "Ibuprofen" in out


def test_confirm_all_uses_6h_window_after_digest(state_file):
    # 'all taken' at 07:32 for an 11:00 dose: only the 6h window credits it
    med = make_med(med_id="med-001", frequency="once_daily", times=["11:00"])
    write_state(state_file, meds=[med])
    digest_sent = event_store.new_event("__global__", "sent", local_dt(7, 30),
                                        stage="digest", occurrence_key="digest#2026-04-21")
    event_store.append_events(sw.history_file(), [digest_sent])

    handle_confirm_all(None, dry_run=False, clock=FakeClock(local_dt(7, 32)))
    assert events(state_file)[-1]["occurrence_key"] == "2026-04-21T11:00#0"


def test_confirm_all_outside_digest_grace_uses_90min_window(state_file):
    # digest sent 3h ago — outside the 60-min grace, so the 90-min window
    # applies and the 11:00 dose is too far off; yesterday's dose is credited
    med = make_med(med_id="med-001", frequency="once_daily", times=["11:00"])
    write_state(state_file, meds=[med])
    digest_sent = event_store.new_event("__global__", "sent", local_dt(4, 30),
                                        stage="digest", occurrence_key="digest#2026-04-21")
    event_store.append_events(sw.history_file(), [digest_sent])

    handle_confirm_all(None, dry_run=False, clock=FakeClock(local_dt(7, 32)))
    assert events(state_file)[-1]["occurrence_key"] == "2026-04-20T11:00#0"


# ── defer — rewritten for PR 4: it is now a deprecated alias for snooze ────────
# (the old defer wrote the dead `deferred` status; issue #1 §6 replaces it)

def test_defer_is_snooze_alias_with_min_120_cap(state_file):
    # once-daily 08:00: next dose tomorrow → gap 24h → cap 12h → min(120, 720)=120
    med = make_med(med_id="med-001", frequency="once_daily", times=["08:00"])
    write_state(state_file, meds=[med])
    handle_defer("med-001", dry_run=False, clock=FakeClock(local_dt(8, 5)))
    evs = events(state_file)
    assert evs[0]["event"] == "snoozed"
    assert parse_instant(evs[0]["ref"]) == utc(local_dt(10, 5))   # 08:05 + 120min


def test_defer_capped_below_120_when_gap_is_tight(state_file):
    # 08:00/09:30 at 08:05: the dose closes at 09:30 → cap 84min → min(120, 84)
    med = make_med(med_id="med-001", frequency="twice_daily", times=["08:00", "09:30"])
    write_state(state_file, meds=[med])
    handle_defer("med-001", dry_run=False, clock=FakeClock(local_dt(8, 5)))
    assert parse_instant(events(state_file)[0]["ref"]) == utc(local_dt(9, 29))


def test_defer_never_writes_deferred_status(state_file):
    med = make_med(med_id="med-001", status="reminded")
    write_state(state_file, meds=[med])
    handle_defer("med-001", dry_run=False, clock=FakeClock(local_dt(8, 5)))
    st = on_disk(state_file)["meds"][0]["state"]
    assert st["status"] != "deferred"
    assert all(e["event"] != "deferred" for e in st["history"])
