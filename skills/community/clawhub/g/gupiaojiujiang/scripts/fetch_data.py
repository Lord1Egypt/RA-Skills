#!/usr/bin/env python3
"""
独孤九剑 · 数据获取层
基于 akshare 获取 A 股所需全维度数据

数据维度：
  1. 日K线（OHLCV）— 主力战场
  2. 分钟K线 — 日内走势
  3. 资金流向 — 主力/散户资金
  4. 实时行情 — 盘口快照
  5. 股票基本信息
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Optional

import akshare as ak
import pandas as pd


# ── 工具函数 ───────────────────────────────────────────

def _clean_stock_code(code: str) -> str:
    """清洗股票代码，去除 sh/sz 前缀和多余字符"""
    return code.strip().replace("sh", "").replace("sz", "").replace(" ", "")


def _to_ak_code(code: str) -> str:
    """转换为 akshare 格式（如 600519 或 sz002594）"""
    code = _clean_stock_code(code)
    if code.startswith(("0", "3")):
        return f"sz{code}"
    elif code.startswith("6"):
        return f"sh{code}"
    elif code.startswith("8") or code.startswith("4"):
        return f"bj{code}"
    return code


def _safe_fetch(fn, name: str, **kwargs):
    """安全获取数据，捕获异常后优雅返回"""
    try:
        result = fn(**kwargs)
        if result is None or (isinstance(result, pd.DataFrame) and result.empty):
            return {"error": f"{name}: 返回空数据", "success": False}
        return {"data": result, "success": True}
    except Exception as e:
        return {"error": f"{name}: {str(e)}", "success": False}


# ── 核心数据获取 ────────────────────────────────────────

def fetch_daily_kline(code: str, days: int = 120) -> dict:
    """
    获取日K线数据
    返回: OHLCV + 换手率 + 涨跌幅
    """
    ak_code = _to_ak_code(code)
    raw_code = _clean_stock_code(code)
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=days + 30)).strftime("%Y%m%d")

    result = _safe_fetch(
        ak.stock_zh_a_hist,
        "日K线",
        symbol=raw_code,
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust="qfq",  # 前复权
    )

    if not result["success"]:
        return result

    df = result["data"]
    # 标准化列名
    col_map = {
        "日期": "date",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
        "成交额": "amount",
        "换手率": "turnover",
        "涨跌幅": "pct_change",
    }
    df = df.rename(columns=col_map)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").tail(days).reset_index(drop=True)

    # 确保数值类型
    for col in ["open", "close", "high", "low", "volume", "amount", "turnover", "pct_change"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return {"data": df, "success": True, "source": "akshare:stock_zh_a_hist"}


def fetch_minute_kline(code: str, period: str = "5") -> dict:
    """
    获取分钟K线数据
    period: "1"/"5"/"15"/"30"/"60"
    """
    ak_code = _to_ak_code(code)
    raw_code = _clean_stock_code(code)

    result = _safe_fetch(
        ak.stock_zh_a_hist,
        "分钟K线",
        symbol=raw_code,
        period=period,
        adjust="qfq",
    )

    if not result["success"]:
        return result

    df = result["data"]
    col_map = {
        "日期": "datetime",
        "开盘": "open",
        "收盘": "close",
        "最高": "high",
        "最低": "low",
        "成交量": "volume",
    }
    df = df.rename(columns=col_map)
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
    df = df.sort_values("datetime").reset_index(drop=True)

    return {"data": df, "success": True, "source": f"akshare:stock_zh_a_hist:{period}min"}


def fetch_fund_flow(code: str, days: int = 30) -> dict:
    """
    获取个股资金流向（主力/超大单/大单/中单/小单）
    """
    raw_code = _clean_stock_code(code)

    result = _safe_fetch(
        ak.stock_individual_fund_flow,
        "资金流向",
        stock=raw_code,
        market="sh" if raw_code.startswith("6") else "sz",
    )

    if not result["success"]:
        return result

    df = result["data"]
    if not df.empty:
        date_col = df.columns[0]
        df = df.rename(columns={date_col: "date"})
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").tail(days).reset_index(drop=True)

    return {"data": df, "success": True, "source": "akshare:stock_individual_fund_flow"}


def fetch_real_time_quote(code: str) -> dict:
    """
    获取实时行情快照（最新价、量比、换手、涨速等）
    """
    raw_code = _clean_stock_code(code)
    market = "sh" if raw_code.startswith("6") else "sz"

    try:
        # 尝试获取实时行情
        df = ak.stock_zh_a_spot_em()
        df = df[df["代码"] == raw_code]
        if df.empty:
            return {"error": "未找到该股票实时行情", "success": False}

        row = df.iloc[0].to_dict()

        # 标准化字段
        quote = {
            "code": row.get("代码", raw_code),
            "name": row.get("名称", ""),
            "price": float(row.get("最新价", 0)),
            "change_pct": float(row.get("涨跌幅", 0)),
            "change_amount": float(row.get("涨跌额", 0)),
            "volume_ratio": float(row.get("量比", 0)),
            "turnover_rate": float(row.get("换手率", 0)),
            "volume": float(row.get("成交量", 0)),
            "amount": float(row.get("成交额", 0)),
            "high": float(row.get("最高", 0)),
            "low": float(row.get("最低", 0)),
            "open": float(row.get("今开", 0)),
            "pre_close": float(row.get("昨收", 0)),
            "pe": float(row.get("市盈率-动态", 0) or 0),
            "total_market_cap": float(row.get("总市值", 0) or 0),
        }
        return {"data": quote, "success": True, "source": "akshare:stock_zh_a_spot_em"}

    except Exception as e:
        return {"error": f"实时行情: {str(e)}", "success": False}


def fetch_stock_info(code: str) -> dict:
    """获取股票基本信息"""
    raw_code = _clean_stock_code(code)
    try:
        df = ak.stock_individual_info_em(symbol=raw_code)
        info = {}
        for _, row in df.iterrows():
            info[row["item"]] = row["value"]
        return {"data": info, "success": True}
    except Exception as e:
        return {"error": f"股票信息: {str(e)}", "success": False}


# ── 一站式获取 ──────────────────────────────────────────

def fetch_all(code: str, days: int = 120, include_intraday: bool = True) -> dict:
    """
    一站式获取全部数据

    Args:
        code: 股票代码，如 600519
        days: 日线回溯天数
        include_intraday: 是否包含分钟数据

    Returns:
        {
            "success": True/False,
            "code": "600519",
            "name": "贵州茅台",
            "daily_kline": DataFrame,
            "minute_60": DataFrame (optional),
            "fund_flow": DataFrame,
            "realtime": dict,
            "stock_info": dict,
            "fetched_at": "2024-01-01 12:00:00",
            "errors": [...]
        }
    """
    code = _clean_stock_code(code)
    errors = []

    # 并行获取（顺序执行，akshare 不支持并发）
    kline = fetch_daily_kline(code, days)
    if not kline["success"]:
        errors.append(kline.get("error", "日K线获取失败"))

    fund = fetch_fund_flow(code, days=30)
    if not fund["success"]:
        errors.append(fund.get("error", "资金流向获取失败"))

    realtime = fetch_real_time_quote(code)
    if not realtime["success"]:
        errors.append(realtime.get("error", "实时行情获取失败"))

    info = fetch_stock_info(code)
    stock_name = ""
    if info["success"]:
        stock_name = info["data"].get("股票简称", "")

    result = {
        "success": kline["success"],
        "code": code,
        "name": stock_name or realtime.get("data", {}).get("name", ""),
        "daily_kline": kline.get("data") if kline["success"] else None,
        "fund_flow": fund.get("data") if fund["success"] else None,
        "realtime": realtime.get("data") if realtime["success"] else None,
        "stock_info": info.get("data") if info["success"] else None,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "errors": errors if errors else None,
    }

    # 分钟线（可选的，较大数据量）
    if include_intraday and kline["success"]:
        m60 = fetch_minute_kline(code, "60")
        if m60["success"]:
            result["minute_60"] = m60["data"]
        else:
            errors.append(m60.get("error", "60分钟线获取失败"))

    return result


# ── CLI 入口 ────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fetch_data.py <股票代码> [回溯天数] [--json]")
        print("示例: python fetch_data.py 600519 120 --json")
        sys.exit(1)

    code = sys.argv[1]
    days = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    as_json = "--json" in sys.argv

    data = fetch_all(code, days)

    if as_json:
        # 将 DataFrame 转为可序列化的格式
        output = {k: v for k, v in data.items() if k not in ("daily_kline", "minute_60", "fund_flow")}
        if data.get("daily_kline") is not None:
            output["daily_kline"] = data["daily_kline"].to_dict("records")
        if data.get("minute_60") is not None:
            output["minute_60"] = data["minute_60"].to_dict("records")[-240:]  # 最近240条（约20个交易日）
        if data.get("fund_flow") is not None:
            output["fund_flow"] = data["fund_flow"].to_dict("records")
        print(json.dumps(output, ensure_ascii=False, indent=2, default=str))
    else:
        print(f"✅ 股票: {data['name']}({data['code']})")
        print(f"📅 获取时间: {data['fetched_at']}")
        if data.get("daily_kline") is not None:
            print(f"📊 日K线: {len(data['daily_kline'])} 条")
        if data.get("minute_60") is not None:
            print(f"⏱️ 60分钟线: {len(data['minute_60'])} 条")
        if data.get("fund_flow") is not None:
            print(f"💰 资金流向: {len(data['fund_flow'])} 条")
        if data.get("errors"):
            for e in data["errors"]:
                print(f"⚠️ {e}")
        # 打印最近5日K线概要
        if data.get("daily_kline") is not None:
            print("\n📈 最近5日K线:")
            print(data["daily_kline"][["date", "open", "close", "high", "low", "volume", "turnover"]].tail(5).to_string(index=False))
