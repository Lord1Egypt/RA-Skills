"""Tests for memory_router — tag-based routing engine."""

import os
import json
import pytest

from memory_router import (
    _extract_tokens,
    _score_tag_match,
    compute_dynamic_n,
    TAG_KEYWORDS,
    TAG_SUBDIRS,
    BUDGET_HIGH,
    BUDGET_LOW,
)


class TestExtractTokens:
    def test_chinese_bigrams(self):
        tokens = _extract_tokens("记忆系统")
        assert "记忆" in tokens
        assert "系统" in tokens

    def test_english_words(self):
        tokens = _extract_tokens("Hello World Test")
        assert "hello" in tokens
        assert "world" in tokens

    def test_single_char(self):
        tokens = _extract_tokens("a")
        assert "a" not in tokens  # len < 2

    def test_single_chinese_char(self):
        tokens = _extract_tokens("一")
        assert "一" in tokens

    def test_empty(self):
        assert _extract_tokens("") == []

    def test_mixed(self):
        tokens = _extract_tokens("hello 记忆 world")
        assert "hello" in tokens
        assert "记忆" in tokens


class TestScoreTagMatch:
    def test_exact_keyword_match(self):
        score = _score_tag_match("项目开发", "project")
        assert score > 0

    def test_no_match(self):
        score = _score_tag_match("完全无关的内容", "event")
        assert score == 0

    def test_multiple_keywords(self):
        score = _score_tag_match("项目计划任务迭代", "project")
        assert score > _score_tag_match("项目", "project")


class TestComputeDynamicN:
    def test_high_budget_three_categories(self):
        n = compute_dynamic_n(0.5)
        assert n == 3

    def test_low_budget_one_category(self):
        n = compute_dynamic_n(0.15)
        assert n == 1

    def test_medium_budget_two_categories(self):
        n = compute_dynamic_n(0.3)
        assert n == 2

    def test_zero_budget(self):
        n = compute_dynamic_n(0.0)
        assert n == 1


class TestTagKeywords:
    def test_all_have_keywords(self):
        for tag, keywords in TAG_KEYWORDS.items():
            assert len(keywords) > 0

    def test_tag_subdirs_match_keywords(self):
        for tag in TAG_KEYWORDS:
            assert tag in TAG_SUBDIRS


# ─── New tests for uncovered functions ───────────────────────

from memory_router import append_routing_log, build_category_activity, route


class TestAppendRoutingLog:
    def test_appends_log(self, tmp_path):
        import json
        meta = {"memories": [], "routing_log": []}
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        entry = {"timestamp": "2026-01-01T00:00:00", "query_preview": "test"}
        append_routing_log(p, entry)
        with open(p) as f:
            updated = json.load(f)
        assert len(updated["routing_log"]) == 1

    def test_trims_old_logs(self, tmp_path):
        import json
        logs = [{"ts": i} for i in range(60)]
        meta = {"memories": [], "routing_log": logs}
        p = str(tmp_path / "meta.json")
        with open(p, "w") as f:
            json.dump(meta, f)
        append_routing_log(p, {"ts": 99})
        with open(p) as f:
            updated = json.load(f)
        assert len(updated["routing_log"]) == 50
        assert updated["routing_log"][-1]["ts"] == 99


class TestBuildCategoryActivity:
    def test_empty_meta(self):
        activity = build_category_activity({"memories": []})
        assert activity == {}

    def test_counts_access(self):
        meta = {
            "memories": [{
                "id": "m1", "tags": ["project"],
                "classification": {"primary_tag": "project"},
                "access_count": 10,
                "reactivation_count": 2,
            }]
        }
        activity = build_category_activity(meta)
        assert "project" in activity
        assert activity["project"] > 0

    def test_falls_back_to_first_tag(self):
        meta = {
            "memories": [{
                "id": "m1", "tags": ["tech"],
                "access_count": 5,
            }]
        }
        activity = build_category_activity(meta)
        assert "tech" in activity


class TestRoute:
    def test_basic_routing(self, tmp_path):
        meta = {
            "memories": [{
                "id": "m1", "content": "项目开发进度报告", "tags": ["project"],
                "classification": {"primary_tag": "project"},
                "access_count": 1,
            }]
        }
        # Create the workspace subdirectory
        subdir = tmp_path / "memory" / "projects"
        subdir.mkdir(parents=True)
        result = route("项目进度", meta, str(tmp_path), token_budget_ratio=0.5)
        assert "categories" in result
        assert "dynamic_n" in result
        assert isinstance(result["categories"], list)

    def test_no_match_returns_empty(self, tmp_path):
        meta = {"memories": []}
        result = route("xyznonexistent123", meta, str(tmp_path), token_budget_ratio=0.1)
        assert isinstance(result["categories"], list)
