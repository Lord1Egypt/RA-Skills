# tests/test_table.py
import json

from jev_webbridge import table

SAMPLE = json.dumps({"url": "https://example.org", "rows": [
    {"idx": 0, "role": "button", "name": "搜索", "value": None, "ops": ["CLICK"]},
    {"idx": 1, "role": "textbox", "name": "query", "value": "", "ops": ["CLICK", "TYPE_TEXT"]},
    {"idx": 2, "role": "combobox", "name": "model", "value": "K3", "ops": ["CLICK", "TYPE_TEXT", "SELECT"]},
]})

def test_parse_table_roundtrip():
    rows = table.parse_table(SAMPLE)
    assert [r["idx"] for r in rows] == [0, 1, 2]
    assert rows[1]["ops"] == ["CLICK", "TYPE_TEXT"]

def test_parse_table_rejects_malformed():
    import pytest
    with pytest.raises(ValueError):
        table.parse_table("not json")
    with pytest.raises(ValueError):
        table.parse_table(json.dumps({"rows": [{"role": "button"}]}))  # missing idx/ops

def test_ops_only_known_enums():
    rows = table.parse_table(SAMPLE)
    allowed = {"CLICK", "TYPE_TEXT", "SELECT", "SCROLL_UP", "SCROLL_DOWN"}
    assert all(set(r["ops"]) <= allowed for r in rows)

def test_table_js_is_one_iife_and_contains_no_site_knowledge():
    js = table.observe_js()
    assert js.strip().startswith("(() =>")
    low = js.lower()
    for banned in ("perplexity", "github", "pplx", ".prose", "data-testid"):
        assert banned not in low, f"site knowledge leaked into TABLE_JS: {banned}"

def test_typeable_targets_never_dropped():
    # Probe finding 2026-09-24: unnamed contenteditable composer was dropped by
    # the name/value filter, losing the primary TYPE_TEXT target.
    assert "if (!name && !value && !typeable) return" in table.TABLE_CORE_JS
    assert "label[for=" in table.TABLE_CORE_JS  # name fallback via associated <label>


def test_core_modules_have_no_site_knowledge():
    # Closes T8 finding: the anti-hardcode lint must cover every core module,
    # with provenance tokens (our own source repo) allowlisted.
    import pathlib
    base = pathlib.Path(table.__file__).parent
    files = ["table.py", "policy.py", "executor.py", "loop.py", "cli.py",
             "predicates/generic.py"]
    banned = ("perplexity", "github.com", "pplx", "div.prose")
    allow = ("perplexity-skill", "perplexity_toolkit")
    for f in files:
        txt = (base / f).read_text().lower()
        for a in allow:
            txt = txt.replace(a, "")
        for b in banned:
            assert b not in txt, f"site knowledge leaked into {f}: {b}"


def test_python_modules_have_no_site_knowledge():
    import pathlib
    src = pathlib.Path(table.__file__).read_text().lower()
    for banned in ("perplexity", "github.com", "pplx"):
        assert banned not in src

def test_core_js_shared_and_composed_into_observe():
    # structural: ordinals can never diverge — OBSERVE_JS is built from TABLE_CORE_JS
    assert table.TABLE_CORE_JS in table.OBSERVE_JS
    assert table.TABLE_CORE_JS in table.TABLE_JS
    assert table.OBSERVE_JS == table.observe_js()
    assert table.OBSERVE_JS.strip().startswith("(() =>")


def test_row_and_element_index_are_one_to_one():
    # Live bug 2026-09-24: resolve() stamped els[ROW_idx] but els includes rows
    # the table skipped (empty name/value/typeable) -> stamp landed on the WRONG
    # element -> every fill/click readback failed ("element not found" / error).
    from jev_webbridge import table
    assert "const rowEls = []" in table.TABLE_CORE_JS  # rows keep their own element list
    assert "rowEls.push(el)" in table.TABLE_CORE_JS
    # stamp happens at include time with the SAME dense ordinal rows.push uses
    assert "el.setAttribute('data-jw-idx', String(rows.length))" in table.TABLE_CORE_JS


def test_stamps_are_refreshed_not_stale():
    # OBSERVE/RESOLVE must drop old data-jw-idx first (re-render/re-observe)
    # and stamp only INCLUDED rows.
    from jev_webbridge import table
    assert "removeAttribute('data-jw-idx')" in table.TABLE_CORE_JS
    assert "setAttribute('data-jw-idx'" in table.TABLE_CORE_JS


def test_resolve_targets_row_element_not_filtered_list():
    from jev_webbridge.executor import RESOLVE_JS
    assert "rowEls[idx]" in RESOLVE_JS
    assert "const el = els[idx];" not in RESOLVE_JS


def test_typeable_mirrors_extension_capability():
    # Live errors 2026-09-24: role=textbox WITHOUT contenteditable was marked
    # TYPE_TEXT, the structural gate passed it, then the extension refused
    # ("not a native input/textarea"). Typeable == native input/textarea/CE only.
    from jev_webbridge import table
    assert "if (el.isContentEditable || el.tagName === 'INPUT' || el.tagName === 'TEXTAREA')" in table.TABLE_CORE_JS
    assert "['textbox','searchbox'].includes(t)\n  return ['CLICK','TYPE_TEXT']" not in table.TABLE_CORE_JS
