#!/usr/bin/env python3
"""
Query 12306 for train tickets: Hankou -> Xianning
Uses Playwright to bypass anti-bot, then queries API in browser context.
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright


# Query parameters
FROM_STATION = "HKN"  # 汉口
FROM_NAME = "汉口"

# Query multiple destination stations to cover all Xianning stations
DESTINATIONS = [
    ("UNN", "咸宁南"),
    ("XNN", "咸宁"),
    ("XRN", "咸宁北"),
]

DATES = [
    "2026-03-27",  # 今天
    "2026-04-03",  # 下周五
    "2026-04-10",  # 下下周五
]

DATE_LABELS = {
    "2026-03-27": "今天 (3月27日 周五)",
    "2026-04-03": "下周五 (4月3日)",
    "2026-04-10": "下下周五 (4月10日)",
}


def parse_train_data(raw_str):
    """Parse 12306 raw train data string into structured dict"""
    fields = raw_str.split('|')
    if len(fields) < 35:
        return None

    try:
        return {
            "train_no": fields[2],         # 车次完整编号
            "train_code": fields[3],       # 车次（如C5601）
            "from_station": fields[6],     # 出发站代码
            "to_station": fields[7],       # 到达站代码
            "depart_time": fields[8],      # 出发时间
            "arrive_time": fields[9],      # 到达时间
            "duration": fields[10],        # 历时
            "can_buy": fields[11],         # 是否可预订 Y/N
            "date": fields[13],            # 出发日期
            # Seat availability
            "swz": fields[25] or "--",     # 商务座/特等座
            "ydz": fields[31] or "--",     # 一等座
            "edz": fields[30] or "--",     # 二等座
            "gjrw": fields[21] or "--",    # 高级软卧
            "rw": fields[23] or "--",      # 软卧/一等卧
            "dw": fields[33] or "--",      # 动卧
            "yw": fields[28] or "--",      # 硬卧/二等卧
            "rz": fields[24] or "--",      # 软座
            "yz": fields[29] or "--",      # 硬座
            "wz": fields[26] or "--",      # 无座
        }
    except (IndexError, ValueError):
        return None


async def query_tickets(page, date, from_code, to_code, to_name):
    """Query tickets for a specific date and route"""
    api_url = (
        f"https://kyfw.12306.cn/otn/leftTicket/queryZ?"
        f"leftTicketDTO.train_date={date}"
        f"&leftTicketDTO.from_station={from_code}"
        f"&leftTicketDTO.to_station={to_code}"
        f"&purpose_codes=ADULT"
    )

    try:
        result = await page.evaluate(f'''
            async () => {{
                try {{
                    const resp = await fetch("{api_url}", {{
                        headers: {{
                            "Accept": "application/json",
                            "X-Requested-With": "XMLHttpRequest"
                        }}
                    }});
                    return await resp.json();
                }} catch(e) {{
                    return {{"error": e.message}};
                }}
            }}
        ''')

        if not result or "data" not in result or "result" not in result.get("data", {}):
            return []

        trains = []
        for raw in result["data"]["result"]:
            train = parse_train_data(raw)
            if train:
                train["to_name"] = to_name
                trains.append(train)
        return trains

    except Exception as e:
        print(f"    Query error ({to_name}, {date}): {e}")
        return []


async def query_with_alt_api(page, date, from_code, to_code, to_name):
    """Try alternative API endpoint"""
    api_url = (
        f"https://kyfw.12306.cn/otn/leftTicket/query?"
        f"leftTicketDTO.train_date={date}"
        f"&leftTicketDTO.from_station={from_code}"
        f"&leftTicketDTO.to_station={to_code}"
        f"&purpose_codes=ADULT"
    )

    try:
        result = await page.evaluate(f'''
            async () => {{
                try {{
                    const resp = await fetch("{api_url}", {{
                        headers: {{
                            "Accept": "application/json",
                            "X-Requested-With": "XMLHttpRequest"
                        }}
                    }});
                    return await resp.json();
                }} catch(e) {{
                    return {{"error": e.message}};
                }}
            }}
        ''')

        if not result or "data" not in result or "result" not in result.get("data", {}):
            return []

        trains = []
        for raw in result["data"]["result"]:
            train = parse_train_data(raw)
            if train:
                train["to_name"] = to_name
                trains.append(train)
        return trains

    except Exception as e:
        return []


def format_train(t):
    """Format a single train for display"""
    buy_status = "可预订" if t["can_buy"] == "Y" else "已售完"

    seats = []
    seat_fields = [
        ("商务座", "swz"), ("一等座", "ydz"), ("二等座", "edz"),
        ("软卧", "rw"), ("硬卧", "yw"), ("软座", "rz"),
        ("硬座", "yz"), ("无座", "wz"),
    ]
    for name, key in seat_fields:
        val = t.get(key, "--")
        if val and val != "--" and val != "" and val != "无":
            seats.append(f"{name}:{val}")

    seat_str = " | ".join(seats) if seats else "无余票信息"
    return (
        f"  {t['train_code']:>7s}  {t['depart_time']}->{t['arrive_time']}  "
        f"历时{t['duration']}  到{t['to_name']}  [{buy_status}]  {seat_str}"
    )


async def main():
    print("=" * 70)
    print(f"  12306 余票查询: {FROM_NAME} → 咸宁")
    print("=" * 70)

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        headless=False,
        channel="chrome",
        args=['--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        viewport={'width': 1280, 'height': 800},
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    page = await context.new_page()

    # Step 1: Visit 12306 to establish session/cookies
    print("\n[*] 正在访问12306建立会话...")
    await page.goto("https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc", wait_until="domcontentloaded", timeout=20000)
    await asyncio.sleep(3)
    print("[*] 会话已建立\n")

    all_results = {}

    for date in DATES:
        label = DATE_LABELS.get(date, date)
        print(f"\n{'='*70}")
        print(f"  查询日期: {label}")
        print(f"{'='*70}")

        date_trains = []
        for to_code, to_name in DESTINATIONS:
            trains = await query_tickets(page, date, FROM_STATION, to_code, to_name)
            if not trains:
                # Try alternative API endpoint
                trains = await query_with_alt_api(page, date, FROM_STATION, to_code, to_name)
            date_trains.extend(trains)
            await asyncio.sleep(0.5)  # Rate limiting

        if date_trains:
            # Sort by departure time
            date_trains.sort(key=lambda t: t["depart_time"])

            # Deduplicate by train_code (same train may appear for different dest stations)
            seen = set()
            unique_trains = []
            for t in date_trains:
                if t["train_code"] not in seen:
                    seen.add(t["train_code"])
                    unique_trains.append(t)

            # Count available
            available = [t for t in unique_trains if t["can_buy"] == "Y"]
            sold_out = [t for t in unique_trains if t["can_buy"] != "Y"]

            print(f"\n  共 {len(unique_trains)} 趟列车 | 可预订: {len(available)} | 已售完: {len(sold_out)}")
            print(f"  {'—'*65}")

            for t in unique_trains:
                print(format_train(t))

            all_results[date] = unique_trains
        else:
            print(f"\n  未查询到列车信息（可能该日期未开售或无直达列车）")
            all_results[date] = []

    # Summary
    print(f"\n\n{'='*70}")
    print("  查询结果汇总")
    print(f"{'='*70}")
    for date in DATES:
        label = DATE_LABELS.get(date, date)
        trains = all_results.get(date, [])
        available = [t for t in trains if t["can_buy"] == "Y"]
        print(f"  {label}: {len(trains)}趟列车, {len(available)}趟可预订")

    print(f"\n[*] 浏览器保持打开 8 秒...")
    await asyncio.sleep(8)
    await browser.close()
    await pw.stop()
    print("[*] 完成")


if __name__ == "__main__":
    asyncio.run(main())
