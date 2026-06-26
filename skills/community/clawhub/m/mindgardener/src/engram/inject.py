#!/usr/bin/env python3
"""
Auto-injection for MindGardener.

Generates context to inject at session start based on:
- Recent facts (last N days)
- Relevant entities (by topic/query)
- Active projects/tasks
- Identity beliefs
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .config import EngramConfig
from .recall import recall, list_entities


def get_recent_facts(config: EngramConfig, days: int = 2) -> list[dict]:
    """Get facts from the last N days."""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    
    facts = []
    if config.graph_file.exists():
        for line in config.graph_file.read_text().strip().split('\n'):
            if not line:
                continue
            try:
                fact = json.loads(line)
                ts = fact.get("provenance", {}).get("timestamp", "")
                if ts >= cutoff:
                    facts.append(fact)
            except:
                continue
    
    return facts


def get_top_entities(config: EngramConfig, limit: int = 10) -> list[dict]:
    """Get most connected entities."""
    entities = list_entities(config)
    
    # Count connections per entity
    connections = {}
    if config.graph_file.exists():
        for line in config.graph_file.read_text().strip().split('\n'):
            if not line:
                continue
            try:
                fact = json.loads(line)
                subj = fact.get("subject", "")
                obj = fact.get("object", "")
                connections[subj] = connections.get(subj, 0) + 1
                connections[obj] = connections.get(obj, 0) + 1
            except:
                continue
    
    # Sort by connections
    for e in entities:
        e["connections"] = connections.get(e["name"], 0)
    
    return sorted(entities, key=lambda x: -x["connections"])[:limit]


def get_active_beliefs(config: EngramConfig) -> list[dict]:
    """Get current identity beliefs."""
    beliefs_file = config.memory_dir / "self-model.json"
    if not beliefs_file.exists():
        return []
    
    try:
        model = json.loads(beliefs_file.read_text())
        return model.get("beliefs", [])[:10]  # Top 10 beliefs
    except:
        return []


def format_fact(fact: dict) -> str:
    """Format a fact for injection."""
    subj = fact.get("subject", "?")
    pred = fact.get("predicate", "?")
    obj = fact.get("object", "?")
    conf = fact.get("provenance", {}).get("confidence", "?")
    return f"- {subj} → {pred} → {obj} (confidence: {conf})"


def format_entity(entity: dict) -> str:
    """Format an entity for injection."""
    name = entity.get("name", "?")
    etype = entity.get("type", "?")
    facts = entity.get("facts", [])[:3]
    facts_str = "; ".join(facts) if facts else "no facts"
    return f"- **{name}** ({etype}): {facts_str}"


def generate_context(
    config: EngramConfig,
    query: Optional[str] = None,
    max_tokens: int = 2000,
    strategy: str = "recent_and_relevant",
) -> str:
    """
    Generate context for injection.
    
    Strategies:
    - recent_only: Just chronological recent facts
    - recent_and_relevant: Recent facts + top entities
    - query_based: Focus on query-relevant content
    """
    sections = []
    char_budget = max_tokens * 4  # Rough chars-to-tokens
    
    # Always include: recent facts
    recent = get_recent_facts(config, days=2)
    if recent:
        recent_section = "## Recent Facts (last 48h)\n"
        for fact in recent[-20:]:  # Last 20
            recent_section += format_fact(fact) + "\n"
        sections.append(recent_section)
    
    if strategy in ("recent_and_relevant", "query_based"):
        # Top entities
        top = get_top_entities(config, limit=5)
        if top:
            entities_section = "## Key Entities\n"
            for e in top:
                entities_section += format_entity(e) + "\n"
            sections.append(entities_section)
    
    if strategy == "query_based" and query:
        # Query-specific recall
        results = recall(config, query, limit=10)
        if results:
            query_section = f"## Relevant to '{query}'\n"
            for r in results:
                query_section += f"- {r}\n"
            sections.append(query_section)
    
    # Identity beliefs
    beliefs = get_active_beliefs(config)
    if beliefs:
        beliefs_section = "## Current Beliefs\n"
        for b in beliefs[:5]:
            claim = b.get("claim", "?")
            conf = b.get("confidence", "?")
            beliefs_section += f"- [{conf:.0%}] {claim}\n"
        sections.append(beliefs_section)
    
    # Combine and truncate
    context = "\n".join(sections)
    if len(context) > char_budget:
        context = context[:char_budget] + "\n[...truncated...]"
    
    return context


def write_recall_context(config: EngramConfig, output_path: Optional[Path] = None, **kwargs):
    """Write context to RECALL-CONTEXT.md."""
    if output_path is None:
        output_path = config.workspace / "RECALL-CONTEXT.md"
    
    context = generate_context(config, **kwargs)
    
    header = f"""# Recall Context
Generated: {datetime.now().isoformat()}
Strategy: {kwargs.get('strategy', 'recent_and_relevant')}

---

"""
    output_path.write_text(header + context)
    return output_path
