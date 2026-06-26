#!/usr/bin/env python3
"""Score and rank opportunity findings by signal strength, engagement,
freshness, competition, and recurrence.

Usage:
    score_signals.py <findings.json>           Score findings, output ranked JSON
    score_signals.py <findings.json> --config <config.json>   Custom weights
    score_signals.py - < findings.json         Read from stdin
"""

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timedelta

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_DIR, "config.json")
HISTORY_PATH = os.path.join(SKILL_DIR, "history.json")

DEFAULT_WEIGHTS = {
    "signal_strength": 0.30,
    "engagement": 0.20,
    "freshness": 0.20,
    "competition": 0.15,
    "recurrence": 0.15,
}

# Strong demand signal keywords (weighted higher)
# Use flexible patterns — people don't say things exactly the same way
STRONG_SIGNALS = [
    "i wish", "someone should build", "someone would build", "someone needs to build",
    "shut up and take my money", "take my money",
    "i'd pay", "i would pay", "worth paying", "gladly pay",
    "why is there no", "why isn't there", "why does no one",
    "need a tool", "need something that",
]

# Moderate demand signal keywords
MODERATE_SIGNALS = [
    "frustrated", "so frustrated", "fed up", "drives me crazy", "annoyed",
    "looking for", "alternative to", "anyone solved", "has anyone solved",
    "workaround", "has anyone found", "hate that", "cobbled together",
    "duct tape", "jerry-rigged", "hack", "too expensive",
    "overkill", "bloated", "clunky", "terrible experience",
]

# Competition indicators (things that suggest the need IS being met)
COMPETITION_INDICATORS = [
    "try this", "I use", "check out", "have you tried", "I recommend",
    "we built", "just released", "solved this with",
]


def score_signal_strength(finding):
    """Score 0-10 based on how clearly the finding expresses unmet demand.

    Factors: number and type of matched keywords, keyword density in text.
    """
    matched = [k.lower() for k in finding.get("matched_keywords", [])]
    text = f"{finding.get('title', '')} {finding.get('snippet', '')}".lower()

    score = 0.0

    # Strong signal matches (3 points each, max 9)
    strong_matches = sum(1 for s in STRONG_SIGNALS if s in text)
    score += min(strong_matches * 3.0, 9.0)

    # Moderate signal matches (1.5 points each, max 6)
    moderate_matches = sum(1 for s in MODERATE_SIGNALS if s in text)
    score += min(moderate_matches * 1.5, 6.0)

    # Bonus for question marks (seeking behavior)
    question_marks = text.count("?")
    score += min(question_marks * 0.5, 1.5)

    # Bonus for specificity indicators (dollar amounts, named tools, metrics)
    if re.search(r'\$\d+', text):
        score += 1.0
    if re.search(r'\d+\s*(users|customers|employees|people|clients)', text):
        score += 0.5

    # Penalty for very short snippets (less context = less confidence)
    if len(text) < 50:
        score *= 0.5

    return min(round(score, 1), 10.0)


def score_engagement(finding):
    """Score 0-10 based on engagement signals extracted from snippet.

    Look for upvote counts, comment counts, and other engagement markers.
    """
    text = f"{finding.get('title', '')} {finding.get('snippet', '')}".lower()
    score = 5.0  # Default middle score when engagement data is absent

    # Try to extract upvote/point counts
    upvote_match = re.search(r'(\d+)\s*(upvotes?|points?|votes?|likes?)', text)
    if upvote_match:
        count = int(upvote_match.group(1))
        if count >= 100:
            score = 9.0
        elif count >= 50:
            score = 8.0
        elif count >= 20:
            score = 7.0
        elif count >= 10:
            score = 6.0
        elif count >= 5:
            score = 5.0
        else:
            score = 3.0

    # Try to extract comment counts
    comment_match = re.search(r'(\d+)\s*(comments?|replies?|responses?)', text)
    if comment_match:
        count = int(comment_match.group(1))
        if count >= 50:
            score = max(score, 9.0)
        elif count >= 20:
            score = max(score, 7.5)
        elif count >= 10:
            score = max(score, 6.5)

    return min(round(score, 1), 10.0)


def score_freshness(finding):
    """Score 0-10 based on how recent the finding is.

    Newer = more actionable = higher score.
    """
    date_str = finding.get("date", "")
    if not date_str:
        return 5.0  # Unknown age, middle score

    now = datetime.now()

    # Try parsing various date formats
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%b %d, %Y", "%B %d, %Y"):
        try:
            post_date = datetime.strptime(date_str.strip()[:19], fmt)
            days_old = (now - post_date).days

            if days_old <= 1:
                return 10.0
            elif days_old <= 7:
                return 9.0
            elif days_old <= 14:
                return 8.0
            elif days_old <= 30:
                return 7.0
            elif days_old <= 60:
                return 5.0
            elif days_old <= 90:
                return 3.0
            elif days_old <= 180:
                return 2.0
            else:
                return 1.0
        except ValueError:
            continue

    # Handle relative dates like "2 days ago", "3 hours ago"
    relative = re.search(r'(\d+)\s*(hour|day|week|month|year)s?\s*ago', date_str.lower())
    if relative:
        num = int(relative.group(1))
        unit = relative.group(2)
        if unit == "hour":
            return 10.0
        elif unit == "day":
            if num <= 1:
                return 10.0
            elif num <= 7:
                return 9.0
            elif num <= 14:
                return 8.0
            elif num <= 30:
                return 7.0
            else:
                return 5.0
        elif unit == "week":
            if num <= 1:
                return 8.5
            elif num <= 4:
                return 7.0
            else:
                return 5.0
        elif unit == "month":
            if num <= 1:
                return 6.0
            elif num <= 3:
                return 4.0
            else:
                return 2.0
        elif unit == "year":
            return 1.0

    return 5.0  # Can't parse, assume moderate


def score_competition(finding):
    """Score 0-10 where HIGH score = LOW competition (bigger opportunity).

    Check if the snippet suggests solutions already exist.
    """
    text = f"{finding.get('title', '')} {finding.get('snippet', '')}".lower()

    # Count competition indicators
    comp_count = sum(1 for c in COMPETITION_INDICATORS if c in text)

    if comp_count == 0:
        return 9.0  # No solutions mentioned — wide open
    elif comp_count == 1:
        return 7.0  # One mention — might be a partial solution
    elif comp_count == 2:
        return 5.0  # Multiple solutions mentioned
    elif comp_count <= 4:
        return 3.0  # Well-served market
    else:
        return 1.0  # Saturated

    return 5.0


def score_recurrence(finding):
    """Score 0-10 based on whether this signal has appeared in past scans.

    Reads from history.json to check for recurring topics.
    """
    if not os.path.exists(HISTORY_PATH):
        return 5.0  # No history yet, neutral score

    try:
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f)
    except (json.JSONDecodeError, IOError):
        return 5.0

    # Normalize title for matching
    title_lower = finding.get("title", "").lower().strip()
    url = finding.get("url", "")

    signals = history.get("signals", {})

    # Check for URL match (exact same post recurring in searches)
    for sig_key, sig_data in signals.items():
        if url and url in sig_data.get("urls", []):
            appearances = len(sig_data.get("scan_dates", []))
            if appearances >= 5:
                return 10.0
            elif appearances >= 3:
                return 8.5
            elif appearances >= 2:
                return 7.0
            else:
                return 5.5

    # Check for topic similarity (rough title overlap)
    title_words = set(title_lower.split()) - {"the", "a", "an", "is", "are", "was",
                                                "for", "to", "in", "on", "of", "and",
                                                "or", "but", "with", "how", "what",
                                                "why", "has", "anyone", "does", "do"}
    for sig_key, sig_data in signals.items():
        key_words = set(sig_key.split())
        overlap = title_words & key_words
        if len(overlap) >= 3:
            appearances = len(sig_data.get("scan_dates", []))
            if appearances >= 3:
                return 8.0
            elif appearances >= 2:
                return 6.5

    return 5.0  # No match found, neutral


def compute_composite_score(scores, weights):
    """Compute weighted composite score from individual dimension scores."""
    composite = 0.0
    for key, weight in weights.items():
        composite += scores.get(key, 5.0) * weight
    return round(composite, 2)


def score_findings(findings, weights=None):
    """Score all findings and return sorted by composite score."""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    scored = []
    for finding in findings:
        scores = {
            "signal_strength": score_signal_strength(finding),
            "engagement": score_engagement(finding),
            "freshness": score_freshness(finding),
            "competition": score_competition(finding),
            "recurrence": score_recurrence(finding),
        }
        composite = compute_composite_score(scores, weights)

        scored_finding = {
            **finding,
            "scores": scores,
            "composite_score": composite,
        }
        scored.append(scored_finding)

    # Sort by composite score descending
    scored.sort(key=lambda x: x["composite_score"], reverse=True)

    return scored


def main():
    parser = argparse.ArgumentParser(description="Score opportunity signal findings")
    parser.add_argument("findings", help="Path to findings JSON (or - for stdin)")
    parser.add_argument("--config", help="Path to config.json for custom weights")

    args = parser.parse_args()

    # Load findings
    if args.findings == "-":
        findings = json.load(sys.stdin)
    else:
        with open(args.findings, "r") as f:
            findings = json.load(f)

    # Load custom weights if provided
    weights = DEFAULT_WEIGHTS
    config_path = args.config or CONFIG_PATH
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            if "scoring_weights" in config:
                weights = config["scoring_weights"]
        except (json.JSONDecodeError, IOError):
            pass

    scored = score_findings(findings, weights)
    print(json.dumps(scored, indent=2))


if __name__ == "__main__":
    main()
