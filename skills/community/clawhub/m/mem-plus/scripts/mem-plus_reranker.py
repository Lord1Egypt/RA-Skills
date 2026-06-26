#!/usr/bin/env python3
"""
MemPalace Enhancement Layer
==========================
MMR reranking + content deduplication + metadata stripping
"""
import os
import sys
import json
import hashlib
from typing import List, Dict, Any

sys.path.insert(0, '/Users/mars/Library/Python/3.9/lib/python/site-packages')

# ---------------------------------------------------------------------------
# 1. Metadata Stripping
# ---------------------------------------------------------------------------

import re

# Patterns for metadata stripping
STRIP_PATTERNS = [
    # JSON metadata blocks (feishu/webhook)
    (r'^\[message_id:\s*[^\]]+\]\s*', ''),
    (r'^Sender\s*\(untrusted metadata\):\s*```json\s*\n[\s\S]*?```\s*\n', ''),
    (r'^```json\s*\n[\s\S]*?```\s*\n', ''),
    # OpenClaw message envelope
    (r'^\[user:ou_[^\]]+\]\s*', ''),
    (r'^Conversation info[\s\S]*?```\s*\n', ''),
    # Markdown code fences
    (r'^```\w*\s*\n', ''),
    (r'^```\s*\n', ''),
    # Generic metadata prefix patterns
    (r'^\[source:[^\]]+\]\s*', ''),
]

def strip_metadata(text: str) -> str:
    """Remove OpenClaw metadata prefixes and code fences from text."""
    for pattern, replacement in STRIP_PATTERNS:
        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)
    return text.strip()

# ---------------------------------------------------------------------------
# 2. Levenshtein Deduplication
# ---------------------------------------------------------------------------

def levenshtein(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings."""
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def similarity(s1: str, s2: str) -> float:
    """Return similarity ratio 0.0-1.0."""
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    dist = levenshtein(s1, s2)
    return 1.0 - (dist / max_len)

def dedup_results(results: List[Dict], threshold: float = 0.85) -> List[Dict]:
    """Remove duplicate contents using Levenshtein similarity."""
    if not results:
        return []
    
    deduped = []
    for r in results:
        content = r.get('content', '')
        is_duplicate = False
        for existing in deduped:
            if similarity(content, existing.get('content', '')) > threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            deduped.append(r)
    return deduped

# ---------------------------------------------------------------------------
# 3. MMR Diversity Reranking
# ---------------------------------------------------------------------------

def mmr_rerank(
    results: List[Dict],
    query: str,
    lambda_param: float = 0.7,
    limit: int = 5
) -> List[Dict]:
    """
    Maximum Marginal Relevance reranking.
    
    Balances relevance (score) with diversity (maximize dissimilarity to already selected).
    lambda=1.0 → pure relevance ranking
    lambda=0.0 → pure diversity ranking
    
    Args:
        results: list of dicts with 'content' and 'score' keys
        query: original query (used for relevance)
        lambda_param: weight for relevance vs diversity
        limit: number of results to return
    """
    if not results:
        return []
    if len(results) <= limit:
        return results
    
    selected = []
    remaining = list(results)
    
    # Normalize scores
    max_score = max(r.get('score', 0) for r in remaining)
    min_score = min(r.get('score', 0) for r in remaining)
    score_range = max_score - min_score if max_score != min_score else 1.0
    
    def norm_score(r):
        return (r.get('score', 0) - min_score) / score_range
    
    while len(selected) < limit and remaining:
        best_score = -float('inf')
        best_item = None
        best_idx = -1
        
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        for idx, item in enumerate(remaining):
            relevance = norm_score(item)
            
            # Diversity: max similarity to already selected items
            max_sim_to_selected = 0.0
            for sel in selected:
                sim = similarity(
                    item.get('content', '').lower(),
                    sel.get('content', '').lower()
                )
                max_sim_to_selected = max(max_sim_to_selected, sim)
            
            diversity = 1.0 - max_sim_to_selected
            
            # MMR score
            mmr_score = lambda_param * relevance + (1 - lambda_param) * diversity
            
            if mmr_score > best_score:
                best_score = mmr_score
                best_item = item
                best_idx = idx
        
        if best_item is not None:
            selected.append(best_item)
            remaining.pop(best_idx)
        else:
            break
    
    return selected

# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='MemPalace Enhancement Layer')
    subparsers = parser.add_subparsers(dest='cmd')
    
    p_dedup = subparsers.add_parser('dedup')
    p_dedup.add_argument('--input', required=True, help='JSON results to dedup')
    p_dedup.add_argument('--threshold', type=float, default=0.85)
    
    p_mmr = subparsers.add_parser('mmr')
    p_mmr.add_argument('--input', required=True, help='JSON results to rerank')
    p_mmr.add_argument('--query', required=True, help='Original query')
    p_mmr.add_argument('--lambda', type=float, dest='lambda_param', default=0.7)
    p_mmr.add_argument('--limit', type=int, default=5)
    
    p_strip = subparsers.add_parser('strip')
    p_strip.add_argument('--text', required=True, help='Text to strip metadata from')
    
    args = parser.parse_args()
    
    if args.cmd == 'dedup':
        data = json.loads(args.input)
        results = data if isinstance(data, list) else data.get('results', [])
        out = dedup_results(results, args.threshold)
        print(json.dumps({'status': 'ok', 'deduped': out}, ensure_ascii=False))
    
    elif args.cmd == 'mmr':
        data = json.loads(args.input)
        results = data if isinstance(data, list) else data.get('results', [])
        out = mmr_rerank(results, args.query, args.lambda_param, args.limit)
        print(json.dumps({'status': 'ok', 'reranked': out}, ensure_ascii=False))
    
    elif args.cmd == 'strip':
        out = strip_metadata(args.text)
        print(json.dumps({'status': 'ok', 'cleaned': out}, ensure_ascii=False))
    
    else:
        parser.print_help()
