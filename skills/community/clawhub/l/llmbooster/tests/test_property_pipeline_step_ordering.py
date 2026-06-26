"""Property-based test: Pipeline 按 depth 執行正確順序嘅 steps.

Feature: llm-booster-skill, Property 1: Pipeline 按 depth 執行正確順序嘅 steps
Validates: Requirements 1.1, 2.2
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


class MockLLM:
    """Mock LLM that returns deterministic output per call."""

    async def generate(self, prompt: str):
        yield "mock_output"


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
    """Build a PipelineOrchestrator with the given depth and mock dependencies."""
    config = BoosterConfig(enabled=True, thinkingDepth=depth, maxRetries=0)
    handler = SilentStreamHandler()
    prompts_dir = os.path.join(os.path.dirname(__file__), "..", "prompts")
    prompt_loader = PromptTemplateLoader(prompts_dir)
    llm = MockLLM()
    retry_handler = RetryHandler(max_retries=0)
    step_executor = StepExecutor(llm, retry_handler, handler)
    return PipelineOrchestrator(config, step_executor, prompt_loader, handler)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

depths = st.integers(min_value=1, max_value=4)
task_inputs = st.text(min_size=1, max_size=200)

# ---------------------------------------------------------------------------
# Property 1: Pipeline 按 depth 執行正確順序嘅 steps
# ---------------------------------------------------------------------------


class TestPipelineStepOrderingProperty:
    """**Validates: Requirements 1.1, 2.2**"""

    @settings(max_examples=100)
    @given(depth=depths, task_input=task_inputs)
    @pytest.mark.asyncio
    async def test_pipeline_executes_exactly_n_steps(
        self, depth: int, task_input: str
    ) -> None:
        """For any thinkingDepth N (1-4) and any task input, the pipeline
        should execute exactly N steps."""

        orch = build_orchestrator(depth)
        result = await orch.execute(task_input)

        assert len(result.steps_executed) == depth, (
            f"Expected {depth} steps, got {len(result.steps_executed)}"
        )

    @settings(max_examples=100)
    @given(depth=depths, task_input=task_inputs)
    @pytest.mark.asyncio
    async def test_pipeline_steps_are_first_n_in_order(
        self, depth: int, task_input: str
    ) -> None:
        """For any thinkingDepth N (1-4) and any task input, the executed
        steps should be the first N elements of [plan, draft, self_critique,
        refine] in order."""

        orch = build_orchestrator(depth)
        result = await orch.execute(task_input)

        executed_names = [s.step_name for s in result.steps_executed]
        expected_names = STEP_ORDER[:depth]

        assert executed_names == expected_names, (
            f"Expected steps {expected_names}, got {executed_names}"
        )
