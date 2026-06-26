#!/usr/bin/env python3
"""
E2E Test für spawn_task() + self_report.py Integration.
Simuliert den vollständigen governed agent flow ohne echtes sessions_spawn.
"""
import subprocess
import sys
import tempfile
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from governed_agents.orchestrator import GovernedOrchestrator
from governed_agents.reputation import get_task_history, get_agent_stats, init_db


def test_full_flow():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    os.environ["GOVERNED_DB_PATH"] = db_path
    init_db()

    # 1. Orchestrator erstellen
    g = GovernedOrchestrator.for_task(
        objective="E2E Test: Implement Hello World",
        model="openai/gpt-5.2-codex",
        criteria=["File hello.py exists", "print('hello') works"],
        files=["hello.py"],
    )

    # 2. spawn_task() Instructions prüfen
    task = g.spawn_task()
    assert "self_report.py" in task
    assert g.task_id in task
    print(f"✅ spawn_task() correct — Task ID: {g.task_id}")

    # 3. Simuliere Sub-Agent self-report (wie Sub-Agent es tun würde)
    script = Path(__file__).parent / "self_report.py"
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--task-id",
            g.task_id,
            "--agent-id",
            "openai-gpt-5_2-codex",
            "--objective",
            g.contract.objective,
            "--status",
            "success",
            "--details",
            "E2E test: hello.py created, tests passed",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"self_report.py failed: {result.stderr}"
    print(f"✅ self_report.py success: {result.stdout.strip()}")

    # 4. DB prüfen — ohne manuelles record_success()!
    tasks = get_task_history(agent_id="openai-gpt-5_2-codex", limit=1)
    latest = tasks[0]
    assert latest["task_id"] == g.task_id
    assert latest["objective"] == g.contract.objective
    assert latest["status"] == "success"
    assert latest["score"] == 1.0
    print(f"✅ DB auto-updated: objective='{latest['objective']}'")
    print(f"   score={latest['score']}, status={latest['status']}")

    # 5. Blocked status test (score == 0.5)
    script = Path(__file__).parent / "self_report.py"
    result_blocked = subprocess.run(
        [
            sys.executable,
            str(script),
            "--task-id",
            "TASK-blocked-test",
            "--agent-id",
            "openai-gpt-5_2-codex",
            "--objective",
            "Test blocked scenario",
            "--status",
            "blocked",
            "--details",
            "Permission denied: cannot write to /etc",
        ],
        capture_output=True,
        text=True,
    )
    assert result_blocked.returncode == 0, f"blocked failed: {result_blocked.stderr}"
    blocked_tasks = get_task_history(agent_id="openai-gpt-5_2-codex", limit=10)
    blocked = next((t for t in blocked_tasks if t["task_id"] == "TASK-blocked-test"), None)
    assert blocked and blocked["score"] == 0.5, f"Score should be 0.5 for blocked, got: {blocked}"
    print("✅ blocked status: score=0.5 verified")

    # 6. Special chars in objective (shlex.quote safety)
    result_special = subprocess.run(
        [
            sys.executable,
            str(script),
            "--task-id",
            "TASK-special-chars",
            "--agent-id",
            "openai-gpt-5_2-codex",
            "--objective",
            'Fix "quotes" & ampersands; special $chars',
            "--status",
            "success",
            "--details",
            "Special char test",
        ],
        capture_output=True,
        text=True,
    )
    assert result_special.returncode == 0, f"special chars failed: {result_special.stderr}"
    special_tasks = get_task_history(agent_id="openai-gpt-5_2-codex", limit=10)
    special = next((t for t in special_tasks if t["task_id"] == "TASK-special-chars"), None)
    assert special and 'Fix "quotes"' in special["objective"], f"Objective not stored: {special}"
    print('✅ special chars in objective: stored correctly')

    print("\n🏆 ALL TESTS PASS (including edge cases)")


if __name__ == "__main__":
    test_full_flow()
