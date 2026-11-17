#!/usr/bin/env python3
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""
贵金属历史走势/K线查询脚本（京东金融公开接口，免 OAuth 登录）

功能：
- chart: 查询近 N 天走势，输出纯文字走势描述（本项目黄金场景主用）
- kline: 查询 K 线数据（日/周/月），输出原始 JSON
- quote: 查询实时行情（黄金实时行情建议优先用 jdjr_query_gold.py）
- intraday: 查询分时走势

本项目黄金定位：仅面向贵金属（SGE 前缀），常用代码：
- SGE-Au99.99  黄金
- SGE-Ag99.99  白银
- SGE-Pt99.95  铂金

用法（黄金历史走势）：
    python3 jdjr_query_stock.py chart SGE-Au99.99 --days 15
    python3 jdjr_query_stock.py kline SGE-Au99.99 --k-type day

注：脚本正则同时兼容股票代码（SZ/SH/HK/US），但本项目仅对客暴露贵金属走势。
"""
import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from typing import Optional

from jdjr_config import get_source_attribution, get_source_metadata, get_claw_headers, set_claw


# ============ 全局常量 ============

# 京东金融 API 基础地址
BASE_URL = "https://ms.jr.jd.com/gw2/generic/ugActs/h5/m"

# 股票代码正则：支持 SZ-000001、SH-600519、SGE-Au99.99 等格式
STOCK_CODE_PATTERN = re.compile(r"^(SZ|SH|HK|US|SGE)-[A-Za-z0-9._()-]+$")


# ============ 核心函数 ============

def post_json(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{BASE_URL}/{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **get_claw_headers()},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build_payload(stock_code: str, k_type: Optional[str] = None) -> dict:
    payload = {"paramMap": {"stockCode": stock_code}}
    if k_type:
        payload["paramMap"]["kType"] = k_type
    return payload


def print_chart(data: list, stock_name: str, days: int):
    """
    打印纯文字走势描述（适用于 chart 命令）。
    
    参数:
        data: K 线数据列表，每项包含 date/open/high/low/close/volume
        stock_name: 股票名称，用于标题显示
        days: 显示的天数
    
    输出:
        纯文字走势说明
    
    描述规则:
        - 列出最高点/最低点及日期
        - 描述整体趋势
        - 标注关键转折点
    """
    if not data:
        print("无数据")
        return
    
    # 只取最近 days 天的数据
    data = data[-days:]
    
    # 计算关键数据
    closes = [float(d['close']) for d in data]
    opens = [float(d['open']) for d in data]
    highs = [float(d['high']) for d in data]
    lows = [float(d['low']) for d in data]
    
    first_close = closes[0]
    last_close = closes[-1]
    max_price = max(closes)
    min_price = min(closes)
    max_date = data[closes.index(max_price)]['date'][5:]  # MM-DD
    min_date = data[closes.index(min_price)]['date'][5:]
    
    # 计算涨跌
    change = last_close - first_close
    change_pct = (change / first_close) * 100
    
    # 判断整体趋势
    if change_pct > 5:
        trend = "📈 上涨趋势"
    elif change_pct < -5:
        trend = "📉 下跌趋势"
    else:
        trend = "➡️ 震荡整理"
    
    # 找出上涨/下跌天数
    up_days = sum(1 for c, o in zip(closes[1:], opens[1:]) if c > o)
    down_days = len(data) - 1 - up_days
    
    print(f"\n{stock_name} 近{days}天走势（{data[0]['date'][5:]} ~ {data[-1]['date'][5:]}）")
    print(f"\n{trend}\n")
    print(f"- 起始价: {first_close:.2f} 元 → 收盘价: {last_close:.2f} 元")
    print(f"- 累计涨跌: {'+' if change > 0 else ''}{change:.2f} 元 ({'+' if change_pct > 0 else ''}{change_pct:.2f}%)")
    print(f"- 最高: {max_price:.2f} 元 ({max_date})")
    print(f"- 最低: {min_price:.2f} 元 ({min_date})")
    print(f"- 涨跌天数: {up_days} 涨 / {down_days} 跌")
    print(f"- 波动幅度: {max_price - min_price:.2f} 元 ({(max_price - min_price) / min_price * 100:.1f}%)")
    print(f"\n{get_source_attribution('STOCK')}")


def main() -> int:
    """
    主函数：解析命令行参数、调用 API、输出结果。
    
    命令行参数:
        action: quote | intraday | kline | chart
        stock_code: 股票代码
        --k-type: K 线类型（kline 命令必需）
        --days: 图表显示天数（chart 命令，默认 15）
    
    返回:
        0 表示成功，1 表示失败
    """
    parser = argparse.ArgumentParser(description="查询股票行情、分时或 K 线")
    parser.add_argument("action", choices=["quote", "intraday", "kline", "chart"])
    parser.add_argument("stock_code")
    parser.add_argument("--k-type", choices=["day", "week", "month"])
    parser.add_argument("--days", type=int, default=15, help="chart 模式显示的天数")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args()
    set_claw(args.claw)

    # 校验股票代码格式
    if not STOCK_CODE_PATTERN.match(args.stock_code):
        print(json.dumps({"success": False, "error": "股票代码格式不正确，请使用类似 SZ-000001、SH-600519 的格式"}, ensure_ascii=False))
        return 1

    # 根据 action 调用不同 API
    try:
        if args.action in {"quote", "intraday"}:
            # quote/intraday 都用 queryStockData，返回实时行情 + 分时数据
            result = post_json("queryStockData", build_payload(args.stock_code))
        elif args.action == "chart":
            # chart 用 queryStockKLine 获取日K，再绘制图表
            result = post_json("queryStockKLine", build_payload(args.stock_code, "day"))
        else:
            # kline 需要指定 k-type
            if not args.k_type:
                parser.error("action 为 kline 时必须传 --k-type")
            result = post_json("queryStockKLine", build_payload(args.stock_code, args.k_type))
    except urllib.error.HTTPError as exc:
        if exc.code == 403:
            print(json.dumps({"success": False, "error": "您的账户已被限制访问，如有疑问请联系京东黄金客服"}, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": f"HTTP {exc.code}"}, ensure_ascii=False))
        return 1
    except urllib.error.URLError as exc:
        print(json.dumps({"success": False, "error": f"网络请求失败: {exc.reason}"}, ensure_ascii=False))
        return 1
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}, ensure_ascii=False))
        return 1

    # 检查 API 响应是否成功
    if not result.get("success") or result.get("resultCode") != 0:
        print(json.dumps({"success": False, "code": result.get("resultCode"), "msg": result.get("resultMsg"), "data": result.get("resultData")}, ensure_ascii=False))
        return 1

    # 提取数据并输出
    result_data = result.get("resultData") or {}
    data = result_data.get("data") or {}
    
    if args.action == "chart":
        # chart 特殊处理：调用 print_chart 绘制 ASCII 图
        kline_data = data.get("kLineDtoList") or []
        stock_name = data.get("stockName", args.stock_code)
        print_chart(kline_data, stock_name, args.days)
    else:
        # quote/intraday/kline 输出原始 JSON（供 agent 后续格式化）
        print(json.dumps({"success": True, "data": data, "source": get_source_metadata("STOCK")}, ensure_ascii=False, indent=2))
    return 0


# 脚本入口
if __name__ == "__main__":
    sys.exit(main())
