"""Tests for scripts/humanizer_check.py — the de-AI-tone gate.

The wordlists live in the script and are tuned against real manuscript text,
so these tests do not freeze the thresholds. They freeze the mechanics: what
counts as Chinese, what counts as dialogue, and the fact that a banned word in
narration is caught while the same word inside dialogue is not.
"""

from __future__ import annotations

import humanizer_check as hc


def test_count_cn_ignores_latin_and_punctuation():
    assert hc.count_cn("ab，。12") == 0
    assert hc.count_cn("四个汉字") == 4


def test_strip_dialogue_removes_quoted_speech():
    assert hc.strip_dialogue('他说“首先，其次”然后走') == "他说然后走"


def test_banned_word_in_narration_is_caught(tree):
    p = tree("chapters/ch-001.md", "首先，其次，与此同时，总的来说。\n")
    r = hc.check_file(p)
    assert r["level"] == "FAIL"
    assert r["issues"]


def test_punctuation_density_excludes_dialogue(tree):
    # The dash budget applies to narration, so a dash-heavy line of speech
    # alone must not trip it.
    body = '他吼道：“走——开——滚——出去——现在——马上——”\n' + "雪落在阶前，没有人回头。\n"
    p = tree("chapters/ch-002.md", body)
    r = hc.check_file(p)
    assert not any("破折号" in i[1] for i in r["issues"])


def test_clean_prose_passes(tree):
    body = "\n".join(
        f"院子里的雪压着竹枝，他把手缩进袖口，等巷口那盏灯灭掉。第{i}句。" for i in range(12)
    )
    p = tree("chapters/ch-003.md", body)
    r = hc.check_file(p)
    assert r["level"] in ("PASS", "WARN")
    assert r["cn"] > 0


def test_result_shape(tree):
    p = tree("chapters/ch-004.md", "很普通的叙述。\n")
    r = hc.check_file(p)
    assert set(r) >= {"file", "cn", "level", "density", "issues", "stats"}
    assert r["level"] in ("PASS", "WARN", "FAIL")
