"""GitHub 公共开奖抓取 + 极简开奖日历（无 holiday_overrides）。"""
from __future__ import annotations

import json
import os
import re
from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

import store
from store import CN_TZ, cn_now, now_iso

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "config.json"
CONFIG: dict[str, Any] = json.loads(_CONFIG_PATH.read_text(encoding="utf-8-sig")) if _CONFIG_PATH.exists() else {}

# 默认开奖周历（节假日休市以公共数据为准，本地不再硬编码 holiday）
DEFAULT_WEEKLY: dict[str, dict[str, Any]] = {
    "ssq":  {"draw_weekdays": [2, 4, 7], "draw_time": "21:15", "buy_end_time": "20:00"},
    "dlt":  {"draw_weekdays": [1, 3, 6], "draw_time": "20:30", "buy_end_time": "20:00"},
    "qxc":  {"draw_weekdays": [2, 5, 7], "draw_time": "20:30", "buy_end_time": "20:00"},
    "qlc":  {"draw_weekdays": [1, 3, 5], "draw_time": "21:15", "buy_end_time": "20:00"},
    "fc3d": {"draw_weekdays": [1,2,3,4,5,6,7], "draw_time": "21:15", "buy_end_time": "20:00"},
    "pl3":  {"draw_weekdays": [1,2,3,4,5,6,7], "draw_time": "20:30", "buy_end_time": "20:00"},
    "pl5":  {"draw_weekdays": [1,2,3,4,5,6,7], "draw_time": "20:30", "buy_end_time": "20:00"},
    "kl8":  {"draw_weekdays": [1,2,3,4,5,6,7], "draw_time": "21:30", "buy_end_time": "20:00"},
}


def _api_base() -> str:
    base = os.environ.get("LOTTERY_PUBLIC_DATA_BASE_URL")
    if base:
        return base.rstrip("/")
    return str(CONFIG.get("api_base_url",
        "https://raw.githubusercontent.com/wenjinliuu/lottery-data-repo/main/public_data")).rstrip("/")


# ---------- 抓取 ----------
def fetch_draw(lottery: str = "all", issue: str | None = None) -> dict[str, Any]:
    if lottery == "all":
        results = []
        ok = 0
        for key in DEFAULT_WEEKLY:
            r = fetch_draw(key, issue=issue)
            results.append(r)
            ok += 1 if r.get("ok") else 0
        return {"ok": ok == len(results), "results": results,
                "message_text": f"开奖抓取完成：{ok}/{len(results)} 成功"}
    try:
        payload = _read_json(_url(lottery, issue))
        draw = _select_draw(lottery, issue, payload)
        store.upsert_draw(draw)
        return {"ok": True, "draw": draw, "message_text": _render_draw(draw)}
    except (OSError, ValueError, KeyError, json.JSONDecodeError, HTTPError, URLError, TimeoutError) as exc:
        return {"ok": False, "error": str(exc), "lottery": lottery,
                "message_text": f"{lottery} 抓取失败：{exc}"}


def _url(lottery: str, issue: str | None) -> str:
    base = _api_base()
    if issue:
        return f"{base}/draws/{lottery}.json"
    return f"{base}/latest.json"


def _read_json(location: str) -> dict[str, Any]:
    if location.startswith(("http://", "https://")):
        with urlopen(location, timeout=12) as resp:
            return json.loads(resp.read().decode("utf-8"))
    with Path(location).open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _select_draw(lottery: str, issue: str | None, payload: dict[str, Any]) -> dict[str, Any]:
    if issue:
        draws = payload.get("draws", [])
        if isinstance(draws, dict):
            d = draws.get(issue)
            if d:
                return _normalize(lottery, d)
        for d in draws or []:
            if str(d.get("issue")) == str(issue):
                return _normalize(lottery, d)
        raise ValueError(f"公开开奖源中找不到 {lottery} 第 {issue} 期")
    d = payload.get("draws", {}).get(lottery)
    if not d:
        raise ValueError(f"latest.json 没有 {lottery}")
    return _normalize(lottery, d)


def _normalize(lottery: str, payload: dict[str, Any]) -> dict[str, Any]:
    issue = str(payload.get("issue") or "")
    if not issue:
        raise ValueError("开奖数据缺少期号")
    return {
        "lottery": lottery, "issue": issue,
        "draw_date": str(payload.get("draw_date") or "")[:10],
        "numbers": payload.get("numbers") or {},
        "prize_pool": payload.get("prize_pool"),
        "prize_details": payload.get("prize_details") or [],
        "next_issue": str(payload.get("next_issue") or ""),
        "next_draw_date": str(payload.get("next_draw_date") or "")[:10],
        "next_buy_end_time": str(payload.get("next_buy_end_time") or ""),
        "raw": payload, "fetched_at": now_iso(),
    }


def _render_draw(draw: dict[str, Any]) -> str:
    import lotto
    name = lotto.LOTTERIES[draw["lottery"]]["name"]
    parts = [f"{name} 第{draw['issue']}期开奖",
             lotto.format_numbers(draw["lottery"], draw.get("numbers") or {}),
             f"开奖日期：{draw.get('draw_date') or '-'}"]
    if draw.get("prize_pool"):
        parts.append(f"奖池：{draw['prize_pool']}")
    return "\n".join(parts)


# ---------- 开奖日历 / 选号绑定 ----------
def parse_cn_dt(text: str | None) -> datetime | None:
    if not text:
        return None
    text = str(text).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
        try:
            dt = datetime.strptime(text, fmt)
            return dt if dt.tzinfo else dt.replace(tzinfo=CN_TZ)
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(text)
        return dt if dt.tzinfo else dt.replace(tzinfo=CN_TZ)
    except ValueError:
        return None


def is_draw_day(lottery: str, day_iso: str) -> bool:
    """根据公共开奖日历判断当天是否开奖。优先看 draws 表里有没有这天的记录，否则用周历兜底。"""
    row = store.fetch_one(
        "SELECT issue FROM draws WHERE lottery=? AND draw_date=? LIMIT 1",
        (lottery, day_iso),
    )
    if row:
        return True
    try:
        target = date.fromisoformat(day_iso)
    except ValueError:
        return False
    cfg = DEFAULT_WEEKLY.get(lottery, {})
    return target.isoweekday() in {int(d) for d in cfg.get("draw_weekdays", [])}


def next_fallback(lottery: str, start: date | None = None) -> dict[str, str]:
    cfg = DEFAULT_WEEKLY.get(lottery, {})
    weekdays = {int(d) for d in cfg.get("draw_weekdays", [])}
    if not weekdays:
        return {}
    start_date = start or cn_now().date()
    draw_t = cfg.get("draw_time", "21:00")
    buy_t = cfg.get("buy_end_time", "20:00")
    now = cn_now()
    for offset in range(0, 15):
        cand = start_date + timedelta(days=offset)
        if cand.isoweekday() not in weekdays:
            continue
        buy_end = _combine(cand, buy_t)
        if cand == now.date() and buy_end and now > buy_end:
            continue
        return {"draw_date": cand.isoformat(),
                "next_open_time": f"{cand.isoformat()} {draw_t}:00",
                "buy_end_time": f"{cand.isoformat()} {buy_t}:00"}
    return {}


def _combine(d: date, hm: str) -> datetime | None:
    try:
        parts = [int(p) for p in hm.split(":")]
        while len(parts) < 3:
            parts.append(0)
        return datetime.combine(d, time(parts[0], parts[1], parts[2]), tzinfo=CN_TZ)
    except (ValueError, IndexError):
        return None


def resolve_tracking(lottery: str) -> dict[str, Any]:
    """选号时绑定下一期：优先看本地最新 draw 的 next_*，stale 则回退到周历。"""
    latest = store.latest_draw(lottery) or {}
    now = cn_now()
    next_buy_end = parse_cn_dt(latest.get("next_buy_end_time"))
    if latest.get("next_issue") and next_buy_end and now <= next_buy_end:
        return {
            "issue": latest.get("next_issue"),
            "draw_date": latest.get("next_draw_date") or _date_part(latest.get("next_buy_end_time")),
            "notice": "",
        }
    fb = next_fallback(lottery, now.date())
    notice = ""
    if latest.get("next_issue"):
        notice = f"最新日历中的 {latest.get('next_issue')} 期已过销售截止时间，已按下一次开奖日生成。"
    return {
        "issue": None,
        "draw_date": fb.get("draw_date"),
        "notice": notice,
    }


def _date_part(value: Any) -> str:
    return str(value or "")[:10]
