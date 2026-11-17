#!/usr/bin/env python3
"""Kerrystock 步骤3：基于标的自身历史，计算真实的月度/年度季节性，并跑 SignalEngine。

核心思想：绝不套用 seasonality.py 的 A股默认 bullish/bearish 月份，而是用
本标的的月度收益统计，按阈值判定出它自己的做多/回避月份，再喂给 SignalEngine。

用法:
  python3 seasonal_analysis.py --csv 601138_day.csv --out-json seasonal_stats.json --out-csv seasonal_stats.csv
  python3 seasonal_analysis.py --csv 601138_day.csv --win 0.55 --lose 0.45
"""
import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import _builtin_skill_path

WB_QUANT = os.environ.get("WB_FINANCE_QUANT_DIR") or _builtin_skill_path("wb-finance-skill/scripts/quant")
if not WB_QUANT or not os.path.isdir(WB_QUANT):
    print("[error] 找不到 wb-finance-skill 的 quant 目录，请设置 WB_FINANCE_QUANT_DIR", file=sys.stderr)
    sys.exit(1)
sys.path.insert(0, WB_QUANT)
from seasonality import SignalEngine  # noqa: E402


def analyze(csv_path: str, win: float, lose: float, out_json: str, out_csv: str):
    df = pd.read_csv(csv_path)
    df = df[df["Date"] != "date"].copy()
    # ETF/基金纯净值CSV兼容：缺失 OHLC 用 close 填充，volume 补 0
    for col in ["open", "high", "low"]:
        if col not in df.columns or df[col].isna().all():
            df[col] = df["close"]
    if "volume" not in df.columns:
        df["volume"] = 0
    else:
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.dropna(subset=["close"]).sort_values("Date").reset_index(drop=True)
    df = df.set_index("Date")

    # ---- 月度 close-to-close 收益 ----
    mc = df["close"].resample("ME").last()
    ret = mc.pct_change().dropna()
    monthly = pd.DataFrame({"month": ret.index.month, "ret": ret.values})
    stats = monthly.groupby("month")["ret"].agg(["count", "mean", "median", lambda x: (x > 0).sum()])
    stats.columns = ["n", "mean", "median", "up"]
    stats["win_rate"] = stats["up"] / stats["n"]
    stats = stats.sort_index()

    bull, bear = [], []
    for m, row in stats.iterrows():
        if row["win_rate"] >= win and row["mean"] > 0:
            bull.append(int(m))
        elif row["win_rate"] <= lose and row["mean"] < 0:
            bear.append(int(m))

    # ---- 年度收益 ----
    d2 = df.copy()
    d2["year"] = d2.index.year
    yearly = d2.groupby("year")["close"].agg(["first", "last"])
    yearly["ret"] = yearly["last"] / yearly["first"] - 1

    # ---- SignalEngine（用真实月份） ----
    eng = SignalEngine(bullish_months=bull or None, bearish_months=bear or None, use_weekday=False)
    sig = eng.generate({os.path.basename(csv_path): df})[os.path.basename(csv_path)]
    n_long = int((sig == 1).sum())
    n_short = int((sig == -1).sum())
    n_flat = int((sig == 0).sum())

    # ---- 全区间高低点（用日线） ----
    peak = float(df["high"].max())
    peak_date = str(df["high"].idxmax().date())
    trough = float(df["low"].min())
    trough_date = str(df["low"].idxmin().date())
    last_close = float(df["close"].iloc[-1])

    out = {
        "code_csv": csv_path,
        "date_range": [str(df.index.min().date()), str(df.index.max().date())],
        "last_close": round(last_close, 3),
        "peak": round(peak, 3), "peak_date": peak_date,
        "trough": round(trough, 3), "trough_date": trough_date,
        "bull": bull, "bear": bear,
        "win_thresh": win, "lose_thresh": lose,
        "signal_days": {"long": n_long, "short": n_short, "flat": n_flat},
        "monthly": {
            int(m): {
                "n": int(r["n"]),
                "win_rate": round(float(r["win_rate"]), 3),
                "mean": round(float(r["mean"]), 4),
                "median": round(float(r["median"]), 4),
            }
            for m, r in stats.iterrows()
        },
        "yearly": {int(y): round(float(r["ret"]), 4) for y, r in yearly.iterrows()},
    }
    with open(out_json, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    stats.to_csv(out_csv)
    print(f"bull months (做多): {bull}")
    print(f"bear months (回避): {bear}")
    print(f"signal days: long={n_long} short={n_short} flat={n_flat}")
    print(f"saved -> {out_json}, {out_csv}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="步骤1导出的日线 CSV")
    ap.add_argument("--out-json", default="seasonal_stats.json")
    ap.add_argument("--out-csv", default="seasonal_stats.csv")
    ap.add_argument("--win", type=float, default=0.55, help="做多月阈值：胜率≥此且均值>0")
    ap.add_argument("--lose", type=float, default=0.45, help="回避月阈值：胜率≤此且均值<0")
    args = ap.parse_args()
    analyze(args.csv, args.win, args.lose, args.out_json, args.out_csv)


if __name__ == "__main__":
    main()
