#!/usr/bin/env python3
"""
Test suite for add-event.py - Pure logic & boundary testing.
Run: python test_add_event.py
"""
import sys

# Force UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import json, os, tempfile
import importlib.util
from datetime import timedelta, datetime as _dt
from pathlib import Path
from unittest.mock import patch, MagicMock
from zoneinfo import ZoneInfo

# Load add-event.py (hyphenated filename cannot be normal import)
script_path = Path(__file__).parent / 'scripts' / 'add-event.py'
spec = importlib.util.spec_from_file_location('add_event', script_path)
add_event = importlib.util.module_from_spec(spec)
spec.loader.exec_module(add_event)

# Convenience aliases
parse_dt                = add_event.parse_dt
parse_date_range_for_query = add_event.parse_date_range_for_query
escape_ical             = add_event.escape_ical
sanitize_for_log        = add_event.sanitize_for_log
build_ical              = add_event.build_ical
find_calendar           = add_event.find_calendar
_new_uid                = add_event._new_uid
_validate_rrule         = add_event._validate_rrule
build_vevent            = add_event.build_vevent
build_vtimezone         = add_event.build_vtimezone
_get_tz_abbr            = add_event._get_tz_abbr
_format_offset          = add_event._format_offset
extract_event           = add_event.extract_event
search_events           = add_event.search_events

ELLIPSIS = chr(8230)  # Unicode ellipsis …

pass_count = 0
fail_count = 0

def eq(got, expected, label=''):
    global pass_count, fail_count
    if got == expected:
        pass_count += 1
    else:
        fail_count += 1
        print(f'  FAIL {label}: got={repr(got)}, expected={repr(expected)}')

def check(cond, label=''):
    global pass_count, fail_count
    if cond:
        pass_count += 1
    else:
        fail_count += 1
        print(f'  FAIL {label}: assertion failed')

def section(name):
    print(f'\n{"="*60}')
    print(f'  {name}')
    print(f'{"="*60}')

# ==================================================================
# 1. parse_dt
# ==================================================================
section('1. parse_dt -- time parsing boundaries')

tz = ZoneInfo('Asia/Shanghai')

dt, ad = parse_dt('2026-04-08T15:30:00', tz)
check(dt is not None, 'datetime with seconds')
eq(ad, False, 'not all-day')

dt, ad = parse_dt('2026-04-08T15:30', tz)
check(dt is not None, 'datetime without seconds')
eq(ad, False)

dt, ad = parse_dt('2026-04-08 15:30:00', tz)
check(dt is not None, 'space-separated datetime')
eq(ad, False)

dt, ad = parse_dt('2026-04-08', tz)
check(dt is not None, 'date only')
eq(ad, True, 'all-day detected for pure date')
eq(dt.hour, 0)
eq(dt.minute, 0)

dt, ad = parse_dt('2026\xe5\xb9\xb44\xe6\x9c\x888\xe6\x97\xa5 15:30', tz)
if dt is None:
    # The above is raw bytes; let's use the actual string
    dt, ad = parse_dt('2026\u5e744\u67088\u65e5 15:30', tz)
check(dt is not None, 'Chinese date format')
eq(dt.month, 4)
eq(dt.day, 8)

eq(parse_dt('', tz)[0], None, 'empty string')
eq(parse_dt(None, tz)[0], None, 'None input')

dt, _ = parse_dt('not-a-date', tz)
eq(dt, None, 'invalid date string')

dt, _ = parse_dt('2024-02-29T10:00:00', tz)
check(dt is not None, 'leap year date accepted')

dt, _ = parse_dt('2026-02-29T10:00:00', tz)
eq(dt, None, 'non-leap Feb 29 rejected')

# ==================================================================
# 2. parse_date_range_for_query
# ==================================================================
section('2. parse_date_range_for_query -- relative date boundaries')

tz = ZoneInfo('Asia/Shanghai')

s, e = parse_date_range_for_query('today', tz)
check(s is not None, 'today parses')
check(e == s + timedelta(days=1), 'today +1 day')

s, e = parse_date_range_for_query('tomorrow', tz)
check(s is not None, 'tomorrow parses')

s, e = parse_date_range_for_query('week', tz)
check(s is not None, 'week parses')
eq(s.weekday(), 0, 'week starts on Monday')

s, e = parse_date_range_for_query('nextweek', tz)
check(s is not None, 'nextweek parses')

s, e = parse_date_range_for_query('month', tz)
check(s is not None, 'month parses')
eq(s.day, 1, 'month starts on 1st')

s, e = parse_date_range_for_query('nextmonth', tz)
check(s is not None, 'nextmonth parses')

s, e = parse_date_range_for_query('2026-04-01~2026-04-30', tz)
check(s is not None, 'range parses')
eq(s.day, 1)
check(e.day == 1 and e.month == 5, 'range end is May 1')

s, e = parse_date_range_for_query('invalid', tz)
eq(s, None, 'invalid query returns None')

# Single date
s, e = parse_date_range_for_query('2026-12-31', tz)
check(s is not None, 'single date parses')
eq(s.month, 12)
eq(s.day, 31)

# Year boundary: nextmonth from December should not produce month 13
now_mock = _dt(2026, 12, 31, 12, 0, tzinfo=tz)
with patch.object(add_event, 'datetime', wraps=_dt) as mock_dt:
    mock_dt.now.return_value = now_mock
    s, e = parse_date_range_for_query('thismonth', tz)
    check(s is not None, 'thismonth on Dec 31')
    eq(s.month, 12)
    eq(e.month, 1, 'next month is January')
    eq(e.year, 2027, 'year wraps to 2027')

# ==================================================================
# 3. _validate_rrule
# ==================================================================
section('3. _validate_rrule -- RRULE validation')

eq(_validate_rrule('FREQ=WEEKLY;BYDAY=MO'), 'FREQ=WEEKLY;BYDAY=MO')
eq(_validate_rrule('FREQ=DAILY'), 'FREQ=DAILY')
eq(_validate_rrule('FREQ=MONTHLY;BYMONTHDAY=1'), 'FREQ=MONTHLY;BYMONTHDAY=1')
eq(_validate_rrule(''), '')
eq(_validate_rrule('  FREQ=DAILY  '), 'FREQ=DAILY', 'strips whitespace')
eq(_validate_rrule('freq=daily'), 'freq=daily', 'case preserved')

try:
    _validate_rrule('INVALID')
    fail_count += 1
    print('  FAIL INVALID should raise ValueError')
except ValueError:
    pass_count += 1

try:
    _validate_rrule('FREQ=DAILY;DROP!TABLE')
    fail_count += 1
    print('  FAIL special chars should raise ValueError')
except ValueError:
    pass_count += 1

# ==================================================================
# 4. escape_ical
# ==================================================================
section('4. escape_ical -- RFC 5545 escaping')

eq(escape_ical('Hello; World'), 'Hello\\; World')
eq(escape_ical('Line1\nLine2'), 'Line1\\nLine2')
eq(escape_ical('Cats, Dogs'), 'Cats\\, Dogs')
eq(escape_ical('Back\\slash'), 'Back\\\\slash')
eq(escape_ical(''), '')
eq(escape_ical('a;b,c\nd'), 'a\\;b\\,c\\nd', 'multiple escapes')

# ==================================================================
# 5. sanitize_for_log
# ==================================================================
section('5. sanitize_for_log -- log sanitization')

eq(sanitize_for_log('short'), 'short')
eq(sanitize_for_log('a' * 30), 'a' * 30)
eq(sanitize_for_log('a' * 50, max_len=30), 'a' * 30 + ELLIPSIS)
eq(sanitize_for_log(''), '')

sensitive = 'SecretMeetingWithPassword12345xyz'
eq(sanitize_for_log(sensitive), 'SecretMeetingWithPassword12345' + ELLIPSIS, 'sensitive text truncated at 30 chars')

# ==================================================================
# 6. _new_uid
# ==================================================================
section('6. _new_uid -- UID uniqueness')

u1 = _new_uid()
u2 = _new_uid()
check(u1 != u2, 'UIDs are unique')
check(u1.endswith('@openclaw.icloud'), 'UID suffix correct')

# ==================================================================
# 7. build_vtimezone -- DST-safe dynamic offset
# ==================================================================
section('7. build_vtimezone -- DST-safe dynamic offset')

# America/New_York summer (EDT = -0400)
ny_summer = _dt(2026, 7, 15, 12, 0, tzinfo=ZoneInfo('America/New_York'))
off = _format_offset(ny_summer)
eq(off, '-0400', 'NY summer EDT = -0400')

# America/New_York winter (EST = -0500)
ny_winter = _dt(2026, 1, 15, 12, 0, tzinfo=ZoneInfo('America/New_York'))
off = _format_offset(ny_winter)
eq(off, '-0500', 'NY winter EST = -0500')

# Europe/London summer (BST = +0100)
lon_summer = _dt(2026, 7, 15, 12, 0, tzinfo=ZoneInfo('Europe/London'))
off = _format_offset(lon_summer)
eq(off, '+0100', 'London summer BST = +0100')

# Europe/London winter (GMT = +0000)
lon_winter = _dt(2026, 1, 15, 12, 0, tzinfo=ZoneInfo('Europe/London'))
off = _format_offset(lon_winter)
eq(off, '+0000', 'London winter GMT = +0000')

# Shanghai no DST
sh_summer = _dt(2026, 7, 15, 12, 0, tzinfo=ZoneInfo('Asia/Shanghai'))
off = _format_offset(sh_summer)
eq(off, '+0800', 'Shanghai always +0800')

lines = build_vtimezone('America/New_York', ny_summer)
ical_str = '\r\n'.join(lines)
check('TZID:America/New_York' in ical_str, 'VTIMEZONE has TZID')

# Unknown zone fallback
abbr = _get_tz_abbr('Antarctica/McMurdo')
eq(abbr, 'McMurdo', 'unknown zone abbr fallback')

# ==================================================================
# 8. build_ical -- timed vs all-day
# ==================================================================
section('8. build_ical -- timed vs all-day events')

tz_sh = ZoneInfo('Asia/Shanghai')
dt_s = _dt(2026, 4, 8, 15, 0, tzinfo=tz_sh)
dt_e = _dt(2026, 4, 8, 16, 0, tzinfo=tz_sh)

ical = build_ical('Meeting', dt_s, dt_e)
check('DTSTART;TZID=Asia/Shanghai:20260408T150000' in ical, 'timed DTSTART')
check('VTIMEZONE' in ical, 'has VTIMEZONE for timed')

# All-day
ical_allday = build_ical('Birthday', dt_s, dt_e, is_all_day=True)
check('DTSTART;VALUE=DATE:20260408' in ical_allday, 'all-day VALUE=DATE')
check('DTEND;VALUE=DATE:20260408' in ical_allday, 'all-day DTEND VALUE=DATE')

# ==================================================================
# 9. find_calendar
# ==================================================================
section('9. find_calendar -- calendar lookup')

cal_p = MagicMock(); cal_p.get_display_name.return_value = 'Personal'
cal_w = MagicMock(); cal_w.get_display_name.return_value = 'Work Calendar'

check(find_calendar([cal_p, cal_w], 'primary') is cal_p, 'primary -> first')
check(find_calendar([cal_p, cal_w], 'work') is cal_w, 'partial match "work"')
check(find_calendar([cal_p, cal_w], 'WORK') is cal_w, 'case insensitive')
check(find_calendar([cal_p, cal_w], '') is cal_p, 'empty -> first')

try:
    find_calendar([], 'x')
    fail_count += 1
    print('  FAIL empty list should raise ValueError')
except ValueError:
    pass_count += 1

# ==================================================================
# 10. Long text
# ==================================================================
section('10. Long text stress')

long_s = 'A' * 10000
long_d = 'B' * 10000
ical = build_ical(long_s, dt_s, dt_e, description=long_d)
check(f'SUMMARY:{long_s}' in ical, 'long summary in iCal')
check(f'DESCRIPTION:{long_d}' in ical, 'long description in iCal')

# But sanitized in logs
check(sanitize_for_log(long_s) == 'A' * 30 + ELLIPSIS, 'log sanitization truncates')

# ==================================================================
# 11. Alarm boundaries
# ==================================================================
section('11. Alarm parameter boundaries')

check('VALARM' not in build_ical('T', dt_s, dt_e, alarm_minutes=0), 'alarm=0 -> no VALARM')
check('VALARM' not in build_ical('T', dt_s, dt_e, alarm_minutes=-15), 'alarm=-15 -> no VALARM')
check('VALARM' not in build_ical('T', dt_s, dt_e, alarm_minutes=None), 'alarm=None -> no VALARM')
ical1 = build_ical('T', dt_s, dt_e, alarm_minutes=1)
check('VALARM' in ical1, 'alarm=1 -> has VALARM')
check('TRIGGER:-PT1M' in ical1, '1-minute trigger')

# ==================================================================
# 12. RFC 5545 compliance
# ==================================================================
section('12. RFC 5545 compliance')

ical2 = build_ical('M', dt_s, dt_e)
check('\r\n' in ical2, 'CRLF line endings')
bare_lf = ical2.replace('\r\n', '')
check('\n' not in bare_lf, 'no bare LF')
check('CALSCALE:GREGORIAN' in ical2)
check('VERSION:2.0' in ical2)
check('PRODID:' in ical2)
check('STATUS:CONFIRMED' in ical2)
check('DTSTAMP:' in ical2)

# ==================================================================
# 13. search_events error propagation
# ==================================================================
section('13. search_events -- error propagation')

cal_ok = MagicMock()
cal_ok.get_display_name.return_value = 'GoodCal'
cal_ok.date_search.return_value = []

cal_err = MagicMock()
cal_err.get_display_name.return_value = 'BadCal'
cal_err.date_search.side_effect = Exception('timeout')

tz_sh = ZoneInfo('Asia/Shanghai')
start = _dt(2026, 4, 1, tzinfo=tz_sh)
end = _dt(2026, 5, 1, tzinfo=tz_sh)

result = search_events([cal_ok, cal_err], tz_sh, start, end)
check('events' in result, "result has 'events'")
check('errors' in result, "result has 'errors'")
check(len(result['errors']) > 0, 'errors captured from failed calendar')
check(len(result['events']) == 0, 'events list is empty')

# ==================================================================
# 14. Security -- log sanitization with sensitive RRULE
# ==================================================================
section('14. Security -- injection prevention')

try:
    _validate_rrule('DROP TABLE; FREQ=DAILY')
    fail_count += 1
    print('  FAIL SQL injection in RRULE should raise')
except ValueError:
    pass_count += 1

# ==================================================================
# Summary
# ==================================================================
print(f'\n{"="*60}')
print(f'  Results')
print(f'{"="*60}')
total = pass_count + fail_count
print(f'  PASS: {pass_count}/{total}')
if fail_count > 0:
    print(f'  FAIL: {fail_count}/{total}')
else:
    print(f'  ALL PASS!')
print(f'{"="*60}')
