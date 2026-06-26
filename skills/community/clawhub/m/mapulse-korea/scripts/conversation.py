#!/usr/bin/env python3
"""
Mapulse Conversation Memory
简单的对话上下文追踪 — 记住最近聊的股票和话题
"""

import time
import sqlite3
import os
import json

DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))

CONTEXT_TTL = 1800  # 30분钟内의 대화는 연속으로 간주


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_conversation_table():
    conn = _get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversation (
            user_id TEXT PRIMARY KEY,
            last_ticker TEXT DEFAULT '',
            last_tickers TEXT DEFAULT '[]',
            last_intent TEXT DEFAULT '',
            last_query TEXT DEFAULT '',
            last_response TEXT DEFAULT '',
            history TEXT DEFAULT '[]',
            updated_at REAL DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


init_conversation_table()


def get_context(user_id):
    """获取用户最近对话上下文"""
    conn = _get_conn()
    row = conn.execute("SELECT * FROM conversation WHERE user_id=?", (user_id,)).fetchone()
    conn.close()

    if not row:
        return None

    # 超时检查
    if time.time() - row["updated_at"] > CONTEXT_TTL:
        return None

    return {
        "last_ticker": row["last_ticker"],
        "last_tickers": json.loads(row["last_tickers"] or "[]"),
        "last_intent": row["last_intent"],
        "last_query": row["last_query"],
        "history": json.loads(row["history"] or "[]"),
    }


def update_context(user_id, ticker=None, tickers=None, intent=None, query=None, response=None):
    """更新对话上下文"""
    conn = _get_conn()

    # 获取现有context
    row = conn.execute("SELECT * FROM conversation WHERE user_id=?", (user_id,)).fetchone()

    if row:
        # 更新
        updates = []
        params = []

        if ticker:
            updates.append("last_ticker=?")
            params.append(ticker)
        if tickers:
            updates.append("last_tickers=?")
            params.append(json.dumps(tickers))
        if intent:
            updates.append("last_intent=?")
            params.append(intent)
        if query:
            updates.append("last_query=?")
            params.append(query)

        # 追加历史 (最多保留6轮)
        history = json.loads(row["history"] or "[]")
        if query:
            history.append({"role": "user", "content": query[:200]})
        if response:
            history.append({"role": "assistant", "content": response[:300]})
        history = history[-12:]  # 6轮

        updates.append("history=?")
        params.append(json.dumps(history, ensure_ascii=False))
        updates.append("updated_at=?")
        params.append(time.time())
        params.append(user_id)

        conn.execute(f"UPDATE conversation SET {','.join(updates)} WHERE user_id=?", params)
    else:
        # 新建
        history = []
        if query:
            history.append({"role": "user", "content": query[:200]})
        if response:
            history.append({"role": "assistant", "content": response[:300]})

        conn.execute(
            "INSERT INTO conversation (user_id, last_ticker, last_tickers, last_intent, last_query, history, updated_at) VALUES (?,?,?,?,?,?,?)",
            (user_id, ticker or "", json.dumps(tickers or []), intent or "", query or "",
             json.dumps(history, ensure_ascii=False), time.time())
        )

    conn.commit()
    conn.close()


def resolve_from_context(user_id, text, current_ticker=None):
    """
    如果当前消息没有明确股票，从上下文推断。
    
    优先级:
    1. 本轮否定信号 → 清除上下文ticker
    2. 本轮范围切换(整体市场) → 不继承个股
    3. 本轮明确对象 → 使用本轮
    4. 上下文continuation → 继承上轮
    
    返回: (ticker, enriched_text)
    """
    t = text.lower()
    
    # ── 1. 否定前一个对象检测 ──
    negation_patterns = [
        # Korean
        "말고", "아니라", "아니고", "대신", "빼고", "제외",
        "그거 말고", "그 종목 말고", "특정 종목 말고",
        "개별 종목 말고", "개별종목 말고",
        # Chinese
        "不要", "不是", "别看", "换一个", "不用",
        "个股不要", "不看个股",
        # English
        "not that", "instead", "not about", "rather than",
        "don't want", "skip", "except",
    ]
    
    has_negation = any(p in t for p in negation_patterns)
    
    # ── 2. 范围切换到整体市场 ──
    general_scope_patterns = [
        # Korean
        "한국", "시장", "전반", "전체", "코스피", "코스닥",
        "투자자", "시장 분위기", "전체 시장", "한국 시장",
        "전체적", "종합", "전반적", "시장 전체",
        # Chinese  
        "韩国", "整体", "全体", "市场", "大盘", "全市场",
        "投资者", "整个市场",
        # English
        "korea", "market", "overall", "general", "whole market",
        "kospi", "kosdaq", "investor",
    ]
    
    is_general_scope = any(p in t for p in general_scope_patterns)
    
    # 否定 + 整体范围 → 一定不继承个股
    if has_negation or is_general_scope:
        if current_ticker:
            # 本轮有明确ticker但用户说的是整体 → 忽略ticker
            if is_general_scope and not has_negation:
                # 可能ticker是从文本中误提取的(如"카카오 말고 한국 전체")
                # 检查ticker是否是被否定的对象
                pass  # 让调用方决定
            return current_ticker, text
        return None, text
    
    if current_ticker:
        return current_ticker, text

    ctx = get_context(user_id)
    if not ctx or not ctx["last_ticker"]:
        return None, text

    last = ctx["last_ticker"]

    # ── 3. 承接性话语检测 (仅在无否定/无范围切换时) ──
    continuation_words = [
        # 가격/시세
        "价格", "趋势", "怎么样", "买", "卖", "가격", "추세", "시세",
        # 분석/판단
        "분석", "어때", "사", "팔", "분석해", "판단", "의견", "생각",
        "analysis", "opinion", "think", "view",
        # 매매
        "price", "trend", "buy", "sell",
        # 뉴스/리서치
        "news", "뉴스", "수급", "리서치", "공시", "실적",
        # 전망/목표
        "목표가", "전망", "outlook", "target", "forecast",
        # 왜/원인
        "为什么", "왜", "why", "원인", "이유", "reason", "原因",
        # 방향
        "涨", "跌", "올", "빠", "오를", "떨어", "급등", "급락",
        # 代名사 (대명사)
        "它", "이거", "那个", "그거", "this", "that", "이 종목", "그 종목",
        # 추가 분석 요청
        "더", "자세히", "详细", "more", "detail", "계속", "이어서",
        "리스크", "위험", "risk", "风险", "변수", "variable",
        # 비교
        "비교", "比较", "compare", "vs",
    ]

    # 注意: 移除了 "상황", "현재", "현황", "현상", "현상", "how", "current", "status"
    # 等容易误触发的通用词。这些词太泛，容易把"한국 현재 상황"错误继承为上轮个股。

    if any(w in t for w in continuation_words):
        return last, text

    return None, text
