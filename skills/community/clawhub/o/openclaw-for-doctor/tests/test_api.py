import os

from fastapi.testclient import TestClient

os.environ.setdefault("OPENCLAW_DOCTOR_ENV", "test")
os.environ.setdefault("OPENCLAW_DOCTOR_TASK_STORE", "memory")

from app.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    resp = client.get('/api/health')
    assert resp.status_code == 200
    data = resp.json()
    assert data['status'] == 'ok'
    assert data['service'] == 'openclaw-for-doctor'
    assert data['env'] == 'test'
    assert data['task_store'] == 'memory'


def test_execute_endpoint() -> None:
    client = TestClient(app)
    payload = {
        'query': 'Need strict pneumonia differential with citations',
        'channel': 'webchat',
        'use_case': 'diagnosis',
    }
    resp = client.post('/api/tasks/execute', json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data['delivery']['channel'] == 'webchat'
    assert data['delivery']['delivered'] is True
