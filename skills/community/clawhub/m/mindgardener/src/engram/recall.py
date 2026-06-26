"""Graph-aware recall — query the knowledge graph."""

import json
import re
from pathlib import Path
from typing import Optional

from .config import EngramConfig


def levenshtein(s1: str, s2: str) -> int:
    """Compute Levenshtein edit distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            # Insertion, deletion, substitution
            curr_row.append(min(
                prev_row[j + 1] + 1,
                curr_row[j] + 1,
                prev_row[j] + (0 if c1 == c2 else 1)
            ))
        prev_row = curr_row
    return prev_row[-1]


def fuzzy_score(query: str, target: str, threshold: float = 0.6) -> float:
    """Score how well query matches target. Returns 0.0-1.0.
    
    Combines multiple strategies:
    - Exact match
    - Substring containment
    - Word overlap
    - Levenshtein distance (normalized)
    - Prefix matching
    - Initials matching (e.g. "PS" → "Peter Steinberger")
    """
    q_orig = query.strip()
    q = q_orig.lower()
    t = target.lower().strip()
    
    # Initials matching ("PS" → "Peter Steinberger") — check before lowering
    if len(q_orig) <= 5 and q_orig == q_orig.upper() and q_orig.isalpha():
        initials = "".join(w[0].upper() for w in target.split() if w)
        if q_orig.upper() == initials:
            return 0.75
    
    # Exact match
    if q == t:
        return 1.0
    
    # Substring containment (either direction)
    if q in t:
        return 0.9
    if t in q:
        return 0.85
    
    # Word-level matching
    q_words = set(q.split())
    t_words = set(t.split())
    
    if q_words and t_words:
        # Any word exact match
        common = q_words & t_words
        if common:
            return 0.7 + 0.2 * (len(common) / max(len(q_words), len(t_words)))
        
        # Word prefix matching ("stein" matches "steinberger")
        for qw in q_words:
            for tw in t_words:
                if tw.startswith(qw) and len(qw) >= 3:
                    return 0.7
                if qw.startswith(tw) and len(tw) >= 3:
                    return 0.65
    
    # Levenshtein distance (normalized)
    max_len = max(len(q), len(t))
    if max_len > 0:
        dist = levenshtein(q, t)
        similarity = 1.0 - (dist / max_len)
        if similarity >= threshold:
            return similarity * 0.6  # Scale down so fuzzy never beats exact
    
    # Per-word Levenshtein (handles typos in multi-word names)
    if len(q_words) > 0 and len(t_words) > 0:
        best_word_score = 0
        for qw in q_words:
            for tw in t_words:
                if len(qw) >= 3 and len(tw) >= 3:
                    wdist = levenshtein(qw, tw)
                    wsim = 1.0 - (wdist / max(len(qw), len(tw)))
                    best_word_score = max(best_word_score, wsim)
        if best_word_score >= threshold:
            return best_word_score * 0.5
    
    return 0.0


def recall(query: str, config: EngramConfig, hops: int = 1) -> str:
    """
    Query the engram knowledge graph with fuzzy matching.
    
    1. Fuzzy-match entity files by name
    2. Search entity content for query terms
    3. Load matching entity pages
    4. Follow wikilinks for N hops
    5. Search graph.jsonl for related triplets
    6. Return formatted context
    """
    results = []
    
    # Normalize query
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    # Load aliases
    try:
        from .aliases import load_aliases, resolve_name
        aliases = load_aliases(config.entities_dir)
        # Check if query matches an alias
        resolved = resolve_name(query, aliases)
        if resolved != query:
            query = resolved
            query_lower = query.lower()
            query_words = set(query_lower.split())
    except ImportError:
        pass
    
    # Search entity files with fuzzy matching
    matching_entities = []
    for entity_file in sorted(config.entities_dir.glob("*.md")):
        name = entity_file.stem.replace("-", " ")
        content = entity_file.read_text()
        
        # Fuzzy name match
        name_score = fuzzy_score(query, name)
        
        # Content match (lower priority)
        content_score = 0.0
        if query_lower in content.lower():
            content_score = 0.5
        elif any(w in content.lower() for w in query_words if len(w) >= 3):
            content_score = 0.1
        
        score = max(name_score, content_score)
        
        if score > 0.1:  # Minimum threshold
            matching_entities.append((score, name, content, entity_file))
    
    matching_entities.sort(reverse=True)
    
    if not matching_entities:
        results.append(f"No entities found matching '{query}'")
        # Fall back to graph search
        graph_results = search_graph(query, config)
        if graph_results:
            results.append("\n**Graph matches:**")
            results.extend(graph_results)
        return "\n".join(results)
    
    # Top match
    top_score, top_name, top_content, _ = matching_entities[0]
    results.append(top_content)
    
    # Follow wikilinks for hop 1
    if hops >= 1:
        linked = extract_wikilinks(top_content)
        for link in linked[:5]:  # Max 5 linked entities
            link_file = config.entities_dir / f"{link.replace(' ', '-')}.md"
            if link_file.exists():
                link_content = link_file.read_text()
                # Only include summary (first few lines)
                summary_lines = link_content.split("\n")[:8]
                results.append(f"\n---\n**Linked: [[{link}]]**")
                results.append("\n".join(summary_lines))
    
    # Add relevant triplets
    graph_results = search_graph(query, config)
    if graph_results:
        results.append("\n---\n**Graph connections:**")
        results.extend(graph_results)
    
    return "\n".join(results)


def search_graph(query: str, config: EngramConfig) -> list[str]:
    """Search graph.jsonl for matching triplets."""
    if not config.graph_file.exists():
        return []
    
    query_lower = query.lower()
    matches = []
    
    for line in config.graph_file.read_text().strip().split("\n"):
        if not line:
            continue
        try:
            t = json.loads(line)
            # Check if query matches subject, object, or detail
            if (query_lower in (t.get("subject") or "").lower() or
                query_lower in (t.get("object") or "").lower() or
                query_lower in (t.get("detail") or "").lower()):
                matches.append(
                    f"- [{t.get('date', '?')}] {t['subject']} → {t['predicate']} → {t['object']}"
                    + (f" ({t['detail']})" if t.get("detail") else "")
                )
        except json.JSONDecodeError:
            continue
    
    return matches


def extract_wikilinks(text: str) -> list[str]:
    """Extract [[wikilinks]] from text."""
    links = re.findall(r'\[\[([^\]]+)\]\]', text)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for link in links:
        if link not in seen and not re.match(r'^\d{4}-\d{2}-\d{2}$', link):
            seen.add(link)
            unique.append(link)
    return unique


def list_entities(config: EngramConfig) -> list[dict]:
    """List all entities with their types."""
    entities = []
    for f in sorted(config.entities_dir.glob("*.md")):
        content = f.read_text()
        entity_type = "unknown"
        type_match = re.search(r'\*\*Type:\*\*\s*(\w+)', content)
        if type_match:
            entity_type = type_match.group(1)
        
        # Count timeline entries
        timeline_count = len(re.findall(r'### \[\[', content))
        
        entities.append({
            "name": f.stem.replace("-", " "),
            "type": entity_type,
            "file": str(f),
            "timeline_entries": timeline_count,
        })
    return entities
