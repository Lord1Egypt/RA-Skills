import os
import time
from pathlib import Path

from fastapi.testclient import TestClient

os.environ.setdefault("OPENCLAW_DOCTOR_ENV", "test")
os.environ.setdefault("OPENCLAW_DOCTOR_TASK_STORE", "memory")

import app.main as main_module
from app.channels.formatter import format_task_result_message
from app.core.engine import DoctorAssistantEngine
from app.core.models import TaskRequest, TaskStatus
from app.services.sqlite_task_manager import SQLiteTaskManager


def test_api_token_gate() -> None:
    client = TestClient(main_module.app)
    original_token = main_module.settings.api_token
    main_module.settings.api_token = "doctor-secret"

    payload = {
        "query": "Need strict pneumonia differential with citations",
        "channel": "webchat",
        "use_case": "diagnosis",
    }

    try:
        unauthorized = client.post("/api/tasks/execute", json=payload)
        assert unauthorized.status_code == 401

        authorized = client.post(
            "/api/tasks/execute",
            json=payload,
            headers={"X-Doctor-Token": "doctor-secret"},
        )
        assert authorized.status_code == 200
    finally:
        main_module.settings.api_token = original_token


def test_sqlite_task_manager_roundtrip(tmp_path: Path) -> None:
    db_file = tmp_path / "tasks.db"
    manager = SQLiteTaskManager(str(db_file))

    request = TaskRequest(
        query="Sepsis case with hypotension and high lactate",
        channel="webchat",
        use_case="diagnosis",
    )
    task = manager.create(request)
    manager.mark_running(task.task_id)

    result = DoctorAssistantEngine().execute(request, task_id=task.task_id)
    manager.mark_completed(task.task_id, result)

    fetched = manager.get(task.task_id)
    assert fetched.status == TaskStatus.completed
    assert fetched.result is not None
    assert fetched.result.task_id == task.task_id
    assert len(manager.list()) == 1


def test_channel_formatter_includes_core_sections() -> None:
    result = DoctorAssistantEngine().execute(
        TaskRequest(query="Prepare teaching case on stroke", use_case="teaching", channel="webchat")
    )
    text = format_task_result_message(result)

    assert "Summary:" in text
    assert "Action Plan:" in text
    assert "Guardrails:" in text


def test_submit_async_eventually_completes() -> None:
    client = TestClient(main_module.app)
    payload = {
        "query": "Need async rehab care plan for stroke follow-up",
        "channel": "webchat",
        "use_case": "treatment_rehab",
    }
    submit = client.post("/api/tasks/submit-async", json=payload)
    assert submit.status_code == 200
    task_id = submit.json()["task_id"]

    deadline = time.time() + 2.0
    final_status = None
    while time.time() < deadline:
        task_resp = client.get(f"/api/tasks/{task_id}")
        assert task_resp.status_code == 200
        final_status = task_resp.json()["status"]
        if final_status in {"completed", "failed"}:
            break
        time.sleep(0.05)

    assert final_status == "completed"


def test_cancel_then_retry_flow() -> None:
    client = TestClient(main_module.app)
    request = TaskRequest(
        query="Queued task for cancel and retry flow",
        channel="webchat",
        use_case="diagnosis",
    )
    task = main_module.task_manager.create(request)
    profile = main_module.engine.build_profile(request)
    main_module.task_manager.set_profile(task.task_id, profile)

    cancel_resp = client.post(f"/api/tasks/{task.task_id}/cancel")
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == "cancelled"

    retry_resp = client.post(f"/api/tasks/{task.task_id}/retry")
    assert retry_resp.status_code == 200

    deadline = time.time() + 2.0
    final_status = None
    while time.time() < deadline:
        task_resp = client.get(f"/api/tasks/{task.task_id}")
        assert task_resp.status_code == 200
        final_status = task_resp.json()["status"]
        if final_status in {"completed", "failed"}:
            break
        time.sleep(0.05)

    assert final_status == "completed"
