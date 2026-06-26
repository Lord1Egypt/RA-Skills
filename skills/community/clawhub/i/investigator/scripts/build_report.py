#!/usr/bin/env python3
import json
import sys


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print('No input provided.')
        return
    try:
        data = json.loads(raw)
    except Exception as e:
        print(f'Invalid JSON: {e}')
        return

    input_data = data.get('input', {})
    summary = data.get('summary', {})
    strong = data.get('strongest_findings', []) or data.get('matches', []) or data.get('results', [])
    weak = data.get('weak_findings', [])
    unver = data.get('not_verifiable', [])
    breach = data.get('breach_check')

    print('# OSINT Report')
    print()
    print('## Input')
    print(json.dumps(input_data, ensure_ascii=False, indent=2) if isinstance(input_data, dict) else input_data)
    print()
    print('## Summary')
    if summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print('No summary available.')
    print()
    print('## Strongest Findings')
    if strong:
        for m in strong:
            platform = m.get('platform', 'unknown')
            match_type = m.get('match_type', 'unknown')
            final_url = m.get('final_url') or m.get('url') or ''
            print(f'- {platform}: {match_type} - {final_url}')
    else:
        print('- No strong findings')
    print()
    print('## Weak / Ambiguous Findings')
    if weak:
        for m in weak:
            platform = m.get('platform', 'unknown')
            final_url = m.get('final_url') or m.get('url') or ''
            print(f'- {platform}: weak - {final_url}')
    else:
        print('- None')
    print()
    print('## Not Verifiable')
    if unver:
        for m in unver:
            platform = m.get('platform', 'unknown')
            final_url = m.get('final_url') or m.get('url') or ''
            print(f'- {platform}: not_verifiable - {final_url}')
    else:
        print('- None')
    print()
    print('## Breach Check')
    if breach:
        print(json.dumps(breach, ensure_ascii=False, indent=2))
    else:
        print('No breach check data.')


if __name__ == '__main__':
    main()
