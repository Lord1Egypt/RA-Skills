#!/usr/bin/env python3
"""Tests for BibleManager"""
import sys, json, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
from bible import BibleManager, Character, ChapterSpec, Arc, WorldRule


def test_init_creates_bible():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        assert mgr.bible is not None
        assert mgr.bible.title == ""
        print("✅ test_init_creates_bible")


def test_set_meta():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        mgr.set_meta(title="Test Novel", genre="Fantasy", tone="Dark")
        assert mgr.bible.title == "Test Novel"
        assert mgr.bible.genre == "Fantasy"
        assert mgr.bible.tone == "Dark"
        print("✅ test_set_meta")


def test_add_character():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        c = Character(name="张三", role="protagonist", age=25,
                      traits=["brave", "curious"],
                      background="出身山村", motivation="寻找真相")
        mgr.add_character(c)
        assert mgr.bible.characters["张三"].name == "张三"
        assert mgr.get_character("张三").motivation == "寻找真相"
        print("✅ test_add_character")


def test_character_state_update():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        mgr.add_character(Character(name="李四", role="supporting"))
        mgr.update_character_state("李四", "injured")
        assert mgr.get_character("李四").current_state == "injured"
        print("✅ test_character_state_update")


def test_add_chapter():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        spec = ChapterSpec(number=1, title="开端", summary="故事开始")
        mgr.add_chapter(spec)
        assert mgr.get_chapter(1).title == "开端"
        assert mgr.bible.current_chapter == 1
        print("✅ test_add_chapter")


def test_arc():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        arc = Arc(number=1, name="觉醒篇", chapters=[1, 2, 3])
        mgr.add_arc(arc)
        assert len(mgr.bible.arcs) == 1
        assert mgr.bible.arcs[0].name == "觉醒篇"
        print("✅ test_arc")


def test_world_rule():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        rule = WorldRule(name="灵力等级", description="天地玄黄四级",
                         category="magic")
        mgr.add_rule(rule)
        assert len(mgr.bible.world_rules) == 1
        print("✅ test_world_rule")


def test_hooks():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        mgr.plant_hook(1, "神秘人出现", 5)
        mgr.plant_hook(2, "玉佩的秘密", 8)
        assert len(mgr.bible.unresolved_hooks) == 2
        assert mgr.bible.unresolved_hooks[0]["status"] == "unresolved"

        # payoff
        mgr.payoff_hook(5, "神秘人出现")
        resolved = [h for h in mgr.bible.unresolved_hooks
                    if h["description"] == "神秘人出现" and h["status"] == "resolved"]
        assert len(resolved) == 1
        print("✅ test_hooks")


def test_overdue_hooks():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        mgr.plant_hook(1, "伏笔A", 3)  # due ch3
        mgr.bible.current_chapter = 8  # past by 5
        overdue = mgr.check_hooks()
        assert len(overdue) == 1
        assert "overdue" in overdue[0]
        print("✅ test_overdue_hooks")


def test_save_and_reload():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        mgr.set_meta(title="Persist Test")
        mgr.add_character(Character(name="Alice", role="protagonist"))
        # New manager loading same file
        mgr2 = BibleManager(Path(td))
        assert mgr2.bible.title == "Persist Test"
        assert mgr2.get_character("Alice") is not None
        print("✅ test_save_and_reload")


def test_get_summary():
    with tempfile.TemporaryDirectory() as td:
        mgr = BibleManager(Path(td))
        mgr.set_meta(title="Summary Test", genre="SciFi")
        summary = mgr.get_summary()
        assert "Summary Test" in summary
        assert "SciFi" in summary
        print("✅ test_get_summary")


if __name__ == "__main__":
    test_init_creates_bible()
    test_set_meta()
    test_add_character()
    test_character_state_update()
    test_add_chapter()
    test_arc()
    test_world_rule()
    test_hooks()
    test_overdue_hooks()
    test_save_and_reload()
    test_get_summary()
    print("\n🎉 All bible tests passed!")
