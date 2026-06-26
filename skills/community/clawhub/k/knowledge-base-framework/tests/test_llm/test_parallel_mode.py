#!/usr/bin/env python3
"""
Tests for ParallelMixin - Diff/merge logic and parallel strategy dispatch.

Tests primary_first, aggregate, and compare strategies, plus
diff_essences, merge_essences, diff_reports, merge_reports.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from dataclasses import dataclass

from kb.biblio.config import LLMConfig
from kb.biblio.engine.base import LLMProvider, LLMResponse
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError
from kb.biblio.generator.parallel_mixin import (
    ParallelMixin,
    ParallelStrategy,
    DiffType,
    DiffEntry,
    DiffResult,
    ParallelResult,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def reset_singletons():
    """Reset singletons before and after each test."""
    EngineRegistry.reset()
    LLMConfig.reset()
    yield
    EngineRegistry.reset()
    LLMConfig.reset()


@pytest.fixture
def mixin():
    """Create a ParallelMixin instance with test config."""
    config = LLMConfig(
        model_source="auto",
        parallel_mode=True,
        parallel_strategy="primary_first",
        hf_model_name="google/gemma-2-2b-it",
        skip_validation=True,
    )
    m = ParallelMixin()
    m.__init_parallel__(llm_config=config)
    return m


@pytest.fixture
def mixin_compare():
    """ParallelMixin with compare strategy."""
    config = LLMConfig(
        model_source="compare",
        parallel_mode=True,
        parallel_strategy="compare",
        hf_model_name="google/gemma-2-2b-it",
        skip_validation=True,
    )
    m = ParallelMixin()
    m.__init_parallel__(llm_config=config)
    return m


# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------


SAMPLE_ESSENCE_A = {
    "summary": "Vitamin D is essential for bone health",
    "key_points": ["Bone health", "Immune system"],
    "connections": ["Calcium absorption"],
    "contradictions": [],
    "open_questions": ["Optimal dosage?"],
    "entities": ["Vitamin D", "Calcium"],
    "relationships": [
        {"from": "Vitamin D", "type": "enables", "to": "Calcium absorption"}
    ],
    "keywords": ["vitamin D", "bone"],
}


SAMPLE_ESSENCE_B = {
    "summary": "Vitamin D supports immune function and bone health",
    "key_points": ["Bone health", "Immune function", "Sun exposure"],
    "connections": ["Calcium absorption", "Sunlight synthesis"],
    "contradictions": ["RDA varies by country"],
    "open_questions": ["Optimal dosage?", "Sun vs supplements?"],
    "entities": ["Vitamin D", "Calcium", "Sunlight"],
    "relationships": [
        {"from": "Vitamin D", "type": "enables", "to": "Calcium absorption"},
        {"from": "Sunlight", "type": "produces", "to": "Vitamin D"},
    ],
    "keywords": ["vitamin D", "immune"],
}


# ---------------------------------------------------------------------------
# Test: DiffType and DiffEntry
# ---------------------------------------------------------------------------


class TestDiffTypes:
    """Tests for DiffType enum and DiffEntry dataclass."""

    def test_diff_type_values(self):
        assert DiffType.ADDED.value == "added"
        assert DiffType.REMOVED.value == "removed"
        assert DiffType.CHANGED.value == "changed"
        assert DiffType.UNCHANGED.value == "unchanged"

    def test_diff_entry_to_dict(self):
        entry = DiffEntry(field="summary", diff_type=DiffType.CHANGED, value_a="A", value_b="B")
        d = entry.to_dict()
        assert d["field"] == "summary"
        assert d["diff_type"] == "changed"
        assert d["value_a"] == "A"
        assert d["value_b"] == "B"

    def test_diff_entry_default_values(self):
        entry = DiffEntry(field="test", diff_type=DiffType.ADDED)
        assert entry.value_a is None
        assert entry.value_b is None


# ---------------------------------------------------------------------------
# Test: DiffResult
# ---------------------------------------------------------------------------


class TestDiffResult:
    """Tests for DiffResult dataclass."""

    def test_can_merge_no_conflicts_with_complements(self):
        """can_merge is True when there are complements and no conflicts."""
        result = DiffResult(
            complement_count=3,
            conflict_count=0,
            has_conflicts=False,
        )
        assert result.can_merge is True

    def test_can_merge_with_conflicts(self):
        """can_merge is False when there are conflicts."""
        result = DiffResult(
            complement_count=3,
            conflict_count=1,
            has_conflicts=True,
        )
        assert result.can_merge is False

    def test_can_merge_no_complements(self):
        """can_merge is False when there are no complements (nothing to merge)."""
        result = DiffResult(
            complement_count=0,
            conflict_count=0,
            has_conflicts=False,
        )
        assert result.can_merge is False

    def test_diff_result_to_dict(self):
        result = DiffResult(
            diffs=[DiffEntry("field1", DiffType.ADDED, value_b="val")],
            summary="1 difference",
            has_conflicts=False,
            complement_count=1,
            conflict_count=0,
            unchanged_count=5,
        )
        d = result.to_dict()
        assert d["summary"] == "1 difference"
        assert d["can_merge"] is True
        assert len(d["diffs"]) == 1


# ---------------------------------------------------------------------------
# Test: ParallelStrategy
# ---------------------------------------------------------------------------


class TestParallelStrategy:
    """Tests for ParallelStrategy enum."""

    def test_strategy_values(self):
        assert ParallelStrategy.PRIMARY_FIRST.value == "primary_first"
        assert ParallelStrategy.AGGREGATE.value == "aggregate"
        assert ParallelStrategy.COMPARE.value == "compare"

    def test_strategy_from_string(self):
        assert ParallelStrategy("primary_first") == ParallelStrategy.PRIMARY_FIRST
        assert ParallelStrategy("aggregate") == ParallelStrategy.AGGREGATE
        assert ParallelStrategy("compare") == ParallelStrategy.COMPARE


# ---------------------------------------------------------------------------
# Test: diff_essences
# ---------------------------------------------------------------------------


class TestDiffEssences:
    """Tests for ParallelMixin.diff_essences()."""

    def test_identical_essences_no_diffs(self, mixin):
        """Two identical essences should produce no differences."""
        result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_A)
        assert result.complement_count == 0
        assert result.conflict_count == 0
        assert result.unchanged_count > 0

    def test_added_items_detected(self, mixin):
        """Items in B not in A should be marked as ADDED."""
        result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        added_fields = [d for d in result.diffs if d.diff_type == DiffType.ADDED]
        # B has extra items: "Immune function", "Sun exposure" in key_points, etc.
        assert len(added_fields) > 0

    def test_removed_items_detected(self, mixin):
        """Items in A not in B should be marked as REMOVED."""
        essence_a = {"summary": "Test", "key_points": ["A", "B", "C"], "keywords": ["x", "y"]}
        essence_b = {"summary": "Test", "key_points": ["B"], "keywords": ["x"]}
        result = mixin.diff_essences(essence_a, essence_b)
        removed_fields = [d for d in result.diffs if d.diff_type == DiffType.REMOVED]
        assert len(removed_fields) > 0

    def test_changed_summary_detected(self, mixin):
        """Different summaries should be marked as CHANGED."""
        result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        changed = [d for d in result.diffs if d.diff_type == DiffType.CHANGED and d.field == "summary"]
        assert len(changed) == 1
        assert changed[0].value_a != changed[0].value_b

    def test_complementary_items_counted(self, mixin):
        """Complementary items should be counted."""
        result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        # There should be complementary differences (items in B not in A)
        assert result.complement_count > 0

    def test_empty_essence_diff(self, mixin):
        """Diff against empty essence should show all items as ADDED."""
        empty = {"summary": "", "key_points": [], "connections": [],
                 "contradictions": [], "open_questions": [], "entities": [],
                 "relationships": [], "keywords": []}
        result = mixin.diff_essences(empty, SAMPLE_ESSENCE_B)
        assert result.complement_count > 0
        added = [d for d in result.diffs if d.diff_type == DiffType.ADDED]
        assert len(added) > 0

    def test_relationships_diff(self, mixin):
        """Relationships should be compared by from/type/to keys."""
        result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        # B has an extra relationship: Sunlight → produces → Vitamin D
        rel_diffs = [d for d in result.diffs if d.field == "relationships"]
        assert len(rel_diffs) > 0

    def test_diff_result_summary(self, mixin):
        """DiffResult.summary should contain human-readable description."""
        result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        assert isinstance(result.summary, str)
        assert len(result.summary) > 0


# ---------------------------------------------------------------------------
# Test: merge_essences
# ---------------------------------------------------------------------------


class TestMergeEssences:
    """Tests for ParallelMixin.merge_essences()."""

    def test_merge_combines_lists(self, mixin):
        """Merged essence should combine list fields (union)."""
        merged = mixin.merge_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        # key_points should be union of both
        key_points_lower = [str(k).strip().lower() for k in merged["key_points"]]
        assert "bone health" in key_points_lower
        assert "immune function" in key_points_lower
        assert "sun exposure" in key_points_lower

    def test_merge_deduplicates(self, mixin):
        """Merged essence should deduplicate items by lowercase comparison."""
        merged = mixin.merge_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        # "Bone health" appears in both, should appear once
        key_points_lower = [str(k).strip().lower() for k in merged["key_points"]]
        assert key_points_lower.count("bone health") == 1

    def test_merge_prefers_longer_summary(self, mixin):
        """Merge should prefer the longer/more informative summary."""
        merged = mixin.merge_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        # B's summary is longer and more detailed
        assert "immune" in merged["summary"].lower() or len(merged["summary"]) >= len(SAMPLE_ESSENCE_A["summary"])

    def test_merge_empty_essence(self, mixin):
        """Merging with empty essence should return the non-empty one."""
        empty = {"summary": "", "key_points": [], "connections": [],
                 "contradictions": [], "open_questions": [], "entities": [],
                 "relationships": [], "keywords": []}
        merged = mixin.merge_essences(SAMPLE_ESSENCE_A, empty)
        assert merged["summary"] == SAMPLE_ESSENCE_A["summary"]

    def test_merge_relationships(self, mixin):
        """Relationships should be merged by union."""
        merged = mixin.merge_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        # Should contain relationships from both
        assert len(merged["relationships"]) >= len(SAMPLE_ESSENCE_A["relationships"])

    def test_merge_with_explicit_diff_result(self, mixin):
        """merge_essences with explicit DiffResult should use it."""
        diff_result = mixin.diff_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B)
        merged = mixin.merge_essences(SAMPLE_ESSENCE_A, SAMPLE_ESSENCE_B, diff_result)
        assert "key_points" in merged
        # Should still produce correct merge
        key_points_lower = [str(k).strip().lower() for k in merged["key_points"]]
        assert "bone health" in key_points_lower


# ---------------------------------------------------------------------------
# Test: diff_reports
# ---------------------------------------------------------------------------


class TestDiffReports:
    """Tests for ParallelMixin.diff_reports()."""

    def test_identical_reports_no_diffs(self, mixin):
        """Identical reports should produce minimal diff."""
        report = "## Summary\nThis is a test report.\n\n## Details\nSome details here."
        result = mixin.diff_reports(report, report)
        # Only header lines in unified diff, no real changes
        assert result.complement_count == 0 or result.unchanged_count > 0

    def test_added_lines_detected(self, mixin):
        """Added lines in report B should be detected."""
        report_a = "## Summary\nLine 1\n\n## Details\nDetail A"
        report_b = "## Summary\nLine 1\nLine 2\n\n## Details\nDetail A\nDetail B"
        result = mixin.diff_reports(report_a, report_b)
        assert result.complement_count > 0

    def test_removed_lines_detected(self, mixin):
        """Removed lines in report B should be detected."""
        report_a = "## Summary\nLine 1\nLine 2\nLine 3"
        report_b = "## Summary\nLine 1"
        result = mixin.diff_reports(report_a, report_b)
        # Should detect removals
        diffs_with_removed = [d for d in result.diffs if d.diff_type == DiffType.REMOVED]
        assert len(diffs_with_removed) > 0

    def test_diff_result_summary_format(self, mixin):
        """Summary should contain line change counts."""
        report_a = "Line 1\nLine 2"
        report_b = "Line 1\nLine 3"
        result = mixin.diff_reports(report_a, report_b)
        assert "+" in result.summary or "-" in result.summary


# ---------------------------------------------------------------------------
# Test: merge_reports
# ---------------------------------------------------------------------------


class TestMergeReports:
    """Tests for ParallelMixin.merge_reports()."""

    def test_merge_preserves_all_sections(self, mixin):
        """Merged report should contain sections from both reports."""
        report_a = "## Summary\nSummary from A\n\n## Details\nDetails from A"
        report_b = "## Summary\nSummary from B\n\n## Extra\nExtra section"
        merged = mixin.merge_reports(report_a, report_b)
        assert "## Summary" in merged
        assert "## Details" in merged
        assert "## Extra" in merged

    def test_merge_combines_unique_sections(self, mixin):
        """Sections only in B should be appended."""
        report_a = "## Summary\nSummary A"
        report_b = "## Summary\nSummary B\n\n## Analysis\nAnalysis B"
        merged = mixin.merge_reports(report_a, report_b)
        assert "## Analysis" in merged

    def test_merge_overlapping_sections(self, mixin):
        """Overlapping sections should combine A first, then B's additions."""
        report_a = "## Summary\nSummary A content"
        report_b = "## Summary\nSummary B content"
        merged = mixin.merge_reports(report_a, report_b)
        assert "Summary A content" in merged
        # B's additions should be in Ergänzungen section
        assert "Ergänzungen" in merged or "Summary B content" in merged


# ---------------------------------------------------------------------------
# Test: ParallelResult
# ---------------------------------------------------------------------------


class TestParallelResult:
    """Tests for ParallelResult dataclass."""

    def test_parallel_result_defaults(self):
        result = ParallelResult()
        assert result.primary_result is None
        assert result.secondary_result is None
        assert result.merged_result is None
        assert result.strategy_used == ParallelStrategy.PRIMARY_FIRST
        assert result.error is None

    def test_parallel_result_to_dict(self):
        result = ParallelResult(
            primary_result="test",
            strategy_used=ParallelStrategy.AGGREGATE,
            primary_model="gemma4:e2b",
            secondary_model="google/gemma-2-2b-it",
            primary_duration_ms=100,
            secondary_duration_ms=120,
        )
        d = result.to_dict()
        assert d["strategy_used"] == "aggregate"
        assert d["primary_model"] == "gemma4:e2b"
        assert d["secondary_model"] == "google/gemma-2-2b-it"
        assert d["has_diff"] is False

    def test_parallel_result_with_diff(self):
        diff = DiffResult(complement_count=2, conflict_count=0, has_conflicts=False)
        result = ParallelResult(diff_result=diff)
        d = result.to_dict()
        assert d["has_diff"] is True
        assert d["can_merge"] is True


# ---------------------------------------------------------------------------
# Test: _should_use_parallel
# ---------------------------------------------------------------------------


class TestShouldUseParallel:
    """Tests for _should_use_parallel() detection."""

    def test_parallel_disabled_returns_false(self):
        """When parallel_mode=False, should_use_parallel returns False."""
        config = LLMConfig(
            model_source="ollama",
            parallel_mode=False,
            skip_validation=True,
        )
        m = ParallelMixin()
        m.__init_parallel__(llm_config=config)
        assert m._should_use_parallel() is False

    def test_single_source_returns_false(self):
        """Single-source mode without secondary returns False."""
        config = LLMConfig(
            model_source="ollama",
            parallel_mode=True,
            skip_validation=True,
        )
        m = ParallelMixin()
        m.__init_parallel__(llm_config=config)
        # No secondary engine in ollama mode
        with patch.object(EngineRegistry, '_create_ollama_engine', return_value=Mock(get_provider=Mock(return_value=LLMProvider.OLLAMA), get_model_name=Mock(return_value="gemma4:e2b"), is_available=Mock(return_value=True))):
            registry = EngineRegistry(config=config)
            m._parallel_registry = registry
            assert m._should_use_parallel() is False


# ---------------------------------------------------------------------------
# Test: _split_report_sections
# ---------------------------------------------------------------------------


class TestSplitReportSections:
    """Tests for the static _split_report_sections method."""

    def test_split_simple_report(self):
        report = "## Summary\nSummary text\n\n## Details\nDetail text"
        sections = ParallelMixin._split_report_sections(report)
        assert "## Summary" in sections
        assert "## Details" in sections

    def test_split_report_with_header(self):
        report = "Header line\n\n## Section 1\nContent"
        sections = ParallelMixin._split_report_sections(report)
        assert "_header" in sections
        assert "## Section 1" in sections

    def test_split_empty_report(self):
        sections = ParallelMixin._split_report_sections("")
        # Should not crash
        assert isinstance(sections, dict)


# ---------------------------------------------------------------------------
# Test: __init_parallel__
# ---------------------------------------------------------------------------


class TestInitParallel:
    """Tests for ParallelMixin initialization."""

    def test_init_with_config(self):
        config = LLMConfig(
            model_source="compare",
            parallel_mode=True,
            parallel_strategy="compare",
            hf_model_name="google/gemma-2-2b-it",
            skip_validation=True,
        )
        m = ParallelMixin()
        m.__init_parallel__(llm_config=config)
        assert m._parallel_strategy == ParallelStrategy.COMPARE

    def test_init_default_strategy(self):
        config = LLMConfig(
            model_source="auto",
            parallel_mode=False,
            skip_validation=True,
        )
        m = ParallelMixin()
        m.__init_parallel__(llm_config=config)
        assert m._parallel_strategy == ParallelStrategy.PRIMARY_FIRST

    def test_init_aggregate_strategy(self):
        config = LLMConfig(
            model_source="compare",
            parallel_mode=True,
            parallel_strategy="aggregate",
            hf_model_name="google/gemma-2-2b-it",
            skip_validation=True,
        )
        m = ParallelMixin()
        m.__init_parallel__(llm_config=config)
        assert m._parallel_strategy == ParallelStrategy.AGGREGATE


if __name__ == "__main__":
    pytest.main([__file__, "-v"])