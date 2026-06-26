"""Unit tests for benchmark framework."""

import pytest
from unittest.mock import patch, MagicMock
from memory_bench.agents.nanobot_base import run as run_base
from memory_bench.agents.nanobot_with_memory import run as run_with_memory
from memory_bench.report import generate


class TestNanobotBase:
    """Test nanobot_base.py"""

    @patch("memory_bench.agents.nanobot_base.subprocess.run")
    @patch("memory_bench.agents.nanobot_base.tempfile.mkdtemp")
    @patch("memory_bench.agents.nanobot_base.shutil.rmtree")
    def test_happy_path(self, mock_rmtree, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = "/tmp/fake_workspace"
        mock_run.return_value = MagicMock(stdout="task completed", returncode=0)

        duration, response = run_base("test task")

        assert duration > 0
        assert response == "task completed"
        mock_rmtree.assert_called_once()
        # Verify workspace path was passed (onexc param varies by implementation)
        call_args = mock_rmtree.call_args
        assert call_args[0][0] == "/tmp/fake_workspace"

    @patch("memory_bench.agents.nanobot_base.subprocess.run")
    @patch("memory_bench.agents.nanobot_base.tempfile.mkdtemp")
    @patch("memory_bench.agents.nanobot_base.shutil.rmtree")
    def test_empty_response(self, mock_rmtree, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = "/tmp/fake_workspace"
        mock_run.return_value = MagicMock(stdout="", returncode=0)

        _, response = run_base("test task")

        assert response == ""
        mock_rmtree.assert_called_once()

    @patch("memory_bench.agents.nanobot_base.subprocess.run")
    @patch("memory_bench.agents.nanobot_base.tempfile.mkdtemp")
    @patch("memory_bench.agents.nanobot_base.shutil.rmtree")
    def test_timeout_raises(self, mock_rmtree, mock_mkdtemp, mock_run):
        import subprocess

        mock_mkdtemp.return_value = "/tmp/fake_workspace"
        mock_run.side_effect = subprocess.TimeoutExpired("cmd", 10)

        with pytest.raises(subprocess.TimeoutExpired):
            run_base("test task", timeout=10)
        mock_rmtree.assert_called_once()

    @patch("memory_bench.agents.nanobot_base.subprocess.run")
    @patch("memory_bench.agents.nanobot_base.tempfile.mkdtemp")
    @patch("memory_bench.agents.nanobot_base.shutil.rmtree")
    def test_nonzero_returncode(self, _mock_rmtree, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = "/tmp/fake_workspace"
        mock_run.return_value = MagicMock(
            stdout="", stderr="segmentation fault", returncode=1
        )

        _, response = run_base("test task")

        assert "[nanobot error 1]" in response
        assert "segmentation fault" in response


class TestNanobotWithMemory:
    """Test nanobot_with_memory.py"""

    @patch("memory_bench.agents.nanobot_with_memory.subprocess.run")
    @patch("memory_bench.agents.nanobot_with_memory.tempfile.mkdtemp")
    @patch("memory_bench.agents.nanobot_with_memory.shutil.rmtree")
    @patch("memory_bench.agents.nanobot_with_memory.shutil.copytree")
    @patch("memory_bench.agents.nanobot_with_memory.Path")
    def test_happy_path(
        self, mock_Path, mock_copytree, mock_rmtree, mock_mkdtemp, mock_run
    ):
        # Set up Path mocking so path operations work
        mock_workspace_path = MagicMock()
        mock_Path.return_value = mock_workspace_path
        mock_workspace_path.__truediv__ = MagicMock(return_value=mock_workspace_path)
        mock_workspace_path.mkdir = MagicMock()
        mock_mkdtemp.return_value = "/tmp/fake_workspace"
        mock_run.return_value = MagicMock(stdout="task completed", returncode=0)

        _, response = run_with_memory("test task")

        assert response == "task completed"
        mock_copytree.assert_called_once()
        mock_rmtree.assert_called_once()

class TestReport:
    """Test report.py"""

    def test_base_faster(self):
        result = generate((10.0, "response1"), (8.0, "response2"), "test task")
        assert "Time saved: 2.00s (20.0%)" in result
        assert "Faster: memory-optimization" in result

    def test_memory_faster(self):
        result = generate((8.0, "response1"), (10.0, "response2"), "test task")
        assert "Time saved: -2.00s (-25.0%)" in result
        assert "Faster: native memory" in result

    def test_equal_within_tolerance(self):
        result = generate((10.0, "response1"), (10.0, "response2"), "test task")
        assert "Time saved: 0.00s (0.0%)" in result

    def test_empty_response_handling(self):
        result = generate((10.0, ""), (8.0, ""), "test task")
        assert "Response: ..." in result
