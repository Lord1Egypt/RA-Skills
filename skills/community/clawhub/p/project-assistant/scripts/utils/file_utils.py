#!/usr/bin/env python3
"""
工具函数模块
通用文件操作和输出工具

优化版本：支持分层文档生成，减少 Token 消耗
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

# 导入统一常量
try:
    from constants import EXCLUDE_DIRS
except ImportError:
    EXCLUDE_DIRS = {
        '.git', '.svn', '.hg', '.idea', '.vscode',
        'node_modules', '__pycache__', 'build', 'dist', 'out',
        'target', 'vendor', 'CMakeFiles', '_deps',
        '.gradle', 'Pods', 'DerivedData',
        'venv', '.venv', 'env', '.env',
        'Output', 'Listings', 'Objects', 'DebugConfig', 'RTE',
    }


def get_directory_tree(target_dir: str, max_depth: int = 3, exclude_dirs: set = None,
                       max_items: int = 50) -> str:
    """生成目录树（限制输出大小）"""
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS

    lines = []
    item_count = 0

    def walk_dir(path: str, prefix: str = '', depth: int = 0):
        nonlocal item_count
        if depth > max_depth or item_count >= max_items:
            if item_count >= max_items:
                lines.append(f"{prefix}... (已省略)")
            return

        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            return

        dirs = []
        files = []

        for item in items:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                if item not in exclude_dirs:
                    dirs.append(item)
            else:
                files.append(item)

        # 只显示前10个文件
        files = files[:10]

        for i, d in enumerate(dirs):
            if item_count >= max_items:
                lines.append(f"{prefix}... (已省略)")
                return
            item_count += 1
            is_last = (i == len(dirs) - 1) and not files
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{d}/")
            new_prefix = prefix + ('    ' if is_last else '│   ')
            walk_dir(os.path.join(path, d), new_prefix, depth + 1)

        for i, f in enumerate(files):
            if item_count >= max_items:
                lines.append(f"{prefix}... (已省略)")
                return
            item_count += 1
            is_last = i == len(files) - 1
            lines.append(f"{prefix}{'└── ' if is_last else '├── '}{f}")

    walk_dir(target_dir)
    return '\n'.join(lines)


def count_files_by_extension(target_dir: str, extensions: List[str]) -> Dict[str, int]:
    """按扩展名统计文件数量"""
    counts = {ext: 0 for ext in extensions}

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', 'build', 'dist'}]
        for f in files:
            for ext in extensions:
                if f.endswith(ext):
                    counts[ext] += 1

    return counts


def format_size(size_bytes: int) -> str:
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}TB"


def generate_project_md_l0(data: Dict[str, Any]) -> str:
    """生成 L0 项目概览文档（精简版，~1-2KB）

    只包含摘要和索引，优化 Token 消耗
    """
    date = datetime.now().strftime('%Y-%m-%d')
    project_type = data.get('type', 'unknown')
    name = data.get('name', 'unknown')
    subsystems = data.get('subsystems', [])
    processes = data.get('processes', [])
    interfaces = data.get('interfaces', [])

    doc = f"""# {name}

> 类型: {project_type} | 进程: {len(processes)} | 接口: {len(interfaces)}

## 子系统

"""

    if subsystems:
        doc += "| 子系统 | 进程数 | 说明 |\n|--------|--------|------|\n"
        for sub in subsystems[:10]:
            sub_name = sub.get('name', '') if isinstance(sub, dict) else sub
            proc_count = sub.get('process_count', 0) if isinstance(sub, dict) else 0
            desc = sub.get('description', '')[:20] if isinstance(sub, dict) else ''
            doc += f"| {sub_name} | {proc_count} | {desc} |\n"
    else:
        doc += "*暂无子系统信息*\n"

    doc += f"""
## 快速命令

```bash
# 构建
{data.get('build_cmd', 'make')}

# 运行
{data.get('run_cmd', 'make run')}
```

## 数据索引

| 数据 | 文件 |
|------|------|
| 进程列表 | index/processes.json |
| IPC 接口 | index/ipc.json |
| 目录结构 | index/structure.json |

## 详细文档

详细文档按需生成，参见 `docs/` 目录

---
*生成于 {date}*
"""
    return doc


def generate_project_md(data: Dict[str, Any], template_path: str = None,
                        compact: bool = True) -> str:
    """生成项目文档

    Args:
        data: 项目数据
        template_path: 模板路径（保留兼容性）
        compact: 是否使用精简模式（默认 True）
    """
    if compact:
        return generate_project_md_l0(data)

    # 完整模式（向后兼容）
    return _generate_full_project_md(data)


def _generate_full_project_md(data: Dict[str, Any]) -> str:
    """生成完整项目文档（向后兼容）"""
    date = datetime.now().strftime('%Y-%m-%d')
    project_type = data.get('type', 'unknown')

    # 基本信息
    doc = f"""# 项目概览

> 自动生成于 {date} | 项目类型: {project_type}

## 基本信息

| 项目属性 | 值 |
|---------|-----|
| 项目名称 | {data.get('name', 'unknown')} |
| 项目类型 | {project_type} |
| 主要语言 | {data.get('language', 'unknown')} |
| 框架/平台 | {data.get('framework', 'unknown')} |
| 构建系统 | {data.get('build_system', 'unknown')} |
| 目标平台 | {data.get('target_platform', 'unknown')} |

## 目录结构

```
{data.get('directory_tree', '[目录树生成失败]')}
```

## 入口点

"""
    entry_points = data.get('entry_points', [])
    if entry_points:
        doc += f"- **主入口**: `{entry_points[0]}`\n"
        for entry in entry_points[1:5]:
            doc += f"- `{entry}`\n"
    else:
        doc += "- [待识别]\n"

    # 构建指南
    doc += f"""
## 构建指南

```bash
{data.get('build_cmd', '# [待补充]')}
```
"""

    return doc


def write_project_md(target_dir: str, content: str) -> str:
    """写入项目文档"""
    output_dir = os.path.join(target_dir, '.claude')
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, 'project.md')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def read_project_md(target_dir: str) -> Optional[str]:
    """读取项目文档"""
    output_path = os.path.join(target_dir, '.claude', 'project.md')
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None


if __name__ == '__main__':
    # 测试
    import sys
    if len(sys.argv) > 1:
        tree = get_directory_tree(sys.argv[1])
        print(tree)