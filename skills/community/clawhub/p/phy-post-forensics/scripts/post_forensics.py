#!/usr/bin/env python3
"""
phy-post-forensics — "Why Did This Post Work?" Structural Analyzer

Takes a batch of your social media posts + their engagement data, extracts
12 structural features from each, groups by performance tier, and tells you
exactly which content patterns correlate with YOUR best/worst posts.

Not an analytics dashboard (lagging indicators). A forensic analyzer that
separates content quality from distribution luck.

Research basis:
- Buffer 52M+ posts study (2026): dwell time > likes, specificity = 3-4x reach
- LinkedIn 360Brew data: document posts 596% more engagement than text-only
- Reddit 1000-post study: timing = 730% difference, subreddit size = strongest predictor
- Stanford CS229: text features for engagement prediction

Zero external dependencies — pure Python 3.7+ stdlib.
"""

from __future__ import annotations

import json
import math
import re
import sys
import textwrap
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from pathlib import Path
from statistics import mean, median, stdev
from typing import Optional


# ─── Feature extraction ──────────────────────────────────────────────

HOOK_PATTERNS: dict[str, re.Pattern] = {
    "number_lead": re.compile(r"^[\s\"\']*\d"),
    "question": re.compile(r"^[^.!]{5,}\?"),
    "contrarian": re.compile(
        r"(?i)^.{0,20}(stop|don't|never|wrong|myth|actually|unpopular|hot take|"
        r"controversial|nobody|everyone is wrong|forget)"
    ),
    "story_open": re.compile(
        r"(?i)^.{0,10}(i |we |last |yesterday |in 20|when i|my |a few|"
        r"three years|two months|six months|one year)"
    ),
    "challenge": re.compile(
        r"(?i)^.{0,20}(here's|here are|try this|want to|ready to|"
        r"let me show|how to|how i|the secret|the trick)"
    ),
}

POSITIVE_WORDS: set[str] = {
    "love", "great", "amazing", "awesome", "excited", "happy", "best",
    "incredible", "beautiful", "excellent", "wonderful", "fantastic",
    "brilliant", "perfect", "grateful", "proud", "thrilled", "joy",
    "breakthrough", "won", "achieved", "success", "milestone",
}

NEGATIVE_WORDS: set[str] = {
    "hate", "terrible", "awful", "worst", "angry", "frustrated",
    "disappointed", "failed", "broken", "mistake", "struggle",
    "pain", "problem", "issue", "bug", "crash", "loss", "burned",
    "wasted", "regret", "embarrassing", "disaster",
}

CTA_PATTERNS: dict[str, re.Pattern] = {
    "question_cta": re.compile(r"(?i)(what do you|what's your|how do you|have you|anyone else|thoughts\?|agree\?)"),
    "action_cta": re.compile(r"(?i)(follow me|check (out|it)|subscribe|sign up|try it|get started|download|link in)"),
    "share_cta": re.compile(r"(?i)(share this|repost|spread the word|tell your|tag someone)"),
    "comment_cta": re.compile(r"(?i)(comment below|drop a|let me know|tell me|sound off)"),
}

PERSONAL_PRONOUNS: set[str] = {"i", "me", "my", "mine", "myself", "we", "us", "our", "ours"}


@dataclass
class PostFeatures:
    """Extracted structural features from a single post."""
    # Metadata
    text: str = ""
    platform: str = ""
    engagement_rate: float = 0.0
    impressions: int = 0
    date: str = ""

    # Structural features
    hook_type: str = "statement"          # question/number_lead/contrarian/story_open/challenge/statement
    word_count: int = 0
    sentence_count: int = 0
    avg_sentence_length: float = 0.0
    sentence_length_cv: float = 0.0       # coefficient of variation (burstiness)
    question_count: int = 0
    specific_numbers_count: int = 0       # numbers, %, $, data points
    personal_pronoun_density: float = 0.0 # per 100 words
    has_list_formatting: bool = False
    paragraph_count: int = 0
    cta_type: str = "none"                # question_cta/action_cta/share_cta/comment_cta/none
    sentiment: str = "neutral"            # positive/negative/neutral
    specificity_score: float = 0.0        # proper nouns + numbers + tool names per 100 words
    has_external_link: bool = False

    # Derived
    tier: str = ""                        # top/middle/bottom (set after grouping)


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def _sentences(text: str) -> list[str]:
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    # Also split on newlines for social media formatting
    expanded = []
    for s in raw:
        expanded.extend(line.strip() for line in s.split("\n") if len(line.strip()) > 3)
    return expanded


def extract_features(text: str, platform: str = "", engagement_rate: float = 0.0,
                     impressions: int = 0, date: str = "") -> PostFeatures:
    """Extract 12 structural features from a post."""
    tokens = _tokenize(text)
    sentences = _sentences(text)
    text_lower = text.lower()

    feat = PostFeatures(
        text=text[:200],
        platform=platform,
        engagement_rate=engagement_rate,
        impressions=impressions,
        date=date,
    )

    # 1. Hook type (check first sentence)
    first_line = text.strip().split("\n")[0] if text.strip() else ""
    feat.hook_type = "statement"
    for hook_name, pattern in HOOK_PATTERNS.items():
        if pattern.search(first_line):
            feat.hook_type = hook_name
            break

    # 2. Word count
    feat.word_count = len(tokens)

    # 3-4. Sentence stats
    feat.sentence_count = len(sentences)
    if sentences:
        lengths = [len(_tokenize(s)) for s in sentences]
        feat.avg_sentence_length = round(mean(lengths), 1) if lengths else 0
        if len(lengths) >= 2:
            m = mean(lengths)
            if m > 0:
                feat.sentence_length_cv = round(stdev(lengths) / m, 2)

    # 5. Question count (body questions, not just hook)
    feat.question_count = sum(1 for s in sentences if s.rstrip().endswith("?"))

    # 6. Specific numbers (%, $, digits, years)
    numbers = re.findall(r'\b\d+[%$€£¥KkMmBb]?\b', text)
    years = re.findall(r'\b20[12]\d\b', text)
    metrics = re.findall(r'\b\d+(?:\.\d+)?x\b', text)
    feat.specific_numbers_count = len(numbers) + len(years) + len(metrics)

    # 7. Personal pronoun density
    if len(tokens) >= 5:
        pcount = sum(1 for t in tokens if t in PERSONAL_PRONOUNS)
        feat.personal_pronoun_density = round(pcount / (len(tokens) / 100), 1)

    # 8. List formatting
    feat.has_list_formatting = bool(
        re.search(r'(?m)^[\s]*[-•*]\s', text) or
        re.search(r'(?m)^[\s]*\d+[.)]\s', text)
    )

    # 9. Paragraph count
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    feat.paragraph_count = max(1, len(paragraphs))

    # 10. CTA type
    # Check last 30% of text for CTA
    last_portion = text[int(len(text) * 0.7):]
    feat.cta_type = "none"
    for cta_name, pattern in CTA_PATTERNS.items():
        if pattern.search(last_portion):
            feat.cta_type = cta_name
            break

    # 11. Sentiment (simple keyword-based)
    pos_count = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg_count = sum(1 for t in tokens if t in NEGATIVE_WORDS)
    if pos_count > neg_count + 1:
        feat.sentiment = "positive"
    elif neg_count > pos_count + 1:
        feat.sentiment = "negative"
    else:
        feat.sentiment = "neutral"

    # 12. Specificity score (proper nouns + numbers + tool names per 100 words)
    proper_nouns = len(re.findall(r'(?<!\. )\b[A-Z][a-z]{2,}\b', text))
    total_specific = feat.specific_numbers_count + proper_nouns
    if len(tokens) >= 5:
        feat.specificity_score = round(total_specific / (len(tokens) / 100), 1)

    # 13. External link
    feat.has_external_link = bool(re.search(r'https?://', text))

    return feat


# ─── Tier grouping ───────────────────────────────────────────────────

def assign_tiers(posts: list[PostFeatures]) -> list[PostFeatures]:
    """Group posts into top 25%, middle 50%, bottom 25% by engagement."""
    if len(posts) < 4:
        # Too few posts — use simple thirds
        sorted_posts = sorted(posts, key=lambda p: p.engagement_rate, reverse=True)
        third = max(1, len(sorted_posts) // 3)
        for i, p in enumerate(sorted_posts):
            if i < third:
                p.tier = "top"
            elif i >= len(sorted_posts) - third:
                p.tier = "bottom"
            else:
                p.tier = "middle"
        return sorted_posts

    sorted_posts = sorted(posts, key=lambda p: p.engagement_rate, reverse=True)
    q25 = max(1, len(sorted_posts) // 4)
    q75 = len(sorted_posts) - q25

    for i, p in enumerate(sorted_posts):
        if i < q25:
            p.tier = "top"
        elif i >= q75:
            p.tier = "bottom"
        else:
            p.tier = "middle"

    return sorted_posts


# ─── Pattern analysis ─────────────────────────────────────────────────

@dataclass
class TierProfile:
    """Aggregated profile for a performance tier."""
    tier: str
    count: int = 0
    avg_engagement: float = 0.0
    avg_word_count: float = 0.0
    avg_sentence_count: float = 0.0
    avg_sentence_length: float = 0.0
    avg_sentence_cv: float = 0.0
    avg_questions: float = 0.0
    avg_numbers: float = 0.0
    avg_pronoun_density: float = 0.0
    avg_specificity: float = 0.0
    pct_list_formatting: float = 0.0
    pct_external_link: float = 0.0
    hook_distribution: dict = field(default_factory=dict)
    cta_distribution: dict = field(default_factory=dict)
    sentiment_distribution: dict = field(default_factory=dict)


def _safe_mean(values: list[float]) -> float:
    return round(mean(values), 2) if values else 0.0


def build_tier_profile(posts: list[PostFeatures], tier: str) -> TierProfile:
    """Build an aggregated profile for a tier."""
    tier_posts = [p for p in posts if p.tier == tier]
    if not tier_posts:
        return TierProfile(tier=tier)

    profile = TierProfile(tier=tier, count=len(tier_posts))
    profile.avg_engagement = _safe_mean([p.engagement_rate for p in tier_posts])
    profile.avg_word_count = _safe_mean([float(p.word_count) for p in tier_posts])
    profile.avg_sentence_count = _safe_mean([float(p.sentence_count) for p in tier_posts])
    profile.avg_sentence_length = _safe_mean([p.avg_sentence_length for p in tier_posts])
    profile.avg_sentence_cv = _safe_mean([p.sentence_length_cv for p in tier_posts])
    profile.avg_questions = _safe_mean([float(p.question_count) for p in tier_posts])
    profile.avg_numbers = _safe_mean([float(p.specific_numbers_count) for p in tier_posts])
    profile.avg_pronoun_density = _safe_mean([p.personal_pronoun_density for p in tier_posts])
    profile.avg_specificity = _safe_mean([p.specificity_score for p in tier_posts])
    profile.pct_list_formatting = round(sum(1 for p in tier_posts if p.has_list_formatting) / len(tier_posts) * 100, 0)
    profile.pct_external_link = round(sum(1 for p in tier_posts if p.has_external_link) / len(tier_posts) * 100, 0)

    # Distributions
    hook_counts: Counter = Counter(p.hook_type for p in tier_posts)
    profile.hook_distribution = {k: round(v / len(tier_posts) * 100) for k, v in hook_counts.most_common()}

    cta_counts: Counter = Counter(p.cta_type for p in tier_posts)
    profile.cta_distribution = {k: round(v / len(tier_posts) * 100) for k, v in cta_counts.most_common()}

    sentiment_counts: Counter = Counter(p.sentiment for p in tier_posts)
    profile.sentiment_distribution = {k: round(v / len(tier_posts) * 100) for k, v in sentiment_counts.most_common()}

    return profile


# ─── Insight generation ───────────────────────────────────────────────

@dataclass
class Insight:
    """A specific finding comparing top vs bottom posts."""
    feature: str
    top_value: str
    bottom_value: str
    delta: str
    recommendation: str
    impact: str  # HIGH / MEDIUM / LOW


def generate_insights(top: TierProfile, bottom: TierProfile) -> list[Insight]:
    """Compare top and bottom tiers to find differentiating patterns."""
    insights: list[Insight] = []

    # Word count
    if top.avg_word_count > 0 and bottom.avg_word_count > 0:
        ratio = top.avg_word_count / bottom.avg_word_count if bottom.avg_word_count else 1
        if abs(ratio - 1.0) > 0.15:
            direction = "longer" if ratio > 1 else "shorter"
            insights.append(Insight(
                "Word Count",
                f"{top.avg_word_count:.0f} words",
                f"{bottom.avg_word_count:.0f} words",
                f"{direction} by {abs(ratio - 1) * 100:.0f}%",
                f"Aim for ~{top.avg_word_count:.0f} words",
                "MEDIUM",
            ))

    # Sentence variety (CV)
    if top.avg_sentence_cv > bottom.avg_sentence_cv + 0.1:
        insights.append(Insight(
            "Sentence Rhythm",
            f"CV={top.avg_sentence_cv:.2f} (varied)",
            f"CV={bottom.avg_sentence_cv:.2f} (monotone)",
            f"+{(top.avg_sentence_cv - bottom.avg_sentence_cv):.2f}",
            "Mix short punchy sentences (3-5 words) with longer explanations",
            "HIGH",
        ))

    # Specific numbers
    if top.avg_numbers > bottom.avg_numbers + 0.5:
        insights.append(Insight(
            "Specific Data Points",
            f"{top.avg_numbers:.1f} numbers/post",
            f"{bottom.avg_numbers:.1f} numbers/post",
            f"+{top.avg_numbers - bottom.avg_numbers:.1f}",
            "Include specific numbers, percentages, or metrics — posts with data get 3-4x reach",
            "HIGH",
        ))

    # Personal pronouns
    if top.avg_pronoun_density > bottom.avg_pronoun_density + 1.0:
        insights.append(Insight(
            "Personal Voice",
            f"{top.avg_pronoun_density:.1f}/100w pronouns",
            f"{bottom.avg_pronoun_density:.1f}/100w pronouns",
            f"+{top.avg_pronoun_density - bottom.avg_pronoun_density:.1f}",
            "Write from personal experience — use 'I', 'my', 'we' more",
            "HIGH",
        ))

    # Questions
    if top.avg_questions > bottom.avg_questions + 0.3:
        insights.append(Insight(
            "Questions",
            f"{top.avg_questions:.1f} questions/post",
            f"{bottom.avg_questions:.1f} questions/post",
            f"+{top.avg_questions - bottom.avg_questions:.1f}",
            "Add 1-2 genuine questions to spark discussion",
            "MEDIUM",
        ))

    # Specificity
    if top.avg_specificity > bottom.avg_specificity + 1.0:
        insights.append(Insight(
            "Specificity Score",
            f"{top.avg_specificity:.1f}/100w",
            f"{bottom.avg_specificity:.1f}/100w",
            f"+{top.avg_specificity - bottom.avg_specificity:.1f}",
            "Name specific tools, companies, projects — not generic 'best practices'",
            "HIGH",
        ))

    # List formatting
    if top.pct_list_formatting > bottom.pct_list_formatting + 20:
        insights.append(Insight(
            "List Formatting",
            f"{top.pct_list_formatting:.0f}% use lists",
            f"{bottom.pct_list_formatting:.0f}% use lists",
            f"+{top.pct_list_formatting - bottom.pct_list_formatting:.0f}pp",
            "Use bullet points or numbered lists for scannability",
            "MEDIUM",
        ))

    # Hook type
    top_hooks = top.hook_distribution
    bottom_hooks = bottom.hook_distribution
    top_dominant = max(top_hooks, key=top_hooks.get) if top_hooks else "unknown"
    bottom_dominant = max(bottom_hooks, key=bottom_hooks.get) if bottom_hooks else "unknown"
    if top_dominant != bottom_dominant:
        insights.append(Insight(
            "Hook Type",
            f"Mostly '{top_dominant}' ({top_hooks.get(top_dominant, 0)}%)",
            f"Mostly '{bottom_dominant}' ({bottom_hooks.get(bottom_dominant, 0)}%)",
            f"Different hook strategy",
            f"Lead with '{top_dominant}' hooks — they correlate with your best posts",
            "HIGH",
        ))

    # CTA type
    top_cta = top.cta_distribution
    bottom_cta = bottom.cta_distribution
    top_has_cta = 100 - top_cta.get("none", 0)
    bottom_has_cta = 100 - bottom_cta.get("none", 0)
    if top_has_cta > bottom_has_cta + 20:
        insights.append(Insight(
            "Call to Action",
            f"{top_has_cta:.0f}% have CTA",
            f"{bottom_has_cta:.0f}% have CTA",
            f"+{top_has_cta - bottom_has_cta:.0f}pp",
            "End with a clear CTA — question or action prompt",
            "MEDIUM",
        ))

    # External links
    if bottom.pct_external_link > top.pct_external_link + 15:
        insights.append(Insight(
            "External Links",
            f"{top.pct_external_link:.0f}% have links",
            f"{bottom.pct_external_link:.0f}% have links",
            f"-{bottom.pct_external_link - top.pct_external_link:.0f}pp",
            "Avoid external links in post body — LinkedIn gives ~60% less reach to posts with links",
            "HIGH",
        ))

    # Sort by impact
    impact_order = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
    insights.sort(key=lambda i: impact_order.get(i.impact, 0), reverse=True)

    return insights


# ─── Content blueprint ────────────────────────────────────────────────

def generate_blueprint(top: TierProfile, insights: list[Insight]) -> str:
    """Generate a content blueprint based on top-performing patterns."""
    lines = []
    lines.append("📋 YOUR CONTENT BLUEPRINT (based on your top-performing posts):\n")

    # Hook
    top_hook = max(top.hook_distribution, key=top.hook_distribution.get) if top.hook_distribution else "story_open"
    hook_templates = {
        "number_lead": "Start with a specific number: 'I [verb] [number] [things] in [timeframe].'",
        "question": "Open with a question your audience cares about.",
        "contrarian": "Challenge conventional wisdom: 'Stop doing X. Here's why.'",
        "story_open": "Begin with a personal story: 'Last [time], I [did something]...'",
        "challenge": "Present a how-to: 'Here's how I [achieved result].'",
        "statement": "Make a bold statement backed by your experience.",
    }
    lines.append(f"  HOOK: {hook_templates.get(top_hook, 'Start with a strong opening')}")

    # Length
    lines.append(f"  LENGTH: ~{top.avg_word_count:.0f} words, {top.avg_sentence_count:.0f} sentences")

    # Structure
    if top.pct_list_formatting > 50:
        lines.append("  FORMAT: Use bullet points or numbered lists")
    lines.append(f"  PARAGRAPHS: {max(1, int(top.avg_sentence_count / 3))}-{max(2, int(top.avg_sentence_count / 2))} short paragraphs")

    # Data
    lines.append(f"  DATA: Include ~{max(1, int(top.avg_numbers))} specific numbers/metrics")
    lines.append(f"  VOICE: Personal — aim for {top.avg_pronoun_density:.0f}+ first-person pronouns per 100 words")

    # CTA
    top_cta = max(top.cta_distribution, key=top.cta_distribution.get) if top.cta_distribution else "none"
    cta_templates = {
        "question_cta": "End with a genuine question for your audience",
        "action_cta": "End with a clear next step the reader can take",
        "comment_cta": "Invite comments or experiences from readers",
        "share_cta": "Ask readers to share if they found it useful",
        "none": "Consider adding a closing question or call-to-action",
    }
    lines.append(f"  CTA: {cta_templates.get(top_cta, 'End with engagement prompt')}")

    return "\n".join(lines)


# ─── Report formatter ─────────────────────────────────────────────────

def format_report(posts: list[PostFeatures], insights: list[Insight],
                  top: TierProfile, bottom: TierProfile, blueprint: str) -> str:
    """Format the complete forensics report."""
    lines: list[str] = []
    w = lines.append

    w("=" * 66)
    w("  phy-post-forensics — Content Forensics Report")
    w("=" * 66)
    w(f"  Posts analyzed : {len(posts)}")
    w(f"  Top tier       : {top.count} posts (avg {top.avg_engagement:.2f}% engagement)")
    w(f"  Bottom tier    : {bottom.count} posts (avg {bottom.avg_engagement:.2f}% engagement)")
    eng_spread = top.avg_engagement / bottom.avg_engagement if bottom.avg_engagement > 0 else 0
    w(f"  Spread         : Top posts get {eng_spread:.1f}x more engagement")
    w("=" * 66)

    # Per-post feature table
    w("\n📊  Per-Post Feature Extraction:\n")
    w(f"  {'Tier':<7} {'Eng%':>6} {'Words':>6} {'Hook':<14} {'#s':>3} {'Qs':>3} {'I/my':>5} {'CTA':<13} {'Spec':>5}")
    w("  " + "-" * 64)
    for p in posts:
        tier_icon = {"top": "🟢", "middle": "🟡", "bottom": "🔴"}.get(p.tier, "⚪")
        w(f"  {tier_icon}{p.tier:<5} {p.engagement_rate:>5.1f}% {p.word_count:>5} "
          f"{p.hook_type:<14} {p.specific_numbers_count:>3} {p.question_count:>3} "
          f"{p.personal_pronoun_density:>4.1f} {p.cta_type:<13} {p.specificity_score:>4.1f}")

    # Insights
    if insights:
        w(f"\n🔍  Key Insights ({len(insights)} patterns found):\n")
        for i, ins in enumerate(insights, 1):
            impact_icon = {"HIGH": "🔴", "MEDIUM": "🟠", "LOW": "🟡"}.get(ins.impact, "⚪")
            w(f"  {i}. {impact_icon} [{ins.impact}] {ins.feature}")
            w(f"     Top posts: {ins.top_value}")
            w(f"     Bottom:    {ins.bottom_value}")
            w(f"     → {ins.recommendation}")
            w("")

    # Blueprint
    w("\n" + blueprint)

    # Top vs Bottom summary
    w("\n\n📈  YOUR TOP POSTS SHARE:")
    top_features = []
    if insights:
        for ins in insights[:3]:
            top_features.append(f"  • {ins.feature}: {ins.top_value}")
    w("\n".join(top_features) if top_features else "  (need more posts for pattern detection)")

    w("\n📉  YOUR BOTTOM POSTS SHARE:")
    bottom_features = []
    if insights:
        for ins in insights[:3]:
            bottom_features.append(f"  • {ins.feature}: {ins.bottom_value}")
    w("\n".join(bottom_features) if bottom_features else "  (need more posts for pattern detection)")

    w("")
    return "\n".join(lines)


def format_json_report(posts: list[PostFeatures], insights: list[Insight],
                       top: TierProfile, bottom: TierProfile) -> str:
    """JSON output for pipelines."""
    return json.dumps({
        "post_count": len(posts),
        "top_tier": {"count": top.count, "avg_engagement": top.avg_engagement},
        "bottom_tier": {"count": bottom.count, "avg_engagement": bottom.avg_engagement},
        "posts": [
            {
                "text_preview": p.text[:80],
                "platform": p.platform,
                "engagement_rate": p.engagement_rate,
                "tier": p.tier,
                "hook_type": p.hook_type,
                "word_count": p.word_count,
                "specific_numbers": p.specific_numbers_count,
                "question_count": p.question_count,
                "personal_pronoun_density": p.personal_pronoun_density,
                "specificity_score": p.specificity_score,
                "cta_type": p.cta_type,
                "sentiment": p.sentiment,
                "has_list": p.has_list_formatting,
            }
            for p in posts
        ],
        "insights": [
            {"feature": i.feature, "top": i.top_value, "bottom": i.bottom_value,
             "recommendation": i.recommendation, "impact": i.impact}
            for i in insights
        ],
    }, indent=2)


# ─── Main analysis pipeline ──────────────────────────────────────────

def analyze_posts(raw_posts: list[dict]) -> tuple[list[PostFeatures], list[Insight], TierProfile, TierProfile, str]:
    """Run the full forensics pipeline."""
    # Extract features
    posts = []
    for rp in raw_posts:
        text = rp.get("text", "")
        if not text.strip():
            continue
        feat = extract_features(
            text=text,
            platform=rp.get("platform", ""),
            engagement_rate=float(rp.get("engagement_rate", 0)),
            impressions=int(rp.get("impressions", 0)),
            date=rp.get("date", ""),
        )
        posts.append(feat)

    if len(posts) < 3:
        return posts, [], TierProfile("top"), TierProfile("bottom"), "Need at least 3 posts for analysis."

    # Assign tiers
    posts = assign_tiers(posts)

    # Build profiles
    top = build_tier_profile(posts, "top")
    bottom = build_tier_profile(posts, "bottom")

    # Generate insights
    insights = generate_insights(top, bottom)

    # Generate blueprint
    blueprint = generate_blueprint(top, insights)

    return posts, insights, top, bottom, blueprint


# ─── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-post-forensics: Why Did This Post Work?",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Input format (JSON array):
              [
                {"text": "Post content...", "platform": "linkedin", "engagement_rate": 5.2, "impressions": 12000, "date": "2026-03-01"},
                {"text": "Another post...", "platform": "reddit", "engagement_rate": 1.1, "impressions": 500}
              ]

            Examples:
              python3 post_forensics.py --file my_posts.json
              cat posts.json | python3 post_forensics.py
              python3 post_forensics.py --file posts.json --format json
        """),
    )
    parser.add_argument("--file", "-f", help="JSON file with post data")
    parser.add_argument("--format", default="text", choices=["text", "json"],
                        help="Output format (default: text)")

    args = parser.parse_args()

    # Read input
    if args.file:
        with open(args.file, "r") as fh:
            raw_posts = json.load(fh)
    elif not sys.stdin.isatty():
        raw_posts = json.load(sys.stdin)
    else:
        parser.error("Provide posts via --file or stdin pipe")

    if not isinstance(raw_posts, list):
        parser.error("Input must be a JSON array of post objects")

    posts, insights, top, bottom, blueprint = analyze_posts(raw_posts)

    if args.format == "json":
        print(format_json_report(posts, insights, top, bottom))
    else:
        print(format_report(posts, insights, top, bottom, blueprint))


if __name__ == "__main__":
    main()
