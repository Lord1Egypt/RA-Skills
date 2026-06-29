# 📄 `core.py`

**Path:** `/mnt/Morgana/skills/morgana-anti-infinite-loop-v2/anti_loop/core.py`  
**Size:** 24,637 bytes / 704 lines  
**Hash:** `626176ffa92e9d81`  
**Generated:** 2026-06-09T01:00:46.590650+00:00

## 📝 Module Docstring

```
🌀 anti-infinite-loop v2.0 — CORE
─────────────────────────────────────
Spec: /mnt/Morgana/audits/2026-06-08_choir_audit/spec_anti_loop_v2_external.md
Cible: EXTERNAL USERS (dev solo, startup, chercheur)
Deps CORE: stdlib Python + numpy OPTIONNEL
Deps OPT-IN: torch (KAN), embeddings, multi-agent

9 features CORE (zéro dépendance fancy):
1. Predictive Entropy (Shannon) — 0 token, 0ms
2. Novelty Detector (numpy cosine) — fallback hash
3. Loop Taxonomy (4 types: verbatim/semantic/intent_drift/cyclic)
4. Healing Injector (vs hard-kill) — 3 modes
5. Self-Tuning Thresholds — méta-boucle sans ML
6. Breath-Rate Monitor — 0 CPU 0 RAM
7. Pre-Flight Regex — plan-level, 0 LLM
8. Loop DNA (SHA-256) — cross-session
9. Cross-Harness Adapters — 3 lignes pour brancher

PHILOSOPHIE: "Lunedi-matin-ready" (lunedi = lundi en italien)
- Single-agent par défaut
- Multi-agent opt-in
- Healing > Kill
- Coût-aware (track tokens)
```

## 📦 Imports (20)

```python
import os
import re
import json
import math
import time
import hashlib
import logging
import collections.deque
import pathlib.Path
import datetime.datetime
import typing.Optional
import typing.Callable
import typing.Any
import typing.Dict
import typing.List
import typing.Union
import typing.Tuple
import numpy
import argparse
import random
```

## 🏛️ Classes (12)

### `PredictiveEntropy`
> Shannon entropy sur sliding window des N dernières actions.
Quand l'entropie collapse sous un seuil dynamique → précurseur de boucle.
Détecte 5-10 itérations AVANT la catastrophe.
**Methods:** `__init__, observe, is_collapse_imminent`

### `NoveltyDetector`
> Cosine similarity entre actions consécutives.
- Avec numpy: vectorise le texte (simple hashing trick)
- Sans numpy: hash direct, exact match only
**Methods:** `__init__, _text_to_vector, _cosine, observe, is_novelty_low, last_novelty, last_novelty`

### `LoopType`

### `LoopTaxonomy`
> Classify la boucle en 4 types. Chaque type a un remède spécifique.
**Methods:** `__init__, observe, _intent_similar`

### `HealingMode`

### `HealingInjector`
> Au lieu de abort(), INJECTE un system message contextuel.
Le skill apprend à l'agent à se corriger.
**Methods:** `__init__, inject`

### `SelfTuningThresholds`
> Observe TP/FP sur les 100 derniers cas, ajuste seuils via gradient simple.
Pas de ML, juste moving average.
**Methods:** `__init__, record`

### `BreathRateMonitor`
> Δt entre actions consécutives.
Si Δt collapse soudainement → le système est dans un pattern de boucle.
Pure timestamp, 0 CPU 0 RAM.
**Methods:** `__init__, observe, is_collapse`

### `PreFlightRegex`
> Bloque AVANT exécution, sur le plan, en regex pur.
Patterns typiques de loops:
- "if X then X" (tautology)
- "retry N without changing params"
- "while not converged: do same thing"
**Methods:** `__init__, check`

### `LoopDNA`
> SHA-256 fingerprint de chaque boucle résolue.
Stockage local: ~/.anti_loop/loops.json
Si même DNA revu → kill instant.
**Methods:** `__init__, _load, _save, fingerprint, record, is_known, get_known_count`

### `CrossHarnessAdapters`
> Wrappers stdlib pour Claude API, OpenAI API, LangChain, AutoGen, Hermes, custom.
Interface unique: AntiLoop.observe(response, tool_calls).
**Methods:** `adapt_anthropic, adapt_openai, adapt_langchain, adapt_autogen, adapt_hermes, adapt_custom`

### `AntiLoop`
> Main guard class. Branch in 3 lines:

    guard = AntiLoop(mode="heal", max_iter=10)
    result = guard.observe(action, intent)
    if result["intervene"]:
        apply(result["directive"])
**Methods:** `__init__, pre_flight, observe, reset, stats`

## ⚡ Functions (1)

### `def main():`
