"""Deep unit tests for intercept engine with mock CDP, edge cases, and HTML manipulation."""

from __future__ import annotations

import asyncio
import base64
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bs4 import BeautifulSoup

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
    Intercept,
    _apply_form_field_mods,
    _apply_json_patch,
    _build_header_entries,
    _clean_resp_headers,
    _decode_response_body,
    _extract_boundary,
    _get_post_data_str,
    _header_get,
    _header_has_key,
    _json_value_to_str,
    _match_body,
    _match_body_json_path,
    _match_cookie,
    _match_query,
    _match_regex,
    _modify_cookie_header,
    _modify_response_cookie,
    _parse_cookie_pairs,
    _parse_cookies,
    _parse_headers,
    _parse_query,
    _remove_cookie_from_header,
    _remove_form_field_value,
    _remove_multipart_field,
    _remove_query_param_value,
    _remove_response_cookie,
    _resolve_json_path,
    _set_form_field_value,
    _set_multipart_field,
    _set_query_param_value,
)


# ===================================================================
# Mock CDP for testing intercept async methods
# ===================================================================


class MockCDP:
    """Minimal mock CDP client for testing Intercept methods."""

    def __init__(self, host: str = "127.0.0.1", port: int = 9222) -> None:
        self.host = host
        self.port = port
        self.continue_request = AsyncMock()
        self.continue_response = AsyncMock()
        self.fulfill_request = AsyncMock()
        self.fail_request = AsyncMock()
        self.get_response_body = AsyncMock()
        self.enable_network = AsyncMock()
        self.enable_fetch = AsyncMock()


# ===================================================================
# _should_bypass tests
# ===================================================================


class TestShouldBypass:
    @pytest.fixture
    def cdp(self) -> MockCDP:
        return MockCDP()

    @pytest.fixture
    def config(self) -> Config:
        return Config(id="t", name="t", rules=[])

    @pytest.fixture
    def intercept(self, cdp: MockCDP, config: Config) -> Intercept:
        return Intercept(cdp, config)  # type: ignore[arg-type]

    def test_data_url_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "data:text/html,<p>hi</p>"}, "resourceType": "Document"}
        assert intercept._should_bypass(ev)

    def test_blob_url_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "blob:https://example.com/uuid"}, "resourceType": "XHR"}
        assert intercept._should_bypass(ev)

    def test_ftp_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "ftp://example.com/file"}, "resourceType": "Other"}
        assert intercept._should_bypass(ev)

    def test_websocket_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "https://example.com/ws"}, "resourceType": "WebSocket"}
        assert intercept._should_bypass(ev)

    def test_options_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "https://example.com/api", "method": "OPTIONS"}, "resourceType": "XHR"}
        assert intercept._should_bypass(ev)

    def test_cdp_self_traffic_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "http://127.0.0.1:9222/json/list"}, "resourceType": "Document"}
        assert intercept._should_bypass(ev)

    def test_cdp_self_path_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "http://127.0.0.1:9222/devtools/page/abc"}, "resourceType": "Other"}
        assert intercept._should_bypass(ev)

    def test_large_body_content_length_bypassed(self, intercept: Intercept) -> None:
        ev = {
            "request": {
                "url": "https://example.com/upload",
                "method": "POST",
                "headers": {"Content-Length": str(6 * 1024 * 1024)},  # 6 MB
            },
            "resourceType": "XHR",
        }
        assert intercept._should_bypass(ev)

    def test_exactly_max_body_size_bypassed(self, intercept: Intercept) -> None:
        ev = {
            "request": {
                "url": "https://example.com/upload",
                "method": "POST",
                "headers": {"Content-Length": str(5 * 1024 * 1024 + 1)},  # > 5MB
            },
            "resourceType": "XHR",
        }
        assert intercept._should_bypass(ev)

    def test_small_body_not_bypassed(self, intercept: Intercept) -> None:
        ev = {
            "request": {
                "url": "https://example.com/api",
                "method": "POST",
                "headers": {"Content-Length": "1024"},
            },
            "resourceType": "XHR",
        }
        assert not intercept._should_bypass(ev)

    def test_normal_get_not_bypassed(self, intercept: Intercept) -> None:
        ev = {"request": {"url": "https://example.com/api"}, "resourceType": "XHR"}
        assert not intercept._should_bypass(ev)

    def test_invalid_content_length_not_bypassed(self, intercept: Intercept) -> None:
        ev = {
            "request": {
                "url": "https://example.com/api",
                "headers": {"Content-Length": "not-a-number"},
            },
            "resourceType": "XHR",
        }
        assert not intercept._should_bypass(ev)

    def test_no_content_length_not_bypassed(self, intercept: Intercept) -> None:
        ev = {
            "request": {
                "url": "https://example.com/api",
                "headers": {},
            },
            "resourceType": "XHR",
        }
        assert not intercept._should_bypass(ev)


# ===================================================================
# _continue tests
# ===================================================================


class TestContinue:
    @pytest.fixture
    def cdp(self) -> MockCDP:
        return MockCDP()

    @pytest.fixture
    def config(self) -> Config:
        return Config(id="t", name="t", rules=[])

    @pytest.fixture
    def intercept(self, cdp: MockCDP, config: Config) -> Intercept:
        return Intercept(cdp, config)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_continue_request(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1"}
        await intercept._continue(ev, "request")
        cdp.continue_request.assert_called_once_with("req-1", headers=None)

    @pytest.mark.asyncio
    async def test_continue_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1"}
        await intercept._continue(ev, "response")
        cdp.continue_response.assert_called_once_with("req-1")

    @pytest.mark.asyncio
    async def test_continue_response_with_headers(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1"}
        headers = [{"name": "Set-Cookie", "value": "a=1"}]
        await intercept._continue(ev, "response", headers=headers)
        cdp.continue_response.assert_called_once_with("req-1", response_headers=headers)


# ===================================================================
# _match_rules edge cases
# ===================================================================


class TestMatchRulesEdgeCases:
    @pytest.fixture
    def config(self) -> Config:
        return Config(
            id="t", name="t",
            rules=[
                Rule(
                    id="r1", name="same-prio-a", priority=5, stage="request",
                    match=Match(all_of=[Condition(type=ConditionType.URL_CONTAINS, value="a")]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r2", name="same-prio-b", priority=5, stage="request",
                    match=Match(all_of=[Condition(type=ConditionType.URL_CONTAINS, value="a")]),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r3", name="empty-match", priority=1, stage="request",
                    match=Match(),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
                Rule(
                    id="r4", name="allof-and-anyof", priority=15, stage="request",
                    match=Match(
                        all_of=[Condition(type=ConditionType.URL_CONTAINS, value="api")],
                        any_of=[
                            Condition(type=ConditionType.METHOD, values=["GET"]),
                            Condition(type=ConditionType.METHOD, values=["POST"]),
                        ],
                    ),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
            ],
        )

    @pytest.fixture
    def intercept(self, config: Config) -> Intercept:
        return Intercept(MockCDP(), config)  # type: ignore[arg-type]

    def test_empty_match_matches_everything(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://x.com/zzz")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r3"

    def test_allof_and_anyof_both_required(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://x.com/api", method="GET")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r4"

    def test_allof_and_anyof_fails_without_anyof(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://x.com/zzz", method="POST")
        rule = intercept._match_rules(ev, "request")
        assert rule is None or rule.id == "r3"

    def test_same_priority_stable(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://x.com/a")
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "r1"

    def test_config_with_no_rules(self) -> None:
        cfg = Config(id="t", name="t", rules=[])
        inter = Intercept(MockCDP(), cfg)  # type: ignore[arg-type]
        from tests.conftest import make_fetch_event
        ev = make_fetch_event()
        assert inter._match_rules(ev, "request") is None


# ===================================================================
# replaceElement / BeautifulSoup tests
# ===================================================================


class TestReplaceElement:
    def test_select_and_replace_div(self) -> None:
        html = "<html><body><div class='main'>old</div></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(".main")
        assert len(elements) == 1
        for el in elements:
            el.clear()
            el.append(BeautifulSoup("<p>new</p>", "html.parser"))
        result = str(soup)
        assert "<p>new</p>" in result
        assert "old" not in result

    def test_select_by_id(self) -> None:
        html = "<html><body><span id='target'>old</span></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select("#target")
        assert len(elements) == 1
        for el in elements:
            el.clear()
            el.append(BeautifulSoup("replaced", "html.parser"))
        assert "replaced" in str(soup)

    def test_select_nonexistent_element(self) -> None:
        html = "<html><body></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(".missing")
        assert len(elements) == 0

    def test_multiple_matches_all_replaced(self) -> None:
        html = "<ul><li class='item'>a</li><li class='item'>b</li></ul>"
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select(".item")
        assert len(elements) == 2
        for el in elements:
            el.clear()
            el.append(BeautifulSoup("X", "html.parser"))
        result = str(soup)
        assert result.count(">X<") == 2
        assert ">a<" not in result
        assert ">b<" not in result

    def test_replace_with_complex_html(self) -> None:
        html = "<html><body><div class='panel'></div></body></html>"
        soup = BeautifulSoup(html, "html.parser")
        replacement = '<section><h1>Title</h1><p>Content</p></section>'
        for el in soup.select(".panel"):
            el.clear()
            el.append(BeautifulSoup(replacement, "html.parser"))
        result = str(soup)
        assert "<h1>Title</h1>" in result
        assert "<p>Content</p>" in result

    def test_css_selector_attribute(self) -> None:
        html = '<form><input name="email" value="old@x.com"></form>'
        soup = BeautifulSoup(html, "html.parser")
        elements = soup.select('input[name="email"]')
        assert len(elements) == 1


# ===================================================================
# JSON Patch edge cases
# ===================================================================


class TestJsonPatchEdgeCases:
    def test_add_to_empty_object(self) -> None:
        result = _apply_json_patch("{}", [JSONPatch(op=JSONPatchOp.ADD, path="/key", value="val")])
        assert json.loads(result) == {"key": "val"}

    def test_add_to_nested_object(self) -> None:
        result = _apply_json_patch('{"a":{}}', [JSONPatch(op=JSONPatchOp.ADD, path="/a/b", value=42)])
        assert json.loads(result) == {"a": {"b": 42}}

    def test_remove_nonexistent(self) -> None:
        with pytest.raises(ValueError):
            _apply_json_patch('{"a":1}', [JSONPatch(op=JSONPatchOp.REMOVE, path="/b")])

    def test_move_within_nested(self) -> None:
        result = _apply_json_patch(
            '{"a": {"b": {"c": 42}}, "d": {}}',
            [JSONPatch(op=JSONPatchOp.MOVE, from_="/a/b/c", path="/d/e")],
        )
        data = json.loads(result)
        assert data["d"]["e"] == 42
        assert "c" not in data.get("a", {}).get("b", {})

    def test_copy_nested(self) -> None:
        result = _apply_json_patch(
            '{"src": {"val": 99}, "dst": {}}',
            [JSONPatch(op=JSONPatchOp.COPY, from_="/src/val", path="/dst/copied")],
        )
        data = json.loads(result)
        assert data["dst"]["copied"] == 99
        assert data["src"]["val"] == 99

    def test_test_on_array(self) -> None:
        result = _apply_json_patch(
            '{"items": [1, 2, 3]}',
            [JSONPatch(op=JSONPatchOp.TEST, path="/items/0", value=1)],
        )
        assert json.loads(result) == {"items": [1, 2, 3]}

    def test_replace_in_array(self) -> None:
        result = _apply_json_patch(
            '{"items": [1, 2, 3]}',
            [JSONPatch(op=JSONPatchOp.REPLACE, path="/items/1", value=99)],
        )
        assert json.loads(result) == {"items": [1, 99, 3]}

    def test_remove_from_array(self) -> None:
        result = _apply_json_patch(
            '{"items": [1, 2, 3]}',
            [JSONPatch(op=JSONPatchOp.REMOVE, path="/items/1")],
        )
        assert json.loads(result) == {"items": [1, 3]}

    def test_multiple_patches(self) -> None:
        patches = [
            JSONPatch(op=JSONPatchOp.ADD, path="/c", value=3),
            JSONPatch(op=JSONPatchOp.REPLACE, path="/a", value=99),
            JSONPatch(op=JSONPatchOp.REMOVE, path="/b"),
        ]
        result = _apply_json_patch('{"a": 1, "b": 2}', patches)
        assert json.loads(result) == {"a": 99, "c": 3}

    def test_nested_array_operations(self) -> None:
        data = '{"users": [{"name": "alice"}, {"name": "bob"}]}'
        result = _apply_json_patch(
            data,
            [JSONPatch(op=JSONPatchOp.REPLACE, path="/users/0/name", value="ALICE")],
        )
        assert json.loads(result) == {"users": [{"name": "ALICE"}, {"name": "bob"}]}

    def test_patch_order_matters(self) -> None:
        patches = [
            JSONPatch(op=JSONPatchOp.ADD, path="/a", value=1),
            JSONPatch(op=JSONPatchOp.TEST, path="/a", value=1),
            JSONPatch(op=JSONPatchOp.REPLACE, path="/a", value=2),
        ]
        result = _apply_json_patch("{}", patches)
        assert json.loads(result) == {"a": 2}


# ===================================================================
# _json_value_to_str
# ===================================================================


class TestJsonValueToStr:
    def test_bool_true(self) -> None:
        assert _json_value_to_str(True) == "true"

    def test_bool_false(self) -> None:
        assert _json_value_to_str(False) == "false"

    def test_null(self) -> None:
        assert _json_value_to_str(None) == "null"

    def test_int(self) -> None:
        assert _json_value_to_str(42) == "42"

    def test_float(self) -> None:
        assert _json_value_to_str(3.14) == "3.14"

    def test_string(self) -> None:
        assert _json_value_to_str("hello") == "hello"


# ===================================================================
# Multipart edge cases
# ===================================================================


class TestMultipartEdgeCases:
    def test_set_field_with_multiple_parts(self) -> None:
        body = (
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="a"\r\n'
            b"\r\n"
            b"1\r\n"
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="b"\r\n'
            b"\r\n"
            b"2\r\n"
            b"--boundary--\r\n"
        )
        result = _set_multipart_field(body, "boundary", "a", "99")
        decoded = result.decode()
        assert "99" in decoded
        assert 'name="b"' in decoded

    def test_remove_first_field(self) -> None:
        body = (
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="a"\r\n'
            b"\r\n"
            b"1\r\n"
            b"--boundary\r\n"
            b'Content-Disposition: form-data; name="b"\r\n'
            b"\r\n"
            b"2\r\n"
            b"--boundary--\r\n"
        )
        result = _remove_multipart_field(body, "boundary", "a")
        decoded = result.decode()
        assert 'name="a"' not in decoded
        assert 'name="b"' in decoded

    def test_extract_boundary_with_spaces(self) -> None:
        assert _extract_boundary("multipart/form-data; boundary = myboundary") == "myboundary"

    def test_extract_boundary_with_charset(self) -> None:
        assert _extract_boundary("multipart/form-data; charset=utf-8; boundary=abc") == "abc"


# ===================================================================
# Post data edge cases
# ===================================================================


class TestPostDataEdgeCases:
    def test_mixed_entries_base64_and_plain(self) -> None:
        req = {
            "hasPostData": True,
            "postDataEntries": [
                {"bytes": base64.b64encode(b"hello").decode()},
                {"bytes": "plain"},
            ],
        }
        result = _get_post_data_str(req)
        assert "hello" in result

    def test_deprecated_post_data_fallback(self) -> None:
        req = {"postData": "old-style-data"}
        assert _get_post_data_str(req) == "old-style-data"

    def test_has_post_data_false(self) -> None:
        req = {"hasPostData": False, "postDataEntries": [{"bytes": "x"}]}
        assert _get_post_data_str(req) == ""


# ===================================================================
# Query parsing edge cases
# ===================================================================


class TestQueryParsingEdgeCases:
    def test_multiple_values_same_key(self) -> None:
        q = _parse_query("https://x.com?a=1&a=2")
        assert q["a"] == "2"

    def test_empty_value(self) -> None:
        q = _parse_query("https://x.com?flag")
        assert q == {"flag": ""}

    def test_special_chars(self) -> None:
        q = _parse_query("https://x.com?q=hello%20world")
        assert q["q"] == "hello world"

    def test_hash_in_value(self) -> None:
        q = _parse_query("https://x.com?url=http%3A%2F%2Fa.com%2Fb%23c")
        assert "url" in q


# ===================================================================
# Cookie matching edge cases
# ===================================================================


class TestCookieMatchingEdgeCases:
    def test_cookie_regex_no_match(self) -> None:
        c = Condition(type=ConditionType.COOKIE_REGEX, name="token", pattern=r"^\d{3}$")
        assert not _match_cookie(c, {"token": "abc"})

    def test_cookie_contains_case_sensitive(self) -> None:
        c = Condition(type=ConditionType.COOKIE_CONTAINS, name="token", value="AB")
        assert not _match_cookie(c, {"token": "abc"})

    def test_cookie_not_exists_on_empty(self) -> None:
        c = Condition(type=ConditionType.COOKIE_NOT_EXISTS, name="any")
        assert _match_cookie(c, {})

    def test_cookie_with_spaces(self) -> None:
        cookies = _parse_cookies({"Cookie": " a = 1 ; b = 2 "})
        assert cookies.get("a") == "1"
        assert cookies.get("b") == "2"


# ===================================================================
# Header edge cases
# ===================================================================


class TestHeaderEdgeCases:
    def test_build_entries_preserves_other_headers(self) -> None:
        hdrs = {"Content-Type": "json", "Cookie": "a=1"}
        entries = _build_header_entries(hdrs, "Cookie", "a=99; b=2")
        names = [e["name"] for e in entries]
        assert "Content-Type" in names
        assert "Cookie" in names

    def test_build_entries_adds_cookie_when_missing(self) -> None:
        hdrs = {"Content-Type": "json"}
        entries = _build_header_entries(hdrs, "Cookie", "new=1")
        cookie_entries = [e for e in entries if e["name"] == "Cookie"]
        assert len(cookie_entries) == 1
        assert cookie_entries[0]["value"] == "new=1"

    def test_build_entries_removes_cookie_when_empty(self) -> None:
        hdrs = {"Content-Type": "json", "Cookie": "a=1"}
        entries = _build_header_entries(hdrs, "Cookie", "")
        cookie_entries = [e for e in entries if e["name"] == "Cookie"]
        assert len(cookie_entries) == 0


# ===================================================================
# Worker pool edge cases
# ===================================================================


class TestWorkerPool:
    def test_worker_count_minimum(self) -> None:
        cfg = Config(id="t", name="t", rules=[])
        inter = Intercept(MockCDP(), cfg)  # type: ignore[arg-type]
        assert inter._worker_count >= 4

    @pytest.mark.asyncio
    async def test_worker_handles_event(self) -> None:
        cfg = Config(id="t", name="t", rules=[
            Rule(
                id="r1", name="block", priority=10, stage="request",
                match=Match(all_of=[Condition(type=ConditionType.URL_CONTAINS, value="test")]),
                actions=[Action(type=ActionType.BLOCK)],
            ),
        ])
        cdp = MockCDP()
        inter = Intercept(cdp, cfg)  # type: ignore[arg-type]
        ev = {"requestId": "req-1", "request": {"url": "https://x.com/test", "headers": {}}, "resourceType": "XHR"}
        await inter._process(ev)
        cdp.fulfill_request.assert_called_once()
        args, kwargs = cdp.fulfill_request.call_args
        assert args[0] == "req-1"


# ===================================================================
# Response cookie modify/remove edge cases
# ===================================================================


class TestResponseCookieEdgeCases:
    def test_modify_case_insensitive_cookie_name(self) -> None:
        headers = [{"name": "Set-Cookie", "value": "SESSION=old; Path=/"}]
        result = _modify_response_cookie(headers, "session", "new")
        values = [h["value"] for h in result if h["name"] == "Set-Cookie"]
        assert any("session=new" in v or "SESSION=new" in v for v in values)

    def test_remove_case_insensitive_cookie_name(self) -> None:
        headers = [
            {"name": "Set-Cookie", "value": "SESSION=abc"},
            {"name": "Set-Cookie", "value": "token=xyz"},
        ]
        result = _remove_response_cookie(headers, "session")
        values = [h["value"] for h in result if h["name"] == "Set-Cookie"]
        assert len(values) == 1
        assert "token=xyz" in values

    def test_modify_when_no_set_cookie_header(self) -> None:
        headers = [{"name": "Content-Type", "value": "text/html"}]
        result = _modify_response_cookie(headers, "new", "val")
        set_cookie = [h for h in result if h["name"] == "Set-Cookie"]
        assert len(set_cookie) == 1
        assert set_cookie[0]["value"] == "new=val"

    def test_remove_when_no_set_cookie_header(self) -> None:
        headers = [{"name": "Content-Type", "value": "text/html"}]
        result = _remove_response_cookie(headers, "session")
        assert len(result) == 1


# ===================================================================
# Form field edge cases
# ===================================================================


class TestFormFieldEdgeCases:
    def test_set_form_field_preserves_other_fields(self) -> None:
        result = _set_form_field_value(b"a=1&b=2", "c", "3")
        decoded = result.decode()
        assert "a=1" in decoded
        assert "b=2" in decoded
        assert "c=3" in decoded

    def test_remove_form_field_preserves_others(self) -> None:
        result = _remove_form_field_value(b"a=1&b=2&c=3", "b")
        decoded = result.decode()
        assert "a=1" in decoded
        assert "b=2" not in decoded
        assert "c=3" in decoded

    def test_set_form_field_encoded_value(self) -> None:
        result = _set_form_field_value(b"a=1", "q", "hello world")
        decoded = result.decode()
        assert "hello+world" in decoded or "hello%20world" in decoded


# ===================================================================
# Decode response body edge cases
# ===================================================================


class TestDecodeResponseBodyEdgeCases:
    def test_invalid_base64_falls_back(self) -> None:
        result = _decode_response_body({"body": "!!!not-base64!!!", "base64Encoded": True})
        assert "not-base64" in result

    def test_empty_body(self) -> None:
        assert _decode_response_body({"body": ""}) == ""


# ===================================================================
# Match body edge cases
# ===================================================================


class TestMatchBodyEdgeCases:
    def test_body_json_path_with_array(self) -> None:
        body = '{"data": [{"id": 1}, {"id": 2}]}'
        assert _match_body_json_path(body, "/data/1/id", "2")

    def test_body_json_path_deep_nesting(self) -> None:
        body = '{"a": {"b": {"c": {"d": "deep"}}}}'
        assert _match_body_json_path(body, "/a/b/c/d", "deep")

    def test_body_json_path_type_mismatch(self) -> None:
        body = '{"count": 42}'
        assert _match_body_json_path(body, "/count", "42")
        assert not _match_body_json_path(body, "/count", "43")

    def test_body_regex_multiline(self) -> None:
        c = Condition(type=ConditionType.BODY_REGEX, pattern=r'(?s)hello.*world')
        assert _match_body(c, "hello\nbeautiful\nworld")

    def test_body_contains_empty(self) -> None:
        c = Condition(type=ConditionType.BODY_CONTAINS, value="x")
        assert not _match_body(c, "")


# ===================================================================
# URL query param edge cases
# ===================================================================


class TestURLQueryParamEdgeCases:
    def test_set_on_url_with_fragment(self) -> None:
        url = "https://x.com/page#section"
        result = _set_query_param_value(url, "a", "1")
        assert "a=1" in result
        assert "#section" in result

    def test_remove_on_url_with_fragment(self) -> None:
        url = "https://x.com/page?a=1#section"
        result = _remove_query_param_value(url, "a")
        assert "a=1" not in result
        assert "#section" in result

    def test_set_encoded_value(self) -> None:
        url = "https://x.com"
        result = _set_query_param_value(url, "q", "hello world")
        assert "hello+world" in result or "hello%20world" in result


# ===================================================================
# Rule matching — combined allOf + anyOf edge cases
# ===================================================================


class TestRuleMatchingCombinedLogic:
    @pytest.fixture
    def config(self) -> Config:
        return Config(
            id="t", name="t",
            rules=[
                Rule(
                    id="combined", name="combined", priority=10, stage="request",
                    match=Match(
                        all_of=[
                            Condition(type=ConditionType.URL_CONTAINS, value="api"),
                            Condition(type=ConditionType.METHOD, values=["POST", "PUT"]),
                        ],
                        any_of=[
                            Condition(type=ConditionType.HEADER_EXISTS, name="X-Auth"),
                            Condition(type=ConditionType.QUERY_EXISTS, name="token"),
                        ],
                    ),
                    actions=[Action(type=ActionType.BLOCK)],
                ),
            ],
        )

    @pytest.fixture
    def intercept(self, config: Config) -> Intercept:
        return Intercept(MockCDP(), config)  # type: ignore[arg-type]

    def test_all_match(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(
            url="https://x.com/api/v1",
            method="POST",
            headers={"X-Auth": "token123"},
        )
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "combined"

    def test_missing_anyof_fails(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(url="https://x.com/api/v1", method="POST")
        rule = intercept._match_rules(ev, "request")
        assert rule is None

    def test_missing_allof_fails(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(
            url="https://other.com",
            method="POST",
            headers={"X-Auth": "token123"},
        )
        rule = intercept._match_rules(ev, "request")
        assert rule is None

    def test_query_anyof_works(self, intercept: Intercept) -> None:
        from tests.conftest import make_fetch_event
        ev = make_fetch_event(
            url="https://x.com/api/v1?token=abc",
            method="PUT",
        )
        rule = intercept._match_rules(ev, "request")
        assert rule is not None
        assert rule.id == "combined"


# ===================================================================
# Action dispatch tests with mock CDP
# ===================================================================


class TestActionDispatch:
    @pytest.fixture
    def cdp(self) -> MockCDP:
        cdp = MockCDP()
        cdp.get_response_body.return_value = {"body": '{"ok":true}', "base64Encoded": False}
        return cdp

    @pytest.fixture
    def config(self) -> Config:
        return Config(id="t", name="t", rules=[])

    @pytest.fixture
    def intercept(self, cdp: MockCDP, config: Config) -> Intercept:
        return Intercept(cdp, config)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_block_action(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.BLOCK, statusCode=418)])
        await intercept._execute_actions(ev, rule, "request")
        cdp.fulfill_request.assert_called_once()
        call_args = cdp.fulfill_request.call_args
        assert call_args[0][0] == "req-1"
        assert call_args[0][1] == 418

    @pytest.mark.asyncio
    async def test_set_header_action(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.SET_HEADER, name="X-Custom", value="val")])
        await intercept._execute_actions(ev, rule, "request")
        cdp.continue_request.assert_called_once()
        call_kwargs = cdp.continue_request.call_args[1]
        assert call_kwargs["headers"] == [{"name": "X-Custom", "value": "val"}]

    @pytest.mark.asyncio
    async def test_set_url_action(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.SET_URL, value="https://new.com")])
        await intercept._execute_actions(ev, rule, "request")
        cdp.continue_request.assert_called_once()
        assert cdp.continue_request.call_args[1]["url"] == "https://new.com"

    @pytest.mark.asyncio
    async def test_set_method_action(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.SET_METHOD, value="PATCH")])
        await intercept._execute_actions(ev, rule, "request")
        cdp.continue_request.assert_called_once()
        assert cdp.continue_request.call_args[1]["method"] == "PATCH"

    @pytest.mark.asyncio
    async def test_set_body_request(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.SET_BODY, value='{"new":1}')])
        await intercept._execute_actions(ev, rule, "request")
        cdp.continue_request.assert_called_once()
        kwargs = cdp.continue_request.call_args[1]
        assert kwargs["post_data"] == '{"new":1}'
        assert any(h["name"] == "Content-Type" for h in (kwargs.get("headers") or []))

    @pytest.mark.asyncio
    async def test_set_body_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "responseStatusCode": 200, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="response",
                    match=Match(), actions=[Action(type=ActionType.SET_BODY, value="mocked")])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()

    @pytest.mark.asyncio
    async def test_append_body_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        cdp.get_response_body.return_value = {"body": "hello", "base64Encoded": False}
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "responseStatusCode": 200, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="response",
                    match=Match(), actions=[Action(type=ActionType.APPEND_BODY, value=" world")])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()
        body_arg = cdp.fulfill_request.call_args[1]["body"]
        assert body_arg == "hello world"

    @pytest.mark.asyncio
    async def test_replace_body_text_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        cdp.get_response_body.return_value = {"body": "hello user", "base64Encoded": False}
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "responseStatusCode": 200, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="response",
                    match=Match(), actions=[Action(type=ActionType.REPLACE_BODY_TEXT, search="user", replace="admin")])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()
        body_arg = cdp.fulfill_request.call_args[1]["body"]
        assert body_arg == "hello admin"

    @pytest.mark.asyncio
    async def test_patch_body_json_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        cdp.get_response_body.return_value = {"body": '{"a":1,"b":2}', "base64Encoded": False}
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "responseStatusCode": 200, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="response",
                    match=Match(),
                    actions=[Action(type=ActionType.PATCH_BODY_JSON, patches=[
                        JSONPatch(op=JSONPatchOp.REPLACE, path="/a", value=99),
                        JSONPatch(op=JSONPatchOp.REMOVE, path="/b"),
                    ])])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()
        body_arg = cdp.fulfill_request.call_args[1]["body"]
        data = json.loads(body_arg)
        assert data["a"] == 99
        assert "b" not in data

    @pytest.mark.asyncio
    async def test_replace_element_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        cdp.get_response_body.return_value = {
            "body": "<html><body><div class='main'>old</div></body></html>",
            "base64Encoded": False,
        }
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "responseStatusCode": 200, "resourceType": "Document"}
        rule = Rule(id="r", name="r", stage="response",
                    match=Match(),
                    actions=[Action(type=ActionType.REPLACE_ELEMENT, selector=".main", value="<p>new</p>")])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()
        body = cdp.fulfill_request.call_args[1]["body"]
        assert "<p>new</p>" in body
        assert "old" not in body

    @pytest.mark.asyncio
    async def test_set_status_response(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "responseStatusCode": 200, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="response",
                    match=Match(), actions=[Action(type=ActionType.SET_STATUS, status_code=503)])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()
        assert cdp.fulfill_request.call_args[0][1] == 503

    @pytest.mark.asyncio
    async def test_set_status_ignored_on_request(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.SET_STATUS, status_code=500)])
        await intercept._execute_actions(ev, rule, "request")
        cdp.fulfill_request.assert_not_called()

    @pytest.mark.asyncio
    async def test_unknown_action_passes_through(self, intercept: Intercept, cdp: MockCDP) -> None:
        ev = {"requestId": "req-1", "request": {"url": "x", "headers": {}}, "resourceType": "XHR"}
        rule = Rule(id="r", name="r", stage="request",
                    match=Match(), actions=[Action(type=ActionType.BLOCK)])
        await intercept._execute_actions(ev, rule, "request")
        cdp.fulfill_request.assert_called_once()


# ===================================================================
# BUG FIX #1: _apply_form_field_mods with urlencoded string body
# ===================================================================


class TestApplyFormFieldModsUrlEncodedBugFix:
    def test_set_field_modifies_urlencoded_body(self) -> None:
        result = _apply_form_field_mods(
            "a=1&b=2", "application/x-www-form-urlencoded",
            {"c": "3"}, set(), MagicMock(),
        )
        assert "a=1" in result
        assert "b=2" in result
        assert "c=3" in result

    def test_remove_field_modifies_urlencoded_body(self) -> None:
        result = _apply_form_field_mods(
            "a=1&b=2&c=3", "application/x-www-form-urlencoded",
            {}, {"b"}, MagicMock(),
        )
        assert "a=1" in result
        assert "b=2" not in result
        assert "b=" not in result
        assert "c=3" in result

    def test_set_and_remove_together(self) -> None:
        result = _apply_form_field_mods(
            "a=1&b=2", "application/x-www-form-urlencoded",
            {"a": "new"}, {"b"}, MagicMock(),
        )
        assert "a=new" in result
        assert "b=" not in result

    def test_no_content_type_defaults_to_urlencoded(self) -> None:
        result = _apply_form_field_mods(
            "x=1", "", {"y": "2"}, set(), MagicMock(),
        )
        assert "x=1" in result
        assert "y=2" in result


# ===================================================================
# BUG FIX #2+#3: Response header cleaning in no-modifications path
# ===================================================================


class TestApplyResponseHeaderCleaningBugFix:
    @pytest.fixture
    def cdp(self) -> MockCDP:
        cdp = MockCDP()
        cdp.get_response_body.return_value = {"body": "hello", "base64Encoded": False}
        return cdp

    @pytest.fixture
    def config(self) -> Config:
        return Config(id="t", name="t", rules=[])

    @pytest.fixture
    def intercept(self, cdp: MockCDP, config: Config) -> Intercept:
        return Intercept(cdp, config)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_no_mods_does_not_strip_content_encoding(
        self, intercept: Intercept, cdp: MockCDP,
    ) -> None:
        ev = {
            "requestId": "req-1",
            "request": {"url": "x", "headers": {}},
            "responseStatusCode": 200,
            "responseHeaders": [
                {"name": "Content-Encoding", "value": "gzip"},
                {"name": "Content-Type", "value": "text/html"},
            ],
            "resourceType": "Document",
        }
        rule = Rule(id="r", name="r", stage="response", match=Match(), actions=[])
        await intercept._execute_actions(ev, rule, "response")
        cdp.continue_response.assert_called_once()
        cdp.fulfill_request.assert_not_called()

    @pytest.mark.asyncio
    async def test_cookie_only_mod_preserves_content_encoding(
        self, intercept: Intercept, cdp: MockCDP,
    ) -> None:
        ev = {
            "requestId": "req-1",
            "request": {"url": "x", "headers": {}},
            "responseStatusCode": 200,
            "responseHeaders": [
                {"name": "Content-Encoding", "value": "gzip"},
                {"name": "Content-Type", "value": "text/html"},
            ],
            "resourceType": "Document",
        }
        rule = Rule(id="r", name="r", stage="response", match=Match(), actions=[
            Action(type=ActionType.SET_COOKIE, name="session", value="abc"),
        ])
        await intercept._execute_actions(ev, rule, "response")
        cdp.continue_response.assert_called_once()
        call_kwargs = cdp.continue_response.call_args[1]
        headers = call_kwargs.get("response_headers") or []
        names_lower = [h["name"].lower() for h in headers]
        assert "content-encoding" in names_lower

    @pytest.mark.asyncio
    async def test_body_mod_strips_content_encoding(
        self, intercept: Intercept, cdp: MockCDP,
    ) -> None:
        ev = {
            "requestId": "req-1",
            "request": {"url": "x", "headers": {}},
            "responseStatusCode": 200,
            "responseHeaders": [
                {"name": "Content-Encoding", "value": "gzip"},
                {"name": "Content-Type", "value": "text/html"},
            ],
            "resourceType": "Document",
        }
        rule = Rule(id="r", name="r", stage="response", match=Match(), actions=[
            Action(type=ActionType.SET_BODY, value="modified"),
        ])
        await intercept._execute_actions(ev, rule, "response")
        cdp.fulfill_request.assert_called_once()
        call_kwargs = cdp.fulfill_request.call_args[1]
        headers = call_kwargs.get("response_headers") or []
        names_lower = [h["name"].lower() for h in headers]
        assert "content-encoding" not in names_lower


# ===================================================================
# BUG FIX #4: setHeader case-insensitive dedup
# ===================================================================


class TestSetHeaderCaseInsensitive:
    @pytest.fixture
    def cdp(self) -> MockCDP:
        return MockCDP()

    @pytest.fixture
    def config(self) -> Config:
        return Config(id="t", name="t", rules=[])

    @pytest.fixture
    def intercept(self, cdp: MockCDP, config: Config) -> Intercept:
        return Intercept(cdp, config)  # type: ignore[arg-type]

    @pytest.mark.asyncio
    async def test_set_header_replaces_case_insensitive(
        self, intercept: Intercept, cdp: MockCDP,
    ) -> None:
        ev = {
            "requestId": "req-1",
            "request": {"url": "x", "headers": {"Content-Type": "application/json"}},
            "resourceType": "XHR",
        }
        rule = Rule(id="r", name="r", stage="request", match=Match(), actions=[
            Action(type=ActionType.SET_HEADER, name="content-type", value="text/plain"),
        ])
        await intercept._execute_actions(ev, rule, "request")
        cdp.continue_request.assert_called_once()
        headers = cdp.continue_request.call_args[1].get("headers") or []
        ct_headers = [h for h in headers if h["name"].lower() == "content-type"]
        assert len(ct_headers) == 1
        assert ct_headers[0]["value"] == "text/plain"

    @pytest.mark.asyncio
    async def test_remove_header_is_case_insensitive(
        self, intercept: Intercept, cdp: MockCDP,
    ) -> None:
        ev = {
            "requestId": "req-1",
            "request": {"url": "x", "headers": {"Content-Type": "application/json"}},
            "resourceType": "XHR",
        }
        rule = Rule(id="r", name="r", stage="request", match=Match(), actions=[
            Action(type=ActionType.REMOVE_HEADER, name="content-type"),
        ])
        await intercept._execute_actions(ev, rule, "request")
        cdp.continue_request.assert_called_once()
        headers = cdp.continue_request.call_args[1].get("headers") or []
        ct_headers = [h for h in headers if h["name"].lower() == "content-type"]
        assert len(ct_headers) == 0
