#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


APPENDIX_HEADING = '# Appendix: Claim -> Evidence Index'
CLAIM_BULLET_RE = re.compile(r'^\s*-\s+\[(C\d+(?:\.\d+)*)\](?:\[[^\]]+\])?', re.MULTILINE)
ALLOWED_LABELS = {
    'evidence-backed interpretation',
    'plausible inference',
    'speculation',
}


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise SystemExit(f'Failed to read JSON {path}: {exc}') from exc


def extract_report_claims(report_path: Path) -> list[str]:
    text = report_path.read_text(encoding='utf-8')
    if APPENDIX_HEADING in text:
        text = text.split(APPENDIX_HEADING, 1)[0]
    return CLAIM_BULLET_RE.findall(text)


def validate(report_path: Path, manifest_path: Path, paragraphs_path: Path | None = None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    report_claims = extract_report_claims(report_path)
    report_set = set(report_claims)
    duplicates_in_report = sorted({claim for claim in report_claims if report_claims.count(claim) > 1})
    if duplicates_in_report:
        errors.append(f'Duplicate claim ids in report: {", ".join(duplicates_in_report)}')

    manifest = load_json(manifest_path)
    claims = manifest.get('claims', [])
    if not isinstance(claims, list):
        errors.append('`claims` must be a list in traceability manifest.')
        claims = []

    paragraph_ids: set[str] = set()
    if paragraphs_path:
        paragraphs = load_json(paragraphs_path).get('paragraphs', [])
        if isinstance(paragraphs, list):
            paragraph_ids = {item.get('paragraph_id') for item in paragraphs if isinstance(item, dict) and item.get('paragraph_id')}

    manifest_ids: list[str] = []
    for idx, entry in enumerate(claims, start=1):
        if not isinstance(entry, dict):
            errors.append(f'Claim entry #{idx} is not an object.')
            continue
        claim_id = entry.get('claim_id')
        if not claim_id:
            errors.append(f'Claim entry #{idx} is missing `claim_id`.')
            continue
        manifest_ids.append(claim_id)

        label = entry.get('interpretation_type')
        if label not in ALLOWED_LABELS:
            errors.append(f'{claim_id}: invalid interpretation_type `{label}`.')

        statement = str(entry.get('statement') or entry.get('claim_text') or '').strip()
        if not statement:
            errors.append(f'{claim_id}: missing statement.')

        evidences = entry.get('evidences')
        if not isinstance(evidences, list):
            evidences = entry.get('evidence')
        if not isinstance(evidences, list) or not evidences:
            errors.append(f'{claim_id}: missing evidence list.')
            continue

        seen_evidence_ids: set[str] = set()
        for eidx, evidence in enumerate(evidences, start=1):
            if not isinstance(evidence, dict):
                errors.append(f'{claim_id}: evidence #{eidx} is not an object.')
                continue
            evidence_id = evidence.get('evidence_id')
            if not evidence_id:
                errors.append(f'{claim_id}: evidence #{eidx} is missing evidence_id.')
            elif evidence_id in seen_evidence_ids:
                errors.append(f'{claim_id}: duplicate evidence_id `{evidence_id}`.')
            else:
                seen_evidence_ids.add(evidence_id)

            paragraph_id = evidence.get('paragraph_id')
            if paragraph_id and paragraph_ids and paragraph_id not in paragraph_ids:
                errors.append(f'{claim_id}: paragraph_id `{paragraph_id}` not found in latex_paragraphs.json.')

            locator_method = evidence.get('locator_method') or evidence.get('relation')
            if not locator_method:
                warnings.append(f'{claim_id}: evidence #{eidx} has no locator_method.')
            if not any(
                evidence.get(key)
                for key in ('paragraph_id', 'page', 'caption_label', 'equation_label', 'synctex', 'source_file', 'doc', 'locator_snippets')
            ):
                errors.append(f'{claim_id}: evidence #{eidx} has no usable locator field.')

    manifest_dupes = sorted({claim_id for claim_id in manifest_ids if manifest_ids.count(claim_id) > 1})
    if manifest_dupes:
        errors.append(f'Duplicate claim ids in manifest: {", ".join(manifest_dupes)}')

    manifest_set = set(manifest_ids)
    missing_from_manifest = sorted(report_set - manifest_set)
    if missing_from_manifest:
        errors.append('Claims present in report but missing from manifest: ' + ', '.join(missing_from_manifest))

    missing_from_report = sorted(manifest_set - report_set)
    if missing_from_report:
        warnings.append('Claims present in manifest but missing from report: ' + ', '.join(missing_from_report))

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(description='Validate claim-to-evidence traceability.')
    parser.add_argument('--report', required=True, help='Path to report.md')
    parser.add_argument('--manifest', required=True, help='Path to traceability_manifest.json')
    parser.add_argument('--paragraphs', help='Path to latex_paragraphs.json')
    args = parser.parse_args()

    report_path = Path(args.report)
    manifest_path = Path(args.manifest)
    paragraphs_path = Path(args.paragraphs) if args.paragraphs else None

    errors, warnings = validate(report_path, manifest_path, paragraphs_path)

    if warnings:
        print('Warnings:')
        for item in warnings:
            print(f'  - {item}')
    if errors:
        print('Errors:')
        for item in errors:
            print(f'  - {item}')
        raise SystemExit(1)

    print('Traceability validation passed.')


if __name__ == '__main__':
    main()
