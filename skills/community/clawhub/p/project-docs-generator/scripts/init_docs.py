#!/usr/bin/env python3
"""
初始化文档目录结构
"""

import os
import argparse
from pathlib import Path
from datetime import datetime


def create_docs_structure(output_dir: str, project_name: str = "Project"):
    """创建标准文档目录结构"""

    docs_path = Path(output_dir) / "docs"

    # 定义目录结构
    structure = {
        "01-quick-start": [
            "01-project-overview.md",
            "02-tech-stack-summary.md",
            "03-development-setup.md",
        ],
        "02-architecture": [
            "01-system-architecture.md",
            "02-module-dependencies.md",
            "03-data-flow.md",
        ],
        "03-backend": ["00-README.md"],
        "04-frontend": ["00-README.md"],
        "05-tech-decisions": ["00-README.md"],
        "06-core-flows": ["README.md"],
    }

    # 创建目录
    for dir_name, files in structure.items():
        dir_path = docs_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)

        for file_name in files:
            file_path = dir_path / file_name
            if not file_path.exists():
                create_template_file(file_path, file_name, project_name)

    # 创建主 README
    create_main_readme(docs_path, project_name)

    print(f"✅ 文档结构已创建: {docs_path}")
    return docs_path


def create_template_file(file_path: Path, file_name: str, project_name: str):
    """创建模板文件"""

    templates = {
        "01-project-overview.md": f"""# 项目概览

> {project_name} - [一句话介绍]

---

## 是什么？

[项目介绍]

## 核心功能

| 功能 | 说明 |
|------|------|
| 功能1 | ... |
| 功能2 | ... |

## 系统截图

[添加截图]

## 快速演示

```bash
# 1. 克隆项目
git clone [repository]

# 2. 启动项目
[启动命令]

# 3. 访问
http://localhost:3000
```
""",
        "00-README.md": f"""# 模块说明

> [模块名称] - [模块职责]

---

## 模块清单

| 组件 | 职责 | 关键特性 |
|------|------|----------|
| ... | ... | ... |

## 相关文档

- [文档1](./path/to/doc.md)
""",
        "README.md": f"""# 核心流程

> [流程概述]

---

## 流程索引

| 流程 | 说明 | 文档 |
|------|------|------|
| 流程1 | ... | [查看](./01-xxx.md) |
""",
    }

    content = templates.get(
        file_name,
        f"# {file_name.replace('.md', '').replace('-', ' ').title()}\n\n> TODO: 添加内容\n",
    )

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def create_main_readme(docs_path: Path, project_name: str):
    """创建主 README"""
    content = f"""# {project_name} 文档中心

> [一句话项目介绍]

---

## 文档导航

### 第一阶段：快速开始

| 文档 | 说明 |
|------|------|
| [01-项目概览](./01-quick-start/01-project-overview.md) | {project_name} 是什么、核心功能、系统组件 |
| [02-技术栈总览](./01-quick-start/02-tech-stack-summary.md) | 前后端技术栈清单、版本信息 |
| [03-开发环境搭建](./01-quick-start/03-development-setup.md) | 环境要求、依赖安装、快速启动 |

### 第二阶段：架构设计

| 文档 | 说明 |
|------|------|
| [01-系统架构](./02-architecture/01-system-architecture.md) | 系统整体架构、分层设计、组件关系 |
| [02-模块依赖](./02-architecture/02-module-dependencies.md) | 后端模块依赖、前端模块关系 |
| [03-数据流程](./02-architecture/03-data-flow.md) | 核心数据流转路径、异步处理 |

### 第三阶段：后端深入

| 模块 | 说明 |
|------|------|
| [00-后端导航](./03-backend/00-README.md) | 后端模块总览 |

### 第四阶段：前端深入

| 模块 | 说明 |
|------|------|
| [00-前端导航](./04-frontend/00-README.md) | 前端模块总览 |

### 第五阶段：技术选型决策

| 文档 | 说明 |
|------|------|
| [00-选型导航](./05-tech-decisions/00-README.md) | 技术选型总览 |

### 第六阶段：核心业务流程

| 文档 | 说明 |
|------|------|
| [流程索引](./06-core-flows/README.md) | 核心业务流程列表 |

---

## 阅读建议

### 新手入门路径
```
01-quick-start/01-project-overview.md
    ↓
01-quick-start/02-tech-stack-summary.md
    ↓
01-quick-start/03-development-setup.md
    ↓
02-architecture/01-system-architecture.md
```

---

## 文档约定

### 图表渲染
本文档使用 PlantUML 绘制架构图，推荐使用以下方式渲染：
- VS Code 插件：PlantUML
- 在线工具：[PlantText](https://www.planttext.com/)

### 代码示例
文档中的代码示例以伪代码为主，展示核心逻辑。

---

*最后更新: {datetime.now().strftime("%Y-%m-%d")}*
"""

    readme_path = docs_path / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(description="初始化文档目录结构")
    parser.add_argument("output_dir", help="输出目录")
    parser.add_argument("--name", default="Project", help="项目名称")

    args = parser.parse_args()
    create_docs_structure(args.output_dir, args.name)


if __name__ == "__main__":
    main()
