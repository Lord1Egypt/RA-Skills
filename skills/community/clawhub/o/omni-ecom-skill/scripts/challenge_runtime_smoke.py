"""Synthetic native follow-up exports, not real host execution evidence."""
import unittest
import subprocess
import sys
import os
from datetime import datetime,timezone

import challenge_runtime as challenge
import runtime_binding_smoke as fixture
from host_runtime import load,sha,validate_analysis_binding
from quality_gate import validate_quality


class ChallengeTests(unittest.TestCase):
    def setUp(self):
        self.fx=fixture.BindingTests()
        finish=self.fx.finish
        def changed(role,body,attempt='a1'):
            if role=='ad-profit-optimizer': body['evidence_ledger'][0]['value']=200000
            finish(role,body,attempt)
        self.fx.finish=changed
        self.fx.setUp()
        self.root,self.rt,self.report=self.fx.root,self.fx.rt,self.fx.report
        self.fx.fixture.verdict_fixture()
        self.identity,self.round_id,self.targets,_,_=challenge.context(self.rt,self.report)

    def tearDown(self): self.fx.tearDown()

    def begin(self,role):
        request=dict(**self.identity,round_id=self.round_id,agent_id=role,conflict_ids=self.targets[role],
                     question='请核对 GMV 的原始口径，说明保留或修订的理由及证据。合成测试。')
        path=f'challenge-{role}-request.json'
        fixture.write(self.root/path,request)
        obs=dict(run_id=self.report['run_id'],client_scope=self.report['client_scope'],host='codex',
                 task_id=self.fx.tasks[role],state='running',request_sha256=sha(self.root/path),evidence_kind='synthetic_fixture')
        fixture.write(self.root/f'challenge-{role}-start.json',obs)
        return challenge.start(self.rt,path,f'challenge-{role}-start.json')

    def response(self,role):
        raw=f'challenge-{role}-response.json'
        obs=f'challenge-{role}-end.json'
        value=dict(**self.identity,round_id=self.round_id,agent_id=role,agent_task_id=self.fx.tasks[role],
                   request_sha256=sha(self.root/f'challenge-{role}-request.json'),
                   returned_at=datetime.now(timezone.utc).isoformat(),
                   answers=[dict(conflict_id=cid,position='revise',reason='合成回传：重复计数，按原始表合计',
                                 evidence_ids=['E1']) for cid in self.targets[role]])
        fixture.write(self.root/raw,value)
        observation=dict(run_id=self.report['run_id'],client_scope=self.report['client_scope'],host='codex',
                         task_id=self.fx.tasks[role],state='completed',request_sha256=value['request_sha256'],
                         response_sha256=sha(self.root/raw),evidence_kind='synthetic_fixture')
        fixture.write(self.root/obs,observation)
        return raw,obs

    def finish(self,role):
        raw,obs=self.response(role)
        return challenge.terminal(self.rt,self.round_id,role,obs,raw)

    def all_returns(self):
        for role in self.targets: self.begin(role); self.finish(role)
        verdict=load(self.root/'verdict.json')
        rows=self.rt.journal.events(self.rt.run_id,self.rt.client_scope)
        for item in verdict['verdicts']:
            item['challenge_review']=[dict(role=role,return_event_hash=next(r['event_hash'] for r in rows if
                r['kind']=='challenge_returned' and r['payload']['role']==role),disposition='adopted',
                reason='合成测试：核对回复并采用原始表复算值') for role,ids in self.targets.items() if item['conflict_id'] in ids]
        fixture.write(self.root/'verdict.json',verdict)
        fixture.quality_fixture.present_verdict(self.root,self.report,verdict)

    def test_recomputation_alone_cannot_skip_real_challenge_returns(self):
        with self.assertRaisesRegex(ValueError,'challenge_return_missing'):
            validate_quality(self.root,self.report)

    def test_bound_round_allows_numeric_quality_and_freezes_sources(self):
        self.all_returns()
        result=validate_quality(self.root,self.report)
        self.assertEqual(len(result['challenges']),len(self.targets))
        files={i['file'].replace('\\','/') for i in result['inputs']}
        self.assertIn('challenge-data-analyst-response.json',files)
        manifest=self.fx.freeze()
        self.assertEqual(manifest['quality_gate']['challenges'],result['challenges'])

    def test_full_completion_with_bound_challenge(self):
        self.all_returns(); self.fx.freeze(); self.fx.review()
        code,output=self.fx.complete()
        self.assertEqual(code,0,output)
        self.assertEqual(self.rt.status()['next_action'],'reuse_verified_delivery')

    def test_pending_challenge_blocks_idle_and_review(self):
        self.begin('data-analyst')
        self.assertEqual(self.rt.status()['next_action'],'wait_existing_challenges')
        with self.assertRaisesRegex(ValueError,'runtime_challenges_waiting'):
            validate_analysis_binding(self.root,self.report,self.fx.config['handoffs'],require_idle=True)
        with self.assertRaisesRegex(ValueError,'challenge_return_missing'): self.fx.freeze()

    def test_wrong_native_task_cannot_return_for_expert(self):
        self.begin('data-analyst'); raw,obs=self.response('data-analyst')
        value=load(self.root/obs); value['task_id']=self.fx.tasks['platform-ops']; fixture.write(self.root/obs,value)
        with self.assertRaisesRegex(ValueError,'host_observation_mismatch'):
            challenge.terminal(self.rt,self.round_id,'data-analyst',obs,raw)

    def test_terminal_requires_exact_response_hash(self):
        self.begin('data-analyst'); raw,obs=self.response('data-analyst')
        value=load(self.root/raw); value['answers'][0]['reason']='改写后的文本'; fixture.write(self.root/raw,value)
        with self.assertRaisesRegex(ValueError,'response_binding_mismatch'):
            challenge.terminal(self.rt,self.round_id,'data-analyst',obs,raw)

    def test_returned_round_tamper_blocks_quality(self):
        self.all_returns()
        path=self.root/'challenge-data-analyst-response.json'; value=load(path)
        value['answers'][0]['reason']='after acceptance'; fixture.write(path,value)
        with self.assertRaisesRegex(ValueError,'response_binding_mismatch|evidence_changed'):
            validate_quality(self.root,self.report)

    def test_one_round_cannot_be_reopened_with_changed_request(self):
        self.begin('data-analyst'); self.finish('data-analyst')
        path=self.root/'challenge-data-analyst-request.json'; value=load(path); value['question']='重复质疑'; fixture.write(path,value)
        obs=self.root/'challenge-data-analyst-start.json'; value=load(obs); value['request_sha256']=sha(path); fixture.write(obs,value)
        with self.assertRaisesRegex(ValueError,'idempotency_key_conflict'):
            challenge.start(self.rt,path.name,obs.name)

    def test_failure_is_terminal_not_a_successful_response(self):
        self.begin('data-analyst')
        path=self.root/'challenge-data-analyst-start.json'; value=load(path); value['state']='failed'
        fixture.write(self.root/'challenge-failed.json',value)
        challenge.terminal(self.rt,self.round_id,'data-analyst','challenge-failed.json')
        self.assertFalse(self.rt.status()['challenges_waiting'])
        raw,obs=self.response('data-analyst')
        with self.assertRaisesRegex(ValueError,'idempotency_key_conflict'):
            challenge.terminal(self.rt,self.round_id,'data-analyst',obs,raw)
        with self.assertRaisesRegex(ValueError,'challenge_return_missing'): validate_quality(self.root,self.report)

    def test_incomplete_answers_do_not_count_as_return(self):
        self.begin('data-analyst'); raw,obs=self.response('data-analyst')
        value=load(self.root/raw); value['answers']=[]; fixture.write(self.root/raw,value)
        value=load(self.root/obs); value['response_sha256']=sha(self.root/raw); fixture.write(self.root/obs,value)
        with self.assertRaisesRegex(ValueError,'answers_incomplete'):
            challenge.terminal(self.rt,self.round_id,'data-analyst',obs,raw)
        self.assertFalse(self.rt.status()['challenges_waiting'])
        rows=self.rt.journal.events(self.rt.run_id,self.rt.client_scope)
        self.assertEqual(rows[-1]['kind'],'challenge_rejected')

    def test_unknown_evidence_cannot_be_claimed_in_reply(self):
        self.begin('data-analyst'); raw,obs=self.response('data-analyst')
        value=load(self.root/raw); value['answers'][0]['evidence_ids']=['invented']; fixture.write(self.root/raw,value)
        value=load(self.root/obs); value['response_sha256']=sha(self.root/raw); fixture.write(self.root/obs,value)
        with self.assertRaisesRegex(ValueError,'evidence_id_unknown'):
            challenge.terminal(self.rt,self.round_id,'data-analyst',obs,raw)

    def test_still_running_observation_is_not_rejected_or_returned(self):
        self.begin('data-analyst'); raw,obs=self.response('data-analyst')
        value=load(self.root/obs); value['state']='running'; fixture.write(self.root/obs,value)
        with self.assertRaisesRegex(ValueError,'host_observation_mismatch'):
            challenge.terminal(self.rt,self.round_id,'data-analyst',obs,raw)
        self.assertEqual(len(self.rt.status()['challenges_waiting']),1)

    def test_native_failure_closes_wait_even_if_input_changed(self):
        self.begin('data-analyst')
        path=self.root/'challenge-data-analyst-start.json'; value=load(path); value['state']='failed'
        fixture.write(self.root/'challenge-failed.json',value)
        (self.root/'challenge-data-analyst-request.json').write_text('{}',encoding='utf-8')
        challenge.terminal(self.rt,self.round_id,'data-analyst','challenge-failed.json')
        self.assertFalse(self.rt.status()['challenges_waiting'])

    def test_changed_report_revision_requires_a_new_binding(self):
        self.all_returns()
        self.report['report_revision']='R2'; fixture.write(self.root/'report.json',self.report)
        config=load(self.root/'quality-inputs.json'); config['report_revision']='R2'; fixture.write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'challenge_return_missing'): validate_quality(self.root,self.report)

    def test_idempotent_retry_does_not_duplicate_round(self):
        first=self.begin('data-analyst')
        self.assertEqual(challenge.start(self.rt,first['request_file'],first['observation_file']),first)
        last=self.finish('data-analyst')
        self.assertEqual(challenge.terminal(self.rt,self.round_id,'data-analyst',last['observation_file'],last['response_file']),last)
        rows=[r for r in self.rt.journal.events(self.rt.run_id,self.rt.client_scope) if r['kind'].startswith('challenge_')]
        self.assertEqual(len(rows),2)

    def test_lead_must_record_disposition_of_each_actual_reply(self):
        self.all_returns()
        value=load(self.root/'verdict.json'); value['verdicts'][0]['challenge_review'].pop(); fixture.write(self.root/'verdict.json',value)
        with self.assertRaisesRegex(ValueError,'challenge_review_missing'): validate_quality(self.root,self.report)

    def test_lead_cannot_cite_another_return_event(self):
        self.all_returns()
        value=load(self.root/'verdict.json'); value['verdicts'][0]['challenge_review'][0]['return_event_hash']='0'*64
        fixture.write(self.root/'verdict.json',value)
        with self.assertRaisesRegex(ValueError,'challenge_review_invalid'): validate_quality(self.root,self.report)

    def test_cli_context_and_start_use_the_same_native_binding(self):
        import json
        prefix=[sys.executable,'-X','utf8',challenge.__file__,'--run-dir',str(self.root),
                '--run-id',self.rt.run_id,'--client-scope',self.rt.client_scope]
        proc=subprocess.run(prefix+['context'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(proc.returncode,0,proc.stderr+proc.stdout)
        self.assertEqual(json.loads(proc.stdout)['round_id'],self.round_id)
        first=self.begin('data-analyst')
        proc=subprocess.run(prefix+['start','--request',first['request_file'],'--observation',first['observation_file']],
                            capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(proc.returncode,0,proc.stderr+proc.stdout)
        self.assertEqual(json.loads(proc.stdout)['agent_task_id'],self.fx.tasks['data-analyst'])

    def test_caliber_conflict_fingerprint_is_stable_across_processes(self):
        code="""import conflict_scan as c; from adjudication_guard import fingerprint
b={r:{'analysis_depth':{'baseline_ack':{'deviations':[{'item':'metric','reason':r}]}}} for r in ('data-analyst','platform-ops')}
rows=[{'agent_id':r,'metric':'ROI','formula':r,'value':1} for r in b]
print(fingerprint(c.scan_caliber(rows,b)))
"""
        hashes=[]
        for seed in ('1','2','99'):
            proc=subprocess.run([sys.executable,'-X','utf8','-c',code],cwd=str(self.root),
                env=dict(os.environ,PYTHONPATH=str(__import__('pathlib').Path(challenge.__file__).parent),PYTHONHASHSEED=seed),
                capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(proc.returncode,0,proc.stderr); hashes.append(proc.stdout.strip())
        self.assertEqual(len(set(hashes)),1)


if __name__=='__main__': unittest.main()
