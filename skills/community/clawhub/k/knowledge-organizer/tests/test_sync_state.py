from scripts import SyncStateRecord, SyncStateStore


def test_sync_state_round_trip(tmp_path):
    state_path = tmp_path / "state.json"
    store = SyncStateStore(state_path)

    record = SyncStateRecord(
        source_id="s" * 64,
        content_hash="c" * 64,
        destination="feishu",
        remote_id="doc_123",
        remote_url="https://example.com/doc/123",
        last_synced_at="2026-03-22T00:00:00Z",
        status="ok",
        error_message=None,
    )
    store.write(record)

    reloaded = SyncStateStore(state_path)
    loaded = reloaded.read(destination="feishu", source_id="s" * 64)

    assert loaded == record


def test_sync_state_read_missing_returns_none(tmp_path):
    store = SyncStateStore(tmp_path / "state.json")
    assert store.read(destination="ima", source_id="missing") is None


def test_sync_state_ignores_malformed_json(tmp_path):
    state_path = tmp_path / "state.json"
    state_path.write_text("{not valid json", encoding="utf-8")

    store = SyncStateStore(state_path)

    assert store.all_records() == []
