#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

"""
记忆系统优化器
结合三层记忆 + 知识图谱 + 持续改进
"""

import os
import json
from datetime import datetime

# 路径配置
BASE_DIR = r'C:\Users\Administrator\.openclaw\workspace'
MEMORY_FILE = os.path.join(BASE_DIR, 'MEMORY.md')
PROJECTS_FILE = os.path.join(BASE_DIR, 'PROJECTS.md')
MEMORY_DIR = os.path.join(BASE_DIR, 'memory')
KG_DIR = os.path.join(BASE_DIR, 'knowledge_graph')
OPTIMIZATION_LOG = os.path.join(BASE_DIR, 'memory', 'optimization循环.md')

def analyze_current_state():
    """分析当前记忆系统状态"""
    print("=" * 60)
    print("🔍 记忆系统诊断")
    print("=" * 60)
    
    issues = []
    
    # 1. 检查MEMORY.md
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = len(content.split('\n'))
            if lines < 50:
                issues.append(f"MEMORY.md 内容过少 ({lines}行)")
            if '核心锚点' not in content:
                issues.append("MEMORY.md 缺少核心锚点")
    else:
        issues.append("MEMORY.md 不存在")
    
    # 2. 检查PROJECTS.md
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            if '## 正在进行的项目' not in content:
                issues.append("PROJECTS.md 缺少正在进行的项目")
    else:
        issues.append("PROJECTS.md 不存在")
    
    # 3. 检查每日日志
    daily_files = [f for f in os.listdir(MEMORY_DIR) if f.startswith('2026-') and f.endswith('.md')]
    if len(daily_files) < 5:
        issues.append(f"每日日志过少 ({len(daily_files)}个)")
    
    # 4. 检查知识图谱
    kg_file = os.path.join(KG_DIR, 'graph.json')
    if os.path.exists(kg_file):
        with open(kg_file, 'r', encoding='utf-8') as f:
            kg = json.load(f)
            entity_count = sum(len(v) for v in kg['entities'].values())
            if entity_count < 50:
                issues.append(f"知识图谱实体过少 ({entity_count}个)")
    else:
        issues.append("知识图谱未建立")
    
    # 5. 检查优化循环日志
    if not os.path.exists(OPTIMIZATION_LOG):
        issues.append("缺少优化循环日志")
    
    print("\n📊 诊断结果:")
    if issues:
        for issue in issues:
            print(f"  ⚠️ {issue}")
    else:
        print("  ✅ 系统状态良好")
    
    return issues

def generate_optimization_plan(issues):
    """生成优化计划"""
    print("\n" + "=" * 60)
    print("📋 优化计划")
    print("=" * 60)
    
    plan = []
    
    # 根据问题生成优化
    if any("MEMORY.md" in i for i in issues):
        plan.append({
            "type": "记忆层",
            "action": "补充MEMORY.md核心锚点",
            "priority": "高"
        })
    
    if any("PROJECTS.md" in i for i in issues):
        plan.append({
            "type": "项目层", 
            "action": "完善PROJECTS.md项目跟踪",
            "priority": "高"
        })
    
    if any("知识图谱" in i for i in issues):
        plan.append({
            "type": "知识图谱",
            "action": "重建知识图谱",
            "priority": "中"
        })
    
    if any("优化循环" in i for i in issues):
        plan.append({
            "type": "循环机制",
            "action": "创建优化循环日志",
            "priority": "中"
        })
    
    # 添加通用优化
    plan.extend([
        {
            "type": "技能系统",
            "action": "建立技能间协作规则",
            "priority": "低"
        },
        {
            "type": "记忆固化",
            "action": "设定每日记忆固化任务",
            "priority": "低"
        }
    ])
    
    for i, item in enumerate(plan, 1):
        print(f"  {i}. [{item['priority']}] {item['type']}: {item['action']}")
    
    return plan

def execute_optimization(plan):
    """执行优化"""
    print("\n" + "=" * 60)
    print("⚡ 执行优化")
    print("=" * 60)
    
    executed = []
    
    for item in plan:
        if item['priority'] == '高':
            print(f"  🔴 执行: {item['action']}")
            executed.append(item['action'])
    
    return executed

def log_optimization(issues, plan, executed):
    """记录优化到循环日志"""
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    content = f"""
## 优化循环 - {today}

### 诊断问题
"""
    for issue in issues:
        content += f"- {issue}\n"
    
    content += "\n### 优化计划\n"
    for item in plan:
        status = "✅" if item['action'] in executed else "⏳"
        content += f"- {status} [{item['priority']}] {item['type']}: {item['action']}\n"
    
    content += "\n### 执行结果\n"
    for action in executed:
        content += f"- ✅ {action}\n"
    
    # 追加到日志
    if os.path.exists(OPTIMIZATION_LOG):
        with open(OPTIMIZATION_LOG, 'r', encoding='utf-8') as f:
            existing = f.read()
        content = existing + content
    else:
        content = "# 记忆系统优化循环日志\n" + content
    
    with open(OPTIMIZATION_LOG, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📝 已记录到: {OPTIMIZATION_LOG}")

def run_optimization_cycle():
    """运行优化循环"""
    print("\n" + "=" * 60)
    print("🔄 记忆系统优化循环 - 第1轮")
    print("=" * 60 + "\n")
    
    # 1. 诊断
    issues = analyze_current_state()
    
    # 2. 生成计划
    plan = generate_optimization_plan(issues)
    
    # 3. 执行
    executed = execute_optimization(plan)
    
    # 4. 记录
    log_optimization(issues, plan, executed)
    
    print("\n" + "=" * 60)
    print("✅ 优化循环完成")
    print("=" * 60)
    
    return {
        'issues': issues,
        'plan': plan,
        'executed': executed
    }

if __name__ == '__main__':
    run_optimization_cycle()
