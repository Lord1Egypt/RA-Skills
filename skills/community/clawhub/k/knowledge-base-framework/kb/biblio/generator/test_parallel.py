#!/usr/bin/env python3
"""
Standalone tests for parallel_mixin diff/merge logic.
No engine imports - pure logic testing.
"""

import difflib
import json
import sys
from pathlib import Path

# ---- Data classes (copied from parallel_mixin for isolated testing) ----

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


class ParallelStrategy(Enum):
    PRIMARY_FIRST = "primary_first"
    AGGREGATE = "aggregate"
    COMPARE = "compare"


class DiffType(Enum):
    ADDED = "added"
    REMOVED = "removed"
    CHANGED = "changed"
    UNCHANGED = "unchanged"


@dataclass
class DiffEntry:
    field: str
    diff_type: DiffType
    value_a: Any = None
    value_b: Any = None

    def to_dict(self):
        return {
            "field": self.field,
            "diff_type": self.diff_type.value,
            "value_a": self.value_a,
            "value_b": self.value_b,
        }


@dataclass
class DiffResult:
    diffs: List[DiffEntry] = field(default_factory=list)
    summary: str = ""
    has_conflicts: bool = False
    complement_count: int = 0
    conflict_count: int = 0
    unchanged_count: int = 0

    @property
    def can_merge(self) -> bool:
        return not self.has_conflicts and self.complement_count > 0

    def to_dict(self):
        return {
            "summary": self.summary,
            "has_conflicts": self.has_conflicts,
            "complement_count": self.complement_count,
            "conflict_count": self.conflict_count,
            "unchanged_count": self.unchanged_count,
            "can_merge": self.can_merge,
            "diffs": [d.to_dict() for d in self.diffs],
        }


@dataclass
class ParallelResult:
    primary_result: Any = None
    secondary_result: Any = None
    merged_result: Any = None
    strategy_used: ParallelStrategy = ParallelStrategy.PRIMARY_FIRST
    primary_model: Optional[str] = None
    secondary_model: Optional[str] = None
    primary_duration_ms: int = 0
    secondary_duration_ms: int = 0
    diff_result: Optional[DiffResult] = None
    error: Optional[str] = None

    def to_dict(self):
        return {
            "strategy_used": self.strategy_used.value,
            "primary_model": self.primary_model,
            "secondary_model": self.secondary_model,
            "primary_duration_ms": self.primary_duration_ms,
            "secondary_duration_ms": self.secondary_duration_ms,
            "has_diff": self.diff_result is not None,
            "can_merge": self.diff_result.can_merge if self.diff_result else None,
            "error": self.error,
        }


# ---- Logic functions (extracted from ParallelMixin for isolated testing) ----

def diff_essences(essence_a: Dict[str, Any], essence_b: Dict[str, Any]) -> DiffResult:
    """Compare two essence dicts and produce a structured diff."""
    diffs = []
    complement_count = 0
    conflict_count = 0
    unchanged_count = 0

    for field in ("summary",):
        val_a = essence_a.get(field, "")
        val_b = essence_b.get(field, "")
        if val_a == val_b:
            unchanged_count += 1
        elif val_a and not val_b:
            diffs.append(DiffEntry(field, DiffType.REMOVED, val_a, val_b))
            complement_count += 1
        elif not val_a and val_b:
            diffs.append(DiffEntry(field, DiffType.ADDED, val_a, val_b))
            complement_count += 1
        else:
            diffs.append(DiffEntry(field, DiffType.CHANGED, val_a, val_b))
            conflict_count += 1

    list_fields = {
        "key_points": "key point",
        "connections": "connection",
        "contradictions": "contradiction",
        "open_questions": "open question",
        "entities": "entity",
        "keywords": "keyword",
    }

    for field, item_name in list_fields.items():
        list_a = set(str(x).strip().lower() for x in essence_a.get(field, []))
        list_b = set(str(x).strip().lower() for x in essence_b.get(field, []))
        orig_a = {str(x).strip(): x for x in essence_a.get(field, [])}
        orig_b = {str(x).strip(): x for x in essence_b.get(field, [])}

        only_a = list_a - list_b
        only_b = list_b - list_a
        common = list_a & list_b
        unchanged_count += len(common)

        if only_a:
            diffs.append(DiffEntry(field, DiffType.REMOVED,
                                    [orig_a.get(x.lower(), x) for x in only_a], None))
            complement_count += len(only_a)

        if only_b:
            diffs.append(DiffEntry(field, DiffType.ADDED, None,
                                    [orig_b.get(x.lower(), x) for x in only_b]))
            complement_count += len(only_b)

    rels_a = essence_a.get("relationships", [])
    rels_b = essence_b.get("relationships", [])
    if rels_a or rels_b:
        set_a = set(f"{r.get('from','')}→{r.get('type','')}→{r.get('to','')}" for r in rels_a if isinstance(r, dict))
        set_b = set(f"{r.get('from','')}→{r.get('type','')}→{r.get('to','')}" for r in rels_b if isinstance(r, dict))
        only_a = set_a - set_b
        only_b = set_b - set_a
        common = set_a & set_b
        unchanged_count += len(common)
        if only_a:
            diffs.append(DiffEntry("relationships", DiffType.REMOVED, sorted(only_a), None))
            complement_count += len(only_a)
        if only_b:
            diffs.append(DiffEntry("relationships", DiffType.ADDED, None, sorted(only_b)))
            complement_count += len(only_b)

    has_conflicts = conflict_count > 0
    summary_parts = []
    if complement_count:
        summary_parts.append(f"{complement_count} complementary difference(s)")
    if conflict_count:
        summary_parts.append(f"{conflict_count} conflict(s)")
    if unchanged_count:
        summary_parts.append(f"{unchanged_count} field(s) identical")
    summary = "; ".join(summary_parts) if summary_parts else "No differences found"

    return DiffResult(
        diffs=diffs, summary=summary, has_conflicts=has_conflicts,
        complement_count=complement_count, conflict_count=conflict_count,
        unchanged_count=unchanged_count,
    )


def merge_essences(essence_a, essence_b, diff_result=None):
    """Merge two essence dicts, combining complementary results."""
    if diff_result is None:
        diff_result = diff_essences(essence_a, essence_b)

    merged = {}
    for field in ("summary",):
        val_a = essence_a.get(field, "")
        val_b = essence_b.get(field, "")
        if not val_a:
            merged[field] = val_b
        elif not val_b:
            merged[field] = val_a
        elif len(val_b) > len(val_a) * 1.2:
            merged[field] = val_b
        else:
            merged[field] = val_a

    for field in ("key_points", "connections", "contradictions", "open_questions", "entities", "keywords"):
        list_a = essence_a.get(field, [])
        list_b = essence_b.get(field, [])
        seen = set()
        merged_list = []
        for item in list_a + list_b:
            key = str(item).strip().lower()
            if key not in seen:
                seen.add(key)
                merged_list.append(item)
        merged[field] = merged_list

    rels_a = essence_a.get("relationships", [])
    rels_b = essence_b.get("relationships", [])
    seen_rels = set()
    merged_rels = []
    for r in rels_a + rels_b:
        if isinstance(r, dict):
            key = f"{r.get('from','')}→{r.get('type','')}→{r.get('to','')}"
            if key not in seen_rels:
                seen_rels.add(key)
                merged_rels.append(r)
    merged["relationships"] = merged_rels

    return merged


def diff_reports(report_a: str, report_b: str) -> DiffResult:
    """Compare two report strings using unified diff."""
    lines_a = report_a.splitlines(keepends=False)
    lines_b = report_b.splitlines(keepends=False)

    diff_lines = list(difflib.unified_diff(
        lines_a, lines_b, fromfile="primary", tofile="secondary", lineterm="",
    ))

    diffs = []
    added = 0
    removed = 0

    for line in diff_lines:
        if line.startswith("+") and not line.startswith("+++"):
            diffs.append(DiffEntry("report_line", DiffType.ADDED, value_b=line[1:]))
            added += 1
        elif line.startswith("-") and not line.startswith("---"):
            diffs.append(DiffEntry("report_line", DiffType.REMOVED, value_a=line[1:]))
            removed += 1

    summary = f"+{added}/-{removed} lines changed"
    return DiffResult(
        diffs=diffs, summary=summary, has_conflicts=False,
        complement_count=added + removed, conflict_count=0,
        unchanged_count=max(len(lines_a), len(lines_b)) - added - removed,
    )


def merge_reports(report_a: str, report_b: str, diff_result=None) -> str:
    """Merge two report strings by combining their sections."""
    sections_a = _split_report_sections(report_a)
    sections_b = _split_report_sections(report_b)

    merged_sections = {}
    section_order = []

    for title, content in sections_a.items():
        merged_sections[title] = content
        section_order.append(title)

    for title, content in sections_b.items():
        if title in merged_sections:
            if content.strip() != merged_sections[title].strip():
                merged_sections[title] = (
                    merged_sections[title].rstrip() +
                    "\n\n--- Ergänzungen (sekundäres Modell) ---\n\n" +
                    content.strip() + "\n"
                )
        else:
            merged_sections[title] = content
            section_order.append(title)

    parts = []
    for title in section_order:
        content = merged_sections[title]
        if content.strip():
            parts.append(content.strip())

    return "\n\n".join(parts) + "\n"


def _split_report_sections(report: str) -> Dict[str, str]:
    sections = {}
    current_title = "_header"
    current_lines = []
    for line in report.splitlines(keepends=False):
        if line.startswith("## "):
            if current_lines:
                sections[current_title] = "\n".join(current_lines)
            current_title = line.strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines:
        sections[current_title] = "\n".join(current_lines)
    return sections


# ==== TESTS ====

def test_diff_essences_identical():
    essence = {
        "summary": "Test summary",
        "key_points": ["point 1", "point 2"],
        "connections": ["A -> B"],
        "contradictions": [],
        "open_questions": ["why?"],
        "entities": ["Entity1"],
        "keywords": ["test", "ml"],
        "relationships": [{"from": "A", "type": "relates", "to": "B"}],
    }
    result = diff_essences(essence, essence)
    assert result.unchanged_count > 0, f"Expected unchanged > 0, got {result.unchanged_count}"
    assert result.conflict_count == 0
    assert result.complement_count == 0
    assert not result.has_conflicts
    assert not result.can_merge


def test_diff_essences_complementary():
    essence_a = {
        "summary": "Summary A",
        "key_points": ["point 1", "point 2"],
        "connections": ["A -> B"],
        "contradictions": [],
        "open_questions": ["why?"],
        "entities": ["Entity1"],
        "keywords": ["test", "ml"],
        "relationships": [{"from": "A", "type": "relates", "to": "B"}],
    }
    essence_b = {
        "summary": "Summary A",
        "key_points": ["point 1", "point 3"],
        "connections": ["A -> B", "C -> D"],
        "contradictions": ["X contradicts Y"],
        "open_questions": ["why?"],
        "entities": ["Entity1", "Entity2"],
        "keywords": ["test", "ml", "ai"],
        "relationships": [
            {"from": "A", "type": "relates", "to": "B"},
            {"from": "C", "type": "depends", "to": "D"},
        ],
    }
    result = diff_essences(essence_a, essence_b)
    assert result.complement_count > 0, f"Expected complement > 0, got {result.complement_count}"
    assert result.conflict_count == 0
    assert not result.has_conflicts
    assert result.can_merge


def test_diff_essences_conflict():
    essence_a = {
        "summary": "Summary A is short",
        "key_points": ["point 1"],
        "connections": [],
        "contradictions": [],
        "open_questions": [],
        "entities": [],
        "keywords": [],
        "relationships": [],
    }
    essence_b = {
        "summary": "Summary B is completely different and longer",
        "key_points": ["point 2"],
        "connections": [],
        "contradictions": [],
        "open_questions": [],
        "entities": [],
        "keywords": [],
        "relationships": [],
    }
    result = diff_essences(essence_a, essence_b)
    assert result.conflict_count >= 1, f"Expected conflicts, got {result.conflict_count}"
    assert result.has_conflicts
    assert not result.can_merge


def test_merge_essences():
    essence_a = {
        "summary": "Summary A",
        "key_points": ["point 1", "point 2"],
        "connections": ["A -> B"],
        "contradictions": [],
        "open_questions": ["why?"],
        "entities": ["Entity1"],
        "keywords": ["test", "ml"],
        "relationships": [{"from": "A", "type": "relates", "to": "B"}],
    }
    essence_b = {
        "summary": "Summary A",
        "key_points": ["point 1", "point 3"],
        "connections": ["C -> D"],
        "contradictions": ["X contradicts Y"],
        "open_questions": ["how?"],
        "entities": ["Entity2"],
        "keywords": ["ai"],
        "relationships": [{"from": "C", "type": "depends", "to": "D"}],
    }
    merged = merge_essences(essence_a, essence_b)

    assert "point 1" in merged["key_points"]
    assert "point 2" in merged["key_points"]
    assert "point 3" in merged["key_points"]
    assert len(merged["key_points"]) == 3

    assert "A -> B" in merged["connections"]
    assert "C -> D" in merged["connections"]

    assert "X contradicts Y" in merged["contradictions"]
    assert "why?" in merged["open_questions"]
    assert "how?" in merged["open_questions"]
    assert "Entity1" in merged["entities"]
    assert "Entity2" in merged["entities"]
    assert "test" in merged["keywords"]
    assert "ml" in merged["keywords"]
    assert "ai" in merged["keywords"]

    assert len(merged["relationships"]) == 2


def test_merge_essences_prefers_longer_summary():
    essence_a = {
        "summary": "Short summary",
        "key_points": [], "connections": [], "contradictions": [],
        "open_questions": [], "entities": [], "keywords": [], "relationships": [],
    }
    essence_b = {
        "summary": "This is a much more detailed and comprehensive summary that provides significantly more context and information about the topic",
        "key_points": [], "connections": [], "contradictions": [],
        "open_questions": [], "entities": [], "keywords": [], "relationships": [],
    }
    merged = merge_essences(essence_a, essence_b)
    assert "detailed" in merged["summary"], f"Expected longer summary, got: {merged['summary']}"


def test_diff_reports():
    report_a = """## Summary
This is the primary summary.

## Key Findings
- Finding 1
- Finding 2
"""
    report_b = """## Summary
This is the secondary summary.

## Key Findings
- Finding 1
- Finding 3

## Additional Section
Extra content here.
"""
    result = diff_reports(report_a, report_b)
    assert result.complement_count > 0
    assert isinstance(result.summary, str)
    assert "+" in result.summary or "-" in result.summary or "0" in result.summary


def test_merge_reports():
    report_a = """## Summary
This is the primary summary.

## Key Findings
- Finding 1
- Finding 2
"""
    report_b = """## Summary
This is the secondary summary.

## Key Findings
- Finding 1
- Finding 3

## Additional Section
Extra content here.
"""
    merged = merge_reports(report_a, report_b)
    assert "primary" in merged
    assert "Additional" in merged or "additional" in merged.lower()


def test_parallel_strategy_enum():
    assert ParallelStrategy.PRIMARY_FIRST.value == "primary_first"
    assert ParallelStrategy.AGGREGATE.value == "aggregate"
    assert ParallelStrategy.COMPARE.value == "compare"


def test_diff_type_enum():
    assert DiffType.ADDED.value == "added"
    assert DiffType.REMOVED.value == "removed"
    assert DiffType.CHANGED.value == "changed"
    assert DiffType.UNCHANGED.value == "unchanged"


def test_diff_result_can_merge():
    result = DiffResult(
        diffs=[DiffEntry("test", DiffType.ADDED, None, "value")],
        complement_count=1, conflict_count=0,
    )
    assert result.can_merge

    result2 = DiffResult(
        diffs=[DiffEntry("test", DiffType.CHANGED, "a", "b")],
        complement_count=0, conflict_count=1, has_conflicts=True,
    )
    assert not result2.can_merge

    result3 = DiffResult(complement_count=0, conflict_count=0)
    assert not result3.can_merge


def test_parallel_result_to_dict():
    result = ParallelResult(
        primary_result="content",
        strategy_used=ParallelStrategy.AGGREGATE,
        primary_model="gpt-4",
        secondary_model="claude-3",
        primary_duration_ms=500,
        secondary_duration_ms=600,
    )
    d = result.to_dict()
    assert d["strategy_used"] == "aggregate"
    assert d["primary_model"] == "gpt-4"
    assert d["secondary_model"] == "claude-3"


def test_source_structure():
    """Verify the actual source files have all required components."""
    _gen_dir = Path(__file__).resolve().parent
    mixin_path = _gen_dir / "parallel_mixin.py"
    essence_path = _gen_dir / "essence_generator.py"
    report_path = _gen_dir / "report_generator.py"
    init_path = _gen_dir / "__init__.py"

    with open(mixin_path) as f:
        mixin_src = f.read()

    required_in_mixin = [
        "class ParallelStrategy",
        "class DiffType",
        "class DiffEntry",
        "class DiffResult",
        "class ParallelResult",
        "class ParallelMixin",
        "def diff_essences",
        "def merge_essences",
        "def diff_reports",
        "def merge_reports",
        "def _generate_with_strategy",
        "def _generate_primary_first",
        "def _generate_aggregate",
        "def _generate_compare",
        "def _should_use_parallel",
        "def _get_parallel_engines",
    ]
    for req in required_in_mixin:
        assert req in mixin_src, f"Missing in parallel_mixin.py: {req}"

    with open(essence_path) as f:
        essence_src = f.read()

    required_in_essence = [
        "class EssenzGenerator(ParallelMixin)",
        "def generate_essence_parallel",
        "def _process_primary_first_result",
        "def _process_aggregate_result",
        "def _process_compare_result",
        "__init_parallel__",
        "ParallelStrategy",
        "EngineRegistry",
    ]
    for req in required_in_essence:
        assert req in essence_src, f"Missing in essence_generator.py: {req}"

    with open(report_path) as f:
        report_src = f.read()

    required_in_report = [
        "class ReportGenerator(ParallelMixin)",
        "def generate_report_parallel",
        "def _aggregate_report_responses",
        "def _compare_report_responses",
        "__init_parallel__",
        "ParallelStrategy",
    ]
    for req in required_in_report:
        assert req in report_src, f"Missing in report_generator.py: {req}"

    with open(init_path) as f:
        init_src = f.read()

    required_in_init = [
        "ParallelMixin",
        "ParallelStrategy",
        "ParallelResult",
        "DiffResult",
        "DiffEntry",
        "DiffType",
    ]
    for req in required_in_init:
        assert req in init_src, f"Missing in __init__.py: {req}"


def test_syntax_all_files():
    """Verify all modified files have valid Python syntax."""
    import ast
    _gen_dir = Path(__file__).resolve().parent
    files = [
        _gen_dir / "parallel_mixin.py",
        _gen_dir / "essence_generator.py",
        _gen_dir / "report_generator.py",
        _gen_dir / "__init__.py",
    ]
    for fpath in files:
        with open(fpath) as f:
            src = f.read()
        try:
            ast.parse(src)
        except SyntaxError as e:
            raise AssertionError(f"Syntax error in {fpath}: {e}")


# ==== RUN ====

if __name__ == "__main__":
    tests = [
        ("Source structure validation", test_source_structure),
        ("Syntax validation", test_syntax_all_files),
        ("Identical essence diff", test_diff_essences_identical),
        ("Complementary essence diff", test_diff_essences_complementary),
        ("Conflicting essence diff", test_diff_essences_conflict),
        ("Essence merge", test_merge_essences),
        ("Merge prefers longer summary", test_merge_essences_prefers_longer_summary),
        ("Report diff", test_diff_reports),
        ("Report merge", test_merge_reports),
        ("ParallelStrategy enum", test_parallel_strategy_enum),
        ("DiffType enum", test_diff_type_enum),
        ("DiffResult.can_merge", test_diff_result_can_merge),
        ("ParallelResult.to_dict", test_parallel_result_to_dict),
    ]

    print("=" * 60)
    print("Running Phase 3: Parallel Generator Tests")
    print("=" * 60)

    passed = 0
    failed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed! ✅")
    else:
        print(f"{failed} test(s) FAILED ❌")
    print("=" * 60)