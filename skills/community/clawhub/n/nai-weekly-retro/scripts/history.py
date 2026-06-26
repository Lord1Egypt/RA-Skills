#!/usr/bin/env python3
"""
history.py — Track retrospective history for longitudinal analysis.

Maintains a JSON log of past retros: date ranges, scores, key findings,
recommendations, and whether recommendations were acted on.

Usage:
    python3 history.py record --analysis analysis.json [--history PATH]
    python3 history.py show [--history PATH]
    python3 history.py mark-addressed --recommendation "text" [--history PATH]
    python3 history.py trends [--history PATH]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


DEFAULT_HISTORY_PATH = os.path.expanduser(
    '~/.openclaw/workspace/skills/weekly-retro/history.json'
)


def load_history(path):
    """Load or initialize history file."""
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            # Ensure expected structure
            if 'retros' not in data:
                data['retros'] = []
            if 'meta' not in data:
                data['meta'] = {'created': datetime.now().isoformat()}
            return data
        except (json.JSONDecodeError, KeyError):
            return _new_history()
    return _new_history()


def _new_history():
    return {
        'meta': {
            'created': datetime.now().isoformat(),
            'schema_version': 1,
        },
        'retros': [],
    }


def save_history(data, path):
    """Write history to disk."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data['meta']['last_updated'] = datetime.now().isoformat()
    with open(path, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"History saved to: {path}", file=sys.stderr)


def record_retro(analysis_path, history_path):
    """Record a new retrospective entry from analysis JSON."""
    with open(analysis_path, 'r') as f:
        analysis = json.load(f)

    history = load_history(history_path)

    meta = analysis.get('meta', {})
    start_date = meta.get('start_date', '')
    end_date = meta.get('end_date', '')

    # Check for duplicate (same date range)
    for existing in history['retros']:
        if existing.get('date_start') == start_date and existing.get('date_end') == end_date:
            print(f"Retro for {start_date} to {end_date} already recorded. Updating.", file=sys.stderr)
            history['retros'].remove(existing)
            break

    # Extract key data for the history entry
    accomplishments = analysis.get('accomplishments', [])
    failures = analysis.get('failures', [])
    unfinished = analysis.get('unfinished', [])
    formalization = analysis.get('formalization_candidates', [])
    time_sinks = analysis.get('time_sinks', [])
    recurring_themes = analysis.get('recurring_themes', [])

    # Build compact history entry
    entry = {
        'date_start': start_date,
        'date_end': end_date,
        'recorded_at': datetime.now().isoformat(),
        'week_score': analysis.get('suggested_week_score', None),
        'active_days': analysis.get('summary_stats', {}).get('active_days', 0),
        'key_topics': [t['topic'] for t in recurring_themes[:10]],
        'accomplishment_summary': [
            {'label': a['label'], 'count': a['count']}
            for a in accomplishments[:8]
        ],
        'friction_points': [
            {'label': f['label'], 'count': f['count'], 'repeated': f.get('repeated', False)}
            for f in failures if f['count'] >= 2 or f.get('repeated')
        ],
        'unfinished_count': len(unfinished),
        'unfinished_items': [u['text'][:100] for u in unfinished[:5]],
        'top_time_sink': time_sinks[0]['topic'] if time_sinks else None,
        'top_time_sink_share': time_sinks[0]['content_share'] if time_sinks else None,
        'formalization_candidates': [
            {'topic': fc['topic'], 'reason': fc['reason'][:100]}
            for fc in formalization[:3]
        ],
        'recommendations': [],  # Filled below
    }

    # Extract recommendations — we need to regenerate them from the analysis
    # Since retrospective.py generates them, we'll extract the key info
    recs = _extract_recommendations(analysis)
    entry['recommendations'] = recs

    history['retros'].append(entry)

    # Sort by date
    history['retros'].sort(key=lambda x: x.get('date_end', ''))

    save_history(history, history_path)
    print(f"Recorded retro for {start_date} to {end_date} (score: {entry['week_score']})", file=sys.stderr)

    return entry


def _extract_recommendations(analysis):
    """Extract recommendation entries for history tracking."""
    # Re-derive recommendations using same logic as retrospective.py
    recs = []
    failures = analysis.get('failures', [])
    unfinished = analysis.get('unfinished', [])
    formalization = analysis.get('formalization_candidates', [])
    time_patterns = analysis.get('summary_stats', {}).get('time_patterns', {})
    time_sinks = analysis.get('time_sinks', [])

    repeated = [f for f in failures if f.get('repeated')]
    if repeated:
        recs.append({
            'text': f"Address recurring {repeated[0]['label'].lower()}",
            'source': 'repeated_failure',
            'addressed': False,
        })

    if len(unfinished) > 3:
        recs.append({
            'text': f"Clear the backlog ({len(unfinished)} open threads)",
            'source': 'unfinished_threads',
            'addressed': False,
        })

    if formalization:
        recs.append({
            'text': f"Formalize the {formalization[0]['topic']} workflow",
            'source': 'formalization',
            'addressed': False,
        })

    if time_patterns.get('late_night', 0) >= 2:
        recs.append({
            'text': 'Watch the late-night pattern — batch complex work for mornings',
            'source': 'time_pattern',
            'addressed': False,
        })

    if time_sinks and time_sinks[0]['content_share'] > 0.35:
        recs.append({
            'text': f"Diversify focus — {time_sinks[0]['topic']} consumed {time_sinks[0]['content_share']*100:.0f}% of attention",
            'source': 'time_sink',
            'addressed': False,
        })

    return recs[:3]


def mark_addressed(recommendation_text, history_path):
    """Mark a recommendation as addressed."""
    history = load_history(history_path)

    found = False
    for retro in reversed(history['retros']):
        for rec in retro.get('recommendations', []):
            if recommendation_text.lower() in rec.get('text', '').lower():
                rec['addressed'] = True
                rec['addressed_at'] = datetime.now().isoformat()
                found = True
                print(f"Marked as addressed: \"{rec['text']}\" (from {retro['date_start']} to {retro['date_end']})", file=sys.stderr)
                break
        if found:
            break

    if not found:
        print(f"No matching recommendation found for: \"{recommendation_text}\"", file=sys.stderr)
        sys.exit(1)

    save_history(history, history_path)


def show_history(history_path):
    """Display history summary."""
    history = load_history(history_path)
    retros = history.get('retros', [])

    if not retros:
        print("No retrospective history yet.")
        return

    print(f"=== Retrospective History ({len(retros)} entries) ===\n")

    for retro in retros:
        score = retro.get('week_score', '?')
        start = retro.get('date_start', '?')
        end = retro.get('date_end', '?')
        active = retro.get('active_days', '?')
        sink = retro.get('top_time_sink', 'N/A')

        print(f"📅 {start} to {end}  |  Score: {score}/10  |  Active days: {active}  |  Focus: {sink}")

        # Accomplishments
        accs = retro.get('accomplishment_summary', [])
        if accs:
            acc_str = ', '.join(f"{a['label']} ({a['count']})" for a in accs[:4])
            print(f"   ✅ {acc_str}")

        # Friction
        friction = retro.get('friction_points', [])
        if friction:
            fric_str = ', '.join(f['label'] for f in friction[:3])
            print(f"   ⚠️  Friction: {fric_str}")

        # Recommendations
        recs = retro.get('recommendations', [])
        for rec in recs:
            status = '✅' if rec.get('addressed') else '⬜'
            print(f"   {status} {rec['text']}")

        print()


def show_trends(history_path):
    """Display longitudinal trends."""
    history = load_history(history_path)
    retros = history.get('retros', [])

    if len(retros) < 2:
        print("Need at least 2 retros for trend analysis.")
        return

    print("=== Longitudinal Trends ===\n")

    # Score trend
    scores = [(r['date_end'], r.get('week_score', 0)) for r in retros if r.get('week_score')]
    if scores:
        print("📊 Score History:")
        for date, score in scores:
            bar = '█' * score + '░' * (10 - score)
            print(f"   {date}: [{bar}] {score}/10")
        avg = sum(s for _, s in scores) / len(scores)
        print(f"   Average: {avg:.1f}/10")
        if len(scores) >= 3:
            recent_avg = sum(s for _, s in scores[-3:]) / 3
            older_avg = sum(s for _, s in scores[:-3]) / max(len(scores) - 3, 1) if len(scores) > 3 else scores[0][1]
            if recent_avg > older_avg + 0.5:
                print("   📈 Trend: Improving")
            elif recent_avg < older_avg - 0.5:
                print("   📉 Trend: Declining")
            else:
                print("   ➡️  Trend: Stable")
        print()

    # Persistent friction
    from collections import Counter
    friction_counter = Counter()
    for retro in retros:
        for fp in retro.get('friction_points', []):
            friction_counter[fp['label']] += 1

    persistent = [(label, count) for label, count in friction_counter.items() if count >= 2]
    if persistent:
        print("🔁 Persistent Friction (2+ weeks):")
        for label, count in sorted(persistent, key=lambda x: x[1], reverse=True):
            print(f"   ⚠️  {label} — {count} weeks")
        print()

    # Recommendation follow-through
    total_recs = 0
    addressed_recs = 0
    for retro in retros:
        for rec in retro.get('recommendations', []):
            total_recs += 1
            if rec.get('addressed'):
                addressed_recs += 1

    if total_recs > 0:
        rate = addressed_recs / total_recs * 100
        print(f"📋 Recommendation Follow-Through: {addressed_recs}/{total_recs} ({rate:.0f}%)")
        if rate < 30:
            print("   ⚠️  Low follow-through — recommendations may need to be more actionable")
        elif rate > 70:
            print("   ✅ Strong follow-through")
        print()

    # Topic evolution
    all_topics = {}
    for i, retro in enumerate(retros):
        for topic in retro.get('key_topics', []):
            if topic not in all_topics:
                all_topics[topic] = []
            all_topics[topic].append(i)

    evolving = [(t, weeks) for t, weeks in all_topics.items() if len(weeks) >= 2]
    if evolving:
        print("🔄 Recurring Topics Across Weeks:")
        for topic, weeks in sorted(evolving, key=lambda x: len(x[1]), reverse=True)[:8]:
            print(f"   {topic} — appeared in {len(weeks)} retros")
        print()


def main():
    parser = argparse.ArgumentParser(description='Manage retrospective history')
    subparsers = parser.add_subparsers(dest='command', help='Command')

    # record
    record_parser = subparsers.add_parser('record', help='Record a new retro from analysis JSON')
    record_parser.add_argument('--analysis', required=True, help='Path to analysis JSON')
    record_parser.add_argument('--history', default=None, help='Path to history file')

    # show
    show_parser = subparsers.add_parser('show', help='Display history summary')
    show_parser.add_argument('--history', default=None, help='Path to history file')

    # mark-addressed
    mark_parser = subparsers.add_parser('mark-addressed', help='Mark a recommendation as addressed')
    mark_parser.add_argument('--recommendation', required=True, help='Text of the recommendation')
    mark_parser.add_argument('--history', default=None, help='Path to history file')

    # trends
    trends_parser = subparsers.add_parser('trends', help='Display longitudinal trends')
    trends_parser.add_argument('--history', default=None, help='Path to history file')

    args = parser.parse_args()

    # Resolve history path
    config_path = os.environ.get('WEEKLY_RETRO_CONFIG', '')
    config = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

    history_path = getattr(args, 'history', None) or config.get('history_file', DEFAULT_HISTORY_PATH)

    if args.command == 'record':
        record_retro(args.analysis, history_path)
    elif args.command == 'show':
        show_history(history_path)
    elif args.command == 'mark-addressed':
        mark_addressed(args.recommendation, history_path)
    elif args.command == 'trends':
        show_trends(history_path)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
