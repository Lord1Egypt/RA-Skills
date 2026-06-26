"""Tests for garden init."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest
from engram.init import init_workspace


class TestInit:
    def test_creates_structure(self, tmp_path):
        actions = init_workspace(tmp_path, provider="gemini")
        
        assert (tmp_path / "garden.yaml").exists()
        assert (tmp_path / "memory").is_dir()
        assert (tmp_path / "memory" / "entities").is_dir()
        assert (tmp_path / "MEMORY.md").exists()
        assert any("garden.yaml" in a for a in actions)
    
    def test_creates_daily_log(self, tmp_path):
        from datetime import date
        init_workspace(tmp_path)
        
        today = date.today().isoformat()
        daily = tmp_path / "memory" / f"{today}.md"
        assert daily.exists()
        assert "MindGardener" in daily.read_text()
    
    def test_config_provider(self, tmp_path):
        init_workspace(tmp_path, provider="ollama")
        config = (tmp_path / "garden.yaml").read_text()
        assert "provider: ollama" in config
    
    def test_idempotent(self, tmp_path):
        init_workspace(tmp_path)
        actions2 = init_workspace(tmp_path)
        
        assert any("already exists" in a for a in actions2)
    
    def test_force_overwrite(self, tmp_path):
        init_workspace(tmp_path)
        (tmp_path / "garden.yaml").write_text("old config")
        
        init_workspace(tmp_path, force=True)
        config = (tmp_path / "garden.yaml").read_text()
        assert "MindGardener" in config
    
    def test_gitignore(self, tmp_path):
        init_workspace(tmp_path)
        gitignore = (tmp_path / ".gitignore").read_text()
        assert "*.lock" in gitignore
    
    def test_next_steps(self, tmp_path):
        actions = init_workspace(tmp_path)
        assert any("Next steps" in a for a in actions)
        assert any("garden extract" in a for a in actions)
