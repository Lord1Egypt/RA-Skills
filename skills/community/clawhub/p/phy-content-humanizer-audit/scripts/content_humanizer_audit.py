#!/usr/bin/env python3
"""
phy-content-humanizer-audit — AI Content Signature Detector

Measures 8 linguistic dimensions that platforms (especially LinkedIn's 360Brew)
use to detect AI-generated content. Not a humanizer — an auditor that tells you
exactly which signals are triggering detection so you fix only what's wrong.

Research basis:
- DivEye (arXiv:2509.18880): lexical diversity + surprisal variance
- LinkedIn 360Brew: LLM-based feed ranking (2026)
- Stylometric detection: TTR, sentence length variance, burstiness

Zero external dependencies — pure Python 3.7+ stdlib.
"""

from __future__ import annotations

import json
import math
import re
import sys
import textwrap
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional


# ─── Constants ───────────────────────────────────────────────────────

# AI-typical transition words (overused by LLMs)
TRANSITION_WORDS: set[str] = {
    "furthermore", "moreover", "additionally", "consequently", "nevertheless",
    "nonetheless", "subsequently", "accordingly", "henceforth", "thus",
    "hence", "therefore", "in conclusion", "to summarize", "in summary",
    "notably", "significantly", "importantly", "crucially", "essentially",
    "fundamentally", "ultimately", "specifically", "particularly",
    "in particular", "as a result", "on the other hand", "in contrast",
    "conversely", "meanwhile", "similarly", "likewise",
}

# Hedging language (AI uses more than humans)
HEDGE_WORDS: set[str] = {
    "arguably", "potentially", "seemingly", "perhaps", "possibly",
    "it seems", "it appears", "it is worth noting", "it should be noted",
    "one might argue", "it could be argued", "generally speaking",
    "in many cases", "to some extent", "relatively", "somewhat",
    "fairly", "rather", "quite", "tend to", "tends to",
}

# AI-banned words (high-signal LinkedIn/social detectors)
AI_BANNED_WORDS: set[str] = {
    "leverage", "robust", "crucial", "delve", "tapestry", "holistic",
    "synergy", "paradigm", "ecosystem", "landscape", "streamline",
    "cutting-edge", "game-changer", "innovative", "revolutionary",
    "transformative", "comprehensive", "meticulous", "nuanced",
    "multifaceted", "pivotal", "seamless", "foster", "utilize",
    "facilitate", "endeavor", "underscore", "realm", "navigate",
    "embark", "spearhead", "harness", "unveil", "bolster",
    "cornerstone", "unparalleled", "groundbreaking",
}

# Common contractions (human signal)
CONTRACTIONS: set[str] = {
    "i'm", "i've", "i'd", "i'll", "you're", "you've", "you'd", "you'll",
    "we're", "we've", "we'd", "we'll", "they're", "they've", "they'd",
    "he's", "she's", "it's", "that's", "there's", "here's", "what's",
    "who's", "how's", "where's", "when's", "can't", "won't", "don't",
    "doesn't", "didn't", "isn't", "aren't", "wasn't", "weren't",
    "hasn't", "haven't", "hadn't", "couldn't", "wouldn't", "shouldn't",
    "ain't", "let's", "gonna", "wanna", "gotta", "tbh", "imo", "imho",
    "fwiw", "ngl", "iirc",
}

# Personal pronouns (human signal — first person)
PERSONAL_PRONOUNS: set[str] = {
    "i", "me", "my", "mine", "myself", "we", "us", "our", "ours",
}

# Platform-specific thresholds (lower = stricter)
PLATFORM_THRESHOLDS: dict[str, dict[str, float]] = {
    "linkedin": {
        "ai_signature_warning": 45,   # above this = WARN
        "ai_signature_fail": 65,      # above this = FAIL
        "description": "LinkedIn 360Brew actively detects AI via LLM. Strictest.",
    },
    "reddit": {
        "ai_signature_warning": 55,
        "ai_signature_fail": 75,
        "description": "Reddit community detects AI + mod tools. Moderate.",
    },
    "twitter": {
        "ai_signature_warning": 60,
        "ai_signature_fail": 80,
        "description": "Short-form = less detectable. Lenient.",
    },
    "hackernews": {
        "ai_signature_warning": 50,
        "ai_signature_fail": 70,
        "description": "Technical audience spots AI easily. Moderate-strict.",
    },
    "default": {
        "ai_signature_warning": 55,
        "ai_signature_fail": 75,
        "description": "Generic platform threshold.",
    },
}


# ─── Data structures ─────────────────────────────────────────────────

@dataclass
class DimensionScore:
    """Score for a single linguistic dimension."""
    name: str
    score: float           # 0-10, where 10 = very human
    max_score: float = 10.0
    detail: str = ""
    raw_value: float = 0.0


@dataclass
class SentenceFlag:
    """A flagged sentence with fix suggestion."""
    sentence: str
    issue: str
    severity: str          # HIGH / MEDIUM / LOW
    fix_suggestion: str
    ai_signal_score: float  # 0-1, how AI-like this sentence is


@dataclass
class AuditResult:
    """Complete audit result."""
    text: str
    platform: str
    dimensions: list[DimensionScore] = field(default_factory=list)
    flagged_sentences: list[SentenceFlag] = field(default_factory=list)
    banned_words_found: list[str] = field(default_factory=list)
    total_score: float = 0.0
    max_score: float = 80.0
    ai_signature_pct: float = 0.0
    verdict: str = ""


# ─── Tokenization helpers ────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    """Simple word tokenizer. Returns lowercase tokens."""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def _sentences(text: str) -> list[str]:
    """Split text into sentences."""
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in raw if len(s.strip()) > 5]


def _word_count(text: str) -> int:
    return len(_tokenize(text))


# ─── Dimension scorers ───────────────────────────────────────────────

def score_lexical_diversity(tokens: list[str]) -> DimensionScore:
    """
    Type-Token Ratio (TTR).
    Human writing: 0.55-0.80 TTR. AI writing: 0.35-0.55 TTR.
    Higher TTR = more diverse vocabulary = more human.
    """
    if len(tokens) < 10:
        return DimensionScore("Lexical Diversity (TTR)", 5.0, detail="Too short to measure", raw_value=0.0)

    # Use a sliding window to normalize for text length
    window = min(100, len(tokens))
    ttrs = []
    for i in range(0, len(tokens) - window + 1, max(1, window // 2)):
        chunk = tokens[i:i + window]
        ttrs.append(len(set(chunk)) / len(chunk))

    avg_ttr = sum(ttrs) / len(ttrs)

    # Map TTR to score: 0.35 → 0, 0.50 → 5, 0.70+ → 10
    if avg_ttr >= 0.70:
        score = 10.0
    elif avg_ttr >= 0.50:
        score = 5.0 + (avg_ttr - 0.50) * 25.0  # 0.50→5, 0.70→10
    else:
        score = max(0, avg_ttr / 0.50 * 5.0)  # 0→0, 0.50→5

    return DimensionScore(
        "Lexical Diversity (TTR)",
        round(min(10, score), 1),
        detail=f"TTR={avg_ttr:.3f} (human: 0.55-0.80, AI: 0.35-0.55)",
        raw_value=round(avg_ttr, 3),
    )


def score_sentence_variance(sentences: list[str]) -> DimensionScore:
    """
    Sentence length variance (std dev of word counts).
    Humans mix short punchy sentences with long complex ones → high variance.
    AI maintains unnaturally consistent sentence lengths → low variance.
    """
    if len(sentences) < 3:
        return DimensionScore("Sentence Length Variance", 5.0, detail="Too few sentences", raw_value=0.0)

    lengths = [_word_count(s) for s in sentences]
    mean_len = sum(lengths) / len(lengths)
    variance = sum((l - mean_len) ** 2 for l in lengths) / len(lengths)
    std_dev = math.sqrt(variance)

    # Coefficient of variation (normalized)
    cv = std_dev / mean_len if mean_len > 0 else 0

    # Map CV to score: <0.2 → AI-like (low score), 0.4-0.7 → human (high score)
    if cv >= 0.60:
        score = 10.0
    elif cv >= 0.35:
        score = 5.0 + (cv - 0.35) * 20.0  # 0.35→5, 0.60→10
    else:
        score = max(0, cv / 0.35 * 5.0)

    return DimensionScore(
        "Sentence Length Variance",
        round(min(10, score), 1),
        detail=f"CV={cv:.2f}, StdDev={std_dev:.1f} words (human: CV>0.4, AI: CV<0.3)",
        raw_value=round(cv, 3),
    )


def score_transition_density(tokens: list[str], text_lower: str) -> DimensionScore:
    """
    Transition word density. AI overuses formal transitions.
    Lower density = more human for social media.
    """
    if len(tokens) < 20:
        return DimensionScore("Transition Word Density", 5.0, detail="Too short", raw_value=0.0)

    count = 0
    for tw in TRANSITION_WORDS:
        count += text_lower.count(tw)

    density = count / (len(tokens) / 100)  # per 100 words

    # Map: >3 per 100 words → very AI, <1 → very human
    if density <= 0.5:
        score = 10.0
    elif density <= 1.5:
        score = 7.0 + (1.5 - density) * 3.0
    elif density <= 3.0:
        score = 3.0 + (3.0 - density) / 1.5 * 4.0
    else:
        score = max(0, 3.0 - (density - 3.0))

    return DimensionScore(
        "Transition Word Density",
        round(min(10, max(0, score)), 1),
        detail=f"{count} transitions in {len(tokens)} words ({density:.1f}/100w). Human: <1.5, AI: >3.0",
        raw_value=round(density, 2),
    )


def score_hedging_ratio(text_lower: str, token_count: int) -> DimensionScore:
    """
    Hedging language ratio. AI hedges more than humans in social posts.
    Humans on social media are more direct and opinionated.
    """
    if token_count < 20:
        return DimensionScore("Hedging Ratio", 5.0, detail="Too short", raw_value=0.0)

    count = 0
    for hw in HEDGE_WORDS:
        count += text_lower.count(hw)

    density = count / (token_count / 100)

    # Map: >2 per 100 words → very AI, <0.5 → assertive/human
    if density <= 0.3:
        score = 10.0
    elif density <= 1.0:
        score = 6.0 + (1.0 - density) / 0.7 * 4.0
    elif density <= 2.5:
        score = 2.0 + (2.5 - density) / 1.5 * 4.0
    else:
        score = max(0, 2.0 - (density - 2.5))

    return DimensionScore(
        "Hedging Ratio",
        round(min(10, max(0, score)), 1),
        detail=f"{count} hedges in {token_count} words ({density:.1f}/100w). Human: <1.0, AI: >2.0",
        raw_value=round(density, 2),
    )


def score_contraction_usage(tokens: list[str]) -> DimensionScore:
    """
    Contraction frequency. Humans use contractions naturally.
    AI tends to use formal expanded forms (do not, I have, etc.)
    """
    if len(tokens) < 20:
        return DimensionScore("Contraction Usage", 5.0, detail="Too short", raw_value=0.0)

    count = sum(1 for t in tokens if t in CONTRACTIONS)
    density = count / (len(tokens) / 100)

    # Map: 0 contractions → very AI, 2+ per 100 words → human
    if density >= 3.0:
        score = 10.0
    elif density >= 1.5:
        score = 6.0 + (density - 1.5) / 1.5 * 4.0
    elif density >= 0.5:
        score = 2.0 + (density - 0.5) / 1.0 * 4.0
    else:
        score = max(0, density / 0.5 * 2.0)

    return DimensionScore(
        "Contraction Usage",
        round(min(10, max(0, score)), 1),
        detail=f"{count} contractions ({density:.1f}/100w). Human: >1.5, AI: <0.5",
        raw_value=round(density, 2),
    )


def score_personal_pronoun_density(tokens: list[str]) -> DimensionScore:
    """
    First-person pronoun density.
    Social media = personal. Humans use I/my/we much more than AI.
    """
    if len(tokens) < 20:
        return DimensionScore("Personal Pronoun Density", 5.0, detail="Too short", raw_value=0.0)

    count = sum(1 for t in tokens if t in PERSONAL_PRONOUNS)
    density = count / (len(tokens) / 100)

    # Map: <1 per 100 words → impersonal/AI, >4 → very personal/human
    if density >= 5.0:
        score = 10.0
    elif density >= 2.5:
        score = 5.0 + (density - 2.5) / 2.5 * 5.0
    elif density >= 1.0:
        score = 2.0 + (density - 1.0) / 1.5 * 3.0
    else:
        score = max(0, density / 1.0 * 2.0)

    return DimensionScore(
        "Personal Pronoun Density",
        round(min(10, max(0, score)), 1),
        detail=f"{count} first-person pronouns ({density:.1f}/100w). Human social: >3.0, AI: <1.5",
        raw_value=round(density, 2),
    )


def score_question_frequency(sentences: list[str]) -> DimensionScore:
    """
    Question frequency. Humans ask more questions in social posts.
    AI tends to make statements, not ask questions.
    """
    if len(sentences) < 2:
        return DimensionScore("Question Frequency", 5.0, detail="Too short", raw_value=0.0)

    questions = sum(1 for s in sentences if s.rstrip().endswith("?"))
    ratio = questions / len(sentences)

    # Map: 0 questions → AI, 10-25% → ideal human, >30% → too many
    if 0.08 <= ratio <= 0.30:
        score = 8.0 + min(2.0, (ratio - 0.08) * 10)
    elif ratio > 0.30:
        score = 7.0  # still human, just question-heavy
    elif ratio > 0:
        score = 4.0 + ratio / 0.08 * 4.0
    else:
        score = 1.0  # zero questions = strong AI signal

    return DimensionScore(
        "Question Frequency",
        round(min(10, max(0, score)), 1),
        detail=f"{questions}/{len(sentences)} sentences are questions ({ratio:.0%}). Human: 10-25%, AI: 0-5%",
        raw_value=round(ratio, 3),
    )


def score_specific_data_density(text: str, token_count: int) -> DimensionScore:
    """
    Specific numbers, dates, names, data points.
    Humans include specific evidence. AI stays vague and generic.
    """
    if token_count < 20:
        return DimensionScore("Specific Data Density", 5.0, detail="Too short", raw_value=0.0)

    # Count specific data points
    numbers = len(re.findall(r'\b\d+[%$€£¥KkMmBb]?\b', text))  # 30%, $5M, 100K
    years = len(re.findall(r'\b20[12]\d\b', text))                # 2024, 2025, 2026
    metrics = len(re.findall(r'\b\d+(?:\.\d+)?x\b', text))        # 2.5x, 10x
    proper_nouns = len(re.findall(r'(?<!\. )\b[A-Z][a-z]{2,}\b', text))  # Names, products

    total = numbers + years + metrics + (proper_nouns // 3)  # weight names less
    density = total / (token_count / 100)

    # Map: 0 data points → generic/AI, >3 per 100 words → specific/human
    if density >= 4.0:
        score = 10.0
    elif density >= 2.0:
        score = 5.0 + (density - 2.0) / 2.0 * 5.0
    elif density >= 0.5:
        score = 1.0 + (density - 0.5) / 1.5 * 4.0
    else:
        score = max(0, density / 0.5 * 1.0)

    return DimensionScore(
        "Specific Data Density",
        round(min(10, max(0, score)), 1),
        detail=f"{total} data points ({density:.1f}/100w): {numbers} numbers, {years} years, {metrics} metrics. Human: >2.0, AI: <1.0",
        raw_value=round(density, 2),
    )


# ─── Sentence-level flagging ─────────────────────────────────────────

def flag_sentences(sentences: list[str]) -> list[SentenceFlag]:
    """Flag individual sentences that carry strong AI signals."""
    flags: list[SentenceFlag] = []

    for sent in sentences:
        sent_lower = sent.lower()
        sent_tokens = _tokenize(sent_lower)
        issues: list[tuple[str, str, str]] = []  # (issue, severity, fix)

        # Check for banned AI words
        for bw in AI_BANNED_WORDS:
            if bw in sent_lower:
                issues.append((
                    f"AI-flagged word: '{bw}'",
                    "HIGH",
                    f"Replace '{bw}' with a specific, concrete term",
                ))

        # Check for transition word at sentence start
        for tw in TRANSITION_WORDS:
            if sent_lower.startswith(tw):
                issues.append((
                    f"AI-typical sentence opener: '{tw}'",
                    "MEDIUM",
                    "Remove the transition entirely or replace with a short bridge",
                ))

        # Check for hedging
        for hw in HEDGE_WORDS:
            if hw in sent_lower:
                issues.append((
                    f"Hedging language: '{hw}'",
                    "MEDIUM",
                    "State your point directly — be assertive on social media",
                ))

        # Check for no contractions in long sentences (AI signal)
        if len(sent_tokens) > 15:
            has_contraction = any(t in CONTRACTIONS for t in sent_tokens)
            expandable = any(p in sent_lower for p in [
                "do not", "does not", "did not", "is not", "are not",
                "was not", "were not", "have not", "has not", "had not",
                "will not", "would not", "could not", "should not",
                "i am", "i have", "i would", "i will", "it is", "that is",
            ])
            if not has_contraction and expandable:
                issues.append((
                    "Formal expanded form (no contractions)",
                    "LOW",
                    "Use contractions: 'don't' not 'do not', 'I've' not 'I have'",
                ))

        # Check for generic filler (AI loves these)
        filler_patterns = [
            r"in today's .+ landscape",
            r"in the (ever[- ])?evolving .+ (world|landscape|ecosystem)",
            r"it's (no secret|worth noting|important to note)",
            r"let's (dive|delve) (in|into|deeper)",
            r"at the end of the day",
            r"the bottom line is",
        ]
        for fp in filler_patterns:
            if re.search(fp, sent_lower):
                issues.append((
                    "Generic AI filler phrase detected",
                    "HIGH",
                    "Replace with a specific personal observation or data point",
                ))

        if issues:
            # Take the highest severity issue
            severity_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
            issues.sort(key=lambda x: severity_order.get(x[1], 0), reverse=True)
            ai_score = min(1.0, len(issues) * 0.3)

            flags.append(SentenceFlag(
                sentence=sent[:120] + ("..." if len(sent) > 120 else ""),
                issue=issues[0][0],
                severity=issues[0][1],
                fix_suggestion=issues[0][2],
                ai_signal_score=round(ai_score, 2),
            ))

    # Sort by AI signal score descending
    flags.sort(key=lambda f: f.ai_signal_score, reverse=True)
    return flags


# ─── Main audit function ─────────────────────────────────────────────

def audit_content(text: str, platform: str = "linkedin") -> AuditResult:
    """
    Run the full 8-dimension humanizer audit on a text.

    Args:
        text: The social media post draft to audit
        platform: Target platform (linkedin, reddit, twitter, hackernews)

    Returns:
        AuditResult with scores, flags, and verdict
    """
    platform = platform.lower().strip()
    if platform not in PLATFORM_THRESHOLDS:
        platform = "default"

    tokens = _tokenize(text)
    sentences = _sentences(text)
    text_lower = text.lower()
    token_count = len(tokens)

    # Score all 8 dimensions
    dimensions = [
        score_lexical_diversity(tokens),
        score_sentence_variance(sentences),
        score_transition_density(tokens, text_lower),
        score_hedging_ratio(text_lower, token_count),
        score_contraction_usage(tokens),
        score_personal_pronoun_density(tokens),
        score_question_frequency(sentences),
        score_specific_data_density(text, token_count),
    ]

    total = sum(d.score for d in dimensions)
    max_total = sum(d.max_score for d in dimensions)

    # AI signature = inverse of human score
    human_pct = (total / max_total) * 100 if max_total > 0 else 50
    ai_signature = 100 - human_pct

    # Find banned words
    banned_found = [w for w in AI_BANNED_WORDS if w in text_lower]

    # Adjust AI signature for banned words (each adds 3%)
    ai_signature = min(100, ai_signature + len(banned_found) * 3)

    # Flag sentences
    flagged = flag_sentences(sentences)

    # Determine verdict
    thresholds = PLATFORM_THRESHOLDS[platform]
    if ai_signature >= thresholds["ai_signature_fail"]:
        verdict = "FAIL"
    elif ai_signature >= thresholds["ai_signature_warning"]:
        verdict = "WARN"
    else:
        verdict = "PASS"

    return AuditResult(
        text=text,
        platform=platform,
        dimensions=dimensions,
        flagged_sentences=flagged,
        banned_words_found=sorted(banned_found),
        total_score=round(total, 1),
        max_score=max_total,
        ai_signature_pct=round(ai_signature, 1),
        verdict=verdict,
    )


# ─── Report formatter ────────────────────────────────────────────────

def format_report(result: AuditResult) -> str:
    """Format audit result as a human-readable report."""
    lines: list[str] = []
    w = lines.append

    # Verdict emoji
    v_emoji = {"PASS": "✅", "WARN": "🟡", "FAIL": "🔴"}.get(result.verdict, "❓")

    w("=" * 66)
    w("  phy-content-humanizer-audit — AI Signature Report")
    w("=" * 66)
    w(f"  Platform : {result.platform.title()}")
    w(f"  Words    : {_word_count(result.text)}")
    w(f"  AI Sig   : {result.ai_signature_pct}% {v_emoji} {result.verdict}")
    w(f"  Human    : {result.total_score}/{result.max_score}")
    threshold = PLATFORM_THRESHOLDS.get(result.platform, PLATFORM_THRESHOLDS["default"])
    w(f"  Threshold: WARN >{threshold['ai_signature_warning']}%, FAIL >{threshold['ai_signature_fail']}%")
    w("=" * 66)

    # Dimension breakdown
    w("\n📊  Dimension Scores (0-10, higher = more human)\n")
    for d in result.dimensions:
        bar_len = int(d.score)
        bar = "█" * bar_len + "░" * (10 - bar_len)
        label = f"  {d.name:<28}"
        w(f"{label} {bar} {d.score:4.1f}/10")
        w(f"  {'':28} {d.detail}")

    # Banned words
    if result.banned_words_found:
        w(f"\n🚫  AI-Flagged Words Found ({len(result.banned_words_found)}):\n")
        for bw in result.banned_words_found:
            w(f"  • \"{bw}\" — replace with a specific, concrete alternative")

    # Flagged sentences (top 5)
    if result.flagged_sentences:
        top_flags = result.flagged_sentences[:5]
        w(f"\n⚠️  Flagged Sentences (top {len(top_flags)}):\n")
        for i, f in enumerate(top_flags, 1):
            sev_icon = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}.get(f.severity, "⚪")
            w(f"  {i}. {sev_icon} [{f.severity}] {f.issue}")
            w(f"     \"{f.sentence}\"")
            w(f"     → Fix: {f.fix_suggestion}")
            w("")

    # Top 3 fixes
    w("💡  Top 3 Fixes to Lower AI Signature:\n")
    fixes = _generate_top_fixes(result)
    for i, fix in enumerate(fixes[:3], 1):
        w(f"  {i}. {fix}")

    w("")
    return "\n".join(lines)


def _generate_top_fixes(result: AuditResult) -> list[str]:
    """Generate the top 3 actionable fixes based on dimension scores."""
    fixes: list[tuple[float, str]] = []

    for d in result.dimensions:
        if d.name == "Contraction Usage" and d.score < 5:
            fixes.append((d.score, "Add contractions: change 'do not' → 'don't', 'I have' → 'I've', 'it is' → 'it's'"))
        elif d.name == "Personal Pronoun Density" and d.score < 5:
            fixes.append((d.score, "Add personal experience: start 2-3 sentences with 'I' or 'my' — share what YOU did/saw/learned"))
        elif d.name == "Question Frequency" and d.score < 5:
            fixes.append((d.score, "Add 1-2 genuine questions: 'Has anyone else seen this?' or 'What's your experience?'"))
        elif d.name == "Sentence Length Variance" and d.score < 5:
            fixes.append((d.score, "Mix sentence lengths: add one 3-5 word sentence ('Seriously.', 'It worked.', 'Here's why.') between longer ones"))
        elif d.name == "Transition Word Density" and d.score < 5:
            fixes.append((d.score, "Delete transition words: remove 'Furthermore', 'Moreover', 'Additionally' — just start the next point"))
        elif d.name == "Hedging Ratio" and d.score < 5:
            fixes.append((d.score, "Be more assertive: replace 'it seems' with 'I found', 'arguably' with your actual argument"))
        elif d.name == "Lexical Diversity (TTR)" and d.score < 5:
            fixes.append((d.score, "Vary your vocabulary: you're repeating the same words. Use synonyms or rephrase"))
        elif d.name == "Specific Data Density" and d.score < 5:
            fixes.append((d.score, "Add specific data: include a number, date, tool name, or project name instead of vague references"))

    if result.banned_words_found:
        fixes.append((0, f"Remove AI words: {', '.join(result.banned_words_found[:5])} — replace each with a plain, specific term"))

    fixes.sort(key=lambda x: x[0])
    return [f[1] for f in fixes]


def format_json(result: AuditResult) -> str:
    """Format audit result as JSON."""
    return json.dumps({
        "platform": result.platform,
        "word_count": _word_count(result.text),
        "ai_signature_pct": result.ai_signature_pct,
        "human_score": result.total_score,
        "max_score": result.max_score,
        "verdict": result.verdict,
        "dimensions": [
            {"name": d.name, "score": d.score, "detail": d.detail, "raw_value": d.raw_value}
            for d in result.dimensions
        ],
        "banned_words": result.banned_words_found,
        "flagged_sentences": [
            {"sentence": f.sentence, "issue": f.issue, "severity": f.severity,
             "fix": f.fix_suggestion, "ai_score": f.ai_signal_score}
            for f in result.flagged_sentences[:10]
        ],
    }, indent=2)


# ─── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-content-humanizer-audit: AI Content Signature Detector",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              echo "Your post text" | python3 content_humanizer_audit.py --platform linkedin
              python3 content_humanizer_audit.py --file draft.txt --platform reddit
              python3 content_humanizer_audit.py --text "My post..." --format json
        """),
    )
    parser.add_argument("--text", "-t", help="Text to audit (inline)")
    parser.add_argument("--file", "-f", help="Read text from file")
    parser.add_argument("--platform", "-p", default="linkedin",
                        choices=["linkedin", "reddit", "twitter", "hackernews"],
                        help="Target platform (default: linkedin)")
    parser.add_argument("--format", default="text", choices=["text", "json"],
                        help="Output format (default: text)")

    args = parser.parse_args()

    # Get text input
    if args.text:
        text = args.text
    elif args.file:
        with open(args.file, "r") as fh:
            text = fh.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.error("Provide text via --text, --file, or stdin pipe")

    if not text.strip():
        parser.error("Empty text provided")

    result = audit_content(text.strip(), args.platform)

    if args.format == "json":
        print(format_json(result))
    else:
        print(format_report(result))

    # Exit code: 0=PASS, 1=WARN, 2=FAIL
    exit_codes = {"PASS": 0, "WARN": 1, "FAIL": 2}
    sys.exit(exit_codes.get(result.verdict, 0))


if __name__ == "__main__":
    main()
