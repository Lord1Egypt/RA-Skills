#!/usr/bin/env python3
import json
import sys

SCORES = {
    'exact': 25,
    'likely': 15,
    'weak': 5,
    'not_verifiable': 0,
    'no_result': 0,
}


def confidence_band(score):
    if score >= 75:
        return 'strong'
    if score >= 45:
        return 'likely'
    if score >= 20:
        return 'possible'
    return 'weak'


def main():
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({'error': 'no input provided'}))
        return
    try:
        data = json.loads(raw)
    except Exception as e:
        print(json.dumps({'error': f'invalid json: {e}'}))
        return

    findings = data.get('matches') or data.get('results') or []
    exact = []
    likely = []
    weak = []
    unverifiable = []
    no_result = []
    total = 0

    for f in findings:
        mt = f.get('match_type', 'weak')
        total += SCORES.get(mt, 0)
        if mt == 'exact':
            exact.append(f)
        elif mt == 'likely':
            likely.append(f)
        elif mt == 'weak':
            weak.append(f)
        elif mt == 'not_verifiable':
            unverifiable.append(f)
        else:
            no_result.append(f)

    breach = data.get('breach_check') or data.get('hibp')
    if isinstance(breach, dict) and breach.get('breach_found'):
        total += 10

    summary = {
        'overall_score': total,
        'overall_confidence': confidence_band(total),
        'exact_count': len(exact),
        'likely_count': len(likely),
        'weak_count': len(weak),
        'not_verifiable_count': len(unverifiable),
        'no_result_count': len(no_result),
    }

    strongest = exact + likely
    out = {
        'input': data.get('input'),
        'summary': summary,
        'strongest_findings': strongest[:10],
        'weak_findings': weak[:10],
        'not_verifiable': unverifiable[:10],
        'breach_check': breach,
        'raw': data,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
