#!/usr/bin/env python3
"""Tests for PlotTracker"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "memory"))
from plot_tracker import PlotTracker, PlotEvent, ArcProgress


def test_add_event():
    with tempfile.TemporaryDirectory() as td:
        pt = PlotTracker(Path(td))
        ev = PlotEvent(chapter=1, event_type="inciting_incident",
                       description="神秘人出现", arc="Arc 1")
        pt.add_event(ev)
        events = pt.get_events_for_chapter(1)
        assert len(events) == 1
        assert events[0].description == "神秘人出现"
        print("✅ test_add_event")


def test_add_and_update_arc():
    with tempfile.TemporaryDirectory() as td:
        pt = PlotTracker(Path(td))
        ap = ArcProgress(arc_name="觉醒篇", arc_number=1,
                         start_chapter=1, target_end_chapter=10)
        pt.add_arc(ap)
        assert len(pt.arcs) == 1
        pt.update_arc(1, status="climax")
        assert pt.arcs[0].status == "climax"
        print("✅ test_add_and_update_arc")


def test_get_pacing_profile():
    with tempfile.TemporaryDirectory() as td:
        pt = PlotTracker(Path(td))
        for ch in range(1, 4):
            pt.add_event(PlotEvent(chapter=ch, event_type="action",
                                   description=f"事件{ch}", pacing="fast"))
        profile = pt.get_pacing_profile(3, window=3)
        assert profile == "fast"
        print("✅ test_get_pacing_profile")


def test_get_tension_trend():
    with tempfile.TemporaryDirectory() as td:
        pt = PlotTracker(Path(td))
        pt.add_event(PlotEvent(chapter=1, event_type="build",
                               description="紧张氛围", pacing="intense"))
        pt.add_event(PlotEvent(chapter=2, event_type="build",
                               description="冲突升级", pacing="intense"))
        pt.add_event(PlotEvent(chapter=3, event_type="build",
                               description="高潮前奏", pacing="intense"))
        trend = pt.get_tension_trend(3)
        assert trend == "rising", f"Expected rising, got {trend}"
        print("✅ test_get_tension_trend")


def test_arc_status_summary():
    with tempfile.TemporaryDirectory() as td:
        pt = PlotTracker(Path(td))
        pt.add_arc(ArcProgress(arc_name="Test", arc_number=1,
                               start_chapter=1, target_end_chapter=5,
                               current_chapter=2))
        s = pt.arc_status_summary()
        assert "Test" in s
        assert "1" in s
        print("✅ test_arc_status_summary")


def test_empty():
    with tempfile.TemporaryDirectory() as td:
        pt = PlotTracker(Path(td))
        assert len(pt.events) == 0
        events = pt.get_events_for_chapter(1)
        assert len(events) == 0
        print("✅ test_empty")


if __name__ == "__main__":
    test_add_event()
    test_add_and_update_arc()
    test_get_pacing_profile()
    test_get_tension_trend()
    test_arc_status_summary()
    test_empty()
    print("\n🎉 All plot tracker tests passed!")
