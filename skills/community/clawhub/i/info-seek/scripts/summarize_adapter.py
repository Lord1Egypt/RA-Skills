#!/usr/bin/env python3
"""summarize_adapter.py — Infoseek v1.7.0 摘要适配器

主路径: summa TextRank（沙箱内置，零依赖，纯本地）
兜底路径: LLM API（用户配置 API Key 后启用，无 Key 时自动跳过）

调用模式:
  from summarize_adapter import summarize
  result = summarize(text="...", max_words=100)
"""
import json
import os
import re
import sys
from pathlib import Path

_dr = None


def _dep_reg():
    """S7：外部依赖可用性统一经 dep_registry 事实层求值（懒加载，缺失回退）。"""
    global _dr
    if _dr is None:
        import os as _os
        import sys as _sys
        _core = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'core')
        if _core not in _sys.path:
            _sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr

def _summa_summarize(text: str, max_words: int = 100) -> dict:
    """summa TextRank 主路径（沙箱内置，零依赖）"""
    try:
        # S7：可用性经 dep_registry 统一求值；在 try 块顶部 import，避免与外层函数名冲突
        if not _dep_reg().is_available("summa"):
            return None
        from summa.summarizer import summarize as summa_summarize_fn
        from summa.keywords import keywords as summa_keywords_fn

        # 摘要
        summary = summa_summarize_fn(text, words=max_words)

        # 关键词
        try:
            kw_text = summa_keywords_fn(text, words=15)
            keywords = [k.strip() for k in kw_text.split('\n') if k.strip()]
        except Exception:
            keywords = []

        return {
            "summary": summary.strip(),
            "keywords": keywords,
            "method": "summa_textrank",
            "input_length": len(text),
            "summary_length": len(summary.strip()),
            "fallback_used": False
        }
    except ImportError:
        return None

def _dual_run(text: str, max_words: int = 100) -> dict:
    """v1.7.2 新增：双跑择优（summa + jieba 都跑，取关键词多的）
    v1.7.3 增强：增加 regex fallback（沙箱网络问题时）
    v1.0.0 增强：增加零依赖共识兜底（最终防线，纯标准库，中英文皆可）
    """
    summa_result = _summa_summarize(text, max_words)
    jieba_result = _jieba_summarize(text, max_words)
    regex_result = _regex_summarize(text, max_words)

    summa_kw_count = len(summa_result.get('keywords', [])) if summa_result else 0
    jieba_kw_count = len(jieba_result.get('keywords', [])) if jieba_result else 0
    regex_kw_count = len(regex_result.get('keywords', [])) if regex_result else 0

    # v1.7.3: 三跑择优（summa + jieba + regex）
    # 注：仅关键词数 > 0 的候选参与择优；关键词为空的退化结果（如 regex 对
    # 中文文本返回空关键词 + 截断原文）不参与，确保零依赖兜底能真正触发。
    candidates = []
    if summa_result and summa_kw_count > 0:
        candidates.append(('summa', summa_kw_count, summa_result))
    if jieba_result and jieba_kw_count > 0:
        candidates.append(('jieba', jieba_kw_count, jieba_result))
    if regex_result and regex_kw_count > 0:
        candidates.append(('regex', regex_kw_count, regex_result))

    # v1.0.0: 零依赖共识兜底——仅当前三者全无结果时启用（最终防线）
    zerodep_kw_count = 0
    if not candidates:
        zerodep_result = _zerodep_summarize(text, max_words)
        if zerodep_result:
            zerodep_kw_count = len(zerodep_result.get('keywords', []))
            if zerodep_kw_count > 0:
                candidates.append(('zerodep', zerodep_kw_count, zerodep_result))

    if not candidates:
        return _truncation_fallback(text)

    # 取关键词最多的
    candidates.sort(key=lambda x: -x[1])
    chosen, _, result = candidates[0]
    result["chosen_by"] = chosen
    result["dual_run_stats"] = {
        "summa_kw_count": summa_kw_count,
        "jieba_kw_count": jieba_kw_count,
        "regex_kw_count": regex_kw_count,
        "zerodep_kw_count": zerodep_kw_count,
        "candidates_count": len(candidates)
    }
    if result.get('method') not in ('summa_textrank', 'jieba_textrank_zh', 'regex_wordfreq_en', 'zerodep_consensus'):
        result['method'] = f"tri_{result.get('method', 'unknown')}"
    return result

def _zerodep_summarize(text: str, max_words: int = 100) -> dict:
    """v1.0.0 新增：零依赖共识兜底（最终防线，纯标准库，中英文皆可）

    基于 infoseek_zerodep_nlp：多标准库估计器 + 共识投票 + 最长匹配抑制
    抽取关键词，取「含最多共识关键词」的句子作为抽取式摘要。
    """
    try:
        from infoseek_zerodep_nlp import summarize as zd_summarize
        from infoseek_zerodep_nlp import extract_keywords as zd_extract_keywords
    except Exception:
        return None

    try:
        summary = zd_summarize(text, max_sentences=3) or ""
        keywords = [w for w, _ in zd_extract_keywords(text, max_kw=15)]
        if not summary and not keywords:
            return None
        return {
            "summary": summary or text[:max_words * 5],
            "keywords": keywords,
            "method": "zerodep_consensus",
            "input_length": len(text),
            "summary_length": len(summary),
            "fallback_used": True
        }
    except Exception:
        return None

def _regex_summarize(text: str, max_words: int = 100) -> dict:
    """v1.7.3 新增：纯正则+词频英文 fallback（无 summa/jieba 时）

    算法：
      1. 正则提取英文/数字 token
      2. 统计词频
      3. 词频 top-N 作为关键词
      4. 词频 top 句作为摘要
    """
    import re as re_mod
    from collections import Counter

    # 1. token 提取
    tokens = re_mod.findall(r'[a-zA-Z][a-zA-Z0-9]{2,}', text)
    tokens_lower = [t.lower() for t in tokens]

    # 2. 停用词过滤
    stop_words = set([
        'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
        'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his',
        'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who',
        'boy', 'did', 'use', 'than', 'this', 'that', 'with', 'from',
        'have', 'will', 'they', 'been', 'more', 'what', 'when', 'make', 'like',
        'over', 'such', 'also', 'into', 'then', 'them', 'very', 'just',
        'about', 'where', 'would', 'there', 'their', 'these', 'which', 'should'
    ])

    filtered = [t for t in tokens_lower if t not in stop_words and len(t) >= 3]
    counter = Counter(filtered)

    # 3. 关键词（top 15）
    keywords = [w for w, _ in counter.most_common(15)]

    # 4. 摘要（词频 top 句）
    sentences = re_mod.split(r'[.!?。！？]', text)
    sent_scores = []
    for s in sentences:
        s = s.strip()
        if not s or len(s) < 20:
            continue
        score = sum(counter.get(t.lower(), 0) for t in re_mod.findall(r'[a-zA-Z][a-zA-Z0-9]{2,}', s))
        if score > 0:
            sent_scores.append((score, s))

    sent_scores.sort(key=lambda x: -x[0])
    summary = '. '.join(s for _, s in sent_scores[:3])
    if summary and not summary.endswith('.'):
        summary += '.'

    return {
        "summary": summary or text[:max_words * 5],
        "keywords": keywords,
        "method": "regex_wordfreq_en",
        "input_length": len(text),
        "summary_length": len(summary),
        "fallback_used": False
    }

def _jieba_summarize(text: str, max_words: int = 100) -> dict:
    """jieba 中文路径（v1.7.1 新增，针对中文文本优化）

    1. jieba.analyse.textrank 提取关键词（类似 summa 但更擅长中文）
    2. jieba.cut 切分词 + 词频统计 → 生成摘要
    """
    # 2026-09-29：jieba 探测/初始化统一经 jieba_bridge（原裸 import jieba/
    # jieba.analyse 两处；收敛后进程内探测一次）
    import sys as _sys
    import os as _os
    _core = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), 'core')
    if _core not in _sys.path:
        _sys.path.insert(0, _core)
    try:
        import jieba_bridge as _jb
    except Exception:
        return None
    if _jb.get_jieba() is None:
        return None
    try:
        # 关键词（Textrank 算法，中文友好）
        keywords = [k for k in _jb.textrank(text, 15) if len(k) > 1]
        if not keywords:
            # 降级到 TF-IDF
            keywords = [k for k in _jb.extract_tags(text, 15) if len(k) > 1]

        # 摘要（用词频 + 位置权重）
        try:
            words = _jb.lcut(text)
            # 统计词频（过滤停用词）
            stop_words = set(['的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'])
            word_freq = {}
            for w in (words or []):
                if len(w) < 2 or w in stop_words:
                    continue
                word_freq[w] = word_freq.get(w, 0) + 1

            # 取 top-词频词所在的句子
            sorted_words = sorted(word_freq.items(), key=lambda x: -x[1])[:max_words]
            top_words_set = {w for w, _ in sorted_words}

            sentences = text.replace('。', '。\n').replace('！', '！\n').replace('？', '？\n').split('\n')
            scored = []
            for s in sentences:
                if not s.strip():
                    continue
                _s_toks = _jb.lcut(s) or []
                score = sum(word_freq.get(w, 0) for w in _s_toks if w in top_words_set)
                if score > 0:
                    scored.append((score, s.strip()))

            # 按分数降序，取前 N 句
            scored.sort(key=lambda x: -x[0])
            summary = '。'.join(s for _, s in scored[:3])
            if not summary.endswith('。'):
                summary += '。'
        except Exception:
            summary = text[:max_words * 5] + '...'

        return {
            "summary": summary.strip() or text[:max_words * 5],
            "keywords": keywords,
            "method": "jieba_textrank_zh",
            "input_length": len(text),
            "summary_length": len(summary),
            "fallback_used": False
        }
    except ImportError:
        return None

def _auto_detect_summarizer(text: str) -> str:
    """根据文本语言自动选择摘要器（v1.7.1 新增）

    返回: "jieba" 或 "summa"
    """
    # 检测中文字符比例
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    total_chars = len(text)
    if total_chars == 0:
        return "summa"
    chinese_ratio = chinese_chars / total_chars
    return "jieba" if chinese_ratio > 0.3 else "summa"

def _truncation_fallback(text: str, max_chars: int = 500) -> dict:
    """最低级降级：截断前 N 字符（永远可用）"""
    return {
        "summary": text[:max_chars].strip() + ("..." if len(text) > max_chars else ""),
        "keywords": [],
        "method": "truncation_fallback",
        "input_length": len(text),
        "summary_length": min(len(text), max_chars),
        "fallback_used": True,
        "fallback_reason": "summa 未安装"
    }

def _llm_summarize(text: str, max_words: int, api_key: str, api_base: str = None, model: str = "claude-haiku-4-5-20251001") -> dict:
    """LLM API 兜底路径（需要 API Key）

    支持 Anthropic / OpenAI 兼容接口
    """
    try:
        import urllib.request
        import urllib.error

        # 默认走 Anthropic
        if api_base is None:
            api_base = "https://api.anthropic.com"

        # 截断长文本（避免超 token）
        truncated_text = text[:5000]

        if "anthropic" in api_base:
            # Anthropic Messages API
            data = {
                "model": model,
                "max_tokens": max(max_words * 2, 200),
                "messages": [{
                    "role": "user",
                    "content": f"请用中文摘要以下文本（不超过 {max_words} 词），并提取 10 个关键词（逗号分隔）。\n\n文本：\n{truncated_text}\n\n输出格式（严格 JSON）：\n{{\"summary\": \"...\", \"keywords\": [\"...\"]}}"
                }]
            }
            req = urllib.request.Request(
                f"{api_base}/v1/messages",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                }
            )
        elif "openai" in api_base or api_base.endswith("openai.com"):
            # OpenAI Chat Completions API
            data = {
                "model": model,
                "messages": [{
                    "role": "user",
                    "content": f"请用中文摘要以下文本（不超过 {max_words} 词），并提取 10 个关键词（逗号分隔）。\n\n文本：\n{truncated_text}\n\n输出格式（严格 JSON）：\n{{\"summary\": \"...\", \"keywords\": [\"...\"]}}"
                }],
                "max_tokens": max(max_words * 2, 200)
            }
            # v3.0.0 GA 修复: 规范化 api_base（避免双 /v1）
            base = api_base.rstrip('/').removesuffix('/v1')
            req = urllib.request.Request(
                f"{base}/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )
        else:
            # 通用 OpenAI 兼容
            data = {
                "model": model,
                "messages": [{
                    "role": "user",
                    "content": f"请摘要（{max_words} 词内）+ 提取 10 个关键词。\n\n{truncated_text}\n\n严格 JSON 输出。"
                }],
                "max_tokens": max(max_words * 2, 200)
            }
            # v3.0.0 GA 修复: 规范化 api_base（避免双 /v1）
            base = api_base.rstrip('/').removesuffix('/v1')
            req = urllib.request.Request(
                f"{base}/v1/chat/completions",
                data=json.dumps(data).encode('utf-8'),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
            )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        # 解析响应
        if "anthropic" in api_base:
            content_text = result.get("content", [{}])[0].get("text", "")
        else:
            content_text = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        # 提取 JSON
        json_match = re.search(r'\{[^{}]*"summary"[^{}]*\}', content_text, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group(0))
            return {
                "summary": parsed.get("summary", content_text),
                "keywords": parsed.get("keywords", []),
                "method": f"llm_{model}",
                "input_length": len(text),
                "summary_length": len(parsed.get("summary", "")),
                "fallback_used": False
            }

        # JSON 解析失败：返回原文
        return {
            "summary": content_text.strip(),
            "keywords": [],
            "method": f"llm_{model}_raw",
            "input_length": len(text),
            "summary_length": len(content_text.strip()),
            "fallback_used": False
        }

    except Exception as e:
        return None  # LLM 调用失败 → 降级到 summa

def summarize(text: str, max_words: int = 100, prefer: str = "summa", llm_api_key: str = None,
             llm_api_base: str = None, llm_model: str = None) -> dict:
    """
    统一摘要接口（v1.7.0/v1.7.1/v1.7.2）

    策略（v1.7.2 增强）:
      1. prefer="auto"（默认）→ 双跑择优（summa + jieba 都跑，取关键词多的）
      2. prefer="summa" → 强制 summa
      3. prefer="jieba" → 强制 jieba（中文专用）
      4. prefer="llm" + llm_api_key → LLM API 优先
      5. 无 llm_api_key → 降级到本地

    参数:
        text: 待摘要文本
        max_words: 摘要最大词数
        prefer: 首选路径（"auto"/"summa"/"jieba"/"llm"）
        llm_api_key: LLM API Key（None = 禁用 LLM）
        llm_api_base: LLM API 基础 URL（None = 默认 Anthropic）
        llm_model: LLM 模型名（None = 默认 claude-haiku）

    返回:
        dict 含 summary, keywords, method, fallback_used, chosen_by, dual_run_stats
    """
    if not text or not text.strip():
        return {
            "summary": "",
            "keywords": [],
            "method": "empty_input",
            "input_length": 0,
            "summary_length": 0,
            "fallback_used": False
        }

    # v1.7.2: prefer="auto" → 双跑择优
    if prefer == "auto":
        result = _dual_run(text, max_words)
        # 简化：直接返回
        result["fallback_used"] = False
        result["detected_language"] = "zh" if _auto_detect_summarizer(text) == "jieba" else "en"
        return result

    result = None
    fallback_used = False
    fallback_reason = None

    # 第一步：根据 prefer 决定调用顺序
    if prefer == "llm" and llm_api_key:
        result = _llm_summarize(text, max_words, llm_api_key, llm_api_base, llm_model)
        if result is None:
            fallback_reason = "llm_failed"
            fallback_used = True
            result = _summa_summarize(text, max_words)
            if result is None:
                result = _jieba_summarize(text, max_words)
            if result is None:
                # v1.0.0: 零依赖共识兜底（最终防线，纯标准库）
                result = _zerodep_summarize(text, max_words)
            if result is None:
                result = _truncation_fallback(text)
                result["fallback_reason"] = "llm_failed + summa_unavailable + jieba_unavailable + zerodep_unavailable"
            else:
                result["fallback_reason"] = "llm_failed → summa/jieba 兜底"
    elif prefer == "jieba":
        # 强制 jieba
        result = _jieba_summarize(text, max_words)
        if result is None:
            fallback_used = True
            fallback_reason = "jieba_unavailable"
            result = _summa_summarize(text, max_words)
            if result is None:
                # v1.0.0: 零依赖共识兜底（最终防线，纯标准库）
                result = _zerodep_summarize(text, max_words)
            if result is None:
                result = _truncation_fallback(text)
                result["fallback_reason"] = "jieba_unavailable + summa_unavailable + zerodep_unavailable"
            else:
                result["fallback_reason"] = "jieba_unavailable → summa 兜底"
    else:
        # 默认 summa（无需 API Key）
        result = _summa_summarize(text, max_words)
        if result is None:
            # summa 不可用 → 降级 jieba
            result = _jieba_summarize(text, max_words)
            if result is None:
                fallback_used = True
                fallback_reason = "summa_unavailable + jieba_unavailable → zerodep 兜底"
                # v1.0.0: 零依赖共识兜底（最终防线，纯标准库）
                result = _zerodep_summarize(text, max_words)
                if result is None:
                    result = _truncation_fallback(text)
            else:
                # summa 不可用但 jieba 可用
                fallback_used = True
                fallback_reason = "summa_unavailable → jieba 兜底"
        # v1.7.1: summa 关键词少时自动 jieba 备份
        elif _auto_detect_summarizer(text) == "jieba":
            jieba_result = _jieba_summarize(text, max_words)
            if jieba_result and len(jieba_result.get('keywords', [])) > len(result.get('keywords', [])):
                result = jieba_result
                fallback_reason = "summa → jieba (更多关键词)"
                fallback_used = True

    result["fallback_used"] = fallback_used
    if fallback_reason and "fallback_reason" not in result:
        result["fallback_reason"] = fallback_reason

    # v1.7.1: 添加 detected_language 字段
    if "detected_language" not in result:
        result["detected_language"] = "zh" if _auto_detect_summarizer(text) == "jieba" else "en"

    return result

def summarize_url(url: str, max_words: int = 100, prefer: str = "summa",
                  llm_api_key: str = None, fetch_timeout: int = 30) -> dict:
    """
    URL 摘要（包装 fetch + summarize）

    fetch_content 已包含在 fetch_content 工具中，这里只做"文本摘要"
    （URL 获取由调用方负责）
    """
    # 实际集成时，应该先调 fetch_content，再调 summarize
    # 这里只占位
    raise NotImplementedError("请先调用 fetch_content 获取文本，再调用 summarize(text=...)")

# CLI 入口
def main():
    """命令行测试入口：python summarize_adapter.py <text_or_file>"""
    import sys
    if len(sys.argv) < 2:
        print("用法: python summarize_adapter.py <text_or_file>")
        print("环境变量: INFOSEEK_LLM_API_KEY, INFOSEEK_LLM_API_BASE, INFOSEEK_LLM_MODEL")
        sys.exit(1)

    arg = sys.argv[1]
    if Path(arg).is_file():
        text = Path(arg).read_text(encoding='utf-8')
    else:
        text = arg

    # v1.0.1 PATCH: LLM key 经 KeyManager 归一化读取（无注册时退化 env）
    try:
        from core.key_manager import KeyManager
        _llm_key = KeyManager.instance().get('infoseek_llm')
    except Exception:
        _llm_key = os.environ.get('INFOSEEK_LLM_API_KEY')
    result = summarize(
        text=text,
        max_words=100,
        llm_api_key=_llm_key,
        llm_api_base=os.environ.get('INFOSEEK_LLM_API_BASE'),
        llm_model=os.environ.get('INFOSEEK_LLM_MODEL')
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()