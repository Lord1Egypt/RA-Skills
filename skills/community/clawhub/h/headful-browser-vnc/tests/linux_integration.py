"""Linux-only lifecycle test against installed Xvfb, x11vnc and sandboxed Chrome."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('browser', ROOT / 'tools/browser.py')
browser = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(browser)


class LinuxLifecycle(unittest.TestCase):
    def setUp(self):
        self.assertEqual(sys.platform, 'linux', 'Run full lifecycle tests on Linux')
        self.assertNotEqual(os.getuid(), 0, 'Run as non-root, with Chrome sandbox enabled')
        self.temp = tempfile.TemporaryDirectory(prefix='headful-linux-')
        self.directory = Path(self.temp.name)
        self.env = {**os.environ, 'BROWSER_STATE_DIR': str(self.directory / 'state'),
                    'OUT_DIR': str(self.directory / 'out'), 'VNC_PASSFILE': str(self.directory / 'passwd')}
        # A known dummy password solely for this temporary local test session.
        subprocess.run(['x11vnc', '-storepasswd', 'testonly', self.env['VNC_PASSFILE']],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        Path(self.env['VNC_PASSFILE']).chmod(0o600)
        self.addCleanup(self.cleanup)

    def cleanup(self):
        for session in ('alpha', 'beta', 'bad-start'):
            completed = subprocess.run([sys.executable, str(ROOT / 'tools/browser.py'), 'stop', session],
                                       env=self.env, capture_output=True, text=True, timeout=30)
            if completed.returncode:
                raise AssertionError('Cleanup failed: ' + completed.stdout + completed.stderr)
        self.temp.cleanup()

    def cli(self, *args, success=True):
        completed = subprocess.run([sys.executable, str(ROOT / 'tools/browser.py'), *args],
                                   env=self.env, capture_output=True, text=True, timeout=100)
        result = json.loads(completed.stdout)
        self.assertEqual(completed.returncode == 0, success, completed.stdout + completed.stderr)
        self.assertEqual(result['success'], success, result)
        return result

    def test_two_sessions_capture_handoff_and_isolated_stop(self):
        alpha = self.cli('start', 'alpha', '--novnc-port', '16080')
        beta = self.cli('start', 'beta')
        self.assertNotEqual(alpha['display'], beta['display'])
        self.assertNotEqual(alpha['vncPort'], beta['vncPort'])
        self.assertNotEqual(alpha['cdpPort'], beta['cdpPort'])
        self.assertNotEqual(alpha['profileDir'], beta['profileDir'])
        self.assertTrue(all(p['alive'] for p in alpha['processes']))
        self.assertTrue(all(p['alive'] for p in beta['processes']))
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(alpha['operatorUrl'], timeout=5) as response:
            self.assertEqual(response.status, 200)

        # Real process-owned, loopback-only listeners, not inferred port numbers.
        for session in ('alpha', 'beta'):
            directory = Path(self.env['BROWSER_STATE_DIR']) / session
            state = browser.read_state(directory)
            for role, key in (('vnc', 'vncPort'), ('chrome', 'cdpPort')):
                record = next(p for p in state['processes'] if p['role'] == role)
                self.assertTrue(browser.listener_owned(state[key], record, state['token']))
            self.assertEqual(directory.stat().st_mode & 0o777, 0o700)
            self.assertEqual((directory / 'session.json').stat().st_mode & 0o777, 0o600)

        target = self.cli('pages', 'alpha')['pages'][0]['targetId']
        captured = self.cli('capture', 'alpha', '--target', target)
        self.assertTrue(Path(captured['artifacts']['html']['path']).is_file())
        self.assertTrue(Path(captured['artifacts']['screenshot']['path']).is_file())
        self.assertFalse((Path(captured['outputDir']) / 'cookies.json').exists())
        self.cli('start', 'alpha', success=False)
        self.assertEqual(self.cli('pause', 'alpha')['state'], 'paused')
        self.cli('navigate-and-capture', 'alpha', '--target', target,
                 '--url', 'https://example.invalid/', success=False)
        self.assertEqual(self.cli('resume', 'alpha')['state'], 'running')
        self.cli('stop', 'alpha')
        self.cli('stop', 'alpha')
        status = self.cli('status', 'beta')
        self.assertEqual(status['state'], 'running')
        self.assertTrue(all(p['alive'] for p in status['processes']))
        self.assertTrue(Path(alpha['profileDir']).is_dir(), 'stop preserves profile')
        self.cli('stop', 'beta')


if __name__ == '__main__':
    unittest.main()
