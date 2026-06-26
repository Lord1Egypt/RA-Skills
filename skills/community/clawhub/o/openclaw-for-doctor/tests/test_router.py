from app.core.models import ReasoningMode, RoleStage, TaskRequest, UseCase
from app.core.router import ProfileRouter


def test_router_prefers_lookup_for_guideline_query() -> None:
    router = ProfileRouter()
    request = TaskRequest(query="Need latest stroke guideline criteria and citation", use_case=UseCase.diagnosis)
    profile = router.build_profile(request)

    assert profile.role_stage == RoleStage.encyclopedia
    assert profile.reasoning_mode == ReasoningMode.strict


def test_router_can_promote_to_mentor() -> None:
    router = ProfileRouter()
    request = TaskRequest(query="Teach me a residency board oral exam plan", use_case=UseCase.teaching)
    profile = router.build_profile(request)

    assert profile.role_stage == RoleStage.mentor
    assert profile.reasoning_mode == ReasoningMode.innovative
