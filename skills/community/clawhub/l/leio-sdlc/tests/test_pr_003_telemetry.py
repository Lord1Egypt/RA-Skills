import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
import orchestrator

class TestTelemetry(unittest.TestCase):
    @patch('orchestrator.subprocess.run')
    def test_drun_telemetry(self, mock_run):
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            mock_res = MagicMock()
            mock_res.returncode = 0
            mock_res.stdout = "test output"
            mock_res.stderr = ""
            mock_run.return_value = mock_res
            
            old_debug = os.environ.get("SDLC_DEBUG_MODE")
            os.environ["SDLC_DEBUG_MODE"] = "1"
            
            try:
                orchestrator.drun(["echo", "hello"])
                mock_logger.debug.assert_any_call("DEBUG [Subprocess]: echo hello")
            finally:
                if old_debug is None:
                    del os.environ["SDLC_DEBUG_MODE"]
                else:
                    os.environ["SDLC_DEBUG_MODE"] = old_debug

    @patch('orchestrator.subprocess.Popen')
    def test_dpopen_telemetry(self, mock_popen):
        with patch('logging.getLogger') as mock_get_logger:
            mock_logger = MagicMock()
            mock_get_logger.return_value = mock_logger
            
            old_debug = os.environ.get("SDLC_DEBUG_MODE")
            os.environ["SDLC_DEBUG_MODE"] = "1"
            
            try:
                orchestrator.dpopen(["echo", "hello"])
                mock_logger.debug.assert_called_with("DEBUG [Subprocess Popen]: echo hello")
            finally:
                if old_debug is None:
                    del os.environ["SDLC_DEBUG_MODE"]
                else:
                    os.environ["SDLC_DEBUG_MODE"] = old_debug

if __name__ == '__main__':
    unittest.main()
