#!/usr/bin/env python3
"""
文档生成器
支持分层文档生成，优化 Token 消耗

层级：
- L0: 项目概览 (project.md) ~1-2KB
- L1: 子系统摘要 (subsystems/{name}/index.md) ~2KB each
- L2: 详细文档 (按需生成)
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional


class DocGenerator:
    """分层文档生成器"""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.claude_dir = self.project_dir / '.claude'
        self.docs_dir = self.claude_dir / 'docs'
        self.index_dir = self.claude_dir / 'index'

    def ensure_dirs(self) -> None:
        """确保目录存在"""
        self.claude_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(parents=True, exist_ok=True)
        (self.docs_dir / 'subsystems').mkdir(parents=True, exist_ok=True)
        (self.docs_dir / 'ipc').mkdir(parents=True, exist_ok=True)

    # ========== L0: 项目概览 ==========

    def generate_l0_project_md(self, project_info: Dict[str, Any]) -> str:
        """生成 L0 项目概览文档

        只包含摘要和索引，控制在 1-2KB
        """
        self.ensure_dirs()

        lines = [
            f"# {project_info.get('name', '项目名称')}",
            "",
            f"> 类型: {project_info.get('type', 'unknown')} | "
            f"进程: {len(project_info.get('processes', []))} | "
            f"接口: {len(project_info.get('interfaces', []))}",
            "",
            "## 子系统",
            "",
        ]

        subsystems = project_info.get('subsystems', [])
        if subsystems:
            lines.append("| 子系统 | 进程数 | 说明 |")
            lines.append("|--------|--------|------|")
            for sub in subsystems:
                name = sub.get('name', 'unknown')
                proc_count = sub.get('process_count', 0)
                desc = sub.get('description', '')[:20]
                lines.append(f"| {name} | {proc_count} | {desc} |")
        else:
            lines.append("*暂无子系统信息*")

        lines.extend([
            "",
            "## 快速命令",
            "",
            "```bash",
            "# 构建",
            f"{project_info.get('build_cmd', 'make')}",
            "",
            "# 运行",
            f"{project_info.get('run_cmd', 'make run')}",
            "```",
            "",
            "## 数据索引",
            "",
            "| 数据 | 文件 |",
            "|------|------|",
            "| 进程列表 | [index/processes.json](index/processes.json) |",
            "| IPC 接口 | [index/ipc.json](index/ipc.json) |",
            "| 目录结构 | [index/structure.json](index/structure.json) |",
            "",
            "## 详细文档",
            "",
            "详细文档按需生成，参见 `docs/` 目录",
            "",
            "---",
            f"*生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        ])

        content = "\n".join(lines)

        # 写入文件
        project_md_path = self.claude_dir / 'project.md'
        project_md_path.write_text(content, encoding='utf-8')

        return content

    # ========== 索引文件 ==========

    def generate_processes_index(self, processes: List[Dict[str, Any]]) -> str:
        """生成进程索引"""
        self.ensure_dirs()

        # 精简数据，只保留必要字段
        index_data = []
        for proc in processes:
            index_data.append({
                'name': proc.get('name', ''),
                'entry': proc.get('entry_file', ''),
                'subsystem': proc.get('subsystem', ''),
                'provides': proc.get('provides', [])[:5],  # 最多5个
                'consumes': proc.get('consumes', [])[:5],
            })

        path = self.index_dir / 'processes.json'
        path.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding='utf-8')
        return str(path)

    def generate_ipc_index(self, interfaces: List[Dict[str, Any]]) -> str:
        """生成 IPC 索引"""
        self.ensure_dirs()

        index_data = []
        for iface in interfaces:
            index_data.append({
                'name': iface.get('name', ''),
                'protocol': iface.get('protocol', ''),
                'file': iface.get('file', ''),
                'methods': len(iface.get('methods', [])),
                'clients': iface.get('clients', [])[:3],
                'server': iface.get('server', ''),
            })

        path = self.index_dir / 'ipc.json'
        path.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding='utf-8')
        return str(path)

    def generate_structure_index(self, structure: Dict[str, Any]) -> str:
        """生成目录结构索引"""
        self.ensure_dirs()

        # 压缩存储
        compressed = {
            'top_dirs': structure.get('top_dirs', []),
            'key_files': structure.get('key_files', [])[:20],
            'exclude': ['node_modules', 'build', '.git', '__pycache__'],
        }

        path = self.index_dir / 'structure.json'
        path.write_text(json.dumps(compressed, indent=2, ensure_ascii=False), encoding='utf-8')
        return str(path)

    def generate_subsystems_index(self, subsystems: List[Dict[str, Any]]) -> str:
        """生成子系统索引"""
        self.ensure_dirs()

        index_data = []
        for sub in subsystems:
            index_data.append({
                'name': sub.get('name', ''),
                'path': sub.get('path', ''),
                'process_count': sub.get('process_count', 0),
                'has_doc': sub.get('has_doc', False),
            })

        path = self.index_dir / 'subsystems.json'
        path.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding='utf-8')
        return str(path)

    # ========== L1: 子系统摘要 ==========

    def generate_l1_subsystem_md(self, subsystem_name: str,
                                  subsystem_info: Dict[str, Any]) -> str:
        """生成 L1 子系统摘要文档"""
        self.ensure_dirs()

        sub_dir = self.docs_dir / 'subsystems' / subsystem_name
        sub_dir.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# {subsystem_name} 子系统",
            "",
            f"> 进程数: {len(subsystem_info.get('processes', []))} | "
            f"接口数: {len(subsystem_info.get('interfaces', []))}",
            "",
            "## 架构",
            "",
        ]

        # 简化架构描述
        arch = subsystem_info.get('architecture', '')
        if arch:
            lines.append(arch[:500])  # 限制长度
        else:
            lines.append("*架构信息待生成*")

        lines.extend([
            "",
            "## 进程列表",
            "",
            "| 进程名 | 入口文件 |",
            "|--------|----------|",
        ])

        for proc in subsystem_info.get('processes', [])[:10]:
            lines.append(f"| {proc.get('name', '')} | `{proc.get('entry', '')}` |")

        lines.extend([
            "",
            "## 接口",
            "",
        ])

        for iface in subsystem_info.get('interfaces', [])[:5]:
            lines.append(f"- **{iface.get('name', '')}** ({iface.get('protocol', '')})")

        lines.extend([
            "",
            "---",
            f"*详细文档按需生成*",
        ])

        content = "\n".join(lines)
        path = sub_dir / 'index.md'
        path.write_text(content, encoding='utf-8')

        return content

    # ========== L2: 详细文档（按需生成） ==========

    def generate_l2_process_md(self, subsystem_name: str,
                                process_name: str,
                                process_info: Dict[str, Any]) -> str:
        """生成 L2 进程详细文档（按需调用）"""
        self.ensure_dirs()

        sub_dir = self.docs_dir / 'subsystems' / subsystem_name
        sub_dir.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# {process_name}",
            "",
            f"> 入口: `{process_info.get('entry_file', '')}`",
            "",
            "## 功能",
            "",
            process_info.get('description', '*功能描述待补充*'),
            "",
            "## 主要流程",
            "",
        ]

        # 主流程
        main_flow = process_info.get('main_flow', [])
        if main_flow:
            for step in main_flow:
                lines.append(f"1. {step}")
        else:
            lines.append("*流程信息待分析*")

        lines.extend([
            "",
            "## 提供的接口",
            "",
        ])

        for iface in process_info.get('provides', []):
            lines.append(f"- {iface}")

        lines.extend([
            "",
            "## 依赖的接口",
            "",
        ])

        for iface in process_info.get('consumes', []):
            lines.append(f"- {iface}")

        lines.extend([
            "",
            "## 关键代码",
            "",
        ])

        key_code = process_info.get('key_code', [])
        for code in key_code[:5]:
            lines.append(f"- `{code.get('file', '')}:{code.get('line', '')}` - {code.get('desc', '')}")

        content = "\n".join(lines)
        path = sub_dir / f'{process_name}.md'
        path.write_text(content, encoding='utf-8')

        return content

    def generate_l2_ipc_md(self, interfaces: List[Dict[str, Any]],
                           protocol: str = None) -> str:
        """生成 L2 IPC 详细文档"""
        self.ensure_dirs()

        ipc_dir = self.docs_dir / 'ipc'
        ipc_dir.mkdir(parents=True, exist_ok=True)

        lines = [
            "# IPC 通信概览",
            "",
            f"> 接口总数: {len(interfaces)}",
            "",
            "## 通信矩阵",
            "",
            "| 源进程 | 目标进程 | 协议 | 接口 |",
            "|--------|----------|------|------|",
        ]

        # 从接口提取通信关系
        for iface in interfaces:
            for client in iface.get('clients', []):
                lines.append(
                    f"| {client} | {iface.get('server', 'unknown')} | "
                    f"{iface.get('protocol', '')} | {iface.get('name', '')} |"
                )

        lines.extend([
            "",
            "## 接口详情",
            "",
        ])

        for iface in interfaces[:20]:  # 限制数量
            lines.extend([
                f"### {iface.get('name', '')}",
                "",
                f"- **协议**: {iface.get('protocol', '')}",
                f"- **定义文件**: `{iface.get('file', '')}`",
                f"- **方法数**: {len(iface.get('methods', []))}",
                "",
                "**方法列表**:",
                "",
            ])
            for method in iface.get('methods', [])[:10]:
                lines.append(f"- `{method}`")
            lines.append("")

        content = "\n".join(lines)
        path = ipc_dir / 'overview.md'
        path.write_text(content, encoding='utf-8')

        return content

    # ========== 检查文档是否存在 ==========

    def has_l1_subsystem_doc(self, subsystem_name: str) -> bool:
        """检查 L1 子系统文档是否存在"""
        path = self.docs_dir / 'subsystems' / subsystem_name / 'index.md'
        return path.exists()

    def has_l2_process_doc(self, subsystem_name: str, process_name: str) -> bool:
        """检查 L2 进程文档是否存在"""
        path = self.docs_dir / 'subsystems' / subsystem_name / f'{process_name}.md'
        return path.exists()

    def has_l2_ipc_doc(self) -> bool:
        """检查 L2 IPC 文档是否存在"""
        path = self.docs_dir / 'ipc' / 'overview.md'
        return path.exists()

    # ========== 读取文档 ==========

    def read_project_md(self) -> Optional[str]:
        """读取项目概览"""
        path = self.claude_dir / 'project.md'
        if path.exists():
            return path.read_text(encoding='utf-8')
        return None

    def read_index(self, name: str) -> Optional[Dict]:
        """读取索引数据"""
        path = self.index_dir / f'{name}.json'
        if path.exists():
            return json.loads(path.read_text(encoding='utf-8'))
        return None

    def read_l1_subsystem(self, subsystem_name: str) -> Optional[str]:
        """读取 L1 子系统文档"""
        path = self.docs_dir / 'subsystems' / subsystem_name / 'index.md'
        if path.exists():
            return path.read_text(encoding='utf-8')
        return None

    def read_l2_process(self, subsystem_name: str, process_name: str) -> Optional[str]:
        """读取 L2 进程文档"""
        path = self.docs_dir / 'subsystems' / subsystem_name / f'{process_name}.md'
        if path.exists():
            return path.read_text(encoding='utf-8')
        return None

    # ========== 获取文档结构 ==========

    def get_doc_structure(self) -> Dict[str, Any]:
        """获取当前文档结构"""
        result = {
            'has_project_md': (self.claude_dir / 'project.md').exists(),
            'indexes': [],
            'l1_docs': [],
            'l2_docs': [],
        }

        # 索引文件
        for f in self.index_dir.glob('*.json'):
            result['indexes'].append(f.stem)

        # L1 文档
        sub_dir = self.docs_dir / 'subsystems'
        if sub_dir.exists():
            for d in sub_dir.iterdir():
                if d.is_dir() and (d / 'index.md').exists():
                    result['l1_docs'].append(d.name)

        # L2 文档
        if sub_dir.exists():
            for d in sub_dir.iterdir():
                if d.is_dir():
                    for md in d.glob('*.md'):
                        if md.name != 'index.md':
                            result['l2_docs'].append(f"{d.name}/{md.stem}")

        # IPC 文档
        if (self.docs_dir / 'ipc' / 'overview.md').exists():
            result['l2_docs'].append('ipc/overview')

        return result


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: doc_generator.py <command> <project_dir> [args]")
        print("\nCommands:")
        print("  structure <project_dir>          Show doc structure")
        print("  l0 <project_dir>                 Generate L0 project.md")
        print("  l1 <project_dir> <subsystem>     Generate L1 subsystem doc")
        print("  l2-process <project_dir> <sub> <process>  Generate L2 process doc")
        print("  l2-ipc <project_dir>             Generate L2 IPC doc")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'structure':
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
        gen = DocGenerator(project_dir)
        structure = gen.get_doc_structure()
        print(json.dumps(structure, indent=2, ensure_ascii=False))

    elif command == 'l0':
        project_dir = sys.argv[2] if len(sys.argv) > 2 else os.getcwd()
        gen = DocGenerator(project_dir)
        # 示例数据
        project_info = {
            'name': Path(project_dir).name,
            'type': 'embedded-linux',
            'processes': [],
            'interfaces': [],
            'subsystems': [],
            'build_cmd': 'make all',
        }
        content = gen.generate_l0_project_md(project_info)
        print(f"Generated: {gen.claude_dir / 'project.md'}")
        print(f"Size: {len(content)} bytes")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()