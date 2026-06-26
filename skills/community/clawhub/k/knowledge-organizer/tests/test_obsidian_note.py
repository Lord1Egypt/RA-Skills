import re
from pathlib import Path

from scripts import markdown_helpers
import pytest


def test_render_image_markdown_copies_local_images_into_assets(tmp_path):
    from scripts import image_assets

    source_image = tmp_path / "source" / "local-figure.png"
    source_image.parent.mkdir(parents=True)
    source_image.write_bytes(b"local image bytes")

    rendered = image_assets.render_image_markdown(
        {"path": str(source_image), "alt": "Local figure"},
        vault_root=tmp_path,
        note_title="Image Note",
    )

    expected_path = tmp_path / "assets" / "Image Note" / "local-figure.png"
    assert rendered == "![Local figure](assets/Image Note/local-figure.png)"
    assert expected_path.read_bytes() == b"local image bytes"


def test_render_image_markdown_downloads_remote_images_into_assets(tmp_path):
    from scripts import image_assets

    def fake_downloader(url: str, destination: Path) -> None:
        destination.write_bytes(f"downloaded:{url}".encode("utf-8"))

    rendered = image_assets.render_image_markdown(
        {
            "data_src": "https://example.com/hero.png?from=appmsg",
            "alt": "Hero Figure",
        },
        vault_root=tmp_path,
        note_title="Image Note",
        download_image=fake_downloader,
    )

    expected_path = tmp_path / "assets" / "Image Note" / "hero.png"
    assert rendered == "![Hero Figure](assets/Image Note/hero.png)"
    assert expected_path.read_bytes() == b"downloaded:https://example.com/hero.png?from=appmsg"
    assert expected_path.exists()


def test_render_image_markdown_supports_common_remote_src_aliases(tmp_path):
    from scripts import image_assets

    rendered = image_assets.render_image_markdown(
        {
            "src": "https://example.com/hero.png",
            "alt": "Hero Figure",
        },
        vault_root=tmp_path,
        note_title="Image Note",
        download_image=lambda url, destination: destination.write_bytes(url.encode("utf-8")),
    )

    expected_path = tmp_path / "assets" / "Image Note" / "hero.png"
    assert rendered == "![Hero Figure](assets/Image Note/hero.png)"
    assert expected_path.read_bytes() == b"https://example.com/hero.png"


def test_render_image_markdown_supports_data_original_alias(tmp_path):
    from scripts import image_assets

    rendered = image_assets.render_image_markdown(
        {
            "data-original": "https://example.com/cover.png?download=1",
            "alt": "Cover",
        },
        vault_root=tmp_path,
        note_title="Image Note",
        download_image=lambda url, destination: destination.write_bytes(url.encode("utf-8")),
    )

    expected_path = tmp_path / "assets" / "Image Note" / "cover.png"
    assert rendered == "![Cover](assets/Image Note/cover.png)"
    assert expected_path.read_bytes() == b"https://example.com/cover.png?download=1"


def test_render_image_markdown_uses_best_srcset_candidate(tmp_path):
    from scripts import image_assets

    rendered = image_assets.render_image_markdown(
        {
            "srcset": "https://example.com/hero-1x.png 1x, https://example.com/hero-2x.png 2x",
            "alt": "Hero",
        },
        vault_root=tmp_path,
        note_title="Image Note",
        download_image=lambda url, destination: destination.write_bytes(url.encode("utf-8")),
    )

    expected_path = tmp_path / "assets" / "Image Note" / "hero-2x.png"
    assert rendered == "![Hero](assets/Image Note/hero-2x.png)"
    assert expected_path.read_bytes() == b"https://example.com/hero-2x.png"


def test_image_fields_resolve_common_aliases():
    from scripts import image_fields

    assert image_fields.resolve_image_targets(
        {"src": "https://example.com/hero.png", "alt": "Hero"}
    ) == ("", "https://example.com/hero.png", "Hero")
    assert image_fields.resolve_image_targets(
        {"data-original": "https://example.com/cover.png", "alt": "Cover"}
    ) == ("", "https://example.com/cover.png", "Cover")
    assert image_fields.resolve_image_targets(
        {"srcset": "https://example.com/hero-1x.png 1x, https://example.com/hero-2x.png 2x"}
    ) == ("", "https://example.com/hero-2x.png", "hero-2x")
    assert image_fields.resolve_image_targets(
        {"data-lazy-src": "https://example.com/lazy.png", "alt": "Lazy"}
    ) == ("", "https://example.com/lazy.png", "Lazy")
    assert image_fields.resolve_image_targets(
        {"original": "https://example.com/original.png", "alt": "Original"}
    ) == ("", "https://example.com/original.png", "Original")


def test_image_fields_prefers_best_srcset_candidate():
    from scripts import image_fields

    assert image_fields.resolve_image_targets(
        {
            "srcset": (
                "https://example.com/hero-1x.png 1x, "
                "https://example.com/hero-2x.png 2x, "
                "https://example.com/hero-800w.png 800w"
            )
        }
    ) == ("", "https://example.com/hero-800w.png", "hero-800w")


def test_render_image_markdown_falls_back_to_remote_reference_when_download_fails(tmp_path):
    from scripts import image_assets

    def failing_downloader(url: str, destination: Path) -> None:
        raise OSError("network down")

    rendered = image_assets.render_image_markdown(
        {
            "url": "https://example.com/image(1).png",
            "alt": "Remote figure",
        },
        vault_root=tmp_path,
        note_title="Image Note",
        download_image=failing_downloader,
    )

    assert rendered == "![Remote figure](<https://example.com/image(1).png>)"
    assert not (tmp_path / "assets").exists()


def test_render_note_includes_frontmatter_aliases_tags_and_links(tmp_path):
    from scripts import obsidian_note

    draft = {
        "title": "Test\nNote",
        "aliases": ["Alternate Title", "Alt 2"],
        "tags": ["ai", "reading-notes"],
        "source_type": "web",
        "source_url": "https://example.com/article",
        "published": "2024-01-02",
        "created": "2026-03-21",
        "updated": "2026-03-21",
        "importance": "core",
        "status": "processed",
        "summary": "One-line\nsummary.\n",
        "bullets": ["First point\nSecond line", "Second point"],
        "excerpts": [
            "Evidence excerpt line 1.\nEvidence excerpt line 2.",
        ],
        "related_notes": ["Alpha Note", "Beta Note"],
        "embeds": ["Beta Note"],
        "related_links": [
            {"note": "Gamma Note"},
            {"title": "External Ref ] (v1)", "url": "https://example.com/other(path)"},
        ],
    }

    rendered = obsidian_note.render_obsidian_note(draft, vault_root=tmp_path)
    assert rendered.destination_path == tmp_path / "Test Note.md"

    frontmatter = markdown_helpers.load_frontmatter(rendered.content)
    assert frontmatter["title"] == "Test Note"
    assert frontmatter["aliases"] == ["Alternate Title", "Alt 2"]
    assert frontmatter["tags"] == ["ai", "reading-notes"]
    assert frontmatter["source_type"] == "web"
    assert frontmatter["source_url"] == "https://example.com/article"
    assert frontmatter["published"] == "2024-01-02"
    assert frontmatter["created"] == "2026-03-21"
    assert frontmatter["updated"] == "2026-03-21"
    assert frontmatter["importance"] == "core"
    assert frontmatter["status"] == "processed"
    assert re.fullmatch(r"[a-f0-9]{64}", frontmatter["canonical_hash"])

    # Publishable note body structure.
    assert "One-line summary." in rendered.content
    assert "One-line\nsummary." not in rendered.content
    assert "## Key Points" in rendered.content
    assert "- First point" in rendered.content
    assert "- First point Second line" in rendered.content

    # Internal references: wikilinks and embeds.
    assert "[[Alpha Note]]" in rendered.content
    assert "![[Beta Note]]" in rendered.content
    assert "[[Gamma Note]]" in rendered.content
    assert "[External Ref \\] \\(v1\\)](<https://example.com/other(path)>)" in rendered.content
    assert "# Test Note" in rendered.content

    # Evidence block should include a block id for referencing.
    assert re.search(r"\^evidence-[a-f0-9]{8}(?:-\d+)?", rendered.content)
    assert re.search(r"^\^evidence-[a-f0-9]{8}(?:-\d+)?$", rendered.content, flags=re.MULTILINE) is None
    assert re.search(
        r"^> .* \^evidence-[a-f0-9]{8}(?:-\d+)?$",
        rendered.content,
        flags=re.MULTILINE,
    )


def test_render_note_rejects_empty_or_relative_vault_root():
    from scripts import obsidian_note

    with pytest.raises(ValueError):
        obsidian_note.render_obsidian_note({"title": "Test Note"}, vault_root="")

    with pytest.raises(ValueError):
        obsidian_note.render_obsidian_note({"title": "Test Note"}, vault_root="relative/path")


def test_destination_path_sanitizes_title(tmp_path):
    from scripts import obsidian_note

    rendered = obsidian_note.render_obsidian_note(
        {
            "title": 'Bad/Title: "Oops"?',
            "source_type": "web",
            "source_url": "https://example.com/article",
        },
        vault_root=tmp_path,
    )

    # Should remain within the provided vault root and end with .md.
    assert rendered.destination_path.parent == tmp_path
    assert rendered.destination_path.suffix == ".md"
    assert rendered.destination_path.name == "Bad-Title- -Oops-.md"


def test_render_note_preserves_images(tmp_path):
    from scripts import obsidian_note

    source_image = tmp_path / "source" / "local-figure.png"
    source_image.parent.mkdir(parents=True)
    source_image.write_bytes(b"local image bytes")

    def fake_downloader(url: str, destination: Path) -> None:
        destination.write_bytes(f"downloaded:{url}".encode("utf-8"))

    rendered = obsidian_note.render_obsidian_note(
        {
            "title": "Image Note",
            "source_type": "web",
            "source_url": "https://example.com/article",
            "images": [
                {"path": str(source_image), "alt": "Local figure"},
                {"data_src": "https://example.com/image(1).png", "alt": "Remote figure"},
            ],
        },
        vault_root=tmp_path,
        download_image=fake_downloader,
    )

    assert "## Images" in rendered.content
    assert "- ![Local figure](assets/Image Note/local-figure.png)" in rendered.content
    assert "- ![Remote figure](assets/Image Note/image(1).png)" in rendered.content
    assert (tmp_path / "assets" / "Image Note" / "local-figure.png").read_bytes() == b"local image bytes"
    assert (tmp_path / "assets" / "Image Note" / "image(1).png").read_bytes() == b"downloaded:https://example.com/image(1).png"
