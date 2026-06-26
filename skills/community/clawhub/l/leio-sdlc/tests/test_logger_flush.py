import unittest
import os
import shutil
import tempfile
import logging
import time
from pathlib import Path
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from setup_logging import setup_orchestrator_logger

class TestLoggingInfrastructure(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        # Clean up existing logger to avoid interference
        logger = logging.getLogger("sdlc_orchestrator")
        logger.handlers = []

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        logger = logging.getLogger("sdlc_orchestrator")
        for handler in logger.handlers:
            handler.close()
        logger.handlers = []

    def test_logger_creation_and_file_output(self):
        logger = setup_orchestrator_logger(self.test_dir, debug_mode=False)
        log_dir = Path(self.test_dir) / ".tmp" / "sdlc_logs"
        
        self.assertTrue(log_dir.exists())
        
        logger.info("Test Info Message")
        logger.debug("Test Debug Message")
        
        log_files = list(log_dir.glob("orchestrator_*.log"))
        self.assertEqual(len(log_files), 1)
        
        with open(log_files[0], 'r') as f:
            content = f.read()
            self.assertIn("Test Info Message", content)
            self.assertIn("Test Debug Message", content) # File should always be DEBUG

    def test_console_level_respects_debug_flag(self):
        logger_info = setup_orchestrator_logger(self.test_dir, debug_mode=False)
        console_handler = [h for h in logger_info.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)][0]
        self.assertEqual(console_handler.level, logging.INFO)
        
        # Close handlers manually
        for handler in logger_info.handlers:
            handler.close()
        logger_info.handlers = []
        
        logger_debug = setup_orchestrator_logger(self.test_dir, debug_mode=True)
        console_handler_debug = [h for h in logger_debug.handlers if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)][0]
        self.assertEqual(console_handler_debug.level, logging.DEBUG)

        for handler in logger_debug.handlers:
            handler.close()

    def test_ttl_cleanup(self):
        log_dir = Path(self.test_dir) / ".tmp" / "sdlc_logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        old_file = log_dir / "orchestrator_old.log"
        old_file.touch()
        
        # Set mtime to 8 days ago
        eight_days_ago = time.time() - (8 * 86400)
        os.utime(old_file, (eight_days_ago, eight_days_ago))
        
        logger = setup_orchestrator_logger(self.test_dir, debug_mode=False)
        
        self.assertFalse(old_file.exists(), "Old log file should have been cleaned up by TTL")

        for handler in logger.handlers:
            handler.close()

if __name__ == "__main__":
    unittest.main()
