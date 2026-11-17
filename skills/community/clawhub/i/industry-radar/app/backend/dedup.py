"""
M4-a 去重：URL 精确去重 + simhash 近似去重。

中文/英文混排分词采用「字符二元组 + 英文单词」策略，
无需外部分词库即可给出稳定指纹，适配免费源场景。
"""
from __future__ import annotations

import hashlib
import logging
import re
from typing import Dict, List

from config import DEDUP_HAMMING

log = logging.getLogger("industryradar.dedup")

_WORD = re.compile(r"[a-zA-Z0-9]+")
_CJK = re.compile(r"[\u4e00-\u9fff]")
_HASH_BITS = 64


def tokenize(text: str) -> List[str]:
    """英文按单词、中文按二元组切分。"""
    text = (text or "").lower()
    tokens: List[str] = _WORD.findall(text)
    cjk = _CJK.findall(text)
    for i in range(len(cjk) - 1):
        tokens.append(cjk[i] + cjk[i + 1])
    if len(cjk) == 1:
        tokens.append(cjk[0])
    return tokens


def simhash(tokens: List[str], bits: int = _HASH_BITS) -> int:
    if not tokens:
        return 0
    vector = [0] * bits
    for tok in tokens:
        h = int(hashlib.md5(tok.encode("utf-8")).hexdigest(), 16)
        for i in range(bits):
            vector[i] += 1 if (h >> i) & 1 else -1
    fingerprint = 0
    for i in range(bits):
        if vector[i] > 0:
            fingerprint |= 1 << i
    return fingerprint


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def simhash_text(text: str) -> int:
    return simhash(tokenize(text))


def deduplicate(articles: List[Dict], existing_hashes: set,
                existing_simhashes: List[int] | None = None,
                threshold: int = DEDUP_HAMMING) -> List[Dict]:
    """
    返回去重后的文章列表，并给每篇打上 `_simhash`。

    去重维度：
      1. url_hash 完全一致（跨源同链接）
      2. simhash 汉明距离 <= threshold（跨源转载/近似稿）
      3. 批内互相去重
    """
    existing_simhashes = existing_simhashes or []
    seen_urls = set(existing_hashes)
    kept: List[Dict] = []

    for art in articles:
        uh = art.get("url_hash")
        if uh and uh in seen_urls:
            continue

        fp = simhash_text(f"{art.get('title', '')}\n{art.get('content', '')[:2000]}")
        art["_simhash"] = fp

        dup = any(hamming(fp, old) <= threshold for old in existing_simhashes) or \
              any(hamming(fp, k["_simhash"]) <= threshold for k in kept)
        if dup:
            continue

        if uh:
            seen_urls.add(uh)
        kept.append(art)

    log.info("dedup: %d -> %d", len(articles), len(kept))
    return kept