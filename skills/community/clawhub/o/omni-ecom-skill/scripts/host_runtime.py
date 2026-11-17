"""Bridge native host task observations to durable expert-run records.

The host still invokes its real tools. This module records and binds their
observations; it cannot independently authenticate user-editable tool exports.
"""
import argparse
import hashlib
import json
import re
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

from artifact_contract import native_runtime_event_identity
from run_journal import Journal, encoded

ROLES=('data-analyst','platform-ops','content-live-growth','ad-profit-optimizer')
HOSTS=('workbuddy','codex')
ID_PATTERN=r'(?:agent-[A-Za-z0-9_-]+|[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}|(?:/[A-Za-z0-9_-]+){2,8})'


def require(condition, message):
    if not condition: raise ValueError(message)


def load(path):
    value=json.loads(path.read_text(encoding='utf-8-sig'))
    require(isinstance(value,dict),'runtime_json_invalid')
    return value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def valid_task_id(value):
    return isinstance(value,str) and re.fullmatch(ID_PATTERN,value) is not None


def batch_roles(slots,roles=ROLES):
    require(type(slots) is int and slots>=1,'runtime_capacity_unavailable')
    return [list(roles[i:i+slots]) for i in range(0,len(roles),slots)]


class Runtime:
    def __init__(self, root, run_id, client_scope, read_only=False):
        self.root=Path(root).resolve()
        require(self.root.is_dir(),'runtime_directory_missing')
        if not read_only:
            require(not (self.root/'report-revision-successor.json').exists(),
                    'runtime_predecessor_archived_use_successor')
        self.run_id,self.client_scope=run_id,client_scope
        self.journal=Journal(self.root/'run-journal.sqlite',read_only=read_only)

    def close(self): self.journal.close()

    def path(self,raw):
        require(isinstance(raw,str) and raw and not Path(raw).is_absolute(),'runtime_path_invalid')
        path=(self.root/raw).resolve()
        require(path.is_relative_to(self.root),'runtime_path_outside')
        return path

    def init(self,version,task_type):
        self.journal.create(self.run_id,self.client_scope,version,task_type)

    def identity(self):
        self.journal.events(self.run_id,self.client_scope)
        return dict(self.journal.db.execute('SELECT * FROM runs WHERE run_id=?',(self.run_id,)).fetchone())

    def start(self,role,host,task_id,attempt,observation,manifest_file='review-manifest.json'):
        require(role in (*ROLES,'delivery-review'),'runtime_role_invalid')
        require(host in HOSTS and valid_task_id(task_id),'runtime_host_identity_invalid')
        require(re.fullmatch(r'[A-Za-z0-9_-]{1,80}',attempt) is not None,'runtime_attempt_invalid')
        if role in ROLES:
            if attempt not in ('a1','a2'):
                rows=self.journal.events(self.run_id,self.client_scope)
                terminal={item['payload'].get('attempt_id') for item in rows
                          if item['kind'] in ('member_failed','member_rejected') and
                          item['payload'].get('role')==role}
                require(not {'a1','a2'}.issubset(terminal),'member_retry_exhausted')
                raise ValueError('runtime_analysis_attempt_invalid')
        path=self.path(observation)
        original=sha(path)
        obs=load(path)
        require(obs.get('task_id')==task_id and obs.get('host')==host and
                obs.get('state') in ('created','running') and obs.get('run_id')==self.run_id and
                obs.get('client_scope')==self.client_scope,'runtime_start_observation_mismatch')
        binding={}
        if role=='delivery-review':
            status=self.status()
            require(not status['waiting'] and not status['challenges_waiting'] and not status['remaining_roles'],'review_before_analysis_returns')
            manifest=self.path(manifest_file)
            require(manifest.is_file(),'review_manifest_missing')
            from review_guard import validate_manifest, changed_entries
            content=load(manifest)
            validate_manifest(content)
            require(content['run_id']==self.run_id and content['client_scope']==self.client_scope,'runtime_review_scope_mismatch')
            require(not any(changed_entries(content)),'runtime_review_stale')
            from quality_gate import validate_quality, validate_frozen_quality
            report=load(self.root/'report.json')
            quality=validate_quality(self.root,report)
            validate_frozen_quality(content,self.root,quality)
            analysis,_=validate_analysis_binding(self.root,report,load(self.root/'quality-inputs.json')['handoffs'])
            require(content.get('runtime_gate')==analysis,'runtime_frozen_selection_mismatch')
            binding=dict(manifest_file=manifest_file,manifest_sha256=sha(manifest),
                         reviewed_manifest_sha256=content['manifest_sha256'])
        require(original==sha(path),'runtime_inputs_changed')
        p=dict(**native_runtime_event_identity('member_started',self.identity()['team_version']),
               role=role,host=host,agent_task_id=task_id,attempt_id=attempt,
               observation_file=observation,observation_sha256=original,**binding)
        return self.journal.append(self.run_id,self.client_scope,f'start:{role}:{attempt}','member_started',p)

    def accept(self,role,host,task_id,attempt,handoff_file,return_file,observation,output):
        try:
            return self._accept(role,host,task_id,attempt,handoff_file,return_file,observation,output)
        except ValueError as exc:
            # A completed native task with an invalid handoff is NOT a failed
            # host task, and must not remain waiting forever. Preserve that
            # distinction; only a matching completed host observation closes it.
            rows=self.journal.events(self.run_id,self.client_scope)
            identity=dict(role=role,host=host,agent_task_id=task_id,attempt_id=attempt)
            matching=[r for r in rows if r['kind'].startswith('member_') and
                      all(r['payload'].get(k)==v for k,v in identity.items())]
            if matching and matching[-1]['kind']=='member_started':
                path=self.path(observation)
                if path.is_file():
                    original=sha(path)
                    obs=load(path)
                    if (obs.get('task_id')==task_id and obs.get('host')==host and
                        obs.get('run_id')==self.run_id and obs.get('client_scope')==self.client_scope and
                        obs.get('state')=='completed' and sha(path)==original):
                        rejected=dict(**native_runtime_event_identity('member_rejected',self.identity()['team_version']),
                                      **identity,host_state='completed',reason=str(exc).split(':',1)[0],
                                      observation_file=observation,observation_sha256=original)
                        self.journal.append(self.run_id,self.client_scope,f'rejected:{role}:{attempt}',
                            'member_rejected',rejected)
                        from behavior_audit import observe_terminal
                        observe_terminal(self,rejected)
            raise

    def _accept(self,role,host,task_id,attempt,handoff_file,return_file,observation,output):
        # Read the exact dispatched attempt, not the newest file in a directory.
        rows=self.journal.events(self.run_id,self.client_scope)
        match=[r for r in rows if r['kind'].startswith('member_') and all(r['payload'].get(k)==v for k,v in
               dict(role=role,host=host,agent_task_id=task_id,attempt_id=attempt).items())]
        require(bool(match),'runtime_dispatch_missing')
        start=next((r for r in match if r['kind']=='member_started'),None)
        require(start is not None,'runtime_dispatch_missing')
        require(match[-1]['kind'] in ('member_started','member_returned'),'runtime_attempt_terminal_failed')
        start_path=self.path(start['payload']['observation_file'])
        require(sha(start_path)==start['payload']['observation_sha256'],'runtime_start_observation_changed')
        paths=[self.path(p) for p in (handoff_file,return_file,observation)]
        original=[sha(p) for p in paths]
        body,receipt,obs=[load(p) for p in paths]
        identity=self.identity()
        require(obs.get('task_id')==task_id and obs.get('host')==host and obs.get('state')=='completed' and
                obs.get('run_id')==self.run_id and obs.get('client_scope')==self.client_scope,'runtime_terminal_observation_missing')
        # A child may not know the native ID assigned after its initial prompt.
        # Bind the observed host ID here; if the child supplied an ID, it must agree.
        require(receipt.get('agent_task_id',task_id)==task_id and receipt.get('attempt_id')==attempt and
                receipt.get('run_id')==self.run_id and receipt.get('agent_id')==role and
                receipt.get('return_status')=='completed' and receipt.get('handoff_sha256')==original[0] and
                bool(str(receipt.get('contribution_summary') or '').strip()) and bool(receipt.get('response')),
                'runtime_return_binding_mismatch')
        try:
            returned_at=datetime.fromisoformat(str(receipt.get('returned_at','')).replace('Z','+00:00'))
            require(returned_at.tzinfo is not None,'runtime_return_time_missing')
        except ValueError as exc:
            raise ValueError('runtime_return_time_missing') from exc
        require(body.get('run_id')==self.run_id and body.get('agent_id')==role and
                body.get('client_scope')==self.client_scope and
                body.get('agent_version')==identity['team_version'],'runtime_handoff_identity_mismatch')
        require(body.get('agent_task_id',task_id)==task_id,'runtime_handoff_task_mismatch')
        if role in ROLES:
            core=Path(__file__).resolve().parents[1]/'skills'/'ecom-diagnosis-core'/'scripts'
            sys.path.insert(0,str(core)) if str(core) not in sys.path else None
            from validate_handoff import validate
            require(not validate(body),'runtime_handoff_contract_invalid')
        elif role=='delivery-review':
            manifest_path=self.path(start['payload']['manifest_file'])
            require(sha(manifest_path)==start['payload']['manifest_sha256'],'runtime_review_manifest_changed')
            from review_guard import validate_manifest, validate_review_result, changed_entries
            manifest=load(manifest_path)
            validate_manifest(manifest)
            validate_review_result(dict(body,agent_task_id=task_id),manifest)
            require(body.get('review_attempt_id')==attempt,'runtime_review_attempt_mismatch')
            require(body.get('review_status') in ('passed','conditional_pass','rejected') and
                    isinstance(body.get('required_changes'),list) and isinstance(body.get('findings'),list) and
                    bool(body.get('contribution_summary')),'runtime_review_result_invalid')
            require(body['review_status']!='passed' or not body['required_changes'],'runtime_review_result_invalid')
            require(not any(changed_entries(manifest)),'runtime_review_stale')
            require(body['review_status']=='passed' and not body['required_changes'],
                    'runtime_review_requires_report_revision')
        require(original==[sha(p) for p in paths],'runtime_inputs_changed')
        sealed=dict(body,agent_task_id=task_id,agent_attempt_id=attempt,agent_return_status='completed',
                    agent_returned_at=receipt['returned_at'],
                    agent_host=host,raw_handoff_file=handoff_file,raw_handoff_sha256=original[0],
                    agent_return_file=return_file,agent_return_sha256=original[1],
                    host_observation_file=observation,host_observation_sha256=original[2])
        target=self.path(output)
        if target.exists():
            require(load(target)==sealed,'runtime_sealed_handoff_conflict')
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('x',encoding='utf-8') as stream: stream.write(encoded(sealed))
        p=dict(**native_runtime_event_identity('member_returned',identity['team_version']),
               role=role,host=host,agent_task_id=task_id,attempt_id=attempt,handoff_file=output,
               handoff_sha256=sha(target),observation_file=observation,observation_sha256=original[2])
        self.journal.append(self.run_id,self.client_scope,f'return:{role}:{attempt}','member_returned',p)
        from behavior_audit import observe_terminal
        observe_terminal(self,p)
        return p

    def fail(self,role,host,task_id,attempt,observation):
        path=self.path(observation)
        obs=load(path)
        require(obs.get('task_id')==task_id and obs.get('host')==host and obs.get('run_id')==self.run_id and
                obs.get('client_scope')==self.client_scope and obs.get('state') in ('failed','cancelled'),
                'runtime_failure_not_terminal')
        p=dict(**native_runtime_event_identity('member_failed',self.identity()['team_version']),
               role=role,host=host,agent_task_id=task_id,attempt_id=attempt,
               observation_file=observation,observation_sha256=sha(path),reason=obs['state'])
        event=self.journal.append(self.run_id,self.client_scope,f'failed:{role}:{attempt}','member_failed',p)
        from behavior_audit import observe_terminal
        observe_terminal(self,p)
        return event

    def status(self):
        result=self.journal.status(self.run_id,self.client_scope)
        latest={}
        for item in result['members']:
            latest[item['role']]=item
        completed={role:item for role,item in latest.items() if item['state']=='member_returned'}
        for item in completed.values():
            require(sha(self.path(item['handoff_file']))==item['handoff_sha256'],'runtime_sealed_handoff_changed')
            require(sha(self.path(item['observation_file']))==item['observation_sha256'],'runtime_terminal_observation_changed')
        result['selected_returns']=completed
        result['remaining_roles']=[r for r in ROLES if r not in completed]
        result['next_action']='wait_existing_tasks' if result['waiting'] else (
            'dispatch_remaining_roles' if result['remaining_roles'] else 'quality_checks_and_frozen_review')
        if result['challenges_waiting']: result['next_action']='wait_existing_challenges'
        completions=[r for r in self.journal.events(self.run_id,self.client_scope) if r['kind']=='delivery_completed']
        if completions:
            recorded=completions[-1]['payload']
            try:
                path=self.path(recorded['receipt_file'])
                require(sha(path)==recorded['receipt_sha256'],'completion_receipt_changed')
                receipt=load(path)
                from artifact_contract import validate_receipt_identity
                validate_receipt_identity(receipt,'completion',receipt.get('team_version'))
                require(receipt.get('status')=='formal_delivery_complete' and receipt.get('run_id')==self.run_id and
                        receipt.get('client_scope')==self.client_scope,'completion_receipt_identity_mismatch')
                require(bool(receipt.get('input_fingerprints')),'completion_input_fingerprints_missing')
                for name,expected in receipt['input_fingerprints'].items():
                    require(sha(self.path(name))==expected,'completion_inputs_changed')
                require(not result['waiting'],'completion_members_waiting')
                require(not result['challenges_waiting'],'completion_challenges_waiting')
                expected=receipt['runtime_gate']['analysis']['members']
                actual=[_return_evidence(self,role,item)[0] for role,item in sorted(completed.items()) if role in ROLES]
                require(expected==actual,'completion_selection_changed')
                reviewed=receipt['runtime_gate'].get('review')
                if reviewed:
                    require('delivery-review' in completed and
                            _return_evidence(self,'delivery-review',completed['delivery-review'])[0]==reviewed,
                            'completion_review_changed')
                result['completion']=dict(status='formal_delivery_complete',**recorded)
                result['next_action']='reuse_verified_delivery'
            except (OSError,ValueError,KeyError,TypeError) as exc:
                result['completion']=dict(status='completion_invalidated',reason=str(exc),**recorded)
        return result

    def commit_completion(self,receipt,output):
        """Called only by completion_gate after all delivery checks.

        Hold the journal writer lock while binding current selected attempts and
        issuing the receipt. An orphan file after interruption is not completion:
        the event must exist too. No native runtime authenticity is implied.
        """
        target=self.path(output)
        require(not target.exists(),'completion_receipt_already_exists')
        with self.journal.transaction():
            from artifact_contract import native_receipt_identity, validate_receipt_identity
            validate_receipt_identity(receipt,'completion',receipt.get('team_version'))
            require(receipt.get('status')=='formal_delivery_complete' and receipt.get('run_id')==self.run_id and
                    receipt.get('client_scope')==self.client_scope,'completion_receipt_identity_mismatch')
            report=load(self.root/'report.json')
            config=load(self.root/'quality-inputs.json')
            analysis,_=validate_analysis_binding(self.root,report,config['handoffs'],require_idle=True)
            require(analysis==receipt['runtime_gate']['analysis'],'runtime_selection_changed_before_completion')
            reviewed=receipt['runtime_gate'].get('review')
            if report.get('collaboration_mode')=='comprehensive':
                evidence=receipt['review_files']
                actual,_=validate_review_binding(self.root,report,load(self.path(evidence['manifest'])),
                                                load(self.path(evidence['attestation'])))
                require(actual==reviewed,'runtime_review_changed_before_completion')
            require(bool(receipt.get('input_fingerprints')),'completion_input_fingerprints_missing')
            for name,expected in receipt['input_fingerprints'].items():
                require(sha(self.path(name))==expected,'completion_inputs_changed')
            target.parent.mkdir(parents=True,exist_ok=True)
            with target.open('x',encoding='utf-8') as stream:
                stream.write(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
            self.journal.append_locked(self.run_id,self.client_scope,'completion:'+receipt['report_revision'],
                'delivery_completed',dict(**native_receipt_identity('completion_event',receipt['team_version']),
                receipt_file=output,receipt_sha256=sha(target),
                report_revision=receipt['report_revision']))


def _return_evidence(runtime,role,item):
    """Revalidate all files of a selected attempt; a stored completion label is insufficient."""
    rows=runtime.journal.events(runtime.run_id,runtime.client_scope)
    fields=('role','host','agent_task_id','attempt_id')
    matching=[r for r in rows if r['kind'].startswith('member_') and
              all(r['payload'].get(k)==item[k] for k in fields)]
    start=next((r for r in matching if r['kind']=='member_started'),None)
    end=matching[-1] if matching else None
    require(start is not None and end['kind']=='member_returned','runtime_dispatch_missing')
    sealed_path=runtime.path(item['handoff_file'])
    sealed=load(sealed_path)
    require(sealed.get('agent_task_id')==item['agent_task_id'] and
            sealed.get('agent_attempt_id')==item['attempt_id'] and
            sealed.get('agent_host')==item['host'] and sealed.get('agent_id')==role and
            sealed.get('run_id')==runtime.run_id and sealed.get('client_scope')==runtime.client_scope and
            sealed.get('agent_version')==runtime.identity()['team_version'],'runtime_sealed_identity_mismatch')
    inputs={}
    for file,expected in [(item['handoff_file'],item['handoff_sha256']),
                          (start['payload']['observation_file'],start['payload']['observation_sha256']),
                          (sealed.get('raw_handoff_file'),sealed.get('raw_handoff_sha256')),
                          (sealed.get('agent_return_file'),sealed.get('agent_return_sha256')),
                          (item['observation_file'],item['observation_sha256'])]:
        path=runtime.path(file)
        require(sha(path)==expected,'runtime_evidence_changed')
        inputs[str(path.relative_to(runtime.root))]=expected
    raw=load(runtime.path(sealed['raw_handoff_file']))
    ret=load(runtime.path(sealed['agent_return_file']))
    obs=load(runtime.path(item['observation_file']))
    dispatched=load(runtime.path(start['payload']['observation_file']))
    for data,states in ((obs,('completed',)),(dispatched,('created','running'))):
        require(data.get('task_id')==item['agent_task_id'] and data.get('host')==item['host'] and
                data.get('state') in states and data.get('run_id')==runtime.run_id and
                data.get('client_scope')==runtime.client_scope,'runtime_observation_mismatch')
    require(ret.get('agent_task_id',item['agent_task_id'])==item['agent_task_id'] and ret.get('attempt_id')==item['attempt_id'] and
            ret.get('agent_id')==role and ret.get('run_id')==runtime.run_id and
            ret.get('return_status')=='completed' and ret.get('handoff_sha256')==sealed['raw_handoff_sha256'] and
            bool(str(ret.get('contribution_summary') or '').strip()) and bool(ret.get('response')),
            'runtime_return_binding_mismatch')
    require(sealed.get('agent_returned_at')==ret.get('returned_at') and bool(ret.get('returned_at')),
            'runtime_return_time_mismatch')
    require(all(sealed.get(k)==v for k,v in raw.items()),'runtime_raw_sealed_mismatch')
    return dict(role=role,host=item['host'],agent_task_id=item['agent_task_id'],attempt_id=item['attempt_id'],
                handoff_file=item['handoff_file'],handoff_sha256=item['handoff_sha256'],
                start_event_hash=start['event_hash'],return_event_hash=end['event_hash']),inputs,sealed,start


def validate_analysis_binding(root,report,handoffs,require_idle=False):
    """Return a stable analysis snapshot; do not freeze the mutable SQLite database."""
    require((Path(root)/'run-journal.sqlite').is_file(),'runtime_journal_missing')
    runtime=Runtime(root,report['run_id'],report['client_scope'],read_only=True)
    try:
        identity=runtime.identity()
        require(identity['team_version']==report.get('team_version') and
                identity['task_type']==report.get('task_type'),'runtime_report_identity_mismatch')
        status=runtime.status()
        require(not any(i['role'] in ROLES for i in status['waiting']),'runtime_analysis_waiting')
        require(not require_idle or not status['waiting'],'runtime_members_waiting')
        require(not require_idle or not status['challenges_waiting'],'runtime_challenges_waiting')
        selected={k:v for k,v in status['selected_returns'].items() if k in ROLES}
        require(set(selected)==set(handoffs),'runtime_selected_members_mismatch')
        bindings,inputs=[],{}
        for role in sorted(selected):
            item=selected[role]
            require(runtime.path(item['handoff_file'])==runtime.path(handoffs[role]),'runtime_selected_handoff_mismatch')
            binding,files,_,_=_return_evidence(runtime,role,item)
            bindings.append(binding); inputs.update(files)
        return dict(status='analysis_returns_bound',members=bindings,
                    runtime_proof=status['runtime_proof']),inputs
    finally: runtime.close()


def validate_review_binding(root,report,manifest,attestation):
    require((Path(root)/'run-journal.sqlite').is_file(),'runtime_journal_missing')
    runtime=Runtime(root,report['run_id'],report['client_scope'],read_only=True)
    try:
        status=runtime.status()
        require(not status['waiting'],'runtime_members_waiting')
        item=status['selected_returns'].get('delivery-review')
        require(item is not None,'runtime_reviewer_return_missing')
        binding,inputs,sealed,start=_return_evidence(runtime,'delivery-review',item)
        require(item['agent_task_id']==attestation.get('agent_task_id') and
                item['attempt_id']==attestation.get('review_attempt_id'),'runtime_review_attestation_mismatch')
        path=runtime.path(start['payload']['manifest_file'])
        require(sha(path)==start['payload']['manifest_sha256'] and load(path)==manifest,
                'runtime_review_manifest_changed')
        require(attestation.get('review_result_sha256')==sealed['raw_handoff_sha256'],
                'runtime_review_result_mismatch')
        for key in ('review_status','review_attempt_id','returned_at','report_revision','reviewed_manifest_sha256',
                    'reviewed_artifacts','findings','required_changes','contribution_summary'):
            require(sealed.get(key)==attestation.get(key),'runtime_review_result_mismatch')
        inputs[str(path.relative_to(runtime.root))]=sha(path)
        return binding,inputs
    finally: runtime.close()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-dir',required=True)
    parser.add_argument('--run-id',required=True)
    parser.add_argument('--client-scope',required=True)
    sub=parser.add_subparsers(dest='command',required=True)
    init=sub.add_parser('init'); init.add_argument('--team-version',required=True); init.add_argument('--task-type',required=True)
    sub.add_parser('status')
    for name in ('start','accept','fail'):
        p=sub.add_parser(name)
        for key in ('role','host','task-id','attempt','observation'): p.add_argument('--'+key,required=True)
        if name=='accept':
            for key in ('handoff','return-file','output'): p.add_argument('--'+key,required=True)
        if name=='start': p.add_argument('--manifest',default='review-manifest.json')
    args=parser.parse_args()
    runtime=Runtime(args.run_dir,args.run_id,args.client_scope,read_only=args.command=='status')
    try:
        if args.command=='init': runtime.init(args.team_version,args.task_type)
        elif args.command=='start': runtime.start(args.role,args.host,args.task_id,args.attempt,args.observation,args.manifest)
        elif args.command=='accept': runtime.accept(args.role,args.host,args.task_id,args.attempt,args.handoff,args.return_file,args.observation,args.output)
        elif args.command=='fail': runtime.fail(args.role,args.host,args.task_id,args.attempt,args.observation)
        print(encoded(runtime.status()))
        return 0
    except (ValueError,OSError,sqlite3.Error) as exc:
        print(encoded(dict(status='runtime_blocked',reason=str(exc))))
        return 2
    finally: runtime.close()


if __name__=='__main__': raise SystemExit(main())
