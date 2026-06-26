#!/usr/bin/env python3
"""Simple score engine for pathway-score-guide-pro.

Usage:
  python3 score_engine.py --scorecard ../resources/scorecards/baoyan.json --profile profile.json

profile.json format:
{
  "scores": {
    "排名GPA": 30,
    "英语": 12
  },
  "notes": "optional"
}
"""
from __future__ import annotations
import argparse, json, pathlib, sys


def load_json(path: pathlib.Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def grade(total: float) -> str:
    if total >= 85:
        return '高'
    if total >= 75:
        return '中高'
    if total >= 65:
        return '中'
    if total >= 55:
        return '中低'
    return '低'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--scorecard', required=True)
    ap.add_argument('--profile', required=True)
    args = ap.parse_args()

    scorecard = load_json(pathlib.Path(args.scorecard))
    profile = load_json(pathlib.Path(args.profile))
    weights = scorecard['weights']
    user_scores = profile.get('scores', {})

    rows = []
    total = 0.0
    for item, max_points in weights.items():
        user_points = float(user_scores.get(item, 0))
        if user_points > max_points:
            user_points = float(max_points)
        if user_points < 0:
            user_points = 0.0
        total += user_points
        rows.append((item, max_points, user_points))

    result = {
        'pathway': scorecard.get('pathway'),
        'total_score': round(total, 2),
        'grade': grade(total),
        'breakdown': [
            {'item': item, 'max_points': max_points, 'user_points': user_points}
            for item, max_points, user_points in rows
        ],
        'notes': profile.get('notes', '')
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write('\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
