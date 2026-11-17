#!/usr/bin/env python3
"""Kerrystock 步骤1：从 westock-data 导出标的日线（或月线）数据。

自动按约2年一段分段调用，规避 westock-data 日 K 约2000条上限；
解析其 markdown 表格输出（last=收盘价），合并去重为 OHLCV CSV。

用法:
  python3 export_kline.py --code sh601138 --start 2018-06-01 --end 2026-07-18 --out 601138_day.csv
  python3 export_kline.py --code sh000001 --start 2015-01-01 --end 2026-07-18 --period month --out idx_month.csv
"""
import argparse
import os
import subprocess
import sys
import pandas as pd


def _normalize_code(code: str, market: str = None) -> str:
    """归一化代码：已带 sh/sz 前缀则不变；纯数字按 A股/ETF/LOF 约定补前缀
    （沪 5/6/9 -> sh，深 0/1/2/3 -> sz）；显式 --market 优先。指数/北交所请用前缀或 --market。"""
    code = code.strip().lower()
    if code[:2] in ("sh", "sz"):
        return code
    if market:
        return f"{market.lower()}{code}"
    if code.isdigit():
        if code[0] in "569":
            return "sh" + code
        if code[0] in "0123":
            return "sz" + code
    return code


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import _builtin_skill_path, _managed_node

NODE = os.environ.get("NODE_BIN") or _managed_node()
WESTOCK = os.environ.get("WESTOCK_DATA_SCRIPT") or _builtin_skill_path("westock-data/scripts/index.js")


def _segments(start: str, end: str):
    """按约2年一段切分 [start, end]，返回 (s, e) 列表。"""
    s = pd.Timestamp(start)
    e = pd.Timestamp(end)
    segs = []
    cur = s
    while cur <= e:
        nxt = cur + pd.DateOffset(years=2) - pd.Timedelta(days=1)
        if nxt > e:
            nxt = e
        segs.append((cur.strftime("%Y-%m-%d"), nxt.strftime("%Y-%m-%d")))
        cur = nxt + pd.Timedelta(days=1)
    return segs


def _parse_md_table(text: str):
    lines = [l for l in text.splitlines() if l.strip().startswith("|")]
    if not lines:
        return None, []
    header = [c.strip() for c in lines[0].strip().strip("|").split("|")]
    rows = []
    for l in lines[1:]:
        if set(l.strip()) <= set("|- "):  # 分隔行
            continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        rows.append(cells)
    return header, rows


def export(code: str, start: str, end: str, period: str, out: str) -> pd.DataFrame:
    frames = []
    for s, e in _segments(start, end):
        outp = subprocess.run(
            [NODE, WESTOCK, "kline", code, "--period", period,
             "--start", s, "--end", e, "--fq", "qfq"],
            capture_output=True, text=True,
        ).stdout
        header, rows = _parse_md_table(outp)
        if not header or not rows:
            print(f"  [warn] segment {s}~{e} 无数据，跳过")
            continue
        df = pd.DataFrame(rows, columns=header)
        # 列名归一：last->close, date->Date
        df = df.rename(columns={"last": "close", "date": "Date"})
        for c in ["open", "high", "low", "close", "volume"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        keep = [c for c in ["Date", "open", "high", "low", "close", "volume"] if c in df.columns]
        df = df[keep]
        print(f"  segment {s}~{e}: {len(df)} rows")
        frames.append(df)

    if not frames:
        raise SystemExit("未获取到任何 K 线数据，请检查代码/区间/网络。")

    all_df = pd.concat(frames, ignore_index=True)
    all_df = all_df.drop_duplicates(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    all_df = all_df[all_df["Date"] != "date"]  # 清脏行
    for c in ["open", "high", "low", "close", "volume"]:
        if c in all_df.columns:
            all_df[c] = pd.to_numeric(all_df[c], errors="coerce")
    all_df = all_df.dropna(subset=["close"]).reset_index(drop=True)
    all_df.to_csv(out, index=False)
    print(f"TOTAL: {len(all_df)} rows -> {out}")
    print(f"range: {all_df['Date'].min()} -> {all_df['Date'].max()}")
    return all_df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", required=True, help="标的代码，如 sh601138 / 601138 / sh510300(ETF) / sz161725(LOF)")
    ap.add_argument("--market", default=None, choices=["sh", "sz"], help="可选：纯数字代码强制加的市场前缀（绕过自动判断）")
    ap.add_argument("--start", required=True, help="起始日 YYYY-MM-DD")
    ap.add_argument("--end", required=True, help="结束日 YYYY-MM-DD")
    ap.add_argument("--period", default="day", help="day / week / month，默认 day")
    ap.add_argument("--out", required=True, help="输出 CSV 路径")
    args = ap.parse_args()

    if not NODE or not os.path.exists(NODE):
        print(f"[error] node 不存在: {NODE}；请设置 NODE_BIN 或用 managed node", file=sys.stderr)
        sys.exit(1)
    if not WESTOCK or not os.path.exists(WESTOCK):
        print(f"[error] westock-data 脚本不存在: {WESTOCK}\n请设置环境变量 WESTOCK_DATA_SCRIPT 指向其 index.js", file=sys.stderr)
        sys.exit(1)
    code = _normalize_code(args.code, args.market)
    print(f"[info] 归一化代码: {args.code} -> {code}")
    export(code, args.start, args.end, args.period, args.out)


if __name__ == "__main__":
    main()
