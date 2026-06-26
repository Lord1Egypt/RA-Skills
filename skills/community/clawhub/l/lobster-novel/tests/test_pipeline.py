#!/usr/bin/env python3
"""Tests for ContinuityTracker and Pipeline"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "core"))
from continuity import ContinuityTracker, ChapterState
from bible import BibleManager, ChapterSpec, Character


def test_continuity_append():
    with tempfile.TemporaryDirectory() as td:
        ct = ContinuityTracker(Path(td))
        state = ChapterState(chapter=1, summary="故事开始",
                             changed_characters={"张三": "injured"},
                             new_hooks=["神秘人是谁？"])
        ct.append(state)
        latest = ct.get_latest(1)
        assert len(latest) == 1
        assert latest[0].chapter == 1
        assert latest[0].changed_characters["张三"] == "injured"
        print("✅ test_continuity_append")


def test_continuity_multiple():
    with tempfile.TemporaryDirectory() as td:
        ct = ContinuityTracker(Path(td))
        for i in range(1, 6):
            ct.append(ChapterState(chapter=i, summary=f"Ch{i}"))
        latest = ct.get_latest(3)
        assert len(latest) == 3
        assert latest[-1].chapter == 5
        print("✅ test_continuity_multiple")


def test_continuity_summary():
    with tempfile.TemporaryDirectory() as td:
        ct = ContinuityTracker(Path(td))
        ct.append(ChapterState(chapter=1, summary="开局", new_hooks=["谜团"]))
        ct.append(ChapterState(chapter=2, summary="发展",
                               changed_characters={"李四": "觉醒"}))
        summary = ct.get_summary_for(2)
        assert "开局" in summary
        assert "发展" in summary
        assert "觉醒" in summary
        print("✅ test_continuity_summary")


def test_hook_status():
    with tempfile.TemporaryDirectory() as td:
        ct = ContinuityTracker(Path(td))
        ct.append(ChapterState(chapter=1, new_hooks=["钩子A", "钩子B"]))
        ct.append(ChapterState(chapter=2, resolved_hooks=["钩子A"]))
        status = ct.get_hook_status()
        assert "钩子A" not in status  # resolved
        assert "钩子B" in status       # still active
        print("✅ test_hook_status")


def test_pipeline_init():
    with tempfile.TemporaryDirectory() as td:
        from pipeline import Pipeline
        pipe = Pipeline(Path(td))
        assert pipe.bible is not None
        assert pipe.continuity is not None
        print("✅ test_pipeline_init")


def test_pipeline_writing_context():
    with tempfile.TemporaryDirectory() as td:
        from pipeline import Pipeline
        pipe = Pipeline(Path(td))
        pipe.bible.set_meta(title="Test")
        pipe.bible.add_character(
            Character(name="张三", role="protagonist",
                      background="普通人"))
        ctx = pipe.get_writing_context(1)
        assert ctx["chapter"] == 1
        assert "Test" in ctx["bible_summary"]
        assert "张三" in ctx["characters"]
        print("✅ test_pipeline_writing_context")


def test_pipeline_format_prompt():
    with tempfile.TemporaryDirectory() as td:
        from pipeline import Pipeline
        pipe = Pipeline(Path(td))
        ctx = pipe.get_writing_context(1)
        prompt = pipe.format_writing_prompt(ctx)
        assert "Chapter 1" in prompt
        assert "Requirements" in prompt
        assert "Output" in prompt
        print("✅ test_pipeline_format_prompt")


def test_pipeline_save_chapter():
    with tempfile.TemporaryDirectory() as td:
        from pipeline import Pipeline
        pipe = Pipeline(Path(td))
        text = "# Chapter 1: 开端\n\n故事开始了。\n\n突然，门外传来响声。"
        result = pipe.save_chapter(
            chapter=1, text=text, summary="开局",
            char_changes={"张三": "警觉"},
            new_hooks=["门外是谁？"],
            resolved=[])
        assert result["chapter"] == 1
        assert Path(result["file"]).exists()
        assert pipe.bible.get_chapter(1) is not None
        print("✅ test_pipeline_save_chapter")


def test_pipeline_review_context():
    with tempfile.TemporaryDirectory() as td:
        from pipeline import Pipeline
        pipe = Pipeline(Path(td))
        text = "# Chapter 1\n\nTest content."
        pipe.save_chapter(1, text, "test", {}, [], [])
        ctx = pipe.get_review_context(1)
        assert ctx["chapter"] == 1
        assert "Test content" in ctx["text"]
        print("✅ test_pipeline_review_context")


if __name__ == "__main__":
    test_continuity_append()
    test_continuity_multiple()
    test_continuity_summary()
    test_hook_status()
    test_pipeline_init()
    test_pipeline_writing_context()
    test_pipeline_format_prompt()
    test_pipeline_save_chapter()
    test_pipeline_review_context()
    print("\n🎉 All pipeline/continuity tests passed!")
