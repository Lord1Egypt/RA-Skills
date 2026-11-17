#!/usr/bin/env python3
"""Regression guard: atomic fact splitting protects numbers (conflict_resolver).

The bug seen 2026-10-05: `extract_atomic` split a compound statement on every
period, so a version string "Ubuntu 24.04" became "Ubuntu 24" + "04" and
"...à 100% atteint" lost its tail. Atomic extraction feeds conflict arbitration,
so a mangled number means a mangled fact.

This test pins BOTH directions:
  * the splitter still cuts real compound statements (semicolons, coordinating
    conjunctions, genuine sentence boundaries), AND
  * version strings, decimals and percentages survive whole.

Usage:
    python3 hybrid-search/test_extract_atomic.py
Exit 0 = all guards hold; exit 1 = at least one regression.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from conflict_resolver import extract_atomic  # noqa: E402

# (input, expected list) — the splitter must return exactly this.
CASES = [
    # ── numbers must survive ─────────────────────────────────────────────────
    ("On a migré le serveur sous Ubuntu 24.04", ["On a migré le serveur sous Ubuntu 24.04"]),
    ("La capacité est de 3.14 Go", ["La capacité est de 3.14 Go"]),
    ("Le disque est à 100% atteint", ["Le disque est à 100% atteint"]),
    ("L'objectif de 12,5 % est tenu", ["L'objectif de 12,5 % est tenu"]),
    ("Version 1.2.3 installée", ["Version 1.2.3 installée"]),
    # ── real splits must still happen ────────────────────────────────────────
    ("j'ai migré la base ; le backup tourne", ["j'ai migré la base", "le backup tourne"]),
    ("le serveur est en prod et le DNS est à jour",
     ["le serveur est en prod", "le DNS est à jour"]),
    ("il a fini puis il est parti", ["il a fini", "il est parti"]),
    ("première phrase. seconde phrase.", ["première phrase", "seconde phrase"]),
    # ── trailing punctuation trimmed, '%' preserved ──────────────────────────
    ("Le taux est de 50%.", ["Le taux est de 50%"]),
    # ── empty / whitespace never crashes ─────────────────────────────────────
    ("", []),
    ("   ", []),
]

# The specific regression from 2026-10-05, called out so a failure is obvious.
REGRESSION_CASES = [
    ("Ubuntu 24.04", 1),   # must NOT split into 2
    ("100% atteint", 1),   # must NOT lose its tail
]


def main():
    print("== test_extract_atomic ==")
    failures = []
    for text, expected in CASES:
        got = extract_atomic(text)
        if got != expected:
            failures.append(f"{text!r}\n      expected {expected}\n      got      {got}")
        else:
            print(f"  OK  {text!r} -> {got}")

    print("-- 2026-10-05 regression (numbers must stay whole) --")
    for text, want_parts in REGRESSION_CASES:
        got = extract_atomic(text)
        if len(got) != want_parts:
            failures.append(f"REGRESSION {text!r}: split into {len(got)} parts {got}, want {want_parts}")
        else:
            print(f"  OK  {text!r} -> {got}")

    if failures:
        print("\nFAILURES:")
        for f in failures:
            print("  ✗", f)
        return 1
    print("\nAll atomic-extraction guards hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
