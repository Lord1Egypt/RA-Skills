"""Synthetic cross-run storage, substitution and backup acceptance checks."""
import json
from pathlib import Path
import shutil
import sqlite3
import unittest

from action_gateway import ActionGateway
import action_gateway_smoke as gateway_fixtures
from execution_store import ExecutionStore, verify_backup, PROFILE, DATABASE


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.fixture = gateway_fixtures.GatewayTests()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.root = Path(self.fixture.temp.name)
        self.store = ExecutionStore.create(self.root / 'authority', [self.fixture.binding])
        self.addCleanup(lambda: self.store.close())
        self.store.bind_run('run1', self.fixture.binding, '2.0.3-candidate.1', 'synthetic-action')

    def execute(self):
        f = self.fixture
        gateway = self.store.gateway(f.connector, f.binding, execution_enabled=True,
                                    approval_verifier=lambda a, r: a == f.approval)
        return gateway.execute(f.action, f.policy, f.objects, f.credential, f.snapshot, f.approval)

    def test_shared_store_survives_new_task_and_restart(self):
        self.assertEqual('verified', self.execute()['outcome'])
        self.store.close()
        self.store = ExecutionStore.open(self.root / 'authority' / PROFILE)
        self.store.bind_run('run2', self.fixture.binding, '2.0.3-candidate.1', 'synthetic-action')
        self.fixture.action['run_id'] = 'run2'
        with self.assertRaisesRegex(ValueError, 'another_run'):
            self.execute()
        self.assertEqual(1, self.fixture.connector.calls)

    def test_missing_database_is_not_recreated(self):
        self.store.close()
        database = self.root / 'authority' / DATABASE
        database.rename(self.root / 'preserved-database.sqlite')
        with self.assertRaisesRegex(ValueError, 'database_missing'):
            ExecutionStore.open(self.root / 'authority' / PROFILE)
        self.assertFalse(database.exists())

    def test_missing_profile_is_not_recreated(self):
        profile = self.root / 'authority' / PROFILE
        profile.rename(self.root / 'preserved-profile.json')
        with self.assertRaisesRegex(ValueError, 'profile_missing'):
            ExecutionStore.open(profile)
        self.assertFalse(profile.exists())

    def test_new_empty_database_cannot_replace_authority(self):
        self.store.close()
        database = self.root / 'authority' / DATABASE
        database.rename(self.root / 'preserved.sqlite')
        sqlite3.connect(database).close()
        with self.assertRaises((ValueError, sqlite3.Error)):
            ExecutionStore.open(self.root / 'authority' / PROFILE)
        connection = sqlite3.connect(database)
        try:
            self.assertEqual([], connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
        finally:
            connection.close()

    def test_profile_edit_after_open_prevents_connector_use(self):
        profile = self.root / 'authority' / PROFILE
        content = json.loads(profile.read_text(encoding='utf-8'))
        content['scopes'][0]['account_id'] = 'another-account'
        profile.write_text(json.dumps(content), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'profile_changed'):
            self.execute()
        self.assertEqual(0, self.fixture.connector.calls)

    def test_unknown_scope_cannot_be_bound(self):
        other = dict(self.fixture.binding, store_id='another-store')
        with self.assertRaisesRegex(ValueError, 'scope_not_registered'):
            self.store.bind_run('other', other, '2.0.3-candidate.1', 'synthetic-action')
        self.assertIsNone(self.store.journal.db.execute('SELECT * FROM runs WHERE run_id=?', ('other',)).fetchone())

    def test_existing_run_cannot_move_to_other_registered_store(self):
        self.store.close()
        second = dict(self.fixture.binding, store_id='second-store')
        self.store = ExecutionStore.create(self.root / 'multi-store', [self.fixture.binding, second])
        self.store.bind_run('same-run', self.fixture.binding, '2.0.3-candidate.1', 'synthetic-action')
        with self.assertRaisesRegex(ValueError, 'run_scope_conflict'):
            self.store.bind_run('same-run', second, '2.0.3-candidate.1', 'synthetic-action')

    def test_unbound_report_journal_run_is_not_accepted(self):
        self.store.journal.create('plain-run', 'synthetic', '2.0.3-candidate.1', 'synthetic-action')
        self.fixture.action['run_id'] = 'plain-run'
        with self.assertRaisesRegex(ValueError, 'run_not_bound'):
            self.execute()
        self.assertEqual(0, self.fixture.connector.reads)

    def test_copied_store_is_not_a_new_executable_authority(self):
        self.store.close()
        shutil.copytree(self.root / 'authority', self.root / 'copied')
        with self.assertRaisesRegex(ValueError, 'identity_mismatch'):
            ExecutionStore.open(self.root / 'copied' / PROFILE)

    def test_backup_preserves_heads_and_cannot_execute(self):
        self.execute()
        manifest = self.store.backup(self.root / 'backup')
        self.assertEqual(manifest, verify_backup(self.root / 'backup'))
        self.assertEqual(5, manifest['runs'][0]['events'])
        with self.assertRaisesRegex(ValueError, 'identity_mismatch'):
            ExecutionStore.open(self.root / 'backup' / PROFILE)
        self.assertEqual(1, self.fixture.connector.calls)

    def test_existing_backup_destination_is_preserved(self):
        self.store.backup(self.root / 'backup')
        manifest = (self.root / 'backup' / 'backup.json').read_bytes()
        with self.assertRaises(FileExistsError):
            self.store.backup(self.root / 'backup')
        self.assertEqual(manifest, (self.root / 'backup' / 'backup.json').read_bytes())

    def test_backup_tampering_is_detected(self):
        self.store.backup(self.root / 'backup')
        database = self.root / 'backup' / DATABASE
        with database.open('ab') as stream:
            stream.write(b'synthetic tampering')
        with self.assertRaisesRegex(ValueError, 'database_changed'):
            verify_backup(self.root / 'backup')

    def test_scope_metadata_cannot_be_mutated(self):
        with self.assertRaises(sqlite3.Error):
            self.store.journal.db.execute("UPDATE execution_run_scopes SET scope_sha256='wrong'")
        with self.assertRaises(sqlite3.Error):
            self.store.journal.db.execute('DELETE FROM execution_store_identity')

    def test_duplicate_account_assignment_is_rejected_before_directory_creation(self):
        other = dict(self.fixture.binding, client_scope='other-client')
        with self.assertRaisesRegex(ValueError, 'scope_ambiguous'):
            ExecutionStore.create(self.root / 'ambiguous', [self.fixture.binding, other])
        self.assertFalse((self.root / 'ambiguous').exists())

    def test_create_never_overwrites_existing_store(self):
        profile = (self.root / 'authority' / PROFILE).read_bytes()
        with self.assertRaises(FileExistsError):
            ExecutionStore.create(self.root / 'authority', [self.fixture.binding])
        self.assertEqual(profile, (self.root / 'authority' / PROFILE).read_bytes())

    def test_api_mode_requires_authority_even_if_json_says_approved(self):
        f = self.fixture
        original = f.connector.capabilities
        f.connector.capabilities = lambda: dict(original(), mode='api', status='write_ready')
        # This is a mock advertising API mode solely to test the gate, not an API adapter.
        with self.assertRaisesRegex(ValueError, 'authoritative_store_required'):
            f.execute()
        self.assertEqual((0, 0), (f.connector.calls, f.connector.reads))

    def test_wrong_journal_cannot_claim_another_store_authority(self):
        f = self.fixture
        gateway = ActionGateway(f.journal, f.connector, f.binding, authority=self.store,
                                execution_enabled=True, approval_verifier=lambda a, r: True)
        with self.assertRaisesRegex(ValueError, 'wrong_journal'):
            f.execute(gateway)
        self.assertEqual(0, f.connector.calls)

    def test_bound_reference_is_repeatable_and_contains_no_credential(self):
        first = self.store.bind_run('run1', self.fixture.binding, '2.0.3-candidate.1', 'synthetic-action')
        second = self.store.bind_run('run1', self.fixture.binding, '2.0.3-candidate.1', 'synthetic-action')
        self.assertEqual(first, second)
        self.assertNotIn('secret_ref', str(first))
        self.assertEqual(str((self.root / 'authority' / PROFILE).resolve()), first['profile_path'])
        self.assertEqual('run1', self.store.check_reference(first, 'run1', 'synthetic')['run_id'])

    def test_report_reference_cannot_select_another_store_or_run(self):
        ref = self.store.bind_run('run1', self.fixture.binding, '2.0.3-candidate.1', 'synthetic-action')
        for field, value in [('run_id', 'other-run'), ('client_scope', 'other-client'),
                             ('profile_path', str(self.root / 'other' / PROFILE)),
                             ('execution_store_id', 'another-store'), ('scope_sha256', '0' * 64)]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.store.check_reference(dict(ref, **{field: value}), 'run1', 'synthetic')

    def test_backup_during_local_write_transaction_stops_without_creating_files(self):
        with self.store.journal.transaction():
            with self.assertRaisesRegex(ValueError, 'transaction_active'):
                self.store.backup(self.root / 'busy-backup')
        self.assertFalse((self.root / 'busy-backup').exists())


if __name__ == '__main__':
    unittest.main()
