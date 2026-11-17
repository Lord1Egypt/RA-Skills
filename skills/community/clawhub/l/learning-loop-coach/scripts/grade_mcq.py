#!/usr/bin/env python3
"""Validate and grade an explicitly mapped MCQ range. Read-only, stdlib only."""
import argparse
import json
import math
import re
import sys
from pathlib import Path


def validate_key(key):
    if not isinstance(key, dict):
        raise ValueError('Key must be an object')
    for field in ('exam_id', 'version'):
        if not isinstance(key.get(field), str) or not key[field].strip():
            raise ValueError(f'Missing {field}')
    rows = key.get('questions')
    if not isinstance(rows, list) or not rows:
        raise ValueError('questions must be a nonempty list')
    by_id = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('Each question must be an object')
        qid = row.get('id')
        if type(qid) is not int or qid <= 0 or qid in by_id:
            raise ValueError('Question ids must be unique positive integers')
        options = row.get('options')
        if (not isinstance(options, list) or len(options) < 2
                or any(not isinstance(x, str) or not re.fullmatch('[A-Z]', x)
                       for x in options) or len(set(options)) != len(options)):
            raise ValueError(f'Invalid option labels for Q{qid}')
        if row.get('answer') not in options:
            raise ValueError(f'Answer not among options for Q{qid}')
        points = row.get('points', 1)
        if (type(points) not in (int, float) or not math.isfinite(points)
                or points <= 0):
            raise ValueError(f'Invalid points for Q{qid}')
        if not isinstance(row.get('topic', 'unclassified'), str):
            raise ValueError(f'Invalid topic for Q{qid}')
        by_id[qid] = row
    return by_id


def parse_answers(raw):
    if not isinstance(raw, str):
        raise ValueError('Answers must be text')
    raw = raw.upper()
    if re.search(r'[^A-Z?\s,;，；]', raw):
        raise ValueError('Use letters and separators only; do not include question numbers')
    values = re.sub(r'[\s,;，；]', '', raw)
    if not values:
        raise ValueError('No answers supplied')
    return list(values)


def grade(key, start, end, raw, expected_version):
    by_id = validate_key(key)
    if expected_version != key['version']:
        raise ValueError('Exam version mismatch; do not grade against another version')
    if type(start) is not int or type(end) is not int or start < 1 or end < start:
        raise ValueError('Invalid inclusive range')
    if end - start + 1 > len(by_id):
        raise ValueError('Range exceeds the number of questions in this key')
    values = parse_answers(raw)
    if len(values) != end - start + 1:
        raise ValueError(f'Range {start}–{end} requires {end-start+1} answers; received {len(values)}')
    # Validate the entire submission before creating a result.
    for qid, answer in zip(range(start, end + 1), values):
        if qid not in by_id:
            raise ValueError(f'Q{qid} is absent from the key')
        if answer != '?' and answer not in by_id[qid]['options']:
            raise ValueError(f'Invalid submitted option for Q{qid}')
    details, topics = [], {}
    for qid, answer in zip(range(start, end + 1), values):
        row = by_id[qid]
        points = row.get('points', 1)
        status = 'skipped' if answer == '?' else ('correct' if answer == row['answer'] else 'incorrect')
        earned = points if status == 'correct' else 0
        details.append({'id': qid, 'submitted': None if answer == '?' else answer,
                        'correct_answer': row['answer'], 'status': status,
                        'earned': earned, 'possible': points})
        topic = row.get('topic', 'unclassified')
        total = topics.setdefault(topic, {'correct': 0, 'answered': 0, 'skipped': 0,
                                         'earned': 0, 'possible': 0})
        total['correct'] += status == 'correct'
        total['answered'] += status != 'skipped'
        total['skipped'] += status == 'skipped'
        total['earned'] += earned
        total['possible'] += points
    correct = sum(x['status'] == 'correct' for x in details)
    answered = sum(x['status'] != 'skipped' for x in details)
    possible = sum(x['possible'] for x in details)
    earned = sum(x['earned'] for x in details)
    return {'exam_id': key['exam_id'], 'version': key['version'],
            'start': start, 'end': end, 'raw_answers': raw,
            'scope': 'submitted_range_only', 'correct': correct, 'answered': answered,
            'skipped': len(details) - answered, 'earned': earned, 'possible': possible,
            'score_percent_in_range': round(100 * earned / possible, 2),
            'accuracy_percent_answered': round(100 * correct / answered, 2) if answered else None,
            'not_submitted_ids': sorted(qid for qid in by_id if qid < start or qid > end),
            'by_topic': topics, 'details': details}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--key', required=True, type=Path)
    parser.add_argument('--start', required=True, type=int)
    parser.add_argument('--end', required=True, type=int)
    parser.add_argument('--answers', required=True)
    parser.add_argument('--exam-version', required=True)
    args = parser.parse_args()
    try:
        key = json.loads(args.key.read_text(encoding='utf-8-sig'))
        result = grade(key, args.start, args.end, args.answers, args.exam_version)
    except (ValueError, OSError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
