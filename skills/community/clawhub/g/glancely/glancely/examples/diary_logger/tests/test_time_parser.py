"""Time parser tests — no network, no Calendar."""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import _time_parser as tp  # type: ignore


NOW = datetime(2026, 5, 3, 15, 0)


def test_explicit_range():
    r = tp.resolve_range("wrapper refactor from 2:30pm to 4:00pm", now=NOW)
    assert r.mode == "both_explicit"
    assert r.start.hour == 14 and r.start.minute == 30
    assert r.end.hour == 16 and r.end.minute == 0
    assert r.cleaned_title == "wrapper refactor"


def test_start_only_uses_now_as_end():
    r = tp.resolve_range("debugging at 2:30pm", now=NOW)
    assert r.mode == "start_only"
    assert r.start.hour == 14 and r.start.minute == 30
    assert r.end == NOW.replace(second=0, microsecond=0)
    assert r.cleaned_title == "debugging"


def test_end_only_uses_last_event_end():
    last = NOW - timedelta(minutes=30)
    r = tp.resolve_range("quick lunch till 2:50pm", now=NOW, last_event_end=last)
    assert r.mode == "end_only"
    assert r.start == last
    assert r.end.hour == 14 and r.end.minute == 50
    assert r.cleaned_title == "quick lunch"


def test_no_explicit_time_uses_last_event_end_to_now():
    last = NOW - timedelta(minutes=15)
    r = tp.resolve_range("answer messages", now=NOW, last_event_end=last)
    assert r.mode == "none_explicit"
    assert r.start == last
    assert r.end == NOW.replace(second=0, microsecond=0)
    assert r.cleaned_title == "answer messages"


def test_chinese_start_token():
    r = tp.resolve_range("下午两点半 写代码", now=NOW)
    assert r.mode == "start_only"
    assert r.start.hour == 14 and r.start.minute == 30
    assert "写代码" in r.cleaned_title


if __name__ == "__main__":
    for name in [n for n in dir() if n.startswith("test_")]:
        globals()[name]()
        print(f"ok  {name}")
