import importlib.util
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

SPEC = importlib.util.spec_from_file_location("release_version", Path(__file__).resolve().parents[1] / "scripts/check_release_version.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReleaseVersionTests(unittest.TestCase):
    def test_core_version_must_match_checkout_and_reject_plugin_tags(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text('version = "0.16.1"\n', encoding="utf-8")
            for valid in ("v0.16.1", "0.16.1"):
                self.assertEqual(MODULE.check_version(valid, root), "0.16.1")
            for invalid in ("dsh-v0.2.1", "0.16.0", "vgarbage", "0.16.1\nmalformed"):
                with self.assertRaises(ValueError):
                    MODULE.check_version(invalid, root)
