#!/usr/bin/env python3
"""Tests for ExportManager"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "output"))
from export import ExportManager


def _setup_chapters(tmpdir: Path):
    ch_dir = tmpdir / "chapters"
    ch_dir.mkdir()
    for i in range(1, 4):
        ch_dir / f"ch{i:03d}.md"
        (ch_dir / f"ch{i:03d}.md").write_text(
            f"# Chapter {i}\n\n这是第{i}章的内容。\n\n突然发生了意外！",
            encoding="utf-8")
    return ch_dir


def test_export_md():
    with tempfile.TemporaryDirectory() as td:
        ch_dir = _setup_chapters(Path(td))
        out = Path(td) / "output" / "novel.md"
        ExportManager.to_md(ch_dir, out, title="测试小说")
        assert out.exists()
        text = out.read_text(encoding="utf-8")
        assert "测试小说" in text
        assert "Chapter 3" in text
        print("✅ test_export_md")


def test_export_txt():
    with tempfile.TemporaryDirectory() as td:
        ch_dir = _setup_chapters(Path(td))
        out = Path(td) / "output" / "novel.txt"
        ExportManager.to_txt(ch_dir, out, title="测试小说")
        assert out.exists()
        text = out.read_text(encoding="utf-8")
        assert "Chapter" in text
        print("✅ test_export_txt")


def test_export_html():
    with tempfile.TemporaryDirectory() as td:
        ch_dir = _setup_chapters(Path(td))
        out = Path(td) / "output" / "novel.html"
        ExportManager.to_html(ch_dir, out, title="测试小说")
        assert out.exists()
        text = out.read_text(encoding="utf-8")
        assert "<html" in text
        assert "测试小说" in text
        assert "DOCTYPE" in text
        print("✅ test_export_html")


def test_export_no_chapters():
    with tempfile.TemporaryDirectory() as td:
        ch_dir = Path(td) / "empty"
        ch_dir.mkdir()
        out = Path(td) / "out.md"
        try:
            ExportManager.to_md(ch_dir, out)
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            print("✅ test_export_no_chapters")


def test_export_empty_title():
    with tempfile.TemporaryDirectory() as td:
        ch_dir = _setup_chapters(Path(td))
        out = Path(td) / "output" / "novel.md"
        ExportManager.to_md(ch_dir, out)
        text = out.read_text(encoding="utf-8")
        assert "Novel" in text  # default title
        print("✅ test_export_empty_title")


if __name__ == "__main__":
    test_export_md()
    test_export_txt()
    test_export_html()
    test_export_no_chapters()
    test_export_empty_title()
    print("\n🎉 All export tests passed!")
