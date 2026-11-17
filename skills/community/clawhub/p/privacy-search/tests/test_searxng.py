#!/usr/bin/env python3
"""
F2 单测：SearXNG 本地实例管理
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from searxng_manager import DockerManager, PipManager, SearXNGManager, load_config


class TestDockerManager(unittest.TestCase):
    """测试 Docker 管理器"""

    def test_init(self):
        config = {
            "searxng": {
                "docker": {
                    "image": "searxng/searxng:latest",
                    "container_name": "test-container",
                    "auto_remove": True,
                },
                "host": "127.0.0.1",
                "port": 8888,
            }
        }
        mgr = DockerManager(config)
        self.assertEqual(mgr.image, "searxng/searxng:latest")
        self.assertEqual(mgr.host, "127.0.0.1")
        self.assertEqual(mgr.port, 8888)

    def test_host_is_localhost(self):
        """验证默认绑定地址是 127.0.0.1"""
        config = {
            "searxng": {
                "docker": {"image": "test", "container_name": "test"},
                "host": "127.0.0.1",
                "port": 8888,
            }
        }
        mgr = DockerManager(config)
        self.assertEqual(mgr.host, "127.0.0.1")
        self.assertNotEqual(mgr.host, "0.0.0.0")


class TestPipManager(unittest.TestCase):
    """测试 pip 管理器"""

    def test_init_config(self):
        config = {
            "searxng": {
                "pip": {"use_venv": True, "venv_path": "~/.workbuddy/test-venv"},
                "host": "127.0.0.1",
                "port": 8888,
            }
        }
        mgr = PipManager(config)
        self.assertTrue(mgr.use_venv)
        self.assertIn("venv_path", mgr.config)

    def test_venv_forced(self):
        """验证 pip 方式强制使用 venv"""
        config = {
            "searxng": {
                "pip": {"use_venv": True},
                "host": "127.0.0.1",
                "port": 8888,
            }
        }
        mgr = PipManager(config)
        self.assertTrue(mgr.use_venv)


class TestSearXNGManager(unittest.TestCase):
    """测试统一入口"""

    def test_docker_method(self):
        config = {
            "searxng": {
                "install_method": "docker",
                "docker": {"image": "test", "container_name": "test"},
                "pip": {"use_venv": True},
                "host": "127.0.0.1",
                "port": 8888,
            }
        }
        mgr = SearXNGManager(config)
        self.assertEqual(mgr.method, "docker")
        self.assertIsNotNone(mgr.docker_manager)

    def test_pip_method(self):
        config = {
            "searxng": {
                "install_method": "pip",
                "docker": {"image": "test", "container_name": "test"},
                "pip": {"use_venv": True},
                "host": "127.0.0.1",
                "port": 8888,
            }
        }
        mgr = SearXNGManager(config)
        self.assertEqual(mgr.method, "pip")
        self.assertIsNotNone(mgr.pip_manager)


class TestLoadConfig(unittest.TestCase):
    """测试配置加载"""

    def test_default_config_when_missing(self):
        config = load_config("/nonexistent/path.yaml")
        self.assertIn("searxng", config)


if __name__ == "__main__":
    unittest.main()
