# -*- coding: utf-8 -*-
"""v7.9.0 契约测试（test_v70900）：双清单分治 + 收包验收 + 打包闸语义锁。

背景（7.8.0 包评测 accuracy 4.5 实锤）：打包器曾把全包清单写进
data/INTEGRITY_MANIFEST.json 同名覆盖数据文件版——size 字段+全包范围与
gen_integrity_manifest 的 bytes 字段+仅数据 JSON 双语义冲突。v7.9.0 分治：
INTEGRITY=数据文件版（作者签发）；PACKAGE_MANIFEST=全包版（打包生成）；
pp_doctor --deep 双清单验收。

测试用独立 slug（paper-polisher-pro-selftest）驱动真实打包器，避免碰撞
真实发布暂存区 /tmp/pkg_paper-polisher-pro_*。
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"

sys.path.insert(0, str(PKG / "tests"))
import _docs  # noqa: E402


class TestManifestSeparation(unittest.TestCase):
    """trunk 侧：数据清单语义 + 不存在包清单（作者侧）。"""

    def test_integrity_manifest_is_data_semantics(self):
        m = json.loads((PKG / "data" / "INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
        files = m.get("files", {})
        self.assertGreaterEqual(len(files), 14)
        for rel, want in files.items():
            self.assertTrue(rel.startswith("data/") or rel.startswith("references/"),
                            f"数据清单混入非数据键: {rel}")
            self.assertIn("sha256", want)
            self.assertIn("bytes", want)  # v7.9.0 统一字段名（旧 size 与 doctor 消费不符）

    def test_no_package_manifest_in_trunk(self):
        self.assertFalse((PKG / "data" / "PACKAGE_MANIFEST.json").is_file(),
                         "trunk 作者侧不应有包清单（由打包器生成）")


class TestPackageReceipt(unittest.TestCase):
    """打包副本侧：真实打包器产物 → 双清单语义 + doctor 双验 + 篡改定位。

    ⚠ 仅 trunk 形态可跑：真实打包器要求双形态源（SKILL_ZH.md 必在），打包副本
    （SH/CH 两形态）无中文正本 → setUpClass 会 exit 2。副本形态的收包契约由
    打包闸（pkg_dual_lang 对账断言）覆盖。
    """

    @classmethod
    def setUpClass(cls):
        if not _docs.HAS_ZH:
            raise unittest.SkipTest("打包副本无 SKILL_ZH.md——真实打包器需双形态源")
        cls._tmp = tempfile.mkdtemp(prefix="ppp79_pkg_")
        cls.src = Path(cls._tmp) / "src"
        shutil.copytree(PKG, cls.src, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".pytest_cache"))
        cls.slug = "paper-polisher-pro-selftest"
        env = dict(__import__("os").environ, PKG_INCLUDE_TESTS="1")
        r = subprocess.run(["bash", str(Path.home() / "bin" / "pkg_dual_lang.sh"),
                            str(cls.src), cls.slug, "7.9.0"],
                           capture_output=True, text=True, timeout=600,
                           encoding="utf-8", errors="replace", env=env)
        if r.returncode != 0:
            raise AssertionError(f"pkg_dual_lang.sh 失败: {(r.stdout + r.stderr)[-400:]}")
        cls.pkg = Path("/tmp") / f"pkg_{cls.slug}_sh"

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._tmp, ignore_errors=True)
        shutil.rmtree(Path("/tmp") / f"pkg_{cls.slug}_sh", ignore_errors=True)
        shutil.rmtree(Path("/tmp") / f"pkg_{cls.slug}_claw", ignore_errors=True)

    def test_integrity_manifest_untouched_in_package(self):
        m = json.loads((self.pkg / "data" / "INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
        for rel in m.get("files", {}):
            self.assertTrue(rel.startswith("data/") or rel.startswith("references/"),
                            f"打包覆盖了数据清单语义: {rel}")

    def test_package_manifest_covers_all_shipped(self):
        m = json.loads((self.pkg / "data" / "PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
        files = m.get("files", {})
        self.assertIn("scripts/pp_api.py", files)
        self.assertIn("SKILL.md", files)
        self.assertIn("eval/doc_facts.py", files)
        for rel, want in files.items():
            self.assertFalse(rel.startswith("data/"), f"包清单混入 data/ 键: {rel}")
            self.assertIn("bytes", want)
        # 互补性：data/ 内零重叠
        integ = json.loads((self.pkg / "data" / "INTEGRITY_MANIFEST.json").read_text(encoding="utf-8"))
        overlap = set(files) & set(integ.get("files", {}))
        bad = [r for r in overlap if r.startswith("data/")]
        self.assertFalse(bad, f"data/ 内重叠: {bad[:3]}")

    def _deep(self):
        return subprocess.run([sys.executable, str(self.pkg / "scripts" / "pp_doctor.py"),
                               "--deep"], capture_output=True, text=True, timeout=600,
                              encoding="utf-8", errors="replace")

    def test_deep_verifies_both_manifests(self):
        p = self._deep()
        self.assertEqual(p.returncode, 0, (p.stdout + p.stderr)[-300:])
        self.assertIn("完整性深检 --deep", p.stdout)
        self.assertIn("包完整性验收 --deep", p.stdout)
        self.assertIn("GREEN", p.stdout)

    def test_tamper_pinpoints_file(self):
        """收包验收篡改矩阵：改 scripts 一处 → 包清单核对给出精确文件名。"""
        target = self.pkg / "scripts" / "pp_api.py"
        orig = target.read_bytes()
        try:
            target.write_bytes(orig + b"\n# tampered\n")
            p = self._deep()
            self.assertNotEqual(p.returncode, 0, "篡改后 --deep 必须 FAIL")
            self.assertIn("pp_api.py", p.stdout)
            self.assertIn("哈希不符", p.stdout)
        finally:
            target.write_bytes(orig)
        r2 = self._deep()
        self.assertEqual(r2.returncode, 0, "还原后必须回绿")


if __name__ == "__main__":
    unittest.main()
