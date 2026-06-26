#!/usr/bin/env python3
"""Track opportunity signals over time and detect trend patterns.

Usage:
    history.py --update <scored.json>     Add scored findings to history
    history.py --trends                   Show persistent, emerging, and fading signals
    history.py --trends --format json     Machine-readable trend output
    history.py --timeline <topic>         Show timeline for a specific signal topic
    history.py --stats                    Show history statistics
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(SKILL_DIR, "history.json")


def load_history():
    """Load history.json or return empty structure."""
    if not os.path.exists(HISTORY_PATH):
        return {
            "version": 1,
            "scan_log": [],
            "signals": {},
        }
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "version": 1,
            "scan_log": [],
            "signals": {},
        }


def save_history(history):
    """Write history back to disk."""
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


def normalize_title(title):
    """Create a normalized key from a title for fuzzy matching across scans."""
    # Lowercase, remove punctuation, strip common words
    title = title.lower().strip()
    title = re.sub(r'[^\w\s]', '', title)
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "for", "to", "in",
                  "on", "of", "and", "or", "but", "with", "how", "what", "why",
                  "has", "anyone", "does", "do", "i", "my", "there", "this", "that",
                  "it", "be", "have", "can", "just", "so", "not", "any"}
    words = [w for w in title.split() if w not in stop_words and len(w) > 2]
    # Take up to 8 meaningful words as the key
    return " ".join(sorted(words[:8]))


def update_history(history, scored_findings):
    """Add scored findings to history, updating signal tracking."""
    scan_date = datetime.now().strftime("%Y-%m-%d")

    # Log the scan
    scan_entry = {
        "date": scan_date,
        "findings_count": len(scored_findings),
        "niches": list(set(f.get("niche", "") for f in scored_findings if f.get("niche"))),
    }
    history["scan_log"].append(scan_entry)

    # Process each finding
    for finding in scored_findings:
        title = finding.get("title", "")
        if not title:
            continue

        key = normalize_title(title)
        if not key:
            continue

        if key not in history["signals"]:
            history["signals"][key] = {
                "first_seen": scan_date,
                "last_seen": scan_date,
                "scan_dates": [scan_date],
                "titles": [title],
                "urls": [finding.get("url", "")],
                "niches": [finding.get("niche", "")],
                "peak_score": finding.get("composite_score", 0),
                "scores_over_time": [{
                    "date": scan_date,
                    "score": finding.get("composite_score", 0),
                }],
            }
        else:
            sig = history["signals"][key]
            sig["last_seen"] = scan_date

            # Only add scan_date if not already present (same-day re-scan)
            if scan_date not in sig["scan_dates"]:
                sig["scan_dates"].append(scan_date)

            # Track title variants
            if title not in sig["titles"]:
                sig["titles"].append(title)

            # Track URLs
            url = finding.get("url", "")
            if url and url not in sig["urls"]:
                sig["urls"].append(url)

            # Track niches
            niche = finding.get("niche", "")
            if niche and niche not in sig["niches"]:
                sig["niches"].append(niche)

            # Update peak score
            score = finding.get("composite_score", 0)
            sig["peak_score"] = max(sig["peak_score"], score)
            sig["scores_over_time"].append({
                "date": scan_date,
                "score": score,
            })

    return history


def classify_signal(sig):
    """Classify a signal as persistent, emerging, fading, or one-off."""
    scan_count = len(sig.get("scan_dates", []))
    scores = sig.get("scores_over_time", [])

    if scan_count >= 3:
        # Check if scores are declining
        if len(scores) >= 3:
            recent_avg = sum(s["score"] for s in scores[-2:]) / 2
            older_avg = sum(s["score"] for s in scores[:-2]) / max(len(scores) - 2, 1)
            if recent_avg < older_avg * 0.7:
                return "fading"
        return "persistent"
    elif scan_count == 1:
        return "emerging"
    elif scan_count == 2:
        # Check recency — if both scans are recent, emerging; if spread out, watch
        return "emerging"

    return "one-off"


def get_trends(history):
    """Analyze all signals and classify into trend categories."""
    trends = {
        "persistent": [],   # 3+ scans, stable or growing
        "emerging": [],      # 1-2 scans, new
        "fading": [],        # Was persistent, now declining
    }

    for key, sig in history.get("signals", {}).items():
        classification = classify_signal(sig)
        entry = {
            "topic": key,
            "titles": sig.get("titles", [])[:3],
            "first_seen": sig.get("first_seen", ""),
            "last_seen": sig.get("last_seen", ""),
            "scan_count": len(sig.get("scan_dates", [])),
            "peak_score": sig.get("peak_score", 0),
            "niches": sig.get("niches", []),
            "urls": sig.get("urls", [])[:3],
        }

        if classification in trends:
            trends[classification].append(entry)

    # Sort each category by peak score descending
    for cat in trends:
        trends[cat].sort(key=lambda x: x["peak_score"], reverse=True)

    return trends


def show_trends(history, output_format="text"):
    """Display trend analysis."""
    trends = get_trends(history)

    if output_format == "json":
        print(json.dumps(trends, indent=2))
        return

    total_signals = len(history.get("signals", {}))
    total_scans = len(history.get("scan_log", []))
    print(f"\n📊 Signal Trends ({total_signals} signals tracked across {total_scans} scans)\n")

    if trends["persistent"]:
        print("🔥 PERSISTENT SIGNALS (appearing 3+ scans — strong demand)")
        print("-" * 60)
        for s in trends["persistent"][:10]:
            title = s["titles"][0] if s["titles"] else s["topic"]
            print(f"  [{s['peak_score']:.1f}] {title}")
            print(f"       Seen {s['scan_count']}x | First: {s['first_seen']} | "
                  f"Niches: {', '.join(s['niches'][:3])}")
        print()

    if trends["emerging"]:
        print("🌱 EMERGING SIGNALS (new — watch these)")
        print("-" * 60)
        for s in trends["emerging"][:10]:
            title = s["titles"][0] if s["titles"] else s["topic"]
            print(f"  [{s['peak_score']:.1f}] {title}")
            print(f"       First seen: {s['first_seen']} | "
                  f"Niches: {', '.join(s['niches'][:3])}")
        print()

    if trends["fading"]:
        print("📉 FADING SIGNALS (declining — market may be filling)")
        print("-" * 60)
        for s in trends["fading"][:10]:
            title = s["titles"][0] if s["titles"] else s["topic"]
            print(f"  [{s['peak_score']:.1f}] {title}")
            print(f"       Seen {s['scan_count']}x | Last: {s['last_seen']}")
        print()

    if not any(trends.values()):
        print("No trend data yet. Run a few scans to build history.")


def show_timeline(history, topic):
    """Show timeline for a specific signal topic."""
    topic_lower = topic.lower()
    for key, sig in history.get("signals", {}).items():
        # Check if topic matches key or any title
        if (topic_lower in key or
                any(topic_lower in t.lower() for t in sig.get("titles", []))):
            print(f"\n📈 Timeline: {sig['titles'][0] if sig['titles'] else key}")
            print(f"   First seen: {sig['first_seen']}")
            print(f"   Last seen: {sig['last_seen']}")
            print(f"   Total appearances: {len(sig['scan_dates'])}")
            print(f"   Peak score: {sig['peak_score']:.1f}")
            print(f"   Status: {classify_signal(sig)}")
            print(f"\n   Score over time:")
            for entry in sig.get("scores_over_time", []):
                bar = "█" * int(entry["score"])
                print(f"     {entry['date']}: {entry['score']:.1f} {bar}")
            print(f"\n   URLs:")
            for url in sig.get("urls", [])[:5]:
                print(f"     {url}")
            return

    print(f"No signals found matching '{topic}'")


def show_stats(history):
    """Show history statistics."""
    signals = history.get("signals", {})
    scans = history.get("scan_log", [])

    print(f"\n📊 History Stats")
    print(f"   Total scans: {len(scans)}")
    print(f"   Total unique signals: {len(signals)}")

    if scans:
        print(f"   First scan: {scans[0].get('date', 'unknown')}")
        print(f"   Last scan: {scans[-1].get('date', 'unknown')}")

    if signals:
        classifications = {"persistent": 0, "emerging": 0, "fading": 0, "one-off": 0}
        for sig in signals.values():
            c = classify_signal(sig)
            classifications[c] = classifications.get(c, 0) + 1
        print(f"\n   Signal breakdown:")
        for c, count in sorted(classifications.items(), key=lambda x: -x[1]):
            print(f"     {c}: {count}")


def main():
    parser = argparse.ArgumentParser(description="Track opportunity signals over time")
    parser.add_argument("--update", metavar="FILE", help="Add scored findings to history")
    parser.add_argument("--trends", action="store_true", help="Show trend analysis")
    parser.add_argument("--timeline", metavar="TOPIC", help="Show timeline for a topic")
    parser.add_argument("--stats", action="store_true", help="Show history statistics")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="Output format for --trends")

    args = parser.parse_args()

    if not any([args.update, args.trends, args.timeline, args.stats]):
        parser.print_help()
        return

    history = load_history()

    if args.update:
        if args.update == "-":
            scored = json.load(sys.stdin)
        else:
            with open(args.update, "r") as f:
                scored = json.load(f)
        history = update_history(history, scored)
        save_history(history)
        print(f"History updated: {len(scored)} findings logged.")
        print(f"Total unique signals tracked: {len(history.get('signals', {}))}")

    if args.trends:
        show_trends(history, args.format)

    if args.timeline:
        show_timeline(history, args.timeline)

    if args.stats:
        show_stats(history)


if __name__ == "__main__":
    main()
