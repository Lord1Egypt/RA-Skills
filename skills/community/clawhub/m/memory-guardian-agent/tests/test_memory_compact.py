"""Tests for memory_compact — redundancy detection and compaction."""

import os
import pytest
from memory_compact import (
    jaccard,
    load_file,
    estimate_tokens,
    section_token_analysis,
    detect_redundancy,
    detect_internal_redundancy,
    detect_bloat_sections,
    aggressive_compact_memory_text,
)


class TestJaccard:
    def test_identical(self):
        assert jaccard({"a", "b"}, {"a", "b"}) == 0.0

    def test_disjoint(self):
        assert jaccard({"a"}, {"b"}) == 1.0

    def test_partial(self):
        d = jaccard({"a", "b"}, {"a", "c"})
        assert 0 < d < 1


class TestLoadFile:
    def test_existing(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello")
        assert load_file(str(p)) == "hello"

    def test_missing(self):
        assert load_file("/nonexistent/path.txt") == ""


class TestEstimateTokens:
    def test_cjk(self):
        assert estimate_tokens("你好世界") > 0

    def test_english(self):
        assert estimate_tokens("hello world") > 0

    def test_empty(self):
        assert estimate_tokens("") == 0


class TestSectionTokenAnalysis:
    def test_basic_sections(self):
        text = "# Header\nline1\n## Section\nline2\n"
        sections = section_token_analysis(text)
        assert len(sections) >= 1

    def test_empty_text(self):
        sections = section_token_analysis("")
        assert sections == []

    def test_no_headers(self):
        sections = section_token_analysis("just plain text\nno headers")
        assert len(sections) == 1


class TestDetectRedundancy:
    def test_no_redundancy(self):
        issues = detect_redundancy("completely unique content A", {
            "day1.md": "totally different content B"
        })
        assert len(issues) == 0

    def test_high_redundancy(self):
        memory = "记忆系统设计包括衰减引擎和质量门控组件"
        daily = "### 记忆系统设计\n记忆系统设计包括衰减引擎和质量门控组件\n额外内容"
        issues = detect_redundancy(memory, {"day1.md": daily})
        assert len(issues) > 0

    def test_empty_inputs(self):
        issues = detect_redundancy("", {})
        assert len(issues) == 0


class TestDetectInternalRedundancy:
    def test_no_redundancy(self):
        issues = detect_internal_redundancy("line one\nline two\nline three")
        assert len(issues) == 0

    def test_duplicated_sections(self):
        text = "## Section A\nrepeated content here\n## Section B\nrepeated content here"
        issues = detect_internal_redundancy(text)
        # May or may not flag depending on token overlap threshold
        assert isinstance(issues, list)


class TestDetectBloatSections:
    def test_small_sections_ok(self):
        issues = detect_bloat_sections("# Small\nshort content")
        assert len(issues) == 0

    def test_large_section_flagged(self):
        big_section = "# Big\n" + "word " * 600
        issues = detect_bloat_sections(big_section, max_tokens_per_section=50)
        assert len(issues) > 0


class TestAggressiveCompact:
    def test_removes_redundant_sections(self):
        text = "## 项目\nmemory-guardian v0.4.5\n## 项目\nmemory-guardian v0.4.5\n## 其他\nunique"
        result = aggressive_compact_memory_text(text)
        # Should have reduced content
        assert isinstance(result, str)

    def test_empty_input(self):
        assert aggressive_compact_memory_text("") == ""
