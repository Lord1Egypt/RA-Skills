"""Auto-generated smoke test."""

def test_skill_directory_exists():
    from pathlib import Path
    assert Path(r"/Users/study/.openclaw/skills/markitdown").exists()
