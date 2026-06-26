#!/usr/bin/env python3
"""Tests for strand_balance — Strand 节奏量化系统"""
import sys, tempfile, json
from pathlib import Path

_review = Path(__file__).resolve().parent.parent / "review"
if str(_review) not in sys.path:
    sys.path.insert(0, str(_review))
from strand_balance import StrandAnalyzer, DEFAULT_TARGETS, MAX_STREAK


def make_state(chapters: int = 5, imbalances: dict = None) -> dict:
    """Build a sample story-state dict."""
    strands = {
        "quest_ratio": 0.40,
        "fire_ratio": 0.30,
        "constellation_ratio": 0.30,
        "quest_streak": 0,
        "fire_streak": 0,
        "constellation_streak": 0,
    }
    if imbalances:
        strands.update(imbalances)

    chs = {}
    for i in range(1, chapters + 1):
        chs[str(i)] = {
            "number": i,
            "title": f"Chapter {i}",
            "word_count": 2000 + i * 100,
            "strand_weights": {"quest": 0.5, "fire": 0.3, "constellation": 0.2},
        }

    return {
        "strands": strands,
        "chapters": chs,
        "characters": {},
    }


def test_balanced():
    """Perfect balance should produce no issues."""
    state = make_state(5)
    # 每章不同主导线索，避免触发节奏单调
    state["chapters"]["1"]["strand_weights"] = {"quest": 0.5, "fire": 0.3, "constellation": 0.2}
    state["chapters"]["2"]["strand_weights"] = {"quest": 0.2, "fire": 0.5, "constellation": 0.3}
    state["chapters"]["3"]["strand_weights"] = {"quest": 0.3, "fire": 0.2, "constellation": 0.5}
    state["chapters"]["4"]["strand_weights"] = {"quest": 0.4, "fire": 0.4, "constellation": 0.2}
    state["chapters"]["5"]["strand_weights"] = {"quest": 0.2, "fire": 0.4, "constellation": 0.4}
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state)
    assert len(report.issues) == 0, f"Balanced state should have 0 issues, got {len(report.issues)}: {[i.description for i in report.issues]}"
    assert report.overall_score == 100
    assert report.ratios["quest"] == 0.40
    assert report.ratios["fire"] == 0.30
    print("✅ test_balanced")


def test_streak_warning():
    """Fire streak > MAX_STREAK should produce P1 issue."""
    state = make_state(10, {"fire_streak": 5, "fire_ratio": 0.10})
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state, current_chapter=10)
    streak_issues = [i for i in report.issues if "连续" in i.category]
    assert len(streak_issues) >= 1, f"Should flag streak warning, got {len(report.issues)} issues"
    assert any(i.severity == "P1" for i in streak_issues)
    print("✅ test_streak_warning")


def test_imbalance_warning():
    """Imbalance >15% should produce P2 issue."""
    state = make_state(5, {"quest_ratio": 0.70, "fire_ratio": 0.15, "constellation_ratio": 0.15})
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state)
    imbalance_issues = [i for i in report.issues if "比例偏离" in i.category]
    assert len(imbalance_issues) >= 1, f"Should flag imbalance warning, got {len(report.issues)}"
    assert all(i.severity == "P2" for i in imbalance_issues)
    print("✅ test_imbalance_warning")


def test_starvation_warning():
    """Constellation streak >5 should produce P1 warning."""
    state = make_state(10, {"constellation_streak": 7, "constellation_ratio": 0.05})
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state, current_chapter=10)
    starvation_issues = [i for i in report.issues if "长期缺失" in i.category]
    assert len(starvation_issues) >= 1, f"Should flag starvation warning, got {len(report.issues)}"
    assert any(i.severity == "P1" for i in starvation_issues)
    print("✅ test_starvation_warning")


def test_dominant_strand():
    """Dominant strand detection."""
    state = make_state(5, {"quest_ratio": 0.60, "fire_ratio": 0.20, "constellation_ratio": 0.20})
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state)
    assert report.current_dominant == "quest", f"Expected quest as dominant, got {report.current_dominant}"
    print("✅ test_dominant_strand")


def test_monotone_warning():
    """Recent chapters all same strand should produce P2 issue."""
    state = make_state(8, {"quest_ratio": 0.50, "fire_ratio": 0.25, "constellation_ratio": 0.25})
    # All chapters have the same dominant strand weights
    for i in range(1, 9):
        state["chapters"][str(i)]["strand_weights"] = {
            "quest": 0.8, "fire": 0.1, "constellation": 0.1
        }
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state, current_chapter=8)
    monotone_issues = [i for i in report.issues if "节奏单调" in i.category]
    assert len(monotone_issues) >= 1, f"Should flag monotone warning, got {len(report.issues)}"
    print("✅ test_monotone_warning")


def test_from_file():
    """Test analyzing from file."""
    state = make_state(3)
    # 各章不同主导线索避免单调
    state["chapters"]["1"]["strand_weights"] = {"quest": 0.5, "fire": 0.3, "constellation": 0.2}
    state["chapters"]["2"]["strand_weights"] = {"quest": 0.2, "fire": 0.5, "constellation": 0.3}
    state["chapters"]["3"]["strand_weights"] = {"quest": 0.3, "fire": 0.2, "constellation": 0.5}
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(state, f)
        f.flush()
        path = Path(f.name)

    analyzer = StrandAnalyzer()
    report = analyzer.analyze_from_file(path)
    assert report.overall_score == 100
    path.unlink()
    print("✅ test_from_file")


def test_missing_file():
    """Non-existent file should return error report."""
    analyzer = StrandAnalyzer()
    report = analyzer.analyze_from_file(Path("/nonexistent/story-state.json"))
    assert report.overall_score == 0
    assert len(report.issues) >= 1
    print("✅ test_missing_file")


def test_empty_state():
    """Empty state dict should use defaults."""
    analyzer = StrandAnalyzer()
    report = analyzer.analyze({})
    assert report.ratios["quest"] == 0.40
    assert report.ratios["fire"] == 0.30
    assert report.ratios["constellation"] == 0.30
    print("✅ test_empty_state")


def test_report_text():
    """Report should produce readable text output."""
    state = make_state(5)
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state)
    text = report.to_text()
    assert "Strand 节奏分析" in text
    assert "整体评分" in text
    assert "主线" in text and "情感" in text and "世界观" in text
    print("✅ test_report_text")


def test_to_issues():
    """to_issues should return same issues as .issues."""
    state = make_state(10, {"fire_streak": 5, "fire_ratio": 0.10})
    analyzer = StrandAnalyzer()
    report = analyzer.analyze(state, current_chapter=10)
    assert len(report.to_issues()) == len(report.issues)
    for iss in report.to_issues():
        assert iss.role == "Strand分析师"
    print("✅ test_to_issues")


if __name__ == "__main__":
    test_balanced()
    test_streak_warning()
    test_imbalance_warning()
    test_starvation_warning()
    test_dominant_strand()
    test_monotone_warning()
    test_from_file()
    test_missing_file()
    test_empty_state()
    test_report_text()
    test_to_issues()
    print("\n🎉 All strand balance tests passed!")
