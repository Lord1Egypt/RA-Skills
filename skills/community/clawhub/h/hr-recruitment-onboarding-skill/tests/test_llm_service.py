import json
from unittest.mock import Mock

import pytest

import hr_recruitment_onboarding_skill.services.llm_service as llm_service
from hr_recruitment_onboarding_skill.services.llm_service import (
    LLMService,
    ModelGenerationError,
)


def _valid_requirements() -> str:
    return json.dumps(
        {
            "education": "本科及以上",
            "experience_years": 3,
            "required_skills": ["Java"],
            "preferred_skills": [],
            "responsibilities": [],
            "other_requirements": [],
        },
        ensure_ascii=False,
    )


def test_reports_unconfigured_model(monkeypatch):
    for key in ("LLM_BASE_URL", "LLM_MODEL", "LLM_API_KEY"):
        monkeypatch.delenv(key, raising=False)

    assert LLMService.from_environment().is_configured() is False


def test_retries_invalid_json_once_then_accepts_valid_json():
    transport = Mock(side_effect=["not-json", _valid_requirements()])
    service = LLMService("https://example.test/v1", "demo", "secret", transport=transport)

    assert service.generate_requirements({}, "prompt")["required_skills"] == ["Java"]
    assert transport.call_count == 2


def test_retries_invalid_requirement_shape_once_then_accepts_valid_json():
    transport = Mock(side_effect=[json.dumps({"education": "本科及以上"}), _valid_requirements()])
    service = LLMService("https://example.test/v1", "demo", "secret", transport=transport)

    assert service.generate_requirements({}, "prompt")["experience_years"] == 3
    assert transport.call_count == 2


def test_raises_after_two_invalid_responses_without_exposing_api_key():
    transport = Mock(side_effect=["not-json", "still-not-json"])
    service = LLMService("https://example.test/v1", "demo", "top-secret", transport=transport)

    with pytest.raises(ModelGenerationError) as error:
        service.generate_requirements({}, "prompt")

    assert transport.call_count == 2
    assert "top-secret" not in str(error.value)


def test_request_body_uses_openai_chat_contract():
    service = LLMService("https://example.test/v1/", "demo", "secret", transport=Mock())

    assert service._request_body({"job_title": "Java工程师"}, "system prompt") == {
        "model": "demo",
        "messages": [
            {"role": "system", "content": "system prompt"},
            {"role": "user", "content": json.dumps({"job_title": "Java工程师"}, ensure_ascii=False)},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }


class _Response:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self) -> bytes:
        return self.content


def test_default_transport_posts_utf8_openai_request(monkeypatch):
    urlopen = Mock(return_value=_Response(json.dumps({"choices": [{"message": {"content": _valid_requirements()}}]}).encode("utf-8")))
    monkeypatch.setattr(llm_service, "urlopen", urlopen)
    service = LLMService("https://example.test/v1/", "demo", "top-secret")

    assert service.generate_requirements({"job_title": "Java工程师"}, "system prompt")["required_skills"] == ["Java"]

    request = urlopen.call_args.args[0]
    assert request.full_url == "https://example.test/v1/chat/completions"
    assert request.data == json.dumps(service._request_body({"job_title": "Java工程师"}, "system prompt"), ensure_ascii=False).encode("utf-8")
    assert request.get_header("Authorization") == "Bearer top-secret"
    assert request.get_header("Content-type") == "application/json; charset=utf-8"


def test_retries_malformed_openai_envelope_then_raises_model_error(monkeypatch):
    urlopen = Mock(return_value=_Response(b'{"choices": []}'))
    monkeypatch.setattr(llm_service, "urlopen", urlopen)
    service = LLMService("https://example.test/v1", "demo", "top-secret")

    with pytest.raises(ModelGenerationError) as error:
        service.generate_requirements({}, "prompt")

    assert urlopen.call_count == 2
    assert "top-secret" not in str(error.value)


def test_retries_invalid_response_bytes_then_raises_model_error(monkeypatch):
    urlopen = Mock(return_value=_Response(b"\xff"))
    monkeypatch.setattr(llm_service, "urlopen", urlopen)
    service = LLMService("https://example.test/v1", "demo", "top-secret")

    with pytest.raises(ModelGenerationError):
        service.generate_requirements({}, "prompt")

    assert urlopen.call_count == 2
