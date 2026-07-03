"""Tests for the ResponseTranslator module."""

import json

from acp_openai_bridge.response_translator import ResponseTranslator


class TestToChatCompletion:
    """Tests for ResponseTranslator.to_chat_completion()."""

    def test_basic_structure(self):
        result = ResponseTranslator.to_chat_completion(
            request_id="chatcmpl-abc123",
            content="Hello, world!",
            stop_reason="end_turn",
        )
        assert result["id"] == "chatcmpl-abc123"
        assert result["object"] == "chat.completion"
        assert result["model"] == "kiro-acp"
        assert isinstance(result["created"], int)
        assert result["created"] > 0

    def test_choices_format(self):
        result = ResponseTranslator.to_chat_completion(
            request_id="chatcmpl-1",
            content="Test reply",
            stop_reason="end_turn",
        )
        choices = result["choices"]
        assert len(choices) == 1
        choice = choices[0]
        assert choice["index"] == 0
        assert choice["message"]["role"] == "assistant"
        assert choice["message"]["content"] == "Test reply"
        assert choice["finish_reason"] == "stop"

    def test_usage_field(self):
        result = ResponseTranslator.to_chat_completion(
            request_id="chatcmpl-1",
            content="abcdefgh",  # 8 chars → 2 tokens
            stop_reason="end_turn",
        )
        usage = result["usage"]
        assert "prompt_tokens" in usage
        assert "completion_tokens" in usage
        assert "total_tokens" in usage
        assert usage["total_tokens"] == usage["prompt_tokens"] + usage["completion_tokens"]

    def test_custom_model(self):
        result = ResponseTranslator.to_chat_completion(
            request_id="chatcmpl-1",
            content="hi",
            stop_reason="end_turn",
            model="custom-model",
        )
        assert result["model"] == "custom-model"

    def test_stop_reason_mapped(self):
        result = ResponseTranslator.to_chat_completion(
            request_id="chatcmpl-1",
            content="hi",
            stop_reason="max_tokens",
        )
        assert result["choices"][0]["finish_reason"] == "length"


class TestToSseChunk:
    """Tests for ResponseTranslator.to_sse_chunk()."""

    def test_format_data_prefix_and_newlines(self):
        chunk = ResponseTranslator.to_sse_chunk(
            request_id="chatcmpl-abc",
            content="hello",
        )
        assert chunk.startswith("data: ")
        assert chunk.endswith("\n\n")

    def test_parseable_json_payload(self):
        chunk = ResponseTranslator.to_sse_chunk(
            request_id="chatcmpl-abc",
            content="hello",
        )
        payload = json.loads(chunk.removeprefix("data: ").strip())
        assert payload["id"] == "chatcmpl-abc"
        assert payload["object"] == "chat.completion.chunk"
        assert payload["model"] == "kiro-acp"
        assert isinstance(payload["created"], int)

    def test_content_in_delta(self):
        chunk = ResponseTranslator.to_sse_chunk(
            request_id="chatcmpl-abc",
            content="token",
        )
        payload = json.loads(chunk.removeprefix("data: ").strip())
        delta = payload["choices"][0]["delta"]
        assert delta["content"] == "token"
        assert payload["choices"][0]["finish_reason"] is None

    def test_role_in_delta(self):
        chunk = ResponseTranslator.to_sse_chunk(
            request_id="chatcmpl-abc",
            role="assistant",
            content="",
        )
        payload = json.loads(chunk.removeprefix("data: ").strip())
        delta = payload["choices"][0]["delta"]
        assert delta["role"] == "assistant"

    def test_finish_reason_chunk(self):
        chunk = ResponseTranslator.to_sse_chunk(
            request_id="chatcmpl-abc",
            finish_reason="stop",
        )
        payload = json.loads(chunk.removeprefix("data: ").strip())
        choice = payload["choices"][0]
        assert choice["finish_reason"] == "stop"
        # delta should be empty when no content/role provided
        assert choice["delta"] == {}

    def test_no_content_no_role_empty_delta(self):
        chunk = ResponseTranslator.to_sse_chunk(request_id="chatcmpl-abc")
        payload = json.loads(chunk.removeprefix("data: ").strip())
        assert payload["choices"][0]["delta"] == {}

    def test_custom_model(self):
        chunk = ResponseTranslator.to_sse_chunk(
            request_id="chatcmpl-abc",
            content="hi",
            model="my-model",
        )
        payload = json.loads(chunk.removeprefix("data: ").strip())
        assert payload["model"] == "my-model"


class TestMapStopReason:
    """Tests for ResponseTranslator.map_stop_reason()."""

    def test_end_turn(self):
        assert ResponseTranslator.map_stop_reason("end_turn") == "stop"

    def test_max_tokens(self):
        assert ResponseTranslator.map_stop_reason("max_tokens") == "length"

    def test_cancelled(self):
        assert ResponseTranslator.map_stop_reason("cancelled") == "stop"

    def test_refused(self):
        assert ResponseTranslator.map_stop_reason("refused") == "stop"

    def test_unknown_defaults_to_stop(self):
        assert ResponseTranslator.map_stop_reason("something_else") == "stop"


class TestToErrorResponse:
    """Tests for ResponseTranslator.to_error_response()."""

    def test_basic_error(self):
        result = ResponseTranslator.to_error_response("Something went wrong")
        assert result == {
            "error": {
                "message": "Something went wrong",
                "type": "server_error",
                "code": None,
            }
        }

    def test_custom_type_and_code(self):
        result = ResponseTranslator.to_error_response(
            message="Bad request",
            error_type="invalid_request_error",
            code="missing_field",
        )
        assert result["error"]["message"] == "Bad request"
        assert result["error"]["type"] == "invalid_request_error"
        assert result["error"]["code"] == "missing_field"

    def test_error_structure(self):
        result = ResponseTranslator.to_error_response("err")
        assert "error" in result
        error = result["error"]
        assert "message" in error
        assert "type" in error
        assert "code" in error


class TestEstimateTokens:
    """Tests for ResponseTranslator.estimate_tokens()."""

    def test_empty_string(self):
        assert ResponseTranslator.estimate_tokens("") == 0

    def test_short_string(self):
        # "abc" → 3 chars → 3 // 4 = 0
        assert ResponseTranslator.estimate_tokens("abc") == 0

    def test_four_chars(self):
        # "abcd" → 4 chars → 4 // 4 = 1
        assert ResponseTranslator.estimate_tokens("abcd") == 1

    def test_longer_string(self):
        # 20 chars → 20 // 4 = 5
        assert ResponseTranslator.estimate_tokens("a" * 20) == 5

    def test_non_negative(self):
        assert ResponseTranslator.estimate_tokens("") >= 0
