#!/usr/bin/env python3
"""调研报告生成辅助工具 - 结构化输出报告框架"""

from datetime import datetime


def generate_report_outline():
    """生成调研报告框架"""
    client = input("客户名称: ")
    date = datetime.now().strftime("%Y-%m-%d")
    
    print("\n" + "=" * 60)
    print("  调研报告框架生成")
    print("=" * 60)
    
    print(f"\n客户: {client}")
    print(f"日期: {date}")
    
    sections = {
        "1. 项目概述": [
            "1.1 项目背景",
            "1.2 调研范围与对象",
            "1.3 调研日程与方法"
        ],
        "2. 企业现状": [
            "2.1 企业基本情况",
            "2.2 组织架构",
            "2.3 主要产品与工艺",
            "2.4 信息化现状"
        ],
        "3. 核心绩效现状": [
            "3.1 运营KPI总览",
            "3.2 各维度绩效分析"
        ],
        "4. 销售与订单管理诊断": [
            "4.1 流程现状",
            "4.2 关键发现",
            "4.3 根因分析",
            "4.4 改善方向"
        ],
        "5. 生产计划诊断": [
            "5.1 流程现状",
            "5.2 关键发现",
            "5.3 根因分析",
            "5.4 改善方向"
        ],
        "6. 生产现场诊断": [
            "6.1 现场现状",
            "6.2 关键发现",
            "6.3 根因分析",
            "6.4 改善方向"
        ],
        "7. 采购诊断": [
            "7.1 流程现状",
            "7.2 关键发现",
            "7.3 根因分析",
            "7.4 改善方向"
        ],
        "8. 仓储物流诊断": [
            "8.1 现状",
            "8.2 关键发现",
            "8.3 改善方向"
        ],
        "9. 质量管理诊断": [
            "9.1 现状",
            "9.2 关键发现",
            "9.3 改善方向"
        ],
        "10. 工艺技术诊断": [
            "10.1 现状",
            "10.2 关键发现",
            "10.3 改善方向"
        ],
        "11. 问题总结与优先级": [
            "11.1 TOP10问题清单",
            "11.2 根因归类分析"
        ],
        "12. 改善方向与项目规划": [
            "12.1 精益改善方向",
            "12.2 数字化方向",
            "12.3 组织流程方向",
            "12.4 改善路线图"
        ],
        "13. 合作建议": [
            "13.1 合作模式",
            "13.2 实施路径",
            "13.3 价值展望"
        ]
    }
    
    print(f"\n📋 报告结构 ({client} 调研报告)")
    print("=" * 40)
    for section, items in sections.items():
        print(f"\n{section}")
        for item in items:
            print(f"  ├─ {item}")
    
    # 生成具体的发现数据表
    print(f"\n\n🔍 请为每个部门录入关键发现:")
    all_findings = {}
    depts = {
        "销售": "参考: 接单流程/预测/变更/OTD",
        "计划": "参考: MPS/MRP/排产/库存/齐套",
        "生产": "参考: OEE/C/T/换型/5S/异常",
        "采购": "参考: 供应商/周期/来料不良",
        "仓储": "参考: 库位/盘点/准确率/配送",
        "质量": "参考: IQC/IPQC/OQC/追溯",
        "工艺": "参考: BOM/ECN/SOP/NPI"
    }
    
    for dept, hint in depts.items():
        findings = []
        print(f"\n--- {dept} ({hint}) ---")
        while True:
            finding = input(f"  发现(空行结束): ").strip()
            if not finding:
                break
            findings.append(finding)
        if findings:
            all_findings[dept] = findings
    
    # 按优先级排列输出
    print("\n\n" + "=" * 60)
    print("  📊 发现汇总 - 按部门")
    print("=" * 60)
    for dept, findings in all_findings.items():
        print(f"\n{dept}:")
        for i, f in enumerate(findings, 1):
            print(f"  {i}. {f}")
    
    return all_findings


def generate_improvement_list():
    """生成改善项目清单"""
    print("\n" + "=" * 60)
    print("  改善项目清单生成")
    print("=" * 60)
    
    projects = []
    while True:
        name = input("\n项目名称(空行结束): ").strip()
        if not name:
            break
        p_type = input("类型(1=速赢 2=重点改善 3=数字化 4=战略): ")
        p_priority = input("优先级(1/2/3): ")
        benefit = input("预期年效益(万元): ")
        investment = input("投入估算(万元): ")
        duration = input("预计周期(月): ")
        
        type_map = {"1": "速赢", "2": "重点改善", "3": "数字化", "4": "战略"}
        pri_map = {"1": "P1", "2": "P2", "3": "P3"}
        
        projects.append({
            "name": name,
            "type": type_map.get(p_type, "重点改善"),
            "priority": pri_map.get(p_priority, "P2"),
            "benefit": float(benefit) if benefit else 0,
            "investment": float(investment) if investment else 0,
            "duration": duration
        })
    
    if not projects:
        return
    
    print("\n" + "=" * 60)
    print("  📋 改善项目清单")
    print("=" * 60)
    print(f"{'序号':<4} {'项目名称':<16} {'类型':<10} {'优先级':<6} {'投入(万)':<10} {'年效益(万)':<12} {'ROI(月)':<8}")
    print("-" * 66)
    
    for i, p in enumerate(projects, 1):
        roi = (p["investment"] / p["benefit"] * 12) if p["benefit"] > 0 else 0
        name_short = p["name"][:14] + ".." if len(p["name"]) > 14 else p["name"]
        print(f"{i:<4} {name_short:<16} {p['type']:<10} {p['priority']:<6} {p['investment']:<10.1f} {p['benefit']:<12.1f} {roi:<8.1f}")
    
    total_inv = sum(p["investment"] for p in projects)
    total_ben = sum(p["benefit"] for p in projects)
    print("-" * 66)
    print(f"{'合计':<20} {'':<16} {total_inv:<10.1f} {total_ben:<12.1f} ROI:{total_inv/total_ben*12:.1f}月" if total_ben > 0 else "")


def main():
    print("📋 咨询报告生成辅助工具")
    print("=" * 60)
    print("1. 生成调研报告框架+发现录入")
    print("2. 生成改善项目清单")
    print("0. 退出")
    
    while True:
        choice = input("\n请选择 (0-2): ").strip()
        if choice == "1":
            generate_report_outline()
        elif choice == "2":
            generate_improvement_list()
        elif choice == "0":
            print("感谢使用！")
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    main()
