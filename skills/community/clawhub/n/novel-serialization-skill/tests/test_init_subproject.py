"""Tests for scripts/init_subproject.py — the subproject scaffold.

The scaffold is consumed by hand afterwards, so the contract that matters is:
every promised file appears, nothing is written in dry-run, an existing tree is
never overwritten silently, and the generated files are LF and UTF-8.
"""

from __future__ import annotations

import init_subproject as init


def test_build_creates_expected_files(tmp_path):
    root = tmp_path / "novel"
    log = init.build(root, "烟雨长安", "../scripts", "someone", force=False, dry=False)
    files = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}

    assert log, "build reports what it wrote"
    for expected in (
        "README.md",
        "SYNOPSIS.md",
        "CHANGELOG.md",
        "progress.md",
        "SUPPORT.md",
        "SECURITY.md",
        "notes-personal/裁决项台账.md",
        ".gitignore",
        ".gitattributes",
        ".editorconfig",
        ".github/CODEOWNERS",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/PULL_REQUEST_TEMPLATE.md",
    ):
        assert expected in files, expected


def test_dry_run_writes_nothing(tmp_path):
    root = tmp_path / "novel"
    log = init.build(root, "烟雨长安", "../scripts", "someone", force=False, dry=True)
    assert log, "dry-run still reports the plan"
    assert not root.exists() or not any(root.rglob("*")), "dry-run must not write"


def test_existing_file_is_not_overwritten_without_force(tmp_path):
    root = tmp_path / "novel"
    root.mkdir()
    (root / "README.md").write_bytes(b"mine\n")
    init.build(root, "烟雨长安", "../scripts", "someone", force=False, dry=False)
    assert (root / "README.md").read_bytes() == b"mine\n"
    init.build(root, "烟雨长安", "../scripts", "someone", force=True, dry=False)
    assert (root / "README.md").read_bytes() != b"mine\n"


def test_generated_files_are_lf_and_utf8(tmp_path):
    root = tmp_path / "novel"
    init.build(root, "烟雨长安", "../scripts", "someone", force=False, dry=False)
    for p in root.rglob("*"):
        if p.is_file():
            raw = p.read_bytes()
            assert b"\r\n" not in raw, f"CRLF in {p}"
            raw.decode("utf-8")  # raises if the write was not UTF-8


def test_main_smoke(tmp_path, capsys):
    assert init.main(["--name", "烟雨长安", "--root", str(tmp_path / "n")]) == 0
    assert "item(s)" in capsys.readouterr().out
