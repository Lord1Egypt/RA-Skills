"""Pinned cross-run action store. Initialization is explicit, never recovery.

The trusted host owns the profile path and allowed scopes. Configuration is not
platform authorization. Backups are inspection-only, not a new execution store.
"""
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
from uuid import uuid4

from run_journal import Journal, check_payload, digest, encoded


SCOPE_FIELDS = ('client_scope', 'platform', 'account_id', 'store_id', 'connector_id')
PROFILE = 'execution-store.json'
DATABASE = 'execution.sqlite'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def byte_hash(value):
    return hashlib.sha256(value).hexdigest()


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'execution_store_duplicate_json_key')
            result[key] = value
        return result
    raw = path.read_bytes()
    value = json.loads(raw.decode('utf-8-sig'), object_pairs_hook=pairs)
    check_payload(value)
    digest(value)
    return value, byte_hash(raw)


def write_new(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(encoded(value))
        stream.flush()
        os.fsync(stream.fileno())


def validate_scopes(scopes):
    require(isinstance(scopes, list) and scopes, 'execution_store_scope_required')
    seen = set()
    for scope in scopes:
        require(isinstance(scope, dict) and set(scope) == set(SCOPE_FIELDS) and
                all(isinstance(scope[k], str) and scope[k].strip() for k in SCOPE_FIELDS),
                'execution_store_scope_invalid')
        # Never assign the same platform account/store to two clients or connector aliases.
        key = tuple(scope[k] for k in ('platform', 'account_id', 'store_id'))
        require(key not in seen, 'execution_store_scope_ambiguous')
        seen.add(key)


def snapshot_heads(journal):
    require(journal.db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok',
            'execution_store_integrity_failed')
    result = []
    for run in journal.db.execute('SELECT * FROM runs ORDER BY run_id').fetchall():
        rows = journal.events(run['run_id'], run['client_scope'])
        result.append(dict(run_id=run['run_id'], client_scope=run['client_scope'],
                           events=len(rows), last_event_hash=rows[-1]['event_hash'] if rows else ''))
    return result


class ExecutionStore:
    @classmethod
    def create(cls, directory, scopes):
        """Provision once into a new directory. Never auto-called by open/execute."""
        scopes = deepcopy(scopes)
        validate_scopes(scopes)
        check_payload(scopes)
        root = Path(directory).resolve()
        root.mkdir(parents=False, exist_ok=False)
        profile = dict(schema_version='2.0', execution_store_id=uuid4().hex,
                       database=DATABASE, scopes=scopes)
        journal = Journal(root / DATABASE)
        try:
            journal.db.executescript('''
              CREATE TABLE execution_store_identity (
                singleton INTEGER PRIMARY KEY CHECK(singleton=1),
                store_id TEXT NOT NULL, root TEXT NOT NULL, profile_sha256 TEXT NOT NULL);
              CREATE TABLE execution_run_scopes (
                run_id TEXT PRIMARY KEY REFERENCES runs(run_id), scope_sha256 TEXT NOT NULL);
              CREATE TRIGGER execution_identity_no_update BEFORE UPDATE ON execution_store_identity
                BEGIN SELECT RAISE(ABORT,'immutable_store_identity'); END;
              CREATE TRIGGER execution_identity_no_delete BEFORE DELETE ON execution_store_identity
                BEGIN SELECT RAISE(ABORT,'immutable_store_identity'); END;
              CREATE TRIGGER execution_scope_no_update BEFORE UPDATE ON execution_run_scopes
                BEGIN SELECT RAISE(ABORT,'immutable_run_scope'); END;
              CREATE TRIGGER execution_scope_no_delete BEFORE DELETE ON execution_run_scopes
                BEGIN SELECT RAISE(ABORT,'immutable_run_scope'); END;
            ''')
            write_new(root / PROFILE, profile)
            with journal.transaction():
                journal.db.execute('INSERT INTO execution_store_identity VALUES (1,?,?,?)',
                                   (profile['execution_store_id'], str(root), byte_hash((root / PROFILE).read_bytes())))
        finally:
            journal.close()
        return cls.open(root / PROFILE)

    @classmethod
    def open(cls, profile_path):
        """Open only existing files; missing/corrupt state must not start a fresh ledger."""
        location = Path(profile_path).resolve()
        require(location.name == PROFILE and location.is_file(), 'execution_store_profile_missing')
        profile, fingerprint = read_json(location)
        require(isinstance(profile, dict) and set(profile) ==
                {'schema_version', 'execution_store_id', 'database', 'scopes'} and
                profile['schema_version'] == '2.0' and profile['database'] == DATABASE and
                isinstance(profile['execution_store_id'], str) and bool(profile['execution_store_id']),
                'execution_store_profile_invalid')
        validate_scopes(profile['scopes'])
        database = location.parent / DATABASE
        require(database.is_file() and database.resolve().parent == location.parent,
                'execution_store_database_missing_or_redirected')
        journal = Journal(database, existing_only=True)
        instance = cls()
        instance.profile_path, instance.profile, instance.fingerprint = location, profile, fingerprint
        instance.database, instance.journal = database, journal
        stat = database.stat()
        instance.file_identity = (stat.st_dev, stat.st_ino)
        try:
            instance.assert_store()
            snapshot_heads(journal)
        except BaseException:
            journal.close()
            raise
        return instance

    def close(self):
        self.journal.close()

    def assert_store(self):
        require(self.profile_path.is_file() and self.database.is_file(), 'execution_store_files_missing')
        profile, fingerprint = read_json(self.profile_path)
        require(fingerprint == self.fingerprint and profile == self.profile, 'execution_store_profile_changed')
        stat = self.database.stat()
        require((stat.st_dev, stat.st_ino) == self.file_identity, 'execution_store_database_replaced')
        row = self.journal.db.execute('SELECT * FROM execution_store_identity WHERE singleton=1').fetchone()
        require(row is not None and row['store_id'] == self.profile['execution_store_id'] and
                Path(row['root']).resolve() == self.profile_path.parent and
                row['profile_sha256'] == self.fingerprint, 'execution_store_identity_mismatch')
        opened = self.journal.db.execute('PRAGMA database_list').fetchone()['file']
        require(Path(opened).resolve() == self.database.resolve(), 'execution_store_connection_mismatch')

    def bind_run(self, run_id, binding, version, task_type):
        self.assert_store()
        require(binding in self.profile['scopes'], 'execution_store_scope_not_registered')
        require(all(isinstance(v, str) and v.strip() for v in (run_id, version, task_type)),
                'execution_store_run_identity_missing')
        identity = (run_id, binding['client_scope'], version, task_type)
        with self.journal.transaction():
            old = self.journal.db.execute('SELECT * FROM runs WHERE run_id=?', (run_id,)).fetchone()
            scope = self.journal.db.execute('SELECT scope_sha256 FROM execution_run_scopes WHERE run_id=?',
                                            (run_id,)).fetchone()
            require(old is None or tuple(old) == identity, 'execution_store_run_identity_conflict')
            require((old is None and scope is None) or (scope is not None and scope[0] == digest(binding)),
                    'execution_store_run_scope_conflict')
            self.journal.db.execute('INSERT OR IGNORE INTO runs VALUES (?,?,?,?)', identity)
            self.journal.db.execute('INSERT OR IGNORE INTO execution_run_scopes VALUES (?,?)',
                                    (run_id, digest(binding)))
        return dict(schema_version='2.0', execution_store_id=self.profile['execution_store_id'],
                    profile_path=str(self.profile_path), profile_sha256=self.fingerprint,
                    run_id=run_id, client_scope=binding['client_scope'], scope_sha256=digest(binding))

    def assert_run(self, journal, action, binding):
        self.assert_store()
        require(journal is self.journal, 'execution_store_wrong_journal')
        require(binding in self.profile['scopes'] and all(action.get(k) == binding[k] for k in
                ('client_scope', 'platform', 'account_id', 'store_id')), 'execution_store_scope_mismatch')
        row = journal.db.execute('SELECT scope_sha256 FROM execution_run_scopes WHERE run_id=?',
                                 (action['run_id'],)).fetchone()
        require(row is not None and row[0] == digest(binding), 'execution_store_run_not_bound')
        journal.events(action['run_id'], action['client_scope'])

    def check_reference(self, reference, run_id, client_scope):
        """Validate a report's pointer against the host-pinned store, not vice versa."""
        self.assert_store()
        require(isinstance(reference, dict) and set(reference) ==
                {'schema_version', 'execution_store_id', 'profile_path', 'profile_sha256',
                 'run_id', 'client_scope', 'scope_sha256'}, 'execution_store_reference_invalid')
        require(reference['schema_version'] == '2.0' and reference['run_id'] == run_id and
                reference['client_scope'] == client_scope and
                reference['execution_store_id'] == self.profile['execution_store_id'] and
                reference['profile_sha256'] == self.fingerprint and
                Path(reference['profile_path']).resolve() == self.profile_path, 'execution_store_reference_mismatch')
        row = self.journal.db.execute('SELECT scope_sha256 FROM execution_run_scopes WHERE run_id=?',
                                     (run_id,)).fetchone()
        require(row is not None and row[0] == reference['scope_sha256'], 'execution_store_reference_scope_mismatch')
        return self.journal.status(run_id, client_scope)

    def gateway(self, connector, binding, **options):
        from action_gateway import ActionGateway
        self.assert_store()
        require(binding in self.profile['scopes'], 'execution_store_scope_not_registered')
        return ActionGateway(self.journal, connector, binding, authority=self, **options)

    def read_gateway(self, connector, binding, **options):
        """Construct a read-only gateway pinned to this store and scope."""
        from platform_read_guard import PlatformReadGateway
        self.assert_store()
        require(binding in self.profile['scopes'], 'execution_store_scope_not_registered')
        return PlatformReadGateway(self.journal, connector, binding, authority=self, **options)

    def backup(self, destination):
        """Create an inspection-only consistent SQLite snapshot, never overwrite."""
        self.assert_store()
        require(not self.journal.db.in_transaction, 'execution_store_backup_transaction_active')
        root = Path(destination).resolve()
        root.mkdir(parents=False, exist_ok=False)
        target = sqlite3.connect(root / DATABASE)
        try:
            self.journal.db.backup(target)
        finally:
            target.close()
        copied = Journal(root / DATABASE, read_only=True)
        try:
            heads = snapshot_heads(copied)
        finally:
            copied.close()
        # Original canonical profile bytes matter, not a reserialized equivalent.
        with (root / PROFILE).open('xb') as stream:
            stream.write(self.profile_path.read_bytes())
            stream.flush()
            os.fsync(stream.fileno())
        manifest = dict(schema_version='2.0', backup_kind='inspection_only_not_executable',
                        execution_store_id=self.profile['execution_store_id'],
                        created_at=datetime.now(timezone.utc).isoformat(), profile_sha256=self.fingerprint,
                        database_sha256=byte_hash((root / DATABASE).read_bytes()), runs=heads)
        write_new(root / 'backup.json', manifest)
        verify_backup(root)
        return manifest


def verify_backup(directory):
    root = Path(directory).resolve()
    manifest, _ = read_json(root / 'backup.json')
    profile, profile_hash = read_json(root / PROFILE)
    require(manifest.get('backup_kind') == 'inspection_only_not_executable' and
            manifest.get('profile_sha256') == profile_hash and
            manifest.get('execution_store_id') == profile.get('execution_store_id'), 'execution_backup_profile_mismatch')
    before = byte_hash((root / DATABASE).read_bytes())
    require(before == manifest.get('database_sha256'), 'execution_backup_database_changed')
    journal = Journal(root / DATABASE, read_only=True)
    try:
        require(snapshot_heads(journal) == manifest.get('runs'), 'execution_backup_heads_mismatch')
        identity = journal.db.execute('SELECT * FROM execution_store_identity WHERE singleton=1').fetchone()
        require(identity is not None and identity['store_id'] == profile['execution_store_id'] and
                identity['profile_sha256'] == profile_hash, 'execution_backup_identity_mismatch')
    finally:
        journal.close()
    require(byte_hash((root / DATABASE).read_bytes()) == before, 'execution_backup_changed_during_check')
    return manifest
