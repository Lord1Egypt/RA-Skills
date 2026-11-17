"""Synthetic gateway fault injection, never external actions or real approval."""
import copy
import sys
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path
from threading import Thread, Event

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors import MockPlatformConnector
from action_gateway import ActionGateway
from action_policy import evaluate
from run_journal import Journal, digest
from artifact_contract import native_operational_identity


class CountingConnector(MockPlatformConnector):
    def __init__(self):
        super().__init__()
        self.calls = 0
        self.reads = 0
        self.failure = None
        self.before_call = None

    def read(self, *args):
        self.reads += 1
        return super().read(*args)

    def execute(self, *args, **kwargs):
        self.calls += 1
        if self.before_call:
            self.before_call()
        if self.failure == 'crash_before':
            raise SystemExit('synthetic process interruption')
        result = super().execute(*args, **kwargs)
        if self.failure == 'timeout_after':
            raise TimeoutError('synthetic timeout, token should not appear in log')
        if self.failure == 'crash_after':
            raise SystemExit('synthetic process interruption after mutation')
        if self.failure == 'wrong_response':
            result['request_hash'] = '0' * 64
        if self.failure == 'readback_mismatch':
            self._state['campaign']['cmp-001']['status'] = 'paused'
        if self.failure == 'secret_response':
            result['access_token'] = 'synthetic-sensitive-value'
        return result


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db_path = Path(self.temp.name) / 'journal.sqlite'
        self.journal = Journal(self.db_path)
        self.addCleanup(lambda: self.journal.close())
        self.journal.create('run1', 'synthetic', '2.0.3-candidate.1', 'platform-action-test')
        self.connector = CountingConnector()
        self.now = datetime.now(timezone.utc)
        identity = dict(client_scope='synthetic', platform='mock', account_id='acct1', store_id='store1')
        self.binding = dict(**identity, connector_id='mock-platform')
        self.action = dict(**native_operational_identity('controlled_action','2.0.3-candidate.1'), **identity, run_id='run1', action_id='a1',
                           operation='campaign.resume', target=dict(resource='campaign', platform_id='cmp-001'),
                           changes={'status': 'active'}, idempotency_key='once')
        self.policy = dict(schema_version='2.0', client_scope='synthetic', policy_id='synthetic-policy',
                           revision='1', mode='controlled', object_max_age_seconds=3600,
                           snapshot_max_age_seconds=300, operations={'campaign.resume': dict(resource='campaign',
                           fields={'status': dict(allowed_values=['active'])})})
        self.objects = [dict(**identity, object_type='campaign', platform_id='cmp-001', status='active',
                             seen_at=self.now.isoformat())]
        self.credential = dict(**identity, credential_id='cred1', secret_ref='vault://synthetic-ref',
                               status='active', scope=['campaign.get', 'campaign.resume'],
                               expires_at=(self.now + timedelta(hours=1)).isoformat())
        self.snapshot = dict(**identity, target=self.action['target'], data={'budget': 1000, 'status': 'paused'},
                             read_at=self.now.isoformat())
        self.snapshot['source_fingerprint'] = digest(self.snapshot['data'])
        bindings = evaluate(self.action, self.policy, self.objects, self.credential, self.snapshot)['bindings']
        self.approval = dict(**native_operational_identity('approval','2.0.3-candidate.1'), client_scope='synthetic', run_id='run1', action_id='a1',
                             approval_id='ap1', state='approved', actor='synthetic-test-user',
                             source_reference='synthetic test only, not real consent',
                             decided_at=self.now.isoformat(), expires_at=(self.now + timedelta(minutes=5)).isoformat(),
                             **bindings)
        self.gateway = self.make_gateway()

    def make_gateway(self, journal=None, **options):
        defaults = dict(approval_verifier=lambda approval, action: approval == self.approval,
                        execution_enabled=True)
        defaults.update(options)
        return ActionGateway(journal or self.journal, self.connector, self.binding, **defaults)

    def execute(self, gateway=None):
        return (gateway or self.gateway).execute(self.action, self.policy, self.objects,
                                                 self.credential, self.snapshot, self.approval)

    def restart(self):
        self.journal.close()
        self.journal = Journal(self.db_path)
        self.gateway = self.make_gateway()

    def test_action_team_version_must_match_run(self):
        self.action['created_by_team_version']='2.0.3'
        with self.assertRaisesRegex(ValueError,'gateway_action_team_version_mismatch'):
            self.execute()

    def test_success_requires_return_and_readback_audit(self):
        result = self.execute()
        self.assertEqual('verified', result['outcome'])
        self.assertTrue(result['simulated'])
        self.assertEqual(1, self.connector.calls)
        self.assertEqual(2, self.connector.reads)
        rows = self.journal.events('run1', 'synthetic')
        self.assertEqual(['action_policy_decision', 'action_call_reserved', 'action_call_returned',
                          'action_call_readback', 'action_call_outcome'], [r['kind'] for r in rows])
        self.assertEqual(result['connector_call_id'], rows[1]['payload']['connector_call_id'])
        self.assertEqual(result['readback_id'], rows[-2]['payload']['readback_id'])
        expected = ('connector_call','connector_call','readback','outcome')
        for row, contract_kind in zip(rows[1:], expected):
            self.assertEqual('2.0.3-candidate.1', row['payload']['created_by_team_version'])
            self.assertEqual(native_operational_identity(contract_kind, '2.0.3-candidate.1')['contract_name'],
                             row['payload']['contract_name'])

    def test_legacy_or_wrong_version_execution_records_are_rejected(self):
        self.execute()
        rows = self.journal.events('run1', 'synthetic')
        legacy = copy.deepcopy(rows[1]['payload'])
        for key in ('schema_version','artifact_type','contract_name','contract_version',
                    'created_by_team_version','legacy_compatibility'):
            legacy.pop(key)
        with self.assertRaisesRegex(ValueError, 'operational_identity_invalid'):
            self.journal.append('run1', 'synthetic', 'legacy-call', 'action_call_returned', legacy)
        wrong = copy.deepcopy(rows[-1]['payload'])
        wrong['created_by_team_version'] = '2.0.3'
        with self.assertRaisesRegex(ValueError, 'operational_team_version_mismatch'):
            self.journal.append('run1', 'synthetic', 'wrong-version-outcome', 'action_call_outcome', wrong)

    def test_execution_record_types_cannot_impersonate_each_other(self):
        self.execute()
        readback = copy.deepcopy(self.journal.events('run1', 'synthetic')[-2]['payload'])
        readback.update(native_operational_identity('outcome', '2.0.3-candidate.1'))
        readback['readback_id'] = 'forged-type'
        with self.assertRaisesRegex(ValueError, 'operational_identity_invalid'):
            self.journal.append('run1', 'synthetic', 'forged-type', 'action_call_readback', readback)

    def test_restart_replays_without_new_read_or_write(self):
        result = self.execute()
        self.restart()
        self.assertEqual(result, self.execute())
        self.assertEqual((1, 2), (self.connector.calls, self.connector.reads))

    def test_timeout_after_mutation_never_becomes_success_or_retries(self):
        self.connector.failure = 'timeout_after'
        result = self.execute()
        self.assertEqual('blocked', result['outcome'])
        self.assertEqual('execution_uncertain', result['reason'])
        self.assertEqual('active', self.connector._state['campaign']['cmp-001']['status'])
        self.restart()
        self.assertEqual(result, self.execute())
        self.assertEqual('blocked', self.gateway.reconcile(self.action, self.credential)['outcome'])
        self.assertEqual(1, self.connector.calls)

    def test_process_interruption_before_and_after_call_never_resubmits(self):
        for failure in ('crash_before', 'crash_after'):
            with self.subTest(failure=failure):
                self.action['idempotency_key'] = failure
                self.action['action_id'] = failure
                self.approval['action_id'] = failure
                self.approval.update(evaluate(self.action, self.policy, self.objects, self.credential,
                                              self.snapshot)['bindings'])
                self.connector.failure = failure
                before = self.connector.calls
                with self.assertRaises(SystemExit):
                    self.execute()
                self.restart()
                self.assertEqual('blocked', self.execute()['outcome'])
                self.assertEqual('blocked', self.gateway.reconcile(self.action, self.credential)['outcome'])
                self.assertEqual(before + 1, self.connector.calls)

    def test_missing_trusted_confirmation_prevents_call(self):
        with self.assertRaisesRegex(ValueError, 'trusted_approval'):
            self.execute(self.make_gateway(approval_verifier=None))
        self.assertEqual(0, self.connector.calls)

    def test_default_gateway_cannot_execute(self):
        with self.assertRaisesRegex(ValueError, 'execution_not_enabled'):
            self.execute(ActionGateway(self.journal, self.connector, self.binding))
        self.assertEqual(0, self.connector.calls)

    def test_readonly_or_missing_approval_does_not_read_or_write(self):
        self.policy['mode'] = 'readonly'
        self.assertEqual('blocked', self.execute()['outcome'])
        self.policy['mode'] = 'controlled'
        self.approval = None
        self.assertEqual('blocked', self.execute()['outcome'])
        self.assertEqual((0, 0), (self.connector.calls, self.connector.reads))

    def test_changed_approved_state_prevents_call(self):
        self.connector._state['campaign']['cmp-001']['budget'] = 2000
        with self.assertRaisesRegex(ValueError, 'approved_state_changed'):
            self.execute()
        self.assertEqual(0, self.connector.calls)

    def test_change_between_read_and_write_fails_conditional_write(self):
        self.connector.before_call = lambda: self.connector._state['campaign']['cmp-001'].update(budget=2000)
        self.assertEqual('blocked', self.execute()['outcome'])
        self.assertEqual('paused', self.connector._state['campaign']['cmp-001']['status'])

    def test_response_and_readback_failures_cannot_verify(self):
        for failure in ('wrong_response', 'readback_mismatch', 'secret_response'):
            with self.subTest(failure=failure):
                self.connector._state['campaign']['cmp-001']['status'] = 'paused'
                self.action['idempotency_key'] = failure
                self.action['action_id'] = failure
                self.approval['action_id'] = failure
                self.approval['request_sha256'] = digest(self.action)
                self.connector.failure = failure
                self.assertEqual('blocked', self.execute()['outcome'])
        encoded = str(self.journal.events('run1', 'synthetic'))
        self.assertNotIn('synthetic-sensitive-value', encoded)
        self.assertNotIn('vault://', encoded)

    def test_reserved_key_cannot_move_to_new_run(self):
        self.execute()
        self.journal.create('run2', 'synthetic', '2.0.3-candidate.1', 'platform-action-test')
        self.action['run_id'] = 'run2'
        with self.assertRaisesRegex(ValueError, 'another_run'):
            self.execute()
        self.assertEqual(1, self.connector.calls)

    def test_changed_request_cannot_replay_reserved_key(self):
        self.execute()
        self.action['changes']['status'] = 'paused'
        with self.assertRaisesRegex(ValueError, 'key_request_changed'):
            self.execute()
        self.assertEqual(1, self.connector.calls)

    def test_same_action_cannot_bypass_reservation_by_changing_key(self):
        self.connector.failure = 'timeout_after'
        self.execute()
        self.action['idempotency_key'] = 'new-key'
        with self.assertRaisesRegex(ValueError, 'action_key_changed'):
            self.execute()
        self.assertEqual(1, self.connector.calls)

    def test_crash_after_ack_recovers_by_read_only(self):
        original = self.gateway.reconcile
        def crash(*args):
            raise SystemExit('synthetic interruption before readback')
        self.gateway.reconcile = crash
        with self.assertRaises(SystemExit):
            self.execute()
        self.gateway.reconcile = original
        self.restart()
        self.assertEqual('blocked', self.execute()['outcome'])
        self.assertEqual('verified', self.gateway.reconcile(self.action, self.credential)['outcome'])
        self.assertEqual(1, self.connector.calls)

    def test_expired_read_permission_does_not_query_uncertain_call(self):
        self.connector.failure = 'timeout_after'
        self.execute()
        reads = self.connector.reads
        self.credential['expires_at'] = (self.now - timedelta(seconds=1)).isoformat()
        self.assertEqual('blocked', self.gateway.reconcile(self.action, self.credential)['outcome'])
        self.assertEqual(reads, self.connector.reads)

    def test_approval_expiring_after_reservation_prevents_mutation(self):
        def clock_after_reservation():
            reserved = any(r['kind'] == 'action_call_reserved' for r in self.journal.events('run1', 'synthetic'))
            return self.now + (timedelta(minutes=6) if reserved else timedelta(seconds=1))
        gateway = self.make_gateway(clock=clock_after_reservation)
        result = self.execute(gateway)
        self.assertEqual('blocked', result['outcome'])
        self.assertEqual(0, self.connector.calls)

    def test_forged_verified_outcome_without_call_return_is_rejected(self):
        self.connector.failure = 'timeout_after'
        result = self.execute()
        result['outcome'] = 'verified'
        with self.assertRaisesRegex(ValueError, 'outcome_not_verified'):
            self.journal.append('run1', 'synthetic', 'forged-verified', 'action_call_outcome', result)

    def test_error_during_readback_can_be_retried_without_write(self):
        read = self.connector.read
        def fail_after_preflight(*args):
            if self.connector.calls:
                raise OSError('synthetic read failure')
            return read(*args)
        self.connector.read = fail_after_preflight
        self.assertEqual('blocked', self.execute()['outcome'])
        self.connector.read = read
        self.restart()
        self.assertEqual('verified', self.gateway.reconcile(self.action, self.credential)['outcome'])
        self.assertEqual(1, self.connector.calls)

    def test_wrong_scope_and_expired_read_permission_cannot_read(self):
        self.binding['store_id'] = 'another'
        with self.assertRaisesRegex(ValueError, 'scope_mismatch'):
            self.execute(self.make_gateway())
        self.binding['store_id'] = 'store1'
        self.execute()
        self.credential['expires_at'] = (self.now - timedelta(seconds=1)).isoformat()
        # A verified receipt is historical and does not issue a read at all.
        self.assertEqual('verified', self.gateway.reconcile(self.action, self.credential)['outcome'])
        self.assertEqual(2, self.connector.reads)

    def test_concurrent_workers_do_not_submit_reserved_call(self):
        entered, release = Event(), Event()
        self.connector.before_call = lambda: (entered.set(), release.wait(5))
        outputs, errors = [], []
        def worker():
            journal = Journal(self.db_path)
            try:
                outputs.append(self.execute(self.make_gateway(journal)))
            except BaseException as exc:
                errors.append(exc)
            finally:
                journal.close()
        thread = Thread(target=worker)
        thread.start()
        try:
            self.assertTrue(entered.wait(5))
            result = self.execute()
            self.assertEqual('blocked', result['outcome'])
        finally:
            release.set()
            thread.join(10)
        self.assertFalse(thread.is_alive())
        self.assertEqual([], errors)
        self.assertEqual('verified', outputs[0]['outcome'])
        self.assertEqual(1, self.connector.calls)


if __name__ == '__main__':
    unittest.main()
