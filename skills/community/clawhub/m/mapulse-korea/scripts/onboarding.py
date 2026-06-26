#!/usr/bin/env python3
"""
Mapulse Onboarding v2 — 新用户引导 + 自选股管理

流程:
  /start → 欢迎(产品介绍) → 引导提问(1/2/3/4) → 追问一次 → 个性化结果 → 完成

状态机:
  new → welcome_sent → followup_sent → complete

规则:
  - 最多追问一次
  - 用户直接问具体问题 → 跳过 onboarding，直接回答
  - 完成后不再重复触发
"""

import sqlite3
import os
import json
import time
import re
import logging

logger = logging.getLogger("onboarding")

DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))

# ─── 종목 별명 (다국어) ───

STOCK_ALIASES = {
    # 韩文
    "삼성": "005930", "삼전": "005930", "삼성전자": "005930",
    "하이닉스": "000660", "sk하이닉스": "000660",
    "네이버": "035420", "카카오": "035720",
    "현대차": "005380", "현대자동차": "005380",
    "기아": "000270", "셀트리온": "068270",
    "lg에너지": "373220", "lg화학": "051910",
    "삼성sdi": "006400", "sk이노": "096770",
    "한전": "015760", "한국전력": "015760",
    "엔씨": "036570", "하이브": "352820",
    "에코프로": "086520", "알테오젠": "196170",
    "포스코": "003670", "두산에너빌리티": "034020",
    "크래프톤": "259960", "현대모비스": "012330",
    "kb금융": "105560", "신한지주": "055550",
    # 中文
    "三星": "005930", "三星电子": "005930",
    "海力士": "000660", "sk海力士": "000660",
    "现代": "005380", "现代汽车": "005380",
    "起亚": "000270", "lg电子": "066570",
    "lg能源": "373220", "lg化学": "051910",
    "韩国电力": "015760",
    # English
    "samsung": "005930", "hynix": "000660", "sk hynix": "000660",
    "naver": "035420", "kakao": "035720",
    "hyundai": "005380", "kia": "000270",
    "celltrion": "068270", "hybe": "352820",
    "posco": "003670", "krafton": "259960",
}

STOCK_NAMES = {
    "005930": "삼성전자", "000660": "SK하이닉스", "035420": "NAVER",
    "035720": "카카오", "005380": "현대자동차", "000270": "기아",
    "068270": "셀트리온", "373220": "LG에너지솔루션", "051910": "LG화학",
    "006400": "삼성SDI", "096770": "SK이노베이션", "015760": "한국전력",
    "036570": "엔씨소프트", "352820": "하이브", "086520": "에코프로",
    "196170": "알테오젠", "003670": "포스코인터내셔널", "066570": "LG전자",
    "012330": "현대모비스", "105560": "KB금융", "055550": "신한지주",
    "034020": "두산에너빌리티", "259960": "크래프톤",
}

# ─── 상태: new → welcome_sent → followup_sent → complete ───

STATES = ("new", "welcome_sent", "followup_sent", "complete")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_onboarding_table():
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS onboarding (
            user_id TEXT PRIMARY KEY,
            state TEXT DEFAULT 'new',
            language TEXT DEFAULT 'auto',
            interest_type TEXT DEFAULT '',
            push_enabled INTEGER DEFAULT 1,
            push_time TEXT DEFAULT '08:00',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );
    """)
    # interest_type 컬럼 추가 (기존 테이블 호환)
    try:
        conn.execute("ALTER TABLE onboarding ADD COLUMN interest_type TEXT DEFAULT ''")
    except:
        pass
    conn.commit()
    conn.close()

init_onboarding_table()


# ─── 상태 관리 ───

def get_onboarding_state(user_id):
    conn = _get_conn()
    row = conn.execute("SELECT * FROM onboarding WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def set_onboarding_state(user_id, state, **kwargs):
    conn = _get_conn()
    existing = conn.execute("SELECT user_id FROM onboarding WHERE user_id=?", (user_id,)).fetchone()
    if existing:
        updates = ["state=?", "updated_at=datetime('now')"]
        params = [state]
        for k, v in kwargs.items():
            updates.append(f"{k}=?")
            params.append(v)
        params.append(user_id)
        conn.execute(f"UPDATE onboarding SET {','.join(updates)} WHERE user_id=?", params)
    else:
        cols = ["user_id", "state"]
        vals = [user_id, state]
        for k, v in kwargs.items():
            cols.append(k)
            vals.append(v)
        placeholders = ",".join(["?"] * len(vals))
        conn.execute(f"INSERT INTO onboarding ({','.join(cols)}) VALUES ({placeholders})", vals)
    conn.commit()
    conn.close()


def is_onboarding_complete(user_id):
    state = get_onboarding_state(user_id)
    return state is not None and state["state"] == "complete"


# ─── 자선주 관리 ───

def get_watchlist(user_id):
    conn = _get_conn()
    rows = conn.execute("SELECT ticker FROM watchlist WHERE user_id=?", (user_id,)).fetchall()
    conn.close()
    return [r["ticker"] for r in rows]


def add_to_watchlist(user_id, ticker):
    conn = _get_conn()
    conn.execute("INSERT OR IGNORE INTO watchlist (user_id, ticker) VALUES (?,?)", (user_id, ticker))
    conn.commit()
    conn.close()


def remove_from_watchlist(user_id, ticker):
    conn = _get_conn()
    conn.execute("DELETE FROM watchlist WHERE user_id=? AND ticker=?", (user_id, ticker))
    conn.commit()
    conn.close()


def parse_stock_input(text):
    """사용자 입력에서 종목 코드 추출 (여러개 지원)"""
    tickers = []
    seen = set()
    parts = re.split(r'[,，/\s\n]+', text.lower().strip())

    for part in parts:
        part = part.strip()
        if not part:
            continue
        if re.match(r'^\d{6}$', part):
            if part not in seen:
                tickers.append(part)
                seen.add(part)
            continue
        if part in STOCK_ALIASES:
            t = STOCK_ALIASES[part]
            if t not in seen:
                tickers.append(t)
                seen.add(t)
            continue
        for alias, t in STOCK_ALIASES.items():
            if alias in part or part in alias:
                if t not in seen:
                    tickers.append(t)
                    seen.add(t)
                break
    return tickers


def format_watchlist(user_id, lang="ko"):
    tickers = get_watchlist(user_id)
    if not tickers:
        return "📋 관심 종목이 없습니다.\n\n'종목추가 삼성' 또는 '관심 삼성 하이닉스'로 추가하세요."
    lines = ["📋 *관심 종목*", ""]
    for t in tickers:
        name = STOCK_NAMES.get(t, t)
        lines.append(f"  • {name} ({t})")
    lines.append(f"\n총 {len(tickers)}종목")
    lines.append("\n'종목추가 카카오' / '종목삭제 삼성'으로 관리")
    return "\n".join(lines)


# ─── Onboarding v2: 메시지 ───

def _ensure_user_profile(user_id, focus_type="", focus_stocks=""):
    """user_profile 레코드 생성/업데이트"""
    try:
        conn = _get_conn()
        # 테이블 존재 확인
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                user_id TEXT PRIMARY KEY,
                focus_type TEXT DEFAULT '',
                focus_stocks TEXT DEFAULT '',
                push_preference TEXT DEFAULT 'standard',
                prefer_panorama INTEGER DEFAULT 1,
                profile_complete INTEGER DEFAULT 0,
                profile_asked_at TEXT DEFAULT '',
                created_at TEXT DEFAULT (datetime('now')),
                updated_at TEXT DEFAULT (datetime('now'))
            )
        """)
        conn.execute("INSERT OR IGNORE INTO user_profile (user_id) VALUES (?)", (user_id,))
        if focus_type:
            conn.execute(
                "UPDATE user_profile SET focus_type=?, updated_at=datetime('now') WHERE user_id=?",
                (focus_type, user_id)
            )
        if focus_stocks:
            conn.execute(
                "UPDATE user_profile SET focus_stocks=?, updated_at=datetime('now') WHERE user_id=?",
                (focus_stocks, user_id)
            )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"user_profile update error: {e}")


def _sync_watchlist_to_profile(user_id):
    """watchlist → user_profile.focus_stocks 동기화"""
    try:
        conn = _get_conn()
        rows = conn.execute("SELECT ticker FROM watchlist WHERE user_id=?", (user_id,)).fetchall()
        tickers = ",".join([r["ticker"] for r in rows]) if rows else ""
        conn.execute("INSERT OR IGNORE INTO user_profile (user_id) VALUES (?)", (user_id,))
        conn.execute(
            "UPDATE user_profile SET focus_stocks=?, updated_at=datetime('now') WHERE user_id=?",
            (tickers, user_id)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"watchlist sync error: {e}")


def get_welcome_messages(user_id, first_name="", lang="ko"):
    """첫 방문 시 환영 메시지 2개 반환.
    
    Returns:
        list[str]: [산품소개, 포커스 질문]
    """
    set_onboarding_state(user_id, "welcome_sent", language=lang)
    _ensure_user_profile(user_id)
    name = first_name or "User"

    # ── 메시지 1: 산품소개 ──
    intro = (
        f"📈 *Mapulse — 한국 주식 AI 나침반*\n\n"
        f"{name}님, 안녕하세요!\n\n"
        f"시장은 매일 움직입니다.\n"
        f"중요한 건 *\"지금 어떤 포지션을 가져야 하는가\"*입니다.\n\n"
        f"Mapulse는 단순한 정보가 아니라,\n"
        f"📊 시장 신호를 해석하고\n"
        f"🧠 리스크와 기회를 정리해드립니다.\n\n"
        f"━━━━━━━━━━\n"
        f"이렇게 물어보세요:\n\n"
        f"• `삼성전자` → 시세 + Trend + Risk\n"
        f"• `삼성 왜 떨어졌어?` → 원인 + 영향 분석\n"
        f"• `시장` → KOSPI/KOSDAQ + 환율 + 리스크\n"
        f"• `아침 브리핑` → 매일 오전 AI 시황\n\n"
        f"━━━━━━━━━━\n"
        f"🌐 한국어 / English / 中文 지원\n"
        f"_※ 본 서비스는 투자 자문이 아닌 참고용 분석입니다._"
    )

    # ── 메시지 2: 포커스 질문 (사용자 관심사 수집) ──
    guide = (
        f"{name}님, 가장 관심 있는 분야를 알려주세요!\n\n"
        f"1️⃣ 개별 종목 (삼성전자, SK하이닉스 등)\n"
        f"2️⃣ 시장 전체 (KOSPI/KOSDAQ 시황)\n"
        f"3️⃣ 해외 변수 (미국, 환율, 원자재)\n"
        f"4️⃣ 매일 시황만 (AI 브리핑만 받기)\n\n"
        f"번호, 종목명, 또는 궁금한 내용을 바로 보내주셔도 됩니다."
    )

    return [intro, guide]


# 호환용: 기존 코드에서 get_welcome_message(단수) 호출 시
def get_welcome_message(user_id, first_name="", lang="ko"):
    msgs = get_welcome_messages(user_id, first_name, lang)
    return msgs[0] + "\n\n" + msgs[1]


# ─── 사용자 응답 처리 ───

def is_onboarding_input(user_id, text):
    """이 메시지가 onboarding 응답인지 확인.
    
    Returns:
        bool: True if we should handle this in onboarding flow
    """
    state = get_onboarding_state(user_id)
    if not state:
        return False
    if state["state"] in ("welcome_sent", "followup_sent"):
        return True
    return False


def _is_direct_question(text):
    """사용자가 구체적인 질문을 했는지 판별.
    (이 경우 onboarding을 건너뛰고 바로 답변해야 함)
    """
    question_patterns = [
        r'왜\s*(떨어|빠|올|내려|급락|급등)',
        r'어떻게|어때|전망|리스크',
        r'시장|코스피|코스닥|환율|비트코인',
        r'뉴스|공시|공매도|금투세|밸류업',
        r'why.*(drop|fall|rise|up|down)',
        r'(market|kospi|kosdaq|bitcoin)',
        r'为什么|怎么样|行情|大盘',
    ]
    tl = text.lower()
    for pat in question_patterns:
        if re.search(pat, tl):
            return True
    return False


def handle_onboarding_input(user_id, text, lang="ko"):
    """핵심: 사용자 onboarding 응답 처리.
    
    Returns:
        dict: {
            "action": "reply" | "skip_to_normal" | "complete",
            "messages": [str, ...],      # 보낼 메시지들
            "tickers_found": [str, ...],  # 발견된 종목 코드
        }
    """
    state_data = get_onboarding_state(user_id)
    if not state_data:
        return {"action": "skip_to_normal", "messages": [], "tickers_found": []}

    current_state = state_data["state"]
    text_stripped = text.strip()
    tl = text_stripped.lower()

    # ── 사용자가 구체적 질문을 한 경우 → 바로 정상 흐름 ──
    if _is_direct_question(text_stripped):
        # 질문에 종목이 포함되어 있으면 watchlist에 추가
        tickers = parse_stock_input(text_stripped)
        if tickers:
            for t in tickers:
                add_to_watchlist(user_id, t)
        set_onboarding_state(user_id, "complete", interest_type="direct_question")
        return {"action": "skip_to_normal", "messages": [], "tickers_found": tickers}

    # ── welcome_sent: 첫 응답 처리 ──
    if current_state == "welcome_sent":
        return _handle_first_response(user_id, text_stripped, tl, lang)

    # ── followup_sent: 추가 응답 처리 ──
    elif current_state == "followup_sent":
        return _handle_followup_response(user_id, text_stripped, tl, lang)

    return {"action": "skip_to_normal", "messages": [], "tickers_found": []}


def _handle_first_response(user_id, text, tl, lang):
    """welcome_sent → 사용자 첫 응답"""

    # Map: 1→stocks, 2→market, 3→overseas, 4→briefing
    FOCUS_MAP = {"1": "stocks", "2": "market", "3": "overseas", "4": "briefing"}

    # ── 1) 개별 종목 (숫자 "1" 또는 직접 종목 입력) ──
    tickers = parse_stock_input(text)
    if tl in ("1", "1️⃣") or (tickers and tl not in ("2", "3", "4", "2️⃣", "3️⃣", "4️⃣")):
        if tickers:
            # 바로 종목 입력 → watchlist 추가 → 완료
            for t in tickers:
                add_to_watchlist(user_id, t)
            set_onboarding_state(user_id, "complete", interest_type="stocks")
            _ensure_user_profile(user_id, focus_type="stocks")
            _sync_watchlist_to_profile(user_id)
            return {
                "action": "complete",
                "messages": [_format_complete_stocks(tickers, lang)],
                "tickers_found": tickers,
            }
        else:
            # "1"만 입력 → 추가 질문
            set_onboarding_state(user_id, "followup_sent", interest_type="stocks")
            _ensure_user_profile(user_id, focus_type="stocks")
            return {
                "action": "reply",
                "messages": [
                    "좋아요! 가장 자주 보시는 종목 1~3개를 알려주세요.\n\n"
                    "예시: `삼성전자, SK하이닉스`\n"
                    "또는 코드: `005930, 000660`"
                ],
                "tickers_found": [],
            }

    # ── 2) 시장 전체 ──
    if tl in ("2", "2️⃣") or tl in ("시장", "오늘 시장", "market", "today"):
        set_onboarding_state(user_id, "complete", interest_type="market")
        _ensure_user_profile(user_id, focus_type="market")
        return {
            "action": "complete",
            "messages": [_format_complete_market(lang)],
            "tickers_found": [],
        }

    # ── 3) 해외 변수 ──
    if tl in ("3", "3️⃣") or tl in ("해외", "overseas", "환율", "원자재"):
        set_onboarding_state(user_id, "complete", interest_type="overseas")
        _ensure_user_profile(user_id, focus_type="overseas")
        return {
            "action": "complete",
            "messages": [_format_complete_overseas(lang)],
            "tickers_found": [],
        }

    # ── 4) 매일 시황만 ──
    if tl in ("4", "4️⃣") or tl in ("브리핑", "briefing", "아침", "시황"):
        set_onboarding_state(user_id, "complete", interest_type="briefing")
        _ensure_user_profile(user_id, focus_type="briefing")
        return {
            "action": "complete",
            "messages": [_format_complete_briefing(lang)],
            "tickers_found": [],
        }

    # ── legacy: "왜" 질문 ──
    if tl in ("왜", "why"):
        set_onboarding_state(user_id, "followup_sent", interest_type="why_move")
        return {
            "action": "reply",
            "messages": [
                "어떤 종목의 움직임이 궁금하신가요?\n\n"
                "예시: `삼성전자 왜 떨어졌어?`\n"
                "또는 종목명만 입력하셔도 됩니다."
            ],
            "tickers_found": [],
        }

    # ── 兜底: 인식 불가 ──
    return {
        "action": "reply",
        "messages": [
            "원하시는 방향을 아래 중 하나로 보내주세요.\n\n"
            "1️⃣ 개별 종목 (삼성전자, SK하이닉스 등)\n"
            "2️⃣ 시장 전체 (KOSPI/KOSDAQ 시황)\n"
            "3️⃣ 해외 변수 (미국, 환율, 원자재)\n"
            "4️⃣ 매일 시황만 (AI 브리핑만 받기)\n\n"
            "종목명이나 궁금한 내용을 바로 보내주셔도 됩니다."
        ],
        "tickers_found": [],
    }


def _handle_followup_response(user_id, text, tl, lang):
    """followup_sent → 추가 응답 (최대 1회 추가 질문 후 여기)"""

    interest = (get_onboarding_state(user_id) or {}).get("interest_type", "")

    # 종목 파싱 시도
    tickers = parse_stock_input(text)

    if tickers:
        for t in tickers:
            add_to_watchlist(user_id, t)
        set_onboarding_state(user_id, "complete")
        _sync_watchlist_to_profile(user_id)
        return {
            "action": "complete",
            "messages": [_format_complete_stocks(tickers, lang)],
            "tickers_found": tickers,
        }

    # 종목 없지만 텍스트 입력 (예: "반도체", "전체 시장")
    if text.strip():
        set_onboarding_state(user_id, "complete")

        if interest == "briefing":
            return {
                "action": "complete",
                "messages": [
                    f"좋아요. *\"{text}\"* 관련 브리핑을 설정했습니다.\n\n"
                    f"매일 오전 8시(KST)에 관련 시황을 보내드립니다.\n\n"
                    f"지금 바로 물어볼 수도 있어요:\n"
                    f"• `오늘 시장 어때?`\n"
                    f"• `삼성전자 분석해줘`\n"
                    f"• `관심종목` — 자선주 확인"
                ],
                "tickers_found": [],
            }
        elif interest == "why_move":
            # 사용자가 질문으로 입력 → 정상 흐름으로 넘기기
            return {"action": "skip_to_normal", "messages": [], "tickers_found": []}
        else:
            return {
                "action": "complete",
                "messages": [
                    f"알겠습니다. 앞으로 관련 내용을 중심으로 도와드릴게요.\n\n"
                    f"지금 바로 사용해보세요:\n"
                    f"• 종목명 입력 → 상세 분석\n"
                    f"• `시장` → 전체 시황\n"
                    f"• `관심종목` → 자선주 확인"
                ],
                "tickers_found": [],
            }

    # 빈 입력 → 완료 처리
    set_onboarding_state(user_id, "complete")
    return {
        "action": "complete",
        "messages": ["준비 완료! 종목명이나 궁금한 내용을 바로 보내주세요. 🚀"],
        "tickers_found": [],
    }


# ─── 완료 메시지 포맷 ───

def _format_complete_stocks(tickers, lang="ko"):
    """종목 추가 완료 메시지"""
    names = [f"{STOCK_NAMES.get(t, t)} ({t})" for t in tickers]
    names_str = "\n  • ".join(names)

    return (
        f"✅ *관심 종목 {len(tickers)}개 설정 완료!*\n"
        f"  • {names_str}\n\n"
        f"📊 매일 오전 8시(KST) 이 종목들의 AI 시황을 보내드립니다.\n\n"
        f"*지금 바로 물어보세요:*\n"
        f"• `{STOCK_NAMES.get(tickers[0], tickers[0])} 왜 떨어졌어?`\n"
        f"• `{STOCK_NAMES.get(tickers[0], tickers[0])} 리스크`\n"
        f"• `시장` — 전체 시황\n"
        f"• `관심종목` — 자선주 확인"
    )


def _format_complete_market(lang="ko"):
    """시장 관심 완료 메시지"""
    return (
        "좋아요. 시장 전체 현황을 중심으로 도와드릴게요.\n\n"
        "지금 바로 확인해보세요:\n"
        "• `시장` — KOSPI/KOSDAQ + 환율 + 리스크\n"
        "• `업종` — 업종별 등락 현황\n"
        "• `인기` — 실시간 인기 종목\n"
        "• `뉴스` — 오늘의 주요 뉴스\n\n"
        "관심 종목이 생기면 언제든 `종목추가 삼성`으로 추가하세요."
    )


def _format_complete_overseas(lang="ko"):
    """해외 변수 관심 완료 메시지"""
    return (
        "좋아요. 해외 변수를 중심으로 분석해 드릴게요.\n\n"
        "지금 바로 확인해보세요:\n"
        "• `시장` — 미국/유럽/아시아 + 환율 + VIX\n"
        "• `환율` — USD/KRW 실시간\n"
        "• `비트코인` — BTC 가격 + 크립토 동향\n\n"
        "매일 오후 2시에 *오늘의 핵심 해외 변수*도 보내드립니다.\n"
        "관심 종목이 생기면 `종목추가 삼성`으로 추가하세요."
    )


def _format_complete_briefing(lang="ko"):
    """매일 시황만 완료 메시지"""
    return (
        "✅ *매일 AI 시황 브리핑 설정 완료!*\n\n"
        "📅 매일 받으시게 됩니다:\n"
        "• 🌅 08:30 — 모닝 브리프 (개장 전)\n"
        "• 📊 12:20 — 장중 리포트 (오전장 정리)\n"
        "• 📌 14:00 — 핵심 변수 알림\n"
        "• 🌙 20:50 — 나이트 브리프 (해외 동향)\n\n"
        "궁금한 종목이 생기면 언제든 종목명을 보내주세요!"
    )


# ─── handle_stock_input: 호환용 ───

def handle_stock_input(user_id, text, lang="ko"):
    """기존 코드 호환: 종목 입력 처리"""
    result = handle_onboarding_input(user_id, text, lang)
    if result["messages"]:
        return result["messages"][0]
    return "종목명이나 궁금한 내용을 바로 보내주세요."
