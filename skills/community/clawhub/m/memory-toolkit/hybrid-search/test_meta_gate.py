#!/usr/bin/env python3
"""M5 gate test: the memory toolkit must never mine its own plumbing.

The M4 echo guard (assistant_turn_is_echo) catches MACHINE-GENERATED turns —
tool logs, cron payloads, status lines. It does NOT catch a turn written in
fluent natural language whose SUBJECT is the memory system itself.

Observed 2026-10-09: the pipeline captured
    «il y a trois jobs qui touchent la mémoire chaque nuit»
a true sentence, but pure meta-noise about the agent's own plumbing. Storing it
as a durable fact about the user is an echo loop: the toolkit feeding on its own
description.

This test locks the M5 gate in place. It asserts BOTH directions:
  * self-referential turns are refused (the bug), AND
  * ordinary user facts that merely mention memory vocabulary still pass
    (the false-positive trap — a gate that eats real facts is worse than none).

Usage:
    python3 hybrid-search/test_meta_gate.py
Exit 0 = all gates hold; exit 1 = at least one regression.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from auto_capture import should_capture, text_is_self_referential  # noqa: E402

# ─── Must be REFUSED: the agent talking about its own machinery ───────────────
# Each of these is fluent French prose — the M4 echo guard does NOT match them.
# They must be caught by M5.
META_NOISE = [
    "il y a trois jobs qui touchent la mémoire chaque nuit",          # the observed bug
    "le pipeline nightly fait extraction puis arbitration",
    "la skill memory-health a été publiée sur ClawHub",
    "le trace-extractor tourne chaque nuit à 23h",
    "les jobs auto-capture et nightly-extraction sont dans le même pipeline",
    "on récupère les faits dans le store de faits",
    "le pipeline me pose problème",
    "la skill de Stéphane sur ClawHub sera publiée",
    "l'ontologie contient 1200 entités après consolidation",
    "trois facts ont été superseded cette nuit",
]

# ─── Must PASS: genuine user assertions, even when memory words appear ────────
# A gate that drops these is a regression: they are exactly what the toolkit
# exists to remember.
LEGIT_FACTS = [
    "j'ai migré le serveur sous Ubuntu 24.04",
    "note que mon nouveau tel est un Pixel 9",
    "correction : c'est 4 pas 6",
    "ma mémoire me joue des tours en ce moment",
    "note que ma nouvelle voiture est une Tesla",
    "désormais le backup tourne à 23h",
    "mon pipeline de données Astro est en production",
    "j'ai trois jobs à Airbus en ce moment et ça me pèse",
]

# ─── Ambiguous prose: must NOT be flagged as self-referential ─────────────────
# Not necessarily captured (other gates may apply), but the META gate itself
# must stay silent — this is the false-positive boundary.
NOT_META = [
    "j'ai une bonne mémoire",
    "la mémoire de l'ordi est saturée",
    "j'ai trois jobs à Airbus",
    "le scoring de football",
    "mon pipeline de données Astro",
    "il a fait une extraction dentaire",
]


def main() -> int:
    failures = 0

    print("== M5 meta gate: self-referential turns must be REFUSED ==")
    for text in META_NOISE:
        got = should_capture(text)
        ok = got is False
        if not ok:
            failures += 1
        print(f"  {'OK  ' if ok else 'FAIL'} capture={got!s:5}  {text!r}")

    print("\n== M5 meta gate: legitimate user facts must PASS ==")
    for text in LEGIT_FACTS:
        got = should_capture(text)
        ok = got is True
        if not ok:
            failures += 1
        print(f"  {'OK  ' if ok else 'FAIL'} capture={got!s:5}  {text!r}")

    print("\n== M5 meta gate: ambiguous prose must NOT be self-referential ==")
    for text in NOT_META:
        got = text_is_self_referential(text)
        ok = got is False
        if not ok:
            failures += 1
        print(f"  {'OK  ' if ok else 'FAIL'} self_ref={got!s:5}  {text!r}")

    print("\n== M5 meta gate: empty input is never flagged ==")
    for text in ("", "   ", None):
        got = text_is_self_referential(text or "")
        ok = got is False
        if not ok:
            failures += 1
        print(f"  {'OK  ' if ok else 'FAIL'} self_ref={got!s:5}  {text!r}")

    if failures:
        print(f"\n{failures} failure(s)")
        return 1
    print("\nAll M5 meta-gate assertions hold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
