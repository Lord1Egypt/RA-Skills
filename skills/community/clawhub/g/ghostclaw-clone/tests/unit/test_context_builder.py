import pytest
from ghostclaw.core.context_builder import ContextBuilder

def test_build_prompt_with_symbols():
    builder = ContextBuilder()
    metrics = {"total_files": 1}
    issues = ["Test issue"]
    
    # Test with empty symbols
    prompt_flat = builder.build_prompt(metrics, issues, [], [], {}, [])
    assert "<symbols>" not in prompt_flat
    
    # Test with symbol index
    symbol_data = "Class: User\nMethod: login"
    prompt_rich = builder.build_prompt(metrics, issues, [], [], {}, [], symbol_index=symbol_data)
    
    assert "<symbols>" in prompt_rich
    assert symbol_data in prompt_rich
    assert "</symbols>" in prompt_rich


def test_build_delta_prompt_structure():
    """Test that build_delta_prompt produces the expected structure."""
    builder = ContextBuilder()
    current_metrics = {"avg_ccn": 3.5, "files_analyzed": 10}
    current_issues = ["Issue A", "Issue B"]
    current_ghosts = ["Ghost X"]
    current_flags = ["Flag 1"]
    diff_text = "diff --git a/file.py b/file.py\n--- a/file.py\n+++ b/file.py\n@@ -1,2 +1,2 @@\n old\n new"
    base_report = {
        "vibe_score": 75,
        "issues": ["Prior issue"],
        "architectural_ghosts": ["Prior ghost"]
    }
    
    prompt = builder.build_delta_prompt(
        current_metrics=current_metrics,
        current_issues=current_issues,
        current_ghosts=current_ghosts,
        current_flags=current_flags,
        diff_text=diff_text,
        base_report=base_report
    )
    
    # Check all required sections are present
    assert "<base_context>" in prompt
    assert "<diff>" in prompt
    assert "<current_state>" in prompt
    assert "TASK:" in prompt
    
    # Check base context content
    assert "Base Vibe Score: 75/100" in prompt
    assert "Prior Issues:" in prompt
    assert "Prior ghost" in prompt
    
    # Check diff
    assert diff_text in prompt
    
    # Check current state
    assert "Metrics (changed files only)" in prompt
    assert "Current Issues:" in prompt
    assert "Current Ghosts:" in prompt
    assert "Current Flags:" in prompt
    
    # Check task instructions
    assert "architectural drift" in prompt.lower()
    assert "Recommendations" in prompt


def test_build_delta_prompt_without_base_report():
    """Test that delta prompt works even if base_report is None."""
    builder = ContextBuilder()
    current_metrics = {"avg_ccn": 2.0}
    current_issues = []
    current_ghosts = []
    current_flags = []
    diff_text = "diff --git a/test.py b/test.py\n--- a/test.py\n+++ b/test.py\n@@ -1 +1 @@\n-test\n+test"
    
    prompt = builder.build_delta_prompt(
        current_metrics=current_metrics,
        current_issues=current_issues,
        current_ghosts=current_ghosts,
        current_flags=current_flags,
        diff_text=diff_text,
        base_report=None
    )
    
    # Should not include base_context if no base report
    assert "<base_context>" not in prompt
    assert "<diff>" in prompt
    assert "<current_state>" in prompt
