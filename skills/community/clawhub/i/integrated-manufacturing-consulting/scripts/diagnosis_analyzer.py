#!/usr/bin/env python3
"""诊断分析辅助工具 - 问题整理与优先级评估"""


def collect_problems():
    """问题采集与整理"""
    print("\n" + "=" * 60)
    print("  调研问题采集与整理")
    print("=" * 60)
    
    problems = []
    departments = ["销售", "计划", "生产", "采购", "仓储物流", "质量", "工艺"]
    
    while True:
        print(f"\n--- 第{len(problems)+1}个问题 ---")
        dept = input(f"涉及部门({'/'.join(departments)}): ").strip()
        if not dept:
            break
        if dept not in departments:
            print(f"⚠️ 部门名称不正确，可选: {', '.join(departments)}")
            continue
        
        desc = input("问题描述: ")
        data = input("数据支撑（如无数据按Enter跳过）: ")
        
        print("严重程度(1-5, 5=最严重): ", end="")
        severity = int(input() or "3")
        print("紧迫程度(1-5, 5=最紧迫): ", end="")
        urgency = int(input() or "3")
        
        problems.append({
            "dept": dept, "desc": desc, "data": data,
            "severity": severity, "urgency": urgency
        })
        print(f"✅ 已记录")
    
    return problems


def calculate_priorities(problems):
    """计算优先级分数"""
    for p in problems:
        p["priority_score"] = p["severity"] * 0.6 + p["urgency"] * 0.4
        p["priority_level"] = "P1" if p["priority_score"] >= 4.0 else ("P2" if p["priority_score"] >= 2.5 else "P3")
    return sorted(problems, key=lambda x: x["priority_score"], reverse=True)


def generate_report(problems):
    """生成问题清单总结"""
    if not problems:
        print("无问题数据")
        return
    
    print("\n" + "=" * 60)
    print("  📋 问题清单总结")
    print("=" * 60)
    
    table_header = f"{'序号':<4} {'部门':<8} {'问题':<30} {'严重度':<6} {'紧迫度':<6} {'优先级':<6}"
    print(table_header)
    print("-" * 60)
    
    for i, p in enumerate(problems, 1):
        desc_short = p["desc"][:28] + ".." if len(p["desc"]) > 28 else p["desc"]
        print(f"{i:<4} {p['dept']:<8} {desc_short:<30} {p['severity']:<6} {p['urgency']:<6} {p['priority_level']:<6}")
    
    print("-" * 60)
    
    # 统计
    p1 = [p for p in problems if p["priority_level"] == "P1"]
    p2 = [p for p in problems if p["priority_level"] == "P2"]
    p3 = [p for p in problems if p["priority_level"] == "P3"]
    
    print(f"\n📊 统计:")
    print(f"  P1(高优先): {len(p1)} 个")
    print(f"  P2(中优先): {len(p2)} 个")
    print(f"  P3(低优先): {len(p3)} 个")
    print(f"  总计: {len(problems)} 个")
    
    print(f"\n📌 按部门分布:")
    dept_count = {}
    for p in problems:
        dept_count[p["dept"]] = dept_count.get(p["dept"], 0) + 1
    for dept in sorted(dept_count.keys()):
        bar = "█" * dept_count[dept]
        print(f"  {dept:<8} {dept_count[dept]:>2}个 {bar}")


def cross_check():
    """跨部门问题交叉验证"""
    print("\n" + "=" * 60)
    print("  跨部门问题交叉验证")
    print("=" * 60)
    
    print("输入不同部门对同一问题的描述，分析认知差异")
    
    issues = []
    while True:
        issue = input("\n问题名称(空行结束): ").strip()
        if not issue:
            break
        print(f"  A部门描述: ", end="")
        view_a = input()
        print(f"  B部门描述: ", end="")
        view_b = input()
        issues.append((issue, view_a, view_b))
    
    for issue, a, b in issues:
        print(f"\n  📍 {issue}")
        overlap = len(set(a.split()) & set(b.split()))
        if overlap > 3:
            print(f"     ✅ 两部门认知一致")
        else:
            print(f"     ⚠️ 两部门存在认知差异，需进一步核实")
            print(f"     A说: {a}")
            print(f"     B说: {b}")


def improvement_mapping():
    """问题-改善方向映射"""
    print("\n" + "=" * 60)
    print("  问题-改善方向映射")
    print("=" * 60)
    
    directions = {
        "1": ("精益生产", ["5S", "SMED", "TPM", "VSM", "看板", "标准化", "线平衡", "Poka-Yoke"]),
        "2": ("数字化", ["MES", "WMS", "APS", "QMS", "BI", "IoT", "PLM", "数字孪生"]),
        "3": ("组织流程", ["S&OP", "KPI", "流程再造", "组织优化", "供应链协同", "计划集控"])
    }
    
    print("\n可选改善方向:")
    for k, (name, _) in directions.items():
        print(f"  {k}. {name}")
    print(f"  q. 完成")
    
    mappings = []
    while True:
        problem = input("\n要映射的问题描述(空行结束): ").strip()
        if not problem:
            break
        print("选择改善方向编号: ", end="")
        dir_choice = input().strip()
        if dir_choice in directions:
            dir_name, tools = directions[dir_choice]
            print(f"  可选工具/方法: {', '.join(tools)}")
            method = input("  选择具体方法: ").strip()
            mappings.append((problem, dir_name, method))
            print(f"  ✅ {problem} → {dir_name}/{method}")
        else:
            print("  ❌ 无效选择")
    
    if mappings:
        print(f"\n📋 映射结果:")
        for p, d, m in mappings:
            print(f"  {p:<30} → {d:<8} / {m}")


def main():
    print("📋 诊断分析辅助工具")
    print("=" * 60)
    print("1. 问题采集与优先级评估")
    print("2. 跨部门问题交叉验证")
    print("3. 问题-改善方向映射")
    print("0. 退出")
    
    while True:
        choice = input("\n请选择 (0-3): ").strip()
        if choice == "1":
            probs = collect_problems()
            if probs:
                sorted_probs = calculate_priorities(probs)
                generate_report(sorted_probs)
        elif choice == "2":
            cross_check()
        elif choice == "3":
            improvement_mapping()
        elif choice == "0":
            print("感谢使用！")
            break
        else:
            print("无效选择")


if __name__ == "__main__":
    main()
