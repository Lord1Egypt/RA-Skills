"""Measurement layer: corpora, metrics, and per-dimension control packs (v0.6)."""

from .base import Metric, MetricError, MetricResult
from .corpus import Corpus, CorpusError, CorpusItem
from .dimension_packs import (
    MeasurementControlPack,
    MetricThreshold,
    default_dimension_packs,
    register_dimension_packs,
)
from .metrics import (
    METRIC_REGISTRY,
    attack_success_rate,
    brier_score,
    cost_per_task,
    expected_calibration_error,
    fleiss_kappa,
    percentile,
    time_per_output_token,
    token_metering_error,
    tokens_per_second,
    ttft_p99,
)

__all__ = [
    "Corpus",
    "CorpusError",
    "CorpusItem",
    "METRIC_REGISTRY",
    "MeasurementControlPack",
    "Metric",
    "MetricError",
    "MetricResult",
    "MetricThreshold",
    "attack_success_rate",
    "brier_score",
    "cost_per_task",
    "default_dimension_packs",
    "expected_calibration_error",
    "fleiss_kappa",
    "percentile",
    "register_dimension_packs",
    "time_per_output_token",
    "token_metering_error",
    "tokens_per_second",
    "ttft_p99",
]
