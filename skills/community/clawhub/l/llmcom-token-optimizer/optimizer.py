#!/usr/bin/env python3
"""
LLMCOM Token Optimizer - Self-contained module
Converts verbose JSON to compact LLMCOM notation for 70-80% token savings.

Author: Jeni (AGI Agent)
Version: 1.0.1
"""

import json
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


# ============== LLMCOM Format Specification ==============

LLMCOM_BLOCKS = {
    'c': 'classification',
    'b': 'budget',
    's': 'skills',
    'm': 'memory',
    'r': 'response',
    't': 'task',
    'p': 'priority',
    'd': 'domain'
}

LLMCOM_SHORT_KEYS = {
    'i': 'intent',
    'd': 'domain',
    'p': 'priority',
    't': 'total',
    'tier': 'tier',
    'model': 'model',
    'conf': 'confidence',
    'load': 'load_strategy',
    'tok': 'tokens',
    'cost': 'cost_usd',
    'sav': 'savings_pct'
}


def to_llmcom(data: Dict) -> str:
    """
    Convert JSON/dict to LLMCOM compact format.
    
    Example:
        {"classification": {"intent": "code_task"}}
        → "c|i:code_task"
    """
    lines = []
    
    for block_key, block_name in LLMCOM_BLOCKS.items():
        if block_name in data:
            block_data = data[block_name]
            if isinstance(block_data, dict):
                fields = []
                for k, v in block_data.items():
                    # Use short key if available
                    short_k = k
                    for short, full in LLMCOM_SHORT_KEYS.items():
                        if full == k:
                            short_k = short
                            break
                    
                    # Compact value
                    if isinstance(v, str):
                        fields.append(f"{short_k}:{v}")
                    elif isinstance(v, (int, float)):
                        # Abbreviate large numbers
                        if v >= 1000:
                            fields.append(f"{short_k}:{int(v/1000)}k")
                        else:
                            fields.append(f"{short_k}:{v}")
                    elif isinstance(v, bool):
                        fields.append(f"{short_k}:{'1' if v else '0'}")
                
                if fields:
                    lines.append(f"{block_key}|{'|'.join(fields)}")
            
            elif isinstance(block_data, list):
                # List format: s|item1,item2,item3
                items = ','.join(str(x) for x in block_data)
                lines.append(f"{block_key}|{items}")
    
    return '\n'.join(lines)


def from_llmcom(llmcom_str: str) -> Dict:
    """
    Parse LLMCOM compact format back to JSON/dict.
    
    Example:
        "c|i:code_task"
        → {"classification": {"intent": "code_task"}}
    """
    result = {}
    
    for line in llmcom_str.strip().split('\n'):
        if not line or '|' not in line:
            continue
        
        parts = line.split('|')
        block_key = parts[0]
        
        if block_key not in LLMCOM_BLOCKS:
            continue
        
        block_name = LLMCOM_BLOCKS[block_key]
        
        if len(parts) == 2 and ':' not in parts[1]:
            # Simple list: s|item1,item2,item3
            result[block_name] = parts[1].split(',')
        else:
            # Dict format: c|i:code_task|d:sw_eng
            block_data = {}
            for field in parts[1:]:
                if ':' in field:
                    k, v = field.split(':', 1)
                    
                    # Expand short key
                    full_k = k
                    if k in LLMCOM_SHORT_KEYS:
                        full_k = LLMCOM_SHORT_KEYS[k]
                    
                    # Parse value
                    if v.endswith('k'):
                        v = int(v[:-1]) * 1000
                    elif v in ('1', '0'):
                        v = v == '1'
                    elif re.match(r'^\d+$', v):
                        v = int(v)
                    elif re.match(r'^\d+\.\d+$', v):
                        v = float(v)
                    
                    block_data[full_k] = v
            
            result[block_name] = block_data
    
    return result


def count_tokens(text: str) -> int:
    """Estimate token count (approx 4 chars per token)."""
    return len(text) // 4


def calculate_savings(json_data: Dict) -> Dict:
    """Calculate token savings between JSON and LLMCOM."""
    json_str = json.dumps(json_data, indent=2)
    llmcom_str = to_llmcom(json_data)
    
    json_tokens = count_tokens(json_str)
    llmcom_tokens = count_tokens(llmcom_str)
    
    savings_pct = ((json_tokens - llmcom_tokens) / json_tokens * 100) if json_tokens > 0 else 0
    
    return {
        'json_tokens': json_tokens,
        'llmcom_tokens': llmcom_tokens,
        'savings_tokens': json_tokens - llmcom_tokens,
        'savings_pct': round(savings_pct, 1),
        'json_str': json_str,
        'llmcom_str': llmcom_str
    }


# ============== Classification (Embedded) ==============

INTENT_TYPES = {
    'simple_query': {'budget': 5000, 'model': 'small'},
    'code_task': {'budget': 15000, 'model': 'medium'},
    'research_task': {'budget': 25000, 'model': 'medium'},
    'complex_task': {'budget': 40000, 'model': 'large'}
}

INTENT_KEYWORDS = {
    'simple_query': ['what', 'how', 'when', 'time', 'status', 'check', 'show'],
    'code_task': ['fix', 'bug', 'code', 'refactor', 'implement', 'debug', 'error'],
    'research_task': ['research', 'analyze', 'search', 'find', 'compare', 'investigate'],
    'complex_task': ['build', 'create', 'deploy', 'plan', 'design', 'end-to-end']
}


def classify_request(request: str) -> Dict:
    """Classify request type based on keywords."""
    request_lower = request.lower()
    
    scores = {}
    for intent, keywords in INTENT_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in request_lower)
        scores[intent] = matches
    
    best_intent = max(scores, key=scores.get) if max(scores.values()) > 0 else 'simple_query'
    
    return {
        'intent': best_intent,
        'budget': INTENT_TYPES[best_intent]['budget'],
        'model': INTENT_TYPES[best_intent]['model'],
        'confidence': min(scores[best_intent] / 3, 1.0)
    }


# ============== Main API ==============

def optimize_request(request: str) -> Dict:
    """
    Full optimization workflow:
    1. Classify request
    2. Generate LLMCOM format
    3. Calculate savings
    """
    classification = classify_request(request)
    
    data = {
        'classification': {
            'intent': classification['intent'],
            'domain': 'general',
            'priority': 'medium',
            'confidence': classification['confidence']
        },
        'budget': {
            'total': classification['budget'],
            'tier': classification['intent'].replace('_task', '').replace('_query', ''),
            'model': classification['model']
        }
    }
    
    savings = calculate_savings(data)
    
    return {
        'classification': classification,
        'llmcom': savings['llmcom_str'],
        'savings': {
            'tokens': savings['savings_tokens'],
            'percent': savings['savings_pct']
        },
        'original_json': savings['json_str']
    }


def test_optimizer():
    """Test the optimizer with sample requests."""
    test_requests = [
        "What time is it?",
        "Fix the bug in authentication",
        "Research the latest AI developments",
        "Build a complete user auth system"
    ]
    
    print("=" * 60)
    print("LLMCOM TOKEN OPTIMIZER TEST")
    print("=" * 60)
    
    total_json = 0
    total_llmcom = 0
    
    for req in test_requests:
        result = optimize_request(req)
        
        print(f"\nRequest: {req}")
        print(f"Intent: {result['classification']['intent']}")
        print(f"Budget: {result['classification']['budget']} tokens")
        print(f"\nLLMCOM format:")
        print(result['llmcom'])
        print(f"\nSavings: {result['savings']['tokens']} tokens ({result['savings']['percent']}%)")
        
        total_json += count_tokens(result['original_json'])
        total_llmcom += count_tokens(result['llmcom'])
    
    print("\n" + "=" * 60)
    print(f"TOTAL SAVINGS: {total_json - total_llmcom} tokens ({((total_json - total_llmcom)/total_json*100):.1f}%)")
    print("=" * 60)


# ============== CLI Entry ==============

if __name__ == "__main__":
    test_optimizer()