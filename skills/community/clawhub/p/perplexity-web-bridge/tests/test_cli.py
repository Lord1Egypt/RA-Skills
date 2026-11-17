# tests/test_cli.py
import json, subprocess, sys, pathlib  # noqa: F401, I001 — plan test copied verbatim
from jev_webbridge import cli

def test_session_derivation_is_stable_and_prefixed(tmp_path):
    s1 = cli.derive_session("compare databases for a startup")
    s2 = cli.derive_session("compare databases for a startup")
    assert s1 == s2 and s1.startswith("jev-")

def test_dry_run_never_touches_driver(tmp_path, capsys):
    code = cli.main(["run", "--goal", "g", "--site", "unit", "--dry-run",
                     "--receipts", str(tmp_path / "r.jsonl")])
    out = capsys.readouterr().out
    assert code == 0
    payload = json.loads(out)
    assert payload["status"] == "dry_run" and payload["session"].startswith("jev-")

def test_escalate_cmd_bridge(tmp_path):
    script = tmp_path / "esc.sh"
    script.write_text('#!/bin/sh\ncat >/dev/null\necho \'{"op":"WAIT","target":null,"confidence":0.9,"source":"escalation","reason":"low_confidence","value":null}\'\n')
    script.chmod(0o755)
    d = cli.build_escalate_fn(str(script))
    out = d({"reason": "low_confidence", "goal": "g"})
    assert out["source"] == "escalation" and out["op"] == "WAIT"


def test_url_required_without_dry_run(capsys):
    # E2E gap found 2026-09-24: a run with no URL had no tab to observe.
    assert cli.main(["run", "--goal", "g", "--site", "unit"]) == 2
    assert "--url is required" in capsys.readouterr().err


def test_navigate_called_before_loop(monkeypatch):
    calls = []

    class FakeDriver:
        def __init__(self, session):
            self.session = session

        def call(self, action, **kw):
            calls.append((action, kw))

    def fake_loop(driver, **kw):
        calls.append(("loop", {}))
        return {"status": "done", "answer": "a", "cycles": 1,
                "turns": {"escalations": 0}, "wall_ms": 5}

    monkeypatch.setattr(cli, "WebBridgeDriver", FakeDriver)
    monkeypatch.setattr(cli, "run_loop", fake_loop)
    rc = cli.main(["run", "--goal", "g", "--site", "unit", "--url", "https://example.org"])
    assert rc == 0
    assert calls[0] == ("navigate", {"url": "https://example.org"})
    assert calls[-1][0] == "loop"


def test_resolve_text_wraps_goal_with_recipe():
    from jev_webbridge import cli
    assert cli.resolve_text("goal here", None, "finance").startswith("Objective: goal here")
    assert cli.resolve_text("goal here", "raw", "finance") == "raw"
