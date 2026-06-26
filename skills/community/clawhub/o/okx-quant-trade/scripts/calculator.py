"""
OKX 量化交易指标计算器
通过 OKX v5 公共 API 获取 K线数据，计算 RSI、EMA、乖离率、布林带等技术指标。
支持单周期和多周期批量计算，提供 JSON 和人类可读两种输出格式。
"""

import argparse
import json
import sys
import requests
import pandas as pd
from datetime import datetime

# ========== OKX API 数据层 ==========

# OKX API 接受的合法 bar 值映射（大小写兼容）
BAR_MAP = {
    "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m", "30m": "30m",
    "1h": "1H", "1H": "1H",
    "2h": "2H", "2H": "2H",
    "4h": "4H", "4H": "4H",
    "6h": "6H", "6H": "6H",
    "12h": "12H", "12H": "12H",
    "1d": "1D", "1D": "1D",
    "1w": "1W", "1W": "1W",
}

# K线 API 返回的标准列名
KLINE_COLUMNS = ["ts", "o", "h", "l", "c", "vol", "volCcy", "volCcyQuote", "confirm"]


def get_kline_data(inst_id: str, bar: str = "1H", limit: int = 100) -> pd.DataFrame:
    """
    通过 OKX v5 公共 API 获取 K线 数据。
    参数:
        inst_id: 交易标的，例如 BTC-USDT
        bar: K线周期，支持 1m/5m/15m/1H/4H/1D 等
        limit: 获取数据条数上限（OKX 最大 300）
    返回:
        包含 OHLCV 数据的 DataFrame，按时间升序排列；失败时返回空 DataFrame
    """
    url = "https://www.okx.com/api/v5/market/candles"
    api_bar = BAR_MAP.get(bar, bar)  # 尝试映射，若无匹配则原样传递

    params = {
        "instId": inst_id,
        "bar": api_bar,
        "limit": str(min(limit, 300))  # OKX 单次最多 300 条
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        body = resp.json()

        if body.get("code") != "0":
            raise ValueError(f"OKX API 错误 [{body.get('code')}]: {body.get('msg', '未知错误')}")

        if not body.get("data"):
            raise ValueError("OKX API 返回数据为空")

        df = pd.DataFrame(body["data"], columns=KLINE_COLUMNS)

        # 类型转换
        for col in ["o", "h", "l", "c", "vol"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["ts"] = pd.to_datetime(pd.to_numeric(df["ts"], errors="coerce"), unit="ms")
        df.sort_values("ts", inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"网络请求失败: {e}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"数据解析失败: {e}")


# ========== 指标计算层 ==========

def calculate_ema(series: pd.Series, window: int) -> pd.Series:
    """计算指数移动平均线 (EMA)"""
    return series.ewm(span=window, adjust=False).mean()


def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    """
    计算 RSI (相对强弱指数)
    使用 Wilder 平滑法（即 EWM alpha=1/window）
    """
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta.where(delta < 0, 0.0))

    # 使用 Wilder 平滑（等价于 com=window-1）
    avg_gain = gain.ewm(com=window - 1, min_periods=window).mean()
    avg_loss = loss.ewm(com=window - 1, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def calculate_bias(series: pd.Series, window: int = 10) -> pd.Series:
    """计算乖离率 (Bias) = (收盘价 - MA) / MA * 100"""
    ma = series.rolling(window=window, min_periods=window).mean()
    return (series - ma) / ma * 100.0


def calculate_bollinger_bands(series: pd.Series, window: int = 20, num_std: float = 2.0) -> dict:
    """
    计算布林带 (Bollinger Bands)
    返回: {"bb_mid": Series, "bb_upper": Series, "bb_lower": Series}
    """
    mid = series.rolling(window=window, min_periods=window).mean()
    std = series.rolling(window=window, min_periods=window).std()
    return {
        "bb_mid": mid,
        "bb_upper": mid + std * num_std,
        "bb_lower": mid - std * num_std,
    }


def compute_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    对传入的 OHLCV DataFrame 执行全量指标计算。
    会在 df 上新增以下列:
      ema_5, ema_10, ema_20, rsi, bias_10, bb_mid, bb_upper, bb_lower
    """
    close = df["c"]

    # EMA 5 / 10 / 20
    df["ema_5"] = calculate_ema(close, 5)
    df["ema_10"] = calculate_ema(close, 10)
    df["ema_20"] = calculate_ema(close, 20)

    # RSI 14
    df["rsi"] = calculate_rsi(close, 14)

    # 乖离率 (基于 10 周期均线)
    df["bias_10"] = calculate_bias(close, 10)

    # 布林带 (20 周期，2 倍标准差)
    bb = calculate_bollinger_bands(close, 20, 2.0)
    df["bb_mid"] = bb["bb_mid"]
    df["bb_upper"] = bb["bb_upper"]
    df["bb_lower"] = bb["bb_lower"]

    return df


# ========== 输出层 ==========

# 标准输出列顺序
OUTPUT_COLUMNS = ["ts", "o", "h", "l", "c", "ema_5", "ema_10", "ema_20", "rsi", "bias_10", "bb_mid", "bb_upper", "bb_lower"]

# 数值精度控制
ROUND_RULES = {
    "o": 4, "h": 4, "l": 4, "c": 4,
    "ema_5": 4, "ema_10": 4, "ema_20": 4,
    "rsi": 2, "bias_10": 4,
    "bb_mid": 4, "bb_upper": 4, "bb_lower": 4,
}


def format_output(df: pd.DataFrame, inst_id: str, bar: str, profile: str, tail_n: int = 5) -> dict:
    """
    将计算完成的 DataFrame 格式化为标准结构化字典。
    仅保留最近 tail_n 条已确认闭合的 K线 数据。
    """
    # 筛选已确认闭合的 K线（confirm == "1"），若无确认标记列则取全部
    if "confirm" in df.columns:
        confirmed = df[df["confirm"] == "1"].copy()
        if confirmed.empty:
            confirmed = df.copy()  # 降级：全部使用
    else:
        confirmed = df.copy()

    recent = confirmed.tail(tail_n).copy()
    recent_rounded = recent[OUTPUT_COLUMNS].copy()

    # 对浮点列四舍五入
    for col, decimals in ROUND_RULES.items():
        if col in recent_rounded.columns:
            recent_rounded[col] = recent_rounded[col].round(decimals)

    # 时间列转字符串
    recent_rounded["ts"] = recent_rounded["ts"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "instId": inst_id,
        "bar": bar,
        "profile": profile,
        "count": len(recent_rounded),
        "data": recent_rounded.to_dict(orient="records"),
    }


# ========== 核心处理入口 ==========

def process_single(inst_id: str, bar: str, limit: int, profile: str) -> dict:
    """
    处理单个周期的数据获取和指标计算。
    返回格式化后的结果字典。失败时返回包含 error 字段的字典。
    """
    try:
        df = get_kline_data(inst_id, bar, limit)
        df = compute_all_indicators(df)
        return format_output(df, inst_id, bar, profile)
    except Exception as e:
        return {
            "instId": inst_id,
            "bar": bar,
            "profile": profile,
            "error": str(e),
            "data": [],
        }


def process_data(inst_id: str, bars: list, limit: int = 100,
                 profile: str = "live", output_json: bool = False) -> list:
    """
    对指定标的批量执行多周期数据获取与指标计算。
    参数:
        inst_id: 交易标的
        bars: 周期列表，如 ["1H", "4H", "1D"]
        limit: 每个周期获取的数据条数
        profile: 运行环境 (live / demo)
        output_json: 是否以纯 JSON 格式输出（Agent 解析模式）
    返回:
        每个周期的计算结果列表
    """
    results = []

    for bar in bars:
        if not output_json:
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{ts}] 正在获取 {inst_id} ({bar}) 数据... [Profile: {profile}]")

        result = process_single(inst_id, bar, limit, profile)
        results.append(result)

        if not output_json:
            if "error" in result:
                print(f"  ✘ 错误: {result['error']}")
            else:
                print(f"  ✔ 成功获取 {result['count']} 条数据，指标计算完成。")
                # 终端展示最近数据
                df_display = pd.DataFrame(result["data"])
                display_cols = ["ts", "c", "ema_5", "ema_10", "ema_20", "rsi", "bias_10", "bb_upper", "bb_lower"]
                available_cols = [c for c in display_cols if c in df_display.columns]
                print(df_display[available_cols].to_string(index=False))
                print()

    if output_json:
        # 纯 JSON 输出，能被 Agent 直接解析
        output = {
            "instId": inst_id,
            "profile": profile,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "results": results,
        }
        print(json.dumps(output, ensure_ascii=False))

    return results


# ========== CLI 入口 ==========

def main():
    parser = argparse.ArgumentParser(
        description="OKX 量化交易指标计算器 — 获取K线并计算 RSI/EMA/布林带/乖离率",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""使用示例:
  # 获取 BTC-USDT 1小时K线（终端可读输出）
  python calculator.py --instId BTC-USDT --bar 1H

  # 同时获取 1H/4H/1D 三个周期（JSON 输出，供 Agent 解析）
  python calculator.py --instId BTC-USDT --bar 1H 4H 1D --json

  # 模拟盘环境获取数据
  python calculator.py --instId ETH-USDT --bar 4H --profile demo --json
""",
    )
    parser.add_argument("--instId", type=str, required=True,
                        help="交易标的，例: BTC-USDT, ETH-USDT-SWAP")
    parser.add_argument("--bar", type=str, nargs="+", default=["1H"],
                        help="时间周期，可指定多个，例: 1H 4H 1D")
    parser.add_argument("--limit", type=int, default=100,
                        help="每个周期获取数据条数（最大 300）")
    parser.add_argument("--profile", type=str, default="live",
                        choices=["live", "demo"],
                        help="运行环境: live (实盘) / demo (模拟盘)")
    parser.add_argument("--json", action="store_true",
                        help="以纯 JSON 格式输出，供 Agent 或自动化系统解析")

    args = parser.parse_args()

    try:
        process_data(
            inst_id=args.instId,
            bars=args.bar,
            limit=args.limit,
            profile=args.profile,
            output_json=args.json,
        )
    except Exception as e:
        if args.json:
            # JSON 模式下，连顶层异常也用 JSON 格式输出
            error_output = {
                "instId": args.instId,
                "profile": args.profile,
                "error": str(e),
                "results": [],
            }
            print(json.dumps(error_output, ensure_ascii=False))
            sys.exit(1)
        else:
            print(f"\n致命错误: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
