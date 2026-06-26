#!/usr/bin/env python3
import argparse
import json
import re
from common import dump

MONEY_RE = re.compile(r'₹?\s*([0-9]+(?:\.[0-9]+)?)\s*([kKmMlL]?)')


def parse_money(text: str):
    m = MONEY_RE.search(text)
    if not m:
        return None
    value = float(m.group(1))
    suffix = m.group(2).lower()
    mult = {'': 1, 'k': 1_000, 'm': 1_000_000, 'l': 100_000}.get(suffix, 1)
    return round(value * mult, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--text', required=True)
    args = ap.parse_args()
    text = args.text
    lowered = text.lower()

    out = {
        'fy': None,
        'regime': None,
        'resident_salaried': True,
        'signals': {
            'salary': any(w in lowered for w in ['salary', 'form 16', 'tds']),
            'fd_rd': any(w in lowered for w in ['fd', 'rd', '15g', '15h', 'interest certificate']),
            'capital_gains': any(w in lowered for w in ['stock', 'stocks', 'mf', 'mutual fund', 'capital gain', 'dividend', 'rsu']),
            'loans': any(w in lowered for w in ['student loan', 'education loan', 'house loan', 'home loan']),
            'itr': any(w in lowered for w in ['itr', 'return', 'ais', 'tis', '26as']),
        },
        'money_mentions': [],
        'missing_prompts': [],
    }

    if 'old regime' in lowered:
        out['regime'] = 'old'
    elif 'new regime' in lowered:
        out['regime'] = 'new'
    else:
        out['missing_prompts'].append('Ask which tax regime the user wants to use for this question.')

    monies = []
    for chunk in re.split(r'[,.\n]', text):
        val = parse_money(chunk)
        if val is not None:
            monies.append({'text': chunk.strip(), 'value_in_inr': val})
    out['money_mentions'] = monies

    dump(out)


if __name__ == '__main__':
    main()
