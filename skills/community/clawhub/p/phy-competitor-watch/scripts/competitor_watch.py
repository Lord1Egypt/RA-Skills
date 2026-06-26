#!/usr/bin/env python3
"""
phy-competitor-watch — Competitor Social Media Content Analyzer

Analyzes a competitor's content strategy from exported/scraped posts.
Input: JSON file of competitor posts [{text, platform, date, engagement?, url?}]
Output: Content strategy breakdown — topics, posting patterns, content style,
        top-performing formats, and gaps you can exploit.

Zero external dependencies — pure Python 3.7+ stdlib.
"""

from __future__ import annotations

import json
import re
import sys
import textwrap
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from statistics import mean, median
from typing import Optional


# ─── Analysis helpers ─────────────────────────────────────────────────

TOPIC_KEYWORDS: dict[str, list[str]] = {
    "AI/ML": ["ai", "machine learning", "llm", "gpt", "claude", "model", "neural", "training", "inference", "transformer"],
    "DevTools": ["developer", "devtools", "cli", "sdk", "api", "framework", "library", "tooling", "dx", "open source"],
    "StartupGrowth": ["revenue", "mrr", "arr", "customers", "growth", "launch", "shipped", "users", "conversion", "churn"],
    "ProductDev": ["product", "feature", "roadmap", "mvp", "beta", "feedback", "iteration", "design", "ux", "ui"],
    "Marketing": ["marketing", "content", "seo", "brand", "social", "audience", "engagement", "distribution", "funnel"],
    "Engineering": ["architecture", "database", "deploy", "scale", "performance", "latency", "security", "infrastructure"],
    "Career": ["career", "hiring", "interview", "salary", "remote", "job", "team", "management", "leadership"],
    "BuildInPublic": ["building in public", "build in public", "ship", "progress", "update", "milestone", "journey"],
}

CONTENT_STYLES: dict[str, re.Pattern] = {
    "listicle": re.compile(r'(?m)(?:^[\s]*[-•*]\s+.+\n){3,}|(?m)(?:^[\s]*\d+[.)]\s+.+\n){3,}'),
    "story": re.compile(r'(?i)^(i |we |last |when i|my |back in|in 20)'),
    "contrarian": re.compile(r'(?i)^.{0,30}(stop|don\'t|never|wrong|myth|actually|unpopular|hot take|controversial)'),
    "how-to": re.compile(r'(?i)(how to|how i|step.by.step|here\'s how|guide|tutorial|playbook)'),
    "data-driven": re.compile(r'\b\d+[%$€£KkMmBbx]\b'),
    "question-led": re.compile(r'^[^.!]{5,}\?'),
    "announcement": re.compile(r'(?i)(just launched|announcing|excited to share|introducing|releasing|shipped|live now)'),
    "thread": re.compile(r'(?i)(🧵|thread|1/\d|part 1)'),
}


@dataclass
class CompetitorPost:
    text: str
    platform: str = ""
    date: str = ""
    engagement: float = 0.0
    url: str = ""
    # Derived
    word_count: int = 0
    topics: list[str] = field(default_factory=list)
    styles: list[str] = field(default_factory=list)
    has_link: bool = False
    has_media_hint: bool = False
    has_question: bool = False
    weekday: str = ""


@dataclass
class CompetitorProfile:
    name: str
    total_posts: int = 0
    date_range: str = ""
    avg_engagement: float = 0.0
    top_engagement: float = 0.0
    # Topic distribution
    topic_counts: dict[str, int] = field(default_factory=dict)
    # Style distribution
    style_counts: dict[str, int] = field(default_factory=dict)
    # Timing
    weekday_counts: dict[str, int] = field(default_factory=dict)
    # Length
    avg_word_count: float = 0.0
    # Top posts
    top_posts: list[CompetitorPost] = field(default_factory=list)
    # Gaps
    missing_topics: list[str] = field(default_factory=list)
    missing_styles: list[str] = field(default_factory=list)
    posting_frequency: str = ""


def _tokenize(text: str) -> list[str]:
    return re.findall(r'[a-z]+(?:\'[a-z]+)?', text.lower())


def _classify_topics(text: str) -> list[str]:
    text_lower = text.lower()
    topics = []
    for topic, keywords in TOPIC_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in text_lower)
        if hits >= 2:
            topics.append(topic)
    return topics or ["Other"]


def _classify_styles(text: str) -> list[str]:
    styles = []
    for style, pattern in CONTENT_STYLES.items():
        if pattern.search(text):
            styles.append(style)
    return styles or ["generic"]


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _parse_weekday(date_str: str) -> str:
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            dt = datetime.strptime(date_str[:19], fmt)
            return WEEKDAYS[dt.weekday()]
        except (ValueError, IndexError):
            continue
    return ""


def analyze_competitor(posts_data: list[dict], name: str = "Competitor") -> CompetitorProfile:
    """Analyze a competitor's content strategy."""
    profile = CompetitorProfile(name=name)
    posts: list[CompetitorPost] = []

    for raw in posts_data:
        text = raw.get("text", "")
        if not text.strip():
            continue

        p = CompetitorPost(
            text=text,
            platform=raw.get("platform", ""),
            date=raw.get("date", ""),
            engagement=float(raw.get("engagement", raw.get("engagement_rate", 0))),
            url=raw.get("url", ""),
        )
        p.word_count = len(_tokenize(text))
        p.topics = _classify_topics(text)
        p.styles = _classify_styles(text)
        p.has_link = bool(re.search(r'https?://', text))
        p.has_media_hint = bool(re.search(r'(?i)(image|video|screenshot|demo|gif|photo|pic)', text))
        p.has_question = '?' in text
        p.weekday = _parse_weekday(p.date)
        posts.append(p)

    if not posts:
        return profile

    profile.total_posts = len(posts)
    profile.avg_engagement = round(mean(p.engagement for p in posts), 2)
    profile.top_engagement = max(p.engagement for p in posts)

    # Date range
    dates = sorted(p.date for p in posts if p.date)
    if len(dates) >= 2:
        profile.date_range = f"{dates[0][:10]} → {dates[-1][:10]}"
    elif dates:
        profile.date_range = dates[0][:10]

    # Topics
    topic_counter: Counter = Counter()
    for p in posts:
        topic_counter.update(p.topics)
    profile.topic_counts = dict(topic_counter.most_common())

    # Styles
    style_counter: Counter = Counter()
    for p in posts:
        style_counter.update(p.styles)
    profile.style_counts = dict(style_counter.most_common())

    # Weekday distribution
    wd_counter: Counter = Counter(p.weekday for p in posts if p.weekday)
    profile.weekday_counts = {d: wd_counter.get(d, 0) for d in WEEKDAYS}

    # Word count
    profile.avg_word_count = round(mean(p.word_count for p in posts), 0)

    # Top posts by engagement
    sorted_posts = sorted(posts, key=lambda p: p.engagement, reverse=True)
    profile.top_posts = sorted_posts[:5]

    # Posting frequency
    if len(dates) >= 2:
        try:
            first = datetime.strptime(dates[0][:10], "%Y-%m-%d")
            last = datetime.strptime(dates[-1][:10], "%Y-%m-%d")
            days = max(1, (last - first).days)
            posts_per_week = round(len(posts) / days * 7, 1)
            profile.posting_frequency = f"{posts_per_week} posts/week"
        except ValueError:
            profile.posting_frequency = "unknown"

    # Gaps — topics and styles they DON'T cover
    all_topics = set(TOPIC_KEYWORDS.keys())
    covered_topics = set(profile.topic_counts.keys()) - {"Other"}
    profile.missing_topics = sorted(all_topics - covered_topics)

    all_styles = set(CONTENT_STYLES.keys())
    covered_styles = set(profile.style_counts.keys()) - {"generic"}
    profile.missing_styles = sorted(all_styles - covered_styles)

    return profile


def format_report(profile: CompetitorProfile) -> str:
    lines: list[str] = []
    w = lines.append

    w("=" * 66)
    w(f"  phy-competitor-watch — {profile.name} Content Analysis")
    w("=" * 66)
    w(f"  Posts analyzed   : {profile.total_posts}")
    w(f"  Date range       : {profile.date_range}")
    w(f"  Avg engagement   : {profile.avg_engagement}")
    w(f"  Top engagement   : {profile.top_engagement}")
    w(f"  Avg post length  : {profile.avg_word_count:.0f} words")
    w(f"  Posting frequency: {profile.posting_frequency}")
    w("=" * 66)

    # Topic distribution
    w("\n📊  Topic Distribution:\n")
    total = sum(profile.topic_counts.values())
    for topic, count in sorted(profile.topic_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100 if total else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        w(f"  {topic:<18} {bar} {pct:4.0f}% ({count})")

    # Style distribution
    w("\n🎨  Content Styles:\n")
    total_s = sum(profile.style_counts.values())
    for style, count in sorted(profile.style_counts.items(), key=lambda x: -x[1]):
        pct = count / total_s * 100 if total_s else 0
        w(f"  {style:<16} {pct:4.0f}% ({count} posts)")

    # Posting schedule
    if any(profile.weekday_counts.values()):
        w("\n📅  Posting Schedule:\n")
        max_wd = max(profile.weekday_counts.values()) if profile.weekday_counts else 1
        for day in WEEKDAYS:
            count = profile.weekday_counts.get(day, 0)
            bar = "█" * int(count / max(1, max_wd) * 15)
            w(f"  {day:<11} {bar} {count}")

    # Top posts
    if profile.top_posts:
        w(f"\n🏆  Top {len(profile.top_posts)} Posts by Engagement:\n")
        for i, p in enumerate(profile.top_posts, 1):
            preview = p.text[:80].replace("\n", " ")
            w(f"  {i}. [{p.engagement}] {preview}...")
            w(f"     Topics: {', '.join(p.topics)} | Style: {', '.join(p.styles)}")

    # Gaps you can exploit
    w("\n🎯  Gaps You Can Exploit:\n")
    if profile.missing_topics:
        w(f"  Topics they DON'T cover: {', '.join(profile.missing_topics)}")
    else:
        w("  They cover all major topics — differentiate on depth or angle.")

    if profile.missing_styles:
        w(f"  Styles they DON'T use:   {', '.join(profile.missing_styles)}")
    else:
        w("  They use all content styles — differentiate on quality.")

    # Actionable intel
    w("\n💡  Actionable Intel:\n")
    if profile.topic_counts:
        top_topic = max(profile.topic_counts, key=profile.topic_counts.get)
        w(f"  • Their #1 topic is {top_topic} — either compete directly or flank with adjacent topics")
    if profile.style_counts:
        top_style = max(profile.style_counts, key=profile.style_counts.get)
        w(f"  • Their dominant style is '{top_style}' — try a style they're NOT using")
    if profile.top_posts:
        top_topics = profile.top_posts[0].topics
        w(f"  • Their best-performing content is about {', '.join(top_topics)} — this is what their audience wants")

    w("")
    return "\n".join(lines)


def format_json(profile: CompetitorProfile) -> str:
    return json.dumps({
        "name": profile.name,
        "total_posts": profile.total_posts,
        "date_range": profile.date_range,
        "avg_engagement": profile.avg_engagement,
        "posting_frequency": profile.posting_frequency,
        "topics": profile.topic_counts,
        "styles": profile.style_counts,
        "weekday_distribution": profile.weekday_counts,
        "missing_topics": profile.missing_topics,
        "missing_styles": profile.missing_styles,
        "top_posts": [
            {"text": p.text[:200], "engagement": p.engagement,
             "topics": p.topics, "styles": p.styles}
            for p in profile.top_posts
        ],
    }, indent=2)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-competitor-watch: Competitor Content Strategy Analyzer",
        epilog=textwrap.dedent("""\
            Input JSON format:
              [{"text": "Post...", "platform": "linkedin", "date": "2026-03-01", "engagement": 5.2}]

            Examples:
              python3 competitor_watch.py --file competitor_posts.json --name "Dan Koe"
              cat posts.json | python3 competitor_watch.py --name "Competitor X"
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file", "-f", help="JSON file with competitor posts")
    parser.add_argument("--name", "-n", default="Competitor", help="Competitor name for report")
    parser.add_argument("--format", default="text", choices=["text", "json"])

    args = parser.parse_args()

    if args.file:
        with open(args.file) as fh:
            data = json.load(fh)
    elif not sys.stdin.isatty():
        data = json.load(sys.stdin)
    else:
        parser.error("Provide posts via --file or stdin")

    profile = analyze_competitor(data, args.name)

    if args.format == "json":
        print(format_json(profile))
    else:
        print(format_report(profile))


if __name__ == "__main__":
    main()
