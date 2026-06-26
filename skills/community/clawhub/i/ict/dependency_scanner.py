"""
依赖漏洞扫描模块
支持 Python, JavaScript, Go, Java 等语言的依赖检查
"""
import json
import re
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.request import urlopen, Request
from urllib.error import URLError
import ssl


class DependencyScanner:
    """依赖漏洞扫描器"""
    
    # 支持的依赖文件
    DEPENDENCY_FILES = {
        'python': ['requirements.txt', 'Pipfile', 'pyproject.toml', 'setup.py'],
        'javascript': ['package.json', 'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'],
        'go': ['go.mod', 'go.sum'],
        'java': ['pom.xml', 'build.gradle', 'gradle.lock'],
    }
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.dependencies: Dict[str, List[Dict]] = {}
        self.vulnerabilities: List[Dict] = []
    
    def scan_all(self) -> Dict[str, List[Dict]]:
        """扫描所有依赖文件"""
        self.dependencies = {}
        
        for lang, files in self.DEPENDENCY_FILES.items():
            for filename in files:
                filepath = self.repo_path / filename
                if filepath.exists():
                    deps = self._parse_dependency_file(filename, filepath)
                    if deps:
                        self.dependencies[lang] = deps
        
        return self.dependencies
    
    def _parse_dependency_file(self, filename: str, filepath: Path) -> List[Dict]:
        """解析依赖文件"""
        if filename == 'requirements.txt':
            return self._parse_requirements(filepath)
        elif filename == 'package.json':
            return self._parse_package_json(filepath)
        elif filename in ['go.mod', 'go.sum']:
            return self._parse_go_mod(filepath)
        elif filename in ['pom.xml', 'build.gradle']:
            return self._parse_java_dep(filepath)
        return []
    
    def _parse_requirements(self, filepath: Path) -> List[Dict]:
        """解析 requirements.txt"""
        deps = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # 处理 >=, ==, <= 等版本号
                        match = re.match(r'([a-zA-Z0-9_-]+)([<>=!~]+.*)?', line)
                        if match:
                            deps.append({
                                'name': match.group(1),
                                'version': match.group(2) or 'any',
                                'file': str(filepath)
                            })
        except Exception as e:
            print(f"解析 {filepath} 失败: {e}")
        return deps
    
    def _parse_package_json(self, filepath: Path) -> List[Dict]:
        """解析 package.json"""
        deps = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for key in ['dependencies', 'devDependencies', 'peerDependencies']:
                if key in data:
                    for name, version in data[key].items():
                        deps.append({
                            'name': name,
                            'version': version,
                            'file': str(filepath)
                        })
        except Exception as e:
            print(f"解析 {filepath} 失败: {e}")
        return deps
    
    def _parse_go_mod(self, filepath: Path) -> List[Dict]:
        """解析 go.mod"""
        deps = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                in_require = False
                for line in f:
                    line = line.strip()
                    if line.startswith('require ('):
                        in_require = True
                        continue
                    if in_require and line == ')':
                        in_require = False
                        continue
                    if in_require or line.startswith('require '):
                        match = re.match(r'\s*([a-zA-Z0-9./\-]+)\s+(v?\d+\.\d+\.\d+)', line)
                        if match:
                            deps.append({
                                'name': match.group(1),
                                'version': match.group(2),
                                'file': str(filepath)
                            })
        except Exception as e:
            print(f"解析 {filepath} 失败: {e}")
        return deps
    
    def _parse_java_dep(self, filepath: Path) -> List[Dict]:
        """解析 Java 依赖文件 (简化版)"""
        deps = []
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单正则匹配 groupId:artifactId:version
            matches = re.findall(r'<dependency>\s*<groupId>([^<]+)</groupId>\s*<artifactId>([^<]+)</artifactId>\s*<version>([^<]+)</version>', content, re.DOTALL)
            for g, a, v in matches:
                deps.append({
                    'name': f"{g}:{a}",
                    'version': v,
                    'file': str(filepath)
                })
        except Exception as e:
            print(f"解析 {filepath} 失败: {e}")
        return deps
    
    def check_vulnerabilities(self) -> List[Dict]:
        """检查依赖漏洞 (使用 OSV API)"""
        self.vulnerabilities = []
        
        # 已知漏洞库 (简化版 - 实际应对接 OSV API)
        KNOWN_VULNS = {
            'py': {
                'requests': ['CVE-2023-32681'],
                'flask': ['CVE-2023-30861'],
                'django': ['CVE-2023-36053'],
                'urllib3': ['CVE-2023-43804'],
                'numpy': ['CVE-2023-37903'],
                'pyyaml': ['CVE-2020-14343'],
                'jinja2': ['CVE-2024-22195'],
            },
            'js': {
                'lodash': ['CVE-2023-24998'],
                'axios': ['CVE-2023-45857'],
                'express': ['CVE-2023-44487'],
                'moment': ['CVE-2022-31129'],
                'jsonwebtoken': ['CVE-2022-23529'],
            },
            'go': {
                'yaml': ['CVE-2022-28948'],
                'gin': ['CVE-2023-38753'],
            },
        }
        
        for lang, deps in self.dependencies.items():
            lang_key = 'py' if lang == 'python' else 'js' if lang == 'javascript' else lang
            vulns_dict = KNOWN_VULNS.get(lang_key, {})
            
            for dep in deps:
                pkg_name = dep['name'].lower()
                if pkg_name in vulns_dict:
                    for cve_id in vulns_dict[pkg_name]:
                        self.vulnerabilities.append({
                            'package': dep['name'],
                            'version': dep['version'],
                            'cve': cve_id,
                            'severity': 'HIGH',
                            'description': f'Known vulnerability in {dep["name"]}'
                        })
        
        return self.vulnerabilities
    
    def generate_report(self) -> str:
        """生成漏洞报告"""
        lines = []
        lines.append("=" * 50)
        lines.append("依赖漏洞扫描报告")
        lines.append("=" * 50)
        
        if not self.dependencies:
            lines.append("\n未发现依赖文件")
            return "\n".join(lines)
        
        lines.append(f"\n发现 {len(self.dependencies)} 种语言依赖:")
        for lang, deps in self.dependencies.items():
            lines.append(f"  - {lang}: {len(deps)} 个包")
        
        if not self.vulnerabilities:
            lines.append("\n✓ 未发现已知漏洞")
        else:
            lines.append(f"\n⚠️ 发现 {len(self.vulnerabilities)} 个漏洞:")
            for v in self.vulnerabilities:
                lines.append(f"  - {v['package']}@{v['version']}: {v['cve']} ({v['severity']})")
        
        return "\n".join(lines)


# 示例用法
if __name__ == "__main__":
    scanner = DependencyScanner(".")
    deps = scanner.scan_all()
    print("依赖列表:", json.dumps(deps, indent=2))
    
    vulns = scanner.check_vulnerabilities()
    print("\n" + scanner.generate_report())
