#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path
from load_sender_config import load_sender_config

CSS = """
body { font-family: Arial, Helvetica, sans-serif; color: #111827; margin: 0; padding: 32px; background: #F8FAFC; }
.wrap { max-width: 820px; margin: 0 auto; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 14px; overflow: hidden; box-shadow: 0 12px 30px rgba(15,23,42,0.06); }
.hero { padding: 28px 32px; background: #0F172A; color: #FFFFFF; }
.hero h1 { margin: 0 0 8px 0; font-size: 28px; }
.hero p { margin: 0; color: #DBEAFE; font-size: 14px; }
.section { padding: 24px 32px; border-top: 1px solid #E5E7EB; }
.section h2 { margin: 0 0 14px 0; font-size: 18px; color: #111827; }
.card { background: #F8FAFC; border: 1px solid #E5E7EB; border-radius: 10px; padding: 16px; margin: 12px 0; }
.kv { margin: 6px 0; }
.label { font-weight: 700; }
ul { margin: 10px 0 0 18px; padding: 0; }
li { margin: 8px 0; }
.fit { border-left: 4px solid #2563EB; }
.topfit { display: inline-block; background: #DBEAFE; color: #2563EB; font-weight: 700; font-size: 12px; padding: 6px 10px; border-radius: 999px; margin-bottom: 10px; }
.footer { padding: 20px 32px 28px 32px; color: #6B7280; font-size: 13px; border-top: 1px solid #E5E7EB; }
"""


def esc(v):
    return html.escape(str(v or ''))


def main():
    ap = argparse.ArgumentParser(description='Render polished HTML outreach brief from structured JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    sender = load_sender_config()
    fits = data.get('openclaw_fits', [])
    fit_html = []
    priority_move = ''
    priority_why = ''
    priority_benefit = ''
    priority = data.get('priority_move') or {}
    if isinstance(priority, dict):
        priority_move = priority.get('move', '')
        priority_why = priority.get('why_first', '')
        priority_benefit = priority.get('expected_benefit', '')
    if not priority_move and fits:
        priority_move = fits[0].get('use_case', '')
        priority_why = fits[0].get('why_it_fits', '')
        priority_benefit = fits[0].get('likely_value', '')
    why_it_matters = data.get('why_it_matters', [])
    for i, fit in enumerate(fits):
        badge = '<div class="topfit">Top fit</div>' if i == 0 else ''
        fit_html.append(f'''<div class="card fit">{badge}
<h3>{esc(fit.get('use_case','Use case'))}</h3>
<div class="kv"><span class="label">Why it fits:</span> {esc(fit.get('why_it_fits',''))}</div>
<div class="kv"><span class="label">Likely value:</span> {esc(fit.get('likely_value',''))}</div>
<div class="kv"><span class="label">Lowest-friction start:</span> {esc(fit.get('starting_point',''))}</div>
</div>''')

    obs = ''.join(f'<li>{esc(item)}</li>' for item in data.get('website_observations', [])) or '<li>No public observations captured.</li>'
    matters = ''.join(f'<li>{esc(item)}</li>' for item in why_it_matters) or '<li>No business consequence notes captured.</li>'
    html_doc = f'''<!doctype html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Outreach Brief — {esc(data.get('business_name','Unknown'))}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <h1>{esc(data.get('business_name','Unknown'))}</h1>
    <p>Short outreach brief prepared from public website signals and tailored OpenClaw fit analysis.</p>
  </div>
  <div class="section">
    <h2>Business snapshot</h2>
    <div class="card">
      <div class="kv"><span class="label">Website:</span> {esc(data.get('website_url',''))}</div>
      <div class="kv"><span class="label">What they appear to do:</span> {esc(data.get('business_summary',''))}</div>
      <div class="kv"><span class="label">Likely audience:</span> {esc(data.get('likely_audience',''))}</div>
    </div>
  </div>
  <div class="section">
    <h2>Website observations</h2>
    <div class="card"><ul>{obs}</ul></div>
  </div>
  <div class="section">
    <h2>OpenClaw fit</h2>
    {''.join(fit_html)}
  </div>
  <div class="section">
    <h2>Priority move</h2>
    <div class="card fit"><div class="topfit">Start here</div>
      <div class="kv"><span class="label">Move:</span> {esc(priority_move)}</div>
      <div class="kv"><span class="label">Why first:</span> {esc(priority_why)}</div>
      <div class="kv"><span class="label">Expected benefit:</span> {esc(priority_benefit)}</div>
    </div>
  </div>
  <div class="section">
    <h2>Why it matters</h2>
    <div class="card"><ul>{matters}</ul></div>
  </div>
  <div class="section">
    <h2>Suggested demo angle</h2>
    <div class="card">{esc(data.get('demo_angle',''))}</div>
  </div>
  <div class="section">
    <h2>Outreach summary</h2>
    <div class="card">{esc(data.get('outreach_summary',''))}</div>
  </div>
  <div class="footer">Prepared for outreach-demo · OpenClaw Opportunity Brief · {esc(sender['senderBrandLine'])}</div>
</div>
</body>
</html>
'''
    Path(args.output).write_text(html_doc, encoding='utf-8')


if __name__ == '__main__':
    main()
