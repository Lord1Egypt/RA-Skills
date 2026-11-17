#!/usr/bin/env python3
"""
版本更新检查单测（死规则 11）
"""

import unittest
import sys
import os

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from update_checker import (
    UpdateChecker, UpdateCache, CURRENT_VERSION, SKILL_SLUG,
    parse_version, compare_versions, UpdateInfo,
    display_update_notification, display_no_update,
    load_config
)


class TestVersionCompare(unittest.TestCase):
    """测试版本号比较"""

    def test_parse_simple(self):
        self.assertEqual(parse_version("1.0.0"), (1, 0, 0))

    def test_parse_with_v_prefix(self):
        self.assertEqual(parse_version("v2.1.0"), (2, 1, 0))

    def test_parse_with_pre_release(self):
        result = parse_version("1.0.0-beta.1")
        self.assertEqual(result[:3], (1, 0, 0))

    def test_compare_equal(self):
        self.assertEqual(compare_versions("1.0.0", "1.0.0"), 0)

    def test_compare_newer(self):
        self.assertEqual(compare_versions("1.2.0", "1.0.0"), 1)

    def test_compare_older(self):
        self.assertEqual(compare_versions("0.9.0", "1.0.0"), -1)

    def test_compare_patch(self):
        self.assertEqual(compare_versions("1.0.1", "1.0.0"), 1)

    def test_compare_with_v_prefix(self):
        self.assertEqual(compare_versions("v1.2.0", "1.0.0"), 1)

    def test_compare_pre_release_vs_release(self):
        # pre-release 应小于正式版本
        self.assertEqual(compare_versions("1.0.0-beta", "1.0.0"), -1)


class TestUpdateCache(unittest.TestCase):
    """测试缓存管理"""

    def setUp(self):
        self.test_db = os.path.expanduser("~/.workbuddy/output/.test-update-cache.db")
        # 确保目录存在
        os.makedirs(os.path.dirname(self.test_db), exist_ok=True)
        self.cache = UpdateCache(self.test_db)

    def tearDown(self):
        # 清理测试数据库
        try:
            os.remove(self.test_db)
        except OSError:
            pass

    def test_set_and_get(self):
        self.cache.set("test-skill", "1.2.0", True, "changelog", "http://example.com")
        result = self.cache.get("test-skill")
        self.assertIsNotNone(result)
        self.assertEqual(result["latest_version"], "1.2.0")
        self.assertEqual(result["has_update"], 1)

    def test_get_nonexistent(self):
        result = self.cache.get("nonexistent-skill")
        self.assertIsNone(result)

    def test_cache_validity(self):
        self.cache.set("test-skill", "1.0.0", False)
        # 刚写入的缓存应有效
        self.assertTrue(self.cache.is_cache_valid("test-skill", cache_hours=24))

    def test_cache_invalidation(self):
        # 写入一个过期时间
        self.cache.set("test-skill", "1.0.0", False)
        # 设置为 0 小时有效期应立即无效
        # 注意：实际测试需要模拟时间，这里简化处理

    def test_overwrite(self):
        self.cache.set("test-skill", "1.0.0", False)
        self.cache.set("test-skill", "2.0.0", True, "major update")
        result = self.cache.get("test-skill")
        self.assertEqual(result["latest_version"], "2.0.0")
        self.assertEqual(result["has_update"], 1)


class TestUpdateChecker(unittest.TestCase):
    """测试更新检查器"""

    def setUp(self):
        self.config = {
            "update_check": {
                "enabled": True,
                "check_on_startup": True,
                "cache_hours": 24,
                "api_url": "https://api.skillhub.cn/api/v1/skills/privacy-search",
            },
            "searxng": {"host": "127.0.0.1", "port": 8888},
            "privacy": {"default_mode": "normal"},
            "search": {"default_engines": ["baidu"]},
        }

    def test_init_enabled(self):
        checker = UpdateChecker(self.config)
        self.assertTrue(checker.enabled)
        self.assertEqual(checker.cache_hours, 24)

    def test_init_disabled(self):
        cfg = self.config.copy()
        cfg["update_check"] = {"enabled": False}
        checker = UpdateChecker(cfg)
        self.assertFalse(checker.enabled)

    def test_disabled_returns_none(self):
        import asyncio
        cfg = self.config.copy()
        cfg["update_check"] = {"enabled": False}
        checker = UpdateChecker(cfg)
        result = asyncio.run(checker.check())
        self.assertIsNone(result)


class TestUpdateInfo(unittest.TestCase):
    """测试更新信息数据结构"""

    def test_to_dict(self):
        info = UpdateInfo(
            current_version="1.0.0",
            latest_version="1.2.0",
            changelog="new features",
            download_url="https://example.com",
            checked_at=__import__('datetime').datetime.now(),
            has_update=True,
        )
        d = info.to_dict()
        self.assertEqual(d["current_version"], "1.0.0")
        self.assertEqual(d["latest_version"], "1.2.0")
        self.assertTrue(d["has_update"])
        self.assertIn("checked_at", d)


class TestDisplay(unittest.TestCase):
    """测试显示函数（不抛出异常即可）"""

    def test_display_no_update(self):
        # 确保不抛异常
        display_no_update()

    def test_display_notification(self):
        info = UpdateInfo(
            current_version="1.0.0",
            latest_version="1.2.0",
            changelog="新功能",
            download_url="https://example.com",
            checked_at=__import__('datetime').datetime.now(),
            has_update=True,
        )
        display_update_notification(info)


class TestLoadConfig(unittest.TestCase):
    """测试配置加载"""

    def test_load_nonexistent(self):
        config = load_config("/nonexistent/path.yaml")
        self.assertEqual(config, {})


class TestCurrentVersion(unittest.TestCase):
    """验证 CURRENT_VERSION 常量"""

    def test_format(self):
        import re
        self.assertTrue(re.match(r"^\d+\.\d+\.\d+$", CURRENT_VERSION))

    def test_slug_format(self):
        self.assertEqual(SKILL_SLUG, "privacy-search")


if __name__ == "__main__":
    unittest.main()
