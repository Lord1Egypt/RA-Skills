"""lgd_engine.judges — domain adapters."""
from .base import (
    DomainJudge,
    JudgeVerdict,
    Reason,
    Evidence,
    VALID_VERDICTS,
    VALID_LEVELS,
)

__all__ = [
    "DomainJudge",
    "JudgeVerdict",
    "Reason",
    "Evidence",
    "VALID_VERDICTS",
    "VALID_LEVELS",
]
