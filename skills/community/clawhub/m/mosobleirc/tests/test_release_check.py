from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("release_check_under_test", ROOT / "tools" / "release_check.py")
release_check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release_check)


class ReleaseCheckRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_runtime_variant_and_env_production_are_forbidden(self):
        (self.root / "config").mkdir()
        (self.root / "config" / "runtime.prod.json").write_text("{}", encoding="utf-8")
        (self.root / ".env.production").write_text("X=1", encoding="utf-8")
        errors = release_check.scan_root(self.root)
        self.assertTrue(any("runtime.prod.json" in x and "forbidden runtime file" in x for x in errors))
        self.assertTrue(any(".env.production" in x and "forbidden runtime file" in x for x in errors))

    def test_yandex_credentials_are_scanned_even_with_unknown_extension(self):
        secret = "AQV" + ("Z" * 28)
        (self.root / "notes.production").write_text("token=" + secret, encoding="utf-8")
        errors = release_check.scan_root(self.root)
        self.assertTrue(any("notes.production" in x and "Yandex API key" in x for x in errors))

    def test_embedded_url_credentials_are_detected(self):
        value = "https://" + "svc" + ":" + "verysecretpassword" + "@example.invalid/relay"
        (self.root / "custom.conf").write_text(value, encoding="utf-8")
        errors = release_check.scan_root(self.root)
        self.assertTrue(any("custom.conf" in x and "embedded credentials" in x for x in errors))


if __name__ == "__main__":
    unittest.main(verbosity=2)
