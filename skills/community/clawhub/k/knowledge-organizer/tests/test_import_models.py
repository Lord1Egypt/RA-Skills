import re


def test_import_draft_normalizes_required_fields():
    from scripts import ImportDraft

    draft = ImportDraft.from_mapping(
        {
            "title": "  Hello\nWorld  ",
            "source_type": "  Web  ",
            "source_url": " https://example.com/a?b=1 ",
            "content": "Line1\r\nLine2\n",
            "tags": ["  a ", None, "b", ""],
        }
    )

    assert draft.title == "Hello World"
    assert draft.source_type == "web"
    assert draft.source_url == "https://example.com/a?b=1"
    assert draft.tags == ["a", "b"]

    assert re.fullmatch(r"[0-9a-f]{64}", draft.source_id)
    assert re.fullmatch(r"[0-9a-f]{64}", draft.content_hash)


def test_import_draft_hashes_are_stable():
    from scripts import ImportDraft

    payload = {
        "title": "Test",
        "source_type": "web",
        "source_url": "https://example.com/x",
        "content": "same content",
    }
    one = ImportDraft.from_mapping(payload)
    two = ImportDraft.from_mapping(payload)

    assert one.source_id == two.source_id
    assert one.content_hash == two.content_hash


def test_import_draft_uses_source_path_for_non_url_sources():
    from scripts import ImportDraft

    one = ImportDraft.from_mapping(
        {
            "title": "Shared Title",
            "source_type": "markdown",
            "source_path": "/vault/a.md",
            "content": "same content",
        }
    )
    two = ImportDraft.from_mapping(
        {
            "title": "Shared Title",
            "source_type": "markdown",
            "source_path": "/vault/b.md",
            "content": "same content",
        }
    )

    assert one.source_id != two.source_id


def test_import_draft_round_trips_media_fields():
    from scripts import ImportDraft

    images = [
        {"url": "https://img.example/a.png", "alt": "a"},
        {"path": "assets/a.png"},
    ]
    attachments = {"url": "https://files.example/a.pdf", "name": "a.pdf"}

    draft = ImportDraft.from_mapping(
        {
            "title": "Media",
            "source_type": "web",
            "source_url": "https://example.com/media",
            "content": "Body",
            "images": images,
            # Accept single-object values without turning dicts into key lists.
            "attachments": attachments,
        }
    )

    assert draft.images == images
    assert draft.attachments == [attachments]

    mapping = draft.to_mapping()
    assert mapping["images"] == images
    assert mapping["attachments"] == [attachments]


def test_import_draft_copies_media_lists_on_input():
    from scripts import ImportDraft

    images = [{"url": "https://img.example/a.png"}]
    attachments = [{"url": "https://files.example/a.pdf"}]

    draft = ImportDraft.from_mapping(
        {
            "title": "Media",
            "source_type": "web",
            "source_url": "https://example.com/media",
            "content": "Body",
            "images": images,
            "attachments": attachments,
        }
    )

    images.append({"url": "https://img.example/b.png"})
    attachments.append({"url": "https://files.example/b.pdf"})

    assert draft.images == [{"url": "https://img.example/a.png"}]
    assert draft.attachments == [{"url": "https://files.example/a.pdf"}]
