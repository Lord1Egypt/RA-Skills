"""
radial_memory/summarizer.py
─────────────────────────────────────────────────────────
摘要与匹配验证的抽象层。

提供三种实现：
  1. KeywordSummarizer      — 无 LLM 依赖，截断+关键词匹配（测试/离线用）
  2. OpenAISummarizer        — OpenAI API（gpt-4o-mini 等）
  3. LiteLLMSummarizer       — 任意 LiteLLM 兼容后端（Ollama/Claude/Gemini 等）

生产场景推荐：agent 本身即 LLM，可直接调用 AgentProvidedSummarizer，
由 agent 在 complete_task() 前自行计算各级摘要后传入，无需额外 API 调用。
"""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from typing import Tuple


class BaseSummarizer(ABC):
    """摘要器基类，所有实现须实现这两个方法。"""

    @abstractmethod
    def summarize(self, text: str, max_chars: int, context_hint: str = "") -> str:
        """
        将 text 压缩到 max_chars 字符以内。
        context_hint: 提示摘要重点，如任务名称。
        """

    @abstractmethod
    def verify_match(self, query: str, node_summary: str) -> Tuple[bool, float]:
        """
        判断 node_summary 是否是 query 描述的任务。
        返回 (是否匹配, 置信度 0.0-1.0)
        """


# ─────────────────────────────────────────────
# 1. 关键词摘要器（无依赖，供测试/演示）
# ─────────────────────────────────────────────

class KeywordSummarizer(BaseSummarizer):
    """
    纯文本截断 + 关键词重叠匹配。
    不依赖任何外部库，适合本地测试和演示。
    生产环境请替换为 LLM 摘要器。
    """

    def summarize(self, text: str, max_chars: int, context_hint: str = "") -> str:
        text = text.strip()
        if not text:
            return context_hint or ""
        if max_chars is None or len(text) <= max_chars:
            return text
        # 保留首尾各一部分，比纯截断丢失信息更少
        half = (max_chars - 6) // 2
        return text[:half] + " … " + text[-half:]

    def verify_match(self, query: str, node_summary: str) -> Tuple[bool, float]:
        """基于中英文词语重叠的简单匹配。"""
        q_tokens = set(_tokenize(query))
        s_tokens = set(_tokenize(node_summary))
        if not q_tokens:
            return False, 0.0
        overlap = len(q_tokens & s_tokens)
        confidence = overlap / len(q_tokens)
        return confidence >= 0.3, round(confidence, 3)


def _tokenize(text: str) -> list:
    """简单分词：英文按空格/标点，中文按字。"""
    # 英文单词
    en_words = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    # 中文字符（单字作为 token，实际生产应用 jieba）
    zh_chars = re.findall(r"[\u4e00-\u9fff]", text)
    return en_words + zh_chars


# ─────────────────────────────────────────────
# 2. OpenAI 摘要器
# ─────────────────────────────────────────────

class OpenAISummarizer(BaseSummarizer):
    """
    使用 OpenAI API 进行摘要与匹配验证。
    安装依赖: pip install openai
    """

    def __init__(self, api_key: str, model: str = "gpt-4o-mini", base_url: str = None):
        try:
            from openai import OpenAI
        except ImportError as e:
            raise ImportError("需要安装 openai: pip install openai") from e

        kwargs = {"api_key": api_key}
        if base_url:
            kwargs["base_url"] = base_url
        self.client = OpenAI(**kwargs)
        self.model = model

    def summarize(self, text: str, max_chars: int, context_hint: str = "") -> str:
        if not text.strip():
            return ""
        if max_chars and len(text) <= max_chars:
            return text

        hint = f"请重点保留与「{context_hint}」相关的内容。" if context_hint else ""
        limit = f"{max_chars}个字符" if max_chars else "尽量简洁"
        prompt = (
            f"请将以下内容压缩摘要，控制在{limit}以内。{hint}\n\n"
            f"---\n{text}\n---\n\n只输出摘要，不要解释。"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max(50, (max_chars or 600) // 2),
        )
        return resp.choices[0].message.content.strip()

    def verify_match(self, query: str, node_summary: str) -> Tuple[bool, float]:
        prompt = (
            f"用户查询: {query}\n\n"
            f"节点摘要: {node_summary}\n\n"
            f"这个节点摘要是否描述了用户查询所要找的任务？\n"
            f"只回复格式: YES 0.9 或 NO 0.1（YES/NO加空格加0到1的置信度）"
        )
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8,
        )
        result = resp.choices[0].message.content.strip().upper()
        is_match = result.startswith("YES")
        try:
            confidence = float(result.split()[-1])
            confidence = max(0.0, min(1.0, confidence))
        except (IndexError, ValueError):
            confidence = 0.8 if is_match else 0.2
        return is_match, confidence


# ─────────────────────────────────────────────
# 3. LiteLLM 通用摘要器（支持 Ollama / Claude / Gemini 等）
# ─────────────────────────────────────────────

class LiteLLMSummarizer(BaseSummarizer):
    """
    通过 LiteLLM 调用任意 LLM 后端。
    安装依赖: pip install litellm
    示例 model: "ollama/qwen2.5:7b", "claude-3-haiku-20240307", "gemini/gemini-flash"
    """

    def __init__(self, model: str, **litellm_kwargs):
        try:
            import litellm
            self._litellm = litellm
        except ImportError as e:
            raise ImportError("需要安装 litellm: pip install litellm") from e
        self.model = model
        self.kwargs = litellm_kwargs

    def summarize(self, text: str, max_chars: int, context_hint: str = "") -> str:
        if not text.strip():
            return ""
        if max_chars and len(text) <= max_chars:
            return text

        hint = f"重点保留「{context_hint}」相关内容。" if context_hint else ""
        limit = f"{max_chars}字符以内" if max_chars else "尽量简洁"
        prompt = f"压缩以下内容为{limit}的摘要。{hint}\n\n{text}\n\n只输出摘要。"

        resp = self._litellm.completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max(50, (max_chars or 600) // 2),
            **self.kwargs,
        )
        return resp.choices[0].message.content.strip()

    def verify_match(self, query: str, node_summary: str) -> Tuple[bool, float]:
        prompt = (
            f"用户查询: {query}\n节点摘要: {node_summary}\n\n"
            f"匹配吗？回复 YES 0.9 或 NO 0.1"
        )
        resp = self._litellm.completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8,
            **self.kwargs,
        )
        result = resp.choices[0].message.content.strip().upper()
        is_match = result.startswith("YES")
        try:
            confidence = float(result.split()[-1])
            confidence = max(0.0, min(1.0, confidence))
        except (IndexError, ValueError):
            confidence = 0.8 if is_match else 0.2
        return is_match, confidence
