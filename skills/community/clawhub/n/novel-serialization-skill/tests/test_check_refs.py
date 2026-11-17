"""Tests for scripts/check_refs.py — the release-only reference rule.

The rule under test: a file inside the release tree may only reference files
that are also inside the release tree. Files outside it (drafts, personal
notes, the workspace area) may reference anything. Everything else here is
mechanics: how links and backtick paths resolve, and how odd encodings behave.
"""

from __future__ import annotations

import check_refs as cr


def _targets(findings, bucket):
    return {(f["file"], f["target"]) for f in findings[bucket]}


def test_release_link_to_release_is_ok(tree):
    tree("a.md", "see [b](b.md)\n")
    tree("b.md", "b\n")
    f = cr.scan(tree.root)
    assert ("a.md", "b.md") in _targets(f, "OK")


def test_release_link_into_private_area_is_nonrelease(tree):
    tree("a.md", "see [note](notes-personal/x.md)\n")
    tree("notes-personal/x.md", "x\n")
    f = cr.scan(tree.root)
    assert ("a.md", "notes-personal/x.md") in _targets(f, "NONRELEASE")


def test_private_file_may_reference_private_area(tree):
    # A report or working note may point into another private area; only files
    # inside the release tree are held to the release-only rule.
    tree("notes-personal/a.md", "see [x](../_trash/x.md)\n")
    tree("_trash/x.md", "x\n")
    f = cr.scan(tree.root)
    assert ("notes-personal/a.md", "../_trash/x.md") in _targets(f, "PRIVATE_OK")
    assert not f["NONRELEASE"]


def test_missing_target(tree):
    tree("a.md", "see [gone](gone.md)\n")
    f = cr.scan(tree.root)
    assert ("a.md", "gone.md") in _targets(f, "MISSING")


def test_link_resolves_relative_to_source_not_root(tree):
    tree("sub/a.md", "see [b](b.md)\n")
    tree("sub/b.md", "b\n")
    f = cr.scan(tree.root)
    assert ("sub/a.md", "b.md") in _targets(f, "OK")


def test_root_absolute_link_resolves_from_repo_root(tree):
    tree("sub/a.md", "see [b](/top.md)\n")
    tree("top.md", "top\n")
    f = cr.scan(tree.root)
    assert ("sub/a.md", "/top.md") in _targets(f, "OK")
    assert not f["MISSING"]


def test_url_encoded_link_is_decoded(tree):
    # GitHub decodes %20 in link targets; the checker must do the same or every
    # path with a space in it is reported as missing.
    tree("a.md", "see [seed](README%20FOR%20AI.md)\n")
    tree("README FOR AI.md", "seed\n")
    f = cr.scan(tree.root)
    assert ("a.md", "README%20FOR%20AI.md") in _targets(f, "OK")
    assert not f["MISSING"]


def test_backtick_path_resolves_from_root(tree):
    tree("sub/a.md", "edit `sub/b.md`\n")
    tree("sub/b.md", "b\n")
    f = cr.scan(tree.root)
    assert ("sub/a.md", "sub/b.md") in _targets(f, "BARE")


def test_template_paths_are_not_reported_missing(tree):
    tree("a.md", "see [sheet](角色名.md) and `tools/xxx.py`\n")
    f = cr.scan(tree.root)
    assert f["TEMPLATE"]
    assert not f["MISSING"]


def test_external_and_anchor_links_are_ignored(tree):
    tree("a.md", "[site](https://example.com) [here](#section) [mail](mailto:a@b.c)\n")
    f = cr.scan(tree.root)
    assert not f["MISSING"]
    assert not f["OK"]


def test_ignore_pattern_suppresses_matches(tree):
    tree("a.md", "see [x](state/timeline.md)\n")
    import re

    assert cr.scan(tree.root)["MISSING"]
    assert not cr.scan(tree.root, re.compile(r"^state/"))["MISSING"]


def test_ignore_file_suppresses_matches(tree):
    # The exemption list must live in a file the local run, pre-commit and CI
    # all read, so that the three cannot disagree.
    tree(".refsignore", "# comment\n\n^state/\n")
    tree("a.md", "see [x](state/timeline.md)\n")
    assert not cr.scan(tree.root, cr.build_ignore(tree.root, [], ".refsignore"))["MISSING"]
    assert cr.scan(tree.root)["MISSING"]
    assert cr.scan(tree.root, cr.build_ignore(tree.root, [], ""))["MISSING"], \
        "an empty --ignore-file disables the exemption"


def test_missing_from_a_release_file_is_gated(tree):
    tree("a.md", "see [gone](gone.md)\n")
    f = cr.scan(tree.root)
    assert f["MISSING"] and not f["PRIVATE_MISSING"]
    assert cr.main(["--root", str(tree.root), "--fail-on", "MISSING"]) == 1


def test_missing_from_a_report_is_not_gated(tree):
    tree("notes-personal/r.md", "see [timeline](../worldbuilding/时间线.md)\n")
    f = cr.scan(tree.root)
    assert f["PRIVATE_MISSING"] and not f["MISSING"]
    assert cr.main(["--root", str(tree.root), "--fail-on", "MISSING"]) == 0


def test_ignore_file_patterns_are_valid(tree):
    # The patterns are written by hand; a typo must fail loudly, not silently
    # disable every exemption.
    tree(".refsignore", "^state/(\n")
    try:
        cr.build_ignore(tree.root, [], ".refsignore")
    except SystemExit:
        pass
    else:
        raise AssertionError("a malformed pattern should raise")


def test_main_fail_on_returns_one(tree):
    tree("a.md", "see [note](notes-personal/x.md)\n")
    tree("notes-personal/x.md", "x\n")
    assert cr.main(["--root", str(tree.root), "--fail-on", "NONRELEASE"]) == 1
    assert cr.main(["--root", str(tree.root), "--fail-on", "MISSING"]) == 0


def test_main_json_is_parseable(tree, capsys):
    tree("a.md", "see [b](b.md)\n")
    tree("b.md", "b\n")
    assert cr.main(["--root", str(tree.root), "--json"]) == 0
    import json

    out = capsys.readouterr().out
    data = json.loads(out)
    assert set(data) == set(cr.SEVERITY_ORDER)
