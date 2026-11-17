#!/usr/bin/env python3
"""Recompute coverage/depth/conflicts on the exact inputs selected for delivery.

All paths in quality-inputs.json are relative to its directory. Input hashes
are taken before and after verification to detect concurrent changes. A stored
PASS alone is not accepted. Hard conflicts require verified adjudication.
"""
from __future__ import annotations

import contextlib
import hashlib
import io
import json
import tempfile
from pathlib import Path

import analysis_depth_guard as depth
import conflict_scan as conflicts
import coverage_guard as coverage
from adjudication_guard import validate_adjudication
from artifact_contract import validate_baseline_identity,validate_run_scope_identity,validate_stage_identity

ROLES = ('data-analyst','platform-ops','content-live-growth','ad-profit-optimizer')


def read(path):
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if not isinstance(data, dict):
        raise ValueError('quality_json_invalid')
    return data


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def validate_frozen_quality(manifest, report_dir, receipt):
    """Every rechecked input must match the exact object frozen for review."""
    root=report_dir.resolve()
    entries=manifest.get('sources',[])+manifest.get('artifacts',[])
    index={str(Path(item['path']).resolve()):item['sha256'] for item in entries}
    for item in receipt['inputs']:
        path=(root/item['file']).resolve()
        require(path.is_relative_to(root), 'quality_frozen_path_invalid')
        require(index.get(str(path))==item['sha256'] and sha(path)==item['sha256'],
                'quality_frozen_input_missing_or_changed')
    require(manifest.get('quality_gate')==receipt, 'quality_frozen_receipt_mismatch')


def validate_quality(report_dir: Path, report: dict) -> dict:
    config_path = report_dir / 'quality-inputs.json'
    config = read(config_path)
    require(config.get('run_id') == report.get('run_id') and
            config.get('client_scope') == report.get('client_scope') and
            config.get('report_revision') == report.get('report_revision'), 'quality_identity_mismatch')
    root = report_dir.resolve()
    def resolve(value):
        require(isinstance(value, str) and bool(value) and not Path(value).is_absolute(), 'quality_path_invalid')
        path = (root/value).resolve()
        require(path.is_relative_to(root) and path.is_file(), 'quality_path_outside_or_missing')
        return path
    paths = {key: resolve(config.get(key)) for key in ('inventory','chapter_plan','baseline','run_scope')}
    paths['quality_inputs'] = config_path
    paths['report_json'] = report_dir/'report.json'
    paths['report_md'] = report_dir/'report.md'
    require(read(paths['report_json'])==report, 'quality_report_argument_stale')
    raw_handoffs = config.get('handoffs', {})
    require(isinstance(raw_handoffs, dict), 'quality_handoffs_invalid')
    required_roles = ROLES if report.get('collaboration_mode') == 'comprehensive' else tuple(raw_handoffs)
    require(bool(required_roles) and set(raw_handoffs) == set(required_roles) and
            set(raw_handoffs).issubset(ROLES), 'quality_members_missing')
    handoffs = {role: resolve(raw_handoffs[role]) for role in required_roles}
    paths.update(handoffs)
    run_scope=read(paths['run_scope'])
    validate_run_scope_identity(run_scope,report.get('team_version'),report.get('run_id'),report.get('client_scope'))
    require(run_scope.get('status')=='scope_verified' and not run_scope.get('errors'),'quality_run_scope_blocked')
    def local_path(value,kind):
        require(isinstance(value,str) and value and not Path(value).is_absolute(),'quality_run_scope_path_invalid')
        candidate=(root/value).resolve()
        require(candidate.is_relative_to(root) and candidate.exists(),'quality_run_scope_path_missing')
        require((kind=='file' and candidate.is_file()) or (kind=='any'),'quality_run_scope_path_type_invalid')
        return candidate
    allowed=[local_path(value,'any') for value in run_scope.get('allowed_roots',[])]
    selected=[local_path(value,'any') for value in run_scope.get('input_paths',[])]
    require(bool(allowed) and bool(selected) and all(any(path.is_relative_to(base) for base in allowed) for path in selected),
            'quality_run_scope_selection_invalid')
    scope_files=run_scope.get('files')
    require(isinstance(scope_files,list) and bool(scope_files) and run_scope.get('scanned_files')==len(scope_files),
            'quality_run_scope_files_invalid')
    seen=set()
    for item in scope_files:
        require(isinstance(item,dict) and isinstance(item.get('file'),str) and item['file'] not in seen,
                'quality_run_scope_files_invalid')
        seen.add(item['file']); path=local_path(item['file'],'file')
        require(path!=paths['run_scope'] and any(path==choice or path.is_relative_to(choice) for choice in selected) and
                sha(path)==item.get('sha256') and path.stat().st_size==item.get('size_bytes'),
                'quality_run_scope_source_changed')
        paths['scope_source:'+item['file']]=path
    before = {key: sha(path) for key,path in paths.items()}
    inventory, plan, baseline = [read(paths[key]) for key in ('inventory','chapter_plan','baseline')]
    validate_stage_identity(inventory,'report_inventory',report.get('team_version'),
                            report.get('run_id'),report.get('client_scope'))
    validate_stage_identity(plan,'chapter_plan',report.get('team_version'),
                            report.get('run_id'),report.get('client_scope'))
    validate_baseline_identity(baseline,report.get('team_version'),report.get('run_id'),report.get('client_scope'))
    for item in (inventory, plan, baseline):
        require(item.get('run_id') == report.get('run_id'), 'quality_run_mismatch')
    require(inventory.get('client_scope') == report.get('client_scope'), 'quality_scope_mismatch')
    require(baseline.get('team_version') == report.get('team_version'), 'quality_version_mismatch')
    reports = inventory.get('reports')
    require(isinstance(reports,list) and bool(reports), 'quality_inventory_empty')
    ids = [item['report_id'] for item in reports]
    require(len(ids)==len(set(ids)) and inventory.get('report_count')==len(ids), 'quality_inventory_count_mismatch')
    require(not inventory.get('identification',{}).get('model_review_pending'), 'quality_identification_pending')
    min_level = config.get('min_level', 'L2')
    require(min_level in ('L2','L3','L4'), 'quality_min_level_invalid')
    depth_results, bodies, evidence_rows = [], {}, []
    for role,path in handoffs.items():
        body = read(path)
        require(body.get('agent_id')==role and body.get('run_id')==report.get('run_id'), 'quality_member_identity_mismatch')
        require(body.get('scope')==baseline.get('scope'), 'quality_member_scope_mismatch')
        result = depth.check_handoff(role,path,body,before['baseline'],min_level)
        require(result['status']=='passed', 'quality_depth_blocked:'+role)
        # Legacy code only warns on an omitted minimum analysis set; completion cannot.
        require(bool(body.get('analysis_depth',{}).get('minimum_analysis_set')), 'quality_analysis_set_missing')
        depth_results.append(result)
        bodies[role] = body
        evidence_rows.extend(conflicts.evidence_rows(body,role))
    with tempfile.TemporaryDirectory(prefix='omni-quality-') as tmp:
        output = Path(tmp)/'coverage.json'
        with contextlib.redirect_stdout(io.StringIO()):
            result = coverage.main(['--inventory',str(paths['inventory']), '--chapter-plan',str(paths['chapter_plan']),
                                    '--report-md',str(paths['report_md']), '--output',str(output)])
        cov = read(output)
        require(result==0 and cov['status'] in ('coverage_passed','coverage_passed_with_gaps'), 'quality_coverage_blocked')
        require(any(c['check_id']=='final_report_mentions_all' and c['status']=='pass' for c in cov['checks']), 'quality_body_unchecked')
    causal_review = conflicts.review_handoffs(
        bodies,
        report.get('run_id'),
        report.get('client_scope'),
        report.get('team_version'),
    )
    found = (conflicts.scan_numeric(evidence_rows,0.02) + conflicts.scan_caliber(evidence_rows,bodies) +
             conflicts.scan_direction(bodies) + conflicts.causal_conflicts(causal_review))
    if (root/'run-journal.sqlite').is_file():
        from behavior_audit import observe_conflicts
        hosts={str(body.get('agent_host','unknown')) for body in bodies.values()}
        kinds=set()
        for body in bodies.values():
            if body.get('host_observation_file'):
                observation=read(resolve(body['host_observation_file']))
                kinds.add(observation.get('evidence_kind','unclassified_host_observation'))
        observe_conflicts(root,report,found,{str(path.relative_to(root)):before[key] for key,path in paths.items()},
                          next(iter(hosts)) if len(hosts)==1 else 'mixed',
                          next(iter(kinds)) if len(kinds)==1 else 'unclassified_host_observation')
    adjudications=[]; challenges=[]
    if any(c['severity']=='hard' for c in found):
        if (root/'run-journal.sqlite').is_file():
            from challenge_runtime import validate_challenges
            challenges,challenge_sources=validate_challenges(root,report,found)
            for path,original in challenge_sources.items():
                paths[path]=Path(path); before[path]=original
        require(bool(config.get('adjudication')), 'quality_adjudication_required')
        verdict_path=resolve(config['adjudication'])
        paths['adjudication']=verdict_path
        before['adjudication']=sha(verdict_path)
        verdict=read(verdict_path)
        if challenges:
            for row in verdict.get('verdicts',[]):
                expected={item['role']:item['return_event_hash'] for item in challenges
                          if row.get('conflict_id') in item['conflict_ids']}
                assessed=row.get('challenge_review')
                require(isinstance(assessed,list) and all(isinstance(a,dict) for a in assessed) and
                        len(assessed)==len(expected) and {a.get('role') for a in assessed}==set(expected),
                        'adjudication_challenge_review_missing')
                require(all(a.get('return_event_hash')==expected[a['role']] and
                            a.get('disposition') in ('adopted','not_adopted','data_gap') and
                            isinstance(a.get('reason'),str) and bool(a['reason'].strip()) for a in assessed),
                        'adjudication_challenge_review_invalid')
        adjudications,sources=validate_adjudication(found,verdict,report,resolve,
                                                  {r['file_name'] for r in reports},baseline,inventory,before['baseline'])
        from decision_display import validate_presentation
        validate_presentation(report,verdict,paths['report_md'].read_text(encoding='utf-8-sig'))
        for path,original in sources.items():
            paths[path]=Path(path)
            before[path]=original
    else:
        require(not any(report.get(key) for key in ('adjudication_summary','adjudicated_claims','unresolved_conflicts',
                                                    'adjudicated_downstream')),
                'quality_decision_without_current_conflict')
    from report_metric_guard import validate_delivery_metrics as validate_report_metrics
    metric_checks=validate_report_metrics(report)
    from claim_source_guard import validate_report_sources
    claim_check=validate_report_sources(report,root,paths['report_md'].read_text(encoding='utf-8-sig'))
    from narrative_value_guard import validate_narrative_numbers
    narrative_check=validate_narrative_numbers(report)
    for item in claim_check['inputs']:
        path=resolve(item['file'])
        key='claim_source:'+item['file']
        paths[key]=path
        before[key]=item['sha256']
    require(before == {key:sha(path) for key,path in paths.items()}, 'quality_inputs_changed_during_check')
    return dict(status='quality_gate_passed', run_id=report['run_id'], client_scope=report['client_scope'],
                team_version=report['team_version'], report_revision=report['report_revision'],
                coverage_status=cov['status'], run_scope_status=run_scope['status'], depth=depth_results,
                causal_review=causal_review, conflicts=found, adjudications=adjudications,challenges=challenges,
                report_metric_checks=metric_checks,
                narrative_value_gate=narrative_check,
                claim_source_gate=claim_check,
                inputs=[dict(file=str(path.relative_to(root)),sha256=before[key]) for key,path in paths.items()])
