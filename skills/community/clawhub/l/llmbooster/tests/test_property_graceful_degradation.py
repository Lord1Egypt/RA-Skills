"""Property-based test: Step failure 後 graceful degradation.

Feature: llm-booster-skill, Property 5: Step failure 後 graceful degradation
Validates: Requirements 1.5
"""

from __future__ import annotations

import os
import sys

import pytest
from hypothesis import given, settings, strategies as st

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from booster import PipelineOrchestrator
from models import BoosterConfig
from step_executor import RetryHandler, StepExecutor
from prompt_loader import PromptTemplateLoader
from stream_handler import StreamingOutputHandler

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STEP_ORDER = ["plan", "draft", "self_critique", "refine"]

# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


class FailAtStepLLM:
    """Mock LLM that fails at a specific step (1-indexed).

    Steps before the failure point return deterministic output.
    The step at the failure point raises an exception.
    """

    def __init__(self, fail_at_step: int) -> None:
        self._fail_at = fail_at_step
        self._call_count = 0

    async def generate(self, prompt: str):
        self._call_count += 1
        if self._call_count == self._fail_at:
            raise RuntimeError(f"LLM failure at call {self._call_count}")
        yield f"output_step_{self._call_count}"


class SilentStreamHandler(StreamingOutputHandler):
    """Stream handler that suppresses all output."""

    def on_step_start(self, step_number, total_steps, step_name):
        pass

    def on_token(self, token):
        pass

    def on_step_complete(self, step_name, time_taken_seconds):
        pass

    def on_pipeline_complete(self, total_time_seconds, steps_executed):
        pass


def build_orchestrator_with_failure(
    depth: int, fail_at_step: int
) -> PipelineOrchestrator:
    """Build a PipelineOrchestrator that fails at a specific step number."""
    config = BoosterConfig(enabled=True, thinkingDepth=depth, maxRetries=0)
    handler = SilentStreamHandler()
    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    prompt_loader = PromptTemplateLoader(prompts_dir)
    llm = FailAtStepLLM(fail_at_step)
    retry_handler = RetryHandler(max_retries=0)
    step_executor = StepExecutor(llm, retry_handler, handler)
    return PipelineOrchestrator(config, step_executor, prompt_loader, handler)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Generate depth 1-4 and a failure point between 1 and depth
depth_and_failure = st.integers(min_value=1, max_value=4).flatmap(
    lambda d: st.tuples(st.just(d), st.integers(min_value=1, max_value=d))
)

# ---------------------------------------------------------------------------
# Property 5: Step failure 後 graceful degradation
# ---------------------------------------------------------------------------


class TestGracefulDegradationProperty:
    """**Validates: Requirements 1.5**"""

    @settings(max_examples=100)
    @given(data=depth_and_failure)
    @pytest.mark.asyncio
    async def test_step_failure_returns_previous_output_or_empty(
        self, data: tuple[int, int]
    ) -> None:
        """If step K fails (K > 1), pipeline returns step K-1's output.
        If step 1 fails, pipeline returns empty output."""

        depth, fail_at = data

        orch = build_orchestrator_with_failure(depth, fail_at)
        result = await orch.execute("test task")

        if fail_at == 1:
            assert result.final_output == "", (
                f"Step 1 failed but final_output was '{result.final_output}', "
                f"expected empty string"
            )
        else:
            # The output should be from the last successful step (fail_at - 1)
            expected_output = f"output_step_{fail_at - 1}"
            assert result.final_output == expected_output, (
                f"Step {fail_at} failed (depth={depth}) but final_output was "
                f"'{result.final_output}', expected '{expected_output}'"
            )

    @settings(max_examples=100)
    @given(data=depth_and_failure)
    @pytest.mark.asyncio
    async def test_step_failure_sets_completed_successfully_false(
        self, data: tuple[int, int]
    ) -> None:
        """Pipeline's completed_successfully should be False when a step fails."""

        depth, fail_at = data

        orch = build_orchestrator_with_failure(depth, fail_at)
        result = await orch.execute("test task")

        assert result.completed_successfully is False, (
            f"Expected completed_successfully=False when step {fail_at} fails "
            f"(depth={depth}), got True"
        )

    @settings(max_examples=100)
    @given(data=depth_and_failure)
    @pytest.mark.asyncio
    async def test_step_failure_warning_contains_failed_step_name(
        self, data: tuple[int, int]
    ) -> None:
        """warning_message should contain the name of the failed step."""

        depth, fail_at = data
        failed_step_name = STEP_ORDER[fail_at - 1]

        orch = build_orchestrator_with_failure(depth, fail_at)
        result = await orch.execute("test task")

        assert result.warning_message is not None, (
            f"Expected a warning_message when step '{failed_step_name}' fails, "
            f"got None"
        )
        assert failed_step_name in result.warning_message, (
            f"warning_message '{result.warning_message}' does not contain "
            f"failed step name '{failed_step_name}'"
        )
