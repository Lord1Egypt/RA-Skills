# -*- coding: utf-8 -*-
"""个股公开数据速读 · 取数引擎（任意 A 股代码可复用）。
用法：
    python3 fetch.py <代码> [输出目录]
    例：python3 fetch.py 603629 ./out
照 daily_stock_analysis 的数据层思路，用 akshare 拉：资金流 / 龙虎榜 / 估值band /
财务三表 / 主营构成 / 北向 / 日K。每个接口独立兜底，能拿到就存 CSV，拿不到记进 _report.json。
只读公开行情/财务数据，不含任何交易动作。
"""
import os
import sys
import json

try:
    import akshare as ak
    import pandas as pd
except ImportError:
    sys.exit("缺依赖：pip install akshare pandas（建议用 venv）")

# 注：受限网络/沙箱里 eastmoney 的 push2his（资金流/筹码）可能被挡；正常机器直连即可。
# 若公司网络强制代理导致超时，可在运行前 `unset HTTP_PROXY HTTPS_PROXY` 再跑。


def market_of(code):
    """沪 6 / 深 0,3 / 北 8,4 → akshare 用的市场前缀。"""
    c = str(code)
    if c[0] == "6":
        return "sh"
    if c[0] in "03":
        return "sz"
    return "bj"


def run(code, outdir):
    code = str(code).strip()
    mkt = market_of(code)              # 'sh' / 'sz' / 'bj'
    MKT = mkt.upper()                  # 'SH' / 'SZ'
    os.makedirs(outdir, exist_ok=True)
    report = {"code": code, "market": mkt}

    def grab(name, fn):
        try:
            df = fn()
            if df is None or (hasattr(df, "empty") and df.empty):
                report[name] = "EMPTY"
                print("[EMPTY]", name)
                return None
            df.to_csv(os.path.join(outdir, name + ".csv"), index=False)
            report[name] = "OK rows=%d" % len(df)
            print("[OK]   ", name, "rows=%d" % len(df))
            return df
        except Exception as e:
            report[name] = "FAIL %s: %s" % (type(e).__name__, str(e)[:120])
            print("[FAIL] ", name, type(e).__name__)
            return None

    # 1) 日K（前复权，走 sina 源最稳，避开 eastmoney push2his）
    grab("kline_qfq", lambda: ak.stock_zh_a_daily(
        symbol=mkt + code, start_date="20240101", end_date="20261231", adjust="qfq"))
    # 2) 主力资金流向
    grab("fund_flow", lambda: ak.stock_individual_fund_flow(stock=code, market=mkt))
    # 3) 估值历史 PE/PB/市值band（不同 akshare 版本函数名不同，按序回退）
    def _valuation():
        for fn in ("stock_value_em", "stock_a_indicator_lg"):
            f = getattr(ak, fn, None)
            if f is None:
                continue
            try:
                return f(symbol=code)
            except Exception:
                continue
        raise RuntimeError("无可用估值接口")
    grab("valuation", _valuation)
    # 4) 主营构成（分行业/产品 营收+成本，可算毛利率）
    grab("zygc", lambda: ak.stock_zygc_em(symbol=MKT + code))
    # 5) 财务三表（sina 源）
    grab("profit", lambda: ak.stock_financial_report_sina(stock=mkt + code, symbol="利润表"))
    grab("cashflow", lambda: ak.stock_financial_report_sina(stock=mkt + code, symbol="现金流量表"))
    grab("balance", lambda: ak.stock_financial_report_sina(stock=mkt + code, symbol="资产负债表"))
    # 6) 财务摘要
    grab("fin_abstract", lambda: ak.stock_financial_abstract(symbol=code))
    # 7) 北向持股
    grab("hsgt", lambda: ak.stock_hsgt_individual_em(symbol=code))

    # 8) 龙虎榜：取上榜日期 → 近 N 个交易日逐日买卖明细
    try:
        dts = ak.stock_lhb_stock_detail_date_em(symbol=code)
        dts["交易日"] = dts["交易日"].astype(str)
        recent = [d for d in dts["交易日"] if d >= "2025-01-01"][-12:]
        frames = []
        for d in recent:
            dd = d.replace("-", "")
            for flag in ("买入", "卖出"):
                try:
                    x = ak.stock_lhb_stock_detail_em(symbol=code, date=dd, flag=flag)
                    if x is not None and not x.empty:
                        x.insert(0, "方向", flag)
                        x.insert(0, "日期", d)
                        frames.append(x)
                except Exception:
                    pass
        if frames:
            allx = pd.concat(frames, ignore_index=True)
            allx.to_csv(os.path.join(outdir, "lhb_detail.csv"), index=False)
            report["lhb_detail"] = "OK rows=%d" % len(allx)
            print("[OK]    lhb_detail rows=%d" % len(allx))
        else:
            report["lhb_detail"] = "EMPTY (近期未上榜)"
    except Exception as e:
        report["lhb_detail"] = "FAIL %s" % type(e).__name__
        print("[FAIL]  lhb_detail", type(e).__name__)

    with open(os.path.join(outdir, "_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print("\n=== 取数汇总（%s %s）===" % (code, mkt))
    for k, v in report.items():
        print("  %-14s %s" % (k, v))
    print("CSV 已存：", outdir)


def probe():
    """轻量探针：依赖是否可用、akshare 能否连上东财接口。"""
    print("=== stock-data-reader 探针 ===")
    try:
        import akshare as ak  # noqa: F401
        import pandas as pd  # noqa: F401
        print("[OK]   import akshare, pandas")
    except ImportError as e:
        print("[FAIL] import:", e)
        print("修复: bash scripts/bootstrap.sh")
        return 1
    try:
        df = ak.stock_zh_a_spot_em()
        n = len(df) if df is not None else 0
        print("[OK]   ak.stock_zh_a_spot_em rows=%d" % n)
    except Exception as e:
        print("[FAIL] akshare 联网:", type(e).__name__, e)
        print("提示: 公司代理可能挡东财；可 unset HTTP_PROXY HTTPS_PROXY 后重试")
        return 2
    print("探针通过，可跑: python3 scripts/fetch.py <代码>")
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] in ("--probe", "-p"):
        sys.exit(probe())
    if len(sys.argv) < 2:
        sys.exit("用法：python3 fetch.py <代码> [输出目录]\n      python3 fetch.py --probe")
    code = sys.argv[1]
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "out", code)
    run(code, outdir)
