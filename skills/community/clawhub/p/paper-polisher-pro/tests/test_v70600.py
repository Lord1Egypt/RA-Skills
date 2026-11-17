# -*- coding: utf-8 -*-
"""v7.6.0 契约测试（test_v70600）：安装完整性自证（清单+--deep 深检+双闸）。"""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"


class TestManifest(unittest.TestCase):
    def test_manifest_covers_all_data_and_reference_json(self):
        m = json.loads((PKG / "data" / "INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
        expected = {f"data/{p.name}" for p in (PKG / "data").glob("*.json")
                    if p.name != "INTEGRITY_MANIFEST.json"}
        expected |= {f"references/{p.name}" for p in (PKG / "references").glob("*.json")}
        self.assertEqual(set(m["files"].keys()), expected)

    def test_manifest_hashes_match(self):
        m = json.loads((PKG / "data" / "INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
        for rel, want in m["files"].items():
            got = hashlib.sha256((PKG / rel).read_bytes()).hexdigest()
            self.assertEqual(got, want["sha256"], f"{rel} 与清单不符")
            self.assertEqual((PKG / rel).stat().st_size, want["bytes"])

    def test_generator_reproduces(self):
        p = subprocess.run([sys.executable, str(PKG / "eval" / "gen_integrity_manifest.py")],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        m = json.loads((PKG / "data" / "INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(m["files"]), 14)


class TestDeepCheck(unittest.TestCase):
    def test_deep_passes_on_clean_tree(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp_doctor.py"), "--deep"],
                           capture_output=True, text=True, timeout=300)
        self.assertIn("完整性深检 --deep", p.stdout)
        self.assertIn("全部一致", p.stdout)
        self.assertIn("GREEN", p.stdout)

    def test_deep_catches_tampering(self):
        """截断/篡改场景：临时改一个清单在册文件 → --deep 给出精确文件名与哈希对。"""
        target = PKG / "references" / "term_variants.json"
        orig = target.read_bytes()
        try:
            target.write_bytes(orig[:-20])  # 模拟尾部截断
            p = subprocess.run([sys.executable, str(SCRIPTS / "pp_doctor.py"), "--deep"],
                               capture_output=True, text=True, timeout=300)
            self.assertIn("哈希不符", p.stdout)
            self.assertIn("term_variants.json", p.stdout)
            self.assertIn("期望", p.stdout)
        finally:
            target.write_bytes(orig)
        # 恢复后必须回绿（防测试自身污染）
        r2 = subprocess.run([sys.executable, str(SCRIPTS / "pp_doctor.py"), "--deep"],
                            capture_output=True, text=True, timeout=300)
        self.assertIn("全部一致", r2.stdout)


if __name__ == "__main__":
    unittest.main()
