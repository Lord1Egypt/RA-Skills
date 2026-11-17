"""Check that environment diagnostics do not report broken engines as ready."""
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import sys
import unittest
from unittest.mock import patch
import check_env
import ladybug

class EnvironmentChecks(unittest.TestCase):
    def test_native_loader_failure_is_reported(self):
        with patch.object(sys, 'argv', ['check_env.py', '--smoke']), patch.object(ladybug, 'Database', side_effect=OSError('missing native library')) as db, redirect_stderr(StringIO()) as error, redirect_stdout(StringIO()):
            self.assertEqual(check_env.main(), 1)
        self.assertIn('native engine unavailable', error.getvalue())
        db.assert_called_once_with(':memory:', buffer_pool_size=256 * 1024 * 1024)

    def test_missing_api_is_reported_without_traceback(self):
        with patch.object(sys, 'argv', ['check_env.py']), patch.object(ladybug, 'Connection', None), redirect_stderr(StringIO()) as error, redirect_stdout(StringIO()):
            self.assertEqual(check_env.main(), 1)
        self.assertIn('missing API', error.getvalue())

if __name__ == '__main__':
    unittest.main()
