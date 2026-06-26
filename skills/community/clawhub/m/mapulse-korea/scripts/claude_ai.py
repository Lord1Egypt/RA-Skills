#!/usr/bin/env python3
"""
Mapulse — Claude AI 分析层
接入 Claude API 提供深度利弊分析、用户语言偏好感知

支持:
  1. Anthropic 直连 (ANTHROPIC_API_KEY)
  2. OpenRouter 代理 (OPENROUTER_API_KEY)
  3. 无 API 时 fallback 到规则引擎

功能:
  - analyze_with_claude(): 对市场数据做利弊分析
  - detect_language(): 检测用户语言偏好
  - get_user_preferences(): 获取用户历史偏好
  - update_user_preferences(): 更新偏好记录
"""

import os
import sys
import json
import time
import re
import requests
import logging

sys.path.insert(0, os.path.dirname(__file__))

logger = logging.getLogger("mapulse.claude")

# ─── API 配置 (from environment variables only) ───

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
CLAUDE_MODEL = os.environ.get("MAPULSE_CLAUDE_MODEL", "claude-sonnet-4")


def reload_api_keys():
    """Reload API keys from environment variables."""
    global ANTHROPIC_API_KEY, OPENROUTER_API_KEY, CLAUDE_MODEL
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
    CLAUDE_MODEL = os.environ.get("MAPULSE_CLAUDE_MODEL", "claude-sonnet-4")

# Token 限制 (控制成本)
MAX_INPUT_TOKENS = 2000
MAX_OUTPUT_TOKENS = 800


def _get_api_config():
    """选择可用的 API 通道"""
    if ANTHROPIC_API_KEY:
        return {
            "type": "anthropic",
            "url": "https://api.anthropic.com/v1/messages",
            "headers": {
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        }
    elif OPENROUTER_API_KEY:
        return {
            "type": "openrouter",
            "url": "https://openrouter.ai/api/v1/chat/completions",
            "headers": {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "content-type": "application/json",
            },
        }
    return None


def _call_claude(system_prompt, user_message, max_tokens=MAX_OUTPUT_TOKENS):
    """调用 Claude API (Anthropic 或 OpenRouter)"""
    config = _get_api_config()
    if not config:
        return None

    try:
        if config["type"] == "anthropic":
            payload = {
                "model": CLAUDE_MODEL,
                "max_tokens": max_tokens,
                "system": system_prompt,
                "messages": [{"role": "user", "content": user_message}],
            }
            resp = requests.post(config["url"], headers=config["headers"],
                                 json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["content"][0]["text"]
            else:
                logger.warning(f"Anthropic API error {resp.status_code}: {resp.text[:200]}")
                return None

        elif config["type"] == "openrouter":
            or_model = CLAUDE_MODEL if "/" in CLAUDE_MODEL else f"anthropic/{CLAUDE_MODEL}"
            payload = {
                "model": or_model,
                "max_tokens": max_tokens,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            }
            resp = requests.post(config["url"], headers=config["headers"],
                                 json=payload, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                logger.warning(f"OpenRouter API error {resp.status_code}: {resp.text[:200]}")
                return None

    except Exception as e:
        logger.error(f"Claude API call failed: {e}")
        return None


# ═══════════════════════════════════════════
#  1. 语言检测 & 偏好
# ═══════════════════════════════════════════

def detect_language(text):
    """检测用户输入语言
    Returns: 'ko' | 'zh' | 'en' | 'ja'
    """
    # 韩文字符范围
    ko_count = len(re.findall(r'[\uAC00-\uD7AF\u3130-\u318F]', text))
    # 中文字符范围
    zh_count = len(re.findall(r'[\u4E00-\u9FFF]', text))
    # 日文字符范围
    ja_count = len(re.findall(r'[\u3040-\u309F\u30A0-\u30FF]', text))
    # ASCII/Latin
    en_count = len(re.findall(r'[a-zA-Z]', text))

    scores = {"ko": ko_count, "zh": zh_count, "ja": ja_count, "en": en_count}
    best = max(scores, key=scores.get)

    # 如果没有明显语言特征，默认中文 (群组主要用户)
    if max(scores.values()) == 0:
        return "zh"

    return best


LANG_LABELS = {
    "ko": "한국어",
    "zh": "中文",
    "en": "English",
    "ja": "日本語",
}


# ═══════════════════════════════════════════
#  2. 用户偏好管理 (SQLite)
# ═══════════════════════════════════════════

def _get_prefs_conn():
    """获取 DB 连接"""
    try:
        from db import get_conn, init_db
        return get_conn()
    except:
        return None


def _ensure_prefs_table():
    """确保偏好表存在"""
    conn = _get_prefs_conn()
    if not conn:
        return
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                language TEXT DEFAULT 'auto',
                interested_tickers TEXT DEFAULT '[]',
                analysis_style TEXT DEFAULT 'balanced',
                risk_tolerance TEXT DEFAULT 'moderate',
                focus_sectors TEXT DEFAULT '[]',
                query_history TEXT DEFAULT '[]',
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to create prefs table: {e}")
    finally:
        conn.close()


_ensure_prefs_table()


def get_user_preferences(user_id):
    """获取用户偏好"""
    conn = _get_prefs_conn()
    if not conn:
        return _default_prefs()

    try:
        row = conn.execute(
            "SELECT * FROM user_preferences WHERE user_id=?", (user_id,)
        ).fetchone()
        if row:
            prefs = dict(row)
            # 解析 JSON 字段
            for field in ["interested_tickers", "focus_sectors", "query_history"]:
                try:
                    prefs[field] = json.loads(prefs.get(field, "[]"))
                except:
                    prefs[field] = []
            return prefs
        return _default_prefs()
    except:
        return _default_prefs()
    finally:
        conn.close()


def _default_prefs():
    return {
        "language": "auto",
        "interested_tickers": [],
        "analysis_style": "balanced",
        "risk_tolerance": "moderate",
        "focus_sectors": [],
        "query_history": [],
    }


def update_user_preferences(user_id, query_text, detected_lang, tickers_queried=None):
    """根据用户查询自动更新偏好

    - 记录语言偏好
    - 记录关注的股票
    - 记录查询历史 (最近20条)
    """
    conn = _get_prefs_conn()
    if not conn:
        return

    try:
        prefs = get_user_preferences(user_id)

        # 更新语言
        if detected_lang and detected_lang != "auto":
            prefs["language"] = detected_lang

        # 更新关注股票
        if tickers_queried:
            current = prefs.get("interested_tickers", [])
            for t in tickers_queried:
                if t not in current:
                    current.append(t)
            # 保留最近关注的 20 个
            prefs["interested_tickers"] = current[-20:]

        # 查询历史 (最近20条)
        history = prefs.get("query_history", [])
        history.append({
            "q": query_text[:100],
            "lang": detected_lang,
            "ts": int(time.time()),
        })
        prefs["query_history"] = history[-20:]

        # 推断关注领域
        prefs["focus_sectors"] = _infer_sectors(prefs["interested_tickers"])

        # 写入 DB
        conn.execute("""
            INSERT INTO user_preferences (user_id, language, interested_tickers,
                analysis_style, risk_tolerance, focus_sectors, query_history, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            ON CONFLICT(user_id) DO UPDATE SET
                language=excluded.language,
                interested_tickers=excluded.interested_tickers,
                focus_sectors=excluded.focus_sectors,
                query_history=excluded.query_history,
                updated_at=datetime('now')
        """, (
            user_id,
            prefs["language"],
            json.dumps(prefs["interested_tickers"]),
            prefs.get("analysis_style", "balanced"),
            prefs.get("risk_tolerance", "moderate"),
            json.dumps(prefs["focus_sectors"]),
            json.dumps(prefs["query_history"]),
        ))
        conn.commit()
    except Exception as e:
        logger.error(f"Failed to update preferences: {e}")
    finally:
        conn.close()


# 股票 → 板块 映射
SECTOR_MAP = {
    "005930": "반도체", "000660": "반도체", "009150": "반도체",
    "035420": "IT/플랫폼", "035720": "IT/플랫폼", "036570": "게임",
    "373220": "배터리/EV", "051910": "배터리/EV", "006400": "배터리/EV",
    "068270": "바이오",
    "005380": "자동차", "000270": "자동차",
    "096770": "에너지", "015760": "에너지",
    "003670": "철강/소재", "028260": "건설/인프라",
    "352820": "엔터",
}


def _infer_sectors(tickers):
    """从关注股票推断关注板块"""
    sectors = {}
    for t in tickers:
        s = SECTOR_MAP.get(t)
        if s:
            sectors[s] = sectors.get(s, 0) + 1
    # 按频率排序
    return sorted(sectors.keys(), key=lambda x: sectors[x], reverse=True)[:5]


# ═══════════════════════════════════════════
#  3. Claude AI 利弊分析
# ═══════════════════════════════════════════

def analyze_with_claude(market_data, query_text, user_id=None):
    """用 Claude 对市场数据做利弊分析

    Args:
        market_data: str - 已格式化的市场数据文本
        query_text: str - 用户原始查询
        user_id: str - 用户ID (用于获取偏好)

    Returns:
        str - 利弊分析文本 (已按用户语言格式化)
    """
    # 检测语言
    lang = detect_language(query_text)

    # 获取用户偏好
    prefs = get_user_preferences(user_id) if user_id else _default_prefs()
    if prefs.get("language") and prefs["language"] != "auto":
        lang = prefs["language"]

    # 构建 system prompt
    lang_instruction = {
        "ko": "한국어로 답변하세요.",
        "zh": "用中文回答。",
        "en": "Reply in English.",
        "ja": "日本語で回答してください。",
    }.get(lang, "用中文回答。")

    focus_context = ""
    if prefs.get("focus_sectors"):
        focus_context = f"\n用户关注的板块: {', '.join(prefs['focus_sectors'])}"
    if prefs.get("interested_tickers"):
        from fetch_briefing import STOCK_NAMES
        names = [STOCK_NAMES.get(t, t) for t in prefs["interested_tickers"][-5:]]
        focus_context += f"\n用户关注的股票: {', '.join(names)}"

    system_prompt = f"""你是 Mapulse 韩国股市AI分析师。根据提供的市场数据，给出简洁的利弊分析。

要求:
1. {lang_instruction}
2. 分析分为 ✅ 利好因素 和 ⚠️ 风险因素 两部分
3. 每部分 2-4 条，每条一句话
4. 最后给一句总结性判断
5. 不要给具体买卖建议或价格预测
6. 保持客观、专业、简洁 (总字数 ≤ 300)
{focus_context}"""

    user_message = f"""用户查询: {query_text}

市场数据:
{market_data[:MAX_INPUT_TOKENS]}

请给出利弊分析:"""

    # 调用 Claude
    result = _call_claude(system_prompt, user_message)

    if result:
        return _format_analysis(result, lang)

    # Fallback: 规则引擎分析
    return _rule_based_analysis(market_data, lang)


def _format_analysis(raw_text, lang):
    """格式化 Claude 返回的分析"""
    header = {
        "ko": "🧠 *AI 분석*",
        "zh": "🧠 *AI 分析*",
        "en": "🧠 *AI Analysis*",
        "ja": "🧠 *AI 分析*",
    }.get(lang, "🧠 *AI 分析*")

    disclaimer = {
        "ko": "\n_⚠️ AI 분석은 참고용이며 투자 조언이 아닙니다._",
        "zh": "\n_⚠️ AI分析仅供参考，不构成投资建议。_",
        "en": "\n_⚠️ AI analysis is for reference only, not investment advice._",
        "ja": "\n_⚠️ AI分析は参考用であり、投資アドバイスではありません。_",
    }.get(lang, "\n_⚠️ AI分析仅供参考，不构成投资建议。_")

    return f"\n{header}\n\n{raw_text}{disclaimer}"


def _rule_based_analysis(market_data, lang):
    """无 API 时的规则引擎 fallback"""
    text = market_data.lower()

    pros = []
    cons = []

    # 检测关键信号
    if "🟢" in market_data:
        count = market_data.count("🟢")
        if count >= 3:
            pros.append("多数股票上涨，市场情绪偏乐观")

    if "🔴" in market_data:
        count = market_data.count("🔴")
        if count >= 3:
            cons.append("多数股票下跌，市场承压")

    # 半导体信号
    if any(w in text for w in ["삼성전자", "sk하이닉스", "반도체", "semiconductor"]):
        if "+".join(["+"]) in market_data:
            pros.append("半导体板块走强，AI/HBM需求持续")
        elif "-" in market_data:
            cons.append("半导体板块承压，注意全球需求变化")

    # 外资动向
    if "외국인" in text and ("순매도" in text or "매도" in text):
        cons.append("外资净卖出，资金流出压力")
    elif "외국인" in text and ("순매수" in text or "매수" in text):
        pros.append("外资净买入，资金流入支撑")

    if not pros:
        pros.append("数据不足以判断明确利好因素")
    if not cons:
        cons.append("当前未发现明显风险信号")

    # 按语言格式化
    if lang == "ko":
        lines = ["🧠 *AI 분석*\n"]
        lines.append("✅ *긍정 요인:*")
        for p in pros:
            lines.append(f"  • {p}")
        lines.append("\n⚠️ *리스크 요인:*")
        for c in cons:
            lines.append(f"  • {c}")
        lines.append("\n_⚠️ 규칙 기반 분석입니다. Claude AI 연결 시 더 정확한 분석이 가능합니다._")
    elif lang == "en":
        lines = ["🧠 *AI Analysis*\n"]
        lines.append("✅ *Positive Factors:*")
        for p in pros:
            lines.append(f"  • {p}")
        lines.append("\n⚠️ *Risk Factors:*")
        for c in cons:
            lines.append(f"  • {c}")
        lines.append("\n_⚠️ Rule-based analysis. Connect Claude AI for deeper insights._")
    else:  # zh / ja
        lines = ["🧠 *AI 分析*\n"]
        lines.append("✅ *利好因素:*")
        for p in pros:
            lines.append(f"  • {p}")
        lines.append("\n⚠️ *风险因素:*")
        for c in cons:
            lines.append(f"  • {c}")
        lines.append("\n_⚠️ 规则引擎分析。接入 Claude API 后可获得更深度的分析。_")

    return "\n".join(lines)


# ═══════════════════════════════════════════
#  4. 包装函数: 数据 + AI分析 一体化
# ═══════════════════════════════════════════

def enrich_with_analysis(raw_result, query_text, user_id=None):
    """在原始查询结果后追加 Claude AI 利弊分析

    这是主入口：chat_query 和 bot 调用此函数

    Args:
        raw_result: str - 原始查询结果 (价格/新闻等)
        query_text: str - 用户原始查询
        user_id: str - 用户ID

    Returns:
        str - 原始结果 + AI分析
    """
    # 检测语言并更新偏好
    lang = detect_language(query_text)

    # 提取查询中的 ticker
    try:
        from chat_query import resolve_ticker, resolve_multiple_tickers
        ticker = resolve_ticker(query_text)
        tickers = resolve_multiple_tickers(query_text)
        if ticker and ticker not in ("KOSPI", "KOSDAQ"):
            tickers = list(set(tickers + [ticker]))
    except:
        tickers = []

    # 更新用户偏好
    if user_id:
        update_user_preferences(user_id, query_text, lang, tickers)

    # 生成 AI 分析
    analysis = analyze_with_claude(raw_result, query_text, user_id)

    # 拼接
    return f"{raw_result}\n{analysis}"


# ─── CLI 测试 ───

if __name__ == "__main__":
    print("=" * 55)
    print("🧠 Mapulse Claude AI Layer")
    print("=" * 55)

    api = _get_api_config()
    if api:
        print(f"✅ API: {api['type']}")
    else:
        print("⚠️  No API key configured. Using rule-based fallback.")
        print("   Set ANTHROPIC_API_KEY or OPENROUTER_API_KEY to enable Claude AI.")

    # 测试语言检测
    tests = [
        ("삼성 오늘 어때?", "ko"),
        ("三星今天怎么样？", "zh"),
        ("How is Samsung today?", "en"),
        ("サムスンの今日はどう？", "ja"),
    ]
    print("\n📝 Language Detection:")
    for text, expected in tests:
        detected = detect_language(text)
        status = "✅" if detected == expected else "❌"
        print(f"  {status} '{text}' → {detected} (expected {expected})")

    # 测试分析
    sample_data = """
🟢 삼성전자 (005930)
📊 종가: ₩82,900 (+2.7%)
📦 거래량: 15,234,567
🔴 SK하이닉스: ₩198,500 (-1.2%)
"""
    print("\n🧠 Analysis Test:")
    result = analyze_with_claude(sample_data, "삼성 오늘 어때?", "test_user")
    print(result)
