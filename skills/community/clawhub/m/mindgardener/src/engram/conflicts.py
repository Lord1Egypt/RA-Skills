#!/usr/bin/env python3
"""
Conflict detection and resolution for MindGardener.

Detects when new facts contradict existing facts and provides
resolution strategies.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .filelock import file_lock, safe_append


# Predicates that indicate state (only one value can be true at a time)
STATE_PREDICATES = {
    "works_at", "lives_in", "status", "role", "title", "position",
    "employed_by", "member_of", "located_in", "married_to", "dating",
}

# Predicates that can have multiple values
ADDITIVE_PREDICATES = {
    "knows", "contacted", "applied_to", "submitted_pr", "merged_pr",
    "worked_on", "contributed_to", "mentioned", "discussed",
}


class Conflict:
    """Represents a detected conflict between facts."""
    
    def __init__(
        self,
        subject: str,
        predicate: str,
        old_value: str,
        new_value: str,
        old_provenance: dict,
        new_provenance: dict,
    ):
        self.subject = subject
        self.predicate = predicate
        self.old_value = old_value
        self.new_value = new_value
        self.old_provenance = old_provenance
        self.new_provenance = new_provenance
        self.detected_at = datetime.now().isoformat()
        self.resolved = False
        self.resolution = None
    
    def to_dict(self) -> dict:
        return {
            "subject": self.subject,
            "predicate": self.predicate,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "old_provenance": self.old_provenance,
            "new_provenance": self.new_provenance,
            "detected_at": self.detected_at,
            "resolved": self.resolved,
            "resolution": self.resolution,
        }
    
    def __str__(self) -> str:
        return (
            f"Conflict: {self.subject} {self.predicate}\n"
            f"  Old: {self.old_value} (confidence: {self.old_provenance.get('confidence', '?')})\n"
            f"  New: {self.new_value} (confidence: {self.new_provenance.get('confidence', '?')})"
        )


def is_conflicting_predicate(predicate: str) -> bool:
    """Check if predicate represents state that can only have one value."""
    pred_lower = predicate.lower().replace("_", "")
    for state_pred in STATE_PREDICATES:
        if state_pred.replace("_", "") in pred_lower:
            return True
    return False


def find_existing_fact(
    graph_file: Path,
    subject: str,
    predicate: str,
) -> Optional[dict]:
    """Find the most recent fact for subject+predicate."""
    if not graph_file.exists():
        return None
    
    matches = []
    for line in graph_file.read_text().strip().split('\n'):
        if not line:
            continue
        try:
            fact = json.loads(line)
            if (fact.get("subject") == subject and 
                fact.get("predicate") == predicate):
                matches.append(fact)
        except json.JSONDecodeError:
            continue
    
    if not matches:
        return None
    
    # Return most recent by timestamp
    return max(matches, key=lambda f: f.get("provenance", {}).get("timestamp", ""))


def detect_conflict(
    graph_file: Path,
    new_triplet: dict,
    new_provenance: dict,
) -> Optional[Conflict]:
    """
    Check if new triplet conflicts with existing facts.
    
    Returns Conflict if detected, None otherwise.
    """
    subject = new_triplet.get("subject")
    predicate = new_triplet.get("predicate")
    new_value = new_triplet.get("object")
    
    # Only check state predicates for conflicts
    if not is_conflicting_predicate(predicate):
        return None
    
    existing = find_existing_fact(graph_file, subject, predicate)
    if not existing:
        return None
    
    old_value = existing.get("object")
    
    # No conflict if values are the same
    if old_value == new_value:
        return None
    
    # Conflict detected!
    return Conflict(
        subject=subject,
        predicate=predicate,
        old_value=old_value,
        new_value=new_value,
        old_provenance=existing.get("provenance", {}),
        new_provenance=new_provenance,
    )


def log_conflict(conflicts_file: Path, conflict: Conflict):
    """Log conflict to conflicts.md for human review."""
    with file_lock(conflicts_file):
        # Create file if doesn't exist
        if not conflicts_file.exists():
            conflicts_file.write_text("# Detected Conflicts\n\n")
        
        # Append conflict entry
        entry = f"""
## {conflict.subject} → {conflict.predicate} ({conflict.detected_at[:10]})

| | Old | New |
|---|-----|-----|
| Value | {conflict.old_value} | {conflict.new_value} |
| Source | {conflict.old_provenance.get('source', '?')} | {conflict.new_provenance.get('source', '?')} |
| Confidence | {conflict.old_provenance.get('confidence', '?')} | {conflict.new_provenance.get('confidence', '?')} |
| Agent | {conflict.old_provenance.get('agent', '?')} | {conflict.new_provenance.get('agent', '?')} |

**Status:** Unresolved

---
"""
        with open(conflicts_file, "a") as f:
            f.write(entry)


def resolve_conflict(
    conflict: Conflict,
    strategy: str = "latest_wins",
) -> dict:
    """
    Resolve a conflict using the specified strategy.
    
    Strategies:
    - latest_wins: Newer timestamp wins
    - confidence_wins: Higher confidence wins
    - keep_both: Mark both as valid (for human review)
    
    Returns the winning fact.
    """
    old_ts = conflict.old_provenance.get("timestamp", "")
    new_ts = conflict.new_provenance.get("timestamp", "")
    old_conf = conflict.old_provenance.get("confidence", 0.5)
    new_conf = conflict.new_provenance.get("confidence", 0.5)
    
    if strategy == "latest_wins":
        winner = "new" if new_ts >= old_ts else "old"
    elif strategy == "confidence_wins":
        winner = "new" if new_conf >= old_conf else "old"
    elif strategy == "keep_both":
        winner = "both"
    else:
        winner = "new"  # Default to latest
    
    conflict.resolved = True
    conflict.resolution = {
        "strategy": strategy,
        "winner": winner,
        "resolved_at": datetime.now().isoformat(),
    }
    
    if winner == "new":
        return {
            "subject": conflict.subject,
            "predicate": conflict.predicate,
            "object": conflict.new_value,
            "provenance": conflict.new_provenance,
        }
    elif winner == "old":
        return {
            "subject": conflict.subject,
            "predicate": conflict.predicate,
            "object": conflict.old_value,
            "provenance": conflict.old_provenance,
        }
    else:
        # keep_both - return new but mark as conflicted
        return {
            "subject": conflict.subject,
            "predicate": conflict.predicate,
            "object": conflict.new_value,
            "provenance": conflict.new_provenance,
            "conflicted": True,
            "alternative": conflict.old_value,
        }
