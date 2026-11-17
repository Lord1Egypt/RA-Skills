"""Regression tests for routing, session, CLI, and verification contracts."""
import json
import sys
from argparse import Namespace

import pytest

sys.path.insert(0, "src")

from perplexity_toolkit.commands.cli import build_parser, cmd_route, cmd_search
from perplexity_toolkit.config import Config
from perplexity_toolkit.drivers import create_driver
from perplexity_toolkit.routing import select_route
from perplexity_toolkit.search import (
    _resolve_new_tab,
    _session_has_tabs,
    build_grounded_query,
)
from perplexity_toolkit.verify import verify_result, verify_sources


class TabsDriver:
    def __init__(self, responses):
        self.responses = iter(responses)

    def list_tabs(self):
        return next(self.responses)


class Response:
    def __init__(self, status, body=b"", content_type="text/html"):
        self.status = status
        self._body = body
        self.headers = {"Content-Type": content_type}

    def read(self, limit=-1):
        return self._body[:limit] if limit >= 0 else self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_empty_webbridge_session_is_healthy_and_opens_first_tab():
    driver = TabsDriver([
        {"success": True, "tabs": []},
        {"success": True, "tabs": [{"id": "tab-1"}]},
    ])
    assert _resolve_new_tab(driver, None) is True
    assert _resolve_new_tab(driver, None) is False


def test_webbridge_session_error_fails_closed():
    driver = TabsDriver([{"error": "no extension connected"}])
    with pytest.raises(RuntimeError, match="list_tabs precheck failed"):
        _session_has_tabs(driver)


def test_explicit_navigation_override_is_preserved():
    driver = TabsDriver([{"success": True, "tabs": [{"id": "tab-1"}]}])
    assert _resolve_new_tab(driver, True) is True
    assert _resolve_new_tab(TabsDriver([{"success": True, "tabs": []}]), False) is False


def test_unknown_backend_fails_closed():
    with pytest.raises(ValueError, match="Unknown driver backend"):
        create_driver(Config(driver_backend="not-implemented"))


def test_toolkit_modes_share_the_explicit_task_session():
    driver = create_driver(Config(session_prefix="task-123"))
    assert getattr(driver, "session") == "task-123"


def test_cli_json_is_one_valid_document_and_forwards_verify(monkeypatch, capsys):
    calls = []

    def fake_search(query, **kwargs):
        calls.append((query, kwargs))
        return {
            "answer": "answer",
            "sources": [],
            "url": "https://example.test/search/1",
            "title": "Example",
            "follow_ups": [],
            "quality": {"verdict": "good"},
        }

    import perplexity_toolkit.search as search_module
    monkeypatch.setattr(search_module, "search", fake_search)
    args = build_parser().parse_args(["search", "question", "--no-verify", "-f", "json"])

    assert cmd_search(args) == 0
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["answer"] == "answer"
    assert calls == [("question", {"new_tab": None, "verify": False})]


def test_cli_search_error_returns_nonzero_but_keeps_json_valid(monkeypatch, capsys):
    def fake_search(query, **kwargs):
        return {"error": "CLI transport failed", "answer": None, "sources": []}

    import perplexity_toolkit.search as search_module
    monkeypatch.setattr(search_module, "search", fake_search)
    args = build_parser().parse_args(["search", "question", "-f", "json"])

    assert cmd_search(args) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["error"] == "CLI transport failed"


def test_verify_flag_defaults_on_and_can_be_disabled_after_subcommand():
    parser = build_parser()
    assert parser.parse_args(["search", "q"]).verify is True
    assert parser.parse_args(["--no-verify", "search", "q"]).verify is False
    assert parser.parse_args(["search", "q", "--no-verify"]).verify is False


def test_readback_is_separate_from_head_reachability(monkeypatch):
    def fake_urlopen(request, timeout):
        if request.get_method() == "HEAD":
            return Response(403)
        return Response(200, b"<html><body>canonical page</body></html>")

    monkeypatch.setattr("perplexity_toolkit.verify.urllib.request.urlopen", fake_urlopen)
    sources = [{"text": "Example", "href": "https://example.test/page"}]
    checked = verify_sources(sources, readback=True)

    assert checked["valid"] == 0
    assert checked["broken"] == 1
    assert checked["readback"]["readable"] == 1
    assert checked["readback"]["unreadable"] == 0
    assert checked["page_content"][0]["claim_support"] == "not_evaluated"

    result = verify_result({"answer": "A sufficiently long answer. " * 10, "sources": sources})
    assert result["quality"]["verification_state"] == "candidate"
    assert result["quality"]["claim_support"] == "not_evaluated"


def test_route_gate_only_matches_explicit_browser_wording():
    assert select_route("Perplexity search the best web frameworks")['route'] == "cli"
    assert select_route("请用网页方式搜索 Perplexity")['route'] == "browser"
    assert select_route("Open Perplexity in Chrome")['route'] == "browser"
    # One-sentence browser requests (verified 2026-09-21)
    assert select_route("用网页搜 Perplexity")['route'] == "browser"
    assert select_route("帮我拿网页版的 Perplexity 搜东西")['route'] == "browser"
    assert select_route("拿网页版 Perplexity 问一下这个问题")['route'] == "browser"


def test_route_cli_command_is_local_and_machine_readable(capsys):
    args = build_parser().parse_args(["route", "use WebBridge", "-f", "json"])
    assert cmd_route(args) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["route"] == "browser"
    assert "WebBridge" in payload["matched_terms"]


def test_grounding_wrapper_is_applied_once():
    wrapped = build_grounded_query("latest AI agent pricing")
    assert wrapped.count("Requirements:") == 1
    assert build_grounded_query(wrapped) == wrapped
