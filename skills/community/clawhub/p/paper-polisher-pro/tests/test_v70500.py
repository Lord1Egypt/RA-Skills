# -*- coding: utf-8 -*-
"""v7.5.0 契约测试（test_v70500）：双形态验收对偶 / archive README 口径纪律 / 层级计数对齐。"""
import json
import re
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"

sys.path.insert(0, str(PKG / "tests"))
import _docs  # noqa: E402


class TestFormsRunner(unittest.TestCase):
    def test_script_exists_and_declares_both_forms(self):
        t = (PKG / "eval" / "verify_forms.py").read_text(encoding="utf-8")
        self.assertIn("--form", t)
        self.assertIn('"sh"', t) and self.assertIn('"ch"', t)
        self.assertIn("copytree", t)  # 副本隔离
        self.assertIn("O_EXCL", t)    # 锁序列化

    @unittest.skipUnless((PKG / "SKILL_ZH.md").is_file(),
                         "打包副本内无 SKILL_ZH.md：构造测试仅在 trunk 形态跑（防自递归）")
    def test_sh_form_builds_skillzh_as_skillmd(self):
        """SH 形态构造规则：SKILL.md=SKILL_ZH 内容（副本内断言，不动正本）。"""
        import shutil, tempfile
        sys.path.insert(0, str(PKG / "eval"))
        import verify_forms as vf
        tmp = Path(tempfile.mkdtemp(prefix="ppp7500_"))
        try:
            copy, tmpd = vf._make_form_copy("sh", None)
            try:
                self.assertFalse((copy / "SKILL_ZH.md").is_file())
                sk = (copy / "SKILL.md").read_text(encoding="utf-8")
                zh = _docs.zh_text(encoding="utf-8")  # 走助手（残留锁字面纪律）
                self.assertEqual(sk, zh)  # SKILL.md 即中文版
            finally:
                shutil.rmtree(tmpd, ignore_errors=True)
        finally:
            pass

    @unittest.skipUnless((PKG / "SKILL_ZH.md").is_file(),
                         "打包副本内无 SKILL_ZH.md：构造测试仅在 trunk 形态跑（防自递归）")
    def test_ch_form_removes_skillzh(self):
        import shutil, tempfile
        sys.path.insert(0, str(PKG / "eval"))
        import verify_forms as vf
        copy, tmpd = vf._make_form_copy("ch", None)
        try:
            self.assertFalse((copy / "SKILL_ZH.md").is_file())
            self.assertTrue((copy / "SKILL.md").is_file())
        finally:
            shutil.rmtree(tmpd, ignore_errors=True)


class TestArchiveDiscipline(unittest.TestCase):
    def test_readme_no_old_claim(self):
        t = (PKG / "eval" / "results" / "archive" / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("可复现基线", t)
        self.assertIn("CURRENT.md", t)
        self.assertIn("不可作为现行口径引用", t)

    def test_current_md_still_authoritative(self):
        t = (PKG / "eval" / "results" / "CURRENT.md").read_text(encoding="utf-8")
        self.assertIn("物理分层", t)


class TestLayerCount(unittest.TestCase):
    def test_skilljson_12layer_matches_map(self):
        d = json.loads((PKG / "skill.json").read_text(encoding="utf-8"))
        self.assertIn("12-layer", d["description"])
        sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("L12", sk)

    def test_form_note_refined(self):
        zh = _docs.zh_text(encoding="utf-8")
        self.assertIn("两种包形态共用同一套包内测试", zh)


if __name__ == "__main__":
    unittest.main()
