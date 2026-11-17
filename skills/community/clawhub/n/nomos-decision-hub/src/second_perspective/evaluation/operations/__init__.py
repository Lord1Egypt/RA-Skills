"""Institution product & operations layer (module C, v0.6).

- ``base``          : protocols & data models
- ``leaderboard``   : public leaderboard (in-memory)
- ``report_portal`` : deep-report portal index (in-memory)
- ``appeal``        : appeal workflow state machine (in-memory)
- ``drift``         : version-drift monitoring scheduler (in-memory)
- ``comparison``    : paired comparison statistics — Wilson / exact McNemar
                      / churn (spec §5.3 margin, paired test, churn layers)
"""

from .appeal import InMemoryAppealWorkflow
from .base import (
    AppealCase,
    AppealStatus,
    AppealWorkflow,
    DriftSchedule,
    DriftScheduler,
    Leaderboard,
    LeaderboardEntry,
    ReportPortal,
)
from .comparison import (
    ChurnReport,
    ComparisonError,
    McNemarResult,
    PairedComparison,
    WilsonInterval,
    assert_zero_churn,
    churn,
    compare_paired,
    mcnemar_exact,
    wilson_interval,
)
from .drift import InMemoryDriftScheduler, cadence_seconds
from .leaderboard import InMemoryLeaderboard
from .report_portal import InMemoryReportPortal, ReportRef

__all__ = [
    "AppealCase",
    "AppealStatus",
    "AppealWorkflow",
    "ChurnReport",
    "ComparisonError",
    "DriftSchedule",
    "DriftScheduler",
    "InMemoryAppealWorkflow",
    "InMemoryDriftScheduler",
    "InMemoryLeaderboard",
    "InMemoryReportPortal",
    "Leaderboard",
    "LeaderboardEntry",
    "McNemarResult",
    "PairedComparison",
    "ReportPortal",
    "ReportRef",
    "WilsonInterval",
    "assert_zero_churn",
    "cadence_seconds",
    "churn",
    "compare_paired",
    "mcnemar_exact",
    "wilson_interval",
]
