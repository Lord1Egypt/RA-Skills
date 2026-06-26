#!/usr/bin/env python3
"""
亲子关系四轴诊断工具
根据用户输入，系统化评估控制权、解释权、能量流、责任归属四轴的失衡程度
"""

import argparse
import json
import sys
from typing import Dict, List, Optional


def get_axis_score(axis_name: str, indicators: List[str]) -> Dict:
    """获取单个轴的评分"""
    print(f"\n{'='*50}")
    print(f"【{axis_name}】评估")
    print(f"{'='*50}")
    
    total = 0
    scores = []
    
    for i, indicator in enumerate(indicators, 1):
        print(f"\n{i}. {indicator}")
        print("   评分标准: 1=从不 | 2=偶尔 | 3=有时 | 4=经常 | 5=总是")
        
        while True:
            try:
                score = int(input("   请评分(1-5): "))
                if 1 <= score <= 5:
                    scores.append(score)
                    total += score
                    break
                else:
                    print("   请输入1-5之间的数字")
            except ValueError:
                print("   请输入数字")
    
    avg_score = round(total / len(indicators), 2)
    
    # 评估结果
    if avg_score <= 2:
        status = "健康"
        desc = "该维度运行良好，主体性得到保护"
    elif avg_score <= 3.5:
        status = "轻度失衡"
        desc = "存在一定程度的剥夺风险"
    elif avg_score <= 4.5:
        status = "中度失衡"
        desc = "该维度存在明显的剥夺问题"
    else:
        status = "严重失衡"
        desc = "该维度被严重剥夺，主体性受到严重威胁"
    
    return {
        "axis": axis_name,
        "avg_score": avg_score,
        "total_score": total,
        "max_score": len(indicators) * 5,
        "status": status,
        "description": desc,
        "details": scores
    }


def diagnose_control_axis() -> Dict:
    """诊断控制权轴"""
    indicators = [
        "父母是否经常替孩子做决定（如兴趣班、朋友选择）",
        "孩子是否有权决定自己的时间安排",
        "孩子的选择是否经常被否定或忽视",
        "父母是否控制孩子的行为细节",
        "孩子是否需要获得许可才能行动"
    ]
    return get_axis_score("控制权轴", indicators)


def diagnose_explanation_axis() -> Dict:
    """诊断解释权轴"""
    indicators = [
        "孩子的感受是否经常被否定（'你怎么会这么想'）",
        "孩子的行为是否需要符合父母的解释框架",
        "孩子是否有权给出自己的理由",
        "父母的解释是否经常变化让孩子困惑",
        "孩子的理解是否被认可"
    ]
    return get_axis_score("解释权轴", indicators)


def diagnose_energy_axis() -> Dict:
    """诊断能量流轴"""
    indicators = [
        "孩子的时间是否被作业和培训班占满",
        "孩子的兴趣探索是否被打断或否定",
        "孩子的试错是否被惩罚或嘲笑",
        "孩子是否有自由玩耍和发呆的时间",
        "孩子的探索行为是否被允许"
    ]
    return get_axis_score("能量流轴", indicators)


def diagnose_responsibility_axis() -> Dict:
    """诊断责任归属轴"""
    indicators = [
        "成功时功劳归谁（父母/孩子）",
        "失败时责任归谁（父母/孩子）",
        "孩子是否有承担后果的机会",
        "父母是否替孩子承担本属于孩子的责任",
        "孩子是否能从结果中学习"
    ]
    return get_axis_score("责任归属轴", indicators)


def diagnose_entropy_adjustment() -> Dict:
    """诊断熵调节状态"""
    print(f"\n{'='*50}")
    print("【熵调节状态】评估")
    print(f"{'='*50}")
    
    print("\n请选择家庭熵调节结构类型:")
    print("1 = 高压结构（低熵）: 只有一种正确路径，其他行为被定义错误")
    print("2 = 混乱结构（无边界）: 没有规则、没有反馈、没有标准")
    print("3 = 健康结构（可调熵）: 允许探索、有反馈边界、允许失败可修正")
    
    while True:
        try:
            choice = int(input("\n请选择(1-3): "))
            if choice in [1, 2, 3]:
                break
            print("请输入1-3之间的数字")
        except ValueError:
            print("请输入数字")
    
    types = {
        1: {
            "type": "高压结构（低熵）",
            "description": "世界被压扁，孩子主体性严重受损",
            "risk": "极高"
        },
        2: {
            "type": "混乱结构（无边界）",
            "description": "世界失序，孩子缺乏安全感",
            "risk": "高"
        },
        3: {
            "type": "健康结构（可调熵）",
            "description": "世界可生长，孩子主体性得到保护",
            "risk": "低"
        }
    }
    
    return types[choice]


def diagnose_threefold_deprivation() -> Dict:
    """诊断三重剥夺"""
    print(f"\n{'='*50}")
    print("【三重剥夺】评估")
    print(f"{'='*50}")
    
    deprivations = [
        ("熵剥夺", [
            "不允许孩子接触不确定性",
            "过度保护，不让孩子尝试",
            "替孩子消除所有潜在风险"
        ]),
        ("反馈剥夺", [
            "孩子的行为不产生真实结果",
            "结果被父母过滤或替代承担",
            "孩子的选择无法带来可感知的反馈"
        ]),
        ("责任剥夺", [
            "孩子无法为选择承担后果",
            "责任被外包给父母",
            "孩子无法建立'我负责'的结构"
        ])
    ]
    
    results = []
    
    for dep_name, indicators in deprivations:
        print(f"\n【{dep_name}】")
        freq = 0
        
        for i, ind in enumerate(indicators, 1):
            print(f"\n{i}. {ind}")
            print("   1=从不 | 2=偶尔 | 3=有时 | 4=经常 | 5=总是")
            
            while True:
                try:
                    score = int(input("   请评分(1-5): "))
                    if 1 <= score <= 5:
                        freq += score
                        break
                    print("   请输入1-5之间的数字")
                except ValueError:
                    print("   请输入数字")
        
        avg = freq / len(indicators)
        
        if avg <= 2:
            status = "无明显剥夺"
        elif avg <= 3.5:
            status = "轻度剥夺"
        elif avg <= 4.5:
            status = "中度剥夺"
        else:
            status = "严重剥夺"
        
        results.append({
            "type": dep_name,
            "avg_score": round(avg, 2),
            "status": status
        })
    
    return {"deprivations": results}


def generate_diagnosis_report(diagnoses: Dict, child_age: str) -> str:
    """生成综合诊断报告"""
    report = []
    report.append("\n")
    report.append("=" * 60)
    report.append("【综合诊断报告】")
    report.append("=" * 60)
    report.append(f"\n孩子年龄: {child_age}")
    report.append(f"诊断时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 四轴汇总
    report.append("\n\n【四轴诊断汇总】")
    report.append("-" * 40)
    
    axis_scores = []
    for axis_name in ["控制权轴", "解释权轴", "能量流轴", "责任归属轴"]:
        result = diagnoses[axis_name]
        score = result["avg_score"]
        axis_scores.append(score)
        status_icon = {"健康": "✓", "轻度失衡": "△", "中度失衡": "⚠", "严重失衡": "✗"}[result["status"]]
        report.append(f"{status_icon} {axis_name}: {score}/5.0 ({result['status']})")
    
    overall_axis = sum(axis_scores) / len(axis_scores)
    report.append(f"\n总体四轴评分: {overall_axis:.2f}/5.0")
    
    if overall_axis <= 2:
        report.append("评估: 整体健康，主体性保护良好")
    elif overall_axis <= 3.5:
        report.append("评估: 存在轻度失衡，需要关注")
    elif overall_axis <= 4.5:
        report.append("评估: 存在中度失衡，需要干预")
    else:
        report.append("评估: 存在严重失衡，建议寻求专业帮助")
    
    # 熵调节
    entropy = diagnoses["entropy"]
    report.append(f"\n【熵调节状态】: {entropy['type']}")
    report.append(f"风险等级: {entropy['risk']}")
    report.append(f"说明: {entropy['description']}")
    
    # 三重剥夺
    report.append("\n【三重剥夺评估】")
    report.append("-" * 40)
    
    for dep in diagnoses["deprivations"]["deprivations"]:
        status_icon = {"无明显剥夺": "✓", "轻度剥夺": "△", "中度剥夺": "⚠", "严重剥夺": "✗"}[dep["status"]]
        report.append(f"{status_icon} {dep['type']}: {dep['avg_score']}/5.0 ({dep['status']})")
    
    # 干预优先级
    report.append("\n\n【干预优先级建议】")
    report.append("-" * 40)
    
    # 找出最严重的问题
    issues = []
    for axis_name in ["控制权轴", "解释权轴", "能量流轴", "责任归属轴"]:
        result = diagnoses[axis_name]
        if result["avg_score"] > 2.5:
            issues.append((axis_name, result["avg_score"], result["status"]))
    
    for dep in diagnoses["deprivations"]["deprivations"]:
        if dep["avg_score"] > 2.5:
            issues.append((dep["type"], dep["avg_score"], dep["status"]))
    
    # 排序并输出
    issues.sort(key=lambda x: x[1], reverse=True)
    
    for i, (name, score, status) in enumerate(issues[:5], 1):
        report.append(f"{i}. {name}: {score:.1f}分 ({status})")
    
    if not issues:
        report.append("✓ 未发现需要干预的问题")
    
    # 年龄段建议
    report.append("\n\n【年龄段重点关注】")
    report.append("-" * 40)
    
    age_advice = {
        "0-3": "建立安全依恋是最高优先级。确保及时回应，保护自主探索的萌芽。",
        "3-6": "保护自主性是关键。提供有限选择，允许适度的'不'和反抗。",
        "6-12": "培养能力感为重点。关注过程而非结果，支持自我管理尝试。",
        "12+": "支持身份探索是核心。尊重独立性，允许试错，提供情感支持。"
    }
    
    age_key = "12+" if child_age.endswith(("岁", "+")) and int(child_age.replace("+", "").replace("岁", "").split("-")[0]) >= 12 else child_age
    report.append(f"当前建议: {age_advice.get(age_key, age_advice['6-12'])}")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(description="亲子关系四轴诊断工具")
    parser.add_argument("--age", type=str, default="6-12", help="孩子年龄，如 '6-12' 或 '12+'")
    parser.add_argument("--interactive", action="store_true", help="交互式诊断")
    parser.add_argument("--output", type=str, help="输出报告文件路径")
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("   亲子关系四轴诊断系统")
    print("   评估维度: 控制权 | 解释权 | 能量流 | 责任归属")
    print("=" * 60)
    
    child_age = args.age
    
    # 执行诊断
    diagnoses = {
        "控制权轴": diagnose_control_axis(),
        "解释权轴": diagnose_explanation_axis(),
        "能量流轴": diagnose_energy_axis(),
        "责任归属轴": diagnose_responsibility_axis(),
        "entropy": diagnose_entropy_adjustment(),
        "deprivations": diagnose_threefold_deprivation()
    }
    
    # 生成报告
    report = generate_diagnosis_report(diagnoses, child_age)
    print(report)
    
    # 输出到文件
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n报告已保存至: {args.output}")
    
    # 输出JSON格式数据（供其他工具使用）
    output_data = {
        "child_age": child_age,
        "diagnosis_time": __import__('datetime').datetime.now().isoformat(),
        "four_axis": {k: v for k, v in diagnoses.items() if k in ["控制权轴", "解释权轴", "能量流轴", "责任归属轴"]},
        "entropy": diagnoses["entropy"],
        "deprivations": diagnoses["deprivations"]
    }
    
    print("\n【JSON格式数据】")
    print(json.dumps(output_data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
