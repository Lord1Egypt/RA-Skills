#!/usr/bin/env python3
"""
学习日志快速写入工具
用法: python add_entry.py --type LRN --title "标题" --content "内容"
"""
import argparse
import os
from datetime import datetime

TEMPLATE = """
## {id}: {title}
**日期**: {date}
**类型**: {type_name}

### 核心
{content}

---
"""

def get_counter_file(learnings_dir):
    counter_file = os.path.join(learnings_dir, ".counter")
    if os.path.exists(counter_file):
        with open(counter_file, "r") as f:
            return int(f.read().strip() or "0")
    return 0

def increment_counter(learnings_dir, count):
    counter_file = os.path.join(learnings_dir, ".counter")
    with open(counter_file, "w") as f:
        f.write(str(count))

def add_entry(entry_type: str, title: str, content: str, workspace: str):
    # 确定类型名称
    type_map = {
        "LRN": "学习/新发现",
        "ERR": "踩坑/错误",
        "FEAT": "技能亮点",
        "DEC": "重要决策",
        "IDEA": "想法/灵感"
    }
    type_name = type_map.get(entry_type, entry_type)
    
    # 日志目录
    learnings_dir = os.path.join(workspace, ".learnings")
    os.makedirs(learnings_dir, exist_ok=True)
    
    # 生成ID
    date = datetime.now().strftime("%Y%m%d")
    counter = get_counter_file(learnings_dir) + 1
    entry_id = f"{entry_type}-{date}-{counter:03d}"
    
    # 写入日志
    log_file = os.path.join(learnings_dir, "LEARNINGS.md")
    
    # 如果文件不存在，创建标题
    if not os.path.exists(log_file):
        with open(log_file, "w", encoding="utf-8") as f:
            f.write("# 学习日志\n\n")
    
    # 追加内容
    entry = TEMPLATE.format(
        id=entry_id,
        title=title,
        date=datetime.now().strftime("%Y-%m-%d"),
        type_name=type_name,
        content=content
    )
    
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry)
    
    # 更新计数器
    increment_counter(learnings_dir, counter)
    
    print(f"✅ 已记录: {entry_id}")
    print(f"📁 位置: {log_file}")
    return entry_id

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="学习日志快速写入")
    parser.add_argument("--type", "-t", default="LRN", choices=["LRN", "ERR", "FEAT", "DEC", "IDEA"])
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--workspace", "-w", default=None)
    
    args = parser.parse_args()
    
    # 确定workspace
    if args.workspace:
        workspace = args.workspace
    else:
        workspace = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        workspace = os.path.dirname(workspace)  # 返回上一级
    
    add_entry(args.type, args.title, args.content, workspace)
