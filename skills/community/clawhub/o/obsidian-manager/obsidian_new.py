#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 笔记创建工具

用法:
    python obsidian_new.py --title "笔记标题" --direction "01-振动台控制技术"
    python obsidian_new.py --title "笔记标题" --template "literature"
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path


# 研究方向映射
DIRECTIONS = {
    '01': '01-振动台控制技术',
    '02': '02-RTHS 子结构试验',
    '03': '03-文物隔震',
    '04': '04-粉末阻尼',
    '05': '05-超材料隔震',
    '06': '06-NTMD 减振',
    '07': '07-地震预测',
    '08': '08-爆破模拟地震',
    '09': '09-实验室管理',
    '10': '10-研究生培养'
}

# 笔记模板
TEMPLATES = {
    'default': '''# {title}

**创建时间：** {date}  
**标签：** {tags}

---

## 概述

待填充

---

## 核心内容

待填充

---

## 相关笔记

[[INDEX|返回总索引]]

---

**备注：** 本笔记待填充。
''',
    
    'literature': '''---
title: {title}
authors: {authors}
year: {year}
journal: {journal}
tags: [文献，{direction}]
zotero-link: {zotero_link}
created: {date}
---

# {title}

## 核心贡献

待填充

---

## 研究方法

待填充

---

## 主要结论

待填充

---

## 我的思考

待填充

---

## 相关研究
[[相关笔记链接]]

---

**备注：** 本笔记待填充。
''',
    
    'topic': '''---
title: {title}
tags: [主题，{direction}]
created: {date}
---

# {title}

## 概述

待填充

---

## 核心概念

待填充

---

## 关键文献
- [[文献笔记 1]]
- [[文献笔记 2]]

---

## 研究进展

待填充

---

## 待解决问题

待填充

---

**备注：** 本笔记待填充。
''',
    
    'experiment': '''---
title: {title}
date: {date}
tags: [实验，{direction}]
---

# {title}

## 实验目的

待填充

---

## 实验设备

待填充

---

## 实验步骤

待填充

---

## 实验数据

待填充

---

## 结果分析

待填充

---

## 下一步计划

待填充

---

**备注：** 本笔记待填充。
'''
}


def get_research_base_path():
    """获取 research 基础路径"""
    base = Path(__file__).parent.parent / 'research'
    if not base.exists():
        # 尝试其他可能路径
        base = Path(r'D:\Personal\OpenClaw\research')
    return base


def get_direction_path(direction):
    """获取研究方向目录路径"""
    base = get_research_base_path()
    
    # 如果 direction 是编号（如"01"），转换为完整名称
    if direction in DIRECTIONS:
        direction = DIRECTIONS[direction]
    
    dir_path = base / direction
    if not dir_path.exists():
        print(f"错误：研究方向目录不存在：{dir_path}")
        print(f"可用方向：{', '.join(DIRECTIONS.values())}")
        return None
    
    return dir_path


def create_note(title, direction='01', template='default', authors='', year='', journal='', zotero_link=''):
    """创建笔记"""
    # 获取目录路径
    dir_path = get_direction_path(direction)
    if not dir_path:
        return None
    
    # 生成文件名
    filename = f"{title}.md"
    file_path = dir_path / filename
    
    # 检查文件是否已存在
    if file_path.exists():
        print(f"警告：文件已存在：{file_path}")
        overwrite = input("是否覆盖？(y/n): ")
        if overwrite.lower() != 'y':
            print("已取消")
            return None
    
    # 获取方向名称
    direction_name = direction
    for k, v in DIRECTIONS.items():
        if v == direction:
            direction_name = v
            break
    
    # 准备模板参数
    params = {
        'title': title,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
        'tags': direction,
        'direction': direction_name,
        'authors': authors,
        'year': year,
        'journal': journal,
        'zotero_link': zotero_link
    }
    
    # 获取模板
    template_content = TEMPLATES.get(template, TEMPLATES['default'])
    
    # 填充模板
    content = template_content.format(**params)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return file_path


def main():
    parser = argparse.ArgumentParser(description='Obsidian 笔记创建工具')
    parser.add_argument('--title', '-t', type=str, required=True, help='笔记标题')
    parser.add_argument('--direction', '-d', type=str, default='01', 
                       help='研究方向（编号或名称）')
    parser.add_argument('--template', '-tpl', type=str, default='default',
                       choices=['default', 'literature', 'topic', 'experiment'],
                       help='笔记模板类型')
    parser.add_argument('--authors', type=str, default='', help='作者（文献笔记用）')
    parser.add_argument('--year', type=str, default='', help='年份（文献笔记用）')
    parser.add_argument('--journal', type=str, default='', help='期刊（文献笔记用）')
    parser.add_argument('--zotero-link', type=str, default='', help='Zotero 链接（文献笔记用）')
    
    args = parser.parse_args()
    
    print(f"创建笔记：{args.title}")
    print(f"研究方向：{args.direction}")
    print(f"模板类型：{args.template}")
    print("-" * 60)
    
    # 创建笔记
    file_path = create_note(
        title=args.title,
        direction=args.direction,
        template=args.template,
        authors=args.authors,
        year=args.year,
        journal=args.journal,
        zotero_link=args.zotero_link
    )
    
    if file_path:
        print(f"\n✅ 笔记创建成功")
        print(f"   文件：{file_path}")
        print(f"   链接：[[{args.direction}/{args.title}]]")
        print(f"\n提示：可以用 Obsidian 打开并编辑笔记")
    else:
        print("\n❌ 笔记创建失败")
        sys.exit(1)


if __name__ == '__main__':
    main()
