# -*- coding: utf-8 -*-
"""字符级分词器(char-level tokenizer)。

真实开源大模型(GPT-2 / Qwen 等)使用 BPE 等子词分词;为了让本项目
零额外依赖、并在中小语料上快速看到学习效果,这里采用最简单的
字符级方案(思路同 Karpathy 的 char-rnn):一个字符 = 一个 token。
"""

from __future__ import annotations

import json
from pathlib import Path


class CharTokenizer:
    """把文本按「字符」编码为整数 id,字符表由语料统计得到。"""

    def __init__(self, chars):
        # 排序去重,保证同一份语料得到完全一致的词表
        self.chars = sorted(set(chars))
        self.stoi = {ch: i for i, ch in enumerate(self.chars)}
        self.itos = {i: ch for i, ch in enumerate(self.chars)}

    @classmethod
    def from_text(cls, text: str) -> "CharTokenizer":
        return cls(text)

    @property
    def vocab_size(self) -> int:
        return len(self.chars)

    def encode(self, text: str) -> list[int]:
        """文本 -> id 列表;词表外的字符直接跳过(对任意提示词都鲁棒)。"""
        return [self.stoi[c] for c in text if c in self.stoi]

    def decode(self, ids) -> str:
        """id 列表 -> 文本。"""
        return "".join(self.itos[int(i)] for i in ids if int(i) in self.itos)

    def save(self, path) -> None:
        Path(path).write_text(
            json.dumps({"version": 1, "chars": self.chars}, ensure_ascii=False),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path) -> "CharTokenizer":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(data["chars"])
