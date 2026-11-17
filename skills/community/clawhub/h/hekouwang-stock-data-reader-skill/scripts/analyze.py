# -*- coding: utf-8 -*-
"""个股公开数据速读 · 分析引擎。
读 fetch.py 产出的 CSV，算出固定指标体系，写 analysis.json（供出报告用）并打印摘要。
用法：python3 analyze.py <out目录>
指标体系（栏目固定）：价格轨迹 · 主力进出 · 龙虎榜结构 · 利润质量 · 利润结构 · 估值 · 风险线索。
⚠️ 只做事实计算，不产出买卖建议/评级/预测（合规见 references/compliance.md）。
"""
import os
import sys
import json

try:
    import pandas as pd
except ImportError:
    sys.exit("缺依赖：pip install pandas")


def load(outdir, name):
    p = os.path.join(outdir, name + ".csv")
    return pd.read_csv(p) if os.path.exists(p) else None


def col(df, keys):
    for k in keys:
        for c in df.columns:
            if k in c:
                return c
    return None


def run(outdir):
    A = {}                       # 汇总结果 → analysis.json
    print("=" * 56)

    # 1) 价格 / 市值 / 估值轨迹
    v = load(outdir, "valuation")
    if v is not None and "数据日期" in v.columns:
        v["数据日期"] = v["数据日期"].astype(str)
        v26 = v[v["数据日期"] >= "2026-01-01"].copy()
        if not v26.empty:
            peak = v26.loc[v26["总市值"].idxmax()]
            last = v26.iloc[-1]
            first = v26.iloc[0]
            A["price"] = {
                "start_date": first["数据日期"], "start_px": round(float(first["当日收盘价"]), 2),
                "start_mktcap_yi": round(float(first["总市值"]) / 1e8),
                "peak_date": peak["数据日期"], "peak_px": round(float(peak["当日收盘价"]), 2),
                "peak_mktcap_yi": round(float(peak["总市值"]) / 1e8),
                "peak_pe": round(float(peak["PE(TTM)"]), 1), "peak_pb": round(float(peak["市净率"]), 1),
                "last_date": last["数据日期"], "last_px": round(float(last["当日收盘价"]), 2),
                "last_mktcap_yi": round(float(last["总市值"]) / 1e8),
                "last_pe": round(float(last["PE(TTM)"]), 1), "last_pb": round(float(last["市净率"]), 1),
                "drawdown_pct": round((1 - float(last["当日收盘价"]) / float(peak["当日收盘价"])) * 100, 1),
            }
            print("价格：%(start_px)s→峰值%(peak_px)s→%(last_px)s | 市值%(start_mktcap_yi)s→%(peak_mktcap_yi)s→%(last_mktcap_yi)s亿 | PE %(peak_pe)s→%(last_pe)s | 回撤%(drawdown_pct)s%%" % A["price"])

    # 2) 主力资金（近 N 日 + 关键日）
    f = load(outdir, "fund_flow")
    if f is not None:
        c = col(f, ["主力净流入-净额"])
        dc = col(f, ["日期"])
        pc = col(f, ["涨跌幅"])
        if c and dc:
            f[dc] = f[dc].astype(str)
            f4 = f[f[dc] >= "2026-04-01"].copy()
            total = round(f4[c].sum() / 1e8, 1)
            key = []
            for _, r in f4.reindex(f4[c].abs().sort_values(ascending=False).index).head(6).iterrows():
                key.append({"date": r[dc][5:], "chg": round(float(r[pc]), 2), "net_yi": round(float(r[c]) / 1e8, 2)})
            key.sort(key=lambda x: x["date"])
            A["fundflow"] = {"net_4mo_yi": total, "key_days": key}
            print("主力 4 月以来净额合计：%s 亿" % total)

    # 3) 龙虎榜结构（席位类型计数 + 买卖对称度）
    l = load(outdir, "lhb_detail")
    if l is not None:
        seatcol = col(l, ["交易营业部名称", "营业部"])
        dircol = col(l, ["方向"]) or ("方向" if "方向" in l.columns else None)
        if seatcol:
            seats = l[seatcol].astype(str)
            n_hgt = int(seats.str.contains("沪股通|深股通").sum())
            n_inst = int(seats.str.contains("机构专用").sum())
            lhb = {"rows": int(len(l)), "n_northbound_rows": n_hgt, "n_institution_rows": n_inst}
            if dircol:
                sym = []
                n_bidir = 0
                n_channel = 0
                for seat, grp in l.groupby(seatcol):
                    buys = int((grp[dircol].astype(str) == "买入").sum())
                    sells = int((grp[dircol].astype(str) == "卖出").sum())
                    if buys == 0 and sells == 0:
                        continue
                    if buys > 0 and sells > 0:
                        n_bidir += 1
                    ratio = round(buys / sells, 2) if sells > 0 else None
                    if ratio is not None and 0.85 <= ratio <= 1.15 and (buys + sells) >= 4:
                        n_channel += 1
                    sym.append({
                        "seat": str(seat)[:48],
                        "buys": buys,
                        "sells": sells,
                        "buy_sell_ratio": ratio,
                    })
                sym.sort(key=lambda x: x["buys"] + x["sells"], reverse=True)
                lhb["n_bidirectional_seats"] = n_bidir
                lhb["n_channel_like_seats"] = n_channel
                lhb["seat_symmetry"] = sym[:10]
                lhb["symmetry_note"] = (
                    "买卖比近1且出现频次高→通道型席位，勿推方向；"
                    "解读前建议对照当日全市场基准（见 references/lhb-symmetry.md）"
                )
                print(
                    "龙虎榜：%d 行，沪深股通 %d，机构 %d；双向席位 %d，通道型 %d"
                    % (len(l), n_hgt, n_inst, n_bidir, n_channel)
                )
            else:
                print("龙虎榜：%d 行，沪深股通 %d，机构专用 %d" % (len(l), n_hgt, n_inst))
            A["lhb"] = lhb

    # 4) 利润质量：归母净利 vs 经营现金流（最近几期）
    p = load(outdir, "profit")
    c = load(outdir, "cashflow")
    quality = []
    if p is not None and c is not None:
        npc = col(p, ["归属于母公司"]) or col(p, ["净利润"])
        cfo = col(c, ["经营活动产生的现金流量净额", "经营活动产生的现金流量"])
        dpc = col(p, ["报告日"])
        dcc = col(c, ["报告日"])
        if npc and cfo and dpc and dcc:
            cmap = {str(r[dcc]): r[cfo] for _, r in c.iterrows()}
            for _, r in p.head(5).iterrows():
                d = str(r[dpc])
                if d in cmap:
                    quality.append({"period": d, "net_yi": round(float(r[npc]) / 1e8, 2),
                                    "cfo_yi": round(float(cmap[d]) / 1e8, 2)})
            A["profit_quality"] = quality
            if quality:
                print("利润质量（净利/现金流）：", "; ".join("%s %.2f/%.2f" % (q["period"], q["net_yi"], q["cfo_yi"]) for q in quality[:3]))

    # 5) 利润结构：主营分部 收入 + 毛利率
    z = load(outdir, "zygc")
    if z is not None and "报告日期" in z.columns:
        z["报告日期"] = z["报告日期"].astype(str)
        latest = z["报告日期"].max()
        seg = z[(z["报告日期"] == latest) & (z["分类类型"].astype(str).str.contains("行业", na=False))]
        segs = []
        for _, r in seg.iterrows():
            rev = float(r["主营收入"]) if pd.notna(r["主营收入"]) else 0
            cost = float(r["主营成本"]) if pd.notna(r["主营成本"]) else 0
            gm = round((1 - cost / rev) * 100, 1) if rev else None
            segs.append({"name": str(r["主营构成"]), "rev_yi": round(rev / 1e8, 2),
                         "rev_pct": round(float(r["收入比例"]) * 100, 1) if pd.notna(r["收入比例"]) else None,
                         "gross_margin_pct": gm, "gross_yi": round((rev - cost) / 1e8, 2)})
        if segs:
            tot_g = sum(s["gross_yi"] for s in segs if s["gross_yi"])
            for s in segs:
                s["gross_share_pct"] = round(s["gross_yi"] / tot_g * 100, 1) if tot_g else None
            A["structure"] = {"period": latest, "segments": segs}
            print("利润结构（%s）：" % latest, "; ".join("%s 收入%.0f%% 毛利率%s%% 毛利占比%s%%" % (s["name"][:6], s["rev_pct"] or 0, s["gross_margin_pct"], s["gross_share_pct"]) for s in segs))

    # 6) 资产负债关键项
    b = load(outdir, "balance")
    if b is not None:
        r0 = b.iloc[0]
        bd = {"period": str(r0[col(b, ["报告日"])])}
        for key, jk in [("资产总计", "assets"), ("负债合计", "liab"), ("应收账款", "ar"),
                        ("合同负债", "contract_liab"), ("货币资金", "cash")]:
            cc = col(b, [key])
            if cc:
                try:
                    bd[jk] = round(float(r0[cc]) / 1e8, 2)
                except Exception:
                    pass
        if bd.get("assets") and bd.get("liab"):
            bd["debt_ratio_pct"] = round(bd["liab"] / bd["assets"] * 100, 1)
        A["balance"] = bd
        print("资产负债率：%s%%（负债%s/资产%s 亿，%s）" % (bd.get("debt_ratio_pct"), bd.get("liab"), bd.get("assets"), bd.get("period")))

    out = os.path.join(outdir, "analysis.json")
    with open(out, "w", encoding="utf-8") as fobj:
        json.dump(A, fobj, ensure_ascii=False, indent=2)
    print("=" * 56)
    print("结构化指标已写：", out)
    print("⚠️ 仅事实计算，出报告时务必套合规框架（references/compliance.md）。")
    return A


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法：python3 analyze.py <out目录>")
    run(sys.argv[1])
