"""Tests for the RequestTranslator module."""

import pytest

from acp_openai_bridge.request_translator import RequestTranslator, TranslatedRequest


class TestTranslatedRequest:
    """Tests for the TranslatedRequest dataclass."""

    def test_fields(self):
        req = TranslatedRequest(
            session_id="sess-1",
            content=[{"type": "text", "text": "hello"}],
            is_stream=True,
            request_id="chatcmpl-abc",
        )
        assert req.session_id == "sess-1"
        assert req.content == [{"type": "text", "text": "hello"}]
        assert req.is_stream is True
        assert req.request_id == "chatcmpl-abc"


class TestExtractUserMessage:
    """Tests for RequestTranslator.extract_user_message()."""

    def test_single_user_message(self):
        messages = [{"role": "user", "content": "hello"}]
        assert RequestTranslator.extract_user_message(messages) == "hello"

    def test_last_user_message_extracted(self):
        messages = [
            {"role": "user", "content": "first"},
            {"role": "assistant", "content": "reply"},
            {"role": "user", "content": "second"},
        ]
        assert RequestTranslator.extract_user_message(messages) == "second"

    def test_user_message_among_system_and_assistant(self):
        messages = [
            {"role": "system", "content": "you are helpful"},
            {"role": "user", "content": "question"},
            {"role": "assistant", "content": "answer"},
        ]
        assert RequestTranslator.extract_user_message(messages) == "question"

    def test_no_user_message_raises(self):
        messages = [
            {"role": "system", "content": "system prompt"},
            {"role": "assistant", "content": "hi"},
        ]
        with pytest.raises(ValueError, match="No user message"):
            RequestTranslator.extract_user_message(messages)

    def test_user_message_with_empty_content(self):
        messages = [{"role": "user", "content": ""}]
        assert RequestTranslator.extract_user_message(messages) == ""

    def test_user_message_missing_content_field(self):
        messages = [{"role": "user"}]
        assert RequestTranslator.extract_user_message(messages) == ""


class TestTranslate:
    """Tests for RequestTranslator.translate()."""

    def test_basic_translate(self):
        request = {
            "model": "kiro-acp",
            "messages": [{"role": "user", "content": "write a function"}],
        }
        result = RequestTranslator.translate(request, "sess-123")

        assert result.session_id == "sess-123"
        assert result.content == [{"type": "text", "text": "write a function"}]
        assert result.is_stream is False
        assert result.request_id.startswith("chatcmpl-")

    def test_stream_true(self):
        request = {
            "messages": [{"role": "user", "content": "hi"}],
            "stream": True,
        }
        result = RequestTranslator.translate(request, "sess-1")
        assert result.is_stream is True

    def test_stream_false(self):
        request = {
            "messages": [{"role": "user", "content": "hi"}],
            "stream": False,
        }
        result = RequestTranslator.translate(request, "sess-1")
        assert result.is_stream is False

    def test_stream_default_false(self):
        request = {
            "messages": [{"role": "user", "content": "hi"}],
        }
        result = RequestTranslator.translate(request, "sess-1")
        assert result.is_stream is False

    def test_missing_messages_raises(self):
        with pytest.raises(ValueError, match="messages"):
            RequestTranslator.translate({"model": "kiro-acp"}, "sess-1")

    def test_empty_messages_raises(self):
        with pytest.raises(ValueError, match="messages"):
            RequestTranslator.translate({"messages": []}, "sess-1")

    def test_request_id_unique(self):
        request = {
            "messages": [{"role": "user", "content": "hi"}],
        }
        r1 = RequestTranslator.translate(request, "sess-1")
        r2 = RequestTranslator.translate(request, "sess-1")
        assert r1.request_id != r2.request_id

    def test_content_block_format(self):
        request = {
            "messages": [{"role": "user", "content": "test content"}],
        }
        result = RequestTranslator.translate(request, "sess-1")
        assert len(result.content) == 1
        assert result.content[0]["type"] == "text"
        assert result.content[0]["text"] == "test content"

    def test_extracts_last_user_from_multi_message(self):
        request = {
            "messages": [
                {"role": "system", "content": "be helpful"},
                {"role": "user", "content": "first question"},
                {"role": "assistant", "content": "first answer"},
                {"role": "user", "content": "follow up"},
            ],
        }
        result = RequestTranslator.translate(request, "sess-1")
        assert result.content == [{"type": "text", "text": "follow up"}]
