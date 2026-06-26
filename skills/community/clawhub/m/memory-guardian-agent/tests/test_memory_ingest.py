"""Tests for memory_ingest — core ingest helpers (unit-level, no file I/O)."""

import pytest
from memory_ingest import (
    quick_dedup_check,
    extract_entities,
    evaluate_cost_signals,
    build_importance_explain,
    _determine_provenance,
    _assign_memory_type,
    _classify,
    _build_content_from_case_fields,
    _build_new_memory,
)


# ─── quick_dedup_check ───────────────────────────────────────

class TestQuickDedupCheck:
    def test_exact_duplicate(self):
        mem = {"id": "mem_1", "content": "hello world test", "status": "active"}
        result = quick_dedup_check("hello world test", [mem])
        assert result is not None
        assert result["id"] == "mem_1"

    def test_no_duplicate(self):
        mem = {"id": "mem_1", "content": "completely different", "status": "active"}
        assert quick_dedup_check("hello world test", [mem]) is None

    def test_skips_archived(self):
        mem = {"id": "mem_1", "content": "hello world test", "status": "archived"}
        assert quick_dedup_check("hello world test", [mem]) is None

    def test_empty_memories(self):
        assert quick_dedup_check("test", []) is None

    def test_partial_overlap_below_threshold(self):
        mem = {"id": "mem_1", "content": "a b c d e f g h i j", "status": "active"}
        assert quick_dedup_check("a b x y z", [mem]) is None


# ─── extract_entities ────────────────────────────────────────

class TestExtractEntities:
    def test_feishu_open_id(self):
        entities = extract_entities("user ou_abcdef1234567890abcdef12")
        assert any(e["type"] == "feishu_open_id" for e in entities)

    def test_memory_id(self):
        entities = extract_entities("related to mem_abc12345")
        assert any(e["type"] == "memory_id" for e in entities)

    def test_url(self):
        entities = extract_entities("see https://example.com/path?q=1")
        assert any(e["type"] == "url" for e in entities)

    def test_version(self):
        entities = extract_entities("upgraded to v0.4.5")
        assert any(e["type"] == "version" and e["value"] == "v0.4.5" for e in entities)

    def test_no_duplicates(self):
        entities = extract_entities("ou_abc123 ou_abc123")
        assert len([e for e in entities if e["type"] == "feishu_open_id"]) == 1

    def test_empty_content(self):
        assert extract_entities("") == []


# ─── evaluate_cost_signals ───────────────────────────────────

class TestEvaluateCostSignals:
    def test_no_signals(self):
        costs = evaluate_cost_signals("short text")
        assert costs["human_cost"] == 0
        assert costs["transfer_cost"] == 0

    def test_long_content_write_cost(self):
        costs = evaluate_cost_signals("x" * 600)
        assert costs["write_cost"] >= 1

    def test_verify_keywords(self):
        costs = evaluate_cost_signals("需要测试验证确认")
        assert costs["verify_cost"] >= 1

    def test_human_keywords(self):
        costs = evaluate_cost_signals("通知用户回复")
        assert costs["human_cost"] >= 1

    def test_transfer_keywords(self):
        costs = evaluate_cost_signals("社区分享发布")
        assert costs["transfer_cost"] >= 1

    def test_capped_at_3(self):
        text = "测试 测试 测试 测试 验证 验证 确认"
        costs = evaluate_cost_signals(text)
        assert costs["verify_cost"] <= 3

    def test_case_fields_contribute(self):
        costs = evaluate_cost_signals("short", situation="需要用户确认回复")
        assert costs["human_cost"] >= 1


# ─── build_importance_explain ────────────────────────────────

class TestBuildImportanceExplain:
    def test_with_cost_signals(self):
        explain = build_importance_explain(0.8, {"human_cost": 1, "transfer_cost": 2})
        assert explain is not None
        assert "0.80" in explain

    def test_no_cost_signals(self):
        explain = build_importance_explain(0.5, {"write_cost": 0, "verify_cost": 0, "human_cost": 0, "transfer_cost": 0})
        assert explain is not None


# ─── _determine_provenance ───────────────────────────────────

class TestDetermineProvenance:
    def test_explicit_human(self):
        level, source = _determine_provenance("test", None, False, source="human")
        assert level == "L1"
        assert source == "human_direct"

    def test_explicit_system(self):
        level, source = _determine_provenance("test", None, False, source="system")
        assert level == "L2"

    def test_explicit_external(self):
        level, source = _determine_provenance("test", None, False, source="external")
        assert level == "L3"

    def test_content_keyword_l1(self):
        level, source = _determine_provenance("记住这个重要的事情", None, False)
        assert level == "L1"

    def test_default_l2(self):
        level, source = _determine_provenance("普通内容", None, False)
        assert level == "L2"


# ─── _assign_memory_type ─────────────────────────────────────

class TestAssignMemoryType:
    def test_l3_absorb(self):
        assert _assign_memory_type("L3", None, []) == "absorb"

    def test_l1_bootstrap_static(self):
        assert _assign_memory_type("L1", None, ["bootstrap"]) == "static"

    def test_l1_no_tag_derive(self):
        assert _assign_memory_type("L1", None, ["other"]) == "derive"

    def test_l2_derive(self):
        assert _assign_memory_type("L2", None, []) == "derive"


# ─── _classify ───────────────────────────────────────────────

class TestClassify:
    def test_explicit_tag_mapping(self):
        result = _classify("test content", tags_hint=["项目"])
        assert "项目" in result["tags"]
        assert result["primary_tag"] == "project"
        assert result["confidence"] >= 0.8

    def test_keyword_match_project(self):
        result = _classify("memory-guardian v0.4.5 版本开发中")
        assert result["primary_tag"] == "project"
        assert result["confidence"] > 0.5

    def test_keyword_match_tech(self):
        result = _classify("系统架构设计模式讨论")
        assert result["primary_tag"] == "tech"

    def test_fallback_misc(self):
        result = _classify("random content with no keywords")
        assert result["primary_tag"] == "misc"
        assert result["confidence"] < 0.5

    def test_return_structure(self):
        result = _classify("test")
        assert "tags" in result
        assert "confidence" in result
        assert "primary_tag" in result


# ─── _build_content_from_case_fields ─────────────────────────

class TestBuildContentFromCaseFields:
    def test_situation_and_judgment(self):
        content, is_case = _build_content_from_case_fields("sit", "judg", None, None, None)
        assert "情境：sit" in content
        assert "判断：judg" in content
        assert is_case is True

    def test_nothing(self):
        content, is_case = _build_content_from_case_fields(None, None, None, None, None)
        assert content is None
        assert is_case is False


# ─── _build_new_memory ───────────────────────────────────────

class TestBuildNewMemory:
    def test_basic_memory(self):
        mem, costs, is_l1, explain = _build_new_memory(
            "test content", 0.5, [], None, None, None, None,
            None, None, None, None, False
        )
        assert mem["content"] == "test content"
        assert mem["importance"] == 0.5
        assert mem["status"] == "active"
        assert mem["id"].startswith("mem_")

    def test_case_memory(self):
        mem, costs, is_l1, explain = _build_new_memory(
            "", 0.7, [], "situation", "judgment", None, None,
            None, None, None, None, True
        )
        assert mem["status"] == "observing"
        assert mem["situation"] == "situation"
        assert mem["judgment"] == "judgment"
        assert mem["id"].startswith("case_")

    def test_l1_flagged(self):
        mem, costs, is_l1, explain = _build_new_memory(
            "通知用户回复", 0.5, [], None, None, None, None,
            None, None, None, None, False
        )
        assert is_l1 is True
        assert explain is not None

    def test_returns_four_values(self):
        result = _build_new_memory("test", 0.5, [], None, None, None, None,
                                   None, None, None, None, False)
        assert len(result) == 4
