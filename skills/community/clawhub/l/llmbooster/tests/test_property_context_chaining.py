"""Property-based test: Step 之間嘅 context chaining.

Feature: llm-booster-skill, Property 2: Step 之間嘅 context chaining
Validates: Requirements 1.2
"""

from __future__ import annotations

import os
import sys
from typing import List, Tuple

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


class CapturingMockLLM:
    """Mock LLM that returns identifiable outputs per step and captures prompts.

    For each call, it records the prompt it received and yields a deterministic
    output string derived from the step name embedded in the prompt template.
    """

    # Map a keyword found in each prompt template to a step-specific output.
    _STEP_OUTPUTS = {
        "Plan": "output_of_plan",
        "Draft": "output_of_draft",
        "Self-Critique": "output_of_self_critique",
        "Refine": "output_of_refine",
    }

    def __init__(self) -> None:
        self.captured_prompts: List[str] = []

    async def generate(self, prompt: str):
        self.captured_prompts.append(prompt)
        # Determine which step this prompt belongs to by checking template headers
        for keyword, output in self._STEP_OUTPUTS.items():
            if f"# {keyword}" in prompt:
                yield output
                return
        # Fallback — should not happen with real templates
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


def build_orchestrator(depth: int) -> Tuple[PipelineOrchestrator, CapturingMockLLM]:
    """Build a PipelineOrchestrator with the given depth and a capturing mock LLM."""
    config = BoosterConfig(enabled=True, thinkingDepth=depth, maxRetries=0)
    handler = SilentStreamHandler()
    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    prompt_loader = PromptTemplateLoader(prompts_dir)
    llm = CapturingMockLLM()
    retry_handler = RetryHandler(max_retries=0)
    step_executor = StepExecutor(llm, retry_handler, handler)
    orch = PipelineOrchestrator(config, step_executor, prompt_loader, handler)
    return orch, llm


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Chaining requires at least 2 steps
depths = st.integers(min_value=2, max_value=4)
task_inputs = st.text(min_size=1, max_size=200)

# ---------------------------------------------------------------------------
# Property 2: Step 之間嘅 context chaining
# ---------------------------------------------------------------------------


class TestContextChainingProperty:
    """**Validates: Requirements 1.2**"""

    @settings(max_examples=100)
    @given(depth=depths, task_input=task_inputs)
    @pytest.mark.asyncio
    async def test_step_k_plus_1_context_contains_step_k_output(
        self, depth: int, task_input: str
    ) -> None:
        """For any pipeline execution with depth >= 2, the context input of
        step K+1 should contain the output of step K, for all consecutive
        step pairs in the pipeline."""

        orch, llm = build_orchestrator(depth)
        result = await orch.execute(task_input)

        # All steps should succeed
        assert result.completed_successfully, (
            f"Pipeline did not complete successfully: {result.warning_message}"
        )
        assert len(result.steps_executed) == depth

        # Map step names to their outputs
        step_outputs = {
            sr.step_name: sr.output for sr in result.steps_executed
        }

        # We should have exactly `depth` captured prompts (one per step)
        assert len(llm.captured_prompts) == depth, (
            f"Expected {depth} captured prompts, got {len(llm.captured_prompts)}"
        )

        # Verify chaining: for each consecutive pair (K, K+1),
        # the prompt sent for step K+1 must contain step K's output.
        steps_run = STEP_ORDER[:depth]
        for k in range(len(steps_run) - 1):
            step_k_name = steps_run[k]
            step_k_output = step_outputs[step_k_name]
            step_k_plus_1_prompt = llm.captured_prompts[k + 1]

            assert step_k_output in step_k_plus_1_prompt, (
                f"Step '{steps_run[k + 1]}' prompt does not contain "
                f"output of step '{step_k_name}'.\n"
                f"  Expected to find: {step_k_output!r}\n"
                f"  In prompt: {step_k_plus_1_prompt[:300]!r}..."
            )

    @settings(max_examples=100)
    @given(depth=depths, task_input=task_inputs)
    @pytest.mark.asyncio
    async def test_first_step_receives_task_input_as_context(
        self, depth: int, task_input: str
    ) -> None:
        """For any pipeline execution, the first step's prompt should contain
        the original task input as its context."""

        orch, llm = build_orchestrator(depth)
        await orch.execute(task_input)

        assert len(llm.captured_prompts) >= 1
        first_prompt = llm.captured_prompts[0]

        assert task_input in first_prompt, (
            f"First step prompt does not contain the task input.\n"
            f"  Task input: {task_input!r}\n"
            f"  First prompt: {first_prompt[:300]!r}..."
        )
