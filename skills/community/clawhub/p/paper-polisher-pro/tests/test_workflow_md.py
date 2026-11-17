# -*- coding: utf-8 -*-
"""workflow Markdown 报告契约：节号/固定内容/页脚一次性。"""
import unittest

try:
    from tests._common import AI_TEXT
except ImportError:  # 直跑模式（-s tests）
    from _common import AI_TEXT
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import pp_workflow  # noqa: E402


class TestWorkflowMarkdown(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = pp_workflow.workflow(AI_TEXT)
        cls.md = pp_workflow.to_markdown(cls.r)

    def test_all_sections_numbered(self):
        for i, name in [(1, "段落级归因"), (2, "四层降AI门禁"), (3, "句子级改写建议"),
                        (4, "术语保护"), (5, "翻译腔"), (6, "文体距离"),
                        (7, "质量报告"), (8, "AIGC 合规标识自查")]:
            self.assertIn("## %d. %s" % (i, name), self.md, f"缺节: {i}. {name}")

    def test_fix_block_has_chinese_labels(self):
        self.assertIn("特征分布：", self.md)
        self.assertNotIn("filler×", self.md, "MD 报告不应出现英文 type 键")

    def test_star_footer_once(self):
        self.assertEqual(self.md.count("Star / 收藏"), 1)

    def test_json_serializable(self):
        import json
        s = json.dumps(self.r, ensure_ascii=False)
        self.assertIn("fix_suggest", s)


if __name__ == "__main__":
    unittest.main()
