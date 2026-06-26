"""
恶意代码扫描器 - 检测技能代码中的安全威胁
支持 Python 代码的静态分析

检测范围：
- 危险函数调用（eval, exec, os.system, subprocess）
- 敏感信息泄露（硬编码密钥、密码）
- 可疑网络请求（硬编码 IP、域名）
- 文件系统攻击（删除系统文件、路径遍历）
- 无限循环/递归
- 反调试技术
"""

import ast
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, asdict
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_logger import audit_logger


@dataclass
class ScanResult:
    """扫描结果数据类"""
    file_path: str
    skill_id: str
    threat_level: str  # 'critical', 'high', 'medium', 'low', 'safe'
    issues: List[Dict[str, Any]]
    scanned_lines: int
    scanned_time: float

    def to_dict(self):
        return asdict(self)


class PythonCodeScanner:
    """Python 代码恶意模式扫描器"""

    # 危险函数和模块（威胁等级：critical）
    DANGEROUS_FUNCTIONS = {
        'eval': 'critical',
        'exec': 'critical',
        'compile': 'high',
        '__import__': 'high',
        'open': 'medium',  # 需要上下文判断
        'os.system': 'critical',
        'os.popen': 'critical',
        'os.spawn': 'critical',
        'os.exec': 'critical',
        'subprocess.run': 'critical',
        'subprocess.call': 'critical',
        'subprocess.Popen': 'critical',
        'subprocess.check_output': 'high',
        'subprocess.check_call': 'high'
    }

    # 危险模块导入
    DANGEROUS_MODULES = {
        'subprocess': 'high',
        'pty': 'critical',
        'os': 'medium',  # 需要检查具体用法
        'sys': 'low',
        'socket': 'medium',
        'urllib': 'medium',
        'requests': 'low',
        'ftplib': 'medium',
        'paramiko': 'medium',
        'telnetlib': 'medium'
    }

    # 敏感信息正则（硬编码密钥、密码等）
    SENSITIVE_PATTERNS = [
        (r'(api[_-]?key|apikey|secret|password|token)\s*[=:]\s*[\'"][^\'"]{8,}[\'"]', 'high', '硬编码敏感信息'),
        (r'(sk_live_|sk_test_|Bearer\s+)[A-Za-z0-9\-_]{20,}', 'critical', '硬编码 API 密钥'),
        (r'(ghp_|github_pat_)[A-Za-z0-9\-_]{22,}', 'critical', '硬编码 GitHub token'),
        (r'(AKIA|A3T|AGPA|AIDA|AIPA|AKIA|ANPA|ANVA|AROA|ASIA)[A-Z0-9]{16,}', 'critical', 'AWS 访问密钥'),
        (r'(xox[baprs]-)[0-9]{12}-[0-9]{12}-[0-9A-Za-z]{32}', 'high', 'Slack token'),
        (r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', 'low', '硬编码 IP 地址'),  # IPv4
        (r'(localhost|127\.0\.0\.1|0\.0\.0\.0)', 'medium', '本地地址'),
        (r'(mongodb|mysql|postgresql|redis)://[^\s]+', 'medium', '数据库连接字符串')
    ]

    # 危险操作正则
    DANGEROUS_OPERATIONS = [
        (r'rm\s+-rf\s+/', 'critical', '删除根目录'),
        (r'rm\s+-rf\s+~', 'critical', '删除 home 目录'),
        (r'rm\s+-rf\s+\.', 'critical', '删除当前目录'),
        (r'rmdir\s+/s\s+/q\s+[A-Za-z]:\\', 'critical', '删除 Windows 盘符'),
        (r'format\s+[A-Za-z]:', 'critical', '格式化磁盘'),
        (r'chmod\s+-R\s+777', 'high', '过度宽松权限'),
        (r'chown\s+-R\s+root', 'high', '修改系统文件所有者'),
        (r'shutdown\s+|reboot\s+|halt\s+', 'high', '系统关机/重启命令'),
        (r'kill\s+-9\s+-1', 'critical', '杀死所有进程'),
        (r'killall\s+-9', 'critical', '杀死所有进程')
    ]

    def __init__(self, skill_root: Optional[str] = None):
        self.skill_root = skill_root or os.getenv('LOBSTERAI_HOME', os.path.expanduser('~/.lobsterai'))
        self.resources_dir = os.path.join(self.skill_root, 'resources', 'SKILLs')

    def scan_file(self, file_path: str) -> ScanResult:
        """
        扫描单个 Python 文件

        Args:
            file_path: 文件路径

        Returns:
            ScanResult: 扫描结果
        """
        import time
        start_time = time.time()

        # 提取 skill_id（从路径中）
        skill_id = self._extract_skill_id(file_path)

        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # AST 分析
            tree = ast.parse(content)
            ast_issues = self._scan_ast(tree, file_path, lines)
            issues.extend(ast_issues)

            # 正则匹配
            regex_issues = self._scan_regex(content, file_path, lines)
            issues.extend(regex_issues)

            # 计算威胁等级
            threat_level = self._calculate_threat_level(issues)

            scanned_lines = len(lines)

        except Exception as e:
            issues.append({
                'line': 0,
                'column': 0,
                'type': 'parse_error',
                'severity': 'critical',
                'message': f'无法解析文件: {str(e)}',
                'snippet': ''
            })
            threat_level = 'critical'
            scanned_lines = 0

        scan_time = time.time() - start_time

        result = ScanResult(
            file_path=file_path,
            skill_id=skill_id,
            threat_level=threat_level,
            issues=issues,
            scanned_lines=scanned_lines,
            scanned_time=scan_time
        )

        # 记录审计日志
        audit_logger.log_event(
            event_type='code_scan',
            details=result.to_dict()
        )

        return result

    def _extract_skill_id(self, file_path: str) -> str:
        """从文件路径提取 skill_id"""
        path = Path(file_path)
        # 查找 SKILLs 目录下的技能
        try:
            idx = path.parts.index('SKILLs')
            if idx + 1 < len(path.parts):
                return path.parts[idx + 1]
        except ValueError:
            pass
        return 'unknown'

    def _scan_ast(self, tree: ast.AST, file_path: str, lines: List[str]) -> List[Dict[str, Any]]:
        """使用 AST 扫描危险模式"""
        issues = []

        class DangerVisitor(ast.NodeVisitor):
            def __init__(self, scanner: 'PythonCodeScanner'):
                self.scanner = scanner
                self.issues = []

            def visit_Call(self, node: ast.Call):
                """检查危险函数调用"""
                func_name = self._get_func_name(node)
                if func_name in self.scanner.DANGEROUS_FUNCTIONS:
                    severity = self.scanner.DANGEROUS_FUNCTIONS[func_name]
                    self.issues.append({
                        'line': node.lineno,
                        'column': node.col_offset,
                        'type': 'dangerous_function_call',
                        'severity': severity,
                        'message': f'调用危险函数: {func_name}',
                        'snippet': lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ''
                    })
                self.generic_visit(node)

            def visit_Import(self, node: ast.Import):
                """检查危险模块导入"""
                for alias in node.names:
                    module_name = alias.name.split('.')[0]
                    if module_name in self.scanner.DANGEROUS_MODULES:
                        severity = self.scanner.DANGEROUS_MODULES[module_name]
                        self.issues.append({
                            'line': node.lineno,
                            'column': node.col_offset,
                            'type': 'dangerous_import',
                            'severity': severity,
                            'message': f'导入危险模块: {module_name}',
                            'snippet': lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ''
                        })
                self.generic_visit(node)

            def visit_ImportFrom(self, node: ast.ImportFrom):
                """检查 from ... import ..."""
                if node.module:
                    module_name = node.module.split('.')[0]
                    if module_name in self.scanner.DANGEROUS_MODULES:
                        severity = self.scanner.DANGEROUS_MODULES[module_name]
                        self.issues.append({
                            'line': node.lineno,
                            'column': node.col_offset,
                            'type': 'dangerous_import_from',
                            'severity': severity,
                            'message': f'从危险模块导入: {module_name}',
                            'snippet': lines[node.lineno - 1].strip() if node.lineno <= len(lines) else ''
                        })
                self.generic_visit(node)

            def _get_func_name(self, node: ast.Call) -> str:
                """提取函数名"""
                if isinstance(node.func, ast.Name):
                    return node.func.id
                elif isinstance(node.func, ast.Attribute):
                    # 例如: os.system
                    value = node.func.value
                    if isinstance(value, ast.Name):
                        return f"{value.id}.{node.func.attr}"
                return ''

        visitor = DangerVisitor(self)
        visitor.visit(tree)
        issues.extend(visitor.issues)

        return issues

    def _scan_regex(self, content: str, file_path: str, lines: List[str]) -> List[Dict[str, Any]]:
        """使用正则扫描"""
        issues = []

        # 扫描敏感信息
        for pattern, severity, message in self.SENSITIVE_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'line': line_num,
                    'column': match.start(),
                    'type': 'sensitive_data_exposure',
                    'severity': severity,
                    'message': message,
                    'snippet': lines[line_num - 1].strip() if line_num <= len(lines) else ''
                })

        # 扫描危险操作（shell 命令）
        for pattern, severity, message in self.DANGEROUS_OPERATIONS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                line_num = content[:match.start()].count('\n') + 1
                issues.append({
                    'line': line_num,
                    'column': match.start(),
                    'type': 'dangerous_operation',
                    'severity': severity,
                    'message': message,
                    'snippet': lines[line_num - 1].strip() if line_num <= len(lines) else ''
                })

        return issues

    def _calculate_threat_level(self, issues: List[Dict[str, Any]]) -> str:
        """计算总体威胁等级"""
        if not issues:
            return 'safe'

        severities = [issue['severity'] for issue in issues]
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}

        max_severity = max(severities, key=lambda s: severity_order.get(s, 0))

        # 如果有多个 critical，保持 critical
        if severities.count('critical') >= 2:
            return 'critical'
        if 'critical' in severities:
            return 'critical'
        if 'high' in severities:
            return 'high'

        return max_severity

    def scan_skill(self, skill_id: str) -> ScanResult:
        """
        扫描整个技能目录

        Args:
            skill_id: 技能ID

        Returns:
            ScanResult: 扫描结果
        """
        skill_path = os.path.join(self.resources_dir, skill_id)
        if not os.path.exists(skill_path):
            return ScanResult(
                file_path=skill_path,
                skill_id=skill_id,
                threat_level='error',
                issues=[{'type': 'not_found', 'message': f'技能目录不存在: {skill_path}'}],
                scanned_lines=0,
                scanned_time=0.0
            )

        # 递归扫描所有 Python 文件
        all_issues = []
        total_lines = 0
        py_files = list(Path(skill_path).rglob('*.py'))

        for py_file in py_files:
            result = self.scan_file(str(py_file))
            all_issues.extend(result.issues)
            total_lines += result.scanned_lines

        threat_level = self._calculate_threat_level(all_issues)

        return ScanResult(
            file_path=skill_path,
            skill_id=skill_id,
            threat_level=threat_level,
            issues=all_issues,
            scanned_lines=total_lines,
            scanned_time=0.0
        )

    def scan_all_skills(self) -> List[ScanResult]:
        """扫描所有技能"""
        results = []
        if not os.path.exists(self.resources_dir):
            return results

        for skill_id in os.listdir(self.resources_dir):
            skill_path = os.path.join(self.resources_dir, skill_id)
            if os.path.isdir(skill_path):
                result = self.scan_skill(skill_id)
                results.append(result)

        return results

    def generate_report(self, results: List[ScanResult], output_format: str = 'json') -> str:
        """
        生成扫描报告

        Args:
            results: 扫描结果列表
            output_format: 输出格式（json, markdown）

        Returns:
            str: 报告内容
        """
        if output_format == 'json':
            report = {
                'scan_time': audit_logger.format_timestamp(),
                'total_skills': len(results),
                'summary': {
                    'critical': sum(1 for r in results if r.threat_level == 'critical'),
                    'high': sum(1 for r in results if r.threat_level == 'high'),
                    'medium': sum(1 for r in results if r.threat_level == 'medium'),
                    'low': sum(1 for r in results if r.threat_level == 'low'),
                    'safe': sum(1 for r in results if r.threat_level == 'safe')
                },
                'results': [r.to_dict() for r in results]
            }
            return json.dumps(report, indent=2, ensure_ascii=False)

        elif output_format == 'markdown':
            lines = [
                '# 恶意代码扫描报告',
                f'- 扫描时间: {audit_logger.format_timestamp()}',
                f'- 扫描技能数: {len(results)}',
                '',
                '## 汇总',
                '| 威胁等级 | 数量 |',
                '|----------|------|',
                f"| 🔴 Critical | {sum(1 for r in results if r.threat_level == 'critical')} |",
                f"| 🟠 High | {sum(1 for r in results if r.threat_level == 'high')} |",
                f"| 🟡 Medium | {sum(1 for r in results if r.threat_level == 'medium')} |",
                f"| 🟢 Low | {sum(1 for r in results if r.threat_level == 'low')} |",
                f"| ✅ Safe | {sum(1 for r in results if r.threat_level == 'safe')} |",
                '',
                '## 详细结果',
                ''
            ]

            for result in results:
                if result.threat_level != 'safe':
                    lines.extend([
                        f'### {result.skill_id}',
                        f'- **威胁等级**: {result.threat_level}',
                        f'- 文件: `{result.file_path}`',
                        f'- 扫描行数: {result.scanned_lines}',
                        '',
                        '| 行号 | 类型 | 严重性 | 描述 |',
                        '|------|------|--------|------|'
                    ])
                    for issue in result.issues:
                        lines.append(f"| {issue['line']} | {issue['type']} | {issue['severity']} | {issue['message']} |")
                    lines.append('')

            return '\n'.join(lines)

        return ''


# 全局扫描器实例
_global_scanner: Optional[PythonCodeScanner] = None


def get_scanner() -> PythonCodeScanner:
    """获取全局扫描器实例"""
    global _global_scanner
    if _global_scanner is None:
        _global_scanner = PythonCodeScanner()
    return _global_scanner


def scan_skill(skill_id: str) -> ScanResult:
    """扫描单个技能"""
    return get_scanner().scan_skill(skill_id)


def scan_all_skills() -> List[ScanResult]:
    """扫描所有技能"""
    return get_scanner().scan_all_skills()
