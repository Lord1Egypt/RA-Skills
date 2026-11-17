import contextlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _posix import requires_posix
from setup_runtime import setup
from mosobleirc_core import MosOblEIRCError
import mosobleirc as cli


class SetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'data'

    @requires_posix
    def test_setup_private_and_no_secret_output(self):
        answers = iter(['yes','1','Home','Test address','yes','2','ColdWater','TEST01','no','no'])
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            setup(self.root, 'direct', ask=lambda _: next(answers), secret=lambda _: 'test-secret')
        self.assertNotIn('test-secret', output.getvalue())
        self.assertEqual(self.root.stat().st_mode & 0o777, 0o700)
        for name in ['config/runtime.json','config/inventory.json','secrets/provider_token']:
            self.assertEqual((self.root/name).stat().st_mode & 0o777, 0o600)
        with patch.dict(os.environ, {}, clear=True):
            args = cli.build_parser().parse_args(['--data-root',str(self.root),'status'])
            cli._resolve_runtime_args(args)
            self.assertEqual(args.transport,'direct')
            self.assertEqual(type(cli._relay(args)).__name__, 'DirectClient')
        with self.assertRaises(MosOblEIRCError):
            setup(self.root, 'direct', secret=lambda _: self.fail('must not ask again'))

    @requires_posix
    def test_symlink_directory_refused(self):
        target = Path(self.tmp.name)/'target'; target.mkdir()
        self.root.symlink_to(target, target_is_directory=True)
        with self.assertRaises(MosOblEIRCError):
            setup(self.root,'direct',ask=lambda _: 'no',secret=lambda _: 'test-secret')
        self.assertEqual(list(target.iterdir()), [])

    @requires_posix
    def test_relay_setup_and_old_config_default(self):
        answers = iter(['https://example.invalid/relay','no'])
        setup(self.root,'yandex-relay',ask=lambda _: next(answers),secret=lambda _: 'test-key')
        cfgpath = self.root/'config/runtime.json'
        cfg = json.loads(cfgpath.read_text()); del cfg['transport']; cfgpath.write_text(json.dumps(cfg))
        with patch.dict(os.environ, {}, clear=True):
            args = cli.build_parser().parse_args(['--data-root',str(self.root),'status'])
            cli._resolve_runtime_args(args)
            self.assertEqual(args.transport,'yandex-relay')
            self.assertEqual(type(cli._relay(args)).__name__,'RelayClient')

    def test_cli_beats_environment(self):
        with patch.dict(os.environ, {'MOSOBLEIRC_TRANSPORT':'direct'}):
            args = cli.build_parser().parse_args(['--data-root',str(self.root),'--transport','yandex-relay','status'])
            cli._resolve_runtime_args(args)
            self.assertEqual(args.transport,'yandex-relay')
