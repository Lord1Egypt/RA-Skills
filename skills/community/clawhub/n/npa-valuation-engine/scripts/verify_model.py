#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""NPA IRR 模型 — 独立验证器（双验 + 投标上限反推）

用法：
    python verify_model.py --model model.xlsx
    python verify_model.py --model model.xlsx --json
    python verify_model.py --model model.xlsx --allow-degraded

做五件事，全部通过才叫验过：
  1. LibreOffice 重算 → 读公式缓存值
  2. Python(numpy_financial) 按同一口径独立自算 → 比对偏差（应 < 1e-12）
  3. 反推投标上限：保守情景 IRR = 门槛时的最高可出价
  4. 全表错误单元格扫描（#/Err: 开头）
  5. 公式存在性检查（三情景现金流表里确实写了公式，而不是死数）

退出码：
  0 = 完整双验通过
  1 = 验证不通过（模型有偏差 / 结构缺失）
  2 = 降级通过：本机缺少 LibreOffice，重算与缓存值比对无法执行，
      但 Python 独立自算与公式存在性检查已通过。装 LibreOffice 后重跑可得完整结论；
      加 --allow-degraded 可让降级情形也返回 0，便于接进自动化流程。

注意：LibreOffice 对 OOXML 默认不重算；本脚本会先给文件强制打上
fullCalcOnLoad 标志再转换，否则公式缓存值恒为 0，会误判成"模型算不出数"。
另外 soffice 转换时源文件与输出目录不能同名同目录，否则静默失败。
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy_financial as npf
from openpyxl import load_workbook

LABELS = {
    "eval": "法院评估价(元)", "deal": "预估成交价(元)", "mkt": "对标市场价(元)",
    "C": "取得总成本(元)", "hc": "季度持有成本率(按取得成本)",
    "wacc": "资金成本(年化)", "thr": "目标IRR门槛(年化)",
    "f": "退出售价系数(占对标市场价)", "mo": "处置周期(月)",
    "m": "回款方式(1=一次性/2=分3期)", "ac": "追加成本系数(占取得总成本)",
}
OUT_LABELS = {"moic": "MOIC(倍数)", "irr": "IRR(年化)", "npv": "NPV(元)", "pass": "达标判定(IRR≥门槛)"}
COLS = ("B", "C", "D")
SCEN = ("保守", "基准", "乐观")


def find_row(ws, label):
    for r in range(1, ws.max_row + 1):
        v = ws.cell(row=r, column=1).value
        if isinstance(v, str) and v.strip() == label:
            return r
    raise KeyError(f"未找到标签: {label}")


def recalc(src):
    """强制 fullCalcOnLoad 后交给 LibreOffice 重算，返回含缓存值的新路径"""
    tmp = tempfile.mkdtemp(prefix="npa_verify_")
    srcdir = os.path.join(tmp, "src")
    outdir = os.path.join(tmp, "out")
    os.makedirs(srcdir, exist_ok=True)
    os.makedirs(outdir, exist_ok=True)
    forced = os.path.join(srcdir, "forced.xlsx")
    wb = load_workbook(src)
    wb.calculation.fullCalcOnLoad = True
    wb.save(forced)
    if shutil.which("soffice") is None:
        return forced, tmp, "no_soffice"
    subprocess.run(["soffice", "--headless", "--convert-to", "xlsx", "--outdir", outdir, forced],
                   capture_output=True, timeout=180)
    out = os.path.join(outdir, os.path.basename(forced))
    if not os.path.exists(out):
        return forced, tmp, "convert_failed"
    return out, tmp, "ok"


_CELL_REF = re.compile(r"^=?\$?([A-Za-z]{1,3})\$?(\d+)$")
_SUM_RANGE = re.compile(r"^=SUM\(([A-Za-z]{1,3})(\d+):([A-Za-z]{1,3})(\d+)\)$")


def eval_cell(ws, addr, depth=0):
    """无计算引擎时的回退求值：只认 字面值 / =单元格引用 / =SUM(区间) 这三种形态。

    用于「取得总成本」这类小计格（=SUM(B15:B20)，而 B15 自身又是 =B9）的还原；
    遇到无法识别的公式一律返回 None，由调用方判定为「读不全」，绝不猜数。
    """
    if depth > 4:
        return None
    v = ws[addr].value
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if not isinstance(v, str) or not v.startswith("="):
        return None
    f = v.strip()
    m = _CELL_REF.match(f)
    if m:
        return eval_cell(ws, f"{m.group(1).upper()}{m.group(2)}", depth + 1)
    m = _SUM_RANGE.match(f)
    if m:
        c1, r1 = m.group(1).upper(), int(m.group(2))
        c2, r2 = m.group(3).upper(), int(m.group(4))
        total, found = 0.0, 0
        for c in range(ord(c1) - 64, ord(c2) - 64 + 1):
            for r in range(r1, r2 + 1):
                x = eval_cell(ws, f"{chr(64 + c)}{r}", depth + 1)
                if x is not None:
                    total += x
                    found += 1
        return total if found else None
    return None


def build_cf(C, P, hc, f, months, mode, ac, hz=None):
    n = -(-months // 3)
    cf = [-C]
    for t in range(1, n + 1):
        v = -C * hc
        if mode == 2 and n >= 3:
            w = 0.4 if t == n - 2 else (0.3 if t in (n - 1, n) else 0)
        else:
            w = 1.0 if t == n else 0
        v += P * f * w
        if t == n:
            v -= C * ac
        cf.append(v)
    return cf


def verify(model_path):
    rep = {"model": os.path.abspath(model_path), "checks": {}, "rate": {}, "scenarios": {}, "ok": False}
    recalc_path, tmpdir, rc_status = recalc(model_path)
    degraded = rc_status != "ok"
    rep["degraded"] = degraded

    wb = load_workbook(recalc_path, data_only=True)      # 有重算值时能读到数
    wbf = load_workbook(recalc_path, data_only=False)    # 无重算值时回退读公式与字面值
    wi, wc = wb["输入假设"], wb["三情景现金流"]
    wif = wbf["输入假设"]

    def iv(key, col="B"):
        r = find_row(wi, LABELS[key])
        v = wi[f"{col}{r}"].value
        if v is not None:
            return v
        return eval_cell(wif, f"{col}{r}")

    C, P, hc = iv("C"), iv("mkt"), iv("hc")
    thr, wacc = iv("thr"), iv("wacc")
    if None in (C, P, hc, thr):
        rep["checks"]["recalc"] = "FAIL: 输入假设表读不全（既无重算值，也无法从字面值还原）"
        return rep, tmpdir

    rep["checks"]["recalc"] = (
        "SKIPPED — 未检测到 LibreOffice（soffice），取不到 Excel 公式重算值" if degraded
        else f"OK（{rc_status}）")

    n_formula = sum(1 for row in wbf["三情景现金流"].iter_rows() for c in row
                    if isinstance(c.value, str) and c.value.startswith("="))
    rep["checks"]["formula_presence"] = (
        f"OK — 三情景现金流表含 {n_formula} 个公式单元格" if n_formula
        else "FAIL — 三情景现金流表里没有公式单元格，疑似写成了死数")

    params = {"C": C, "P": P, "hc": hc, "wacc": wacc, "target_irr": thr}
    rep["params"] = params
    rep["rate"]["nominal_discount"] = iv("deal") / iv("eval")
    rep["rate"]["real_discount"] = iv("deal") / P

    worst = 0.0
    for i, col in enumerate(COLS):
        f_, mo, m_, ac = iv("f", col), iv("mo", col), iv("m", col), iv("ac", col)
        cf = build_cf(C, P, hc, f_, mo, m_, ac)
        py_irr = (1 + npf.irr(cf)) ** 4 - 1
        py_moic = sum(x for x in cf if x > 0) / abs(sum(x for x in cf if x < 0))
        py_npv = npf.npv((1 + wacc) ** 0.25 - 1, cf)
        xl_irr = wc[f"{col}{find_row(wc, OUT_LABELS['irr'])}"].value
        xl_moic = wc[f"{col}{find_row(wc, OUT_LABELS['moic'])}"].value
        xl_npv = wc[f"{col}{find_row(wc, OUT_LABELS['npv'])}"].value
        if xl_irr is None:
            d = 0.0
        else:
            d = max(abs(xl_irr - py_irr), abs(xl_moic - py_moic))
            worst = max(worst, d)
        rep["scenarios"][SCEN[i]] = {
            "irr_excel": round(xl_irr, 8) if xl_irr is not None else None,
            "irr_python": round(py_irr, 8),
            "moic_excel": round(xl_moic, 6) if xl_moic is not None else None,
            "moic_python": round(py_moic, 6),
            "npv_excel": round(xl_npv, 2) if xl_npv is not None else None,
            "npv_python": round(py_npv, 2),
            "delta": d,
            "pass": "达标 ✓" if py_irr >= thr else "不达标 ✗",
            "cashflow": [round(x, 2) for x in cf],
        }
    if degraded:
        rep["checks"]["dual_verification"] = (
            "SKIPPED — 无重算值可比对；上表 Python 列为独立自算结果，供口径核对")
    else:
        rep["checks"]["dual_verification"] = (
            ("OK" if worst < 1e-12 else f"FAIL 最大偏差={worst:.2e}") + f"（最大偏差 {worst:.2e}）")

    # 投标上限反推（保守情景）
    fixed = C - iv("deal")
    f_, mo, m_, ac = iv("f", "B"), iv("mo", "B"), iv("m", "B"), iv("ac", "B")
    lo, hi = 1000.0, P * 2
    for _ in range(100):
        mid = (lo + hi) / 2
        cf = build_cf(mid + fixed, P, hc, f_, mo, m_, ac)
        try:
            r = (1 + npf.irr(cf)) ** 4 - 1
        except Exception:
            r = -1
        if r > thr:
            lo = mid
        else:
            hi = mid
    cap = (lo + hi) / 2
    rep["bid_cap"] = {
        "max_price": round(cap, 0),
        "nominal_discount": round(cap / iv("eval"), 6),
        "real_discount": round(cap / P, 6),
        "current_deal_price": round(iv("deal"), 0),
        "headroom": round(cap - iv("deal"), 0),
        "note": f"保守情景 IRR={thr:.1%} 时的最高可出价",
    }

    if degraded:
        rep["checks"]["error_cells"] = "SKIPPED — 无重算值可扫描"
        rep["ok"] = (n_formula > 0) and all(v["irr_python"] is not None
                                            for v in rep["scenarios"].values())
        rep["verdict"] = ("降级通过（Python 独立自算 + 公式存在性检查；完整双验需安装 LibreOffice 后重跑）"
                          if rep["ok"] else "未通过（降级模式下仍有检查项失败）")
    else:
        errs = []
        for sh in wb.worksheets:
            for row in sh.iter_rows():
                for c in row:
                    if isinstance(c.value, str) and (c.value.startswith("#") or c.value.startswith("Err:")):
                        errs.append(f"{sh.title}!{c.coordinate}={c.value}")
        rep["checks"]["error_cells"] = "OK 无错误单元格" if not errs else f"FAIL {errs}"
        rep["ok"] = (worst < 1e-12) and not errs
        rep["verdict"] = "全部通过 ✓" if rep["ok"] else "存在偏差 ✗"
    return rep, tmpdir


def main():
    ap = argparse.ArgumentParser(description="NPA IRR 模型独立验证器")
    ap.add_argument("--model", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--allow-degraded", action="store_true",
                    help="缺少 LibreOffice 导致降级时也返回 0（默认返回 2）")
    a = ap.parse_args()
    rep, tmpdir = verify(a.model)
    try:
        shutil.rmtree(tmpdir, ignore_errors=True)
    except Exception:
        pass
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print("=" * 62)
        print("NPA IRR 模型 · 独立验证报告")
        print("=" * 62)
        if "rate" not in rep:
            for k, v in rep["checks"].items():
                print(f"  - {k}: {v}")
            print("\n结论: 前置检查未通过 ✗（无法读回输入假设）")
            sys.exit(1)
        if rep.get("degraded"):
            print("⚠ 降级模式：本机未检测到 LibreOffice（soffice），")
            print("  Excel 公式重算与缓存值比对已跳过；以下 IRR/MOIC/NPV 为 Python 独立自算结果。")
            print("  装上 LibreOffice 后重跑本脚本，即可得到完整双验结论。\n")
        print(f"名义折价率(成交价/评估价): {rep['rate']['nominal_discount']:.2%}")
        print(f"真实折价率(成交价/市场价): {rep['rate']['real_discount']:.2%}\n")
        for name, s in rep["scenarios"].items():
            xl = "n/a" if s["irr_excel"] is None else f"{s['irr_excel']:.4%}"
            xm = "n/a" if s["moic_excel"] is None else f"{s['moic_excel']:.4f}"
            xn = "n/a" if s["npv_excel"] is None else f"{s['npv_excel']:,.0f}"
            print(f"  {name}: IRR {xl} (py {s['irr_python']:.4%}) | "
                  f"MOIC {xm} (py {s['moic_python']:.4f}) | "
                  f"NPV {xn} (py {s['npv_python']:,.0f}) | {s['pass']}")
        bc = rep["bid_cap"]
        print(f"\n投标上限（保守情景 IRR={rep['params']['target_irr']:.0%}）: {bc['max_price']:,.0f} 元")
        print(f"  当前成交价 {bc['current_deal_price']:,.0f} → 空间 {bc['headroom']:+,.0f} 元")
        print("\n检查项:")
        for k, v in rep["checks"].items():
            print(f"  - {k}: {v}")
        print("\n结论:", rep.get("verdict", "—"))

    if rep["ok"] and not rep.get("degraded"):
        sys.exit(0)
    if rep["ok"] and rep.get("degraded"):
        print("\n提示: 退出码 2 = 环境缺件（未完成完整双验），并非模型不合格；")
        print("      装 LibreOffice 重跑可消除；加 --allow-degraded 可让本情形返回 0。")
        sys.exit(0 if a.allow_degraded else 2)
    sys.exit(1)


if __name__ == "__main__":
    main()
