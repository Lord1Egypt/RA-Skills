import json
import io
import re
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

from generator.paged_report import ReportValidationError, main, render_report


class RenderReportTests(unittest.TestCase):
    def setUp(self):
        self.data = {
            "family": "confirmation",
            "toc": True,
            "meta": {
                "language": "zh-CN",
                "title": "运费规则确认",
                "client": "ACME Corp",
                "category": "运营确认",
                "subtitle": "请确认以下规则调整",
                "date": "2026-09-07",
                "version": "v1.0",
                "footer": "ACME Corp · 运费确认 · 2026-09-07",
            },
            "pages": [
                {
                    "label": "规则与确认",
                    "sections": [
                        {
                            "id": "rules",
                            "title": "规则变更对比",
                            "components": [
                                {
                                    "type": "compare_table",
                                    "columns": ["项目", "变更前", "变更后"],
                                    "rows": [
                                        ["免运门槛", "$200", "$150"],
                                    ],
                                },
                                {
                                    "type": "callout",
                                    "variant": "amber",
                                    "label": "注意",
                                    "text": "请先完成测试订单。",
                                },
                            ],
                        },
                        {
                            "id": "checklist",
                            "title": "上线确认清单",
                            "components": [
                                {
                                    "type": "checklist",
                                    "items": [
                                        {"text": "后台规则已配置", "done": True},
                                        {"text": "客户确认邮件已发送", "done": False},
                                    ],
                                },
                                {"type": "tag", "variant": "green", "text": "已完成"},
                                {"type": "kpi", "value": "3", "unit": "笔测试订单"},
                                {"type": "progress", "variant": "green", "value": 75},
                                {"type": "status_row", "label": "数据", "status": "已补全", "variant": "green"},
                                {
                                    "type": "grid",
                                    "columns": 2,
                                    "cards": [{"title": "规则", "body": "按地区配置。"}],
                                },
                                {"type": "divider"},
                            ],
                        },
                    ],
                }
            ],
        }

    def test_render_report_builds_self_contained_html(self):
        html = render_report(self.data)

        self.assertTrue(html.startswith("<!DOCTYPE html>"))
        self.assertIn('<html lang="zh-CN">', html)
        self.assertIn('<title>运费规则确认</title>', html)
        self.assertIn("--accent: #1f4e5f", html)
        self.assertIn('class="report-page cover"', html)
        self.assertIn('id="rules"', html)
        self.assertIn('href="#rules"', html)
        self.assertIn('class="compare-table"', html)
        self.assertIn('class="callout amber"', html)
        self.assertIn('class="checklist"', html)
        self.assertIn('class="progress-bar green"', html)
        self.assertIn('class="status-row"', html)
        self.assertIn('class="grid two"', html)
        self.assertNotIn("<link ", html)
        self.assertNotIn("<script", html)

    def test_render_report_adds_print_boundary_guard(self):
        html = render_report(self.data)

        self.assertIn(".report-page { box-shadow: none; border: 0; padding: 0 4mm; margin: 0; min-height: auto; page-break-after: always; }", html)
        self.assertIn(".page-label, .footer { padding-left: 4mm; padding-right: 4mm; }", html)

    def test_render_report_escapes_text(self):
        data = json.loads(json.dumps(self.data))
        data["meta"]["title"] = '<Unsafe & "title">'
        data["pages"][0]["sections"][0]["components"][1]["text"] = "<b>not markup</b>"

        html = render_report(data)

        self.assertIn("&lt;Unsafe &amp; &quot;title&quot;&gt;", html)
        self.assertIn("&lt;b&gt;not markup&lt;/b&gt;", html)
        self.assertNotIn("<b>not markup</b>", html)

    def test_render_report_rejects_unknown_family(self):
        data = json.loads(json.dumps(self.data))
        data["family"] = "invoice"

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_rejects_invalid_progress_value(self):
        data = json.loads(json.dumps(self.data))
        data["pages"][0]["sections"][1]["components"][3]["value"] = 101

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_rejects_string_boolean_flags(self):
        data = json.loads(json.dumps(self.data))
        data["toc"] = "false"

        with self.assertRaises(ReportValidationError):
            render_report(data)

        data = json.loads(json.dumps(self.data))
        data["pages"][0]["sections"][1]["components"][0]["items"][0]["done"] = "false"

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_uses_english_toc_label(self):
        data = json.loads(json.dumps(self.data))
        data["meta"]["language"] = "en"

        html = render_report(data)

        self.assertIn(">Contents<", html)
        self.assertNotIn(">目录<", html)

    def test_render_report_rejects_style_terminator_in_custom_css(self):
        with self.assertRaises(ReportValidationError):
            render_report(self.data, css="body{}</style><script>marker</script>")

    def test_render_report_rejects_external_css_imports_and_urls(self):
        css_cases = [
            "@import 'https://cdn.example.com/report.css';",
            ".hero { background-image: url(https://cdn.example.com/hero.png); }",
            ".hero { background-image: url('images/hero.png'); }",
            r".hero { background-image: u\72l(https://cdn.example.com/hero.png); }",
            r"@im\70ort 'https://cdn.example.com/report.css';",
            r".hero { background-image: u\000072l(https://cdn.example.com/hero.png); }",
            ".hero { background-image: u/**/rl(https://cdn.example.com/hero.png); }",
            "@im/**/port 'https://cdn.example.com/report.css';",
            r"@im\70/**/ort 'https://cdn.example.com/report.css';",
        ]

        for css in css_cases:
            with self.subTest(css=css):
                with self.assertRaises(ReportValidationError):
                    render_report(self.data, css=css)

    def test_render_report_rejects_unknown_checklist_item_fields(self):
        data = json.loads(json.dumps(self.data))
        item = data["pages"][0]["sections"][1]["components"][0]["items"][0]
        item["unexpected"] = "拒绝"

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_rejects_unknown_grid_card_fields(self):
        data = json.loads(json.dumps(self.data))
        card = data["pages"][0]["sections"][1]["components"][5]["cards"][0]
        card["unexpected"] = "拒绝"

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_rejects_unhashable_grid_columns(self):
        data = json.loads(json.dumps(self.data))
        data["pages"][0]["sections"][1]["components"][5]["columns"] = []

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_rejects_whitespace_only_required_text(self):
        cases = []

        meta_title = json.loads(json.dumps(self.data))
        meta_title["meta"]["title"] = " \t\n"
        cases.append(("meta.title", meta_title))

        section_title = json.loads(json.dumps(self.data))
        section_title["pages"][0]["sections"][0]["title"] = " \t\n"
        cases.append(("section.title", section_title))

        callout_text = json.loads(json.dumps(self.data))
        callout_text["pages"][0]["sections"][0]["components"][1]["text"] = " \t\n"
        cases.append(("callout.text", callout_text))

        tag_text = json.loads(json.dumps(self.data))
        tag_text["pages"][0]["sections"][1]["components"][1]["text"] = " \t\n"
        cases.append(("tag.text", tag_text))

        status_label = json.loads(json.dumps(self.data))
        status_label["pages"][0]["sections"][1]["components"][4]["label"] = " \t\n"
        cases.append(("status_row.label", status_label))

        status_value = json.loads(json.dumps(self.data))
        status_value["pages"][0]["sections"][1]["components"][4]["status"] = " \t\n"
        cases.append(("status_row.status", status_value))

        checklist_text = json.loads(json.dumps(self.data))
        checklist_text["pages"][0]["sections"][1]["components"][0]["items"][0]["text"] = " \t\n"
        cases.append(("checklist.items[].text", checklist_text))

        grid_title = json.loads(json.dumps(self.data))
        grid_title["pages"][0]["sections"][1]["components"][5]["cards"][0]["title"] = " \t\n"
        cases.append(("grid.cards[].title", grid_title))

        table_tag_text = json.loads(json.dumps(self.data))
        table_tag_text["pages"][0]["sections"][0]["components"] = [
            {
                "type": "table",
                "columns": ["状态"],
                "rows": [[{"tag": {"text": " \t\n", "variant": "green"}}]],
            }
        ]
        cases.append(("tableCell.tag.text", table_tag_text))

        for field, case in cases:
            with self.subTest(field=field):
                with self.assertRaises(ReportValidationError):
                    render_report(case)

    def test_schema_marks_required_text_fields_as_non_whitespace(self):
        schema_path = Path(__file__).resolve().parents[1] / "schemas" / "report.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        definitions = schema["$defs"]
        required_text_schemas = {
            "meta.title": definitions["meta"]["properties"]["title"],
            "section.title": definitions["section"]["properties"]["title"],
            "tableTag.text": definitions["tableTag"]["properties"]["text"],
            "callout.text": definitions["callout"]["properties"]["text"],
            "tag.text": definitions["tag"]["properties"]["text"],
            "statusRow.label": definitions["statusRow"]["properties"]["label"],
            "statusRow.status": definitions["statusRow"]["properties"]["status"],
            "checklist.items[].text": definitions["checklist"]["properties"]["items"]["items"]["properties"]["text"],
            "grid.cards[].title": definitions["grid"]["properties"]["cards"]["items"]["properties"]["title"],
        }

        for field, text_schema in required_text_schemas.items():
            with self.subTest(field=field):
                self.assertEqual(text_schema.get("minLength"), 1)
                self.assertEqual(
                    text_schema.get("pattern"),
                    r"^(?![\u0009-\u000d\u001c-\u001f\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]*$)[\s\S]+$",
                )

        pattern = required_text_schemas["meta.title"]["pattern"]
        self.assertIsNotNone(re.search(pattern, "line one\nline two"))
        self.assertIsNone(re.search(pattern, "\u0085"))

    def test_render_report_emits_accessibility_semantics(self):
        html = render_report(self.data)

        self.assertIn(
            '<th scope="col">项目</th><th scope="col">变更前</th><th scope="col">变更后</th>',
            html,
        )
        self.assertIn(
            '<div class="progress-bar green" role="progressbar" aria-label="75%" aria-valuemin="0" aria-valuemax="100" aria-valuenow="75">',
            html,
        )
        self.assertIn(
            '<li role="checkbox" aria-checked="true" class="done">后台规则已配置</li>',
            html,
        )
        self.assertIn(
            '<li role="checkbox" aria-checked="false">客户确认邮件已发送</li>',
            html,
        )

    def test_render_report_matches_strict_contract(self):
        cases = []

        extra = json.loads(json.dumps(self.data))
        extra["unexpected"] = True
        cases.append(extra)

        numeric_title = json.loads(json.dumps(self.data))
        numeric_title["meta"]["title"] = 123
        cases.append(numeric_title)

        null_toc = json.loads(json.dumps(self.data))
        null_toc["toc"] = None
        cases.append(null_toc)

        for case in cases:
            with self.subTest(case=case):
                with self.assertRaises(ReportValidationError):
                    render_report(case)

    def test_render_report_wraps_tag_cells_in_table_cells(self):
        data = json.loads(json.dumps(self.data))
        data["pages"][0]["sections"][0]["components"] = [
            {
                "type": "table",
                "columns": ["状态"],
                "rows": [[{"tag": {"text": "已完成", "variant": "green"}}]],
            }
        ]

        html = render_report(data)

        self.assertIn('<tr><td><span class="tag green">已完成</span></td></tr>', html)
        self.assertNotIn('<tr><span class="tag green">', html)

    def test_render_report_rejects_unknown_table_cell_fields(self):
        data = json.loads(json.dumps(self.data))
        data["pages"][0]["sections"][0]["components"][0]["rows"] = [
            [{"text": "免运门槛", "unexpected": "拒绝"}, "$200", "$150"]
        ]

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_render_report_rejects_duplicate_section_ids(self):
        data = json.loads(json.dumps(self.data))
        data["pages"][0]["sections"][1]["id"] = "rules"

        with self.assertRaises(ReportValidationError):
            render_report(data)

    def test_cli_writes_html_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "report.json"
            target = root / "report.html"
            source.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")

            exit_code = main([str(source), "-o", str(target)])

            self.assertEqual(exit_code, 0)
            self.assertTrue(target.exists())
            self.assertIn("运费规则确认", target.read_text(encoding="utf-8"))

    def test_cli_reports_output_path_errors_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "report.json"
            target_dir = root / "report.html"
            source.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
            target_dir.mkdir()
            stderr = io.StringIO()

            with redirect_stderr(stderr):
                exit_code = main([str(source), "-o", str(target_dir)])

            self.assertEqual(exit_code, 2)
            self.assertIn("paged-report:", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
