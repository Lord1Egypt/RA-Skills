#!/usr/bin/env python3
"""
Log Analyzer — Parse application logs into actionable error digests.

Supports common log formats: syslog, JSON (structured), Apache/Nginx access/error,
Docker, Python traceback, Node.js, generic timestamped. Auto-detects format.

Usage:
    python3 analyze_logs.py <logfile_or_dir> [options]

Options:
    --format FORMAT     Force log format (auto|syslog|json|apache|nginx|python|node|docker|generic)
    --since TIMESPEC    Only include entries after this time (e.g., "1h", "24h", "2026-03-28")
    --severity LEVEL    Minimum severity to report (debug|info|warn|error|fatal) [default: warn]
    --top N             Show top N error patterns [default: 20]
    --output FORMAT     Output format (text|json|markdown) [default: text]
    --trends            Enable trend detection (frequency analysis over time)
    --group-by FIELD    Group errors by: message, file, service, hour [default: message]
    --ignore PATTERN    Regex pattern(s) to ignore (can be repeated)
    --context N         Lines of context around errors [default: 2]
    -q, --quiet         Only output the summary, skip individual entries
"""

import sys
import os
import re
import json
import hashlib
import argparse
from datetime import datetime, timedelta, timezone
from collections import Counter, defaultdict
from pathlib import Path


# ─── Log Format Detection & Parsing ────────────────────────────────────────

LOG_FORMATS = {
    'json': re.compile(r'^\s*\{.*"(?:level|severity|msg|message|log)"'),
    'syslog': re.compile(r'^(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+\s+\d+:\d+:\d+'),
    'syslog_iso': re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'),
    'apache_access': re.compile(r'^\d+\.\d+\.\d+\.\d+\s.*\s"\w+\s'),
    'apache_error': re.compile(r'^\[(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s'),
    'nginx_error': re.compile(r'^\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2}\s+\['),
    'python_traceback': re.compile(r'^Traceback \(most recent call last\)|^  File "'),
    'node_error': re.compile(r'(?:Error|TypeError|ReferenceError|SyntaxError):'),
    'docker': re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z\s'),
    'generic_timestamp': re.compile(r'^\[?\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}'),
}

SEVERITY_MAP = {
    'trace': 0, 'debug': 1, 'info': 2, 'notice': 2,
    'warn': 3, 'warning': 3,
    'error': 4, 'err': 4, 'critical': 5, 'crit': 5,
    'fatal': 5, 'emerg': 5, 'alert': 5, 'panic': 5,
}

SEVERITY_LABELS = {0: 'TRACE', 1: 'DEBUG', 2: 'INFO', 3: 'WARN', 4: 'ERROR', 5: 'FATAL'}

# HTTP status codes that indicate errors
HTTP_ERROR_CODES = {
    '400': ('WARN', 'Bad Request'),
    '401': ('WARN', 'Unauthorized'),
    '403': ('WARN', 'Forbidden'),
    '404': ('INFO', 'Not Found'),
    '405': ('WARN', 'Method Not Allowed'),
    '408': ('WARN', 'Request Timeout'),
    '429': ('WARN', 'Too Many Requests'),
    '500': ('ERROR', 'Internal Server Error'),
    '502': ('ERROR', 'Bad Gateway'),
    '503': ('ERROR', 'Service Unavailable'),
    '504': ('ERROR', 'Gateway Timeout'),
}


def detect_format(lines):
    """Auto-detect log format from first 20 non-empty lines."""
    sample = [l for l in lines[:50] if l.strip()][:20]
    scores = Counter()
    for line in sample:
        for fmt, pattern in LOG_FORMATS.items():
            if pattern.search(line):
                scores[fmt] += 1
    if not scores:
        return 'generic_timestamp'
    return scores.most_common(1)[0][0]


def parse_severity(text):
    """Extract severity level from text. Returns int 0-5."""
    if not text:
        return 2  # default INFO
    t = text.lower().strip()
    return SEVERITY_MAP.get(t, 2)


def parse_timestamp(text, fmt=None):
    """Best-effort timestamp parsing. Returns datetime or None."""
    if not text:
        return None
    text = text.strip()
    # ISO 8601
    for pattern in [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S,%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%d/%b/%Y:%H:%M:%S %z',
        '%d/%b/%Y:%H:%M:%S',
    ]:
        try:
            return datetime.strptime(text, pattern)
        except (ValueError, OverflowError):
            continue
    # Syslog (no year) — assume current year
    for pattern in ['%b %d %H:%M:%S', '%b  %d %H:%M:%S']:
        try:
            dt = datetime.strptime(text, pattern)
            return dt.replace(year=datetime.now().year)
        except (ValueError, OverflowError):
            continue
    return None


class LogEntry:
    __slots__ = ('timestamp', 'severity', 'message', 'source', 'raw', 'line_num', 'extra')

    def __init__(self, timestamp=None, severity=2, message='', source='', raw='', line_num=0, extra=None):
        self.timestamp = timestamp
        self.severity = severity
        self.message = message
        self.source = source
        self.raw = raw
        self.line_num = line_num
        self.extra = extra or {}


def parse_json_line(line, line_num):
    """Parse a JSON-formatted log line."""
    try:
        obj = json.loads(line)
    except (json.JSONDecodeError, ValueError):
        return None

    msg = obj.get('msg') or obj.get('message') or obj.get('log') or obj.get('text') or ''
    sev_raw = obj.get('level') or obj.get('severity') or obj.get('loglevel') or 'info'
    ts_raw = obj.get('timestamp') or obj.get('time') or obj.get('ts') or obj.get('@timestamp') or ''
    source = obj.get('service') or obj.get('source') or obj.get('logger') or obj.get('name') or ''

    if isinstance(sev_raw, int):
        # Some loggers use numeric levels (bunyan: 50=error, 40=warn, 30=info)
        if sev_raw >= 50:
            severity = 4
        elif sev_raw >= 40:
            severity = 3
        elif sev_raw >= 30:
            severity = 2
        elif sev_raw >= 20:
            severity = 1
        else:
            severity = 0
    else:
        severity = parse_severity(str(sev_raw))

    ts = None
    if isinstance(ts_raw, (int, float)):
        try:
            if ts_raw > 1e12:  # milliseconds
                ts = datetime.fromtimestamp(ts_raw / 1000)
            else:
                ts = datetime.fromtimestamp(ts_raw)
        except (OSError, OverflowError, ValueError):
            pass
    else:
        ts = parse_timestamp(str(ts_raw))

    return LogEntry(
        timestamp=ts, severity=severity, message=str(msg),
        source=str(source), raw=line, line_num=line_num, extra=obj
    )


# Syslog: "Mar 28 02:31:00 hostname service[pid]: message"
SYSLOG_RE = re.compile(
    r'^(\w{3}\s+\d+\s+\d+:\d+:\d+)\s+'  # timestamp
    r'(\S+)\s+'                            # hostname
    r'(\S+?)(?:\[\d+\])?:\s*'             # service
    r'(.*)$'                               # message
)

# Generic timestamped: "[2026-03-28 02:31:00] ERROR: message" or similar
GENERIC_RE = re.compile(
    r'^\[?(\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}[^\]]*)\]?\s*'  # timestamp
    r'(?:[-|]\s*)?'
    r'(?:(\w+)[-:|]\s*)?'  # optional severity
    r'(.*)$'               # message
)

# Nginx error: "2026/03/28 02:31:00 [error] 1234#0: message"
NGINX_ERR_RE = re.compile(
    r'^(\d{4}/\d{2}/\d{2}\s+\d{2}:\d{2}:\d{2})\s+'
    r'\[(\w+)\]\s+'
    r'(\d+#\d+:\s*.*)'
)

# Apache access log
APACHE_ACCESS_RE = re.compile(
    r'^(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"(\w+)\s+(\S+)\s+\S+"\s+(\d{3})\s+(\d+|-)'
)

# Severity keywords in message text
SEVERITY_KEYWORDS = re.compile(
    r'\b(FATAL|PANIC|EMERG|CRITICAL|CRIT|ERROR|ERR|WARNING|WARN|NOTICE|INFO|DEBUG|TRACE)\b',
    re.IGNORECASE
)


def parse_line(line, line_num, fmt):
    """Parse a single log line according to detected format."""
    line = line.rstrip('\n\r')
    if not line.strip():
        return None

    if fmt == 'json':
        return parse_json_line(line, line_num)

    if fmt == 'syslog':
        m = SYSLOG_RE.match(line)
        if m:
            ts = parse_timestamp(m.group(1))
            msg = m.group(4)
            sev_m = SEVERITY_KEYWORDS.search(msg)
            severity = parse_severity(sev_m.group(1)) if sev_m else 2
            return LogEntry(timestamp=ts, severity=severity, message=msg,
                            source=m.group(3), raw=line, line_num=line_num)

    if fmt == 'nginx_error':
        m = NGINX_ERR_RE.match(line)
        if m:
            ts = parse_timestamp(m.group(1).replace('/', '-'))
            severity = parse_severity(m.group(2))
            return LogEntry(timestamp=ts, severity=severity, message=m.group(3),
                            source='nginx', raw=line, line_num=line_num)

    if fmt == 'apache_access':
        m = APACHE_ACCESS_RE.match(line)
        if m:
            ts = parse_timestamp(m.group(2))
            status = m.group(5)
            method = m.group(3)
            path = m.group(4)
            msg = f'{method} {path} → {status}'
            if status in HTTP_ERROR_CODES:
                sev_label, desc = HTTP_ERROR_CODES[status]
                severity = parse_severity(sev_label)
                msg = f'{method} {path} → {status} {desc}'
            else:
                severity = 2 if status.startswith(('2', '3')) else 3
            return LogEntry(timestamp=ts, severity=severity, message=msg,
                            source=m.group(1), raw=line, line_num=line_num,
                            extra={'status': status, 'method': method, 'path': path})

    # Generic / fallback
    m = GENERIC_RE.match(line)
    if m:
        ts = parse_timestamp(m.group(1))
        sev_text = m.group(2) or ''
        msg = m.group(3) or line
        if sev_text and sev_text.lower() in SEVERITY_MAP:
            severity = parse_severity(sev_text)
        else:
            sev_m = SEVERITY_KEYWORDS.search(line)
            severity = parse_severity(sev_m.group(1)) if sev_m else 2
            if sev_text:
                msg = f'{sev_text}: {msg}'
        return LogEntry(timestamp=ts, severity=severity, message=msg,
                        raw=line, line_num=line_num)

    # Completely unstructured — try to extract severity from content
    sev_m = SEVERITY_KEYWORDS.search(line)
    severity = parse_severity(sev_m.group(1)) if sev_m else 2
    return LogEntry(severity=severity, message=line, raw=line, line_num=line_num)


def parse_python_traceback(lines, start_idx):
    """Collect a Python traceback starting from 'Traceback (most recent call last)'."""
    tb_lines = [lines[start_idx]]
    i = start_idx + 1
    while i < len(lines):
        line = lines[i]
        if line.startswith('  ') or line.startswith('\t') or (not line.strip()):
            tb_lines.append(line)
            i += 1
        elif re.match(r'^[A-Za-z][\w.]*(?:Error|Exception|Warning|Fault|Exists?):', line):
            tb_lines.append(line)
            i += 1
            break
        elif re.match(r'^[A-Za-z][\w.]*:\s', line) and not re.match(r'^\[?\d', line):
            # Catch other exception-like endings (DoesNotExist, etc.)
            tb_lines.append(line)
            i += 1
            break
        else:
            break
    message = tb_lines[-1].rstrip() if tb_lines else 'Unknown exception'
    raw = '\n'.join(l.rstrip() for l in tb_lines)
    return LogEntry(severity=4, message=message, raw=raw, line_num=start_idx + 1,
                    extra={'traceback': raw}), i


# ─── Analysis ──────────────────────────────────────────────────────────────

def normalize_message(msg):
    """Normalize a log message for grouping: replace variable parts with placeholders."""
    m = msg.strip()
    # Replace UUIDs
    m = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>', m, flags=re.I)
    # Replace hex hashes (8+ chars)
    m = re.sub(r'\b[0-9a-f]{8,64}\b', '<HASH>', m, flags=re.I)
    # Replace IP addresses
    m = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', m)
    # Replace numbers (but keep HTTP status codes in context)
    m = re.sub(r'(?<!\w)\d{5,}(?!\w)', '<NUM>', m)
    # Replace quoted strings
    m = re.sub(r'"[^"]{20,}"', '"<STR>"', m)
    m = re.sub(r"'[^']{20,}'", "'<STR>'", m)
    # Replace file paths
    m = re.sub(r'/[\w/.-]{20,}', '<PATH>', m)
    # Replace timestamps in messages
    m = re.sub(r'\d{4}-\d{2}-\d{2}[\sT]\d{2}:\d{2}:\d{2}[.\d]*', '<TIMESTAMP>', m)
    # Collapse whitespace
    m = re.sub(r'\s+', ' ', m).strip()
    return m


def fingerprint(msg):
    """Create a short fingerprint for grouping similar messages."""
    norm = normalize_message(msg)
    return hashlib.md5(norm.encode()).hexdigest()[:12]


def parse_since(spec):
    """Parse --since value. Returns datetime."""
    if not spec:
        return None
    # Relative: "1h", "24h", "30m", "7d"
    m = re.match(r'^(\d+)([mhd])$', spec.lower())
    if m:
        val = int(m.group(1))
        unit = m.group(2)
        delta = {'m': timedelta(minutes=val), 'h': timedelta(hours=val), 'd': timedelta(days=val)}[unit]
        return datetime.now() - delta
    # Absolute
    return parse_timestamp(spec)


# ─── Recommendations ──────────────────────────────────────────────────────

KNOWN_PATTERNS = [
    (re.compile(r'out of memory|oom|memory allocation|cannot allocate', re.I),
     'Memory exhaustion detected. Check for memory leaks, increase limits, or add swap.'),
    (re.compile(r'connection refused|ECONNREFUSED', re.I),
     'Service dependency is down or unreachable. Check target service health and network/firewall rules.'),
    (re.compile(r'connection reset|ECONNRESET|broken pipe', re.I),
     'Connection dropped mid-request. May indicate upstream timeout, load balancer issues, or client disconnect.'),
    (re.compile(r'timeout|timed out|ETIMEDOUT|deadline exceeded', re.I),
     'Operation timed out. Check network latency, increase timeout values, or investigate slow dependency.'),
    (re.compile(r'disk full|no space left|ENOSPC', re.I),
     'Disk space exhausted. Clean up logs/temp files, increase volume size, or add log rotation.'),
    (re.compile(r'permission denied|EACCES|403 Forbidden', re.I),
     'Permission issue. Check file permissions, IAM roles, or API key scopes.'),
    (re.compile(r'too many open files|EMFILE|ENFILE', re.I),
     'File descriptor limit reached. Increase ulimit or check for file handle leaks.'),
    (re.compile(r'SSL|TLS|certificate|handshake fail', re.I),
     'SSL/TLS issue. Check certificate expiry, chain validity, or protocol compatibility.'),
    (re.compile(r'authentication fail|unauthorized|401|invalid token|invalid credentials', re.I),
     'Authentication failure. Check credentials, token expiry, or auth service health.'),
    (re.compile(r'rate limit|429|throttl', re.I),
     'Rate limited by upstream service. Implement backoff/retry or request quota increase.'),
    (re.compile(r'segfault|segmentation fault|SIGSEGV|core dump', re.I),
     'Process crash (segfault). Check for native module issues, update dependencies, or inspect core dump.'),
    (re.compile(r'database.*lock|deadlock|lock wait timeout', re.I),
     'Database lock contention. Review transaction isolation, query patterns, or add indexes.'),
    (re.compile(r'DNS.*fail|ENOTFOUND|name.*resolution', re.I),
     'DNS resolution failure. Check DNS configuration, /etc/resolv.conf, or target hostname.'),
    (re.compile(r'502 Bad Gateway|503 Service Unavailable|504 Gateway Timeout', re.I),
     'Upstream service error. Check backend health, load balancer config, and backend capacity.'),
    (re.compile(r'stack overflow|maximum call stack', re.I),
     'Stack overflow — likely infinite recursion. Check recursive function calls.'),
]


def get_recommendation(message):
    """Match a message against known error patterns and return recommendation."""
    for pattern, rec in KNOWN_PATTERNS:
        if pattern.search(message):
            return rec
    return None


# ─── Main Logic ────────────────────────────────────────────────────────────

def read_log_file(filepath):
    """Read a log file, handling common encodings."""
    for enc in ['utf-8', 'latin-1', 'ascii']:
        try:
            with open(filepath, 'r', encoding=enc, errors='replace') as f:
                return f.readlines()
        except (UnicodeDecodeError, PermissionError):
            continue
    return []


def collect_files(path):
    """Collect log files from a path (file or directory)."""
    p = Path(path)
    if p.is_file():
        return [p]
    if p.is_dir():
        files = []
        for ext in ['*.log', '*.log.*', '*.txt', '*.err', '*.out']:
            files.extend(p.rglob(ext))
        # Also grab files without extension that look like logs
        for f in p.iterdir():
            if f.is_file() and f.suffix == '' and f.name not in ('README', 'LICENSE', 'Makefile'):
                files.append(f)
        return sorted(set(files))
    return []


def analyze(entries, args):
    """Analyze parsed log entries and produce digest."""
    min_sev = parse_severity(args.severity)
    since = parse_since(args.since)

    # Filter
    filtered = []
    for e in entries:
        if e.severity < min_sev:
            continue
        if since and e.timestamp and e.timestamp < since:
            continue
        if args.ignore:
            skip = False
            for pat in args.ignore:
                if re.search(pat, e.message, re.I):
                    skip = True
                    break
            if skip:
                continue
        filtered.append(e)

    # Group by normalized message
    groups = defaultdict(list)
    for e in filtered:
        fp = fingerprint(e.message)
        groups[fp].append(e)

    # Build pattern summaries
    patterns = []
    for fp, group_entries in groups.items():
        sample = group_entries[0]
        count = len(group_entries)
        max_sev = max(e.severity for e in group_entries)
        timestamps = [e.timestamp for e in group_entries if e.timestamp]

        first_seen = min(timestamps) if timestamps else None
        last_seen = max(timestamps) if timestamps else None

        # Trend: frequency over time buckets
        hourly = Counter()
        if timestamps:
            for ts in timestamps:
                hourly[ts.strftime('%Y-%m-%d %H:00')] += 1

        rec = get_recommendation(sample.message)

        patterns.append({
            'fingerprint': fp,
            'message': sample.message,
            'normalized': normalize_message(sample.message),
            'count': count,
            'severity': max_sev,
            'severity_label': SEVERITY_LABELS.get(max_sev, 'UNKNOWN'),
            'first_seen': first_seen,
            'last_seen': last_seen,
            'sources': list(set(e.source for e in group_entries if e.source))[:5],
            'sample_lines': [e.line_num for e in group_entries[:5]],
            'hourly_trend': dict(sorted(hourly.items())),
            'recommendation': rec,
            'sample_raw': sample.raw[:500],
        })

    # Sort by severity desc, then count desc
    patterns.sort(key=lambda p: (-p['severity'], -p['count']))

    # Truncate to top N
    top_n = args.top
    patterns = patterns[:top_n]

    # Overall stats
    sev_counts = Counter(e.severity for e in filtered)
    total_entries = len(entries)
    filtered_count = len(filtered)
    time_range = None
    all_ts = [e.timestamp for e in entries if e.timestamp]
    if all_ts:
        time_range = (min(all_ts), max(all_ts))

    return {
        'total_lines': total_entries,
        'filtered_count': filtered_count,
        'severity_counts': {SEVERITY_LABELS.get(k, 'UNKNOWN'): v for k, v in sorted(sev_counts.items(), reverse=True)},
        'time_range': time_range,
        'patterns': patterns,
        'top_n': top_n,
    }


# ─── Output Formatters ────────────────────────────────────────────────────

def format_text(result, args):
    """Format analysis result as human-readable text."""
    out = []
    out.append('=' * 60)
    out.append('  LOG ANALYSIS REPORT')
    out.append('=' * 60)
    out.append('')

    # Stats
    out.append(f'Total lines parsed: {result["total_lines"]:,}')
    out.append(f'Entries matching filters: {result["filtered_count"]:,}')
    if result['time_range']:
        t0, t1 = result['time_range']
        out.append(f'Time range: {t0.strftime("%Y-%m-%d %H:%M")} → {t1.strftime("%Y-%m-%d %H:%M")}')

    # Severity breakdown
    out.append('')
    out.append('Severity breakdown:')
    for label, count in result['severity_counts'].items():
        bar = '█' * min(count, 50)
        out.append(f'  {label:>6}: {count:>6}  {bar}')

    # Patterns
    out.append('')
    out.append(f'─── Top {result["top_n"]} Error Patterns ───')
    out.append('')

    for i, p in enumerate(result['patterns'], 1):
        sev = p['severity_label']
        out.append(f'[{sev}] #{i} — {p["count"]:,}x occurrences')
        out.append(f'  Message: {p["message"][:200]}')
        if p['sources']:
            out.append(f'  Sources: {", ".join(p["sources"])}')
        if p['first_seen']:
            out.append(f'  First seen: {p["first_seen"].strftime("%Y-%m-%d %H:%M:%S")}')
        if p['last_seen']:
            out.append(f'  Last seen:  {p["last_seen"].strftime("%Y-%m-%d %H:%M:%S")}')
        if p['sample_lines']:
            out.append(f'  Sample lines: {", ".join(str(l) for l in p["sample_lines"])}')

        # Trend
        if args.trends and p['hourly_trend']:
            trend_str = '  Trend: '
            for hour, cnt in list(p['hourly_trend'].items())[-8:]:
                trend_str += f'{hour.split(" ")[1]}:{cnt} '
            out.append(trend_str.rstrip())

        # Recommendation
        if p['recommendation']:
            out.append(f'  → Recommendation: {p["recommendation"]}')

        out.append('')

    # Summary
    out.append('─── Summary ───')
    fatal = result['severity_counts'].get('FATAL', 0)
    errors = result['severity_counts'].get('ERROR', 0)
    warns = result['severity_counts'].get('WARN', 0)

    if fatal > 0:
        out.append(f'🔴 CRITICAL: {fatal} fatal entries — immediate attention required!')
    if errors > 0:
        out.append(f'🟠 {errors} errors found — review top patterns above')
    if warns > 0:
        out.append(f'🟡 {warns} warnings — monitor for escalation')
    if fatal == 0 and errors == 0:
        out.append('🟢 No errors detected in the analyzed window')

    out.append('')
    return '\n'.join(out)


def format_json(result, args):
    """Format analysis result as JSON."""
    # Make datetime serializable
    def serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return str(obj)

    output = {
        'total_lines': result['total_lines'],
        'filtered_count': result['filtered_count'],
        'severity_counts': result['severity_counts'],
        'time_range': {
            'start': result['time_range'][0].isoformat() if result['time_range'] else None,
            'end': result['time_range'][1].isoformat() if result['time_range'] else None,
        },
        'patterns': [],
    }
    for p in result['patterns']:
        output['patterns'].append({
            'fingerprint': p['fingerprint'],
            'severity': p['severity_label'],
            'count': p['count'],
            'message': p['message'][:500],
            'normalized': p['normalized'][:300],
            'sources': p['sources'],
            'first_seen': p['first_seen'].isoformat() if p['first_seen'] else None,
            'last_seen': p['last_seen'].isoformat() if p['last_seen'] else None,
            'hourly_trend': p['hourly_trend'],
            'recommendation': p['recommendation'],
        })
    return json.dumps(output, indent=2, default=serialize)


def format_markdown(result, args):
    """Format analysis result as Markdown."""
    out = []
    out.append('# Log Analysis Report')
    out.append('')
    out.append(f'**Total lines:** {result["total_lines"]:,} | **Matched:** {result["filtered_count"]:,}')
    if result['time_range']:
        t0, t1 = result['time_range']
        out.append(f'**Time range:** {t0.strftime("%Y-%m-%d %H:%M")} → {t1.strftime("%Y-%m-%d %H:%M")}')
    out.append('')

    # Severity table
    out.append('## Severity Breakdown')
    out.append('| Level | Count |')
    out.append('|-------|-------|')
    for label, count in result['severity_counts'].items():
        out.append(f'| {label} | {count:,} |')
    out.append('')

    # Patterns
    out.append(f'## Top {result["top_n"]} Error Patterns')
    out.append('')

    for i, p in enumerate(result['patterns'], 1):
        sev = p['severity_label']
        out.append(f'### {i}. [{sev}] {p["count"]:,}x — {p["message"][:120]}')
        if p['sources']:
            out.append(f'**Sources:** {", ".join(p["sources"])}')
        if p['first_seen']:
            out.append(f'**First seen:** {p["first_seen"].strftime("%Y-%m-%d %H:%M:%S")}')
        if p['last_seen']:
            out.append(f'**Last seen:** {p["last_seen"].strftime("%Y-%m-%d %H:%M:%S")}')
        if p['recommendation']:
            out.append(f'> **Recommendation:** {p["recommendation"]}')
        out.append('')

    return '\n'.join(out)


# ─── Entry Point ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Analyze application logs and produce error digests.')
    parser.add_argument('path', help='Log file or directory to analyze')
    parser.add_argument('--format', dest='log_format', default='auto',
                        help='Log format (auto|syslog|json|apache|nginx|python|node|docker|generic)')
    parser.add_argument('--since', default=None, help='Only include entries after this time (e.g., 1h, 24h, 2026-03-28)')
    parser.add_argument('--severity', default='warn', help='Minimum severity (debug|info|warn|error|fatal)')
    parser.add_argument('--top', type=int, default=20, help='Top N error patterns to show')
    parser.add_argument('--output', default='text', help='Output format (text|json|markdown)')
    parser.add_argument('--trends', action='store_true', help='Enable hourly trend detection')
    parser.add_argument('--group-by', default='message', help='Group by: message, file, service, hour')
    parser.add_argument('--ignore', action='append', default=[], help='Regex pattern(s) to ignore')
    parser.add_argument('--context', type=int, default=2, help='Lines of context around errors')
    parser.add_argument('-q', '--quiet', action='store_true', help='Summary only')

    args = parser.parse_args()

    # Collect files
    files = collect_files(args.path)
    if not files:
        print(f'Error: No log files found at {args.path}', file=sys.stderr)
        sys.exit(1)

    print(f'Scanning {len(files)} file(s)...', file=sys.stderr)

    # Parse all entries
    all_entries = []
    for fpath in files:
        lines = read_log_file(str(fpath))
        if not lines:
            continue

        fmt = args.log_format
        if fmt == 'auto':
            fmt = detect_format(lines)

        i = 0
        while i < len(lines):
            line = lines[i]
            # Handle Python tracebacks specially
            if LOG_FORMATS['python_traceback'].search(line):
                entry, i = parse_python_traceback(lines, i)
                if entry:
                    entry.source = str(fpath.name)
                    all_entries.append(entry)
                continue

            entry = parse_line(line, i + 1, fmt)
            if entry:
                if not entry.source:
                    entry.source = str(fpath.name)
                all_entries.append(entry)
            i += 1

    if not all_entries:
        print('No log entries found.', file=sys.stderr)
        sys.exit(0)

    print(f'Parsed {len(all_entries):,} entries. Analyzing...', file=sys.stderr)

    # Analyze
    result = analyze(all_entries, args)

    # Format output
    formatters = {
        'text': format_text,
        'json': format_json,
        'markdown': format_markdown,
    }
    formatter = formatters.get(args.output, format_text)
    print(formatter(result, args))

    # Exit code based on findings
    fatal = result['severity_counts'].get('FATAL', 0)
    errors = result['severity_counts'].get('ERROR', 0)
    if fatal > 0:
        sys.exit(2)
    elif errors > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
