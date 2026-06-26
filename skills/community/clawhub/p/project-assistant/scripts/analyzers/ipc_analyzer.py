#!/usr/bin/env python3
"""
IPC（跨进程通信）分析器
分析项目中的跨进程通信接口

支持：
- Binder (Android/AIDL)
- DBus
- Socket (TCP/Unix Domain)
- Shared Memory
- Protobuf/gRPC
- SOME/IP (车载)
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field

# 添加日志支持
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


@dataclass
class IPCInterface:
    """IPC 接口"""
    name: str
    protocol: str                           # binder/dbus/socket/protobuf/someip
    file: str                               # 定义文件
    methods: List[str] = field(default_factory=list)
    clients: List[str] = field(default_factory=list)  # 调用方进程
    server: str = ""                        # 服务方进程
    description: str = ""


@dataclass
class ProcessInfo:
    """进程信息"""
    name: str
    entry_file: str                         # 入口文件
    subsystem: str = ""                     # 所属子系统
    provides: List[str] = field(default_factory=list)  # 提供的接口
    consumes: List[str] = field(default_factory=list)  # 使用的接口
    dependencies: List[str] = field(default_factory=list)  # 依赖的其他进程


class IPCAnalyzer:
    """IPC 分析器"""

    # AIDL 接口定义正则
    AIDL_INTERFACE_PATTERN = re.compile(
        r'interface\s+(\w+)\s*\{([^}]+)\}',
        re.MULTILINE
    )
    AIDL_METHOD_PATTERN = re.compile(
        r'(?:oneway\s+)?(\w+(?:<[^>]+>)?)\s+(\w+)\s*\(([^)]*)\)'
    )

    # DBus 接口定义正则 (XML)
    DBUS_INTERFACE_PATTERN = re.compile(
        r'<interface\s+name="([^"]+)"[^>]*>(.*?)</interface>',
        re.DOTALL
    )
    DBUS_METHOD_PATTERN = re.compile(
        r'<method\s+name="([^"]+)"'
    )

    # Protobuf service 定义正则
    PROTO_SERVICE_PATTERN = re.compile(
        r'service\s+(\w+)\s*\{([^}]+)\}',
        re.MULTILINE
    )
    PROTO_RPC_PATTERN = re.compile(
        r'rpc\s+(\w+)\s*\('
    )

    # SOME/IP 接口定义正则
    SOMEIP_INTERFACE_PATTERN = re.compile(
        r'(?:method|event|field)\s+(\w+)'
    )

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir).resolve()
        self.interfaces: Dict[str, IPCInterface] = {}
        self.processes: Dict[str, ProcessInfo] = {}
        self.communication_matrix: List[Dict[str, Any]] = []

    def analyze(self) -> Dict[str, Any]:
        """执行分析（优化版：单次遍历）"""
        logger.info(f"开始 IPC 分析: {self.project_dir}")

        # 单次遍历收集所有相关文件
        self._scan_all_files()

        self._build_communication_matrix()

        result = self._generate_report()
        logger.info(f"IPC 分析完成: {len(self.interfaces)} 接口, {len(self.processes)} 进程")
        return result

    def _scan_all_files(self) -> None:
        """单次遍历扫描所有相关文件（优化性能）"""
        # 文件扩展名到处理函数的映射
        extension_handlers = {
            '.aidl': self._handle_aidl_file,
            '.proto': self._handle_proto_file,
            '.xml': self._handle_xml_file,
            '.json': self._handle_json_file,
            '.cpp': self._handle_source_file,
            '.c': self._handle_source_file,
            '.java': self._handle_source_file,
            '.kt': self._handle_source_file,
            '.py': self._handle_source_file,
        }

        # 排除目录
        exclude_dirs = {
            '.git', '.svn', '.hg', '.idea', '.vscode',
            'node_modules', 'build', 'dist', 'out', 'bin', 'obj',
            '__pycache__', '.pytest_cache', '.mypy_cache',
            'target', 'vendor', 'CMakeFiles', '_deps',
            '.gradle', 'Pods', 'DerivedData',
        }

        # 单次遍历
        for root, dirs, files in os.walk(self.project_dir):
            # 排除特定目录
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for f in files:
                ext = Path(f).suffix.lower()
                handler = extension_handlers.get(ext)
                if handler:
                    file_path = Path(root) / f
                    try:
                        handler(file_path)
                    except Exception as e:
                        logger.debug(f"处理文件失败 {file_path}: {e}")

    def _handle_aidl_file(self, file_path: Path) -> None:
        """处理 AIDL 文件"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        self._parse_aidl(content, str(file_path.relative_to(self.project_dir)))

    def _handle_proto_file(self, file_path: Path) -> None:
        """处理 Protobuf 文件"""
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        self._parse_proto(content, str(file_path.relative_to(self.project_dir)))

    def _handle_xml_file(self, file_path: Path) -> None:
        """处理 XML 文件（DBus introspection）"""
        # 只处理 DBus introspection 文件
        if 'dbus' not in file_path.name.lower():
            return
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        self._parse_dbus(content, str(file_path.relative_to(self.project_dir)))

    def _handle_json_file(self, file_path: Path) -> None:
        """处理 JSON 文件（SOME/IP 配置）"""
        if 'someip' not in file_path.name.lower():
            return
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        try:
            data = json.loads(content)
            self._parse_someip_config(data, str(file_path.relative_to(self.project_dir)))
        except json.JSONDecodeError:
            pass

    def _handle_source_file(self, file_path: Path) -> None:
        """处理源代码文件（Socket 使用和进程检测）"""
        ext = file_path.suffix.lower()
        rel_path = str(file_path.relative_to(self.project_dir))

        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')

            # 检测 Socket 使用
            self._detect_socket_usage_in_file(content, rel_path, ext)

            # 检测进程（main 函数）
            self._detect_process_in_file(content, rel_path, ext)
        except Exception:
            pass

    def _detect_socket_usage_in_file(self, content: str, file_path: str, ext: str) -> None:
        """在文件中检测 Socket 使用"""
        socket_patterns = [
            (r'unix\s*socket.*?(\S+\.sock)', 'unix_socket'),
            (r'connect\s*\([^,]+,\s*"([^"]+)"', 'tcp_socket'),
            (r'bind\s*\([^,]+,\s*"([^"]+)"', 'tcp_socket'),
        ]

        for pattern, socket_type in socket_patterns:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                socket_path = match.group(1)
                interface_name = Path(socket_path).stem
                key = f"socket:{interface_name}"
                if key not in self.interfaces:
                    self.interfaces[key] = IPCInterface(
                        name=interface_name,
                        protocol=socket_type,
                        file=file_path,
                        methods=['connect', 'send', 'receive'],
                    )

    def _detect_process_in_file(self, content: str, file_path: str, ext: str) -> None:
        """在文件中检测进程入口"""
        main_patterns = {
            '.cpp': r'int\s+main\s*\(',
            '.c': r'int\s+main\s*\(',
            '.py': r'def\s+main\s*\(',
            '.java': r'public\s+static\s+void\s+main\s*\(',
            '.kt': r'fun\s+main\s*\(',
        }

        pattern = main_patterns.get(ext)
        if pattern and re.search(pattern, content):
            process_name = Path(file_path).parent.name
            if process_name not in self.processes:
                self.processes[process_name] = ProcessInfo(
                    name=process_name,
                    entry_file=file_path,
                    subsystem=self._infer_subsystem_from_path(file_path),
                )

    def _infer_subsystem_from_path(self, file_path: str) -> str:
        """从文件路径推断所属子系统"""
        parts = Path(file_path).parts
        if len(parts) > 1:
            return parts[0]
        return "main"

    def _parse_aidl(self, content: str, file_path: str) -> None:
        """解析 AIDL 内容"""
        for match in self.AIDL_INTERFACE_PATTERN.finditer(content):
            interface_name = match.group(1)
            methods_block = match.group(2)

            methods = []
            for method_match in self.AIDL_METHOD_PATTERN.finditer(methods_block):
                return_type = method_match.group(1)
                method_name = method_match.group(2)
                params = method_match.group(3)
                methods.append(f"{method_name}({params})")

            key = f"aidl:{interface_name}"
            self.interfaces[key] = IPCInterface(
                name=interface_name,
                protocol="binder",
                file=file_path,
                methods=methods,
            )

    def _parse_dbus(self, content: str, file_path: str) -> None:
        """解析 DBus XML 内容"""
        for match in self.DBUS_INTERFACE_PATTERN.finditer(content):
            interface_name = match.group(1)
            methods_block = match.group(2)

            methods = []
            for method_match in self.DBUS_METHOD_PATTERN.finditer(methods_block):
                methods.append(method_match.group(1))

            key = f"dbus:{interface_name}"
            self.interfaces[key] = IPCInterface(
                name=interface_name,
                protocol="dbus",
                file=file_path,
                methods=methods,
            )

    def _parse_proto(self, content: str, file_path: str) -> None:
        """解析 Protobuf 内容"""
        for match in self.PROTO_SERVICE_PATTERN.finditer(content):
            service_name = match.group(1)
            service_block = match.group(2)

            methods = []
            for rpc_match in self.PROTO_RPC_PATTERN.finditer(service_block):
                methods.append(rpc_match.group(1))

            key = f"grpc:{service_name}"
            self.interfaces[key] = IPCInterface(
                name=service_name,
                protocol="grpc",
                file=file_path,
                methods=methods,
            )

    def _parse_someip_config(self, data: Dict, file_path: str) -> None:
        """解析 SOME/IP 配置"""
        services = data.get('services', [])
        for service in services:
            name = service.get('name', 'unknown')
            methods = []
            for method in service.get('methods', []):
                methods.append(method.get('name', ''))
            for event in service.get('events', []):
                methods.append(f"event:{event.get('name', '')}")

            key = f"someip:{name}"
            self.interfaces[key] = IPCInterface(
                name=name,
                protocol="someip",
                file=file_path,
                methods=methods,
            )

    def _build_communication_matrix(self) -> None:
        """构建通信矩阵"""
        # 分析接口调用关系
        for key, interface in self.interfaces.items():
            # 在源码中查找接口使用
            for ext in ['.cpp', '.c', '.java', '.kt', '.py']:
                for source_file in self.project_dir.rglob(f'*{ext}'):
                    try:
                        content = source_file.read_text(encoding='utf-8', errors='ignore')
                        if interface.name in content:
                            process_name = source_file.parent.name
                            if process_name in self.processes:
                                if interface.server and interface.server != process_name:
                                    interface.clients.append(process_name)
                                    self.processes[process_name].consumes.append(key)
                    except Exception:
                        pass

        # 构建矩阵
        for key, interface in self.interfaces.items():
            for client in interface.clients:
                self.communication_matrix.append({
                    'source': client,
                    'target': interface.server or 'unknown',
                    'protocol': interface.protocol,
                    'interface': interface.name,
                    'file': interface.file,
                })

    def _generate_report(self) -> Dict[str, Any]:
        """生成分析报告"""
        return {
            'summary': {
                'total_interfaces': len(self.interfaces),
                'total_processes': len(self.processes),
                'protocols': list(set(i.protocol for i in self.interfaces.values())),
            },
            'interfaces': [
                {
                    'name': iface.name,
                    'protocol': iface.protocol,
                    'file': iface.file,
                    'methods': iface.methods[:10],  # 限制输出
                    'clients': iface.clients,
                    'server': iface.server,
                }
                for iface in self.interfaces.values()
            ],
            'processes': [
                {
                    'name': proc.name,
                    'entry': proc.entry_file,
                    'subsystem': proc.subsystem,
                    'provides': proc.provides,
                    'consumes': proc.consumes,
                }
                for proc in self.processes.values()
            ],
            'communication_matrix': self.communication_matrix,
        }

    def generate_ipc_document(self) -> str:
        """生成 IPC 文档 (Markdown)"""
        lines = [
            "# IPC 通信概览",
            "",
            f"> 自动生成 | 接口数: {len(self.interfaces)} | 进程数: {len(self.processes)}",
            "",
            "## 通信矩阵",
            "",
            "| 源进程 | 目标进程 | 协议 | 接口 |",
            "|--------|----------|------|------|",
        ]

        for comm in self.communication_matrix:
            lines.append(
                f"| {comm['source']} | {comm['target']} | {comm['protocol']} | {comm['interface']} |"
            )

        lines.extend([
            "",
            "## 接口详情",
            "",
        ])

        for key, iface in self.interfaces.items():
            lines.extend([
                f"### {iface.name}",
                "",
                f"- **协议**: {iface.protocol}",
                f"- **定义文件**: `{iface.file}`",
                f"- **方法数**: {len(iface.methods)}",
                "",
                "**方法列表**:",
                "",
            ])
            for method in iface.methods[:10]:
                lines.append(f"- `{method}`")
            if len(iface.methods) > 10:
                lines.append(f"- ... (共 {len(iface.methods)} 个)")
            lines.append("")

        return "\n".join(lines)


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: ipc_analyzer.py <project_dir> [--doc]")
        print("\nOptions:")
        print("  --doc    Generate markdown document")
        sys.exit(1)

    project_dir = sys.argv[1]
    generate_doc = '--doc' in sys.argv

    analyzer = IPCAnalyzer(project_dir)
    result = analyzer.analyze()

    if generate_doc:
        print(analyzer.generate_ipc_document())
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()