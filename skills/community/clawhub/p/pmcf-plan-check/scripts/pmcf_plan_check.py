#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PMCF 计划完整性检查器（零依赖 / 确定性 / JSON IR / 修复回执）
# 要素依据：MDCG 2020-7 Annex I / MDCG 2019-8 核心要素提炼，以官方最新版本为准。
import argparse, json, re, sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

REQUIRED = [
    ("objectives", "目标（objectives）", None),
    ("methods", "方法（methods）", lambda v: bool(re.search(r"文献|survey|调查|登记|registry|真实世界|real.?world|上市后|PMS", v, re.I))),
    ("endpoints", "终点（endpoints）", None),
    ("follow_up_period", "随访期（follow-up period）", lambda v: bool(re.search(r"\d", v))),
    ("statistical_plan", "统计考量（statistical plan）", lambda v: bool(re.search(r"样本|统计|sample|statist|目标值|置信|power|检验|alpha", v, re.I))),
    ("benefit_risk_linkage", "获益-风险关联（benefit-risk linkage）", None),
    ("pms_linkage", "PMS 衔接（PMS linkage）", None),
    ("cer_update_trigger", "CER 更新触发（CER update trigger）", None),
    ("responsible_person", "责任人（responsible person）", None),
    ("timeline", "时间表（timeline）", lambda v: bool(re.search(r"\d|季度|月|Q[1-4]|阶段", v, re.I))),
]
METHOD_HINT = "方法建议覆盖两类以上：文献综述 / 问卷调查 / 登记库 / 真实世界数据 / 上市后监督数据"


def main():
    ap = argparse.ArgumentParser(prog="pmcf_plan_check", description="PMCF 计划核心要素完整性检查（MDCG 2020-7/2019-8 口径）")
    ap.add_argument("--plan", help="JSON 计划文件路径（键=要素名）")
    ap.add_argument("--fields", action="append", default=[], help="k=v，可重复")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    plan = {}
    if a.plan:
        try:
            with open(a.plan, encoding="utf-8-sig") as fh:
                plan = json.load(fh)
        except Exception as e:
            print(json.dumps({"errors": [{"code": "PMCF_E_PLAN_FILE", "subject": a.plan,
                                          "evidence": str(e), "fixes": ["提供可读的 JSON 文件"]}]},
                             ensure_ascii=False))
            sys.exit(2)
    for f in a.fields:
        if "=" not in f:
            ap.error("--fields 需要 k=v 形式")
        k, v = f.split("=", 1)
        plan[k.strip()] = v.strip()
    if not plan:
        print(json.dumps({"errors": [{"code": "PMCF_E_NO_INPUT", "subject": "input",
                                      "evidence": "未提供 --plan 或 --fields",
                                      "fixes": ["任选其一提供计划内容"]}]}, ensure_ascii=False))
        sys.exit(1)
    missing, weak = [], []
    present = 0
    for key, label, qfn in REQUIRED:
        val = str(plan.get(key, "") or "").strip()
        if not val:
            missing.append({"code": "PMCF_E_MISSING_FIELD", "subject": key, "evidence": label,
                            "fixes": ["补充「%s」内容（参照 MDCG 2020-7 Annex I 要素）" % label]})
        else:
            present += 1
            if qfn is not None and not qfn(val):
                weak.append({"code": "PMCF_E_WEAK_FIELD", "subject": key, "evidence": val[:60],
                             "fixes": ["「%s」内容存疑，请补充可核验的量化描述" % label]})
    score = "%d/10" % present
    basis = ["MDCG 2020-7（PMCF 计划模板 Annex I）", "MDCG 2019-8（PMCF 方法摘要）",
             "NMPA 上市后随访要求参照国内指导原则，以官方最新为准"]
    if a.json:
        print(json.dumps({"completeness": score, "missing": missing, "weak": weak, "basis": basis},
                         ensure_ascii=False, indent=2))
    else:
        print("完整性 %s" % score)
        for m in missing:
            print("  缺失：%s -> %s" % (m["subject"], m["fixes"][0]))
        for w in weak:
            print("  存疑：%s（%s）" % (w["subject"], w["evidence"]))
        if present == 10:
            print("  %s" % METHOD_HINT)
        print("  依据：" + "；".join(basis))
    sys.exit(0 if (not missing and not weak) else 1)


if __name__ == "__main__":
    main()
