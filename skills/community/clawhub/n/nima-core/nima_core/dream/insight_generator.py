#!/usr/bin/env python3
"""
Insight Generator
=================
Generates insights from memory patterns during dream consolidation.

This module analyzes detected patterns and memories to generate:
  - Deep insights from strong recurring patterns
  - Emotional trajectory shifts over time
  - Domain gap detection (neglected areas)
  - Creative cross-domain connections (aha moments)

Author: Lilu / nima-core
"""

from __future__ import annotations

import json
import random
import hashlib
import itertools
from datetime import datetime
from typing import Dict, List, Set
from collections import defaultdict

from .models import Insight, Pattern, _now_str
from .domain_classifier import classify_domain, DOMAINS

__all__ = [
    "InsightGenerator",
    "STRONG_PATTERN",
]


# ── Constants ──────────────────────────────────────────────────────────────────

STRONG_PATTERN = 0.6  # strength threshold for deeper insights


# ── InsightGenerator Class ─────────────────────────────────────────────────────

class InsightGenerator:
    """
    Generates insights from detected patterns and memories.

    Produces three types of insights:
      1. Pattern insights - from strong recurring patterns
      2. Emotional insights - trajectory shifts over time
      3. Domain gap insights - neglected areas
      4. Connection insights - creative cross-domain links
    """

    def __init__(self):
        """Initialize the InsightGenerator with empty insight collection."""
        self.insights: List[Insight] = []

    def generate_insights(self, memories: List[Dict], patterns: List[Pattern]) -> List[Insight]:
        """
        Generate deep insights from memories and detected patterns.

        Args:
            memories: List of memory dictionaries
            patterns: List of detected Pattern objects

        Returns:
            List of generated Insight objects
        """
        insights: List[Insight] = []

        # ── 1. Deep insight from strong patterns ──
        for p in patterns:
            if p.strength >= STRONG_PATTERN:
                ins = Insight(
                    id=f"insight_{p.id}",
                    type="pattern",
                    content=(
                        f"Strong pattern: {p.description} "
                        f"(occurred {p.occurrences}×, strength {p.strength:.2f})"
                    ),
                    confidence=p.strength,
                    sources=p.examples[:2],
                    domains=p.domains,
                    timestamp=_now_str(),
                    importance=0.75,
                )
                insights.append(ins)
                self.insights.append(ins)

        # ── 2. Emotional trajectory shift ──
        chronological = sorted(
            memories,
            key=lambda m: str(m.get("timestamp", ""))
        )
        emotions_over_time = [m.get("dominant_emotion") for m in chronological]
        emotions_over_time = [e for e in emotions_over_time if e]
        if len(emotions_over_time) >= 3:
            first = set(emotions_over_time[:len(emotions_over_time) // 3])
            last  = set(emotions_over_time[-len(emotions_over_time) // 3:])
            if first != last:
                ins = Insight(
                    id=f"emo_shift_{datetime.now().strftime('%Y%m%d%H%M')}",
                    type="emotion_shift",
                    content=(
                        f"Emotional trajectory shift detected: "
                        f"started with {sorted(first) or ['neutral']}, "
                        f"ended with {sorted(last) or ['neutral']}. "
                        f"Something changed in the {len(memories)}-memory window."
                    ),
                    confidence=0.65,
                    sources=[],
                    domains=["emotional"],
                    timestamp=_now_str(),
                    importance=0.6,
                )
                insights.append(ins)
                self.insights.append(ins)

        # ── 3. Domain gap detection (what's been neglected?) ──
        active_domains: Set[str] = set()
        for m in memories:
            text = (m.get("text") or m.get("summary") or "")
            active_domains.update(classify_domain(text))
        neglected = set(DOMAINS.keys()) - active_domains - {"general"}
        for domain in list(neglected)[:2]:
            ins = Insight(
                id=f"gap_{domain}_{datetime.now().strftime('%Y%m%d')}",
                type="question",
                content=(
                    f"No recent activity in the '{domain}' domain. "
                    f"When did this area last get attention? Worth checking in."
                ),
                confidence=0.5,
                sources=[],
                domains=[domain],
                timestamp=_now_str(),
                importance=0.4,
            )
            insights.append(ins)
            self.insights.append(ins)

        return insights

    def generate_connections(self, memories: List[Dict]) -> List[Insight]:
        """
        Generate creative cross-domain connections — aha moments.

        Randomly samples pairs of memories from different domains
        and creates connection insights exploring potential relationships.

        Args:
            memories: List of memory dictionaries

        Returns:
            List of connection Insight objects
        """
        insights: List[Insight] = []

        by_domain: Dict[str, List[Dict]] = defaultdict(list)
        for m in memories:
            text = (m.get("text") or m.get("summary") or "")
            for d in classify_domain(text):
                by_domain[d].append(m)

        domain_pairs = list(itertools.combinations(by_domain.keys(), 2))
        random.shuffle(domain_pairs)

        for d1, d2 in domain_pairs[:5]:
            mems1 = by_domain[d1]
            mems2 = by_domain[d2]
            if not mems1 or not mems2:
                continue
            m1 = random.choice(mems1)
            m2 = random.choice(mems2)
            c1 = (m1.get("text") or m1.get("summary") or "")[:80]
            c2 = (m2.get("text") or m2.get("summary") or "")[:80]
            if len(c1) < 20 or len(c2) < 20 or d1 == d2:
                continue

            templates = [
                f"What if the approach to {d1} could inform {d2}? Both involve transformation.",
                f"The pattern in {d1} ({c1[:40]}…) might apply to {d2}.",
                f"Connection: {d1} and {d2} share underlying structure — worth exploring.",
                f"Question: How does '{c1[:30]}' relate to '{c2[:30]}'?",
                f"Insight: {d1} activity may be influencing {d2} outcomes indirectly.",
            ]
            content = random.choice(templates)

            # Stable ID using sorted source snippets
            canonical = json.dumps(sorted([c1[:40], c2[:40]]))
            ins = Insight(
                id=f"conn_{hashlib.sha256(canonical.encode()).hexdigest()[:10]}",
                type="connection",
                content=content,
                confidence=0.45,
                sources=[c1[:60], c2[:60]],
                domains=[d1, d2],
                timestamp=_now_str(),
                importance=0.5,
            )
            insights.append(ins)
            self.insights.append(ins)

        return insights
