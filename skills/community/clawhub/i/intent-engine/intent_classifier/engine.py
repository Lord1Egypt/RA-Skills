"""Core intent classification engine with multi-strategy matching."""
import re
import math
from typing import Optional

from .models import Intent, ClassificationResult
from .storage import IntentStore


class IntentEngine:
    """
    Multi-strategy intent classifier.

    Strategies (weighted):
    1. Regex pattern matching  — highest precision
    2. Keyword matching        — broad recall
    3. Text length adjustment  — short texts penalized
    4. Multi-intent conflict resolution
    """

    MIN_SCORE = 0.8  # Minimum raw score to consider (filters priority-only noise)

    def __init__(self, store: IntentStore = None):
        self.store = store or IntentStore()

    def classify(self, text: str, top_k: int = 3) -> Optional[ClassificationResult]:
        """
        Classify input text and return the best match.

        Returns None if no intent matches above threshold.
        """
        if not text or not text.strip():
            return None

        text_stripped = text.strip()
        text_lower = text_stripped.lower()
        text_len = len(text_stripped)

        scores = []

        for intent in self.store.get_all(enabled_only=True):
            score, kw_matches, pt_matches = self._score_intent(
                intent, text_stripped, text_lower, text_len
            )
            if score >= self.MIN_SCORE:
                scores.append((intent, score, kw_matches, pt_matches))

        if not scores:
            return None

        # Sort by score descending
        scores.sort(key=lambda x: -x[1])

        best = scores[0]
        intent, score, kw_matches, pt_matches = best

        # Normalize confidence to 0-1
        confidence = min(score / max(10.0, score + 2), 0.99)

        # Build alternatives
        alternatives = []
        for alt in scores[1:top_k + 1]:
            alt_intent, alt_score, alt_kw, alt_pt = alt
            alt_conf = alt_score / max(10.0, alt_score + 2)
            if alt_conf > 0.05:
                alternatives.append(ClassificationResult(
                    intent_id=alt_intent.id,
                    intent_name=alt_intent.name,
                    category=alt_intent.category,
                    sub_category=alt_intent.sub_category,
                    icon=alt_intent.icon,
                    confidence=alt_conf,
                    matched_keywords=alt_kw,
                    matched_patterns=alt_pt,
                    route_skill=alt_intent.route_skill,
                    route_description=alt_intent.route_description,
                ))

        return ClassificationResult(
            intent_id=intent.id,
            intent_name=intent.name,
            category=intent.category,
            sub_category=intent.sub_category,
            icon=intent.icon,
            confidence=confidence,
            matched_keywords=kw_matches,
            matched_patterns=pt_matches,
            route_skill=intent.route_skill,
            route_description=intent.route_description,
            alternatives=alternatives[:top_k],
        )

    def _score_intent(self, intent: Intent, text: str, text_lower: str, text_len: int):
        """Calculate composite score for a single intent."""
        score = 0.0
        kw_matches = []
        pt_matches = []

        # --- Pattern matching (high weight) ---
        for pattern in intent.patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 4.0
                    pt_matches.append(pattern)
            except re.error:
                continue

        # --- Keyword matching ---
        for kw in intent.keywords:
            if isinstance(kw, dict):
                kw_val = kw.get("value", "")
                kw_weight = kw.get("weight", 1.0)
            else:
                kw_val = str(kw)
                kw_weight = 1.0
            if kw_val.lower() in text_lower:
                score += 2.0 * kw_weight
                kw_matches.append(kw_val)

        # --- Text length adjustment ---
        if text_len < 10:
            score *= 0.8   # Short text reduces confidence
        elif text_len > 50:
            score *= 1.1   # Long detailed text boosts confidence

        # --- Intent priority bonus ---
        score += intent.priority * 0.05

        return score, kw_matches, pt_matches

    def classify_multi(self, text: str, threshold: float = 0.3, top_k: int = 5):
        """Return all intents above threshold (for multi-label scenarios)."""
        if not text or not text.strip():
            return []

        text_stripped = text.strip()
        text_lower = text_stripped.lower()
        text_len = len(text_stripped)

        results = []
        max_score = 1.0

        for intent in self.store.get_all(enabled_only=True):
            score, kw_matches, pt_matches = self._score_intent(
                intent, text_stripped, text_lower, text_len
            )
            if score >= self.MIN_SCORE:
                if score > max_score:
                    max_score = score
                results.append((intent, score, kw_matches, pt_matches))

        # Normalize
        results.sort(key=lambda x: -x[1])
        output = []
        for intent, score, kw, pt in results[:top_k]:
            conf = score / max(1.0, max_score)
            if conf >= threshold:
                output.append(ClassificationResult(
                    intent_id=intent.id, intent_name=intent.name,
                    category=intent.category, sub_category=intent.sub_category,
                    icon=intent.icon, confidence=round(conf, 4),
                    matched_keywords=kw, matched_patterns=pt,
                    route_skill=intent.route_skill,
                    route_description=intent.route_description,
                ))
        return output

    # --- Batch operations ---

    def classify_batch(self, texts: list[str]) -> list:
        """Classify multiple texts at once."""
        return [
            {
                "input": t,
                "result": (self.classify(t).to_dict()
                           if (r := self.classify(t)) else None)
            }
            for t in texts
        ]

    def evaluate(self, test_cases: list[dict]) -> dict:
        """
        Run evaluation with labeled test cases.
        test_cases: [{"text": "...", "expected_category": "CODE"}, ...]
        """
        correct = 0
        total = len(test_cases)
        details = []

        for tc in test_cases:
            result = self.classify(tc["text"])
            is_correct = (
                result and result.category == tc.get("expected_category")
            )
            if is_correct:
                correct += 1
            details.append({
                "text": tc["text"],
                "predicted": result.category if result else "NONE",
                "expected": tc.get("expected_category"),
                "confidence": result.confidence if result else 0,
                "correct": is_correct,
            })

        return {
            "accuracy": round(correct / total, 4) if total > 0 else 0,
            "correct": correct, "total": total, "details": details,
        }
