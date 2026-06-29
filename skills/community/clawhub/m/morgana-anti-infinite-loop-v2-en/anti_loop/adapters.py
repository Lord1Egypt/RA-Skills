"""
🌀 anti-loop v2.0 — Cross-Harness Adapters.

Wrappers stdlib (zero-dep) pour interfacer le guard avec n'importe quel
LLM agent harness : Claude API, OpenAI API, LangChain, AutoGen, Hermes, custom.

Public API:
    >>> from anti_loop.adapters import CrossHarnessAdapters
    >>> text = CrossHarnessAdapters.adapt_anthropic(response)

Note: La classe complète `CrossHarnessAdapters` est définie dans `core.py`
pour minimiser les dépendances. Ce module la re-exporte pour les imports
explicites (`from anti_loop.adapters import CrossHarnessAdapters`).
"""

from .core import CrossHarnessAdapters

__all__ = ["CrossHarnessAdapters"]
