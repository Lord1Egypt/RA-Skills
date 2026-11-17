#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lgd-fin-guard — LGD 三律在本域的合规守门器（零依赖）。
把"有籍·有证·有门禁"翻译进本域合规语言，对 AI 系统做三律自评与门禁判定。
理论真源：LGD 凡自治之物三律（SynomosAI Governance Line）。"""
import argparse, json, sys

RUBRIC = json.loads(r"""{"LGD-I 有籍": {"持牌身份登记": ["牌照", "备案", "license", "持牌", "资质"], "版本留痕": ["版本", "version", "回滚", "快照", "模型版本"], "数据来源登记": ["行情", "客户数据", "来源", "source", "数据血缘", "训练集"], "责任主体登记": ["持牌机构", "合规官", "责任", "问责", "accountability"]}, "LGD-II 有证": {"01 身份证据": ["牌照", "备案号", "did", "登记文件"], "02 数据证据": ["数据血缘", "外部审计", "哈希", "hash", "数据集证明"], "03 验证证据": ["回测", "压力测试", "benchmark", "指标", "评测"], "04 行为边界证据": ["反洗钱", "禁止无资质荐股", "红线", "适当性"], "05 变更证据": ["变更日志", "changelog", "评估记录"], "06 签发证据": ["合规官签发", "时间戳", "签发人"]}, "LGD-III 有门禁": {"触发门禁": ["高风险交易", "对外荐股", "大额"], "评审门禁": ["合规双签", "风控复核"], "放行门禁": ["限额", "分级审批"], "复盘门禁": ["交易复盘", "监管报送"]}}""")

def guess(text):
    t = (text or "").lower()
    out = {}
    for law, items in RUBRIC.items():
        for item, hints in items.items():
            out[f"{law}::{item}"] = "yes" if any(h.lower() in t for h in hints) else "no"
    return out

def score(answers):
    res = {}
    for law, items in RUBRIC.items():
        tot = len(items); yes = 0; part = 0
        for item in items:
            v = str(answers.get(f"{law}::{item}", "no")).lower()
            if v in ("yes", "y", "true", "1"): yes += 1
            elif v in ("partial", "p", "半"): part += 1
        res[law] = round((yes + 0.5 * part) / tot * 100)
    return res

def missing(answers):
    m = []
    for law, items in RUBRIC.items():
        for item in items:
            v = str(answers.get(f"{law}::{item}", "no")).lower()
            if v in ("no", "n", "false", "0", ""):
                m.append(f"{law} · {item}")
    return m

def gate(scores):
    return all(s >= 60 for s in scores.values())

def main():
    ap = argparse.ArgumentParser(description="lgd-fin-guard · LGD 三律本域守门器")
    ap.add_argument("--rubric", action="store_true", help="打印本域三律 rubric")
    ap.add_argument("--system", help="系统描述文本（启发式自评）")
    ap.add_argument("--answers", help="正式评分 JSON：键为 '<律>::<条目>'，值 yes/partial/no")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    a = ap.parse_args()
    if a.rubric:
        print(json.dumps(RUBRIC, ensure_ascii=False, indent=2)); return
    if not a.system and not a.answers:
        print("用法：--system <文本> 启发式自评 | --answers <JSON> 正式评分 | --rubric 看 rubric", file=sys.stderr)
        sys.exit(2)
    if a.answers:
        try:
            ans = json.loads(a.answers)
        except Exception as e:
            print(f"answers JSON 解析失败：{e}", file=sys.stderr); sys.exit(2)
    else:
        ans = guess(a.system)
    scores = score(ans)
    miss = missing(ans)
    ok = gate(scores)
    if a.json:
        print(json.dumps({"scores": scores, "gate_pass": ok, "missing": miss}, ensure_ascii=False, indent=2))
    else:
        print(f"=== lgd-fin-guard · LGD 三律本域守门 ===")
        for law, s in scores.items():
            print("  " + law + "：" + str(s) + "%")
        print("  门禁判定：" + ("PASS ✅ 可放行" if ok else "FAIL ⛔ 缺证据不可放行"))
        if miss:
            print("  待补证据：")
            for x in miss: print("    - " + x)
        else:
            print("  三律证据齐备 ✅")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
