import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))

from handoff_prompter import HandoffPrompter

def test_prompts():
    print("Verifying handoff prompter strings...")
    
    # Acceptance Criteria 1: dirty_workspace
    dirty = HandoffPrompter.get_prompt("dirty_workspace")
    assert "git stash" in dirty.lower()
    assert "git clean" not in dirty.lower()
    assert "git restore" not in dirty.lower()
    assert "[FATAL_STARTUP]" in dirty
    print("✅ dirty_workspace prompt verified.")

    # Acceptance Criteria 2: happy_path
    happy = HandoffPrompter.get_prompt("happy_path")
    assert "[SUCCESS_HANDOFF]" in happy
    assert "1. Update PRD status" in happy
    assert "python3 ~/.openclaw/skills/issue_tracker/scripts/issues.py" in happy
    print("✅ happy_path prompt verified.")

    # Acceptance Criteria 3: New prompts
    assert "[FATAL_STARTUP]" in HandoffPrompter.get_prompt("startup_validation_failed")
    assert "Startup validation failed" in HandoffPrompter.get_prompt("startup_validation_failed")
    
    assert "[FATAL_STARTUP]" in HandoffPrompter.get_prompt("invalid_git_boundary")
    assert "Invalid Git boundary" in HandoffPrompter.get_prompt("invalid_git_boundary")
    
    assert "[FATAL_LOCK]" in HandoffPrompter.get_prompt("pipeline_locked")
    assert "Another SDLC pipeline is actively running" in HandoffPrompter.get_prompt("pipeline_locked")
    print("✅ New specific prompts verified.")

if __name__ == "__main__":
    try:
        test_prompts()
        print("\nALL HANDOFF PROMPT TESTS PASSED")
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        exit(1)
