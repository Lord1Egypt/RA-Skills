import argparse, json, sys

def main():
    ap = argparse.ArgumentParser(description="loan-rate-disclosure · 借贷年化利率披露校验（零依赖）")
    ap.add_argument("--rate", type=float, help="对外报价利率（百分比，如 24 表示 24%%）")
    ap.add_argument("--base", type=float, default=3.85, help="参考基准利率LPR（百分比，默认3.85）")
    ap.add_argument("--text", help="披露文案（校验是否含年化口径）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.rate is None and not a.text:
        ap.error("至少提供 --rate 或 --text")
    problems, checks = [], []
    if a.text:
        ok = ("年化" in a.text)
        checks.append({"check": "披露含年化利率口径", "ok": ok})
        if not ok:
            problems.append("未按年化口径披露（监管要求明示年化利率）")
    if a.rate is not None:
        mult = a.rate / a.base if a.base else 0
        cap = 4 * a.base
        over = a.rate > cap
        checks.append({"check": "利率/基准倍数", "value": round(mult, 2), "cap_multiple": 4, "ok": not over})
        if over:
            problems.append("报价 %.2f%% 超过基准 %.2f%% 的4倍上限（%.2f%%），触及民间借贷司法保护上限风险" % (a.rate, a.base, cap))
    if a.json:
        print(json.dumps({"pass": not problems, "checks": checks, "problems": problems}, ensure_ascii=False, indent=2))
    else:
        for c in checks:
            mark = "  [PASS] " if c.get("ok") else "  [FAIL] "
            extra = "" if c.get("value") is None else "  = " + str(c["value"])
            print(mark + c["check"] + extra)
        print("  判定：" + ("PASS 可披露" if not problems else "FAIL 需整改"))
        for p in problems:
            print("    - " + p)
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
