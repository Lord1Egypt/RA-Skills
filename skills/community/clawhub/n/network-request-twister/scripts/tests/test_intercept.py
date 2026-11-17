"""Tests for intercept engine: rule matching, helper functions, and JSON patch."""

from __future__ import annotations

import base64
import json

import pytest

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
)
from twist.intercept import (
    _apply_json_patch,
    _decode_response_body,
    _extract_boundary,
    _get_post_data_str,
    _header_get,
    _header_has_key,
    _match_body,
    _match_body_json_path,
    _match_cookie,
    _match_query,
    _match_regex,
    _modify_cookie_header,
    _modify_response_cookie,
    _parse_cookies,
    _parse_headers,
    _parse_query,
    _remove_cookie_from_header,
    _remove_form_field_value,
    _remove_query_param_value,
    _remove_response_cookie,
    _resolve_json_path,
    _set_form_field_value,
    _set_multipart_field,
    _set_query_param_value,
    Intercept,
)


# ===================================================================
# Regex
# ===================================================================


class TestMatchRegex:
    def test_basic_match(self) -> None:
        assert _match_regex(r"^https://", "https://example.com")

    def test_no_match(self) -> None:
        assert not _match_regex(r"^https://", "http://example.com")

    def test_empty_pattern(self) -> None:
        assert not _match_regex("", "foo")

    def test_invalid_regex(self) -> None:
        assert not _match_regex("[", "foo")


# ===================================================================
# Headers
# ===================================================================


class TestParseHeaders:
    def test_dict_headers(self) -> None:
        hdrs = _parse_headers({"Content-Type": "application/json"})
        assert hdrs["Content-Type"] == "application/json"

    def test_empty(self) -> None:
        assert _parse_headers({}) == {}


class TestHeaderHelpers:
    def test_has_key(self) -> None:
        hdrs = {"Content-Type": "json"}
        assert _header_has_key(hdrs, "content-type")
        assert not _header_has_key(hdrs, "x-missing")

    def test_get_case_insensitive(self) -> None:
        hdrs = {"Content-Type": "application/json"}
        assert _header_get(hdrs, "content-type") == "application/json"
        assert _header_get(hdrs, "X-Missing") == ""


# ===================================================================
# Cookies
# ===================================================================


class TestParseCookies:
    def test_basic(self) -> None:
        hdrs = {"Cookie": "session=abc; token=xyz"}
        cookies = _parse_cookies(hdrs)
        assert cookies == {"session": "abc", "token": "xyz"}

    def test_single(self) -> None:
        hdrs = {"Cookie": "a=1"}
        assert _parse_cookies(hdrs) == {"a": "1"}

    def test_empty(self) -> None:
        assert _parse_cookies({}) == {}
        assert _parse_cookies({"Cookie": ""}) == {}

    def test_no_value(self) -> None:
        hdrs = {"Cookie": "flag"}
        assert _parse_cookies(hdrs) == {"flag": ""}


class TestMatchCookie:
    def test_exists(self) -> None:
        c = Condition(type=ConditionType.COOKIE_EXISTS, name="session")
        assert _match_cookie(c, {"session": "abc"})

    def test_not_exists(self) -> None:
        c = Condition(type=ConditionType.COOKIE_NOT_EXISTS, name="missing")
        assert _match_cookie(c, {"session": "abc"})

    def test_equals(self) -> None:
        c = Condition(type=ConditionType.COOKIE_EQUALS, name="session", value="abc")
        assert _match_cookie(c, {"session": "abc"})
        assert not _match_cookie(c, {"session": "xyz"})

    def test_contains(self) -> None:
        c = Condition(type=ConditionType.COOKIE_CONTAINS, name="token", value="ab")
        assert _match_cookie(c, {"token": "abc"})

    def test_regex(self) -> None:
        c = Condition(type=ConditionType.COOKIE_REGEX, name="token", pattern=r"^\d+$")
        assert _match_cookie(c, {"token": "12345"})
        assert not _match_cookie(c, {"token": "abc"})


# ===================================================================
# Query parameters
# ===================================================================


class TestParseQuery:
    def test_basic(self) -> None:
        q = _parse_query("https://x.com?a=1&b=2")
        assert q == {"a": "1", "b": "2"}

    def test_no_query(self) -> None:
        assert _parse_query("https://x.com") == {}

    def test_encoded(self) -> None:
        q = _parse_query("https://x.com?name=%E4%B8%AD%E6%96%87")
        assert q == {"name": "中文"}

    def test_fragment(self) -> None:
        q = _parse_query("https://x.com?a=1#section")
        assert q == {"a": "1"}


class TestMatchQuery:
    def test_exists(self) -> None:
        c = Condition(type=ConditionType.QUERY_EXISTS, name="page")
        assert _match_query(c, {"page": "1"})

    def test_not_exists(self) -> None:
        c = Condition(type=ConditionType.QUERY_NOT_EXISTS, name="missing")
        assert _match_query(c, {"page": "1"})

    def test_equals(self) -> None:
        c = Condition(type=ConditionType.QUERY_EQUALS, name="page", value="1")
        assert _match_query(c, {"page": "1"})

    def test_contains(self) -> None:
        c = Condition(type=ConditionType.QUERY_CONTAINS, name="q", value="twist")
        assert _match_query(c, {"q": "twist tool"})

    def test_regex(self) -> None:
        c = Condition(type=ConditionType.QUERY_REGEX, name="id", pattern=r"^\d+$")
        assert _match_query(c, {"id": "42"})


# ===================================================================
# Query param manipulation
# ===================================================================


class TestSetQueryParam:
    def test_add_param(self) -> None:
        url = "https://example.com/api"
        assert "foo=bar" in _set_query_param_value(url, "foo", "bar")

    def test_replace_param(self) -> None:
        url = "https://example.com/api?foo=old"
        result = _set_query_param_value(url, "foo", "new")
        assert "foo=new" in result
        assert "foo=old" not in result


class TestRemoveQueryParam:
    def test_remove_existing(self) -> None:
        url = "https://example.com/api?foo=bar&baz=1"
        result = _remove_query_param_value(url, "foo")
        assert "foo" not in result
        assert "baz=1" in result

    def test_remove_nonexistent(self) -> None:
        url = "https://example.com/api"
        assert _remove_query_param_value(url, "foo") == url


# ===================================================================
# Post data
# ===================================================================


class TestGetPostData:
    def test_direct_post_data(self) -> None:
        req = {"postData": "hello"}
        assert _get_post_data_str(req) == "hello"

    def test_post_data_entries(self) -> None:
        req = {
            "hasPostData": True,
            "postDataEntries": [
                {"bytes": base64.b64encode(b"world").decode()},
            ],
        }
        assert _get_post_data_str(req) == "world"

    def test_no_post_data(self) -> None:
        assert _get_post_data_str({}) == ""

    def test_has_post_data_no_entries(self) -> None:
        assert _get_post_data_str({"hasPostData": True, "postDataEntries": []}) == ""


# ===================================================================
# Body matching
# ===================================================================


class TestMatchBody:
    def test_contains(self) -> None:
        c = Condition(type=ConditionType.BODY_CONTAINS, value="hello")
        assert _match_body(c, "hello world")
        assert not _match_body(c, "goodbye")

    def test_regex(self) -> None:
        c = Condition(type=ConditionType.BODY_REGEX, pattern=r'"ok":\s*true')
        assert _match_body(c, '{"ok": true}')
        assert not _match_body(c, '{"ok": false}')

    def test_json_path(self) -> None:
        c = Condition(type=ConditionType.BODY_JSON_PATH, path="/user/name", value="alice")
        assert _match_body(c, '{"user": {"name": "alice"}}')

    def test_empty_body(self) -> None:
        c = Condition(type=ConditionType.BODY_CONTAINS, value="x")
        assert not _match_body(c, "")


class TestMatchBodyJsonPath:
    def test_simple_key(self) -> None:
        assert _match_body_json_path('{"ok": true}', "/ok", "true")

    def test_nested(self) -> None:
        body = '{"data": {"items": [{"id": 1}, {"id": 2}]}}'
        assert _match_body_json_path(body, "/data/items/0/id", "1")

    def test_not_found(self) -> None:
        assert not _match_body_json_path('{"x": 1}', "/y", "1")

    def test_invalid_json(self) -> None:
        assert not _match_body_json_path("not json", "/x", "1")


class TestResolveJsonPath:
    def test_root(self) -> None:
        assert _resolve_json_path({"a": 1}, "") == {"a": 1}

    def test_nested(self) -> None:
        data = {"a": {"b": {"c": 42}}}
        assert _resolve_json_path(data, "/a/b/c") == 42

    def test_array(self) -> None:
        data = {"items": [10, 20, 30]}
        assert _resolve_json_path(data, "/items/1") == 20


# ===================================================================
# Form field manipulation
# ===================================================================


class TestFormField:
    def test_set_value(self) -> None:
        result = _set_form_field_value(b"a=1&b=2", "a", "99")
        decoded = result.decode()
        assert "a=99" in decoded

    def test_remove_value(self) -> None:
        result = _remove_form_field_value(b"a=1&b=2", "a")
        decoded = result.decode()
        assert "a=1" not in decoded
        assert "b=2" in decoded

    def test_add_new_field(self) -> None:
        result = _set_form_field_value(b"a=1", "c", "3")
        decoded = result.decode()
        assert "c=3" in decoded


class TestExtractBoundary:
    def test_standard(self) -> None:
        assert _extract_boundary("multipart/form-data; boundary=abc123") == "abc123"

    def test_quoted(self) -> None:
        assert _extract_boundary('multipart/form-data; boundary="abc def"') == "abc def"

    def test_no_boundary(self) -> None:
        assert _extract_boundary("application/json") == ""


class TestMultipartField:
    def test_set_field(self) -> None:
        body = (
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="foo"\r\n'
            b"\r\n"
            b"old\r\n"
            b"--boundary--\r\n"
        )
        result = _set_multipart_field(body, "boundary", "foo", "new")
        decoded = result.decode()
        assert "new" in decoded
        assert "old" not in decoded

    def test_remove_field(self) -> None:
        from twist.intercept import _remove_multipart_field
        body = (
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="foo"\r\n'
            b"\r\n"
            b"value\r\n"
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="bar"\r\n'
            b"\r\n"
            b"keep\r\n"
            b"--boundary--\r\n"
        )
        result = _remove_multipart_field(body, "boundary", "foo")
        decoded = result.decode()
        assert "foo" not in decoded
        assert "keep" in decoded


# ===================================================================
# Cookie header manipulation
# ===================================================================


class TestModifyCookieHeader:
    def test_set_existing(self) -> None:
        hdrs = {"Cookie": "a=1; b=2"}
        result = _modify_cookie_header(hdrs, "a", "99")
        cookie_hdr = next(h["value"] for h in result if h["name"] == "Cookie")
        assert "a=99" in cookie_hdr
        assert "b=2" in cookie_hdr

    def test_set_new(self) -> None:
        hdrs = {"Cookie": "a=1"}
        result = _modify_cookie_header(hdrs, "b", "2")
        cookie_hdr = next(h["value"] for h in result if h["name"] == "Cookie")
        assert "b=2" in cookie_hdr

    def test_remove_existing(self) -> None:
        hdrs = {"Cookie": "a=1; b=2"}
        result = _remove_cookie_from_header(hdrs, "a")
        cookie_hdr = next((h["value"] for h in result if h["name"] == "Cookie"), "")
        assert "a=1" not in cookie_hdr
        assert "b=2" in cookie_hdr

    def test_remove_only(self) -> None:
        hdrs = {"Cookie": "a=1"}
        result = _remove_cookie_from_header(hdrs, "a")
        cookie_hdrs = [h for h in result if h["name"] == "Cookie"]
        assert not cookie_hdrs or cookie_hdrs[0]["value"] == ""


# ===================================================================
# Response cookie manipulation
# ===================================================================


class TestResponseCookie:
    def test_modify_existing(self) -> None:
        resp_headers = [
            {"name": "Set-Cookie", "value": "session=old; Path=/"},
        ]
        result = _modify_response_cookie(resp_headers, "session", "new")
        values = [h["value"] for h in result if h["name"] == "Set-Cookie"]
        assert any("session=new" in v for v in values)

    def test_modify_new(self) -> None:
        resp_headers = [
            {"name": "Content-Type", "value": "text/html"},
        ]
        result = _modify_response_cookie(resp_headers, "token", "abc")
        cookie_vals = [h["value"] for h in result if h["name"] == "Set-Cookie"]
        assert any("token=abc" in v for v in cookie_vals)

    def test_remove_existing(self) -> None:
        resp_headers = [
            {"name": "Set-Cookie", "value": "session=abc"},
            {"name": "Set-Cookie", "value": "token=xyz"},
        ]
        result = _remove_response_cookie(resp_headers, "session")
        values = [h["value"] for h in result if h["name"] == "Set-Cookie"]
        assert "session=abc" not in values
        assert "token=xyz" in values


# ===================================================================
# Response body
# ===================================================================


class TestDecodeResponseBody:
    def test_plain_text(self) -> None:
        assert _decode_response_body({"body": "hello"}) == "hello"

    def test_base64(self) -> None:
        encoded = base64.b64encode(b"decoded").decode()
        assert _decode_response_body({"body": encoded, "base64Encoded": True}) == "decoded"


# ===================================================================
# JSON Patch
# ===================================================================


class TestApplyJsonPatch:
    def test_add(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.ADD, path="/new", value="val")]
        result = _apply_json_patch('{"a": 1}', patches)
        data = json.loads(result)
        assert data == {"a": 1, "new": "val"}

    def test_replace(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.REPLACE, path="/a", value=99)]
        result = _apply_json_patch('{"a": 1}', patches)
        assert json.loads(result) == {"a": 99}

    def test_remove(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.REMOVE, path="/a")]
        result = _apply_json_patch('{"a": 1, "b": 2}', patches)
        assert json.loads(result) == {"b": 2}

    def test_move(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.MOVE, from_="/a", path="/b")]
        result = _apply_json_patch('{"a": 1}', patches)
        assert json.loads(result) == {"b": 1}

    def test_copy(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.COPY, from_="/a", path="/b")]
        result = _apply_json_patch('{"a": 1}', patches)
        assert json.loads(result) == {"a": 1, "b": 1}

    def test_test_pass(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.TEST, path="/a", value=1)]
        result = _apply_json_patch('{"a": 1}', patches)
        assert json.loads(result) == {"a": 1}

    def test_test_fail(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.TEST, path="/a", value=2)]
        with pytest.raises(ValueError, match="test failed"):
            _apply_json_patch('{"a": 1}', patches)

    def test_invalid_json(self) -> None:
        with pytest.raises(ValueError, match="not valid JSON"):
            _apply_json_patch("not json", [JSONPatch(op=JSONPatchOp.ADD, path="/x", value=1)])

    def test_nested_path(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.ADD, path="/a/b/c", value=42)]
        result = _apply_json_patch('{"a": {"b": {}}}', patches)
        assert json.loads(result) == {"a": {"b": {"c": 42}}}

    def test_array_index(self) -> None:
        patches = [JSONPatch(op=JSONPatchOp.REPLACE, path="/items/1", value=99)]
        result = _apply_json_patch('{"items": [1, 2, 3]}', patches)
        assert json.loads(result) == {"items": [1, 99, 3]}


# ===================================================================
# Rule matching
# ===================================================================


class TestRuleMatching:
    @pytest.fixture
    def config(self) -> Config:
        return Config(
            id="test",
            name="test",
            rules=[
                Rule(
                    id="r1",
                    name="url-equals",
                    priority=10,
                    stage="request",
                    match=Match(all_of=[
                        Condition(type=ConditionType.URL_EQUALS, value="https://example.com/api"),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r2",
                    name="url-regex",
                    priority=5,
                    stage="request",
                    match=Match(all_of=[
                        Condition(type=ConditionType.URL_REGEX, pattern=r"/api/v\d+/"),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r3",
                    name="method-post",
                    priority=8,
                    stage="request",
                    match=Match(all_of=[
                        Condition(type=ConditionType.METHOD, values=["POST", "PUT"]),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r4",
                    name="any-of",
                    priority=7,
                    stage="request",
                    match=Match(any_of=[
                        Condition(type=ConditionType.URL_CONTAINS, value="analytics"),
                        Condition(type=ConditionType.URL_CONTAINS, value="tracker"),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r5",
                    name="response-only",
                    stage="response",
                    match=Match(all_of=[
                        Condition(type=ConditionType.URL_CONTAINS, value="api"),
                    ]),
                    actions=[Action(type=ActionType.SET_STATUS, status_code=500)],
                ),
                Rule(
                    id="r6",
                    name="disabled",
                    enabled=False,
                    stage="request",
                    match=Match(all_of=[
                        Condition(type=ConditionType.URL_CONTAINS, value="secret"),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r7",
                    name="header-check",
                    priority=9,
                    stage="request",
                    match=Match(all_of=[
                        Condition(type=ConditionType.HEADER_EQUALS, name="X-Token", value="trusted"),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r8",
                    name="resource-type",
                    priority=6,
                    stage="request",
                    match=Match(all_of=[
                        Condition(type=ConditionType.RESOURCE_TYPE, values=["Image"]),
                    ]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
            ],
        )

    @pytest.fixture
    def intercept(self, config: Config) -> Intercept:
        return Intercept(None, config)  # type: ignore[arg-type]

    def test_url_equals_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/api")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r1"

    def test_url_equals_no_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/other")
        rule = intercept._match_rules(ev, "request")
        assert rule is None or rule.id != "r1"

    def test_url_regex_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/api/v2/users")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r2"

    def test_method_post_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/other", method="POST")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r3"

    def test_any_of_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/tracker/event")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r4"

    def test_any_of_no_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/legit")
        rule = intercept._match_rules(ev, "request")
        assert rule is None or rule.id != "r4"

    def test_disabled_rule_skipped(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/secret/data")
        rule = intercept._match_rules(ev, "request")
        assert rule is None or rule.id != "r6"

    def test_response_stage_only(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://example.com/api", response_status=200)
        rule = intercept._match_rules(ev, "response")
        assert rule is not None
        assert rule.id == "r5"

    def test_header_equals_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(
            url="https://example.com/any",
            headers={"X-Token": "trusted"},
        )
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r7"

    def test_resource_type_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(
            url="https://example.com/img.png",
            resource_type="Image",
        )
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r8"

    def test_priority_order(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(
            url="https://example.com/api/v3/data",
            headers={"X-Token": "trusted"},
        )
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r7"


# ===================================================================
# Bypass filter
# ===================================================================


class TestBypassFilter:
    @pytest.fixture
    def config(self) -> Config:
        return Config(id="test", name="test", rules=[])

    class _MockCDP:
        host = "127.0.0.1"
        port = 9222

    def test_non_http_bypassed(self, config: Config) -> None:
        from tests.conftest import make_fetch_event
        inter = Intercept(self._MockCDP(), config)  # type: ignore[arg-type]
        ev = make_fetch_event(url="ftp://example.com")
        assert inter._should_bypass(ev)

    def test_websocket_bypassed(self, config: Config) -> None:
        from tests.conftest import make_fetch_event
        inter = Intercept(self._MockCDP(), config)  # type: ignore[arg-type]
        ev = make_fetch_event(url="https://example.com/ws", resource_type="WebSocket")
        assert inter._should_bypass(ev)

    def test_options_bypassed(self, config: Config) -> None:
        from tests.conftest import make_fetch_event
        inter = Intercept(self._MockCDP(), config)  # type: ignore[arg-type]
        ev = make_fetch_event(url="https://example.com/api", method="OPTIONS")
        assert inter._should_bypass(ev)

    def test_http_passes(self, config: Config) -> None:
        from tests.conftest import make_fetch_event
        inter = Intercept(self._MockCDP(), config)  # type: ignore[arg-type]
        ev = make_fetch_event(url="https://example.com/api", method="GET")
        assert not inter._should_bypass(ev)


# ===================================================================
# URL query param manipulation edge cases
# ===================================================================


class TestSetQueryParamEdgeCases:
    def test_preserve_other_params(self) -> None:
        url = "https://x.com?a=1&b=2"
        result = _set_query_param_value(url, "c", "3")
        assert "a=1" in result
        assert "b=2" in result
        assert "c=3" in result

    def test_empty_value(self) -> None:
        url = "https://x.com"
        result = _set_query_param_value(url, "key", "")
        assert "key=" in result


class TestRemoveQueryParamEdgeCases:
    def test_remove_only_param(self) -> None:
        url = "https://x.com?a=1"
        result = _remove_query_param_value(url, "a")
        assert "a=1" not in result
