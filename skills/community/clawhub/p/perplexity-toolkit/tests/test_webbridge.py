"""Tests for the WebBridge driver rewrite (T9a: transport injection,
WebBridgeError classification, idempotent evaluate retry, no-swallow-502)."""

import json
from typing import Any

import pytest

from perplexity_toolkit.drivers.webbridge import (
    WebBridgeDriver,
    WebBridgeError,
    _classify_error,
)


# ── Fake transport helpers ────────────────────────────────────────


class TransportRecorder:
    """Records all call payloads and returns canned results."""

    def __init__(self, *canned: dict):
        self.calls: list[tuple[str, dict]] = []
        self._canned = list(canned)

    def __call__(self, url: str, payload: dict) -> dict:
        self.calls.append((url, payload))
        return self._canned.pop(0)


def recording_transport(*canned: dict) -> tuple[TransportRecorder, Any]:
    """Return (recorder, callable) for inject into WebBridgeDriver."""
    rec = TransportRecorder(*canned)
    return rec, rec


def ok_response(data: Any) -> dict:
    return {"data": data}


error_502 = {"error": "HTTP Error 502 from remote: Bad Gateway"}
error_timeout = {"error": "WebBridge request timed out: timed out"}
error_conn = {"error": "WebBridge connection failed — Connection refused"}


# ── Classification unit tests ─────────────────────────────────────


class TestClassifyError:
    def test_502(self):
        assert _classify_error("502 Bad Gateway") == "http_502"

    def test_bad_gateway(self):
        assert _classify_error("HTTP Error 502 from upstream: Bad Gateway") == "http_502"

    def test_timeout(self):
        assert _classify_error("timed out") == "timeout"

    def test_timeout_case_insensitive(self):
        assert _classify_error("Timeout after 30s") == "timeout"

    def test_connect_refused(self):
        assert _classify_error("Connection refused") == "connect"

    def test_connect_connection_error(self):
        assert _classify_error("Connection to remote failed") == "connect"

    def test_unknown_falls_to_protocol(self):
        assert _classify_error("Boom") == "protocol"
        assert _classify_error("") == "protocol"

    def test_urllib_unreachable_is_connect(self):
        assert _classify_error("unreachable") == "connect"


# ── WebBridgeError tests ──────────────────────────────────────────


class TestWebBridgeError:
    def test_carries_kind(self):
        err = WebBridgeError("timeout", "timed out")
        assert err.kind == "timeout"
        assert "timed out" in str(err)

    def test_is_runtime_error(self):
        assert issubclass(WebBridgeError, RuntimeError)


# ── Constructor tests ─────────────────────────────────────────────


class TestConstructor:
    def test_default_construction(self):
        d = WebBridgeDriver(url="http://x", session="s")
        assert d.url == "http://x" and d.session == "s"
        assert d._transport is not None
        assert d._sleep is not None

    def test_injected_transport(self):
        rec, transport = recording_transport(ok_response({"value": "42"}))
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        assert d.evaluate("1+1") == 42

    def test_injected_sleep(self):
        slept = []

        def fake_sleep(n):
            slept.append(n)

        rec, transport = recording_transport(error_timeout, ok_response({"value": '"ok"'}))
        d = WebBridgeDriver(url="x", session="s", transport=transport, sleep=fake_sleep)
        assert d.evaluate("1+1", mutating=False) == "ok"
        assert len(rec.calls) == 2
        assert len(slept) == 1 and slept[0] == 2


# ── Evaluate retry semantics ──────────────────────────────────────


class TestEvaluateRetry:
    def test_readonly_retries_once_on_timeout(self):
        rec, transport = recording_transport(error_timeout, ok_response({"value": '"ok"'}))
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        assert d.evaluate("1+1", mutating=False) == "ok"
        assert len(rec.calls) == 2

    def test_mutating_never_retried(self):
        rec, transport = recording_transport(error_timeout)
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        with pytest.raises(WebBridgeError) as exc_info:
            d.evaluate("dangerous", mutating=True)
        assert exc_info.value.kind == "timeout"
        assert len(rec.calls) == 1

    def test_mutating_default_is_true(self):
        """Default mutating=True means no retry — matches today's behaviour
        for callers that don't know about the argument."""
        rec, transport = recording_transport(error_502)
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        with pytest.raises(WebBridgeError) as exc_info:
            d.evaluate("eval(default)")
        assert exc_info.value.kind == "http_502"
        assert len(rec.calls) == 1

    def test_502_is_not_swallowed_into_empty_default(self):
        """Regression: single-shot (mutating=True) 502 raises WebBridgeError,
        never silently returns '' like the old code."""
        rec, transport = recording_transport(error_502)
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        with pytest.raises(WebBridgeError) as exc_info:
            d.evaluate("1+1", mutating=True)
        assert exc_info.value.kind == "http_502"
        assert len(rec.calls) == 1

    def test_readonly_retry_two_errors_raises_second_502(self):
        """Retry path (mutating=False) with 2 consecutive 502 errors
        raises WebBridgeError with correct kind from the second error."""
        rec, transport = recording_transport(error_502, error_502)
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        with pytest.raises(WebBridgeError) as exc_info:
            d.evaluate("1+1", mutating=False)
        assert exc_info.value.kind == "http_502"
        assert len(rec.calls) == 2

    def test_readonly_recovers_after_retry_on_connect(self):
        rec, transport = recording_transport(error_conn, ok_response({"value": '"recovered"'}))
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.evaluate("window.probe", mutating=False)
        assert result == "recovered"
        assert len(rec.calls) == 2

    def test_code_evaluation_result_parsed(self):
        rec, transport = recording_transport(ok_response({"value": json.dumps({"a": 1})}))
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.evaluate("document.title", mutating=False)
        assert result == {"a": 1}


# ── Backward compat: list_tabs / snapshot / navigate / … return dicts ──


class TestBackwardCompatMethods:
    def test_list_tabs_returns_dict(self):
        rec, transport = recording_transport({"ok": True, "data": {"tabs": []}})
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.list_tabs()
        assert isinstance(result, dict)
        assert result["ok"] is True

    def test_snapshot_returns_dict(self):
        rec, transport = recording_transport({"ok": True})
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.snapshot()
        assert isinstance(result, dict)

    def test_navigate_returns_dict(self):
        rec, transport = recording_transport({"ok": True})
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.navigate("http://example.com", new_tab=True)
        assert isinstance(result, dict)

    def test_click_returns_dict(self):
        rec, transport = recording_transport({"ok": True, "data": {}})
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.click("button")
        assert isinstance(result, dict)

    def test_fill_returns_dict(self):
        rec, transport = recording_transport({"ok": True})
        d = WebBridgeDriver(url="x", session="s", transport=transport)
        result = d.fill("textarea", "hello")
        assert isinstance(result, dict)


# ── Sleep verification ────────────────────────────────────────────


class TestSleepOnRetry:
    def test_retry_sleeps_two_seconds(self):
        slept = []

        def fake_sleep(n):
            slept.append(n)

        rec, transport = recording_transport(error_timeout, ok_response({"value": '"ok"'}))
        d = WebBridgeDriver(url="x", session="s", transport=transport, sleep=fake_sleep)
        d.evaluate("1+1", mutating=False)
        assert len(slept) == 1
        assert slept[0] == 2.0

    def test_no_retry_no_sleep(self):
        slept = []

        def fake_sleep(n):
            slept.append(n)

        rec, transport = recording_transport(error_timeout)
        d = WebBridgeDriver(url="x", session="s", transport=transport, sleep=fake_sleep)
        with pytest.raises(WebBridgeError):
            d.evaluate("click()")
        assert len(slept) == 0