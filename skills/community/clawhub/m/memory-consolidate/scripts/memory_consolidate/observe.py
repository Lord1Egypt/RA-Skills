"""Memory observation: load current health + history, print concise report.

History is read from memory/structured/health_history.jsonl (appended by main.py
after each run), NOT from the cron run log.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


import os

WS = Path(os.environ.get("OPENCLAW_WORKSPACE", str(Path.home() / ".openclaw" / "workspace"))).resolve()
STRUCT = WS / 'memory' / 'structured'
HEALTH_HISTORY_PATH = STRUCT / 'health_history.jsonl'


def count_jsonl(path: Path) -> int:
    if not path.exists():
        return 0
    with path.open('r', encoding='utf-8') as f:
        return sum(1 for line in f if line.strip())


def load_current():
    health_path = STRUCT / 'health.json'
    health = json.loads(health_path.read_text(encoding='utf-8')) if health_path.exists() else {}
    return {
        'date': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
        'facts': count_jsonl(STRUCT / 'facts.jsonl'),
        'beliefs': count_jsonl(STRUCT / 'beliefs.jsonl'),
        'summaries': count_jsonl(STRUCT / 'summaries.jsonl'),
        'events': count_jsonl(STRUCT / 'events.jsonl'),
        'active_total': int(health.get('active_total', 0) or 0),
        'archived_total': int(health.get('archived_total', 0) or 0),
        'archive_ratio': float(health.get('archive_ratio', 0.0) or 0.0),
        'hot': int(health.get('hot', 0) or 0),
        'warm': int(health.get('warm', 0) or 0),
        'cold': int(health.get('cold', 0) or 0),
        'reinforced_count': int(health.get('reinforced_count', 0) or 0),
        'distilled_count': int(health.get('distilled_count', 0) or 0),
        'signal_noise_ratio': float(health.get('signal_noise_ratio', 0.0) or 0.0),
    }


def load_history():
    """Load history from health_history.jsonl (written by main.py after each run)."""
    rows = []
    if not HEALTH_HISTORY_PATH.exists():
        return rows
    with HEALTH_HISTORY_PATH.open('r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            run_at = obj.get('run_at') or obj.get('generated_at') or ''
            try:
                ts = datetime.fromisoformat(run_at.replace('Z', '+00:00')).timestamp()
            except Exception:
                ts = 0.0
            row = {
                'runAtMs': int(ts * 1000),
                'date': datetime.fromtimestamp(ts, tz=timezone.utc).strftime('%Y-%m-%d') if ts else '',
                'active_total': int(obj.get('active_total', 0) or 0),
                'archived_total': int(obj.get('archived_total', 0) or 0),
                'archive_ratio': float(obj.get('archive_ratio', 0.0) or 0.0),
                'hot': int(obj.get('hot', 0) or 0),
                'warm': int(obj.get('warm', 0) or 0),
                'cold': int(obj.get('cold', 0) or 0),
                'reinforced_count': int(obj.get('reinforced_count', 0) or 0),
                'distilled_count': int(obj.get('distilled_count', 0) or 0),
                'signal_noise_ratio': float(obj.get('signal_noise_ratio', 0.0) or 0.0),
                'facts': int(obj.get('facts', 0) or 0),
                'beliefs': int(obj.get('beliefs', 0) or 0),
                'summaries': int(obj.get('summaries', 0) or 0),
                'events': int(obj.get('events', 0) or 0),
            }
            if row['active_total'] > 0 or row['facts'] > 0:
                rows.append(row)
    rows.sort(key=lambda x: x['runAtMs'])
    return rows


def pct_change(curr, prev):
    if prev in (None, 0):
        return None
    return (curr - prev) / prev * 100.0


def status_good_watch_bad(value, good_cond, watch_cond):
    if good_cond(value):
        return 'good'
    if watch_cond(value):
        return 'watch'
    return 'bad'


def badge(status: str) -> str:
    return {
        'good': '🟢',
        'watch': '🟡',
        'bad': '🔴',
        'n/a': '⚪',
        'improving': '🟢',
        'observe': '🟡',
        'needs_tuning': '🔴',
    }.get(status, '⚪')


def label(status: str) -> str:
    return {
        'good': 'good',
        'watch': 'watch',
        'bad': 'bad',
        'n/a': 'n/a',
        'improving': 'improving',
        'observe': 'observe',
        'needs_tuning': 'needs_tuning',
    }.get(status, status)


def compute_summary():
    current = load_current()
    history = load_history()
    prev = history[-1] if history else None
    recent = history[-3:] if len(history) >= 3 else history[:]

    active_prev_pct = pct_change(current['active_total'], prev.get('active_total') if prev else None)
    facts_prev_pct = pct_change(current['facts'], prev.get('facts') if prev else None)

    baseline_active = min((r.get('active_total', current['active_total']) for r in recent), default=current['active_total'])
    active_vs_baseline_pct = pct_change(current['active_total'], baseline_active)

    active_status = status_good_watch_bad(
        current['active_total'],
        lambda v: v <= 1000,
        lambda v: v <= 1100,
    )
    if active_prev_pct is not None and active_prev_pct > 5:
        active_status = 'bad'
    elif active_prev_pct is not None and active_prev_pct > 2 and active_status == 'good':
        active_status = 'watch'

    archive_status = status_good_watch_bad(
        current['archive_ratio'],
        lambda v: v >= 0.03,
        lambda v: v >= 0.01,
    )

    snr_status = status_good_watch_bad(
        current['signal_noise_ratio'],
        lambda v: v >= 15,
        lambda v: v >= 8,
    )

    facts_status = status_good_watch_bad(
        facts_prev_pct if facts_prev_pct is not None else 0,
        lambda v: v <= 3,
        lambda v: v <= 8,
    )
    if prev is None:
        facts_status = 'n/a'

    if active_status == 'good' and archive_status in ('good', 'watch') and snr_status == 'good':
        verdict = 'improving'
    elif active_status == 'bad' or archive_status == 'bad' or snr_status == 'bad':
        verdict = 'needs_tuning'
    else:
        verdict = 'observe'

    return {
        'current': current,
        'recent': recent,
        'verdict': verdict,
        'active_status': active_status,
        'archive_status': archive_status,
        'snr_status': snr_status,
        'facts_status': facts_status,
        'active_prev_pct': active_prev_pct,
        'facts_prev_pct': facts_prev_pct,
        'active_vs_baseline_pct': active_vs_baseline_pct,
    }


def _fmt_pct(value, digits=1):
    if value is None:
        return 'n/a'
    return f'{value:+.{digits}f}%'


def print_brief(summary) -> None:
    current = summary['current']
    recent = summary['recent']
    verdict = summary['verdict']

    print(f"memory_observation: {badge(verdict)} {label(verdict)}")
    print(
        "  active/archive: "
        f"{current['active_total']} / {current['archived_total']} "
        f"(archive {badge(summary['archive_status'])} {current['archive_ratio']:.2%})"
    )
    print(
        "  items: "
        f"facts {current['facts']}, beliefs {current['beliefs']}, summaries {current['summaries']}, events {current['events']}"
    )
    print(
        "  quality: "
        f"snr {badge(summary['snr_status'])} {current['signal_noise_ratio']:.3f}; "
        f"facts_dod {badge(summary['facts_status'])} {_fmt_pct(summary['facts_prev_pct'])}"
    )
    print(
        "  temp: "
        f"hot={current['hot']}, warm={current['warm']}, cold={current['cold']}; "
        f"reinforced={current['reinforced_count']}, distilled={current['distilled_count']}"
    )
    print(
        "  drift: "
        f"active_vs_prev {badge(summary['active_status'])} {_fmt_pct(summary['active_prev_pct'])}; "
        f"vs_recent_min {_fmt_pct(summary['active_vs_baseline_pct'])}"
    )
    if recent:
        recent_dates = ', '.join(r['date'] for r in recent)
        print(f"  compared_runs: {recent_dates}")


def print_verbose(summary) -> None:
    current = summary['current']
    recent = summary['recent']
    verdict = summary['verdict']

    print('memory_observation:')
    print(f"  verdict: {badge(verdict)} {label(verdict)}")
    print('  thresholds:')
    print('    active_total: 🟢<=1000, 🟡<=1100, 🔴>1100 or day-over-day>5%')
    print('    archive_ratio: 🟢>=3%, 🟡>=1%, 🔴<1%')
    print('    signal_noise_ratio: 🟢>=15%, 🟡>=8%, 🔴<8%')
    print('    facts_growth_dod: 🟢<=3%, 🟡<=8%, 🔴>8%')
    print('  current:')
    print(f"    active_total: {badge(summary['active_status'])} {current['active_total']} ({label(summary['active_status'])})")
    if summary['active_prev_pct'] is not None:
        print(f"    active_total_vs_prev: {summary['active_prev_pct']:+.1f}%")
    if summary['active_vs_baseline_pct'] is not None:
        print(f"    active_total_vs_recent_min: {summary['active_vs_baseline_pct']:+.1f}%")
    print(f"    facts: {current['facts']}")
    if summary['facts_prev_pct'] is not None:
        print(f"    facts_vs_prev: {badge(summary['facts_status'])} {summary['facts_prev_pct']:+.1f}% ({label(summary['facts_status'])})")
    print(f"    events: {current['events']}")
    print(f"    summaries: {current['summaries']}")
    print(f"    archive_ratio: {badge(summary['archive_status'])} {current['archive_ratio']:.2%} ({label(summary['archive_status'])})")
    print(f"    signal_noise_ratio: {badge(summary['snr_status'])} {current['signal_noise_ratio']:.3f} ({label(summary['snr_status'])})")
    print(f"    reinforced_count: {current['reinforced_count']}")
    print(f"    distilled_count: {current['distilled_count']}")
    if recent:
        recent_dates = ', '.join(r['date'] for r in recent)
        print(f'  compared_runs: {recent_dates}')


def main(argv=None):
    parser = argparse.ArgumentParser(description='Print memory observation summary.')
    parser.add_argument('--verbose', action='store_true', help='Print the previous verbose report.')
    args = parser.parse_args(argv)

    summary = compute_summary()
    if args.verbose:
        print_verbose(summary)
    else:
        print_brief(summary)


if __name__ == '__main__':
    main()
