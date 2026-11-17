# -*- coding: utf-8 -*-
"""医疗器械分类与注册路径初判器 — 零依赖单文件 CLI · JSON IR 输出。规则源：EU MDR (EU) 2017/745 Annex VIII /《医疗器械分类目录》/ FDA 21 CFR 860"""
import argparse
import json
import sys

META = {"slug": "md-classification-route", "version": "1.0.0", "args": [{"name": "market", "help": "目标市场: cn/eu/us（默认 cn）"}, {"name": "invasive", "help": "是否侵入性: yes/no"}, {"name": "duration", "help": "侵入时长: transient/short_term/long_term（侵入性必填）"}, {"name": "active", "help": "是否有源: yes/no"}, {"name": "implant", "help": "是否植入: yes/no"}, {"name": "contact", "help": "接触部位: skin/mucosa/blood/cns/heart"}, {"name": "software", "help": "是否含驱动决策的软件: yes/no"}]}


class GateError(Exception):
    code = "E_RUNTIME"
    def __init__(self, msg, code=None):
        super().__init__(msg)
        if code:
            self.code = code


def classify_route(args):
    """分类与注册路径初判。规则源：EU MDR (EU) 2017/745 Annex VIII 分类规则 / 《医疗器械分类目录》/ FDA 21 CFR 860。"""
    market = (args.get("market") or "cn").lower()
    invasive = (args.get("invasive") or "").lower()
    duration = (args.get("duration") or "").lower()
    active = (args.get("active") or "").lower()
    implant = (args.get("implant") or "").lower()
    contact = (args.get("contact") or "").lower()
    software = (args.get("software") or "").lower()
    if market not in ("cn", "eu", "us"):
        raise GateError("--market 必须为 cn / eu / us 之一", "E_ENUM_INVALID")
    if not (invasive or active or software or implant):
        raise GateError("参数不足：至少提供 --invasive / --active / --software / --implant 之一", "E_INPUT_MISSING")
    if invasive in ("yes", "true") and duration not in ("transient", "short_term", "long_term"):
        raise GateError("侵入性器械必须提供 --duration（transient / short_term / long_term）", "E_INPUT_MISSING")

    eu, rule, cn_hint, us_hint = "", "", "", ""
    if software in ("yes", "true") and invasive not in ("yes", "true"):
        if contact in ("cns", "heart"):
            eu, rule = "III（推定）", "MDR Annex VIII Rule 11（提供诊断/治疗决策信息，且危及生命或导致不可逆损害）"
        else:
            eu, rule = "IIa（推定，多数情形）", "MDR Annex VIII Rule 11（提供诊断/治疗决策信息的软件）"
    elif invasive not in ("yes", "true"):
        if contact == "mucosa":
            eu, rule = "IIa（推定）", "MDR Annex VIII Rule 4（非侵入接触黏膜/受损皮肤）"
        else:
            eu, rule = "I（推定）", "MDR Annex VIII Rule 1（非侵入器械）"
    else:
        if implant in ("yes", "true") and duration == "long_term":
            eu, rule = "III（推定）", "MDR Annex VIII Rule 8（植入器械与长期侵入器械，一般归 III）"
        elif duration == "transient":
            eu, rule = "I 或 IIa（推定）", "MDR Annex VIII Rule 5/6（经自然腔道为非手术侵入；手术侵入为 IIa）"
        elif duration == "short_term":
            eu, rule = "IIa 或 IIb（推定）", "MDR Annex VIII Rule 5/6/7（短期侵入，视部位与是否手术）"
        else:
            eu, rule = "IIb 或 III（推定）", "MDR Annex VIII Rule 6/7/8（长期侵入）"

    if implant in ("yes", "true") or eu.startswith("III"):
        cn_hint = "三类（推定）"
    elif active in ("yes", "true") or duration in ("short_term", "long_term"):
        cn_hint = "二类或三类（推定）"
    else:
        cn_hint = "一类或二类（推定）"

    if eu.startswith("III"):
        us_hint = "Class III（推定，多为 PMA）"
    elif eu in ("IIa（推定，多数情形）", "I（推定）") and not active:
        us_hint = "Class I / II（推定，多为 510(k) 豁免或 510(k)）"
    else:
        us_hint = "Class II（推定，多为 510(k)）"

    route = {
        "eu": "MDR 技术文件 + 公告机构（NB）符合性评定；III 类须 NB + （如适用）临床评价",
        "cn": "按《分类目录》确定类别 → 一类备案 / 二类·三类注册 → 注册检验 → 技术审评",
        "us": "确定 I/II/III → 510(k) / De Novo / PMA → （如适用）FDA 注册与列名",
    }
    oblig = [
        "类别判定结果直接影响后续全部合规义务，必须以《分类目录》/MDR Annex VIII/FDA 分类法规原文核对",
        "初判不适用于创新/药械组合/边界产品，此类须走分类界定或 Pre-Sub",
        "同一产品在 cn / eu / us 的类别可能不同，不可互推",
    ]
    notes = [
        "本输出为「初判线索」，规则源条款号可回溯核对；正式分类以主管部门决定为准",
        "EU Annex VIII 共 22 条规则，本工具覆盖高频规则；特殊情形（纳米材料、药械组合、生物制品）未覆盖",
        "中国分类以《医疗器械分类目录》及分类界定文件为准，初判仅作检索方向",
    ]
    warns = []
    if eu.startswith("III") or cn_hint.startswith("三类"):
        warns.append("初判落在最高风险档，后续须公告机构/技术审评介入，建议尽早安排分类界定或 Pre-Sub 复核")
    if contact in ("cns", "heart"):
        warns.append("接触中枢神经/心脏属高风险接触部位，请复核是否触发更严格规则（如 Rule 11/12）")
    if software in ("yes", "true") and not contact:
        warns.append("输入不完整：软件器械未提供 --contact——若软件输出用于危及生命/不可逆损害情形的诊断或治疗决策"
                     "（接触中枢神经/心脏等），按 MDR Rule 11 可能升至 III 类（推定）；当前按 IIa（推定，多数情形）输出，"
                     "建议补参后复核。")
    if invasive in ("yes", "true") and duration == "long_term" and not implant:
        warns.append("输入不完整：长期侵入器械未提供 --implant——若为植入器械，按 MDR Annex VIII Rule 8 可能归 III 类（推定）；"
                     "当前按 IIb 或 III（推定）输出，建议补参后复核。")
    return {
        "market": market, "eu_class_hint": eu, "eu_rule": rule,
        "cn_class_hint": cn_hint, "us_class_hint": us_hint,
        "next_step": route[market] if market in route else "以目的国法规为准",
        "all_markets": route, "obligations": oblig, "notes": notes,
        "evidence": ["MDR (EU) 2017/745 Annex VIII", "《医疗器械分类目录》", "FDA 21 CFR 860"],
        "warnings": warns,
    }


def _call(args):
    fn_name = "classify_route"
    res = globals()[fn_name](args)
    return res


def main():
    p = argparse.ArgumentParser(prog="md-classification-route", description="医疗器械分类与注册路径初判器（决策支持·须人工复核）")
    for a in META["args"]:
        p.add_argument("--" + a["name"], required=False, default=None, help=a.get("help", ""))
    p.add_argument("--demo", action="store_true", help="跑内置冒烟案例")
    p.add_argument("--json", action="store_true", help="输出 JSON IR")
    ns = p.parse_args()
    names = [a["name"] for a in META["args"]]

    if ns.demo:
        ok = True
        for d in [{"market": "eu", "invasive": "yes", "duration": "long_term", "implant": "yes"}, {"market": "cn", "invasive": "no", "contact": "skin"}, {"market": "eu", "invasive": "no", "software": "yes", "contact": "cns"}]:
            try:
                res = _call(dict(d))
                rc = 1 if (res.get("warnings") or []) else 0
                print(json.dumps({"tool": META["slug"], "input": d, "result": res,
                                  "rc": rc, "error_code": None}, ensure_ascii=False))
            except GateError as e:
                ok = False
                print(json.dumps({"tool": META["slug"], "input": d, "errors": [str(e)],
                                  "rc": 2, "error_code": e.code}, ensure_ascii=False))
        sys.exit(0 if ok else 2)

    args = {k: getattr(ns, k) for k in names}
    if not any(v not in (None, "") for v in args.values()):
        p.print_help()
        sys.exit(0)
    try:
        res = _call(args)
    except GateError as e:
        print(json.dumps({"tool": META["slug"], "version": META["version"], "input": args,
                          "errors": [str(e)], "rc": 2, "error_code": e.code},
                         ensure_ascii=False, indent=2))
        sys.exit(2)
    rc = 1 if (res.get("warnings") or []) else 0
    ir = {"tool": META["slug"], "version": META["version"], "input": args,
          "result": res, "rc": rc, "error_code": None,
          "aigc_mark": {"standard": "GB 45438-2025", "is_generated": True,
                        "generator": META["slug"] + "@SynomosAI",
                        "content_type": "decision_support_output",
                        "disclaimer": "决策支持非权威结论，须人工复核；以官方最新文件为准"}}
    print(json.dumps(ir, ensure_ascii=False, indent=2))
    sys.exit(rc)


if __name__ == "__main__":
    main()
