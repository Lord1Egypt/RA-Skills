# -*- coding: utf-8 -*-
"""v7.7.0 契约测试（test_v70700）：输出契约 Schema / 生成器单一来源 / SDK 对齐收官。"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(PKG / "tests"))
import _docs  # noqa: E402


class TestSchemas(unittest.TestCase):
    def test_four_schemas_parse_and_declare(self):
        for name in ("detect", "fix_suggest", "workflow", "term_report"):
            d = json.loads((PKG / "schemas" / f"{name}.schema.json").read_text(encoding="utf-8"))
            self.assertIn("$schema", d)
            self.assertIn("required", d)
            self.assertIn("properties", d)

    def test_validator_selfcheck_passes(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp_schema.py"), "--selfcheck"],
                           capture_output=True, text=True, timeout=300, encoding="utf-8")
        self.assertEqual(p.returncode, 0, p.stdout[-300:])
        self.assertIn("PASS（4/4）", p.stdout)

    def test_validator_rejects_unknown_keyword(self):
        sys.path.insert(0, str(SCRIPTS))
        import pp_schema
        with self.assertRaises(pp_schema.SchemaError):
            pp_schema.validate({}, {"patternProperties": {}})

    def test_validator_catches_violations(self):
        sys.path.insert(0, str(SCRIPTS))
        import pp_schema
        schema = {"type": "object", "required": ["a"], "properties": {"a": {"type": "integer", "minimum": 1}}}
        with self.assertRaises(pp_schema.SchemaError):
            pp_schema.validate({"a": 0}, schema)      # minimum 违规
        with self.assertRaises(pp_schema.SchemaError):
            pp_schema.validate({}, schema)             # 缺必填
        pp_schema.validate({"a": 5}, schema)           # 合法不抛


class TestManifestClosure(unittest.TestCase):
    def test_generated_reads_skilljson(self):
        t = (PKG / "eval" / "gen_integrity_manifest.py").read_text(encoding="utf-8")
        self.assertIn('skill.json', t)
        self.assertNotIn('"generated": "7.6.0"', t)  # 硬编码版本串已清

    def test_check_mode_byte_compare(self):
        p = subprocess.run([sys.executable, str(PKG / "eval" / "gen_integrity_manifest.py"), "--check"],
                           capture_output=True, text=True, timeout=120)
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        self.assertIn("逐字节一致", p.stdout)


class TestSdkParity(unittest.TestCase):
    def test_trend_data(self):
        import pp_api, glob
        files = sorted(glob.glob(str(PKG / "examples" / "**" / "*.workflow.json"), recursive=True))
        if not files:
            self.skipTest("无随包 workflow JSON")
        runs = pp_api.trend_data(files[:1])
        self.assertGreaterEqual(len(runs), 1)
        self.assertIn("file", runs[0])

    def test_trend_data_input_validation(self):
        import pp_api
        with self.assertRaises(ValueError):
            pp_api.trend_data([])

    def test_schema_selfcheck_sdk(self):
        import pp_api
        r = pp_api.schema_selfcheck()
        self.assertTrue(r["ok"])
        self.assertEqual(set(r["results"].keys()),
                         {"detect", "fix_suggest", "workflow", "term_report"})

    def test_pp_help_documents_schema(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py")],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("schema", p.stdout)

    def test_skill_documents_contract_section(self):
        import _docs
        # SKILL.md（任一形态必在）
        sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("schema --selfcheck", sk)
        self.assertIn("schemas/", sk)
        # SKILL_ZH.md 仅双语 trunk 形态在位（打包副本走 _docs 自适应 skip）
        zh = _docs.zh_text(encoding="utf-8")
        self.assertIn("schema --selfcheck", zh)


if __name__ == "__main__":
    unittest.main()
