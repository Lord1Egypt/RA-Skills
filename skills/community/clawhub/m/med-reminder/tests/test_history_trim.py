"""
Cases 16-17: history retention.

Updated for issue #1 PR 1: state.history is no longer trimmed at 30 —
history.jsonl is the source of truth and the 30-entry cap lives only in the
rollback mirror (event_store.MIRROR_MAX). Full history is retained.
"""
from tests.conftest import make_med
from dispatch import append_history


def _make_history(n):
    """Build n dummy history entries with guaranteed-unique timestamps."""
    from datetime import datetime, timedelta, timezone
    base = datetime(2026, 1, 1, 8, 0, 0, tzinfo=timezone.utc)
    return [
        {
            "timestamp": (base + timedelta(days=i)).isoformat(),
            "event": "taken",
            "dose_prescribed": "500mg",
            "dose_taken": None,
        }
        for i in range(n)
    ]


# ── Case 16: 29 entries → append → 30 ────────────────────────────────────────

def test_case_16_29_entries_append_reaches_30():
    med = make_med(history=_make_history(29))
    assert len(med["state"]["history"]) == 29

    append_history(med, "taken")

    assert len(med["state"]["history"]) == 30


# ── Case 17: 30 entries → append → 31, oldest retained (no trim) ──────────────

def test_case_17_30_entries_append_retains_oldest():
    entries = _make_history(30)
    oldest_ts = entries[0]["timestamp"]
    med = make_med(history=entries)
    assert len(med["state"]["history"]) == 30

    append_history(med, "missed")

    hist = med["state"]["history"]
    assert len(hist) == 31, f"Expected 31 entries (no trim), got {len(hist)}"
    timestamps = [e["timestamp"] for e in hist]
    assert oldest_ts in timestamps, "Oldest entry must be retained — full history is kept"
    assert hist[-1]["event"] == "missed", "New entry should be last"


# ── Extra: dose_prescribed is formatted correctly ─────────────────────────────

def test_append_history_formats_dose_prescribed():
    med = make_med(dose="500", unit="mg")
    append_history(med, "taken")
    assert med["state"]["history"][-1]["dose_prescribed"] == "500mg"


def test_append_history_dose_taken_stored():
    med = make_med(dose="500", unit="mg")
    append_history(med, "taken", dose_taken="250mg")
    assert med["state"]["history"][-1]["dose_taken"] == "250mg"


def test_append_history_notes_stored():
    med = make_med()
    append_history(med, "taken", notes="felt nauseous")
    assert med["state"]["history"][-1]["notes"] == "felt nauseous"


def test_append_history_no_notes_key_when_empty():
    """Notes key should be absent when notes is empty string."""
    med = make_med()
    append_history(med, "taken", notes="")
    assert "notes" not in med["state"]["history"][-1]
