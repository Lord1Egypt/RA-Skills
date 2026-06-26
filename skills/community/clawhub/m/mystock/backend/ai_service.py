"""
AI 服务管理器
统一接口，支持多种提供商
"""

import json
import httpx
from typing import List, Dict, Optional
from ai_config import AI_CONFIG, AIProvider

class AIService:
    def __init__(self):
        self.config = AI_CONFIG
        self.provider = self.config.get_provider()

    async def chat(self, message: str, history: List[Dict] = None) -> str:
        """统一的聊天接口"""
        if self.provider == AIProvider.MINIMAX:
            return await self._chat_minimax(message, history)
        elif self.provider == AIProvider.OPENAI:
            return await self._chat_openai(message, history)
        elif self.provider == AIProvider.ZHIPU:
            return await self._chat_zhipu(message, history)
        elif self.provider == AIProvider.SILICONFLOW:
            return await self._chat_siliconflow(message, history)
        else:
            return self._chat_rule_based(message, history)

    async def _chat_minimax(self, message: str, history: List[Dict]) -> str:
        """Minimax AI"""
        try:
            import urllib.request

            url = "https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId=your_group_id"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.api_key}'
            }

            messages = [{"role": "system", "content": self.config.get_system_prompt()}]

            if history:
                for h in history[-10:]:  # 限制历史长度
                    messages.append({
                        "role": h.get("role", "user"),
                        "content": h.get("content", "")
                    })

            messages.append({"role": "user", "content": message})

            data = {
                "model": self.config.model or "abab5.5-chat",
                "tokens_to_generate": 512,
                "messages": messages
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['messages'][-1]['text']

        except Exception as e:
            return f"Minimax API 调用失败: {str(e)}\n\n请检查 API Key 是否正确配置。"

    async def _chat_openai(self, message: str, history: List[Dict]) -> str:
        """OpenAI GPT"""
        try:
            import urllib.request

            if self.config.base_url:
                url = f"{self.config.base_url.rstrip('/')}/chat/completions"
            else:
                url = "https://api.openai.com/v1/chat/completions"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.api_key}'
            }

            messages = [{"role": "system", "content": self.config.get_system_prompt()}]

            if history:
                for h in history[-10:]:
                    messages.append({
                        "role": h.get("role", "user"),
                        "content": h.get("content", "")
                    })

            messages.append({"role": "user", "content": message})

            data = {
                "model": self.config.model or "gpt-3.5-turbo",
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']

        except Exception as e:
            return f"OpenAI API 调用失败: {str(e)}\n\n请检查 API Key 是否正确配置。"

    async def _chat_zhipu(self, message: str, history: List[Dict]) -> str:
        """智谱 GLM"""
        try:
            import urllib.request

            url = "https://open.biggl.cn/v2/chat/completions"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.api_key}'
            }

            messages = [{"role": "system", "content": self.config.get_system_prompt()}]

            if history:
                for h in history[-10:]:
                    messages.append({
                        "role": h.get("role", "user"),
                        "content": h.get("content", "")
                    })

            messages.append({"role": "user", "content": message})

            data = {
                "model": self.config.model or "glm-4",
                "messages": messages
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']

        except Exception as e:
            return f"智谱 API 调用失败: {str(e)}\n\n请检查 API Key 是否正确配置。"

    async def _chat_siliconflow(self, message: str, history: List[Dict]) -> str:
        """硅基流动"""
        try:
            import urllib.request

            url = "https://api.siliconflow.cn/v1/chat/completions"

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.config.api_key}'
            }

            messages = [{"role": "system", "content": self.config.get_system_prompt()}]

            if history:
                for h in history[-10:]:
                    messages.append({
                        "role": h.get("role", "user"),
                        "content": h.get("content", "")
                    })

            messages.append({"role": "user", "content": message})

            data = {
                "model": self.config.model or "Qwen/Qwen2.5-7B-Instruct",
                "messages": messages
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )

            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result['choices'][0]['message']['content']

        except Exception as e:
            return f"硅基流动 API 调用失败: {str(e)}\n\n请检查 API Key 是否正确配置。"

    def _chat_rule_based(self, message: str, history: List[Dict]) -> str:
        """基于规则的响应（无AI）"""
        message_lower = message.lower()

        # 基础问答
        if any(kw in message_lower for kw in ['你好', 'hi', 'hello']):
            return "你好！我是 MyStock，可以帮你查询持仓、分析股票。有什么可以帮你的吗？"

        if any(kw in message_lower for kw in ['帮助', 'help', '怎么用']):
            return """我可以帮你：
• 查询持仓和观察列表
• 分析股票走势
• 回答投资相关问题

直接告诉我你想查询的内容就好！"""

        return "抱歉，我目前仅支持基础问答功能。\n\n要启用智能对话，请配置 AI 服务商：\n1. 注册 SiliconFlow（免费额度）\n2. 设置环境变量 AI_API_KEY\n3. 重启服务"

AI_SERVICE = AIService()
