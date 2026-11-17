#!/usr/bin/env python3
import os
"""Sands conflict scan template — cron-compatible.

Usage: python3 conflict_scan_template.py
Output: /tmp/sands_conflict_scan_result.json

This script handles:
- Multi-account OAuth fallback (owner → indigo)
- 7-day lookahead window
- Overlap detection
- Cross-calendar duplicate detection
- Intra-calendar duplicate detection
- Zero-duration warnings
- Back-to-back chain detection
- Flexibility classification

After running, append results to evidence.jsonl and update config.json.
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from collections import defaultdict

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 conflict_scan_template.py")
    sys.exit(0)

sys.path.insert(0, os.path.expanduser("~/.hermes") + "/scripts")
from google_auth_mcp import get_service


# --- Config ---
CONFIG_PATH = os.path.expanduser("~/indigo-repo") + "/commons/data/ocas-sands/config.json"
with open(CONFIG_PATH) as f:
    config = json.load(f)

PRIMARY_CALENDARS = config['primary_calendar_ids']
TZ = ZoneInfo(config.get('default_timezone', 'America/Los_Angeles'))

# --- Multi-account fallback ---
ACCOUNTS_TO_TRY = [os.environ.get("OCAS_OPERATOR_EMAIL", "operator@example.com"), os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com")]

calendar = None
working_account = None

for account in ACCOUNTS_TO_TRY:
    try:
        cal = get_service('calendar', 'v3', ['https://www.googleapis.com/auth/calendar.readonly'], account=account)
        # Lightweight test call
        cal.calendarList().list(maxResults=1).execute()
        calendar = cal
        working_account = account
        break
    except Exception as e:
        continue

if calendar is None:
    print(json.dumps({"error": "Both OAuth tokens invalid", "degraded": ["oauth_stale"]}))
    sys.exit(1)

# --- Scan window: today + 7 days ---
today = datetime.now(TZ).date()
start_dt = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=TZ)
end_dt = start_dt + timedelta(days=7)
time_min = start_dt.isoformat()
time_max = end_dt.isoformat()

# --- Fetch events ---
all_events = []
calendar_errors = {}
accessible_calendars = []

for cal_id in PRIMARY_CALENDARS:
    try:
        result = calendar.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            showDeleted=False
        ).execute()
        items = result.get('items', [])
        for ev in items:
            ev['_source_calendar'] = cal_id
        all_events.extend(items)
        accessible_calendars.append(cal_id)
    except Exception as e:
        calendar_errors[cal_id] = str(e)

# --- Parse events ---
def parse_event(ev):
    start = ev.get('start', {})
    end = ev.get('end', {})
    all_day = 'date' in start

    if all_day:
        start_dt_local = datetime.fromisoformat(start['date']).replace(tzinfo=TZ)
        end_dt_local = datetime.fromisoformat(end['date']).replace(tzinfo=TZ)
        start_utc = start_dt_local.astimezone(timezone.utc)
        end_utc = end_dt_local.astimezone(timezone.utc)
    else:
        raw_start = start.get('dateTime', '')
        raw_end = end.get('dateTime', '')
        if raw_start.endswith('Z'):
            start_utc = datetime.fromisoformat(raw_start.replace('Z', '+00:00'))
        else:
            start_utc = datetime.fromisoformat(raw_start)
        if raw_end.endswith('Z'):
            end_utc = datetime.fromisoformat(raw_end.replace('Z', '+00:00'))
        else:
            end_utc = datetime.fromisoformat(raw_end)
        start_dt_local = start_utc.astimezone(TZ)
        end_dt_local = end_utc.astimezone(TZ)

    duration_min = (end_utc - start_utc).total_seconds() / 60

    return {
        'id': ev.get('id', ''),
        'summary': ev.get('summary', '(no title)'),
        'start_utc': start_utc,
        'end_utc': end_utc,
        'start_local': start_dt_local,
        'end_local': end_dt_local,
        'all_day': all_day,
        'duration_min': duration_min,
        'attendees': ev.get('attendees', []),
        'conference': ev.get('conferenceData', {}),
        'recurring': bool(ev.get('recurrence', [])),
        'location': ev.get('location', ''),
        'calendar': ev.get('_source_calendar', 'unknown'),
        'description': ev.get('description', ''),
        'event_id': ev.get('id', ''),
    }

parsed = [parse_event(ev) for ev in all_events]
timed_events = sorted([e for e in parsed if not e['all_day']], key=lambda e: e['start_utc'])
all_day_events = [e for e in parsed if e['all_day']]

# --- Overlap detection ---
overlaps = []
for i in range(len(timed_events)):
    for j in range(i + 1, len(timed_events)):
        a, b = timed_events[i], timed_events[j]
        if b['start_utc'] >= a['end_utc']:
            break
        if a['start_utc'] < b['end_utc'] and b['start_utc'] < a['end_utc']:
            overlap_start = max(a['start_utc'], b['start_utc'])
            overlap_end = min(a['end_utc'], b['end_utc'])
            overlap_min = (overlap_end - overlap_start).total_seconds() / 60
            overlaps.append({
                'event_a': a, 'event_b': b,
                'overlap_min': overlap_min,
                'overlap_start': overlap_start.astimezone(TZ),
                'overlap_end': overlap_end.astimezone(TZ),
            })

# --- Zero-duration ---
zero_duration = [e for e in timed_events if e['duration_min'] == 0]

# --- Cross-calendar duplicates ---
cross_cal_groups = defaultdict(list)
for e in timed_events:
    key = (e['summary'].lower().strip(), e['start_local'].strftime('%Y-%m-%dT%H:%M'), e['location'].lower().strip())
    cross_cal_groups[key].append(e)

cross_cal_duplicates = []
for key, group in cross_cal_groups.items():
    cal_ids = set(e['calendar'] for e in group)
    event_ids = set(e['event_id'] for e in group)
    if len(group) > 1 and len(cal_ids) > 1 and len(event_ids) > 1:
        cross_cal_duplicates.append({'key': key, 'events': group, 'calendars': list(cal_ids)})

# --- Intra-calendar duplicates ---
intra_cal_groups = defaultdict(list)
for e in timed_events:
    key = (e['summary'].lower().strip(), e['start_local'].strftime('%Y-%m-%dT%H:%M'))
    intra_cal_groups[(e['calendar'], key)].append(e)

intra_cal_duplicates = []
for (cal, key), group in intra_cal_groups.items():
    if len(group) > 1 and len(set(e['event_id'] for e in group)) > 1:
        intra_cal_duplicates.append({'calendar': cal, 'key': key, 'events': group})

# --- Back-to-back chains (3+ events, gaps <= 15 min) ---
day_events = defaultdict(list)
for e in timed_events:
    day_events[e['start_local'].date()].append(e)

chains = []
for day, events in sorted(day_events.items()):
    events.sort(key=lambda e: e['start_utc'])
    if len(events) < 3:
        continue
    chain = [events[0]]
    for i in range(1, len(events)):
        gap = (events[i]['start_utc'] - events[i-1]['end_utc']).total_seconds() / 60
        if gap <= 15:
            chain.append(events[i])
        else:
            if len(chain) >= 3:
                chains.append({'day': day, 'chain': chain})
            chain = [events[i]]
    if len(chain) >= 3:
        chains.append({'day': day, 'chain': chain})

# --- Flexibility classification ---
def classify_event(ev):
    title = ev['summary'].lower()
    attendees = ev.get('attendees', [])
    conference = ev.get('conference', {})
    location = ev.get('location', '').lower()
    recurring = ev.get('recurring', False)
    calendar = ev.get('calendar', '')

    fixed_signals = []
    for att in attendees:
        email = att.get('email', '')
        if email and not email.endswith(('@gmail.com', '@googlemail.com')):
            fixed_signals.append('external attendees')
            break

    fixed_keywords = [
        'call', 'meeting', 'interview', 'sync', 'standup', 'review',
        'appointment', 'doctor', 'dentist', 'flight', 'train', 'reservation',
        'class', 'course', 'workshop', 'concert', 'show', 'game', 'lesson',
        'visit', 'patient', 'therapy', 'session', 'checkup', 'consultation',
        'screening', 'massage', 'spa', 'haircut', 'salon', 'treatment',
        'mri', 'scan', 'x-ray', 'bloodwork', 'lab', 'dental', 'medical',
        'physician', 'specialist', 'chiropractor', 'acupuncture',
        'dinner', 'lunch', 'breakfast', 'brunch', 'mastery', 'training'
    ]
    for kw in fixed_keywords:
        if kw in title:
            fixed_signals.append(f'title keyword: {kw}')
            break

    if conference:
        fixed_signals.append('conference link')
    if recurring:
        fixed_signals.append('recurring event')
    if 'work' in calendar.lower():
        fixed_signals.append('work calendar busy block')

    flexible_keywords = [
        'gym', 'workout', 'run', 'walk', 'errand', 'personal', 'reading',
        'focus time', 'deep work', 'solo lunch', 'groceries', 'cleaners',
        'ikebana', 'flower market', 'meditation', 'yoga', 'journaling'
    ]
    flexible_signals = []
    for kw in flexible_keywords:
        if kw in title:
            flexible_signals.append(f'title keyword: {kw}')
            break

    no_external = not any('external attendees' in s for s in fixed_signals)
    no_conference = not conference
    no_fixed_venue = not any(v in location for v in ['spa', 'clinic', 'hospital', 'office', 'restaurant', 'salon'])

    if flexible_signals and no_external and no_conference and no_fixed_venue:
        return 'FLEXIBLE', flexible_signals
    if fixed_signals:
        return 'FIXED', fixed_signals
    return 'AMBIGUOUS', ['insufficient metadata or mixed signals']

# --- Build output ---
output = {
    'scan_date': datetime.now(TZ).isoformat(),
    'window_start': time_min,
    'window_end': time_max,
    'calendars_queried': accessible_calendars,
    'calendars_failed': list(calendar_errors.keys()),
    'total_events': len(parsed),
    'timed_events': len(timed_events),
    'all_day_events': len(all_day_events),
    'auth_account_used': working_account,
    'degraded': ['oauth_fallback_indigo'] if working_account != ACCOUNTS_TO_TRY[0] else [],
    'overlaps': [],
    'cross_calendar_duplicates': [],
    'intra_calendar_duplicates': [],
    'zero_duration_warnings': [],
    'back_to_back_chains': [],
    'calendar_errors': calendar_errors,
}

# Format overlaps
for ov in overlaps:
    a, b = ov['event_a'], ov['event_b']
    flex_a, signals_a = classify_event(a)
    flex_b, signals_b = classify_event(b)

    min_dur = min(a['duration_min'], b['duration_min'])
    if min_dur > 0 and ov['overlap_min'] >= min_dur * 0.8:
        severity = '🔴'
        overlap_type = 'Full overlap'
    else:
        severity = '🟡'
        overlap_type = 'Partial overlap'

    if flex_a == 'FLEXIBLE' and flex_b != 'FLEXIBLE':
        resolution = f"Move [{a['summary']}] — it's FLEXIBLE"
    elif flex_b == 'FLEXIBLE' and flex_a != 'FLEXIBLE':
        resolution = f"Move [{b['summary']}] — it's FLEXIBLE"
    elif flex_a == 'FLEXIBLE' and flex_b == 'FLEXIBLE':
        resolution = f"Both flexible — move either"
    else:
        resolution = "Both FIXED — manual resolution required"

    output['overlaps'].append({
        'severity': severity,
        'overlap_type': overlap_type,
        'overlap_min': int(ov['overlap_min']),
        'day': ov['overlap_start'].strftime('%A, %B %d'),
        'time_range': f"{ov['overlap_start'].strftime('%I:%M %p')} – {ov['overlap_end'].strftime('%I:%M %p')}",
        'event_a': {'title': a['summary'], 'calendar': a['calendar'], 'flexibility': flex_a, 'signals': signals_a, 'time': f"{a['start_local'].strftime('%I:%M %p')} – {a['end_local'].strftime('%I:%M %p')}"},
        'event_b': {'title': b['summary'], 'calendar': b['calendar'], 'flexibility': flex_b, 'signals': signals_b, 'time': f"{b['start_local'].strftime('%I:%M %p')} – {b['end_local'].strftime('%I:%M %p')}"},
        'resolution': resolution,
    })

# Format duplicates
for dup in cross_cal_duplicates:
    evs = dup['events']
    output['cross_calendar_duplicates'].append({
        'title': evs[0]['summary'],
        'calendars': dup['calendars'],
        'start': evs[0]['start_local'].strftime('%A, %B %d at %I:%M %p'),
        'recommendation': f"Remove from non-canonical calendar",
    })

for dup in intra_cal_duplicates:
    evs = dup['events']
    keep = max(evs, key=lambda e: len(e.get('description', '')) + len(e.get('location', '')))
    output['intra_calendar_duplicates'].append({
        'title': evs[0]['summary'],
        'calendar': dup['calendar'],
        'start': evs[0]['start_local'].strftime('%A, %B %d at %I:%M %p'),
        'recommendation': f"Keep {keep['event_id'][:12]}... (more detailed)",
    })

for e in zero_duration:
    output['zero_duration_warnings'].append({
        'title': e['summary'],
        'calendar': e['calendar'],
        'start': e['start_local'].strftime('%A, %B %d at %I:%M %p'),
        'note': 'start == end — end time may not have been set correctly',
    })

for chain_info in chains:
    chain = chain_info['chain']
    chain_str = ' → '.join([
        f"{e['summary']} ({e['start_local'].strftime('%I:%M %p')}-{e['end_local'].strftime('%I:%M %p')})"
        for e in chain
    ])
    gaps = []
    for i in range(1, len(chain)):
        gap = (chain[i]['start_utc'] - chain[i-1]['end_utc']).total_seconds() / 60
        gaps.append(int(gap))
    has_zero_gap = any(g <= 0 for g in gaps)
    output['back_to_back_chains'].append({
        'day': chain_info['day'].strftime('%A, %B %d'),
        'chain': chain_str,
        'gaps': gaps,
        'zero_gap_warning': has_zero_gap,
        'recommendation': 'Zero-gap chain — no room for travel' if has_zero_gap else f'Tight gaps ({", ".join(f"{g} min" for g in gaps)}) — verify travel feasibility',
    })

# Write output
with open('/tmp/sands_conflict_scan_result.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)

# Print summary
print(f"Account used: {working_account}")
print(f"Window: {time_min} → {time_max}")
print(f"Events: {len(parsed)} ({len(timed_events)} timed, {len(all_day_events)} all-day)")
print(f"Overlaps: {len(output['overlaps'])}")
print(f"Cross-cal duplicates: {len(output['cross_calendar_duplicates'])}")
print(f"Intra-cal duplicates: {len(output['intra_calendar_duplicates'])}")
print(f"Zero-duration: {len(output['zero_duration_warnings'])}")
print(f"Chains: {len(output['back_to_back_chains'])}")
print(f"Errors: {calendar_errors}")
print(f"\nResults: /tmp/sands_conflict_scan_result.json")
