"""Human / expert panel layer (module B, v0.6).

- scoring protocols + agreement aggregation (``base``)
- versioned expert-score I/O (``io``)
- ethics review workflow (``ethics``)
"""

from .base import (
    ExpertPanel,
    ExpertScore,
    PanelAgreement,
    aggregate_by_dimension,
    aggregate_panel_agreement,
    kappa_metric_result,
)
from .ethics import (
    EthicsReviewCase,
    EthicsReviewWorkflow,
    EthicsStatus,
    InMemoryEthicsReview,
)
from .io import ExpertScoreSet, ScoreSetError

__all__ = [
    "EthicsReviewCase",
    "EthicsReviewWorkflow",
    "EthicsStatus",
    "ExpertPanel",
    "ExpertScore",
    "ExpertScoreSet",
    "InMemoryEthicsReview",
    "PanelAgreement",
    "ScoreSetError",
    "aggregate_by_dimension",
    "aggregate_panel_agreement",
    "kappa_metric_result",
]
