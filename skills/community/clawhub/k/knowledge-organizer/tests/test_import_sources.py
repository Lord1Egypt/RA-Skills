from pathlib import Path


def test_detect_source_type_wechat_xiaohongshu_and_web():
    from scripts.import_sources import detect_source_type

    assert (
        detect_source_type("https://mp.weixin.qq.com/s/some-article") == "wechat_article"
    )
    assert detect_source_type("mp.weixin.qq.com/s/some-article") == "wechat_article"
    assert (
        detect_source_type("https://www.xiaohongshu.com/explore/abc")
        == "xiaohongshu_note"
    )
    assert detect_source_type("xhslink.com/xyz") == "xiaohongshu_note"
    assert detect_source_type("https://xhslink.com/xyz") == "xiaohongshu_note"
    assert detect_source_type("https://example.com/post") == "web"


def test_load_markdown_file_sets_source_path_and_title(tmp_path: Path):
    from scripts.import_sources import load_markdown_file

    md_path = tmp_path / "note.md"
    md_path.write_text("# Hello World\n\nBody\n", encoding="utf-8")

    draft = load_markdown_file(md_path)

    assert draft.title == "Hello World"
    assert draft.source_type == "markdown"
    assert draft.source_url == ""
    assert "Body" in draft.content
    assert draft.source_id


def test_folder_scan_matches_single_file_import(tmp_path: Path):
    from scripts.import_sources import load_folder, load_markdown_file

    md_path = tmp_path / "note.md"
    md_path.write_text("# Title\n\nBody\n", encoding="utf-8")

    direct = load_markdown_file(md_path).to_mapping()
    scanned = load_folder(tmp_path)

    assert len(scanned) == 1
    assert scanned[0].to_mapping() == direct


def test_folder_scan_skips_unreadable_markdown(tmp_path: Path):
    from scripts.import_sources import load_folder

    good = tmp_path / "good.md"
    good.write_text("# Good\n\nBody\n", encoding="utf-8")
    bad = tmp_path / "bad.md"
    bad.write_bytes(b"\xff\xfe\x00not utf-8")

    scanned = load_folder(tmp_path)

    assert len(scanned) == 1
    assert scanned[0].title == "Good"
