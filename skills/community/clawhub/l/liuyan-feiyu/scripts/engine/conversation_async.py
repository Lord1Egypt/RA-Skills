"""
留言非语 — 异步对话管理引擎

与同步版 conversation.py 的关键区别：
- 人格分析（_analyze_and_switch）在后台异步运行，不阻塞主对话
- 用户发完消息后立即收到回复，分析结果在下一轮生效
- 依赖 openai 的 AsyncOpenAI 客户端
"""

import asyncio
import json
import re

from openai import AsyncOpenAI

from config import OPENAI_API_KEY, MODEL
from engine.counselors import COUNSELORS, DEFAULT_COUNSELOR
from engine.personality import build_analysis_prompt
from prompts.system import build_system_prompt, OPENING_MESSAGE


class AsyncConversationEngine:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)
        self.history: list = []
        self.current_counselor: str = DEFAULT_COUNSELOR
        self.personality_context: str = ""
        self.turn_count: int = 0
        self.analysis_results: dict = {}

        # 追踪当前是否有后台分析任务在跑，避免并发重复触发
        self._analysis_task: asyncio.Task | None = None

    def get_system_prompt(self) -> str:
        return build_system_prompt(self.current_counselor, self.personality_context)

    async def chat(self, user_message: str) -> str:
        """
        处理用户消息，返回咨询师回复。

        人格分析在后台 asyncio.Task 中运行：
        - 每 5 轮触发一次
        - 不等分析完成，直接用当前人格上下文生成回复
        - 分析结果在下一轮对话生效
        """
        self.history.append({"role": "user", "content": user_message})
        self.turn_count += 1

        # 每5轮触发一次后台分析（不阻塞，fire-and-forget）
        if self.turn_count % 5 == 0 and self.turn_count >= 5:
            # 若上次分析还没结束，取消它（对话继续，分析任务放弃）
            if self._analysis_task and not self._analysis_task.done():
                self._analysis_task.cancel()
            self._analysis_task = asyncio.create_task(self._analyze_and_switch())

        # 构建消息列表（用当前已有的人格上下文，分析结果下轮生效）
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        messages.extend(self.history)

        # 调用 API，这里才是用户感知到的延迟
        response = await self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.8,
            max_tokens=500,
        )

        assistant_message = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    async def _analyze_and_switch(self):
        """
        后台人格分析任务。
        在 asyncio.Task 中运行，任何异常不会影响主对话流。
        """
        analysis_prompt = build_analysis_prompt(self.history)

        try:
            response = await self.client.chat.completions.create(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个人格分析专家。请严格按照要求的JSON格式输出分析结果，不要包含任何额外文本。",
                    },
                    {"role": "user", "content": analysis_prompt},
                ],
                temperature=0.3,
                max_tokens=800,
            )

            result_text = response.choices[0].message.content.strip()

            # 清理 markdown 代码块包裹（```json ... ``` 或 ``` ... ```）
            result_text = re.sub(r"^```(?:json)?\s*", "", result_text)
            result_text = re.sub(r"\s*```$", "", result_text)
            result_text = result_text.strip()

            analysis = json.loads(result_text)
            self.analysis_results = analysis

            # 更新咨询师
            recommended = analysis.get("recommended_counselor", self.current_counselor)
            if recommended in COUNSELORS:
                self.current_counselor = recommended

            # 更新人格上下文，下一轮对话生效
            summary = analysis.get("personality_summary", "")
            counselor_reason = analysis.get("counselor_reason", "")
            self.personality_context = f"人格概要：{summary}\n切换原因：{counselor_reason}"

        except asyncio.CancelledError:
            # 被主动取消，正常退出
            pass
        except (json.JSONDecodeError, KeyError, Exception):
            # 分析失败静默忽略，不影响主对话
            pass

    def get_opening(self) -> str:
        """返回开场白。"""
        return OPENING_MESSAGE

    def get_status(self) -> dict:
        """返回当前状态（调试用）。"""
        return {
            "turn_count": self.turn_count,
            "current_counselor": self.current_counselor,
            "personality_context": self.personality_context,
            "analysis_results": self.analysis_results,
            "analysis_running": (
                self._analysis_task is not None
                and not self._analysis_task.done()
            ),
        }
