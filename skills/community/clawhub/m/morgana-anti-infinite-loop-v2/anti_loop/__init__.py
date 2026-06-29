"""
🌀 anti-loop v2.0 — Lightweight anti-infinite-loop guard for LLM agents.

Healing > Kill. Predictive. Zero-dep. 9 layers of protection.

Quickstart:
    >>> from anti_loop import AntiLoop
    >>> guard = AntiLoop(mode="heal", max_iter=10)
    >>> result = guard.observe("search for X", intent="find X")
    >>> if result["intervene"]:
    ...     apply(result["directive"])
"""

from .core import (
    # Main public API
    AntiLoop,
    # Modes
    HealingMode,
    # Loop types
    LoopType,
    # Individual layers (power users)
    PredictiveEntropy,
    NoveltyDetector,
    LoopTaxonomy,
    HealingInjector,
    SelfTuningThresholds,
    BreathRateMonitor,
    PreFlightRegex,
    LoopDNA,
    CrossHarnessAdapters,
)

__version__ = "2.0.0"
__author__ = "Morgana (Axioma Stellaris)"
__license__ = "MIT"

__all__ = [
    "AntiLoop",
    "HealingMode",
    "LoopType",
    "PredictiveEntropy",
    "NoveltyDetector",
    "LoopTaxonomy",
    "HealingInjector",
    "SelfTuningThresholds",
    "BreathRateMonitor",
    "PreFlightRegex",
    "LoopDNA",
    "CrossHarnessAdapters",
]
