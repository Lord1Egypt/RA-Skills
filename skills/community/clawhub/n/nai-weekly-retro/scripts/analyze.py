#!/usr/bin/env python3
"""
analyze.py — Pattern detection and analysis for weekly retrospective.

Takes gathered data (from gather_week.py), identifies accomplishments,
recurring themes, failures, time sinks, pattern shifts, unfinished threads,
and formalization candidates. Outputs structured JSON with confidence scores.

Usage:
    python3 gather_week.py [...] | python3 analyze.py [--history PATH] [--soul PATH] [--agents PATH]
    python3 analyze.py --input gathered.json [--history PATH]
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


def _clean_evidence(text):
    """Clean markdown artifacts from evidence text."""
    t = text.strip()
    # Remove leading markdown formatting: ##, numbering, checkboxes
    t = re.sub(r'^#+\s*', '', t)
    t = re.sub(r'^\d+\.\s*', '', t)
    t = re.sub(r'^[⬜✅]\s*', '', t)
    # Remove bold markers around labels like "**Bug 1:** — text"
    # First handle "**Label:** — rest" or "**Label** — rest"
    t = re.sub(r'^\*\*([^*]+?)(?::?\s*)\*\*\s*[-—]\s*', r'\1: ', t)
    # Then remove remaining bold markers (keep the text inside)
    t = re.sub(r'\*\*([^*]*)\*\*', r'\1', t)
    # Remove any remaining stray double asterisks
    t = t.replace('**', '')
    # Remove backtick code markers for cleaner evidence
    t = t.replace('`', '')
    # Strip leading/trailing whitespace and dashes
    t = t.strip().strip('-—').strip()
    # Skip very short or meaningless results
    if len(t) < 15:
        return ''
    # Skip lines that are just section headers
    if t.endswith(':') and len(t) < 60:
        return ''
    return t


def load_json(path):
    """Load a JSON file, return empty dict on failure."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_stdin_or_file(input_path):
    """Read gathered data from stdin or file."""
    if input_path:
        with open(input_path, 'r') as f:
            return json.load(f)
    else:
        return json.load(sys.stdin)


def scan_for_formalized(soul_path, agents_path):
    """Read SOUL.md and AGENTS.md to find already-formalized patterns."""
    formalized = set()
    for path in [soul_path, agents_path]:
        if path and os.path.exists(path):
            text = Path(path).read_text(encoding='utf-8').lower()
            # Extract key concepts mentioned in operational docs
            # Look for specific workflows, cron jobs, rules that are codified
            if 'cron' in text:
                formalized.add('cron-jobs')
            if 'daily recap' in text or 'daily-recap' in text:
                formalized.add('daily-recap')
            if 'media vault' in text or 'youtube' in text:
                formalized.add('media-vault')
            if 'trending' in text and 'scanner' in text:
                formalized.add('trending-scanner')
            if 'obsidian' in text and 'vault' in text:
                formalized.add('obsidian-vault')
            if 'smart routing' in text or 'model routing' in text:
                formalized.add('model-routing')
            if 'memory' in text and ('daily' in text or 'log' in text):
                formalized.add('memory-logging')
    return formalized


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def analyze_accomplishments(gathered):
    """Extract and deduplicate accomplishments with evidence."""
    agg = gathered['aggregation']
    raw_accomplishments = agg.get('accomplishments', [])

    # Group by similarity (keyword clustering with fallback)
    clusters = defaultdict(list)
    for item in raw_accomplishments:
        text = item['text'].lower()
        # Find the primary subject — order matters (most specific first)
        if 'mission control' in text:
            clusters['Mission Control dashboard'].append(item)
        elif 'tokenpulse' in text or 'token pulse' in text or ('proxy' in text and ('port' in text or 'live' in text)) or ('phase' in text and 'complete' in text):
            clusters['TokenPulse development'].append(item)
        elif 'clawhub' in text or ('skill' in text and ('publish' in text or 'built' in text or 'batch' in text or 'live on' in text)):
            clusters['ClawHub skills'].append(item)
        elif 'lilith' in text:
            clusters['Lilith bot'].append(item)
        elif 'soul' in text or 'identity' in text or 'agents.md' in text or 'workspace file' in text:
            clusters['Identity/workspace rewrite'].append(item)
        elif 'dashboard' in text and ('web' in text or 'react' in text or 'production' in text):
            clusters['TokenPulse development'].append(item)
        elif ('cron' in text and 'job' in text) or 'scanner' in text:
            clusters['Automation setup'].append(item)
        elif 'routing' in text and 'model' in text:
            clusters['Model routing'].append(item)
        elif 'open webui' in text:
            clusters['Open WebUI'].append(item)
        elif 'youtube' in text or 'media vault' in text:
            clusters['Media vault'].append(item)
        elif 'claude' in text and ('max' in text or 'swap' in text):
            clusters['Claude auth'].append(item)
        elif 'workflow' in text and 'crystallizer' in text:
            clusters['Workflow Crystallizer'].append(item)
        elif 'readme' in text or 'changelog' in text or 'getting_started' in text or 'documentation' in text:
            clusters['Documentation'].append(item)
        elif 'launchd' in text or 'service' in text and ('deploy' in text or 'running' in text):
            clusters['Infrastructure'].append(item)
        elif 'build' in text or 'axum' in text or 'sqlite' in text or 'react' in text or 'cargo' in text:
            clusters['TokenPulse development'].append(item)
        elif 'llama.cpp' in text or 'ollama' in text or 'qwen' in text:
            clusters['Local model infrastructure'].append(item)
        elif 'git' in text or 'commit' in text or 'github' in text or 'pushed' in text:
            clusters['Git/shipping'].append(item)
        elif 'fix' in text or 'bug' in text or 'verified' in text or 'tested' in text:
            clusters['Bug fixes & verification'].append(item)
        elif 'research' in text or 'market' in text or 'analysis' in text:
            clusters['Research'].append(item)
        elif 'domain' in text or 'name' in text and 'finalized' in text:
            clusters['Product decisions'].append(item)
        else:
            # Try to assign based on context from date — same-day clustering
            assigned = False
            date = item.get('date', '')
            # Check what other items on this date are categorized as
            for label, items_in_cluster in clusters.items():
                if label == 'Uncategorized':
                    continue
                for existing in items_in_cluster:
                    if existing.get('date') == date:
                        clusters[label].append(item)
                        assigned = True
                        break
                if assigned:
                    break
            if not assigned:
                clusters['Uncategorized'].append(item)

    # Build accomplishment entries with evidence
    results = []
    for label, items in clusters.items():
        if not items:
            continue
        if label == 'Uncategorized' and len(items) <= 2:
            continue  # Skip tiny uncategorized clusters
        dates = sorted(set(i['date'] for i in items))
        # Pick the best evidence lines (most descriptive)
        evidence = []
        seen = set()
        # Score items: prefer positive shipping language over bug/fix language
        def _evidence_score(text):
            t = text.lower()
            score = len(text)  # Longer = more descriptive
            # Boost shipping language
            if any(w in t for w in ['deployed', 'live', 'shipped', 'published', 'built', 'complete']):
                score += 200
            if '✅' in t:
                score += 100
            # Penalize bug/error language in evidence for accomplishment sections
            if any(w in t for w in ['bug', 'error', 'broke', 'missing', 'not working']):
                score -= 150
            return score

        for i in sorted(items, key=lambda x: _evidence_score(x['text']), reverse=True):
            # Deduplicate near-identical evidence
            key = i['text'][:60].lower()
            if key not in seen:
                # Clean up markdown artifacts
                clean_text = _clean_evidence(i['text'])
                if clean_text:
                    evidence.append(clean_text)
                    seen.add(key)
            if len(evidence) >= 5:
                break

        results.append({
            'label': label,
            'count': len(items),
            'dates': dates,
            'evidence': evidence,
            'confidence': min(0.95, 0.5 + len(items) * 0.05 + len(dates) * 0.1),
        })

    # Sort by count descending
    results.sort(key=lambda x: x['count'], reverse=True)
    return results


def analyze_recurring_themes(gathered):
    """Find topics that appeared on 3+ days or consumed heavy attention."""
    agg = gathered['aggregation']
    recurring = agg.get('recurring_topics', {})
    day_weights = agg.get('day_weights', {})

    results = []
    for topic, dates in recurring.items():
        day_count = len(dates)
        if day_count < 2:
            continue

        # Calculate topic weight as share of total content
        # We estimate this from the normalized topic → how many sections in each day
        topic_sections = 0
        topic_weight = 0
        for day in gathered['days']:
            if day.get('missing'):
                continue
            for s in day.get('sections', []):
                from scripts.gather_week import normalize_topic  # noqa
                pass  # We'll use inline normalization instead

        results.append({
            'topic': topic,
            'day_count': day_count,
            'dates': sorted(dates),
            'is_positive': topic not in ('failures', 'bugs', 'friction'),
            'confidence': min(0.95, 0.3 + day_count * 0.15),
        })

    results.sort(key=lambda x: x['day_count'], reverse=True)
    return results


def analyze_recurring_themes_v2(gathered):
    """Find topics that appeared on 2+ days — uses pre-aggregated data."""
    agg = gathered['aggregation']
    recurring = agg.get('recurring_topics', {})

    # Also check tool frequency for recurring tool themes
    tool_freq = agg.get('tool_frequency', {})

    results = []
    for topic, dates in recurring.items():
        day_count = len(dates)
        if day_count < 2:
            continue
        results.append({
            'topic': topic,
            'day_count': day_count,
            'dates': sorted(dates),
            'type': 'topic',
            'confidence': min(0.95, 0.3 + day_count * 0.15),
        })

    # Add tool-based themes (tools used on 3+ days)
    for tool, count in tool_freq.items():
        if count >= 3:
            results.append({
                'topic': f'{tool} (tool usage)',
                'day_count': count,
                'dates': [],  # tool frequency doesn't track per-day
                'type': 'tool',
                'confidence': min(0.9, 0.4 + count * 0.1),
            })

    results.sort(key=lambda x: x['day_count'], reverse=True)
    return results


def analyze_failures(gathered):
    """Find repeated failures and breakage patterns."""
    agg = gathered['aggregation']
    raw_failures = agg.get('failures', [])

    # Group failures by theme
    clusters = defaultdict(list)
    for item in raw_failures:
        text = item['text'].lower()
        if 'tokenpulse' in text or 'proxy' in text or 'header' in text or 'https' in text or 'reqwest' in text:
            clusters['TokenPulse proxy bugs'].append(item)
        elif 'token' in text and ('0' in text or 'unknown' in text or 'missing' in text):
            clusters['Token tracking failures'].append(item)
        elif 'lilith' in text or ('ollama' in text and 'error' in text):
            clusters['Lilith/Ollama errors'].append(item)
        elif 'rate' in text and 'limit' in text:
            clusters['Rate limiting'].append(item)
        elif 'restart' in text or 'reboot' in text or ('manual' in text and 'restart' in text):
            clusters['Manual restart burden'].append(item)
        elif ('log' in text and ('empty' in text or 'missing' in text)) or 'no logging' in text:
            clusters['Logging gaps'].append(item)
        elif 'test' in text and ('zero' in text or 'no ' in text or 'never' in text):
            clusters['Missing tests'].append(item)
        elif 'vision' in text and ('didn' in text or 'not' in text or 'support' in text):
            clusters['Vision model compatibility'].append(item)
        elif 'oauth' in text or 'scope' in text or 'unauthorized' in text or '401' in text:
            clusters['Authentication issues'].append(item)
        elif 'dashboard' in text and ('flat' in text or 'boring' in text or 'not' in text):
            clusters['UX/design feedback'].append(item)
        elif 'streaming' in text and ('0' in text or 'not' in text or 'missing' in text):
            clusters['Streaming extraction gaps'].append(item)
        elif 'junk' in text or 'cleanup' in text or 'corrupt' in text:
            clusters['Data quality'].append(item)
        else:
            # Try to infer from context
            if 'bug' in text or 'fix' in text or 'broke' in text:
                clusters['General bugs'].append(item)
            else:
                clusters['Miscellaneous friction'].append(item)

    results = []
    for label, items in clusters.items():
        dates = sorted(set(i['date'] for i in items))
        raw_evidence = list(dict.fromkeys(i['text'] for i in items))[:5]
        evidence = [_clean_evidence(e) for e in raw_evidence]
        evidence = [e for e in evidence if e]  # Filter empties
        repeated = len(dates) > 1

        results.append({
            'label': label,
            'count': len(items),
            'dates': dates,
            'repeated': repeated,
            'evidence': evidence,
            'confidence': min(0.95, 0.4 + len(items) * 0.08 + (0.2 if repeated else 0)),
        })

    results.sort(key=lambda x: (x['repeated'], x['count']), reverse=True)
    return results


def analyze_time_sinks(gathered):
    """Identify topics that consumed disproportionate attention."""
    days = gathered['days']
    total_content = gathered['aggregation'].get('total_content_bytes', 1)

    # Calculate per-topic content volume using section weight (line count)
    topic_volume = defaultdict(lambda: {'weight': 0, 'sections': 0, 'dates': set()})
    total_weight = 0

    for day in days:
        if day.get('missing'):
            continue
        for section in day.get('sections', []):
            header = section['header']
            topic_key = _normalize_for_sink(header)
            weight = section.get('weight', 0)
            topic_volume[topic_key]['weight'] += weight
            topic_volume[topic_key]['sections'] += 1
            topic_volume[topic_key]['dates'].add(day['date'])
            total_weight += weight

    results = []
    for topic, data in topic_volume.items():
        share = data['weight'] / max(total_weight, 1)
        # A notable topic is >3% of total weight OR >3 sections across days
        if share > 0.03 or data['sections'] >= 3:
            results.append({
                'topic': topic,
                'content_share': round(share, 3),
                'section_count': data['sections'],
                'dates': sorted(data['dates']),
                'is_sink': share > 0.25,
                'confidence': min(0.95, 0.3 + share * 2 + data['sections'] * 0.05),
            })

    # Filter out meta-topics that aren't real "work"
    skip = {'Daily Recap', 'daily-recap'}
    results = [r for r in results if r['topic'] not in skip]

    results.sort(key=lambda x: x['content_share'], reverse=True)
    return results


def _normalize_for_sink(header):
    """Normalize header text for time-sink grouping."""
    h = header.lower()
    if 'tokenpulse' in h:
        return 'TokenPulse'
    if 'lilith' in h:
        return 'Lilith'
    if 'clawhub' in h or 'skill' in h and 'batch' in h:
        return 'ClawHub Skills'
    if 'mission control' in h:
        return 'Mission Control'
    if 'model' in h or 'routing' in h:
        return 'Model Routing'
    if 'soul' in h or 'identity' in h or 'workspace file' in h:
        return 'Identity Rewrite'
    if 'youtube' in h or 'media' in h:
        return 'Media Vault'
    if 'workflow' in h or 'crystallizer' in h:
        return 'Workflow Crystallizer'
    if 'open webui' in h:
        return 'Open WebUI'
    if 'audit' in h:
        return 'Audit'
    if 'daily recap' in h or 'end of day' in h:
        return 'Daily Recap'
    if 'api' in h and ('tokenizer' in h or 'brainstorm' in h):
        return 'TokenPulse'
    if 'research' in h or 'market' in h:
        return 'Research'
    if 'trending' in h or 'scanner' in h:
        return 'Automation'
    if 'strategy' in h or 'quality' in h or 'first.?principle' in h:
        return 'Strategy'
    if 'fiverr' in h or 'freelance' in h:
        return 'Freelance'
    if 'account' in h or 'publishing' in h:
        return 'Publishing'
    if 'documentation' in h:
        return 'Documentation'
    if 'setup' in h or 'config' in h:
        return 'Setup & Config'
    if 'hardware' in h or 'mac mini' in h:
        return 'Infrastructure'
    if 'beta' in h or 'checklist' in h:
        return 'TokenPulse'
    if 'feedback' in h:
        return 'User Feedback'
    if 'discussion' in h:
        return 'Discussions'
    if 'git' in h and 'status' in h:
        return 'TokenPulse'
    if 'domain' in h:
        return 'TokenPulse'
    return header.title()


def analyze_unfinished(gathered):
    """Find action items and TODOs that weren't resolved later in the week."""
    agg = gathered['aggregation']
    action_items = agg.get('action_items', [])
    accomplishments = agg.get('accomplishments', [])

    # Flatten accomplishment text for checking if items were resolved
    accomplished_text = ' '.join(a['text'].lower() for a in accomplishments)

    results = []
    for item in action_items:
        text = item['text']
        text_lower = text.lower()

        # Check if this was likely resolved
        resolved = False
        # Simple heuristic: check if key words from the action item appear in accomplishments
        keywords = set(re.findall(r'\b[a-z]{4,}\b', text_lower))
        keywords -= {'need', 'needs', 'should', 'have', 'been', 'this', 'that', 'with', 'from', 'will'}
        if keywords:
            match_count = sum(1 for kw in keywords if kw in accomplished_text)
            if match_count / len(keywords) > 0.5:
                resolved = True

        if not resolved:
            # Filter out noise: job IDs, pure references, very short items
            if re.match(r'^[a-f0-9-]{20,}$', text.strip()):
                continue  # Skip bare UUIDs
            if 'job id' in text_lower:
                continue  # Skip job ID references
            results.append({
                'text': text,
                'date': item['date'],
                'confidence': 0.6,  # Action items are inherently uncertain
            })

    return results


def analyze_formalization_candidates(gathered, formalized_set):
    """Find things that keep being re-discussed or re-decided that should be codified."""
    agg = gathered['aggregation']
    recurring = agg.get('recurring_topics', {})
    decisions = agg.get('decisions', [])

    candidates = []

    # Topics discussed many days that aren't formalized
    for topic, dates in recurring.items():
        if len(dates) >= 3 and topic not in formalized_set:
            candidates.append({
                'topic': topic,
                'reason': f'Discussed on {len(dates)} days this week — consider formalizing in AGENTS.md or as a skill',
                'dates': sorted(dates),
                'confidence': min(0.9, 0.4 + len(dates) * 0.1),
            })

    # Repeated decisions about the same thing (sign of unclear policy)
    decision_topics = defaultdict(list)
    for d in decisions:
        text_lower = d['text'].lower()
        if 'tokenpulse' in text_lower:
            decision_topics['tokenpulse'].append(d)
        elif 'model' in text_lower or 'routing' in text_lower:
            decision_topics['model-routing'].append(d)
        elif 'lilith' in text_lower:
            decision_topics['lilith'].append(d)

    for topic, items in decision_topics.items():
        dates = set(i['date'] for i in items)
        if len(dates) >= 2 and topic not in formalized_set:
            candidates.append({
                'topic': f'{topic} decisions',
                'reason': f'Decisions about {topic} made on {len(dates)} different days — policy should be documented',
                'dates': sorted(dates),
                'confidence': min(0.85, 0.5 + len(dates) * 0.1),
            })

    return candidates


def analyze_pattern_shifts(gathered, history):
    """Detect what's new this week vs. historical patterns."""
    if not history or not history.get('retros'):
        return {
            'has_history': False,
            'shifts': [],
            'note': 'No prior retros — cannot detect pattern shifts yet.',
        }

    retros = history['retros']
    prior_topics = set()
    prior_friction = set()

    for retro in retros:
        prior_topics.update(retro.get('key_topics', []))
        prior_friction.update(f.get('label', '') for f in retro.get('friction_points', []))

    # Current week topics
    current_topics = set(gathered['aggregation'].get('recurring_topics', {}).keys())

    new_topics = current_topics - prior_topics
    dropped_topics = prior_topics - current_topics

    shifts = []
    for topic in new_topics:
        shifts.append({
            'type': 'new',
            'topic': topic,
            'description': f'"{topic}" is new this week — not seen in prior retros',
        })
    for topic in dropped_topics:
        shifts.append({
            'type': 'dropped',
            'topic': topic,
            'description': f'"{topic}" was active in prior weeks but absent this week',
        })

    # Score trends
    prior_scores = [r.get('week_score', 0) for r in retros if r.get('week_score')]
    score_trend = None
    if len(prior_scores) >= 2:
        avg_recent = sum(prior_scores[-3:]) / len(prior_scores[-3:])
        avg_older = sum(prior_scores[:-3]) / max(len(prior_scores[:-3]), 1)
        if avg_recent > avg_older + 0.5:
            score_trend = 'improving'
        elif avg_recent < avg_older - 0.5:
            score_trend = 'declining'
        else:
            score_trend = 'stable'

    # Check for persistent friction
    current_friction_labels = set()
    # We'll get these from the caller — for now, flag from history
    recurring_friction = []
    friction_counts = Counter()
    for retro in retros:
        for fp in retro.get('friction_points', []):
            friction_counts[fp.get('label', '')] += 1
    for label, count in friction_counts.items():
        if count >= 2:
            recurring_friction.append({
                'label': label,
                'weeks': count,
                'warning': f'This has been a friction point for {count} consecutive weeks',
            })

    # Check for unaddressed recommendations
    unaddressed = []
    for retro in retros[-3:]:  # Last 3 retros
        for rec in retro.get('recommendations', []):
            if not rec.get('addressed', False):
                unaddressed.append({
                    'recommendation': rec.get('text', ''),
                    'from_date': retro.get('date_end', ''),
                    'weeks_ago': len(retros) - retros.index(retro),
                })

    return {
        'has_history': True,
        'prior_retro_count': len(retros),
        'shifts': shifts,
        'score_trend': score_trend,
        'prior_scores': prior_scores,
        'recurring_friction': recurring_friction,
        'unaddressed_recommendations': unaddressed,
    }


def compute_week_score(accomplishments, failures, time_sinks, unfinished, active_days):
    """Compute a suggested week score (1-10) based on analysis."""
    score = 5.0  # Baseline

    # Accomplishments boost
    total_accomplishment_items = sum(a['count'] for a in accomplishments)
    if total_accomplishment_items > 20:
        score += 2.0
    elif total_accomplishment_items > 10:
        score += 1.5
    elif total_accomplishment_items > 5:
        score += 1.0

    # Variety of accomplishment areas
    if len(accomplishments) >= 4:
        score += 0.5

    # Failures drag
    repeated_failures = sum(1 for f in failures if f.get('repeated'))
    if repeated_failures > 2:
        score -= 1.5
    elif repeated_failures > 0:
        score -= 0.5

    # Unfinished items drag slightly
    if len(unfinished) > 5:
        score -= 0.5

    # Active days bonus
    if active_days >= 6:
        score += 0.5
    elif active_days <= 3:
        score -= 0.5

    # Time sink penalty (if one topic > 40% of content)
    for sink in time_sinks:
        if sink['content_share'] > 0.4:
            score -= 0.5
            break

    return max(1, min(10, round(score)))


def main():
    parser = argparse.ArgumentParser(description='Analyze gathered weekly data')
    parser.add_argument('--input', type=str, help='Path to gathered JSON (default: stdin)')
    parser.add_argument('--history', type=str, help='Path to retro history JSON')
    parser.add_argument('--soul', type=str, help='Path to SOUL.md')
    parser.add_argument('--agents', type=str, help='Path to AGENTS.md')
    parser.add_argument('--config', type=str, help='Path to config JSON')
    args = parser.parse_args()

    # Load config
    config = {}
    config_path = args.config or os.environ.get('WEEKLY_RETRO_CONFIG', '')
    if config_path and os.path.exists(config_path):
        config = load_json(config_path)

    # Load gathered data
    gathered = load_stdin_or_file(args.input)

    # Load history
    history_path = args.history or config.get('history_file', '')
    history = load_json(history_path) if history_path else {}

    # Load SOUL.md / AGENTS.md for formalization detection
    soul_path = args.soul or config.get('soul_path', os.path.expanduser('~/.openclaw/workspace/SOUL.md'))
    agents_path = args.agents or config.get('agents_path', os.path.expanduser('~/.openclaw/workspace/AGENTS.md'))
    formalized = scan_for_formalized(soul_path, agents_path)

    # Run analyses
    accomplishments = analyze_accomplishments(gathered)
    recurring_themes = analyze_recurring_themes_v2(gathered)
    failures = analyze_failures(gathered)
    time_sinks = analyze_time_sinks(gathered)
    unfinished = analyze_unfinished(gathered)
    formalization = analyze_formalization_candidates(gathered, formalized)
    pattern_shifts = analyze_pattern_shifts(gathered, history)

    active_days = gathered['aggregation'].get('active_days', 0)
    suggested_score = compute_week_score(
        accomplishments, failures, time_sinks, unfinished, active_days
    )

    output = {
        'meta': gathered['meta'],
        'summary_stats': {
            'active_days': active_days,
            'total_days': gathered['aggregation'].get('total_days', 0),
            'total_content_bytes': gathered['aggregation'].get('total_content_bytes', 0),
            'accomplishment_clusters': len(accomplishments),
            'failure_clusters': len(failures),
            'unfinished_count': len(unfinished),
            'tool_frequency': gathered['aggregation'].get('tool_frequency', {}),
            'time_patterns': gathered['aggregation'].get('time_patterns', {}),
        },
        'accomplishments': accomplishments,
        'recurring_themes': recurring_themes,
        'failures': failures,
        'time_sinks': time_sinks,
        'unfinished': unfinished,
        'formalization_candidates': formalization,
        'pattern_shifts': pattern_shifts,
        'suggested_week_score': suggested_score,
    }

    json.dump(output, sys.stdout, indent=2, default=str)
    print()


if __name__ == '__main__':
    main()
