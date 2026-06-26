#!/usr/bin/env python3
"""
Report Data Aggregation Package

Collects and processes data for report generation:
- Essence and report collection for time periods
- Content reading from disk
- Hotspot computation and graph data generation
- Generation statistics
"""

from kb.biblio.generator.aggregators.data_aggregator import (
    ReportDataAggregator,
)
from kb.biblio.generator.aggregators.stats_calculator import (
    StatsCalculator,
)

__all__ = [
    "ReportDataAggregator",
    "StatsCalculator",
]