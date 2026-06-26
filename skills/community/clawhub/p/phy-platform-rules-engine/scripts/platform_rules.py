#!/usr/bin/env python3
"""
phy-platform-rules-engine — Social Media Pre-Flight Checker

Scans any draft post against platform-specific invisible rules and outputs
PASS/WARN/FAIL per rule with exact fix suggestions. Like a linter for content.

Platforms: Reddit, LinkedIn, Twitter/X, HackerNews
Rules: 30+ platform-specific checks derived from algorithm research

Research basis:
- Reddit: 90/10 self-promo ratio, 30-day link ban, shadowban triggers
- LinkedIn: 360Brew LLM detection, 60% link penalty, engagement bait NLP filter
- Twitter/X: 150x reply-with-author multiplier, 30-min velocity window, link depression
- HackerNews: Show HN rules, tutorial downrank, clickbait edit by dang

Zero external dependencies — pure Python 3.7+ stdlib.
"""

from __future__ import annotations

import json
import re
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Optional


# ─── Rule definitions ─────────────────────────────────────────────────

@dataclass
class RuleResult:
    """Result from checking a single rule."""
    rule_id: str
    name: str
    status: str        # PASS / WARN / FAIL
    detail: str
    fix: str = ""
    impact: str = ""   # HIGH / MEDIUM / LOW


# ─── Shared detection helpers ─────────────────────────────────────────

def _word_count(text: str) -> int:
    return len(re.findall(r'[a-z]+(?:\'[a-z]+)?', text.lower()))

def _has_external_link(text: str) -> bool:
    return bool(re.search(r'https?://', text))

def _extract_links(text: str) -> list[str]:
    return re.findall(r'https?://[^\s)>\]]+', text)

def _has_question(text: str) -> bool:
    return '?' in text

def _count_hashtags(text: str) -> int:
    return len(re.findall(r'#\w+', text))

AI_BANNED_WORDS = {
    "leverage", "robust", "crucial", "delve", "tapestry", "holistic",
    "synergy", "paradigm", "ecosystem", "landscape", "streamline",
    "cutting-edge", "game-changer", "innovative", "revolutionary",
    "transformative", "comprehensive", "meticulous", "nuanced",
    "multifaceted", "pivotal", "seamless", "foster", "utilize",
    "facilitate", "endeavor", "underscore", "realm", "navigate",
    "embark", "spearhead", "harness", "unveil", "bolster",
    "cornerstone", "unparalleled", "groundbreaking",
}

ENGAGEMENT_BAIT_PATTERNS = [
    r"(?i)comment\s+(yes|no|if you|below|your)",
    r"(?i)like\s+for\s+(part|more|this)",
    r"(?i)tag\s+(a\s+friend|someone)",
    r"(?i)share\s+if\s+you",
    r"(?i)who\s+(else|agrees)\s*\?",
    r"(?i)agree\s*\?\s*(comment|like|share)",
    r"(?i)drop\s+a\s+\S+\s+if",
    r"(?i)type\s+['\"]\w+['\"]\s+in\s+the\s+comments",
    r"(?i)repost\s+this",
    r"(?i)\breact\s+with\b",
]

SELF_PROMO_SIGNALS = [
    r"(?i)(check out|try|use|download|sign up|get started|subscribe|my product|my tool|my app|my saas|my startup|my company|we built|i built|launching|just launched|we're launching|link in bio)",
]

CLICKBAIT_PATTERNS = [
    r"(?i)you won't believe",
    r"(?i)this (one|simple) trick",
    r"(?i)number \d+ will (shock|surprise|blow)",
    r"(?i)(mind-blowing|jaw-dropping|insane|crazy)",
    r"(?i)what happened next",
    r"(?i)the secret (to|of|behind)",
    r"(?i)no one (talks|is talking) about",
    r"(?i)\b(SHOCKING|BREAKING|URGENT|MUST READ)\b",
]


# ─── Reddit Rules ─────────────────────────────────────────────────────

def check_reddit(text: str, context: dict = None) -> list[RuleResult]:
    """Check a post draft against Reddit's rules."""
    ctx = context or {}
    results = []
    text_lower = text.lower()
    wc = _word_count(text)

    # R001: Self-promotion in first paragraph
    first_para = text.split("\n\n")[0] if "\n\n" in text else text[:200]
    promo_in_lead = any(re.search(p, first_para) for p in SELF_PROMO_SIGNALS)
    if promo_in_lead:
        results.append(RuleResult(
            "R001", "Self-promo in opening",
            "FAIL",
            "Product/self-promotion detected in the first paragraph. Reddit users downvote self-promo openers.",
            "Move product mention to a reply comment or later in the post. Lead with value/insight first.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("R001", "Self-promo in opening", "PASS", "No self-promotion in opening paragraph."))

    # R002: Self-promotion ratio check
    promo_count = sum(1 for p in SELF_PROMO_SIGNALS if re.search(p, text))
    sentences = [s.strip() for s in re.split(r'[.!?]\s+', text) if len(s.strip()) > 5]
    promo_ratio = promo_count / max(1, len(sentences))
    if promo_ratio > 0.3:
        results.append(RuleResult(
            "R002", "Self-promotion ratio",
            "FAIL",
            f"~{promo_ratio:.0%} of content is promotional (max 10% recommended). Reddit's 90/10 rule violated.",
            "Add more value-first content: insights, data, personal lessons learned. Max 1 promo mention per post.",
            "HIGH",
        ))
    elif promo_ratio > 0.1:
        results.append(RuleResult(
            "R002", "Self-promotion ratio",
            "WARN",
            f"~{promo_ratio:.0%} promotional content. Close to Reddit's 90/10 limit.",
            "Consider reducing promotional mentions. Lead with insight, mention product only in context.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("R002", "Self-promotion ratio", "PASS", f"Promotional ratio: {promo_ratio:.0%} (within 90/10 limit)."))

    # R003: External link in body
    links = _extract_links(text)
    if links:
        results.append(RuleResult(
            "R003", "External link in body",
            "WARN",
            f"Found {len(links)} external link(s). Reddit tracks link-to-comment ratio. >10% links → spam flag.",
            "Consider posting the link in a reply comment instead. Text-only posts get more trust on Reddit.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("R003", "External link in body", "PASS", "No external links in post body."))

    # R004: Post length
    if wc < 50:
        results.append(RuleResult(
            "R004", "Post length",
            "WARN",
            f"Only {wc} words. Short posts on Reddit often get ignored or seen as low-effort.",
            "Expand with context, personal experience, or data. 100-300 words is the sweet spot.",
            "LOW",
        ))
    elif wc > 500:
        results.append(RuleResult(
            "R004", "Post length",
            "WARN",
            f"{wc} words is quite long for Reddit. Consider splitting into a post + comments.",
            "Put the TL;DR at the top. Reddit users decide in 3 seconds whether to read.",
            "LOW",
        ))
    else:
        results.append(RuleResult("R004", "Post length", "PASS", f"{wc} words — good length for Reddit."))

    # R005: Missing question / discussion prompt
    if not _has_question(text):
        results.append(RuleResult(
            "R005", "No discussion prompt",
            "WARN",
            "No question mark found. Reddit rewards discussion-generating posts.",
            "End with a genuine question: 'Has anyone else experienced this?' or 'What's your approach?'",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("R005", "Discussion prompt", "PASS", "Contains a question — encourages discussion."))

    # R006: Clickbait patterns
    clickbait = [p for p in CLICKBAIT_PATTERNS if re.search(p, text)]
    if clickbait:
        results.append(RuleResult(
            "R006", "Clickbait language",
            "WARN",
            "Clickbait-style language detected. Reddit community actively downvotes clickbait.",
            "Use straightforward, specific titles. State facts, not hype.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("R006", "Clickbait language", "PASS", "No clickbait patterns detected."))

    # R007: Cross-posting signal (same text format)
    if re.search(r'(?i)(also posted|cross-posted|x-post|shared on my)', text):
        results.append(RuleResult(
            "R007", "Cross-posting signal",
            "FAIL",
            "Cross-posting mention detected. Reddit penalizes content that looks mass-distributed.",
            "Remove cross-posting references. Each platform version should feel native.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("R007", "Cross-posting signal", "PASS", "No cross-posting references."))

    return results


# ─── LinkedIn Rules ───────────────────────────────────────────────────

def check_linkedin(text: str, context: dict = None) -> list[RuleResult]:
    """Check a post draft against LinkedIn's 2026 algorithm rules."""
    results = []
    text_lower = text.lower()
    wc = _word_count(text)

    # L001: External link penalty
    links = _extract_links(text)
    if links:
        results.append(RuleResult(
            "L001", "External link penalty",
            "FAIL",
            f"External link found in post body. LinkedIn gives ~60% LESS reach to posts with links.",
            "Move the link to the first comment. Make the post valuable without requiring a click.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("L001", "External link penalty", "PASS", "No external links — maximum reach potential."))

    # L002: Engagement bait
    bait = [p for p in ENGAGEMENT_BAIT_PATTERNS if re.search(p, text)]
    if bait:
        results.append(RuleResult(
            "L002", "Engagement bait detection",
            "FAIL",
            "Engagement bait pattern detected. LinkedIn's NLP filter actively detects and penalizes this.",
            "Replace with a genuine question that invites sharing experiences, not performative reactions.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("L002", "Engagement bait detection", "PASS", "No engagement bait patterns found."))

    # L003: AI content signals
    ai_words = [w for w in AI_BANNED_WORDS if w in text_lower]
    if len(ai_words) >= 3:
        results.append(RuleResult(
            "L003", "AI content signals",
            "FAIL",
            f"Found {len(ai_words)} AI-flagged words: {', '.join(ai_words[:5])}. LinkedIn's 360Brew penalizes AI content with 30% less reach.",
            "Replace each flagged word with a specific, concrete alternative. Use phy-content-humanizer-audit for full analysis.",
            "HIGH",
        ))
    elif ai_words:
        results.append(RuleResult(
            "L003", "AI content signals",
            "WARN",
            f"Found {len(ai_words)} AI-flagged word(s): {', '.join(ai_words)}. Minor risk.",
            "Consider replacing with plain language.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("L003", "AI content signals", "PASS", "No AI-flagged vocabulary detected."))

    # L004: Hashtag count
    hashtag_count = _count_hashtags(text)
    if hashtag_count > 5:
        results.append(RuleResult(
            "L004", "Hashtag overuse",
            "WARN",
            f"{hashtag_count} hashtags found. LinkedIn recommends 3-5 max. More looks spammy.",
            "Reduce to 3-5 highly relevant hashtags.",
            "MEDIUM",
        ))
    elif hashtag_count == 0:
        results.append(RuleResult(
            "L004", "No hashtags",
            "WARN",
            "No hashtags. 3-5 relevant hashtags help LinkedIn categorize and distribute your post.",
            "Add 3-5 niche-specific hashtags.",
            "LOW",
        ))
    else:
        results.append(RuleResult("L004", "Hashtag count", "PASS", f"{hashtag_count} hashtags — within optimal range."))

    # L005: Hook quality (first 150 chars)
    first_150 = text[:150]
    has_hook_number = bool(re.search(r'\d', first_150))
    has_hook_question = '?' in first_150
    has_hook_story = bool(re.search(r'(?i)^(i |we |last |when |my |in 20)', first_150))
    has_hook_contrarian = bool(re.search(r'(?i)^.{0,20}(stop|don\'t|never|wrong|myth|actually|forget)', first_150))

    hook_signals = sum([has_hook_number, has_hook_question, has_hook_story, has_hook_contrarian])
    if hook_signals == 0:
        results.append(RuleResult(
            "L005", "Weak hook (first 150 chars)",
            "WARN",
            "First 150 characters have no strong hook signal (number, question, story, contrarian). This determines 'See more' clicks → dwell time.",
            "Start with a specific number, personal story, contrarian take, or compelling question.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("L005", "Hook strength", "PASS", f"Hook has {hook_signals} signal(s) in first 150 chars."))

    # L006: Post length
    if wc < 30:
        results.append(RuleResult(
            "L006", "Post too short",
            "WARN",
            f"Only {wc} words. Short posts generate less dwell time, which is LinkedIn's primary ranking signal.",
            "Aim for 100-250 words for text posts. Add personal context or data.",
            "MEDIUM",
        ))
    elif wc > 400:
        results.append(RuleResult(
            "L006", "Post length",
            "WARN",
            f"{wc} words. Long posts are fine if well-formatted, but check paragraph breaks.",
            "Use short paragraphs (2-3 lines max). Add line breaks for mobile readability.",
            "LOW",
        ))
    else:
        results.append(RuleResult("L006", "Post length", "PASS", f"{wc} words — within optimal range."))

    # L007: Paragraph formatting (mobile readability)
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    long_paragraphs = [p for p in paragraphs if _word_count(p) > 40]
    if long_paragraphs:
        results.append(RuleResult(
            "L007", "Long paragraphs",
            "WARN",
            f"{len(long_paragraphs)} paragraph(s) over 40 words. Long paragraphs reduce mobile readability → lower dwell time.",
            "Break into 2-3 line paragraphs. LinkedIn is consumed 60%+ on mobile.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("L007", "Paragraph formatting", "PASS", "All paragraphs are mobile-friendly length."))

    # L008: Engagement pod signals (checking for reciprocal patterns)
    pod_signals = re.findall(r'(?i)(engagement pod|pod members|engagement group|let\'s support each other|mutual engagement)', text)
    if pod_signals:
        results.append(RuleResult(
            "L008", "Engagement pod reference",
            "FAIL",
            "Engagement pod reference detected. LinkedIn actively detects and penalizes pod-driven engagement in 2026.",
            "Remove all pod references. LinkedIn's detection looks for reciprocal timing patterns.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("L008", "Engagement pod reference", "PASS", "No engagement pod signals."))

    return results


# ─── Twitter/X Rules ──────────────────────────────────────────────────

def check_twitter(text: str, context: dict = None) -> list[RuleResult]:
    """Check a post draft against Twitter/X's 2026 algorithm rules."""
    results = []
    text_lower = text.lower()
    wc = _word_count(text)

    # X001: External link penalty
    links = _extract_links(text)
    if links:
        results.append(RuleResult(
            "X001", "External link depression",
            "FAIL",
            "External link in tweet. Since March 2026, non-Premium accounts get near-zero engagement with links.",
            "Post value natively in the tweet. Put the link in a reply to yourself (reply with author = 150x multiplier).",
            "HIGH",
        ))
    else:
        results.append(RuleResult("X001", "External link depression", "PASS", "No external links — maximum algorithmic reach."))

    # X002: Thread hook strength
    first_line = text.strip().split("\n")[0]
    is_thread = bool(re.search(r'(🧵|thread|1/)', text_lower))
    if is_thread:
        hook_wc = _word_count(first_line)
        if hook_wc < 10:
            results.append(RuleResult(
                "X002", "Thread hook too short",
                "WARN",
                f"Thread hook is only {hook_wc} words. The hook tweet must perform independently — if it doesn't get traction, the rest won't be distributed.",
                "Spend 50% of writing time on the hook. Make it a standalone banger.",
                "HIGH",
            ))
        else:
            results.append(RuleResult("X002", "Thread hook", "PASS", f"Thread hook is {hook_wc} words — good length."))

    # X003: Character count
    char_count = len(text)
    if char_count > 280 and not is_thread:
        results.append(RuleResult(
            "X003", "Exceeds tweet limit",
            "FAIL" if char_count > 280 else "WARN",
            f"Tweet is {char_count} characters (limit: 280 for non-Premium). Will be truncated.",
            "Trim to 280 chars or restructure as a thread.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("X003", "Character count", "PASS", f"{char_count} characters — within limit."))

    # X004: Missing self-reply strategy hint
    if _has_external_link(text):
        results.append(RuleResult(
            "X004", "Link placement strategy",
            "WARN",
            "Tip: Reply to your own tweet with the link. Author reply = 150x algorithmic multiplier (vs like = 1x).",
            "Post the tweet without the link first. Immediately reply with the link.",
            "HIGH",
        ))

    # X005: Bookmark-worthy content check
    has_list = bool(re.search(r'(?m)^[\s]*[-•*]\s|(?m)^\d+[.)]\s', text))
    has_data = bool(re.search(r'\b\d+[%$€£KkMmx]\b', text))
    has_framework = bool(re.search(r'(?i)(step|tip|rule|lesson|principle|framework|playbook)', text))
    save_signals = sum([has_list, has_data, has_framework])

    if save_signals == 0:
        results.append(RuleResult(
            "X005", "Bookmark potential",
            "WARN",
            "No save-worthy signals (lists, data, frameworks). Bookmarks carry a 10x multiplier on X.",
            "Add a numbered list, specific data point, or actionable framework to increase saves.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("X005", "Bookmark potential", "PASS", f"{save_signals} bookmark-worthy element(s) detected."))

    # X006: Engagement velocity helper — question prompt
    last_portion = text[int(len(text) * 0.7):]
    if not _has_question(last_portion) and not _has_question(text[:50]):
        results.append(RuleResult(
            "X006", "No engagement prompt",
            "WARN",
            "No question to drive replies. Replies = 27x multiplier (vs like = 1x). Critical for first-30-min velocity.",
            "End with a question or opinion prompt. Replies are the #1 engagement signal on X.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("X006", "Engagement prompt", "PASS", "Contains a question — drives replies (27x multiplier)."))

    return results


# ─── HackerNews Rules ─────────────────────────────────────────────────

def check_hackernews(text: str, context: dict = None) -> list[RuleResult]:
    """Check a post draft against HackerNews submission rules."""
    results = []
    text_lower = text.lower()
    wc = _word_count(text)

    # HN001: Clickbait title patterns
    clickbait = [p for p in CLICKBAIT_PATTERNS if re.search(p, text)]
    if clickbait:
        results.append(RuleResult(
            "HN001", "Clickbait title",
            "FAIL",
            "Clickbait language detected. HN moderator (dang) will edit your title and may penalize the post.",
            "Use a factual, specific title. State what it IS, not how it makes you FEEL.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("HN001", "Title quality", "PASS", "No clickbait patterns detected."))

    # HN002: ALL CAPS detection
    caps_words = re.findall(r'\b[A-Z]{3,}\b', text)
    non_acronym_caps = [w for w in caps_words if w not in {"API", "SDK", "CLI", "SQL", "CSS", "HTML", "HTTP",
                                                           "AWS", "GCP", "TLS", "JWT", "PDF", "URL", "DNS",
                                                           "TCP", "UDP", "SSH", "YAML", "JSON", "TOML", "GPU",
                                                           "LLM", "NLP", "MLM", "SaaS", "OWASP", "CWE", "CORS",
                                                           "SSRF", "XSS", "OIDC", "HN", "YC", "MIT", "BSD"}]
    if non_acronym_caps:
        results.append(RuleResult(
            "HN002", "ALL CAPS in title",
            "WARN",
            f"Found capitalized words: {', '.join(non_acronym_caps[:3])}. HN guidelines: don't use ALL CAPS for emphasis.",
            "Use normal capitalization. Let the content speak for itself.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("HN002", "Capitalization", "PASS", "No inappropriate ALL CAPS."))

    # HN003: Show HN format check
    is_show_hn = bool(re.search(r'(?i)show\s+hn', text))
    if is_show_hn:
        has_url = _has_external_link(text)
        if not has_url:
            results.append(RuleResult(
                "HN003", "Show HN missing URL",
                "FAIL",
                "Show HN posts MUST include a URL. 'Posts without URLs get penalized' — HN rules.",
                "Add a link to your project, demo, or GitHub repo.",
                "HIGH",
            ))
        else:
            results.append(RuleResult("HN003", "Show HN URL", "PASS", "Show HN includes a URL."))

        # Show HN must be something people can run/hold
        blog_signals = re.search(r'(?i)(blog|article|post|newsletter|list of|opinion|essay|thoughts on)', text)
        if blog_signals:
            results.append(RuleResult(
                "HN004", "Show HN content type",
                "WARN",
                "Show HN is for things people can RUN or HOLD — not blog posts, newsletters, or reading material.",
                "If this is a blog post, submit it as a regular HN submission, not Show HN.",
                "HIGH",
            ))
        else:
            results.append(RuleResult("HN004", "Show HN content type", "PASS", "Appears to be a project/tool — correct for Show HN."))

    # HN005: Tutorial detection (downranked)
    tutorial_signals = re.search(r'(?i)(tutorial|how to|step.by.step|beginner.s guide|getting started with|introduction to)', text)
    if tutorial_signals:
        results.append(RuleResult(
            "HN005", "Tutorial content",
            "WARN",
            "Tutorial-style content detected. HN moderators explicitly downrank tutorials — they 'gratify intellectual curiosity less.'",
            "Frame as a technical deep-dive or novel approach, not a tutorial. HN values insight over instruction.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("HN005", "Content type", "PASS", "Not flagged as tutorial content."))

    # HN006: Self-promotion signals
    promo = any(re.search(p, text) for p in SELF_PROMO_SIGNALS)
    if promo and not is_show_hn:
        results.append(RuleResult(
            "HN006", "Self-promotion",
            "WARN",
            "Self-promotional content outside Show HN. Regular HN submissions flagged for self-promo get penalized.",
            "Use Show HN format for your own projects. For regular submissions, submit the underlying tech/insight.",
            "HIGH",
        ))
    else:
        results.append(RuleResult("HN006", "Self-promotion", "PASS", "Self-promotion within acceptable context."))

    # HN007: Technical depth signals
    tech_keywords = re.findall(r'(?i)\b(algorithm|benchmark|architecture|compiler|protocol|kernel|database|distributed|concurrent|cache|latency|throughput|parsing|binary|syscall|runtime)\b', text)
    if len(tech_keywords) < 1 and wc > 20:
        results.append(RuleResult(
            "HN007", "Technical depth",
            "WARN",
            "Low technical depth signal. HN audience strongly prefers technically substantive content.",
            "Include technical specifics: benchmarks, architecture decisions, performance data, or implementation details.",
            "MEDIUM",
        ))
    else:
        results.append(RuleResult("HN007", "Technical depth", "PASS", f"Found {len(tech_keywords)} technical term(s)."))

    return results


# ─── Main check dispatcher ───────────────────────────────────────────

PLATFORM_CHECKERS = {
    "reddit": check_reddit,
    "linkedin": check_linkedin,
    "twitter": check_twitter,
    "x": check_twitter,
    "hackernews": check_hackernews,
    "hn": check_hackernews,
}


def check_post(text: str, platform: str, context: dict = None) -> list[RuleResult]:
    """Run all rules for a given platform."""
    platform = platform.lower().strip()
    checker = PLATFORM_CHECKERS.get(platform)
    if not checker:
        return [RuleResult("ERR", "Unknown platform", "FAIL",
                           f"Platform '{platform}' not supported. Use: reddit, linkedin, twitter, hackernews")]
    return checker(text, context)


def compute_risk_score(results: list[RuleResult]) -> tuple[int, str]:
    """Compute overall risk score from rule results."""
    fail_count = sum(1 for r in results if r.status == "FAIL")
    warn_count = sum(1 for r in results if r.status == "WARN")
    total = len(results)

    score = max(0, 100 - fail_count * 25 - warn_count * 10)

    if fail_count >= 2:
        verdict = "HIGH RISK"
    elif fail_count == 1:
        verdict = "MODERATE RISK"
    elif warn_count >= 3:
        verdict = "MODERATE RISK"
    elif warn_count >= 1:
        verdict = "LOW RISK"
    else:
        verdict = "CLEAR"

    return score, verdict


# ─── Report formatter ─────────────────────────────────────────────────

def format_report(text: str, platform: str, results: list[RuleResult]) -> str:
    """Format the pre-flight check as a readable report."""
    lines: list[str] = []
    w = lines.append

    score, verdict = compute_risk_score(results)
    verdict_icon = {"CLEAR": "✅", "LOW RISK": "🟡", "MODERATE RISK": "🟠", "HIGH RISK": "🔴"}.get(verdict, "❓")

    platform_names = {"reddit": "Reddit", "linkedin": "LinkedIn", "twitter": "Twitter/X",
                      "x": "Twitter/X", "hackernews": "HackerNews", "hn": "HackerNews"}

    w("=" * 66)
    w("  phy-platform-rules-engine — Pre-Flight Check")
    w("=" * 66)
    w(f"  Platform : {platform_names.get(platform.lower(), platform)}")
    w(f"  Words    : {_word_count(text)}")
    w(f"  Score    : {score}/100 {verdict_icon} {verdict}")
    w(f"  Rules    : {sum(1 for r in results if r.status == 'PASS')} PASS, "
      f"{sum(1 for r in results if r.status == 'WARN')} WARN, "
      f"{sum(1 for r in results if r.status == 'FAIL')} FAIL")
    w("=" * 66)

    # Rule table
    w("\n📋  Rule Results:\n")
    for r in results:
        icon = {"PASS": "✅", "WARN": "🟡", "FAIL": "🔴"}.get(r.status, "❓")
        w(f"  {icon} [{r.rule_id}] {r.name} — {r.status}")
        if r.status != "PASS":
            w(f"     {r.detail}")
            if r.fix:
                w(f"     → Fix: {r.fix}")
            w("")

    # Summary
    fails = [r for r in results if r.status == "FAIL"]
    if fails:
        w("\n🚨  Must Fix Before Posting:\n")
        for i, f in enumerate(fails, 1):
            w(f"  {i}. {f.name}: {f.fix}")

    warns = [r for r in results if r.status == "WARN"]
    if warns:
        w(f"\n💡  Recommendations ({len(warns)}):\n")
        for i, wr in enumerate(warns, 1):
            w(f"  {i}. {wr.name}: {wr.fix}")

    w("")
    return "\n".join(lines)


def format_json(text: str, platform: str, results: list[RuleResult]) -> str:
    """JSON output for pipelines."""
    score, verdict = compute_risk_score(results)
    return json.dumps({
        "platform": platform,
        "word_count": _word_count(text),
        "score": score,
        "verdict": verdict,
        "rules": [
            {"id": r.rule_id, "name": r.name, "status": r.status,
             "detail": r.detail, "fix": r.fix, "impact": r.impact}
            for r in results
        ],
    }, indent=2)


# ─── CLI ──────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="phy-platform-rules-engine: Social Media Pre-Flight Checker",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              echo "My post" | python3 platform_rules.py --platform reddit
              python3 platform_rules.py --file draft.txt --platform linkedin
              python3 platform_rules.py --text "My post..." --platform twitter --format json
        """),
    )
    parser.add_argument("--text", "-t", help="Text to check (inline)")
    parser.add_argument("--file", "-f", help="Read text from file")
    parser.add_argument("--platform", "-p", required=True,
                        choices=["reddit", "linkedin", "twitter", "x", "hackernews", "hn"],
                        help="Target platform")
    parser.add_argument("--format", default="text", choices=["text", "json"],
                        help="Output format (default: text)")

    args = parser.parse_args()

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

    results = check_post(text.strip(), args.platform)

    if args.format == "json":
        print(format_json(text, args.platform, results))
    else:
        print(format_report(text, args.platform, results))

    # Exit code: 0=CLEAR, 1=warnings, 2=fails
    fail_count = sum(1 for r in results if r.status == "FAIL")
    sys.exit(2 if fail_count else (1 if any(r.status == "WARN" for r in results) else 0))


if __name__ == "__main__":
    main()
