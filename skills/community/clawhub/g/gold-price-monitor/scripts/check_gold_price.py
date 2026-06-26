#!/usr/bin/env python3
"""
黄金积存金价格监控脚本
- 从中国建设银行获取积存金实时报价（人民币/克）
- 记录每天北京时间9点开盘价
- 与上次记录对比，判断是否需要通知
- 用于 OpenClaw 定时调用，辅助买入/卖出决策
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from pathlib import Path
import xml.etree.ElementTree as ET
import ssl

# ==================== 配置 ====================
ALERT_THRESHOLD = 10  # 人民币/克，价格差超过此值触发警报
BEIJING_TZ = timezone(timedelta(hours=8))

# 数据文件路径
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
HISTORY_FILE = DATA_DIR / "price_history.json"
DAILY_OPEN_FILE = DATA_DIR / "daily_open.json"

# 建设银行积存金行情 XML 接口（无需 API Key）
CCB_GOLD_URL = "https://www2.ccb.com/cn/home/news/gjshjjc01.xml"


def _create_ssl_context() -> ssl.SSLContext:
    """创建兼容建设银行服务器的 SSL 上下文"""
    ctx = ssl.create_default_context()
    ctx.options |= ssl.OP_LEGACY_SERVER_CONNECT
    return ctx


def fetch_ccb_gold_price() -> dict:
    """从新浪财经获取上海金交所 Au99.99 报价（作为建行积存金平替）"""
    ssl_ctx = _create_ssl_context()
    import time
    url = f"http://hq.sinajs.cn/rn={int(time.time()*1000)}&list=gds_AU9999"
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://finance.sina.com.cn/",
    })
    
    with urlopen(req, timeout=15, context=ssl_ctx) as resp:
        data = resp.read().decode("gbk")

    if '="' not in data:
        raise ValueError("新浪财经数据格式异常: " + data)

    content = data.split('="')[1].split('";')[0]
    parts = content.split(',')

    if len(parts) < 13:
        raise ValueError(f"价格数据异常: 字段数量不足 ({len(parts)})")

    current_price = float(parts[0])
    # 新浪接口中：
    # parts[2] 是买一价(Bid)，代表买家的最高出价，是客户能够卖出（套现）的价格 (Customer Sell Price)
    # parts[3] 是卖一价(Ask)，代表卖家的最低要价，是客户能够买入（建仓）的价格 (Customer Buy Price)
    buy_price = float(parts[3]) if float(parts[3]) > 0 else current_price
    sell_price = float(parts[2]) if float(parts[2]) > 0 else current_price
    update_time = f"{parts[12]} {parts[6]}" # 例如: 2026-03-25 23:22:39

    return {
        "buy_price": buy_price,
        "sell_price": sell_price,
        "mid_price": current_price,
        "update_time": update_time,
    }


# ==================== 开盘价管理 ====================

def load_daily_open() -> dict:
    """加载每日开盘价记录 {日期字符串: {buy_price, sell_price, timestamp}}"""
    if DAILY_OPEN_FILE.exists():
        try:
            with open(DAILY_OPEN_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_daily_open(data: dict):
    """保存每日开盘价记录"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DAILY_OPEN_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_daily_open(buy_price: float, sell_price: float, now: datetime) -> dict | None:
    """
    检查并更新今日开盘价。
    规则：每天北京时间 9:00 之后的第一次调用记录为当日开盘价。
    返回今日开盘价记录，如果还未到开盘时间则返回 None。
    """
    beijing_now = now.astimezone(BEIJING_TZ)
    today_str = beijing_now.strftime("%Y-%m-%d")
    daily_open = load_daily_open()

    # 如果今天已经有开盘价，直接返回
    if today_str in daily_open:
        return daily_open[today_str]

    # 如果还没到 9:00，不记录开盘价
    if beijing_now.hour < 9:
        return None

    # 北京时间 9:00 之后的首次调用，记录为今日开盘价
    open_record = {
        "buy_price": buy_price,
        "sell_price": sell_price,
        "timestamp": now.isoformat(),
    }
    daily_open[today_str] = open_record

    # 只保留最近 30 天的开盘价
    if len(daily_open) > 30:
        sorted_dates = sorted(daily_open.keys())
        for old_date in sorted_dates[:-30]:
            del daily_open[old_date]

    save_daily_open(daily_open)
    return open_record


# ==================== 历史记录管理 ====================

def load_history() -> list:
    if HISTORY_FILE.exists():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_history(history: list):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_last_record(history: list) -> dict | None:
    if history:
        return history[-1]
    return None


# ==================== 主逻辑 ====================

def main():
    try:
        # 1. 获取建设银行积存金报价
        price_data = fetch_ccb_gold_price()
        buy_price = price_data["buy_price"]
        sell_price = price_data["sell_price"]
        mid_price = price_data["mid_price"]
        bank_update_time = price_data["update_time"]

        # 2. 处理每日开盘价
        now = datetime.now(timezone.utc).astimezone()
        timestamp = now.isoformat()
        today_open = update_daily_open(buy_price, sell_price, now)

        # 开盘价信息
        if today_open is not None:
            open_buy = today_open["buy_price"]
            open_sell = today_open["sell_price"]
            day_change = round(buy_price - open_buy, 2)
            day_change_sign = "+" if day_change >= 0 else ""
            day_change_pct = f"{(day_change / open_buy * 100):.2f}%" if open_buy else "N/A"
        else:
            open_buy = None
            open_sell = None
            day_change = None
            day_change_pct = None

        # 3. 加载历史记录，对比上次价格
        history = load_history()
        last_record = get_last_record(history)

        if last_record is not None:
            last_buy = last_record["buy_price"]
            last_sell = last_record["sell_price"]
            last_time = last_record.get("bank_update_time", "")
            
            is_new_update = (bank_update_time != last_time)

            buy_change = round(buy_price - last_buy, 2)
            sell_change = round(sell_price - last_sell, 2)
            buy_change_pct = f"{(buy_change / last_buy * 100):.2f}%"
            sell_change_pct = f"{(sell_change / last_sell * 100):.2f}%"
            alert = is_new_update and (abs(buy_change) >= ALERT_THRESHOLD)
            change_sign = "+" if buy_change >= 0 else ""

            if not is_new_update:
                suggestion = "⏳ 银行报价未更新"
            elif buy_change <= -ALERT_THRESHOLD:
                suggestion = "📉 价格大幅下跌，可考虑买入"
            elif buy_change >= ALERT_THRESHOLD:
                suggestion = "📈 价格大幅上涨，可考虑卖出"
            else:
                suggestion = "➡️ 价格波动不大，建议观望"

            msg_lines = [
                "上金所Au99.99报价(新浪平替)",
                f"  买入价: ¥{buy_price:.2f}/克（{change_sign}{buy_change:.2f}）",
                f"  卖出价: ¥{sell_price:.2f}/克（{'+' if sell_change >= 0 else ''}{sell_change:.2f}）",
                f"  中间价: ¥{mid_price:.2f}/克",
                f"  上次买入价: ¥{last_buy:.2f}/克",
            ]
            if open_buy is not None:
                msg_lines.append(f"  今日开盘价: ¥{open_buy:.2f}/克（日内{day_change_sign}{day_change:.2f}, {day_change_sign}{day_change_pct}）")
            msg_lines.append(f"  建议: {suggestion}")
            message = "\n".join(msg_lines)
        else:
            is_new_update = True
            buy_change = 0
            sell_change = 0
            buy_change_pct = "N/A"
            sell_change_pct = "N/A"
            alert = False
            suggestion = "📝 首次记录，暂无对比数据"
            msg_lines = [
                "上金所Au99.99报价(新浪平替)（首次记录）",
                f"  买入价: ¥{buy_price:.2f}/克",
                f"  卖出价: ¥{sell_price:.2f}/克",
                f"  中间价: ¥{mid_price:.2f}/克",
            ]
            if open_buy is not None:
                msg_lines.append(f"  今日开盘价: ¥{open_buy:.2f}/克")
            message = "\n".join(msg_lines)
            last_buy = None
            last_sell = None

        # 4. 追加记录到历史 (只保存作为下次对比基准的记录，即首次记录或触发警报时)
        if is_new_update and (alert or not history):
            record = {
                "timestamp": timestamp,
                "buy_price": buy_price,
                "sell_price": sell_price,
                "mid_price": mid_price,
                "bank_update_time": bank_update_time,
            }
            history.append(record)
            if len(history) > 1000:
                history = history[-1000:]
            save_history(history)

        # 5. 输出结果
        result = {
            "status": "success",
            "source": "上海金交所Au99.99",
            "buy_price": buy_price,
            "sell_price": sell_price,
            "mid_price": mid_price,
            "last_buy_price": last_buy if last_record else None,
            "last_sell_price": last_sell if last_record else None,
            "buy_change": buy_change,
            "sell_change": sell_change,
            "buy_change_pct": buy_change_pct,
            "sell_change_pct": sell_change_pct,
            "today_open_buy": open_buy,
            "today_open_sell": open_sell,
            "day_change": day_change,
            "day_change_pct": day_change_pct,
            "alert": alert,
            "alert_threshold": ALERT_THRESHOLD,
            "suggestion": suggestion,
            "message": message,
            "bank_update_time": bank_update_time,
            "timestamp": timestamp,
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        error_result = {
            "status": "error",
            "message": f"获取积存金价格失败: {str(e)}",
            "alert": False,
            "timestamp": datetime.now(timezone.utc).astimezone().isoformat(),
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
