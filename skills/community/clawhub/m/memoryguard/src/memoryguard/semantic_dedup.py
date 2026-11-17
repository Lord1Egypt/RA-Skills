"""语义级去重：基于 embedding 的语义相似度。

补充 auto_organizer.py 的 Jaccard/关键词启发式，处理跨语言、改写等
字符不重合但语义相同的场景。

默认 HashBackend 纯标准库，无新依赖；可通过 duck typing 注入外部
embedding 后端（OpenAI/本地模型等），只要实现 embed_text(text)->list[float]。

设计要点：
- HashBackend 用 分词 + 双语对齐 + n-gram shingles + MinHash 生成固定维度
  0/1 签名，cosine 近似 Jaccard。相同 shingles 集合 cosine=1.0；独立集合
  baseline 约 0.5，threshold=0.85 足够严格。
- 跨语言对齐靠内置中英对照词典 + 英文词干化，让同义句共享 token。
- threshold 由环境变量 MEMORYGUARD_SEMANTIC_THRESHOLD 配置，默认 0.85。
"""
from __future__ import annotations

import hashlib
import math
import os
import re
from pathlib import Path
from typing import Any, Protocol

from .schema_v3 import MemoryKind, SharedMemoryRecord
from .shared_memory_store import SharedMemoryStore


DEFAULT_SEMANTIC_THRESHOLD = 0.85


def _env_threshold() -> float:
    """从环境变量读取阈值，默认 0.85。"""
    v = os.environ.get("MEMORYGUARD_SEMANTIC_THRESHOLD", "")
    try:
        val = float(v)
        if 0.0 <= val <= 1.0:
            return val
    except (ValueError, TypeError):
        pass
    return DEFAULT_SEMANTIC_THRESHOLD


class EmbeddingBackend(Protocol):
    """Embedding 后端接口（duck typing）。

    任何实现 embed_text(text) -> list[float] 的对象都可注入 SemanticDedup。
    外部实现（OpenAI / 本地模型）只需满足此协议，无需继承。
    """

    def embed_text(self, text: str) -> list[float]:
        ...


# 中英对照词典（常见概念，用于跨语言语义对齐）
# 纯标准库内置常量，无外部依赖；词典越大精度越高。
_BILINGUAL_MAP: dict[str, str] = {
    # 代词
    "我": "i", "你": "you", "他": "he", "她": "she", "它": "it",
    "我们": "we", "你们": "you", "他们": "they",
    # 常见动词
    "喜欢": "like", "爱": "love", "吃": "eat", "喝": "drink",
    "看": "see", "听": "hear", "说": "say", "做": "do", "想": "think",
    "是": "be", "有": "have", "去": "go", "来": "come",
    # 常见名词
    "苹果": "apple", "香蕉": "banana", "橙子": "orange",
    "天气": "weather", "今天": "today", "昨天": "yesterday",
    "明天": "tomorrow", "时间": "time",
    "项目": "project", "代码": "code", "程序": "program",
    "文档": "document", "文件": "file", "目录": "directory",
    # 形容词
    "好": "good", "坏": "bad", "大": "big", "小": "small",
    # 常见副词/虚词
    "不": "not", "的": "of",
}


def _stem_english(word: str) -> str:
    """简单英文词干化（后缀剥离），规则保守，避免误伤。

    顺序：ing -> ed -> s（s 只在非 ss/us/is 结尾时剥离）。
    """
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and len(word) > 3 and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


class HashBackend:
    """纯标准库 embedding 后端：分词 + 双语对齐 + n-gram + MinHash。

    离线可用，无网络依赖，精度低于真实 embedding，但跨语言同义句
    能产生合理相似度。固定维度 0/1 向量，用 cosine similarity。

    实现要点：
    - 中英文分词：英文按 word + 词干化，中文按单字 + bigram 词典对齐
    - 双语对齐：中文词通过内置词典映射到英文 token，使跨语言同义句共享 token
    - n-gram shingles：token 序列生成 n-gram
    - MinHash：用 dim 个 salt 生成 dim 维 0/1 签名，cosine 近似 Jaccard
    """

    def __init__(self, dim: int = 256, ngram: int = 2):
        if dim < 8:
            raise ValueError("dim must be >= 8")
        if ngram < 1:
            raise ValueError("ngram must be >= 1")
        self.dim = dim
        self.ngram = ngram
        self._salts = [f"memoryguard_salt_{i}".encode("utf-8") for i in range(dim)]

    def _tokenize(self, text: str) -> list[str]:
        tokens: list[str] = []
        # 英文词 + 词干化
        for m in re.finditer(r"[a-zA-Z][a-zA-Z0-9_]*", text.lower()):
            tokens.append(_stem_english(m.group(0)))
        # 中文：先匹配 bigram 词典，再单字词典，最后原字
        for seg in re.findall(r"[\u4e00-\u9fff]+", text):
            i = 0
            while i < len(seg):
                if i + 2 <= len(seg) and seg[i:i + 2] in _BILINGUAL_MAP:
                    tokens.append(_BILINGUAL_MAP[seg[i:i + 2]])
                    i += 2
                elif seg[i] in _BILINGUAL_MAP:
                    tokens.append(_BILINGUAL_MAP[seg[i]])
                    i += 1
                else:
                    tokens.append(seg[i])
                    i += 1
        return tokens

    def _shingles(self, tokens: list[str]) -> set[str]:
        if not tokens:
            return set()
        if len(tokens) < self.ngram:
            return set(tokens)
        return {
            "\x1f".join(tokens[i:i + self.ngram])
            for i in range(len(tokens) - self.ngram + 1)
        }

    def _minhash_bit(self, shingles: set[str], salt: bytes) -> int:
        """对 shingles 用 salt 取最小哈希，二值化（uint32 中位数为阈值）。"""
        min_h = min(
            int(hashlib.sha256(salt + s.encode("utf-8")).hexdigest()[:8], 16)
            for s in shingles
        )
        return 1 if min_h > 0x80000000 else 0

    def embed_text(self, text: str) -> list[float]:
        """生成 dim 维浮点向量（0.0 或 1.0）。空文本返回全零向量。"""
        tokens = self._tokenize(text)
        shingles = self._shingles(tokens)
        if not shingles:
            return [0.0] * self.dim
        return [float(self._minhash_bit(shingles, salt)) for salt in self._salts]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """cosine 相似度，优先用 numpy（若可用），否则标准库。"""
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    try:
        import numpy as np  # type: ignore
        arr_a = np.asarray(a[:n], dtype=np.float64)
        arr_b = np.asarray(b[:n], dtype=np.float64)
        na = float(np.linalg.norm(arr_a))
        nb = float(np.linalg.norm(arr_b))
        if na <= 0.0 or nb <= 0.0:
            return 0.0
        return float(np.dot(arr_a, arr_b) / (na * nb))
    except ImportError:
        pass
    # 标准库 fallback
    dot = 0.0
    na = 0.0
    nb = 0.0
    for i in range(n):
        x = a[i]
        y = b[i]
        dot += x * y
        na += x * x
        nb += y * y
    if na <= 0.0 or nb <= 0.0:
        return 0.0
    return dot / (math.sqrt(na) * math.sqrt(nb))


class SemanticDedup:
    """基于 embedding 的语义去重。

    补充 AutoOrganizer 的 Jaccard 启发式，处理跨语言、改写等场景。
    默认使用 HashBackend（纯标准库），可通过 backend 参数注入外部实现。
    """

    def __init__(
        self,
        workspace: str | Path,
        share_group_id: str,
        backend: EmbeddingBackend | None = None,
    ):
        self.store = SharedMemoryStore(workspace, share_group_id)
        self.backend: EmbeddingBackend = backend or HashBackend()

    def embed_text(self, text: str) -> list[float]:
        """生成文本的 embedding 向量。"""
        return self.backend.embed_text(text)

    def find_semantic_duplicates(
        self,
        new_text: str,
        threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        """查找与 new_text 语义相似的 active 记录。

        返回 [{memory_id, similarity, kind, record}]，按相似度降序。
        threshold 默认取环境变量 MEMORYGUARD_SEMANTIC_THRESHOLD（0.85）。
        """
        if threshold is None:
            threshold = _env_threshold()

        active_records = self.store.list_records(status="active")
        if not active_records:
            return []

        new_vec = self.embed_text(new_text)
        if not any(new_vec):
            return []

        results: list[dict[str, Any]] = []
        for rec in active_records:
            rec_vec = self.embed_text(rec.body)
            sim = cosine_similarity(new_vec, rec_vec)
            if sim >= threshold:
                results.append({
                    "memory_id": rec.memory_id,
                    "similarity": sim,
                    "kind": rec.kind.value if hasattr(rec.kind, "value") else str(rec.kind),
                    "record": rec,
                })
        results.sort(key=lambda x: -x["similarity"])
        return results

    def find_semantic_conflicts(
        self,
        new_text: str,
        new_kind: MemoryKind,
        threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        """查找语义冲突：语义相似但 kind 不同的记忆。

        返回 [{memory_id, similarity, kind, record}]。
        """
        dups = self.find_semantic_duplicates(new_text, threshold=threshold)
        new_kind_val = new_kind.value if hasattr(new_kind, "value") else str(new_kind)
        return [d for d in dups if d["kind"] != new_kind_val]
