#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""risk_matrix.py — ISO 14971 risk-matrix calculator and RM-file completeness check.

Modes
-----
  matrix                                   print the reference 5x5 matrix
  assess -s S -p P [--rs RS --rp RP]       score one risk (and an optional residual)
  options                                  risk-control option hierarchy (ISO 14971:2019, 7.1)
  check <file>                             check a risk-management file for the
                                           elements ISO 14971:2019 requires

Reference matrix only — ISO 14971:2019 4.4 requires the *manufacturer* to define,
in its risk management plan, the policy for determining acceptable risk. This
tool ships one common 5x5 convention and is explicit that it is a convention.

Stdlib only. Exit code 0 = ok, 1 = findings/blocking, 2 = usage error.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SEVERITY = {
    1: ("可忽略 Negligible", "无伤害或不适"),
    2: ("轻度 Minor", "可逆的轻微伤害，无需专业医疗干预"),
    3: ("严重 Serious", "需要专业医疗干预的伤害"),
    4: ("危重 Critical", "不可逆伤害或危及生命"),
    5: ("灾难性 Catastrophic", "导致死亡"),
}
PROBABILITY = {
    1: ("极不可能 Improbable", "≤1e-6 / 器械寿命"),
    2: ("罕见 Remote", "1e-5 量级"),
    3: ("偶然 Occasional", "1e-4 量级"),
    4: ("很可能 Probable", "1e-3 量级"),
    5: ("频繁 Frequent", "≥1e-2 / 高于 1e-3"),
}
BANDS = [
    ("L", "低 / 可接受", "记录并保持监测；剩余风险按 ISO 14971:2019 7.3 评价"),
    ("M", "中 / ALARP", "须降到合理可行最低（ALARP）；措施须验证有效，评价剩余风险"),
    ("H", "高 / 不可接受", "重新设计或加强防护措施；若剩余风险仍不可接受，须做获益-风险分析（7.4）"),
]


def band(score: int):
    if score <= 4:
        return BANDS[0]
    if score <= 9:
        return BANDS[1]
    return BANDS[2]


CONTROL_OPTIONS = [
    ("a", "固有安全设计 (inherently safe design and manufacture)",
     "从设计上消除危险或降低风险——优先级最高，最可靠"),
    ("b", "器械本身或制造过程中的防护措施 (protective measures)",
     "如屏蔽、联锁、冗余、灭菌工艺参数控制；不依赖使用者行为"),
    ("c", "安全信息与培训 (information for safety and training)",
     "标签、说明书、警示语、培训——最弱的措施，不得单独用于高风险项"),
]

#: (clause, element, keyword alternatives — any hit counts as present, critical?)
RM_ELEMENTS = [
    ("4.4", "风险管理计划 Risk management plan",
     ["risk management plan", "风险管理计划"], True),
    ("4.5", "风险管理文件 Risk management file",
     ["risk management file", "风险管理文件", "风险管理文档"], True),
    ("5.2", "预期用途与可合理预见的误用 Intended use & foreseeable misuse",
     ["intended use", "foreseeable misuse", "预期用途", "可合理预见的误用"], True),
    ("5.3", "与安全有关的特征 Identification of safety characteristics",
     ["characteristics related to safety", "safety characteristics",
      "与安全有关的特征", "安全有关特征"], False),
    ("5.4", "危害与危险情况识别 Hazards & hazardous situations",
     ["hazard", "hazardous situation", "危害", "危险情况"], True),
    ("5.5", "风险估计 Risk estimation",
     ["risk estimation", "风险估计"], True),
    ("6", "风险评价 Risk evaluation",
     ["risk evaluation", "风险评价"], True),
    ("7.1", "风险控制方案分析 Risk control option analysis",
     ["risk control option", "control option analysis", "风险控制方案", "控制方案分析"], True),
    ("7.2", "风险控制措施实施与验证 Implementation of risk control measures",
     ["implementation of risk control", "风险控制措施的实施", "实施并验证"], True),
    ("7.3", "剩余风险评价 Residual risk evaluation",
     ["residual risk evaluation", "剩余风险评价", "剩余风险"], True),
    ("7.4", "获益-风险分析 Benefit-risk analysis",
     ["benefit-risk", "benefit/risk", "获益-风险", "获益风险"], False),
    ("7.5", "控制措施引发的风险 Risks arising from risk control measures",
     ["arising from risk control", "risks from risk control",
      "控制措施引发的风险", "控制措施产生的风险"], False),
    ("7.6", "风险控制的完整性 Completeness of risk control",
     ["completeness of risk control", "风险控制的完整性", "完整性检查"], False),
    ("8", "整体剩余风险评价 Evaluation of overall residual risk",
     ["overall residual risk", "整体剩余风险"], True),
    ("9", "风险管理评审 Risk management review",
     ["risk management review", "风险管理评审"], True),
    ("10", "生产和生产后活动 Production and post-production activities",
     ["production and post-production", "post-production",
      "生产和生产后", "生产后活动", "生产和售后"], True),
]


def cmd_matrix() -> int:
    print("ISO 14971 参考风险矩阵（5x5，示例准则）")
    print("  单元格 = 严重度 x 概率 → 风险等级；L 低 / M 中(ALARP) / H 高(不可接受)\n")
    header = "        " + "".join(f"{p:>10}" for p in PROBABILITY)
    print(header)
    for s in range(5, 0, -1):
        row = f"  S{s}   "
        for p in range(1, 6):
            row += f"{band(s * p)[0]:>10}"
        print(row)
    print("\n  概率轴：" + " / ".join(f"{k}={v[0].split()[0]}" for k, v in PROBABILITY.items()))
    print("  严重度轴：" + " / ".join(f"{k}={v[0].split()[0]}" for k, v in SEVERITY.items()))
    print("\n  ⚠️ 这是**示例**矩阵。ISO 14971:2019 4.4 要求由制造商在风险管理计划中自定"
          "\n     风险可接受性准则；正式文件必须引用企业自己的计划，不是本表。")
    return 0


def cmd_assess(s: int, p: int, rs: int | None, rp: int | None) -> int:
    if not (1 <= s <= 5 and 1 <= p <= 5):
        print("severity / probability must be 1..5")
        return 2
    score = s * p
    code, label, action = band(score)
    print("ISO 14971 风险估计\n" + "-" * 60)
    print(f"  初始风险：严重度 S{s} ({SEVERITY[s][0]}) × 概率 P{p} ({PROBABILITY[p][0]})")
    print(f"  风险评分：{s} × {p} = {score}")
    print(f"  风险等级：{code} — {label}")
    print(f"  处置要求：{action}")

    print("\n  词汇链自查（ISO 14971:2019 第 3 章术语，缺一环即分析不完整）：")
    for step in ("危害 hazard", "→ 可预见的事件序列 sequence of events",
                 "→ 危险情况 hazardous situation", "→ 伤害 harm"):
        print(f"    {step}")

    rc = 0
    if rs is not None and rp is not None:
        rscore = rs * rp
        rcode, rlabel, _ = band(rscore)
        print("\n  剩余风险（措施之后）："
              f"S{rs} × P{rp} = {rscore} → {rcode} — {rlabel}")
        if rcode == "H":
            print("    → 剩余风险不可接受：必须继续降低；若确实无法降低，"
                  "须按 7.4 做获益-风险分析并记录结论")
            rc = 1
        elif rcode == "M" and code == "L":
            print("    → 注意：措施后风险等级反而升高，核对赋值是否写反")
            rc = 1
        elif rscore > score:
            print("    → 注意：剩余风险高于初始风险，核对赋值是否写反")
            rc = 1
        elif rscore == score:
            print("    → 注意：剩余风险与初始风险同值，说明未识别到有效降险措施")
            rc = 1
    elif code == "H":
        print("\n  提示：高风险项应给出措施后的剩余风险（--rs / --rp）以完成 7.3 评价")
    return rc


def cmd_options() -> int:
    print("ISO 14971:2019 §7.1 风险控制方案分析（优先级自上而下）\n")
    for code, name, why in CONTROL_OPTIONS:
        print(f"  ({code}) {name}\n      {why}")
    print("\n  规则：方案 (c) 安全信息不得作为降低高风险项的唯一手段；"
          "\n        每个控制措施都须验证其实施与有效性（§7.2）。")
    return 0


def cmd_check(path: str) -> int:
    p = Path(path)
    if not p.exists():
        sys.exit(f"no such file: {path}")
    raw = p.read_text(encoding="utf-8-sig", errors="replace")
    low = raw.lower()

    present, missing_critical, missing_optional = [], [], []
    for clause, element, kws, critical in RM_ELEMENTS:
        hit = next((k for k in kws if k.lower() in low), None)
        if hit:
            present.append((clause, element, hit))
        elif critical:
            missing_critical.append((clause, element))
        else:
            missing_optional.append((clause, element))

    print(f"ISO 14971:2019 风险管理文件完整性自查 — {p.name} ({len(raw)} chars)\n")
    print(f"{'条款':<6} {'要素':<52} 状态")
    print("-" * 84)
    for clause, element, _ in sorted(present, key=lambda x: [float(n) for n in re.findall(r'\d+(?:\.\d+)?', x[0])]):
        print(f"{clause:<6} {element[:50]:<52} ✅ 已覆盖")
    for clause, element in missing_critical:
        print(f"{clause:<6} {element[:50]:<52} ❌ 缺失（关键）")
    for clause, element in missing_optional:
        print(f"{clause:<6} {element[:50]:<52} ⚠️ 未见")

    print("-" * 84)
    print(f"已覆盖 {len(present)} / {len(RM_ELEMENTS)}；"
          f"关键缺失 {len(missing_critical)}；非关键未见 {len(missing_optional)}")
    if missing_critical:
        print("\n关键缺失要素（逐条补齐后再定稿）：")
        for clause, element in missing_critical:
            print(f"  - [{clause}] {element}")
        return 1
    print("\n关键要素齐备。注意：关键词命中只说明文档'提到了'该要素，"
          "\n不等同于该要素已实质完成——仍需人工核对内容。")
    return 0


def main(argv) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    cmd = argv[1]
    if cmd == "matrix":
        return cmd_matrix()
    if cmd == "options":
        return cmd_options()
    if cmd == "check" and len(argv) == 3:
        return cmd_check(argv[2])
    if cmd == "assess":
        args = argv[2:]
        vals = {}
        i = 0
        while i < len(args):
            a = args[i]
            if a in ("-s", "--severity", "-p", "--probability", "--rs", "--rp"):
                if i + 1 >= len(args):
                    print(f"missing value for {a}")
                    return 2
                vals[a.lstrip("-")] = args[i + 1]
                i += 2
            else:
                print(f"unknown argument: {a}")
                return 2
        try:
            s = int(vals["s"] if "s" in vals else vals["severity"])
            p = int(vals["p"] if "p" in vals else vals["probability"])
            rs = int(vals["rs"]) if "rs" in vals else None
            rp = int(vals["rp"]) if "rp" in vals else None
        except (KeyError, ValueError):
            print("assess requires -s <1-5> and -p <1-5>")
            return 2
        return cmd_assess(s, p, rs, rp)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
