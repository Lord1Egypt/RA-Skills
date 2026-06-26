from src.app import app


def test_index_ok():
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200


def test_health_ok():
    client = app.test_client()
    r = client.get("/health")
    assert r.status_code == 200


def test_health_json_shape():
    client = app.test_client()
    r = client.get("/health")
    data = r.get_json()
    assert isinstance(data, dict)
    assert data.get("status") == "ok"
    assert data.get("service") == "lobster-eval"
