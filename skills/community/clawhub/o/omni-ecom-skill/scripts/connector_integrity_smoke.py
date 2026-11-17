"""Behavioral checks for mock request identity and non-vacuous readback."""
import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from connectors import MockPlatformConnector, ConnectorError


class ConnectorIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.connector = MockPlatformConnector()
        self.action = dict(action_id='synthetic-action', client_scope='synthetic-client',
                           operation='campaign.resume',
                           target=dict(resource='campaign', platform_id='cmp-001'))

    def execute(self, action=None, dry_run=False):
        return self.connector.execute(action or self.action, approval_state='approved',
                                      idempotency_key='synthetic-key', dry_run=dry_run)

    def test_same_request_replays_without_reapplying(self):
        first = self.execute()
        self.connector._state['campaign']['cmp-001']['status'] = 'paused'
        self.assertEqual(first, self.execute())
        self.assertEqual('paused', self.connector.read('campaign', 'cmp-001')['data']['status'])
        first['after']['status'] = 'tampered'
        self.assertEqual('active', self.execute()['after']['status'])

    def test_changed_request_cannot_reuse_key(self):
        self.execute()
        for field, value in [('operation', 'campaign.pause'), ('client_scope', 'another-client'),
                             ('target', dict(resource='campaign', platform_id='other'))]:
            with self.subTest(field=field):
                changed = deepcopy(self.action)
                changed[field] = value
                with self.assertRaises(ConnectorError) as caught:
                    self.execute(changed)
                self.assertEqual('idempotency_conflict', caught.exception.error_class)

    def test_preview_cannot_be_replayed_as_execution(self):
        self.execute(dry_run=True)
        with self.assertRaises(ConnectorError):
            self.execute(dry_run=False)
        self.assertEqual('paused', self.connector.read('campaign', 'cmp-001')['data']['status'])

    def test_execution_cannot_be_replayed_as_preview(self):
        self.execute()
        with self.assertRaises(ConnectorError):
            self.execute(dry_run=True)

    def test_empty_readback_is_not_verification(self):
        for expected in ({}, None, []):
            with self.subTest(expected=expected), self.assertRaises(ConnectorError):
                self.connector.readback(self.action, expected)

    def test_missing_null_field_is_not_match(self):
        self.assertFalse(self.connector.readback(self.action, {'missing': None})['matched'])

    def test_boolean_is_not_numeric_match(self):
        self.connector._state['campaign']['cmp-001']['budget'] = 1
        self.assertFalse(self.connector.readback(self.action, {'budget': True})['matched'])

    def test_mock_results_always_disclose_simulation(self):
        self.assertTrue(self.execute()['simulated'])
        result = self.connector.readback(self.action, {'status': 'active'})
        self.assertTrue(result['matched'])
        self.assertTrue(result['simulated'])

    def test_nonfinite_request_does_not_mutate(self):
        self.action['budget'] = float('nan')
        with self.assertRaises(ValueError):
            self.execute()
        self.assertEqual('paused', self.connector.read('campaign', 'cmp-001')['data']['status'])


if __name__ == '__main__':
    unittest.main()
