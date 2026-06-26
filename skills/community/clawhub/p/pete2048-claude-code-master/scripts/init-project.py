#!/usr/bin/env python3
"""
Claude Code 项目初始化脚本
快速创建 Context Engineering 所需的标准目录结构
"""

import os
import argparse
from pathlib import Path


def create_project_structure(project_path: str):
    """创建标准项目结构"""
    base = Path(project_path)

    # 定义目录结构
    directories = [
        ".claude/commands",
        ".claude/agents",
        ".claude/output-styles",
        ".ai-rules",
        "specs",
        "PRPs/templates",
        "examples",
    ]

    # 创建目录
    for dir_path in directories:
        full_path = base / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录: {dir_path}")

    # 创建 CLAUDE.md
    claude_md = base / "CLAUDE.md"
    if not claude_md.exists():
        claude_md.write_text("""# 项目 AI 协作规则

## 项目感知
- 能理解规划文档、任务清单
- 自动读取 specs/ 目录下的规范文件

## 代码结构约束
- 文件大小：单文件 < 300 行
- 模块拆分：按功能域组织
- 命名规范：使用一致的命名模式

## 测试要求
- 单元测试：所有新功能必须有测试
- 覆盖率：最低 80%
- 测试框架：使用项目标准测试框架

## 编码风格
- 语言偏好：[修改为你的语言]
- 格式规范：使用 linter 自动格式化
- 注释要求：复杂逻辑必须注释

## 文档规范
- API 文档：所有公开接口必须文档化
- README：保持更新
- 变更日志：记录重要变更
""")
        print("✓ 创建文件: CLAUDE.md")

    # 创建 INITIAL.md
    initial_md = base / "INITIAL.md"
    if not initial_md.exists():
        initial_md.write_text("""# 功能需求

## 功能：
[具体描述你想实现什么功能，清晰明确地写出需求]

## 示例：
[列出 examples/ 文件夹中参考的代码，并说明它们的用途]

## 文档链接：
[加入相关文档、API 说明或 MCP 服务器资源链接]

## 其他注意事项：
[说明任何易错点、特别需求，或 AI 可能忽略的内容]
""")
        print("✓ 创建文件: INITIAL.md")

    # 创建 .ai-rules 文件
    create_ai_rules(base)

    # 创建 PRP 模板
    create_prp_template(base)

    print("\n✅ 项目初始化完成！")
    print(f"项目路径: {base.absolute()}")
    print("\n下一步：")
    print("1. 编辑 CLAUDE.md 配置项目规则")
    print("2. 编辑 .ai-rules/ 下的文件")
    print("3. 在 examples/ 中添加代码示例")
    print("4. 编辑 INITIAL.md 描述你的功能需求")


def create_ai_rules(base: Path):
    """创建 .ai-rules 目录下的文件"""
    ai_rules = base / ".ai-rules"

    # product.md
    product_md = ai_rules / "product.md"
    if not product_md.exists():
        product_md.write_text("""---
title: Product Vision
description: "Defines the project's core purpose, target users, and main features."
inclusion: always
---

# Product Vision

## 产品名称
[产品名称]

## 核心价值主张
[一句话描述产品解决的核心问题]

## 目标用户
- 主要用户：[描述]
- 次要用户：[描述]

## 主要功能
1. [功能 1]
2. [功能 2]
3. [功能 3]

## 成功指标
- [指标 1]
- [指标 2]
""")
        print("✓ 创建文件: .ai-rules/product.md")

    # tech.md
    tech_md = ai_rules / "tech.md"
    if not tech_md.exists():
        tech_md.write_text("""---
title: Technology Stack
description: "Technology choices, frameworks, and tools used in the project."
inclusion: always
---

# Technology Stack

## 核心技术
- **语言**: [你的语言]
- **框架**: [你的框架]
- **数据库**: [你的数据库]
- **缓存**: [缓存方案]

## 开发工具
- **包管理器**: [包管理器]
- **测试框架**: [测试框架]
- **Linter**: [Linter 工具]
- **Formatter**: [格式化工具]

## 部署
- **容器化**: Docker
- **编排**: Kubernetes (可选)
- **CI/CD**: [CI/CD 工具]

## 常用命令
```bash
# 开发
[开发命令]

# 测试
[测试命令]

# 构建
[构建命令]

# Lint
[Lint 命令]
```
""")
        print("✓ 创建文件: .ai-rules/tech.md")

    # structure.md
    structure_md = ai_rules / "structure.md"
    if not structure_md.exists():
        structure_md.write_text("""---
title: Project Structure
description: "File organization and naming conventions."
inclusion: always
---

# Project Structure & Conventions

## 目录组织

[根据你的项目结构描述]

## 命名规范

### 文件命名
- 组件: PascalCase.tsx
- 工具: camelCase.ts
- 类型: types.ts
- 测试: *.test.ts

## 代码组织原则
- 单一职责原则
- 每个文件 < 300 行
- 相关文件就近放置
- 共享代码提升到 lib/
""")
        print("✓ 创建文件: .ai-rules/structure.md")


def create_prp_template(base: Path):
    """创建 PRP 模板"""
    prp_template = base / "PRPs" / "templates" / "prp_base.md"
    if not prp_template.exists():
        prp_template.write_text("""# PRP: {功能名称}

## 概览
- **功能名称**: {name}
- **优先级**: P0/P1/P2
- **预计时间**: {duration}
- **置信度**: {1-10}

## 上下文信息

### 技术栈
[从 tech.md 提取的相关技术栈]

### 相关代码模式
[从 examples/ 提取的相关代码示例]

### 文档资源
[从 INITIAL.md 提取的文档链接]

## 实现步骤

### Task 1: {task name}
**目标**: {description}
**文件**: {files to create/modify}
**验证**: {how to verify}

**实现细节**:
```python
# 伪代码或关键实现
```

**测试**:
```python
def test_{task_name}():
    # 测试代码
```

### Task 2: {task name}
[同上结构]

## 错误处理
- 预期错误: {error}
- 处理方式: {handling}

## 验收标准
- [ ] 标准 1
- [ ] 标准 2
- [ ] 标准 3

## 风险和注意事项
- 风险 1: {description}
- 缓解措施: {mitigation}
""")
        print("✓ 创建文件: PRPs/templates/prp_base.md")


def main():
    parser = argparse.ArgumentParser(description="初始化 Claude Code 项目结构")
    parser.add_argument("path", nargs="?", default=".", help="项目路径（默认为当前目录）")
    args = parser.parse_args()

    project_path = os.path.abspath(args.path)
    create_project_structure(project_path)


if __name__ == "__main__":
    main()
