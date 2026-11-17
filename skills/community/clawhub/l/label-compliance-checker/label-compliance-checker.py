# -*- coding: utf-8 -*-
"""医疗器械标签合规核对器 — 零依赖单文件 CLI · JSON IR 输出。
规则源：《医疗器械说明书和标签管理规定》(总局令 第6号) 第10-11条
定位：决策支持工具，非权威结论，须人工复核。
"""
import argparse, json, sys

META = {"slug": "label-compliance-checker", "version": "1.0.0", "args": [{"name": "has_name", "help": "含产品名称: yes/no", "required": False}, {"name": "has_reg_no", "help": "含注册证号/备案号: yes/no", "required": False}, {"name": "has_manufacturer", "help": "含生产企业名称地址: yes/no", "required": False}, {"name": "has_indications", "help": "含适用范围/禁忌症: yes/no", "required": False}, {"name": "has_warnings", "help": "含警示/注意事项: yes/no", "required": False}, {"name": "has_lot", "help": "含批号/日期/有效期: yes/no", "required": False}, {"name": "has_udi", "help": "含UDI标识(若适用): yes/no", "required": False}]}

class GateError(Exception):
    pass

_YES = ('yes', 'true', '1')
_NO = ('no', 'false', '0')

def classify_label(args):
    """标签/说明书要素完整性核对。规则源：《医疗器械说明书和标签管理规定》(原总局令 第6号) 第10-11条。"""
    fields = {
        "has_name": "产品名称",
        "has_reg_no": "注册证号/备案号",
        "has_manufacturer": "生产企业名称/地址/联系方式",
        "has_indications": "适用范围/禁忌症",
        "has_warnings": "警示/注意事项/使用说明",
        "has_lot": "生产批号/生产日期/有效期",
        "has_udi": "UDI 标识（若适用）",
    }
    provided = [k for k in fields if args.get(k) not in (None, '')]
    if not provided:
        raise GateError("缺少必要参数：请至少提供一个 has_* 要素字段（取值 yes/no），否则无法核对")
    bad = [(k, args.get(k)) for k in provided
           if (args.get(k) or '').lower() not in _YES + _NO]
    if bad:
        raise GateError("取值非法（仅接受 yes/no）：%s；请核对输入" %
                        "、".join("%s=%r" % (k, v) for k, v in bad))
    explicit_no = [cn for k, cn in fields.items() if (args.get(k) or '').lower() in _NO]
    unknown = [cn for k, cn in fields.items() if args.get(k) in (None, '')]
    missing_fields = explicit_no + unknown
    compliant = len(missing_fields) == 0
    oblig = ["标签须含产品名称、注册证号、生产企业、批号等法定要素", "说明书须含适用范围、禁忌、警示、使用方法", "植入类须注明注意事项与随访要求"]
    notes = ["要素以《规定》第10条(标签)/第11条(说明书)为准", "UDI 标识依产品风险类别适用", "本核对为清单化自查，非合规证明",
             "要素齐全，但内容准确性仍须与注册证/技术要求一致核对"]
    warns = []
    if explicit_no:
        warns.append("存在缺失要素：" + "、".join(explicit_no) + "——上市前须补齐")
    if unknown:
        # 从严推定：未提供的字段从严按缺失处理，明示告警与补参建议，不静默按齐全输出
        warns.append("以下要素未提供核对信息，从严按缺失处理：" + "、".join(unknown) +
                     "；建议补齐后复核，避免核对范围不完整。")
    return {"compliant": compliant, "missing_fields": missing_fields, "obligations": oblig,
            "notes": notes, "evidence": ["说明书和标签管理规定 第6号 第10-11条"], "warnings": warns}


def _run(args):
    res = classify_label(args)
    warns = res.get("warnings") or []
    rc = 1 if warns else 0
    return res, rc

def main():
    p = argparse.ArgumentParser(prog="label-compliance-checker", description="医疗器械标签合规核对器（决策支持·须人工复核）")
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
        demos = [{"has_name": "yes", "has_reg_no": "yes", "has_manufacturer": "yes", "has_indications": "yes", "has_warnings": "yes", "has_lot": "yes", "has_udi": "yes"}, {"has_name": "yes", "has_reg_no": "no", "has_manufacturer": "yes", "has_indications": "no", "has_warnings": "no", "has_lot": "yes", "has_udi": "no"}, {"has_name": "yes", "has_reg_no": "yes", "has_manufacturer": "yes", "has_indications": "yes", "has_warnings": "yes", "has_lot": "yes"}]
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
