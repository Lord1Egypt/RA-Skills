from app.core.engine import DoctorAssistantEngine
from app.core.models import ReasoningMode, TaskRequest, UseCase


def test_engine_returns_guardrails_in_strict_mode() -> None:
    engine = DoctorAssistantEngine()
    request = TaskRequest(query="Complex sepsis case differential", use_case=UseCase.diagnosis)

    result = engine.execute(request, task_id="t-1")

    assert result.task_id == "t-1"
    assert result.reasoning_mode == ReasoningMode.strict
    assert len(result.guardrails) >= 3
    assert any("clinicians" in line.lower() for line in result.guardrails)


def test_engine_keeps_extension_tracks() -> None:
    engine = DoctorAssistantEngine()
    request = TaskRequest(query="Prepare a teaching deck", use_case=UseCase.teaching)

    result = engine.execute(request)

    assert len(result.next_expansion_tracks) == 3
