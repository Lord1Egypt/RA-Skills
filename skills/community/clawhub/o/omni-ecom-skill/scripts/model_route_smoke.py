"""Synthetic model-route assessment tests; never changes a host model."""
import copy
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from jsonschema import Draft202012Validator
from model_route_guard import assess
from run_journal import digest
from artifact_contract import validate_audit_identity


ROOT=Path(__file__).resolve().parents[1]


def metric(value,n): return dict(value=value,numerator=0,denominator=n)


class ModelRouteTests(unittest.TestCase):
    def setUp(self):
        self.policy=json.loads((ROOT/'config'/'behavior-monitor.json').read_text(encoding='utf-8'))
        self.request=dict(request_id='route-1',client_scope='synthetic',team_version='2.0.3-candidate.1',
                          task_class='weekly_report',role='data-analyst',host='codex',
                          current_model_alias='current',candidate_model_alias='candidate',
                          requested_by='synthetic-test',reason='contract exercise only')
        self.comparison=dict(schema_version='2.0',status='behavior_comparison',client_scope='synthetic',
                             threshold_status='validated_live',policy_sha256='',cohorts=[])
        for alias in ('current','candidate'):
            base=dict(samples=30,structure_error_rate=metric(0.05,30),handoff_rejection_rate=metric(0.03,30),
                      host_failure_rate=metric(0.01,30),human_correction_rate=metric(None,0),
                      disagreement_rate=metric(None,0),latency_ms=dict(value=1000,denominator=30),
                      cost=dict(value=None,denominator=0,currencies=[]),model_variants=['fixture@1'])
            current=copy.deepcopy(base); current['samples']=6
            for name in ('structure_error_rate','handoff_rejection_rate','host_failure_rate','latency_ms'):
                current[name]['denominator']=6
            self.comparison['cohorts'].append(dict(cohort=dict(task_class='weekly_report',role='data-analyst',
                host='codex',model_alias=alias,evidence_kind='native_codex_runtime_observation'),
                status='no_drift_in_observed_metrics',baseline_days=14,baseline=base,current=current,
                signals=[],unavailable_metrics=['human_correction_rate','disagreement_rate','cost'],
                model_configuration_changed=False))

    def run_assess(self):
        self.comparison['policy_sha256']=digest(self.policy)
        self.comparison['policy_registry_reference']=dict(client_scope='synthetic',policy_id=self.policy['policy_id'],
            revision=self.policy['revision'],policy_sha256=digest(self.policy),source_kind='native_v2',
            current_authority=True,legacy_permissions_inherited=False)
        return assess(self.comparison,self.policy,self.request,
                      comparison_sha256='a'*64,policy_sha256=digest(self.policy))

    def test_current_provisional_policy_cannot_claim_live_calibration(self):
        self.comparison['threshold_status']=self.policy['threshold_status']
        result=self.run_assess()
        self.assertEqual('live_baseline_not_ready',result['status'])
        self.assertIn('live_thresholds_not_validated',result['reasons'])
        self.assertFalse(result['route_selection_applied'])

    def test_two_eligible_stable_live_cohorts_enable_manual_review_only(self):
        self.policy['threshold_status']='validated_live'
        result=self.run_assess()
        self.assertEqual('manual_route_review_ready',result['status'])
        self.assertTrue(result['calibration_ready'])
        self.assertFalse(result['host_model_changed'])
        self.assertTrue(result['explicit_user_or_admin_approval_required'])
        self.assertFalse(result['formal_acceptance_completed'])
        self.assertEqual('2.0.3-candidate.1',validate_audit_identity(
            result,'model_route_assessment','2.0.3-candidate.1'))
        schema=json.loads((ROOT/'schemas'/'model-route-assessment.schema.json').read_text(encoding='utf-8'))
        self.assertEqual([],list(Draft202012Validator(schema).iter_errors(result)))

    def test_synthetic_evidence_never_enters_live_calibration(self):
        self.policy['threshold_status']='validated_live'
        self.comparison['cohorts'][0]['cohort']['evidence_kind']='synthetic_fixture'
        result=self.run_assess()
        self.assertIn('current:non_live_evidence_kind',result['reasons'])
        self.assertFalse(result['calibration_ready'])

    def test_missing_candidate_or_required_metric_blocks(self):
        self.policy['threshold_status']='validated_live'
        self.comparison['cohorts'].pop()
        self.assertIn('both_model_cohorts_required',self.run_assess()['reasons'])
        self.setUp(); self.policy['threshold_status']='validated_live'
        self.comparison['cohorts'][1]['current']['host_failure_rate']['value']=None
        self.assertIn('candidate:metric_unavailable:host_failure_rate',self.run_assess()['reasons'])

    def test_policy_can_never_enable_automatic_override(self):
        self.policy['automatic_model_override']=True
        with self.assertRaisesRegex(ValueError,'automatic_override_forbidden'): self.run_assess()
        self.policy['automatic_model_override']=False
        self.policy['live_calibration']['automatic_model_override']=True
        with self.assertRaisesRegex(ValueError,'automatic_override_forbidden'): self.run_assess()

    def test_scope_and_policy_hash_are_bound(self):
        self.comparison['client_scope']='other'
        with self.assertRaisesRegex(ValueError,'client_scope_mismatch'): self.run_assess()
        self.comparison['client_scope']='synthetic'; self.comparison['policy_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'policy_binding_invalid'):
            assess(self.comparison,self.policy,self.request,comparison_sha256='a'*64,policy_sha256=digest(self.policy))


if __name__=='__main__': unittest.main()
