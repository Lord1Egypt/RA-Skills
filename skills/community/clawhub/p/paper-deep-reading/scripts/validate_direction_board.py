#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ALLOWED_SEED_TYPES = {
    'assumption_violation',
    'unavailable_mechanism',
    'proxy_mismatch',
    'evidence_gap',
    'tiny_example',
    'successor_paper_gap',
    'reviewer_objection',
    'negative_result',
    'cross_domain_transfer',
}

ALLOWED_INTERPRETATION_TYPES = {
    'evidence-backed interpretation',
    'plausible inference',
    'speculation',
}

CLAIM_ID_RE = re.compile(r'^C\d+(?:\.\d+)*$')

REQUIRED_TOP_LEVEL = {
    'schema_version',
    'paper_id',
    'purpose',
    'source_confidence',
    'direction_seeds',
    'ranking_notes',
    'search_limitations',
}

REQUIRED_SEED_FIELDS = {
    'seed_id',
    'title',
    'seed_type',
    'trigger_interpretation_type',
    'paper_anchor_claim_ids',
    'trigger_evidence_summary',
    'hidden_assumption_or_gap',
    'research_question',
    'hypothesis',
    'proposed_mechanism',
    'minimum_viable_experiment',
    'negative_result_interpretation',
    'killer_objection',
    'killer_result',
    'first_week_plan',
    'score',
    'risk_level',
    'expected_value',
    'confidence',
}

REQUIRED_MVE_FIELDS = {
    'setup',
    'intervention',
    'comparison',
    'metric_or_decision_rule',
    'expected_supporting_result',
}

REQUIRED_SCORE_FIELDS = {
    'novelty',
    'significance',
    'testability',
    'feasibility',
    'evidence_anchor',
    'risk_adjusted_value',
    'overall',
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise SystemExit(f'Failed to read JSON {path}: {exc}') from exc


def as_number(value: object) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    try:
        if isinstance(value, str) and value.strip():
            return float(value)
    except ValueError:
        return None
    return None


def validate(board: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing_top = sorted(REQUIRED_TOP_LEVEL - set(board))
    if missing_top:
        errors.append('Missing top-level keys: ' + ', '.join(missing_top))

    seeds = board.get('direction_seeds', [])
    if not isinstance(seeds, list):
        errors.append('`direction_seeds` must be a list.')
        return errors, warnings

    seed_ids: list[str] = []
    for idx, seed in enumerate(seeds, start=1):
        if not isinstance(seed, dict):
            errors.append(f'Seed #{idx} is not an object.')
            continue
        seed_id = str(seed.get('seed_id') or f'#{idx}')
        seed_ids.append(seed_id)

        missing = sorted(REQUIRED_SEED_FIELDS - set(seed))
        if missing:
            errors.append(f'{seed_id}: missing fields: ' + ', '.join(missing))

        seed_type = seed.get('seed_type')
        if seed_type not in ALLOWED_SEED_TYPES:
            errors.append(f'{seed_id}: invalid seed_type `{seed_type}`.')

        trigger_type = seed.get('trigger_interpretation_type')
        if trigger_type not in ALLOWED_INTERPRETATION_TYPES:
            errors.append(f'{seed_id}: invalid trigger_interpretation_type `{trigger_type}`.')

        claim_ids = seed.get('paper_anchor_claim_ids')
        if not isinstance(claim_ids, list) or not claim_ids:
            warnings.append(f'{seed_id}: paper_anchor_claim_ids should be a non-empty list when evidence exists.')
        elif any(not isinstance(item, str) or not CLAIM_ID_RE.match(item) for item in claim_ids):
            errors.append(f'{seed_id}: invalid claim id in paper_anchor_claim_ids.')

        mve = seed.get('minimum_viable_experiment')
        if not isinstance(mve, dict):
            errors.append(f'{seed_id}: minimum_viable_experiment must be an object.')
        else:
            missing_mve = sorted(REQUIRED_MVE_FIELDS - set(mve))
            if missing_mve:
                errors.append(f'{seed_id}: MVE missing fields: ' + ', '.join(missing_mve))

        score = seed.get('score')
        if not isinstance(score, dict):
            errors.append(f'{seed_id}: score must be an object.')
        else:
            missing_score = sorted(REQUIRED_SCORE_FIELDS - set(score))
            if missing_score:
                errors.append(f'{seed_id}: score missing fields: ' + ', '.join(missing_score))
            for key in REQUIRED_SCORE_FIELDS & set(score):
                number = as_number(score.get(key))
                if number is None:
                    errors.append(f'{seed_id}: score.{key} must be numeric.')
                elif not (0 <= number <= 5):
                    errors.append(f'{seed_id}: score.{key} must be between 0 and 5.')

        for field in ('negative_result_interpretation', 'killer_objection', 'killer_result'):
            value = str(seed.get(field) or '').strip()
            if not value:
                errors.append(f'{seed_id}: `{field}` must not be empty.')

    duplicates = sorted({sid for sid in seed_ids if seed_ids.count(sid) > 1})
    if duplicates:
        errors.append('Duplicate seed ids: ' + ', '.join(duplicates))

    if not seeds:
        warnings.append('No direction seeds were provided. This is acceptable only for a conservative reading with insufficient evidence.')

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate direction_board.json research seeds.')
    parser.add_argument('--board', required=True, help='Path to direction_board.json')
    args = parser.parse_args()

    board = load_json(Path(args.board))
    errors, warnings = validate(board)

    if warnings:
        print('Warnings:')
        for item in warnings:
            print(f'  - {item}')
    if errors:
        print('Errors:')
        for item in errors:
            print(f'  - {item}')
        raise SystemExit(1)

    print('Direction board validation passed.')


if __name__ == '__main__':
    main()
