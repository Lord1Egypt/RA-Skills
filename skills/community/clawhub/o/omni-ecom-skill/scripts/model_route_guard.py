"""Assess source-bound model cohorts; never changes a host model route."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from artifact_contract import native_audit_identity
from run_journal import check_payload, digest


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read(path):
    value=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    check_payload(value); digest(value)
    require(isinstance(value,dict),'model_route_json_invalid')
    return value


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _metric_ready(summary, metric, minimum):
    value=summary.get(metric)
    return isinstance(value,dict) and value.get('value') is not None and \
           type(value.get('denominator')) is int and value['denominator'] >= minimum


def assess(comparison, policy, request, *, comparison_sha256, policy_sha256):
    require(all(isinstance(x,str) and len(x)==64 and all(c in '0123456789abcdef' for c in x)
                for x in (comparison_sha256,policy_sha256)),'model_route_source_hash_invalid')
    require(comparison.get('schema_version')=='2.0' and comparison.get('status')=='behavior_comparison',
            'model_route_comparison_invalid')
    require(policy.get('schema_version')=='2.0' and digest(policy)==policy_sha256 and
            comparison.get('policy_sha256')==policy_sha256,'model_route_policy_binding_invalid')
    required=('request_id','client_scope','team_version','task_class','role','host',
              'current_model_alias','candidate_model_alias','requested_by','reason')
    require(isinstance(request,dict) and set(request)==set(required) and
            all(isinstance(request.get(k),str) and request[k].strip() for k in required),
            'model_route_request_invalid')
    require(request['current_model_alias']!=request['candidate_model_alias'],
            'model_route_candidate_must_differ')
    require(comparison.get('client_scope')==request['client_scope'],
            'model_route_client_scope_mismatch')
    reference=comparison.get('policy_registry_reference')
    require(isinstance(reference,dict) and reference.get('client_scope')==request['client_scope'] and
            reference.get('policy_id')==policy.get('policy_id') and reference.get('revision')==policy.get('revision') and
            reference.get('policy_sha256')==policy_sha256 and reference.get('source_kind')=='native_v2' and
            reference.get('current_authority') is True and reference.get('legacy_permissions_inherited') is False,
            'model_route_registered_policy_required')
    calibration=policy.get('live_calibration')
    require(isinstance(calibration,dict) and calibration.get('manual_approval_required') is True and
            calibration.get('automatic_model_override') is False and
            policy.get('automatic_model_override') is False,'model_route_automatic_override_forbidden')
    kinds=calibration.get('eligible_evidence_kinds')
    metrics=calibration.get('required_metrics')
    require(isinstance(kinds,list) and kinds and all(isinstance(x,str) and x for x in kinds) and
            isinstance(metrics,list) and metrics and all(x in
            ('structure_error_rate','handoff_rejection_rate','host_failure_rate',
             'human_correction_rate','disagreement_rate','latency_ms','cost') for x in metrics),
            'model_route_calibration_policy_invalid')
    for key in ('minimum_baseline_days','minimum_baseline_samples','minimum_current_samples'):
        require(type(calibration.get(key)) is int and calibration[key]>0,
                'model_route_calibration_policy_invalid')
    matches={}
    for cohort in comparison.get('cohorts',[]):
        identity=cohort.get('cohort') or {}
        if all(identity.get(k)==request[k] for k in ('task_class','role','host')) and \
           identity.get('model_alias') in (request['current_model_alias'],request['candidate_model_alias']):
            alias=identity['model_alias']
            require(alias not in matches,'model_route_ambiguous_cohort')
            matches[alias]=cohort
    reasons=[]
    if set(matches)!={request['current_model_alias'],request['candidate_model_alias']}:
        reasons.append('both_model_cohorts_required')
    if comparison.get('threshold_status')!=calibration.get('required_threshold_status'):
        reasons.append('live_thresholds_not_validated')
    summaries={}
    for alias,cohort in matches.items():
        identity=cohort.get('cohort') or {}; before=cohort.get('baseline') or {}; current=cohort.get('current') or {}
        summaries[alias]=dict(cohort=identity,status=cohort.get('status'),baseline=before,current=current,
                              signals=cohort.get('signals',[]),unavailable_metrics=cohort.get('unavailable_metrics',[]))
        if identity.get('evidence_kind') not in kinds: reasons.append(alias+':non_live_evidence_kind')
        if cohort.get('status')!='no_drift_in_observed_metrics': reasons.append(alias+':cohort_not_stable')
        if cohort.get('model_configuration_changed') is not False: reasons.append(alias+':model_configuration_changed')
        if type(cohort.get('baseline_days')) is not int or cohort['baseline_days']<calibration['minimum_baseline_days']:
            reasons.append(alias+':baseline_days_insufficient')
        if before.get('samples',0)<calibration['minimum_baseline_samples'] or \
           current.get('samples',0)<calibration['minimum_current_samples']:
            reasons.append(alias+':sample_count_insufficient')
        for metric in metrics:
            if not (_metric_ready(before,metric,calibration['minimum_baseline_samples']) and
                    _metric_ready(current,metric,calibration['minimum_current_samples'])):
                reasons.append(alias+':metric_unavailable:'+metric)
    reasons=sorted(set(reasons))
    ready=not reasons
    return dict(**native_audit_identity('model_route_assessment',request['team_version']),
                request_id=request['request_id'],client_scope=request['client_scope'],
                team_version=request['team_version'],task_class=request['task_class'],role=request['role'],
                host=request['host'],current_model_alias=request['current_model_alias'],
                candidate_model_alias=request['candidate_model_alias'],requested_by=request['requested_by'],
                reason=request['reason'],comparison_sha256=comparison_sha256,policy_sha256=policy_sha256,
                status='manual_route_review_ready' if ready else 'live_baseline_not_ready',
                evidence_kind='eligible_live_cohort_comparison' if ready else 'calibration_readiness_check',
                calibration_ready=ready,reasons=reasons,cohort_summaries=summaries,
                automatic_changes=False,host_model_changed=False,route_selection_applied=False,
                explicit_user_or_admin_approval_required=True,formal_acceptance_completed=False)


def write_new(path,value):
    target=Path(path).resolve(); target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False); stream.write('\n')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--comparison',required=True); ap.add_argument('--policy',required=True)
    ap.add_argument('--request',required=True); ap.add_argument('--output',required=True)
    ap.add_argument('--policy-store-profile',required=True)
    args=ap.parse_args()
    try:
        paths=[Path(x).resolve() for x in (args.comparison,args.policy,args.request)]
        output=Path(args.output).resolve()
        require(output not in paths and not output.exists(),'model_route_output_must_be_new')
        comparison,policy,request=map(read,paths)
        from monitor_policy_store import MonitorPolicyStore
        store=MonitorPolicyStore.open(args.policy_store_profile)
        try: store.assert_current(request['client_scope'],policy,comparison.get('policy_registry_reference'))
        finally: store.close()
        result=assess(comparison,policy,request,comparison_sha256=sha(paths[0]),policy_sha256=digest(policy))
        # JSON canonical hash and byte hash differ; comparison binds policy canonically,
        # while the artifact also freezes the exact source file bytes below.
        result['policy_file_sha256']=sha(paths[1]); result['request_file_sha256']=sha(paths[2])
        write_new(output,result)
        print(json.dumps({'status':result['status'],'output':str(output)},ensure_ascii=False))
        return 0 if result['calibration_ready'] else 2
    except (OSError,ValueError,KeyError,TypeError,json.JSONDecodeError) as exc:
        print(json.dumps({'status':'model_route_assessment_blocked','reason':str(exc)},ensure_ascii=False))
        return 2


if __name__=='__main__': raise SystemExit(main())
