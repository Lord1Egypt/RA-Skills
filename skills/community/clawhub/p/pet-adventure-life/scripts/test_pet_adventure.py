#!/usr/bin/env python3
"""Smoke tests for pet-adventure-life."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ENGINE = Path(__file__).with_name("pet_adventure.py")
ADAPTER = Path(__file__).with_name("openclaw_adapter.py")


def run(workspace: Path, *args: str) -> dict:
    cmd = [sys.executable, str(ENGINE), "--workspace", str(workspace), *args]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(completed.stdout)


def test_engine_flow() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        run(workspace, "init", "--seed", "fixed", "--force")
        for day in range(1, 8):
            run(
                workspace,
                "advance",
                "--date",
                f"2026-01-0{day}",
                "--offline",
                "--force",
                "--force-call" if day == 1 else "--offline",
            )
        status = run(workspace, "status", "--json")
        assert status["pending_calls"], "expected at least one pending call"
        call_id = status["pending_calls"][0]["id"]
        result = run(workspace, "answer", "--call-id", call_id, "--choice", "1", "--roll", "20")
        assert result["outcome"] == "critical_success"
        assert (workspace / "pet-life" / "diary" / "2026-01-01.md").exists()
        assert (workspace / "pet-life" / "events.jsonl").exists()


def test_auto_resolve_and_adapter() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        run(workspace, "init", "--seed", "fixed", "--force")
        call = run(workspace, "call", "--template", "暴雨前的山路", "--deadline-minutes", "-1")
        assert call["call"]["status"] == "pending"
        resolved = run(workspace, "auto-resolve")
        assert resolved["resolved"], "expected expired urgent call to resolve"
        payload = json.dumps({"workspace": str(workspace)})
        completed = subprocess.run(
            [sys.executable, str(ADAPTER), "status", "--payload", payload],
            capture_output=True,
            text=True,
            check=True,
        )
        adapted = json.loads(completed.stdout)
        assert adapted["ok"] is True


def test_roll_boundaries() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp)
        run(workspace, "init", "--seed", "fixed", "--force")
        for roll, expected in [(1, "critical_failure"), (20, "critical_success")]:
            call = run(workspace, "call", "--template", "夜市里的旧地图")
            call_id = call["call"]["id"]
            result = run(workspace, "answer", "--call-id", call_id, "--choice", "1", "--roll", str(roll))
            assert result["outcome"] == expected


if __name__ == "__main__":
    test_engine_flow()
    test_auto_resolve_and_adapter()
    test_roll_boundaries()
    print("ok")
