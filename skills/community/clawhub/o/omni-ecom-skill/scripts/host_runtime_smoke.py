"""Synthetic task exports exercise dispatch/return/restart binding; not native proof."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from datetime import datetime,timezone

from analysis_depth_smoke import BODY
from host_runtime import Runtime,batch_roles,sha


def write(path,value): path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.rt=Runtime(self.root,'runtime-test','test-client')
        self.rt.init('2.0.3','monthly_report')
        self.role='data-analyst'
        self.host='codex'
        self.task='11111111-1111-4111-8111-111111111111'
        self.args=(self.role,self.host,self.task,'a1')
        self.obs=dict(run_id='runtime-test',client_scope='test-client',host=self.host,task_id=self.task,
                      state='running',evidence_kind='synthetic_fixture')
        write(self.root/'started.json',self.obs)

    def tearDown(self):
        self.rt.close()
        self.tmp.cleanup()

    def start(self): self.rt.start(*self.args,'started.json')

    def make_return(self):
        body=copy.deepcopy(BODY)
        body.update(run_id='runtime-test',client_scope='test-client',agent_version='2.0.3',
                    created_by_team_version='2.0.3',judgments=[])
        write(self.root/'handoff.json',body)
        ret=dict(run_id='runtime-test',agent_id=self.role,agent_task_id=self.task,attempt_id='a1',
                 returned_at=datetime.now(timezone.utc).isoformat(),
                 return_status='completed',handoff_sha256=sha(self.root/'handoff.json'),
                 contribution_summary='合成测试贡献',response={'result':'ok'})
        write(self.root/'return.json',ret)
        write(self.root/'completed.json',dict(self.obs,state='completed'))

    def accept(self):
        return self.rt.accept(*self.args,'handoff.json','return.json','completed.json','sealed.json')

    def test_native_id_preserved(self):
        self.start(); self.make_return(); self.accept()
        data=json.loads((self.root/'sealed.json').read_text(encoding='utf-8'))
        self.assertEqual(data['agent_task_id'],self.task)
        self.assertEqual(self.rt.status()['remaining_roles'],['platform-ops','content-live-growth','ad-profit-optimizer'])

    def test_codex_canonical_task_name_is_preserved(self):
        self.task='/root/codex_v2_data_r1'
        self.args=(self.role,self.host,self.task,'a1')
        self.obs.update(task_id=self.task)
        write(self.root/'started.json',self.obs)
        self.start(); self.make_return(); self.accept()
        data=json.loads((self.root/'sealed.json').read_text(encoding='utf-8'))
        self.assertEqual(data['agent_task_id'],self.task)

    def test_restart_waits_existing(self):
        self.start(); self.rt.close()
        self.rt=Runtime(self.root,'runtime-test','test-client')
        self.assertEqual(self.rt.status()['next_action'],'wait_existing_tasks')

    def test_no_double_dispatch_while_waiting(self):
        self.start()
        write(self.root/'second.json',dict(self.obs,task_id='agent-another'))
        with self.assertRaisesRegex(ValueError,'role_still_waiting'):
            self.rt.start(self.role,self.host,'agent-another','a2','second.json')

    def test_analysis_attempt_id_must_be_canonical(self):
        with self.assertRaisesRegex(ValueError,'runtime_analysis_attempt_invalid'):
            self.rt.start(self.role,self.host,self.task,'data-analyst-a1','started.json')

    def test_wrong_attempt_return(self):
        self.start(); self.make_return()
        path=self.root/'return.json'
        ret=json.loads(path.read_text(encoding='utf-8')); ret['attempt_id']='a2'; write(path,ret)
        with self.assertRaisesRegex(ValueError,'return_binding'):
            self.accept()

    def test_return_summary_and_response_are_mandatory(self):
        self.start(); self.make_return()
        path=self.root/'return.json'
        ret=json.loads(path.read_text(encoding='utf-8'))
        ret.pop('contribution_summary')
        ret['summary_for_lead']='wrong alias'
        write(path,ret)
        with self.assertRaisesRegex(ValueError,'return_binding'):
            self.accept()
        self.assertEqual(self.rt.status()['members'][0]['state'],'member_rejected')

    def test_child_without_host_id_binds_observed_id(self):
        self.start(); self.make_return()
        path=self.root/'return.json'
        ret=json.loads(path.read_text(encoding='utf-8')); del ret['agent_task_id']; write(path,ret)
        self.accept()
        self.assertEqual(self.rt.status()['selected_returns'][self.role]['agent_task_id'],self.task)

    def test_wrong_child_host_id_is_not_overwritten(self):
        self.start(); self.make_return()
        path=self.root/'return.json'
        ret=json.loads(path.read_text(encoding='utf-8')); ret['agent_task_id']='agent-wrong'; write(path,ret)
        with self.assertRaisesRegex(ValueError,'return_binding'):
            self.accept()

    def test_completed_host_bad_return_is_rejected_not_waiting(self):
        self.start(); self.make_return()
        write(self.root/'return.json',{})
        with self.assertRaisesRegex(ValueError,'return_binding'):
            self.accept()
        status=self.rt.status()
        self.assertEqual(status['members'][0]['state'],'member_rejected')
        self.assertEqual(status['waiting'],[])
        self.assertNotIn(self.role,status['selected_returns'])
        write(self.root/'second.json',dict(self.obs,task_id='agent-retry'))
        self.rt.start(self.role,self.host,'agent-retry','a2','second.json')
        self.assertEqual(len(self.rt.status()['waiting']),1)

    def test_rejected_attempt_cannot_be_fixed_in_place(self):
        self.start(); self.make_return()
        write(self.root/'return.json',{})
        with self.assertRaises(ValueError): self.accept()
        self.make_return()
        with self.assertRaisesRegex(ValueError,'terminal_failed'): self.accept()

    def test_two_terminal_failures_exhaust_retry(self):
        self.start()
        write(self.root/'failed.json',dict(self.obs,state='failed'))
        self.rt.fail(*self.args,'failed.json')
        self.rt.start(self.role,self.host,self.task,'a2','started.json')
        self.rt.fail(self.role,self.host,self.task,'a2','failed.json')
        with self.assertRaisesRegex(ValueError,'member_retry_exhausted'):
            self.rt.start(self.role,self.host,self.task,'a3','started.json')

    def test_ambiguous_host_result_is_not_completed(self):
        self.start(); self.make_return()
        write(self.root/'completed.json',dict(self.obs,state='running'))
        with self.assertRaisesRegex(ValueError,'terminal_observation_missing'):
            self.accept()

    def test_sealed_return_is_immutable(self):
        self.start(); self.make_return(); self.accept()
        (self.root/'sealed.json').write_text('{}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'sealed_handoff_changed'):
            self.rt.status()

    def test_accept_retry_is_idempotent(self):
        self.start(); self.make_return(); self.accept()
        self.accept()
        self.assertEqual(self.rt.status()['events'],3)

    def test_returned_member_cannot_start_another_attempt(self):
        self.start(); self.make_return(); self.accept()
        write(self.root/'second.json',dict(self.obs,task_id='agent-another'))
        with self.assertRaisesRegex(ValueError,'member_already_returned'):
            self.rt.start(self.role,self.host,'agent-another','a2','second.json')

    def test_capacity_batches(self):
        batches=batch_roles(3)
        self.assertEqual([len(b) for b in batches],[3,1])
        self.assertEqual(len(set(sum(batches,[]))),4)

    def test_early_reviewer_blocked(self):
        with self.assertRaisesRegex(ValueError,'review_before_analysis_returns'):
            self.rt.start('delivery-review',self.host,self.task,'r1','started.json')

    def test_terminal_failure_allows_new_attempt(self):
        self.start()
        write(self.root/'failed.json',dict(self.obs,state='failed'))
        self.rt.fail(*self.args,'failed.json')
        write(self.root/'second.json',dict(self.obs,task_id='agent-retry'))
        self.rt.start(self.role,self.host,'agent-retry','a2','second.json')
        self.assertEqual(len(self.rt.status()['waiting']),1)

    def test_failed_attempt_cannot_late_return(self):
        self.start(); self.make_return()
        write(self.root/'failed.json',dict(self.obs,state='failed'))
        self.rt.fail(*self.args,'failed.json')
        with self.assertRaisesRegex(ValueError,'terminal_failed'):
            self.accept()


if __name__=='__main__': unittest.main()
