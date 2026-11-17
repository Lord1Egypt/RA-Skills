#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
data_export_toolkit.py — 医械数据出海合规本地工具包
仅使用 Python 标准库，零网络、零数据采集。

命令：
  path      --desc "<出境情况描述>"    出境路径判定
  threshold --personal <N> --sensitive <N>   人数阈值计算
  scene     --type <clinical|cloud|remote|employee|aftermarket>   场景合规清单
  market    --region <eu|us|sg|jp|kr>   目标市场数据要求速查
  audit                             落地与审计清单
  --help                            查看帮助
"""

import argparse
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- path

def path(desc):
    if not desc or not desc.strip():
        print("错误：--desc 不能为空。示例：--desc \"向海外CRO传输临床试验受试者个人信息，全年约50万人\"")
        return 2
    d = desc
    print("=" * 62)
    print("数据出境路径判定（初步，正式以申报口径为准）")
    print("=" * 62)
    print(f"出境情况：{d}")
    print("-" * 62)

    # 重要数据/敏感关键词
    if any(k in d for k in ["重要数据", "健康", "医疗", "病历", "基因", "生物识别", "受试者"]):
        sensitive_flag = True
        print("  · 涉及健康医疗/敏感个人信息（出境门槛低、要求严）")
    else:
        sensitive_flag = False
        print("  · 未见明确敏感个人信息关键词（请核实）")

    # 数量提取（支持 X万 / X百万 / X人 写法）
    import re

    def _extract_qty(d):
        qty = 0
        for m in re.finditer(r"(\d+(?:\.\d+)?)\s*百万", d):
            qty = max(qty, int(float(m.group(1)) * 1000000))
        for m in re.finditer(r"(\d+(?:\.\d+)?)\s*万", d):
            qty = max(qty, int(float(m.group(1)) * 10000))
        for m in re.finditer(r"(\d+)\s*人", d):
            qty = max(qty, int(m.group(1)))
        return qty

    n = _extract_qty(d)
    if n:
        if n >= 1000000:
            verdict = "需申报【数据出境安全评估】（>100 万个人信息）"
        elif n >= 100000:
            verdict = "可走【标准合同 或 出境认证】（10 万-100 万个人信息）"
        elif n >= 10000 and sensitive_flag:
            verdict = "需申报【数据出境安全评估】（>1 万敏感个人信息）"
        else:
            verdict = "未达三条路径阈值（仍须一般合规）——若涉敏感数据请精确盘点"
    else:
        verdict = "未识别到数量——请按『自当年 1 月 1 日累计』口径盘点出境人数后判定"

    print(f"  · 判定：{verdict}")
    print("-" * 62)
    print("提示：①阈值按当年 1 月 1 日起累计，非单笔；②医疗健康数据=敏感个人信息；")
    print("     ③重要数据（行业规则判定）无论数量直接安全评估；④豁免情形见 02 模块 §6。")
    return 0


# ---------------------------------------------------------------- threshold

def threshold(personal, sensitive):
    print("=" * 62)
    print("数据出境人数阈值判定（自当年 1 月 1 日累计）")
    print("=" * 62)
    print(f"个人信息（不含敏感）：{personal:,} 人")
    print(f"敏感个人信息：{sensitive:,} 人")
    print("-" * 62)

    if personal >= 1000000 or sensitive >= 10000:
        verdict = "【数据出境安全评估】（强制申报）"
    elif personal >= 100000 or sensitive > 0:
        verdict = "【标准合同 或 出境认证】"
    else:
        verdict = "【未达三条路径阈值】——仍须履行一般合规（同意/告知/安全措施）"
    print(f"判定：{verdict}")
    print("-" * 62)
    print("⚠️ 注意：①累计计算（化整为零规避=违规）；②已走标准合同/认证后累计达安全评估门槛，")
    print("     须申报评估并把此前出境数据纳入范围；③涉重要数据直接安全评估。")
    return 0


# ---------------------------------------------------------------- scene

SCENES = {
    "clinical": [
        "受试者个人信息与健康数据 = 敏感个人信息（出境门槛低）",
        "知情同意：单独同意（中国）+ 目标市场同意要求",
        "出境路径判定：按累计数量（敏感 1 万条触发安全评估）",
        "去标识化/匿名化评估：源头减少敏感数据出境",
        "海外 CRO 合同：数据处理条款 + 数据保护义务 + 审计权",
        "数据回传与留存：试验数据保留期限与存储地",
        "医疗数据安全审查（境外医疗合作）",
    ],
    "cloud": [
        "境外云存储 = 数据出境 → 按路径合规",
        "数据驻留要求：中国（境内收集存储受限）/欧盟（传输机制）/韩国（本地化倾向）",
        "云服务商评估：存储地、加密、合规认证（ISO 27001/42001）、DPA",
        "多区域部署架构：数据按区域驻留，最小跨境",
        "数据分类分级：区分技术数据 vs 患者数据",
    ],
    "remote": [
        "远程诊疗数据 = 敏感个人信息（健康数据）",
        "医疗数据安全审查（境外合作场景）",
        "跨境传输路径 + 目标市场合法依据（GDPR 等）",
        "三重加密 + 数据最小化",
        "设备端/云端数据处理边界明确",
        "未成年人患者数据（如有）特殊保护",
    ],
    "employee": [
        "员工个人信息出境：人力资源管理豁免（劳动合同所必需）——注意边界",
        "集团内部传输：标准合同/集团约束规则（BCR）",
        "跨境系统（薪酬/差旅/HR 系统）数据出境评估",
        "供应商联系人数据：合同条款 + 最小化",
    ],
    "aftermarket": [
        "售后数据分级：设备技术数据 vs 患者数据",
        "脱敏优先：技术数据脱敏后跨境",
        "不良事件报告：法规义务优先的法定基础衔接",
        "设备联网数据：跨境传输合规 + 安全评估",
    ],
}

SCENE_NAMES = {"clinical": "临床试验", "cloud": "境外云服务", "remote": "远程诊疗/数字疗法",
               "employee": "员工与供应商", "aftermarket": "售后与不良事件"}


def scene(stype):
    if stype not in SCENES:
        print("错误：--type 仅支持 clinical/cloud/remote/employee/aftermarket。")
        return 2
    print(f"{'=' * 62}")
    print(f"{SCENE_NAMES[stype]} 数据出海合规清单")
    print(f"{'=' * 62}")
    for i, s in enumerate(SCENES[stype], 1):
        print(f"  [ ] {i}. {s}")
    print("\n[说明] 详细见 05 模块；路径与阈值用 path/threshold 命令。")
    return 0


# ---------------------------------------------------------------- market

MARKETS = {
    "eu": [
        "GDPR：健康数据属特殊类别（第 9 条），处理须明确同意/必要医疗服务等法定依据",
        "EHDS《欧洲健康数据空间条例》2025-03 生效：健康数据跨境与二次使用更高标准",
        "跨境传输：充分性认定 / SCC 标准合同条款 / 其他保障措施",
        "医疗器械联动：MDR/AI Act 与数据合规并行（AI 训练数据须 GDPR 合规）",
        "德国参考：DSK 2025-09 跨境传输敏感健康数据两步法指南",
        "落地：DPIA + 合法依据 + 跨境机制（SCC 常用）",
    ],
    "us": [
        "HIPAA 安全规则 2026 重大升级：强制 MFA + 强加密",
        "覆盖 PHI（受保护健康信息）；与医院合作常需签 BAA",
        "州法：加州 CCPA/CPRA 等健康数据要求",
        "无联邦统一出境审批，但 PHI 传输须 HIPAA 合规",
        "明确是否属 HIPAA 覆盖范围（设备厂商等需判断）",
    ],
    "sg": [
        "PDPA（2021 修订）：健康数据属敏感个人数据，处理限制更严",
        "跨境传输：接收方须提供与 PDPA 相当的保护（SCC/集团规则常用）",
        "数据泄露通报：达到危害门槛 72 小时内向 PDPC 通报",
        "医疗 AI/健康应用：AI Verify + 模型 AI 治理框架参考",
    ],
    "jp": [
        "APPI（2022/2025 修订）：健康/医疗属需特别注意的个人信息",
        "跨境传输：接收国充分保护（EEA/英国在列）或合同/同意",
        "医疗 AI 器械：PMDA 路径（DASH/PACMP）与数据合规并行",
    ],
    "kr": [
        "PIPA（2023 修订）：健康/基因属敏感信息，处理须单独同意",
        "AI 基本法（2026-01 生效）：医疗 AI 属高影响 AI",
        "跨境：数据本地化倾向强（部分数据须境内处理）",
    ],
}

MARKET_NAMES = {"eu": "欧盟", "us": "美国", "sg": "新加坡", "jp": "日本", "kr": "韩国"}


def market(region):
    if region not in MARKETS:
        print("错误：--region 仅支持 eu/us/sg/jp/kr。")
        return 2
    print(f"{'=' * 62}")
    print(f"{MARKET_NAMES[region]} 数据要求速查")
    print(f"{'=' * 62}")
    for i, s in enumerate(MARKETS[region], 1):
        print(f"  {i}. {s}")
    print("\n[说明] 核对基准日 2026-08-27；详见 04 模块。")
    return 0


# ---------------------------------------------------------------- audit

AUDIT_ITEMS = [
    "数据地图：盘点所有跨境数据流（临床试验/云/员工/售后）",
    "分类分级：重要数据/敏感个人信息/一般个人信息",
    "路径判定：path/threshold 命令 + 医疗数据叠加要求",
    "合规动作：安全评估/标准合同/认证 + 知情同意 + 合同条款",
    "技术措施：三重加密/MFA/最小化/脱敏",
    "运营落地：出境台账 + 监控告警 + 政策制度",
    "持续合规：重要数据每年风险评估（2026-08-20 办法）",
    "个保审计：>1000 万人每两年一次（2026-04 政策问答）",
    "到期管理：评估届满前 60 个工作日申请延期（提前 6 个月自检）",
    "法规跟踪：中国+目标市场季度复核",
]


def audit():
    print("=" * 62)
    print("医械数据出海合规落地审计清单")
    print("=" * 62)
    for i, s in enumerate(AUDIT_ITEMS, 1):
        print(f"  [ ] {i}. {s}")
    print("\n[说明] 五步落地流程见 06 模块。")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="data_export_toolkit",
        description=f"医械数据出海合规本地工具包 v{VERSION}（零网络、零数据采集，仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_path = sub.add_parser("path", help="出境路径判定")
    p_path.add_argument("--desc", required=True, help="出境情况描述")

    p_th = sub.add_parser("threshold", help="人数阈值计算")
    p_th.add_argument("--personal", type=int, required=True, help="个人信息数量（不含敏感）")
    p_th.add_argument("--sensitive", type=int, required=True, help="敏感个人信息数量")

    p_sc = sub.add_parser("scene", help="场景合规清单")
    p_sc.add_argument("--type", required=True, choices=["clinical", "cloud", "remote", "employee", "aftermarket"])

    p_mk = sub.add_parser("market", help="目标市场数据要求")
    p_mk.add_argument("--region", required=True, choices=["eu", "us", "sg", "jp", "kr"])

    sub.add_parser("audit", help="落地审计清单")

    args = parser.parse_args()

    if args.command == "path":
        return path(args.desc)
    if args.command == "threshold":
        return threshold(args.personal, args.sensitive)
    if args.command == "scene":
        return scene(args.type)
    if args.command == "market":
        return market(args.region)
    if args.command == "audit":
        return audit()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
