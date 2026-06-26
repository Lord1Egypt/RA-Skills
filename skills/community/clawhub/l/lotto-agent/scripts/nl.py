"""自然语言解析（两段式）+ 反问 + generate guard。"""
from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Any

import lotto
from store import cn_now

# ---------- 关键词表 ----------
IMMEDIATE = ("现在", "立刻", "马上", "立即", "直接给", "直接生成", "直接出", "现就", "这就")
TIME_OF_DAY = ("早上", "早晨", "明早", "上午", "中午", "下午", "晚上", "今晚", "明晚", "等下", "等一下", "晚点")
FUTURE_DAY = ("明天", "明晚", "后天", "大后天", "明早")
TODAY_WORDS = ("今天", "今晚")
RECURRING_WORDS = ("每天", "每日", "每晚", "每早", "每周", "每期开奖后", "以后每天", "定时", "自动")

WEEKDAY_RE = re.compile(r"(?:周|星期|礼拜)([一二三四五六日天])")
EXPLICIT_DATE_RE = re.compile(r"(\d{4}[-/年])?(\d{1,2})[-/月](\d{1,2})日?")
CLOCK_RE = re.compile(r"(\d{1,2})\s*[点:：]\s*(\d{0,2})")
TIME_RANGE_RE = re.compile(r"(\d{1,2})\s*[点:：]\s*\d{0,2}\s*(?:到|至|-)\s*(\d{1,2})\s*[点:：]?\s*(\d{0,2})")
ISSUE_RE = re.compile(r"第?\s*(\d{3,})\s*期")
CN_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
WEEKDAY_CN = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "日": 7, "天": 7}


# ---------- 字段抽取 ----------
def detect_lottery(text: str) -> str | None:
    low = text.lower()
    for key, cfg in lotto.LOTTERIES.items():
        for alias in cfg.get("aliases", []):
            if str(alias).lower() in low:
                return key
    return None


def detect_count(text: str) -> int | None:
    m = re.search(r"(\d+)\s*注", text)
    return int(m.group(1)) if m else None


def detect_budget(text: str) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)\s*元", text)
    if m and "奖金" not in text and "奖池" not in text:
        return float(m.group(1))
    return None


def detect_multiple(text: str) -> int | None:
    if "双倍" in text or "两倍" in text:
        return 2
    m = re.search(r"(\d+)\s*倍", text)
    return int(m.group(1)) if m else None


def detect_play_type(text: str) -> str | None:
    if "组三" in text:
        return "group3"
    if "组六" in text:
        return "group6"
    if "单选" in text or "直选" in text:
        return "single"
    m = re.search(r"选\s*(十|[一二三四五六七八九]|\d{1,2})", text)
    if m:
        v = m.group(1)
        return str(CN_NUM.get(v, int(v) if v.isdigit() else v))
    return None


def detect_additional(text: str) -> bool | None:
    if "不追加" in text or "不要追加" in text:
        return False
    if "追加" in text:
        return True
    return None


def detect_issue(text: str) -> str | None:
    m = ISSUE_RE.search(text)
    return m.group(1) if m else None


def detect_explicit_date(text: str) -> str | None:
    m = re.search(r"(\d{4})[-/年](\d{1,2})[-/月](\d{1,2})日?", text)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
    m = re.search(r"(?<!\d)(\d{1,2})\s*月\s*(\d{1,2})\s*日?", text)
    if m:
        base = cn_now().date()
        cand = date(base.year, int(m.group(1)), int(m.group(2)))
        if cand < base - timedelta(days=180):
            cand = date(base.year + 1, int(m.group(1)), int(m.group(2)))
        return cand.isoformat()
    return None


def detect_relative_date(text: str) -> str | None:
    base = cn_now().date()
    if "今天" in text or "今晚" in text:
        return base.isoformat()
    if "明天" in text or "明晚" in text or "明早" in text:
        return (base + timedelta(days=1)).isoformat()
    if "后天" in text:
        return (base + timedelta(days=2)).isoformat()
    if "大后天" in text:
        return (base + timedelta(days=3)).isoformat()
    return None


def detect_time_window(text: str) -> tuple[str, str, bool]:
    """返回 (time_start, time_end, random_window)。无明确时段时返回 ('', '', False)。"""
    m = TIME_RANGE_RE.search(text)
    if m:
        start_h = _normalize_hour(int(m.group(1)), text)
        end_h = _normalize_hour(int(m.group(2)), text)
        end_m = int(m.group(3) or 0)
        return f"{start_h:02d}:00", f"{end_h:02d}:{end_m:02d}", True
    m = CLOCK_RE.search(text)
    if m:
        h = _normalize_hour(int(m.group(1)), text)
        mm = int(m.group(2) or 0)
        return f"{h:02d}:{mm:02d}", f"{h:02d}:{mm:02d}", False
    if any(w in text for w in ("早上", "早晨", "明早", "上午")):
        return "07:00", "12:00", True
    if "中午" in text:
        return "11:00", "13:00", True
    if "下午" in text:
        return "12:00", "18:00", True
    if "晚上" in text or "今晚" in text or "明晚" in text or "每晚" in text:
        return "18:00", "23:30", True
    return "", "", False


def _normalize_hour(hour: int, text: str) -> int:
    if any(w in text for w in ("下午", "晚上", "今晚", "每晚", "明晚")) and hour < 12:
        return hour + 12
    if "中午" in text and hour < 11:
        return hour + 12
    return hour


def detect_weekdays(text: str) -> list[int]:
    m = re.search(r"每周([一二三四五六日天,，、和及]+)", text)
    if not m:
        return []
    return sorted({WEEKDAY_CN[ch] for ch in m.group(1) if ch in WEEKDAY_CN})


def detect_single_weekday(text: str) -> int | None:
    m = WEEKDAY_RE.search(text)
    if not m:
        return None
    return WEEKDAY_CN.get(m.group(1))


def detect_draw_day_offset(text: str) -> tuple[bool, int]:
    if "开奖前一天" in text or "开奖日前一天" in text:
        return True, -1
    if "开奖那天" in text or "开奖当天" in text or "开奖日" in text:
        return True, 0
    return False, 0


def detect_report_window(text: str) -> int:
    if "本月" in text or "月报" in text or "这个月" in text:
        return 30
    if "本周" in text or "周报" in text or "这一周" in text or "这周" in text:
        return 7
    return 30


# ---------- 状态判断 ----------
def has_immediate(text: str) -> bool:
    return any(w in text for w in IMMEDIATE)


def has_time_info(text: str) -> bool:
    if any(w in text for w in TIME_OF_DAY):
        return True
    if CLOCK_RE.search(text):
        return True
    return False


def has_future_time(text: str) -> bool:
    if any(w in text for w in FUTURE_DAY):
        return True
    if WEEKDAY_RE.search(text):
        return True
    if has_time_info(text):
        return True
    if EXPLICIT_DATE_RE.search(text):
        return True
    if any(w in text for w in TODAY_WORDS):
        return True
    return False


def has_day_info(text: str) -> bool:
    return (any(w in text for w in FUTURE_DAY)
            or bool(WEEKDAY_RE.search(text))
            or bool(EXPLICIT_DATE_RE.search(text))
            or any(w in text for w in TODAY_WORDS))


# ---------- guard：generate 入口的二次校验 ----------
def guard_text_intent(text: str | None) -> dict[str, Any] | None:
    if not text:
        return None
    if has_immediate(text):
        return None
    if not has_future_time(text):
        return None
    has_day = has_day_info(text)
    has_time = has_time_info(text)
    if has_day and has_time:
        msg = "你这句像是要让我到点再发，不是现在出号。我把它存成定时任务，确认下时间和彩种就行。"
        fb = "是想等到那个时段我再自动给你，对吧？只这一次还是以后每次都来？"
    else:
        msg = "时间或日期不够明确，我还不能直接出号。先告诉我哪一天 / 什么时段（早上/上午/中午/下午/晚上）？"
        fb = "再补一下日期或时段（早上/下午/晚上/X点都行），我再给你排上。"
    return {"ok": False, "needs_clarification": True, "requires_automation": True,
            "message_text": msg, "followup_messages": [fb]}


# ---------- 反问 ----------
def _clarify(message: str, fallback: str, error: str) -> dict[str, Any]:
    return {"ok": False, "needs_clarification": True, "error": error,
            "message_text": message, "followup_messages": [fallback]}


def needs_clarification(text: str) -> dict[str, Any] | None:
    """日期/时段缺一半时反问。仅当 generate-类意图触发。"""
    if not any(w in text for w in ("生成", "选号", "给我", "来一组", "再来一组", "一注", "几注", "注")):
        return None
    if has_immediate(text):
        return None
    # 含 recurring 关键词或开奖日触发器时不需要"哪一天"，因为定义里就是周期性 / 跟开奖走
    if any(w in text for w in RECURRING_WORDS):
        return None
    if any(w in text for w in ("开奖那天", "开奖当天", "开奖日", "开奖前一天", "开奖日前一天")):
        return None
    has_day = has_day_info(text)
    has_time = has_time_info(text)
    weekday = WEEKDAY_RE.search(text)
    weekday_recurring = "每周" in text or any(w in text for w in ("这周", "本周", "这个周", "下周", "下个周"))
    # 时段词没说哪天
    if has_time and not has_day:
        return _clarify("你说的是今天还是明天？我帮你排个一次性定时任务，到时间再生成并推给你。",
                         "今天还是明天？", "未指定日期")
    # 周X 没说每周/这周
    if weekday and not weekday_recurring:
        return _clarify("你说的周X：只这一次（这周或下周），还是以后每周都来？时段呢——早上/上午/下午/晚上？",
                         "只这一次还是以后每周？时段呢？", "未指定一次还是每周")
    # 有日期但没说时段
    if has_day and not has_time and (any(w in text for w in FUTURE_DAY) or EXPLICIT_DATE_RE.search(text)):
        return _clarify("那一天什么时候给你？早上、上午、中午、下午还是晚上？或者直接说几点。",
                         "再补一下时段（早上/上午/中午/下午/晚上）或具体几点。", "未指定时段")
    return None


# ---------- INTENT 分类表 ----------
INTENTS: list[tuple[str, str]] = [
    (r"我买了|帮我记录|这几注我买", "record"),
    (r"取消|不要算成本|不算成本", "cancel"),
    (r"自动任务列表|查看自动任务|有哪些自动任务", "list_tasks"),
    (r"停用.*任务|停用自动任务|取消每天|停止每天", "disable_task"),
    (r"绑定通知|绑定当前窗口|以后发到这里|把消息发到这里", "setup_notify"),
    (r"开奖|奖池|最新开奖", "fetch_draw"),
    (r"兑奖|中奖|有没有中|帮我查一下今天中了没|今天中了没", "check_prize"),
    (r"盈亏|报表|花了多少|本周|本月|月报|周报", "report"),
]


# ---------- 主入口 ----------
def parse(text: str) -> dict[str, Any]:
    msg = (text or "").strip()
    if not msg:
        return {"ok": False, "error": "空命令"}

    # 1. 含"立即字样" → 直接 generate（不反问、不走 guard）
    if has_immediate(msg) and any(w in msg for w in ("给我", "生成", "选号", "注")):
        return {"ok": True, "action": "generate",
                "params": _build_generate_params(msg, force_immediate=True)}

    # 2. 反问优先
    clar = needs_clarification(msg)
    if clar:
        return clar

    # 3. 未来时间词 / 周期词 / 开奖日触发器 → create_task
    has_recurring = any(w in msg for w in RECURRING_WORDS)
    has_draw_trigger = any(w in msg for w in ("开奖那天", "开奖当天", "开奖日", "开奖前一天", "开奖日前一天"))
    has_future = has_future_time(msg) or has_recurring or has_draw_trigger
    # "今天/明天" 配合 兑奖/开奖 是查询类意图（"兑奖今天的号码"），不进 create_task
    is_query_intent = (
        any(w in msg for w in ("兑奖", "中奖", "有没有中"))
        and not has_recurring and not has_draw_trigger
        and not (any(w in msg for w in TIME_OF_DAY) or CLOCK_RE.search(msg))
        and not (WEEKDAY_RE.search(msg) or any(w in msg for w in FUTURE_DAY) or EXPLICIT_DATE_RE.search(msg))
    )
    if has_future and any(w in msg for w in ("给我", "生成", "选号", "注", "兑奖", "开奖", "报告")) and not is_query_intent:
        return _build_task_intent(msg)

    # 4. 显式意图分类
    for pattern, action in INTENTS:
        if re.search(pattern, msg):
            return {"ok": True, "action": action,
                    "params": EXTRACTORS[action](msg)}

    # 5. lottery + 期号 / "查/最新" 等查询 → fetch_draw
    if detect_lottery(msg) and (detect_issue(msg) or any(w in msg for w in ("查", "最新", "开奖"))):
        return {"ok": True, "action": "fetch_draw",
                "params": EXTRACTORS["fetch_draw"](msg)}

    # 6. 兜底：generate（仅当用户明确表达"出号"意图）
    if any(w in msg for w in ("给我", "生成", "来一组", "选号", "方案", "注")):
        return {"ok": True, "action": "generate",
                "params": _build_generate_params(msg, force_immediate=False)}

    return {"ok": False, "error": "未识别命令", "text": msg}


# ---------- 各 action 的字段抽取 ----------
def _build_generate_params(text: str, force_immediate: bool) -> dict[str, Any]:
    p: dict[str, Any] = {"text": text}
    lot = detect_lottery(text) or "dlt"
    p["lottery"] = lot
    if (c := detect_count(text)) is not None: p["count"] = c
    if (b := detect_budget(text)) is not None: p["budget"] = b
    if (m := detect_multiple(text)) is not None: p["multiple"] = m
    if (pt := detect_play_type(text)) is not None: p["play_type"] = pt
    if (ad := detect_additional(text)) is not None: p["additional"] = ad
    return p


def _build_task_intent(text: str) -> dict[str, Any]:
    """根据文本组装 create_task 参数。已在调用前确认 has_future_time + 至少含一个 trigger 关键词。"""
    action = _detect_task_action(text)

    # schedule_kind
    recurring = any(w in text for w in RECURRING_WORDS)
    has_draw_day, offset = detect_draw_day_offset(text)
    weekdays_every = detect_weekdays(text)
    explicit_date = detect_explicit_date(text)
    relative_date = detect_relative_date(text)
    weekday_one = detect_single_weekday(text)

    if has_draw_day:
        kind = "draw_day"
        spec = f"{detect_lottery(text) or 'all'}:{offset}"
    elif weekdays_every:
        kind = "weekly"
        spec = ",".join(str(w) for w in weekdays_every)
    elif "每天" in text or "每日" in text or "每晚" in text or "每早" in text or recurring:
        kind = "daily"
        spec = None
    else:
        # once
        kind = "once"
        run_date = explicit_date or relative_date
        if not run_date and weekday_one is not None:
            base = cn_now().date()
            delta = (weekday_one - base.isoweekday()) % 7
            if delta == 0:
                delta = 7
            run_date = (base + timedelta(days=delta)).isoformat()
        if not run_date:
            run_date = cn_now().date().isoformat()
        spec = run_date

    ts, te, rand = detect_time_window(text)
    if not ts:
        ts = te = "09:00"

    params: dict[str, Any] = {}
    lot = detect_lottery(text)
    if lot: params["lottery"] = lot
    elif action in {"fetch_draw", "draw_check_prize", "check_prize"}: params["lottery"] = "all"
    if action == "generate":
        params["count"] = detect_count(text) or 1
        if (m := detect_multiple(text)): params["multiple"] = m
        if (pt := detect_play_type(text)): params["play_type"] = pt
        if (ad := detect_additional(text)): params["additional"] = ad
        if (b := detect_budget(text)) is not None: params["budget"] = b
    if action == "report":
        params["since_days"] = detect_report_window(text)

    return {"ok": True, "action": "create_task",
            "params": {
                "task_action": action,
                "schedule_kind": kind,
                "schedule_spec": spec,
                "time_start": ts,
                "time_end": te,
                "random_window": rand,
                "params": params,
                "raw_text": text,
            }}


def _detect_task_action(text: str) -> str:
    if "开奖后" in text and any(w in text for w in ("兑奖", "中奖", "查中奖")):
        return "draw_check_prize"
    if any(w in text for w in ("兑奖", "中奖", "有没有中")):
        return "draw_check_prize" if any(w in text for w in ("开奖后", "数据出来")) else "check_prize"
    if any(w in text for w in ("报表", "盈亏", "月报", "周报")):
        return "report"
    if "开奖" in text and not any(w in text for w in ("号码", "选号", "生成", "给我", "注")):
        return "fetch_draw"
    return "generate"


def extract_record(text: str) -> dict[str, Any]:
    p: dict[str, Any] = {"text": text}
    if (lot := detect_lottery(text)): p["lottery"] = lot
    if (m := detect_multiple(text)): p["multiple"] = m
    if (ad := detect_additional(text)) is not None: p["additional"] = ad
    if (i := detect_issue(text)): p["issue"] = i
    return p


def extract_cancel(text: str) -> dict[str, Any]:
    if (c := detect_count(text)): return {"limit": c}
    return {"limit": 10}


def extract_list_tasks(_: str) -> dict[str, Any]:
    return {}


def extract_disable_task(text: str) -> dict[str, Any]:
    m = re.search(r"#?\s*(\d+)\s*号?任务", text)
    return {"task_id": int(m.group(1))} if m else {}


def extract_setup_notify(_: str) -> dict[str, Any]:
    return {}


def extract_fetch_draw(text: str) -> dict[str, Any]:
    p: dict[str, Any] = {"lottery": detect_lottery(text) or "all"}
    if (i := detect_issue(text)): p["issue"] = i
    return p


def extract_check_prize(text: str) -> dict[str, Any]:
    p: dict[str, Any] = {}
    if (lot := detect_lottery(text)): p["lottery"] = lot
    if (i := detect_issue(text)): p["issue"] = i
    return p


def extract_report(text: str) -> dict[str, Any]:
    return {"since_days": detect_report_window(text)}


EXTRACTORS = {
    "record": extract_record,
    "cancel": extract_cancel,
    "list_tasks": extract_list_tasks,
    "disable_task": extract_disable_task,
    "setup_notify": extract_setup_notify,
    "fetch_draw": extract_fetch_draw,
    "check_prize": extract_check_prize,
    "report": extract_report,
}
