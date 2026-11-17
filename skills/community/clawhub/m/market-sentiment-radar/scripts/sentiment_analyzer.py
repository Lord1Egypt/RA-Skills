#!/usr/bin/env python3
"""v1.3.1: read-only, dated observations. Never substitute mock market data."""
import argparse
import json
import math
import subprocess
import sys
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

VERSION = "1.3.2"
TZ = ZoneInfo("Asia/Shanghai")
INDICES = {"000001": "上证指数", "399001": "深证成指", "399006": "创业板指"}
MISSING = ["全市场涨跌家数", "两市总成交额及同口径比较", "涨跌停家数及连板高度",
           "板块资金流与多日轮动", "北向资金净流入", "跨市场与宏观新闻"]


def finite(value):
    if isinstance(value, bool):
        raise ValueError("boolean is not a market value")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError("non-finite market value")
    return value


def select_day(calendar, requested, now):
    days = sorted({date.fromisoformat(str(x)[:10]) for x in calendar})
    # No estimate from weekdays. Calendar coverage is required even for history.
    if not days or max(days) < now.date():
        raise ValueError("交易日历覆盖不足，无法核验日期")
    completed = [d for d in days if d < now.date() or
                 (d == now.date() and now.time() >= time(16, 0))]
    if requested:
        target = date.fromisoformat(requested)
        if target not in completed:
            raise ValueError("请求日期不是已完成的交易日（当日日线需16:00后）")
        return target
    if not completed:
        raise ValueError("没有可核验的已完成交易日")
    return completed[-1]


def observation(rows, symbol, target, source):
    # Enforce exact requested date, order, uniqueness, finite values and prior close.
    dated = {}
    for row in rows:
        day = date.fromisoformat(str(row["date"])[:10])
        if day in dated:
            raise ValueError("duplicate data date")
        dated[day] = row
    if target not in dated:
        raise ValueError("来源缺少目标交易日，拒绝以旧行情替代")
    prior = [d for d in dated if d < target]
    if not prior:
        raise ValueError("缺少前一交易日收盘价")
    close = finite(dated[target]["close"])
    previous = finite(dated[max(prior)]["close"])
    if close <= 0 or previous <= 0:
        raise ValueError("invalid close")
    return {"symbol": symbol, "name": INDICES[symbol], "trade_date": target.isoformat(),
            "close": close, "change_pct": round((close / previous - 1) * 100, 4),
            "unit": "指数点；涨跌幅为百分比", "source": source,
            "kind": "已完成交易日日线；非实时行情"}


def collect(api, requested=None, now=None):
    now = now or datetime.now(TZ)
    result = {"version": VERSION, "status": "unavailable", "collected_at": now.isoformat(),
              "requested_date": requested, "trade_date": None, "indices": [], "errors": [],
              "missing": list(MISSING), "sentiment": "证据不足，无法判断", "score": None,
              "confidence": None, "position_suggestion": None}
    try:
        calendar = api.tool_trade_date_hist_sina()
        target = select_day(calendar["trade_date"].tolist(), requested, now)
        result["trade_date"] = target.isoformat()
    except Exception as exc:
        result["errors"].append("交易日历/日期校验失败: " + type(exc).__name__ +
                                "；请检查日期是否已收盘、日历覆盖与网络")
        return result
    for symbol in INDICES:
        attempts = []
        # Sina daily index history is the first source because it is the
        # low-latency path verified on this host. Eastmoney remains a fallback.
        # The outer process timeout still protects against a provider outage.
        for provider in ("sina", "eastmoney"):
            try:
                if provider == "eastmoney":
                    df = api.index_zh_a_hist(symbol=symbol, period="daily",
                        start_date=(target - timedelta(days=60)).strftime("%Y%m%d"),
                        end_date=target.strftime("%Y%m%d"))
                    rows = df.rename(columns={"日期": "date", "收盘": "close"}).to_dict("records")
                    source = "AKShare/index_zh_a_hist · 东方财富 · https://quote.eastmoney.com/"
                else:
                    code = ("sh" if symbol == "000001" else "sz") + symbol
                    rows = api.stock_zh_index_daily(symbol=code).to_dict("records")
                    source = "AKShare/stock_zh_index_daily · 新浪财经 · https://finance.sina.com.cn/"
                item = observation(rows, symbol, target, source)
                # A valid but incomplete history must not mislabel multi-day change as daily change.
                prior_days = sorted(d for d in calendar["trade_date"].astype(str).str[:10].tolist()
                                    if d < target.isoformat())
                row_days = sorted(str(r["date"])[:10] for r in rows if str(r["date"])[:10] < target.isoformat())
                if not prior_days or not row_days or row_days[-1] != prior_days[-1]:
                    raise ValueError("前一交易日日线缺失")
                result["indices"].append(item)
                break
            except Exception as exc:
                # Do not leak request URLs, proxy credentials or full exceptions.
                attempts.append(provider + ": " + type(exc).__name__)
        else:
            result["errors"].append(INDICES[symbol] + "获取/校验失败 (" + ", ".join(attempts) + ")")
    if result["indices"]:
        result["status"] = "partial"
    return result


def render(result):
    lines = ["📡 市场环境体检｜真实数据参考（覆盖不完整）",
             "交易日：" + str(result.get("trade_date") or "不可用"),
             "采集时间：" + result["collected_at"],
             "口径：已完成交易日日线，不是盘中异动信号。"]
    for item in result["indices"]:
        lines += [f"• {item['name']}：{item['close']:.2f} 点 | {item['change_pct']:+.2f}%",
                  "  来源：" + item["source"] + "；数据日期：" + item["trade_date"]]
    if not result["indices"]:
        lines.append("行情不可用；未生成行情结论。")
    lines += ["缺失/未接入：" + "、".join(result["missing"]),
              "情绪周期：证据不足，无法判断；不评分、不生成仓位建议。"]
    if result["errors"]:
        lines.append("异常：" + "；".join(result["errors"]))
    lines.append("仅供学习与信息参考，不构成投资建议。")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="已完成交易日 YYYY-MM-DD")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--force-akshare", action="store_true", help="兼容旧参数；始终只使用真实来源")
    parser.add_argument("--timeout", type=int, default=90, help="整个采集进程超时秒数（1-180）")
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.date:
        try:
            if date.fromisoformat(args.date).isoformat() != args.date:
                raise ValueError()
        except ValueError:
            parser.error("--date 必须为 YYYY-MM-DD")
    if not 1 <= args.timeout <= 180:
        parser.error("--timeout 必须在 1-180 秒之间")
    if args.worker:
        try:
            import akshare as ak
            result = collect(ak, args.date)
        except ImportError:
            result = failure("缺少 AKShare；请在你选择的 Python 环境中安装，不自动安装依赖。")
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
        return 0
    command = [sys.executable, str(Path(__file__).resolve()), "--worker"]
    if args.date:
        command += ["--date", args.date]
    try:
        child = subprocess.run(command, capture_output=True, text=True, timeout=args.timeout)
        if child.returncode:
            result = failure("采集进程失败；未生成行情结论")
        else:
            result = json.loads(child.stdout)
    except subprocess.TimeoutExpired:
        result = failure("真实数据采集超时；未使用默认值或模拟数据")
    except (ValueError, OSError):
        result = failure("采集结果无效；未生成行情结论")
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) if args.json else render(result))
    return 0 if result["indices"] else 2


def failure(reason):
    return {"version": VERSION, "status": "unavailable", "collected_at": datetime.now(TZ).isoformat(),
            "trade_date": None, "indices": [], "errors": [reason], "missing": list(MISSING),
            "sentiment": "证据不足，无法判断", "score": None, "confidence": None,
            "position_suggestion": None}


if __name__ == "__main__":
    sys.exit(main())
