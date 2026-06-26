from scripts import ImportDraft


def test_build_ima_payload_contains_required_fields():
    from scripts.ima_kb import build_ima_payload

    draft = ImportDraft.from_mapping(
        {
            "title": "IMA Note",
            "source_type": "web",
            "source_url": "https://example.com/note",
            "content": "Body text",
            "tags": ["tag-a", "tag-b"],
            "images": [{"url": "https://img.example/a.png"}],
            "attachments": [{"url": "https://files.example/a.pdf", "name": "a.pdf"}],
        }
    )

    payload = build_ima_payload(draft)

    assert payload["content_format"] == 1
    assert payload["content"].startswith("# IMA Note")
    assert "https://example.com/note" in payload["content"]
    assert "tag-a" in payload["content"]
    assert "Body text" in payload["content"]
    assert "https://img.example/a.png" in payload["content"]
    assert "https://files.example/a.pdf" in payload["content"]


def test_build_ima_payload_honors_folder_id():
    from scripts.ima_kb import build_ima_payload

    draft = ImportDraft.from_mapping(
        {
            "title": "IMA Note",
            "source_type": "markdown",
            "source_path": "/vault/note.md",
            "content": "Body text",
        }
    )

    payload = build_ima_payload(draft, folder_id="folder_123")
    assert payload["folder_id"] == "folder_123"


def test_import_to_ima_returns_sync_record_from_transport():
    from scripts.ima_kb import ImaImportConfig, import_to_ima

    draft = ImportDraft.from_mapping(
        {
            "title": "IMA Note",
            "source_type": "markdown",
            "source_path": "/vault/note.md",
            "content": "Body text",
        }
    )

    seen = {}

    def fake_transport(payload, config):
        seen["payload"] = payload
        seen["config"] = config
        return {"doc_id": "doc_123"}

    result = import_to_ima(
        draft,
        ImaImportConfig(client_id="c", api_key="k", base_url="https://ima.qq.com/openapi/note/v1"),
        transport=fake_transport,
    )

    assert seen["payload"]["content_format"] == 1
    assert result.remote_id == "doc_123"
    assert result.remote_url is None
    assert result.sync_record.destination == "ima"
    assert result.sync_record.remote_id == "doc_123"


def test_import_to_ima_raises_on_application_error():
    from scripts.ima_kb import ImaImportConfig, import_to_ima

    draft = ImportDraft.from_mapping(
        {
            "title": "IMA Note",
            "source_type": "markdown",
            "source_path": "/vault/note.md",
            "content": "Body text",
        }
    )

    def fake_transport(payload, config):
        return {"code": 100001, "msg": "参数错误"}

    try:
        import_to_ima(
            draft,
            ImaImportConfig(client_id="c", api_key="k", base_url="https://ima.qq.com/openapi/note/v1"),
            transport=fake_transport,
        )
    except RuntimeError as exc:
        assert "100001" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError for application-level failure")


def test_resolve_ima_config_reads_environment(monkeypatch):
    from scripts.ima_kb import resolve_ima_config

    monkeypatch.setenv("IMA_OPENAPI_CLIENTID", "client_123")
    monkeypatch.setenv("IMA_OPENAPI_APIKEY", "key_456")
    monkeypatch.setenv("IMA_OPENAPI_BASE_URL", "https://ima.qq.com/openapi/note/v1")
    monkeypatch.setenv("IMA_OPENAPI_FOLDER_ID", "folder_abc")

    config = resolve_ima_config()

    assert config.client_id == "client_123"
    assert config.api_key == "key_456"
    assert config.base_url == "https://ima.qq.com/openapi/note/v1"
    assert config.folder_id == "folder_abc"
