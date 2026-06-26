#!/usr/bin/env python3
"""
Plagiarism Checker & AI Detector
Detects copied content and AI-generated text.
"""

import sys
import argparse
import re
from collections import Counter
import math
from pathlib import Path

# ── AI Detection heuristics ──────────────────────────────────────────────────

def compute_burstiness(text: str) -> float:
    """Sentence length variance — high variance = human-like."""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    if len(sentences) < 2:
        return 0.0
    lengths = [len(s.split()) for s in sentences]
    mean = sum(lengths) / len(lengths)
    variance = sum((l - mean) ** 2 for l in lengths) / len(lengths)
    return math.sqrt(variance) / max(mean, 1)


def compute_lexical_diversity(text: str) -> float:
    """Type-token ratio — human text tends to be more varied."""
    words = re.findall(r'\b\w+\b', text.lower())
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def compute_avg_word_length(text: str) -> float:
    """Average word length — AI often uses slightly longer words."""
    words = re.findall(r'\b\w+\b', text)
    if not words:
        return 0.0
    return sum(len(w) for w in words) / len(words)


def ai_probability(text: str) -> float:
    """
    Estimate AI-generation probability using heuristics.
    Returns a float 0.0–1.0.
    """
    if len(text) < 50:
        return 0.5  # Too short to judge

    burst = compute_burstiness(text)
    ldiv  = compute_lexical_diversity(text)
    awl   = compute_avg_word_length(text)

    # Heuristic scoring
    score = 0.0

    # Low burstiness → higher AI probability
    if burst < 4:
        score += 0.3
    elif burst < 8:
        score += 0.15

    # Low lexical diversity → higher AI probability
    if ldiv < 0.45:
        score += 0.3
    elif ldiv < 0.55:
        score += 0.15

    # Unusually uniform sentence lengths
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    if len(sentences) >= 3:
        word_counts = [len(s.split()) for s in sentences]
        if max(word_counts) - min(word_counts) < 4:
            score += 0.2

    # Repeated common AI phrases
    ai_phrases = [
        "it's important to note", "in conclusion", "additionally",
        "furthermore", "moreover", "in summary", "in today's world",
        "as mentioned earlier", "on the other hand", "in other words",
        "as a result", "due to the fact", "it is worth noting",
        "in this regard", "ultimately"
    ]
    phrase_count = sum(1 for phrase in ai_phrases if phrase.lower() in text.lower())
    score += min(phrase_count * 0.05, 0.2)

    return min(score, 1.0)


# ── Plagiarism / similarity detection ───────────────────────────────────────

def ngrams(text: str, n: int = 3):
    words = re.findall(r'\b\w+\b', text.lower())
    return [' '.join(words[i:i+n]) for i in range(len(words) - n + 1)]


def similarity(text1: str, text2: str) -> float:
    """Jaccard similarity between two texts based on trigrams."""
    ng1 = set(ngrams(text1))
    ng2 = set(ngrams(text2))
    if not ng1 or not ng2:
        return 0.0
    inter = len(ng1 & ng2)
    union = len(ng1 | ng2)
    return inter / union if union > 0 else 0.0


def originality_score(text: str, database: list[str] | None = None) -> float:
    """
    Compute originality score.
    Without an external DB, this uses internal heuristics.
    Returns 0.0–1.0 (higher = more original).
    """
    if not database:
        # Self-similarity check: split into halves and compare
        words = re.findall(r'\b\w+\b', text.lower())
        mid = len(words) // 2
        if mid < 10:
            return 0.8  # Too short to measure
        first_half = ' '.join(words[:mid])
        second_half = ' '.join(words[mid:])
        internal_sim = similarity(first_half, second_half)
        return max(0.0, 1.0 - internal_sim * 1.5)
    else:
        max_sim = max(similarity(text, ref) for ref in database)
        return max(0.0, 1.0 - max_sim)


# ── Paragraph analysis ───────────────────────────────────────────────────────

def analyze_paragraphs(text: str, database: list[str] | None = None):
    """Break text into paragraphs and score each."""
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]
    results = []
    for i, para in enumerate(paragraphs, 1):
        orig = originality_score(para, database)
        ai   = ai_probability(para)
        if orig >= 0.85 and ai <= 0.20:
            flag = "PASS"
        elif orig >= 0.60 or ai <= 0.50:
            flag = "WARN"
        else:
            flag = "FAIL"
        results.append({
            "index": i,
            "preview": para[:60] + ("..." if len(para) > 60 else ""),
            "originality": orig,
            "ai_prob": ai,
            "flag": flag,
        })
    return results


# ── Report ────────────────────────────────────────────────────────────────────

def print_report(text: str, database: list[str] | None = None):
    ai   = ai_probability(text)
    orig = originality_score(text, database)
    paras = analyze_paragraphs(text, database)

    word_count = len(re.findall(r'\b\w+\b', text))
    char_count = len(text)

    # Risk level
    if orig >= 0.85 and ai <= 0.20:
        risk, emoji = "Low Risk", "🟢"
    elif orig >= 0.60 or ai <= 0.50:
        risk, emoji = "Medium Risk", "🟡"
    elif orig >= 0.30 or ai <= 0.75:
        risk, emoji = "High Risk", "🟠"
    else:
        risk, emoji = "Critical", "🔴"

    print()
    print("═" * 60)
    print("             Content Originality & AI Detection Report")
    print("═" * 60)
    print(f"📝 Text Overview")
    print(f"   Word Count:   {word_count}")
    print(f"   Character Count: {char_count}")
    print(f"   Paragraph Count: {len(paras)}")
    print()
    print(f"📊 Comprehensive Score")
    print(f"   Originality:              {orig*100:.0f}%")
    print(f"   AI Generation Probability: {ai*100:.0f}%")
    print(f"   Risk Level:               {emoji} {risk}")
    print()
    print("─" * 60)
    print("Paragraph Analysis")
    print("─" * 60)

    for p in paras:
        flag_icon = {"PASS": "✅", "WARN": "⚠️", "FAIL": "❌"}[p["flag"]]
        print(f"  {flag_icon} Paragraph {p['index']}: Originality {p['originality']*100:.0f}% | AI {p['ai_prob']*100:.0f}%")
        print(f"     → {p['preview']}")

    print()
    print("─" * 60)
    print("Recommendations")
    print("─" * 60)

    fail_paras = [p for p in paras if p["flag"] in ("WARN", "FAIL")]
    if not fail_paras:
        print("  ✅ No issues found. Content is ready for use.")
    else:
        for p in fail_paras:
            if p["ai_prob"] > 0.50:
                print(f"  Paragraph {p['index']}: AI generation probability is high. Recommend enriching sentence variety and adding specific examples or data.")
            if p["originality"] < 0.60:
                print(f"  Paragraph {p['index']}: Similarity is high. Recommend adding original analysis and unique perspective.")

    print()
    print("═" * 60)
    print("⚠️  Note: This tool is based on statistical heuristics. Results are for")
    print("   reference only and should not be used as the basis for any")
    print("   academic or legal decisions.")
    print("═" * 60)
    print()


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Plagiarism Checker & AI Detector")
    parser.add_argument("--text", type=str, help="Text to check")
    parser.add_argument("--file", type=str, help="File path to read (.txt, .md)")
    parser.add_argument("--db", type=str, help="Reference text file (one URL/per line)")
    args = parser.parse_args()

    if not args.text and not args.file:
        parser.print_help()
        sys.exit(1)

    if args.file:
        path = Path(args.file)
        if not path.exists():
            print(f"Error: File does not exist → {path}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding="utf-8")
    else:
        text = args.text

    if not text.strip():
        print("Error: Text is empty", file=sys.stderr)
        sys.exit(1)

    if len(text) < 30:
        print("Error: Text too short (at least 30 characters)", file=sys.stderr)
        sys.exit(1)

    database = None
    if args.db:
        db_path = Path(args.db)
        if db_path.exists():
            database = [line.strip() for line in db_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    print_report(text, database)


if __name__ == "__main__":
    main()