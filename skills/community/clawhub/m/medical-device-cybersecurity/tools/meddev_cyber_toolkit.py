#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
meddev_cyber_toolkit.py — 医疗器械网络安全本地工具包
仅使用 Python 标准库，零网络、零扫描、零数据采集。

命令：
  reg       --region <us|eu|cn>    区域网络安全要求速查
  checklist --phase <design|development|submission|postmarket>   检查清单
  sbom                               SBOM 字段模板（JSON）
  vuln      --desc "<漏洞描述>"     漏洞分级（CVSS 风格）
  standard                           标准速查
  --help                             查看帮助
"""

import argparse
import json
import sys

VERSION = "1.0.0"

# ---------------------------------------------------------------- reg

REGS = {
    "us": [
        "联网器械（Cyber Device）强制：SBOM + 漏洞管理计划 + 安全架构文档 + 渗透测试 + 更新机制",
        "缺失后果：510(k)/De Novo 不予受理（RTA, Refuse to Accept）",
        "参考标准：IEC 81001-5-1、NIST SP 800-53（COSAiS 草案）、UL 2900",
        "上市后：漏洞监测、协调披露、补丁分发",
        "QMSR（2026-02 生效）：质量体系须覆盖网络安全工程",
    ],
    "eu": [
        "MDR Annex I 17.2：网络攻击防护、数据保护、安全更新、最小权限",
        "NIS2 Directive（2024-10）：医疗机构关键基础设施要求间接影响供应商",
        "Cyber Resilience Act（CRA，预期 2027 强制）：联网产品统一安全要求（含协调披露）",
        "RED（无线电设备指令）：带无线电功能器械网络安全（2025-08 起）",
        "公告机构审核：网络安全文档 + 上市后监控纳入 PMCF/PSUR",
    ],
    "cn": [
        "NMPA《医疗器械网络安全注册审查指导原则》：注册申报提交网络安全描述文档",
        "维度：数据安全（个保法）、访问控制、更新机制、漏洞管理、上市后监测",
        "上位法：网络安全法（2026-01-01 修订生效）、数据安全法、个人信息保护法",
        "AI 软件：算法安全 + 网络安全双维度审评",
    ],
}

REG_NAMES = {"us": "美国 FDA", "eu": "欧盟", "cn": "中国 NMPA"}


def reg(region):
    if region not in REGS:
        print("错误：--region 仅支持 us/eu/cn。")
        return 2
    print(f"{'=' * 62}")
    print(f"{REG_NAMES[region]} 医疗器械网络安全要求")
    print(f"{'=' * 62}")
    for i, s in enumerate(REGS[region], 1):
        print(f"  {i}. {s}")
    print("\n[说明] 核对基准日 2026-08-27；详见 02/03/04 模块。")
    return 0


# ---------------------------------------------------------------- checklist

PHASES = {
    "design": [
        "是否为联网器械（Cyber Device）判断",
        "威胁建模（攻击面/威胁/缓解）",
        "安全需求规格（功能+安全需求）",
        "网络安全计划（目标/范围/资源）",
        "安全架构设计（认证/权限/加密/最小权限）",
    ],
    "development": [
        "IEC 62304 软件生命周期集成网络安全",
        "ISO 81001-5-1 网络安全工程落地",
        "SBOM 建立与维护（05 模块）",
        "安全编码与代码审查",
        "模糊测试/静态扫描（开发中持续）",
        "供应链组件安全（上游 SBOM/漏洞扫描）",
    ],
    "submission": [
        "SBOM（FDA 强制，RTA 条件）",
        "渗透测试报告（联网器械强制）",
        "漏洞管理计划",
        "安全架构文档",
        "更新与补丁机制说明",
        "网络安全描述文档（NMPA 随注册提交）",
        "威胁模型文档",
    ],
    "postmarket": [
        "持续漏洞扫描（SBOM 联动）",
        "漏洞协调披露流程（受理/验证/分级/修复/公开）",
        "补丁发布与分发（OTA 安全）",
        "安全事件响应（与不良事件衔接）",
        "定期网络安全评审（PSUR/年度）",
        "监管报告义务（漏洞/事件按时限报告）",
    ],
}

PHASE_NAMES = {"design": "设计阶段", "development": "开发阶段", "submission": "申报阶段", "postmarket": "上市后"}


def checklist(phase):
    if phase not in PHASES:
        print("错误：--phase 仅支持 design/development/submission/postmarket。")
        return 2
    print(f"{'=' * 62}")
    print(f"医疗器械网络安全检查清单（{PHASE_NAMES[phase]}）")
    print(f"{'=' * 62}")
    for i, s in enumerate(PHASES[phase], 1):
        print(f"  [ ] {i}. {s}")
    print("\n[说明] 详见 07 模块文档体系。")
    return 0


# ---------------------------------------------------------------- sbom

SBOM_FIELDS = {
    "schema": "CycloneDX-1.5",
    "metadata": {"component": {"name": "<产品名>", "version": "<版本>", "type": "application"}},
    "components": [
        {
            "name": "<组件名>",
            "version": "<精确版本>",
            "supplier": {"name": "<供应商>"},
            "licenses": [{"license": {"name": "<许可证>"}}],
            "hashes": [{"alg": "SHA-256", "content": "<哈希>"}],
            "dependencies": ["<依赖组件ID>"],
            "externalReferences": [{"type": "vcs", "url": "<来源URL>"}],
        }
    ],
    "vulnerabilities": [
        {"id": "CVE-XXXX-XXXXX", "rating": "<严重度>", "affects": [{"ref": "<组件>"}]}
    ],
}


def sbom():
    print(json.dumps(SBOM_FIELDS, ensure_ascii=False, indent=2))
    print("\n[说明] 核心字段定义见 05 模块；格式选 SPDX 或 CycloneDX（推荐后者，漏洞关联强）。")
    return 0


# ---------------------------------------------------------------- vuln

VULN_RULES = [
    (["任意代码", "完全控制", "接管", "RCE", "远程执行", "远程代码"], "严重（9.0-10.0）", "立即处置"),
    (["远程", "利用", "重大", "数据", "敏感", "提权", "越权"], "高（7.0-8.9）", "30 天修复"),
    (["有条件", "低权限", "有限", "信息泄露"], "中（4.0-6.9）", "90 天修复"),
]


def vuln(desc):
    if not desc or not desc.strip():
        print("错误：--desc 不能为空。示例：--desc \"远程可被利用执行任意代码\"")
        return 2
    print("=" * 62)
    print("漏洞分级（CVSS 风格，参考 06 模块）")
    print("=" * 62)
    print(f"漏洞描述：{desc}")
    print("-" * 62)
    for kws, level, fix in VULN_RULES:
        if any(k in desc for k in kws):
            print(f"判定：【{level}】")
            print(f"修复时限：{fix}")
            return 0
    print("判定：【低（0.1-3.9）】")
    print("修复时限：180 天")
    print("-" * 62)
    print("提示：实际分级请用 CVSS 计算器按向量精确评分（06 模块 §1）。")
    return 0


# ---------------------------------------------------------------- standard

STANDARDS = [
    ("ISO/IEC 81001-5-1", "产品网络安全工程（医械核心安全标准）", "全生命周期"),
    ("IEC 62304", "医疗器械软件生命周期", "开发过程"),
    ("ISO 14971", "医疗器械风险管理（总纲）", "管理总纲"),
    ("ISO 13485", "医疗器械质量管理体系", "质量体系"),
    ("ISO/IEC 27001", "组织信息安全管理体系", "组织层面"),
    ("NIST SP 800-53", "安全控制目录（COSAiS 覆盖层草案中）", "控制项"),
    ("UL 2900", "互联产品安全系列", "产品安全"),
    ("SPDX / CycloneDX", "SBOM 格式标准", "SBOM 格式"),
]


def standard():
    print("=" * 62)
    print("医疗器械网络安全相关标准速查")
    print("=" * 62)
    print(f"{'标准':<22s} {'定位':<32s} {'层级'}")
    print("-" * 62)
    for name, desc, lvl in STANDARDS:
        print(f"{name:<22s} {desc:<32s} {lvl}")
    print("-" * 62)
    print("联动关系见 07 模块 §2（14971 总纲 / 62304 软件 / 81001-5-1 安全 / 13485 体系 / 27001 组织）。")
    return 0


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        prog="meddev_cyber_toolkit",
        description=f"医疗器械网络安全本地工具包 v{VERSION}（零网络、零扫描、仅标准库）",
    )
    sub = parser.add_subparsers(dest="command")

    p_reg = sub.add_parser("reg", help="区域要求速查")
    p_reg.add_argument("--region", required=True, choices=["us", "eu", "cn"])

    p_cl = sub.add_parser("checklist", help="检查清单")
    p_cl.add_argument("--phase", required=True, choices=["design", "development", "submission", "postmarket"])

    sub.add_parser("sbom", help="SBOM 字段模板")

    p_vuln = sub.add_parser("vuln", help="漏洞分级")
    p_vuln.add_argument("--desc", required=True, help="漏洞描述")

    sub.add_parser("standard", help="标准速查")

    args = parser.parse_args()

    if args.command == "reg":
        return reg(args.region)
    if args.command == "checklist":
        return checklist(args.phase)
    if args.command == "sbom":
        return sbom()
    if args.command == "vuln":
        return vuln(args.desc)
    if args.command == "standard":
        return standard()

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
