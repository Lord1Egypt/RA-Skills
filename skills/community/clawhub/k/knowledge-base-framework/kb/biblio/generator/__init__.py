#!/usr/bin/env python3
"""
kb.llm.generator - Essence and Report Generator Package

LLM-powered essence extraction and report generation from Knowledge Base content.
"""

from kb.biblio.generator.base import (
    BaseGenerator,
    BaseGeneratorError,
)

from kb.biblio.generator.essence_generator import (
    EssenzGenerator,
    EssenzGeneratorError,
    EssenzGenerationResult,
)

from kb.biblio.generator.report_generator import (
    ReportGenerator,
)

from kb.biblio.generator.report_models import (
    ReportGeneratorError,
    ReportGenerationResult,
)

from kb.biblio.generator.parallel_mixin import (
    ParallelMixin,
    ParallelStrategy,
    ParallelResult,
    DiffResult,
    DiffEntry,
    DiffType,
)

from kb.biblio.generator.diff_merger import (
    DiffMerger,
    diff_essences,
    merge_essences,
    diff_reports,
    merge_reports,
)

from kb.biblio.generator.report_parallel import (
    ParallelReportMixin,
)

# New sub-modules (Phase 5: Module Split)
from kb.biblio.generator.aggregators import (
    ReportDataAggregator,
    StatsCalculator,
)

__all__ = [
    # Base Generator
    "BaseGenerator",
    "BaseGeneratorError",
    # Essence Generator
    "EssenzGenerator",
    "EssenzGeneratorError",
    "EssenzGenerationResult",
    # Report Generator
    "ReportGenerator",
    "ReportGeneratorError",
    "ReportGenerationResult",
    # Parallel Support
    "ParallelMixin",
    "ParallelStrategy",
    "ParallelResult",
    "DiffResult",
    "DiffEntry",
    "DiffType",
    # Diff & Merge
    "DiffMerger",
    "diff_essences",
    "merge_essences",
    "diff_reports",
    "merge_reports",
    # Parallel Report Mixin
    "ParallelReportMixin",
    # Data Aggregation (Phase 5)
    "ReportDataAggregator",
    "StatsCalculator",
]