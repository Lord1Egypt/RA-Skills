#!/usr/bin/env python3
"""
score_ai_patterns.py — Lightweight AI-pattern detector
Flags common AI writing tells before running full de-ai-ify skill.

Usage:
    python3 score_ai_patterns.py <article_file>

Output:
    Score 0–10 (10 = fully human, 0 = very AI)
    List of flagged patterns with line numbers

Exit codes:
    0 = score >= 8 (pass — de-ai-ify skill likely not needed)
    1 = score < 8 (fail — run de-ai-ify skill)
"""

import sys
import re

AI_PATTERNS = [
    # Hedging / throat-clearing
    (r"\bit'?s important to (note|remember|understand)\b", "Throat-clearing hedge"),
    (r"\bin (today'?s|this) (landscape|world|environment|era)\b", "Generic era opener"),
    (r"\bwhen it comes to\b", "Filler phrase"),
    (r"\bit is worth (noting|mentioning)\b", "Unnecessary qualifier"),
    (r"\bone cannot (overstate|understate|deny)\b", "AI emphasis pattern"),
    (r"\bwithout (further ado|delay)\b", "Filler transition"),

    # Hollow enthusiasm
    (r"\bexciting (times|opportunities|developments)\b", "Hollow enthusiasm"),
    (r"\bgame.?changer\b", "Overused buzzword"),
    (r"\btransformative\b", "Buzzword"),
    (r"\bseamless(ly)?\b", "Buzzword"),
    (r"\bleverage\b", "Corporate buzzword"),
    (r"\bsynerg(y|ies|ize)\b", "Corporate buzzword"),
    (r"\bpivot\b", "Startup cliché"),
    (r"\brobust\b", "Overused adjective"),
    (r"\bcomprehensive\b", "Hollow adjective"),

    # AI structural tells
    (r"\bin (conclusion|summary|closing),?\b", "AI closing pattern"),
    (r"\bto summarize\b", "AI summary opener"),
    (r"\bfirst and foremost\b", "AI list opener"),
    (r"\blast but not least\b", "AI list closer"),
    (r"\bin (this|the following) (article|post|guide|piece)\b", "Self-referential opener"),
    (r"\bwe (will|are going to) (explore|discuss|cover|look at)\b", "Preview narration"),
    (r"\bby the end of this (article|post|guide)\b", "Preview narration"),

    # Passive voice tells
    (r"\bit (should|must|can) be (noted|said|mentioned)\b", "Passive hedge"),
    (r"\bit has been (shown|demonstrated|proven)\b", "Vague authority claim"),

    # Filler connectors
    (r"\bmoreover\b", "Overused connector"),
    (r"\bfurthermore\b", "Overused connector"),
    (r"\badditionally\b", "Overused connector"),
    (r"\bnevertheless\b", "Formal filler"),
    (r"\bnotwithstanding\b", "Formal filler"),
]

def score(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    content = ''.join(lines)
    word_count = len(content.split())

    hits = []
    for pattern, label in AI_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                hits.append((i, label, line.strip()[:80]))

    # Score: start at 10, deduct per unique pattern type hit
    unique_patterns_hit = len(set(label for _, label, _ in hits))
    raw_score = max(0, 10 - unique_patterns_hit)

    # Density penalty: if hits > 1% of word count, extra deduction
    density = len(hits) / max(word_count, 1)
    if density > 0.01:
        raw_score = max(0, raw_score - 1)

    print(f"\n=== AI Pattern Score: {raw_score}/10 ===")
    print(f"    ({len(hits)} pattern hits across {word_count} words)")

    if hits:
        print("\nFlagged patterns:")
        for lineno, label, snippet in hits[:20]:  # cap at 20 to avoid noise
            print(f"  Line {lineno:>4} [{label}]: {snippet}")
        if len(hits) > 20:
            print(f"  ... and {len(hits) - 20} more")

    if raw_score >= 8:
        print(f"\n✅ Score {raw_score}/10 — passes threshold. De-ai-ify skill likely not needed.")
    else:
        print(f"\n❌ Score {raw_score}/10 — below threshold. Run de-ai-ify skill before publishing.")

    print()
    return raw_score

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 score_ai_patterns.py <article_file>")
        sys.exit(1)
    result = score(sys.argv[1])
    sys.exit(0 if result >= 8 else 1)
