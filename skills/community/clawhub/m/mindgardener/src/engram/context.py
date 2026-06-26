"""Context assembly — token-budget-aware context selection.

Solves the "context delivery problem" described by Koylanai:
Instead of dumping everything at boot, assemble the right context
per turn based on a query and token budget.

Returns a manifest documenting what was loaded and what was skipped.
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .config import EngramConfig
from .recall import fuzzy_score, extract_wikilinks, search_graph


CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English."""
    return max(1, len(text) // CHARS_PER_TOKEN) if text is not None else 1


# Aliases for test compatibility
_estimate_tokens = estimate_tokens


def assemble_context(
    query: str,
    config: EngramConfig,
    token_budget: int = 4000,
    budget_tokens: int | None = None,  # Alias for token_budget
    include_recent_days: int = 2,
    max_entities: int = 10,
    max_hops: int = 1,
    hops: int | None = None,  # Alias for max_hops
    include_graph: bool = True,
    include_memory: bool = True,
) -> dict:
    """Assemble context for a query within a token budget.
    
    Returns:
        {
            "context": str,          # The assembled context text
            "manifest": {
                "query": str,
                "token_budget": int,
                "tokens_used": int,
                "loaded": [...],       # What was included
                "skipped": [...],      # What was excluded and why
                "timestamp": str,
            }
        }
    """
    # Resolve aliases
    if budget_tokens is not None:
        token_budget = budget_tokens
    if hops is not None:
        max_hops = hops
    
    manifest_loaded = []
    manifest_skipped = []
    context_parts = []
    tokens_used = 0
    
    # --- Phase 1: Entity recall (highest priority) ---
    entity_matches = _score_entities(query, config)
    
    for score, name, content, filepath in entity_matches[:max_entities]:
        est = estimate_tokens(content)
        if tokens_used + est <= token_budget:
            context_parts.append(f"## Entity: {name}\n{content}")
            tokens_used += est
            manifest_loaded.append({
                "type": "entity",
                "name": name,
                "score": round(score, 3),
                "tokens": est,
            })
        else:
            # Try truncated version (first 20 lines)
            truncated = "\n".join(content.split("\n")[:20])
            est_trunc = estimate_tokens(truncated)
            if tokens_used + est_trunc <= token_budget:
                context_parts.append(f"## Entity: {name} (truncated)\n{truncated}")
                tokens_used += est_trunc
                manifest_loaded.append({
                    "type": "entity",
                    "name": name,
                    "score": round(score, 3),
                    "tokens": est_trunc,
                    "truncated": True,
                })
            else:
                manifest_skipped.append({
                    "type": "entity",
                    "name": name,
                    "score": round(score, 3),
                    "tokens": est,
                    "reason": "token_budget_exceeded",
                })
    
    # --- Phase 2: Linked entities (1-hop graph traversal) ---
    if max_hops >= 1 and entity_matches:
        top_content = entity_matches[0][2] if entity_matches else ""
        linked = extract_wikilinks(top_content)
        
        for link in linked[:5]:
            link_file = config.entities_dir / f"{link.replace(' ', '-')}.md"
            if link_file.exists():
                link_content = link_file.read_text()
                # Summary only for linked entities (first 8 lines)
                summary = "\n".join(link_content.split("\n")[:8])
                est = estimate_tokens(summary)
                if tokens_used + est <= token_budget:
                    context_parts.append(f"## Linked: {link}\n{summary}")
                    tokens_used += est
                    manifest_loaded.append({
                        "type": "linked_entity",
                        "name": link,
                        "tokens": est,
                    })
                else:
                    manifest_skipped.append({
                        "type": "linked_entity",
                        "name": link,
                        "tokens": est,
                        "reason": "token_budget_exceeded",
                    })
    
    # --- Phase 3: Graph connections ---
    graph_results = search_graph(query, config) if include_graph else []
    if graph_results:
        graph_text = "\n".join(graph_results[:10])
        est = estimate_tokens(graph_text)
        if tokens_used + est <= token_budget:
            context_parts.append(f"## Graph Connections\n{graph_text}")
            tokens_used += est
            manifest_loaded.append({
                "type": "graph",
                "count": len(graph_results[:10]),
                "tokens": est,
            })
    
    # --- Phase 4: Recent daily logs ---
    today = datetime.now()
    for day_offset in range(include_recent_days):
        date = today - timedelta(days=day_offset)
        date_str = date.strftime("%Y-%m-%d")
        log_file = config.memory_dir / f"{date_str}.md"
        
        if log_file.exists():
            log_content = log_file.read_text()
            est = estimate_tokens(log_content)
            
            if tokens_used + est <= token_budget:
                context_parts.append(f"## Daily Log: {date_str}\n{log_content}")
                tokens_used += est
                manifest_loaded.append({
                    "type": "daily_log",
                    "date": date_str,
                    "tokens": est,
                })
            else:
                # Try to extract only query-relevant lines
                relevant = _extract_relevant_lines(log_content, query)
                if relevant:
                    est_rel = estimate_tokens(relevant)
                    if tokens_used + est_rel <= token_budget:
                        context_parts.append(
                            f"## Daily Log: {date_str} (relevant excerpts)\n{relevant}"
                        )
                        tokens_used += est_rel
                        manifest_loaded.append({
                            "type": "daily_log",
                            "date": date_str,
                            "tokens": est_rel,
                            "filtered": True,
                        })
                    else:
                        manifest_skipped.append({
                            "type": "daily_log",
                            "date": date_str,
                            "tokens": est,
                            "reason": "token_budget_exceeded",
                        })
                else:
                    manifest_skipped.append({
                        "type": "daily_log",
                        "date": date_str,
                        "tokens": est,
                        "reason": "no_relevant_content",
                    })
    
    # --- Phase 5: Long-term memory (MEMORY.md) ---
    if include_memory and config.long_term_memory.exists():
        ltm_content = config.long_term_memory.read_text()
        est = estimate_tokens(ltm_content)
        if tokens_used + est <= token_budget:
            context_parts.append(f"## Long-Term Memory\n{ltm_content}")
            tokens_used += est
            manifest_loaded.append({
                "type": "long_term_memory",
                "tokens": est,
            })
        else:
            # Extract relevant sections
            relevant = _extract_relevant_lines(ltm_content, query)
            if relevant:
                est_rel = estimate_tokens(relevant)
                if tokens_used + est_rel <= token_budget:
                    context_parts.append(
                        f"## Long-Term Memory (relevant excerpts)\n{relevant}"
                    )
                    tokens_used += est_rel
                    manifest_loaded.append({
                        "type": "long_term_memory",
                        "tokens": est_rel,
                        "filtered": True,
                    })
    
    # Build manifest
    manifest = {
        "query": query,
        "token_budget": token_budget,
        "tokens_used": tokens_used,
        "tokens_remaining": token_budget - tokens_used,
        "utilization": round(tokens_used / token_budget, 2) if token_budget else 0,
        "loaded": manifest_loaded,
        "skipped": manifest_skipped,
        "loaded_count": len(manifest_loaded),
        "skipped_count": len(manifest_skipped),
        "timestamp": datetime.now().isoformat(),
    }
    
    # Log manifest
    _log_manifest(config, manifest)
    
    return {
        "context": "\n\n---\n\n".join(context_parts),
        "manifest": manifest,
    }


def _score_entities(query: str, config: EngramConfig) -> list[tuple]:
    """Score and rank all entities against query."""
    if not config.entities_dir.exists():
        return []
    
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    # Resolve aliases
    try:
        from .aliases import load_aliases, resolve_name
        aliases = load_aliases(config.entities_dir)
        resolved = resolve_name(query, aliases)
        if resolved != query:
            query = resolved
            query_lower = query.lower()
            query_words = set(query_lower.split())
    except ImportError:
        pass
    
    matches = []
    for entity_file in sorted(config.entities_dir.glob("*.md")):
        name = entity_file.stem.replace("-", " ")
        content = entity_file.read_text()
        
        name_score = fuzzy_score(query, name)
        content_score = 0.0
        if query_lower in content.lower():
            content_score = 0.5
        elif any(w in content.lower() for w in query_words if len(w) >= 3):
            content_score = 0.1
        
        score = max(name_score, content_score)
        if score > 0.1:
            matches.append((score, name, content, entity_file))
    
    matches.sort(reverse=True)
    return matches


def _extract_relevant_lines(content: str, query: str, context_lines: int = 3) -> str:
    """Extract lines from content that are relevant to the query."""
    query_words = set(query.lower().split())
    lines = content.split("\n")
    relevant_indices = set()
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if any(w in line_lower for w in query_words if len(w) >= 3):
            # Include surrounding context
            for j in range(max(0, i - context_lines), min(len(lines), i + context_lines + 1)):
                relevant_indices.add(j)
    
    if not relevant_indices:
        return ""
    
    return "\n".join(lines[i] for i in sorted(relevant_indices))


def _log_manifest(config: EngramConfig, manifest: dict):
    """Append manifest to the manifest log."""
    log_file = config.memory_dir / "context-manifests.jsonl"
    try:
        with open(log_file, "a") as f:
            f.write(json.dumps(manifest) + "\n")
    except OSError:
        pass  # Non-critical


# --- Compatibility layer for Sven's tests ---

class ContextResult:
    """Simple result container."""
    def __init__(self, context: str, manifest: dict):
        self.context = context
        self.manifest = manifest
        self.tokens_used = manifest.get("tokens_used", 0)
        self.loaded = manifest.get("loaded", [])
        self.skipped = manifest.get("skipped", [])


def _score_entity(query: str, name: str, content: str, query_words: set) -> float:
    """Score a single entity against query. Test-compatible wrapper."""
    from .recall import fuzzy_score
    name_score = fuzzy_score(query, name)
    content_score = 0.0
    query_lower = query.lower()
    if query_lower in content.lower():
        content_score = 0.5
    elif any(w in content.lower() for w in query_words if len(w) >= 3):
        content_score = 0.1
    return max(name_score, content_score)


def _score_daily(query: str, content: str, query_words: set, days_ago: int = 0) -> float:
    """Score daily log relevance. Test-compatible wrapper."""
    query_lower = query.lower()
    score = 0.0
    if query_lower in content.lower():
        score = 0.5
    elif any(w in content.lower() for w in query_words if len(w) >= 3):
        score = 0.3
    # Recency decay
    if days_ago > 0:
        score *= max(0.1, 1.0 - (days_ago * 0.15))
    return score
