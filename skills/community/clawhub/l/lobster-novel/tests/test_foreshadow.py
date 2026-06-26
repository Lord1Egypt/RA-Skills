#!/usr/bin/env python3
"""Tests for ForeshadowTracker"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "memory"))
from foreshadowing import ForeshadowTracker, Hook


def test_plant():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        h = ft.plant("神秘人的真实身份", chapter=1, payoff_chapter=10)
        assert h.id == "hook-1"
        assert h.status == "active"
        assert len(ft.hooks) == 1
        print("✅ test_plant")


def test_resolve():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("玉佩的秘密", 1, 8)
        ft.resolve("hook-1", 8)
        assert ft.hooks[0].status == "resolved"
        assert ft.hooks[0].resolved_chapter == 8
        print("✅ test_resolve")


def test_resolve_by_desc():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("爷爷留下的玉佩", 1, 8)
        ft.resolve_by_desc("玉佩", 8)
        assert ft.hooks[0].status == "resolved"
        print("✅ test_resolve_by_desc")


def test_abandon():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("废弃支线", 1, 5)
        ft.abandon("hook-1")
        assert ft.hooks[0].status == "abandoned"
        print("✅ test_abandon")


def test_get_active():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("钩子A", 1, 5)
        ft.plant("钩子B", 2, 10)
        active = ft.get_active(4)
        assert len(active) == 2
        print("✅ test_get_active")


def test_get_overdue():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("正常伏笔", 1, 10)   # due ch10, not overdue
        ft.plant("过期伏笔", 1, 3)    # due ch3, overdue by 5 at ch8
        overdue = ft.get_overdue(8, threshold=3)
        assert len(overdue) == 1, f"Expected 1, got {len(overdue)}"
        assert overdue[0].description == "过期伏笔"
        print("✅ test_get_overdue")


def test_summary():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("伏笔", 1, 5)
        s = ft.summary(3)
        assert "active" in s
        print("✅ test_summary")


def test_save_reload():
    with tempfile.TemporaryDirectory() as td:
        ft = ForeshadowTracker(Path(td))
        ft.plant("持久化测试", 1, 10)
        ft2 = ForeshadowTracker(Path(td))
        assert len(ft2.hooks) == 1
        assert ft2.hooks[0].description == "持久化测试"
        print("✅ test_save_reload")


if __name__ == "__main__":
    test_plant()
    test_resolve()
    test_resolve_by_desc()
    test_abandon()
    test_get_active()
    test_get_overdue()
    test_summary()
    test_save_reload()
    print("\n🎉 All foreshadow tests passed!")
