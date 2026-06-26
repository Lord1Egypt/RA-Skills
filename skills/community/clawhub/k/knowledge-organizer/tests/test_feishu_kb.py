from scripts import ImportDraft


def test_build_feishu_payload_contains_required_fields():
    from scripts.feishu_kb import build_feishu_payload

    draft = ImportDraft.from_mapping(
        {
            "title": "Feishu Note",
            "source_type": "web",
            "source_url": "https://example.com/note",
            "content": "Body text",
            "tags": ["tag-a", "tag-b"],
            "images": [{"url": "https://img.example/a.png"}],
            "attachments": [{"url": "https://files.example/a.pdf", "name": "a.pdf"}],
        }
    )

    payload = build_feishu_payload(draft)

    assert payload["title"] == "Feishu Note"
    assert "markdown" in payload
    assert not payload["markdown"].startswith("# Feishu Note")
    assert "https://example.com/note" in payload["markdown"]
    assert "tag-a" in payload["markdown"]
    assert "Body text" in payload["markdown"]
    assert '<image url="https://img.example/a.png"' in payload["markdown"]
    assert '<file url="https://files.example/a.pdf" name="a.pdf"' in payload["markdown"]


def test_import_to_feishu_returns_sync_record_from_transport():
    from scripts.feishu_kb import FeishuImportConfig, import_to_feishu

    draft = ImportDraft.from_mapping(
        {
            "title": "Feishu Note",
            "source_type": "markdown",
            "source_path": "/vault/note.md",
            "content": "Body text",
            "images": [{"url": "https://img.example/a.png"}],
            "attachments": [{"url": "https://files.example/a.pdf", "name": "a.pdf"}],
        }
    )

    seen = {}

    def fake_transport(payload, config):
        seen["payload"] = payload
        seen["config"] = config
        return {
            "doc_id": "doc_123",
            "doc_url": "https://www.feishu.cn/docx/doc_123",
        }

    result = import_to_feishu(
        draft,
        FeishuImportConfig(wiki_space="my_library"),
        transport=fake_transport,
    )

    assert seen["payload"]["title"] == "Feishu Note"
    assert seen["payload"]["wiki_space"] == "my_library"
    assert '<image url="https://img.example/a.png"' in seen["payload"]["markdown"]
    assert '<file url="https://files.example/a.pdf" name="a.pdf"' in seen["payload"]["markdown"]
    assert result.remote_id == "doc_123"
    assert result.remote_url == "https://www.feishu.cn/docx/doc_123"
    assert result.sync_record.destination == "feishu"
    assert result.sync_record.remote_id == "doc_123"


def test_resolve_feishu_config_reads_environment(monkeypatch):
    from scripts.feishu_kb import resolve_feishu_config

    monkeypatch.setenv("FEISHU_FOLDER_TOKEN", "fldcn_abc")
    monkeypatch.setenv("FEISHU_WIKI_NODE", "wikcn_def")
    monkeypatch.setenv("FEISHU_WIKI_SPACE", "7448000000000009300")

    config = resolve_feishu_config()

    assert config.folder_token == "fldcn_abc"
    assert config.wiki_node == "wikcn_def"
    assert config.wiki_space == "7448000000000009300"
