#!/usr/bin/env python3
"""Skill 包结构与入口链接的轻量回归测试。"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


class SkillPackageTests(unittest.TestCase):
    def test_required_metadata_is_present(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))
        frontmatter = content.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^name:\s*project-engineering\s*$")
        self.assertRegex(frontmatter, r"(?m)^description:\s*\S.+$")
        self.assertRegex(frontmatter, r"(?m)^license:\s*MIT-0\s*$")

    def test_skill_reference_links_resolve(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", content)
        relative_links = [link for link in links if "://" not in link and not link.startswith("#")]
        self.assertTrue(relative_links)
        for link in relative_links:
            with self.subTest(link=link):
                self.assertTrue((ROOT / link).is_file(), f"缺少引用文件：{link}")

    def test_greenfield_and_existing_modes_are_explicit(self) -> None:
        content = SKILL.read_text(encoding="utf-8")
        frontmatter = content.split("---", 2)[1]
        self.assertIn("`greenfield`", content)
        self.assertIn("`existing`", content)
        self.assertIn("references/greenfield.md", content)
        self.assertNotIn('"requires"', frontmatter)

        greenfield = (ROOT / "references" / "greenfield.md").read_text(encoding="utf-8")
        for status in ("已确认约束", "暂定假设", "待决策项", "已实现/已验证"):
            with self.subTest(status=status):
                self.assertIn(status, greenfield)

        discovery = (ROOT / "references" / "discovery.md").read_text(encoding="utf-8")
        delivery = (ROOT / "references" / "delivery.md").read_text(encoding="utf-8")
        self.assertIn("Git 可用", discovery)
        self.assertIn("具备 Python 3.10+", discovery)
        self.assertIn("不自动初始化 Git", delivery)


if __name__ == "__main__":
    unittest.main()
