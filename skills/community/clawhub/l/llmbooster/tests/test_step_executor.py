"""Unit tests for RetryHandler, RetryResult, and StepExecutor."""

from __future__ import annotations

import pytest

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from step_executor import RetryHandler, RetryResult, StepExecutor, OpenClawLLMInterface
from models import StepResult
from stream_handler import StreamingOutputHandler


@pytest.mark.asyncio
async def test_retry_result_fields():
    """RetryResult dataclass stores all expected fields."""
    r = RetryResult(success=True, output="hello", error=None, retries_used=0)
    assert r.success is True
    assert r.output == "hello"
    assert r.error is None
    assert r.retries_used == 0


@pytest.mark.asyncio
async def test_execute_with_retry_succeeds_first_try():
    """Operation succeeds on first attempt — no retries used."""
    handler = RetryHandler(max_retries=3)

    async def ok():
        return "done"

    result = await handler.execute_with_retry(ok, "plan")
    assert result.success is True
    assert result.output == "done"
    assert result.error is None
    assert result.retries_used == 0


@pytest.mark.asyncio
async def test_execute_with_retry_succeeds_after_failures():
    """Operation fails twice then succeeds — retries_used reflects attempts."""
    call_count = 0
    handler = RetryHandler(max_retries=3)

    async def flaky():
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise RuntimeError("boom")
        return "recovered"

    result = await handler.execute_with_retry(flaky, "draft")
    assert result.success is True
    assert result.output == "recovered"
    assert result.error is None
    assert result.retries_used == 2


@pytest.mark.asyncio
async def test_execute_with_retry_exhausts_all_retries():
    """Operation always fails — returns failure after max_retries."""
    handler = RetryHandler(max_retries=2)

    async def always_fail():
        raise ValueError("nope")

    result = await handler.execute_with_retry(always_fail, "refine")
    assert result.success is False
    assert result.output is None
    assert result.error is not None
    assert "refine" in result.error
    assert result.retries_used == 2


@pytest.mark.asyncio
async def test_execute_with_retry_zero_retries():
    """With max_retries=0, only one attempt is made."""
    handler = RetryHandler(max_retries=0)

    async def fail():
        raise RuntimeError("fail")

    result = await handler.execute_with_retry(fail, "plan")
    assert result.success is False
    assert result.retries_used == 0


@pytest.mark.asyncio
async def test_execute_with_retry_zero_retries_success():
    """With max_retries=0, a successful first attempt works fine."""
    handler = RetryHandler(max_retries=0)

    async def ok():
        return "ok"

    result = await handler.execute_with_retry(ok, "plan")
    assert result.success is True
    assert result.output == "ok"
    assert result.retries_used == 0


@pytest.mark.asyncio
async def test_error_message_contains_step_name():
    """Error message includes the step name for debugging."""
    handler = RetryHandler(max_retries=1)

    async def fail():
        raise RuntimeError("connection lost")

    result = await handler.execute_with_retry(fail, "self_critique")
    assert result.success is False
    assert "self_critique" in result.error
    assert "connection lost" in result.error


# ---------------------------------------------------------------------------
# Helpers for StepExecutor tests
# ---------------------------------------------------------------------------

class MockLLM:
    """Mock LLM that yields predefined tokens."""

    def __init__(self, tokens: list[str] | None = None, fail_count: int = 0):
        self.tokens = tokens or ["Hello", " ", "World"]
        self.fail_count = fail_count
        self._calls = 0

    async def generate(self, prompt: str):
        self._calls += 1
        if self._calls <= self.fail_count:
            raise RuntimeError("LLM error")
        for token in self.tokens:
            yield token


class RecordingStreamHandler(StreamingOutputHandler):
    """Stream handler that records all calls for assertion."""

    def __init__(self):
        self.step_starts: list[tuple[int, int, str]] = []
        self.tokens: list[str] = []
        self.step_completes: list[tuple[str, float]] = []

    def on_step_start(self, step_number, total_steps, step_name):
        self.step_starts.append((step_number, total_steps, step_name))

    def on_token(self, token):
        self.tokens.append(token)

    def on_step_complete(self, step_name, time_taken_seconds):
        self.step_completes.append((step_name, time_taken_seconds))

    def on_pipeline_complete(self, total_time_seconds, steps_executed):
        pass


# ---------------------------------------------------------------------------
# StepExecutor — successful execution
# ---------------------------------------------------------------------------

class TestStepExecutorSuccess:
    @pytest.mark.asyncio
    async def test_returns_step_result(self):
        """execute_step returns a StepResult with correct fields."""
        llm = MockLLM(tokens=["foo", "bar"])
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=2), handler)

        result = await executor.execute_step("plan", "Do: {{context}}", "my task", 1, 4)

        assert isinstance(result, StepResult)
        assert result.step_name == "plan"
        assert result.output == "foobar"
        assert result.success is True
        assert result.retries_used == 0
        assert result.error_message is None

    @pytest.mark.asyncio
    async def test_time_taken_is_non_negative(self):
        """time_taken_seconds should be >= 0."""
        llm = MockLLM(tokens=["x"])
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=0), handler)

        result = await executor.execute_step("draft", "{{context}}", "ctx", 1, 1)
        assert result.time_taken_seconds >= 0

    @pytest.mark.asyncio
    async def test_stream_handler_receives_step_start(self):
        """on_step_start is called with correct step_number, total_steps, step_name."""
        llm = MockLLM(tokens=["a"])
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=0), handler)

        await executor.execute_step("draft", "{{context}}", "ctx", 2, 4)

        assert handler.step_starts == [(2, 4, "draft")]

    @pytest.mark.asyncio
    async def test_stream_handler_receives_tokens(self):
        """All tokens from LLM are forwarded to stream handler."""
        llm = MockLLM(tokens=["Hello", " ", "World"])
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=0), handler)

        await executor.execute_step("plan", "{{context}}", "ctx", 1, 1)

        assert handler.tokens == ["Hello", " ", "World"]

    @pytest.mark.asyncio
    async def test_stream_handler_receives_step_complete(self):
        """on_step_complete is called with step_name and non-negative time."""
        llm = MockLLM(tokens=["ok"])
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=0), handler)

        await executor.execute_step("refine", "{{context}}", "ctx", 4, 4)

        assert len(handler.step_completes) == 1
        assert handler.step_completes[0][0] == "refine"
        assert handler.step_completes[0][1] >= 0


# ---------------------------------------------------------------------------
# StepExecutor — prompt assembly
# ---------------------------------------------------------------------------

class TestStepExecutorPromptAssembly:
    @pytest.mark.asyncio
    async def test_context_replaces_placeholder(self):
        """{{context}} in prompt_template is replaced with the context string."""
        received_prompts = []

        class CaptureLLM:
            async def generate(self, prompt):
                received_prompts.append(prompt)
                yield "ok"

        handler = RecordingStreamHandler()
        executor = StepExecutor(CaptureLLM(), RetryHandler(max_retries=0), handler)

        await executor.execute_step("plan", "Task: {{context}}", "write tests", 1, 1)

        assert received_prompts == ["Task: write tests"]

    @pytest.mark.asyncio
    async def test_template_without_placeholder(self):
        """If template has no {{context}}, prompt is the template as-is."""
        received_prompts = []

        class CaptureLLM:
            async def generate(self, prompt):
                received_prompts.append(prompt)
                yield "ok"

        handler = RecordingStreamHandler()
        executor = StepExecutor(CaptureLLM(), RetryHandler(max_retries=0), handler)

        await executor.execute_step("plan", "No placeholder here", "ignored", 1, 1)

        assert received_prompts == ["No placeholder here"]


# ---------------------------------------------------------------------------
# StepExecutor — retry on failure
# ---------------------------------------------------------------------------

class TestStepExecutorRetry:
    @pytest.mark.asyncio
    async def test_retries_on_llm_failure(self):
        """If LLM fails initially, retry handler retries and succeeds."""
        llm = MockLLM(tokens=["recovered"], fail_count=2)
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=3), handler)

        result = await executor.execute_step("draft", "{{context}}", "ctx", 1, 1)

        assert result.success is True
        assert result.output == "recovered"
        assert result.retries_used == 2

    @pytest.mark.asyncio
    async def test_all_retries_exhausted(self):
        """If LLM always fails, returns failure result."""
        llm = MockLLM(tokens=["never"], fail_count=100)
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=2), handler)

        result = await executor.execute_step("plan", "{{context}}", "ctx", 1, 1)

        assert result.success is False
        assert result.output == ""
        assert result.error_message is not None
        assert "plan" in result.error_message

    @pytest.mark.asyncio
    async def test_step_complete_called_even_on_failure(self):
        """on_step_complete is called even when the step fails."""
        llm = MockLLM(tokens=["x"], fail_count=100)
        handler = RecordingStreamHandler()
        executor = StepExecutor(llm, RetryHandler(max_retries=0), handler)

        await executor.execute_step("plan", "{{context}}", "ctx", 1, 1)

        assert len(handler.step_completes) == 1
        assert handler.step_completes[0][0] == "plan"
