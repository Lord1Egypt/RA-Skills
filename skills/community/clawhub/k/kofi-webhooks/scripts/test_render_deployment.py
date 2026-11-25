"""Offline checks for configurable, consistent deployment files."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from render_deployment import render


class RenderTests(unittest.TestCase):
    def test_custom_settings_are_consistent(self):
        with TemporaryDirectory() as temp:
            out = Path(temp) / 'rendered'
            config = render(out, 'payments-demo', 9191, '/srv/payments', '/etc/payments', '/usr/local/bin/python3')
            unit = (out / config['service']).read_text()
            self.assertIn('StateDirectory=payments-demo', unit)
            self.assertIn('WorkingDirectory=/var/lib/payments-demo', unit)
            self.assertIn('/usr/local/bin/python3 -B /srv/payments/kofi_webhooks.py', unit)
            self.assertIn('verification-token:/etc/payments/verification-token.txt', unit)
            self.assertIn('--port 9191', unit)
            self.assertIn('/var/lib/payments-demo/test-events.sqlite3', (out / 'testing.conf').read_text())
            self.assertIn('http://127.0.0.1:9191/kofi', (out / 'nginx-location.conf').read_text())
            self.assertFalse(any('@@' in p.read_text() for p in out.iterdir()))

    def test_existing_output_is_preserved(self):
        with TemporaryDirectory() as temp:
            out = Path(temp) / 'rendered'
            render(out)
            snapshot = {p.name: p.read_bytes() for p in out.iterdir()}
            with self.assertRaises(FileExistsError):
                render(out, port=9999)
            self.assertEqual(snapshot, {p.name: p.read_bytes() for p in out.iterdir()})

    def test_reject_unsafe_values_before_writing(self):
        with TemporaryDirectory() as temp:
            out = Path(temp) / 'rendered'
            for kwargs in ({'name': '../other'}, {'port': 0}, {'port': 65536},
                           {'app_dir': '/srv/../other'}, {'config_dir': '/etc/a\nBad=yes'},
                           {'python': '/usr/bin/python%3'}, {'app_dir': 'relative'}):
                with self.subTest(kwargs=kwargs):
                    with self.assertRaises(ValueError):
                        render(out, **kwargs)
                    self.assertFalse(out.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
