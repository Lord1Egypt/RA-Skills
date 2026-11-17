"""Unit tests for the optional Jev judge layer (console_judge)."""
import sys; sys.path.insert(0, "src")

import pytest

from perplexity_toolkit import console_judge as cj


class TestResolve:
    def test_env_and_flag(self, monkeypatch):
        monkeypatch.delenv("PERPLEXITY_CONSOLE_JUDGE", raising=False)
        assert cj.resolve_judge() is False
        monkeypatch.setenv("PERPLEXITY_CONSOLE_JUDGE", "1")
        assert cj.resolve_judge() is True
        monkeypatch.setenv("PERPLEXITY_CONSOLE_JUDGE", "off")
        assert cj.resolve_judge() is False
        assert cj.resolve_judge(True) is True
        assert cj.resolve_judge(False) is False


class TestValidation:
    def test_choice_valid_and_invalid(self):
        ids = {"a", "b"}
        assert cj._validate_choice(
            {"choice": "a", "confidence": 0.8, "probabilities": {"a": 0.8, "b": 0.2}}, ids)
        # probabilities must sum to ~1
        assert not cj._validate_choice(
            {"choice": "a", "confidence": 0.8, "probabilities": {"a": 0.8, "b": 0.5}}, ids)
        # choice must be the arg-max
        assert not cj._validate_choice(
            {"choice": "b", "confidence": 0.9, "probabilities": {"a": 0.9, "b": 0.1}}, ids)
        # choice must be in the offered set
        assert not cj._validate_choice(
            {"choice": "c", "confidence": 0.5, "probabilities": {"a": 0.5, "b": 0.5}}, ids)
        assert not cj._validate_choice({}, ids)

    def test_noul_validation(self):
        assert cj._validate_noul({"noul": 0.42})
        assert not cj._validate_noul({"noul": "x"})
        assert not cj._validate_noul({"noul": 1.5})
        assert not cj._validate_noul(None)


class TestJevAsk:
    def _questions(self):
        return {"q": {"type": "noul", "instructions": "i"}}

    def test_request_failure_is_fail_open(self):
        def boom(url, key, body, timeout):
            raise TimeoutError("timed out")
        res = cj.jev_ask("s", self._questions(), key="k", post=boom)
        assert res["ok"] is False and res["reason"].startswith("request-failed")

    def test_invalid_response_rejected(self):
        def bad(url, key, body, timeout):
            return {"answers": {"q": {"noul": "x"}}}
        res = cj.jev_ask("s", self._questions(), key="k", post=bad)
        assert res["ok"] is False and "invalid-response" in res["reason"]

    def test_good_response(self):
        def good(url, key, body, timeout):
            return {"answers": {"q": {"noul": 0.9}}, "model": "jev-1.13.0"}
        res = cj.jev_ask("s", self._questions(), key="k", post=good)
        assert res["ok"] is True and res["answers"]["q"]["noul"] == 0.9

    def test_missing_key(self, monkeypatch):
        monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
        monkeypatch.delenv("JEV_API_KEY", raising=False)
        monkeypatch.setenv("HERMES_ENV_FILE", "/definitely/missing.env")
        res = cj.jev_ask("s", self._questions())
        assert res["ok"] is False and res["reason"] == "no-api-key"


class TestJudgments:
    def _client(self, aq, cp):
        def client(state, questions):
            return {"ok": True, "answers": {
                "answers_question": {"noul": aq}, "complete": {"noul": cp}},
                "model": "jev-1.13.0", "latency_ms": 300}
        return client

    def test_disabled(self):
        assert cj.judge_extraction("q", "a", client=self._client(1, 1), flag=False) == {"enabled": False}

    def test_verdicts(self):
        assert cj.judge_extraction("q", "a", client=self._client(0.98, 0.95), flag=True)["status"] == "ok"
        assert cj.judge_extraction("q", "a", client=self._client(0.5, 0.9), flag=True)["status"] == "review"
        assert cj.judge_extraction("q", "a", client=self._client(0.1, 0.2), flag=True)["status"] == "concern"

    def test_unavailable_fail_open(self):
        def fail(state, questions):
            return {"ok": False, "reason": "request-failed"}
        res = cj.judge_extraction("q", "a", client=fail, flag=True)
        assert res["status"] == "unavailable" and res["enabled"] is True

    def test_skipped_without_query(self):
        res = cj.judge_extraction("", "a", client=self._client(1, 1), flag=True)
        assert res["status"] == "skipped"


class TestRouteHint:
    def test_route_hint_ok(self):
        def client(state, questions):
            return {"ok": True, "answers": {"route": {
                "choice": "reload-and-retry", "confidence": 0.8,
                "probabilities": {"retry-step": 0.1, "reload-and-retry": 0.7,
                                  "wait-longer": 0.1, "escalate": 0.1}}},
                "model": "jev-1.13.0", "latency_ms": 200}
        h = cj.route_hint("fill", "fill.not-committed", "never committed",
                          client=client, flag=True)
        assert h["status"] == "ok"
        assert h["route"] == "reload-and-retry"
        assert h["confidence"] == 0.8

    def test_route_hint_disabled_and_failure(self):
        def client(state, questions):
            return {"ok": True, "answers": {}}
        assert cj.route_hint("g", "c", "m", client=client, flag=False) == {"enabled": False}

        def fail(state, questions):
            return {"ok": False, "reason": "request-failed"}
        h = cj.route_hint("g", "c", "m", client=fail, flag=True)
        assert h["status"] == "unavailable"

    def test_route_hint_skips_pending_codes(self):
        res = cj.route_hint("pending", "pending.missing", "no staged turn", flag=True)
        assert res == {"enabled": True, "status": "skipped",
                       "reason": "deterministic pending guidance is already in the error message"}
