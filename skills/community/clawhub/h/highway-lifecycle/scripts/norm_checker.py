#!/usr/bin/env python3
"""
桥梁设计文档审查工具
用于检查规范符合性和上下文一致性
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# 规范版本映射
NORM_VERSIONS = {
    "JTG/T F50": {"current": "JTG/T 3650-2020", "name": "《公路桥涵施工技术规范》"},
    "JTG/T B02-01": {"current": "JTG/T 2231-01-2020", "name": "《公路桥梁抗震设计规范》"},
    "JT/T 329": {"current": "JT/T 329-2025", "name": "《公路桥梁预应力钢绞线用锚具、夹具和连接器》"},
    "JT/T 1062": {"current": "JT/T 1062-2025", "name": "《桥梁减隔震装置通用技术条件》"},
    "JTG D62": {"current": "JTG 3362-2018", "name": "《公路钢筋混凝土及预应力混凝土桥涵设计规范》"},
}

# 规范限值表
NORM_LIMITS = {
    "水胶比": {"C30": 0.55, "C40": 0.45, "C50": 0.36},
    "裂缝宽度": {"I类环境": {"钢筋混凝土": 0.20, "预应力": 0.10}, "II类环境": {"钢筋混凝土": 0.15, "预应力": 0}},
    "保护层厚度": {"I-A类_100年": {"板": 30, "梁": 35, "柱": 40}},
}


def check_norm_version(cited_norm: str) -> Dict:
    """检查规范版本是否为最新"""
    result = {"status": "pass", "issues": []}
    
    for old_prefix, info in NORM_VERSIONS.items():
        if old_prefix in cited_norm:
            current = info["current"]
            if current not in cited_norm:
                result["status"] = "fail"
                result["issues"].append({
                    "type": "规范版本过时",
                    "cited": cited_norm,
                    "current": current,
                    "correct_name": info["name"],
                })
    
    return result


def check_parameter_consistency(params: Dict[str, List]) -> Dict:
    """检查参数一致性"""
    result = {"status": "pass", "inconsistencies": []}
    
    for param_name, values in params.items():
        unique_values = set(values)
        if len(unique_values) > 1:
            result["status"] = "fail"
            result["inconsistencies"].append({
                "parameter": param_name,
                "values": list(unique_values),
                "locations": values,
            })
    
    return result


def check_value_against_norm(param_name: str, value: float, conditions: Dict) -> Dict:
    """检查数值是否符合规范限值"""
    result = {"status": "pass", "issues": []}
    
    if param_name in NORM_LIMITS:
        limits = NORM_LIMITS[param_name]
        
        # 根据条件查找限值
        limit_value = None
        for key, val in limits.items():
            if key in str(conditions):
                if isinstance(val, dict):
                    # 需要进一步匹配
                    for sub_key, sub_val in val.items():
                        if sub_key in str(conditions):
                            limit_value = sub_val
                            break
                else:
                    limit_value = val
                break
        
        if limit_value is not None:
            if value > limit_value:
                result["status"] = "fail"
                result["issues"].append({
                    "type": "数值超限",
                    "parameter": param_name,
                    "value": value,
                    "limit": limit_value,
                    "condition": conditions,
                })
    
    return result


def extract_parameters_from_text(text: str) -> Dict[str, List]:
    """从文本中提取参数"""
    params = {}
    
    # 混凝土等级
    concrete_pattern = r"C\d+"
    concrete_matches = re.findall(concrete_pattern, text)
    if concrete_matches:
        params["混凝土等级"] = concrete_matches
    
    # 钢材牌号
    steel_pattern = r"Q\d+[A-D]"
    steel_matches = re.findall(steel_pattern, text)
    if steel_matches:
        params["钢材牌号"] = steel_matches
    
    # 保护层厚度
    cover_pattern = r"保护层厚度[:：]?\s*(\d+)\s*mm"
    cover_matches = re.findall(cover_pattern, text)
    if cover_matches:
        params["保护层厚度"] = cover_matches
    
    # 水胶比
    w_b_pattern = r"水胶比[:：]?\s*([\d.]+)"
    w_b_matches = re.findall(w_b_pattern, text)
    if w_b_matches:
        params["水胶比"] = w_b_matches
    
    return params


def generate_review_report(results: Dict) -> str:
    """生成审查报告"""
    report = []
    report.append("# 桥梁设计文档审查报告\n")
    
    # 规范符合性
    report.append("## 一、规范符合性审查\n")
    if results.get("norm_issues"):
        for issue in results["norm_issues"]:
            report.append(f"- **{issue['type']}**\n")
            report.append(f"  - 引用：{issue['cited']}\n")
            report.append(f"  - 正确：{issue['correct_name']}（{issue['current']}）\n")
    else:
        report.append("未发现规范符合性问题。\n")
    
    # 上下文一致性
    report.append("\n## 二、上下文一致性审查\n")
    if results.get("consistency_issues"):
        for issue in results["consistency_issues"]:
            report.append(f"- **{issue['parameter']}不一致**\n")
            report.append(f"  - 发现值：{issue['values']}\n")
    else:
        report.append("未发现上下文一致性问题。\n")
    
    # 数值限值
    report.append("\n## 三、数值限值审查\n")
    if results.get("limit_issues"):
        for issue in results["limit_issues"]:
            report.append(f"- **{issue['parameter']}超限**\n")
            report.append(f"  - 设计值：{issue['value']}\n")
            report.append(f"  - 限值：{issue['limit']}\n")
    else:
        report.append("未发现数值超限问题。\n")
    
    return "\n".join(report)


def review_document(text: str, project_context: Optional[Dict] = None) -> Dict:
    """审查文档主函数"""
    results = {
        "norm_issues": [],
        "consistency_issues": [],
        "limit_issues": [],
    }
    
    # 1. 检查规范版本
    norm_pattern = r"[《<]([^》>]+)[》>]\s*\(([^)]+)\)"
    norm_matches = re.findall(norm_pattern, text)
    for name, code in norm_matches:
        full_citation = f"{name}（{code}）"
        check_result = check_norm_version(full_citation)
        if check_result["status"] == "fail":
            results["norm_issues"].extend(check_result["issues"])
    
    # 2. 检查参数一致性
    params = extract_parameters_from_text(text)
    consistency_result = check_parameter_consistency(params)
    if consistency_result["status"] == "fail":
        results["consistency_issues"] = consistency_result["inconsistencies"]
    
    # 3. 检查数值限值
    # TODO: 实现更完善的数值限值检查
    
    return results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python norm_checker.py <document_file>")
        sys.exit(1)
    
    doc_path = Path(sys.argv[1])
    if not doc_path.exists():
        print(f"Error: File not found: {doc_path}")
        sys.exit(1)
    
    text = doc_path.read_text(encoding="utf-8")
    results = review_document(text)
    report = generate_review_report(results)
    print(report)