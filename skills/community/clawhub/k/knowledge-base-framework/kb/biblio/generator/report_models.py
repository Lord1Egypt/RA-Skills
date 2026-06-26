#!/usr/bin/env python3
"""
Report Generation Models and Exceptions

Data structures and error types for the report generation pipeline.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any


class ReportGeneratorError(Exception):
    """Error in report generation operations."""
    pass


class ReportGenerationResult:
    """
    Result of a report generation.

    Attributes:
        report_type: Type of report (daily, weekly, monthly)
        success: Whether generation succeeded
        report_path: Path to saved report file (None if failed)
        period_start: Start of the covered period
        period_end: End of the covered period
        sections_included: List of sections included in the report
        model_used: LLM model used for generation
        duration_ms: Generation time in milliseconds
        sources_count: Number of source essences/reports used
        error: Error message if generation failed
    """

    def __init__(
        self,
        report_type: str,
        success: bool,
        *,
        report_path: Optional[Path] = None,
        period_start: Optional[str] = None,
        period_end: Optional[str] = None,
        sections_included: Optional[List[str]] = None,
        model_used: Optional[str] = None,
        duration_ms: int = 0,
        sources_count: int = 0,
        error: Optional[str] = None,
    ):
        self.report_type = report_type
        self.success = success
        self.report_path = report_path
        self.period_start = period_start
        self.period_end = period_end
        self.sections_included = sections_included or []
        self.model_used = model_used
        self.duration_ms = duration_ms
        self.sources_count = sources_count
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "report_type": self.report_type,
            "success": self.success,
            "report_path": str(self.report_path) if self.report_path else None,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "sections_included": self.sections_included,
            "model_used": self.model_used,
            "duration_ms": self.duration_ms,
            "sources_count": self.sources_count,
            "error": self.error,
        }