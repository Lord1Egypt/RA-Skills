#!/usr/bin/env python3
"""
KG Extractor Tests
"""

import json
import sys
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import pytest
from kg_extractor import (
    JSONLParser,
    MessageFilter,
    LLMClient,
    EntityExtractor,
    BatchProcessor,
    Message,
    Conversation,
    ExtractedEntity
)


class TestJSONLParser:
    """测试 JSONL 解析器"""

    def test_parse_file_not_exists(self):
        """测试解析不存在的文件"""
        result = JSONLParser.parse_file(Path('/nonexistent/file.jsonl'))
        assert result is None

    def test_scan_directory(self):
        """测试扫描目录"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 创建正确的目录结构：agents/*/sessions/*.jsonl
            agents_dir = Path(tmpdir)
            sessions_dir = agents_dir / 'main' / 'sessions'
            sessions_dir.mkdir(parents=True)

            # 创建测试文件
            (sessions_dir / 'session1.jsonl').write_text('{"messages": []}\n')
            (sessions_dir / 'session2.jsonl').write_text('{"messages": []}\n')
            # 创建非 jsonl 文件（应被忽略）
            (sessions_dir / 'readme.txt').write_text('not a jsonl')

            files = JSONLParser.scan_directory(agents_dir)
            assert len(files) == 2
            assert all(f.suffix == '.jsonl' for f in files)


class TestMessageFilter:
    """测试消息过滤器"""

    def test_is_system_message(self):
        """测试系统消息识别"""
        assert MessageFilter.is_system_message("system: hello")
        assert MessageFilter.is_system_message("Conversation info")
        assert not MessageFilter.is_system_message("Hello, how are you?")

    def test_is_error_message(self):
        """测试错误消息识别"""
        assert MessageFilter.is_error_message("429 error rate limit")  # 需要2个markers
        assert MessageFilter.is_error_message("500 server error exception")
        assert MessageFilter.is_error_message("")  # 空消息

    def test_filter_messages(self):
        """测试消息过滤"""
        messages = [
            Message(role='user', content='hello', timestamp='2026-01-01T00:00:00Z'),
            Message(role='assistant', content='error: something failed', timestamp='2026-01-01T00:01:00Z'),
            Message(role='user', content='system: config', timestamp='2026-01-01T00:02:00Z'),
            Message(role='assistant', content='Here is the result', timestamp='2026-01-01T00:03:00Z'),
        ]

        filtered = MessageFilter.filter_messages(messages)
        assert len(filtered) == 2  # 只保留最后两条
        assert filtered[0].content == 'hello'
        assert filtered[1].content == 'Here is the result'

    def test_merge_consecutive(self):
        """测试合并相邻消息"""
        messages = [
            Message(role='user', content='first', timestamp='2026-01-01T00:00:00Z', session_id='s1'),
            Message(role='user', content='second', timestamp='2026-01-01T00:00:01Z', session_id='s1'),
            Message(role='assistant', content='response', timestamp='2026-01-01T00:00:02Z', session_id='s1'),
        ]

        merged = MessageFilter.merge_consecutive(messages)
        assert len(merged) == 2
        assert 'first\nsecond' in merged[0].content


class TestLLMClient:
    """测试 LLM 客户端"""

    def test_mock_response(self):
        """测试模拟响应"""
        client = LLMClient(api_key='')  # 无 API key
        response = client.mock_response({"entities": [{"type": "Decision", "title": "Test"}]})

        assert response is not None
        data = json.loads(response)
        assert "entities" in data

    def test_call_with_api_key(self):
        """测试配置 API key 时的实际调用"""
        client = LLMClient(api_key='test-api-key', base_url='https://api.test.com')

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"entities": [{"type": "Decision", "title": "API Test", "rationale": "From API", "made_at": "2026-01-01T00:00:00Z", "confidence": 0.8, "tags": ["#api"]}]}'}}]
        }

        with patch('requests.post', return_value=mock_response) as mock_post:
            response = client.call([{"role": "user", "content": "test"}])

            assert response is not None
            data = json.loads(response)
            assert data["entities"][0]["title"] == "API Test"
            mock_post.assert_called_once()
            call_args = mock_post.call_args
            assert "Bearer test-api-key" in call_args.kwargs['headers']['Authorization']


class TestEntityExtractor:
    """测试实体提取器"""

    def test_parse_response_valid_json(self):
        """测试解析有效 JSON 响应"""
        client = Mock()
        client.call.return_value = json.dumps({
            "entities": [
                {
                    "type": "Decision",
                    "title": "Test Decision",
                    "rationale": "Test rationale",
                    "made_at": "2026-01-01T00:00:00Z",
                    "confidence": 0.9,
                    "tags": ["#test"]
                }
            ]
        })

        mock_validate = Mock(return_value=[])
        mock_create = Mock()
        extractor = EntityExtractor(client, mock_create, mock_validate)

        conversation = Conversation(
            session_id="test-session",
            messages=[
                Message(role='user', content='test', timestamp='2026-01-01T00:00:00Z')
            ]
        )

        entities = extractor._parse_response(client.call.return_value, "test-session", dry_run=True)

        assert len(entities) == 1
        assert entities[0].type == "Decision"
        assert entities[0].title == "Test Decision"

    def test_parse_response_invalid_json(self):
        """测试解析无效 JSON"""
        client = Mock()
        mock_validate = Mock(return_value=[])
        mock_create = Mock()
        extractor = EntityExtractor(client, mock_create, mock_validate)

        entities = extractor._parse_response("not valid json", "test-session", dry_run=True)
        assert len(entities) == 0


class TestBatchProcessor:
    """测试批量处理器"""

    def test_init(self):
        """测试初始化"""
        client = Mock()
        extractor = EntityExtractor(client)
        processor = BatchProcessor(extractor)

        assert processor.stats['files_processed'] == 0
        assert processor.stats['total_entities'] == 0


# 运行测试
if __name__ == '__main__':
    pytest.main([__file__, '-v'])
