#!/usr/bin/env python3
import os
"""
Sands Morning Briefing Template (cron-compatible)

Generates a Vesper-ready morning briefing for today's events:
- Multi-account OAuth fallback (owner → indigo)
- Multi-calendar query (configurable CALENDAR_IDS)
- Cross-calendar deduplication (summary + start time)
- Intra-calendar overlap detection
- Preparation signal flagging
- Free-hours calculation within working hours
- Vesper InsightProposal JSON payload output

Usage:
    1. Copy this template: cp templates/sands_briefing_morning.py /tmp/
    2. Set CALENDAR_IDS to match your config.json primary_calendar_ids
    3. Run: python3 /tmp/sands_briefing_morning.py
    4. Read JSON from /tmp/sands_morning_briefing.json

Output:
    - /tmp/sands_morning_briefing.json — full Vesper emit payload (suggested_follow_up)
    - stdout: human-readable summary line
"""
import json
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, 'os.path.expanduser("~/.hermes")/scripts')
from google_auth_mcp import get_service

# =============================================================================
# CONFIGURATION — update these to match config.json
# =============================================================================
CALENDAR_IDS = [
    os.environ.get("OCAS_OPERATOR_EMAIL", "operator@example.com"),
    "<family-calendar-id>@group.calendar.google.com"
]
WORK_CALENDAR_ID = ""  # leave empty if no work calendar
ACCOUNTS_TO_TRY = [os.environ.get("OCAS_OPERATOR_EMAIL", "operator@example.com"), os.environ.get("OCAS_AGENT_EMAIL", "agent@example.com")]
WORKING_HOURS = {"start": "09:00", "end": "18:00"}

# =============================================================================
# DATE SETUP (auto-detects PDT from system timezone)
# =============================================================================
PDT = timezone(timedelta(hours=-7))
now = datetime.now(PDT)
today_str = now.strftime('%Y-%m-%d')
tomorrow_str = (now + timedelta(days=1)).strftime('%Y-%m-%d')

time_min = f"{today_str}T00:00:00-07:00"
time_max = f"{tomorrow_str}T00:00:00-07:00"

# =============================================================================
# OAUTH: FIND WORKING ACCOUNT (multi-account fallback)
# =============================================================================
calendar = None
working_account = None
auth_fallback_used = False

for account in ACCOUNTS_TO_TRY:
    try:
        cal = get_service(
            'calendar', 'v3',
            ['https://www.googleapis.com/auth/calendar.readonly'],
            account=account
        )
        cal.calendarList().list(maxResults=1).execute()
        calendar = cal
        working_account = account
        break
    except Exception as e:
        err_str = str(e)
        # Both invalid_grant (403) and 400 Bad Request from oauth2.googleapis.com
        # signal dead credentials. Move to next account.
        if 'invalid_grant' in err_str or '400' in err_str:
            print(f"Account {account}: dead token ({err_str[:80]})")
        else:
            print(f"Account {account}: unexpected error: {err_str[:80]}")
        continue

if calendar is None:
    print("DEGRADED: All OAuth tokens invalid. Cannot generate briefing.")
    sys.exit(1)

if working_account != ACCOUNTS_TO_TRY[0]:
    auth_fallback_used = True

print(f"Using account: {working_account}" + (" (FALLBACK)" if auth_fallback_used else ""))

# =============================================================================
# HELPERS
# =============================================================================
def to_min(hhmm):
    """Convert 'HH:MM' to minutes since midnight."""
    return int(hhmm[:2]) * 60 + int(hhmm[3:])

def span_minutes(start_hhmm, end_hhmm):
    """Return (start_min, end_min) for a timed event. Treat end <= start as
    crossing midnight (e.g. 19:30-00:00 -> end = 1440) so overlaps and busy
    spans compute correctly. Naive parsing of '00:00' as minute 0 hides real
    conflicts between a late event and an after-midnight event."""
    s = to_min(start_hhmm)
    e = to_min(end_hhmm)
    if e <= s:
        e += 1440
    return s, e

def fromisoformat_safe(s):
    """Parse ISO datetime string handling Z suffix and timezone offsets."""
    if s.endswith('Z'):
        s = s.replace('Z', '+00:00')
    try:
        return datetime.fromisoformat(s)
    except Exception:
        if 'T' in s and ('+' in s[10:] or s[10:].count('-') > 0):
            idx = s.rfind('+') if '+' in s[10:] else s.rfind('-', 10)
            base = s[:idx]
            tz = s[idx:]
            sign = 1 if tz[0] == '+' else -1
            hours = int(tz[1:3])
            minutes = int(tz[4:6])
            offset = timedelta(hours=sign * hours, minutes=sign * minutes)
            base_dt = datetime.fromisoformat(base)
            return base_dt.replace(tzinfo=timezone(offset))
        return datetime.fromisoformat(s)

# =============================================================================
# QUERY CALENDARS
# =============================================================================
all_events = []
calendar_errors = {}

for cal_id in CALENDAR_IDS:
    try:
        result = calendar.events().list(
            calendarId=cal_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            showDeleted=False,
            maxResults=250
        ).execute()
        events = result.get('items', [])
        for ev in events:
            ev['_source_calendar'] = cal_id
        all_events.extend(events)
        print(f"  {cal_id}: {len(events)} events")
    except Exception as e:
        calendar_errors[cal_id] = str(e)
        print(f"  {cal_id}: ERROR {e}")

work_busy_blocks = []
if WORK_CALENDAR_ID:
    try:
        result = calendar.events().list(
            calendarId=WORK_CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime',
            showDeleted=False,
            maxResults=250
        ).execute()
        for ev in result.get('items', []):
            if 'dateTime' in ev['start']:
                work_busy_blocks.append({
                    'start': ev['start']['dateTime'],
                    'end': ev['end']['dateTime']
                })
    except Exception as e:
        calendar_errors['work'] = str(e)

# =============================================================================
# DEDUPLICATION (case-insensitive summary + start time)
# =============================================================================
seen = {}
deduped_events = []

for ev in all_events:
    key = (
        ev.get('summary', '').strip().lower(),
        ev.get('start', {}).get('dateTime', ev.get('start', {}).get('date', ''))
    )
    if key in seen:
        continue
    seen[key] = ev
    deduped_events.append(ev)

all_events = deduped_events

# =============================================================================
# PARSE EVENTS
# =============================================================================
parsed_events = []

for ev in all_events:
    start_data = ev.get('start', {})
    end_data = ev.get('end', {})

    all_day = 'date' in start_data
    is_timed = 'dateTime' in start_data

    if is_timed:
        start_dt = fromisoformat_safe(start_data['dateTime'])
        end_dt = fromisoformat_safe(end_data['dateTime'])
        start_local = start_dt.astimezone(PDT)
        end_local = end_dt.astimezone(PDT)
        start_hhmm = start_local.strftime('%H:%M')
        end_hhmm = end_local.strftime('%H:%M')
        sort_key = f"{start_local.hour:02d}{start_local.minute:02d}"
    else:
        start_hhmm = "All day"
        end_hhmm = "All day"
        sort_key = "0000"

    cal_label = 'family' if 'family' in ev.get('_source_calendar', '') else 'personal'

    parsed_events.append({
        'summary': ev.get('summary', '(untitled)'),
        'description': ev.get('description', ''),
        'start': start_hhmm,
        'end': end_hhmm,
        'sort_key': sort_key,
        'location': ev.get('location'),
        'calendar': cal_label,
        'htmlLink': ev.get('htmlLink', ''),
        'all_day': all_day,
        'is_timed': is_timed,
        'attendees': ev.get('attendees', []),
        'organizer': ev.get('organizer', {}).get('email', ''),
        'start_data': start_data,
        'end_data': end_data,
    })

parsed_events.sort(key=lambda e: (0 if e['all_day'] else 1, e['sort_key']))

# =============================================================================
# CONFLICT DETECTION
# =============================================================================
timed_events = [e for e in parsed_events if e['is_timed']]
conflicts_detected = 0
event_conflict_notes = {}

for i in range(len(timed_events)):
    for j in range(i + 1, len(timed_events)):
        a = timed_events[i]
        b = timed_events[j]
        a_s, a_e = span_minutes(a['start'], a['end'])
        b_s, b_e = span_minutes(b['start'], b['end'])

        overlap_start = max(a_s, b_s)
        overlap_end = min(a_e, b_e)
        overlap_min = overlap_end - overlap_start

        if overlap_min > 0:
            conflicts_detected += 1
            event_conflict_notes.setdefault(id(a), []).append(
                f'Overlaps with "{b["summary"]}" ({overlap_min} min)')
            event_conflict_notes.setdefault(id(b), []).append(
                f'Overlaps with "{a["summary"]}" ({overlap_min} min)')

# =============================================================================
# PREPARATION SIGNALS
# =============================================================================
PREP_TITLE_KEYWORDS = [
    'review', 'prep', 'preparation', 'presentation', 'briefing', 'interview',
    'pitch', 'demo', 'proposal', 'debrief', 'kickoff', 'onboarding',
    'performance', 'evaluation', 'assessment', 'report', 'workshop', 'panel', 'keynote'
]

def check_prep_signals(event):
    """Returns (bool, reason_str) for whether event needs prep."""
    title_lower = event['summary'].lower()
    for kw in PREP_TITLE_KEYWORDS:
        if kw in title_lower:
            return True, f"'{kw}' in title"

    attendees = event.get('attendees', [])
    if len(attendees) >= 3:
        return True, f"{len(attendees)} attendees"
    if len(attendees) >= 1:
        for att in attendees:
            email = att.get('email', '')
            if email and '@' in email:
                domain = email.split('@')[1]
                if domain not in ('gmail.com',):
                    return True, "External attendee"

    if event.get('location'):
        return True, f"Location: {event['location'][:40]}"

    return False, ""

# =============================================================================
# FREE HOURS
# =============================================================================
def calc_free_hours(events, work_start="09:00", work_end="18:00"):
    ws = int(work_start[:2]) * 60 + int(work_start[3:])
    we = int(work_end[:2]) * 60 + int(work_end[3:])

    busy = []
    for ev in events:
        if not ev['is_timed']:
            continue
        s, e = span_minutes(ev['start'], ev['end'])
        busy.append((max(s, ws), min(e, we)))
    busy = [b for b in busy if b[1] > b[0]]

    if not busy:
        return (we - ws) / 60

    busy.sort()
    merged = []
    for s, e in busy:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], e))
        else:
            merged.append((s, e))

    total_busy = sum(max(0, e - s) for s, e in merged)
    return max(0, (we - ws - total_busy) / 60)

free_hours = calc_free_hours(parsed_events, WORKING_HOURS["start"], WORKING_HOURS["end"])

# =============================================================================
# BUILD OUTPUT
# =============================================================================
output_events = []
prep_count = 0
timed_starts = [e['start'] for e in parsed_events if e['is_timed']]
first_event_time = timed_starts[0] if timed_starts else ""
last_event_time = timed_events[-1]['end'] if timed_events else ""

for ev in parsed_events:
    is_conflict = id(ev) in event_conflict_notes
    conflict_note = "; ".join(event_conflict_notes[id(ev)]) if is_conflict else None
    prep_needed, prep_reason = check_prep_signals(ev)
    if prep_needed:
        prep_count += 1

    output_events.append({
        'title': ev['summary'],
        'start': ev['start'],
        'end': ev['end'],
        'location': ev.get('location'),
        'calendar': ev.get('calendar', 'personal'),
        'htmlLink': ev.get('htmlLink', ''),
        'all_day': ev['all_day'],
        'conflict': is_conflict,
        'conflict_note': conflict_note,
        'prep_required': prep_needed,
        'prep_note': prep_reason if prep_needed else None,
        'travel_before': False,
        'travel_minutes': None
    })

# =============================================================================
# SUMMARY NOTE
# =============================================================================
today_display = now.strftime('%A, %B %d, %Y')
total_events = len(parsed_events)

if total_events == 0:
    summary_note = f"Today is {today_display}. No events scheduled."
elif total_events == 1:
    only = parsed_events[0]
    summary_note = f"Today is {today_display}. One event: \"{only['summary']}\""
    if only['is_timed']:
        summary_note += f" at {only['start']}"
    summary_note += "."
else:
    time_range = ""
    if timed_events and first_event_time:
        time_range = f" from {first_event_time}"
        if last_event_time:
            time_range += f" to {last_event_time}"

    prep_str = ""
    if prep_count:
        prep_str = f". {prep_count} item{'s' if prep_count > 1 else ''} need preparation"

    conflict_str = ""
    if conflicts_detected:
        conflict_str = f". {conflicts_detected} conflict{'s' if conflicts_detected > 1 else ''} detected"

    summary_note = (
        f"Today is {today_display}. {total_events} events scheduled"
        f"{time_range}, ~{free_hours:.1f} free working hours"
        f"{prep_str}{conflict_str}."
    )

# =============================================================================
# OUTPUT
# =============================================================================
payload = {
    'brief_type': 'morning',
    'target_date': today_str,
    'summary_note': summary_note,
    'day_overview': {
        'total_events': total_events,
        'first_event': first_event_time,
        'last_event': last_event_time,
        'free_hours': round(free_hours, 1),
        'prep_items_count': prep_count
    },
    'events': output_events,
    'work_busy_blocks': [],
    'conflicts_detected': conflicts_detected,
    'prep_items_count': prep_count
}

with open('/tmp/sands_morning_briefing.json', 'w') as f:
    json.dump(payload, f, indent=2)

print(f"\n{'='*55}")
print(f"MORNING BRIEFING — {today_display}")
print(f"{'='*55}")
print(f"Events: {total_events} | Conflicts: {conflicts_detected} | Prep: {prep_count}")
print(f"Free hours: {free_hours:.1f}")
print(f"Auth: {working_account}" + (" (fallback)" if auth_fallback_used else ""))
if calendar_errors:
    print(f"Calendar errors: {list(calendar_errors.keys())}")
print(f"\n{summary_note}")
print(f"\nJSON: /tmp/sands_morning_briefing.json")
