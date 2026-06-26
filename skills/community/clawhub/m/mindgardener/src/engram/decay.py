#!/usr/bin/env python3
"""
Temporal decay for MindGardener facts.

Facts lose relevance over time unless reinforced.
"""

import json
import math
import os
from datetime import datetime, timedelta
from pathlib import Path

from .filelock import file_lock


# Default decay rate (half-life in days)
DEFAULT_HALF_LIFE = 30  # Facts lose 50% relevance every 30 days


def calculate_decay(
    timestamp: str,
    half_life_days: float = DEFAULT_HALF_LIFE,
    reinforcements: int = 0,
) -> float:
    """
    Calculate decay factor for a fact.
    
    Returns value 0.0-1.0 where 1.0 is fresh and 0.0 is fully decayed.
    
    Reinforcements slow decay (each reinforcement adds to effective age).
    """
    try:
        ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except:
        return 1.0  # Can't parse, assume fresh
    
    age_days = (datetime.now(ts.tzinfo) - ts).total_seconds() / 86400
    
    # Reinforcements extend effective freshness
    effective_half_life = half_life_days * (1 + 0.5 * reinforcements)
    
    # Exponential decay: score = 0.5 ^ (age / half_life)
    decay = math.pow(0.5, age_days / effective_half_life)
    
    return max(0.0, min(1.0, decay))


def score_fact(fact: dict, half_life_days: float = DEFAULT_HALF_LIFE) -> float:
    """
    Calculate overall score for a fact.
    
    Combines:
    - Confidence (from provenance)
    - Decay (from timestamp)
    - Reinforcement count
    """
    provenance = fact.get("provenance", {})
    confidence = provenance.get("confidence", 0.8)
    timestamp = provenance.get("timestamp", "")
    reinforcements = fact.get("reinforcements", 0)
    
    decay = calculate_decay(timestamp, half_life_days, reinforcements)
    
    # Combined score: confidence * decay
    return confidence * decay


def apply_decay_to_graph(
    graph_file: Path,
    half_life_days: float = DEFAULT_HALF_LIFE,
    dry_run: bool = True,
) -> list[dict]:
    """
    Apply decay scoring to all facts in graph.
    
    Returns list of facts with their decay scores.
    """
    if not graph_file.exists():
        return []
    
    scored_facts = []
    
    for line in graph_file.read_text().strip().split('\n'):
        if not line:
            continue
        try:
            fact = json.loads(line)
            score = score_fact(fact, half_life_days)
            fact["_decay_score"] = round(score, 3)
            scored_facts.append(fact)
        except:
            continue
    
    # Sort by score (lowest first = most decayed)
    scored_facts.sort(key=lambda f: f.get("_decay_score", 0))
    
    return scored_facts


def prune_decayed(
    graph_file: Path,
    threshold: float = 0.1,
    half_life_days: float = DEFAULT_HALF_LIFE,
    dry_run: bool = True,
) -> tuple[int, int]:
    """
    Remove facts below decay threshold.
    
    Returns (kept_count, pruned_count).
    """
    scored = apply_decay_to_graph(graph_file, half_life_days, dry_run=True)
    
    keep = [f for f in scored if f.get("_decay_score", 0) >= threshold]
    prune = [f for f in scored if f.get("_decay_score", 0) < threshold]
    
    if not dry_run and prune:
        # Rewrite graph without pruned facts
        with file_lock(graph_file):
            with open(graph_file, "w") as out:
                for fact in keep:
                    del fact["_decay_score"]  # Remove temp field
                    out.write(json.dumps(fact) + "\n")
    
    return len(keep), len(prune)


def reinforce_fact(
    graph_file: Path,
    subject: str,
    predicate: str,
    obj: str,
) -> bool:
    """
    Reinforce a fact (increment reinforcement count).
    
    Called when a fact is confirmed/mentioned again.
    """
    if not graph_file.exists():
        return False
    
    lines = graph_file.read_text().strip().split('\n')
    updated = False
    
    with file_lock(graph_file):
        with open(graph_file, "w") as out:
            for line in lines:
                if not line:
                    continue
                try:
                    fact = json.loads(line)
                    if (fact.get("subject") == subject and
                        fact.get("predicate") == predicate and
                        fact.get("object") == obj):
                        fact["reinforcements"] = fact.get("reinforcements", 0) + 1
                        fact["provenance"]["last_reinforced"] = datetime.now().isoformat()
                        updated = True
                    out.write(json.dumps(fact) + "\n")
                except:
                    out.write(line + "\n")
    
    return updated
