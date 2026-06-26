#!/usr/bin/env python3
"""
MO§ES™ Commitment Conservation Engine — commitment.py
© 2026 Ello Cello LLC — Patent pending: Serial No. 63/877,177

Measures semantic drift between a proposed action and conversation history.
Based on the Conservation Law: C(T(S)) = C(S) — Zenodo 10.5281/zenodo.18792459

Drift > block_threshold → commitment VIOLATED, action blocked.

Uses TF-IDF cosine similarity (sklearn) if available, falls back to Jaccard.

Usage:
  python3 commitment.py check "<new action>" --history "<prior1>" "<prior2>"
  python3 commitment.py check "<new action>" --block-threshold 40
"""

from __future__ import annotations

import argparse
import json
import sys

_SKLEARN_AVAILABLE = False
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    _SKLEARN_AVAILABLE = True
except ImportError:
    pass


# ---------------------------------------------------------------------------
# Drift scoring
# ---------------------------------------------------------------------------

def score_commitment(new_message: str, history: list[str] | None = None) -> float:
    """
    Measure semantic drift between a new message and conversation history.

    Returns:
        drift (float): 0–100. Lower = more committed to prior context.
        < 5   → green  — commitment preserved
        5–20  → yellow — minor drift, log and continue
        20–40 → orange — significant drift, add conditions
        > 40  → red    — block or escalate
    """
    if not history:
        history = ["INITIAL COMMITMENT BASELINE"]

    if _SKLEARN_AVAILABLE:
        return _score_tfidf(new_message, history)
    return _score_word_overlap(new_message, history)


def _score_tfidf(new_message: str, history: list[str]) -> float:
    vectorizer = TfidfVectorizer(stop_words="english", min_df=1)
    all_texts = history + [new_message]
    try:
        tfidf_matrix = vectorizer.fit_transform(all_texts)
    except ValueError:
        return 0.0
    history_mean = np.asarray(tfidf_matrix[:-1].mean(axis=0))
    sim = cosine_similarity(history_mean, tfidf_matrix[-1])[0][0]
    return round((1.0 - float(sim)) * 100.0, 2)


def _score_word_overlap(new_message: str, history: list[str]) -> float:
    def tokenize(text: str) -> set[str]:
        return set(text.lower().split())

    history_words: set[str] = set()
    for h in history:
        history_words.update(tokenize(h))

    new_words = tokenize(new_message)
    if not history_words and not new_words:
        return 0.0

    intersection = history_words & new_words
    union = history_words | new_words
    jaccard = len(intersection) / len(union) if union else 1.0
    return round((1.0 - jaccard) * 100.0, 2)


# ---------------------------------------------------------------------------
# Drift classification
# ---------------------------------------------------------------------------

DRIFT_THRESHOLDS = {
    "green":  5.0,
    "yellow": 20.0,
    "orange": 40.0,
}


def classify_drift(drift: float) -> str:
    if drift < DRIFT_THRESHOLDS["green"]:
        return "green"
    elif drift < DRIFT_THRESHOLDS["yellow"]:
        return "yellow"
    elif drift < DRIFT_THRESHOLDS["orange"]:
        return "orange"
    return "red"


# ---------------------------------------------------------------------------
# Full evaluation
# ---------------------------------------------------------------------------

def evaluate_commitment(
    new_message: str,
    history: list[str] | None = None,
    block_threshold: float = 40.0,
) -> dict:
    """
    Full commitment evaluation with enforcement verdict.

    Returns:
        drift_score, drift_level, commitment_preserved, reason, conditions, scorer
    """
    drift = score_commitment(new_message, history)
    level = classify_drift(drift)
    preserved = drift < block_threshold

    conditions: list[str] = []
    if level == "yellow":
        conditions.append(f"Drift {drift:.1f}% — minor deviation logged")
    elif level == "orange":
        conditions.append(f"Drift {drift:.1f}% — operator review recommended")
    elif level == "red":
        conditions.append(f"Drift {drift:.1f}% — escalated to High Integrity mode")

    return {
        "drift_score": drift,
        "drift_level": level,
        "commitment_preserved": preserved,
        "reason": f"Drift {drift:.1f}% — commitment {'preserved' if preserved else 'VIOLATED'}",
        "conditions": conditions,
        "block_threshold": block_threshold,
        "scorer": "tfidf" if _SKLEARN_AVAILABLE else "word_overlap",
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="MO§ES™ Commitment Conservation Engine")
    sub = parser.add_subparsers(dest="cmd")

    p = sub.add_parser("check")
    p.add_argument("message", help="Proposed action or response")
    p.add_argument("--history", nargs="*", default=[], help="Prior messages")
    p.add_argument("--block-threshold", type=float, default=40.0)

    args = parser.parse_args()

    if args.cmd == "check":
        result = evaluate_commitment(
            args.message,
            history=args.history or None,
            block_threshold=args.block_threshold,
        )
        print(json.dumps(result, indent=2))
        if not result["commitment_preserved"]:
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
