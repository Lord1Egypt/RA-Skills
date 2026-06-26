import pytest
import json
from unittest.mock import MagicMock, patch, AsyncMock
from ghostclaw_mcp.server import ghostclaw_analyze, ghostclaw_get_ghosts, ghostclaw_refactor_plan
from ghostclaw.core.models import ArchitectureReport

@pytest.mark.asyncio
async def test_ghostclaw_analyze_invalid_path():
    result = await ghostclaw_analyze("/invalid/path")
    data = json.loads(result)
    assert "error" in data

@pytest.mark.asyncio
async def test_ghostclaw_analyze_success(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")

    with patch("ghostclaw.core.analyzer.CodebaseAnalyzer.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = ArchitectureReport(
            repo_path=str(repo),
            vibe_score=100,
            stack="python",
            files_analyzed=1,
            total_lines=10
        )
        result = await ghostclaw_analyze(str(repo))
        data = json.loads(result)
        assert data["vibe_score"] == 100

@pytest.mark.asyncio
async def test_ghostclaw_get_ghosts_success(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")

    with patch("ghostclaw.core.analyzer.CodebaseAnalyzer.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = ArchitectureReport(
            repo_path=str(repo),
            vibe_score=100,
            stack="python",
            files_analyzed=1,
            total_lines=10,
            architectural_ghosts=["Ghost1"]
        )
        result = await ghostclaw_get_ghosts(str(repo))
        data = json.loads(result)
        assert "Ghost1" in data["architectural_ghosts"]

@pytest.mark.asyncio
async def test_ghostclaw_refactor_plan_success(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")

    with patch("ghostclaw.core.analyzer.CodebaseAnalyzer.analyze", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = ArchitectureReport(
            repo_path=str(repo),
            vibe_score=50,
            stack="python",
            files_analyzed=1,
            total_lines=10,
            issues=["Issue1"],
            architectural_ghosts=["Ghost1"]
        )
        result = await ghostclaw_refactor_plan(str(repo))
        assert "### Ghostclaw Refactor Blueprint" in result
        assert "Issue1" in result
        assert "Ghost1" in result
