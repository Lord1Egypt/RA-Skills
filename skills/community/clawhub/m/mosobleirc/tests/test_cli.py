from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "scripts" / "mosobleirc.py"
INVENTORY = ROOT / "tests" / "fixtures" / "inventory.fixture.json"

spec = importlib.util.spec_from_file_location("mosobleirc_cli", MODULE)
cli = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(cli)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name) / "data"

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = cli.main([
                "--data-root", str(self.data),
                "--inventory", str(INVENTORY),
                *args,
            ])
        payload = json.loads(out.getvalue())
        return rc, payload

    def test_init_seeds_fixture_meters(self):
        rc, payload = self.run_cli("init")
        self.assertEqual(rc, 0)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["meters"], 13)
        self.assertEqual(payload["pending_references"], 13)

    def test_status_is_local_and_does_not_require_yandex_key(self):
        self.run_cli("init")
        rc, payload = self.run_cli("status")
        self.assertEqual(rc, 0)
        self.assertTrue(payload["ok"])
        self.assertFalse(payload["provider_contacted"])
        self.assertEqual(payload["meters"], 13)

    def test_reference_pending_is_local(self):
        self.run_cli("init")
        rc, payload = self.run_cli("reference", "pending")
        self.assertEqual(rc, 0)
        self.assertFalse(payload["provider_contacted"])
        self.assertEqual(payload["count"], 13)

    def test_no_direct_write_command_exists(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err), self.assertRaises(SystemExit):
            cli.build_parser().parse_args(["submit", "--meter-id", "1", "--value", "2"])
        self.assertIn("invalid choice", err.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)

class SerialIdentifyCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.data = Path(self.tmp.name) / 'data'
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            cli.main(['--data-root',str(self.data),'--inventory',str(INVENTORY),'init'])
        store=cli.StateStore(self.data)
        store.set_meter_identity(1011, physical_serial='PHYSHW05')

    def run_cli(self,*args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            rc=cli.main(['--data-root',str(self.data),'--inventory',str(INVENTORY),*args])
        return rc,json.loads(out.getvalue())

    def test_local_identify_returns_exact_meter(self):
        rc,p=self.run_cli('local','identify','--serial','TESTHW05')
        self.assertEqual(rc,0); self.assertTrue(p['ok'])
        self.assertEqual(p['meter_id'],1011); self.assertEqual(p['apartment'],'Fixture D')

    def test_local_identify_unknown_is_review_not_guess(self):
        rc,p=self.run_cli('local','identify','--serial','999999')
        self.assertEqual(rc,2); self.assertFalse(p['ok'])
        self.assertEqual(p['status'],'REVIEW')
        self.assertIsNone(p['meter_id'])

class ReferenceBindingGuardCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.data=Path(self.tmp.name)/'data'
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            cli.main(['--data-root',str(self.data),'--inventory',str(INVENTORY),'init'])

    def run_cli(self,*args):
        out=io.StringIO()
        with contextlib.redirect_stdout(out):
            rc=cli.main(['--data-root',str(self.data),'--inventory',str(INVENTORY),*args])
        return rc,json.loads(out.getvalue())

    def test_reference_add_without_identity_proof_is_refused_before_file_access(self):
        rc,p=self.run_cli('reference','add','1007','/does/not/exist.jpg')
        self.assertEqual(rc,2)
        self.assertEqual(p['error'],'REFERENCE_BINDING_CONFIRMATION_REQUIRED')

    def test_reference_add_rejects_serial_belonging_to_other_meter(self):
        rc,p=self.run_cli('reference','add','1007','/does/not/exist.jpg','--observed-serial','TESTHW05')
        self.assertEqual(rc,2)
        self.assertEqual(p['error'],'REFERENCE_SERIAL_MISMATCH')
