# -*- coding: utf-8 -*-
"""人类遗传资源事项路径判定器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《人类遗传资源管理条例》(国务院令717号)+实施细则(2023-07-01施行) 第8-22条
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "hgrac-route-checker", "version": "1.0.1", "args": [{"name": "action", "help": "事项: collect/store/use/transfer/coop", "required": False}, {"name": "foreign_involved", "help": "是否涉外: yes/no", "required": False}, {"name": "scale", "help": "重要种类/累计人份: big/normal", "required": False}]}

class GateError(Exception):
    pass

def classify_hgrac(args):
    """人类遗传资源事项路径判定。规则源：人类遗传资源管理条例(国务院令717号)+实施细则(2023-07-01施行) 第8-22条。"""
    action = (args.get('action') or '').lower()      # collect/store/use/transfer/coop
    foreign = args.get('foreign_involved')           # 是否涉外: yes/no
    scale = args.get('scale')                        # 重要种类/累计人份: big/normal
    if foreign is not None and foreign not in ('yes', 'no'):
        raise GateError("foreign_involved 取值必须为 yes/no（当前：%s）" % foreign)
    if scale is not None and scale not in ('big', 'normal'):
        raise GateError("scale 取值必须为 big/normal（当前：%s）" % scale)
    warns = []
    if action in ('collect', '采集'):
        ev = ["条例 第8-11条"]
        # 输入不足 → 从严推定：枚举未知参数补全后可达路径，取义务最重者
        f_cands = ['yes', 'no'] if foreign is None else [foreign]
        s_cands = ['big', 'normal'] if scale is None else [scale]
        possible = set()
        for f in f_cands:
            for s in s_cands:
                possible.add("审批（科技部）" if (s == 'big' or f == 'yes') else "备案")
        naive = "审批（科技部）" if (scale == 'big' or foreign == 'yes') else "备案"
        strict = "审批（科技部）" if "审批（科技部）" in possible else "备案"
        lenient = "备案" if "备案" in possible else "审批（科技部）"
        route = strict
        if strict != naive:
            missing = [n for n, v in (("foreign_involved", foreign), ("scale", scale)) if v is None]
            warns.append(
                "输入不完整：未提供 %s；官方对采集按「重要种类/累计人份规模」与「是否涉外」区分审批与备案，"
                "建议补齐后复核。" % " / ".join(missing))
            if strict != lenient:
                warns.append(
                    "路径不确定（可能区间 %s～%s）：已按从严推定取『%s』（义务最重者），"
                    "实际路径可能更宽松；请补齐参数后复核。" % (lenient, strict, strict))
    elif action in ('store', '保藏'):
        route, ev = "审批（保藏审批）", ["条例 第12-13条"]
    elif action in ('use', '利用'):
        route, ev = "备案 / 审批（依规模涉外）", ["条例 第14-16条"]
        if scale is None and foreign is None:
            warns.append(
                "输入不完整：未提供 scale / foreign_involved；「利用」的备案或审批路径依规模与涉外情况而定，"
                "请补齐后复核。")
    elif action in ('transfer', '对外提供', 'coop', '国际合作'):
        route, ev = "审批（对外提供/国际合作科学研究）", ["条例 第17-22条"]
    else:
        raise GateError("action 必填：collect/store/use/transfer/coop")
    if foreign in ('yes',):
        warns.append("涉外环节须通过国际合作行政审批，不得私下对外提供")
    oblig = [f"路径：{route}", "提交材料清单（依托单位+伦理+合同）", "取得批件/备案号后方可实施"]
    return {"route": route, "obligations": oblig,
            "notes": ["生命科学企业涉外必踩", "错一步涉行政处罚",
                      "输入不足时按从严推定（取可能路径中义务最重者），不静默按宽松路径输出"],
            "evidence": ev, "warnings": warns}


def _run(args):
    res = classify_hgrac(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="hgrac-route-checker", description="人类遗传资源事项路径判定器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    ns = p.parse_args()
    argnames = [a["name"] for a in META["args"]]
    AIGC = {"standard": "GB45438-2025", "is_generated": False, "generator": META["slug"] + "@SynomosAI",
             "content_type": "decision_support_output", "disclaimer": "决策支持非权威结论，须人工复核"}
    if ns.demo:
        demos = [{"action": "collect", "scale": "big"}, {"action": "store"}, {"action": "transfer", "foreign_involved": "yes"}]
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
