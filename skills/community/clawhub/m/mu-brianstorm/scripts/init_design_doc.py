#!/usr/bin/env python3
"""
初始化设计文档脚本

用法:
    python init_design_doc.py <topic> [--output-dir <dir>]

示例:
    python init_design_doc.py user-auth
    python init_design_doc.py payment-system --output-dir docs/plans
"""

import argparse
import os
from datetime import datetime
from pathlib import Path


TEMPLATE = '''# {title} 设计文档

> 创建日期: {date}
> 状态: 草稿

## 背景

[描述为什么要做这个，解决什么问题]

## 目标

### 核心目标
- [目标 1]
- [目标 2]

### 非目标
- [明确不在范围内的内容]

## 解决方案

### 方案概述
[一句话描述方案]

### 方案对比
| 方案 | 优点 | 缺点 | 结论 |
|------|------|------|------|
| 方案 A | ... | ... | |
| 方案 B | ... | ... | |

## 架构设计

### 整体架构
[架构图或描述]

### 核心组件
| 组件 | 职责 | 技术选型 |
|------|------|----------|
| | | |

## 数据模型

[实体定义和关系]

## API 设计

| 方法 | 路径 | 描述 |
|------|------|------|
| | | |

## 错误处理

| 错误码 | 描述 | 处理方式 |
|--------|------|----------|
| | | |

## 安全考虑

- [ ] 输入验证
- [ ] 认证授权
- [ ] 数据加密

## 测试策略

- 单元测试:
- 集成测试:
- E2E 测试:

## 实施计划

| 阶段 | 内容 | 预计时间 |
|------|------|----------|
| Phase 1 | MVP | |
| Phase 2 | 完善 | |

## 风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| | | |

## 变更记录

| 日期 | 变更内容 | 作者 |
|------|----------|------|
| {date} | 初稿 | |
'''


def to_title(topic: str) -> str:
    """将 kebab-case 转换为标题格式"""
    return ' '.join(word.capitalize() for word in topic.split('-'))


def main():
    parser = argparse.ArgumentParser(description='初始化设计文档')
    parser.add_argument('topic', help='设计主题（kebab-case 格式）')
    parser.add_argument('--output-dir', '-o', default='docs/plans',
                        help='输出目录（默认: docs/plans）')

    args = parser.parse_args()

    # 准备路径
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    date = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date}-{args.topic}-design.md"
    filepath = output_dir / filename

    # 生成内容
    content = TEMPLATE.format(
        title=to_title(args.topic),
        date=date
    )

    # 写入文件
    filepath.write_text(content, encoding='utf-8')
    print(f"✅ 已创建设计文档: {filepath}")


if __name__ == '__main__':
    main()
