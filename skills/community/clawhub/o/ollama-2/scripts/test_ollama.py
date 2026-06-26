import unittest
from unittest.mock import patch, MagicMock
import requests
import json
import io
import logging

# 禁用测试期间的日志输出，使结果更整洁
logging.disable(logging.CRITICAL)

# 导入要测试的函数
from ollama_query import query_ollama


class TestOllamaQuery(unittest.TestCase):
    @patch("requests.Session.post")
    def test_query_ollama_success(self, mock_post):
        """测试正常响应（非流式）"""
        # 模拟响应对象
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Hello world", "done": True}
        mock_post.return_value = mock_response

        result = query_ollama("hi", model="test-model", stream=False)

        self.assertEqual(result, "Hello world")
        mock_post.assert_called_once()
        # 验证发送的参数 (第一个参数是 url)
        args, kwargs = mock_post.call_args
        self.assertIn("/api/generate", args[0])
        self.assertEqual(kwargs["json"]["model"], "test-model")
        self.assertEqual(kwargs["json"]["prompt"], "hi")
        self.assertFalse(kwargs["json"]["stream"])

    @patch("requests.Session.post")
    def test_query_ollama_streaming_success(self, mock_post):
        """测试正常响应（流式）"""
        # 模拟流式响应内容
        chunks = [
            json.dumps({"response": "Hello", "done": False}),
            json.dumps({"response": " world", "done": False}),
            json.dumps({"done": True}),
        ]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [c.encode("utf-8") for c in chunks]
        mock_post.return_value = mock_response

        # query_ollama 在 stream=True 时是一个生成器
        gen = query_ollama("hi", stream=True)
        results = list(gen)

        self.assertEqual(results, ["Hello", " world"])
        mock_post.assert_called_once()
        self.assertTrue(mock_post.call_args.kwargs["json"]["stream"])

    @patch("requests.Session.post")
    def test_query_ollama_network_error(self, mock_post):
        """测试网络连接错误"""
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = query_ollama("hi")

        self.assertIn("Error", result)
        self.assertIn("Connection failed", result)

    @patch("requests.Session.post")
    def test_query_ollama_http_error(self, mock_post):
        """测试 HTTP 错误（如 404 模型不存在）"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error: Not Found"
        )
        mock_post.return_value = mock_response

        result = query_ollama("hi", model="non-existent-model")

        self.assertIn("Error", result)
        self.assertIn("404 Client Error", result)

    @patch("requests.Session.post")
    def test_query_ollama_invalid_url(self, mock_post):
        """测试异常 URL 情况"""
        mock_post.side_effect = requests.exceptions.MissingSchema("Invalid URL")

        with patch("ollama_query.OLLAMA_HOST", "invalid_host"):
            result = query_ollama("hi")
            self.assertIn("Error", result)
            self.assertIn("Invalid URL", result)


if __name__ == "__main__":
    unittest.main(buffer=True)
