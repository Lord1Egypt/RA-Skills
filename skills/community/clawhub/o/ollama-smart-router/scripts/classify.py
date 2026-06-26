#!/usr/bin/env python3
"""
Classify task complexity (1-5) for smart routing.
1 = Simple factual answer
2 = Basic reasoning  
3 = Complex work
4 = Deep reasoning
5 = Expert level
"""

import re
import sys
import argparse

# Negative patterns - things that look complex but aren't
NEGATIVE_PATTERNS = [
    r'zip\s+code',           # "What is the zip code for..."
    r'area\s+code',          # "What is the area code..."
    r'dress\s+code',         # "What's the dress code..."
    r'morse\s+code',         # "What is morse code..."
    r'bar\s+code',           # "How do bar codes work..."
    r'source\s+code',         # "Where is the source code..."
    r'vs\s+code',            # "VS Code editor..."
    r'error\s+code',          # "What does error code 404 mean"
]

# Search patterns - indicate need for web search
SEARCH_PATTERNS = [
    r'\bsearch\s+(for|the)\b',
    r'\blook\s+up\b',
    r'\bfind\s+(information|news|data|latest)\s+(about|on)\b',
    r'\bcurrent\s+(events|news|prices|weather)\b',
    r'\bwhat\s+is\s+the\s+(latest|current|recent)\b',
    r'\bhow\s+much\s+is\b',  # Prices
    r'\bweather\s+in\b',
    r'\bwho\s+won\b',  # Sports/events
    r'\blatest\s+(news|update|version)\b',
]

# Classification rules (heuristic-based, no LLM call needed for speed)
# Ordered by complexity - higher scores checked last
COMPLEXITY_PATTERNS = {
    1: [  # Simple
        r'^(what|who|when|where|is|are|can|do|does)\s+\w+',  # Simple questions
        r'^define\b',
        r'^meaning\s+of\b',
        r'^explain\s+simply\b',
        r'^list\s+\d*',  # List requests
        r'^(yes|no)\s+or\s+(no|yes)',
    ],
    2: [  # Basic
        r'\bwrite\b.*\b(short|brief|simple)\b',
        r'\bsummarize\b',
        r'\btl;dr\b',
        r'\bexample\s+of\b',
        r'\bsample\s+code\b',
        r'\bconvert\b.*\bto\b',
        r'\btranslate\b',
        r'^how\s+to\s+\w+\s+in\s+\w+\s*$',  # Simple "how to X in Python"
    ],
    3: [  # Complex
        r'\bfix\b.*\berror\b',
        r'\bdebug\b',
        r'\bcompare\b.*\b(and|vs|with)\b',
        r'\banalyze\b',
        r'\bstep\s+by\s+step\b',
        r'\bimplement\b',
        r'\bcreate\b.*\bfunction\b',
        r'\brefactor\b',
    ],
    4: [  # Deep
        r'\bresearch\b',
        r'\bsynthesize\b',
        r'\bevaluate\b.*\boptions\b',
        r'\bdesign\b.*\bsystem\b',
        r'\barchitecture\b',
        r'\bcreative\s+writing\b',
        r'\bwrite\b.*\b(essay|article|blog)\b',
        r'\breview\b.*\b(code|document|plan)\b',
        r'\bcritique\b',
    ],
    5: [  # Expert
        r'\bbuild\b.*\bsystem\b.*\bfrom\s+scratch\b',
        r'\bcomplex\b.*\bproject\b',
        r'\bmulti[- ]?file\b',
        r'\bagentic\b',
        r'\bworkflow\b.*\bautomation\b',
        r'\bnovel\b.*\b(approach|solution)\b',
        r'\bintegrate\b.*\b(API|service|database)\b.*\bwith\b',
    ]
}

def contains_negative_pattern(task: str) -> bool:
    """Check if task contains a false-positive pattern."""
    task_lower = task.lower()
    for pattern in NEGATIVE_PATTERNS:
        if re.search(pattern, task_lower):
            return True
    return False

def classify_task(task: str, use_llm: bool = False) -> tuple[int, str, bool]:
    """
    Classify task complexity (1-5) and detect if web search needed.
    
    Returns: (score, reason, needs_search)
    """
    task_lower = task.lower()
    
    # Check if task needs web search
    needs_search = False
    for pattern in SEARCH_PATTERNS:
        if re.search(pattern, task_lower):
            needs_search = True
            break
    
    # Length heuristic (longer = more complex)
    word_count = len(task.split())
    if word_count > 100:
        return 5, "very-long-context"
    if word_count > 50:
        return 4, "long-context"
    
    # Check for false positives first
    is_false_positive = contains_negative_pattern(task)
    
    # Pattern matching - build up score progressively
    # Start with 1, only promote if we see stronger patterns
    current_score = 1
    reason = "default-simple"
    
    for score in sorted(COMPLEXITY_PATTERNS.keys()):
        for pattern in COMPLEXITY_PATTERNS[score]:
            if re.search(pattern, task_lower):
                # If this is a code-related pattern and we have a false positive, skip
                if is_false_positive and score >= 3:
                    continue
                current_score = max(current_score, score)
                break
    
    # Map to reason
    reasons = {
        1: "simple-qa",
        2: "basic-task", 
        3: "complex-work",
        4: "deep-reasoning",
        5: "expert-level"
    }
    reason = reasons[current_score]
    
    return current_score, reason, needs_search

def main():
    parser = argparse.ArgumentParser(description='Classify task complexity')
    parser.add_argument('task', help='The task to classify')
    parser.add_argument('--llm', action='store_true', help='Use LLM for classification')
    args = parser.parse_args()
    
    score, reason = classify_task(args.task, args.llm)
    print(f"{score}:{reason}")
    
    # Return exit code for shell scripting
    sys.exit(score)

if __name__ == '__main__':
    main()
