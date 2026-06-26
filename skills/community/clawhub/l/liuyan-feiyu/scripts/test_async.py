"""
留言非语 — 异步引擎单元测试

用 mock 替代真实 API，验证：
1. chat() 正常返回回复
2. 第5轮触发后台分析任务（fire-and-forget）
3. 主对话不等待分析完成
4. /status 能正确显示 analysis_running 状态
"""

import asyncio
import sys
import io
import os
import time
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

# Windows 终端强制 UTF-8，避免 ✓ 等 Unicode 字符报编码错误
if sys.stdout.encoding and sys.stdout.encoding.lower() in ("gbk", "cp936", "gb2312"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class MockChoice:
    def __init__(self, content):
        self.message = MagicMock()
        self.message.content = content


class MockResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]


# 分析任务会故意延迟，测试主对话是否不被阻塞
ANALYSIS_DELAY = 0.5   # 秒
CHAT_MAX_WAIT = 0.3    # 主对话最长允许等待时间（应该远小于分析延迟）

MOCK_ANALYSIS_JSON = """{
  "expression_style": {"score": 5, "observation": "测试"},
  "locus_of_control": {"score": 5, "observation": "测试"},
  "conflict_pattern": {"score": 5, "observation": "测试"},
  "self_awareness": {"score": 5, "observation": "测试"},
  "emotional_regulation": {"score": 5, "observation": "测试"},
  "attachment_style": {"type": "安全型", "observation": "测试"},
  "change_readiness": {"score": 5, "observation": "测试"},
  "recommended_counselor": "烈风",
  "counselor_reason": "用户绕圈了",
  "personality_summary": "有点绕"
}"""


async def slow_analysis_response(*args, **kwargs):
    """模拟一个慢速的分析 API 调用"""
    await asyncio.sleep(ANALYSIS_DELAY)
    return MockResponse(MOCK_ANALYSIS_JSON)


async def fast_chat_response(*args, **kwargs):
    """模拟快速的对话 API 调用"""
    await asyncio.sleep(0.05)
    return MockResponse("这是测试回复。")


class TestAsyncEngine(unittest.IsolatedAsyncioTestCase):

    def _make_engine_with_mock(self):
        """创建带 mock 客户端的引擎"""
        from engine.conversation_async import AsyncConversationEngine
        engine = AsyncConversationEngine.__new__(AsyncConversationEngine)
        # 手动初始化（绕过真实 API key 检查）
        from engine.counselors import DEFAULT_COUNSELOR
        engine.history = []
        engine.current_counselor = DEFAULT_COUNSELOR
        engine.personality_context = ""
        engine.turn_count = 0
        engine.analysis_results = {}
        engine._analysis_task = None

        # mock client
        engine.client = MagicMock()
        engine.client.chat = MagicMock()
        engine.client.chat.completions = MagicMock()
        engine.client.chat.completions.create = AsyncMock(side_effect=fast_chat_response)
        return engine

    async def test_basic_chat_returns_reply(self):
        """普通对话能正确返回回复"""
        engine = self._make_engine_with_mock()
        reply = await engine.chat("你好")
        self.assertEqual(reply, "这是测试回复。")
        self.assertEqual(engine.turn_count, 1)
        self.assertEqual(len(engine.history), 2)  # user + assistant
        print("✓ 基础对话：正常返回回复")

    async def test_analysis_fires_at_turn_5(self):
        """第5轮触发后台分析任务"""
        engine = self._make_engine_with_mock()
        # 让第5轮的分析 API 变慢
        call_count = 0
        async def side_effect(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # 判断是否为分析调用（通过 max_tokens 区分）
            if kwargs.get("max_tokens") == 800:
                await asyncio.sleep(ANALYSIS_DELAY)
                return MockResponse(MOCK_ANALYSIS_JSON)
            return MockResponse("测试回复")

        engine.client.chat.completions.create = AsyncMock(side_effect=side_effect)

        # 跑4轮（不触发分析）
        for i in range(4):
            await engine.chat(f"消息{i+1}")
        self.assertIsNone(engine._analysis_task)

        # 第5轮，触发分析
        start = time.time()
        reply = await engine.chat("消息5")
        elapsed = time.time() - start

        self.assertIsNotNone(engine._analysis_task, "第5轮应创建分析任务")
        self.assertLess(elapsed, CHAT_MAX_WAIT,
            f"第5轮对话耗时 {elapsed:.3f}s，超过阈值 {CHAT_MAX_WAIT}s，说明分析阻塞了主流程")
        print(f"✓ 第5轮触发分析：对话耗时 {elapsed*1000:.0f}ms（分析延迟 {ANALYSIS_DELAY*1000:.0f}ms，未阻塞）")

    async def test_counselor_switches_after_analysis(self):
        """分析完成后咨询师切换"""
        engine = self._make_engine_with_mock()
        async def side_effect(*args, **kwargs):
            if kwargs.get("max_tokens") == 800:
                return MockResponse(MOCK_ANALYSIS_JSON)
            return MockResponse("测试回复")
        engine.client.chat.completions.create = AsyncMock(side_effect=side_effect)

        for i in range(5):
            await engine.chat(f"消息{i+1}")

        # 等待后台分析完成
        if engine._analysis_task:
            await engine._analysis_task

        self.assertEqual(engine.current_counselor, "烈风",
            "分析结果推荐「烈风」，咨询师应已切换")
        self.assertIn("有点绕", engine.personality_context)
        print(f"✓ 咨询师切换：分析完成后切换为「{engine.current_counselor}」")

    async def test_status_shows_analysis_running(self):
        """/status 能正确反映后台分析状态"""
        engine = self._make_engine_with_mock()
        async def side_effect(*args, **kwargs):
            if kwargs.get("max_tokens") == 800:
                await asyncio.sleep(0.2)
                return MockResponse(MOCK_ANALYSIS_JSON)
            return MockResponse("测试回复")
        engine.client.chat.completions.create = AsyncMock(side_effect=side_effect)

        for i in range(5):
            await engine.chat(f"消息{i+1}")

        # 分析任务刚启动，还在跑
        status = engine.get_status()
        self.assertTrue(status["analysis_running"], "分析任务应该在后台运行中")
        print("✓ 状态查询：analysis_running=True 正确")

        # 等待完成
        await engine._analysis_task
        status = engine.get_status()
        self.assertFalse(status["analysis_running"], "分析完成后 analysis_running 应为 False")
        print("✓ 状态查询：analysis_running=False 正确")


if __name__ == "__main__":
    print("=" * 50)
    print("  留言非语 — 异步引擎测试")
    print("=" * 50)
    print()
    unittest.main(verbosity=0)
