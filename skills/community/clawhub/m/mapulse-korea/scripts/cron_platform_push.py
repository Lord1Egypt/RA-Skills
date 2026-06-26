#!/usr/bin/env python3
"""
Mapulse — 플랫폼 고정 3회 푸시
매일 모든 사용자에게 3번 고정 푸시

시간 (KST):
  08:30 — 개장 전 브리핑 (오늘 뭘 봐야 하나?)
  12:20 — 오전장 정리 (오전에 뭐가 있었나, 오후 뭘 봐야 하나?)
  20:50 — 해외 야간 브리핑 (해외 변수가 내일 한국 시장에 어떤 영향?)

실행:
  python3 cron_platform_push.py morning    # 08:30 KST
  python3 cron_platform_push.py midday     # 12:20 KST
  python3 cron_platform_push.py evening    # 20:50 KST

crontab (서버 시간 = CST/UTC+8, KST = UTC+9):
  30 7 * * 1-5  → KST 08:30 (morning)
  20 11 * * 1-5 → KST 12:20 (midday)
  50 19 * * 1-5 → KST 20:50 (evening)

주의: 사용자 개인 푸시와 독립적으로 운영 (push_type='platform_xxx')
"""

import os
import sys
import json
import time
import logging
import sqlite3
import requests

sys.path.insert(0, os.path.dirname(__file__))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("platform_push")

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
DB_PATH = os.environ.get("MAPULSE_DB", os.path.join(os.path.dirname(__file__), "..", "data", "mapulse.db"))

# Public channel for briefing (set after channel is created)
CHANNEL_ID = os.environ.get("MAPULSE_CHANNEL_ID", "")

# LLM for generating analysis
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
LLM_MODEL = "anthropic/claude-sonnet-4"


# ─── DB Helpers ───

def get_all_users():
    """모든 사용자 (한 번이라도 사용한 유저)"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT DISTINCT user_id FROM users").fetchall()
    conn.close()
    return [r["user_id"] for r in rows]


def log_push(user_id, push_type, content):
    """푸시 기록"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO push_log (user_id, push_type, content) VALUES (?,?,?)",
            (user_id, push_type, content[:500])
        )
        conn.commit()
        conn.close()
    except:
        pass


def send_message(chat_id, text):
    """텔레그램 전송 (Markdown, fallback to plain text on parse error)"""
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        return False
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True,
            },
            timeout=10
        )
        result = resp.json()
        if not result.get("ok"):
            desc = result.get("description", "")
            # Markdown parse error → retry without parse_mode
            if "can't parse entities" in desc.lower() or "parse" in desc.lower():
                logger.warning(f"Markdown parse error for {chat_id}, retrying as plain text")
                plain = text.replace("*", "").replace("_", "").replace("`", "")
                resp2 = requests.post(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": plain,
                        "disable_web_page_preview": True,
                    },
                    timeout=10
                )
                result2 = resp2.json()
                if not result2.get("ok"):
                    logger.warning(f"Plain text also failed for {chat_id}: {result2.get('description','')}")
                return result2.get("ok", False)
            logger.warning(f"Send failed to {chat_id}: {desc}")
        return result.get("ok", False)
    except Exception as e:
        logger.error(f"Send error to {chat_id}: {e}")
        return False


# ─── Market Data ───

def get_market_data():
    """실시간 시장 데이터 수집 — 실제 함수명 사용"""
    data = {}

    # 1. 한국 시장 브리핑 데이터
    try:
        from fetch_briefing import find_trading_date, fetch_all, DEFAULT_WATCHLIST
        date_str = find_trading_date()
        watchlist = [t.strip() for t in DEFAULT_WATCHLIST.split(",")]
        raw = fetch_all(date_str, watchlist)
        data["briefing_raw"] = raw
        data["date"] = date_str
    except Exception as e:
        logger.warning(f"Briefing fetch error: {e}")
        data["briefing_raw"] = {}

    # 2. 환율
    try:
        from market_data import fetch_exchange_rates
        data["exchange_rates"] = fetch_exchange_rates()
    except Exception as e:
        logger.warning(f"Exchange rate error: {e}")

    # 3. VIX
    try:
        from market_data import fetch_vix
        data["vix"] = fetch_vix()
    except Exception as e:
        logger.warning(f"VIX error: {e}")

    # 4. Fear & Greed
    try:
        from market_data import fetch_fear_greed
        data["fear_greed"] = fetch_fear_greed()
    except Exception as e:
        logger.warning(f"Fear&Greed error: {e}")

    # 5. 미국 지수
    try:
        from market_data import fetch_us_indices
        data["us_indices"] = fetch_us_indices()
    except Exception as e:
        logger.warning(f"US indices error: {e}")

    # 6. 업종 등락
    try:
        from market_data import fetch_sector_ranking
        data["sectors"] = fetch_sector_ranking()
    except Exception as e:
        logger.warning(f"Sector error: {e}")

    # 7. BTC 실시간 (Binance API)
    try:
        import requests as _req
        resp = _req.get("https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT", timeout=5)
        if resp.status_code == 200:
            btc = resp.json()
            data["btc"] = {
                "price": float(btc["lastPrice"]),
                "change_pct": float(btc["priceChangePercent"]),
                "high_24h": float(btc["highPrice"]),
                "low_24h": float(btc["lowPrice"]),
            }
    except Exception as e:
        logger.warning(f"BTC error: {e}")

    # 8. 금/유가 (Binance 선물 or Yahoo)
    try:
        import requests as _req
        # Gold
        gold_resp = _req.get("https://api.binance.com/api/v3/ticker/price?symbol=XAUUSDT", timeout=5)
        if gold_resp.status_code == 200:
            data["gold_price"] = float(gold_resp.json()["price"])
        # ETH
        eth_resp = _req.get("https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT", timeout=5)
        if eth_resp.status_code == 200:
            eth = eth_resp.json()
            data["eth"] = {"price": float(eth["lastPrice"]), "change_pct": float(eth["priceChangePercent"])}
    except Exception as e:
        logger.warning(f"Gold/ETH error: {e}")

    return data


def format_market_context(data):
    """AI에 전달할 시장 컨텍스트 — 실제 데이터 구조 매핑"""
    lines = []

    # 한국 지수
    raw = data.get("briefing_raw", {})
    indices = raw.get("indices", [])
    if isinstance(indices, list):
        for idx in indices:
            if isinstance(idx, dict):
                lines.append(f"{idx.get('name', '?')}: {idx.get('close', '?')} ({idx.get('change_pct', '?')}%)")
            elif isinstance(idx, str):
                lines.append(idx)

    # 관심종목
    watchlist = raw.get("watchlist", [])
    if watchlist:
        lines.append("\n관심 종목:")
        for s in watchlist[:10]:
            if isinstance(s, dict):
                lines.append(f"  {s.get('name','?')}: ₩{s.get('close',0):,} ({s.get('change_pct',0):+.1f}%)")

    # 상승/하락 TOP
    for label, key in [("상승 TOP", "gainers"), ("하락 TOP", "losers")]:
        items = raw.get(key, [])
        if items:
            lines.append(f"\n{label}:")
            for s in items[:5]:
                if isinstance(s, dict):
                    lines.append(f"  {s.get('name','?')}: {s.get('change_pct',0):+.1f}%")

    # 환율
    fx = data.get("exchange_rates")
    if fx and isinstance(fx, dict):
        lines.append(f"\n환율:")
        for k, v in fx.items():
            lines.append(f"  {k}: {v}")

    # VIX
    vix = data.get("vix")
    if vix:
        if isinstance(vix, dict):
            lines.append(f"\nVIX: {vix.get('value', vix.get('close', '?'))}")
        else:
            lines.append(f"\nVIX: {vix}")

    # Fear & Greed
    fg = data.get("fear_greed")
    if fg:
        if isinstance(fg, dict):
            lines.append(f"Fear&Greed: {fg.get('value', '?')}/100 ({fg.get('label', '?')})")
        else:
            lines.append(f"Fear&Greed: {fg}")

    # 미국 지수
    us = data.get("us_indices")
    if us:
        lines.append(f"\n미국 지수:")
        if isinstance(us, dict):
            for k, v in us.items():
                if isinstance(v, dict):
                    lines.append(f"  {k}: {v.get('price', v.get('close', '?'))} ({v.get('change_pct', '?')}%)")
                else:
                    lines.append(f"  {k}: {v}")
        elif isinstance(us, list):
            for idx in us[:5]:
                if isinstance(idx, dict):
                    lines.append(f"  {idx.get('name','?')}: {idx.get('close','?')} ({idx.get('change_pct','?')}%)")

    # 업종
    sectors = data.get("sectors")
    if sectors and isinstance(sectors, list):
        lines.append(f"\n업종 등락 (상위):")
        for s in sectors[:5]:
            if isinstance(s, dict):
                lines.append(f"  {s.get('name','?')}: {s.get('change_pct','?')}%")

    # BTC (Binance 실시간)
    btc = data.get("btc")
    if btc:
        lines.append(f"\nBTC: ${btc['price']:,.0f} ({btc['change_pct']:+.2f}%)")
        lines.append(f"  24h High: ${btc['high_24h']:,.0f} / Low: ${btc['low_24h']:,.0f}")

    # ETH
    eth = data.get("eth")
    if eth:
        lines.append(f"ETH: ${eth['price']:,.0f} ({eth['change_pct']:+.2f}%)")

    # Gold
    gold = data.get("gold_price")
    if gold:
        lines.append(f"Gold: ${gold:,.0f}")

    return "\n".join(lines) if lines else "시장 데이터 수집 실패"


# ─── LLM Generation ───

def generate_with_llm(system_prompt, user_prompt, max_tokens=800):
    """OpenRouter LLM 호출"""
    if not OPENROUTER_API_KEY:
        logger.error("OPENROUTER_API_KEY not set")
        return None

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": 0.4,
            },
            timeout=30,
        )
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"LLM error: {e}")
        return None


# ─── 3 Push Types ───

SYSTEM_PROMPT = """당신은 한국 주식 시장 전문 애널리스트입니다.
Telegram 메시지 포맷으로 작성하세요.

필수 규칙:
- 반드시 첫 줄에 한 줄 요약 (🚨 또는 📌): "오늘 가장 중요한 한 가지"를 한 문장으로
- 마지막에 행동 지침 (📌 오늘 주목): 구체적 수치와 함께 투자자가 뭘 해야 하는지 1-2줄
- Markdown 사용 (*bold*) — 단, Telegram에서 깨지지 않도록 모든 *는 반드시 짝을 맞출 것
- 밑줄(_)은 사용하지 마세요 — 이탤릭 대신 *bold* 사용
- 간결하고 핵심만, 이모지 적절히
- 투자 자문이 아닌 참고용 분석임을 마지막에 명시
- 한국어로 작성"""


def generate_morning(market_data):
    """08:30 KST — 개장 전 브리핑"""
    context = format_market_context(market_data)
    
    prompt = f"""오늘의 한국 증시 개장 전 브리핑을 작성하세요.

시장 데이터:
{context}

다음 구조로 작성 (순서 엄수):
1. 🌅 *Mapulse 모닝 브리프*
2. 🚨 *한 줄 요약:* 오늘 가장 중요한 변수 한 가지를 한 문장으로 (예: "외국인 대규모 이탈, 관망 권장")
3. 핵심 포인트 3-4개 (어떤 섹터/종목/이슈를 봐야 하는지)
4. 어제 해외 시장 영향 요약 (미국, 유럽, 아시아)
5. 핵심 숫자 (KOSPI 전일 종가, 환율, VIX 등)
6. 📌 *오늘 주목:* 구체적 행동 지침 1-2줄 (예: "달러/원 1,501원 돌파. 외국인 추가 매도 가능성. 반도체 보유 중이라면 오전 동향 주시 권장.")

절대 "오늘 시장 요약"처럼 뻔한 말 쓰지 마세요. "오늘 뭘 봐야 하나"에 구체적으로 답하세요."""

    result = generate_with_llm(SYSTEM_PROMPT, prompt)
    if not result:
        result = (
            "🌅 *Mapulse 모닝 브리프*\n\n"
            "시장 데이터를 불러오는 중 오류가 발생했습니다.\n"
            "잠시 후 종목명을 입력하여 직접 조회해주세요."
        )
    return result


def generate_midday(market_data):
    """12:20 KST — 오전장 정리"""
    context = format_market_context(market_data)

    prompt = f"""한국 증시 오전장 정리를 작성하세요. 지금은 점심시간입니다.

시장 데이터:
{context}

다음 구조로 작성 (순서 엄수):
1. 📊 *Mapulse 장중 리포트*
2. 🚨 *한 줄 요약:* 오전장에서 가장 중요한 변화 한 가지를 한 문장으로
3. 오전장 핵심 변화 3-4개 (주요 종목/섹터 움직임)
4. 특이 수급 동향 (외국인, 기관)
5. 핵심 숫자 업데이트
6. 📌 *오후 주목:* 구체적 행동 지침 1-2줄

"오전에 뭐가 있었고, 오후에 뭘 해야 하나"에 구체적으로 답하세요."""

    result = generate_with_llm(SYSTEM_PROMPT, prompt)
    if not result:
        result = (
            "📊 *Mapulse 장중 리포트*\n\n"
            "시장 데이터를 불러오는 중 오류가 발생했습니다.\n"
            "종목명을 입력하여 직접 조회해주세요."
        )
    return result


def generate_evening(market_data):
    """20:50 KST — 해외 야간 브리핑"""
    context = format_market_context(market_data)

    prompt = f"""한국 시간 저녁, 해외 시장 브리핑을 작성하세요.

시장 데이터:
{context}

다음 구조로 작성 (순서 엄수):
1. 🌙 *Mapulse 나이트 브리프*
2. 🚨 *한 줄 요약:* 오늘 밤 가장 중요한 해외 변수 한 가지를 한 문장으로
3. 해외 주요 변수 3-4개 (미국, 유럽, 환율, 원자재, 비트코인)
4. 이 변수가 내일 한국 시장에 미칠 영향
5. 핵심 숫자 (미국 선물, 달러/원, 유가, 금, BTC)
6. 📌 *내일 주목:* 구체적 행동 지침 1-2줄

"오늘 밤 해외에서 뭐가 일어나고 있고, 내일 뭘 해야 하는지"에 구체적으로 답하세요."""

    result = generate_with_llm(SYSTEM_PROMPT, prompt)
    if not result:
        result = (
            "🌙 *Mapulse 나이트 브리프*\n\n"
            "해외 시장 데이터를 불러오는 중 오류가 발생했습니다.\n"
            "내일 아침 모닝 브리프에서 업데이트 드리겠습니다."
        )
    return result


# ─── Push Executor ───

def get_top_news_digest():
    """news_digest에서 오늘의 최고 점수 뉴스 가져오기"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """SELECT * FROM news_digest
               WHERE created_at >= datetime('now', '-12 hours')
               AND impact_direction != ''
               ORDER BY score DESC
               LIMIT 5""",
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows] if rows else []
    except Exception as e:
        logger.warning(f"news_digest query error: {e}")
        return []


def generate_afternoon(market_data):
    """14:00 KST — 오늘의 핵심 변수 + 질문 유도"""
    context = format_market_context(market_data)
    
    # news_digest에서 오늘의 핵심 뉴스 가져오기
    top_news = get_top_news_digest()
    news_context = ""
    if top_news:
        news_lines = []
        for n in top_news[:3]:
            news_lines.append(f"- [{n['source']}] {n['title']} (impact: {n['impact_direction']} {n['impact_text']})")
        news_context = "\n".join(news_lines)

    prompt = f"""오늘의 핵심 변수 1개를 골라서 짧은 알림을 작성하세요.

시장 데이터:
{context}

오늘의 주요 뉴스:
{news_context if news_context else "특이 뉴스 없음"}

규칙:
1. 가장 중요한 변수 딱 1개만 선택 (원유, 환율, 미국 금리, AI, 지정학 등)
2. 그 변수의 현재 수치 + 변동을 먼저 보여주기
3. 한국 시장에 미치는 영향을 2줄 이내로 설명
4. 마지막에 사용자가 질문하도록 유도

포맷 (반드시 이 형식):
📌 *오늘의 핵심 변수*

[이모지] [변수명] [수치] ([변동]) — [한줄 배경]

한국 영향: [구체적 영향 2줄 이내]

💬 관심 종목에 어떤 영향이 있는지 물어보세요!
예: "[구체적인 질문 예시]"

전체 분석 부분은 200자 이내로 매우 짧게. 이모지는 변수 종류에 맞게."""

    result = generate_with_llm(SYSTEM_PROMPT, prompt, max_tokens=400)
    if not result:
        result = (
            "📌 *오늘의 핵심 변수*\n\n"
            "시장 데이터를 불러오는 중 오류가 발생했습니다.\n"
            "종목명을 입력하여 직접 조회해주세요."
        )
    return result


PUSH_TYPES = {
    "morning": ("platform_morning", generate_morning),
    "midday": ("platform_midday", generate_midday),
    "evening": ("platform_evening", generate_evening),
    "afternoon": ("platform_afternoon", generate_afternoon),
}


def run_push(push_name):
    """플랫폼 푸시 실행"""
    if push_name not in PUSH_TYPES:
        logger.error(f"Unknown push type: {push_name}. Use: morning/midday/evening")
        return

    push_type, generator = PUSH_TYPES[push_name]
    logger.info(f"Starting platform push: {push_name} ({push_type})")

    # 1. 시장 데이터 수집
    logger.info("Fetching market data...")
    market_data = get_market_data()

    # 2. AI 메시지 생성
    logger.info("Generating message with LLM...")
    message = generator(market_data)

    # 3. 면책 추가
    if "참고용" not in message and "투자 자문" not in message:
        message += "\n\n※ 본 내용은 투자 자문이 아닌 참고용 분석입니다."

    logger.info(f"Message generated ({len(message)} chars)")

    # 4. 공개 채널에 게시
    if CHANNEL_ID:
        channel_msg = message
        # 채널용 CTA 추가
        if "Mapulse_bot" not in channel_msg:
            channel_msg += "\n\n💬 1:1 AI 심층 분석은 @Mapulse_bot 에서!"
        if send_message(CHANNEL_ID, channel_msg):
            logger.info(f"✅ Channel post sent to {CHANNEL_ID}")
        else:
            logger.warning(f"❌ Channel post failed for {CHANNEL_ID}")
    else:
        logger.info("No CHANNEL_ID configured, skipping channel post")

    # 5. 모든 사용자에게 전송
    users = get_all_users()
    logger.info(f"Sending to {len(users)} users...")

    sent = 0
    failed = 0
    for uid in users:
        if send_message(uid, message):
            log_push(uid, push_type, message)
            sent += 1
        else:
            failed += 1
        time.sleep(0.3)  # Rate limiting

    logger.info(f"Platform push [{push_name}] complete: {sent} sent, {failed} failed, {len(users)} total")
    return {"sent": sent, "failed": failed, "total": len(users)}


# ─── Main ───

if __name__ == "__main__":
    # All config via environment variables — set them before running
    if len(sys.argv) < 2:
        print("Usage: python3 cron_platform_push.py <morning|midday|afternoon|evening>")
        print()
        print("Crontab (server=CST/UTC+8, push=KST/UTC+9):")
        print("  30 7  * * 1-5  → KST 08:30 morning")
        print("  20 11 * * 1-5  → KST 12:20 midday")
        print("  0  13 * * 1-5  → KST 14:00 afternoon")
        print("  50 19 * * 1-5  → KST 20:50 evening")
        sys.exit(1)

    push_name = sys.argv[1].lower()
    run_push(push_name)
