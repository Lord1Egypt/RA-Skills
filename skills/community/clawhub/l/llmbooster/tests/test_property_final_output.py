"""Property-based test: Final output 等於最後一個 step 嘅 output.

Feature: llm-booster-skill, Property 4: Final output 等於最後一個 step 嘅 output
Validates: Requirements 1.4
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


class IdentifiableMockLLM:
    """Mock LLM that returns identifiable outputs per step.

    Each step produces a unique output derived from the step's prompt template
    header, making it easy to verify which step produced the final output.
    Uses a precise line-start match to avoid false positives from context
    content that may contain similar substrings.
    """

    # Ordered from most specific to least to avoid substring collisions.
    _STEP_OUTPUTS = [
        ("# Self-Critique", "output_of_self_critique"),
        ("# Plan", "output_of_plan"),
        ("# Draft", "output_of_draft"),
        ("# Refine", "output_of_refine"),
    ]

    async def generate(self, prompt: str):
        # Match only lines that START with the header (avoids matching
        # "## Draft to Review" when looking for "# Draft").
        for header, output in self._STEP_OUTPUTS:
            for line in prompt.splitlines():
                if line.strip() == header:
                    yield output
                    return
        yield "output_of_unknown"


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


def build_orchestrator(depth: int) -> PipelineOrchestrator:
    """Build a PipelineOrchestrator with the given depth and identifiable mock LLM."""
    config = BoosterConfig(enabled=True, thinkingDepth=depth, maxRetries=0)
    handler = SilentStreamHandler()
    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    prompt_loader = PromptTemplateLoader(prompts_dir)
    llm = IdentifiableMockLLM()
    retry_handler = RetryHandler(max_retries=0)
    step_executor = StepExecutor(llm, retry_handler, handler)
    return PipelineOrchestrator(config, step_executor, prompt_loader, handler)


# Map step names to expected mock outputs
EXPECTED_STEP_OUTPUTS = {
    "plan": "output_of_plan",
    "draft": "output_of_draft",
    "self_critique": "output_of_self_critique",
    "refine": "output_of_refine",
}

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

depths = st.integers(min_value=1, max_value=4)
task_inputs = st.text(min_size=1, max_size=200)

# ---------------------------------------------------------------------------
# Property 4: Final output 等於最後一個 step 嘅 output
# ---------------------------------------------------------------------------


class TestFinalOutputProperty:
    """**Validates: Requirements 1.4**"""

    @settings(max_examples=100)
    @given(depth=depths, task_input=task_inputs)
    @pytest.mark.asyncio
    async def test_final_output_equals_last_step_output(
        self, depth: int, task_input: str
    ) -> None:
        """For any successfully completed pipeline execution with depth N,
        the pipeline's final_output should equal the output of the Nth step."""

        orch = build_orchestrator(depth)
        result = await orch.execute(task_input)

        # Pipeline should complete successfully
        assert result.completed_successfully, (
            f"Pipeline did not complete successfully: {result.warning_message}"
        )
        assert len(result.steps_executed) == depth

        # The last step executed
        last_step = result.steps_executed[-1]
        expected_last_step_name = STEP_ORDER[depth - 1]

        # Verify the last step is the correct one
        assert last_step.step_name == expected_last_step_name, (
            f"Expected last step '{expected_last_step_name}', "
            f"got '{last_step.step_name}'"
        )

        # Property 4: final_output == last step's output
        assert result.final_output == last_step.output, (
            f"final_output does not match last step output.\n"
            f"  final_output: {result.final_output!r}\n"
            f"  last step ({last_step.step_name}) output: {last_step.output!r}"
        )

    @settings(max_examples=100)
    @given(depth=depths, task_input=task_inputs)
    @pytest.mark.asyncio
    async def test_final_output_matches_expected_step_output(
        self, depth: int, task_input: str
    ) -> None:
        """For any depth N, the final_output should equal the known mock
        output for the Nth step in STEP_ORDER."""

        orch = build_orchestrator(depth)
        result = await orch.execute(task_input)

        assert result.completed_successfully

        last_step_name = STEP_ORDER[depth - 1]
        expected_output = EXPECTED_STEP_OUTPUTS[last_step_name]

        assert result.final_output == expected_output, (
            f"final_output does not match expected output for step "
            f"'{last_step_name}'.\n"
            f"  final_output: {result.final_output!r}\n"
            f"  expected: {expected_output!r}"
        )
