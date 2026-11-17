"""Tests for observe engine: filter matching, event construction, helpers."""

from __future__ import annotations

import base64

import pytest

from twist.observe import (
    OBSERVE_BODY_LIMIT,
    Observe,
    ObserveEvent,
    ObserveFilter,
    ObserveOptions,
    _get_post_data_str,
    _parse_headers,
    _parse_response_headers,
    parse_filter,
)


# ===================================================================
# ObserveFilter.match
# ===================================================================


class TestObserveFilterMatch:
    def test_empty_filter_matches_anything(self) -> None:
        f = ObserveFilter()
        assert f.match("https://anything.com/foo", "XHR") is True
        assert f.match("", "") is True

    def test_url_substring_match(self) -> None:
        f = ObserveFilter(urls=["api"])
        assert f.match("https://example.com/api/users", "XHR") is True
        assert f.match("https://example.com/static/app.js", "Script") is False

    def test_url_multiple_values_ored(self) -> None:
        f = ObserveFilter(urls=["api", "graphql"])
        assert f.match("https://example.com/api/x", "XHR") is True
        assert f.match("https://example.com/graphql", "XHR") is True
        assert f.match("https://example.com/other", "XHR") is False

    def test_type_exact_match_case_insensitive(self) -> None:
        f = ObserveFilter(types=["xhr"])
        assert f.match("https://example.com/api", "XHR") is True
        assert f.match("https://example.com/api", "xhr") is True
        assert f.match("https://example.com/api", "Fetch") is False

    def test_type_multiple_values_ored(self) -> None:
        f = ObserveFilter(types=["xhr", "fetch"])
        assert f.match("https://example.com/api", "XHR") is True
        assert f.match("https://example.com/api", "Fetch") is True
        assert f.match("https://example.com/api", "Document") is False

    def test_url_and_type_anded(self) -> None:
        f = ObserveFilter(urls=["api"], types=["xhr"])
        assert f.match("https://example.com/api/users", "XHR") is True
        assert f.match("https://example.com/api/users", "Fetch") is False
        assert f.match("https://example.com/static", "XHR") is False

    def test_url_no_match_skips_type_check(self) -> None:
        f = ObserveFilter(urls=["api"], types=["xhr"])
        assert f.match("https://example.com/static", "XHR") is False

    @property
    def test_is_empty(self) -> None:
        assert ObserveFilter().is_empty is True
        assert ObserveFilter(urls=["a"]).is_empty is False
        assert ObserveFilter(types=["xhr"]).is_empty is False


# ===================================================================
# Observe._should_bypass
# ===================================================================


class TestShouldBypass:
    def test_data_url_bypassed(self) -> None:
        ev = {"request": {"url": "data:text/html,<p>hi</p>"}, "resourceType": "Document"}
        assert Observe._should_bypass(ev) is True

    def test_blob_url_bypassed(self) -> None:
        ev = {"request": {"url": "blob:https://example.com/uuid"}, "resourceType": "XHR"}
        assert Observe._should_bypass(ev) is True

    def test_ftp_bypassed(self) -> None:
        ev = {"request": {"url": "ftp://example.com/file"}, "resourceType": "Other"}
        assert Observe._should_bypass(ev) is True

    def test_websocket_bypassed(self) -> None:
        ev = {"request": {"url": "https://example.com/ws"}, "resourceType": "WebSocket"}
        assert Observe._should_bypass(ev) is True

    def test_http_not_bypassed(self) -> None:
        ev = {"request": {"url": "https://example.com/api"}, "resourceType": "XHR"}
        assert Observe._should_bypass(ev) is False

    def test_http_ip_not_bypassed(self) -> None:
        ev = {"request": {"url": "http://10.0.0.1/api"}, "resourceType": "Fetch"}
        assert Observe._should_bypass(ev) is False


# ===================================================================
# _parse_headers
# ===================================================================


class TestParseHeaders:
    def test_dict_headers(self) -> None:
        result = _parse_headers({"Content-Type": "application/json", "X-Token": "abc"})
        assert result == {"Content-Type": "application/json", "X-Token": "abc"}

    def test_empty_dict(self) -> None:
        assert _parse_headers({}) == {}

    def test_non_string_values_cast(self) -> None:
        result = _parse_headers({"Count": 42})
        assert result == {"Count": "42"}


# ===================================================================
# _parse_response_headers
# ===================================================================


class TestParseResponseHeaders:
    def test_list_headers(self) -> None:
        raw = [
            {"name": "Content-Type", "value": "text/html"},
            {"name": "Server", "value": "nginx"},
        ]
        result = _parse_response_headers(raw)
        assert result == {"Content-Type": "text/html", "Server": "nginx"}

    def test_empty_list(self) -> None:
        assert _parse_response_headers([]) == {}

    def test_skips_empty_name(self) -> None:
        raw = [
            {"name": "", "value": "ignored"},
            {"name": "X-Valid", "value": "ok"},
        ]
        result = _parse_response_headers(raw)
        assert result == {"X-Valid": "ok"}

    def test_non_string_values_cast(self) -> None:
        raw = [{"name": "X-Count", "value": 5}]
        result = _parse_response_headers(raw)
        assert result == {"X-Count": "5"}


# ===================================================================
# _get_post_data_str
# ===================================================================


class TestGetPostDataStr:
    def test_direct_post_data(self) -> None:
        req = {"postData": '{"key":"value"}'}
        assert _get_post_data_str(req) == '{"key":"value"}'

    def test_post_data_entries(self) -> None:
        req = {
            "postDataEntries": [
                {"bytes": base64.b64encode(b"hello").decode()},
                {"bytes": base64.b64encode(b" world").decode()},
            ],
        }
        assert _get_post_data_str(req) == "hello world"

    def test_post_data_entries_invalid_base64(self) -> None:
        req = {"postDataEntries": [{"bytes": "!!invalid!!"}]}
        result = _get_post_data_str(req)
        assert result == "!!invalid!!"

    def test_no_post_data(self) -> None:
        assert _get_post_data_str({}) == ""

    def test_post_data_entries_empty_bytes(self) -> None:
        req = {"postDataEntries": [{"bytes": ""}, {"bytes": base64.b64encode(b"x").decode()}]}
        assert _get_post_data_str(req) == "x"


# ===================================================================
# parse_filter
# ===================================================================


class TestParseFilter:
    def test_empty(self) -> None:
        f = parse_filter([])
        assert f.urls == []
        assert f.types == []
        assert f.is_empty is True

    def test_url_filter(self) -> None:
        f = parse_filter(["url=api"])
        assert f.urls == ["api"]
        assert f.types == []

    def test_type_filter(self) -> None:
        f = parse_filter(["type=xhr"])
        assert f.urls == []
        assert f.types == ["xhr"]

    def test_multiple_values_comma_separated(self) -> None:
        f = parse_filter(["type=xhr,fetch"])
        assert f.types == ["xhr", "fetch"]

    def test_multiple_values_with_spaces(self) -> None:
        f = parse_filter(["type= xhr , fetch "])
        assert f.types == ["xhr", "fetch"]

    def test_multiple_filters_appended(self) -> None:
        f = parse_filter(["url=a", "url=b"])
        assert f.urls == ["a", "b"]

    def test_invalid_format_skipped(self) -> None:
        f = parse_filter(["no_equals_sign"])
        assert f.is_empty is True

    def test_unknown_key_ignored(self) -> None:
        f = parse_filter(["unknown=foo"])
        assert f.is_empty is True

    def test_empty_values_after_strip_ignored(self) -> None:
        f = parse_filter(["url=,,"])
        assert f.urls == []


# ===================================================================
# ObserveEvent.to_json
# ===================================================================


class TestObserveEventToJson:
    def test_request_event(self) -> None:
        ev = ObserveEvent(
            type="request",
            request_id="req-001",
            url="https://example.com/api",
            method="GET",
            resource_type="XHR",
            request_headers={"Authorization": "Bearer token"},
        )
        import json
        d = json.loads(ev.to_json())
        assert d["type"] == "request"
        assert d["requestId"] == "req-001"
        assert d["url"] == "https://example.com/api"
        assert d["method"] == "GET"
        assert d["resourceType"] == "XHR"
        assert d["requestHeaders"] == {"Authorization": "Bearer token"}
        assert "statusCode" not in d

    def test_request_event_with_post_data(self) -> None:
        ev = ObserveEvent(
            type="request",
            request_id="req-002",
            url="https://example.com/api",
            method="POST",
            resource_type="XHR",
            post_data='{"key":"value"}',
        )
        import json
        d = json.loads(ev.to_json())
        assert d["postData"] == '{"key":"value"}'

    def test_response_event(self) -> None:
        ev = ObserveEvent(
            type="response",
            request_id="req-003",
            url="https://example.com/api",
            status_code=200,
            status_text="OK",
            response_headers={"Content-Type": "application/json"},
            body='{"ok":true}',
            body_size=10,
        )
        import json
        d = json.loads(ev.to_json())
        assert d["type"] == "response"
        assert d["statusCode"] == 200
        assert d["statusText"] == "OK"
        assert d["responseHeaders"] == {"Content-Type": "application/json"}
        assert d["body"] == '{"ok":true}'
        assert d["bodySize"] == 10
        assert "bodyTruncated" not in d

    def test_response_event_truncated(self) -> None:
        ev = ObserveEvent(
            type="response",
            request_id="req-004",
            url="https://example.com/large",
            body="x" * OBSERVE_BODY_LIMIT,
            body_truncated=True,
            body_size=10000,
        )
        import json
        d = json.loads(ev.to_json())
        assert d["bodyTruncated"] is True
        assert d["bodySize"] == 10000

    def test_response_event_error(self) -> None:
        ev = ObserveEvent(
            type="response",
            request_id="req-005",
            url="https://example.com/api",
            error_reason="NameNotResolved",
        )
        import json
        d = json.loads(ev.to_json())
        assert d["errorReason"] == "NameNotResolved"
        assert "statusCode" not in d

    def test_minimal_event(self) -> None:
        ev = ObserveEvent(type="request", request_id="req")
        import json
        d = json.loads(ev.to_json())
        assert d == {"type": "request", "requestId": "req"}

    def test_non_ascii_body(self) -> None:
        ev = ObserveEvent(
            type="response",
            request_id="req-006",
            body="中文内容",
        )
        encoded = ev.to_json()
        import json
        d = json.loads(encoded)
        assert d["body"] == "中文内容"
