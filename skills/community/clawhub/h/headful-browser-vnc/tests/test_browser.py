import importlib.util
import contextlib
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('browser', Path(__file__).resolve().parents[1] / 'tools/browser.py')
browser = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(browser)


class BrowserTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_configuration_is_literal_not_shell(self):
        config = self.directory / '.env'
        config.write_text('VNC_PORT=5908\nOUT_DIR="/tmp/path with spaces"\n# comment\n')
        config.chmod(0o600)
        self.assertEqual(browser.load_config(config), {'VNC_PORT': '5908', 'OUT_DIR': '/tmp/path with spaces'})
        marker = self.directory / 'executed'
        config.write_text(f'OUT_DIR="$(touch {marker})"\n')
        with self.assertRaises(browser.BrowserError):
            browser.load_config(config)
        self.assertFalse(marker.exists())

    def test_unsafe_config_permissions_and_symlink_are_rejected(self):
        config = self.directory / '.env'
        config.write_text('VNC_PORT=5901')
        config.chmod(0o644)
        with self.assertRaises(browser.BrowserError):
            browser.load_config(config)
        config.chmod(0o600)
        link = self.directory / 'link'
        link.symlink_to(config)
        with self.assertRaises(browser.BrowserError):
            browser.load_config(link)

    def test_unknown_and_legacy_config_rejected(self):
        config = self.directory / '.env'
        config.write_text('ALLOW_CHROME_FORCE_RESTART=true')
        config.chmod(0o600)
        with self.assertRaises(browser.BrowserError):
            browser.load_config(config)

    def test_allocated_port_is_free_and_explicit_busy_port_fails(self):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            busy = sock.getsockname()[1]
            with self.assertRaises(browser.BrowserError):
                browser.choose_port(busy, 5901, set())
        port = browser.choose_port(None, 15901, set())
        self.assertTrue(browser.port_available(port))
        with self.assertRaises(browser.BrowserError):
            browser.choose_port(port, 5901, {port})

    def test_private_output_state_and_symlink_directory(self):
        directory = browser.private_dir(self.directory / 'session')
        browser.save(directory / 'session.json', {'state': 'paused'})
        self.assertEqual(directory.stat().st_mode & 0o777, 0o700)
        self.assertEqual((directory / 'session.json').stat().st_mode & 0o777, 0o600)
        self.assertEqual(json.loads((directory / 'session.json').read_text())['state'], 'paused')
        link = self.directory / 'link'
        link.symlink_to(directory)
        with self.assertRaises(browser.BrowserError):
            browser.private_dir(link)

    def test_pause_blocks_navigation_before_any_export(self):
        args = browser.parser().parse_args(['navigate-and-capture', 'test', '--target', 'tab', '--url', 'https://example.test'])
        with patch.object(browser, 'require_browser'):
            with self.assertRaisesRegex(browser.BrowserError, 'paused'):
                browser.export(args, {}, self.directory, {'state': 'paused'})

    def test_named_arguments_and_unknown_arguments(self):
        args = browser.parser().parse_args(['start', 'test', '--display=:101', '--resolution=800x600', '--port=5908', '--remote-debug-port=9228'])
        self.assertEqual((args.display, args.resolution, args.port, args.remote_debug_port), (':101', '800x600', 5908, 9228))
        with self.assertRaises(SystemExit), contextlib.redirect_stderr(io.StringIO()):
            browser.parser().parse_args(['start', 'test', '--unknown'])

    def test_pid_reuse_is_not_treated_as_owned_leader(self):
        with patch.object(browser, 'proc_info', return_value={'start': 'new', 'status': 'S'}):
            self.assertFalse(browser.alive({'pid': 123, 'start': 'old'}))

    def test_failed_start_rolls_back_tracked_children(self):
        pf = self.directory / 'passwd'
        pf.write_bytes(b'12345678')
        pf.chmod(0o600)
        args = browser.parser().parse_args(['start-vnc', 'test', '--passfile', str(pf), '--display=:199'])
        def fake_launch(state, directory, role, command):
            state['processes'].append({'role': role, 'pid': 123, 'pgid': 123, 'start': '1'})
            return state['processes'][-1]
        with patch.object(browser, 'require_tools'), patch.object(browser, 'display_free', return_value=True), \
             patch.object(browser, 'choose_port', return_value=15901), \
             patch.object(browser.subprocess, 'run'), patch.object(browser, 'launch', side_effect=fake_launch), \
             patch.object(browser, 'wait_ready', side_effect=browser.BrowserError('not ready')), \
             patch.object(browser, 'stop_processes') as stop:
            with self.assertRaisesRegex(browser.BrowserError, 'not ready'):
                browser.start_vnc(args, {}, self.directory)
            stop.assert_called_once()
        self.assertEqual(json.loads((self.directory / 'session.json').read_text())['state'], 'failed')

    def test_corrupt_session_state_fails_with_a_diagnostic(self):
        browser.save(self.directory / 'session.json', {'schema': 99})
        with self.assertRaisesRegex(browser.BrowserError, 'Invalid session state'):
            browser.read_state(self.directory)

    def test_missing_passfile_does_not_spawn_display(self):
        args = browser.parser().parse_args(['start-vnc', 'test'])
        with patch.object(browser, 'require_tools'), patch.object(browser, 'launch') as launch:
            with self.assertRaises(browser.BrowserError):
                browser.start_vnc(args, {}, self.directory)
            launch.assert_not_called()

    @unittest.skipUnless(os.path.isdir('/proc/self'), 'Linux /proc required')
    def test_stop_preserves_an_unrelated_process(self):
        owned = subprocess.Popen(['sleep', '60'], start_new_session=True,
                                 env={**os.environ, 'HF_SESSION_TOKEN': 'test-owned'})
        unrelated = subprocess.Popen(['sleep', '60'], start_new_session=True)
        self.addCleanup(lambda: unrelated.poll() is None and unrelated.terminate())
        self.addCleanup(lambda: owned.poll() is None and owned.terminate())
        record = browser.proc_info(owned.pid)
        record['role'] = 'test'
        browser.stop_processes({'processes': [record], 'token': 'test-owned'})
        owned.wait(timeout=2)
        self.assertIsNone(unrelated.poll())
        unrelated.terminate()
        unrelated.wait(timeout=2)


if __name__ == '__main__':
    unittest.main()
