# 📄 `__init__.py`

**Path:** `/mnt/Morgana/skills/morgana-anti-infinite-loop-v2/anti_loop/__init__.py`  
**Size:** 1,089 bytes / 51 lines  
**Hash:** `97cc76dd9955ba6d`  
**Generated:** 2026-06-09T01:00:46.590901+00:00

## 📝 Module Docstring

```
🌀 anti-loop v2.0 — Lightweight anti-infinite-loop guard for LLM agents.

Healing > Kill. Predictive. Zero-dep. 9 layers of protection.

Quickstart:
    >>> from anti_loop import AntiLoop
    >>> guard = AntiLoop(mode="heal", max_iter=10)
    >>> result = guard.observe("search for X", intent="find X")
    >>> if result["intervene"]:
    ...     apply(result["directive"])
```

## 📦 Imports (12)

```python
import core.AntiLoop
import core.HealingMode
import core.LoopType
import core.PredictiveEntropy
import core.NoveltyDetector
import core.LoopTaxonomy
import core.HealingInjector
import core.SelfTuningThresholds
import core.BreathRateMonitor
import core.PreFlightRegex
import core.LoopDNA
import core.CrossHarnessAdapters
```
