"""Storage reservations remain isolated across sessions, workers and restarts."""
import json
import hashlib
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from skill.core import AuditEngine
from skill.security import b64, canonical, sign_event
from skill.types import FriendlyEvent


@pytest.fixture
def signing_keys():
    private = Ed25519PrivateKey.generate()
    public = {'writer': {'test': b64(private.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw))}}
    return private, public


def event(keys, tenant, session, payload=None):
    value = FriendlyEvent(str(uuid4()), 'J', 'writer', datetime.now(timezone.utc).isoformat(),
                          target='test', assertion=payload or {'value': True})
    value.signature = sign_event(value, {'purpose': 'audit', 'tenant': tenant, 'session': session},
                                 keys[0], 'test')
    return value


def reservations(monkeypatch, **tenants):
    policy = {name: {'max_events': count, 'max_bytes': 32768} for name, count in tenants.items()}
    monkeypatch.setenv('JEP_AUDIT_TENANT_QUOTAS', json.dumps(policy))
    return policy


def test_one_tenant_cannot_consume_another_tenants_reservation(monkeypatch, signing_keys):
    reservations(monkeypatch, alpha=2, beta=2)
    engine = AuditEngine(':memory:', signing_keys[1])
    for session in ['first', 'second']:
        engine.ingest(session, event(signing_keys, 'alpha', session), 'alpha')
    with pytest.raises(OverflowError):
        engine.ingest('third', event(signing_keys, 'alpha', 'third'), 'alpha')
    # Even after alpha reaches its aggregate quota, beta can fill its own reservation.
    for session in ['first', 'second']:
        engine.ingest(session, event(signing_keys, 'beta', session), 'beta')
    assert engine.db.execute('SELECT tenant, COUNT(*) FROM events GROUP BY tenant ORDER BY tenant').fetchall() == [
        ('alpha', 2), ('beta', 2)]


def test_byte_quota_is_atomic_and_does_not_block_other_tenants(signing_keys):
    first = event(signing_keys, 'alpha', 's', {'text': '中文' * 50})
    policy = {'alpha': {'max_events': 10, 'max_bytes': len(canonical(first))},
              'beta': {'max_events': 10, 'max_bytes': 32768}}
    engine = AuditEngine(':memory:', signing_keys[1], tenant_quotas=policy)
    with pytest.raises(OverflowError, match='byte capacity'):
        engine.ingest_batch('s', [first, event(signing_keys, 'alpha', 's')], 'alpha')
    assert not engine.build_chain('s', 'alpha').links
    # The rolled-back batch must not consume quota or burn its replay identifier.
    engine.ingest('s', first, 'alpha')
    with pytest.raises(OverflowError, match='byte capacity'):
        engine.ingest('another', event(signing_keys, 'alpha', 'another'), 'alpha')
    engine.ingest('s', event(signing_keys, 'beta', 's'), 'beta')
    assert len(engine.build_chain('s', 'beta').links) == 1


def test_event_quota_rejects_entire_batch(monkeypatch, signing_keys):
    reservations(monkeypatch, alpha=2)
    engine = AuditEngine(':memory:', signing_keys[1])
    values = [event(signing_keys, 'alpha', 's') for _ in range(3)]
    with pytest.raises(OverflowError):
        engine.ingest_batch('s', values, 'alpha')
    assert not engine.build_chain('s', 'alpha').links
    engine.ingest_batch('s', values[:2], 'alpha')
    assert len(engine.build_chain('s', 'alpha').links) == 2


def test_quotas_survive_restart_without_erasing_history(monkeypatch, signing_keys, tmp_path):
    reservations(monkeypatch, alpha=1, beta=1)
    tmp_path.chmod(0o700)
    database = str(tmp_path / 'audit.db')
    first = AuditEngine(database, signing_keys[1])
    first.ingest('s', event(signing_keys, 'alpha', 's'), 'alpha')
    first.db.close()
    second = AuditEngine(database, signing_keys[1])
    with pytest.raises(OverflowError):
        second.ingest('new-session', event(signing_keys, 'alpha', 'new-session'), 'alpha')
    second.ingest('s', event(signing_keys, 'beta', 's'), 'beta')
    assert len(second.build_chain('s', 'alpha').links) == 1
    assert len(second.build_chain('s', 'beta').links) == 1
    second.db.close()


def test_concurrent_connections_cannot_oversubscribe(monkeypatch, signing_keys, tmp_path):
    reservations(monkeypatch, alpha=3, beta=2)
    tmp_path.chmod(0o700)
    database = str(tmp_path / 'audit.db')
    engines = [AuditEngine(database, signing_keys[1]) for _ in range(2)]
    barrier = threading.Barrier(2)
    batches = [[event(signing_keys, 'alpha', str(i)) for _ in range(2)] for i in range(2)]
    def write(i):
        barrier.wait(timeout=5)
        try:
            engines[i].ingest_batch(str(i), batches[i], 'alpha')
            return 'accepted'
        except OverflowError:
            return 'full'
    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sorted(pool.map(write, range(2))) == ['accepted', 'full']
    assert engines[0].db.execute("SELECT COUNT(*) FROM events WHERE tenant='alpha'").fetchone()[0] == 2
    engines[0].ingest_batch('s', [event(signing_keys, 'beta', 's') for _ in range(2)], 'beta')
    for engine in engines:
        engine.db.close()


@pytest.mark.parametrize('policy', [
    {}, [], {'alpha': 10}, {'alpha': {'max_events': True, 'max_bytes': 1000}},
    {'alpha': {'max_events': 0, 'max_bytes': 1000}},
    {'alpha': {'max_events': 10, 'max_bytes': -1}},
    {'alpha': {'max_events': '10', 'max_bytes': 1000}},
    {' alpha ': {'max_events': 10, 'max_bytes': 1000}},
    {'alpha': {'max_events': 60000, 'max_bytes': 1000}, 'beta': {'max_events': 60000, 'max_bytes': 1000}},
    {'alpha': {'max_events': 10, 'max_bytes': 200 * 1024 * 1024}, 'beta': {'max_events': 10, 'max_bytes': 200 * 1024 * 1024}},
])
def test_invalid_or_overcommitted_reservations_fail_closed(policy, signing_keys):
    with pytest.raises(ValueError):
        AuditEngine(':memory:', signing_keys[1], tenant_quotas=policy)


def test_unconfigured_tenant_cannot_allocate_capacity(monkeypatch, signing_keys):
    reservations(monkeypatch, alpha=2)
    engine = AuditEngine(':memory:', signing_keys[1])
    with pytest.raises(ValueError, match='No storage reservation'):
        engine.ingest('s', event(signing_keys, 'beta', 's'), 'beta')
    assert engine.db.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 0


def test_different_worker_policy_is_rejected(monkeypatch, signing_keys, tmp_path):
    policy = reservations(monkeypatch, alpha=2, beta=2)
    tmp_path.chmod(0o700)
    database = str(tmp_path / 'audit.db')
    first = AuditEngine(database, signing_keys[1])
    policy['alpha']['max_events'] = 3
    with pytest.raises(ValueError, match='differs from this database'):
        AuditEngine(database, signing_keys[1], tenant_quotas=policy)
    first.ingest('s', event(signing_keys, 'beta', 's'), 'beta')
    assert len(first.build_chain('s', 'beta').links) == 1
    first.db.close()


def test_legacy_database_adoption_preserves_replay_protection(monkeypatch, signing_keys, tmp_path):
    reservations(monkeypatch, alpha=3)
    tmp_path.chmod(0o700)
    database = str(tmp_path / 'audit.db')
    first = AuditEngine(database, signing_keys[1])
    value = event(signing_keys, 'alpha', 's')
    first.ingest('s', value, 'alpha')
    # 2.0.0 used the same events schema without a reservation policy table.
    first.db.execute('DROP TABLE audit_capacity_policy')
    first.db.commit()
    first.db.close()
    second = AuditEngine(database, signing_keys[1])
    with pytest.raises(ValueError, match='Duplicate event ID'):
        second.ingest('s', value, 'alpha')
    assert len(second.build_chain('s', 'alpha').links) == 1
    second.db.close()


def test_legacy_overquota_data_is_preserved_on_failed_migration(monkeypatch, signing_keys, tmp_path):
    policy = reservations(monkeypatch, alpha=3)
    tmp_path.chmod(0o700)
    database = str(tmp_path / 'audit.db')
    first = AuditEngine(database, signing_keys[1])
    first.ingest_batch('s', [event(signing_keys, 'alpha', 's') for _ in range(2)], 'alpha')
    first.db.execute('DROP TABLE audit_capacity_policy')
    first.db.commit()
    first.db.close()
    policy['alpha']['max_events'] = 1
    with pytest.raises(ValueError, match='Existing audit data'):
        AuditEngine(database, signing_keys[1], tenant_quotas=policy)
    with sqlite3.connect(database) as connection:
        assert connection.execute('SELECT COUNT(*) FROM events').fetchone()[0] == 2


def test_api_uses_authenticated_tenant_and_returns_429_at_quota(monkeypatch, signing_keys):
    reservations(monkeypatch, alpha=1, beta=1)
    monkeypatch.setenv('JEP_AUDIT_DB', ':memory:')
    from fastapi.testclient import TestClient
    from skill import api
    engine = AuditEngine(':memory:', signing_keys[1])
    monkeypatch.setattr(api, 'engine', engine)
    tokens = {name: 'test-' + name + 'x' * 40 for name in ['alpha', 'beta']}
    config = {hashlib.sha256(token.encode()).hexdigest():
              {'tenant': name, 'issuers': ['writer'], 'permissions': ['audit:write', 'audit:read']}
              for name, token in tokens.items()}
    monkeypatch.setenv('JEP_CLIENTS', json.dumps(config))
    client = TestClient(api.app)
    def ingest(name, session, **extra):
        return client.post('/audit/ingest', headers={'Authorization': 'Bearer ' + tokens[name]},
                           json={'session_id': session, 'events': [asdict(event(signing_keys, name, session))], **extra})
    assert ingest('alpha', 's').status_code == 200
    assert ingest('alpha', 'another').status_code == 429
    assert ingest('alpha', 'another', tenant='beta').status_code == 422
    assert ingest('alpha', 'another', max_events=99999).status_code == 422
    assert ingest('beta', 's').status_code == 200
