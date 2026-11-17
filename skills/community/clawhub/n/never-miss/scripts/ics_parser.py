# -*- coding: utf-8 -*-
"""RFC5545 (.ics) 子集解析与生成（需求 §6.5）。

解析：SUMMARY / DTSTART / DTEND / LOCATION / ORGANIZER / ATTENDEE / STATUS / RRULE。
- VALUE=DATE → all_day=True，start/end 为 'YYYY-MM-DD'
- 带 Z → 视为 UTC 并转换到配置时区；带 TZID 或裸时间 → 视为本地时间（不解析 VTIMEZONE，已知局限）
- STATUS:CANCELLED 或 METHOD:CANCELLED → cancelled=True（调用方丢弃）
- RRULE 存在 → rrule=True（仅取首次，runbook 说明）
生成：降级 .ics 输出（含 UID 与 VALARM；文本转义 + 75 字节折行）。
"""
import os
from datetime import datetime, timedelta, timezone

CRLF = '\r\n'


def _unfold(text):
    lines = []
    for raw in text.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        if raw[:1] in (' ', '\t') and lines:
            lines[-1] += raw[1:]
        else:
            lines.append(raw)
    return lines


def _split_prop(line):
    """'DTSTART;VALUE=DATE:20260912' → ('DTSTART', {params}, '20260912')。"""
    in_q = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_q = not in_q
        elif ch == ':' and not in_q:
            head, value = line[:i], line[i + 1:]
            parts = head.split(';')
            name = parts[0].strip().upper()
            params = {}
            for p in parts[1:]:
                if '=' in p:
                    k, v = p.split('=', 1)
                    params[k.strip().upper()] = v.strip().strip('"')
            return name, params, value
    return None, None, None


def _unescape(s):
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            n = s[i + 1]
            if n in ('n', 'N'):
                out.append('\n')
            elif n in ('\\', ';', ','):
                out.append(n)
            else:
                out.append(n)
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def _parse_dt(value, params, tz):
    """返回 (iso_str, all_day)。"""
    v = value.strip()
    if params.get('VALUE') == 'DATE' or (len(v) == 8 and v.isdigit()):
        return '%s-%s-%s' % (v[0:4], v[4:6], v[6:8]), True
    if len(v) >= 15 and v[8] == 'T':
        try:
            dt = datetime(int(v[0:4]), int(v[4:6]), int(v[6:8]),
                          int(v[8 + 1:10 + 1]), int(v[10 + 1:12 + 1]), int(v[12 + 1:14 + 1]))
        except ValueError:
            return None, False
        if v.endswith('Z'):
            dt = dt.replace(tzinfo=timezone.utc).astimezone(tz)
        else:
            dt = dt.replace(tzinfo=tz)  # TZID/裸时间视为本地时区（局限，见模块注释）
        return dt.isoformat(), False
    return None, False


def parse(text, tz):
    """解析 .ics 文本 → 事件列表。"""
    events, method = [], None
    cur = None
    for line in _unfold(text):
        if not line.strip():
            continue
        name, params, value = _split_prop(line)
        if name is None:
            continue
        if name == 'BEGIN' and value.strip().upper() == 'VEVENT':
            cur = {'title': '', 'start': None, 'end': None, 'all_day': False,
                   'location': '', 'organizer': '', 'attendees': [],
                   'cancelled': False, 'rrule': False}
            continue
        if name == 'END' and value.strip().upper() == 'VEVENT':
            if cur is not None and cur.get('start'):
                cur['cancelled'] = cur['cancelled'] or (method == 'CANCELLED')
                events.append(cur)
            cur = None
            continue
        if cur is None:
            if name == 'METHOD':
                method = value.strip().upper()
            continue
        if name == 'SUMMARY':
            cur['title'] = _unescape(value)
        elif name == 'DTSTART':
            iso, all_day = _parse_dt(value, params, tz)
            if iso:
                cur['start'], cur['all_day'] = iso, all_day
        elif name == 'DTEND':
            iso, _ = _parse_dt(value, params, tz)
            if iso:
                cur['end'] = iso
        elif name == 'LOCATION':
            cur['location'] = _unescape(value)
        elif name == 'ORGANIZER':
            cur['organizer'] = params.get('CN') or value.replace('mailto:', '')
        elif name == 'ATTENDEE':
            cur['attendees'].append(params.get('CN') or value.replace('mailto:', ''))
        elif name == 'STATUS' and value.strip().upper() == 'CANCELLED':
            cur['cancelled'] = True
        elif name == 'RRULE':
            cur['rrule'] = True
    return events


# ---------- 生成（降级输出） ----------

def _escape(s):
    return (str(s)
            .replace('\\', '\\\\')
            .replace(';', '\\;')
            .replace(',', '\\,')
            .replace('\n', '\\n'))


def _fold(line):
    """RFC5545：行 ≤75 字节（UTF-8），续行以空格开头。"""
    raw = line.encode('utf-8')
    if len(raw) <= 75:
        return [line]
    parts, cur, cur_len = [], [], 75
    for ch in line:
        b = len(ch.encode('utf-8'))
        if cur_len + b > 75:
            parts.append(''.join(cur))
            cur, cur_len = [ch], 1 + b
        else:
            cur.append(ch)
            cur_len += b
    if cur:
        parts.append(''.join(cur))
    return [parts[0]] + [' ' + p for p in parts[1:]]


def write_ics(path, event, uid, tz, reminder_lead_minutes=60, all_day_at='09:00'):
    """生成降级 .ics 文件（含 UID 与 VALARM）。返回文件路径。"""
    all_day = bool(event.get('all_day'))
    lines = [
        'BEGIN:VCALENDAR',
        'VERSION:2.0',
        'PRODID:-//never-miss//Schedule to Calendar//CN',
        'CALSCALE:GREGORIAN',
        'BEGIN:VEVENT',
        'UID:%s' % uid,
        'DTSTAMP:%s' % datetime.now(tz).strftime('%Y%m%dT%H%M%SZ'),
    ]
    if all_day:
        day = str(event['start'])[:10]
        lines.append('DTSTART;VALUE=DATE:%s' % day.replace('-', ''))
        # DTEND 对全天事件为排他日期：结束日=开始日（单日）或次日
        end_day = str(event.get('end') or day)[:10]
        if end_day == day:
            end_day = (datetime.strptime(day, '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
        lines.append('DTEND;VALUE=DATE:%s' % end_day.replace('-', ''))
    else:
        start = datetime.fromisoformat(str(event['start']))
        end = datetime.fromisoformat(str(event.get('end') or start + timedelta(hours=1)))
        lines.append('DTSTART:%s' % start.strftime('%Y%m%dT%H%M%S'))
        lines.append('DTEND:%s' % end.strftime('%Y%m%dT%H%M%S'))
    lines.append('SUMMARY:%s' % _escape(event.get('title', '')))
    if event.get('location'):
        lines.append('LOCATION:%s' % _escape(event['location']))
    if event.get('description'):
        lines.append('DESCRIPTION:%s' % _escape(event['description']))
    lines.append('BEGIN:VALARM')
    if all_day:
        day = str(event['start'])[:10]
        trigger = '%sT%s00' % (day.replace('-', ''), all_day_at.replace(':', ''))
        lines.append('TRIGGER;VALUE=DATE-TIME:%s' % trigger)
    else:
        lines.append('TRIGGER:-PT%dM' % int(reminder_lead_minutes))
    lines.extend(['ACTION:DISPLAY', 'DESCRIPTION:never-miss 提醒', 'END:VALARM'])
    lines.extend(['END:VEVENT', 'END:VCALENDAR'])
    folded = []
    for l in lines:
        folded.extend(_fold(l))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(CRLF.join(folded) + CRLF)
    return path
