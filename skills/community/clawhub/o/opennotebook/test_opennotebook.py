#!/usr/bin/env python3
"""
OpenNotebook CLI 测试脚本

测试所有 CLI 命令的参数解析和基本功能。
需要 mock 一个 API 服务器来测试网络调用。

运行方式:
    # 快速测试（不需要服务器）
    python3 test_opennotebook.py

    # 完整测试（需要运行 OpenNotebook 服务器）
    python3 test_opennotebook.py --integration --base-url http://localhost:8000
"""

import argparse
import json
import os
import sys
import subprocess
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# 添加当前目录到 path
sys.path.insert(0, str(Path(__file__).parent))

from opennotebook import OpenNotebookClient, Config, OpenNotebookError


class TestConfig(unittest.TestCase):
    """配置测试"""

    def test_config_defaults(self):
        """测试默认配置"""
        config = Config()
        self.assertEqual(config.base_url, "http://localhost:8000")
        self.assertEqual(config.api_key, "")
        self.assertEqual(config.timeout, 30)

    def test_config_save_and_load(self):
        """测试配置保存和加载"""
        import tempfile
        import shutil

        # 创建临时目录
        temp_dir = Path(tempfile.mkdtemp())
        config_file = temp_dir / "opennotebook.env"

        try:
            config = Config()
            config.base_url = "http://test:8080"
            config.api_key = "test-key"

            # 手动保存
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, "w") as f:
                f.write(f"OPENNOTEBOOK_BASE_URL={config.base_url}\n")
                f.write(f"OPENNOTEBOOK_API_KEY={config.api_key}\n")

            # 加载
            config2 = Config()
            with open(config_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line:
                        key, value = line.split("=", 1)
                        if key == "OPENNOTEBOOK_BASE_URL":
                            config2.base_url = value
                        elif key == "OPENNOTEBOOK_API_KEY":
                            config2.api_key = value

            self.assertEqual(config2.base_url, "http://test:8080")
            self.assertEqual(config2.api_key, "test-key")
        finally:
            shutil.rmtree(temp_dir)


class TestClientMocked(unittest.TestCase):
    """使用 Mock 测试客户端"""

    def setUp(self):
        self.config = Config()
        self.config.base_url = "http://test:8000"
        self.config.api_key = "test-key"

    @patch('opennotebook.requests.Session')
    def test_health(self, mock_session_class):
        """测试健康检查"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)
        result = client.health()

        self.assertEqual(result, {"status": "ok"})
        mock_session.request.assert_called_once()

    @patch('opennotebook.requests.Session')
    def test_notebooks_list(self, mock_session_class):
        """测试列出笔记本"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "1", "name": "Test"}]
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)
        result = client.notebooks_list()

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Test")

    @patch('opennotebook.requests.Session')
    def test_notebooks_create(self, mock_session_class):
        """测试创建笔记本"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "1", "name": "New Notebook"}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)
        result = client.notebooks_create(name="New Notebook", description="Test")

        self.assertEqual(result["name"], "New Notebook")

    @patch('opennotebook.requests.Session')
    def test_sources_upload_file_not_found(self, mock_session_class):
        """测试上传不存在的文件"""
        client = OpenNotebookClient(self.config)

        with self.assertRaises(FileNotFoundError):
            client.sources_upload("/nonexistent/file.pdf")

    @patch('opennotebook.requests.Session')
    def test_search_query(self, mock_session_class):
        """测试搜索"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": [], "total": 0}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)
        result = client.search_query("test query")

        self.assertIn("results", result)

    @patch('opennotebook.requests.Session')
    def test_error_handling(self, mock_session_class):
        """测试错误处理"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"detail": "Not found"}
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)

        with self.assertRaises(OpenNotebookError) as context:
            client.notebooks_get("nonexistent")

        self.assertEqual(context.exception.status_code, 404)

    @patch('opennotebook.requests.Session')
    def test_models_operations(self, mock_session_class):
        """测试模型操作"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "1", "name": "gpt-4"}]
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)
        result = client.models_list()

        self.assertEqual(len(result), 1)

    @patch('opennotebook.requests.Session')
    def test_transformations_operations(self, mock_session_class):
        """测试转换操作"""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "1", "name": "summarize"}]
        mock_session.request.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = OpenNotebookClient(self.config)
        result = client.transformations_list()

        self.assertEqual(len(result), 1)


class TestCLIArgumentParsing(unittest.TestCase):
    """测试 CLI 参数解析"""

    def run_cli(self, args):
        """运行 CLI 命令"""
        result = subprocess.run(
            ["python3", "opennotebook.py"] + args,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        return result

    def test_help(self):
        """测试帮助信息"""
        result = self.run_cli(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("OpenNotebook CLI", result.stdout)

    def test_notebooks_help(self):
        """测试 notebooks 帮助"""
        result = self.run_cli(["notebooks", "--help"])
        self.assertEqual(result.returncode, 0)
        # argparse subparser 显示子命令列表
        self.assertIn("notebooks", result.stdout.lower())

    def test_sources_help(self):
        """测试 sources 帮助"""
        result = self.run_cli(["sources", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("sources", result.stdout.lower())

    def test_notes_help(self):
        """测试 notes 帮助"""
        result = self.run_cli(["notes", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("notes", result.stdout.lower())

    def test_search_help(self):
        """测试 search 帮助"""
        result = self.run_cli(["search", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("search", result.stdout.lower())

    def test_models_help(self):
        """测试 models 帮助"""
        result = self.run_cli(["models", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("models", result.stdout.lower())

    def test_transformations_help(self):
        """测试 transformations 帮助"""
        result = self.run_cli(["transformations", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("transformations", result.stdout.lower())

    def test_embeddings_help(self):
        """测试 embeddings 帮助"""
        result = self.run_cli(["embeddings", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("embeddings", result.stdout.lower())

    def test_chat_help(self):
        """测试 chat 帮助"""
        result = self.run_cli(["chat", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("chat", result.stdout.lower())

    def test_podcasts_help(self):
        """测试 podcasts 帮助"""
        result = self.run_cli(["podcasts", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("podcasts", result.stdout.lower())

    def test_notebooks_list_help(self):
        """测试 notebooks list 帮助"""
        result = self.run_cli(["notebooks", "list", "--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("--archived", result.stdout)

    def test_sources_upload_missing_file(self):
        """测试上传缺少文件参数"""
        result = self.run_cli(["sources", "upload"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("required", result.stderr.lower())

    def test_notebooks_create_missing_name(self):
        """测试创建笔记本缺少名称"""
        result = self.run_cli(["notebooks", "create"])
        self.assertNotEqual(result.returncode, 0)

    def test_search_query_missing_query(self):
        """测试搜索缺少查询词"""
        result = self.run_cli(["search", "query"])
        self.assertNotEqual(result.returncode, 0)


class TestIntegration(unittest.TestCase):
    """集成测试（需要运行的 API 服务器）"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = os.getenv("OPENNOTEBOOK_BASE_URL", "http://localhost:8000")
        self.skip_integration = os.getenv("SKIP_INTEGRATION", "true").lower() == "true"

    def setUp(self):
        if self.skip_integration:
            self.skipTest("集成测试已禁用，设置 SKIP_INTEGRATION=false 来启用")

        self.config = Config()
        self.config.base_url = self.base_url

    def test_health_check(self):
        """测试健康检查"""
        client = OpenNotebookClient(self.config)
        try:
            result = client.health()
            self.assertIsNotNone(result)
            print(f"✅ Health check passed: {result}")
        except Exception as e:
            self.skipTest(f"无法连接到服务器: {e}")

    def test_notebooks_list(self):
        """测试列出笔记本"""
        client = OpenNotebookClient(self.config)
        try:
            result = client.notebooks_list()
            self.assertIsInstance(result, list)
            print(f"✅ Found {len(result)} notebooks")
        except Exception as e:
            self.skipTest(f"无法连接到服务器: {e}")

    def test_models_list(self):
        """测试列出模型"""
        client = OpenNotebookClient(self.config)
        try:
            result = client.models_list()
            self.assertIsInstance(result, list)
            print(f"✅ Found {len(result)} models")
        except Exception as e:
            self.skipTest(f"无法连接到服务器: {e}")

    def test_transformations_list(self):
        """测试列出转换"""
        client = OpenNotebookClient(self.config)
        try:
            result = client.transformations_list()
            self.assertIsInstance(result, list)
            print(f"✅ Found {len(result)} transformations")
        except Exception as e:
            self.skipTest(f"无法连接到服务器: {e}")


def run_quick_tests():
    """运行快速测试（不需要服务器）"""
    print("=" * 60)
    print("运行快速测试（不需要 API 服务器）")
    print("=" * 60)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 添加不需要服务器的测试
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestClientMocked))
    suite.addTests(loader.loadTestsFromTestCase(TestCLIArgumentParsing))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


def run_integration_tests(base_url):
    """运行集成测试"""
    print("\n" + "=" * 60)
    print(f"运行集成测试（连接到 {base_url}）")
    print("=" * 60)

    os.environ["SKIP_INTEGRATION"] = "false"
    os.environ["OPENNOTEBOOK_BASE_URL"] = base_url

    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestIntegration)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessfull()


def test_all_cli_commands(base_url=None):
    """测试所有 CLI 命令"""
    print("\n" + "=" * 60)
    print("测试所有 CLI 命令")
    print("=" * 60)

    commands = [
        # 帮助命令
        (["--help"], "帮助"),

        # 各模块帮助
        (["notebooks", "--help"], "笔记本帮助"),
        (["sources", "--help"], "源文件帮助"),
        (["notes", "--help"], "笔记帮助"),
        (["search", "--help"], "搜索帮助"),
        (["transformations", "--help"], "转换帮助"),
        (["models", "--help"], "模型帮助"),
        (["embeddings", "--help"], "嵌入帮助"),
        (["chat", "--help"], "聊天帮助"),
        (["podcasts", "--help"], "播客帮助"),

        # 子命令帮助
        (["notebooks", "list", "--help"], "笔记本列表帮助"),
        (["notebooks", "create", "--help"], "笔记本创建帮助"),
        (["notebooks", "get", "--help"], "笔记本获取帮助"),
        (["sources", "list", "--help"], "源文件列表帮助"),
        (["sources", "upload", "--help"], "源文件上传帮助"),
        (["notes", "create", "--help"], "笔记创建帮助"),
        (["search", "query", "--help"], "搜索查询帮助"),
        (["transformations", "execute", "--help"], "转换执行帮助"),
        (["models", "sync", "--help"], "模型同步帮助"),
    ]

    passed = 0
    failed = 0

    for cmd, desc in commands:
        result = subprocess.run(
            ["python3", "opennotebook.py"] + cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )

        if result.returncode == 0:
            print(f"  ✅ {desc}: {' '.join(cmd)}")
            passed += 1
        else:
            print(f"  ❌ {desc}: {' '.join(cmd)}")
            print(f"     stderr: {result.stderr[:100]}")
            failed += 1

    print(f"\n命令测试完成: {passed} 通过, {failed} 失败")
    return failed == 0


def main():
    parser = argparse.ArgumentParser(description="OpenNotebook CLI 测试")
    parser.add_argument("--integration", action="store_true", help="运行集成测试")
    parser.add_argument("--base-url", default="http://localhost:8000", help="API 基础 URL")
    parser.add_argument("--quick", action="store_true", help="只运行快速测试")
    parser.add_argument("--cli-only", action="store_true", help="只测试 CLI 命令")

    args = parser.parse_args()

    success = True

    if args.cli_only:
        success = test_all_cli_commands(args.base_url)
    elif args.integration:
        success = run_quick_tests()
        if success:
            success = run_integration_tests(args.base_url)
    elif args.quick:
        success = run_quick_tests()
    else:
        # 默认：快速测试 + CLI 命令测试
        success = run_quick_tests()
        if success:
            success = test_all_cli_commands(args.base_url)

    print("\n" + "=" * 60)
    if success:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    print("=" * 60)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()