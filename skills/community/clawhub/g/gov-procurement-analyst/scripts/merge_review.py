#!/usr/bin/env python3
"""
标书协作引擎 - 合并审校脚本
功能：全文一致性检查（交叉引用编号、术语统一表、格式规范扫描）+ 输出修订清单
版本：v5.2.0
"""

import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime

# 运行时数据库路径（符合死规则 #12 运行时例外）
OUTPUT_DIR = Path.home() / ".workbuddy" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
GOV_COLLAB_DB = OUTPUT_DIR / "gov_collab.db"


def merge_review(project_id: str, chapters: dict) -> dict:
    """
    合并审校：全文一致性检查
    
    Args:
        project_id: 项目ID
        chapters: 章节内容字典 {chapter_name: content}
    
    Returns:
        审校报告（含修订清单）
    """
    issues = []
    
    # 1. 交叉引用编号一致性检查
    issues.extend(_check_cross_references(chapters))
    
    # 2. 术语统一表检查
    issues.extend(_check_terminology(chapters))
    
    # 3. 格式规范扫描
    issues.extend(_check_format(chapters))
    
    # 4. 资质数据一致性检查
    issues.extend(_check_qualification_data(chapters))
    
    # 生成审校报告
    report = {
        "project_id": project_id,
        "review_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_chapters": len(chapters),
        "total_issues": len(issues),
        "issues": issues,
        "summary": _generate_summary(issues),
        "quality_score": _calculate_quality_score(issues),
    }
    
    return report


def _check_cross_references(chapters: dict) -> list:
    """交叉引用编号一致性检查"""
    issues = []
    
    # 收集所有章节标题和编号
    chapter_numbers = {}
    for chapter_name, content in chapters.items():
        # 提取章节编号（如 1.1, 2.3.1）
        numbers = re.findall(r'^(\d+(?:\.\d+)*)\s', content, re.MULTILINE)
        for num in numbers:
            chapter_numbers[num] = chapter_name
    
    # 检查引用是否指向存在的章节
    for chapter_name, content in chapters.items():
        # 查找引用（如"见3.2.1节"、"参见第2章"）
        refs = re.findall(r'(?:见|参见|详见)\s*(\d+(?:\.\d+)*)\s*(?:节|章)', content)
        for ref in refs:
            if ref not in chapter_numbers:
                issues.append({
                    "type": "交叉引用",
                    "severity": "medium",
                    "location": chapter_name,
                    "description": f"「{ref}」但无对应章节",
                    "suggestion": f"更正为已存在的章节编号",
                })
    
    # 检查图表编号连续性
    for chapter_name, content in chapters.items():
        fig_numbers = re.findall(r'图(\d+)', content)
        if fig_numbers:
            fig_nums = sorted([int(n) for n in fig_numbers])
            for i in range(1, len(fig_nums)):
                if fig_nums[i] - fig_nums[i-1] > 1:
                    missing = list(range(fig_nums[i-1]+1, fig_nums[i]))
                    issues.append({
                        "type": "交叉引用",
                        "severity": "low",
                        "location": chapter_name,
                        "description": f"图表编号不连续（图{fig_nums[i-1]}→图{fig_nums[i]}，缺少图{', 图'.join(map(str, missing))}）",
                        "suggestion": "检查图表编号是否连续",
                    })
    
    return issues


def _check_terminology(chapters: dict) -> list:
    """术语统一表检查"""
    issues = []
    
    # 常见术语同义词映射
    term_synonyms = {
        "甲方": ["采购人", "采购单位", "招标人", "业主"],
        "乙方": ["投标人", "供应商", "中标人"],
        "投标保证金": ["保证金", "投标保证金"],
        "履约保证金": ["履约保证金", "履约担保"],
    }
    
    # 统计术语使用频率
    term_usage = {}
    for chapter_name, content in chapters.items():
        for canonical, synonyms in term_synonyms.items():
            for term in [canonical] + synonyms:
                count = len(re.findall(re.escape(term), content))
                if count > 0:
                    term_usage.setdefault(canonical, {})
                    term_usage[canonical][term] = term_usage[canonical].get(term, 0) + count
    
    # 检查是否混用
    for canonical, usage in term_usage.items():
        if len(usage) > 1:
            # 混用了多个同义词
            used_terms = list(usage.keys())
            issues.append({
                "type": "术语统一",
                "severity": "medium",
                "location": "全文",
                "description": f"混用术语：{', '.join([f'{t}({usage[t]}次)' for t in used_terms])}",
                "suggestion": f"统一为「{canonical}」",
            })
    
    return issues


def _check_format(chapters: dict) -> list:
    """格式规范扫描"""
    issues = []
    
    # 字体使用一致性（从内容中的Markdown标记推断）
    font_patterns = {
        "bold": r'\*\*.*?\*\*',
        "heading": r'#{1,6}\s',
        "table": r'\|.*?\|',
    }
    
    for chapter_name, content in chapters.items():
        # 检查标题格式一致性
        headings = re.findall(r'^#{1,6}\s+.+$', content, re.MULTILINE)
        if headings:
            heading_levels = [len(h.split()[0]) for h in headings]
            # 检查标题层级是否合理（如出现# ###跳跃）
            for i in range(1, len(heading_levels)):
                if heading_levels[i] - heading_levels[i-1] > 1:
                    issues.append({
                        "type": "格式规范",
                        "severity": "low",
                        "location": chapter_name,
                        "description": f"标题层级跳跃（{'#'*heading_levels[i-1]}→{'#'*heading_levels[i]}）",
                        "suggestion": f"检查标题层级是否连续",
                    })
        
        # 检查金额格式一致性
        amounts = re.findall(r'¥?\s*(\d+(?:\.\d+)?)\s*(万元|元|万)', content)
        if amounts:
            units = set(a[1] for a in amounts)
            if len(units) > 1:
                issues.append({
                    "type": "格式规范",
                    "severity": "low",
                    "location": chapter_name,
                    "description": f"金额单位混用：{', '.join(units)}",
                    "suggestion": "统一为「万元」",
                })
    
    return issues


def _check_qualification_data(chapters: dict) -> list:
    """资质数据一致性检查"""
    issues = []
    
    # 统一社会信用代码格式
    credit_code_pattern = r'[0-9A-Z]{18}'
    
    # 提取各章节的资质相关信息
    qual_data = {}
    for chapter_name, content in chapters.items():
        codes = re.findall(credit_code_pattern, content)
        if codes:
            qual_data[chapter_name] = codes
    
    # 检查不同章节的信用代码是否一致
    all_codes = set()
    for codes in qual_data.values():
        all_codes.update(codes)
    
    if len(all_codes) > 1:
        issues.append({
            "type": "数据一致性",
            "severity": "high",
            "location": "全文",
            "description": f"统一社会信用代码不一致（发现{len(all_codes)}个不同代码）",
            "suggestion": "核对并统一为正确的统一社会信用代码",
        })
    
    # 检查有效期格式一致性
    date_patterns = [
        r'\d{4}年\d{1,2}月\d{1,2}日',
        r'\d{4}-\d{2}-\d{2}',
        r'\d{4}/\d{2}/\d{2}',
    ]
    
    for chapter_name, content in chapters.items():
        used_patterns = []
        for pattern in date_patterns:
            if re.search(pattern, content):
                used_patterns.append(pattern)
        if len(used_patterns) > 1:
            issues.append({
                "type": "数据一致性",
                "severity": "low",
                "location": chapter_name,
                "description": "日期格式混用",
                "suggestion": "统一为「YYYY年MM月DD日」格式",
            })
    
    return issues


def _generate_summary(issues: list) -> str:
    """生成审校总结"""
    if not issues:
        return "✅ 审校通过，全文一致性问题"
    
    severity_count = {"high": 0, "medium": 0, "low": 0}
    type_count = {}
    
    for issue in issues:
        severity_count[issue["severity"]] += 1
        type_count[issue["type"]] = type_count.get(issue["type"], 0) + 1
    
    parts = []
    for severity, count in severity_count.items():
        if count > 0:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[severity]
            parts.append(f"{icon} {severity}: {count}项")
    
    type_parts = ", ".join([f"{t}{c}项" for t, c in type_count.items()])
    
    return f"发现问题{len(issues)}项（{type_parts}）"


def _calculate_quality_score(issues: list) -> int:
    """计算质量评分（满分100）"""
    score = 100
    for issue in issues:
        if issue["severity"] == "high":
            score -= 10
        elif issue["severity"] == "medium":
            score -= 5
        elif issue["severity"] == "low":
            score -= 2
    return max(0, score)


if __name__ == "__main__":
    # 示例用法
    sample_chapters = {
        "投标函及法定代表人证明": """
# 1. 投标函
## 1.1 投标函
我方愿参加XX项目的投标。
## 1.2 法定代表人证明
我方法定代表人为张三。
""",
        "技术方案": """
# 2. 技术方案
## 2.1 技术路线
采用云计算技术路线。
## 2.2 实施方案
分三期实施，见3.2.1节（引用不存在）。
""",
        "商务文件": """
# 3. 商务文件
## 3.1 企业简介
北京XX科技有限公司成立于2018年。
## 3.2 资质说明
我方具备相关资质。甲方要求严格。
""",
    }
    
    report = merge_review("test_project", sample_chapters)
    print(json.dumps(report, ensure_ascii=False, indent=2))
