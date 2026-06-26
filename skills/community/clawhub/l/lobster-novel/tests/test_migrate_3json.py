#!/usr/bin/env python3
"""Tests for migrate_3json.py — 3JSON → story-state.json migration."""
import sys, json, tempfile, os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from migrate_3json import (
    migrate_project, check_project,
    _parse_chapter_num, _clean_title, _name_to_id,
    _normalize_characters, _normalize_chapters, _normalize_hooks,
)


def test_parse_chapter_num():
    assert _parse_chapter_num(1) == 1
    assert _parse_chapter_num("Ch001") == 1
    assert _parse_chapter_num("v10ch001") == 1
    assert _parse_chapter_num("V5Ch001") == 1
    assert _parse_chapter_num("ch20") == 20
    assert _parse_chapter_num("") == 0
    assert _parse_chapter_num("abc") == 0
    print("✅ test_parse_chapter_num")


def test_clean_title():
    assert _clean_title("第1章 测试") == "第1章 测试"
    assert _clean_title("[V5Ch001] 标题") == "标题"
    assert _clean_title("V5Ch001 标题") == "标题"
    print("✅ test_clean_title")


def test_name_to_id():
    assert _name_to_id("理查德·泰森") == "char_理查德_泰森"
    assert _name_to_id("梅丽安") == "char_梅丽安"
    print("✅ test_name_to_id")


def test_normalize_characters_v10():
    """V10 format: {characters: {name: {...}}, carry_over: {...}}"""
    raw = {
        "characters": {
            "林风": {
                "role": "主角",
                "first_appearance": "v10ch001",
                "last_appearance": "v10ch020",
                "status": "active",
                "state": "寻找星辰碎片",
                "key_items": ["星辰剑"],
            }
        }
    }
    result = _normalize_characters(raw, "dict_v10")
    assert "char_林风" in result
    assert result["char_林风"]["first_appearance"] == 1
    assert result["char_林风"]["last_appearance"] == 20
    assert "星辰剑" in result["char_林风"]["key_items"]
    print("✅ test_normalize_characters_v10")


def test_normalize_characters_v5():
    """V5 format: {name: {...}}"""
    raw = {
        "林风": {
            "role": "配角",
            "first_appearance": "ch001",
            "last_appearance": "ch030",
        }
    }
    result = _normalize_characters(raw, "dict_v5")
    assert "char_林风" in result
    assert result["char_林风"]["first_appearance"] == 1
    print("✅ test_normalize_characters_v5")


def test_normalize_chapters_list_v5():
    """list_v5: [{chapter, title, characters, key_events}]"""
    raw = [
        {"chapter": 1, "title": "开始", "characters": ["林风"], "key_events": ["出发"]},
        {"chapter": 2, "title": "路上", "characters": ["林风", "冷月"], "key_events": ["相遇"]},
    ]
    result = _normalize_chapters(raw, "list_v5")
    assert 1 in result
    assert 2 in result
    assert result[1]["title"] == "开始"
    assert "冷月" in result[2]["characters_present"]
    print("✅ test_normalize_chapters_list_v5")


def test_normalize_chapters_dict_v9():
    """dict_v9: {entries: [{chapter, title, characters, key_events}]}"""
    raw = {
        "entries": [
            {"chapter": "Ch001", "title": "测试", "characters": ["林风"],
             "key_events": ["事件1"]},
        ]
    }
    result = _normalize_chapters(raw, "dict_v9")
    assert 1 in result
    assert result[1]["key_events"] == ["事件1"]
    print("✅ test_normalize_chapters_dict_v9")


def test_normalize_chapters_dict_v10():
    """dict_v10: {volume: {Ch001: {title, characters: {name: {...}}, ...}}}"""
    raw = {
        "V10_测试": {
            "Ch001": {
                "title": "开始",
                "characters": {"林风": {"role": "登场", "scene": "森林", "interaction": ""}},
                "key_events": ["出发"],
            }
        }
    }
    result = _normalize_chapters(raw, "dict_v10")
    assert 1 in result
    assert result[1]["title"] == "开始"
    assert "林风" in result[1]["characters_present"]
    print("✅ test_normalize_chapters_dict_v10")


def test_normalize_hooks_list():
    """List hooks format."""
    raw = [
        {"id": "h1", "type": "悬念", "description": "星辰碎片的下落",
         "chapter": "Ch001", "status": "活跃", "expected_payoff": "Ch010"},
    ]
    result = _normalize_hooks(raw, "list")
    assert len(result) == 1
    assert result[0]["chapter_created"] == 1
    assert result[0]["description"] == "星辰碎片的下落"
    print("✅ test_normalize_hooks_list")


def test_normalize_hooks_dict_v9():
    """V9 dict hooks: {hook, desc, planted, payoff}"""
    raw = [
        {"hook": "蓝色羽毛的秘密", "desc": "羽毛从蓝色变为金色",
         "planted": "ch001", "payoff": "ch030", "status": "active"},
    ]
    result = _normalize_hooks(raw, "list")
    assert result[0]["chapter_created"] == 1
    print("✅ test_normalize_hooks_dict_v9")


def test_migrate_project_v10():
    """Full migration pipeline with V10-format data."""
    with tempfile.TemporaryDirectory() as tmp:
        # Create V10-format data
        ca = {"V10_测试": {"Ch001": {"title": "开始", "characters": {"林风": {"role": "登场", "scene": "森林"}}, "key_events": ["出发"]}}}
        cr = {"characters": {"林风": {"role": "主角", "first_appearance": "v10ch001", "last_appearance": "v10ch001", "status": "active"}}}
        hk = [{"id": "h1", "type": "悬念", "description": "秘密", "chapter": "Ch001", "status": "活跃"}]
        for name, data in [("chapter_appearances.json", ca), ("character_roster.json", cr), ("hooks.json", hk)]:
            (Path(tmp) / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        report = migrate_project(tmp, dry_run=False)
        assert report["characters_migrated"] == 1
        assert report["chapters_migrated"] == 1
        assert report["hooks_migrated"] == 1
        assert (Path(tmp) / "story-state.json").exists()
        print("✅ test_migrate_project_v10")


def test_migrate_project_v9():
    """V9 format migration."""
    with tempfile.TemporaryDirectory() as tmp:
        ca = {"entries": [{"chapter": "Ch001", "title": "开始", "characters": ["林风"], "key_events": ["出发"]}],
              "v9ch001": ["林风"]}
        cr = {"characters": {"林风": {"role": "主角", "first_appearance": "ch001", "last_appearance": "ch020", "status": "active"}}}
        hk = [{"hook": "秘密", "desc": "测试", "planted": "ch001", "payoff": "", "status": "active"}]
        for name, data in [("chapter_appearances.json", ca), ("character_roster.json", cr), ("hooks.json", hk)]:
            (Path(tmp) / name).write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        report = migrate_project(tmp, dry_run=False)
        assert report["chapters_migrated"] >= 1
        assert report["characters_migrated"] >= 1
        assert (Path(tmp) / "story-state.json").exists()
        print("✅ test_migrate_project_v9")


def test_empty_project():
    """No JSON files should produce empty story-state."""
    with tempfile.TemporaryDirectory() as tmp:
        report = migrate_project(tmp, dry_run=False)
        assert report["characters_migrated"] == 0
        assert report["chapters_migrated"] == 0
        assert report["hooks_migrated"] == 0
        print("✅ test_empty_project")


def test_corrupted_hooks():
    """Corrupted hooks.json should not crash."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "hooks.json").write_text("{invalid json!!!", encoding="utf-8")
        report = migrate_project(tmp, dry_run=False)
        assert len(report["warnings"]) >= 1
        print("✅ test_corrupted_hooks")


def test_check_project():
    """Check command should report file status."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "bible.json").write_text('{"title": "测试"}', encoding="utf-8")
        (Path(tmp) / "chapter_appearances.json").write_text('[]', encoding="utf-8")
        result = check_project(tmp)
        assert "files" in result
        assert "chapter_appearances.json" in result["files"]
        assert "story-state.json" in result["files"]
        print("✅ test_check_project")


if __name__ == "__main__":
    test_parse_chapter_num()
    test_clean_title()
    test_name_to_id()
    test_normalize_characters_v10()
    test_normalize_characters_v5()
    test_normalize_chapters_list_v5()
    test_normalize_chapters_dict_v9()
    test_normalize_chapters_dict_v10()
    test_normalize_hooks_list()
    test_normalize_hooks_dict_v9()
    test_migrate_project_v10()
    test_migrate_project_v9()
    test_empty_project()
    test_corrupted_hooks()
    test_check_project()
    print("\n🎉 All migration tests passed!")
