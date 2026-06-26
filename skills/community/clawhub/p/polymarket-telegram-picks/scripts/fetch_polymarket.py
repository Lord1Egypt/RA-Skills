#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Polymarket Gamma API 拉取「当日、未开赛」的 NBA 比赛及赔率，输出为便于 AI 分析的文本摘要。
无需 API Key，可直接运行。
"""
import json
import sys
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

GAMMA_BASE = "https://gamma-api.polymarket.com"
CHINA_TZ_OFFSET = timedelta(hours=8)

# Polymarket 体育元数据中 NBA 的 tag_id（/sports 返回的 "nba" 项里 tags 含 745）
NBA_TAG_ID = 745


def parse_utc(ts):
    """将 API 返回的时间转为 UTC datetime。"""
    if ts is None:
        return None
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts, tz=timezone.utc)
        s = str(ts).replace("Z", "+00:00")
        return datetime.fromisoformat(s)
    except Exception:
        return None


def fetch_nba_events_today(limit=80):
    """
    拉取 NBA 活动事件（tag_id=745），返回列表供后续按「当日、未开赛」过滤。
    若 API 支持 start_date_min/max 则传入今日中国时间对应的 UTC 范围以缩小数据量。
    """
    now_utc = datetime.now(timezone.utc)
    today_china = (now_utc + CHINA_TZ_OFFSET).date()
    start_utc = datetime(today_china.year, today_china.month, today_china.day, 0, 0, 0, tzinfo=timezone.utc) - CHINA_TZ_OFFSET
    end_utc = start_utc + timedelta(days=1) - timedelta(seconds=1)
    start_iso = start_utc.isoformat().replace("+00:00", "Z")
    end_iso = end_utc.isoformat().replace("+00:00", "Z")

    params = [
        f"limit={limit}",
        "active=true",
        "closed=false",
        f"tag_id={NBA_TAG_ID}",
        "order=startDate",
        "ascending=true",
    ]
    # 部分 Gamma API 支持事件按日期范围筛选；若不支持则用无日期参数的请求再过滤
    url_with_dates = f"{GAMMA_BASE}/events?{'&'.join(params + [f'start_date_min={start_iso}', f'start_date_max={end_iso}'])}"
    url_fallback = f"{GAMMA_BASE}/events?{'&'.join(params)}"
    req_headers = {"Accept": "application/json"}
    raw = None
    for url in (url_with_dates, url_fallback):
        try:
            req = Request(url, headers=req_headers)
            with urlopen(req, timeout=30) as r:
                raw = json.loads(r.read().decode())
            break
        except (URLError, HTTPError):
            continue
    if raw is None:
        raise URLError("无法拉取 Polymarket NBA 事件列表")
    # 本地二次过滤：只保留「中国时间当日」且「未开赛」
    result = []
    for ev in raw:
        start = ev.get("startDate") or ev.get("start_date")
        start_dt = parse_utc(start)
        if start_dt is None:
            continue
        local_dt = start_dt + CHINA_TZ_OFFSET
        if local_dt.date() != today_china:
            continue
        if start_dt <= now_utc:
            continue
        result.append(ev)
    return result


def format_outcome_prices(outcomes_str, prices_str):
    """解析 outcomes 和 outcomePrices（均为 JSON 字符串）。"""
    try:
        outcomes = json.loads(outcomes_str) if isinstance(outcomes_str, str) else outcomes_str
        prices = json.loads(prices_str) if isinstance(prices_str, str) else prices_str
    except (json.JSONDecodeError, TypeError):
        return []
    if not outcomes or not prices:
        return []
    return list(zip(outcomes, prices))


def main():
    try:
        events = fetch_nba_events_today()
    except (URLError, HTTPError) as e:
        print(f"[错误] 拉取 Polymarket NBA 数据失败: {e}", file=sys.stderr)
        sys.exit(1)

    now_utc = datetime.now(timezone.utc)
    today_str = (now_utc + CHINA_TZ_OFFSET).strftime("%Y-%m-%d")

    lines = [
        f"# Polymarket 当日未开赛 NBA 比赛（UTC+8 日期: {today_str}）",
        "",
        "以下为今日、且尚未开赛的 NBA 相关市场及赔率（隐含概率），可作为下注参考。",
        "",
    ]

    count = 0
    for ev in events:
        start = ev.get("startDate") or ev.get("start_date")
        start_dt = parse_utc(start)
        title = ev.get("title") or "无标题"
        markets = ev.get("markets") or ev.get("groupItemMarkets") or []
        if not markets:
            continue

        count += 1
        start_desc = start_dt.strftime("%Y-%m-%d %H:%M UTC") if start_dt else "—"
        lines.append(f"## {title}")
        lines.append(f"开赛时间: {start_desc}")
        lines.append("")
        for m in markets[:20]:
            q = m.get("question") or m.get("groupItemTitle") or "无题目"
            outcomes_str = m.get("outcomes")
            prices_str = m.get("outcomePrices")
            if not outcomes_str or not prices_str:
                lines.append(f"- {q}: (无赔率)")
                continue
            pairs = format_outcome_prices(outcomes_str, prices_str)
            parts = [f"{name} {float(p)*100:.1f}%" for name, p in pairs if p]
            lines.append(f"- {q}")
            lines.append(f"  选项与隐含概率: {', '.join(parts)}")
        lines.append("")

    if count == 0:
        lines.append("今日暂无符合条件的未开赛 NBA 比赛。")
    else:
        lines.append(f"--- 共 {count} 场当日未开赛 NBA 相关事件。")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
