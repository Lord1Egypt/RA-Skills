import json
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.manifest import build_manifest, verify_manifest
from novelforge_engine.engine import EngineValidationError, load_engine


class ManifestTests(unittest.TestCase):
    def test_manifest_records_and_verifies_embedded_engine_hashes(self):
        root = SKILL_ROOT / "engines" / "jin-yong"
        manifest = build_manifest(root)
        self.assertEqual(manifest["engine"], "jin-yong")
        self.assertTrue(all(len(value) == 64 for value in manifest["files"].values()))
        self.assertTrue(verify_manifest(root, manifest))

    def test_manifest_detects_tampered_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "engine.json").write_text(json.dumps({"id": "demo", "version": 1, "card_files": []}), encoding="utf-8")
            manifest = build_manifest(root)
            (root / "engine.json").write_text("tampered", encoding="utf-8")
            self.assertFalse(verify_manifest(root, manifest))

    def test_engine_rejects_invalid_existing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "engine.json").write_text(json.dumps({"id": "demo", "version": 1, "card_files": []}), encoding="utf-8")
            (root / "manifest.json").write_text(json.dumps({"schema": 1, "engine": "demo", "files": {"engine.json": "bad"}}), encoding="utf-8")
            with self.assertRaises(EngineValidationError):
                load_engine(root)


if __name__ == "__main__":
    unittest.main()
