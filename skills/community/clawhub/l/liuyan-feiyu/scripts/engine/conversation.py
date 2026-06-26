"""
留言非语 — 对话管理引擎

管理对话流、咨询师切换、人格分析触发。
"""

import json
import re
from openai import OpenAI

from config import OPENAI_API_KEY, MODEL
from engine.counselors import COUNSELORS, DEFAULT_COUNSELOR
from engine.personality import build_analysis_prompt
from prompts.system import build_system_prompt, OPENING_MESSAGE


class ConversationEngine:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.history: list = []
        self.current_counselor: str = DEFAULT_COUNSELOR
        self.personality_context: str = ""
        self.turn_count: int = 0
        self.analysis_results: dict = {}

    def get_system_prompt(self) -> str:
        return build_system_prompt(self.current_counselor, self.personality_context)

    def chat(self, user_message: str) -> str:
        """处理用户消息，返回咨询师回复。"""
        self.history.append({"role": "user", "content": user_message})
        self.turn_count += 1

        # 每5轮进行一次人格分析并决定是否切换咨询师
        if self.turn_count % 5 == 0 and self.turn_count >= 5:
            self._analyze_and_switch()

        # 构建消息列表
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        messages.extend(self.history)

        # 调用API
        response = self.client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.8,
            max_tokens=500,
        )

        assistant_message = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def _analyze_and_switch(self):
        """分析用户人格并决定是否切换咨询师。"""
        analysis_prompt = build_analysis_prompt(self.history)

        try:
            response = self.client.chat.completions.create(
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

            # 更新人格上下文
            summary = analysis.get("personality_summary", "")
            counselor_reason = analysis.get("counselor_reason", "")
            self.personality_context = f"人格概要：{summary}\n切换原因：{counselor_reason}"

        except (json.JSONDecodeError, KeyError, Exception):
            # 分析失败不影响对话继续
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
        }
