"""Synthetic cross-run monitor policy governance and legacy isolation tests."""
import copy
import json
import sqlite3
import tempfile
import unittest
from datetime import datetime,timezone,timedelta
from pathlib import Path

from monitor_policy_store import MonitorPolicyStore,PROFILE,DATABASE
from run_journal import digest


ROOT=Path(__file__).resolve().parents[1]


class MonitorPolicyStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.policy=json.loads((ROOT/'config'/'behavior-monitor.json').read_text(encoding='utf-8'))
        self.store=MonitorPolicyStore.create(self.root/'store',['client-a','client-b'])
        self.addCleanup(lambda: self.store.close())

    def decision(self,policy=None,previous=None):
        policy=policy or self.policy
        return dict(state='adopted',client_scope='client-a',policy_sha256=digest(policy),
                    actor='synthetic-test',source_reference='synthetic approval reference',
                    decided_at=datetime.now(timezone.utc).isoformat(),previous_policy_sha256=previous)

    def test_adopted_policy_survives_restart_and_is_current(self):
        ref=self.store.adopt('client-a',self.policy,self.decision())
        self.assertTrue(ref['current_authority']); self.assertEqual('native_v2',ref['source_kind'])
        from jsonschema import Draft202012Validator
        schema=json.loads((ROOT/'schemas'/'monitor-policy-reference.schema.json').read_text(encoding='utf-8'))
        self.assertEqual([],list(Draft202012Validator(schema).iter_errors(ref)))
        self.store.close(); self.store=MonitorPolicyStore.open(self.root/'store'/PROFILE)
        policy,current=self.store.current('client-a',self.policy['policy_id'])
        self.assertEqual(self.policy,policy); self.assertEqual(ref,current)

    def test_revision_chain_cannot_skip_or_rewrite_history(self):
        first=self.store.adopt('client-a',self.policy,self.decision())
        second=copy.deepcopy(self.policy); second['revision']='candidate-2'; second['thresholds']['cost']=2.0
        with self.assertRaisesRegex(ValueError,'previous_revision_mismatch'):
            self.store.adopt('client-a',second,self.decision(second))
        ref=self.store.adopt('client-a',second,self.decision(second,first['policy_sha256']))
        self.assertEqual(first['policy_sha256'],self.store.db.execute(
            'SELECT previous_sha256 FROM policies WHERE revision=?',('candidate-2',)).fetchone()[0])
        self.assertEqual(ref,self.store.reference('client-a',second['policy_id'],'candidate-2'))
        with self.assertRaisesRegex(ValueError,'revision_already_exists'):
            self.store.adopt('client-a',second,self.decision(second,ref['policy_sha256']))

    def test_legacy_policy_is_exact_history_and_never_current(self):
        legacy=dict(schema_version='1.0',policy_id='old-monitor',revision='1',thresholds={'error':0.2})
        source=self.root/'legacy.json'; raw=(json.dumps(legacy,ensure_ascii=False)+'\n').encode('utf-8'); source.write_bytes(raw)
        ref=self.store.import_legacy('client-a',source)
        self.assertFalse(ref['current_authority']); self.assertEqual('legacy_v1',ref['source_kind'])
        source.write_text('{}',encoding='utf-8')
        self.assertEqual(ref,self.store.verify_legacy('client-a','old-monitor','1'))
        with self.assertRaisesRegex(ValueError,'current_missing'): self.store.current('client-a','old-monitor')

    def test_cross_client_access_is_denied(self):
        ref=self.store.adopt('client-a',self.policy,self.decision())
        with self.assertRaisesRegex(ValueError,'not_found'):
            self.store.reference('client-b',ref['policy_id'],ref['revision'])
        with self.assertRaisesRegex(ValueError,'client_scope_denied'):
            self.store.reference('client-x',ref['policy_id'],ref['revision'])

    def test_profile_or_database_substitution_is_detected(self):
        profile=self.root/'store'/PROFILE; value=json.loads(profile.read_text(encoding='utf-8'))
        value['client_scopes'].append('attacker'); profile.write_text(json.dumps(value),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'profile_changed'): self.store.current('client-a',self.policy['policy_id'])

    def test_rows_and_identity_are_append_only(self):
        self.store.adopt('client-a',self.policy,self.decision())
        with self.assertRaises(sqlite3.Error): self.store.db.execute('DELETE FROM policies')
        with self.assertRaises(sqlite3.Error): self.store.db.execute("UPDATE policies SET revision='x'")
        with self.assertRaises(sqlite3.Error): self.store.db.execute('DELETE FROM identity')

    def test_automatic_override_or_unbound_decision_is_rejected(self):
        unsafe=copy.deepcopy(self.policy); unsafe['automatic_model_override']=True
        with self.assertRaisesRegex(ValueError,'automatic_override_forbidden'):
            self.store.adopt('client-a',unsafe,self.decision(unsafe))
        wrong=self.decision(); wrong['policy_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'adoption_invalid'):
            self.store.adopt('client-a',self.policy,wrong)
        future=self.decision(); future['decided_at']=(datetime.now(timezone.utc)+timedelta(days=1)).isoformat()
        with self.assertRaisesRegex(ValueError,'decision_in_future'):
            self.store.adopt('client-a',self.policy,future)

    def test_assert_current_rejects_old_reference(self):
        first=self.store.adopt('client-a',self.policy,self.decision())
        second=copy.deepcopy(self.policy); second['revision']='candidate-2'
        second_ref=self.store.adopt('client-a',second,self.decision(second,first['policy_sha256']))
        self.assertEqual(second_ref,self.store.assert_current('client-a',second,second_ref))
        with self.assertRaisesRegex(ValueError,'not_current'):
            self.store.assert_current('client-a',self.policy,first)


if __name__=='__main__': unittest.main()
