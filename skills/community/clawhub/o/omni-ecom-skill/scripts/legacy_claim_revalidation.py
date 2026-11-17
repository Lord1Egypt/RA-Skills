#!/usr/bin/env python3
"""Prepare a native v2 claim ledger from archived v1 claims and real local exports.

The result is source-recomputed and scope-label checked, but it does not certify
platform ownership or authenticity and grants no execution permission.
"""
from __future__ import annotations

import argparse
import json
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from adjudication_guard import fingerprint, require, sha
from artifact_contract import native_claim_identity
from claim_guard import validate_claims
from claim_source_guard import validate_sources
from legacy_migration import read, verify
from source_context_guard import summary


BOUNDARY = 'operator_attested_not_platform_authenticated'


def _inside(root, value, reason):
    require(isinstance(value, str) and value and not Path(value).is_absolute(), reason)
    path = (root / value).resolve()
    require(path.is_relative_to(root) and path.is_file(), reason)
    return path


def _load_context(path, client_scope):
    value = read(path)
    require(value.get('client_scope') == client_scope, 'revalidation_scope_client_mismatch')
    scope = value.get('scope')
    require(isinstance(scope, dict) and all(isinstance(scope.get(key), str) and scope[key].strip()
            for key in ('platform', 'store')), 'revalidation_scope_missing')
    attestation = value.get('scope_attestation')
    require(isinstance(attestation, dict) and attestation.get('status') == BOUNDARY,
            'revalidation_scope_attestation_invalid')
    require(all(isinstance(attestation.get(key), str) and attestation[key].strip()
            for key in ('authority_reference', 'attested_at')), 'revalidation_scope_attestation_missing')
    try:
        datetime.fromisoformat(attestation['attested_at'].replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError('revalidation_scope_attested_at_invalid') from exc
    claims = value.get('claims')
    require(isinstance(claims, dict), 'revalidation_context_claims_invalid')
    return value


def prepare(migration_dir, receipt_sha256, client_scope, record_id, evidence_root,
            context_file, output, run_id, team_version):
    migration_root = Path(migration_dir).resolve()
    receipt = verify(migration_root, client_scope, receipt_sha256)
    matches = [item for item in receipt['records'] if item.get('record_id') == record_id and item.get('kind') == 'claim']
    require(len(matches) == 1, 'revalidation_legacy_claim_record_not_found')
    record_path = (migration_root / matches[0]['record_file']).resolve()
    record = read(record_path)
    require(record.get('entity_type') == 'legacy_claim' and
            record.get('permissions', {}).get('current_numeric_evidence') is False,
            'revalidation_legacy_claim_authority_invalid')
    historical = record.get('historical_content')
    require(isinstance(historical, dict), 'revalidation_historical_claims_missing')
    context_path = Path(context_file).resolve()
    context = _load_context(context_path, client_scope)
    root = Path(evidence_root).resolve()
    require(root.is_dir(), 'revalidation_evidence_root_missing')
    target = Path(output).resolve()
    require(not target.exists(), 'revalidation_target_exists')
    require(not target.is_relative_to(root) and not root.is_relative_to(target) and
            not target.is_relative_to(migration_root) and not migration_root.is_relative_to(target),
            'revalidation_path_overlap')
    require(isinstance(run_id, str) and run_id.strip(), 'revalidation_run_id_missing')

    claims = json.loads(json.dumps(historical.get('claims')))
    require(isinstance(claims, list) and claims, 'revalidation_claims_missing')
    mappings = context['claims']
    source_map = {}
    source_inputs = []
    raw_sources = {}
    for row in claims:
        require(isinstance(row, dict), 'revalidation_claim_invalid')
        source = row.get('source_ref')
        require(isinstance(source, dict), 'revalidation_source_ref_missing')
        original_name = source.get('source_file')
        original = _inside(root, original_name, 'revalidation_source_outside_or_missing')
        digest = sha(original)
        require(digest == str(source.get('source_sha256', '')).lower(),
                'revalidation_source_hash_mismatch')
        relative = str(original.relative_to(root))
        if relative not in source_map:
            copied = f"sources/{len(source_map):04d}-{original.name}"
            source_map[relative] = copied
            raw_sources[copied] = original.read_bytes()
            source_inputs.append(dict(original_relative_path=relative, copied_file=copied,
                                      sha256=digest, bytes=len(raw_sources[copied])))
        source['source_file'] = source_map[relative]
        if row.get('status') == 'verified':
            contexts = mappings.get(row.get('claim_id'))
            require(isinstance(contexts, dict) and contexts, 'revalidation_claim_context_missing')
            source['contexts'] = contexts
    require(set(mappings) == {row['claim_id'] for row in claims if row.get('status') == 'verified'},
            'revalidation_context_claim_set_mismatch')
    payload = dict(**native_claim_identity(team_version), run_id=run_id, client_scope=client_scope,
                   period=historical.get('period'), source_context_policy='required',
                   scope=context['scope'], claims=claims)
    if historical.get('additional_periods'):
        payload['additional_periods'] = historical['additional_periods']
    errors, counts = validate_claims(payload)
    require(not errors, 'revalidation_claim_structure_blocked:' + ';'.join(errors))

    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.omni-ecom-revalidate-', dir=target.parent) as temp_name:
        temp = Path(temp_name)
        for name, raw in raw_sources.items():
            path = temp / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        ledger_path = temp / 'claim-ledger.json'
        ledger_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        checks = validate_sources(payload, temp)
        require(summary(checks)['status'] == 'all_verified_source_labels_checked',
                'revalidation_source_context_incomplete')
        receipt_payload = {
            'schema_version': '2.0', 'artifact_type': 'legacy_claim_revalidation',
            'contract_name': 'omni-ecom.legacy-claim-revalidation', 'contract_version': '2.0',
            'created_by_team_version': team_version,
            'legacy_compatibility': {'source_contract': 'omni-ecom.claim-ledger@1.0',
                                     'current_authority_inherited': False,
                                     'execution_permission_inherited': False},
            'status': 'source_recomputed_scope_labels_checked_requires_current_report_binding',
            'authenticity_status': BOUNDARY, 'run_id': run_id, 'client_scope': client_scope,
            'legacy_record_id': record_id, 'legacy_record_sha256': sha(record_path),
            'migration_receipt_sha256': receipt_sha256,
            'scope_attestation_fingerprint': fingerprint(context['scope_attestation']),
            'scope': context['scope'], 'claim_ledger_file': 'claim-ledger.json',
            'claim_ledger_sha256': sha(ledger_path), 'source_inputs': source_inputs,
            'source_checks': checks, **counts, 'prepared_at': datetime.now(timezone.utc).isoformat(),
            'formal_delivery_completed': False, 'platform_authenticity_verified': False,
        }
        receipt_path = temp / 'revalidation-receipt.json'
        receipt_path.write_text(json.dumps(receipt_payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        from jsonschema import Draft202012Validator, FormatChecker
        schema = read(Path(__file__).resolve().parents[1] / 'schemas' / 'legacy-claim-revalidation.schema.json')
        require(not list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(receipt_payload)),
                'revalidation_receipt_schema_invalid')
        for item in source_inputs:
            require(sha(temp / item['copied_file']) == item['sha256'], 'revalidation_source_changed')
        Path(temp_name).replace(target)
    return receipt_payload


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--migration-dir', required=True); parser.add_argument('--receipt-sha256', required=True)
    parser.add_argument('--client-scope', required=True); parser.add_argument('--record-id', required=True)
    parser.add_argument('--evidence-root', required=True); parser.add_argument('--context', required=True)
    parser.add_argument('--output', required=True); parser.add_argument('--run-id', required=True)
    parser.add_argument('--team-version', required=True)
    args = parser.parse_args()
    try:
        result = prepare(args.migration_dir, args.receipt_sha256, args.client_scope, args.record_id,
                         args.evidence_root, args.context, args.output, args.run_id, args.team_version)
        print(json.dumps(result, ensure_ascii=False, indent=2)); return 0
    except (ValueError, OSError, KeyError, TypeError, ImportError, RecursionError) as exc:
        print(json.dumps({'status': 'revalidation_blocked', 'reason': str(exc)}, ensure_ascii=False)); return 2


if __name__ == '__main__':
    raise SystemExit(main())
