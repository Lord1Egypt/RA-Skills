#!/usr/bin/env python3
"""
PayAClaw Helper - 任务助手
帮助用户完成PayAClaw任务的工作流助手
"""

import argparse
import json
import os
import sys
from datetime import datetime

# 评分标准清单
SCORING_CHECKLIST = """
## 评分标准检查清单

### 内容完整性 (25分)
- [ ] 任务要求的所有要点都已覆盖
- [ ] 没有遗漏关键信息
- [ ] 内容结构完整（开头、正文、结尾）

### 格式规范性 (25分)
- [ ] 标题格式正确
- [ ] 段落层次清晰
- [ ] 使用适当的标记和列表
- [ ] 长度符合要求

### 价值贡献度 (25分)
- [ ] 提供实用的信息或解决方案
- [ ] 内容有独到见解
- [ ] 对目标受众有实际帮助
- [ ] 避免了常识性重复

### 专业程度 (25分)
- [ ] 用词准确专业
- [ ] 逻辑清晰严谨
- [ ] 数据/案例真实可靠
- [ ] 无语法或表达错误

## 总分评估
- 90-100分: 优秀
- 75-89分: 良好
- 60-74分: 合格
- 60分以下: 需要改进
"""

# 提交格式模板
SUBMISSION_TEMPLATE = """
## PayAClaw 任务提交格式

### 基本信息
- 任务名称: {task_name}
- 提交时间: {submit_time}
- 难度等级: {difficulty}

### 内容摘要
{summary}

### 详细内容
{content}

### 附加说明
{additional}

### 自评分数
{self_score}

---
*提交格式版本: v1.0*
"""

# 任务分析提示词
ANALYZE_PROMPT = """分析以下任务，并提供执行建议：

任务描述：
{task}

请分析：
1. 任务核心目标
2. 关键要求点
3. 建议的执行步骤
4. 可能遇到的难点
"""

# 内容生成提示词
GENERATE_PROMPT = """根据以下任务和背景信息，生成内容方案：

任务：{task}
背景：{context}

请生成：
1. 内容大纲
2. 各部分要点
3. 参考模板/示例
4. 注意事项
"""

def analyze_task(task: str) -> str:
    """分析任务"""
    prompt = ANALYZE_PROMPT.format(task=task)
    return f"""# 任务分析报告
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 原始任务
{task}

## 分析结果
{prompt}

---
请将上述分析发送给AI助手获取详细分析结果
"""

def generate_content(task: str, context: str = "") -> str:
    """生成内容"""
    prompt = GENERATE_PROMPT.format(task=task, context=context)
    return f"""# 内容生成方案
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 任务
{task}

## 背景信息
{context or '未提供'}

## 生成方案
{prompt}

---
请将上述提示发送给AI助手获取完整内容
"""

def check_content(content: str) -> str:
    """检查内容"""
    return f"""# 内容评分检查
检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 待检查内容
{content}

## 评分标准
{SCORING_CHECKLIST}

## 检查指引
请根据上述评分标准逐项检查内容，并给出：
1. 每项得分
2. 具体改进建议
3. 最终总分
"""

def format_content(task_name: str, content: str, summary: str = "", 
                   additional: str = "", self_score: str = "") -> str:
    """格式化内容"""
    template = SUBMISSION_TEMPLATE.format(
        task_name=task_name,
        submit_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        difficulty="中等",
        summary=summary or "见详细内容",
        content=content,
        additional=additional or "无",
        self_score=self_score or "待评分"
    )
    return template

def main():
    parser = argparse.ArgumentParser(description='PayAClaw Helper - 任务助手')
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # analyze 命令
    analyze_parser = subparsers.add_parser('analyze', help='分析任务')
    analyze_parser.add_argument('task', help='任务描述')
    
    # generate 命令
    generate_parser = subparsers.add_parser('generate', help='生成内容')
    generate_parser.add_argument('--task', '-t', required=True, help='任务描述')
    generate_parser.add_argument('--context', '-c', default='', help='背景信息')
    
    # check 命令
    check_parser = subparsers.add_parser('check', help='检查内容')
    check_parser.add_argument('--content', required=True, help='待检查的内容')
    
    # format 命令
    format_parser = subparsers.add_parser('format', help='格式化提交')
    format_parser.add_argument('--task', required=True, help='任务名称')
    format_parser.add_argument('--content', required=True, help='原始内容')
    format_parser.add_argument('--summary', default='', help='内容摘要')
    format_parser.add_argument('--additional', default='', help='附加说明')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        result = analyze_task(args.task)
    elif args.command == 'generate':
        result = generate_content(args.task, args.context)
    elif args.command == 'check':
        result = check_content(args.content)
    elif args.command == 'format':
        result = format_content(args.task, args.content, args.summary)
    else:
        parser.print_help()
        return
    
    print(result)
    
    # 保存到文件
    output_file = f"payaclaw_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"\n💾 结果已保存到: {output_file}")

if __name__ == '__main__':
    main()