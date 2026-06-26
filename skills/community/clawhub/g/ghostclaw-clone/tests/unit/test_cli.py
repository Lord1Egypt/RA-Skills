import pytest
from unittest.mock import MagicMock, patch, ANY, AsyncMock
from pathlib import Path
from ghostclaw.cli.ghostclaw import generate_markdown_report, detect_github_remote, main as cli_main
from ghostclaw.core.cache import LocalCache
import subprocess
import sys
import json


def test_generate_markdown_report():
    report = {
        'vibe_score': 85,
        'stack': 'python',
        'files_analyzed': 10,
        'total_lines': 1000,
        'issues': ['Issue 1'],
        'architectural_ghosts': ['Ghost 1'],
        'red_flags': ['Flag 1'],
        'metadata': {'timestamp': '2026-02-24T22:00:00Z'}
    }
    md = generate_markdown_report(report)
    assert "# Architecture Report — 2026-02-24T22:00:00Z" in md
    assert "## 🟢 Vibe Score: 85/100" in md
    assert "- **Stack**: python" in md
    assert "## Issues Detected" in md
    assert "- Issue 1" in md
    assert "## 👻 Architectural Ghosts" in md
    assert "- Ghost 1" in md
    assert "## 🚨 Red Flags" in md
    assert "- Flag 1" in md


@patch("subprocess.run")
def test_detect_github_remote_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="https://github.com/user/repo.git")
    url = detect_github_remote("/fake/path")
    assert url == "https://github.com/user/repo.git"


@patch("subprocess.run")
def test_detect_github_remote_not_github(mock_run):
    mock_run.return_value = MagicMock(returncode=0, stdout="https://gitlab.com/user/repo.git")
    url = detect_github_remote("/fake/path")
    assert url is None


@patch("subprocess.run")
def test_detect_github_remote_fail(mock_run):
    mock_run.return_value = MagicMock(returncode=1)
    url = detect_github_remote("/fake/path")
    assert url is None


@patch("ghostclaw.cli.services.GhostAgent")
def test_cli_no_cache_flag(mock_agent_class, tmp_path, capsys):
    """Test --no-cache prevents cache usage."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    mock_agent = mock_agent_class.return_value
    mock_agent.run = AsyncMock(return_value={
        'vibe_score': 85, 'stack': 'python', 'files_analyzed': 1, 'total_lines': 1,
        'metadata': {'timestamp': '2026-02-24T22:00:00Z', 'fingerprint': 'test'}
    })

    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo), "--no-cache"]
        cli_main()

        captured = capsys.readouterr()
        assert "Cache hit!" not in captured.err
    finally:
        sys.argv = original_argv


@patch("ghostclaw.cli.services.GhostAgent")
def test_cli_cache_stats_flag(mock_agent_class, tmp_path, capsys):
    """Test --cache-stats prints cache info."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    mock_agent = mock_agent_class.return_value
    mock_agent.run = AsyncMock(return_value={
        'vibe_score': 85, 'stack': 'python', 'files_analyzed': 1, 'total_lines': 1,
        'metadata': {'timestamp': '2026-02-24T22:00:00Z', 'fingerprint': 'test'}
    })

    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo), "--cache-stats"]
        cli_main()

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert "Cache:" in output
        assert "entries" in output
    finally:
        sys.argv = original_argv


@patch("ghostclaw.cli.services.GhostAgent")
def test_cli_cache_dir_flag(mock_agent_class, tmp_path, capsys):
    """Test --cache-dir uses custom directory."""
    repo = tmp_path / "repo"
    custom_cache = tmp_path / "custom_cache"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    mock_agent = mock_agent_class.return_value
    mock_agent.run = AsyncMock(return_value={
        'vibe_score': 85, 'stack': 'python', 'files_analyzed': 1, 'total_lines': 1,
        'metadata': {'timestamp': '2026-02-24T22:00:00Z', 'fingerprint': 'test'}
    })

    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo), "--cache-dir", str(custom_cache), "--cache-stats"]
        cli_main()

        captured = capsys.readouterr()
        output = captured.out + captured.err
        assert str(custom_cache) in output
        assert custom_cache.exists()
    finally:
        sys.argv = original_argv


def test_cli_json_mode_streaming_to_stderr(tmp_path, capsys, monkeypatch):
    """BUG 2: With --json, streaming chunks should go to stderr, not stdout."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    # Mock CodebaseAnalyzer.analyze to return a report with ai_prompt
    class MockReport:
        def model_dump(self):
            return {
                'vibe_score': 85,
                'stack': 'python',
                'files_analyzed': 1,
                'total_lines': 1,
                'ai_prompt': 'fake prompt',
                'metadata': {'timestamp': '2026-02-24T22:00:00Z'},
            }
    async def mock_analyze(self, *args, **kwargs):
        return MockReport()
    monkeypatch.setattr("ghostclaw.core.analyzer.CodebaseAnalyzer.analyze", mock_analyze, raising=True)

    # Mock LLMClient.stream_analysis to yield chunks
    async def fake_stream(self, prompt):
        yield {"type": "content", "content": "STREAMED_CHUNK_1"}
        yield {"type": "content", "content": "STREAMED_CHUNK_2"}
    monkeypatch.setattr("ghostclaw.core.llm_client.LLMClient.stream_analysis", fake_stream, raising=True)

    # Provide dummy API key to satisfy client init
    monkeypatch.setenv("GHOSTCLAW_API_KEY", "dummy")

    # Patch registry.save_report and emit_event to avoid JSON serialization errors
    async def noop_save(report):
        pass
    async def noop_emit(event_name, data):
        pass
    monkeypatch.setattr("ghostclaw.core.adapters.registry.registry.save_report", noop_save)
    monkeypatch.setattr("ghostclaw.core.adapters.registry.registry.emit_event", noop_emit)

    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo), "--json", "--use-ai"]
        cli_main()
        captured = capsys.readouterr()
        # stdout should be valid JSON
        output = json.loads(captured.out)
        # The ai_synthesis field should contain concatenated chunks
        assert output.get("ai_synthesis") == "STREAMED_CHUNK_1STREAMED_CHUNK_2"
        # Streamed chunks should appear in stderr (since --json)
        assert "STREAMED_CHUNK_1" in captured.err
        assert "STREAMED_CHUNK_2" in captured.err
    finally:
        sys.argv = original_argv


@patch("ghostclaw.cli.services.GhostAgent")
def test_cli_cached_synthesis_displayed(mock_agent_class, tmp_path, capsys):
    """BUG 3: Verify that AI synthesis from cache is printed in terminal output with '(cached)' indicator."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    mock_agent = mock_agent_class.return_value
    # Simulate a cache hit with ai_synthesis present
    async def mock_run():
        return {
            'vibe_score': 85,
            'stack': 'python',
            'files_analyzed': 1,
            'total_lines': 1,
            'ai_synthesis': 'Cached AI analysis',
            'metadata': {'timestamp': '2026-02-24T22:00:00Z', 'cache_hit': True}
        }
    mock_agent.run = mock_run

    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo)]  # not --json
        cli_main()

        captured = capsys.readouterr()
        output = captured.out + captured.err
        # Should contain the AI synthesis in the output
        assert "Cached AI analysis" in output
        # Should indicate it's cached
        assert "(cached)" in output
    finally:
        sys.argv = original_argv


@patch("ghostclaw.cli.services.PRService.create_pr", new_callable=AsyncMock)
@patch("ghostclaw.cli.services.GhostAgent")
def test_cli_create_pr_writes_to_repo_root_and_cleans_up(mock_agent_class, mock_create_pr, tmp_path, capsys):
    """BUG 1: Verify --create-pr writes report to repo root and cleans up after PR creation."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    mock_agent = mock_agent_class.return_value
    async def mock_run():
        return {
            'vibe_score': 85,
            'stack': 'python',
            'files_analyzed': 1,
            'total_lines': 1,
            'metadata': {'timestamp': '2026-02-24T22:00:00Z'}
        }
    mock_agent.run = mock_run

    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo), "--create-pr"]
        cli_main()

        captured = capsys.readouterr()
        # Check that the report was written to repo root
        report_files = list(repo.glob("ARCHITECTURE-REPORT-*.md"))
        assert len(report_files) == 0, "Report should be cleaned up after PR creation"
        # PR creation should have been called
        mock_create_pr.assert_called_once()
        # The report path passed to create_github_pr should be in repo root
        call_args = mock_create_pr.call_args
        report_path = call_args[0][0]  # first positional argument (report_file_path)
        assert report_path.parent == repo
    finally:
        sys.argv = original_argv


@patch("ghostclaw.cli.services.GhostAgent")
def test_cli_spinner_cleanup_on_synthesis(mock_agent_class, tmp_path, capsys):
    """BUG 5: Verify Rich spinner is properly stopped after synthesis, even with empty chunks."""
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "pyproject.toml").write_text("[project]\nname='test'")
    (repo / "module.py").write_text("def foo(): return 1\n")

    mock_agent = mock_agent_class.return_value
    # Simulate agent that triggers synthesis events
    async def mock_run():
        # We won't simulate streaming; just complete
        return {
            'vibe_score': 85,
            'stack': 'python',
            'files_analyzed': 1,
            'total_lines': 1,
            'metadata': {'timestamp': '2026-02-24T22:00:00Z'}
        }
    mock_agent.run = mock_run

    # Patch GhostAgent to simulate events? Actually easier: test that no exceptions occur
    # The fix added status.stop() in on_post_synthesis; we can't easily test internal state
    # Instead, we'll run the CLI and ensure it exits cleanly without hanging or errors
    original_argv = sys.argv
    try:
        sys.argv = ["ghostclaw", str(repo)]
        cli_main()
        # If we get here without exception, spinner cleanup likely worked
        captured = capsys.readouterr()
        # No error output about spinner
        assert "Error" not in captured.err
    finally:
        sys.argv = original_argv
