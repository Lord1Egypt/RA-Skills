"""Synthetic monitoring fixtures; no invented historical live baseline."""
import copy
import contextlib
import io
import json
import unittest
from jsonschema import Draft202012Validator
from datetime import datetime,timedelta,timezone
from pathlib import Path
from unittest.mock import patch

from artifact_contract import native_audit_identity
import host_runtime_smoke as runtime_fixture
import behavior_audit
from behavior_audit import telemetry,snapshot,compare,read,record_feedback,record_comparison

POLICY=read(Path(__file__).resolve().parents[1]/'config'/'behavior-monitor.json')
SPLIT='2026-08-15T00:00:00+08:00'


def sample(index,current=False,**overrides):
    date=datetime(2026,8,1,tzinfo=timezone(timedelta(hours=8)))+timedelta(days=14 if current else index//2)
    value=dict(**telemetry({}),run_id='synthetic-run',sample_id=('new-' if current else 'old-')+str(index),
          client_scope='synthetic',team_version='2.0.3',task_class='monthly_report',role='data-analyst',host='codex',
          observed_at=date.isoformat(),terminal_kind='member_returned',human_corrected=None,
          evidence_kind='synthetic_fixture')
    value.update(overrides)
    return value


def history(before=None,after=None):
    return [dict(client_scope='synthetic',samples=(before if before is not None else [sample(i) for i in range(28)])+
                 (after if after is not None else [sample(i,True) for i in range(5)]))]


class ComparisonTests(unittest.TestCase):
    def evaluate(self,before=None,after=None): return compare(history(before,after),'synthetic',POLICY,SPLIT)

    def test_unknown_model_and_cost_remain_null(self):
        data=telemetry({})
        self.assertIsNone(data['cost']); self.assertIsNone(data['model_name'])
        self.assertEqual(data['telemetry_state'],'unavailable')

    def test_explicit_zero_is_preserved(self):
        value=telemetry(dict(model=dict(cost=0,currency='CNY',latency_ms=0,input_tokens=0)))
        self.assertEqual(value['cost'],0); self.assertEqual(value['latency_ms'],0)

    def test_invalid_measurements_are_not_recorded_as_fact(self):
        value=telemetry(dict(model=dict(cost=5,latency_ms=float('nan'),input_tokens=True)))
        self.assertIsNone(value['cost']); self.assertIsNone(value['latency_ms']); self.assertIsNone(value['input_tokens'])
        self.assertIn('cost_currency_missing',value['limitations'])

    def test_no_feedback_is_unknown_not_zero(self):
        cohort=self.evaluate()['cohorts'][0]
        self.assertIsNone(cohort['baseline']['human_correction_rate']['value'])
        self.assertIn('human_correction_rate',cohort['unavailable_metrics'])

    def test_one_day_cannot_fake_two_week_baseline(self):
        before=[sample(i,observed_at='2026-08-01T01:00:00+08:00') for i in range(100)]
        self.assertEqual(self.evaluate(before)['cohorts'][0]['status'],'baseline_collecting')

    def test_rejection_spike_requests_review(self):
        after=[sample(i,True,terminal_kind='member_rejected') for i in range(5)]
        result=self.evaluate(after=after)
        self.assertEqual(result['cohorts'][0]['status'],'review_required')
        self.assertEqual(result['cohorts'][0]['signals'][0]['metric'],'handoff_rejection_rate')
        self.assertFalse(result['automatic_changes'])
        self.assertEqual(result['evidence_kinds'],['synthetic_fixture'])

    def test_insufficient_metric_coverage_does_not_claim_stability(self):
        before=[sample(i,human_corrected=False if i==0 else None) for i in range(28)]
        after=[sample(i,True,human_corrected=True) for i in range(5)]
        group=self.evaluate(before,after)['cohorts'][0]
        self.assertIn('human_correction_rate',group['unavailable_metrics'])
        self.assertNotIn('human_correction_rate',[s['metric'] for s in group['signals']])

    def test_currency_mismatch_not_compared(self):
        before=[sample(i,cost=1,currency='USD') for i in range(28)]
        after=[sample(i,True,cost=20,currency='CNY') for i in range(5)]
        group=self.evaluate(before,after)['cohorts'][0]
        self.assertIn('cost',group['unavailable_metrics'])
        self.assertFalse(group['signals'])

    def test_weekly_and_diagnosis_are_separate(self):
        after=[sample(i,True,task_class='store_diagnosis',terminal_kind='member_rejected') for i in range(5)]
        groups=self.evaluate(after=after)['cohorts']
        self.assertEqual(len(groups),2)
        self.assertTrue(all(g['status']=='baseline_collecting' for g in groups))

    def test_cross_client_rejected(self):
        with self.assertRaisesRegex(ValueError,'scope_mismatch'):
            self.evaluate(after=[sample(0,True,client_scope='other')])

    def test_duplicate_sample_rejected(self):
        with self.assertRaisesRegex(ValueError,'duplicate_sample'):
            self.evaluate(after=[sample(0),sample(0)])

    def test_timezone_required(self):
        with self.assertRaisesRegex(ValueError,'timestamp_invalid'):
            self.evaluate(after=[sample(0,True,observed_at='2026-08-15')])

    def test_nan_cannot_enter_comparison(self):
        with self.assertRaisesRegex(ValueError,'measurement_invalid'):
            self.evaluate(after=[sample(0,True,cost=float('nan'),currency='USD')])

    def test_disagreement_rate_from_scans(self):
        before=[sample(i,role='analysis-cohort',terminal_kind='quality_scan',has_conflict=False) for i in range(28)]
        after=[sample(i,True,role='analysis-cohort',terminal_kind='quality_scan',has_conflict=True) for i in range(5)]
        group=self.evaluate(before,after)['cohorts'][0]
        self.assertIsNone(group['baseline']['host_failure_rate']['value'])
        self.assertEqual([s['metric'] for s in group['signals']],['disagreement_rate'])

    def test_synthetic_and_live_observations_never_share_baseline(self):
        after=[sample(i,True,evidence_kind='native_host_observation',terminal_kind='member_rejected') for i in range(5)]
        groups=self.evaluate(after=after)['cohorts']
        self.assertEqual(len(groups),2)
        self.assertTrue(all(g['status']=='baseline_collecting' for g in groups))

    def test_old_data_is_not_silently_used_as_current_baseline(self):
        before=[sample(i,observed_at='2020-01-01T00:00:00+08:00') for i in range(28)]
        result=self.evaluate(before)
        self.assertEqual(result['samples_outside_windows'],28)
        self.assertEqual(result['cohorts'][0]['status'],'baseline_collecting')

    def test_structure_error_rate_uses_only_checked_contracts(self):
        before=[sample(i,structure_valid=True) for i in range(28)]
        after=[sample(i,True,structure_valid=False) for i in range(5)]
        group=self.evaluate(before,after)['cohorts'][0]
        self.assertEqual(group['current']['structure_error_rate']['denominator'],5)
        self.assertEqual([s['metric'] for s in group['signals']],['structure_error_rate'])

    def test_comparison_schema(self):
        schema=read(Path(__file__).resolve().parents[1]/'schemas'/'behavior-audit.schema.json')
        errors=list(Draft202012Validator(schema).iter_errors(self.evaluate()))
        self.assertEqual(errors,[])


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.fixture=runtime_fixture.RuntimeTests(); self.fixture.setUp()
        self.rt=self.fixture.rt; self.root=self.fixture.root

    def tearDown(self): self.fixture.tearDown()

    def get(self): return snapshot(self.root,'runtime-test','test-client')

    def test_inflight_task_has_no_completed_measurement(self):
        self.fixture.start()
        self.assertEqual(self.get()['samples'],[])

    def test_accepted_return_automatically_records_model_observation(self):
        self.fixture.start(); self.fixture.make_return(); self.fixture.accept()
        samples=self.get()['samples']; self.assertEqual(len(samples),1)
        self.assertIsNone(samples[0]['cost'])
        events=self.rt.journal.events('runtime-test','test-client')
        self.assertEqual(len([r for r in events if r['kind']=='model_observation']),1)
        schemas=Path(__file__).resolve().parents[1]/'schemas'
        model=next(r['payload'] for r in events if r['kind']=='model_observation')
        self.assertEqual(list(Draft202012Validator(read(schemas/'model-route.schema.json')).iter_errors(model)),[])
        self.assertEqual(list(Draft202012Validator(read(schemas/'behavior-audit.schema.json')).iter_errors(self.get())),[])

    def test_actual_exported_metadata_is_retained(self):
        self.fixture.start(); self.fixture.make_return()
        path=self.root/'completed.json'; data=read(path)
        data['model']=dict(model_name='fixture-model',model_version='fixture-v2',latency_ms=123,cost=0,currency='CNY')
        path.write_text(json.dumps(data),encoding='utf-8'); self.fixture.accept()
        item=self.get()['samples'][0]
        self.assertEqual(item['latency_ms'],123); self.assertEqual(item['cost'],0)

    def test_changed_observation_blocks_snapshot(self):
        self.fixture.start(); self.fixture.make_return(); self.fixture.accept()
        (self.root/'completed.json').write_text('{}',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'observation_changed'): self.get()

    def test_explicit_feedback_changes_only_target(self):
        self.fixture.start(); self.fixture.make_return(); self.fixture.accept()
        feedback=dict(run_id='runtime-test',client_scope='test-client',role=self.fixture.role,host=self.fixture.host,
                      agent_task_id=self.fixture.task,attempt_id='a1',outcome='corrected',
                      message_reference='synthetic-fixture-message',observed_at='2026-09-08T09:00:00+08:00')
        path=self.root/'feedback.json'; path.write_text(json.dumps(feedback),encoding='utf-8')
        record_feedback(self.rt,'feedback.json')
        self.assertTrue(self.get()['samples'][0]['human_corrected'])
        self.assertIsNone(self.get()['samples'][0]['cost'])

    def test_policy_revision_cannot_silently_change_thresholds(self):
        policy=copy.deepcopy(POLICY)
        result=compare(history(),'synthetic',policy,SPLIT)
        result['client_scope']='test-client'
        record_comparison(self.rt,policy,result,'comparison-a.json')
        policy['thresholds']['cost']=99
        result['policy_sha256']=__import__('run_journal').digest(policy)
        with self.assertRaisesRegex(ValueError,'policy_revision_reused'):
            record_comparison(self.rt,policy,result,'comparison-b.json')
        self.assertFalse((self.root/'comparison-b.json').exists())

    def test_cli_snapshot_then_comparison_records_audit(self):
        self.fixture.start(); self.fixture.make_return(); self.fixture.accept()
        with patch('sys.argv',['behavior_audit.py','snapshot','--run-dir',str(self.root),'--run-id','runtime-test',
                '--client-scope','test-client','--output',str(self.root/'snapshot.json')]),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(behavior_audit.main(),0)
        self.assertEqual(len(read(self.root/'snapshot.json')['samples']),1)
        manifest=dict(client_scope='test-client',runs=[dict(run_id='runtime-test',run_dir='.')])
        (self.root/'history.json').write_text(json.dumps(manifest),encoding='utf-8')
        now=datetime.now(timezone.utc).isoformat()
        from monitor_policy_store import MonitorPolicyStore,PROFILE
        policy_path=Path(__file__).resolve().parents[1]/'config'/'behavior-monitor.json'
        policy=read(policy_path)
        store=MonitorPolicyStore.create(self.root/'monitor-policy-store',['test-client'])
        store.adopt('test-client',policy,dict(state='adopted',client_scope='test-client',
            policy_sha256=__import__('run_journal').digest(policy),actor='synthetic-test',
            source_reference='synthetic CLI contract test',decided_at=now,previous_policy_sha256=None))
        store.close()
        with patch('sys.argv',['behavior_audit.py','compare','--history',str(self.root/'history.json'),
                '--client-scope','test-client','--policy',str(policy_path),
                '--policy-store-profile',str(self.root/'monitor-policy-store'/PROFILE),
                '--split-at',now,'--audit-run-dir',str(self.root),'--audit-run-id','runtime-test',
                '--output','audits/comparison.json']),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(behavior_audit.main(),0)
        result=read(self.root/'audits'/'comparison.json')
        self.assertEqual(result['cohorts'][0]['status'],'baseline_collecting')
        self.assertTrue(result['policy_registry_reference']['current_authority'])
        events=self.rt.journal.events('runtime-test','test-client')
        self.assertEqual(events[-1]['kind'],'monitor_comparison')
        self.assertEqual('omni-ecom.behavior-monitor-policy',events[-2]['payload']['contract_name'])
        self.assertEqual('omni-ecom.behavior-monitor-comparison',events[-1]['payload']['contract_name'])
        self.assertTrue(all(row['payload']['created_by_team_version']==self.rt.identity()['team_version']
                            for row in events[-2:]))

    def test_legacy_monitor_records_cannot_enter_current_run(self):
        payload=dict(policy_id='legacy',revision='1',sha256='a'*64,previous_sha256=None)
        with self.assertRaisesRegex(ValueError,'audit_identity_invalid'):
            self.rt.journal.append('runtime-test','test-client','legacy-monitor','monitor_policy',payload)

    def test_monitor_record_types_cannot_impersonate_each_other(self):
        policy=copy.deepcopy(POLICY); result=compare(history(),'synthetic',policy,SPLIT)
        result['client_scope']='test-client'
        record_comparison(self.rt,policy,result,'comparison-type.json')
        row=self.rt.journal.events('runtime-test','test-client')[-1]['payload']
        forged=copy.deepcopy(row)
        forged.update(native_audit_identity('monitor_policy',self.rt.identity()['team_version']))
        with self.assertRaisesRegex(ValueError,'audit_identity_invalid'):
            self.rt.journal.append('runtime-test','test-client','forged-monitor-type','monitor_comparison',forged)

    def test_history_cannot_escape_supplied_root(self):
        value=dict(client_scope='test-client',runs=[dict(run_id='runtime-test',run_dir='../outside')])
        path=self.root/'history.json'; path.write_text(json.dumps(value),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'history_path_outside'):
            behavior_audit.load_history(path,'test-client')


if __name__=='__main__': unittest.main()
