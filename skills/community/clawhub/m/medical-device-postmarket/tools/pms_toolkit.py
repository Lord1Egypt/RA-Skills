#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pms_toolkit.py — 医械上市后监管本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  obligations --region <us|eu|cn|jp>   四市场 PMS 义务对照
  report      --region <us|eu|cn|jp>   不良事件报告时限速查
  plan                                  PMS 计划框架（Markdown 骨架）
  psur        --class <I|IIa|IIb|III>   PSUR 撰写框架
  recall                                FSCA/召回流程
  --help                                查看帮助
"""

import argparse
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- obligations

OBLIGATIONS = {
    "us": [
        "不良事件报告（21 CFR 803）：致死 30 日历日、严重伤害/故障 90 日历日，eMDR 提交入 MAUDE",
        "纠正与移除报告（21 CFR 806）：召回/纠正报告",
        "注册与列名更新（21 CFR 807）",
        "趋势报告（如有）",
        "上市后研究/监测（FDA 要求时）",
    ],
    "eu": [
        "警戒（Vigilance）：严重事件报告（死亡/严重伤害 10 天、其他 15 天，MDCG 指南）",
        "FSCA（现场安全纠正）：触发即报告主管当局 + 用户通知",
        "PSUR：IIb 至少每 2 年、III 类至少每年（MDCG 2022-21）",
        "PMCF：上市后临床跟踪计划与报告（MDCG 2020-7/8）",
        "EUDAMED 报告（逐步上线）",
        "PMS 计划：所有器械须有（含 I/IIa 的 PMS 报告）",
    ],
    "cn": [
        "不良事件监测（2018 年 1 号令）：获证产品不良事件监测与报告",
        "报告时限：死亡/严重伤害按法规时限报告（监测系统）",
        "再评价：定期风险评价 + 临床评价更新",
        "召回：主动召回 + 报告（责令召回情形）",
        "年度自查报告（部分类别）",
    ],
    "jp": [
        "PMDA 报告：不良事件/感染报告（PMD Act 时限）",
        "安全信息更新：定期安全报告",
        "召回报告",
        "上市后调查（PMDA 要求时）",
    ],
}

REG_NAMES = {"us": "美国", "eu": "欧盟", "cn": "中国", "jp": "日本"}


def obligations(region):
    if region not in OBLIGATIONS:
        print("错误：--region 仅支持 us/eu/cn/jp。")
        return 2
    print(f"{'=' * 62}")
    print(f"{REG_NAMES[region]} PMS 义务对照")
    print(f"{'=' * 62}")
    for i, s in enumerate(OBLIGATIONS[region], 1):
        print(f"  {i}. {s}")
    print("\n[说明] 详细依据见 references/上市后监管知识库.md；报告时限以官方最新要求为准。")
    return 0


# ---------------------------------------------------------------- report

REPORTS = {
    "us": [
        "死亡事件：30 日历日内报告 FDA（eMDR）",
        "严重伤害/器械故障：90 日历日",
        "提交渠道：eMDR 系统（进入 MAUDE 数据库）",
        "依据：21 CFR 803",
    ],
    "eu": [
        "严重事件报告：死亡/严重伤害 10 天、其他严重事件 15 天（MDCG 指南）",
        "趋势报告：重大趋势即报告",
        "FSCA：现场安全纠正触发即报告主管当局",
        "渠道：EUDAMED 警戒模块（逐步）",
    ],
    "cn": [
        "不良事件报告：死亡/严重伤害/群体事件按 2018 年 1 号令时限报告",
        "提交渠道：国家不良事件监测信息系统",
        "再评价：定期风险评价结果报告",
    ],
    "jp": [
        "PMDA 报告：不良事件/感染报告按 PMD Act 规定时限",
        "定期安全报告：按批准时条件",
    ],
}


def report(region):
    if region not in REPORTS:
        print("错误：--region 仅支持 us/eu/cn/jp。")
        return 2
    print(f"{'=' * 62}")
    print(f"{REG_NAMES[region]} 不良事件报告时限速查")
    print(f"{'=' * 62}")
    for i, s in enumerate(REPORTS[region], 1):
        print(f"  {i}. {s}")
    print("\n[说明] 时限以各国官方最新要求为准（法规更新频繁）。")
    return 0


# ---------------------------------------------------------------- plan

def plan():
    print("# PMS 计划（Post-Market Surveillance Plan）")
    print()
    print("## 1. 产品与市场信息")
    print("- 产品名称/型号：___")
    print("- 上市市场：___（美国/欧盟/中国/日本/其他）")
    print("- 风险等级：___")
    print()
    print("## 2. 上市后数据收集策略")
    print("- 不良事件数据：渠道 ___ 频率 ___")
    print("- 用户反馈/投诉：渠道 ___")
    print("- 文献与临床数据：检索策略 ___")
    print("- PMCF 数据（如适用）：计划 ___")
    print()
    print("## 3. 数据分析与评估")
    print("- 趋势分析方法：___")
    print("- 获益-风险评估频率：___")
    print()
    print("## 4. 输出文件")
    print("- PSUR / PMS 报告：频率 ___ 格式 ___")
    print("- 结论回流：技术文档/风险管理更新 ___")
    print()
    print("## 5. 责任与资源")
    print("- 责任部门/人：___")
    print("- 资源与预算：___")
    print()
    print("[说明] 框架细化见 references/上市后监管知识库.md 第七章。")
    return 0


# ---------------------------------------------------------------- psur

PSUR_FREQ = {
    "I": "PMS 报告（非 PSUR）——按 PMS 计划频率",
    "IIa": "PMS 报告——按 PMS 计划频率",
    "IIb": "PSUR——至少每 2 年更新一次",
    "III": "PSUR——至少每年更新一次",
}


def psur(cls):
    if cls not in PSUR_FREQ:
        print("错误：--class 仅支持 I/IIa/IIb/III。")
        return 2
    print("# PSUR（定期安全更新报告）框架")
    print()
    print(f"适用：Class {cls} 器械 —— {PSUR_FREQ[cls]}")
    print()
    print("## 1. 产品概况")
    print("- 产品描述/预期用途/适应症：___")
    print("- 上市时间与市场：___")
    print()
    print("## 2. 上市后数据汇总")
    print("- 不良事件数据（数量/类型/趋势）：___")
    print("- 投诉与用户反馈：___")
    print("- PMCF 数据（如适用）：___")
    print("- 文献与监管信息：___")
    print()
    print("## 3. 获益-风险再评估")
    print("- 获益分析：___")
    print("- 风险分析（含趋势）：___")
    print("- 结论：获益-风险比 ___")
    print()
    print("## 4. 纠正措施与结论")
    print("- 已采取/计划纠正措施：___")
    print("- 更新技术文档/风险管理结论：___")
    print()
    print("[说明] 依据 MDCG 2022-21；频率按风险等级（IIb 至少 2 年/III 至少 1 年）。")
    return 0


# ---------------------------------------------------------------- recall

def recall():
    print("=" * 62)
    print("FSCA / 召回流程")
    print("=" * 62)
    print("1. 触发评估：发现安全风险（不良事件/趋势/缺陷）→ 评估严重性")
    print("2. 分级：按风险分级（FSCA 触发/召回分级）")
    print("3. 通知：")
    print("   · 欧盟：FSCA 触发即报告主管当局 + 通知用户（FSCA 通知）")
    print("   · 美国：召回报告（21 CFR 806 纠正与移除报告）")
    print("   · 中国：主动召回 + 报告（或责令召回）")
    print("   · 日本：召回报告 PMDA")
    print("4. 实施：纠正措施（维修/替换/退款/停用）")
    print("5. 完成报告：纠正效果确认 + 报告归档")
    print("6. 复盘：根因分析 → 风险管理/设计变更 → 更新 PMS")
    print("-" * 62)
    print("联动：与变更管理、风险管理（生产后活动）联动；知识库第三章详见。")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="pms_toolkit",
        description=f"医械上市后监管本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_ob = sub.add_parser("obligations", help="PMS 义务对照")
    p_ob.add_argument("--region", required=True, choices=["us", "eu", "cn", "jp"])

    p_rp = sub.add_parser("report", help="报告时限速查")
    p_rp.add_argument("--region", required=True, choices=["us", "eu", "cn", "jp"])

    sub.add_parser("plan", help="PMS 计划框架")

    p_psur = sub.add_parser("psur", help="PSUR 撰写框架")
    p_psur.add_argument("--class", dest="cls", required=True, choices=["I", "IIa", "IIb", "III"])

    sub.add_parser("recall", help="FSCA/召回流程")

    args = parser.parse_args()

    if args.command == "obligations":
        return obligations(args.region)
    if args.command == "report":
        return report(args.region)
    if args.command == "plan":
        return plan()
    if args.command == "psur":
        return psur(args.cls)
    if args.command == "recall":
        return recall()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
