#!/usr/bin/env python3
"""
Pattern Detector
================
Pattern detection logic for dream consolidation.

Detects recurring patterns across memories:
  - Emotion patterns (recurring emotional states)
  - Participant patterns (frequently mentioned people)
  - Domain clusters (thematic groupings)
  - Cross-domain co-occurrence (temporal proximity)
  - Near-duplicate detection (consolidation candidates)

Author: Lilu / nima-core
"""

from __future__ import annotations

import re
import json
import hashlib
import itertools
from datetime import datetime
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Set

from .models import Pattern, _now_str
from .domain_classifier import classify_domain, extract_keywords

__all__ = [
    "PatternDetector",
    "PATTERN_MIN_OCC",
    "CROSS_DOMAIN_WINDOW_S",
]


# ── Constants ─────────────────────────────────────────────────────────────────

PATTERN_MIN_OCC = 3      # min occurrences to count as a pattern
CROSS_DOMAIN_WINDOW_S = 3600  # 1 hour temporal proximity


# ── Helper functions ──────────────────────────────────────────────────────────

def _find_temporal_overlap(mems1: List[Dict], mems2: List[Dict]) -> int:
    """Count pairs from two sets that occurred within CROSS_DOMAIN_WINDOW_S."""
    overlap = 0
    for m1 in mems1:
        for m2 in mems2:
            try:
                t1 = datetime.fromisoformat(str(m1["timestamp"]).replace("Z", "+00:00"))
                t2 = datetime.fromisoformat(str(m2["timestamp"]).replace("Z", "+00:00"))
                if abs((t1 - t2).total_seconds()) < CROSS_DOMAIN_WINDOW_S:
                    overlap += 1
            except (ValueError, KeyError, TypeError):
                pass
    return overlap


def _simple_similarity(a: str, b: str) -> float:
    """Jaccard similarity on word tokens — no deps required."""
    wa = set(re.findall(r'\w+', a.lower()))
    wb = set(re.findall(r'\w+', b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


# ── PatternDetector ───────────────────────────────────────────────────────────

class PatternDetector:
    """
    Detects patterns in memory collections.

    Usage:
        detector = PatternDetector(existing_patterns)
        new_patterns = detector.detect_patterns(memories)
    """

    def __init__(self, existing_patterns: List[Pattern]):
        """
        Initialize detector with existing patterns for accumulation.

        Args:
            existing_patterns: Previously detected patterns to update
        """
        self.patterns = existing_patterns

    def detect_patterns(self, memories: List[Dict]) -> List[Pattern]:
        """
        Detect all pattern types in the given memories.

        Args:
            memories: List of memory dictionaries

        Returns:
            List of newly detected patterns
        """
        new_patterns: List[Pattern] = []

        # Run all detection methods
        new_patterns.extend(self.emotion_patterns(memories))
        new_patterns.extend(self.participant_patterns(memories))
        new_patterns.extend(self.domain_clusters(memories))
        new_patterns.extend(self.cross_domain_patterns(memories))
        new_patterns.extend(self.near_duplicate_patterns(memories))

        return new_patterns

    @staticmethod
    def _count_emotions_from_memories(memories: List[Dict]) -> "Counter":
        """Tally emotion labels from dominant_emotion and themes fields."""
        emotion_counts: Counter = Counter()
        for m in memories:
            dom_emo = m.get("dominant_emotion")
            if dom_emo:
                emotion_counts[dom_emo] += 1
            themes_raw = m.get("themes", "")
            if themes_raw:
                try:
                    themes = json.loads(themes_raw) if isinstance(themes_raw, str) else themes_raw
                    if isinstance(themes, list):
                        emotion_counts.update(t for t in themes if isinstance(t, str))
                except (json.JSONDecodeError, TypeError):
                    pass
        return emotion_counts

    def _upsert_emotion_pattern(
        self, emotion: str, count: int, memories: List[Dict]
    ) -> "Optional[Pattern]":
        """Update an existing emotion pattern or create and return a new one."""
        existing = next((p for p in self.patterns if p.name == f"Recurring {emotion}"), None)
        if existing:
            existing.occurrences += count
            existing.last_seen    = _now_str()
            existing.strength     = min(1.0, existing.strength + 0.1)
            return None
        pid = f"emotion_{emotion}_{datetime.now().strftime('%Y%m%d')}"
        p = Pattern(
            id=pid,
            name=f"Recurring {emotion}",
            description=f"The state '{emotion}' appears frequently ({count}×) in recent memories.",
            occurrences=count,
            domains=["emotional"],
            examples=[
                (m.get("text") or m.get("summary") or "")[:100]
                for m in memories
                if m.get("dominant_emotion") == emotion
            ][:3],
            first_seen=_now_str(),
            last_seen=_now_str(),
            strength=min(1.0, 0.4 + count * 0.07),
        )
        self.patterns.append(p)
        return p

    def emotion_patterns(self, memories: List[Dict]) -> List[Pattern]:
        """
        Detect recurring emotional states from affect data.

        Analyzes dominant_emotion fields and themes to identify
        frequently occurring emotional states across memories.

        Args:
            memories: List of memory dictionaries with emotion metadata

        Returns:
            List of Pattern objects representing recurring emotions
        """
        emotion_counts = self._count_emotions_from_memories(memories)
        new_patterns: List[Pattern] = []
        for emotion, count in emotion_counts.items():
            if count < PATTERN_MIN_OCC:
                continue
            new_p = self._upsert_emotion_pattern(emotion, count, memories)
            if new_p is not None:
                new_patterns.append(new_p)
        return new_patterns

    def participant_patterns(self, memories: List[Dict]) -> List[Pattern]:
        """
        Detect frequently mentioned people across memories.

        Identifies recurring participants (people mentioned in 'who' field)
        excluding system entities like 'self', 'bot', 'assistant'.

        Args:
            memories: List of memory dictionaries with 'who' fields

        Returns:
            List of Pattern objects for frequent interactions
        """
        new_patterns: List[Pattern] = []
        participant_counts: Counter = Counter()
        participant_mems: Dict[str, List[Dict]] = defaultdict(list)

        for m in memories:
            who = m.get("who", "")
            if who and who not in {"self", "assistant", "bot", "system", "user", ""}:
                participant_counts[who] += 1
                participant_mems[who].append(m)

        for person, count in participant_counts.items():
            if count < PATTERN_MIN_OCC:
                continue
            existing = next(
                (p for p in self.patterns if person.lower() in p.name.lower() and "interaction" in p.name.lower()),
                None
            )
            if existing:
                existing.occurrences += count
                existing.last_seen    = _now_str()
                existing.strength     = min(1.0, existing.strength + 0.08)
            else:
                p = Pattern(
                    id=f"person_{person.lower()}_{datetime.now().strftime('%Y%m%d')}",
                    name=f"Frequent interaction: {person}",
                    description=f"{person} appears in {count} recent memories.",
                    occurrences=count,
                    domains=["relational"],
                    examples=[
                        (m.get("text") or m.get("summary") or "")[:100]
                        for m in participant_mems[person]
                    ][:3],
                    first_seen=_now_str(),
                    last_seen=_now_str(),
                    strength=min(1.0, 0.5 + count * 0.06),
                )
                new_patterns.append(p)
                self.patterns.append(p)

        return new_patterns

    def domain_clusters(self, memories: List[Dict]) -> List[Pattern]:
        """
        Detect thematic clusters by semantic domain.

        Groups memories by domain (technical, personal, creative, etc.)
        and identifies significant domain concentrations.

        Args:
            memories: List of memory dictionaries with text content

        Returns:
            List of Pattern objects representing domain clusters
        """
        new_patterns: List[Pattern] = []
        by_domain: Dict[str, List[Dict]] = defaultdict(list)

        for m in memories:
            text = (m.get("text") or m.get("summary") or "")
            for d in classify_domain(text):
                by_domain[d].append(m)

        for domain, mems in by_domain.items():
            if len(mems) < PATTERN_MIN_OCC:
                continue
            kws = extract_keywords(
                [(m.get("text") or m.get("summary") or "") for m in mems], top_n=5
            )
            existing = next((p for p in self.patterns if p.name == f"Domain cluster: {domain}"), None)
            if existing:
                existing.occurrences = len(mems)
                existing.last_seen   = _now_str()
                existing.strength    = min(1.0, existing.strength + 0.05)
            else:
                p = Pattern(
                    id=f"domain_{domain}_{datetime.now().strftime('%Y%m%d')}",
                    name=f"Domain cluster: {domain}",
                    description=(
                        f"{len(mems)} memories in '{domain}' domain. "
                        f"Core concepts: {', '.join(kws[:4])}."
                    ),
                    occurrences=len(mems),
                    domains=[domain],
                    examples=[(m.get("text") or m.get("summary") or "")[:100] for m in mems[:3]],
                    first_seen=_now_str(),
                    last_seen=_now_str(),
                    strength=min(1.0, 0.4 + len(mems) * 0.05),
                )
                new_patterns.append(p)
                self.patterns.append(p)

        return new_patterns

    def cross_domain_patterns(self, memories: List[Dict]) -> List[Pattern]:
        """
        Detect temporal co-occurrence between different domains.

        Finds domain pairs that appear together within a temporal
        window (CROSS_DOMAIN_WINDOW_S), suggesting thematic connections.

        Args:
            memories: List of memory dictionaries with timestamps

        Returns:
            List of Pattern objects for cross-domain co-occurrences
        """
        new_patterns: List[Pattern] = []
        by_domain: Dict[str, List[Dict]] = defaultdict(list)

        # Build domain mapping
        for m in memories:
            text = (m.get("text") or m.get("summary") or "")
            for d in classify_domain(text):
                by_domain[d].append(m)

        # Check domain pairs for temporal overlap
        domain_pairs = list(itertools.combinations(by_domain.keys(), 2))
        for d1, d2 in domain_pairs[:10]:  # cap to avoid O(n²) explosion
            overlap = _find_temporal_overlap(by_domain[d1], by_domain[d2])
            if overlap >= 2:
                existing = next(
                    (p for p in self.patterns
                     if d1 in p.domains and d2 in p.domains and "cross" in p.name.lower()),
                    None
                )
                if existing:
                    existing.occurrences += overlap
                    existing.last_seen    = _now_str()
                else:
                    p = Pattern(
                        id=f"cross_{d1}_{d2}_{datetime.now().strftime('%Y%m%d')}",
                        name=f"Cross-domain: {d1} ↔ {d2}",
                        description=(
                            f"Memories in '{d1}' and '{d2}' co-occur within "
                            f"{CROSS_DOMAIN_WINDOW_S // 3600}h ({overlap} pair(s))."
                        ),
                        occurrences=overlap,
                        domains=[d1, d2],
                        examples=[],
                        first_seen=_now_str(),
                        last_seen=_now_str(),
                        strength=0.4,
                    )
                    new_patterns.append(p)
                    self.patterns.append(p)

        return new_patterns

    def near_duplicate_patterns(self, memories: List[Dict]) -> List[Pattern]:
        """
        Detect near-duplicate memories as consolidation candidates.

        Uses Jaccard similarity on word tokens to find memories with
        high content overlap (>50%), flagging them for potential merging.

        Args:
            memories: List of memory dictionaries to compare

        Returns:
            List of Pattern objects identifying near-duplicate pairs
        """
        new_patterns: List[Pattern] = []
        seen_similar: Set[str] = set()

        for i, m1 in enumerate(memories):
            for m2 in memories[i + 1 : min(i + 15, len(memories))]:
                if m1["id"] in seen_similar:
                    break
                t1 = (m1.get("text") or m1.get("summary") or "")
                t2 = (m2.get("text") or m2.get("summary") or "")
                sim = _simple_similarity(t1, t2)
                if sim > 0.5:
                    seen_similar.add(m1["id"])
                    seen_similar.add(m2["id"])
                    p = Pattern(
                        id=f"dup_{hashlib.sha256(json.dumps(sorted([m1['id'], m2['id']])).encode()).hexdigest()[:10]}",
                        name="Near-duplicate pair",
                        description=f"Two memories are {sim:.0%} similar — candidate for consolidation.",
                        occurrences=1,
                        domains=["maintenance"],
                        examples=[t1[:80], t2[:80]],
                        first_seen=_now_str(),
                        last_seen=_now_str(),
                        strength=0.3,
                    )
                    new_patterns.append(p)
                    self.patterns.append(p)

        return new_patterns
