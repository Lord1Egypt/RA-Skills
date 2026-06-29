# 📄 `adapters.py`

**Path:** `/mnt/Morgana/skills/morgana-anti-infinite-loop-v2/anti_loop/adapters.py`  
**Size:** 632 bytes / 19 lines  
**Hash:** `541fb514c253edc3`  
**Generated:** 2026-06-09T01:00:46.590984+00:00

## 📝 Module Docstring

```
🌀 anti-loop v2.0 — Cross-Harness Adapters.

Wrappers stdlib (zero-dep) pour interfacer le guard avec n'importe quel
LLM agent harness : Claude API, OpenAI API, LangChain, AutoGen, Hermes, custom.

Public API:
    >>> from anti_loop.adapters import CrossHarnessAdapters
    >>> text = CrossHarnessAdapters.adapt_anthropic(response)

Note: La classe complète `CrossHarnessAdapters` est définie dans `core.py`
pour minimiser les dépendances. Ce module la re-exporte pour les imports
explicites (`from anti_loop.adapters import CrossHarnessAdapters`).
```

## 📦 Imports (1)

```python
import core.CrossHarnessAdapters
```
