"""Bind one targeted challenge round to selected native expert returns.

Native follow-up tools are invoked by the host, not by this recorder. Exported
observations remain user-editable claims, never independently authenticated proof.
"""
import argparse
import sqlite3
from datetime import datetime

import conflict_scan
from artifact_contract import native_runtime_event_identity, validate_baseline_identity
from host_runtime import Runtime, load, sha, require, validate_analysis_binding
from run_journal import digest, encoded


def context(runtime,report):
    config=load(runtime.root/'quality-inputs.json')
    binding,inputs=validate_analysis_binding(runtime.root,report,config['handoffs'])
    baseline=runtime.path(config['baseline'])
    validate_baseline_identity(load(baseline),report.get('team_version'),report.get('run_id'),report.get('client_scope'))
    inputs[str(baseline.relative_to(runtime.root))]=sha(baseline)
    bodies={role:load(runtime.path(path)) for role,path in config['handoffs'].items()}
    rows=[item for role,body in bodies.items() for item in conflict_scan.evidence_rows(body,role)]
    causal_review=conflict_scan.review_handoffs(
        bodies,report.get('run_id'),report.get('client_scope'),report.get('team_version'))
    found=(conflict_scan.scan_numeric(rows,0.02)+conflict_scan.scan_caliber(rows,bodies)+
           conflict_scan.scan_direction(bodies)+conflict_scan.causal_conflicts(causal_review))
    from adjudication_guard import fingerprint
    identity=dict(run_id=report['run_id'],client_scope=report['client_scope'],
                  team_version=report['team_version'],report_revision=report['report_revision'],
                  conflicts_sha256=fingerprint(found),selection_sha256=digest(binding),baseline_sha256=sha(baseline))
    round_id=digest(identity)
    targets={}
    for conflict in found:
        if conflict['severity']=='hard':
            for position in conflict['positions']:
                targets.setdefault(position['agent_id'],set()).add(conflict['conflict_id'])
    return identity,round_id,{r:sorted(ids) for r,ids in targets.items()},binding,inputs


def observe(runtime,path,request_hash,task,states):
    original=sha(path); value=load(path)
    require(value.get('run_id')==runtime.run_id and value.get('client_scope')==runtime.client_scope and
            value.get('host')==task['host'] and value.get('task_id')==task['agent_task_id'] and
            value.get('state') in states and value.get('request_sha256')==request_hash,
            'challenge_host_observation_mismatch')
    require(sha(path)==original,'challenge_observation_changed')
    return value,original


def start(runtime,request_file,observation_file):
    report=load(runtime.root/'report.json')
    identity,round_id,targets,binding,inputs=context(runtime,report)
    request_path=runtime.path(request_file); request_hash=sha(request_path); request=load(request_path)
    role=request.get('agent_id')
    require(role in targets,'challenge_role_not_in_conflict')
    require(all(request.get(k)==v for k,v in identity.items()) and request.get('round_id')==round_id and
            request.get('conflict_ids')==targets[role] and isinstance(request.get('question'),str) and
            bool(request['question'].strip()),'challenge_request_mismatch')
    task=next(m for m in binding['members'] if m['role']==role)
    _,observation_hash=observe(runtime,runtime.path(observation_file),request_hash,task,('running','created'))
    require(sha(request_path)==request_hash and all(sha(runtime.path(p))==h for p,h in inputs.items()),
            'challenge_inputs_changed')
    payload=dict(**native_runtime_event_identity('challenge_started',runtime.identity()['team_version']),
                 round_id=round_id,role=role,host=task['host'],agent_task_id=task['agent_task_id'],
                 request_file=request_file,request_sha256=request_hash,observation_file=observation_file,
                 observation_sha256=observation_hash,identity=identity,inputs=inputs,conflict_ids=targets[role])
    runtime.journal.append(runtime.run_id,runtime.client_scope,f'challenge:start:{round_id}:{role}',
                           'challenge_started',payload)
    return payload


def terminal(runtime,round_id,role,observation_file,response_file=None,record=True):
    try:
        return _terminal(runtime,round_id,role,observation_file,response_file,record)
    except ValueError as exc:
        # A native completed follow-up with invalid content must not wait forever.
        # Record rejection only when the terminal observation matches the dispatch.
        if record and response_file:
            rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
            matching=[r for r in rows if r['kind'].startswith('challenge_') and
                      r['payload'].get('round_id')==round_id and r['payload'].get('role')==role]
            if len(matching)==1 and matching[0]['kind']=='challenge_started':
                first=matching[0]['payload']
                try:
                    _,original=observe(runtime,runtime.path(observation_file),first['request_sha256'],first,('completed',))
                except (ValueError,OSError): pass
                else:
                    runtime.journal.append(runtime.run_id,runtime.client_scope,f'challenge:terminal:{round_id}:{role}',
                        'challenge_rejected',dict(**native_runtime_event_identity('challenge_rejected',runtime.identity()['team_version']),
                        round_id=round_id,role=role,host=first['host'],
                        agent_task_id=first['agent_task_id'],observation_file=observation_file,observation_sha256=original,
                        host_state='completed',reason=str(exc)))
        raise


def _terminal(runtime,round_id,role,observation_file,response_file=None,record=True):
    rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
    matching=[r for r in rows if r['kind'].startswith('challenge_') and
              r['payload'].get('round_id')==round_id and r['payload'].get('role')==role]
    require(bool(matching) and matching[0]['kind']=='challenge_started','challenge_dispatch_missing')
    first=matching[0]['payload']
    obs,obs_hash=observe(runtime,runtime.path(observation_file),first['request_sha256'],first,
                         ('completed',) if response_file else ('failed','cancelled'))
    event_type='challenge_returned' if response_file else 'challenge_failed'
    payload=dict(**native_runtime_event_identity(event_type,runtime.identity()['team_version']),
                 round_id=round_id,role=role,host=first['host'],agent_task_id=first['agent_task_id'],
                 observation_file=observation_file,observation_sha256=obs_hash)
    if response_file:
        require(sha(runtime.path(first['request_file']))==first['request_sha256'] and
                sha(runtime.path(first['observation_file']))==first['observation_sha256'] and
                all(sha(runtime.path(p))==h for p,h in first['inputs'].items()),'challenge_inputs_changed')
        response_path=runtime.path(response_file); response_hash=sha(response_path); response=load(response_path)
        require(all(response.get(k)==v for k,v in first['identity'].items()) and
                response.get('round_id')==round_id and response.get('agent_id')==role and
                response.get('agent_task_id',first['agent_task_id'])==first['agent_task_id'] and
                response.get('request_sha256')==first['request_sha256'] and
                obs.get('response_sha256')==response_hash,'challenge_response_binding_mismatch')
        answers=response.get('answers')
        require(isinstance(answers,list) and all(isinstance(a,dict) for a in answers) and
                sorted(a.get('conflict_id','') for a in answers)==first['conflict_ids'],
                'challenge_answers_incomplete')
        config=load(runtime.root/'quality-inputs.json')
        body=load(runtime.path(config['handoffs'][role]))
        known_ids={item['id'] for item in body.get('evidence_ledger',[]) if isinstance(item,dict) and item.get('id')}
        for answer in answers:
            require(answer.get('position') in ('maintain','revise','insufficient_data') and
                    isinstance(answer.get('reason'),str) and bool(answer['reason'].strip()) and
                    isinstance(answer.get('evidence_ids'),list) and
                    (bool(answer['evidence_ids']) or answer['position']=='insufficient_data'),
                    'challenge_answer_invalid')
            require(all(isinstance(e,str) and e in known_ids for e in answer['evidence_ids']) and
                    len(answer['evidence_ids'])==len(set(answer['evidence_ids'])),'challenge_evidence_id_unknown')
        try:
            require(datetime.fromisoformat(str(response.get('returned_at','')).replace('Z','+00:00')).tzinfo is not None,
                    'challenge_return_time_invalid')
        except ValueError as exc: raise ValueError('challenge_return_time_invalid') from exc
        require(sha(response_path)==response_hash,'challenge_response_changed')
        payload.update(response_file=response_file,response_sha256=response_hash)
    require(sha(runtime.path(observation_file))==obs_hash,'challenge_observation_changed')
    kind=event_type
    if record:
        runtime.journal.append(runtime.run_id,runtime.client_scope,f'challenge:terminal:{round_id}:{role}',kind,payload)
    return payload


def validate_challenges(root,report,found):
    runtime=Runtime(root,report['run_id'],report['client_scope'],read_only=True)
    try:
        identity,round_id,targets,binding,inputs=context(runtime,report)
        from adjudication_guard import fingerprint
        require(identity['conflicts_sha256']==fingerprint(found),'challenge_conflicts_changed')
        rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
        results=[]
        for role,ids in targets.items():
            matching=[r for r in rows if r['kind'].startswith('challenge_') and
                      r['payload'].get('round_id')==round_id and r['payload'].get('role')==role]
            require(len(matching)==2 and matching[0]['kind']=='challenge_started' and
                    matching[1]['kind']=='challenge_returned','challenge_return_missing:'+role)
            first,last=matching[0]['payload'],matching[1]['payload']
            require(first['identity']==identity and first['conflict_ids']==ids,'challenge_scope_changed')
            task=next(m for m in binding['members'] if m['role']==role)
            require(all(first[k]==last[k]==task[k] for k in ('host','agent_task_id')),'challenge_task_changed')
            request=load(runtime.path(first['request_file']))
            require(all(request.get(k)==v for k,v in identity.items()) and request.get('round_id')==round_id and
                    request.get('agent_id')==role and request.get('conflict_ids')==ids and
                    isinstance(request.get('question'),str) and bool(request['question'].strip()),'challenge_request_mismatch')
            observe(runtime,runtime.path(first['observation_file']),first['request_sha256'],task,('running','created'))
            require(terminal(runtime,round_id,role,last['observation_file'],last['response_file'],record=False)==last,
                    'challenge_terminal_changed')
            files=dict(first['inputs'])
            for item in (first,last):
                for name in ('request','observation','response'):
                    if name+'_file' in item: files[item[name+'_file']]=item[name+'_sha256']
            require(all(sha(runtime.path(p))==h for p,h in files.items()),'challenge_evidence_changed')
            inputs.update(files)
            results.append(dict(role=role,agent_task_id=last['agent_task_id'],round_id=round_id,
                                conflict_ids=ids,return_event_hash=matching[1]['event_hash']))
        return results,{str(runtime.path(p)):h for p,h in inputs.items()}
    finally: runtime.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ('run-dir','run-id','client-scope'): parser.add_argument('--'+key,required=True)
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('context')
    p=commands.add_parser('start'); p.add_argument('--request',required=True); p.add_argument('--observation',required=True)
    for name in ('accept','fail'):
        p=commands.add_parser(name)
        for key in ('round-id','role','observation'): p.add_argument('--'+key,required=True)
        if name=='accept': p.add_argument('--response',required=True)
    args=parser.parse_args()
    runtime=Runtime(args.run_dir,args.run_id,args.client_scope)
    try:
        if args.command=='context':
            identity,round_id,targets,_,_=context(runtime,load(runtime.root/'report.json'))
            result=dict(**identity,round_id=round_id,targets=targets)
        elif args.command=='start': result=start(runtime,args.request,args.observation)
        else: result=terminal(runtime,args.round_id,args.role,args.observation,getattr(args,'response',None))
        print(encoded(result)); return 0
    except (ValueError,OSError,KeyError,TypeError,sqlite3.Error) as exc:
        print(encoded(dict(status='challenge_blocked',reason=str(exc)))); return 2
    finally: runtime.close()


if __name__=='__main__': raise SystemExit(main())
