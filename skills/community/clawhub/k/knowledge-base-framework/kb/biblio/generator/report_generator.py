#!/usr/bin/env python3
"""
ReportGenerator - LLM-powered Report Generation (Orchestration Layer)

Generates daily, weekly, and monthly reports from Knowledge Base content
and extracted essences. This module provides the core orchestration logic,
delegating data collection to aggregators and stats computation to
StatsCalculator.

Extracted submodules:
- aggregators/data_aggregator.py: Essence/report collection & reading
- aggregators/stats_calculator.py: Hotspots, graph data, stats
- report_prompts.py: Prompt building & templates
- report_models.py: Data models & exceptions
- report_parallel.py: Parallel generation strategies

Usage:
    generator = ReportGenerator()

    # Daily report (last 24h)
    result = await generator.generate_daily_report()

    # Weekly report (last 7 days)
    result = await generator.generate_weekly_report()

    # Monthly report (last 30 days)
    result = await generator.generate_monthly_report()

    # Parallel report (when parallel_mode=True in config)
    result = await generator.generate_report_parallel(
        report_type="daily",
        period_start=start,
        period_end=end,
        strategy="compare",
    )
"""

import asyncio
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional, List, Dict, Any

from kb.biblio.config import LLMConfig, get_llm_config
from kb.biblio.engine.base import LLMResponse
from kb.biblio.engine import OllamaEngine, OllamaEngineError
from kb.biblio.engine.registry import EngineRegistry, EngineRegistryError, get_engine_registry
from kb.biblio.content_manager import LLMContentManager
from kb.biblio.generator.parallel_mixin import (
    ParallelMixin, ParallelResult, ParallelStrategy, DiffResult,
)
from kb.biblio.generator.report_parallel import ParallelReportMixin
from kb.biblio.generator.report_models import ReportGeneratorError, ReportGenerationResult
from kb.biblio.generator.report_prompts import (
    load_template,
    default_template,
)
from kb.biblio.generator.aggregators.data_aggregator import ReportDataAggregator
from kb.biblio.generator.aggregators.stats_calculator import StatsCalculator
from kb.base.logger import KBLogger, get_logger

logger = get_logger("kb.llm.generator.report")


class ReportGenerator(ParallelReportMixin, ParallelMixin):
    """
    LLM-powered Report Generator with parallel engine support.

    Generates daily, weekly, and monthly reports from KB content and
    extracted essences. Supports parallel generation strategies when
    parallel_mode is enabled:
    - primary_first: Primary engine for reports; secondary on failure
    - aggregate: Both engines generate, results combined
    - compare: Both generate, diff-view + merge if complementary

    Delegates to:
    - ReportDataAggregator: Data collection and reading
    - StatsCalculator: Hotspot computation, graph data, statistics
    - report_prompts module: Prompt building
    - report_parallel module: Parallel generation strategies
    """

    # Report type constants
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    # Period durations
    PERIOD_HOURS = {
        "daily": 24,
        "weekly": 168,   # 7 * 24
        "monthly": 720,  # 30 * 24
    }

    def __init__(
        self,
        llm_config: Optional[LLMConfig] = None,
        engine: Optional[OllamaEngine] = None,
        content_manager: Optional[LLMContentManager] = None,
        registry: Optional[EngineRegistry] = None,
    ):
        self._config = llm_config or get_llm_config()
        self._engine = engine or OllamaEngine.get_instance()
        self._content_manager = content_manager or LLMContentManager()
        self._template = load_template(self._config.templates_path)

        # Initialize parallel mixin support
        self.__init_parallel__(llm_config)
        if registry is not None:
            self._parallel_registry = registry

        # Initialize sub-components
        self._aggregator = ReportDataAggregator(
            content_manager=self._content_manager,
            essences_path=self._config.essences_path,
        )
        self._stats_calc = StatsCalculator(
            essences_path=self._config.essences_path,
            graph_path=self._config.graph_path,
        )

        logger.info(
            "ReportGenerator initialized",
            extra={
                "model": self._config.model,
                "parallel_mode": self._config.parallel_mode,
                "parallel_strategy": self._config.parallel_strategy,
            }
        )

    # --- Delegation Properties for Backward Compatibility ---

    @property
    def aggregator(self) -> ReportDataAggregator:
        """Access the data aggregator sub-component."""
        return self._aggregator

    @property
    def stats_calculator(self) -> StatsCalculator:
        """Access the stats calculator sub-component."""
        return self._stats_calc

    # --- Data Collection (delegates to ReportDataAggregator) ---

    async def _collect_essences_for_period(
        self,
        period_start: datetime,
        period_end: datetime,
    ) -> List[Dict[str, Any]]:
        """Collect essences for a period. Delegates to ReportDataAggregator."""
        return await self._aggregator.collect_essences_for_period(
            period_start, period_end
        )

    async def _collect_reports_for_period(
        self,
        report_type: str,
        period_start: datetime,
        period_end: datetime,
    ) -> List[Dict[str, Any]]:
        """Collect reports for a period. Delegates to ReportDataAggregator."""
        return await self._aggregator.collect_reports_for_period(
            report_type, period_start, period_end
        )

    async def _read_essence_content(
        self,
        essence_hash: str,
    ) -> Dict[str, Any]:
        """Read essence content. Delegates to ReportDataAggregator."""
        return await self._aggregator.read_essence_content(essence_hash)

    async def _read_report_content(
        self,
        report_path: str,
    ) -> Dict[str, Any]:
        """Read report content. Delegates to ReportDataAggregator."""
        return await self._aggregator.read_report_content(report_path)

    async def _collect_sub_reports(
        self,
        sub_report_type: str,
        period_start: datetime,
        period_end: datetime,
    ) -> List[Dict[str, Any]]:
        """Collect sub-reports. Delegates to ReportDataAggregator."""
        return await self._aggregator.collect_sub_reports(
            sub_report_type, period_start, period_end
        )

    # --- Stats & Graph (delegates to StatsCalculator) ---

    def _compute_hotspots(self, essences):
        """Compute hotspots. Delegates to StatsCalculator."""
        return self._stats_calc.compute_hotspots(essences)

    def _generate_graph_data(
        self,
        essences: List[Dict[str, Any]],
        hotspots: List[Dict[str, str]],
        period_start: datetime,
        period_end: datetime,
    ) -> Dict[str, Any]:
        """Generate graph data. Delegates to StatsCalculator."""
        return self._stats_calc.generate_graph_data(
            essences, hotspots, period_start, period_end
        )

    async def _save_graph_data(
        self,
        graph_data: Dict[str, Any],
        period_start: datetime,
    ) -> Path:
        """Save graph data. Delegates to StatsCalculator."""
        return self._stats_calc.save_graph_data(graph_data, period_start)

    # --- Prompt Building (delegates to report_prompts module) ---

    def _build_daily_prompt(self, essences, hotspots, period_start, period_end):
        """Build daily prompt. Delegates to report_prompts."""
        from kb.biblio.generator.report_prompts import build_daily_prompt
        return build_daily_prompt(
            essences, hotspots, period_start, period_end,
            self._config.essences_path,
        )

    def _build_weekly_prompt(self, daily_reports, essences, hotspots, period_start, period_end):
        """Build weekly prompt. Delegates to report_prompts."""
        from kb.biblio.generator.report_prompts import build_weekly_prompt
        return build_weekly_prompt(
            daily_reports, essences, hotspots, period_start, period_end,
        )

    def _build_monthly_prompt(self, weekly_reports, essences, hotspots, period_start, period_end):
        """Build monthly prompt. Delegates to report_prompts."""
        from kb.biblio.generator.report_prompts import build_monthly_prompt
        return build_monthly_prompt(
            weekly_reports, essences, hotspots, period_start, period_end,
        )

    @staticmethod
    def _default_template():
        """Default template fallback. Delegates to report_prompts."""
        return default_template()

    # --- Retry Logic ---

    async def _generate_with_retry(
        self,
        prompt: str,
        max_retries: Optional[int] = None,
    ) -> LLMResponse:
        """
        Generate LLM response with retry logic and exponential backoff.

        Args:
            prompt: The prompt to send
            max_retries: Override config max_retries

        Returns:
            LLMResponse on success

        Raises:
            ReportGeneratorError: After all retries exhausted
        """
        retries = max_retries if max_retries is not None else self._config.max_retries
        last_error = None

        for attempt in range(retries):
            try:
                response = await self._engine.generate_async(prompt)

                if response.success and response.content:
                    return response

                # Empty response - treat as transient
                last_error = ReportGeneratorError(
                    f"Empty LLM response (attempt {attempt + 1}/{retries})"
                )
                logger.warning(
                    "Empty LLM response, retrying",
                    extra={"attempt": attempt + 1, "retries": retries}
                )

            except OllamaEngineError as e:
                last_error = ReportGeneratorError(f"LLM engine error: {e}")
                logger.warning(
                    "LLM engine error, retrying",
                    extra={
                        "attempt": attempt + 1,
                        "retries": retries,
                        "error": str(e)
                    }
                )

            except Exception as e:
                last_error = ReportGeneratorError(f"Unexpected error: {e}")
                logger.error(
                    "Unexpected error during report generation",
                    extra={
                        "attempt": attempt + 1,
                        "error": str(e)
                    }
                )

            # Exponential backoff
            if attempt < retries - 1:
                delay = self._config.retry_delay * (2 ** attempt)
                logger.info(
                    f"Retrying in {delay:.1f}s",
                    extra={"attempt": attempt + 1}
                )
                await asyncio.sleep(delay)

        raise ReportGeneratorError(
            f"All {retries} retries exhausted. Last error: {last_error}"
        )

    # --- Core Generation Methods ---

    async def generate_daily_report(
        self,
        *,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
    ) -> ReportGenerationResult:
        """
        Generate a daily report for the last 24 hours.

        Summarizes new essences, KB files, and hotspots from the period.

        Args:
            period_start: Custom start time (default: 24h ago)
            period_end: Custom end time (default: now)
            tags: Optional tags for categorization
            on_progress: Optional callback(stage, detail) for progress updates

        Returns:
            ReportGenerationResult with success status and details
        """
        now = datetime.now(timezone.utc)
        start = period_start or (now - timedelta(hours=24))
        end = period_end or now

        return await self.generate_report(
            report_type=self.DAILY,
            period_start=start,
            period_end=end,
            tags=tags,
            on_progress=on_progress,
        )

    async def generate_weekly_report(
        self,
        *,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
    ) -> ReportGenerationResult:
        """
        Generate a weekly report for the last 7 days.

        Aggregates daily reports and adds trend analysis.

        Args:
            period_start: Custom start time (default: 7 days ago)
            period_end: Custom end time (default: now)
            tags: Optional tags for categorization
            on_progress: Optional callback(stage, detail) for progress updates

        Returns:
            ReportGenerationResult with success status and details
        """
        now = datetime.now(timezone.utc)
        start = period_start or (now - timedelta(days=7))
        end = period_end or now

        return await self.generate_report(
            report_type=self.WEEKLY,
            period_start=start,
            period_end=end,
            tags=tags,
            on_progress=on_progress,
        )

    async def generate_monthly_report(
        self,
        *,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
    ) -> ReportGenerationResult:
        """
        Generate a monthly report for the last 30 days.

        Aggregates weekly reports and includes graph visualization data.

        Args:
            period_start: Custom start time (default: 30 days ago)
            period_end: Custom end time (default: now)
            tags: Optional tags for categorization
            on_progress: Optional callback(stage, detail) for progress updates

        Returns:
            ReportGenerationResult with success status and details
        """
        now = datetime.now(timezone.utc)
        start = period_start or (now - timedelta(days=30))
        end = period_end or now

        return await self.generate_report(
            report_type=self.MONTHLY,
            period_start=start,
            period_end=end,
            tags=tags,
            on_progress=on_progress,
        )

    async def generate_report(
        self,
        report_type: str,
        period_start: datetime,
        period_end: datetime,
        *,
        tags: Optional[List[str]] = None,
        on_progress: Optional[callable] = None,
    ) -> ReportGenerationResult:
        """
        Generate a report of any type for a given period.

        This is the core method that handles all report types.

        Args:
            report_type: One of "daily", "weekly", "monthly"
            period_start: Start of the period
            period_end: End of the period
            tags: Optional tags
            on_progress: Optional progress callback(stage, detail)

        Returns:
            ReportGenerationResult
        """
        start_time = time.time()

        if report_type not in (self.DAILY, self.WEEKLY, self.MONTHLY):
            raise ReportGeneratorError(
                f"Invalid report type: {report_type}. "
                f"Must be one of: daily, weekly, monthly"
            )

        logger.info(
            f"Generating {report_type} report",
            extra={
                "report_type": report_type,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
            }
        )

        try:
            # Stage 1: Collect essences
            if on_progress:
                on_progress("collecting", "Lese Essenzen...")

            essences = await self._collect_essences_for_period(
                period_start, period_end
            )

            logger.info(
                f"Collected {len(essences)} essences for {report_type} report",
                extra={"report_type": report_type, "essence_count": len(essences)}
            )

            # Stage 2: Compute hotspots
            if on_progress:
                on_progress("analyzing", "Analysiere Hotspots...")

            hotspots = self._compute_hotspots(essences)

            # Stage 3: Build prompt based on type
            if on_progress:
                on_progress("building_prompt", "Erstelle Prompt...")

            prompt = await self._build_prompt_for_type(
                report_type, essences, hotspots, period_start, period_end
            )

            # Stage 4: Generate with LLM
            if on_progress:
                on_progress("generating", "Generiere Bericht via LLM...")

            response = await self._generate_with_retry(prompt)

            # Stage 5: Post-process
            if on_progress:
                on_progress("saving", "Speichere Bericht...")

            sections = self._extract_sections(response.content, report_type)
            title = self._build_report_title(report_type, period_start, period_end)
            query = (
                f"{report_type.capitalize()} Report für "
                f"{period_start.strftime('%Y-%m-%d')} – {period_end.strftime('%Y-%m-%d')}"
            )
            source_hashes = [e.get("hash", "") for e in essences if e.get("hash")]

            # Save report via ContentManager
            report_path = await self._content_manager.save_report(
                title=title,
                content=response.content,
                query=query,
                report_type=report_type,
                source_hashes=source_hashes,
                model_used=response.model,
                related_topics=[hs["topic"] for hs in hotspots[:5]],
                tags=tags or [],
            )

            # Stage 6: For monthly, also save graph data
            if report_type == self.MONTHLY:
                graph_data = self._generate_graph_data(
                    essences, hotspots, period_start, period_end
                )
                await self._save_graph_data(graph_data, period_start)

            duration_ms = int((time.time() - start_time) * 1000)

            logger.info(
                f"{report_type.capitalize()} report generated successfully",
                extra={
                    "report_type": report_type,
                    "report_path": str(report_path),
                    "duration_ms": duration_ms,
                    "sections": sections,
                }
            )

            if on_progress:
                on_progress("complete", f"Bericht erstellt: {report_path.name}")

            return ReportGenerationResult(
                report_type=report_type,
                success=True,
                report_path=report_path,
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                sections_included=sections,
                model_used=response.model,
                duration_ms=duration_ms,
                sources_count=len(essences),
            )

        except Exception as e:
            duration_ms = int((time.time() - start_time) * 1000)

            logger.error(
                f"Failed to generate {report_type} report",
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

    # --- Prompt Assembly Helper ---

    async def _build_prompt_for_type(
        self,
        report_type: str,
        essences: List[Dict[str, Any]],
        hotspots: List[Dict[str, str]],
        period_start: datetime,
        period_end: datetime,
    ) -> str:
        """Build the appropriate prompt based on report type.

        Collects sub-reports as needed (daily reports for weekly,
        weekly reports for monthly).

        Args:
            report_type: One of "daily", "weekly", "monthly"
            essences: Collected essences for the period
            hotspots: Computed hotspots
            period_start: Period start
            period_end: Period end

        Returns:
            Formatted prompt string
        """
        if report_type == self.DAILY:
            return self._build_daily_prompt(
                essences, hotspots, period_start, period_end
            )

        elif report_type == self.WEEKLY:
            daily_reports_data = await self._collect_sub_reports(
                self.DAILY, period_start, period_end
            )
            return self._build_weekly_prompt(
                daily_reports_data, essences, hotspots,
                period_start, period_end
            )

        elif report_type == self.MONTHLY:
            weekly_reports_data = await self._collect_sub_reports(
                self.WEEKLY, period_start, period_end
            )
            return self._build_monthly_prompt(
                weekly_reports_data, essences, hotspots,
                period_start, period_end
            )

        raise ReportGeneratorError(f"Invalid report type: {report_type}")

    # --- Parallel Generation ---
    # Inherited from ParallelReportMixin via MRO.
    # See report_parallel.py for: generate_report_parallel,
    #   _process_parallel_result, _aggregate_report_responses,
    #   _compare_report_responses

    # --- Helpers ---

    @staticmethod
    def _extract_sections(
        content: str,
        report_type: str,
    ) -> List[str]:
        """
        Extract section headings from generated report content.

        Args:
            content: Markdown content
            report_type: Report type

        Returns:
            List of section heading strings
        """
        sections = []
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("## "):
                # Remove markdown heading markers
                heading = line.lstrip("#").strip()
                sections.append(heading)
        return sections

    @staticmethod
    def _build_report_title(
        report_type: str,
        period_start: datetime,
        period_end: datetime,
    ) -> str:
        """Build report title from type and period."""
        if report_type == "daily":
            return f"Daily Report — {period_start.strftime('%Y-%m-%d')}"
        elif report_type == "weekly":
            return (
                f"Weekly Report — "
                f"{period_start.strftime('%Y-%m-%d')} bis "
                f"{period_end.strftime('%Y-%m-%d')}"
            )
        else:
            return f"Monthly Report — {period_start.strftime('%Y-%m-%')}"

    async def get_generation_stats(self) -> Dict[str, Any]:
        """
        Get statistics about report generation.

        Returns:
            Dict with counts of reports by type and last generation times
        """
        return await self._stats_calc.get_generation_stats(self._content_manager)