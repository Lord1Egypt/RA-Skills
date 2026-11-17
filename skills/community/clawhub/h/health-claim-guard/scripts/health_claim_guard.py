import argparse, json, sys

BANNED = ["根治", "治愈", "疗效", "无副作用", "最安全", "包治", "药到病除", "彻底摆脱"]
NEED_NOTE = ("保健食品", "益生菌", "维生素", "鱼油", "蛋白粉")

def main():
    ap = argparse.ArgumentParser(description="health-claim-guard · 健康宣称合规扫描（零依赖）")
    ap.add_argument("--text", required=True, help="宣传文案")
    ap.add_argument("--kind", help="产品类别，如 保健食品")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    t = a.text
    hits = [k for k in BANNED if k in t]
    problems = []
    if hits:
        problems.append("违规宣称（涉疾病治疗/绝对化用语）：" + "、".join(hits))
    if a.kind and any(k in a.kind for k in NEED_NOTE):
        if "不能代替药物" not in t:
            problems.append("保健食品类宣传须含「本品不能代替药物」警示语")
    if a.json:
        print(json.dumps({"pass": not problems, "banned_hits": hits, "problems": problems},
                         ensure_ascii=False, indent=2))
    else:
        print("  判定：" + ("PASS 宣称合规" if not problems else "FAIL 需整改"))
        for p in problems:
            print("    - " + p)
        print("  依据：广告法/食品安全法禁止普通食品与保健食品宣称疾病预防治疗功能。")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
