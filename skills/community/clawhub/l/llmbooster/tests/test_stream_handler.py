"""Unit tests for StreamingOutputHandler."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from stream_handler import StreamingOutputHandler


@pytest.fixture
def handler() -> StreamingOutputHandler:
    return StreamingOutputHandler()


# ---------------------------------------------------------------------------
# on_step_start
# ---------------------------------------------------------------------------

class TestOnStepStart:
    def test_format_step_2_of_4(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_start(2, 4, "draft")
        captured = capsys.readouterr().out
        assert "Step 2/4: Draft" in captured

    def test_format_step_1_of_1(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_start(1, 1, "plan")
        captured = capsys.readouterr().out
        assert "Step 1/1: Plan" in captured

    def test_underscore_step_name(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_start(3, 4, "self_critique")
        captured = capsys.readouterr().out
        assert "Step 3/4: Self Critique" in captured

    def test_step_4_of_4_refine(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_start(4, 4, "refine")
        captured = capsys.readouterr().out
        assert "Step 4/4: Refine" in captured


# ---------------------------------------------------------------------------
# on_token
# ---------------------------------------------------------------------------

class TestOnToken:
    def test_single_token(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_token("hello")
        captured = capsys.readouterr().out
        assert captured == "hello"

    def test_no_trailing_newline(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_token("word")
        captured = capsys.readouterr().out
        assert not captured.endswith("\n")

    def test_multiple_tokens_concatenate(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_token("foo")
        handler.on_token("bar")
        captured = capsys.readouterr().out
        assert captured == "foobar"

    def test_empty_token(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_token("")
        captured = capsys.readouterr().out
        assert captured == ""


# ---------------------------------------------------------------------------
# on_step_complete
# ---------------------------------------------------------------------------

class TestOnStepComplete:
    def test_displays_step_name_and_time(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_complete("draft", 3.2)
        captured = capsys.readouterr().out
        assert "Draft" in captured
        assert "3.2s" in captured

    def test_underscore_step_name(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_complete("self_critique", 1.5)
        captured = capsys.readouterr().out
        assert "Self Critique" in captured
        assert "1.5s" in captured

    def test_zero_time(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_step_complete("plan", 0.0)
        captured = capsys.readouterr().out
        assert "0.0s" in captured


# ---------------------------------------------------------------------------
# on_pipeline_complete
# ---------------------------------------------------------------------------

class TestOnPipelineComplete:
    def test_displays_summary(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_pipeline_complete(12.5, 4)
        captured = capsys.readouterr().out
        assert "4 steps" in captured
        assert "12.5s" in captured

    def test_single_step(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_pipeline_complete(2.0, 1)
        captured = capsys.readouterr().out
        assert "1 steps" in captured
        assert "2.0s" in captured

    def test_contains_pipeline_complete(self, handler: StreamingOutputHandler, capsys: pytest.CaptureFixture[str]) -> None:
        handler.on_pipeline_complete(5.3, 3)
        captured = capsys.readouterr().out
        assert "Pipeline complete" in captured
