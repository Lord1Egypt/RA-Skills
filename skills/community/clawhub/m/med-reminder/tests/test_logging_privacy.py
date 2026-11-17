"""
Logging + privacy tests (issue #1 §7, AC 36).

Timestamps: each module installs per-handler Formatters whose converter is
gmtime, so the trailing Z is true UTC. Time is frozen by patching
time.time / time.time_ns (logging reads record.created from them) rather
than the injectable Clock, because the logging module has no Clock hook. The class-wide
logging.Formatter.converter global is never mutated.

Redaction: MEDS_LOG_REDACT=1 or global.log_redact replaces med names with
med ids in every rendered record — including sender stderr that reaches a
log.warning through dispatch.send_once.
"""
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

import dispatch
import safe_write
from dispatch import setup_logging as dispatch_logging
from reply import setup_logging as reply_logging
from tests.conftest import make_med, make_state

# 2026-10-18T02:30:00Z — on this machine's local tz (Pacific) that renders
# as 2026-10-17T19:30, so gmtime vs localtime is distinguishable in the log.
FROZEN = datetime(2026, 10, 18, 2, 30, tzinfo=timezone.utc).timestamp()


@pytest.fixture
def fresh_root():
    """
    A root logger whose handlers we control. pytest attaches its own
    capture handler for the call phase (after fixture setup), which would
    make basicConfig a no-op — so tests clear `fresh_root.handlers` again
    right before configuring. Handlers are closed on teardown so Windows
    lets tmp_path unlink the log files.
    """
    root = logging.getLogger()
    saved = root.handlers[:]
    root.handlers.clear()
    yield root
    for h in root.handlers[:]:
        root.removeHandler(h)
        h.close()
    root.handlers.extend(saved)


def write_state(tmp_path, meds=None, log_redact=None):
    state = make_state(meds=meds if meds is not None else [])
    if log_redact is not None:
        state["global"]["log_redact"] = log_redact
    sf = tmp_path / "meds-state.json"
    sf.write_text(json.dumps(state), encoding="utf-8")
    return sf


# ── true-UTC timestamps under a frozen clock (AC 36) ──────────────────────────

def test_dispatch_timestamps_are_utc(tmp_path, fresh_root, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: FROZEN)
    monkeypatch.setattr(time, "time_ns", lambda: int(FROZEN * 1_000_000_000))
    monkeypatch.setattr(safe_write, "STATE_FILE", tmp_path / "absent.json")
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch_logging(False)
    logging.getLogger("dispatch").warning("utc check")
    assert logfile.read_text(encoding="utf-8").split(" ", 1)[0] == "2026-10-18T02:30:00Z"


def test_reply_timestamps_are_utc(tmp_path, fresh_root, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: FROZEN)
    monkeypatch.setattr(time, "time_ns", lambda: int(FROZEN * 1_000_000_000))
    monkeypatch.setattr(safe_write, "STATE_FILE", tmp_path / "absent.json")
    logfile = tmp_path / "reply.log"
    monkeypatch.setenv("MEDS_LOG_FILE", str(logfile))
    fresh_root.handlers.clear()
    reply_logging(False)
    logging.getLogger("reply").warning("utc check")
    assert logfile.read_text(encoding="utf-8").split(" ", 1)[0] == "2026-10-18T02:30:00Z"


def test_safe_write_timestamps_are_utc(tmp_path, fresh_root, monkeypatch):
    monkeypatch.setattr(time, "time", lambda: FROZEN)
    monkeypatch.setattr(time, "time_ns", lambda: int(FROZEN * 1_000_000_000))
    logfile = tmp_path / "sw.log"
    fresh_root.handlers.clear()
    safe_write.configure_root_logging("safe_write", logfile, logging.INFO)
    logging.getLogger("safe_write").warning("utc check")
    assert logfile.read_text(encoding="utf-8").split(" ", 1)[0] == "2026-10-18T02:30:00Z"


def test_classwide_converter_untouched(tmp_path, fresh_root):
    # The class-wide global stays localtime; only our handler instances gmtime.
    fresh_root.handlers.clear()
    safe_write.configure_root_logging("dispatch", tmp_path / "d.log", logging.INFO)
    assert logging.Formatter.converter is time.localtime
    fmts = [h.formatter for h in fresh_root.handlers]
    assert fmts and all(f.converter is time.gmtime for f in fmts)


# ── redaction (AC 36) ──────────────────────────────────────────────────────────

def test_env_redaction_replaces_names(tmp_path, fresh_root, monkeypatch):
    monkeypatch.setattr(safe_write, "STATE_FILE",
                        write_state(tmp_path, meds=[make_med(name="Metformin")]))
    monkeypatch.setenv("MEDS_LOG_REDACT", "1")
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch_logging(False)
    logging.getLogger("dispatch").warning("Send failed (exit 1): Metformin says no")
    text = logfile.read_text(encoding="utf-8")
    assert "Metformin" not in text
    assert "med-001" in text


def test_state_flag_redaction(tmp_path, fresh_root, monkeypatch):
    monkeypatch.delenv("MEDS_LOG_REDACT", raising=False)
    monkeypatch.setattr(
        safe_write, "STATE_FILE",
        write_state(tmp_path, meds=[make_med(name="Metformin")], log_redact=True))
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch_logging(False)
    logging.getLogger("dispatch").warning("nudge for Metformin muted (quiet hours)")
    text = logfile.read_text(encoding="utf-8")
    assert "Metformin" not in text and "med-001" in text


def test_no_redaction_by_default(tmp_path, fresh_root, monkeypatch):
    monkeypatch.delenv("MEDS_LOG_REDACT", raising=False)
    monkeypatch.setattr(
        safe_write, "STATE_FILE",
        write_state(tmp_path, meds=[make_med(name="Metformin")], log_redact=False))
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch_logging(False)
    logging.getLogger("dispatch").warning("Send failed (exit 1): Metformin says no")
    assert "Metformin" in logfile.read_text(encoding="utf-8")


def test_redaction_covers_every_med_name(tmp_path, fresh_root, monkeypatch):
    monkeypatch.setattr(
        safe_write, "STATE_FILE",
        write_state(tmp_path, meds=[make_med(med_id="med-001", name="Metformin"),
                                    make_med(med_id="med-002", name="Lisinopril")]))
    monkeypatch.setenv("MEDS_LOG_REDACT", "1")
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch_logging(False)
    logging.getLogger("dispatch").warning("Metformin + Lisinopril interact?")
    text = logfile.read_text(encoding="utf-8")
    assert "Metformin" not in text and "Lisinopril" not in text
    assert "med-001" in text and "med-002" in text


def test_sender_stderr_redacted(tmp_path, fresh_root, monkeypatch):
    """
    AC 36's hard case: a failing sender whose stderr names the med. The
    stderr reaches a log.warning verbatim — the handler filter must
    redact it before the record hits the file.
    """
    monkeypatch.setattr(safe_write, "STATE_FILE",
                        write_state(tmp_path, meds=[make_med(name="Metformin")]))
    monkeypatch.setenv("MEDS_LOG_REDACT", "1")
    logfile = tmp_path / "dispatch.log"
    monkeypatch.setattr(dispatch, "LOG_FILE", logfile)
    fresh_root.handlers.clear()
    dispatch_logging(False)

    sender = f'"{sys.executable}" -c "import sys; ' \
             f"sys.stderr.write('Metformin sender blew up'); sys.exit(1)\""
    monkeypatch.setattr(dispatch, "SEND_CMD", sender)

    ok, err = dispatch.send_once("reminder text")
    assert not ok and "Metformin sender blew up" in err   # the return value is unredacted
    text = logfile.read_text(encoding="utf-8")
    assert "Metformin" not in text
    assert "med-001 sender blew up" in text
