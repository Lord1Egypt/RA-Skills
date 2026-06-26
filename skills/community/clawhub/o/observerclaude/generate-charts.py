#!/usr/bin/env python3
"""
UxrObserver Chart Generator

Generates PNG chart images from UxrObserver observation data for inclusion in reports.
Uses matplotlib for rendering. Falls back to text-based charts if matplotlib is unavailable.

Usage:
    python generate-charts.py --data-dir ~/.uxr-observer --output-dir ~/.uxr-observer/reports/charts --start-date 2026-03-01 --end-date 2026-03-03

If matplotlib is not installed, run: pip install matplotlib
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter, defaultdict

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend for server/headless use
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not available. Charts will be generated as text tables.", file=sys.stderr)


def load_jsonl(filepath):
    """Load a JSONL file and return list of parsed records."""
    records = []
    if not os.path.exists(filepath):
        return records
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return records


def load_json(filepath):
    """Load a JSON file."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r') as f:
        return json.load(f)


def gather_data(data_dir, start_date, end_date):
    """Gather all observations and surveys within the date range."""
    observations = []
    surveys = []
    sessions_dir = Path(data_dir) / "sessions"

    if not sessions_dir.exists():
        return observations, surveys

    current = start_date
    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        day_dir = sessions_dir / date_str

        if day_dir.exists():
            obs_file = day_dir / "observations.jsonl"
            observations.extend(load_jsonl(str(obs_file)))

            survey_file = day_dir / "surveys.jsonl"
            surveys.extend(load_jsonl(str(survey_file)))

        current += timedelta(days=1)

    return observations, surveys


# ── Color palette ────────────────────────────────────────────────────────────

COLORS = {
    'primary': '#4A90D9',
    'success': '#27AE60',
    'warning': '#F2994A',
    'danger': '#EB5757',
    'neutral': '#828282',
    'delighted': '#27AE60',
    'positive': '#6FCF97',
    'frustrated': '#F2994A',
    'confused': '#F2C94C',
    'angry': '#EB5757',
    'resigned': '#828282',
}

SENTIMENT_COLORS = {
    'delighted': '#27AE60',
    'positive': '#6FCF97',
    'neutral': '#BDBDBD',
    'frustrated': '#F2994A',
    'confused': '#F2C94C',
    'angry': '#EB5757',
    'resigned': '#828282',
}

COMPLEXITY_COLORS = {
    'trivial': '#E0E0E0',
    'simple': '#90CAF9',
    'moderate': '#4A90D9',
    'complex': '#1565C0',
    'multi_session': '#0D47A1',
}


def chart_use_case_distribution(observations, output_dir):
    """Horizontal bar chart of use case frequency."""
    categories = Counter()
    for obs in observations:
        cat = obs.get('task', {}).get('category', 'other')
        categories[cat] += 1

    if not categories:
        return None

    sorted_cats = sorted(categories.items(), key=lambda x: x[1], reverse=True)
    labels = [c[0] for c in sorted_cats]
    values = [c[1] for c in sorted_cats]
    total = sum(values)

    fig, ax = plt.subplots(figsize=(10, max(4, len(labels) * 0.6)))
    bars = ax.barh(labels[::-1], values[::-1], color=COLORS['primary'], edgecolor='white')

    for bar, val in zip(bars, values[::-1]):
        pct = (val / total) * 100
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{val} ({pct:.0f}%)', va='center', fontsize=9)

    ax.set_xlabel('Number of Interactions')
    ax.set_title('Use Case Distribution', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'use-case-distribution.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def chart_satisfaction_trend(surveys, output_dir):
    """Line chart of satisfaction ratings over time."""
    ratings = []
    for s in surveys:
        if s.get('survey_type') == 'post_task' and not s.get('declined'):
            ts = s.get('timestamp', '')
            rating = s.get('responses', {}).get('experience_rating')
            if ts and rating is not None:
                try:
                    dt = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                    ratings.append((dt, rating))
                except (ValueError, TypeError):
                    continue

    if len(ratings) < 2:
        return None

    ratings.sort(key=lambda x: x[0])
    dates = [r[0] for r in ratings]
    values = [r[1] for r in ratings]

    # Rolling average (window of 3 or fewer)
    window = min(3, len(values))
    rolling = []
    for i in range(len(values)):
        start = max(0, i - window + 1)
        rolling.append(sum(values[start:i+1]) / (i - start + 1))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(dates, values, color=COLORS['primary'], alpha=0.5, s=40, zorder=3, label='Individual ratings')
    ax.plot(dates, rolling, color=COLORS['primary'], linewidth=2, zorder=4, label='Rolling average')
    ax.axhline(y=3, color=COLORS['neutral'], linestyle='--', alpha=0.5, label='Neutral (3.0)')

    ax.set_ylim(0.5, 5.5)
    ax.set_ylabel('Satisfaction Rating')
    ax.set_title('Satisfaction Trend Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='lower left')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    fig.autofmt_xdate()
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'satisfaction-trend.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def chart_failure_distribution(observations, output_dir):
    """Donut chart of failure types."""
    failures = Counter()
    no_failure = 0
    for obs in observations:
        outcome = obs.get('outcome', {})
        ftype = outcome.get('failure_type')
        if ftype:
            failures[ftype] += 1
        elif outcome.get('result') == 'success':
            no_failure += 1

    if not failures and no_failure == 0:
        return None

    labels = list(failures.keys())
    values = list(failures.values())
    if no_failure > 0:
        labels.append('no failures')
        values.append(no_failure)

    colors = []
    for label in labels:
        if label == 'no failures':
            colors.append(COLORS['success'])
        elif label in ('hallucination', 'loop', 'critical'):
            colors.append(COLORS['danger'])
        else:
            colors.append(COLORS['warning'])

    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.0f%%',
        colors=colors, pctdistance=0.8, startangle=90
    )
    centre = plt.Circle((0, 0), 0.50, fc='white')
    ax.add_artist(centre)
    ax.set_title('Failure Type Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'failure-distribution.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def chart_sentiment_distribution(observations, output_dir):
    """Stacked bar chart of sentiment by date."""
    daily_sentiment = defaultdict(lambda: Counter())
    for obs in observations:
        ts = obs.get('timestamp', '')
        sentiment = obs.get('user', {}).get('sentiment', 'neutral')
        # Handle compound sentiments like "frustrated_then_positive"
        if '_then_' in sentiment:
            sentiment = sentiment.split('_then_')[-1]
        try:
            date = ts[:10]
            if date:
                daily_sentiment[date][sentiment] += 1
        except (IndexError, TypeError):
            continue

    if not daily_sentiment:
        return None

    dates = sorted(daily_sentiment.keys())
    sentiments = ['delighted', 'positive', 'neutral', 'frustrated', 'confused', 'angry', 'resigned']

    fig, ax = plt.subplots(figsize=(10, 5))
    bottom = [0] * len(dates)

    for sentiment in sentiments:
        values = [daily_sentiment[d].get(sentiment, 0) for d in dates]
        color = SENTIMENT_COLORS.get(sentiment, COLORS['neutral'])
        ax.bar(dates, values, bottom=bottom, label=sentiment, color=color, edgecolor='white', linewidth=0.5)
        bottom = [b + v for b, v in zip(bottom, values)]

    ax.set_ylabel('Number of Interactions')
    ax.set_title('Sentiment Distribution', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'sentiment-distribution.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def chart_cost_over_time(observations, output_dir):
    """Area chart of estimated cost over time."""
    daily_cost = defaultdict(lambda: {'input': 0, 'output': 0, 'tool': 0})
    for obs in observations:
        ts = obs.get('timestamp', '')
        infra = obs.get('infrastructure', {})
        date = ts[:10] if ts else None
        if not date:
            continue

        input_tokens = infra.get('estimated_input_tokens', 0)
        output_tokens = infra.get('estimated_output_tokens', 0)
        # Rough cost split: attribute tool overhead proportionally
        total_cost = infra.get('estimated_cost_usd', 0)
        if total_cost > 0:
            daily_cost[date]['input'] += total_cost * 0.3
            daily_cost[date]['output'] += total_cost * 0.6
            daily_cost[date]['tool'] += total_cost * 0.1

    if not daily_cost:
        return None

    dates = sorted(daily_cost.keys())
    input_costs = [daily_cost[d]['input'] for d in dates]
    output_costs = [daily_cost[d]['output'] for d in dates]
    tool_costs = [daily_cost[d]['tool'] for d in dates]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.stackplot(dates, input_costs, output_costs, tool_costs,
                 labels=['Input tokens', 'Output tokens', 'Tool overhead'],
                 colors=[COLORS['primary'], COLORS['success'], COLORS['warning']],
                 alpha=0.7)

    # Cumulative line
    cumulative = []
    running = 0
    for d in dates:
        running += daily_cost[d]['input'] + daily_cost[d]['output'] + daily_cost[d]['tool']
        cumulative.append(running)

    ax2 = ax.twinx()
    ax2.plot(dates, cumulative, color=COLORS['danger'], linewidth=2, linestyle='--', label='Cumulative')
    ax2.set_ylabel('Cumulative Cost ($)')

    ax.set_ylabel('Daily Estimated Cost ($)')
    ax.set_title('Estimated API Cost Over Time', fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize=8)
    ax2.legend(loc='upper right', fontsize=8)
    ax.spines['top'].set_visible(False)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'cost-over-time.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def chart_tool_usage(observations, output_dir):
    """Horizontal bar chart of tool usage frequency."""
    tools = Counter()
    for obs in observations:
        for tool in obs.get('openclaw', {}).get('tools_used', []):
            tools[tool] += 1

    if not tools:
        return None

    sorted_tools = sorted(tools.items(), key=lambda x: x[1], reverse=True)[:15]
    labels = [t[0] for t in sorted_tools]
    values = [t[1] for t in sorted_tools]

    fig, ax = plt.subplots(figsize=(10, max(4, len(labels) * 0.5)))
    ax.barh(labels[::-1], values[::-1], color=COLORS['success'], edgecolor='white')

    for i, (label, val) in enumerate(zip(labels[::-1], values[::-1])):
        ax.text(val + 0.3, i, str(val), va='center', fontsize=9)

    ax.set_xlabel('Number of Uses')
    ax.set_title('Tool Usage Frequency', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'tool-usage.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def chart_complexity_distribution(observations, output_dir):
    """Bar chart of task complexity."""
    complexities = Counter()
    for obs in observations:
        c = obs.get('task', {}).get('complexity', 'unknown')
        complexities[c] += 1

    if not complexities:
        return None

    order = ['trivial', 'simple', 'moderate', 'complex', 'multi_session']
    labels = [c for c in order if c in complexities]
    values = [complexities[c] for c in labels]
    colors = [COMPLEXITY_COLORS.get(c, COLORS['neutral']) for c in labels]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, values, color=colors, edgecolor='white')

    for i, val in enumerate(values):
        ax.text(i, val + 0.2, str(val), ha='center', fontsize=10)

    ax.set_ylabel('Number of Tasks')
    ax.set_title('Task Complexity Distribution', fontsize=14, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    filepath = os.path.join(output_dir, 'complexity-distribution.png')
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filepath


def generate_text_fallback(observations, surveys, output_dir):
    """Generate text-based chart alternatives when matplotlib is unavailable."""
    output = []
    output.append("=" * 60)
    output.append("UXROBSERVER TEXT CHARTS (matplotlib unavailable)")
    output.append("=" * 60)

    # Use case distribution
    categories = Counter()
    for obs in observations:
        cat = obs.get('task', {}).get('category', 'other')
        categories[cat] += 1

    if categories:
        output.append("\n--- Use Case Distribution ---")
        total = sum(categories.values())
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            bar_len = int((count / total) * 40)
            pct = (count / total) * 100
            output.append(f"  {cat:20s} {'█' * bar_len} {count} ({pct:.0f}%)")

    # Sentiment distribution
    sentiments = Counter()
    for obs in observations:
        s = obs.get('user', {}).get('sentiment', 'neutral')
        sentiments[s] += 1

    if sentiments:
        output.append("\n--- Sentiment Distribution ---")
        total = sum(sentiments.values())
        for sent, count in sorted(sentiments.items(), key=lambda x: -x[1]):
            bar_len = int((count / total) * 40)
            output.append(f"  {sent:20s} {'█' * bar_len} {count}")

    text = "\n".join(output)
    filepath = os.path.join(output_dir, 'text-charts.txt')
    with open(filepath, 'w') as f:
        f.write(text)
    return filepath


def main():
    parser = argparse.ArgumentParser(description='Generate UxrObserver report charts')
    parser.add_argument('--data-dir', default=os.path.expanduser('~/.uxr-observer'),
                        help='Path to UxrObserver data directory')
    parser.add_argument('--output-dir', default=None,
                        help='Output directory for chart images')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = os.path.join(args.data_dir, 'reports', 'charts')

    os.makedirs(args.output_dir, exist_ok=True)

    start = datetime.strptime(args.start_date, '%Y-%m-%d')
    end = datetime.strptime(args.end_date, '%Y-%m-%d')

    print(f"Gathering data from {args.start_date} to {args.end_date}...")
    observations, surveys = gather_data(args.data_dir, start, end)
    print(f"Found {len(observations)} observations and {len(surveys)} survey responses.")

    if not HAS_MATPLOTLIB:
        filepath = generate_text_fallback(observations, surveys, args.output_dir)
        print(f"Text charts saved to: {filepath}")
        return

    generated = []

    print("Generating charts...")
    charts = [
        ("Use case distribution", chart_use_case_distribution, observations),
        ("Satisfaction trend", chart_satisfaction_trend, surveys),
        ("Failure distribution", chart_failure_distribution, observations),
        ("Sentiment distribution", chart_sentiment_distribution, observations),
        ("Cost over time", chart_cost_over_time, observations),
        ("Tool usage", chart_tool_usage, observations),
        ("Complexity distribution", chart_complexity_distribution, observations),
    ]

    for name, func, data in charts:
        try:
            result = func(data, args.output_dir)
            if result:
                generated.append(result)
                print(f"  ✓ {name}: {result}")
            else:
                print(f"  ⊘ {name}: insufficient data")
        except Exception as e:
            print(f"  ✗ {name}: error - {e}", file=sys.stderr)

    print(f"\nGenerated {len(generated)} charts in {args.output_dir}")


if __name__ == '__main__':
    main()
