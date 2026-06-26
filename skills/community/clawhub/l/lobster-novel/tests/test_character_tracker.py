#!/usr/bin/env python3
"""Tests for CharacterTracker"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "memory"))
from character_tracker import CharacterTracker, CharacterSnapshot


def test_record_and_get():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        snap = CharacterSnapshot(chapter=1, name="张三", state="alive",
                                 location="山村", emotional_state="平静")
        ct.record(snap)
        got = ct.get_state_at("张三", 1)
        assert got is not None
        assert got.state == "alive"
        assert got.location == "山村"
        print("✅ test_record_and_get")


def test_get_history():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        ct.record(CharacterSnapshot(chapter=1, name="张三", state="alive"))
        ct.record(CharacterSnapshot(chapter=2, name="张三", state="injured"))
        hist = ct.get_history("张三")
        assert len(hist) == 2
        assert hist[1].state == "injured"
        print("✅ test_get_history")


def test_state_transition():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        ct.record(CharacterSnapshot(chapter=1, name="李四", state="alive"))
        ct.record(CharacterSnapshot(chapter=3, name="李四", state="captured"))
        trans = ct.get_state_transition("李四")
        assert len(trans) == 1
        assert trans[0] == (1, "alive", 3, "captured")
        print("✅ test_state_transition")


def test_active_characters():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        ct.record(CharacterSnapshot(chapter=1, name="张三", state="alive"))
        ct.record(CharacterSnapshot(chapter=1, name="李四", state="alive"))
        ct.record(CharacterSnapshot(chapter=2, name="张三", state="alive"))
        active = ct.get_active_characters(1)
        assert "张三" in active
        assert "李四" in active
        assert len(active) == 2
        print("✅ test_active_characters")


def test_get_state_before():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        ct.record(CharacterSnapshot(chapter=2, name="张三", state="injured"))
        # No state at ch1, so should be None
        got = ct.get_state_at("张三", 1)
        assert got is None
        # Should find at ch3 (closest <=)
        got2 = ct.get_state_at("张三", 3)
        assert got2 is not None
        assert got2.state == "injured"
        print("✅ test_get_state_before")


def test_summary():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        ct.record(CharacterSnapshot(chapter=1, name="张三", state="alive",
                                    location="森林"))
        s = ct.summary(1)
        assert "张三" in s
        assert "森林" in s
        print("✅ test_summary")


def test_save_reload():
    with tempfile.TemporaryDirectory() as td:
        ct = CharacterTracker(Path(td))
        ct.record(CharacterSnapshot(chapter=1, name="王五", state="alive"))
        ct2 = CharacterTracker(Path(td))
        assert len(ct2.timeline) == 1
        assert ct2.timeline[0].name == "王五"
        print("✅ test_save_reload")


if __name__ == "__main__":
    test_record_and_get()
    test_get_history()
    test_state_transition()
    test_active_characters()
    test_get_state_before()
    test_summary()
    test_save_reload()
    print("\n🎉 All character tracker tests passed!")
