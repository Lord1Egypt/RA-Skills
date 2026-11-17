#!/usr/bin/env python3
"""
translate_utils.py — 翻译工具模块

功能：
  1. detect_language(text) → 判断文本是否为"全外文"（CJK 占比 < 5%）
  2. translate_text(text, ...) → 翻译单段文本（C:translators → A:本地LLM 降级）
  3. batch_translate(texts, ...) → 批量翻译（合并请求降低调用次数）
"""

import re
import sys
import unicodedata
from typing import Optional

# ──────────────────────────────────────────────
# 语言检测
# ──────────────────────────────────────────────

def cjk_ratio(text: str) -> float:
    """计算文本中 CJK（中日韩）字符的占比"""
    if not text:
        return 0.0
    cjk_count = sum(
        1 for ch in text
        if unicodedata.category(ch) in ('Lo',) and ord(ch) > 0x2E7F
    )
    # 更精确：用 Unicode 区段判断
    cjk_count = sum(
        1 for ch in text
        if (
            '\u4e00' <= ch <= '\u9fff' or   # CJK 统一表意文字
            '\u3400' <= ch <= '\u4dbf' or   # CJK 扩展A
            '\u20000' <= ch <= '\u2a6df' or # CJK 扩展B
            '\uf900' <= ch <= '\ufaff' or   # CJK 兼容表意文字
            '\u3040' <= ch <= '\u309f' or   # 平假名
            '\u30a0' <= ch <= '\u30ff'      # 片假名
        )
    )
    total = len([c for c in text if not c.isspace()])
    return cjk_count / total if total > 0 else 0.0


def is_foreign_pdf(texts: list[str], cjk_threshold: float = 0.05, min_chars: int = 50) -> bool:
    """
    判断 PDF 是否为"全外文"文档。

    条件：
    - 合并所有文本后 CJK 字符占比 < cjk_threshold（默认 5%）
    - 总有效字符数 > min_chars（排除空文档误判）

    返回 True 表示"全外文，需要翻译"
    """
    full_text = " ".join(texts)
    total_chars = len([c for c in full_text if not c.isspace()])
    if total_chars < min_chars:
        return False
    ratio = cjk_ratio(full_text)
    return ratio < cjk_threshold


# ──────────────────────────────────────────────
# 专有名词保护
# ──────────────────────────────────────────────

# 常见英文缩写/专有名词（全大写或已知词），翻译时保留
_PROTECT_PATTERNS = [
    r'\b[A-Z]{2,}\b',          # 全大写缩写: HR, KPI, GDP, AI, CEO
    r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b',  # 日期
    r'\b\d+[\.,]\d+\b',        # 数字
    r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}',  # 邮箱
    r'https?://\S+',            # URL
]

def _protect_terms(text: str) -> tuple[str, dict]:
    """
    用占位符替换需要保护的专有名词，返回处理后的文本和还原映射。
    """
    protected = {}
    counter = [0]

    def replacer(m):
        key = f"__PROT{counter[0]}__"
        protected[key] = m.group(0)
        counter[0] += 1
        return key

    for pat in _PROTECT_PATTERNS:
        text = re.sub(pat, replacer, text)

    return text, protected


def _restore_terms(text: str, protected: dict) -> str:
    """将占位符还原为原始专有名词"""
    for key, val in protected.items():
        text = text.replace(key, val)
    return text


# ──────────────────────────────────────────────
# 翻译函数
# ──────────────────────────────────────────────

_translators_engine: Optional[str] = None  # 缓存可用引擎


def _find_working_engine() -> Optional[str]:
    """探测可用的 translators 引擎（按优先级）"""
    global _translators_engine
    if _translators_engine:
        return _translators_engine

    try:
        import translators as ts
    except ImportError:
        return None

    for engine in ['google', 'alibaba', 'baidu', 'youdao', 'bing']:
        try:
            result = ts.translate_text("test", to_language='zh', translator=engine)
            if result:
                _translators_engine = engine
                return engine
        except Exception:
            continue
    return None


def translate_text(
    text: str,
    from_lang: str = 'auto',
    to_lang: str = 'zh',
    verbose: bool = False,
) -> str:
    """
    翻译单段文本。

    策略：
    1. C: translators 库（google → alibaba → baidu → youdao 依次降级）
    2. A: 本地 LLM（通过 Ollama / OpenAI-compatible API）

    空文本或纯符号直接返回原文。
    专有名词（全大写缩写等）用占位符保护，翻译后还原。
    """
    text = text.strip()
    if not text or len(text) < 2:
        return text

    # 如果本身是纯数字/符号，直接返回
    if re.match(r'^[\d\s\W]+$', text):
        return text

    # 保护专有名词
    protected_text, protected_map = _protect_terms(text)

    # ── 策略 C: translators 库 ──
    engine = _find_working_engine()
    if engine:
        try:
            import translators as ts
            result = ts.translate_text(
                protected_text,
                from_language=from_lang,
                to_language=to_lang,
                translator=engine,
            )
            if result:
                result = _restore_terms(result, protected_map)
                if verbose:
                    print(f"  [翻译|{engine}] {text[:30]!r} → {result[:30]!r}", file=sys.stderr)
                return result
        except Exception as e:
            if verbose:
                print(f"  [翻译|{engine}失败] {e}", file=sys.stderr)
            global _translators_engine
            _translators_engine = None  # 重置，下次重探

    # ── 策略 A: 本地 LLM 降级 ──
    try:
        result = _translate_via_llm(text, to_lang=to_lang, verbose=verbose)
        if result:
            return result
    except Exception as e:
        if verbose:
            print(f"  [翻译|LLM失败] {e}", file=sys.stderr)

    # 全部失败，返回原文
    return text


def _translate_via_llm(text: str, to_lang: str = 'zh', verbose: bool = False) -> Optional[str]:
    """
    降级策略 A：通过本地 LLM（Ollama / OpenAI-compatible）翻译。
    批量文本用 '|||' 分隔减少调用次数。
    """
    import os
    import json

    # 优先从环境变量或本地配置读取 API 地址
    api_base = os.environ.get("OPENAI_API_BASE", "http://localhost:11434/v1")
    api_key = os.environ.get("OPENAI_API_KEY", "dummy")
    model = os.environ.get("TRANSLATE_MODEL", "qwen2.5:7b")

    try:
        import requests
        prompt = (
            f"Translate the following text to Simplified Chinese. "
            f"Keep proper nouns, abbreviations (all-caps), numbers, and technical terms in English. "
            f"Return ONLY the translated text, no explanation.\n\n"
            f"Text: {text}"
        )
        resp = requests.post(
            f"{api_base}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "max_tokens": 500,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        result = data["choices"][0]["message"]["content"].strip()
        if verbose:
            print(f"  [翻译|LLM] {text[:30]!r} → {result[:30]!r}", file=sys.stderr)
        return result
    except Exception as e:
        raise RuntimeError(f"LLM 翻译失败: {e}") from e


def batch_translate(
    texts: list[str],
    from_lang: str = 'auto',
    to_lang: str = 'zh',
    batch_size: int = 20,
    verbose: bool = False,
) -> list[str]:
    """
    批量翻译文本列表。

    为降低 API 调用次数，将多段文本合并后一次请求，
    用唯一分隔符拆分结果，失败时逐条 fallback。

    参数:
        texts: 待翻译文本列表
        batch_size: 每批合并的文本数（默认 20）
    返回:
        与 texts 等长的翻译结果列表
    """
    if not texts:
        return []

    results = [''] * len(texts)
    SEP = '\n|||NEXT|||\n'

    for batch_start in range(0, len(texts), batch_size):
        batch = texts[batch_start:batch_start + batch_size]
        batch_indices = list(range(batch_start, batch_start + len(batch)))

        # 过滤空/纯符号文本，直接返回原文
        to_translate_idx = []
        for i, t in enumerate(batch):
            if t.strip() and not re.match(r'^[\d\s\W]+$', t.strip()):
                to_translate_idx.append(i)
            else:
                results[batch_indices[i]] = batch[i]

        if not to_translate_idx:
            continue

        # 合并翻译
        combined = SEP.join(batch[i] for i in to_translate_idx)
        try:
            translated_combined = translate_text(combined, from_lang, to_lang, verbose)
            parts = translated_combined.split('|||NEXT|||')
            parts = [p.strip() for p in parts]

            if len(parts) == len(to_translate_idx):
                for j, idx in enumerate(to_translate_idx):
                    results[batch_indices[idx]] = parts[j]
            else:
                # 拆分失败，逐条翻译
                if verbose:
                    print(f"  [批量翻译] 拆分失败（期望{len(to_translate_idx)}段，得到{len(parts)}段），改逐条翻译", file=sys.stderr)
                for idx in to_translate_idx:
                    results[batch_indices[idx]] = translate_text(batch[idx], from_lang, to_lang, verbose)

        except Exception as e:
            if verbose:
                print(f"  [批量翻译失败] {e}，改逐条翻译", file=sys.stderr)
            for idx in to_translate_idx:
                try:
                    results[batch_indices[idx]] = translate_text(batch[idx], from_lang, to_lang, verbose)
                except Exception:
                    results[batch_indices[idx]] = batch[idx]  # 彻底失败保留原文

    return results
