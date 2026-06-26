"""
依赖漏洞扫描器 - 检查 Python 依赖的安全漏洞
支持 requirements.txt, pyproject.toml, setup.py

集成选项：
- 内置轻量级扫描（使用本地漏洞数据库）
- 可选集成 safety/pip-audit（如果安装）
"""

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, asdict
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_logger import audit_logger


@dataclass
class Vulnerability:
    """漏洞数据类"""
    package: str
    version: str
    vulnerability_id: str
    severity: str  # critical, high, medium, low
    description: str
    fixed_in: Optional[str] = None


@dataclass
class DependencyScanResult:
    """依赖扫描结果"""
    skill_id: str
    dependencies: List[Dict[str, str]]
    vulnerabilities: List[Dict[str, Any]]
    threat_level: str
    scanned_files: List[str]

    def to_dict(self):
        return asdict(self)


class DependencyScanner:
    """依赖漏洞扫描器"""

    # 已知高危漏洞（内置数据库 - 示例）
    KNOWN_VULNERABILITIES = {
        'requests': {
            '2.0.0-2.3.0': [
                {
                    'id': 'CVE-2018-18074',
                    'severity': 'high',
                    'description': 'Requests 2.0.0-2.3.0 存在信息泄露漏洞，在重定向时可能泄露凭证'
                }
            ]
        },
        'django': {
            '1.11.0-2.0.0': [
                {
                    'id': 'CVE-2019-3498',
                    'severity': 'critical',
                    'description': 'Django 1.11.x-2.0.x 存在任意文件读取漏洞'
                }
            ],
            '2.0.0-2.1.0': [
                {
                    'id': 'CVE-2019-3498',
                    'severity': 'high',
                    'description': 'Django 2.0.x-2.1.x 存在 SQL 注入漏洞'
                }
            ]
        },
        'flask': {
            '0.5.0-1.0.0': [
                {
                    'id': 'CVE-2019-1010083',
                    'severity': 'medium',
                    'description': 'Flask 0.5.0-1.0.0 存在正则表达式拒绝服务漏洞'
                }
            ]
        },
        'pyyaml': {
            '5.1-5.2': [
                {
                    'id': 'CVE-2020-1747',
                    'severity': 'high',
                    'description': 'PyYAML 5.1-5.2 存在任意代码执行漏洞'
                }
            ]
        },
        'urllib3': {
            '1.24.0-1.25.0': [
                {
                    'id': 'CVE-2019-11324',
                    'severity': 'medium',
                    'description': 'urllib3 1.24.0-1.25.0 存在 CRLF 注入漏洞'
                }
            ]
        }
    }

    def __init__(self, skill_root: Optional[str] = None):
        self.skill_root = skill_root or os.getenv('LOBSTERAI_HOME', os.path.expanduser('~/.lobsterai'))
        self.resources_dir = os.path.join(self.skill_root, 'resources', 'SKILLs')

    def find_dependency_files(self, skill_id: str) -> List[str]:
        """查找技能目录下的依赖文件"""
        skill_path = os.path.join(self.resources_dir, skill_id)
        if not os.path.exists(skill_path):
            return []

        dependency_files = []
        patterns = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile']
        for pattern in patterns:
            files = list(Path(skill_path).rglob(pattern))
            dependency_files.extend([str(f) for f in files])

        return dependency_files

    def parse_requirements_txt(self, file_path: str) -> List[Dict[str, str]]:
        """解析 requirements.txt"""
        dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # 解析 package==version 或 package>=version
                    match = re.match(r'^([a-zA-Z0-9\-_]+)\s*([<>=!~]=?)\s*([a-zA-Z0-9\.\-_]+)', line)
                    if match:
                        dependencies.append({
                            'package': match.group(1).lower(),
                            'version': match.group(3),
                            'file': file_path,
                            'specifier': match.group(2)
                        })
        except Exception as e:
            audit_logger.log_event(
                event_type='dependency_scan_error',
                details={'file': file_path, 'error': str(e)},
                level='error'
            )
        return dependencies

    def parse_pyproject_toml(self, file_path: str) -> List[Dict[str, str]]:
        """解析 pyproject.toml（简化版）"""
        dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 查找 [project.dependencies] 或 [tool.poetry.dependencies]
            if '[project.dependencies]' in content or 'dependencies = [' in content:
                # 匹配依赖字符串: "package >=1.0,<2.0" 或 "package==1.0"
                pattern = r'"([a-zA-Z0-9\-_]+)\s*([<>=!~]=?)\s*([a-zA-Z0-9\.\-_,]+)"'
                for match in re.finditer(pattern, content):
                    package = match.group(1).lower()
                    version = match.group(3)
                    # 简化：取第一个版本约束
                    if ',' in version:
                        version = version.split(',')[0]
                    dependencies.append({
                        'package': package,
                        'version': version,
                        'file': file_path,
                        'specifier': match.group(2)
                    })
        except Exception as e:
            audit_logger.log_event(
                event_type='dependency_scan_error',
                details={'file': file_path, 'error': str(e)},
                level='error'
            )
        return dependencies

    def parse_dependencies(self, file_path: str) -> List[Dict[str, str]]:
        """根据文件类型解析依赖"""
        if file_path.endswith('requirements.txt'):
            return self.parse_requirements_txt(file_path)
        elif file_path.endswith('pyproject.toml'):
            return self.parse_pyproject_toml(file_path)
        elif file_path.endswith('setup.py'):
            # 简化处理：提取 install_requires
            return self._parse_setup_py(file_path)
        return []

    def _parse_setup_py(self, file_path: str) -> List[Dict[str, str]]:
        """解析 setup.py（提取 install_requires）"""
        dependencies = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'setup':
                    for keyword in node.keywords:
                        if keyword.arg == 'install_requires':
                            if isinstance(keyword.value, ast.List):
                                for elt in keyword.value.elts:
                                    if isinstance(elt, ast.Str):
                                        dep = elt.s
                                        match = re.match(r'^([a-zA-Z0-9\-_]+)\s*([<>=!~]=?)\s*([a-zA-Z0-9\.\-_]+)', dep)
                                        if match:
                                            dependencies.append({
                                                'package': match.group(1).lower(),
                                                'version': match.group(3),
                                                'file': file_path,
                                                'specifier': match.group(2)
                                            })
        except Exception as e:
            audit_logger.log_event(
                event_type='dependency_scan_error',
                details={'file': file_path, 'error': str(e)},
                level='error'
            )
        return dependencies

    def check_vulnerabilities(self, dependencies: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        检查依赖漏洞

        优先级：
        1. 尝试使用 safety（如果安装）
        2. 尝试使用 pip-audit（如果安装）
        3. 始终结合内置轻量级数据库（作为补充，不替代）
        """
        vulnerabilities = []

        # 尝试使用外部工具
        tool_vulns = []
        if self._is_tool_available('safety'):
            tool_vulns = self._check_with_safety(dependencies)
        elif self._is_tool_available('pip_audit'):
            tool_vulns = self._check_with_pip_audit(dependencies)

        # 始终检查内置数据库（作为后备和补充）
        builtin_vulns = self._check_with_builtin_db(dependencies)

        # 合并结果，去重（基于 vulnerability_id + package）
        seen = set()
        for vuln in tool_vulns + builtin_vulns:
            key = (vuln['package'], vuln['vulnerability_id'])
            if key not in seen:
                seen.add(key)
                vulnerabilities.append(vuln)

        return vulnerabilities

    def _is_tool_available(self, tool: str) -> bool:
        """检查外部工具是否可用"""
        try:
            if tool == 'safety':
                import safety  # noqa
                return True
            elif tool == 'pip_audit':
                subprocess.run([sys.executable, '-m', 'pip_audit', '--version'], capture_output=True, check=False)
                return True
        except:
            pass
        return False

    def _check_with_safety(self, dependencies: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """使用 safety 检查漏洞"""
        vulnerabilities = []
        try:
            # 创建临时 requirements 文件
            temp_req = 'temp_requirements.txt'
            with open(temp_req, 'w') as f:
                for dep in dependencies:
                    f.write(f"{dep['package']}=={dep['version']}\n")

            # 运行 safety check
            result = subprocess.run(
                [sys.executable, '-m', 'safety', 'check', '-r', temp_req, '--json'],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                # 无漏洞
                pass
            else:
                # 解析输出
                try:
                    data = json.loads(result.stdout)
                    for vuln in data.get('vulnerabilities', []):
                        vulnerabilities.append({
                            'package': vuln['package'],
                            'version': vuln['vulnerable_spec'],
                            'vulnerability_id': vuln['vulnerability_id'],
                            'severity': vuln['severity'],
                            'description': vuln['advisory'],
                            'fixed_in': vuln.get('fixed_version')
                        })
                except:
                    pass

            # 清理临时文件
            if os.path.exists(temp_req):
                os.remove(temp_req)

        except Exception as e:
            audit_logger.log_event(
                event_type='safety_check_error',
                details={'error': str(e)},
                level='error'
            )
        return vulnerabilities

    def _check_with_pip_audit(self, dependencies: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """使用 pip-audit 检查漏洞"""
        vulnerabilities = []
        try:
            temp_req = 'temp_requirements.txt'
            with open(temp_req, 'w') as f:
                for dep in dependencies:
                    f.write(f"{dep['package']}=={dep['version']}\n")

            result = subprocess.run(
                [sys.executable, '-m', 'pip_audit', '-r', temp_req, '--format', 'json'],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.stdout:
                try:
                    data = json.loads(result.stdout)
                    for vuln in data.get('dependencies', []):
                        pkg = vuln['name']
                        for v in vuln.get('vulnerabilities', []):
                            vulnerabilities.append({
                                'package': pkg,
                                'version': vuln['version'],
                                'vulnerability_id': v['id'],
                                'severity': v['severity'],
                                'description': v['description'],
                                'fixed_in': v.get('fixed_versions', [None])[0]
                            })
                except:
                    pass

            if os.path.exists(temp_req):
                os.remove(temp_req)

        except Exception as e:
            audit_logger.log_event(
                event_type='pip_audit_error',
                details={'error': str(e)},
                level='error'
            )
        return vulnerabilities

    def _check_with_builtin_db(self, dependencies: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """使用内置漏洞数据库"""
        vulnerabilities = []

        for dep in dependencies:
            package = dep['package']
            version = dep['version']

            # 检查内置数据库
            if package in self.KNOWN_VULNERABILITIES:
                for version_range, vulns in self.KNOWN_VULNERABILITIES[package].items():
                    if self._version_in_range(version, version_range):
                        for vuln in vulns:
                            vulnerabilities.append({
                                'package': package,
                                'version': version,
                                'vulnerability_id': vuln['id'],
                                'severity': vuln['severity'],
                                'description': vuln['description'],
                                'fixed_in': None,
                                'source': 'builtin_db'
                            })

        return vulnerabilities

    def _version_in_range(self, version: str, version_range: str) -> bool:
        """检查版本是否在漏洞范围内（简化版）"""
        # 格式: "1.0.0-1.2.0" 表示闭区间
        if '-' in version_range:
            low, high = version_range.split('-')
            return low <= version <= high
        return False

    def scan_skill(self, skill_id: str) -> DependencyScanResult:
        """扫描单个技能的依赖"""
        files = self.find_dependency_files(skill_id)

        all_dependencies = []
        scanned_files = []

        for file_path in files:
            deps = self.parse_dependencies(file_path)
            all_dependencies.extend(deps)
            scanned_files.append(file_path)

        vulnerabilities = self.check_vulnerabilities(all_dependencies)

        # 计算威胁等级
        threat_level = self._calculate_threat_level(vulnerabilities)

        return DependencyScanResult(
            skill_id=skill_id,
            dependencies=[{'package': d['package'], 'version': d['version'], 'file': d['file']} for d in all_dependencies],
            vulnerabilities=vulnerabilities,
            threat_level=threat_level,
            scanned_files=scanned_files
        )

    def scan_all_skills(self) -> List[DependencyScanResult]:
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

    def _calculate_threat_level(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """计算威胁等级"""
        if not vulnerabilities:
            return 'safe'

        severities = [v['severity'] for v in vulnerabilities]
        if 'critical' in severities:
            return 'critical'
        if 'high' in severities:
            return 'high'
        if 'medium' in severities:
            return 'medium'
        return 'low'

    def generate_report(self, results: List[DependencyScanResult], output_format: str = 'json') -> str:
        """生成扫描报告"""
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
                '# 依赖漏洞扫描报告',
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
                '## 详细漏洞',
                ''
            ]

            for result in results:
                if result.vulnerabilities:
                    lines.extend([
                        f'### {result.skill_id}',
                        f'- **威胁等级**: {result.threat_level}',
                        f'- 依赖数: {len(result.dependencies)}',
                        f'- 漏洞数: {len(result.vulnerabilities)}',
                        '',
                        '| 包名 | 当前版本 | CVE ID | 严重性 | 描述 | 修复版本 |',
                        '|------|----------|--------|--------|------|----------|'
                    ])
                    for vuln in result.vulnerabilities:
                        lines.append(
                            f"| {vuln['package']} | {vuln['version']} | {vuln['vulnerability_id']} | {vuln['severity']} | {vuln['description'][:50]}... | {vuln.get('fixed_in', 'N/A')} |"
                        )
                    lines.append('')

            return '\n'.join(lines)

        return ''


# 全局扫描器实例
_global_dep_scanner: Optional[DependencyScanner] = None


def get_dependency_scanner() -> DependencyScanner:
    """获取全局依赖扫描器实例"""
    global _global_dep_scanner
    if _global_dep_scanner is None:
        _global_dep_scanner = DependencyScanner()
    return _global_dep_scanner


def scan_skill_dependencies(skill_id: str) -> DependencyScanResult:
    """扫描技能依赖"""
    return get_dependency_scanner().scan_skill(skill_id)


def scan_all_dependencies() -> List[DependencyScanResult]:
    """扫描所有技能依赖"""
    return get_dependency_scanner().scan_all_skills()
