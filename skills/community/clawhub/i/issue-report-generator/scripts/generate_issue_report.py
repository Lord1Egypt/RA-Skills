#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
医疗设备软件问题报告生成器
根据用户输入的缺陷描述，自动生成符合规范的问题报告
"""

import json
import sys
from datetime import datetime

def analyze_severity(description: str) -> str:
    """根据问题描述自动判断严重等级"""
    keywords_high = ['崩溃', '死机', '数据丢失', '患者安全', '误诊', '错误结果', '无法启动', '系统瘫痪']
    keywords_medium = ['卡顿', '延迟', '偶发', '有时', '部分', '显示错误', '功能异常']
    keywords_low = ['界面', '文字', '拼写', '提示', '建议', '优化', '体验']
    
    desc_lower = description.lower()
    
    for kw in keywords_high:
        if kw in description:
            return '高'
    for kw in keywords_medium:
        if kw in description:
            return '中'
    for kw in keywords_low:
        if kw in description:
            return '低'
    
    return '中'  # 默认中等

def generate_issue_report(user_input: str) -> dict:
    """生成结构化问题报告"""
    
    severity = analyze_severity(user_input)
    
    report = {
        '问题标题': '[待完善] 请用一句话概括问题',
        '严重等级': severity,
        '报告日期': datetime.now().strftime('%Y-%m-%d'),
        '报告人': '[待填写]',
        '软件版本': '[待填写，如 v2.3.1]',
        '硬件版本': '[待填写，如 RevB]',
        '复现概率': '[待填写，如 必现/约 50%/偶发]',
        '问题现象': '[待完善] 详细描述观察到的异常现象',
        '复现步骤': [
            '[待完善] 步骤 1',
            '[待完善] 步骤 2',
            '[待完善] 步骤 3'
        ],
        '预期结果': '[待填写] 正常情况下应该发生什么',
        '实际结果': '[待填写] 实际发生了什么',
        '影响分析': '[待完善] 该问题对用户使用、患者安全、数据完整性的影响',
        '附件': '[如有截图、日志等请在此注明]',
        '备注': '[其他需要说明的信息]'
    }
    
    return report

def format_markdown(report: dict) -> str:
    """将报告格式化为 Markdown"""
    
    md = f"""# 🐛 问题报告

**报告编号：** ISSUE-{datetime.now().strftime('%Y%m%d')}-001  
**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 基本信息

| 字段 | 内容 |
|------|------|
| **问题标题** | {report['问题标题']} |
| **严重等级** | {report['严重等级']} |
| **报告日期** | {report['报告日期']} |
| **报告人** | {report['报告人']} |
| **软件版本** | {report['软件版本']} |
| **硬件版本** | {report['硬件版本']} |
| **复现概率** | {report['复现概率']} |

---

## 问题描述

### 现象
{report['问题现象']}

### 复现步骤
"""
    
    for i, step in enumerate(report['复现步骤'], 1):
        md += f"{i}. {step}\n"
    
    md += f"""
### 预期结果
{report['预期结果']}

### 实际结果
{report['实际结果']}

---

## 影响分析

{report['影响分析']}

---

## 附件与备注

**附件：** {report['附件']}

**备注：** {report['备注']}

---

## 填写指南

请补充以下信息后提交：

- [ ] **问题标题**：用一句话概括问题（如：试剂仓更换与进核心舱时序冲突）
- [ ] **软件/硬件版本**：填写具体的版本号
- [ ] **复现概率**：必现/高概率 (>50%)/中概率 (10-50%)/低概率 (<10%)/偶发
- [ ] **问题现象**：详细描述观察到的异常，包含报错信息、异常行为等
- [ ] **复现步骤**：按顺序列出可复现问题的操作步骤，确保他人可按此复现
- [ ] **影响分析**：说明对患者安全、测试结果、用户体验的影响

---

**提交目标：** Jira / 禅道 / 质量管理系统
"""
    
    return md

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': '请提供问题描述'}, ensure_ascii=False))
        sys.exit(1)
    
    user_input = ' '.join(sys.argv[1:])
    report = generate_issue_report(user_input)
    markdown = format_markdown(report)
    
    print(markdown)

if __name__ == '__main__':
    main()
