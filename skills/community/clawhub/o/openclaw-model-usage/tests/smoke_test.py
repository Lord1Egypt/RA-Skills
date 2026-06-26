#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "model_usage.py"
FIXTURE_ROOT = ROOT / "tests" / "fixtures_root"
SESSION_DIR = FIXTURE_ROOT / "sample-agent" / "sessions"
FIXTURE_PARENT = ROOT / "tests" / "fixtures" / "sample_parent_usage.jsonl"
FIXTURE_CHILD = ROOT / "tests" / "fixtures" / "sample_subagent_usage.jsonl"
FIXTURE_SESSIONS = ROOT / "tests" / "fixtures" / "sample_sessions.json"

PYTHON = ROOT / ".venv" / "bin" / "python"


def run(*args: str) -> str:
    python = str(PYTHON if PYTHON.exists() else Path(sys.executable))
    cmd = [python, str(SCRIPT), *args]
    return subprocess.check_output(cmd, text=True)


def main() -> int:
    if FIXTURE_ROOT.exists():
        shutil.rmtree(FIXTURE_ROOT)
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    (SESSION_DIR / "parent-session.jsonl").write_text(FIXTURE_PARENT.read_text())
    (SESSION_DIR / "child-session.jsonl").write_text(FIXTURE_CHILD.read_text())

    sessions = json.loads(FIXTURE_SESSIONS.read_text())
    sessions["agent:sample-agent:subagent:no-usage"] = {
        "sessionId": "child-no-usage",
        "label": "metadata-only-subagent",
        "channel": "discord",
        "status": "done",
        "spawnDepth": 1,
        "subagentRole": "leaf",
        "spawnedBy": "agent:sample-agent:discord:channel:123",
        "startedAt": 1774602600000,
        "updatedAt": 1774602900000,
        "sessionFile": "/tmp/sample-agent/sessions/child-no-usage.jsonl",
    }
    (SESSION_DIR / "sessions.json").write_text(json.dumps(sessions))
    (SESSION_DIR / "child-no-usage.jsonl").write_text(
        '{"type":"session","version":3,"id":"header-only-child-no-usage","timestamp":"2026-03-27T09:10:00.000Z","cwd":"/tmp/workspace"}\n'
    )
    (SESSION_DIR / "child-from-prompt.jsonl").write_text(
        '{"type":"session","version":3,"id":"child-from-prompt","timestamp":"2026-03-27T09:15:00.000Z","cwd":"/tmp/workspace"}\n'
        '{"type":"message","id":"u1","timestamp":"2026-03-27T09:15:01.000Z","message":{"role":"user","content":[{"type":"text","text":"[Thu 2026-03-27 09:15 GMT+11] [Subagent Context] You are running as a subagent (depth 1/1).\\nRequester session: agent:sample-agent:discord:channel:123\\nRequester channel: discord\\nYour session: agent:sample-agent:subagent:prompt-only\\n\\n[Subagent Task]: prompt-only-subagent"}]}}\n'
        '{"type":"message","id":"a1","timestamp":"2026-03-27T09:15:02.000Z","message":{"role":"assistant","provider":"openai-codex","model":"gpt-5.4","usage":{"input":400,"output":200,"cacheRead":0,"cacheWrite":0,"totalTokens":600,"cost":{"input":0.001,"output":0.001,"cacheRead":0.0,"cacheWrite":0.0,"total":0.002}},"content":[{"type":"text","text":"done"}]}}\n'
    )

    overview = json.loads(run("overview", "--root", str(FIXTURE_ROOT), "--json"))
    assert overview["rows"] == 4
    assert overview["totals"]["total_tokens"] == 3700
    assert overview["totals"]["cost_total_usd"] == 0.0119
    assert overview["top_agents"][0]["agent"] == "sample-agent"
    assert overview["top_sessions"][0]["session_id"] == "parent-session"
    assert overview["current"]["session_label"] == "prompt-only-subagent"

    summary_text = run("overview", "--root", str(FIXTURE_ROOT), "--limit", "3")
    assert "Usage overview" in summary_text
    assert "Top agents" in summary_text
    assert "Top sessions" in summary_text
    assert "Top models" in summary_text

    top_agents_text = run("top-agents", "--root", str(FIXTURE_ROOT), "--limit", "3")
    assert "Top agents" in top_agents_text
    assert "sample-agent" in top_agents_text

    top_sessions_text = run("top-sessions", "--root", str(FIXTURE_ROOT), "--limit", "3")
    assert "Top sessions" in top_sessions_text
    assert "Discord · sample-agent" in top_sessions_text

    current = json.loads(run("current", "--root", str(FIXTURE_ROOT), "--json"))
    assert current["model"] == "gpt-5.4"
    assert current["parent_session_id"] == "parent-session"
    assert current["session_label"] == "prompt-only-subagent"

    agents = json.loads(run("agents", "--root", str(FIXTURE_ROOT), "--json"))
    assert agents["agents"][0]["agent"] == "sample-agent"
    assert agents["agents"][0]["sessions"] == 3

    sessions_json = json.loads(run("sessions", "--root", str(FIXTURE_ROOT), "--json"))
    assert len(sessions_json["sessions"]) == 4
    child = next(item for item in sessions_json["sessions"] if item["session_id"] == "child-session")
    assert child["parent_session_id"] == "parent-session"
    assert child["spawn_depth"] == 1
    metadata_only = next(item for item in sessions_json["sessions"] if item["session_id"] == "child-no-usage")
    assert metadata_only["parent_session_id"] == "parent-session"
    assert metadata_only["calls"] == 0
    assert metadata_only["started_at"] == "2026-03-27T09:10:00Z"
    prompt_only = next(item for item in sessions_json["sessions"] if item["session_id"] == "child-from-prompt")
    assert prompt_only["label"] == "prompt-only-subagent"
    assert prompt_only["parent_session_id"] == "parent-session"
    assert prompt_only["spawn_depth"] == 1

    subagents = json.loads(run("subagents", "--root", str(FIXTURE_ROOT), "--json"))
    assert len(subagents["subagents"]) == 3
    assert {item["session_id"] for item in subagents["subagents"]} == {"child-session", "child-no-usage", "child-from-prompt"}

    tree = json.loads(run("session-tree", "--root", str(FIXTURE_ROOT), "--json"))
    assert len(tree["trees"]) == 1
    assert tree["trees"][0]["session_id"] == "parent-session"
    assert tree["trees"][0]["tree_total_tokens"] == 3700
    assert {item["session_id"] for item in tree["trees"][0]["children"]} == {"child-session", "child-no-usage", "child-from-prompt"}

    daily = json.loads(run("daily", "--root", str(FIXTURE_ROOT), "--json"))
    assert len(daily["daily"]) >= 2

    dashboard_path = ROOT / "dist" / "test-dashboard.html"
    if dashboard_path.exists():
        dashboard_path.unlink()
    dashboard_result = json.loads(run("dashboard", "--root", str(FIXTURE_ROOT), "--out", str(dashboard_path), "--title", "Fixture Dashboard", "--json"))
    assert dashboard_result["output"] == str(dashboard_path.resolve())
    dashboard_html = dashboard_path.read_text()
    assert "Fixture Dashboard" in dashboard_html
    assert "Who is spending the budget" in dashboard_html
    assert "Most expensive sessions" in dashboard_html
    assert "Recent cost pulse" in dashboard_html
    assert "Latest assistant usage rows" in dashboard_html
    assert "trend-summary" in dashboard_html
    assert "prompt-only-subagent" in dashboard_html
    assert "Discord · sample-agent" in dashboard_html

    rows = json.loads(run("rows", "--root", str(FIXTURE_ROOT), "--session-id", "child-session", "--json"))
    assert len(rows) == 1
    assert rows[0]["session_id"] == "child-session"

    print("smoke test passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
