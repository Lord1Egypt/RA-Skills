#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
global_ai_toolkit.py — 全球 AI 治理版图本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  org        --name <waico|un|wdo|g7|g20|oecd|unesco>   国际组织速查
  initiative --actor <cn|un|intl>   倡议事件速查
  region     --name <us|eu|uk|jp|kr|in|cn>   主要经济体 AI 战略速查
  timeline                            全球治理时间线
  assess                              趋势观测清单
  --help                              查看帮助
"""

import argparse
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- org

ORGS = {
    "waico": "世界人工智能合作组织（WAICO）——2026-07-16 上海签署成立，全球首个 AI 政府间国际组织；29 创始国、总部上海；遵循联合国宪章、共商共建共享；三大目标=深化创新合作/推动普惠发展/加强协同共治",
    "un": "联合国体系——AI 治理主渠道：全球数字契约（2024-09）、AI 独立国际科学小组首份报告（2026-07-01）、联大 AI 能力建设决议（2024）、UNESCO AI 伦理建议书（2021）",
    "wdo": "世界数据组织（WDO）——2026-03-30 北京成立，全球首个数据发展与治理国际组织；弥合数据鸿沟、释放数据价值",
    "g7": "G7 广岛 AI 进程（2023 起）——国际指导原则 + 开发先进 AI 系统行为准则（自愿）",
    "g20": "G20——2019 年起采纳并更新全球 AI 原则（与 OECD 原则协同）",
    "oecd": "OECD——AI 原则（2019 采纳、2024 更新，47 国认同），价值观层面最广国际共识",
    "unesco": "UNESCO——《人工智能伦理建议书》（2021），首个全球 AI 伦理规范文件",
}


def org(name):
    if name not in ORGS:
        print("错误：--name 仅支持 waico/un/wdo/g7/g20/oecd/unesco。")
        return 2
    print("=" * 62)
    print("国际组织速查")
    print("=" * 62)
    print(ORGS[name])
    print("-" * 62)
    print("详见 references/01-全球治理格局.md 组织地图。")
    return 0


# ---------------------------------------------------------------- initiative

INITIATIVES = {
    "cn": [
        "2023《全球人工智能治理倡议》——首个中国系统 AI 治理国际倡议（以人为本、向上向善）",
        "2024《人工智能能力建设普惠计划》——面向全球南方的能力建设方案",
        "2024 联大《加强人工智能能力建设国际合作》决议——推动能力建设入联合国议程",
        "2025-09 '人工智能+'国际合作倡议（联合国总部）——应用合作模式",
        "2026-07-16 WAICO 成立协定签署（29 创始国）——全球首个 AI 政府间组织",
        "2026-07-17《人工智能合作发展行动计划》——八大行动（数据供给/算力普惠/开源生态/深度赋能/人才共育/规则共建/安全治理/向善）",
        "2026-07-17《智能体互信互联互操作全球合作倡议》（网信办）——Agent 生态规则先行",
    ],
    "un": [
        "2021 UNESCO《人工智能伦理建议书》",
        "2024-09 联合国未来峰会通过《全球数字契约》",
        "2024 联大 AI 能力建设国际合作决议",
        "2026-07-01 AI 独立国际科学小组首份报告《对人工智能机遇、风险与影响的循证评估》",
        "持续：AI 治理主渠道 + 能力建设议程",
    ],
    "intl": [
        "2023-11 英国 Bletchley AI 安全峰会——《布莱切利宣言》",
        "2024-05 韩国首尔峰会——首尔宣言 + 前沿 AI 安全国际协议",
        "2025-02 法国巴黎峰会——多元治理 + 全球南方参与",
        "2025 起 国际 AI 安全报告（年度，多国科学家联合）",
        "2024 起 各国 AI Safety Institute 设立与国际网络",
        "2026-07 WAIC 2026 暨人工智能全球治理高级别会议（上海）——15 点主席共识",
    ],
}

ACTOR_NAMES = {"cn": "中国", "un": "联合国", "intl": "国际峰会/多边"}


def initiative(actor):
    if actor not in INITIATIVES:
        print("错误：--actor 仅支持 cn/un/intl。")
        return 2
    print(f"{'=' * 62}")
    print(f"{ACTOR_NAMES[actor]} 全球 AI 治理倡议/事件")
    print(f"{'=' * 62}")
    for i, s in enumerate(INITIATIVES[actor], 1):
        print(f"  {i}. {s}")
    print("\n[说明] 详见 references/02-05 模块；时间线用 timeline 命令。")
    return 0


# ---------------------------------------------------------------- region

REGIONS = {
    "us": "美国——技术领先+安全双轨；联邦无统一 AI 法（州法拼图）；NIST AI RMF；AISI 模型评估；出口管制与算力治理",
    "eu": "欧盟——规范输出+产业追赶；AI Act 全球首部综合 AI 法（2026-08 全面执法）；AI 工厂投资；EN ISO 42001 标准化",
    "uk": "英国——安全主导+灵活性；不立硬法（原则导向）；UK AISI 前沿安全；软件与 AI 器械改革",
    "jp": "日本——促进为主（软法）；AI 促进法（2025，无罚则）；AI 基本计划；产业应用优先",
    "kr": "韩国——严格立法（亚太最严）；AI 基本法（2026-01 生效）；高影响 AI 注册与透明度",
    "in": "印度——发展优先；DPDP Act 数据保护；IndiaAI 使命；AI 治理指南（咨询性）",
    "cn": "中国——发展与安全并重；专项规章体系；2026 智能体/拟人化新规；全球治理机制供给（WAICO）",
}

REGION_NAMES = {"us": "美国", "eu": "欧盟", "uk": "英国", "jp": "日本", "kr": "韩国", "in": "印度", "cn": "中国"}


def region(name):
    if name not in REGIONS:
        print("错误：--name 仅支持 us/eu/uk/jp/kr/in/cn。")
        return 2
    print("=" * 62)
    print(f"{REGION_NAMES[name]} AI 战略速览")
    print("=" * 62)
    print(REGIONS[name])
    print("-" * 62)
    print("战略光谱与发展差异见 references/06-主要经济体战略.md。")
    return 0


# ---------------------------------------------------------------- timeline

def timeline():
    print("=" * 62)
    print("全球 AI 治理时间线（关键节点）")
    print("=" * 62)
    events = [
        ("2019", "OECD AI 原则采纳；G20 原则"),
        ("2021", "UNESCO AI 伦理建议书"),
        ("2023-11", "英国 Bletchley AI 安全峰会（布莱切利宣言）"),
        ("2023", "中国《全球人工智能治理倡议》；G7 广岛 AI 进程"),
        ("2024-05", "韩国首尔峰会（前沿 AI 安全国际协议）"),
        ("2024-09", "联合国未来峰会《全球数字契约》"),
        ("2024", "联大 AI 能力建设决议；中国《能力建设普惠计划》"),
        ("2025-02", "法国巴黎 AI 行动峰会"),
        ("2025", "国际 AI 安全报告首版；各国 AISI 网络"),
        ("2025-09", "中国'人工智能+'国际合作倡议（联合国总部）"),
        ("2026-03-30", "世界数据组织（WDO）北京成立"),
        ("2026-07-01", "联合国 AI 科学小组首份报告"),
        ("2026-07-16", "WAICO 成立协定签署（29 创始国，上海）"),
        ("2026-07-17", "WAIC 2026 全球治理高级别会议；AI 合作发展行动计划；智能体互信倡议"),
    ]
    for year, ev in events:
        print(f"  {year:<12s} {ev}")
    print("-" * 62)
    print("趋势判断见 assess 命令与 08 模块。")
    return 0


# ---------------------------------------------------------------- assess

def assess():
    print("=" * 62)
    print("全球 AI 治理趋势观测清单")
    print("=" * 62)
    items = [
        "机制化转型：WAICO 运转细则与成员扩员（从论坛对话到机制化合作）",
        "多边化：联合国/WAICO/峰会/区域机制的分工协调",
        "科学化：联合国科学小组报告、国际 AI 安全报告成为政策依据",
        "安全技术化：AISI 评估网络扩大、评估标准统一",
        "普惠化：全球南方能力建设实效、南南合作框架",
        "规则渗透：OECD/G20 原则向各国立法映射（AI Act/基本法）",
        "智能体治理：Agent 时代国际规则先行（智能体互信倡议）",
        "地缘政治：技术壁垒与开放生态的张力（出口管制 vs 共商共建）",
    ]
    for i, s in enumerate(items, 1):
        print(f"  [ ] {i}. {s}")
    print("\n[说明] 建议季度更新观测；跟踪来源见 08 模块 FAQ。")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="global_ai_toolkit",
        description=f"全球 AI 治理版图本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_org = sub.add_parser("org", help="国际组织速查")
    p_org.add_argument("--name", required=True, choices=["waico", "un", "wdo", "g7", "g20", "oecd", "unesco"])

    p_init = sub.add_parser("initiative", help="倡议事件速查")
    p_init.add_argument("--actor", required=True, choices=["cn", "un", "intl"])

    p_reg = sub.add_parser("region", help="经济体战略速查")
    p_reg.add_argument("--name", required=True, choices=["us", "eu", "uk", "jp", "kr", "in", "cn"])

    sub.add_parser("timeline", help="全球治理时间线")
    sub.add_parser("assess", help="趋势观测清单")

    args = parser.parse_args()

    if args.command == "org":
        return org(args.name)
    if args.command == "initiative":
        return initiative(args.actor)
    if args.command == "region":
        return region(args.name)
    if args.command == "timeline":
        return timeline()
    if args.command == "assess":
        return assess()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
