#!/usr/bin/env python3
"""
ParallelMixin - Diff-View and Merge Logic for Multi-Engine Generation

Provides reusable diff comparison and merge functionality for generators
that support parallel mode (primary_first, aggregate, compare).

Strategies:
- primary_first: Primary engine runs; on failure, secondary takes over.
- aggregate: Both engines generate; results are combined (union).
- compare: Both engines generate; differences are shown (diff-view)
  and results are merged if they complement each other.

Usage:
    from kb.biblio.generator.parallel_mixin import ParallelMixin, DiffResult

    class MyGenerator(ParallelMixin):
        ...

    result = generator.diff_essences(essence_a, essence_b)
    merged = generator.merge_essences(essence_a, essence_b)
"""

import asyncio
import difflib
import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Tuple

from kb.biblio.engine.base import BaseLLMEngine, LLMResponse
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError, get_engine_registry
from kb.biblio.config import LLMConfig, get_llm_config

logger = logging.getLogger(__name__)


class ParallelStrategy(Enum):
    """Supported parallel generation strategies."""
    PRIMARY_FIRST = "primary_first"
    AGGREGATE = "aggregate"
    COMPARE = "compare"


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


@dataclass
class ParallelResult:
    """Result from parallel generation with one or two engines."""
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
    
    def to_dict(self) -> Dict[str, Any]:
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


class ParallelMixin:
    """
    Mixin providing parallel generation capabilities for generators.
    
    Subclass must implement:
        - _generate_single(topic, source_files, engine, **kwargs) -> result
    
    This mixin adds:
        - _generate_parallel(topic, source_files, strategy, **kwargs) -> ParallelResult
        - diff_essences(a, b) -> DiffResult
        - merge_essences(a, b, diff_result) -> merged dict
        - diff_reports(a, b) -> DiffResult
        - merge_reports(a, b, diff_result) -> merged dict
    """
    
    def __init_parallel__(
        self,
        llm_config: Optional[LLMConfig] = None,
    ):
        """Initialize parallel support. Call in generator __init__."""
        self._parallel_config = llm_config or get_llm_config()
        self._parallel_strategy = ParallelStrategy(
            self._parallel_config.parallel_strategy
        ) if self._parallel_config.parallel_strategy in (
            "primary_first", "aggregate", "compare"
        ) else ParallelStrategy.PRIMARY_FIRST
        
        self._parallel_registry: Optional[EngineRegistry] = None
    
    def _get_parallel_registry(self) -> EngineRegistry:
        """Get or lazily create the engine registry."""
        if self._parallel_registry is None:
            self._parallel_registry = get_engine_registry()
        return self._parallel_registry
    
    def _get_parallel_engines(self) -> Tuple[BaseLLMEngine, Optional[BaseLLMEngine]]:
        """Get primary and secondary engines from registry."""
        registry = self._get_parallel_registry()
        return registry.get_both()
    
    def _should_use_parallel(self) -> bool:
        """Check if parallel mode is enabled and a secondary engine is available."""
        if not self._parallel_config.parallel_mode:
            return False
        try:
            _, secondary = self._get_parallel_engines()
            return secondary is not None
        except EngineRegistryError:
            return False
    
    # ---- Diff Logic ----
    
    def diff_essences(self, essence_a: Dict[str, Any], essence_b: Dict[str, Any]) -> DiffResult:
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
        diffs = []
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
                # Both have content but different - this is a conflict for string fields
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
        
        for field, item_name in list_fields.items():
            list_a = set(str(x).strip().lower() for x in essence_a.get(field, []))
            list_b = set(str(x).strip().lower() for x in essence_b.get(field, []))
            
            # Get original values for reference
            orig_a = {str(x).strip(): x for x in essence_a.get(field, [])}
            orig_b = {str(x).strip(): x for x in essence_b.get(field, [])}
            
            only_a = list_a - list_b  # In A, not in B
            only_b = list_b - list_a  # In B, not in A
            common = list_a & list_b  # In both
            
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
            set_a = set(
                f"{r.get('from','')}→{r.get('type','')}→{r.get('to','')}"
                for r in rels_a if isinstance(r, dict)
            )
            set_b = set(
                f"{r.get('from','')}→{r.get('type','')}→{r.get('to','')}"
                for r in rels_b if isinstance(r, dict)
            )
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
            diffs=diffs,
            summary=summary,
            has_conflicts=has_conflicts,
            complement_count=complement_count,
            conflict_count=conflict_count,
            unchanged_count=unchanged_count,
        )
    
    def merge_essences(
        self,
        essence_a: Dict[str, Any],
        essence_b: Dict[str, Any],
        diff_result: Optional[DiffResult] = None,
    ) -> Dict[str, Any]:
        """
        Merge two essence dicts, combining complementary results.
        
        Merges list fields by union, keeps the longer/more informative
        string field. Only merges if diff_result.can_merge is True.
        
        Args:
            essence_a: Primary essence dict
            essence_b: Secondary essence dict
            diff_result: Pre-computed diff. If None, computed automatically.
            
        Returns:
            Merged essence dict
        """
        if diff_result is None:
            diff_result = self.diff_essences(essence_a, essence_b)
        
        merged = {}
        
        # String fields: prefer longer/more informative
        for field in ("summary",):
            val_a = essence_a.get(field, "")
            val_b = essence_b.get(field, "")
            if not val_a:
                merged[field] = val_b
            elif not val_b:
                merged[field] = val_a
            elif len(val_b) > len(val_a) * 1.2:
                # B is significantly more detailed, prefer it
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
            seen = set()
            merged_list = []
            for item in list_a + list_b:
                key = str(item).strip().lower()
                if key not in seen:
                    seen.add(key)
                    merged_list.append(item)
            merged[field] = merged_list
        
        # Relationships: union merge
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
        
        diffs = []
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
        
        has_conflicts = False  # Text diffs don't inherently conflict
        
        summary = f"+{added}/-{removed} lines changed"
        
        return DiffResult(
            diffs=diffs,
            summary=summary,
            has_conflicts=has_conflicts,
            complement_count=added + removed,
            conflict_count=0,
            unchanged_count=max(len(lines_a), len(lines_b)) - added - removed,
        )
    
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
        # Split into sections by ## headings
        sections_a = self._split_report_sections(report_a)
        sections_b = self._split_report_sections(report_b)
        
        # Combine sections: A's versions first, then B's unique sections
        merged_sections = {}
        section_order = []
        
        for title, content in sections_a.items():
            merged_sections[title] = content
            section_order.append(title)
        
        for title, content in sections_b.items():
            if title in merged_sections:
                # Both have this section - append B's additions if different
                if content.strip() != merged_sections[title].strip():
                    merged_sections[title] = (
                        merged_sections[title].rstrip() +
                        "\n\n--- Ergänzungen (sekundäres Modell) ---\n\n" +
                        content.strip() + "\n"
                    )
            else:
                merged_sections[title] = content
                section_order.append(title)
        
        # Reconstruct report
        parts = []
        for title in section_order:
            content = merged_sections[title]
            if content.strip():
                parts.append(content.strip())
        
        return "\n\n".join(parts) + "\n"
    
    @staticmethod
    def _split_report_sections(report: str) -> Dict[str, str]:
        """
        Split a report into sections by ## headings.
        
        Returns:
            Dict mapping section title to full section text (including heading)
        """
        sections = {}
        current_title = "_header"
        current_lines = []
        
        for line in report.splitlines(keepends=False):
            if line.startswith("## "):
                # Save previous section
                if current_lines:
                    sections[current_title] = "\n".join(current_lines)
                current_title = line.strip()
                current_lines = [line]
            else:
                current_lines.append(line)
        
        # Save last section
        if current_lines:
            sections[current_title] = "\n".join(current_lines)
        
        return sections
    
    # ---- Parallel Generation Dispatch ----
    
    async def _generate_with_strategy(
        self,
        prompt: str,
        strategy: Optional[ParallelStrategy] = None,
        **kwargs,
    ) -> ParallelResult:
        """
        Generate LLM response using the configured parallel strategy.
        
        Args:
            prompt: The generation prompt
            strategy: Override the default strategy
            **kwargs: Additional arguments passed to generate_async
            
        Returns:
            ParallelResult with generation details
        """
        effective_strategy = strategy or self._parallel_strategy
        
        # If not in parallel mode, just use primary engine
        if not self._should_use_parallel():
            return await self._generate_primary_only(prompt, **kwargs)
        
        if effective_strategy == ParallelStrategy.PRIMARY_FIRST:
            return await self._generate_primary_first(prompt, **kwargs)
        elif effective_strategy == ParallelStrategy.AGGREGATE:
            return await self._generate_aggregate(prompt, **kwargs)
        elif effective_strategy == ParallelStrategy.COMPARE:
            return await self._generate_compare(prompt, **kwargs)
        else:
            # Fallback to primary only
            return await self._generate_primary_only(prompt, **kwargs)
    
    async def _generate_primary_only(self, prompt: str, **kwargs) -> ParallelResult:
        """Generate using only the primary engine."""
        import time
        start = time.time()
        
        primary, _ = self._get_parallel_engines()
        response = await primary.generate_async(prompt, **kwargs)
        
        return ParallelResult(
            primary_result=response,
            strategy_used=ParallelStrategy.PRIMARY_FIRST,
            primary_model=primary.get_model_name(),
            primary_duration_ms=int((time.time() - start) * 1000),
        )
    
    async def _generate_primary_first(self, prompt: str, **kwargs) -> ParallelResult:
        """
        Primary-first strategy: try primary, fall back to secondary on failure.
        """
        import time
        start = time.time()
        
        primary, secondary = self._get_parallel_engines()
        
        try:
            response = await primary.generate_async(prompt, **kwargs)
            if response.success and response.content:
                return ParallelResult(
                    primary_result=response,
                    strategy_used=ParallelStrategy.PRIMARY_FIRST,
                    primary_model=primary.get_model_name(),
                    primary_duration_ms=int((time.time() - start) * 1000),
                )
        except Exception as e:
            logger.warning(
                "Primary engine failed, falling back to secondary: %s", e
            )
        
        # Fall back to secondary
        if secondary is None:
            return ParallelResult(
                error="Primary engine failed and no secondary available",
                strategy_used=ParallelStrategy.PRIMARY_FIRST,
                primary_model=primary.get_model_name(),
                primary_duration_ms=int((time.time() - start) * 1000),
            )
        
        try:
            response = await secondary.generate_async(prompt, **kwargs)
            return ParallelResult(
                secondary_result=response,
                strategy_used=ParallelStrategy.PRIMARY_FIRST,
                primary_model=primary.get_model_name(),
                secondary_model=secondary.get_model_name(),
                primary_duration_ms=int((time.time() - start) * 1000),
            )
        except Exception as e:
            return ParallelResult(
                error=f"Both engines failed. Secondary error: {e}",
                strategy_used=ParallelStrategy.PRIMARY_FIRST,
                primary_model=primary.get_model_name(),
                secondary_model=secondary.get_model_name() if secondary else None,
                primary_duration_ms=int((time.time() - start) * 1000),
            )
    
    async def _generate_aggregate(self, prompt: str, **kwargs) -> ParallelResult:
        """
        Aggregate strategy: both engines generate, results are combined.
        """
        import time
        start = time.time()
        
        primary, secondary = self._get_parallel_engines()
        
        # Run both in parallel
        tasks = [primary.generate_async(prompt, **kwargs)]
        if secondary is not None:
            tasks.append(secondary.generate_async(prompt, **kwargs))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        primary_response = results[0] if not isinstance(results[0], Exception) else None
        secondary_response = results[1] if len(results) > 1 and not isinstance(results[1], Exception) else None
        
        duration_ms = int((time.time() - start) * 1000)
        
        if primary_response is None and secondary_response is None:
            return ParallelResult(
                error="Both engines failed in aggregate mode",
                strategy_used=ParallelStrategy.AGGREGATE,
                primary_duration_ms=duration_ms,
            )
        
        return ParallelResult(
            primary_result=primary_response,
            secondary_result=secondary_response,
            strategy_used=ParallelStrategy.AGGREGATE,
            primary_model=primary.get_model_name(),
            secondary_model=secondary.get_model_name() if secondary else None,
            primary_duration_ms=duration_ms,
        )
    
    async def _generate_compare(self, prompt: str, **kwargs) -> ParallelResult:
        """
        Compare strategy: both engines generate, diff-view is created,
        and results are merged if they complement each other.
        """
        import time
        start = time.time()
        
        primary, secondary = self._get_parallel_engines()
        
        if secondary is None:
            # No secondary available, just use primary
            response = await primary.generate_async(prompt, **kwargs)
            return ParallelResult(
                primary_result=response,
                strategy_used=ParallelStrategy.COMPARE,
                primary_model=primary.get_model_name(),
                primary_duration_ms=int((time.time() - start) * 1000),
            )
        
        # Run both in parallel
        primary_task = primary.generate_async(prompt, **kwargs)
        secondary_task = secondary.generate_async(prompt, **kwargs)
        
        primary_response, secondary_response = await asyncio.gather(
            primary_task, secondary_task, return_exceptions=True
        )
        
        if isinstance(primary_response, Exception):
            primary_response = None
        if isinstance(secondary_response, Exception):
            secondary_response = None
        
        duration_ms = int((time.time() - start) * 1000)
        
        result = ParallelResult(
            primary_result=primary_response,
            secondary_result=secondary_response,
            strategy_used=ParallelStrategy.COMPARE,
            primary_model=primary.get_model_name(),
            secondary_model=secondary.get_model_name(),
            primary_duration_ms=duration_ms,
            secondary_duration_ms=duration_ms,
        )
        
        return result