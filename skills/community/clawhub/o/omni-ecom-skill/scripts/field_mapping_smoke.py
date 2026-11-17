"""Tests for the native v2 platform field mapping registry."""
import json
import tempfile
import unittest
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "skills" / "ecom-diagnosis-core" / "scripts"
import sys
sys.path.insert(0, str(CORE))
from normalize_reports import AdapterError, MAPPING_FILE, load_mapping, mapping_index


class FieldMappingTests(unittest.TestCase):
    def payload(self):
        return json.loads(MAPPING_FILE.read_text(encoding="utf-8"))

    def write(self, payload):
        folder = tempfile.TemporaryDirectory()
        path = Path(folder.name) / "mapping.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return folder, path

    def test_actual_registry_is_native_v2_and_schema_valid(self):
        payload = self.payload()
        schema = json.loads((ROOT / "schemas" / "platform-field-mappings.schema.json").read_text(encoding="utf-8"))
        validate(payload, schema)
        self.assertIn("gmv", load_mapping())

    def test_legacy_mapping_identity_is_rejected(self):
        payload = self.payload(); payload["schema_version"] = "1.0"
        folder, path = self.write(payload)
        try:
            with self.assertRaisesRegex(AdapterError, "身份不是受支持"):
                load_mapping(path)
        finally:
            folder.cleanup()

    def test_invalid_alias_shape_is_rejected(self):
        payload = self.payload(); payload["aliases"]["gmv"] = []
        folder, path = self.write(payload)
        try:
            with self.assertRaisesRegex(AdapterError, "aliases 结构无效"):
                load_mapping(path)
        finally:
            folder.cleanup()

    def test_normalized_alias_collision_is_rejected(self):
        with self.assertRaisesRegex(AdapterError, "字段别名冲突"):
            mapping_index({"gmv": ["支付金额（元）"], "ad_spend": ["支付金额(元)"]})


if __name__ == "__main__":
    unittest.main()
