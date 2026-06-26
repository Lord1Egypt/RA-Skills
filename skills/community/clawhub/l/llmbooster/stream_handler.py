"""Streaming Output Handler for LLMBooster skill."""

from __future__ import annotations

import sys


class StreamingOutputHandler:
    """
    Handles real-time output during pipeline execution.
    Displays step progress, streams tokens, reports timing.
    Provides clear Booster branding for user awareness.
    """

    def on_pipeline_start(self, task_preview: str = "") -> None:
        """Display Booster branding when pipeline starts."""
        preview = f": {task_preview[:50]}..." if task_preview and len(task_preview) > 50 else f": {task_preview}" if task_preview else ""
        print(f"\n🚀 **Booster Pipeline 啟動**{preview}", flush=True)
        print("─" * 40, flush=True)

    def on_step_start(self, step_number: int, total_steps: int, step_name: str) -> None:
        """Display step progress with emoji and progress bar."""
        label = step_name.replace("_", " ").title()
        # Progress bar: [███░░] for step 3/5
        filled = "█" * step_number
        empty = "░" * (total_steps - step_number)
        progress = f"[{filled}{empty}]"
        print(f"\n🚀 Booster {progress} Step {step_number}/{total_steps}: **{label}**", flush=True)

    def on_token(self, token: str) -> None:
        """Stream single token to output (print without newline, flush)."""
        sys.stdout.write(token)
        sys.stdout.flush()

    def on_step_complete(self, step_name: str, time_taken_seconds: float) -> None:
        """Display step completion with checkmark."""
        label = step_name.replace("_", " ").title()
        print(f"\n✅ {label} 完成 ({time_taken_seconds:.1f}s)", flush=True)

    def on_pipeline_complete(self, total_time_seconds: float, steps_executed: int) -> None:
        """Display pipeline summary with branding."""
        print("─" * 40, flush=True)
        print(f"✅ **Booster 完成** - {steps_executed} 步驟，耗時 {total_time_seconds:.1f}s", flush=True)
        print("", flush=True)
