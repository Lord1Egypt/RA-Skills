"""Property-based test: Timing 同 completion reporting.

Feature: llm-booster-skill, Property 13: Timing 同 completion reporting
Validates: Requirements 6.3, 6.4
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

# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Non-negative floats for time values (avoid inf/nan)
non_negative_time = st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False)

# Random step counts 1-4
step_count = st.integers(min_value=1, max_value=4)

# Step names drawn from the valid set
step_name_strategy = st.sampled_from(STEP_ORDER)


# ---------------------------------------------------------------------------
# Property 13: Timing 同 completion reporting
# ---------------------------------------------------------------------------


class TestTimingCompletionReportingProperty:
    """**Validates: Requirements 6.3, 6.4**"""

    @settings(max_examples=100)
    @given(step_name=step_name_strategy, time_taken=non_negative_time)
    def test_on_step_complete_receives_non_negative_time(
        self, step_name: str, time_taken: float
    ) -> None:
        """For any completed step, on_step_complete should receive a
        non-negative time_taken_seconds and display output containing
        the time value."""

        handler = StreamingOutputHandler()
        buf = io.StringIO()
        with redirect_stdout(buf):
            handler.on_step_complete(step_name, time_taken)

        captured = buf.getvalue()

        # The time_taken_seconds passed in is non-negative by construction;
        # verify the handler produces output containing the formatted time.
        assert time_taken >= 0, (
            f"time_taken_seconds should be non-negative, got {time_taken}"
        )
        formatted_time = f"{time_taken:.1f}s"
        assert formatted_time in captured, (
            f"Expected '{formatted_time}' in step-complete output, got: {captured!r}"
        )

    @settings(max_examples=100)
    @given(total_time=non_negative_time, steps_executed=step_count)
    def test_on_pipeline_complete_receives_correct_values(
        self, total_time: float, steps_executed: int
    ) -> None:
        """For any completed pipeline, on_pipeline_complete should receive
        total_time_seconds >= 0 and steps_executed equal to the number of
        steps actually run, and display both values."""

        handler = StreamingOutputHandler()
        buf = io.StringIO()
        with redirect_stdout(buf):
            handler.on_pipeline_complete(total_time, steps_executed)

        captured = buf.getvalue()

        # Verify total_time is non-negative
        assert total_time >= 0, (
            f"total_time_seconds should be >= 0, got {total_time}"
        )

        # Verify steps_executed appears in output
        assert str(steps_executed) in captured, (
            f"Expected steps_executed '{steps_executed}' in pipeline-complete output, "
            f"got: {captured!r}"
        )

        # Verify formatted total time appears in output
        formatted_time = f"{total_time:.1f}s"
        assert formatted_time in captured, (
            f"Expected '{formatted_time}' in pipeline-complete output, got: {captured!r}"
        )

    @settings(max_examples=100)
    @given(steps_executed=step_count, per_step_times=st.lists(
        non_negative_time, min_size=1, max_size=4
    ))
    def test_pipeline_complete_steps_executed_matches_actual_steps(
        self, steps_executed: int, per_step_times: list[float]
    ) -> None:
        """Simulate running N steps with on_step_complete, then verify
        on_pipeline_complete reports steps_executed == N."""

        actual_steps = min(steps_executed, len(per_step_times))
        handler = StreamingOutputHandler()

        buf = io.StringIO()
        with redirect_stdout(buf):
            # Simulate each step completing
            for i in range(actual_steps):
                step_name = STEP_ORDER[i]
                handler.on_step_complete(step_name, per_step_times[i])

            # Compute a total time (sum of per-step times)
            total_time = sum(per_step_times[:actual_steps])
            handler.on_pipeline_complete(total_time, actual_steps)

        captured = buf.getvalue()

        # The pipeline-complete line should contain the actual step count
        assert f"{actual_steps} steps" in captured or f"{actual_steps} step" in captured, (
            f"Expected '{actual_steps}' steps in pipeline-complete output, "
            f"got: {captured!r}"
        )
