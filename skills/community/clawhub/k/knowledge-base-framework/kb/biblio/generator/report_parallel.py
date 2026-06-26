#!/usr/bin/env python3
"""
Parallel Report Generation Strategies

Handles parallel engine strategies for report generation:
- primary_first: Try primary, fallback to secondary on failure
- aggregate: Both engines generate, results combined
- compare: Both generate, diff-view + merge if complementary
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from kb.biblio.engine.registry import EngineRegistry
from kb.biblio.generator.parallel_mixin import (
    ParallelMixin, ParallelResult, ParallelStrategy,
)
from kb.biblio.generator.report_models import ReportGeneratorError, ReportGenerationResult
from kb.base.logger import get_logger

logger = get_logger("kb.llm.generator.report.parallel")


class ParallelReportMixin(ParallelMixin):
    """
    Mixin providing parallel report generation strategies.

    Intended to be mixed into ReportGenerator alongside ParallelMixin.
    Provides generate_report_parallel() and helper methods.
    """

    async def generate_report_parallel(
        self,
        report_type: str,
        period_start: datetime,
        period_end: datetime,
        *,
        strategy: Optional[str] = None,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
    ) -> ReportGenerationResult:
        """
        Generate a report using parallel engine strategies.

        When parallel_mode is enabled and a secondary engine is available,
        uses the specified strategy:
        - "primary_first": Try primary, fallback to secondary on failure
        - "aggregate": Both engines generate, results combined
        - "compare": Both generate, diff-view + merge if complementary

        Falls back to single-engine generation if parallel mode is disabled.

        Args:
            report_type: One of "daily", "weekly", "monthly"
            period_start: Start of the period
            period_end: End of the period
            strategy: Override strategy ("primary_first", "aggregate", "compare")
            tags: Optional tags for categorization
            on_progress: Optional progress callback(stage, detail)

        Returns:
            ReportGenerationResult with success status and details
        """
        start_time = time.time()

        # Resolve strategy
        if strategy is not None:
            effective_strategy = ParallelStrategy(strategy)
        else:
            effective_strategy = self._parallel_strategy

        logger.info(
            f"Generating parallel {report_type} report",
            extra={
                "report_type": report_type,
                "strategy": effective_strategy.value,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
            }
        )

        # If not in parallel mode or no secondary engine, fall back to standard
        if not self._should_use_parallel():
            logger.info("Parallel mode disabled or no secondary engine, using standard generation")
            return await self.generate_report(
                report_type=report_type,
                period_start=period_start,
                period_end=period_end,
                tags=tags,
                on_progress=on_progress,
            )

        try:
            # Collect data (same as standard generation)
            if on_progress:
                on_progress("collecting", "Lese Essenzen...")

            essences = await self._collect_essences_for_period(period_start, period_end)
            hotspots = self._compute_hotspots(essences)

            # Build prompt based on type
            if on_progress:
                on_progress("building_prompt", "Erstelle Prompt...")

            prompt = await self._build_prompt_for_type(
                report_type, essences, hotspots, period_start, period_end
            )

            # Generate with strategy
            if on_progress:
                on_progress("generating", "Generiere Bericht via parallelem LLM...")

            parallel_result = await self._generate_with_strategy(
                prompt, effective_strategy
            )

            # Process result based on strategy
            report_content, model_used = self._process_parallel_result(
                effective_strategy, parallel_result
            )

            # Save report
            if on_progress:
                on_progress("saving", "Speichere Bericht...")

            sections = self._extract_sections(report_content, report_type)
            title = self._build_report_title(report_type, period_start, period_end)
            query = (
                f"{report_type.capitalize()} Report für "
                f"{period_start.strftime('%Y-%m-%d')} – {period_end.strftime('%Y-%m-%d')}"
            )
            source_hashes = [e.get("hash", "") for e in essences if e.get("hash")]

            report_path = await self._content_manager.save_report(
                title=title,
                content=report_content,
                query=query,
                report_type=report_type,
                source_hashes=source_hashes,
                model_used=model_used,
                related_topics=[hs["topic"] for hs in hotspots[:5]],
                tags=tags or [],
            )

            # Save diff metadata for compare mode
            if effective_strategy == ParallelStrategy.COMPARE and parallel_result.diff_result:
                diff_path = report_path.parent / "diff.json" if hasattr(report_path, 'parent') else None
                if diff_path:
                    diff_path.write_text(
                        json.dumps(parallel_result.diff_result.to_dict(), indent=2, ensure_ascii=False),
                        encoding="utf-8"
                    )

            # Monthly graph data
            if report_type == self.MONTHLY:
                graph_data = self._generate_graph_data(
                    essences, hotspots, period_start, period_end
                )
                await self._save_graph_data(graph_data, period_start)

            duration_ms = int((time.time() - start_time) * 1000)

            if on_progress:
                on_progress("complete", f"Bericht erstellt: {report_path.name}")

            return ReportGenerationResult(
                report_type=report_type,
                success=True,
                report_path=report_path,
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                sections_included=sections,
                model_used=model_used,
                duration_ms=duration_ms,
                sources_count=len(essences),
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)
            logger.error(
                f"Failed parallel {report_type} report generation",
                extra={
                    "report_type": report_type,
                    "duration_ms": duration_ms,
                    "error": str(e),
                }
            )
            if on_progress:
                on_progress("error", str(e))
            return ReportGenerationResult(
                report_type=report_type,
                success=False,
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                model_used=self._config.model,
                duration_ms=duration_ms,
                error=str(e),
            )

    def _process_parallel_result(
        self,
        strategy: ParallelStrategy,
        parallel_result: ParallelResult,
    ) -> tuple:
        """
        Process parallel result based on strategy.

        Args:
            strategy: The parallel strategy used
            parallel_result: Result from both engines

        Returns:
            Tuple of (report_content, model_used)
        """
        if strategy == ParallelStrategy.PRIMARY_FIRST:
            response = parallel_result.primary_result or parallel_result.secondary_result
            if response is None:
                raise ReportGeneratorError(
                    parallel_result.error or "Both engines failed"
                )
            return response.content, response.model

        elif strategy == ParallelStrategy.AGGREGATE:
            content = self._aggregate_report_responses(parallel_result)
            model_used = f"{parallel_result.primary_model or 'primary'}+{parallel_result.secondary_model or 'secondary'}"
            return content, model_used

        elif strategy == ParallelStrategy.COMPARE:
            return self._compare_report_responses(parallel_result)

        raise ReportGeneratorError(f"Unknown strategy: {strategy}")

    def _aggregate_report_responses(self, parallel_result: ParallelResult) -> str:
        """
        Aggregate two report responses by merging their sections.

        Args:
            parallel_result: ParallelResult with primary and secondary responses

        Returns:
            Merged report content string
        """
        primary_content = ""
        secondary_content = ""

        if parallel_result.primary_result and parallel_result.primary_result.content:
            primary_content = parallel_result.primary_result.content
        if parallel_result.secondary_result and parallel_result.secondary_result.content:
            secondary_content = parallel_result.secondary_result.content

        if not primary_content and not secondary_content:
            raise ReportGeneratorError("Both engines returned empty content")

        if not secondary_content:
            return primary_content
        if not primary_content:
            return secondary_content

        # Merge using ParallelMixin's merge_reports
        return self.merge_reports(primary_content, secondary_content)

    def _compare_report_responses(self, parallel_result: ParallelResult) -> tuple:
        """
        Compare two report responses, create diff-view and merge if complementary.

        Args:
            parallel_result: ParallelResult with both responses

        Returns:
            Tuple of (report_content, model_used)
        """
        primary_content = ""
        secondary_content = ""
        primary_model = parallel_result.primary_model or "primary"
        secondary_model = parallel_result.secondary_model or "secondary"

        if parallel_result.primary_result and parallel_result.primary_result.content:
            primary_content = parallel_result.primary_result.content
        if parallel_result.secondary_result and parallel_result.secondary_result.content:
            secondary_content = parallel_result.secondary_result.content

        if not primary_content and not secondary_content:
            raise ReportGeneratorError("Both engines returned empty content")

        if not secondary_content:
            return primary_content, primary_model
        if not primary_content:
            return secondary_content, secondary_model

        # Compute diff
        diff_result = self.diff_reports(primary_content, secondary_content)
        parallel_result.diff_result = diff_result

        if diff_result.can_merge:
            merged = self.merge_reports(primary_content, secondary_content, diff_result)
            model_used = f"{primary_model}+{secondary_model} (merged)"
            logger.info(
                f"Compare mode: reports merged "
                f"({diff_result.complement_count} complementary, "
                f"{diff_result.conflict_count} conflicts)",
            )
            return merged, model_used
        else:
            # Use primary result when conflicts exist
            logger.info(
                f"Compare mode: conflicts detected "
                f"({diff_result.conflict_count} conflicts, "
                f"{diff_result.complement_count} complementary), "
                f"using primary result",
            )
            return primary_content, f"{primary_model} (conflicts: use primary)"