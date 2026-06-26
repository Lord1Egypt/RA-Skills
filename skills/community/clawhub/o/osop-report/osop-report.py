#!/usr/bin/env python3
"""
OSOP Report Generator — Standalone, zero-dependency (beyond PyYAML).
Generates self-contained HTML reports from .osop + .osoplog.yaml files.

Usage:
  python osop-report.py <file.osop> [file.osoplog.yaml] [-o output.html]

Works with: Claude Code, Codex, Grok, Cursor, OpenClaw, or any CLI.
"""

import sys
import html
import json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# --- 5-color system ---

TYPE_COLOR = {
    'human': '#ea580c', 'agent': '#7c3aed',
    'api': '#2563eb', 'mcp': '#2563eb', 'cli': '#2563eb',
    'git': '#475569', 'docker': '#475569', 'cicd': '#475569', 'system': '#475569', 'infra': '#475569', 'gateway': '#475569',
    'db': '#059669', 'data': '#059669',
    'company': '#ea580c', 'department': '#ea580c', 'event': '#475569',
}

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--ok:#16a34a;--err:#dc2626;--warn:#d97706;--bg:#fff;--fg:#1e293b;--mu:#64748b;--bd:#e2e8f0;--cd:#f8fafc}
@media(prefers-color-scheme:dark){:root{--bg:#0f172a;--fg:#e2e8f0;--mu:#94a3b8;--bd:#334155;--cd:#1e293b}}
body{font:14px/1.6 system-ui,sans-serif;background:var(--bg);color:var(--fg);max-width:800px;margin:0 auto;padding:16px}
h1{font-size:1.4rem;font-weight:700}
.st{display:flex;gap:12px;flex-wrap:wrap;margin:6px 0}.st span{font-weight:600}
.s{padding:2px 8px;border-radius:3px;color:#fff;font-size:12px}.s.ok{background:var(--ok)}.s.err{background:var(--err)}
.desc{color:var(--mu);font-size:13px;margin:4px 0}
.meta{font:11px monospace;color:var(--mu);margin:4px 0}
.eb{background:#fef2f2;border:1px solid #fecaca;color:var(--err);padding:8px 12px;border-radius:6px;margin:12px 0;font-size:13px}
@media(prefers-color-scheme:dark){.eb{background:#450a0a;border-color:#7f1d1d}}
.n{border:1px solid var(--bd);border-radius:6px;margin:8px 0;overflow:hidden}
.n.child{margin-left:24px;border-style:dashed}
.n.coordinator{border-width:2px}
.n summary{display:flex;align-items:center;gap:8px;padding:8px 12px;cursor:pointer;background:var(--cd);font-size:13px;list-style:none}
.n summary::-webkit-details-marker{display:none}
.n.er{border-left:3px solid var(--err)}
.tp{color:#fff;padding:1px 6px;border-radius:3px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.du{margin-left:auto;color:var(--mu);font-size:12px;font-family:monospace}
.br{height:4px;border-radius:2px;display:inline-block;min-width:2px}
.bd{padding:12px;font-size:13px;border-top:1px solid var(--bd)}
.bd p{color:var(--mu);margin-bottom:8px}
.bd table{width:100%;font-size:12px;border-collapse:collapse}
.bd td{padding:3px 8px;border-bottom:1px solid var(--bd);vertical-align:top}
.bd td:first-child{font-weight:600;color:var(--mu);width:30%;font-family:monospace;font-size:11px}
.ai{font-size:12px;color:#7c3aed;margin-top:8px;font-family:monospace}
@media(prefers-color-scheme:dark){.ai{color:#a78bfa}}
.er-box{background:#fef2f2;color:var(--err);padding:8px;border-radius:4px;font-size:12px;margin-top:8px}
@media(prefers-color-scheme:dark){.er-box{background:#450a0a}}
.rt{font-size:12px;color:var(--ok);margin-top:4px}
footer{text-align:center;padding:20px 0;color:var(--mu);font-size:11px}
footer a{color:#2563eb}"""


def h(s):
    return html.escape(str(s)) if s else ''


def ms(v):
    if v is None: return '-'
    v = int(v)
    if v < 1000: return f'{v}ms'
    if v < 60000: return f'{v/1000:.1f}s'
    return f'{v/60000:.1f}m'


def usd(v):
    if not v: return '$0'
    return f'${v:.4f}' if v < 0.01 else f'${v:.3f}'


def kv_table(obj):
    if not obj or not isinstance(obj, dict): return ''
    rows = ''
    for k, v in obj.items():
        val = json.dumps(v) if isinstance(v, (dict, list)) else str(v)
        display = val[:97] + '...' if len(val) > 100 else val
        rows += f'<tr><td>{h(k)}</td><td>{h(display)}</td></tr>'
    return f'<table>{rows}</table>' if rows else ''


def generate_html_report(osop_yaml: str, osoplog_yaml: str | None = None) -> str:
    o = yaml.safe_load(osop_yaml) or {}
    log = yaml.safe_load(osoplog_yaml) if osoplog_yaml else None
    is_exec = bool(log)
    title = o.get('name') or o.get('id') or 'OSOP Report'

    latest: dict[str, dict] = {}
    failures = []
    if log and log.get('node_records'):
        for r in log['node_records']:
            nid = r.get('node_id', '')
            prev = latest.get(nid)
            if not prev or r.get('attempt', 1) > prev.get('attempt', 1):
                latest[nid] = r
            if r.get('status') == 'FAILED':
                failures.append(r)

    total_ms = log.get('duration_ms') if log else None
    body = ''

    # Header
    body += '<header>'
    body += f'<h1>{h(title)}</h1>'
    body += '<div class="st">'
    if is_exec and log:
        sc = 'ok' if log.get('status') == 'COMPLETED' else 'err'
        body += f'<span class="s {sc}">{h(log.get("status", "UNKNOWN"))}</span>'
        body += f'<span>{ms(log.get("duration_ms"))}</span>'
        cost = (log.get('cost') or {}).get('total_usd')
        if cost: body += f'<span>{usd(cost)}</span>'
        body += f'<span>{len(latest)} nodes</span>'
    else:
        body += f'<span>{len(o.get("nodes", []))} nodes</span>'
        body += f'<span>{len(o.get("edges", []))} edges</span>'
        if o.get('version'): body += f'<span>v{h(o["version"])}</span>'
    body += '</div>'
    if o.get('description'): body += f'<p class="desc">{h(o["description"])}</p>'

    meta_parts = []
    if o.get('id'): meta_parts.append(o['id'])
    if log and log.get('run_id'): meta_parts.append('run:' + log['run_id'][:8])
    if log and log.get('mode'): meta_parts.append(log['mode'])
    runtime = log.get('runtime', {}) if log else {}
    if runtime.get('agent'): meta_parts.append(runtime['agent'])
    trigger = log.get('trigger', {}) if log else {}
    if trigger.get('actor'): meta_parts.append(trigger['actor'])
    if log and log.get('started_at'): meta_parts.append(log['started_at'].replace('T', ' ').replace('Z', ''))
    if meta_parts: body += f'<div class="meta">{" &middot; ".join(h(p) for p in meta_parts)}</div>'
    body += '</header>'

    # Error banner
    for f in failures:
        err = f.get('error', {})
        body += f'<div class="eb">{h(f.get("node_id", ""))} failed: {h(err.get("code", ""))} — {h(err.get("message", "unknown"))}</div>'

    # Nodes
    body += '<main>'
    nodes = o.get('nodes', [])
    for node in nodes:
        if not isinstance(node, dict): continue
        nid = node.get('id', '')
        rec = latest.get(nid)
        all_recs = [r for r in (log or {}).get('node_records', []) if r.get('node_id') == nid]
        is_failed = rec and rec.get('status') == 'FAILED'
        is_child = bool(node.get('parent'))
        is_coord = node.get('subtype') == 'coordinator'
        cls = 'n er' if is_failed else 'n'
        if is_child: cls += ' child'
        if is_coord: cls += ' coordinator'
        open_attr = ' open' if is_failed else ''

        ntype = node.get('type', 'system')
        color = TYPE_COLOR.get(ntype, '#475569')

        body += f'<details class="{cls}"{open_attr}>'
        body += '<summary>'
        body += f'<span class="tp" style="background:{color}">{h(ntype.upper())}</span>'
        body += f'<strong>{h(node.get("name", nid))}</strong>'
        if rec:
            body += f'<span class="du">{ms(rec.get("duration_ms"))}</span>'
            st = rec.get('status', '')
            if st == 'COMPLETED' and total_ms:
                pct = max(1, round((rec.get('duration_ms') or 0) / total_ms * 100))
                body += f'<span class="br" style="width:{pct}%;background:var(--ok)"></span>'
            elif st == 'FAILED':
                body += '<span class="s err">FAILED</span>'
            else:
                body += f'<span class="s ok">{h(st)}</span>'
        body += '</summary>'

        body += '<div class="bd">'
        if node.get('description'): body += f'<p>{h(node["description"])}</p>'

        inputs = (rec or {}).get('inputs') or (rec or {}).get('inputs_snapshot') or node.get('inputs')
        outputs = (rec or {}).get('outputs') or (rec or {}).get('outputs_snapshot') or node.get('outputs')
        if isinstance(inputs, dict): body += kv_table(inputs)
        if isinstance(outputs, dict): body += kv_table(outputs)

        # AI metadata
        ai = (rec or {}).get('ai_metadata')
        if ai:
            parts = []
            if ai.get('model'): parts.append(ai['model'])
            pt = ai.get('prompt_tokens')
            ct = ai.get('completion_tokens', 0)
            if pt is not None: parts.append(f'{pt:,}→{ct:,} tok')
            if ai.get('cost_usd'): parts.append(usd(ai['cost_usd']))
            if ai.get('confidence') is not None: parts.append(f'{ai["confidence"]*100:.0f}%')
            if parts: body += f'<div class="ai">{" &middot; ".join(h(p) for p in parts)}</div>'

        # Human metadata
        hm = (rec or {}).get('human_metadata')
        if hm:
            parts = []
            if hm.get('actor'): parts.append(hm['actor'])
            if hm.get('decision'): parts.append('decision=' + hm['decision'])
            if hm.get('notes'): parts.append(hm['notes'])
            if parts: body += f'<div style="font-size:12px;color:var(--mu);margin-top:4px">{" &middot; ".join(h(p) for p in parts)}</div>'

        # Parent info
        if rec and rec.get('parent_id'):
            si = rec.get('spawn_index', '')
            iso = rec.get('isolation', '')
            body += f'<div style="font-size:11px;color:var(--mu);margin-top:4px;font-family:monospace">spawned by {h(rec["parent_id"])}'
            if si: body += f' (#{si})'
            if iso: body += f' &middot; {h(iso)}'
            body += '</div>'

        # Tools used
        tools = (rec or {}).get('tools_used', [])
        if tools:
            body += '<div style="font-size:12px;color:var(--mu);margin-top:4px">'
            for t in tools:
                body += f'<span style="margin-right:8px">{h(t.get("tool",""))} x{t.get("calls",0)}</span>'
            body += '</div>'

        # Reasoning
        reasoning = (rec or {}).get('reasoning')
        if reasoning:
            body += '<details style="margin-top:8px"><summary style="font-size:12px;color:#7c3aed;cursor:pointer;font-weight:600">Reasoning</summary>'
            body += '<div style="font-size:12px;padding:8px 0">'
            if reasoning.get('question'): body += f'<div style="margin-bottom:6px"><strong>Q:</strong> {h(reasoning["question"])}</div>'
            if reasoning.get('selected'): body += f'<div><strong>Selected:</strong> {h(reasoning["selected"])}</div>'
            conf = reasoning.get('confidence')
            if conf is not None: body += f'<div>Confidence: {conf*100:.0f}%</div>'
            body += '</div></details>'

        # Error
        err = (rec or {}).get('error')
        if err:
            body += f'<div class="er-box">{h(err.get("code",""))}: {h(err.get("message",""))}</div>'

        # Retry history
        if len(all_recs) > 1:
            for r in all_recs:
                if r is rec: continue
                body += f'<div class="rt">Attempt {r.get("attempt",1)}: {h(r.get("status",""))} {ms(r.get("duration_ms"))}'
                if r.get('error'): body += f' — {h(r["error"].get("code",""))}'
                body += '</div>'

        body += '</div></details>'

    body += '</main>'

    if log and log.get('result_summary'):
        body += f'<p style="margin:16px 0;padding:12px;background:var(--cd);border-radius:6px;font-size:13px;color:var(--mu)">{h(log["result_summary"])}</p>'

    body += '<footer>OSOP v1.0 &middot; <a href="https://osop.ai">osop.ai</a> &middot; <a href="https://osop-editor.vercel.app">Visual Editor</a></footer>'

    return f'<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{h(title)}</title><style>{CSS}</style></head><body>{body}</body></html>'


def main():
    args = sys.argv[1:]
    if not args or '-h' in args or '--help' in args:
        print("""OSOP Report Generator
Usage: python osop-report.py <file.osop> [file.osoplog.yaml] [-o output.html]

Generates a self-contained HTML report from OSOP workflow + execution log.
Works standalone — only requires PyYAML (pip install pyyaml).""")
        sys.exit(0)

    osop_path = None
    log_path = None
    output_path = None
    i = 0
    while i < len(args):
        if args[i] in ('-o', '--output'):
            i += 1
            output_path = args[i]
        elif not osop_path:
            osop_path = args[i]
        elif not log_path:
            log_path = args[i]
        i += 1

    if not osop_path:
        print('Error: no .osop file specified', file=sys.stderr)
        sys.exit(1)

    osop_yaml = Path(osop_path).read_text(encoding='utf-8')
    log_yaml = Path(log_path).read_text(encoding='utf-8') if log_path else None

    html_out = generate_html_report(osop_yaml, log_yaml)

    if not output_path:
        output_path = Path(osop_path).stem.replace('.osop', '').replace('.yaml', '') + '-report.html'

    Path(output_path).write_text(html_out, encoding='utf-8')
    print(f'Report: {Path(output_path).resolve()} ({len(html_out)/1024:.1f}KB)', file=sys.stderr)


if __name__ == '__main__':
    main()
