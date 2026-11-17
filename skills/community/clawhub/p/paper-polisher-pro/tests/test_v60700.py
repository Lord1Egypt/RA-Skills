# -*- coding: utf-8 -*-
"""v6.7.0 契约测试（test_v60700）：场景目录单一来源 / scenarios 内建 / SKILL 场景化瘦身 / FAQ 分层。"""
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs
SCRIPTS = PKG / "scripts"


def _run(args, timeout=120):
    return subprocess.run([sys.executable] + args, capture_output=True,
                          text=True, timeout=timeout, encoding="utf-8",
                          errors="replace")


class TestScenarioCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((PKG / "references" / "scenarios.json")
                              .read_text(encoding="utf-8"))
        cls.scs = cls.data["scenarios"]

    def test_coverage_and_fields(self):
        self.assertGreaterEqual(len(self.scs), 17)
        for s in self.scs:
            for k in ("scene_zh", "scene_en", "when_zh", "when_en",
                      "cmd", "output_zh", "output_en", "tags"):
                self.assertTrue(s.get(k), f"{s.get('id')} 缺字段 {k}")

    def test_every_command_exists_in_commands(self):
        """场景目录里的 pp.py 子命令必须真实存在于 COMMANDS（防数据腐化）。"""
        src = (SCRIPTS / "pp.py").read_text(encoding="utf-8")
        for s in self.scs:
            cmd = s["cmd"]
            m = re.search(r"pp\.py ([a-z-]+)", cmd)
            if m:
                sub = m.group(1)
                if sub in ("quickstart", "tour", "scenarios", "test", "api",
                           "recommend", "faq"):
                    self.assertIn(f'"{sub}"', src, f"内建 {sub} 未接线")
                else:
                    self.assertIn(f'"{sub}": (', src, f"子命令 {sub} 不在 COMMANDS")

    def test_full_listing(self):
        # 数量动态断言（铁律：断言读运行时真值，绝不硬编码——v6.9.0 加第 18 场景时的教训）
        scs = json.loads((PKG / "references" / "scenarios.json")
                         .read_text(encoding="utf-8"))["scenarios"]
        n = len(scs)
        r = _run([str(SCRIPTS / "pp.py"), "scenarios"])
        self.assertEqual(r.returncode, 0, r.stderr[-200:])
        self.assertIn(f"场景目录（{n}/{n}", r.stdout)
        self.assertIn("什么时候用", r.stdout)
        self.assertIn("你会得到", r.stdout)

    def test_keyword_filter_compact_cjk(self):
        r = _run([str(SCRIPTS / "pp.py"), "scenarios", "测AI率"])
        self.assertIn("测 AI 率", r.stdout)
        r = _run([str(SCRIPTS / "pp.py"), "scenarios", "批量", "投稿"])
        self.assertIn("批量处理", r.stdout)
        self.assertIn("投稿前打包自查", r.stdout)

    def test_en_surface(self):
        env = dict(os.environ, PP_LANG="en")
        r = _run([str(SCRIPTS / "pp.py"), "scenarios"], timeout=120)
        r_en = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "scenarios"],
                              capture_output=True, text=True, timeout=120, env=env)
        self.assertIn("Scenario catalog", r_en.stdout)
        self.assertIn("When:", r_en.stdout)

    def test_recommend_routes_to_scenarios(self):
        r = _run([str(SCRIPTS / "pp.py"), "recommend", "什么时候用哪个命令"])
        self.assertIn("scenarios", r.stdout)

    def test_help_mentions_scenarios(self):
        r = _run([str(SCRIPTS / "pp.py")])
        self.assertIn("scenarios", r.stdout)


class TestQuickStartScenarioFirst(unittest.TestCase):
    def test_annotated_lines(self):
        """快速开始命令块内注释必须是「什么时候用」句式而非版本号堆叠。"""
        for f in _docs.DOCS:
            t = (PKG / f).read_text(encoding="utf-8")
            self.assertIn("scenarios", t)
            # 快速开始块内至少 8 条场景注解注释（# 开头）
            _anchor = ("Quick start" if ("Quick start" in t) else "快速开始")
            qs = t[t.index(_anchor):]
            block = qs[:qs.index("```", qs.index("```") + 3) if "```" in qs else 4000]
            comments = [x for x in block.split("\n") if x.strip().startswith("#")]
            self.assertGreaterEqual(len(comments), 8, f"{f} 快速开始注解不足")

    def test_slimmed(self):
        for f, cap in zip(_docs.DOCS, (308, 307) if _docs.HAS_ZH else (308,)):  # v7.7.0 契约节  # v7.6.0 完整性自证行  # v7.4.0 口径指针行  # v7.2~7.4 文档节累积放宽
            n = len((PKG / f).read_text(encoding="utf-8").split("\n"))
            self.assertLessEqual(n, cap, f"{f} 仍偏重（{n} 行 > {cap}）")


class TestFaqTiers(unittest.TestCase):
    def test_two_tiers_present(self):
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        self.assertIn("#### 用户高频", t)
        self.assertIn("#### 集成者与进阶", t)
        # 用户高频在前
        self.assertLess(t.index("#### 用户高频"), t.index("#### 集成者与进阶"))
        # 阅读分层注已同步
        self.assertIn("技术问答·用户高频", t)

    def test_content_preserved(self):
        """重组不得丢条目（熔断/补扫/证据/PDF/退出码/漂移全在）。"""
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        for q in ("「熔断」是什么", "批量里有几个文件失败了", "被质疑 AI 写作",
                  "为什么不支持 PDF", "退出码 0/1/2/3", "为什么我的分数和上次不一样"):
            self.assertIn(q, t)


if __name__ == "__main__":
    unittest.main()
