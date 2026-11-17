#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级检索语法解析测试（V1.8 新增）
覆盖：时间限定、站点限定、文件类型、bangs、引擎兼容性、本地过滤
"""

import os
import sys
import unittest

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestQueryParser(unittest.TestCase):
    """语法解析"""

    def test_parse_site(self):
        from query_parser import parse_query
        clean, sf = parse_query("python教程 site:github.com")
        self.assertEqual(clean, "python教程")
        self.assertEqual(sf.site, "github.com")

    def test_parse_filetype(self):
        from query_parser import parse_query
        clean, sf = parse_query("报告 filetype:pdf")
        self.assertEqual(clean, "报告")
        self.assertEqual(sf.filetype, "pdf")

    def test_parse_after_year(self):
        from query_parser import parse_query
        clean, sf = parse_query("AI新闻 after:2024")
        self.assertEqual(clean, "AI新闻")
        self.assertEqual(sf.after, "2024")

    def test_parse_after_full_date(self):
        from query_parser import parse_query
        clean, sf = parse_query("新闻 after:2024-06-15")
        self.assertEqual(sf.after, "2024-06-15")

    def test_parse_before(self):
        from query_parser import parse_query
        clean, sf = parse_query("历史 before:2020")
        self.assertEqual(clean, "历史")
        self.assertEqual(sf.before, "2020")

    def test_parse_bang(self):
        from query_parser import parse_query
        clean, sf = parse_query("!w 量子计算")
        self.assertEqual(clean, "量子计算")
        self.assertEqual(sf.bang, "!w")

    def test_parse_combined(self):
        from query_parser import parse_query
        clean, sf = parse_query("量子计算 site:mit.edu after:2024")
        self.assertEqual(clean, "量子计算")
        self.assertEqual(sf.site, "mit.edu")
        self.assertEqual(sf.after, "2024")

    def test_parse_no_syntax(self):
        from query_parser import parse_query
        clean, sf = parse_query("普通搜索词")
        self.assertEqual(clean, "普通搜索词")
        self.assertFalse(sf.has_filters)

    def test_parse_empty_query(self):
        from query_parser import parse_query
        clean, sf = parse_query("")
        self.assertEqual(clean, "")
        self.assertFalse(sf.has_filters)


class TestEngineCapabilities(unittest.TestCase):
    """引擎兼容性"""

    def test_baidu_supports_site(self):
        from query_parser import engine_supports_syntax
        self.assertTrue(engine_supports_syntax("baidu", "site"))

    def test_bing_supports_filetype(self):
        from query_parser import engine_supports_syntax
        self.assertTrue(engine_supports_syntax("bing", "filetype"))

    def test_qwant_not_supports_site(self):
        from query_parser import engine_supports_syntax
        self.assertFalse(engine_supports_syntax("qwant", "site"))

    def test_searxng_supports_time(self):
        from query_parser import engine_supports_syntax
        self.assertTrue(engine_supports_syntax("searxng", "after"))

    def test_get_unsupported(self):
        from query_parser import get_unsupported_syntax, parse_query
        _, sf = parse_query("test site:example.com filetype:pdf")
        unsupported = get_unsupported_syntax("qwant", sf)
        self.assertIn("site", unsupported)
        self.assertIn("filetype", unsupported)


class TestLocalFiltering(unittest.TestCase):
    """本地过滤"""

    def test_filter_by_site(self):
        from query_parser import filter_results_locally, parse_query
        _, sf = parse_query("test site:example.com")
        results = [
            SimpleNamespace(url="https://example.com/a"),
            SimpleNamespace(url="https://other.com/b"),
        ]
        filtered, notices = filter_results_locally(results, sf, "qwant")
        self.assertEqual(len(filtered), 1)
        self.assertIn("example.com", filtered[0].url)

    def test_filter_by_filetype(self):
        from query_parser import filter_results_locally, parse_query
        _, sf = parse_query("test filetype:pdf")
        results = [
            SimpleNamespace(url="https://a.com/doc.pdf"),
            SimpleNamespace(url="https://b.com/page.html"),
        ]
        filtered, notices = filter_results_locally(results, sf, "qwant")
        self.assertEqual(len(filtered), 1)

    def test_filter_no_syntax_returns_original(self):
        from query_parser import filter_results_locally, parse_query
        _, sf = parse_query("普通词")
        results = [SimpleNamespace(url="https://a.com")]
        filtered, notices = filter_results_locally(results, sf, "baidu")
        self.assertEqual(len(filtered), 1)


class TestSyntaxTable(unittest.TestCase):
    """语法表输出"""

    def test_syntax_table_contains_advanced(self):
        from query_parser import get_query_syntax_table
        table = get_query_syntax_table()
        self.assertIn("after:", table)
        self.assertIn("site:", table)
        self.assertIn("filetype:", table)

    def test_syntax_table_contains_bangs(self):
        from query_parser import get_query_syntax_table
        table = get_query_syntax_table()
        self.assertIn("!w", table)
        self.assertIn("bangs", table.lower())


# 用于本地过滤测试的 SimpleNamespace
from types import SimpleNamespace


if __name__ == "__main__":
    unittest.main(verbosity=2)
