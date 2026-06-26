# -*- coding: utf-8 -*-
"""
LLM Router Agent - 理解用户意图，分发到对应场景
"""
import json
from typing import Optional
from loguru import logger
from ..config.settings import LLM_CONFIG


class RouterAgent:
    """
    意图识别 + 任务分发

    使用 LLM 理解用户用自然语言描述的场景，
    提取结构化参数，分发到对应场景处理模块。
    """

    SYSTEM_PROMPT = """你是一个智能出行决策助手。用户会描述他遇到的情况，你需要识别属于哪个场景并提取参数。

支持三个场景：
1. highway - 高速堵车，想下高速找吃的/玩的
2. hotel - 途中想找住宿
3. taxi - 景点太堵，想找地方停车打车

用户输入可能是：
- "我在G4高速上，前面10公里堵死了，想找个地方吃饭"
- "我想在附近找个酒店住一晚，明天去故宫"
- "故宫门口太堵了，我在附近找个地方停车打车"

请以JSON格式返回，不要有其他内容：
{
  "scene": "highway|hotel|taxi",
  "params": {
    // highway场景：highway(高速名), location(当前位置描述), destination(目的地描述)
    // hotel场景：location(当前位置描述), budget(预算), people(人数), next_destination(次日目的地)
    // taxi场景：location(堵车位置描述), destination(想去的景点名)
  },
  "reasoning": "一句话说明为什么选择这个场景"
}
"""

    def __init__(self):
        self.llm_config = LLM_CONFIG
        self._client = None

    @property
    def client(self):
        """懒加载 LLM 客户端"""
        if self._client is None:
            import requests
            self._client = requests
        return self._client

    def parse(self, user_input: str) -> Optional[dict]:
        """
        解析用户输入，识别场景和参数

        Returns:
            {"scene": "highway", "params": {...}, "reasoning": "..."}
        """
        try:
            payload = {
                "model": self.llm_config["model"],
                "messages": [
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
                "temperature": 0.1,
            }
            headers = {
                "Authorization": f"Bearer {self.llm_config['api_key']}",
                "Content-Type": "application/json",
            }
            resp = self.client.post(
                f"{self.llm_config['base_url']}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30,
            )
            if resp.status_code != 200:
                logger.error(f"LLM 调用失败: {resp.status_code} {resp.text}")
                return None
            result = resp.json()
            content = result["choices"][0]["message"]["content"].strip()
            # 尝试解析 JSON
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            return json.loads(content)
        except Exception as e:
            logger.error(f"解析用户输入失败: {e}")
            return None

    def route(self, user_input: str) -> Optional[str]:
        """
        判断应该路由到哪个场景

        Returns: "highway" | "hotel" | "taxi" | None
        """
        parsed = self.parse(user_input)
        if parsed:
            return parsed.get("scene")
        return None
