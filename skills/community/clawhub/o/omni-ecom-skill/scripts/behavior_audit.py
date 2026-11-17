"""Source-bound model observations and scoped behavior comparisons.

This is local monitoring, not a model API client. It never changes a model,
replays a platform write, or treats an unavailable measurement as zero.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

from artifact_contract import native_audit_identity
from run_journal import Journal, digest

TZ=timezone(timedelta(hours=8))
LABEL=re.compile(r'[A-Za-z0-9][A-Za-z0-9._:/-]{0,99}')
TERMINAL=('member_returned','member_rejected','member_failed')
METRICS=('structure_error_rate','handoff_rejection_rate','host_failure_rate','human_correction_rate','disagreement_rate','latency_ms','cost')


def require(value,reason):
    if not value: raise ValueError(reason)


def read(path):
    value=json.loads(Path(path).read_text(encoding='utf-8-sig'))
    require(isinstance(value,dict),'audit_json_invalid')
    return value


def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def timestamp(value):
    try:
        parsed=datetime.fromisoformat(str(value).replace('Z','+00:00'))
        require(parsed.tzinfo is not None,'audit_timezone_required')
        return parsed.astimezone(timezone.utc)
    except (TypeError,ValueError) as exc:
        raise ValueError('audit_timestamp_invalid') from exc


def finite(value):
    return type(value) in (int,float) and math.isfinite(value) and value>=0


def telemetry(observation):
    """Normalize only explicitly exposed metadata; drop invalid values with reasons."""
    source=observation.get('model')
    result=dict(model_alias='host-default',model_name=None,model_version=None,prompt_version=None,
                latency_ms=None,cost=None,currency=None,input_tokens=None,output_tokens=None,
                telemetry_state='unavailable',limitations=[])
    if source is None: return result
    if not isinstance(source,dict):
        result.update(telemetry_state='invalid',limitations=['model_metadata_invalid'])
        return result
    for name in ('model_alias','model_name','model_version','prompt_version'):
        value=source.get(name)
        if value is not None:
            if isinstance(value,str) and LABEL.fullmatch(value): result[name]=value
            else: result['limitations'].append(name+'_invalid')
    for name in ('latency_ms','cost','input_tokens','output_tokens'):
        value=source.get(name)
        if value is not None:
            if finite(value) and (not name.endswith('_tokens') or type(value) is int): result[name]=value
            else: result['limitations'].append(name+'_invalid')
    currency=source.get('currency')
    if isinstance(currency,str) and re.fullmatch('[A-Z]{3}',currency): result['currency']=currency
    elif currency is not None: result['limitations'].append('currency_invalid')
    if result['cost'] is not None and result['currency'] is None:
        result['cost']=None; result['limitations'].append('cost_currency_missing')
    known=any(result[k] is not None for k in ('model_name','model_version','prompt_version','latency_ms','cost','input_tokens','output_tokens'))
    result['telemetry_state']='partial' if result['limitations'] else ('recorded' if known else 'unavailable')
    return result


def observe_terminal(runtime,item):
    """Append metadata only after an actual recorded terminal observation."""
    rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
    matches=[r for r in rows if r['kind'] in TERMINAL and all(r['payload'].get(k)==item.get(k) for k in
             ('role','host','agent_task_id','attempt_id'))]
    require(bool(matches),'audit_terminal_missing')
    event=matches[-1]; p=event['payload']
    path=runtime.path(p['observation_file'])
    require(sha(path)==p['observation_sha256'],'audit_host_observation_changed')
    obs=read(path)
    metadata=telemetry(obs)
    identity=runtime.identity()
    payload=dict(**native_audit_identity('model_observation',identity['team_version']),**metadata,
                 task_class=identity['task_type'],role=p['role'],host=p['host'],
                 agent_task_id=p['agent_task_id'],attempt_id=p['attempt_id'],
                 observed_at=event['created_at'],terminal_event_hash=event['event_hash'],
                 terminal_kind=event['kind'],source_file=p['observation_file'],source_sha256=p['observation_sha256'],
                 quality_result=dict(handoff_status={'member_returned':'accepted','member_rejected':'rejected','member_failed':'host_failed'}[event['kind']]),
                 evidence_kind=obs.get('evidence_kind','unclassified_host_observation'))
    runtime.journal.append(runtime.run_id,runtime.client_scope,'model:'+p['role']+':'+p['attempt_id'],
                           'model_observation',payload)
    return payload


def record_feedback(runtime,source):
    """Record a supplied human feedback reference, not an inferred correction."""
    path=runtime.path(source); before=sha(path); value=read(path)
    require(value.get('run_id')==runtime.run_id and value.get('client_scope')==runtime.client_scope,'feedback_scope_mismatch')
    require(value.get('outcome') in ('corrected','accepted') and
            isinstance(value.get('message_reference'),str) and bool(value['message_reference'].strip()),'feedback_reference_missing')
    timestamp(value.get('observed_at'))
    rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
    terminal=next((r for r in reversed(rows) if r['kind']=='member_returned' and
                   all(r['payload'].get(k)==value.get(k) for k in ('role','host','agent_task_id','attempt_id'))),None)
    require(terminal is not None,'feedback_target_unreturned')
    require(sha(path)==before,'feedback_source_changed')
    payload=dict(**native_audit_identity('human_feedback',runtime.identity()['team_version']),
                 **{k:value[k] for k in ('role','host','agent_task_id','attempt_id','outcome','observed_at')})
    payload.update(reason='explicit_human_feedback',source_file=source,source_sha256=before,
                   terminal_event_hash=terminal['event_hash'])
    runtime.journal.append(runtime.run_id,runtime.client_scope,'feedback:'+before,'human_correction',payload)
    return payload


def observe_conflicts(root,report,found,inputs,host,evidence_kind):
    root=Path(root).resolve()
    if not (root/'run-journal.sqlite').is_file(): return
    for name,expected in inputs.items():
        path=(root/name).resolve()
        require(path.is_relative_to(root) and sha(path)==expected,'audit_scan_input_changed')
    journal=Journal(root/'run-journal.sqlite')
    try:
        identity=journal.db.execute('SELECT team_version FROM runs WHERE run_id=?',(report['run_id'],)).fetchone()
        require(identity is not None,'audit_run_missing')
        payload=dict(**native_audit_identity('quality_observation',identity['team_version']),
                     report_revision=report['report_revision'],has_conflict=bool(found),conflict_count=len(found),
                     host=host,evidence_kind=evidence_kind,inputs=inputs)
        journal.append(report['run_id'],report['client_scope'],'quality:'+digest(payload),'quality_observation',payload)
    finally: journal.close()


def snapshot(root,run_id,client_scope):
    root=Path(root).resolve()
    require((root/'run-journal.sqlite').is_file(),'audit_journal_missing')
    journal=Journal(root/'run-journal.sqlite',read_only=True)
    try:
        rows=journal.events(run_id,client_scope)
        identity=dict(journal.db.execute('SELECT * FROM runs WHERE run_id=?',(run_id,)).fetchone())
        models={r['payload'].get('terminal_event_hash'):r['payload'] for r in rows if r['kind']=='model_observation'}
        feedback={r['payload'].get('terminal_event_hash'):r['payload'] for r in rows if r['kind']=='human_correction' and
                  r['payload'].get('terminal_event_hash')}
        samples=[]
        for event in rows:
            if event['kind'] not in TERMINAL: continue
            p=event['payload']
            path=(root/p['observation_file']).resolve()
            require(path.is_relative_to(root) and sha(path)==p['observation_sha256'],'audit_host_observation_changed')
            obs=read(path)
            require(obs.get('task_id')==p['agent_task_id'] and obs.get('host')==p['host'] and
                    obs.get('run_id')==run_id and obs.get('client_scope')==client_scope,'audit_observation_identity_mismatch')
            expected=('failed','cancelled') if event['kind']=='member_failed' else ('completed',)
            require(obs.get('state') in expected,'audit_observation_not_terminal')
            model=models.get(event['event_hash'])
            actual=telemetry(obs)
            if model is not None:
                require(model.get('source_sha256')==p['observation_sha256'] and
                        all(model.get(k)==v for k,v in actual.items()),'audit_model_record_changed')
            review=feedback.get(event['event_hash'])
            corrected=None
            if review:
                f=(root/review['source_file']).resolve()
                require(f.is_relative_to(root) and sha(f)==review['source_sha256'],'audit_feedback_changed')
                corrected=review['outcome']=='corrected'
            samples.append(dict(**actual,run_id=run_id,client_scope=client_scope,team_version=identity['team_version'],
                 task_class=identity['task_type'],role=p['role'],host=p['host'],attempt_id=p['attempt_id'],
                 agent_task_id=p['agent_task_id'],terminal_kind=event['kind'],sample_id=event['event_hash'],
                 observed_at=event['created_at'],human_corrected=corrected,
                 structure_valid=True if event['kind']=='member_returned' else (
                     False if p.get('reason') in ('runtime_handoff_contract_invalid','runtime_review_result_invalid','runtime_json_invalid') else None),
                 evidence_kind=obs.get('evidence_kind','unclassified_host_observation')))
        latest_scans={r['payload']['report_revision']:r for r in rows if r['kind']=='quality_observation'}
        for event in latest_scans.values():
            p=event['payload']
            for name,expected in p['inputs'].items():
                path=(root/name).resolve()
                require(path.is_relative_to(root) and sha(path)==expected,'audit_scan_input_changed')
            samples.append(dict(**telemetry({}),run_id=run_id,client_scope=client_scope,
                 team_version=identity['team_version'],task_class=identity['task_type'],role='analysis-cohort',host=p['host'],
                 attempt_id=p['report_revision'],agent_task_id='',terminal_kind='quality_scan',sample_id=event['event_hash'],
                 observed_at=event['created_at'],human_corrected=None,has_conflict=p['has_conflict'],evidence_kind=p['evidence_kind']))
        return dict(schema_version='2.0',run_id=run_id,client_scope=client_scope,team_version=identity['team_version'],
                    status='behavior_snapshot',last_event_hash=rows[-1]['event_hash'] if rows else '',samples=samples)
    finally: journal.close()


def load_history(path,client_scope):
    """Only explicit run directories under the supplied history root, never a disk scan."""
    path=Path(path).resolve(); manifest=read(path)
    require(manifest.get('client_scope')==client_scope,'audit_history_scope_mismatch')
    entries=manifest.get('runs')
    require(isinstance(entries,list) and bool(entries),'audit_history_empty')
    seen=set(); snapshots=[]
    for item in entries:
        raw=item['run_dir']
        require(isinstance(raw,str) and not Path(raw).is_absolute(),'audit_history_path_invalid')
        root=(path.parent/raw).resolve()
        require(root.is_relative_to(path.parent),'audit_history_path_outside')
        key=item['run_id']
        require(key not in seen,'audit_history_duplicate_run'); seen.add(key)
        snapshots.append(snapshot(root,key,client_scope))
    return snapshots


def summarize(samples):
    """All rates expose their actual denominator. Unknown feedback is excluded."""
    host_done=[s for s in samples if s['terminal_kind'] in ('member_returned','member_rejected')]
    terminal=[s for s in samples if s['terminal_kind'] in TERMINAL]
    reviewed=[s for s in samples if s.get('human_corrected') is not None]
    scans=[s for s in samples if s.get('has_conflict') is not None]
    structured=[s for s in samples if s.get('structure_valid') is not None]
    def rate(num,den): return dict(value=num/den if den else None,numerator=num,denominator=den)
    def average(field):
        values=[s[field] for s in samples if s.get(field) is not None]
        return dict(value=sum(values)/len(values) if values else None,denominator=len(values))
    currencies=sorted({s['currency'] for s in samples if s.get('cost') is not None and s.get('currency')})
    cost=average('cost') if len(currencies)==1 else dict(value=None,denominator=0)
    cost['currencies']=currencies
    return dict(samples=len(samples),
        structure_error_rate=rate(sum(s['structure_valid'] is False for s in structured),len(structured)),
        handoff_rejection_rate=rate(sum(s['terminal_kind']=='member_rejected' for s in samples),len(host_done)),
        host_failure_rate=rate(sum(s['terminal_kind']=='member_failed' for s in terminal),len(terminal)),
        human_correction_rate=rate(sum(s['human_corrected'] is True for s in reviewed),len(reviewed)),
        disagreement_rate=rate(sum(s['has_conflict'] is True for s in scans),len(scans)),
        latency_ms=average('latency_ms'),cost=cost,
        model_variants=sorted({str(s.get('model_name'))+'@'+str(s.get('model_version')) for s in samples}))


def validate_sample(sample,scope):
    require(sample.get('client_scope')==scope,'audit_sample_scope_mismatch')
    require(sample.get('terminal_kind') in (*TERMINAL,'quality_scan'),'audit_sample_terminal_invalid')
    for k in ('run_id','sample_id','task_class','role','host','model_alias','observed_at'):
        require(isinstance(sample.get(k),str) and bool(sample[k]),'audit_sample_identity_missing')
    timestamp(sample['observed_at'])
    require(sample.get('human_corrected') is None or type(sample['human_corrected']) is bool,'audit_feedback_invalid')
    require(sample.get('has_conflict') is None or type(sample['has_conflict']) is bool,'audit_disagreement_invalid')
    require(sample.get('structure_valid') is None or type(sample['structure_valid']) is bool,'audit_structure_result_invalid')
    for k in ('latency_ms','cost'):
        require(sample.get(k) is None or finite(sample[k]),'audit_measurement_invalid')
    require(sample.get('cost') is None or bool(re.fullmatch('[A-Z]{3}',str(sample.get('currency','')))),'audit_currency_missing')


def compare(snapshots,client_scope,policy,split_at):
    """Compare earlier baseline to later observations in matching task/role cohorts."""
    require(policy.get('schema_version')=='2.0' and policy.get('policy_id') and policy.get('revision'),'audit_policy_invalid')
    for k in ('baseline_days','current_days','baseline_samples','current_samples'):
        require(type(policy.get(k)) is int and policy[k]>0,'audit_policy_invalid')
    require(policy['baseline_days']>=14,'audit_baseline_window_too_short')
    thresholds=policy.get('thresholds',{})
    require(set(thresholds)==set(METRICS) and all(finite(v) for v in thresholds.values()),'audit_thresholds_invalid')
    split=timestamp(split_at)
    start=split-timedelta(days=policy['baseline_days'])
    end=split+timedelta(days=policy['current_days'])
    cohorts=defaultdict(lambda:[[],[]]); seen=set(); kinds=set(); outside=0
    for bundle in snapshots:
        require(bundle.get('client_scope')==client_scope,'audit_snapshot_scope_mismatch')
        for sample in bundle.get('samples',[]):
            validate_sample(sample,client_scope)
            key=(sample['run_id'],sample['sample_id'])
            require(key not in seen,'audit_duplicate_sample'); seen.add(key)
            kind=sample.get('evidence_kind','unclassified_host_observation')
            require(isinstance(kind,str) and bool(kind),'audit_evidence_kind_invalid')
            kinds.add(kind)
            when=timestamp(sample['observed_at'])
            if not start<=when<end:
                outside+=1; continue
            group=tuple(sample[k] for k in ('task_class','role','host','model_alias'))+(kind,)
            cohorts[group][when>=split].append(sample)
    results=[]
    for key,(baseline,current) in sorted(cohorts.items()):
        before,after=summarize(baseline),summarize(current)
        days=len({timestamp(s['observed_at']).astimezone(TZ).date() for s in baseline})
        insufficient=days<policy['baseline_days'] or len(baseline)<policy['baseline_samples'] or len(current)<policy['current_samples']
        signals=[]; unavailable=[]
        for metric in METRICS:
            b,c=before[metric],after[metric]
            if b['value'] is None or c['value'] is None or (metric=='cost' and b['currencies']!=c['currencies']):
                unavailable.append(metric); continue
            if b['denominator']<policy['baseline_samples'] or c['denominator']<policy['current_samples']:
                unavailable.append(metric); continue
            change=c['value']-b['value']
            if not insufficient and change>thresholds[metric]:
                signals.append(dict(metric=metric,baseline=b['value'],current=c['value'],absolute_change=change,
                                    threshold=thresholds[metric],baseline_n=b['denominator'],current_n=c['denominator']))
        status='baseline_collecting' if insufficient else ('review_required' if signals else 'no_drift_in_observed_metrics')
        results.append(dict(cohort=dict(zip(('task_class','role','host','model_alias','evidence_kind'),key)),status=status,
                            baseline_days=days,baseline=before,current=after,signals=signals,unavailable_metrics=unavailable,
                            model_configuration_changed=before['model_variants']!=after['model_variants']))
    return dict(schema_version='2.0',status='behavior_comparison',client_scope=client_scope,split_at=split.isoformat(),
                policy_id=policy['policy_id'],policy_revision=policy['revision'],policy_sha256=digest(policy),
                threshold_status=policy.get('threshold_status','unverified'),
                baseline_start=start.isoformat(),current_end=end.isoformat(),samples_outside_windows=outside,
                evidence_kinds=sorted(kinds),cohorts=results,automatic_changes=False,
                next_action='inspect_flagged_runs_before_next_report' if any(c['signals'] for c in results) else 'continue_observation',
                limitation='Observations are recorded host evidence, not independent verification or causal proof.')


def write_new(path,payload):
    path=Path(path).resolve(); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream: json.dump(payload,stream,ensure_ascii=False,indent=2,allow_nan=False)


def record_comparison(runtime,policy,result,output):
    require(result.get('client_scope')==runtime.client_scope and result.get('policy_sha256')==digest(policy),
            'audit_comparison_identity_mismatch')
    target=runtime.path(output)
    team_version=runtime.identity()['team_version']
    with runtime.journal.transaction():
        rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
        policies=[r['payload'] for r in rows if r['kind']=='monitor_policy']
        prior=next((p for p in policies if p['policy_id']==policy['policy_id'] and p['revision']==policy['revision']),None)
        require(prior is None or prior['sha256']==digest(policy),'audit_policy_revision_reused')
        if prior is None:
            runtime.journal.append_locked(runtime.run_id,runtime.client_scope,'policy:'+policy['policy_id']+':'+policy['revision'],
                'monitor_policy',dict(**native_audit_identity('monitor_policy',team_version),
                                      policy_id=policy['policy_id'],revision=policy['revision'],sha256=digest(policy),
                                      previous_sha256=policies[-1]['sha256'] if policies else None))
        write_new(target,result)
        runtime.journal.append_locked(runtime.run_id,runtime.client_scope,'comparison:'+sha(target),'monitor_comparison',
            dict(**native_audit_identity('monitor_comparison',team_version),
                 output=output,sha256=sha(target),policy_sha256=digest(policy),next_action=result['next_action'],
                 policy_registry_reference=result.get('policy_registry_reference'),
                 automatic_changes=False))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    snap=sub.add_parser('snapshot')
    snap.add_argument('--run-dir',required=True); snap.add_argument('--run-id',required=True)
    cmp=sub.add_parser('compare')
    cmp.add_argument('--history',required=True); cmp.add_argument('--policy',required=True); cmp.add_argument('--split-at',required=True)
    cmp.add_argument('--policy-store-profile',required=True)
    cmp.add_argument('--audit-run-dir',required=True); cmp.add_argument('--audit-run-id',required=True)
    feedback=sub.add_parser('feedback')
    feedback.add_argument('--run-dir',required=True); feedback.add_argument('--run-id',required=True); feedback.add_argument('--source',required=True)
    for p in (snap,cmp,feedback):
        p.add_argument('--client-scope',required=True); p.add_argument('--output',required=True)
    args=parser.parse_args()
    try:
        if args.command=='snapshot': result=snapshot(args.run_dir,args.run_id,args.client_scope)
        elif args.command=='compare':
            policy=read(args.policy)
            from monitor_policy_store import MonitorPolicyStore
            store=MonitorPolicyStore.open(args.policy_store_profile)
            try:
                current,reference=store.current(args.client_scope,policy['policy_id'])
                require(current==policy,'audit_monitor_policy_not_current')
            finally: store.close()
            result=compare(load_history(args.history,args.client_scope),args.client_scope,policy,args.split_at)
            result['policy_registry_reference']=reference
            from host_runtime import Runtime
            runtime=Runtime(args.audit_run_dir,args.audit_run_id,args.client_scope)
            try: record_comparison(runtime,policy,result,args.output)
            finally: runtime.close()
        else:
            from host_runtime import Runtime
            runtime=Runtime(args.run_dir,args.run_id,args.client_scope)
            try: result=record_feedback(runtime,args.source)
            finally: runtime.close()
        if args.command!='compare': write_new(args.output,result)
        print(json.dumps(dict(status=result.get('status','feedback_recorded'),output=Path(args.output).name),ensure_ascii=False))
        return 0
    except (ValueError,OSError,KeyError,TypeError,sqlite3.Error) as exc:
        print(json.dumps(dict(status='behavior_audit_blocked',reason=str(exc)),ensure_ascii=False))
        return 2


if __name__=='__main__': raise SystemExit(main())
