#!/usr/bin/env python3
"""Generate a prioritized markdown digest from scored opportunity findings.

Usage:
    digest.py <scored.json>                      Print digest to stdout
    digest.py <scored.json> --output report.md   Save to file
    digest.py <scored.json> --max-results 15     Limit top opportunities shown
    digest.py - < scored.json                    Read from stdin
"""

import argparse
import json
import os
import sys
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(SKILL_DIR, "history.json")


def load_history():
    """Load history for trend data."""
    if not os.path.exists(HISTORY_PATH):
        return None
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def classify_signal(sig):
    """Classify a signal as persistent, emerging, or fading."""
    scan_count = len(sig.get("scan_dates", []))
    scores = sig.get("scores_over_time", [])
    if scan_count >= 3:
        if len(scores) >= 3:
            recent_avg = sum(s["score"] for s in scores[-2:]) / 2
            older_avg = sum(s["score"] for s in scores[:-2]) / max(len(scores) - 2, 1)
            if recent_avg < older_avg * 0.7:
                return "fading"
        return "persistent"
    return "emerging"


def score_bar(score, max_score=10.0):
    """Generate a visual bar for a score."""
    filled = int(round(score / max_score * 5))
    return "●" * filled + "○" * (5 - filled)


def format_score_breakdown(scores):
    """Format score dimensions as a compact line."""
    parts = []
    labels = {
        "signal_strength": "Signal",
        "engagement": "Engage",
        "freshness": "Fresh",
        "competition": "No-Comp",
        "recurrence": "Recur",
    }
    for key, label in labels.items():
        val = scores.get(key, 0)
        parts.append(f"{label}: {val:.0f}")
    return " · ".join(parts)


def generate_executive_summary(scored_findings):
    """Generate 2-3 sentence executive summary."""
    if not scored_findings:
        return "No signals found in this scan cycle."

    top = scored_findings[:3]
    niches = list(set(f.get("niche", "General") for f in scored_findings if f.get("niche")))
    niche_str = ", ".join(niches[:3]) if niches else "configured niches"

    strong_count = sum(1 for f in scored_findings if f.get("composite_score", 0) >= 7.0)
    total = len(scored_findings)

    lines = []
    lines.append(f"Scanned {total} signals across {niche_str}.")

    if strong_count > 0:
        lines.append(f"**{strong_count} strong opportunities** scored 7.0+ — these deserve attention.")
    else:
        lines.append("No standout signals this cycle — the findings below are moderate strength.")

    if top:
        top_title = top[0].get("title", "Unknown")
        top_score = top[0].get("composite_score", 0)
        lines.append(f"Strongest signal: \"{top_title}\" ({top_score:.1f}/10).")

    return " ".join(lines)


def generate_digest(scored_findings, max_results=20):
    """Generate the full markdown digest."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    niches = list(set(f.get("niche", "") for f in scored_findings if f.get("niche")))
    sources = list(set(f.get("source", "") for f in scored_findings if f.get("source")))

    lines = []

    # YAML frontmatter
    lines.append("---")
    lines.append(f"date: {date_str}")
    lines.append(f"time: {time_str}")
    lines.append("type: opportunity-scan")
    niche_yaml = ", ".join(niches) if niches else "general"
    lines.append(f"niches: [{niche_yaml}]")
    lines.append(f"findings_count: {len(scored_findings)}")

    # Auto-generate tags
    tags = ["opportunity-scout", "demand-signals"]
    for n in niches:
        tag = n.lower().replace(" ", "-")[:30]
        tags.append(tag)
    tags_yaml = ", ".join(tags)
    lines.append(f"tags: [{tags_yaml}]")
    lines.append("---")
    lines.append("")

    # Title
    lines.append(f"# 🔭 Opportunity Scout — {date_str}")
    lines.append("")

    # Executive Summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(generate_executive_summary(scored_findings))
    lines.append("")

    # Top Opportunities
    top = scored_findings[:max_results]
    lines.append(f"## 🎯 Top Opportunities")
    lines.append("")

    for i, finding in enumerate(top, 1):
        title = finding.get("title", "Untitled")
        url = finding.get("url", "")
        snippet = finding.get("snippet", "")
        composite = finding.get("composite_score", 0)
        scores = finding.get("scores", {})
        source = finding.get("source", "unknown")
        matched = finding.get("matched_keywords", [])
        niche = finding.get("niche", "")

        # Score tier
        if composite >= 8.0:
            tier = "🔥"
        elif composite >= 6.0:
            tier = "⚡"
        elif composite >= 4.0:
            tier = "💡"
        else:
            tier = "📌"

        lines.append(f"### {i}. {tier} {title}")
        lines.append("")
        lines.append(f"**Score: {composite:.1f}/10** {score_bar(composite)}")
        lines.append(f"**Source:** [{source}]({url})")
        if niche:
            lines.append(f"**Niche:** {niche}")
        lines.append("")

        if snippet:
            # Truncate long snippets
            if len(snippet) > 300:
                snippet = snippet[:297] + "..."
            lines.append(f"> {snippet}")
            lines.append("")

        lines.append(f"**Signal Analysis:** {format_score_breakdown(scores)}")
        if matched:
            lines.append(f"**Matched signals:** {', '.join(matched[:5])}")
        lines.append("")

        # Why it matters / suggested next step
        if composite >= 7.0:
            lines.append("**Why it matters:** High signal strength with low existing "
                         "competition suggests a genuine unmet need worth exploring.")
            lines.append("**Next step:** Deep-dive research — check the thread replies, "
                         "search for existing solutions, estimate market size.")
        elif composite >= 5.0:
            lines.append("**Why it matters:** Moderate demand signal — worth monitoring "
                         "for recurrence across future scans.")
            lines.append("**Next step:** Add to watchlist. If this signal persists "
                         "across 2-3 more scans, investigate further.")
        else:
            lines.append("**Why it matters:** Weak or partially-served signal. "
                         "Keep on radar but don't invest research time yet.")

        lines.append("")
        lines.append("---")
        lines.append("")

    # Recurring Signals (from history)
    history = load_history()
    if history and history.get("signals"):
        persistent = []
        fading = []
        for key, sig in history["signals"].items():
            classification = classify_signal(sig)
            if classification == "persistent":
                persistent.append(sig)
            elif classification == "fading":
                fading.append(sig)

        if persistent:
            persistent.sort(key=lambda x: x.get("peak_score", 0), reverse=True)
            lines.append("## 🔁 Recurring Signals")
            lines.append("")
            lines.append("*These signals keep appearing across scans — persistent "
                         "demand is a strong indicator of real opportunity.*")
            lines.append("")
            for sig in persistent[:10]:
                title = sig["titles"][0] if sig.get("titles") else "Unknown"
                peak = sig.get("peak_score", 0)
                count = len(sig.get("scan_dates", []))
                first = sig.get("first_seen", "?")
                lines.append(f"- **{title}** — score {peak:.1f}, seen {count}x since {first}")
            lines.append("")

        if fading:
            fading.sort(key=lambda x: x.get("peak_score", 0), reverse=True)
            lines.append("## 📉 Fading Signals")
            lines.append("")
            lines.append("*Previously strong signals that are declining — the market "
                         "may be filling these gaps.*")
            lines.append("")
            for sig in fading[:10]:
                title = sig["titles"][0] if sig.get("titles") else "Unknown"
                peak = sig.get("peak_score", 0)
                last = sig.get("last_seen", "?")
                lines.append(f"- **{title}** — peak score {peak:.1f}, last seen {last}")
            lines.append("")

    # Raw Findings appendix
    if len(scored_findings) > max_results:
        remaining = scored_findings[max_results:]
        lines.append("## 📋 All Findings (Appendix)")
        lines.append("")
        lines.append(f"*{len(remaining)} additional findings below the top {max_results} cutoff.*")
        lines.append("")
        lines.append("| # | Score | Title | Source |")
        lines.append("|---|-------|-------|--------|")
        for i, f in enumerate(remaining, max_results + 1):
            title = f.get("title", "Untitled")[:60]
            score = f.get("composite_score", 0)
            source = f.get("source", "?")
            url = f.get("url", "")
            lines.append(f"| {i} | {score:.1f} | [{title}]({url}) | {source} |")
        lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*Generated by Opportunity Scout on {date_str} at {time_str} ET*")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate opportunity digest")
    parser.add_argument("scored", help="Path to scored findings JSON (or - for stdin)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--max-results", type=int, default=20,
                        help="Max top opportunities to show (default: 20)")

    args = parser.parse_args()

    # Load scored findings
    if args.scored == "-":
        scored = json.load(sys.stdin)
    else:
        with open(args.scored, "r") as f:
            scored = json.load(f)

    digest = generate_digest(scored, args.max_results)

    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w") as f:
            f.write(digest)
        print(f"Digest saved to {args.output}")
    else:
        print(digest)


if __name__ == "__main__":
    main()
