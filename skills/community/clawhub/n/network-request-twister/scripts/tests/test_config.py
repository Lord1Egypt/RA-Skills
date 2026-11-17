"""Tests for config parsing, validation, and Pydantic models."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from twist.config import (
    Action,
    ActionType,
    Condition,
    ConditionType,
    Config,
    JSONPatch,
    JSONPatchOp,
    Match,
    Rule,
    load_config,
)


class TestLoadConfig:
    def test_load_valid_config(self, sample_config_json: bytes) -> None:
        cfg = load_config(sample_config_json)
        assert cfg.id == "test-001"
        assert cfg.name == "test config"
        assert len(cfg.rules) == 1
        assert cfg.rules[0].id == "rule-001"

    def test_load_from_str(self) -> None:
        cfg = load_config('{"id":"x","name":"x","version":"1","rules":[]}')
        assert cfg.id == "x"

    def test_load_invalid_json_raises(self) -> None:
        with pytest.raises(ValidationError):
            load_config(b"not json")


class TestCondition:
    def test_url_equals(self) -> None:
        c = Condition(type=ConditionType.URL_EQUALS, value="https://x.com")
        assert c.value == "https://x.com"

    def test_url_equals_requires_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Condition(type=ConditionType.URL_EQUALS)

    def test_url_regex_requires_pattern(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'pattern'"):
            Condition(type=ConditionType.URL_REGEX)

    def test_method_requires_values(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'values'"):
            Condition(type=ConditionType.METHOD)

    def test_method_valid(self) -> None:
        c = Condition(type=ConditionType.METHOD, values=["GET", "POST"])
        assert c.values == ["GET", "POST"]

    def test_header_exists_requires_name(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'name'"):
            Condition(type=ConditionType.HEADER_EXISTS)

    def test_header_exists_valid(self) -> None:
        c = Condition(type=ConditionType.HEADER_EXISTS, name="Authorization")
        assert c.name == "Authorization"

    def test_header_equals_requires_name_and_value(self) -> None:
        with pytest.raises(ValidationError):
            Condition(type=ConditionType.HEADER_EQUALS, value="bar")
        with pytest.raises(ValidationError):
            Condition(type=ConditionType.HEADER_EQUALS, name="foo")

    def test_header_equals_valid(self) -> None:
        c = Condition(type=ConditionType.HEADER_EQUALS, name="X-Token", value="secret")
        assert c.name == "X-Token"

    def test_header_regex_requires_name_and_pattern(self) -> None:
        with pytest.raises(ValidationError):
            Condition(type=ConditionType.HEADER_REGEX, pattern=".*")
        with pytest.raises(ValidationError):
            Condition(type=ConditionType.HEADER_REGEX, name="X")

    def test_body_json_path_requires_path_and_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'path'"):
            Condition(type=ConditionType.BODY_JSON_PATH, value="x")
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Condition(type=ConditionType.BODY_JSON_PATH, path="/foo")

    def test_body_json_path_valid(self) -> None:
        c = Condition(type=ConditionType.BODY_JSON_PATH, path="/ok", value="true")
        assert c.path == "/ok"

    def test_all_condition_types(self) -> None:
        for ct in ConditionType:
            if ct in (ConditionType.URL_EQUALS, ConditionType.URL_CONTAINS):
                Condition(type=ct, value="x")
            elif ct == ConditionType.URL_REGEX:
                Condition(type=ct, pattern=".*")
            elif ct in (ConditionType.METHOD, ConditionType.RESOURCE_TYPE):
                Condition(type=ct, values=["GET"])
            elif ct in (
                ConditionType.HEADER_EXISTS,
                ConditionType.QUERY_EXISTS,
                ConditionType.COOKIE_EXISTS,
            ):
                Condition(type=ct, name="foo")
            elif ct in (
                ConditionType.HEADER_EQUALS,
                ConditionType.QUERY_EQUALS,
                ConditionType.COOKIE_EQUALS,
            ):
                Condition(type=ct, name="k", value="v")
            elif ct in (
                ConditionType.HEADER_REGEX,
                ConditionType.QUERY_REGEX,
            ):
                Condition(type=ct, name="k", pattern=".*")
            elif ct == ConditionType.BODY_CONTAINS:
                Condition(type=ct, value="x")
            elif ct == ConditionType.BODY_REGEX:
                Condition(type=ct, pattern=".*")


class TestAction:
    def test_block_defaults(self) -> None:
        a = Action(type=ActionType.BLOCK)
        assert a.status_code == 200
        assert a.body_encoding == "text"

    def test_block_custom_status(self) -> None:
        a = Action(type=ActionType.BLOCK, statusCode=404)
        assert a.status_code == 404

    def test_set_body_default_encoding(self) -> None:
        a = Action(type=ActionType.SET_BODY, value="hello")
        assert a.encoding == "text"

    def test_set_url_requires_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Action(type=ActionType.SET_URL)

    def test_set_header_requires_name_and_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'name'"):
            Action(type=ActionType.SET_HEADER, value="v")
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Action(type=ActionType.SET_HEADER, name="X")

    def test_set_header_valid(self) -> None:
        a = Action(type=ActionType.SET_HEADER, name="X-Token", value="abc")
        assert a.name == "X-Token"

    def test_remove_header_requires_name(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'name'"):
            Action(type=ActionType.REMOVE_HEADER)

    def test_set_query_param_requires_name_and_value(self) -> None:
        with pytest.raises(ValidationError):
            Action(type=ActionType.SET_QUERY_PARAM, value="v")
        with pytest.raises(ValidationError):
            Action(type=ActionType.SET_QUERY_PARAM, name="p")

    def test_set_status_requires_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'statusCode'"):
            Action(type=ActionType.SET_STATUS)

    def test_set_body_requires_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Action(type=ActionType.SET_BODY)

    def test_append_body_requires_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Action(type=ActionType.APPEND_BODY)

    def test_replace_body_text_requires_search_and_replace(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'search'"):
            Action(type=ActionType.REPLACE_BODY_TEXT, replace="r")
        with pytest.raises(ValidationError, match="requires field 'replace'"):
            Action(type=ActionType.REPLACE_BODY_TEXT, search="s")

    def test_patch_body_json_requires_patches(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'patches'"):
            Action(type=ActionType.PATCH_BODY_JSON)

    def test_replace_element_requires_selector_and_value(self) -> None:
        with pytest.raises(ValidationError, match="requires field 'selector'"):
            Action(type=ActionType.REPLACE_ELEMENT, value="x")
        with pytest.raises(ValidationError, match="requires field 'value'"):
            Action(type=ActionType.REPLACE_ELEMENT, selector="div")

    def test_replace_element_valid(self) -> None:
        a = Action(type=ActionType.REPLACE_ELEMENT, selector=".main", value="<p>ok</p>")
        assert a.selector == ".main"

    def test_alias_fields(self) -> None:
        a = Action.model_validate({
            "type": "block",
            "statusCode": 418,
            "bodyEncoding": "base64",
        })
        assert a.status_code == 418
        assert a.body_encoding == "base64"


class TestRule:
    def test_minimal_rule(self) -> None:
        r = Rule.model_validate({
            "id": "r1",
            "name": "test",
            "stage": "request",
            "match": {"allOf": [{"type": "urlEquals", "value": "https://x.com"}]},
            "actions": [{"type": "block"}],
        })
        assert r.id == "r1"
        assert r.enabled is True
        assert r.priority == 0

    def test_disabled_rule(self) -> None:
        r = Rule.model_validate({
            "id": "r1",
            "name": "test",
            "enabled": False,
            "stage": "response",
            "match": {"allOf": [{"type": "urlContains", "value": "api"}]},
            "actions": [{"type": "setStatus", "statusCode": 500}],
        })
        assert r.enabled is False
        assert r.stage == "response"


class TestConfig:
    def test_full_config_roundtrip(self, sample_config_json: bytes) -> None:
        cfg = load_config(sample_config_json)
        assert cfg.rules[0].match.all_of[0].type == ConditionType.URL_CONTAINS
        assert cfg.rules[0].match.all_of[0].value == "analytics"
        assert cfg.rules[0].actions[0].type == ActionType.BLOCK
        assert cfg.rules[0].actions[0].status_code == 204

    def test_empty_rules(self) -> None:
        cfg = load_config(
            b'{"id":"c","name":"c","version":"1","rules":[]}'
        )
        assert cfg.rules == []

    def test_description_and_settings_optional(self) -> None:
        cfg = load_config(json.dumps({
            "id": "c", "name": "c", "version": "2",
            "description": "test config",
            "settings": {"timeout": 30},
            "rules": [],
        }))
        assert cfg.description == "test config"
        assert cfg.settings == {"timeout": 30}

    def test_invalid_rule_fails(self) -> None:
        data = json.dumps({
            "id": "c", "name": "c",
            "rules": [{
                "id": "r1", "name": "r1",
                "stage": "request",
                "match": {"allOf": [{"type": "urlEquals"}]},
                "actions": [{"type": "block"}],
            }],
        })
        with pytest.raises(ValidationError):
            load_config(data)


class TestJSONPatch:
    def test_add_operation(self) -> None:
        p = JSONPatch(op=JSONPatchOp.ADD, path="/foo", value="bar")
        assert p.op == JSONPatchOp.ADD

    def test_bare_op_validation(self) -> None:
        with pytest.raises(ValidationError):
            JSONPatch(op="invalid", path="/x")


class TestMatch:
    def test_all_of_only(self) -> None:
        m = Match(all_of=[
            Condition(type=ConditionType.URL_CONTAINS, value="api"),
        ])
        assert len(m.all_of) == 1
        assert len(m.any_of) == 0

    def test_any_of_only(self) -> None:
        m = Match(any_of=[
            Condition(type=ConditionType.METHOD, values=["GET"]),
        ])
        assert len(m.any_of) == 1

    def test_alias_mapping(self) -> None:
        m = Match.model_validate({
            "allOf": [{"type": "urlEquals", "value": "https://x.com"}],
            "anyOf": [{"type": "method", "values": ["POST"]}],
        })
        assert len(m.all_of) == 1
        assert len(m.any_of) == 1
