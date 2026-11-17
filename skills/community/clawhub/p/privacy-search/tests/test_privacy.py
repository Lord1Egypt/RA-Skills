#!/usr/bin/env python3
"""
F3 单测：隐私模式切换
"""

import unittest
import sys
import os

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from privacy import PrivacyManager, PrivacyConfig


class TestPrivacyManager(unittest.TestCase):
    """测试隐私管理器"""

    def test_default_mode_normal(self):
        config = {"privacy": {"default_mode": "normal"}}
        mgr = PrivacyManager(config)
        self.assertEqual(mgr.get_mode(), "normal")

    def test_default_mode_strict(self):
        config = {"privacy": {"default_mode": "strict"}}
        mgr = PrivacyManager(config)
        self.assertEqual(mgr.get_mode(), "strict")

    def test_set_mode_strict(self):
        config = {"privacy": {"default_mode": "normal"}}
        mgr = PrivacyManager(config)
        self.assertTrue(mgr.set_mode("strict"))
        self.assertEqual(mgr.get_mode(), "strict")

    def test_set_mode_invalid(self):
        config = {"privacy": {"default_mode": "normal"}}
        mgr = PrivacyManager(config)
        self.assertFalse(mgr.set_mode("ultra"))  # 无效模式

    def test_strict_allowed_engines(self):
        config = {
            "privacy": {
                "default_mode": "strict",
                "strict": {"allowed_engines": ["duckduckgo", "searxng"]},
            }
        }
        mgr = PrivacyManager(config)
        allowed = mgr.get_allowed_engines()
        self.assertIn("duckduckgo", allowed)
        self.assertIn("searxng", allowed)
        self.assertNotIn("baidu", allowed)

    def test_normal_all_engines(self):
        config = {
            "privacy": {
                "default_mode": "normal",
            },
            "search": {"default_engines": ["baidu", "bing", "duckduckgo", "searxng"]},
        }
        mgr = PrivacyManager(config)
        allowed = mgr.get_allowed_engines()
        self.assertIn("baidu", allowed)
        self.assertIn("bing", allowed)

    def test_blocked_engines_in_strict(self):
        config = {
            "privacy": {
                "default_mode": "strict",
                "strict": {"allowed_engines": ["duckduckgo", "searxng"]},
            }
        }
        mgr = PrivacyManager(config)
        blocked = mgr.get_blocked_engines()
        self.assertIn("baidu", blocked)
        self.assertIn("bing", blocked)
        self.assertNotIn("duckduckgo", blocked)

    def test_build_headers_strict(self):
        config = {
            "privacy": {
                "default_mode": "strict",
                "strict": {
                    "dnt": True,
                    "no_cookie": True,
                    "no_referrer": True,
                },
            }
        }
        mgr = PrivacyManager(config)
        headers = mgr.build_headers()
        self.assertEqual(headers.get("DNT"), "1")
        self.assertNotIn("Cookie", headers)

    def test_build_headers_normal(self):
        config = {"privacy": {"default_mode": "normal"}}
        mgr = PrivacyManager(config)
        headers = mgr.build_headers()
        # normal 模式不强制 DNT
        self.assertNotEqual(headers.get("DNT"), "1")

    def test_check_engine_allowed(self):
        config = {
            "privacy": {
                "default_mode": "strict",
                "strict": {"allowed_engines": ["duckduckgo", "searxng"]},
            }
        }
        mgr = PrivacyManager(config)
        self.assertTrue(mgr.check_engine_allowed("duckduckgo"))
        self.assertFalse(mgr.check_engine_allowed("baidu"))

    def test_generate_report(self):
        config = {
            "privacy": {
                "default_mode": "strict",
                "strict": {"allowed_engines": ["duckduckgo", "searxng"]},
            }
        }
        mgr = PrivacyManager(config)
        report = mgr.generate_report()
        self.assertEqual(report.mode, "strict")
        self.assertIsInstance(report.blocked_engines, list)
        self.assertIsInstance(report.recommendations, list)


class TestPrivacyConfig(unittest.TestCase):
    """测试隐私配置数据结构"""

    def test_default_values(self):
        cfg = PrivacyConfig()
        self.assertEqual(cfg.mode, "strict")
        self.assertTrue(cfg.dnt)
        self.assertTrue(cfg.no_cookie)
        self.assertTrue(cfg.no_referrer)


if __name__ == "__main__":
    unittest.main()
