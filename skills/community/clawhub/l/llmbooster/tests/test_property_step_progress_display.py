"""Property-based test: Step progress display 格式正確.

Feature: llm-booster-skill, Property 11: Step progress display 格式正確
Validates: Requirements 6.1
"""

from __future__ import annotations

import io
import os
import sys
from contextlib import redirect_stdout

from hypothesis import given, settings, strategies as st

# Ensure the skill package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stream_handler import StreamingOutputHandler

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STEP_ORDER = ["plan", "draft", "self_critique", "refine"]

STEP_DISPLAY_NAMES: dict[str, str] = {
    "plan": "Plan",
    "draft": "Draft",
    "self_critique": "Self Critique",
    "refine": "Refine",
}

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Generate (total_steps N, step_number K) where 1 ≤ K ≤ N ≤ 4
step_positions = st.integers(min_value=1, max_value=4).flatmap(
    lambda n: st.tuples(st.just(n), st.integers(min_value=1, max_value=n))
)


# ---------------------------------------------------------------------------
# Property 11: Step progress display 格式正確
# ---------------------------------------------------------------------------


class TestStepProgressDisplayProperty:
    """**Validates: Requirements 6.1**"""

    @settings(max_examples=100)
    @given(position=step_positions)
    def test_step_progress_format_correct(
        self, position: tuple[int, int]
    ) -> None:
        """For any step execution at position K out of N total steps
        (1 ≤ K ≤ N ≤ 4), the streaming handler should display output
        containing 'Step K/N: <StepName>' where StepName is the title-cased
        Kth element of [plan, draft, self_critique, refine]."""

        total_steps, step_number = position
        step_name = STEP_ORDER[step_number - 1]
        expected_display = STEP_DISPLAY_NAMES[step_name]

        handler = StreamingOutputHandler()
        buf = io.StringIO()
        with redirect_stdout(buf):
            handler.on_step_start(step_number, total_steps, step_name)

        captured = buf.getvalue()

        expected_format = f"Step {step_number}/{total_steps}: {expected_display}"
        assert expected_format in captured, (
            f"Expected '{expected_format}' in output, got: {captured!r}"
        )

    @settings(max_examples=100)
    @given(position=step_positions)
    def test_step_name_matches_kth_element(
        self, position: tuple[int, int]
    ) -> None:
        """For any step position K out of N, the step_name passed to
        on_step_start should be the Kth element of STEP_ORDER, and the
        output should reflect that step's display name."""

        total_steps, step_number = position
        step_name = STEP_ORDER[step_number - 1]

        handler = StreamingOutputHandler()
        buf = io.StringIO()
        with redirect_stdout(buf):
            handler.on_step_start(step_number, total_steps, step_name)

        captured = buf.getvalue()

        # Verify the step number and total are present
        assert f"{step_number}/{total_steps}" in captured, (
            f"Expected '{step_number}/{total_steps}' in output, got: {captured!r}"
        )

        # Verify the correct display name is present
        expected_display = STEP_DISPLAY_NAMES[step_name]
        assert expected_display in captured, (
            f"Expected display name '{expected_display}' for step '{step_name}' "
            f"in output, got: {captured!r}"
        )
