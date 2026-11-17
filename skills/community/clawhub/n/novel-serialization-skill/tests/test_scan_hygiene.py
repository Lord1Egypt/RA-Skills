"""Tests for scripts/scan_hygiene.py.

Each check is tested with a file that trips it and a sibling that does not,
so a bug that makes the scanner report everything (or nothing) fails here.
"""

from __future__ import annotations

import scan_hygiene as sh


def test_clean_tree_has_no_findings(tree):
    tree("a.md", "hello\n")
    f = sh.scan(tree.root, 500, set())
    assert not any(f.values())


def test_crlf_detected(tree):
    tree("a.md", "line\r\nline\r\n")
    f = sh.scan(tree.root, 500, set())
    assert [i["file"] for i in f["crlf"]] == ["a.md"]


def test_fix_rewrites_crlf(tree):
    p = tree("a.md", "line\r\nline\r\n")
    f = sh.scan(tree.root, 500, set())
    assert sh.fix_crlf(tree.root, f["crlf"]) == 1
    assert b"\r\n" not in p.read_bytes()


def test_mojibake_detected(tree):
    tree("a.md", "damaged \ufffd text\n")
    f = sh.scan(tree.root, 500, set())
    assert [i["file"] for i in f["mojibake"]] == ["a.md"]


def test_junk_detected_and_skips_content_checks(tree):
    tree("notes.txt.bak", "whatever\r\n")
    f = sh.scan(tree.root, 500, set())
    assert [i["file"] for i in f["junk"]] == ["notes.txt.bak"]
    assert not f["crlf"], "a junk file is reported once, not once per check"


def test_empty_file(tree):
    tree("a.md", "")
    f = sh.scan(tree.root, 500, set())
    assert [i["file"] for i in f["empty"]] == ["a.md"]


def test_missing_trailing_newline(tree):
    tree("a.md", "no newline at end")
    f = sh.scan(tree.root, 500, set())
    assert [i["file"] for i in f["no-eol"]] == ["a.md"]


def test_line_budget_and_allowlist(tree):
    tree("long.md", "x\n" * 20)
    tree("allow.md", "x\n" * 20)
    assert sorted(i["file"] for i in sh.scan(tree.root, 10, set())["lines"]) == ["allow.md", "long.md"]
    assert [i["file"] for i in sh.scan(tree.root, 10, {"allow.md"})["lines"]] == ["long.md"]


def test_binary_suffix_is_not_scanned_for_encoding(tree):
    p = tree("logo.png", "\ufffd")
    p.write_bytes(b"\x00\x01\x02")
    f = sh.scan(tree.root, 500, set())
    assert not f["mojibake"]
    assert not f["empty"]


def test_main_fail_on_exit_codes(tree):
    tree("a.md", "line\r\n")
    assert sh.main(["--root", str(tree.root), "--fail-on", "crlf"]) == 1
    assert sh.main(["--root", str(tree.root), "--fail-on", "mojibake"]) == 0
    assert sh.main(["--root", str(tree.root), "--fix", "--fail-on", "crlf"]) == 0
    assert sh.main(["--root", str(tree.root), "--fail-on", "nonsense"]) == 2
    assert sh.main(["--root", str(tree.root / "missing")]) == 2
