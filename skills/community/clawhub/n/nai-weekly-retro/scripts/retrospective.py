#!/usr/bin/env python3
"""
retrospective.py — Generate a markdown retrospective from analysis JSON.

Takes analysis output (from analyze.py), produces a beautiful markdown document
suitable for Obsidian with YAML frontmatter, forward-looking recommendations,
and longitudinal context when history exists.

Usage:
    python3 analyze.py [...] | python3 retrospective.py [--output PATH]
    python3 retrospective.py --input analysis.json [--output PATH]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_stdin_or_file(input_path):
    """Read analysis data from stdin or file."""
    if input_path:
        with open(input_path, 'r') as f:
            return json.load(f)
    else:
        return json.load(sys.stdin)


def auto_tags(analysis):
    """Generate tags from analysis content."""
    tags = ['weekly-retro']

    # Add tags from top accomplishment clusters
    for acc in analysis.get('accomplishments', [])[:5]:
        label = acc['label'].lower().replace(' ', '-')
        if label != 'other':
            tags.append(label)

    # Add tags from recurring themes
    for theme in analysis.get('recurring_themes', [])[:3]:
        topic = theme['topic'].lower().replace(' ', '-').replace('(', '').replace(')', '')
        if topic not in tags:
            tags.append(topic)

    # Add time pattern tags
    time_patterns = analysis.get('summary_stats', {}).get('time_patterns', {})
    if time_patterns.get('late_night', 0) >= 2:
        tags.append('late-night-sessions')

    return tags


def format_frontmatter(analysis, tags):
    """Generate YAML frontmatter."""
    meta = analysis.get('meta', {})
    start = meta.get('start_date', 'unknown')
    end = meta.get('end_date', 'unknown')
    score = analysis.get('suggested_week_score', '?')

    lines = [
        '---',
        f'date_start: {start}',
        f'date_end: {end}',
        'type: weekly-retro',
        f'week_score: {score}',
        f'tags: [{", ".join(tags)}]',
        '---',
    ]
    return '\n'.join(lines)


def format_week_at_a_glance(analysis):
    """Generate the 3-sentence week summary."""
    stats = analysis.get('summary_stats', {})
    accomplishments = analysis.get('accomplishments', [])
    failures = analysis.get('failures', [])
    time_sinks = analysis.get('time_sinks', [])
    active_days = stats.get('active_days', 0)
    total_days = stats.get('total_days', 7)

    # Determine the dominant thrust — skip meta-topics like "Daily Recap"
    skip_topics = {'Daily Recap', 'daily-recap', 'End of Day'}
    top_topics = [s for s in sorted(time_sinks, key=lambda x: x['content_share'], reverse=True)
                  if s['topic'] not in skip_topics]
    dominant = top_topics[0]['topic'] if top_topics else 'various projects'

    # Count accomplishment items
    total_wins = sum(a['count'] for a in accomplishments)
    win_areas = len(accomplishments)

    # Sentence 1: What dominated
    s1 = f"This was a {active_days}-day week dominated by {dominant}"
    if len(top_topics) > 1:
        s1 += f" alongside {top_topics[1]['topic']}"
    s1 += '.'

    # Sentence 2: What was accomplished
    if total_wins > 15:
        s2 = f"Massive output — {total_wins} accomplishments across {win_areas} areas, with significant shipping and deployment."
    elif total_wins > 8:
        s2 = f"Strong output with {total_wins} accomplishments across {win_areas} areas."
    elif total_wins > 3:
        s2 = f"Moderate output — {total_wins} accomplishments, mostly concentrated in a few areas."
    else:
        s2 = f"Light output with {total_wins} notable accomplishments."

    # Sentence 3: Forward-looking
    unfinished = analysis.get('unfinished', [])
    if len(unfinished) > 5:
        s3 = f"Heading into next week with {len(unfinished)} open threads — prioritization will be key."
    elif failures and any(f.get('repeated') for f in failures):
        s3 = "Some recurring issues need addressing before they become structural."
    else:
        s3 = "Good momentum to carry into next week."

    return f"{s1} {s2} {s3}"


def format_wins(accomplishments):
    """Format the Wins section."""
    if not accomplishments:
        return "*No major wins identified this week.*"

    lines = []
    # Show substantial clusters (3+ items) with full evidence
    major = [a for a in accomplishments if a['count'] >= 3]
    minor = [a for a in accomplishments if a['count'] < 3 and a['label'] not in ('Uncategorized',)]

    for acc in major:
        dates_str = ', '.join(acc['dates'])
        lines.append(f"**{acc['label']}** ({acc['count']} items, {dates_str})")
        for ev in acc['evidence'][:3]:
            lines.append(f"  - {ev}")
        lines.append('')

    # Consolidate small clusters into a compact "Also shipped" section
    if minor:
        lines.append("**Also shipped:**")
        for acc in minor:
            # Single best evidence line per minor cluster
            ev = acc['evidence'][0] if acc['evidence'] else acc['label']
            lines.append(f"  - **{acc['label']}**: {ev}")
        lines.append('')

    return '\n'.join(lines).strip() if lines else "*No major wins identified.*"


def format_patterns(recurring_themes, time_sinks, time_patterns):
    """Format the Patterns section."""
    lines = []

    # Recurring topic themes (not tool mentions — those are noise)
    topic_themes = [t for t in recurring_themes if t.get('type') != 'tool']
    if topic_themes:
        lines.append("**Recurring topics:**")
        for theme in topic_themes[:6]:
            topic = theme['topic']
            days = theme['day_count']
            if theme.get('dates'):
                date_str = ', '.join(theme['dates'][:5])
                lines.append(f"  - **{topic}** — {days} days ({date_str})")
            else:
                lines.append(f"  - **{topic}** — {days} days")
        lines.append('')

    # Top tools (condensed — one line, not per-tool)
    tool_themes = [t for t in recurring_themes if t.get('type') == 'tool' and t['day_count'] >= 4]
    if tool_themes:
        tool_str = ', '.join(f"{t['topic'].replace(' (tool usage)', '')} ({t['day_count']}d)" for t in tool_themes[:6])
        lines.append(f"**Core toolchain this week:** {tool_str}")
        lines.append('')

    # Time-of-day patterns
    if time_patterns:
        active_times = sorted(time_patterns.items(), key=lambda x: x[1], reverse=True)
        time_desc = ', '.join(f"{t.replace('_', ' ')} ({c}d)" for t, c in active_times)
        lines.append(f"**Work schedule:** {time_desc}")
        if time_patterns.get('late_night', 0) >= 2:
            lines.append("  - ⚠️ Late-night sessions on {0} days — sustainability concern".format(
                time_patterns['late_night']
            ))
        lines.append('')

    # Attention distribution — the real insight
    major_sinks = [s for s in time_sinks if s['content_share'] > 0.03]
    if major_sinks:
        lines.append("**Where attention went:**")
        for sink in major_sinks[:6]:
            pct = sink['content_share'] * 100
            bar_len = int(pct / 5)  # Scale to ~20 chars max
            bar = '█' * bar_len + '░' * (20 - bar_len)
            lines.append(f"  - {sink['topic']}: `{bar}` {pct:.0f}%")
        lines.append('')

    return '\n'.join(lines).strip() if lines else "*No strong patterns detected.*"


def format_friction(failures):
    """Format the Friction Points section."""
    if not failures:
        return "*No significant friction points this week.*"

    lines = []
    shown = 0
    for f in failures:
        if shown >= 5:
            break
        if f['count'] < 2 and not f.get('repeated'):
            continue
        repeat_marker = ' 🔁' if f.get('repeated') else ''
        dates_str = ', '.join(f['dates'])
        lines.append(f"**{f['label']}**{repeat_marker}")
        if f.get('repeated'):
            lines.append(f"  - Appeared on {dates_str} — recurring pattern")
        for ev in f['evidence'][:2]:
            lines.append(f"  - {ev}")
        lines.append('')
        shown += 1

    # Include single-occurrence but notable failures if nothing shown yet
    if not lines:
        for f in failures[:3]:
            lines.append(f"**{f['label']}**")
            for ev in f['evidence'][:2]:
                lines.append(f"  - {ev}")
            lines.append('')

    return '\n'.join(lines).strip() if lines else "*No significant friction points.*"


def format_unfinished(unfinished):
    """Format the Unfinished Business section."""
    if not unfinished:
        return "*All threads appear resolved. Clean slate heading into next week.*"

    lines = []
    # Group by date
    by_date = {}
    for item in unfinished:
        d = item.get('date', 'unknown')
        if d not in by_date:
            by_date[d] = []
        by_date[d].append(item['text'])

    for date in sorted(by_date.keys()):
        lines.append(f"**From {date}:**")
        for text in by_date[date][:5]:
            lines.append(f"  - {text}")
        lines.append('')

    return '\n'.join(lines).strip()


def generate_recommendations(analysis):
    """Generate 2-3 specific, actionable recommendations."""
    recs = []
    failures = analysis.get('failures', [])
    unfinished = analysis.get('unfinished', [])
    time_sinks = analysis.get('time_sinks', [])
    formalization = analysis.get('formalization_candidates', [])
    time_patterns = analysis.get('summary_stats', {}).get('time_patterns', {})
    pattern_shifts = analysis.get('pattern_shifts', {})

    # Recommendation from repeated failures (skip vague labels)
    repeated = [f for f in failures if f.get('repeated') and f['label'].lower() not in ('miscellaneous friction', 'general bugs')]
    if repeated:
        top_failure = repeated[0]
        top_evidence = top_failure['evidence'][0] if top_failure['evidence'] else 'multiple issues'
        label = top_failure['label']
        dates = ', '.join(top_failure['dates'])

        # Customize advice based on failure type
        if 'rate limit' in label.lower():
            advice = (f"**Mitigate {label.lower()}** — Hit on {dates}. "
                      f"Consider batching heavy coding sessions, scheduling Claude Code work "
                      f"for off-peak hours, or splitting tasks across sessions to avoid hitting limits mid-flow.")
        else:
            advice = (f"**Fix {label}** — Appeared on {dates}. "
                      f"Root cause: {top_evidence[:120]}. "
                      f"Invest time to fix the underlying issue rather than patching repeatedly.")

        recs.append({
            'text': advice,
            'source': 'repeated_failure',
            'evidence': top_failure['evidence'][:2],
        })

    # Recommendation from unfinished threads
    if len(unfinished) > 3:
        recs.append({
            'text': f"**Clear the backlog** — {len(unfinished)} open threads carried over. "
                    f"Before starting new work next week, triage these: keep what's still relevant, drop what's stale, schedule what matters.",
            'source': 'unfinished_threads',
            'evidence': [u['text'] for u in unfinished[:3]],
        })

    # Recommendation from formalization candidates
    if formalization:
        top_candidate = formalization[0]
        recs.append({
            'text': f"**Formalize the {top_candidate['topic']} workflow** — {top_candidate['reason']}. "
                    f"Writing it down once prevents re-deciding it every session.",
            'source': 'formalization',
            'evidence': [],
        })

    # Recommendation from time patterns
    if time_patterns.get('late_night', 0) >= 2:
        recs.append({
            'text': "**Watch the late-night pattern** — Multiple sessions ran past midnight this week. "
                    "High-quality decisions and code reviews are harder when fatigued. "
                    "Consider batching complex work for morning sessions.",
            'source': 'time_pattern',
            'evidence': [],
        })

    # Recommendation from unaddressed prior recommendations
    unaddressed = pattern_shifts.get('unaddressed_recommendations', [])
    if unaddressed:
        rec = unaddressed[0]
        recs.append({
            'text': f"**Revisit prior recommendation** — \"{rec['recommendation']}\" was suggested "
                    f"{rec.get('weeks_ago', '?')} weeks ago but hasn't been addressed. "
                    f"Either do it, delegate it, or explicitly drop it.",
            'source': 'unaddressed_prior',
            'evidence': [],
        })

    # Recommendation from dominant time sink
    if time_sinks and time_sinks[0]['content_share'] > 0.35:
        sink = time_sinks[0]
        recs.append({
            'text': f"**Diversify focus** — {sink['topic']} consumed {sink['content_share']*100:.0f}% of this week's attention. "
                    f"Consider whether that concentration was intentional or a sign of scope creep.",
            'source': 'time_sink',
            'evidence': [],
        })

    # Take best 3
    return recs[:3]


def format_recommendations(recs):
    """Format recommendations as numbered list."""
    if not recs:
        return "*No specific recommendations — solid week across the board.*"

    lines = []
    for i, rec in enumerate(recs, 1):
        lines.append(f"{i}. {rec['text']}")
        if rec.get('evidence'):
            for ev in rec['evidence'][:2]:
                lines.append(f"   - _{ev}_")
        lines.append('')

    return '\n'.join(lines).strip()


def format_week_score(score, analysis):
    """Format the Week Score section with justification."""
    stats = analysis.get('summary_stats', {})
    accomplishments = analysis.get('accomplishments', [])
    failures = analysis.get('failures', [])
    active_days = stats.get('active_days', 0)

    total_wins = sum(a['count'] for a in accomplishments)
    repeated_failures = sum(1 for f in failures if f.get('repeated'))

    # Build justification
    parts = []
    if total_wins > 15:
        parts.append(f"exceptional output ({total_wins} accomplishments)")
    elif total_wins > 8:
        parts.append(f"strong output ({total_wins} accomplishments)")
    else:
        parts.append(f"moderate output ({total_wins} accomplishments)")

    if repeated_failures > 0:
        parts.append(f"dragged by {repeated_failures} recurring issue(s)")

    if active_days >= 6:
        parts.append(f"consistent {active_days}-day engagement")

    # Capitalize first letter of each sentence
    justification = '. '.join(p[0].upper() + p[1:] if p else p for p in parts) + '.'

    # Score emoji
    if score >= 8:
        emoji = '🟢'
    elif score >= 6:
        emoji = '🟡'
    elif score >= 4:
        emoji = '🟠'
    else:
        emoji = '🔴'

    return f"**{emoji} {score}/10**\n\n{justification}"


def format_longitudinal(pattern_shifts):
    """Format the Longitudinal section (only when history exists)."""
    if not pattern_shifts.get('has_history'):
        return None  # Don't include section at all

    lines = []
    prior_count = pattern_shifts.get('prior_retro_count', 0)
    lines.append(f"*Based on {prior_count} prior retrospective(s).*")
    lines.append('')

    # Score trend
    trend = pattern_shifts.get('score_trend')
    prior_scores = pattern_shifts.get('prior_scores', [])
    if trend and prior_scores:
        scores_str = ' → '.join(str(s) for s in prior_scores[-5:])
        trend_emoji = {'improving': '📈', 'declining': '📉', 'stable': '➡️'}.get(trend, '')
        lines.append(f"**Score trend:** {trend_emoji} {trend.title()} ({scores_str})")
        lines.append('')

    # Pattern shifts
    shifts = pattern_shifts.get('shifts', [])
    new_topics = [s for s in shifts if s['type'] == 'new']
    dropped = [s for s in shifts if s['type'] == 'dropped']

    if new_topics:
        lines.append("**New this week:**")
        for s in new_topics[:5]:
            lines.append(f"  - {s['description']}")
        lines.append('')

    if dropped:
        lines.append("**Dropped from prior weeks:**")
        for s in dropped[:5]:
            lines.append(f"  - {s['description']}")
        lines.append('')

    # Recurring friction
    recurring_friction = pattern_shifts.get('recurring_friction', [])
    if recurring_friction:
        lines.append("**Persistent friction:**")
        for rf in recurring_friction:
            lines.append(f"  - ⚠️ **{rf['label']}** — {rf['warning']}")
        lines.append('')

    # Unaddressed recommendations
    unaddressed = pattern_shifts.get('unaddressed_recommendations', [])
    if unaddressed:
        lines.append("**Unaddressed recommendations:**")
        for ua in unaddressed[:3]:
            lines.append(f"  - \"{ua['recommendation']}\" (from {ua.get('from_date', '?')})")
        lines.append('')

    return '\n'.join(lines).strip() if lines else None


def build_retrospective(analysis):
    """Build the full markdown retrospective."""
    tags = auto_tags(analysis)
    meta = analysis.get('meta', {})
    start = meta.get('start_date', 'unknown')
    end = meta.get('end_date', 'unknown')

    sections = []

    # Frontmatter
    sections.append(format_frontmatter(analysis, tags))
    sections.append('')

    # Title
    sections.append(f"# Weekly Retrospective — {start} to {end}")
    sections.append('')

    # Week at a Glance
    sections.append("## Week at a Glance")
    sections.append('')
    sections.append(format_week_at_a_glance(analysis))
    sections.append('')

    # Wins
    sections.append("## 🏆 Wins")
    sections.append('')
    sections.append(format_wins(analysis.get('accomplishments', [])))
    sections.append('')

    # Patterns
    sections.append("## 🔄 Patterns")
    sections.append('')
    time_patterns = analysis.get('summary_stats', {}).get('time_patterns', {})
    sections.append(format_patterns(
        analysis.get('recurring_themes', []),
        analysis.get('time_sinks', []),
        time_patterns,
    ))
    sections.append('')

    # Friction Points
    sections.append("## 🧱 Friction Points")
    sections.append('')
    sections.append(format_friction(analysis.get('failures', [])))
    sections.append('')

    # Unfinished Business
    sections.append("## 📋 Unfinished Business")
    sections.append('')
    sections.append(format_unfinished(analysis.get('unfinished', [])))
    sections.append('')

    # Recommendations
    sections.append("## 💡 Recommendations")
    sections.append('')
    recs = generate_recommendations(analysis)
    sections.append(format_recommendations(recs))
    sections.append('')

    # Week Score
    sections.append("## 📊 Week Score")
    sections.append('')
    score = analysis.get('suggested_week_score', 5)
    sections.append(format_week_score(score, analysis))
    sections.append('')

    # Longitudinal (only if history exists)
    longitudinal = format_longitudinal(analysis.get('pattern_shifts', {}))
    if longitudinal:
        sections.append("## 📈 Longitudinal")
        sections.append('')
        sections.append(longitudinal)
        sections.append('')

    # Footer
    sections.append("---")
    sections.append(f"*Generated by weekly-retro skill on {datetime.now().strftime('%Y-%m-%d %H:%M ET')}*")

    return '\n'.join(sections)


def main():
    parser = argparse.ArgumentParser(description='Generate markdown retrospective')
    parser.add_argument('--input', type=str, help='Path to analysis JSON (default: stdin)')
    parser.add_argument('--output', type=str, help='Output file path (default: stdout)')
    parser.add_argument('--config', type=str, help='Path to config JSON')
    args = parser.parse_args()

    # Load config
    config = {}
    config_path = args.config or os.environ.get('WEEKLY_RETRO_CONFIG', '')
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

    # Load analysis data
    analysis = load_stdin_or_file(args.input)

    # Build retrospective
    retro_md = build_retrospective(analysis)

    # Output
    if args.output:
        output_path = args.output
    elif config.get('vault_output_dir'):
        start = analysis.get('meta', {}).get('start_date', 'unknown')
        end = analysis.get('meta', {}).get('end_date', 'unknown')
        output_dir = config['vault_output_dir']
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'{start}-to-{end}.md')
    else:
        output_path = None

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        Path(output_path).write_text(retro_md, encoding='utf-8')
        print(f"Retrospective written to: {output_path}", file=sys.stderr)
    else:
        print(retro_md)


if __name__ == '__main__':
    main()
