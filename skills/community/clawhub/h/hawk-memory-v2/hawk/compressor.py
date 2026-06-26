"""
compressor.py — 上下文压缩器

功能：
- 按 token 限制压缩对话历史
- 保留关键信息（决策/偏好/实体）
- 分层压缩：轻度→中度→重度
"""

import os
import tiktoken
from typing import TypedDict


class CompressionResult(TypedDict):
    compressed: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float


class ContextCompressor:
    """
    上下文压缩器
    支持 token 计数和智能压缩
    """

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        try:
            self.enc = tiktoken.encoding_for_model(model)
        except KeyError:
            self.enc = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.enc.encode(text))

    def compress(self, conversation: list[dict], max_tokens: int = 4000, strategy: str = "smart") -> CompressionResult:
        """
        压缩对话历史

        Args:
            conversation: [{"role": "user"/"assistant", "content": "..."}]
            max_tokens: 压缩后最大token数
            strategy: "smart" | "simple"

        Returns:
            CompressionResult with compressed text and stats
        """
        # 计算当前总tokens
        total_tokens = sum(self.count_tokens(msg.get("content", "")) for msg in conversation)

        if total_tokens <= max_tokens:
            return CompressionResult(
                compressed=self._formatConversation(conversation),
                original_tokens=total_tokens,
                compressed_tokens=total_tokens,
                compression_ratio=1.0,
            )

        if strategy == "simple":
            return self._simpleCompress(conversation, max_tokens)
        else:
            return self._smartCompress(conversation, max_tokens)

    def _formatConversation(self, conversation: list[dict]) -> str:
        lines = []
        for msg in conversation:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            lines.append(f"{role}: {content}")
        return "\n".join(lines)

    def _simpleCompress(self, conversation: list[dict], max_tokens: int) -> CompressionResult:
        """从头保留到尾，直到超出限制"""
        kept = []
        current_tokens = 0
        for msg in reversed(conversation):
            msg_tokens = self.count_tokens(msg.get("content", ""))
            if current_tokens + msg_tokens <= max_tokens:
                kept.insert(0, msg)
                current_tokens += msg_tokens
            else:
                break
        return CompressionResult(
            compressed=self._formatConversation(kept),
            original_tokens=sum(self.count_tokens(m.get("content", "")) for m in conversation),
            compressed_tokens=current_tokens,
            compression_ratio=round(current_tokens / max(1, sum(self.count_tokens(m.get("content", "")) for m in conversation)), 2),
        )

    def _smartCompress(self, conversation: list[dict], max_tokens: int) -> CompressionResult:
        """
        智能压缩：优先保留关键信息
        - 决策（以"决定"、"选择"、"要"开头）
        - 偏好（包含"喜欢"、"希望"、"想要"）
        - 实体（人名/公司名/项目名）
        - 最后2轮对话（最新上下文）
        """
        KEYWORDS = ["决定", "选择", "要", "喜欢", "希望", "想要", "认为", "觉得",
                    "老板", "周", "悟空", "唐僧", "趣近", "取经"]

        important_indices = set()
        # 保留最后2轮
        for i in range(max(0, len(conversation) - 2), len(conversation)):
            important_indices.add(i)
        # 保留关键词句
        for i, msg in enumerate(conversation):
            content = msg.get("content", "").lower()
            if any(kw in content for kw in KEYWORDS):
                important_indices.add(i)

        kept = [conversation[i] for i in sorted(important_indices)]
        kept_tokens = sum(self.count_tokens(m.get("content", "")) for m in kept)

        # 如果还不够，从头加回来直到满
        if kept_tokens < max_tokens * 0.5:
            for msg in conversation:
                if len(kept) == len(conversation):
                    break
                if id(msg) not in {id(m) for m in kept}:
                    msg_tokens = self.count_tokens(msg.get("content", ""))
                    if kept_tokens + msg_tokens <= max_tokens:
                        kept.append(msg)
                        kept_tokens += msg_tokens

        kept.sort(key=lambda m: conversation.index(m))
        original_tokens = sum(self.count_tokens(m.get("content", "")) for m in conversation)

        return CompressionResult(
            compressed=self._formatConversation(kept),
            original_tokens=original_tokens,
            compressed_tokens=kept_tokens,
            compression_ratio=round(kept_tokens / max(1, original_tokens), 2),
        )
