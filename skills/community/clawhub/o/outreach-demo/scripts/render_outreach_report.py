#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description='Render outreach demo report from structured JSON.')
    ap.add_argument('--input', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    lines = []
    lines.append(f"# Outreach Demo Report — {data.get('business_name','Unknown')}\n")
    lines.append('## 1. Business snapshot')
    lines.append(f"- Business name: {data.get('business_name','')}")
    lines.append(f"- Website: {data.get('website_url','')}")
    lines.append(f"- What they appear to do: {data.get('business_summary','')}")
    lines.append(f"- Likely audience: {data.get('likely_audience','')}\n")

    lines.append('## 2. Website observations')
    for item in data.get('website_observations', []):
        lines.append(f"- {item}")
    lines.append('')

    lines.append('## 3. OpenClaw fit')
    for fit in data.get('openclaw_fits', []):
        lines.append(f"### {fit.get('use_case','Use case')}")
        lines.append(f"- Why it fits: {fit.get('why_it_fits','')}")
        lines.append(f"- Likely value: {fit.get('likely_value','')}")
        lines.append(f"- Lowest-friction start: {fit.get('starting_point','')}\n")

    lines.append('## 4. Suggested demo angle')
    lines.append(data.get('demo_angle',''))
    lines.append('')
    lines.append('## 5. Outreach summary')
    lines.append(data.get('outreach_summary',''))
    lines.append('')

    Path(args.output).write_text('\n'.join(lines).rstrip() + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
