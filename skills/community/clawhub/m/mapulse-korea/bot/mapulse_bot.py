#!/usr/bin/env python3
"""
Mapulse Telegram Bot 🇰🇷
韩国股市AI分析 — Telegram Bot绑定Mapulse Skill

环境变量:
  TELEGRAM_BOT_TOKEN=your_bot_token  (从 @BotFather 获取)
  DART_API_KEY=your_dart_key         (可选)

启动:
  python3 mapulse_bot.py
"""

import os
import sys
import json
import logging
import asyncio
import re

# 路径
BOT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(BOT_DIR)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
sys.path.insert(0, SCRIPTS_DIR)

# 安装依赖
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import (
        Application, CommandHandler, MessageHandler,
        CallbackQueryHandler, filters
    )
except ImportError:
    raise ImportError(
        "python-telegram-bot not installed. Run: pip install python-telegram-bot"
    )

from db import get_or_create_user
from chat_query import process_query, process_query_fast, process_query_deep, classify_intent, Intent
from fetch_briefing import find_trading_date, fetch_all, format_briefing, DEFAULT_WATCHLIST
from crash_alert import check_once, add_alert

# Claude AI 分析层
try:
    from claude_ai import enrich_with_analysis, detect_language, update_user_preferences
    _CLAUDE_ENABLED = True
except ImportError:
    _CLAUDE_ENABLED = False
    def enrich_with_analysis(result, query, uid=None):
        return result

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger("mapulse")

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")

TG_MAX_LENGTH = 4096

async def send_long_message(message_obj, text, parse_mode="Markdown"):
    """텔레그램 4096자 제한 대응: 긴 메시지 자동 분할"""
    if len(text) <= TG_MAX_LENGTH:
        try:
            return await message_obj.reply_text(text, parse_mode=parse_mode)
        except Exception:
            return await message_obj.reply_text(text)

    # 분할 전송
    chunks = []
    while text:
        if len(text) <= TG_MAX_LENGTH:
            chunks.append(text)
            break
        # 줄바꿈 기준으로 분할
        cut = text[:TG_MAX_LENGTH].rfind('\n')
        if cut < TG_MAX_LENGTH // 2:
            cut = TG_MAX_LENGTH
        chunks.append(text[:cut])
        text = text[cut:].lstrip('\n')

    last_msg = None
    for chunk in chunks:
        try:
            last_msg = await message_obj.reply_text(chunk, parse_mode=parse_mode)
        except Exception:
            last_msg = await message_obj.reply_text(chunk)
    return last_msg


# ─── Rate Limiter ───

import time as _time
from collections import defaultdict

# 설정: 환경변수 또는 기본값
RATE_LIMIT_PER_MIN = int(os.environ.get("RATE_LIMIT_PER_MIN", "10"))   # 분당 최대 요청
RATE_LIMIT_COOLDOWN = float(os.environ.get("RATE_LIMIT_COOLDOWN", "3"))  # 최소 간격 (초)
MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", "500"))     # 입력 글자 제한

# 허용 群组 (쉼표 구분, chat_id). 비어있으면 DM만 허용
# 예: ALLOWED_GROUPS=-100123456,-100789012
ALLOWED_GROUPS_STR = os.environ.get("ALLOWED_GROUPS", "")
ALLOWED_GROUPS = set()
if ALLOWED_GROUPS_STR:
    for g in ALLOWED_GROUPS_STR.split(","):
        g = g.strip()
        if g:
            try:
                ALLOWED_GROUPS.add(int(g))
            except ValueError:
                pass

_user_requests = defaultdict(list)  # user_id → [timestamp, ...]
_user_last = {}                     # user_id → last_request_time


def _rate_check(user_id):
    """Check rate limit. Returns (allowed, message).
    
    Rules:
      1. Min interval: RATE_LIMIT_COOLDOWN seconds between requests
      2. Max frequency: RATE_LIMIT_PER_MIN requests per minute
    """
    now = _time.time()
    uid = str(user_id)

    # Cooldown check
    last = _user_last.get(uid, 0)
    if now - last < RATE_LIMIT_COOLDOWN:
        wait = round(RATE_LIMIT_COOLDOWN - (now - last), 1)
        return False, f"⏳ {wait}초 후 다시 시도해 주세요."

    # Per-minute check
    window = now - 60
    _user_requests[uid] = [t for t in _user_requests[uid] if t > window]
    if len(_user_requests[uid]) >= RATE_LIMIT_PER_MIN:
        return False, f"⚠️ 1분에 {RATE_LIMIT_PER_MIN}회까지 사용 가능합니다. 잠시 후 다시 시도해 주세요."

    # Pass
    _user_requests[uid].append(now)
    _user_last[uid] = now
    return True, ""


def _group_allowed(chat_id):
    """Check if group chat is in whitelist.
    
    - DM (private): always allowed
    - Group: allowed only if in ALLOWED_GROUPS (or if whitelist is empty → all allowed)
    """
    if not ALLOWED_GROUPS:
        return True  # 화이트리스트 미설정 → 전부 허용
    return int(chat_id) in ALLOWED_GROUPS


# ─── User sync helper ───

async def _sync_user_info_async(update, context):
    """每次交互时同步 Telegram 用户信息 + 头像到 DB"""
    try:
        user = update.effective_user
        if not user:
            return
        from db import get_or_create_user, get_conn
        get_or_create_user(str(user.id), username=user.username or "", first_name=user.first_name or "")

        # 获取头像 (仅在没存过时抓取，避免每次都调 API)
        conn = get_conn()
        row = conn.execute("SELECT avatar_file_id FROM users WHERE user_id=?", (str(user.id),)).fetchone()
        existing_avatar = dict(row).get("avatar_file_id", "") if row else ""
        conn.close()

        if not existing_avatar:
            try:
                photos = await context.bot.get_user_profile_photos(user.id, limit=1)
                if photos.total_count > 0:
                    file_id = photos.photos[0][-1].file_id  # 最大尺寸
                    conn = get_conn()
                    conn.execute("UPDATE users SET avatar_file_id=? WHERE user_id=?", (file_id, str(user.id)))
                    conn.commit()
                    conn.close()
            except Exception:
                pass
    except Exception:
        pass


def _sync_user_info(update):
    """同步版 — 仅更新 username/first_name (不含头像)"""
    try:
        user = update.effective_user
        if user:
            from db import get_or_create_user
            get_or_create_user(str(user.id), username=user.username or "", first_name=user.first_name or "")
    except Exception:
        pass


# ─── Command Handlers ───

async def cmd_start(update: Update, context):
    user = update.effective_user
    user_id = str(user.id)

    # 同步用户 TG 信息 + 头像
    await _sync_user_info_async(update, context)

    # Onboarding v2: 환영(2메시지) + 인도질문
    try:
        from onboarding import get_welcome_messages
        lang = "ko"
        if user.language_code and user.language_code.startswith("zh"):
            lang = "zh"
        elif user.language_code and user.language_code.startswith("en"):
            lang = "en"

        messages = get_welcome_messages(user_id, user.first_name or "", lang)
        # 메시지 1: 산품소개
        try:
            await update.message.reply_text(messages[0], parse_mode="Markdown")
        except Exception:
            await update.message.reply_text(messages[0])
        # 1.5초 간격 → Telegram에서 별도 메시지로 표시
        await asyncio.sleep(1.5)
        # 메시지 2: 인도질문
        if len(messages) > 1:
            try:
                await update.message.reply_text(messages[1], parse_mode="Markdown")
            except Exception:
                await update.message.reply_text(messages[1])
    except Exception as e:
        logger.error(f"Onboarding error: {e}", exc_info=True)
        welcome = (
            f"🇰🇷 *Mapulse에 오신 것을 환영합니다!*\n\n"
            f"안녕하세요, {user.first_name}님!\n"
            f"종목명을 입력하면 AI 분석을 제공합니다."
        )
        await update.message.reply_text(welcome, parse_mode="Markdown")


async def cmd_help(update: Update, context):
    help_text = (
        "*📈 Mapulse*\n\n"
        "*자연어로 물어보세요:*\n"
        "삼성 / 하이닉스 — 실시간 시세 + AI 분석\n"
        "삼성 왜 빠졌어? — 하락 원인 분석\n"
        "비교 삼성 하이닉스 — 종목 비교\n"
        "시장 / 코스피 — 시장 종합\n"
        "환율 — USD/KRW, CNY, JPY\n"
        "공포지수 — VIX + Fear & Greed\n"
        "비트코인 — 암호화폐 시세\n"
        "금 / 원유 — 원자재 시세\n"
        "삼성 공시 — 최근 공시\n"
        "삼성 재무 — 재무제표\n"
        "뉴스 — 시장 뉴스 브리핑\n\n"
        "*명령어:*\n"
        "/pulse — 오늘의 시황\n"
        "/alert 005930 3.0 — 변동 알림\n"
        "/help — 도움말\n\n"
        "🌐 한국어 / 中文 / English"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def cmd_pulse(update: Update, context):
    """매일 시황"""
    user_id = str(update.effective_user.id)
    await update.message.reply_text("🔍 데이터 수집 중...")

    try:
        date_str = find_trading_date()
        watchlist = [t.strip() for t in
                     os.environ.get("KOREA_STOCK_WATCHLIST", DEFAULT_WATCHLIST).split(",")]
        data = fetch_all(date_str, watchlist)
        result = format_briefing(data, paid=True)
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"cmd_pulse error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_stock(update: Update, context):
    """종목 조회"""
    user_id = str(update.effective_user.id)
    if not context.args:
        await update.message.reply_text("사용법: /stock 005930")
        return

    try:
        ticker = context.args[0]
        date_str = find_trading_date()
        result = process_query(ticker, date_str)
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"cmd_stock error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_alert(update: Update, context):
    """가격 알림 설정"""
    user_id = str(update.effective_user.id)
    if len(context.args) < 1:
        await update.message.reply_text("사용법: /alert 005930 3.0")
        return

    try:
        ticker = context.args[0]
        threshold = float(context.args[1]) if len(context.args) > 1 else 3.0
        result = add_alert(ticker, threshold)
        await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"cmd_alert error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_dart(update: Update, context):
    """DART 공시"""
    user_id = str(update.effective_user.id)
    try:
        date_str = find_trading_date()
        result = process_query("공시", date_str)
        await update.message.reply_text(result, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"cmd_dart error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_sector(update: Update, context):
    """업종 등락 랭킹"""
    user_id = str(update.effective_user.id)
    try:
        from chat_query import handle_sector_ranking
        result = handle_sector_ranking("업종")
        try:
            await update.message.reply_text(result, parse_mode="Markdown")
        except Exception:
            await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"cmd_sector error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_hot(update: Update, context):
    """실시간 인기 종목"""
    user_id = str(update.effective_user.id)
    try:
        from chat_query import handle_hot_rank
        result = handle_hot_rank("인기")
        try:
            await update.message.reply_text(result, parse_mode="Markdown")
        except Exception:
            await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"cmd_hot error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_stats(update: Update, context):
    """추송 추적 통계 면판"""
    try:
        from push_tracker import get_stats, format_stats
        days = 30
        if context.args:
            try:
                days = int(context.args[0])
            except:
                pass
        # 사용자 언어 감지
        lang = "ko"
        user = update.effective_user
        if user.language_code and user.language_code.startswith("zh"):
            lang = "zh"
        elif user.language_code and user.language_code.startswith("en"):
            lang = "en"

        stats = get_stats(days)
        if stats["total_pushes"] == 0:
            if lang == "zh":
                await update.message.reply_text("📊 暂无推送记录。系统将自动积累数据。")
            else:
                await update.message.reply_text("📊 추송 기록이 아직 없습니다. 시스템이 자동으로 데이터를 축적합니다.")
            return
        result = format_stats(stats, lang)
        await send_long_message(update.message, result)
    except Exception as e:
        logger.error(f"cmd_stats error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


async def cmd_track(update: Update, context):
    """개별 종목 추송 추적"""
    try:
        from push_tracker import get_ticker_tracking, format_ticker_tracking
        from chat_query import resolve_ticker

        if not context.args:
            await update.message.reply_text("사용법: /track 삼성 또는 /track 005930")
            return

        query = " ".join(context.args)
        ticker = resolve_ticker(query)
        if not ticker:
            await update.message.reply_text(f"❌ '{query}' 종목을 찾을 수 없습니다.")
            return

        lang = "ko"
        user = update.effective_user
        if user.language_code and user.language_code.startswith("zh"):
            lang = "zh"

        events = get_ticker_tracking(ticker)
        result = format_ticker_tracking(ticker, events, lang)
        await send_long_message(update.message, result)
    except Exception as e:
        logger.error(f"cmd_track error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류: {e}")


# 运营管理员
ADMIN_IDS = {"502032880", "1421320482", "6725064630"}  # Karry, Rena, Jim


# ─── 자연어 메시지 처리 ───

async def handle_message(update: Update, context):
    """자연어 쿼리 라우팅 (DM + 群组@提及)"""
    if not update.message or not update.message.text:
        return

    await _sync_user_info_async(update, context)
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    chat_type = update.message.chat.type  # 'private', 'group', 'supergroup'

    # ── 群组白名单 ──
    if chat_type in ("group", "supergroup"):
        if not _group_allowed(update.message.chat.id):
            return  # 화이트리스트에 없는 群 → 무시

        bot_username = (await context.bot.get_me()).username.lower()
        is_mentioned = f"@{bot_username}" in text.lower()
        is_reply_to_bot = (
            update.message.reply_to_message
            and update.message.reply_to_message.from_user
            and update.message.reply_to_message.from_user.is_bot
            and update.message.reply_to_message.from_user.username
            and update.message.reply_to_message.from_user.username.lower() == bot_username
        )
        if not is_mentioned and not is_reply_to_bot:
            return  # 群里没@我，不响应

        # 去掉@mention部分
        text = re.sub(rf'@{bot_username}\s*', '', text, flags=re.IGNORECASE).strip()
        if not text:
            text = "help"

    # ── 引用 메시지에서 종목 컨텍스트 추출 ──
    if update.message.reply_to_message and update.message.reply_to_message.text:
        quoted_text = update.message.reply_to_message.text
        try:
            from onboarding import parse_stock_input, STOCK_NAMES
            from conversation import update_context as _update_ctx
            # 引用된 메시지에서 종목 코드 추출 (6자리 숫자 패턴)
            import re as _re2
            ticker_matches = _re2.findall(r'\b(\d{6})\b', quoted_text)
            # 또는 종목명으로 매칭
            quoted_tickers = parse_stock_input(quoted_text)
            found_ticker = None
            if quoted_tickers:
                found_ticker = quoted_tickers[0]
            elif ticker_matches:
                found_ticker = ticker_matches[0]
            # 컨텍스트에 저장하여 후속 질문에서 참조 가능
            if found_ticker:
                _update_ctx(user_id, ticker=found_ticker)
                logger.info(f"Context from quoted message: {found_ticker}")
        except Exception as e:
            logger.debug(f"Quote context extraction: {e}")

    # ── Rate limit ──
    allowed, rate_msg = _rate_check(user_id)
    if not allowed:
        await update.message.reply_text(rate_msg)
        return

    # ── 메시지 길이 제한 ──
    if len(text) > MAX_MESSAGE_LENGTH:
        await update.message.reply_text(f"⚠️ 메시지가 너무 깁니다. {MAX_MESSAGE_LENGTH}자 이내로 입력해 주세요.")
        return

    logger.info(f"[{chat_type}] Message from {user_id}: {text}")

    try:
        # Day-2 survey 응답 처리
        try:
            from cron_day2_survey import handle_day2_response
            day2_reply = handle_day2_response(user_id, text)
            if day2_reply:
                try:
                    await update.message.reply_text(day2_reply, parse_mode="Markdown")
                except Exception:
                    await update.message.reply_text(day2_reply)
                return
        except Exception as e:
            logger.debug(f"Day2 survey check: {e}")

        # Onboarding v2: 인도 흐름 처리
        try:
            from onboarding import is_onboarding_input, handle_onboarding_input, get_watchlist, add_to_watchlist, remove_from_watchlist, parse_stock_input, format_watchlist, STOCK_NAMES as OB_NAMES
            if is_onboarding_input(user_id, text):
                lang = "ko"
                if re.search(r'[\u4e00-\u9fff]', text):
                    lang = "zh"
                elif text.isascii():
                    lang = "en"

                result = handle_onboarding_input(user_id, text, lang)

                if result["action"] == "skip_to_normal":
                    # 사용자가 구체적 질문 → onboarding 건너뛰고 정상 처리
                    pass  # 아래 정상 흐름으로 계속
                else:
                    # reply / complete → 메시지 전송 후 리턴
                    for msg in result.get("messages", []):
                        try:
                            await update.message.reply_text(msg, parse_mode="Markdown")
                        except Exception:
                            await update.message.reply_text(msg)
                    return
        except Exception as e:
            logger.warning(f"Onboarding error: {e}")
            pass

        # 관심종목 관리 명령
        tl = text.lower()
        if tl in ("관심종목", "watchlist", "自选股", "관심", "my stocks"):
            try:
                from onboarding import format_watchlist
                result = format_watchlist(user_id)
                await update.message.reply_text(result, parse_mode="Markdown")
            except:
                await update.message.reply_text("📋 관심 종목 기능 준비 중")
            return

        if any(tl.startswith(p) for p in ["종목추가", "관심추가", "add ", "watch ", "关注 ", "추가 "]):
            try:
                from onboarding import parse_stock_input, add_to_watchlist, STOCK_NAMES as OB_NAMES
                stock_text = re.sub(r'^(종목추가|관심추가|add|watch|关注|추가)\s*', '', text, flags=re.IGNORECASE).strip()
                tickers = parse_stock_input(stock_text)
                if tickers:
                    for t in tickers:
                        add_to_watchlist(user_id, t)
                    names = [f"{OB_NAMES.get(t,t)}" for t in tickers]
                    await update.message.reply_text(f"✅ 추가: {', '.join(names)}")
                else:
                    await update.message.reply_text("❌ 종목을 인식하지 못했습니다.")
            except Exception as e:
                await update.message.reply_text(f"❌ {e}")
            return

        if any(tl.startswith(p) for p in ["종목삭제", "관심삭제", "remove ", "unwatch ", "取消 ", "삭제 "]):
            try:
                from onboarding import parse_stock_input, remove_from_watchlist, STOCK_NAMES as OB_NAMES
                stock_text = re.sub(r'^(종목삭제|관심삭제|remove|unwatch|取消|삭제)\s*', '', text, flags=re.IGNORECASE).strip()
                tickers = parse_stock_input(stock_text)
                if tickers:
                    for t in tickers:
                        remove_from_watchlist(user_id, t)
                    names = [f"{OB_NAMES.get(t,t)}" for t in tickers]
                    await update.message.reply_text(f"🗑 삭제: {', '.join(names)}")
                else:
                    await update.message.reply_text("❌ 종목을 인식하지 못했습니다.")
            except Exception as e:
                await update.message.reply_text(f"❌ {e}")
            return

        # 통계/추적 명령
        if tl in ("통계", "stats", "统计", "추송통계", "리뷰", "review", "推送回顾", "추적통계"):
            await cmd_stats(update, context)
            return

        # 시황 명령
        if text in ("시황", "pulse", "한국 시황", "코스피"):
            await cmd_pulse(update, context)
            return

        # 업종 명령
        if tl in ("업종", "sector", "행업", "行业", "업종별", "섹터"):
            await cmd_sector(update, context)
            return

        # 인기 종목
        if tl in ("인기", "hot", "핫", "热门", "인기종목", "trending", "순위"):
            await cmd_hot(update, context)
            return

        # AI 쿼리
        intent = classify_intent(text)
        date_str = find_trading_date()

        # Phase 1: 즉시 데이터 응답 (1-3초)
        await update.message.chat.send_action("typing")

        fast_result = process_query_fast(text, date_str, user_id)

        # 빠른 응답 먼저 전송
        msg = await send_long_message(update.message, fast_result)

        # Phase 2: AI 심층 분석 추가 (5-20초)
        await update.message.chat.send_action("typing")
        try:
            deep_result = process_query_deep(text, date_str, user_id)
            if deep_result:
                await send_long_message(update.message, deep_result)
        except:
            pass
    except Exception as e:
        logger.error(f"handle_message error: {e}", exc_info=True)
        await update.message.reply_text(f"❌ 오류가 발생했습니다: {e}")


# ─── 메인 ───

def main():
    if not TOKEN:
        print("=" * 50)
        print("🇰🇷 Mapulse Telegram Bot")
        print("=" * 50)
        print()
        print("⚠️  TELEGRAM_BOT_TOKEN 환경변수가 설정되지 않았습니다.")
        print()
        print("설정 방법:")
        print("1. Telegram에서 @BotFather에게 /newbot 명령")
        print("2. Bot 이름: Mapulse")
        print("3. Bot username: mapulse_bot (또는 원하는 이름)")
        print("4. 받은 토큰을 설정:")
        print()
        print("   export TELEGRAM_BOT_TOKEN='your_token_here'")
        print("   python3 mapulse_bot.py")
        print()
        print("BotFather 추천 설정:")
        print("  /setdescription — 한국 주식 AI 분석 봇. 실시간 KOSPI/KOSDAQ 시황, AI 원인 분석, DART 공시 알림.")
        print("  /setcommands —")
        print("    pulse - 오늘의 시황 브리핑")
        print("    stock - 종목 조회 (예: /stock 005930)")
        print("    alert - 급락 알림 설정")
        print("    dart - DART 공시")
        print("    help - 도움말")
        print()
        return

    print("🇰🇷 Mapulse Telegram Bot 시작...")
    print("   [Free / Open Skill Mode]")
    print()

    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("pulse", cmd_pulse))
    app.add_handler(CommandHandler("stock", cmd_stock))
    app.add_handler(CommandHandler("alert", cmd_alert))
    app.add_handler(CommandHandler("dart", cmd_dart))
    app.add_handler(CommandHandler("sector", cmd_sector))
    app.add_handler(CommandHandler("hot", cmd_hot))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("track", cmd_track))

    # Natural language (DM + 群组)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot 준비 완료. 메시지 대기 중...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
