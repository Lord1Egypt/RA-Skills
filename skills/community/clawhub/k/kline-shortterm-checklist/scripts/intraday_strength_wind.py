#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""intraday_strength_wind.py — 分时强度客观化（Wind 金融数据 MCP）本地辅助脚本。

背景：96 原则「下午 2:30 选股法」第 7 层要求看分时图——强势股应"全天运行在分时均价线
上方、跑赢大盘"。原本只能标 👁 人工。Wind 的 `get_stock_quote` / `get_index_quote`
返回分钟级序列（含 MATCH=当时价、AVPRICE=分时均价线），可把"分时强度"客观化。

本脚本不直连 Wind，而是做两件事（与 announcements_wind.py 同模式）：
  (1) --plan : 读 candidates.json + kline_data.json（+ screen_meta.json 取数据基准日），
               复刻 report_html.py 的 prio 深度候选逻辑（在 kline 中 且 多头/低PE<20/近高<1，
               按 -vr 排序取前 10），输出 intraday_plan.json：每只含 Wind 代码（自动转 .SH/.SZ/.BJ）
               与基准指数 000300.SH。助手据此逐只调 Wind 拉分钟数据。
  (2) --merge: 读助手归集的 intraday_raw.json（Wind 原始 data 对象），对每只 prio 票算
               分时强度指标，输出 intraday_strength.json（above_ratio / excess / above_at_close
               / verdict 强·中·弱 / partial 是否未收盘）。报告据此把"分时强度 👁"翻为自动结论，
               题材仍保留 👁（Wind 给不了"今天什么在炒"的主观判断）。

助手归集格式（intraday_raw.json）：
  {
    "date": "2026-08-10",
    "benchmark": {"windcode": "000300.SH", "data": <get_index_quote 返回的 data 对象>},
    "stocks": {
       "603990": {"name": "麦迪科技", "windcode": "603990.SH", "data": <get_stock_quote 返回的 data 对象>},
       ...
    }
  }
其中 data 即 Wind 工具返回的 `data` 字段（含 columns/rows），原样存入即可。

用法:
  python intraday_strength_wind.py --plan [--top N]
  python intraday_strength_wind.py --merge
"""
import json, os, sys

BENCH = "000300.SH"  # 沪深300 作"大盘"基准，用于算"跑赢大盘"超额收益

def norm_key(code):
    return code[2:] if code[:2] in ("sh", "sz", "bj") else code

def to_wind(code):
    """6 位代码 → Wind 代码（沪深主/科创板.SH，深主/创业板.SZ，北交所.BJ）。"""
    c = norm_key(code)
    if c[0] == "6":
        return c + ".SH"
    if c[0] in ("0", "3"):
        return c + ".SZ"
    if c[0] in ("8", "4"):
        return c + ".BJ"
    return c + ".SH"

def load_cands(cwd):
    with open(os.path.join(cwd, "candidates.json"), encoding="utf-8") as f:
        return json.load(f)

def load_kl(cwd):
    try:
        with open(os.path.join(cwd, "kline_data.json"), encoding="utf-8") as f:
            return {norm_key(d["code"]): d for d in json.load(f)}
    except FileNotFoundError:
        return {}

def load_date(cwd):
    try:
        with open(os.path.join(cwd, "screen_meta.json"), encoding="utf-8") as f:
            return json.load(f).get("data_date", "最近交易日")
    except FileNotFoundError:
        return "最近交易日"

def prio_list(cands, kl):
    """复刻 report_html.py 的 prio 深度候选逻辑（与报告卡片严格一致）。"""
    prio = [c for c in cands if c["code"] in kl and (
        kl[c["code"]].get("multi") or
        (c.get("pe") and c["pe"] > 0 and c["pe"] < 20) or
        kl[c["code"]].get("near_high", 99) < 1)]
    prio.sort(key=lambda x: -x["vr"])
    return prio[:10]

def plan(cwd, top=None):
    cands = load_cands(cwd)
    kl = load_kl(cwd)
    date = load_date(cwd)
    sel = prio_list(cands, kl)
    if top:
        sel = sel[:top]
    stocks = [{"code": c["code"], "name": c["name"], "windcode": to_wind(c["code"])}
              for c in sel]
    out = {
        "date": date,
        "benchmark": {"windcode": BENCH, "note": "沪深300，用于算跑赢大盘超额收益"},
        "stocks": stocks,
    }
    path = os.path.join(cwd, "intraday_plan.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"[plan] 已写出 intraday_plan.json：{len(stocks)} 只深度候选（与报告卡片一致）")
    print(f"       数据基准日={date}；基准指数={BENCH}（沪深300）")
    print(f"       下一步（需 wind-finance 已连接）：")
    print(f"         ① 调 mcp__wind-finance__get_index_quote(windcode='{BENCH}', begin='{date}', end='{date}') 拉基准；")
    for s in stocks:
        print(f"         ② 调 mcp__wind-finance__get_stock_quote(windcode='{s['windcode']}', begin='{date}', end='{date}') 拉 {s['name']}；")
    print(f"       把每只返回的 data 对象按 intraday_plan 结构归集进 intraday_raw.json，再运行 `--merge`。")
    if not kl:
        print(f"       ⚠️ 未找到 kline_data.json，prio 为空；请先跑 kline_history.py --top 15 --json。")

def parse_series(data):
    """从 Wind 返回的 data 对象（columns+rows）解析出 时间序列/价/**分时均价线**。
    按列名取索引，避免依赖列顺序。返回 (times, price, avg)。

    ⚠️ 关键纠错（2026-08-10 实测，勿改回）：Wind 的 `AVPRICE` 列**不是分时均价线**，
    而是**该根分钟 bar 自身的均价 (OPEN+HIGH+LOW+MATCH)/4**。铁证有二：
      ① 沪深300 09:30 根 (4698.82+4702.07+4698.82+4701.93)/4 = 4700.41 = AVPRICE，逐根可复现；
      ② 15:00 收盘集合竞价为单一价（O=H=L=C），当日 10 只个股 AVPRICE 全部与 MATCH **完全相等**——
         真正的全日均价线几乎不可能恰好等于收盘价（同日新浪重建的真均价线均与收盘价不等）。
    若直接拿它当均价线，`above_ratio` 实际测的是「收盘价 vs 本分钟中值」，接近抛硬币，第 7 层失效。

    正确做法：**自行重建累计均价线**——
      · 有 TURNOVER/VOLUME 列 → 累计成交额 ÷ 累计成交量（真·VWAP 分时均价线，首选）；
      · 只有 MATCH → 退化为 MATCH 的累计等权均值（近似均价线，误差通常 <0.5%）。
    """
    cols = [c["name"] for c in data["columns"]]
    idx = {name: i for i, name in enumerate(cols)}
    t_i, m_i = idx["TIME"], idx["MATCH"]
    rows = data["rows"]
    times = [r[t_i] for r in rows]
    price = [float(r[m_i]) for r in rows]

    to_i, v_i = idx.get("TURNOVER"), idx.get("VOLUME")
    avg, cum_to, cum_v, cum_p = [], 0.0, 0.0, 0.0
    if to_i is not None and v_i is not None:          # 首选：真·VWAP
        for i, r in enumerate(rows):
            cum_to += float(r[to_i] or 0)
            cum_v += float(r[v_i] or 0)
            cum_p += price[i]
            avg.append(cum_to / cum_v if cum_v > 0 else cum_p / (i + 1))
    else:                                              # 退化：累计等权均价
        for i, p in enumerate(price):
            cum_p += p
            avg.append(cum_p / (i + 1))
    return times, price, avg

def strength_of(times, price, avg):
    """单只/指数的分时强度原始指标。"""
    n = len(price)
    above = sum(1 for p, a in zip(price, avg) if p >= a)
    above_ratio = above / n if n else 0.0
    first_p, last_p = price[0], price[-1]
    ret = (last_p - first_p) / first_p * 100 if first_p else 0.0
    above_at_close = last_p >= avg[-1] if avg else False
    avg_first, avg_last = avg[0], avg[-1]
    avg_ret = (avg_last - avg_first) / avg_first * 100 if avg_first else 0.0
    last_hour = int(times[-1][11:13]) if times else 0
    partial = last_hour < 15  # 最后一根分钟不足 15:00 → 未收盘快照
    return {
        "n_min": n, "above_ratio": round(above_ratio, 4),
        "ret": round(ret, 2), "above_at_close": above_at_close,
        "avg_ret": round(avg_ret, 2), "partial": partial,
        "last_time": times[-1][11:19] if times else "",
    }

def verdict_str(above_ratio, excess, above_at_close):
    """分时强度综合判定：强/中/弱（与"全天在均价线上方 + 跑赢大盘"原则对齐）。"""
    if above_ratio >= 0.60 and excess > 0 and above_at_close:
        return "强"
    if (above_ratio >= 0.45 and excess > 0) or (above_ratio >= 0.60 and above_at_close):
        return "中"
    return "弱"

def merge(cwd):
    raw_path = os.path.join(cwd, "intraday_raw.json")
    if not os.path.exists(raw_path):
        print("[merge] 未找到 intraday_raw.json，跳过（报告「分时强度」将回落到 👁 人工项）。")
        return
    raw = json.load(open(raw_path, encoding="utf-8"))
    bench = raw.get("benchmark", {}).get("data")
    if not bench or not bench.get("rows"):
        print("[merge] 警告：benchmark(沪深300) 数据缺失，无法算超额收益，excess 记为 0。")
        bench_s = None
    else:
        bt, bp, ba = parse_series(bench)
        bench_s = strength_of(bt, bp, ba)
    stocks_raw = raw.get("stocks", {})
    out = {}
    for code, rec in stocks_raw.items():
        d = rec.get("data")
        if not d or not d.get("rows"):
            out[code] = {"covered": False}
            continue
        t, p, a = parse_series(d)
        s = strength_of(t, p, a)
        excess = round(s["ret"] - bench_s["ret"], 2) if bench_s else 0.0
        v = verdict_str(s["above_ratio"], excess, s["above_at_close"])
        out[code] = {
            "covered": True,
            "name": rec.get("name", ""),
            "above_ratio": s["above_ratio"],
            "stock_ret": s["ret"],
            "index_ret": bench_s["ret"] if bench_s else 0.0,
            "excess": excess,
            "above_at_close": s["above_at_close"],
            "avg_ret": s["avg_ret"],
            "verdict": v,
            "partial": s["partial"],
            "last_time": s["last_time"],
            "n_min": s["n_min"],
        }
    path = os.path.join(cwd, "intraday_strength.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    cov = [c for c, v in out.items() if v.get("covered")]
    strong = [c for c, v in out.items() if v.get("verdict") == "强"]
    mid = [c for c, v in out.items() if v.get("verdict") == "中"]
    weak = [c for c, v in out.items() if v.get("verdict") == "弱"]
    print(f"[merge] 已写出 intraday_strength.json：{len(cov)}/{len(out)} 只覆盖")
    print(f"        分时强度：强 {len(strong)} · 中 {len(mid)} · 弱 {len(weak)}")
    print(f"        基准(沪深300)日内涨跌 {bench_s['ret']:+.2f}%" if bench_s else "        基准缺失")
    print(f"        报告将据此把八层第7层「分时强度」👁 翻为自动结论（题材仍 👁）。")

def main():
    cwd = os.getcwd()
    args = sys.argv[1:]
    if "--plan" in args:
        top = None
        if "--top" in args:
            i = args.index("--top")
            top = int(args[i + 1])
        plan(cwd, top)
    elif "--merge" in args:
        merge(cwd)
    else:
        print("用法: python intraday_strength_wind.py --plan [--top N] | --merge")

if __name__ == "__main__":
    main()
