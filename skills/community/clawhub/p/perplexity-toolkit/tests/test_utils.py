"""Tests for perplexity_toolkit.utils DOM lookup helpers."""

import pytest

from perplexity_toolkit.utils import (
    compact_json,
    find_textbox,
    find_menuitem,
    find_ref_by_role,
    _find_by_role,
    _load_tree,
)

# Sample compact JSON accessibility trees — normal field order and reordered.
TEXTBOX_NORMAL = {
    "role": "textbox", "name": "Ask anything", "value": "", "ref": "@e42",
}
TEXTBOX_REORDERED = {
    "ref": "@e42", "value": "", "name": "Ask anything", "role": "textbox",
}
MENUITEM_NORMAL = {"role": "menuitem", "name": "深度研究", "ref": "@e77"}
MENUITEM_REORDERED = {"ref": "@e77", "role": "menuitem", "name": "深度研究"}


def _tree(*nodes):
    """Nest nodes under a root dict to exercise recursive descent."""
    return {"root": {"children": list(nodes)}}


def _tree_json(*nodes):
    return compact_json(_tree(*nodes))


class TestFindTextbox:
    def test_normal_field_order(self):
        assert find_textbox(_tree_json(TEXTBOX_NORMAL)) == "@e42"

    def test_reordered_fields(self):
        assert find_textbox(_tree_json(TEXTBOX_REORDERED)) == "@e42"

    def test_nested_in_children(self):
        tree = {"a": {"b": [TEXTBOX_NORMAL]}}
        assert find_textbox(compact_json(tree)) == "@e42"

    def test_no_textbox_returns_none(self):
        assert find_textbox(_tree_json(MENUITEM_NORMAL)) is None

    def test_first_match_wins(self):
        tree = [TEXTBOX_NORMAL, {**TEXTBOX_NORMAL, "ref": "@e99"}]
        assert find_textbox(compact_json(tree)) == "@e42"


class TestFindMenuitem:
    def test_partial_text_match(self):
        assert find_menuitem(_tree_json(MENUITEM_NORMAL), "深度") == "@e77"

    def test_reordered_fields(self):
        assert find_menuitem(_tree_json(MENUITEM_REORDERED), "深度") == "@e77"

    def test_no_match_returns_none(self):
        assert find_menuitem(_tree_json(MENUITEM_NORMAL), "不存在的项") is None
        assert find_menuitem(_tree_json(TEXTBOX_NORMAL), "深度") is None


class TestFindRefByRole:
    def test_role_only(self):
        assert find_ref_by_role(_tree_json(TEXTBOX_NORMAL), "textbox") == "@e42"

    def test_role_with_name_pattern(self):
        assert find_ref_by_role(_tree_json(TEXTBOX_NORMAL), "textbox", "Ask") == "@e42"

    def test_name_pattern_no_match(self):
        assert find_ref_by_role(_tree_json(TEXTBOX_NORMAL), "textbox", "zzz") is None


class TestFindByRoleDirect:
    def test_on_dict_and_list_and_scalar(self):
        assert _find_by_role(TEXTBOX_NORMAL, "textbox") == "@e42"
        assert _find_by_role([TEXTBOX_NORMAL, MENUITEM_NORMAL], "menuitem") == "@e77"
        assert _find_by_role("just a string", "textbox") is None
        assert _find_by_role(None, "textbox") is None

    def test_name_contains(self):
        assert _find_by_role(MENUITEM_NORMAL, "menuitem", "研究") == "@e77"
        assert _find_by_role(MENUITEM_NORMAL, "menuitem", "zzz") is None


class TestCompactJson:
    def test_no_spaces(self):
        s = compact_json(TEXTBOX_NORMAL)
        assert "Ask anything" in s


class TestLoadTree:
    def test_valid_json_string(self):
        tree = _load_tree(compact_json(TEXTBOX_NORMAL))
        assert tree == TEXTBOX_NORMAL

    def test_dict_passthrough_is_identity(self):
        assert _load_tree(TEXTBOX_NORMAL) is TEXTBOX_NORMAL

    def test_list_passthrough_is_identity(self):
        lst = [TEXTBOX_NORMAL]
        assert _load_tree(lst) is lst

    def test_valid_json_list(self):
        assert _load_tree('[{"role":"textbox"}]') == [{"role": "textbox"}]

    @pytest.mark.parametrize("bad", ["", "not json", "{"])
    def test_invalid_json_returns_none(self, bad):
        assert _load_tree(bad) is None

    def test_non_string_non_container_passthrough(self):
        assert _load_tree(42) == 42


class TestRegexFallback:
    """The old order-dependent regex paths run only when JSON parsing fails."""

    def test_textbox_fallback(self):
        s = 'not-json "role":"textbox","name":"Ask anything","value":"","ref":"@e42"'
        assert find_textbox(s) == "@e42"

    def test_textbox_fallback_without_value_field(self):
        s = 'garbage "role":"textbox","name":"Ask anything","ref":"@e42"'
        assert find_textbox(s) == "@e42"

    def test_menuitem_fallback(self):
        s = 'garbage "role":"menuitem","name":"深度研究","ref":"@e77"'
        assert find_menuitem(s, "深度") == "@e77"

    def test_regex_fallback_fails_on_reordered_fields(self):
        """Regex is order-dependent; reordered fields break it."""
        s = 'garbage "ref":"@e42","name":"Ask anything","role":"textbox"'
        assert find_textbox(s) is None

    def test_no_match_fallback(self):
        assert find_menuitem("garbage", "深度") is None
        assert find_textbox("garbage") is None
