import unittest
from unittest.mock import patch
import os
import time
import logging
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from setup_logging import setup_orchestrator_logger, ImmediateFlushFileHandler

class TestSetupLogging(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.test_dir = tempfile.TemporaryDirectory()
        self.workdir = self.test_dir.name
        self.log_dir = Path(self.workdir) / ".tmp" / "sdlc_logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Clear existing handlers
        logger = logging.getLogger("sdlc_orchestrator")
        logger.handlers.clear()

    def tearDown(self):
        # Clear handlers
        logger = logging.getLogger("sdlc_orchestrator")
        for handler in logger.handlers:
            if hasattr(handler, 'close'):
                handler.close()
        logger.handlers.clear()
        self.test_dir.cleanup()

    def test_ttl_cleanup(self):
        now = time.time()
        
        # Create an old log file
        old_file = self.log_dir / "orchestrator_old.log"
        old_file.touch()
        os.utime(old_file, (now - 8 * 86400, now - 8 * 86400))
        
        # Create a new log file
        new_file = self.log_dir / "orchestrator_new.log"
        new_file.touch()
        
        # Call setup
        logger = setup_orchestrator_logger(self.workdir, debug_mode=True)
        
        # Assert old is deleted, new is kept
        self.assertFalse(old_file.exists())
        self.assertTrue(new_file.exists())
        
    @patch('pathlib.Path.unlink')
    def test_ttl_cleanup_graceful_on_permission_error(self, mock_unlink):
        mock_unlink.side_effect = PermissionError("Cannot delete")
        
        now = time.time()
        old_file = self.log_dir / "orchestrator_old.log"
        old_file.touch()
        os.utime(old_file, (now - 8 * 86400, now - 8 * 86400))
        
        # Call setup - should not crash
        logger = setup_orchestrator_logger(self.workdir, debug_mode=True)
        self.assertTrue(old_file.exists()) # Still exists
        
    @patch('pathlib.Path.mkdir')
    def test_setup_graceful_on_missing_dir(self, mock_mkdir):
        mock_mkdir.side_effect = PermissionError("Cannot create directory")
        # Call setup - should not crash
        logger = setup_orchestrator_logger(self.workdir, debug_mode=True)
        
        # Console handler should still be there
        self.assertGreater(len(logger.handlers), 0)

if __name__ == "__main__":
    unittest.main()
