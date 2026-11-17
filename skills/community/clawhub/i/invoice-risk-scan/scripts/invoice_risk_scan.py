import argparse, json, re, sys

TAXID = re.compile(r"^[0-9A-Z]{15}(?:[0-9A-Z]{3})?(?:[0-9A-Z]{2})?$")

def main():
    ap = argparse.ArgumentParser(description="invoice-risk-scan · 发票要素风险扫描（零依赖）")
    ap.add_argument("--taxid", help="销售方纳税人识别号")
    ap.add_argument("--amount", type=float, help="价税合计金额")
    ap.add_argument("--date", help="开票日期 YYYY-MM-DD")
    ap.add_argument("--kind", choices=["zhuan", "pu", "e"], default=None, help="专票/普票/电子")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.taxid is None and a.amount is None and a.date is None:
        ap.error("至少提供 --taxid/--amount/--date 之一")
    problems, checks = [], []
    if a.taxid is not None:
        ok = bool(TAXID.match(a.taxid.strip()))
        checks.append({"check": "纳税人识别号格式(15/18/20位大写字母数字)", "ok": ok})
        if not ok:
            problems.append("税号格式不符：应为15/18/20位大写字母数字")
    if a.amount is not None:
        ok = a.amount > 0
        checks.append({"check": "金额为正", "ok": ok})
        if not ok:
            problems.append("金额必须大于0")
    if a.date is not None:
        ok = bool(re.match(r"^\d{4}-\d{2}-\d{2}$", a.date))
        if ok:
            y = int(a.date[:4])
            ok = 2000 <= y <= 2035
        checks.append({"check": "开票日期格式与年份合理", "ok": ok})
        if not ok:
            problems.append("日期需为 YYYY-MM-DD 且年份合理")
    if a.json:
        print(json.dumps({"pass": not problems, "checks": checks, "problems": problems}, ensure_ascii=False, indent=2))
    else:
        for c in checks:
            print(("  [PASS] " if c["ok"] else "  [FAIL] ") + c["check"])
        print("  判定：" + ("PASS" if not problems else "FAIL"))
        for p in problems:
            print("    - " + p)
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
