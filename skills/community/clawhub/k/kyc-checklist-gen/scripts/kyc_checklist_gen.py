import argparse, json, sys

LISTS = {
    "personal": ["身份证明（身份证/护照在有效期内）", "地址证明（近3个月账单）",
                 "职业与收入来源说明", "银行账户流水（视机构要求）", "税收居民身份声明（CRS）"],
    "corporate": ["营业执照与最新章程", "受益所有人（UBO）识别材料（持股≥25%）",
                  "法定代表人身份证明与授权委托书", "公司银行账户证明",
                  "业务实质与资金来源说明", "制裁名单与PEP筛查授权"],
}

def main():
    ap = argparse.ArgumentParser(description="kyc-checklist-gen · KYC 材料齐备清单（零依赖）")
    ap.add_argument("--type", choices=["personal", "corporate"], default="personal")
    ap.add_argument("--have", help="已具备材料编号，逗号分隔，如 1,2,3")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    items = LISTS[a.type]
    have = set()
    if a.have:
        for tok in a.have.split(","):
            tok = tok.strip()
            if tok.isdigit() and 1 <= int(tok) <= len(items):
                have.add(int(tok))
    missing = [i for i in range(1, len(items) + 1) if i not in have]
    score = round(100 * (len(items) - len(missing)) / len(items))
    if a.json:
        print(json.dumps({"type": a.type, "complete": not missing, "score": score,
                          "missing_no": missing, "missing": [items[i-1] for i in missing]},
                         ensure_ascii=False, indent=2))
    else:
        label = "个人" if a.type == "personal" else "企业"
        print("KYC 清单（%s）：%d/%d 齐备，完成度 %d%%" % (label, len(items) - len(missing), len(items), score))
        for i, it in enumerate(items, 1):
            print(("  [x] " if i in have else "  [ ] ") + str(i) + ". " + it)
        if missing:
            print("  判定：FAIL 缺 " + "、".join(str(i) for i in missing) + " 号材料")
        else:
            print("  判定：PASS 材料齐备")
    sys.exit(0 if not missing else 1)

if __name__ == "__main__":
    main()
