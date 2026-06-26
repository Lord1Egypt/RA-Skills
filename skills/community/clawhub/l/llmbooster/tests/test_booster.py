"""Unit tests for PipelineOrchestrator."""

from __future__ import annotations

import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from booster import PipelineOrchestrator, BoosterComponents, create_booster, handle_input
from models import BoosterConfig, CommandResult, PipelineResult
from step_executor import RetryHandler, StepExecutor
from prompt_loader import PromptTemplateLoader
from stream_handler import StreamingOutputHandler


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------

class MockLLM:
    """Mock LLM that yields predefined tokens per call."""

    def __init__(self, responses: list[list[str]] | None = None, fail_at: set[int] | None = None):
        self.responses = responses or [["output"]]
        self.fail_at = fail_at or set()
        self._call_idx = 0

    async def generate(self, prompt: str):
        idx = self._call_idx
        self._call_idx += 1
        if idx in self.fail_at:
            raise RuntimeError(f"LLM error at call {idx}")
        tokens = self.responses[idx] if idx < len(self.responses) else ["fallback"]
        for token in tokens:
            yield token


class RecordingStreamHandler(StreamingOutputHandler):
    def __init__(self):
        self.step_starts = []
        self.tokens = []
        self.step_completes = []
        self.pipeline_completes = []

    def on_step_start(self, step_number, total_steps, step_name):
        self.step_starts.append((step_number, total_steps, step_name))

    def on_token(self, token):
        self.tokens.append(token)

    def on_step_complete(self, step_name, time_taken_seconds):
        self.step_completes.append((step_name, time_taken_seconds))

    def on_pipeline_complete(self, total_time_seconds, steps_executed):
        self.pipeline_completes.append((total_time_seconds, steps_executed))


def make_orchestrator(
    depth: int = 4,
    max_retries: int = 0,
    llm: MockLLM | None = None,
    prompts_dir: str | None = None,
) -> tuple[PipelineOrchestrator, RecordingStreamHandler]:
    config = BoosterConfig(enabled=True, thinkingDepth=depth, maxRetries=max_retries)
    handler = RecordingStreamHandler()
    if prompts_dir is None:
        prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    prompt_loader = PromptTemplateLoader(prompts_dir)
    if llm is None:
        llm = MockLLM(responses=[["step_out"]] * 4)
    retry_handler = RetryHandler(max_retries=max_retries)
    step_executor = StepExecutor(llm, retry_handler, handler)
    orch = PipelineOrchestrator(config, step_executor, prompt_loader, handler)
    return orch, handler


# ---------------------------------------------------------------------------
# Basic execution
# ---------------------------------------------------------------------------

class TestBasicExecution:
    @pytest.mark.asyncio
    async def test_depth_1_runs_only_plan(self):
        orch, handler = make_orchestrator(depth=1)
        result = await orch.execute("my task")
        assert len(result.steps_executed) == 1
        assert result.steps_executed[0].step_name == "plan"
        assert result.completed_successfully is True

    @pytest.mark.asyncio
    async def test_depth_4_runs_all_steps(self):
        orch, handler = make_orchestrator(depth=4)
        result = await orch.execute("my task")
        assert len(result.steps_executed) == 4
        names = [s.step_name for s in result.steps_executed]
        assert names == ["plan", "draft", "self_critique", "refine"]
        assert result.completed_successfully is True

    @pytest.mark.asyncio
    async def test_depth_2_runs_plan_and_draft(self):
        orch, handler = make_orchestrator(depth=2)
        result = await orch.execute("my task")
        assert len(result.steps_executed) == 2
        names = [s.step_name for s in result.steps_executed]
        assert names == ["plan", "draft"]

    @pytest.mark.asyncio
    async def test_final_output_is_last_step_output(self):
        llm = MockLLM(responses=[["plan_out"], ["draft_out"]])
        orch, handler = make_orchestrator(depth=2, llm=llm)
        result = await orch.execute("task")
        assert result.final_output == "draft_out"


# ---------------------------------------------------------------------------
# Context chaining
# ---------------------------------------------------------------------------

class TestContextChaining:
    @pytest.mark.asyncio
    async def test_first_step_gets_task_input_as_context(self):
        received_prompts = []

        class CaptureLLM:
            async def generate(self, prompt):
                received_prompts.append(prompt)
                yield "out"

        config = BoosterConfig(thinkingDepth=1)
        handler = RecordingStreamHandler()
        prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
        prompt_loader = PromptTemplateLoader(prompts_dir)
        retry_handler = RetryHandler(max_retries=0)
        executor = StepExecutor(CaptureLLM(), retry_handler, handler)
        orch = PipelineOrchestrator(config, executor, prompt_loader, handler)

        await orch.execute("hello world")
        # The prompt should contain "hello world" (the task_input as context)
        assert "hello world" in received_prompts[0]


# ---------------------------------------------------------------------------
# Failure handling
# ---------------------------------------------------------------------------

class TestFailureHandling:
    @pytest.mark.asyncio
    async def test_step1_fail_returns_empty_output_with_warning(self):
        llm = MockLLM(fail_at={0})
        orch, handler = make_orchestrator(depth=2, llm=llm, max_retries=0)
        result = await orch.execute("task")
        assert result.final_output == ""
        assert result.completed_successfully is False
        assert result.warning_message is not None
        assert "plan" in result.warning_message

    @pytest.mark.asyncio
    async def test_step2_fail_returns_step1_output(self):
        llm = MockLLM(responses=[["plan_ok"]], fail_at={1})
        orch, handler = make_orchestrator(depth=2, llm=llm, max_retries=0)
        result = await orch.execute("task")
        assert result.final_output == "plan_ok"
        assert result.completed_successfully is False
        assert result.warning_message is not None
        assert "draft" in result.warning_message

    @pytest.mark.asyncio
    async def test_failure_stops_pipeline(self):
        llm = MockLLM(responses=[["ok"]], fail_at={1})
        orch, handler = make_orchestrator(depth=4, llm=llm, max_retries=0)
        result = await orch.execute("task")
        # Should stop after step 2 fails, not continue to steps 3 and 4
        assert len(result.steps_executed) == 2


# ---------------------------------------------------------------------------
# Pipeline result fields
# ---------------------------------------------------------------------------

class TestPipelineResultFields:
    @pytest.mark.asyncio
    async def test_total_time_is_non_negative(self):
        orch, handler = make_orchestrator(depth=1)
        result = await orch.execute("task")
        assert result.total_time_seconds >= 0

    @pytest.mark.asyncio
    async def test_warning_message_none_on_success(self):
        orch, handler = make_orchestrator(depth=1)
        result = await orch.execute("task")
        assert result.warning_message is None


# ---------------------------------------------------------------------------
# Stream handler integration
# ---------------------------------------------------------------------------

class TestStreamHandlerIntegration:
    @pytest.mark.asyncio
    async def test_on_pipeline_complete_called(self):
        orch, handler = make_orchestrator(depth=1)
        await orch.execute("task")
        assert len(handler.pipeline_completes) == 1
        total_time, steps = handler.pipeline_completes[0]
        assert total_time >= 0
        assert steps == 1

    @pytest.mark.asyncio
    async def test_on_pipeline_complete_called_on_failure(self):
        llm = MockLLM(fail_at={0})
        orch, handler = make_orchestrator(depth=1, llm=llm, max_retries=0)
        await orch.execute("task")
        assert len(handler.pipeline_completes) == 1


# ---------------------------------------------------------------------------
# create_booster factory
# ---------------------------------------------------------------------------

class TestCreateBooster:
    def test_returns_booster_components(self):
        llm = MockLLM()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        result = create_booster(llm, config_path=config_path)
        assert isinstance(result, BoosterComponents)
        assert result.orchestrator is not None
        assert result.cli_handler is not None
        assert result.state_manager is not None

    def test_uses_config_values(self):
        """Config values from file should propagate to components."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump({"enabled": False, "thinkingDepth": 2, "maxRetries": 5}, f)
            tmp_path = f.name
        try:
            llm = MockLLM()
            result = create_booster(llm, config_path=tmp_path)
            assert result.state_manager.enabled is False
            assert result.state_manager.thinking_depth == 2
        finally:
            os.unlink(tmp_path)

    def test_defaults_when_config_missing(self):
        """When config file doesn't exist, defaults should be used."""
        llm = MockLLM()
        result = create_booster(llm, config_path="/nonexistent/path.json")
        # Defaults: enabled=True, thinkingDepth=4
        assert result.state_manager.enabled is True
        assert result.state_manager.thinking_depth == 4

    def test_named_tuple_unpacking(self):
        llm = MockLLM()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        orchestrator, cli_handler, state_manager = create_booster(llm, config_path=config_path)
        assert isinstance(orchestrator, PipelineOrchestrator)


# ---------------------------------------------------------------------------
# handle_input dispatch
# ---------------------------------------------------------------------------

class TestHandleInput:
    @pytest.mark.asyncio
    async def test_booster_command_dispatches_to_cli(self):
        llm = MockLLM()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        booster = create_booster(llm, config_path=config_path)
        result = await handle_input(booster, "/booster status")
        assert isinstance(result, CommandResult)
        assert "enabled" in result.message.lower() or "disabled" in result.message.lower()

    @pytest.mark.asyncio
    async def test_booster_enable_command(self):
        llm = MockLLM()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        booster = create_booster(llm, config_path=config_path)
        result = await handle_input(booster, "/booster enable")
        assert isinstance(result, CommandResult)
        assert result.success is True

    @pytest.mark.asyncio
    async def test_booster_command_case_insensitive(self):
        llm = MockLLM()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        booster = create_booster(llm, config_path=config_path)
        result = await handle_input(booster, "/Booster status")
        assert isinstance(result, CommandResult)

    @pytest.mark.asyncio
    async def test_non_booster_input_dispatches_to_pipeline(self):
        llm = MockLLM(responses=[["out"]] * 4)
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        booster = create_booster(llm, config_path=config_path)
        result = await handle_input(booster, "write a poem")
        assert isinstance(result, PipelineResult)
        assert result.completed_successfully is True

    @pytest.mark.asyncio
    async def test_whitespace_stripped(self):
        llm = MockLLM()
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.schema.json")
        booster = create_booster(llm, config_path=config_path)
        result = await handle_input(booster, "  /booster help  ")
        assert isinstance(result, CommandResult)
