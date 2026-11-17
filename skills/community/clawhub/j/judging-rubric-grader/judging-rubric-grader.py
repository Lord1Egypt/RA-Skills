# -*- coding: utf-8 -*-
"""赛事评审打分器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：UIBC 评审规范（rubric 加权）
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "judging-rubric-grader", "version": "1.1.0", "args": [{"name": "criteria", "help": "JSON: [{\"dim\":\"创新\",\"weight\":0.3}]", "required": False}, {"name": "scores", "help": "JSON: {\"创新\":90,...}", "required": False}, {"name": "pass_line", "help": "达标线(默认60)", "required": False}]}

class GateError(Exception):
    pass

def classify_judge(args):
    """按评审 rubric 多维加权打分。规则源：UIBC 评审规范（rubric 加权）。"""
    criteria = args.get('criteria')
    scores = args.get('scores')
    try:
        pass_line = float(args.get('pass_line') or 60)
    except Exception:
        pass_line = 60.0
    if not criteria or not scores:
        raise GateError("缺少必要参数：criteria(JSON维度权重) 与 scores(JSON各维度分) 必填")
    try:
        crit = json.loads(criteria) if isinstance(criteria, str) else criteria
        sc = json.loads(scores) if isinstance(scores, str) else scores
    except Exception:
        raise GateError("criteria / scores 须为合法 JSON")
    if not isinstance(sc, dict):
        raise GateError("scores 须为 JSON 对象（维度→分数映射，如 {\"创新\":90}）")
    if not isinstance(crit, list) or not crit:
        raise GateError("criteria 须为非零维度列表")
    weight_sum = sum(float(c.get('weight', 0)) for c in crit)
    total = 0.0
    per = []
    missing_dims = []
    for c in crit:
        dim = c.get('dim')
        w = float(c.get('weight', 0))
        if dim not in sc:
            missing_dims.append(dim)
        s = float(sc.get(dim, 0) if isinstance(sc, dict) else 0)
        total += s * w
        per.append({"dim": dim, "weight": w, "score": s, "weighted": round(s * w, 3)})
    total = round(total, 2)
    grade = 'S' if total >= 90 else ('A' if total >= 80 else ('B' if total >= 70 else ('C' if total >= pass_line else 'D')))
    passed = total >= pass_line
    warnings = []
    if missing_dims:
        # 从严推定：缺失维度按 0 分计（拉低总分），明示告警与补参建议，不静默处理
        warnings.append(
            "以下维度未提供分数，从严按 0 分计（会拉低总分）：%s；请补齐 scores 中对应维度后复核。"
            % "、".join(str(d) for d in missing_dims))
    if abs(weight_sum - 1.0) > 1e-9:
        warnings.append(
            "criteria 权重之和为 %s（≠1）：加权总分的基准可能失真，请核对维度权重后复核。"
            % round(weight_sum, 6))
    if not passed:
        warnings.append("未达达标线（%s）：机器门禁通过≠评审通过，建议复评或退回" % pass_line)
    return {"total": total, "grade": grade, "passed": passed, "pass_line": pass_line,
            "per_dimension": per,
            "warnings": warnings,
            "notes": ["加权总分 = Σ(维度分×权重)", "等级映射 S≥90/A≥80/B≥70/C≥达标线/D<达标线",
                      "评审工具为决策支持，最终裁定权归组委会（不可让渡）",
                      "打分须双评委独立进行后再合议；本输出仅为单一输入",
                      "范围限定（scoped）：分数仅反映 rubric 加权结果，不构成对作品安全性/正确性的整体背书"],
            "evidence": ["UIBC 评审规范·rubric"]}


def _run(args):
    res = classify_judge(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="judging-rubric-grader", description="赛事评审打分器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR（默认）")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB 45438-2025", "is_generated": True, "generator": META["slug"] + "@SynomosAI",
            "content_type": "decision_support_output",
            "label_note": "标识口径待核：输出由确定性规则代码计算，规则文本为 AI 辅助撰写",
            "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"criteria": "[{\"dim\":\"创新\",\"weight\":0.4},{\"dim\":\"工程\",\"weight\":0.3},{\"dim\":\"表达\",\"weight\":0.3}]", "scores": "{\"创新\":90,\"工程\":85,\"表达\":80}", "pass_line": "60"}, {"criteria": "[{\"dim\":\"创新\",\"weight\":0.5},{\"dim\":\"合规\",\"weight\":0.5}]", "scores": "{\"创新\":50,\"合规\":40}", "pass_line": "60"}, {"criteria": "[{\"dim\":\"创新\",\"weight\":0.5},{\"dim\":\"合规\",\"weight\":0.5}]", "scores": "{\"创新\":90}", "pass_line": "60"}]
        allok = True
        out_list = []
        for d in demos:
            try:
                res, rc = _run(dict(d))
                out_list.append({"tool": META["slug"], "input": d, "result": res, "rc": rc, "aigc_mark": AIGC})
            except GateError as e:
                allok = False
                out_list.append({"tool": META["slug"], "input": d, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC})
        print(json.dumps(out_list, ensure_ascii=False, indent=2))
        sys.exit(0 if allok else 2)
    args = {k: getattr(ns, k) for k in argnames}
    try:
        res, rc = _run(args)
    except GateError as e:
        ir = {"tool": META["slug"], "version": META["version"], "input": args, "errors": [str(e)], "rc": 2, "aigc_mark": AIGC}
        print(json.dumps(ir, ensure_ascii=False, indent=2))
        sys.exit(2)
    ir = {"tool": META["slug"], "version": META["version"], "input": args, "result": res, "rc": rc, "aigc_mark": AIGC}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)

if __name__ == "__main__":
    main()
