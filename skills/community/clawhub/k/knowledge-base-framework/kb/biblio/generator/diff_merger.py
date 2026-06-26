#!/usr/bin/env python3
"""
DiffMerger - Diff-View and Merge Logic for LLM Generation Results

Standalone module for comparing and merging essence dictionaries and
report strings from parallel LLM generation.

Provides both a functional API and a DiffMerger class for stateless
diff/merge operations. Used by ParallelMixin and generators for
compare and aggregate strategies.

Core capabilities:
- Compare two essence dicts → structured DiffResult
- Compare two report strings → line-level DiffResult
- Merge two essence dicts → combined essence (union merge)
- Merge two report strings → section-wise merge
- Determine if results complement each other (can_merge)

Usage:
    from kb.biblio.generator.diff_merger import DiffMerger

    merger = DiffMerger()

    # Compare two essences
    diff = merger.diff_essences(essence_a, essence_b)
    print(diff.summary)       # "3 complementary difference(s); 1 conflict(s)"
    print(diff.can_merge)    # True if no conflicts

    # Merge if complementary
    if diff.can_merge:
        merged = merger.merge_essences(essence_a, essence_b, diff)

    # Compare two reports
    diff = merger.diff_reports(report_a, report_b)
    merged = merger.merge_reports(report_a, report_b)
"""

import difflib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DiffType(Enum):
    """Types of differences found during comparison."""
    ADDED = "added"       # Present in B but not A
    REMOVED = "removed"   # Present in A but not B
    CHANGED = "changed"   # Present in both but different
    UNCHANGED = "unchanged"


@dataclass
class DiffEntry:
    """A single difference between two outputs."""
    field: str
    diff_type: DiffType
    value_a: Any = None
    value_b: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "field": self.field,
            "diff_type": self.diff_type.value,
            "value_a": self.value_a,
            "value_b": self.value_b,
        }


@dataclass
class DiffResult:
    """Result of comparing two generated outputs."""
    diffs: List[DiffEntry] = field(default_factory=list)
    summary: str = ""
    has_conflicts: bool = False
    complement_count: int = 0
    conflict_count: int = 0
    unchanged_count: int = 0

    @property
    def can_merge(self) -> bool:
        """Whether the two results can be safely merged."""
        return not self.has_conflicts and self.complement_count > 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "has_conflicts": self.has_conflicts,
            "complement_count": self.complement_count,
            "conflict_count": self.conflict_count,
            "unchanged_count": self.unchanged_count,
            "can_merge": self.can_merge,
            "diffs": [d.to_dict() for d in self.diffs],
        }


class DiffMerger:
    """
    Standalone diff and merge operations for LLM generation results.

    Provides stateless comparison and merging of:
    - Essence dictionaries (structured JSON with list/string fields)
    - Report strings (markdown with ## sections)

    This class is used by ParallelMixin and can also be used directly
    for ad-hoc diff/merge operations outside the parallel context.

    All methods are pure functions with no side effects.
    """

    # ---- Essence Diff ----

    def diff_essences(
        self,
        essence_a: Dict[str, Any],
        essence_b: Dict[str, Any],
    ) -> DiffResult:
        """
        Compare two essence dicts and produce a structured diff.

        Compares all standard essence fields: summary, key_points,
        connections, contradictions, open_questions, entities,
        relationships, keywords.

        Args:
            essence_a: First essence dict (typically from primary engine)
            essence_b: Second essence dict (typically from secondary engine)

        Returns:
            DiffResult with detailed comparison
        """
        diffs: List[DiffEntry] = []
        complement_count = 0
        conflict_count = 0
        unchanged_count = 0

        # String fields: direct comparison
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
                # Both have content but different — conflict for string fields
                diffs.append(DiffEntry(field, DiffType.CHANGED, val_a, val_b))
                conflict_count += 1

        # List fields: item-level comparison
        list_fields = {
            "key_points": "key point",
            "connections": "connection",
            "contradictions": "contradiction",
            "open_questions": "open question",
            "entities": "entity",
            "keywords": "keyword",
        }

        for field, _item_name in list_fields.items():
            set_a = set(str(x).strip().lower() for x in essence_a.get(field, []))
            set_b = set(str(x).strip().lower() for x in essence_b.get(field, []))

            # Original values for reference
            orig_a = {str(x).strip(): x for x in essence_a.get(field, [])}
            orig_b = {str(x).strip(): x for x in essence_b.get(field, [])}

            only_a = set_a - set_b
            only_b = set_b - set_a
            common = set_a & set_b

            unchanged_count += len(common)

            if only_a:
                diffs.append(DiffEntry(
                    field, DiffType.REMOVED,
                    [orig_a.get(x.lower(), x) for x in only_a],
                    None,
                ))
                complement_count += len(only_a)

            if only_b:
                diffs.append(DiffEntry(
                    field, DiffType.ADDED,
                    None,
                    [orig_b.get(x.lower(), x) for x in only_b],
                ))
                complement_count += len(only_b)

        # Relationships: structured comparison
        rels_a = essence_a.get("relationships", [])
        rels_b = essence_b.get("relationships", [])
        if rels_a or rels_b:
            set_a_rel = set(
                f"{r.get('from', '')}→{r.get('type', '')}→{r.get('to', '')}"
                for r in rels_a if isinstance(r, dict)
            )
            set_b_rel = set(
                f"{r.get('from', '')}→{r.get('type', '')}→{r.get('to', '')}"
                for r in rels_b if isinstance(r, dict)
            )
            only_a_rel = set_a_rel - set_b_rel
            only_b_rel = set_b_rel - set_a_rel
            common_rel = set_a_rel & set_b_rel
            unchanged_count += len(common_rel)

            if only_a_rel:
                diffs.append(DiffEntry("relationships", DiffType.REMOVED, sorted(only_a_rel), None))
                complement_count += len(only_a_rel)
            if only_b_rel:
                diffs.append(DiffEntry("relationships", DiffType.ADDED, None, sorted(only_b_rel)))
                complement_count += len(only_b_rel)

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
            diffs=diffs,
            summary=summary,
            has_conflicts=has_conflicts,
            complement_count=complement_count,
            conflict_count=conflict_count,
            unchanged_count=unchanged_count,
        )

    # ---- Essence Merge ----

    def merge_essences(
        self,
        essence_a: Dict[str, Any],
        essence_b: Dict[str, Any],
        diff_result: Optional[DiffResult] = None,
    ) -> Dict[str, Any]:
        """
        Merge two essence dicts, combining complementary results.

        Merges list fields by union, keeps the longer/more informative
        string field. Only merges if diff_result.can_merge is True
        (or if no diff_result is provided, computes it automatically).

        Args:
            essence_a: Primary essence dict
            essence_b: Secondary essence dict
            diff_result: Pre-computed diff. If None, computed automatically.

        Returns:
            Merged essence dict
        """
        if diff_result is None:
            diff_result = self.diff_essences(essence_a, essence_b)

        merged: Dict[str, Any] = {}

        # String fields: prefer longer/more informative
        for field in ("summary",):
            val_a = essence_a.get(field, "")
            val_b = essence_b.get(field, "")
            if not val_a:
                merged[field] = val_b
            elif not val_b:
                merged[field] = val_a
            elif len(val_b) > len(val_a) * 1.2:
                # B is significantly more detailed
                merged[field] = val_b
            else:
                # Prefer A (primary) by default
                merged[field] = val_a

        # List fields: union merge
        list_fields = (
            "key_points", "connections", "contradictions",
            "open_questions", "entities", "keywords",
        )
        for field in list_fields:
            list_a = essence_a.get(field, [])
            list_b = essence_b.get(field, [])
            # Deduplicate by lowercase comparison
            seen: set = set()
            merged_list: list = []
            for item in list_a + list_b:
                key = str(item).strip().lower()
                if key not in seen:
                    seen.add(key)
                    merged_list.append(item)
            merged[field] = merged_list

        # Relationships: union merge
        rels_a = essence_a.get("relationships", [])
        rels_b = essence_b.get("relationships", [])
        seen_rels: set = set()
        merged_rels: list = []
        for r in rels_a + rels_b:
            if isinstance(r, dict):
                key = f"{r.get('from', '')}→{r.get('type', '')}→{r.get('to', '')}"
                if key not in seen_rels:
                    seen_rels.add(key)
                    merged_rels.append(r)
        merged["relationships"] = merged_rels

        return merged

    # ---- Report Diff ----

    def diff_reports(self, report_a: str, report_b: str) -> DiffResult:
        """
        Compare two report strings and produce a text-based diff.

        Uses unified diff format for line-by-line comparison.

        Args:
            report_a: First report content (primary)
            report_b: Second report content (secondary)

        Returns:
            DiffResult with line-level diffs
        """
        lines_a = report_a.splitlines(keepends=False)
        lines_b = report_b.splitlines(keepends=False)

        diff_lines = list(difflib.unified_diff(
            lines_a, lines_b,
            fromfile="primary",
            tofile="secondary",
            lineterm="",
        ))

        diffs: List[DiffEntry] = []
        added = 0
        removed = 0

        for line in diff_lines:
            if line.startswith("+") and not line.startswith("+++"):
                diffs.append(DiffEntry(
                    field="report_line",
                    diff_type=DiffType.ADDED,
                    value_b=line[1:],
                ))
                added += 1
            elif line.startswith("-") and not line.startswith("---"):
                diffs.append(DiffEntry(
                    field="report_line",
                    diff_type=DiffType.REMOVED,
                    value_a=line[1:],
                ))
                removed += 1

        summary = f"+{added}/-{removed} lines changed"

        return DiffResult(
            diffs=diffs,
            summary=summary,
            has_conflicts=False,  # Text diffs don't inherently conflict
            complement_count=added + removed,
            conflict_count=0,
            unchanged_count=max(len(lines_a), len(lines_b)) - added - removed,
        )

    # ---- Report Merge ----

    def merge_reports(
        self,
        report_a: str,
        report_b: str,
        diff_result: Optional[DiffResult] = None,
    ) -> str:
        """
        Merge two report strings by combining their sections.

        Sections unique to each report are kept. Sections appearing in both
        are combined with the primary version first, then secondary additions.

        Args:
            report_a: Primary report content
            report_b: Secondary report content
            diff_result: Pre-computed diff (optional, used for metadata only)

        Returns:
            Merged report string
        """
        sections_a = self._split_report_sections(report_a)
        sections_b = self._split_report_sections(report_b)

        merged_sections: Dict[str, str] = {}
        section_order: list = []

        for title, content in sections_a.items():
            merged_sections[title] = content
            section_order.append(title)

        for title, content in sections_b.items():
            if title in merged_sections:
                # Both have this section — append B's additions if different
                if content.strip() != merged_sections[title].strip():
                    merged_sections[title] = (
                        merged_sections[title].rstrip()
                        + "\n\n--- Ergänzungen (sekundäres Modell) ---\n\n"
                        + content.strip() + "\n"
                    )
            else:
                merged_sections[title] = content
                section_order.append(title)

        parts = [merged_sections[title].strip() for title in section_order
                  if merged_sections[title].strip()]

        return "\n\n".join(parts) + "\n"

    # ---- Helpers ----

    @staticmethod
    def _split_report_sections(report: str) -> Dict[str, str]:
        """
        Split a report into sections by ## headings.

        Returns:
            Dict mapping section title to full section text (including heading)
        """
        sections: Dict[str, str] = {}
        current_title = "_header"
        current_lines: list = []

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

    @staticmethod
    def format_diff(diff_result: DiffResult, verbose: bool = False) -> str:
        """
        Format a DiffResult into a human-readable string.

        Args:
            diff_result: The diff to format
            verbose: If True, include all diff entries

        Returns:
            Formatted string representation
        """
        lines = [
            f"Diff Summary: {diff_result.summary}",
            f"  Can merge: {diff_result.can_merge}",
            f"  Conflicts: {diff_result.conflict_count}",
            f"  Complementary: {diff_result.complement_count}",
            f"  Unchanged: {diff_result.unchanged_count}",
        ]

        if verbose and diff_result.diffs:
            lines.append("")
            lines.append("Details:")
            for entry in diff_result.diffs:
                symbol = {
                    DiffType.ADDED: "+",
                    DiffType.REMOVED: "-",
                    DiffType.CHANGED: "≠",
                    DiffType.UNCHANGED: "=",
                }.get(entry.diff_type, "?")
                lines.append(f"  [{symbol}] {entry.field}")
                if entry.diff_type in (DiffType.CHANGED, DiffType.REMOVED):
                    val_a = entry.value_a
                    if isinstance(val_a, list):
                        val_a = ", ".join(str(x) for x in val_a[:3])
                        if len(entry.value_a) > 3:
                            val_a += f" (+{len(entry.value_a) - 3} more)"
                    lines.append(f"      A: {val_a}")
                if entry.diff_type in (DiffType.CHANGED, DiffType.ADDED):
                    val_b = entry.value_b
                    if isinstance(val_b, list):
                        val_b = ", ".join(str(x) for x in val_b[:3])
                        if len(entry.value_b) > 3:
                            val_b += f" (+{len(entry.value_b) - 3} more)"
                    lines.append(f"      B: {val_b}")

        return "\n".join(lines)


# ---- Module-level convenience functions ----

_default_merger: Optional[DiffMerger] = None


def get_diff_merger() -> DiffMerger:
    """Get or create the default DiffMerger instance."""
    global _default_merger
    if _default_merger is None:
        _default_merger = DiffMerger()
    return _default_merger


def diff_essences(essence_a: Dict[str, Any], essence_b: Dict[str, Any]) -> DiffResult:
    """Convenience function: compare two essence dicts."""
    return get_diff_merger().diff_essences(essence_a, essence_b)


def merge_essences(
    essence_a: Dict[str, Any],
    essence_b: Dict[str, Any],
    diff_result: Optional[DiffResult] = None,
) -> Dict[str, Any]:
    """Convenience function: merge two essence dicts."""
    return get_diff_merger().merge_essences(essence_a, essence_b, diff_result)


def diff_reports(report_a: str, report_b: str) -> DiffResult:
    """Convenience function: compare two report strings."""
    return get_diff_merger().diff_reports(report_a, report_b)


def merge_reports(
    report_a: str,
    report_b: str,
    diff_result: Optional[DiffResult] = None,
) -> str:
    """Convenience function: merge two report strings."""
    return get_diff_merger().merge_reports(report_a, report_b, diff_result)