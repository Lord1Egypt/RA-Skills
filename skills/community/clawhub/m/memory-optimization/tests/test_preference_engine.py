#!/usr/bin/env python3
"""
Tests for PreferenceEngine
"""

import json
import pytest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


class TestLLMCache:
    """Tests for LLMCache"""

    def test_cache_set_and_get(self):
        """Test basic cache set/get"""
        from preference_engine import LLMCache

        cache = LLMCache()
        cache.set("task_a", "task_b", '{"is_same": true}')

        result = cache.get("task_a", "task_b")
        assert result is not None
        assert '"is_same": true' in result

    def test_cache_miss(self):
        """Test cache miss returns None"""
        from preference_engine import LLMCache

        cache = LLMCache()
        result = cache.get("nonexistent", "tasks")
        assert result is None

    def test_cache_order_independent(self):
        """Test cache key is order-independent"""
        from preference_engine import LLMCache

        cache = LLMCache()
        cache.set("apple", "banana", '{"is_same": true}')

        # Should hit cache even with reversed order
        result = cache.get("banana", "apple")
        assert result is not None

    def test_cache_expiry(self):
        """Test cache TTL expiry"""
        from preference_engine import LLMCache

        cache = LLMCache(ttl_seconds=1)  # 1 second TTL
        cache.set("task_a", "task_b", '{"is_same": true}')

        # Should still be valid immediately
        result = cache.get("task_a", "task_b")
        assert result is not None

        # After TTL, should be expired
        import time
        time.sleep(1.1)
        result = cache.get("task_a", "task_b")
        assert result is None

    def test_cache_clear(self):
        """Test cache clear"""
        from preference_engine import LLMCache

        cache = LLMCache()
        cache.set("task_a", "task_b", '{"is_same": true}')
        cache.clear()

        result = cache.get("task_a", "task_b")
        assert result is None


class TestJudgeTaskSimilarity:
    """Tests for judge_task_similarity function"""

    def test_same_task_returns_true(self):
        """Test LLM correctly identifies same task"""
        from preference_engine import judge_task_similarity, LLMClient

        mock_client = MagicMock()
        mock_client.call.return_value = '{"is_same": true, "reasoning": "Both are the same goal"}'

        is_same, reasoning = judge_task_similarity(
            "访问 moltbook",
            "查看 moltbook 帖子",
            mock_client,
            use_cache=False
        )

        assert is_same is True
        assert "same" in reasoning.lower() or "goal" in reasoning.lower()

    def test_different_task_returns_false(self):
        """Test LLM correctly identifies different tasks"""
        from preference_engine import judge_task_similarity, LLMClient

        mock_client = MagicMock()
        mock_client.call.return_value = '{"is_same": false, "reasoning": "Completely different goals"}'

        is_same, reasoning = judge_task_similarity(
            "写代码",
            "回复邮件",
            mock_client,
            use_cache=False
        )

        assert is_same is False

    def test_cache_hit_returns_cached_result(self):
        """Test cache hit skips LLM call"""
        from preference_engine import judge_task_similarity, LLMClient, _llm_cache

        # Pre-populate cache
        _llm_cache.clear()
        _llm_cache.set("task_a", "task_b", '{"is_same": true, "reasoning": "Cached result"}')

        mock_client = MagicMock()

        is_same, reasoning = judge_task_similarity(
            "task_a",
            "task_b",
            mock_client,
            use_cache=True
        )

        # Should not have called LLM
        mock_client.call.assert_not_called()
        assert is_same is True
        assert "[Cache]" in reasoning


class TestPreferenceEngine:
    """Tests for PreferenceEngine class"""

    def test_classify_preference_type_temporal(self):
        """Test temporal preference classification"""
        from preference_engine import PreferenceEngine

        engine = PreferenceEngine()

        result = engine._classify_preference_type(
            "Decision",
            "周末固定时间开会",
            []
        )
        assert result == "temporal"

    def test_classify_preference_type_tool(self):
        """Test tool preference classification"""
        from preference_engine import PreferenceEngine

        engine = PreferenceEngine()

        result = engine._classify_preference_type(
            "Decision",
            "使用 API 访问数据",
            []
        )
        assert result == "tool"

    def test_classify_preference_type_frequency(self):
        """Test frequency preference classification"""
        from preference_engine import PreferenceEngine

        engine = PreferenceEngine()

        result = engine._classify_preference_type(
            "Decision",
            "定期提交代码",
            []
        )
        assert result == "frequency"

    def test_classify_preference_type_action_default(self):
        """Test default action preference classification"""
        from preference_engine import PreferenceEngine

        engine = PreferenceEngine()

        result = engine._classify_preference_type(
            "Decision",
            "完成代码审查",
            []
        )
        assert result == "action"


class TestLLMClient:
    """Tests for LLMClient"""

    def test_mock_response(self):
        """Test mock_response() returns JSON string for given data"""
        from preference_engine import LLMClient

        client = LLMClient(api_key="", model="test")
        response = client.mock_response({"is_same": False, "reasoning": "test"})

        data = json.loads(response)
        assert "is_same" in data
        assert data["is_same"] is False

    def test_call_without_api_key_returns_none(self):
        """Test LLMClient returns None when no API key and no mock_data"""
        from preference_engine import LLMClient
        from unittest.mock import patch

        with patch.dict('os.environ', {'OPENAI_API_KEY': ''}, clear=False):
            client = LLMClient(api_key="")
            result = client.call([])

        assert result is None

    def test_api_timeout_handled_with_mock_data(self):
        """Test API timeout is handled gracefully with mock_data fallback"""
        from preference_engine import LLMClient

        client = LLMClient(api_key="test-key")
        mock_data = {"is_same": False, "reasoning": "timeout fallback"}

        with patch('requests.post') as mock_post:
            mock_post.side_effect = Exception("timeout")
            result = client.call([], mock_data=mock_data)

            # Should fall back to mock_data
            assert result is not None
            data = json.loads(result)
            assert data["is_same"] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
