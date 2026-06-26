#!/usr/bin/env python3
"""
Experience Manager for Live-Evo Claude Skill.
Simplified version for Claude Code environment.
"""
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Experience storage directory — always in ~/.live-evo/ for persistence
# This works regardless of whether live-evo is installed as a personal skill or plugin
EXPERIENCE_DIR = Path.home() / ".live-evo"
DB_PATH = EXPERIENCE_DIR / "experience_db.jsonl"
WEIGHT_HISTORY_PATH = EXPERIENCE_DIR / "weight_history.jsonl"

# Seed data bundled with the skill (for first-run initialization)
_SCRIPT_DIR = Path(__file__).parent
_BUNDLED_SEED = _SCRIPT_DIR.parent / "experiences" / "experience_db.jsonl"

# Weight parameters
INITIAL_WEIGHT = 1.0
MIN_WEIGHT = 0.1
MAX_WEIGHT = 2.0
WEIGHT_INCREASE_RATE = 0.3
WEIGHT_DECREASE_RATE = 0.2


def ensure_dirs():
    """Ensure experience directories exist. Copy seed data on first run."""
    EXPERIENCE_DIR.mkdir(parents=True, exist_ok=True)
    # On first run, copy bundled seed experiences if DB doesn't exist yet
    if not DB_PATH.exists() and _BUNDLED_SEED.exists():
        import shutil
        shutil.copy2(_BUNDLED_SEED, DB_PATH)


def generate_id(text: str) -> str:
    """Generate a short unique ID from text."""
    return hashlib.md5(text.encode()).hexdigest()[:8]


def load_experiences() -> List[Dict]:
    """Load all experiences from the database."""
    ensure_dirs()
    experiences = []
    if DB_PATH.exists():
        with open(DB_PATH, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        exp = json.loads(line)
                        if 'weight' not in exp:
                            exp['weight'] = INITIAL_WEIGHT
                        experiences.append(exp)
                    except json.JSONDecodeError:
                        pass
    return experiences


def save_experiences(experiences: List[Dict]):
    """Save all experiences to the database."""
    ensure_dirs()
    with open(DB_PATH, 'w') as f:
        for exp in experiences:
            f.write(json.dumps(exp, default=str) + "\n")


def add_experience(question: str, failure_reason: str, improvement: str,
                   missed_information: str = "", category: str = "other") -> Dict:
    """Add a new experience to the database."""
    ensure_dirs()

    exp = {
        "id": generate_id(question + datetime.now().isoformat()),
        "question": question,
        "failure_reason": failure_reason,
        "improvement": improvement,
        "missed_information": missed_information,
        "category": category,
        "weight": INITIAL_WEIGHT,
        "created_at": datetime.now().isoformat(),
        "use_count": 0,
        "success_count": 0,
    }

    with open(DB_PATH, 'a') as f:
        f.write(json.dumps(exp, default=str) + "\n")

    return exp


def simple_similarity(query: str, text: str) -> float:
    """
    Simple keyword-based similarity score.
    In production, use embeddings for better results.
    """
    query_words = set(query.lower().split())
    text_words = set(text.lower().split())

    if not query_words or not text_words:
        return 0.0

    intersection = query_words & text_words
    union = query_words | text_words

    # Jaccard similarity
    jaccard = len(intersection) / len(union) if union else 0.0

    # Boost for exact phrase matches
    query_lower = query.lower()
    text_lower = text.lower()
    phrase_boost = 0.3 if query_lower in text_lower or text_lower in query_lower else 0.0

    return min(1.0, jaccard + phrase_boost)


def find_relevant_experiences(query: str, top_k: int = 5,
                              threshold: float = 0.1,
                              category: Optional[str] = None) -> List[Tuple[Dict, float]]:
    """
    Find relevant experiences using simple keyword matching.
    Returns list of (experience, weighted_score) tuples.
    """
    experiences = load_experiences()

    if category:
        experiences = [e for e in experiences if e.get("category") == category]

    if not experiences:
        return []

    results = []
    for exp in experiences:
        # Combine searchable fields
        search_text = " ".join([
            exp.get("question", ""),
            exp.get("failure_reason", ""),
            exp.get("improvement", ""),
            exp.get("missed_information", ""),
        ])

        sim_score = simple_similarity(query, search_text)
        weight = exp.get("weight", INITIAL_WEIGHT)
        weighted_score = sim_score * weight

        if weighted_score >= threshold:
            results.append((exp, weighted_score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_k]


def generate_guideline(task_title: str, experiences: List[Dict]) -> str:
    """
    Generate a task-specific guideline from experiences.
    """
    if not experiences:
        return ""

    lines = ["## Task-Specific Guidelines (from past experiences)\n"]

    for i, exp in enumerate(experiences, 1):
        lines.append(f"### Lesson {i} (weight: {exp.get('weight', 1.0):.2f})")
        lines.append(f"**From similar task:** {exp.get('question', '')[:100]}")
        if exp.get('failure_reason'):
            lines.append(f"**What went wrong:** {exp.get('failure_reason', '')}")
        if exp.get('improvement'):
            lines.append(f"**Key lesson:** {exp.get('improvement', '')}")
        if exp.get('missed_information'):
            lines.append(f"**Don't forget:** {exp.get('missed_information', '')}")
        lines.append("")

    lines.append("---")
    lines.append("**Apply these lessons to your current task. Be cautious about over-generalizing.**")

    return "\n".join(lines)


def update_weights(experience_ids: List[str], helped: bool) -> Dict:
    """
    Update experience weights based on whether they helped or hurt.

    Args:
        experience_ids: IDs of experiences that were used
        helped: True if using experiences improved the outcome

    Returns:
        Summary of weight updates
    """
    experiences = load_experiences()
    updates = []

    for exp in experiences:
        if exp.get("id") in experience_ids:
            old_weight = exp.get("weight", INITIAL_WEIGHT)

            if helped:
                new_weight = min(old_weight + WEIGHT_INCREASE_RATE, MAX_WEIGHT)
                exp["success_count"] = exp.get("success_count", 0) + 1
            else:
                new_weight = max(old_weight - WEIGHT_DECREASE_RATE, MIN_WEIGHT)

            exp["weight"] = new_weight
            exp["use_count"] = exp.get("use_count", 0) + 1
            exp["last_used"] = datetime.now().isoformat()

            updates.append({
                "id": exp["id"],
                "old_weight": old_weight,
                "new_weight": new_weight,
                "change": "increased" if helped else "decreased"
            })

            # Log weight change
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "experience_id": exp["id"],
                "old_weight": old_weight,
                "new_weight": new_weight,
                "helped": helped,
            }
            with open(WEIGHT_HISTORY_PATH, 'a') as f:
                f.write(json.dumps(log_entry) + "\n")

    save_experiences(experiences)
    return {"updates": updates, "total_updated": len(updates)}


def get_statistics() -> Dict:
    """Get statistics about the experience database."""
    experiences = load_experiences()

    if not experiences:
        return {"total": 0, "message": "No experiences yet"}

    categories = {}
    weights = []

    for exp in experiences:
        cat = exp.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
        weights.append(exp.get("weight", INITIAL_WEIGHT))

    return {
        "total_experiences": len(experiences),
        "categories": categories,
        "average_weight": sum(weights) / len(weights),
        "min_weight": min(weights),
        "max_weight": max(weights),
        "high_quality_count": len([w for w in weights if w >= 1.5]),
        "low_quality_count": len([w for w in weights if w <= 0.5]),
    }


if __name__ == "__main__":
    # Test
    print("Experience Manager loaded successfully")
    print(f"Experience directory: {EXPERIENCE_DIR}")
    stats = get_statistics()
    print(f"Statistics: {json.dumps(stats, indent=2)}")
