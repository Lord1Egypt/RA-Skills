"""Synthetic eligibility tests; no external platform requests or real approvals."""
import copy
import tempfile
import unittest
from pathlib import Path
from datetime import datetime,timezone

from action_policy import evaluate,record
from run_journal import Journal,digest
from artifact_contract import native_operational_identity


class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.now=datetime(2026,9,8,8,0,tzinfo=timezone.utc)
        identity=dict(client_scope='synthetic',platform='mock',account_id='account1',store_id='store1')
        self.action=dict(**native_operational_identity('controlled_action','2.0.3-candidate.1'),**identity,action_id='A001',run_id='synthetic-run',operation='campaign.budget',
            target=dict(resource='campaign',platform_id='campaign1'),changes={'budget':110},idempotency_key='once')
        self.policy=dict(schema_version='2.0',client_scope='synthetic',policy_id='controlled-test',revision='1',mode='controlled',
            object_max_age_seconds=3600,snapshot_max_age_seconds=300,
            operations={'campaign.budget':dict(resource='campaign',fields={'budget':dict(minimum=0,maximum=200,max_increase=20,max_decrease=30)}),
                        'campaign.pause':dict(resource='campaign',fields={'status':dict(allowed_values=['paused'])})})
        self.objects=[dict(**identity,object_type='campaign',platform_id='campaign1',status='active',seen_at='2026-09-08T07:50:00Z')]
        self.credential=dict(**identity,status='active',credential_id='CR001',secret_ref='vault://synthetic-reference',
                             expires_at='2026-09-09T00:00:00Z',scope=['campaign.budget','campaign.pause'])
        self.snapshot=dict(**identity,target=self.action['target'],read_at='2026-09-08T07:59:00Z',data={'budget':100,'status':'active'})
        self.snapshot['source_fingerprint']=digest(self.snapshot['data'])
        waiting=self.check()
        self.assertEqual(waiting['decision'],'requires_approval')
        self.approval=dict(**native_operational_identity('approval','2.0.3-candidate.1'),client_scope='synthetic',run_id='synthetic-run',action_id='A001',
            state='approved',approval_id='AP001',actor='synthetic-test-user',source_reference='synthetic fixture, not real consent',
            decided_at='2026-09-08T07:59:30Z',expires_at='2026-09-08T08:05:00Z',**waiting['bindings'])

    def check(self):
        return evaluate(self.action,self.policy,self.objects,self.credential,self.snapshot,getattr(self,'approval',None),self.now)

    def denied(self,reason):
        result=self.check(); self.assertEqual(result['decision'],'denied',result); self.assertEqual(result['reason'],reason)
        self.assertIs(result['executed'],False)

    def test_matching_approval_is_eligible_not_executed(self):
        result=self.check(); self.assertEqual(result['decision'],'eligible_for_execution'); self.assertFalse(result['executed'])

    def test_missing_approval_stays_pending(self):
        self.approval=None; self.assertEqual(self.check()['decision'],'requires_approval')

    def test_readonly_cannot_execute_even_when_approved(self):
        self.policy['mode']='readonly'; self.denied('policy_readonly')

    def test_assisted_mode_is_never_eligible(self):
        self.policy['mode']='assisted'; self.assertEqual(self.check()['decision'],'assisted_plan_only')

    def test_changed_target_cannot_reuse_approval(self):
        self.action['target']={'resource':'campaign','platform_id':'other'}; self.denied('policy_target_unknown_or_ambiguous')

    def test_duplicate_target_is_ambiguous(self):
        self.objects.append(copy.deepcopy(self.objects[0])); self.denied('policy_target_unknown_or_ambiguous')

    def test_disabled_object_is_not_executable(self):
        self.objects[0]['status']='disabled'; self.denied('policy_target_unknown_or_ambiguous')

    def test_other_account_credential_is_rejected(self):
        self.credential['account_id']='another'; self.denied('policy_credential_scope_mismatch')

    def test_expired_credential_is_rejected(self):
        self.credential['expires_at']='2026-09-08T07:00:00Z'; self.denied('policy_credential_expired')

    def test_write_scope_required(self):
        self.credential['scope']=['campaign.get']; self.denied('policy_credential_operation_denied')

    def test_snapshot_fingerprint_cannot_be_false(self):
        self.snapshot['data']['budget']=99; self.denied('policy_snapshot_fingerprint_invalid')

    def test_stale_snapshot_requires_fresh_read(self):
        self.snapshot['read_at']='2026-09-08T07:00:00Z'; self.denied('policy_snapshot_stale')

    def test_budget_increment_cap_applies_even_below_absolute_cap(self):
        self.action['changes']['budget']=150; self.denied('policy_numeric_limit_exceeded')

    def test_budget_decrement_cap(self):
        self.action['changes']['budget']=60; self.denied('policy_numeric_limit_exceeded')

    def test_unknown_field_cannot_be_smuggled_with_budget(self):
        self.action['changes']['publish']=True; self.denied('policy_field_denied')

    def test_action_change_requires_new_approval(self):
        self.action['changes']['budget']=115; self.denied('policy_approval_binding_changed')

    def test_policy_change_requires_new_approval(self):
        self.policy['revision']='2'; self.denied('policy_approval_binding_changed')

    def test_rejected_approval_cannot_be_used(self):
        self.approval['state']='rejected'; self.denied('policy_approval_not_granted')

    def test_expired_approval_cannot_be_used(self):
        self.approval['expires_at']='2026-09-08T07:59:59Z'; self.denied('policy_approval_expired_or_future')

    def test_approval_requires_locatable_user_reference(self):
        self.approval['source_reference']=''; self.denied('policy_approval_provenance_missing')

    def test_nan_string_cannot_pass_numeric_limit(self):
        self.action['changes']['budget']='NaN'; self.denied('policy_number_invalid')

    def test_plaintext_credential_field_is_not_echoed(self):
        self.credential['access_token']='never-echo-test-value'; result=self.check()
        self.assertEqual(result['decision'],'denied'); self.assertNotIn('never-echo',str(result))

    def test_record_preserves_scoped_audit_without_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            journal=Journal(Path(tmp)/'run.sqlite')
            try:
                journal.create('synthetic-run','synthetic','2.0.3-candidate.1','single_topic')
                result=self.check(); fingerprint=record(journal,'synthetic-run','synthetic',self.action,result)
                self.assertEqual(record(journal,'synthetic-run','synthetic',self.action,result),fingerprint)
                rows=journal.events('synthetic-run','synthetic'); self.assertEqual(len(rows),1)
                self.assertFalse(rows[0]['payload']['executed']); self.assertNotIn('secret_ref',rows[0]['body'])
                self.assertEqual('omni-ecom.action-policy-decision',rows[0]['payload']['contract_name'])
                self.assertEqual('2.0.3-candidate.1',rows[0]['payload']['created_by_team_version'])
            finally: journal.close()

    def test_legacy_policy_decision_cannot_enter_current_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            journal=Journal(Path(tmp)/'run.sqlite')
            try:
                journal.create('synthetic-run','synthetic','2.0.3-candidate.1','single_topic')
                payload=dict(action_id='A001',request_sha256=digest(self.action),decision='eligible_for_execution',
                             reason='forged legacy result',bindings=self.check()['bindings'],executed=False,
                             approval_id='AP001',evaluated_at=self.now.isoformat())
                with self.assertRaisesRegex(ValueError,'operational_identity_invalid'):
                    journal.append('synthetic-run','synthetic','legacy-policy','action_policy_decision',payload)
            finally: journal.close()

    def test_v1_action_cannot_enter_current_policy(self):
        self.action['schema_version']='1.0'
        self.denied('policy_schema_unsupported')

    def test_action_legacy_boundary_cannot_grant_execution(self):
        self.action['legacy_compatibility']['current_execution_authority']=True
        self.denied('policy_input_invalid')

    def test_approval_must_match_action_team_version(self):
        self.approval['created_by_team_version']='2.0.3'
        self.denied('policy_input_invalid')

    def test_action_and_approval_contracts_are_distinct(self):
        self.approval['artifact_type']='controlled_action_request'
        self.denied('policy_input_invalid')


if __name__=='__main__': unittest.main()
