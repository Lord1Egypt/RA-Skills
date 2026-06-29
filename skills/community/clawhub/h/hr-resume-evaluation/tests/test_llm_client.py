import json

import pytest
import requests

from scripts.llm_client import (
    MissingApiKey,
    ModelConfig,
    ModelResponseError,
    build_messages,
    evaluate_with_model,
    load_model_config,
)


def test_load_model_config_reads_yaml(tmp_path):
    config_path = tmp_path / "model.yaml"
    config_path.write_text(
        "\n".join(
            [
                "base_url: https://api.example.com",
                "chat_completions_path: /chat/completions",
                "model: test-model",
                "api_key_env: TEST_API_KEY",
                "timeout_seconds: 30",
                "max_retries: 1",
                "temperature: 0.1",
            ]
        ),
        encoding="utf-8",
    )

    config = load_model_config(config_path)

    assert config.model == "test-model"
    assert config.api_key_env == "TEST_API_KEY"


def test_missing_api_key_raises(monkeypatch, tmp_path):
    monkeypatch.delenv("TEST_API_KEY", raising=False)
    config_path = tmp_path / "model.yaml"
    config_path.write_text(
        "\n".join(
            [
                "base_url: https://api.example.com",
                "model: test-model",
                "api_key_env: TEST_API_KEY",
            ]
        ),
        encoding="utf-8",
    )
    config = load_model_config(config_path)

    with pytest.raises(MissingApiKey):
        config.api_key()


def test_build_messages_contains_no_secret(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")

    messages = build_messages(
        candidate_id="alice-resume",
        resume_text="Alice built reporting.",
        jd_text="Need reporting.",
        company_text="B2B company.",
        evaluation_config={"output_language": "zh"},
    )
    joined_content = "\n".join(message["content"] for message in messages)

    assert "secret-value" not in joined_content
    assert "Alice built reporting." in joined_content
    assert "JSON" in joined_content


def test_build_messages_includes_deterministic_candidate_id():
    messages = build_messages(
        candidate_id="alice-resume",
        resume_text="Alice built reporting.",
        jd_text="Need reporting.",
        company_text="B2B company.",
        evaluation_config={"output_language": "zh"},
    )

    user_payload = json.loads(messages[1]["content"])

    assert user_payload["candidate_id"] == "alice-resume"


def test_build_messages_includes_score_formulas():
    messages = build_messages(
        candidate_id="alice-resume",
        resume_text="Alice built reporting.",
        jd_text="Need reporting.",
        company_text="B2B company.",
        evaluation_config={"output_language": "zh"},
    )

    content = messages[1]["content"]

    assert "resume_quality + jd_company_match" in content
    assert "resume_quality / 60 * 100" in content


def test_build_messages_includes_scoring_weights():
    weights = {"resume_quality": {"information_completeness": 10}}
    messages = build_messages(
        candidate_id="alice-resume",
        resume_text="Alice built reporting.",
        jd_text="Need reporting.",
        company_text="B2B company.",
        evaluation_config={"output_language": "zh", "weights": weights},
    )

    user_payload = json.loads(messages[1]["content"])

    assert user_payload["scoring_weights"] == weights


def test_build_messages_includes_enterprise_hiring_calibration():
    messages = build_messages(
        candidate_id="alice-resume",
        resume_text="Alice built reporting.",
        jd_text="Need reporting.",
        company_text="B2B company.",
        evaluation_config={"output_language": "zh"},
    )

    user_payload = json.loads(messages[1]["content"])
    joined_guidance = "\n".join(user_payload["enterprise_hiring_calibration"])

    assert "project delivery" in joined_guidance
    assert "papers or competitions" in joined_guidance
    assert "without rigid caps" in joined_guidance


def _test_config(max_retries):
    return ModelConfig(
        base_url="https://api.example.com",
        chat_completions_path="/chat/completions",
        model="test-model",
        api_key_env="TEST_API_KEY",
        timeout_seconds=30,
        max_retries=max_retries,
        temperature=0.1,
    )


def test_evaluate_with_model_posts_json_and_parses_content(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")
    calls = []

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": '{"ok": true}'}}]}

    def fake_post(url, headers, json, timeout):
        calls.append(
            {
                "url": url,
                "headers": headers,
                "payload": json,
                "timeout": timeout,
            }
        )
        return FakeResponse()

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)
    config = _test_config(max_retries=0)

    result = evaluate_with_model(config, [{"role": "user", "content": "Return JSON"}])

    assert result == {"ok": True}
    assert calls == [
        {
            "url": "https://api.example.com/chat/completions",
            "headers": {
                "Authorization": "Bearer secret-value",
                "Content-Type": "application/json",
            },
            "payload": {
                "model": "test-model",
                "messages": [{"role": "user", "content": "Return JSON"}],
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
            },
            "timeout": 30,
        }
    ]


def test_non_retryable_http_error_fails_once(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")
    monkeypatch.setattr("scripts.llm_client.time.sleep", lambda seconds: None)
    calls = []

    class FakeResponse:
        status_code = 401

        def raise_for_status(self):
            raise requests.HTTPError("401 unauthorized", response=self)

    def fake_post(url, headers, json, timeout):
        calls.append(url)
        return FakeResponse()

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)

    with pytest.raises(ModelResponseError):
        evaluate_with_model(_test_config(max_retries=2), [{"role": "user", "content": "Return JSON"}])

    assert len(calls) == 1


def test_malformed_json_retries_and_succeeds(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")
    monkeypatch.setattr("scripts.llm_client.time.sleep", lambda seconds: None)
    calls = []

    class InvalidResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "{bad json"}}]}

    class SuccessResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": '{"ok": true}'}}]}

    responses = [InvalidResponse(), SuccessResponse()]

    def fake_post(url, headers, json, timeout):
        calls.append(url)
        return responses.pop(0)

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)

    result = evaluate_with_model(_test_config(max_retries=2), [{"role": "user", "content": "Return JSON"}])

    assert len(calls) == 2
    assert result == {"ok": True}


def test_repeated_malformed_json_fails_sanitized_after_retries(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")
    monkeypatch.setattr("scripts.llm_client.time.sleep", lambda seconds: None)
    calls = []

    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "{bad json secret-token"}}]}

    def fake_post(url, headers, json, timeout):
        calls.append(url)
        return FakeResponse()

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)

    with pytest.raises(ModelResponseError) as exc_info:
        evaluate_with_model(_test_config(max_retries=2), [{"role": "user", "content": "Return JSON"}])

    assert len(calls) == 3
    assert "secret-token" not in str(exc_info.value)
    assert "Model response invalid" in str(exc_info.value)


def test_retryable_http_error_retries(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")
    monkeypatch.setattr("scripts.llm_client.time.sleep", lambda seconds: None)
    calls = []

    class RetryableResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.HTTPError("500 server error", response=self)

    class SuccessResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": '{"ok": true}'}}]}

    responses = [RetryableResponse(), SuccessResponse()]

    def fake_post(url, headers, json, timeout):
        calls.append(url)
        return responses.pop(0)

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)

    result = evaluate_with_model(_test_config(max_retries=2), [{"role": "user", "content": "Return JSON"}])

    assert len(calls) > 1
    assert result == {"ok": True}


def test_response_retry_budget_is_separate_from_http_retry_budget(monkeypatch):
    monkeypatch.setenv("TEST_API_KEY", "secret-value")
    monkeypatch.setattr("scripts.llm_client.time.sleep", lambda seconds: None)
    calls = []

    class RetryableResponse:
        status_code = 500

        def raise_for_status(self):
            raise requests.HTTPError("500 server error", response=self)

    class InvalidResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": "{bad json"}}]}

    class SuccessResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"choices": [{"message": {"content": '{"ok": true}'}}]}

    responses = [
        RetryableResponse(),
        RetryableResponse(),
        InvalidResponse(),
        SuccessResponse(),
    ]

    def fake_post(url, headers, json, timeout):
        response = responses.pop(0)
        calls.append(response.__class__.__name__)
        return response

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)

    result = evaluate_with_model(
        _test_config(max_retries=2),
        [{"role": "user", "content": "Return JSON"}],
        max_response_retries=2,
    )

    assert result == {"ok": True}
    assert calls == [
        "RetryableResponse",
        "RetryableResponse",
        "InvalidResponse",
        "SuccessResponse",
    ]


def test_model_response_error_does_not_include_api_key(monkeypatch):
    secret = "secret-value"
    monkeypatch.setenv("TEST_API_KEY", secret)
    monkeypatch.setattr("scripts.llm_client.time.sleep", lambda seconds: None)

    def fake_post(url, headers, json, timeout):
        raise requests.Timeout(f"timed out with {secret}")

    monkeypatch.setattr("scripts.llm_client.requests.post", fake_post)

    with pytest.raises(ModelResponseError) as exc_info:
        evaluate_with_model(_test_config(max_retries=0), [{"role": "user", "content": "Return JSON"}])

    assert secret not in str(exc_info.value)
