"""Polymarket Agent — OpenClaw skill for prediction-market analysis.

Security in one sentence: the language model PROPOSES, the code DISPOSES.
Every operation involving money goes through `guardrails.evaluate_order`,
which does not depend on the LLM's good behavior.
"""

__version__ = "2.2.1"

__all__ = [
    "alerts",
    "config",
    "guardrails",
    "journal",
    "keystore",
    "http",
    "markets",
    "paths",
    "trading",
    "whales",
]
