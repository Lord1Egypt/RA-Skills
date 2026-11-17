import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
RULES = ROOT / "references" / "zh-tw-copy-check.md"
CATALOG = ROOT / "references" / "workplace-meme-catalog.md"
TOP10 = ROOT / "references" / "top-10-sticker-copy-guide.md"
TEMPLATE = ROOT / "templates" / "line-sticker-prompt-template.md"
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"


class SkillPackageTests(unittest.TestCase):
    def test_required_files_exist(self):
        for path in (SKILL, README, RULES, CATALOG, TOP10, TEMPLATE, RELEASE_WORKFLOW, ROOT / "references" / "line-sticker-factory.md"):
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing required file: {path}")

    def test_skill_frontmatter_is_present(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        self.assertRegex(content, r"(?m)^name:\s*line-sticker-master\s*$")
        self.assertRegex(content, r"(?m)^description:\s*.+$")
        self.assertIn("zh-tw-copy-check.md", content)

    def test_workflow_mentions_twelve_panels_and_grid(self):
        content = SKILL.read_text(encoding="utf-8")
        self.assertRegex(content, r"(?i)4x3")
        self.assertRegex(content, r"12 格|12 張")
        self.assertIn("逐格", content)

    def test_traditional_chinese_rules_cover_daily_and_workplace(self):
        content = RULES.read_text(encoding="utf-8")
        required_terms = [
            "台灣常見用字",
            "日常用語",
            "職場梗",
            "同事",
            "主管",
            "客戶",
            "洩密",
            "歧視",
            "霸凌",
            "中性替代句",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_workplace_catalog_has_expansion_fields(self):
        content = CATALOG.read_text(encoding="utf-8")
        for term in ("類別", "趣味用語/迷因", "適用對象", "風險", "安全替代句", "擴充格式"):
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_top10_guide_has_ranked_copy_and_layout_fields(self):
        content = TOP10.read_text(encoding="utf-8")
        ranked_section = content.split("## 逐張", 1)[0]
        ranked_rows = re.findall(r"(?m)^\|\s*(?:[1-9]|10)\s*\|", ranked_section)
        self.assertEqual(len(ranked_rows), 10)
        for term in ("排版", "文字長度", "安全替代句", "前十名"):
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_prompt_template_is_copyable_and_parameterized(self):
        content = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("```text", content)
        for term in ("1480 × 960", "#00FF00", "[文案 1]", "[動作 12]", "負面提示詞", "不要使用任何 emoji"):
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_engineer_and_remote_rules_are_present(self):
        content = RULES.read_text(encoding="utf-8")
        for term in ("工程師與遠端工作專屬規則", "在我電腦可以", "PR 等你看", "金鑰不要貼群組", "你靜音了", "請勿錄影"):
            with self.subTest(term=term):
                self.assertIn(term, content)

    def test_release_workflow_requires_tests_and_semver(self):
        content = RELEASE_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("needs: test", content)
        self.assertIn("contents: write", content)
        self.assertIn("v[0-9]+\\.[0-9]+\\.[0-9]+", content)

    def test_examples_are_not_empty(self):
        content = README.read_text(encoding="utf-8")
        self.assertIn("line-sticker-factory", content)
        self.assertGreaterEqual(len(re.findall(r"```text", content)), 3)


if __name__ == "__main__":
    unittest.main()
