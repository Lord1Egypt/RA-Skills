#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, time, timezone, timedelta
from pathlib import Path
from typing import Dict, Iterable, Optional

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

DEFAULT_AGENTS_BASE = Path.home() / '.openclaw' / 'agents'
METRIC_KEYS = ('input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages')


@dataclass(frozen=True)
class MsgKey:
    agent: str
    session_key: str
    msg_id: Optional[str]
    timestamp: str
    provider: str
    model: str
    input: int
    output: int
    cache_read: int
    cache_write: int
    total: int


@dataclass(frozen=True)
class TranscriptRef:
    agent: str
    path: Path
    session_key: str


def empty_metrics() -> Dict[str, int]:
    return {k: 0 for k in METRIC_KEYS}


def add_metrics(bucket: Dict[str, int], usage: Dict[str, int]) -> None:
    for k in METRIC_KEYS:
        bucket[k] = bucket.get(k, 0) + usage.get(k, 0)


def fmt_num(value: int) -> str:
    return f'{value:,}'


def pct(part: int, whole: int) -> str:
    if whole <= 0:
        return '0.0%'
    return f'{(part / whole) * 100:.1f}%'


def md_escape(value: object) -> str:
    text = str(value)
    return text.replace('|', '\\|').replace('\n', ' ')


def parse_local_dt(value: str, tz, is_end: bool) -> datetime:
    value = value.strip()
    parsed: Optional[datetime] = None
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d'):
        try:
            dt = datetime.strptime(value, fmt)
            if fmt == '%Y-%m-%d':
                dt = datetime.combine(dt.date(), time.max if is_end else time.min)
            parsed = dt.replace(tzinfo=tz)
            break
        except ValueError:
            continue
    if parsed is None:
        try:
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=tz)
            else:
                parsed = parsed.astimezone(tz)
        except ValueError as e:
            raise SystemExit(f'无法解析时间: {value}') from e
    return parsed


def resolve_tz(name: str):
    upper = name.upper()
    if upper in {'UTC+8', 'UTC+08:00', '+08:00', 'ASIA/SHANGHAI', 'SHANGHAI'}:
        return timezone(timedelta(hours=8))
    if upper in {'UTC', 'Z'}:
        return timezone.utc
    if ZoneInfo is None:
        raise SystemExit('当前 Python 不支持 zoneinfo；请改用 --tz UTC 或 --tz UTC+8')
    try:
        return ZoneInfo(name)
    except Exception as e:
        raise SystemExit(f'无法识别时区: {name}') from e


def normalize_usage(usage: dict) -> Dict[str, int]:
    return {
        'input': int(usage.get('input', 0) or 0),
        'output': int(usage.get('output', 0) or 0),
        'cacheRead': int(usage.get('cacheRead', 0) or 0),
        'cacheWrite': int(usage.get('cacheWrite', 0) or 0),
        'totalTokens': int(usage.get('totalTokens', 0) or 0),
        'messages': 1,
    }


def transcript_base_candidates(path: Path) -> list[str]:
    name = path.name
    out = [name]
    if '.jsonl' in name:
        base = name.split('.jsonl', 1)[0] + '.jsonl'
        if base not in out:
            out.append(base)
    return out


def load_session_index(agent_dir: Path) -> Dict[str, str]:
    sessions_path = agent_dir / 'sessions' / 'sessions.json'
    mapping: Dict[str, str] = {}
    if not sessions_path.exists():
        return mapping
    try:
        data = json.loads(sessions_path.read_text(encoding='utf-8'))
    except Exception:
        return mapping

    entries = []
    if isinstance(data, dict):
        sessions = data.get('sessions')
        if isinstance(sessions, list):
            entries = sessions
        elif isinstance(data.get('items'), list):
            entries = data.get('items')
    elif isinstance(data, list):
        entries = data

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        key = entry.get('key')
        session_file = entry.get('sessionFile')
        if not key or not session_file:
            continue
        try:
            basename = Path(str(session_file)).name
        except Exception:
            continue
        mapping[basename] = str(key)
        if '.jsonl' in basename:
            base = basename.split('.jsonl', 1)[0] + '.jsonl'
            mapping.setdefault(base, str(key))
    return mapping


def iter_transcript_files(base: Path) -> Iterable[TranscriptRef]:
    for agent_dir in sorted(base.iterdir()):
        if not agent_dir.is_dir():
            continue
        agent = agent_dir.name
        sess_dir = agent_dir / 'sessions'
        if not sess_dir.exists():
            continue
        session_index = load_session_index(agent_dir)
        for fp in sorted(sess_dir.iterdir()):
            if not fp.is_file() or fp.name == 'sessions.json' or '.jsonl' not in fp.name:
                continue
            session_key = None
            for candidate in transcript_base_candidates(fp):
                if candidate in session_index:
                    session_key = session_index[candidate]
                    break
            if not session_key:
                session_key = f'file:{fp.name}'
            yield TranscriptRef(agent=agent, path=fp, session_key=session_key)


def should_keep(provider: str, model: str, args) -> bool:
    if args.providers and provider not in args.providers:
        return False
    if args.models:
        full = f'{provider}/{model}'
        if model not in args.models and full not in args.models:
            return False
    return True


def sorted_metrics_map(data: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, int]]:
    return {
        key: dict(vals)
        for key, vals in sorted(data.items(), key=lambda kv: (-kv[1]['totalTokens'], kv[0]))
    }


def collect(base: Path, start_local: datetime, end_local: datetime, args) -> dict:
    start_utc = start_local.astimezone(timezone.utc)
    end_utc = end_local.astimezone(timezone.utc)

    summary = empty_metrics()
    by_day_agent = defaultdict(lambda: defaultdict(empty_metrics))
    by_agent = defaultdict(empty_metrics)
    by_model = defaultdict(empty_metrics)
    by_day_model = defaultdict(lambda: defaultdict(empty_metrics))
    by_session = defaultdict(empty_metrics)
    by_day_session = defaultdict(lambda: defaultdict(empty_metrics))
    session_meta: Dict[str, Dict[str, str]] = {}
    seen = set()

    for ref in iter_transcript_files(base):
        if args.agents and ref.agent not in args.agents:
            continue
        try:
            with ref.path.open('r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except Exception:
                        continue
                    if obj.get('type') != 'message':
                        continue
                    msg = obj.get('message') or {}
                    usage = msg.get('usage') or {}
                    if not usage:
                        continue
                    ts = obj.get('timestamp') or msg.get('timestamp')
                    if not ts:
                        continue
                    try:
                        dt = datetime.fromisoformat(str(ts).replace('Z', '+00:00'))
                    except Exception:
                        continue
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    dt_utc = dt.astimezone(timezone.utc)
                    if not (start_utc <= dt_utc <= end_utc):
                        continue

                    provider = str(msg.get('provider') or 'unknown')
                    model = str(msg.get('model') or 'unknown')
                    if not should_keep(provider, model, args):
                        continue

                    norm = normalize_usage(usage)
                    key = MsgKey(
                        agent=ref.agent,
                        session_key=ref.session_key,
                        msg_id=obj.get('id'),
                        timestamp=str(ts),
                        provider=provider,
                        model=model,
                        input=norm['input'],
                        output=norm['output'],
                        cache_read=norm['cacheRead'],
                        cache_write=norm['cacheWrite'],
                        total=norm['totalTokens'],
                    )
                    if key in seen:
                        continue
                    seen.add(key)

                    local_day = dt.astimezone(start_local.tzinfo).strftime('%Y-%m-%d')
                    model_key = f'{provider}/{model}'
                    session_meta.setdefault(ref.session_key, {'agent': ref.agent, 'transcript': ref.path.name})
                    add_metrics(summary, norm)
                    add_metrics(by_day_agent[local_day][ref.agent], norm)
                    add_metrics(by_agent[ref.agent], norm)
                    add_metrics(by_model[model_key], norm)
                    add_metrics(by_day_model[local_day][model_key], norm)
                    add_metrics(by_session[ref.session_key], norm)
                    add_metrics(by_day_session[local_day][ref.session_key], norm)
        except Exception:
            continue

    return {
        'assumption_timezone': str(start_local.tzinfo),
        'range_local': {'start': start_local.isoformat(), 'end': end_local.isoformat()},
        'summary': dict(summary),
        'by_day_agent': {
            day: {
                agent: dict(vals)
                for agent, vals in sorted(agents.items(), key=lambda kv: (-kv[1]['totalTokens'], kv[0]))
            }
            for day, agents in sorted(by_day_agent.items())
        },
        'by_agent': sorted_metrics_map(by_agent),
        'by_model': sorted_metrics_map(by_model),
        'by_day_model': {
            day: {
                model: dict(vals)
                for model, vals in sorted(models.items(), key=lambda kv: (-kv[1]['totalTokens'], kv[0]))
            }
            for day, models in sorted(by_day_model.items())
        },
        'by_session': {
            key: {**dict(vals), **session_meta.get(key, {})}
            for key, vals in sorted(by_session.items(), key=lambda kv: (-kv[1]['totalTokens'], kv[0]))
        },
        'by_day_session': {
            day: {
                key: {**dict(vals), **session_meta.get(key, {})}
                for key, vals in sorted(sessions.items(), key=lambda kv: (-kv[1]['totalTokens'], kv[0]))
            }
            for day, sessions in sorted(by_day_session.items())
        },
        'filters': {
            'agents': sorted(args.agents) if args.agents else [],
            'providers': sorted(args.providers) if args.providers else [],
            'models': sorted(args.models) if args.models else [],
        },
    }


def write_csv_exports(data: dict, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
        with path.open('w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        written.append(path)

    summary = data['summary']
    write_csv(
        out_dir / 'summary.csv',
        ['timezone', 'start', 'end', 'input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages'],
        [[
            data['assumption_timezone'], data['range_local']['start'], data['range_local']['end'],
            summary['input'], summary['output'], summary['cacheRead'], summary['cacheWrite'],
            summary['totalTokens'], summary['messages']
        ]],
    )

    rows = []
    for day, agents in data['by_day_agent'].items():
        for agent, m in agents.items():
            rows.append([day, agent, m['input'], m['output'], m['cacheRead'], m['cacheWrite'], m['totalTokens'], m['messages']])
    write_csv(out_dir / 'by_day_agent.csv', ['day', 'agent', 'input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages'], rows)

    rows = []
    for agent, m in data['by_agent'].items():
        rows.append([agent, m['input'], m['output'], m['cacheRead'], m['cacheWrite'], m['totalTokens'], m['messages']])
    write_csv(out_dir / 'by_agent.csv', ['agent', 'input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages'], rows)

    rows = []
    for model, m in data['by_model'].items():
        rows.append([model, m['input'], m['output'], m['cacheRead'], m['cacheWrite'], m['totalTokens'], m['messages']])
    write_csv(out_dir / 'by_model.csv', ['model', 'input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages'], rows)

    rows = []
    for session_key, m in data['by_session'].items():
        rows.append([m.get('agent', ''), session_key, m.get('transcript', ''), m['input'], m['output'], m['cacheRead'], m['cacheWrite'], m['totalTokens'], m['messages']])
    write_csv(out_dir / 'by_session.csv', ['agent', 'sessionKey', 'transcript', 'input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages'], rows)

    rows = []
    for day, sessions in data['by_day_session'].items():
        for session_key, m in sessions.items():
            rows.append([day, m.get('agent', ''), session_key, m.get('transcript', ''), m['input'], m['output'], m['cacheRead'], m['cacheWrite'], m['totalTokens'], m['messages']])
    write_csv(out_dir / 'by_day_session.csv', ['day', 'agent', 'sessionKey', 'transcript', 'input', 'output', 'cacheRead', 'cacheWrite', 'totalTokens', 'messages'], rows)

    return written


def build_findings(data: dict) -> list[str]:
    findings: list[str] = []
    total = data['summary']['totalTokens']
    by_agent = data['by_agent']
    by_model = data['by_model']
    by_day_agent = data['by_day_agent']
    summary = data['summary']

    if by_agent:
        top_agent, top_agent_metrics = next(iter(by_agent.items()))
        findings.append(f'主消耗集中在 `{top_agent}`，占总 token 的 {pct(top_agent_metrics["totalTokens"], total)}。')

    day_totals = []
    for day, agents in by_day_agent.items():
        day_total = sum(m['totalTokens'] for m in agents.values())
        day_totals.append((day, day_total))
    if day_totals:
        top_day, top_day_total = max(day_totals, key=lambda item: item[1])
        findings.append(f'最高峰出现在 `{top_day}`，当日消耗 {fmt_num(top_day_total)} tokens。')

    if by_model:
        top_model, top_model_metrics = next(iter(by_model.items()))
        findings.append(f'主要由模型 `{top_model}` 贡献，占总 token 的 {pct(top_model_metrics["totalTokens"], total)}。')

    interactive = summary['input'] + summary['output']
    if summary['cacheRead'] > interactive:
        findings.append('缓存读取量高于实时输入输出总和，说明这段时间上下文复用占比很高。')

    return findings


def render_markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    out = []
    out.append('| ' + ' | '.join(md_escape(h) for h in headers) + ' |')
    out.append('| ' + ' | '.join(['---'] * len(headers)) + ' |')
    for row in rows:
        out.append('| ' + ' | '.join(md_escape(v) for v in row) + ' |')
    return '\n'.join(out)


def generate_markdown(data: dict, top_sessions: int) -> str:
    summary = data['summary']
    total = summary['totalTokens']
    top_sessions = max(top_sessions, 5)
    lines = [
        '# OpenClaw Token Usage Report',
        '',
        '## Scope',
        f'- Timezone: `{data["assumption_timezone"]}`',
        f'- Range: `{data["range_local"]["start"]}` ~ `{data["range_local"]["end"]}`',
    ]

    filters = data.get('filters', {})
    if any(filters.values()):
        lines.extend([
            f'- Agents filter: `{", ".join(filters.get("agents", [])) or "all"}`',
            f'- Providers filter: `{", ".join(filters.get("providers", [])) or "all"}`',
            f'- Models filter: `{", ".join(filters.get("models", [])) or "all"}`',
        ])
    else:
        lines.append('- Filters: `all agents / all providers / all models`')

    lines.extend([
        '',
        '## Summary',
        f'- Total tokens: **{fmt_num(summary["totalTokens"])}**',
        f'- Input: {fmt_num(summary["input"])}',
        f'- Output: {fmt_num(summary["output"])}',
        f'- Cache read: {fmt_num(summary["cacheRead"])}',
        f'- Cache write: {fmt_num(summary["cacheWrite"])}',
        f'- Messages: {fmt_num(summary["messages"])}',
        '',
        '## By Day',
    ])

    day_rows = []
    for day, agents in data['by_day_agent'].items():
        day_total = sum(m['totalTokens'] for m in agents.values())
        top_agent = next(iter(agents.items())) if agents else ('-', {'totalTokens': 0})
        day_rows.append([day, fmt_num(day_total), top_agent[0], fmt_num(top_agent[1]['totalTokens'])])
    lines.append(render_markdown_table(['Day', 'Total Tokens', 'Top Agent', 'Top Agent Tokens'], day_rows))

    lines.extend(['', '## By Agent'])
    agent_rows = []
    for agent, m in data['by_agent'].items():
        agent_rows.append([agent, fmt_num(m['totalTokens']), pct(m['totalTokens'], total), fmt_num(m['messages'])])
    lines.append(render_markdown_table(['Agent', 'Tokens', 'Share', 'Messages'], agent_rows))

    lines.extend(['', '## By Model'])
    model_rows = []
    for model, m in data['by_model'].items():
        model_rows.append([model, fmt_num(m['totalTokens']), pct(m['totalTokens'], total), fmt_num(m['messages'])])
    lines.append(render_markdown_table(['Model', 'Tokens', 'Share', 'Messages'], model_rows))

    lines.extend(['', f'## Top Sessions (Top {top_sessions})'])
    session_rows = []
    for idx, (session_key, m) in enumerate(list(data['by_session'].items())[:top_sessions], start=1):
        session_rows.append([idx, m.get('agent', ''), session_key, fmt_num(m['totalTokens']), fmt_num(m['messages'])])
    lines.append(render_markdown_table(['Rank', 'Agent', 'Session', 'Tokens', 'Messages'], session_rows))

    findings = build_findings(data)
    if findings:
        lines.extend(['', '## Findings'])
        lines.extend([f'- {item}' for item in findings])

    if data.get('csv_exports'):
        lines.extend(['', '## CSV Exports'])
        lines.extend([f'- `{p}`' for p in data['csv_exports']])

    lines.append('')
    return '\n'.join(lines)


def print_summary(data: dict, top_sessions: int) -> None:
    s = data['summary']
    print(f"时区: {data['assumption_timezone']}")
    print(f"范围: {data['range_local']['start']} ~ {data['range_local']['end']}")
    print()
    print('总计')
    print(f"- totalTokens: {fmt_num(s['totalTokens'])}")
    print(f"- input:       {fmt_num(s['input'])}")
    print(f"- output:      {fmt_num(s['output'])}")
    print(f"- cacheRead:   {fmt_num(s['cacheRead'])}")
    print(f"- cacheWrite:  {fmt_num(s['cacheWrite'])}")
    print(f"- messages:    {fmt_num(s['messages'])}")
    print()

    print('按天 × agent')
    for day, agents in data['by_day_agent'].items():
        print(f'- {day}')
        for agent, m in agents.items():
            print(f"  - {agent}: {fmt_num(m['totalTokens'])} tokens (input {fmt_num(m['input'])}, output {fmt_num(m['output'])}, cacheRead {fmt_num(m['cacheRead'])}, messages {fmt_num(m['messages'])})")
    print()

    print('按 agent 汇总')
    total = s['totalTokens']
    for agent, m in data['by_agent'].items():
        print(f"- {agent}: {fmt_num(m['totalTokens'])} tokens ({pct(m['totalTokens'], total)})")
    print()

    print('按模型汇总')
    for model, m in data['by_model'].items():
        print(f"- {model}: {fmt_num(m['totalTokens'])} tokens ({pct(m['totalTokens'], total)})")

    if top_sessions > 0:
        print()
        print(f'Top {top_sessions} sessions')
        for idx, (session_key, m) in enumerate(list(data['by_session'].items())[:top_sessions], start=1):
            transcript = m.get('transcript', '')
            suffix = f' · {transcript}' if transcript else ''
            print(f"- {idx}. [{m.get('agent', 'unknown')}] {session_key}: {fmt_num(m['totalTokens'])} tokens{suffix}")


def main() -> None:
    ap = argparse.ArgumentParser(description='统计 OpenClaw transcript 中的 token 使用量')
    ap.add_argument('--from', dest='start', required=True, help='开始时间，如 2026-03-14 或 2026-03-14 00:00')
    ap.add_argument('--to', dest='end', required=True, help='结束时间，如 2026-03-16 或 2026-03-16 23:59')
    ap.add_argument('--tz', default='UTC+8', help='时区，默认 UTC+8；也可用 UTC 或 Asia/Shanghai')
    ap.add_argument('--base', default=str(DEFAULT_AGENTS_BASE), help='agents 根目录（默认 ~/.openclaw/agents）')
    ap.add_argument('--agents', help='逗号分隔的 agent 列表')
    ap.add_argument('--providers', help='逗号分隔的 provider 列表')
    ap.add_argument('--models', help='逗号分隔的 model 或 provider/model 列表')
    ap.add_argument('--top-sessions', type=int, default=0, help='显示 Top N session 排行；markdown 默认至少展示 Top 5')
    ap.add_argument('--format', choices=['summary', 'json', 'markdown'], default='summary')
    ap.add_argument('--output', help='输出到文件（summary/json/markdown）')
    ap.add_argument('--csv-dir', help='导出多份 CSV 到指定目录')
    args = ap.parse_args()

    tz = resolve_tz(args.tz)
    args.agents = {x.strip() for x in (args.agents or '').split(',') if x.strip()} or None
    args.providers = {x.strip() for x in (args.providers or '').split(',') if x.strip()} or None
    args.models = {x.strip() for x in (args.models or '').split(',') if x.strip()} or None

    start_local = parse_local_dt(args.start, tz, is_end=False)
    end_local = parse_local_dt(args.end, tz, is_end=True)
    if end_local < start_local:
        raise SystemExit('结束时间不能早于开始时间')

    data = collect(Path(args.base), start_local, end_local, args)
    if args.csv_dir:
        written = write_csv_exports(data, Path(args.csv_dir))
        data['csv_exports'] = [str(p) for p in written]

    if args.format == 'json':
        text = json.dumps(data, ensure_ascii=False, indent=2)
    elif args.format == 'markdown':
        text = generate_markdown(data, max(0, args.top_sessions))
    else:
        from io import StringIO
        import sys
        old = sys.stdout
        buf = StringIO()
        try:
            sys.stdout = buf
            print_summary(data, max(0, args.top_sessions))
            if args.csv_dir:
                print()
                print('CSV exports')
                for p in data.get('csv_exports', []):
                    print(f'- {p}')
        finally:
            sys.stdout = old
        text = buf.getvalue()

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text, encoding='utf-8')
    print(text, end='' if text.endswith('\n') else '\n')


if __name__ == '__main__':
    main()
