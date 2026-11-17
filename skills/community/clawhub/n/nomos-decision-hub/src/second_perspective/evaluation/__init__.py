"""Evaluation layer (v0.6) — measurement harness + human panel + operations.

Extends NOMOS from an audit *kernel* into an evaluation *institution platform*:

- ``measurement`` — corpora, metrics and per-dimension control packs (implemented)
- ``panel``       — human / expert scoring & ethics review (interface placeholder)
- ``operations``  — leaderboard / report portal / appeal / drift scheduler (placeholders)

The measurement layer is pure-stdlib and deterministic, mirroring the kernel's
"no invention, re-computable provenance" invariants.
"""

from . import measurement, operations, panel
from .measurement import (
    METRIC_REGISTRY,
    Corpus,
    CorpusItem,
    MeasurementControlPack,
    MetricError,
    MetricResult,
    MetricThreshold,
    default_dimension_packs,
    register_dimension_packs,
)

__all__ = [
    "Corpus",
    "CorpusItem",
    "METRIC_REGISTRY",
    "MeasurementControlPack",
    "MetricError",
    "MetricResult",
    "MetricThreshold",
    "default_dimension_packs",
    "measurement",
    "operations",
    "panel",
    "register_dimension_packs",
]

__layer_version__ = "0.6.0"
