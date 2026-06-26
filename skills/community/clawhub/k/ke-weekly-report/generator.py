#!/usr/bin/env python3
"""
周报生成器 - 核心实现
功能：根据用户输入的工作内容，自动生成结构化周报
"""

import json
import sys
from datetime import datetime, timedelta

# 周报模板
WEEKLY_TEMPLATE = """# 周工作报告

**汇报人**: {name}
**部门**: {department}
**汇报周期**: 2026 年 第{week}周（{start_date} - {end_date}）

---

## 一、本周工作完成情况

### 1. 重点工作
{key_work}

### 2. 常规工作
{regular_work}

---

## 二、工作成果与数据

| 任务 | 状态 | 完成度 |
|------|------|--------|
{work_table}

---

## 三、问题与风险

{problems}

---

## 四、下周工作计划

{next_week_plan}

---

## 五、需要支持

{support_needed}
"""

def parse_input(input_text):
    """解析用户输入，提取工作内容"""
    lines = input_text.strip().split('\n')
    work_items = []
    
    for line in lines:
        line = line.strip()
        if line:
            # 移除序号
            if line[0].isdigit() and '.' in line[:3]:
                line = line.split('.', 1)[1].strip()
            work_items.append(line)
    
    return work_items

def categorize_work(work_items):
    """将工作分类为重点工作和常规工作"""
    key_work = []
    regular_work = []
    
    # 简单规则：包含"完成"、"开发"、"项目"的作为重点工作
    for item in work_items:
        if any(kw in item for kw in ['完成', '开发', '项目', '上线', '交付']):
            key_work.append(f"- ✅ {item}")
        else:
            regular_work.append(f"- {item}")
    
    return key_work, regular_work

def generate_work_table(work_items):
    """生成工作表格"""
    rows = []
    for item in work_items[:5]:  # 最多 5 项
        task = item[:20] + '...' if len(item) > 20 else item
        rows.append(f"| {task} | 已完成 | 100% |")
    return '\n'.join(rows) if rows else "| 无 | - | - |"

def generate_report(input_text, name="张三", department="技术部"):
    """生成完整周报"""
    work_items = parse_input(input_text)
    key_work, regular_work = categorize_work(work_items)
    
    # 计算周数
    today = datetime.now()
    week_num = today.isocalendar()[1]
    start_date = (today - timedelta(days=today.weekday())).strftime('%m.%d')
    end_date = (today + timedelta(days=6-today.weekday())).strftime('%m.%d')
    
    # 填充模板
    report = WEEKLY_TEMPLATE.format(
        name=name,
        department=department,
        week=week_num,
        start_date=start_date,
        end_date=end_date,
        key_work='\n'.join(key_work) if key_work else "- 无重点工作",
        regular_work='\n'.join(regular_work) if regular_work else "- 无",
        work_table=generate_work_table(work_items),
        problems="- 无重大风险",
        next_week_plan="1. 继续推进当前项目\n2. 完成技术文档编写",
        support_needed="- 无"
    )
    
    return report

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python weekly_report.py '工作内容 1,工作内容 2,...'")
        sys.exit(1)
    
    input_text = sys.argv[1]
    report = generate_report(input_text)
    print(report)

if __name__ == '__main__':
    main()
