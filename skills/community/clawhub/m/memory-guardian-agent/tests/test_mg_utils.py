"""Tests for mg_utils — shared utilities."""

import json
import os
import time
import pytest
from datetime import datetime, timedelta, timezone

from mg_utils import (
    CST,
    _now_iso,
    read_text_file,
    load_meta,
    save_meta,
    tokenize,
    jaccard_distance,
    split_memory_heading,
    classify_bootstrap_memory_type,
    is_bootstrap_memory_candidate,
    is_protected_memory,
    generate_memory_id,
    resolve_primary_tag,
    derive_file_path,
    classify_confidence_level,
    infer_importance_from_usage,
    get_effective_importance,
    get_memory_type_decay_profile,
    compute_provenance_confidence,
    build_global_index,
    build_inverted_index,
    file_lock_acquire,
    console_safe_text,
    _should_force_console_safe,
)


# ─── CST & _now_iso ──────────────────────────────────────────

class TestCST:
    def test_is_utc_plus_8(self):
        assert CST == timezone(timedelta(hours=8))

class TestNowIso:
    def test_returns_string(self):
        assert isinstance(_now_iso(), str)

    def test_parseable(self):
        dt = datetime.fromisoformat(_now_iso())
        assert dt.tzinfo is not None


# ─── read_text_file ──────────────────────────────────────────

class TestReadTextFile:
    def test_utf8(self, tmp_path):
        p = tmp_path / "test.txt"
        p.write_text("hello 你好", encoding="utf-8")
        assert "你好" in read_text_file(str(p))

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            read_text_file(str(tmp_path / "nonexistent.txt"))


# ─── load_meta / save_meta ───────────────────────────────────

class TestMetaIO:
    def test_load_missing(self, tmp_path):
        meta = load_meta(str(tmp_path / "meta.json"))
        assert "version" in meta
        assert "memories" in meta

    def test_roundtrip(self, tmp_path):
        path = str(tmp_path / "meta.json")
        data = {"version": "0.4.2", "memories": [{"id": "mem_1"}]}
        save_meta(path, data)
        loaded = load_meta(path)
        assert loaded["version"] == "0.4.2"
        assert loaded["memories"][0]["id"] == "mem_1"

    def test_save_creates_dir(self, tmp_path):
        path = str(tmp_path / "a" / "b" / "meta.json")
        save_meta(path, {"version": "0.4.2", "memories": []})
        assert os.path.exists(path)

    def test_load_corrupted(self, tmp_path):
        path = str(tmp_path / "bad.json")
        with open(path, "w") as f:
            f.write("{invalid json!!!")
        meta = load_meta(path)
        assert "_load_error" in meta

    def test_atomic_replace(self, tmp_path):
        path = str(tmp_path / "meta.json")
        save_meta(path, {"version": "0.4.2", "memories": []})
        save_meta(path, {"version": "0.4.5", "memories": []})
        assert load_meta(path)["version"] == "0.4.5"


# ─── tokenize ────────────────────────────────────────────────

class TestTokenize:
    def test_english(self):
        tokens = tokenize("hello world")
        assert "hello" in tokens
        assert "world" in tokens

    def test_chinese_bigram(self):
        tokens = tokenize("记忆系统")
        assert "记忆" in tokens
        assert "系统" in tokens

    def test_single_chinese_char(self):
        tokens = tokenize("一")
        assert "一" in tokens

    def test_empty(self):
        assert tokenize("") == []

    def test_none(self):
        assert tokenize(None) == []

    def test_mixed(self):
        tokens = tokenize("hello 记忆 world 系统")
        assert "hello" in tokens
        assert "world" in tokens
        assert "记忆" in tokens
        assert "系统" in tokens

    def test_single_char_english_skipped(self):
        tokens = tokenize("a b c")
        assert "a" not in tokens


# ─── jaccard_distance ────────────────────────────────────────

class TestJaccardDistance:
    def test_identical(self):
        assert jaccard_distance({"a", "b"}, {"a", "b"}) == 0.0

    def test_disjoint(self):
        assert jaccard_distance({"a"}, {"b"}) == 1.0

    def test_partial(self):
        d = jaccard_distance({"a", "b", "c"}, {"a", "b", "d"})
        assert 0.0 < d < 1.0

    def test_empty_both(self):
        assert jaccard_distance(set(), set()) == 0.0

    def test_one_empty(self):
        assert jaccard_distance({"a"}, set()) == 1.0


# ─── split_memory_heading ────────────────────────────────────

class TestSplitMemoryHeading:
    def test_bracket_format(self):
        heading, body = split_memory_heading("[标题] 内容在这里")
        assert heading == "标题"
        assert body == "内容在这里"

    def test_markdown_heading(self):
        text = "## 标题\n\n内容"
        heading, body = split_memory_heading(text)
        # Returns first line as heading
        assert "标题" in heading
        assert "内容" in body

    def test_plain_text(self):
        text = "第一行\n第二行"
        heading, body = split_memory_heading(text)
        assert heading == "第一行"
        assert body == "第二行"

    def test_empty(self):
        heading, body = split_memory_heading("")
        assert heading == ""
        assert body == ""

    def test_none(self):
        heading, body = split_memory_heading(None)
        assert heading == ""
        assert body == ""

    def test_single_line(self):
        heading, body = split_memory_heading("只有标题没有正文")
        assert "标题" in heading
        assert body == "只有标题没有正文"


# ─── classify_bootstrap_memory_type ──────────────────────────

class TestClassifyBootstrapMemoryType:
    def test_explicit_static(self):
        assert classify_bootstrap_memory_type({"memory_type": "static"}) == "static"

    def test_explicit_derive(self):
        assert classify_bootstrap_memory_type({"memory_type": "derive"}) == "derive"

    def test_explicit_absorb(self):
        assert classify_bootstrap_memory_type({"memory_type": "absorb"}) == "absorb"

    def test_high_importance_static(self):
        mem = {"importance": 0.9, "content": "some text"}
        assert classify_bootstrap_memory_type(mem) == "static"

    def test_keyword_static(self):
        mem = {"importance": 0.5, "content": "这是关于人设的记忆", "tags": []}
        assert classify_bootstrap_memory_type(mem) == "static"

    def test_keyword_derive(self):
        mem = {"importance": 0.6, "content": "经验教训总结", "tags": []}
        assert classify_bootstrap_memory_type(mem) == "derive"

    def test_default_absorb(self):
        mem = {"importance": 0.3, "content": "随便记点什么", "tags": []}
        assert classify_bootstrap_memory_type(mem) == "absorb"


# ─── is_bootstrap_memory_candidate ───────────────────────────

class TestIsBootstrapMemoryCandidate:
    def test_valid_candidate(self):
        mem = {"id": "mem_abc", "status": "active", "tags": ["bootstrapped"]}
        assert is_bootstrap_memory_candidate(mem) is True

    def test_not_mem_prefix(self):
        mem = {"id": "case_abc", "status": "active", "tags": ["bootstrapped"]}
        assert is_bootstrap_memory_candidate(mem) is False

    def test_not_active(self):
        mem = {"id": "mem_abc", "status": "archived", "tags": ["bootstrapped"]}
        assert is_bootstrap_memory_candidate(mem) is False

    def test_no_bootstrapped_tag(self):
        mem = {"id": "mem_abc", "status": "active", "tags": ["other"]}
        assert is_bootstrap_memory_candidate(mem) is False

    def test_not_dict(self):
        assert is_bootstrap_memory_candidate("not a dict") is False


# ─── is_protected_memory ─────────────────────────────────────

class TestIsProtectedMemory:
    def test_pinned(self):
        assert is_protected_memory({"pinned": True}) is True

    def test_high_importance(self):
        assert is_protected_memory({"importance": 0.95}) is True

    def test_low_importance(self):
        assert is_protected_memory({"importance": 0.5}) is False

    def test_not_dict(self):
        assert is_protected_memory(None) is False


# ─── generate_memory_id ──────────────────────────────────────

class TestGenerateMemoryId:
    def test_format(self):
        mid = generate_memory_id("test content")
        assert mid.startswith("mem_")
        parts = mid.split("_")
        assert len(parts) >= 3

    def test_deterministic_same_content(self):
        mid1 = generate_memory_id("test")
        mid2 = generate_memory_id("test")
        assert mid1 == mid2

    def test_uniqueness_with_existing(self):
        existing = {generate_memory_id("test") for _ in range(1)}
        for _ in range(5):
            mid = generate_memory_id("test", existing_ids=existing)
            assert mid not in existing
            existing.add(mid)

    def test_empty_content(self):
        mid = generate_memory_id("")
        assert mid.startswith("mem_")


# ─── resolve_primary_tag ─────────────────────────────────────

class TestResolvePrimaryTag:
    def test_known_tag(self):
        assert resolve_primary_tag(["项目"]) == "project"

    def test_multiple_known_first_wins(self):
        result = resolve_primary_tag(["技术", "项目"])
        assert result in ("tech", "project")

    def test_non_special_tag(self):
        result = resolve_primary_tag(["my_custom_tag"])
        assert result == "my_custom_tag"

    def test_non_special_tag_sanitized(self):
        result = resolve_primary_tag(["my/tag"])
        assert result == "my_tag"

    def test_empty_tags(self):
        assert resolve_primary_tag([]) == "misc"

    def test_content_fallback(self):
        result = resolve_primary_tag(["v0.4.5"], content="这是一个项目开发")
        assert result == "project"


# ─── derive_file_path ────────────────────────────────────────

class TestDeriveFilePath:
    def test_basic(self):
        path = derive_file_path("mem_abc123", ["项目"])
        assert path == "memory/project/mem_abc123.md"

    def test_custom_base_dir(self):
        path = derive_file_path("mem_abc", ["tech"], base_dir="custom")
        assert path.startswith("custom/")

    def test_misc_default(self):
        path = derive_file_path("mem_abc", ["v0.4.5"])
        assert "misc" in path


# ─── classify_confidence_level ───────────────────────────────

class TestClassifyConfidenceLevel:
    def test_high(self):
        assert classify_confidence_level(0.9) == ("direct", "high")

    def test_medium(self):
        assert classify_confidence_level(0.6) == ("review", "medium")

    def test_low(self):
        assert classify_confidence_level(0.3) == ("inbox", "low")

    def test_boundary_high(self):
        assert classify_confidence_level(0.8) == ("direct", "high")

    def test_boundary_medium(self):
        assert classify_confidence_level(0.5) == ("review", "medium")


# ─── infer_importance_from_usage ─────────────────────────────

class TestInferImportanceFromUsage:
    def test_no_usage(self):
        assert infer_importance_from_usage({}) == 0.05

    def test_high_trigger(self):
        mem = {"trigger_count": 10, "access_count": 0}
        imp = infer_importance_from_usage(mem)
        assert imp > 0.05

    def test_capped_at_0_6(self):
        mem = {"trigger_count": 1000, "access_count": 1000}
        assert infer_importance_from_usage(mem) <= 0.6

    def test_not_dict(self):
        assert infer_importance_from_usage(None) == 0.0


# ─── get_effective_importance ────────────────────────────────

class TestGetEffectiveImportance:
    def test_stored_value(self):
        assert get_effective_importance({"importance": 0.7}) == 0.7

    def test_missing_importance(self):
        mem = {"trigger_count": 5, "access_count": 10}
        imp = get_effective_importance(mem)
        assert 0.05 <= imp <= 0.6

    def test_zero_importance(self):
        mem = {"importance": 0, "trigger_count": 5}
        imp = get_effective_importance(mem)
        assert imp > 0

    def test_string_importance(self):
        assert get_effective_importance({"importance": "0.8"}) == 0.8

    def test_not_dict(self):
        assert get_effective_importance(None) == 0.5


# ─── get_memory_type_decay_profile ───────────────────────────

class TestGetMemoryTypeDecayProfile:
    def test_static(self):
        p = get_memory_type_decay_profile("static")
        assert p["memory_type"] == "static"
        assert p["alpha"] >= 0
        assert p["beta_cap"] >= 0

    def test_derive(self):
        p = get_memory_type_decay_profile("derive")
        assert p["memory_type"] == "derive"

    def test_absorb(self):
        p = get_memory_type_decay_profile("absorb")
        assert p["memory_type"] == "absorb"

    def test_unknown_defaults_to_derive(self):
        p = get_memory_type_decay_profile("unknown_type")
        assert p["memory_type"] == "derive"

    def test_custom_config(self):
        config = {"memory_types": {"static": {"alpha": 0.5, "beta_cap": 2.0}}}
        p = get_memory_type_decay_profile("static", decay_config=config)
        assert p["alpha"] == 0.5
        assert p["beta_cap"] == 2.0


# ─── compute_provenance_confidence ───────────────────────────

class TestComputeProvenanceConfidence:
    def test_l1_higher_than_l3(self):
        l1 = compute_provenance_confidence("L1")
        l3 = compute_provenance_confidence("L3")
        assert l1 > l3

    def test_verification_increases(self):
        base = compute_provenance_confidence("L1", verification_count=0)
        verified = compute_provenance_confidence("L1", verification_count=5)
        assert verified > base

    def test_verification_capped(self):
        v3 = compute_provenance_confidence("L1", verification_count=3)
        v100 = compute_provenance_confidence("L1", verification_count=100)
        assert v100 <= v3 + 0.01

    def test_unknown_level_defaults(self):
        result = compute_provenance_confidence("L_UNKNOWN")
        assert 0 < result < 1

    def test_custom_config(self):
        config = {"provenance": {"authoritative_base": 1.0, "authoritative_multiplier": 0.5}}
        result = compute_provenance_confidence("L1", decay_config=config)
        assert result == pytest.approx(0.5, abs=0.05)


# ─── build_global_index ──────────────────────────────────────

class TestBuildGlobalIndex:
    def test_empty(self):
        idx = build_global_index({"memories": []})
        assert "Total: 0" in idx

    def test_with_memories(self):
        meta = {
            "memories": [
                {"id": "mem_1", "importance": 0.8, "status": "active", "tags": ["项目"], "content": "test"},
            ]
        }
        idx = build_global_index(meta)
        assert "mem_1" in idx

    def test_sorted_by_importance(self):
        meta = {
            "memories": [
                {"id": "mem_low", "importance": 0.3, "status": "active", "tags": [], "content": "low"},
                {"id": "mem_high", "importance": 0.9, "status": "active", "tags": [], "content": "high"},
            ]
        }
        idx = build_global_index(meta)
        high_pos = idx.index("mem_high")
        low_pos = idx.index("mem_low")
        assert high_pos < low_pos


# ─── build_inverted_index ────────────────────────────────────

class TestBuildInvertedIndex:
    def test_empty(self):
        assert build_inverted_index({"memories": []}) == {}

    def test_index_built(self):
        meta = {
            "memories": [
                {"id": "mem_1", "content": "记忆系统设计"},
                {"id": "mem_2", "content": "记忆系统测试"},
            ]
        }
        idx = build_inverted_index(meta)
        assert "mem_1" in idx.get("记忆", set())
        assert "mem_2" in idx.get("记忆", set())


# ─── file_lock_acquire ───────────────────────────────────────

class TestFileLockAcquire:
    def test_basic_acquire(self, tmp_path):
        path = str(tmp_path / "test.lock")
        with file_lock_acquire(path, timeout=1.0):
            assert os.path.exists(path + ".lock")


# ─── console_safe_text ───────────────────────────────────────

class TestConsoleSafeText:
    def test_emoji_replaced(self):
        result = console_safe_text("hello ✅ world")
        assert "[OK]" in result
        assert "✅" not in result

    def test_utf8_passthrough(self):
        result = console_safe_text("hello 你好", encoding="utf-8")
        assert "你好" in result


class TestShouldForceConsoleSafe:
    def test_utf8_not_forced(self):
        assert _should_force_console_safe("utf-8") is False

    def test_cp936_forced(self):
        assert _should_force_console_safe("cp936") is True

    def test_none_not_forced(self):
        assert _should_force_console_safe(None) is False
