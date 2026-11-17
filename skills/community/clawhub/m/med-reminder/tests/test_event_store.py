"""
event_store.py — history.jsonl primitives (issue #1 PR 1, testing-plan row 1).

Append (fsync, no duplicate ids), load (dedupe by id, torn last line
skipped and logged), and per-(occurrence, generation) precedence.
"""
import json
import logging
from datetime import datetime, timedelta, timezone

import pytest

from event_store import VALID_STAGES, append_events, load_events, new_event, outcome

UTC = timezone.utc
TS = datetime(2026, 4, 21, 15, 0, tzinfo=UTC)


def ev(med_id="med-001", event="taken", **kw):
    return new_event(med_id, event, TS, **kw)


# ── new_event ─────────────────────────────────────────────────────────────────

def test_new_event_basic_fields():
    e = ev()
    assert set(e) == {"id", "ts_utc", "med_id", "event"}
    assert e["ts_utc"] == "2026-04-21T15:00:00+00:00"
    assert e["id"]                     # uuid4 by default


def test_new_event_occurrence_fills_key_and_utc():
    from occurrence import at_local
    from tests.conftest import TZ
    import datetime as dtmod
    occ = at_local(dtmod.date(2026, 4, 21), "08:00", TZ, index=0)
    e = ev(occurrence=occ, generation=2, dose_prescribed="500mg")
    assert e["occurrence_key"] == "2026-04-21T08:00#0"
    assert e["occurrence_utc"] == "2026-04-21T15:00:00+00:00"
    assert e["generation"] == 2
    assert e["dose_prescribed"] == "500mg"


def test_new_event_rejects_unknown_event_and_stage():
    with pytest.raises(ValueError, match="unknown event"):
        ev(event="deferred")           # legacy name — never written to the store
    with pytest.raises(ValueError, match="unknown stage"):
        ev(event="sent", stage="party")
    assert "nudge" in VALID_STAGES


def test_new_event_rejects_unknown_field():
    with pytest.raises(TypeError, match="unknown event fields"):
        ev(wat=1)


# ── append + load roundtrip ───────────────────────────────────────────────────

def test_append_then_load_roundtrip(tmp_path):
    path = tmp_path / "history.jsonl"
    events = [ev(event="taken"), ev(event="missed"), ev(med_id="med-002", event="skipped")]
    appended = append_events(path, events)
    assert appended == events
    assert load_events(path) == events


def test_append_writes_jsonl_and_fsyncs(tmp_path, monkeypatch):
    path = tmp_path / "history.jsonl"
    fsynced = []
    monkeypatch.setattr("event_store.os.fsync", lambda fd: fsynced.append(fd))
    append_events(path, [ev()])
    raw = path.read_text(encoding="utf-8")
    assert raw.endswith("\n") and raw.count("\n") == 1
    assert json.loads(raw.strip())["event"] == "taken"
    assert fsynced, "append must fsync"


def test_append_skips_ids_already_stored(tmp_path):
    path = tmp_path / "history.jsonl"
    e1, e2 = ev(), ev(event="missed")
    assert append_events(path, [e1, e2]) == [e1, e2]
    # forced retry of the same batch → nothing new written, no duplicate lines
    assert append_events(path, [e1, e2]) == []
    assert len(path.read_text().strip().split("\n")) == 2


def test_append_dedupes_within_batch(tmp_path):
    path = tmp_path / "history.jsonl"
    e = ev()
    assert append_events(path, [e, dict(e)]) == [e]
    assert load_events(path) == [e]


# ── load: dedupe by id, torn tail, corruption ─────────────────────────────────

def test_load_dedupes_by_id(tmp_path):
    path = tmp_path / "history.jsonl"
    e = ev()
    other = ev(event="missed")
    path.write_text(json.dumps(e) + "\n" + json.dumps(other) + "\n" + json.dumps(e) + "\n",
                    encoding="utf-8")
    assert load_events(path) == [e, other]


def test_load_skips_torn_last_line_and_logs(tmp_path, caplog):
    path = tmp_path / "history.jsonl"
    e = ev()
    path.write_text(json.dumps(e) + "\n" + json.dumps(e)[:20], encoding="utf-8")  # cut mid-line
    with caplog.at_level(logging.WARNING, logger="event_store"):
        loaded = load_events(path)
    assert loaded == [e]
    assert any("torn last line" in r.message for r in caplog.records)


def test_load_raises_on_corrupt_line_before_last(tmp_path):
    path = tmp_path / "history.jsonl"
    path.write_text("{oops\n" + json.dumps(ev()) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="corrupt at line 1"):
        load_events(path)


def test_load_missing_file_returns_empty(tmp_path):
    assert load_events(tmp_path / "nope.jsonl") == []


# ── precedence per (occurrence, generation) ───────────────────────────────────

def key(n):  # occurrence keys need not be real to resolve precedence
    return f"2026-04-21T08:00#{n}"


def test_late_taken_overrides_earlier_missed(tmp_path):
    path = tmp_path / "history.jsonl"
    later = datetime(2026, 4, 21, 16, 30, tzinfo=UTC)
    miss = new_event("med-001", "missed", TS, occurrence_key=key(0))
    take = new_event("med-001", "taken", later, occurrence_key=key(0))
    append_events(path, [miss, take])
    assert outcome(load_events(path), key(0)) == "taken"


def test_skipped_beats_missed(tmp_path):
    miss = new_event("med-001", "missed", TS, occurrence_key=key(0))
    skip = new_event("med-001", "skipped", TS + timedelta(minutes=5), occurrence_key=key(0))
    assert outcome([miss, skip], key(0)) == "skipped"


def test_outcome_scoped_by_generation():
    k = key(0)
    miss_gen0 = new_event("med-001", "missed", TS, occurrence_key=k, generation=0)
    take_gen1 = new_event("med-001", "taken", TS + timedelta(hours=1), occurrence_key=k, generation=1)
    events = [miss_gen0, take_gen1]
    assert outcome(events, k, generation=0) == "missed"
    assert outcome(events, k, generation=1) == "taken"


def test_outcome_none_when_unresolved():
    assert outcome([], key(0)) is None
    nudge = new_event("med-001", "sent", TS, occurrence_key=key(0), stage="nudge")
    assert outcome([nudge], key(0)) is None   # sends are not terminal outcomes


# ── keyed migration (issue #1 §1) ─────────────────────────────────────────────

from clock import FakeClock
from event_store import MIRROR_MAX, migrate_state, mirror_entry
from tests.conftest import make_med, make_state, local_dt, iso

NOW = local_dt(10, 0).astimezone(UTC)   # Tue 2026-04-21 10:00 PDT


def hist_entry(event, at, dose_prescribed="500mg"):
    return {"timestamp": iso(at), "event": event, "dose_prescribed": dose_prescribed}


def test_migrate_converts_each_legacy_event_kind():
    med = make_med(history=[
        hist_entry("taken", local_dt(8, 14)),
        hist_entry("late_nudge_sent", local_dt(8, 30)),
        hist_entry("deferred", local_dt(8, 40)),
        hist_entry("missed", local_dt(9, 30)),
    ])
    new_state, events = migrate_state(make_state(meds=[med]), NOW)
    by = {(e["event"], e.get("stage")): e for e in events}
    assert set(by) == {("taken", None), ("sent", "nudge"), ("skipped", None), ("missed", None)}
    # all four referred to the 08:00 dose (most recent past / covered occurrence)
    for e in events:
        assert e["occurrence_key"] == "2026-04-21T08:00#0"
    assert all(e["dose_prescribed"] == "500mg" for e in events)


def test_migrate_keys_last_taken_from_confirmed_dose():
    med = make_med(
        history=[hist_entry("taken", local_dt(8, 14))],
        confirmed_dose=iso(local_dt(8, 0)),
    )
    _, events = migrate_state(make_state(meds=[med]), NOW)
    assert events[0]["occurrence_key"] == "2026-04-21T08:00#0"
    assert events[0]["occurrence_utc"] == local_dt(8, 0).astimezone(UTC).isoformat()


def test_migrate_early_taken_uses_covered_occurrence():
    # taken at 07:32 (before the 08:00 dose) keys to the 08:00 it credited
    med = make_med(frequency="twice_daily", times=["08:00", "20:00"],
                   history=[hist_entry("taken", local_dt(7, 32))])
    _, events = migrate_state(make_state(meds=[med]), NOW)
    assert events[0]["occurrence_key"] == "2026-04-21T08:00#0"


def test_migrate_anchors_confirmed_dose_without_taken_entry():
    med = make_med(history=[], status="confirmed",
                   confirmed_dose=iso(local_dt(8, 0)))
    _, events = migrate_state(make_state(meds=[med]), NOW)
    assert [e["event"] for e in events] == ["taken"]
    assert events[0]["occurrence_key"] == "2026-04-21T08:00#0"


def test_migrate_interval_med_keys_by_utc_instant():
    med = make_med(frequency="interval", interval_hours=8,
                   history=[hist_entry("taken", local_dt(8, 14))])
    _, events = migrate_state(make_state(meds=[med]), NOW)
    assert events[0]["occurrence_key"] == "2026-04-21T15:14:00Z"


def test_migrate_sets_watermark_to_migration_instant():
    med = make_med(history=[hist_entry("taken", local_dt(8, 14))])
    state = make_state(meds=[med])
    new_state, _ = migrate_state(state, NOW)
    assert new_state["tick"]["watermark_utc"] == NOW.isoformat()
    assert "tick" not in state            # input not mutated


def test_migrate_is_idempotent():
    med = make_med(history=[hist_entry("taken", local_dt(8, 14))],
                   confirmed_dose=iso(local_dt(8, 0)))
    state = make_state(meds=[med])
    s1, e1 = migrate_state(state, NOW)
    s2, e2 = migrate_state(s1, NOW + timedelta(hours=1))
    assert e2 == []                        # watermark set → nothing re-derived
    assert s2["tick"]["watermark_utc"] == NOW.isoformat()


def test_migrate_deterministic_ids_survive_forced_retry(tmp_path):
    med = make_med(history=[hist_entry("taken", local_dt(8, 14))])
    state = make_state(meds=[med])
    path = tmp_path / "history.jsonl"
    _, e1 = migrate_state(state, NOW)
    _, e2 = migrate_state(state, NOW)      # crash before state write → re-run
    append_events(path, e1)
    append_events(path, e2)                # same ids → nothing appended
    assert len(load_events(path)) == len(e1)


def test_migrate_empty_history_no_events_but_watermark_set():
    state = make_state(meds=[])
    new_state, events = migrate_state(state, NOW)
    assert events == []
    assert new_state["tick"]["watermark_utc"] == NOW.isoformat()


# ── mirror_entry: legacy state.history mirror ─────────────────────────────────

def test_mirror_entry_maps_representable_events():
    assert mirror_entry({"event": "taken", "ts_utc": "2026-04-21T15:00:00+00:00",
                         "dose_prescribed": "500mg"}) == {
        "timestamp": "2026-04-21T15:00:00+00:00",
        "event": "taken", "dose_prescribed": "500mg"}
    nudged = mirror_entry({"event": "sent", "stage": "nudge",
                           "ts_utc": "2026-04-21T15:30:00+00:00",
                           "dose_prescribed": "500mg"})
    assert nudged["event"] == "late_nudge_sent"


def test_mirror_entry_skips_unrepresentable_events():
    for ev in ("skipped", "undone", "snoozed", "send_intent", "send_failed", "clock_anomaly"):
        assert mirror_entry({"event": ev}) is None
    # a plain send (e.g. stage=reminder) has no legacy history name either
    assert mirror_entry({"event": "sent", "stage": "reminder"}) is None
    assert MIRROR_MAX == 30
