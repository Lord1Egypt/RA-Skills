#!/usr/bin/env python3
"""Tests for the frozen template and generated-deck contract."""

from __future__ import annotations

import unittest
from pathlib import Path

from validate_deck import (
    EXPECTED_SHELL_SHA256,
    EXPECTED_STYLE_SHA256,
    extract_style,
    shell_sha256,
    style_sha256,
    validate_html,
)

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_ROOT / "assets" / "template.html"


class TemplateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = TEMPLATE.read_text(encoding="utf-8")

    def test_template_exists(self) -> None:
        self.assertTrue(TEMPLATE.is_file())

    def test_template_passes_its_contract(self) -> None:
        report = validate_html(
            self.html,
            source="template.html",
            allow_placeholders=True,
        )
        self.assertEqual(report["errors"], [], msg="\n".join(report["errors"]))

    def test_style_matches_original_ppt_snapshot(self) -> None:
        self.assertEqual(
            style_sha256(extract_style(self.html)),
            EXPECTED_STYLE_SHA256,
        )

    def test_shell_matches_frozen_snapshot(self) -> None:
        self.assertEqual(shell_sha256(self.html), EXPECTED_SHELL_SHA256)


class GeneratedDeckContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.template = TEMPLATE.read_text(encoding="utf-8")

    def validate(self, html: str) -> list[str]:
        return validate_html(
            html,
            source="generated.html",
            template_html=self.template,
        )["errors"]

    def completed(self, html: str) -> str:
        return html.replace("[必填]", "完成")

    def test_allows_changes_in_declared_slots(self) -> None:
        html = self.completed(self.template)
        html = html.replace("<title>完成 替换为 PPT 标题</title>", "<title>新主题</title>")
        html = html.replace("完成 替换为标题", "新主题标题")
        html = html.replace(
            "// ANIMATIONS_START",
            "// ANIMATIONS_START\nanims.demo = async () => {};",
        )
        self.assertEqual(self.validate(html), [])

    def test_rejects_unfinished_placeholders(self) -> None:
        errors = self.validate(self.template)
        self.assertTrue(any("placeholder" in error for error in errors), errors)

    def test_rejects_runtime_changes(self) -> None:
        html = self.completed(self.template).replace("const sleep=", "const pause=", 1)
        errors = self.validate(html)
        self.assertTrue(any("template shell" in error for error in errors), errors)

    def test_rejects_invented_classes(self) -> None:
        html = self.completed(self.template).replace(
            'class="panel"', 'class="panel ai-redesign"', 1
        )
        errors = self.validate(html)
        self.assertTrue(any("unknown class .ai-redesign" in error for error in errors), errors)

    def test_requires_title_and_notes_on_every_slide(self) -> None:
        html = self.completed(self.template).replace(' data-title="要点"', "", 1)
        html = html.replace(
            '<aside class="notes">这一页', '<aside class="speaker">这一页', 1
        )
        errors = self.validate(html)
        self.assertTrue(any("missing data-title" in error for error in errors), errors)
        self.assertTrue(any('missing <aside class="notes">' in error for error in errors), errors)

    def test_rejects_executable_html_inside_slides(self) -> None:
        html = self.completed(self.template).replace(
            "</h2>", '</h2><img src="x" onerror="alert(1)">', 1
        )
        errors = self.validate(html)
        self.assertTrue(any("executable HTML" in error for error in errors), errors)

    def test_rejects_unapproved_inline_style_properties(self) -> None:
        html = self.completed(self.template).replace(
            'style="flex:1"',
            'style="flex:1;background:linear-gradient(red, blue)"',
            1,
        )
        errors = self.validate(html)
        self.assertTrue(any("inline style property background" in error for error in errors), errors)

    def test_rejects_unapproved_inline_font_sizes(self) -> None:
        html = self.completed(self.template).replace("font-size:22px", "font-size:16px", 1)
        errors = self.validate(html)
        self.assertTrue(any("inline font-size 16px" in error for error in errors), errors)

    def test_rejects_unapproved_inline_colors(self) -> None:
        html = self.completed(self.template).replace(
            "font-size:22px;color:var(--ink2)",
            "font-size:22px;color:#ff00ff",
            1,
        )
        errors = self.validate(html)
        self.assertTrue(any("inline color #ff00ff" in error for error in errors), errors)

    def test_rejects_more_than_one_callout_per_slide(self) -> None:
        html = self.completed(self.template).replace(
            '<div class="callout">结论写在 callout 里，一句话，不要变成第三段正文。</div>',
            '<div class="callout">一。</div><div class="callout">二。</div>',
            1,
        )
        errors = self.validate(html)
        self.assertTrue(any("more than 1 callout" in error for error in errors), errors)

    def test_rejects_more_than_four_points_per_slide(self) -> None:
        html = self.completed(self.template).replace(
            "</ul>",
            '<li><span class="n">4</span><span>四。</span></li>'
            '<li><span class="n">5</span><span>五。</span></li></ul>',
            1,
        )
        errors = self.validate(html)
        self.assertTrue(any("more than 4 .pts items" in error for error in errors), errors)

    def test_requires_exactly_one_main_title_per_slide(self) -> None:
        html = self.completed(self.template).replace(
            "<h2>用一句结论当标题，不要用「概述」</h2>",
            "<h2>结论一</h2><h2>结论二</h2>",
            1,
        )
        errors = self.validate(html)
        self.assertTrue(any("exactly 1 h1/h2" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
