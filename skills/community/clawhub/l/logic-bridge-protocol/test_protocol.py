"""
Tests for logic_bridge_protocol.
Run: python3 -m pytest test_protocol.py -v
     or: python3 test_protocol.py
"""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from protocol import logic_bridge_protocol


# ── helpers ───────────────────────────────────────────────────────────────────

def assert_status(result: dict, expected: str, label: str) -> None:
    assert result["status"] == expected, (
        f"[{label}] expected status={expected!r}, got {result['status']!r}\n{result}"
    )


# ── invalid input ─────────────────────────────────────────────────────────────

def test_empty_string():
    r = logic_bridge_protocol({"raw_text": ""})
    assert_status(r, "error", "empty string")
    assert r["follow_up_questions"], "should have follow-up questions"


def test_missing_key():
    r = logic_bridge_protocol({})
    assert_status(r, "error", "missing raw_text")
    assert r["follow_up_questions"]


def test_none_value():
    r = logic_bridge_protocol({"raw_text": None})
    assert_status(r, "error", "None value")


def test_wrong_type():
    r = logic_bridge_protocol({"raw_text": 12345})
    # pydantic coerces int→str, so this may succeed or fail; just must not raise
    assert r["status"] in ("ok", "error")


# ── too-vague inputs ──────────────────────────────────────────────────────────

def test_single_word():
    r = logic_bridge_protocol({"raw_text": "button"})
    assert_status(r, "error", "single word")
    assert len(r["follow_up_questions"]) >= 3


def test_add_feature():
    r = logic_bridge_protocol({"raw_text": "add a feature"})
    assert_status(r, "error", "add a feature")


def test_vague_chinese():
    r = logic_bridge_protocol({"raw_text": "做一个新功能"})
    assert_status(r, "error", "vague Chinese")


# ── partially complete ────────────────────────────────────────────────────────

def test_zh_no_path():
    """Has actor + scenario + goal but no step-by-step path."""
    r = logic_bridge_protocol({
        "raw_text": "作为管理员，在用户列表页面，我需要封禁账号，因为有人违规。"
    })
    assert_status(r, "error", "ZH no path")
    questions = r["follow_up_questions"]
    assert len(questions) == 1
    q = questions[0].lower()
    assert "path" in q or "actionable" in q or "操作路径" in questions[0]


# ── valid inputs ──────────────────────────────────────────────────────────────

def test_strong_en_story():
    r = logic_bridge_protocol({
        "raw_text": (
            "As a support agent, when I open a ticket I want to paste logs "
            "and save them so the engineer sees them. "
            "I click Attach, choose file, then Save."
        )
    })
    assert_status(r, "ok", "strong EN story")
    tasks = r["file_editor_tasks"]
    assert len(tasks) == 1
    assert tasks[0]["intent"] == "write"
    assert "sha256=" in tasks[0]["instructions"]


def test_strong_zh_story():
    r = logic_bridge_protocol({
        "raw_text": (
            "作为运营同学，在活动管理页面，我需要批量导出用户数据，"
            "因为现在手动下载很痛苦。"
            "我先点筛选条件，然后点导出按钮，最后看到下载弹窗。"
        )
    })
    assert_status(r, "ok", "strong ZH story")
    tasks = r["file_editor_tasks"]
    assert tasks[0]["target_path"] == "docs/logic_bridge_task.md"


def test_deterministic_hash():
    """Same input must always produce the same sha256."""
    text = "As a user on the orders page I want to cancel my order so I don't pay for wrong items. I click Cancel, confirm, then see a refund notification."
    r1 = logic_bridge_protocol({"raw_text": text})
    r2 = logic_bridge_protocol({"raw_text": text})
    assert_status(r1, "ok", "hash-r1")
    assert r1["file_editor_tasks"][0]["instructions"] == r2["file_editor_tasks"][0]["instructions"]


def test_different_inputs_different_hashes():
    text_a = "As a user on the dashboard page I want to export CSV so I can analyze data. I click Export, pick range, then Download."
    text_b = "As an admin on the settings page I need to disable an account because of abuse. I click the user, toggle Active off, then confirm."
    ra = logic_bridge_protocol({"raw_text": text_a})
    rb = logic_bridge_protocol({"raw_text": text_b})
    assert_status(ra, "ok", "hash-a")
    assert_status(rb, "ok", "hash-b")
    assert ra["file_editor_tasks"][0]["instructions"] != rb["file_editor_tasks"][0]["instructions"]


# ── runner ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [
        test_empty_string,
        test_missing_key,
        test_none_value,
        test_wrong_type,
        test_single_word,
        test_add_feature,
        test_vague_chinese,
        test_zh_no_path,
        test_strong_en_story,
        test_strong_zh_story,
        test_deterministic_hash,
        test_different_inputs_different_hashes,
    ]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as e:
            print(f"  FAIL  {t.__name__}: {e}")
            failed += 1
    print(f"\n{passed}/{passed + failed} tests passed")
    sys.exit(0 if failed == 0 else 1)
