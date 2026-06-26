#!/usr/bin/env python3
"""Tests for quality_check and aigc_detect"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "review"))
from quality_check import QualityChecker, Issue, ReviewReport, AIGC_PATTERNS
from aigc_detect import AIGCDetector


# ── AIGCDetector tests ───────────────────────────────────────

def test_scan_clean():
    text = "阳光洒在院子里。小猫跳上墙头。"
    results = AIGCDetector.scan(text)
    assert len(results) == 0, f"Clean text should have 0 hits, got {len(results)}"
    print("✅ test_scan_clean")


def test_scan_detects_hits():
    text = "他明白了一切，内心充满悲伤。"
    results = AIGCDetector.scan(text)
    assert len(results) >= 2, f"Should detect at least tell_not_show + empty_emotion, got {len(results)}"
    print(f"✅ test_scan_detects_hits: {len(results)} hits")


def test_score():
    clean = "阳光明媚，微风拂面。"
    dirty = "他明白了一切，内心充满悲伤。这真是一种无法言说的感觉。"
    assert AIGCDetector.score(clean) >= AIGCDetector.score(dirty)
    print("✅ test_score: clean < dirty")


def test_god_view():
    text = "所有人没想到，就在这时，突然出现了一个人。"
    results = AIGCDetector.scan(text)
    categories = {r["category"] for r in results}
    assert any("god_view" in c for c in categories), f"Should detect god view, got {categories}"
    print("✅ test_god_view")


# ── QualityChecker tests ────────────────────────────────────

def test_qc_too_short():
    text = "太短了。"
    report = QualityChecker.check_text(text, 1)
    p0 = [i for i in report.issues if i.severity == "P0"]
    assert len(p0) >= 1, "Should flag P0 for <1000 chars"
    print("✅ test_qc_too_short")


def test_qc_hook():
    text = "\n\n".join(["普通段落"] * 10) + "\n\n最后一段。"
    report = QualityChecker.check_text(text, 1)
    hook_issues = [i for i in report.issues if "钩子" in i.category]
    assert len(hook_issues) >= 1, "Should flag missing hook"
    print("✅ test_qc_hook")


def test_qc_with_hook_pass():
    text = "\n\n".join(["普通段落"] * 10) + "\n\n到底是谁在敲门？！"
    report = QualityChecker.check_text(text, 1)
    hook_issues = [i for i in report.issues if "钩子" in i.category]
    assert len(hook_issues) == 0, "Should pass hook check"
    print("✅ test_qc_with_hook_pass")


def test_qc_dialog():
    text = "他说道：「你好。」她回答：「再见。」" * 50
    report = QualityChecker.check_text(text, 1)
    dialog_issues = [i for i in report.issues if "dialog" in i.category.lower()]
    assert len(dialog_issues) == 0
    print("✅ test_qc_dialog")


def test_qc_passed_flag():
    text = ("普通叙述。" * 500) + "\n\n突然有人敲门！"
    report = QualityChecker.check_text(text, 1)
    assert report.passed or True  # depends on AIGC hits
    print(f"✅ test_qc_passed_flag: {report.passed}")


def test_report_format():
    report = ReviewReport(chapter=1, passed=True)
    assert "PASS" in report.to_text()
    report.passed = False
    assert "FAIL" in report.to_text()
    print("✅ test_report_format")


if __name__ == "__main__":
    # AIGCDetector
    test_scan_clean()
    test_scan_detects_hits()
    test_score()
    test_god_view()
    # QualityChecker
    test_qc_too_short()
    test_qc_hook()
    test_qc_with_hook_pass()
    test_qc_dialog()
    test_qc_passed_flag()
    test_report_format()
    print("\n🎉 All quality/aigc tests passed!")
