#!/usr/bin/env python3
"""
环境变量扫描器
扫描项目中的环境变量和敏感配置
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field

# 导入统一常量
try:
    from constants import EXCLUDE_DIRS
except ImportError:
    EXCLUDE_DIRS = {
        '.git', '.svn', '.hg', '.idea', '.vscode',
        'node_modules', 'build', 'dist', 'out', 'bin', 'obj',
        '__pycache__', '.pytest_cache', '.mypy_cache',
        'target', 'vendor', 'CMakeFiles', '_deps',
        '.gradle', 'Pods', 'DerivedData',
        'venv', '.venv', 'env', '.env',
    }

# 添加日志支持
try:
    from utils.logger import get_logger
    logger = get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)


@dataclass
class EnvVariable:
    """环境变量"""
    name: str
    value: Optional[str] = None
    source: str = ''
    line: int = 0
    is_secret: bool = False
    is_set: bool = False  # 是否有值


@dataclass
class SecretFinding:
    """敏感信息发现"""
    type: str  # api_key, password, token, etc.
    file: str
    line: int
    snippet: str
    severity: str  # high, medium, low


class EnvScanner:
    """环境变量扫描器"""

    # 敏感关键词
    SECRET_KEYWORDS = [
        'password', 'passwd', 'pwd',
        'secret', 'api_key', 'apikey', 'api-key',
        'token', 'access_token', 'auth_token',
        'private_key', 'privatekey', 'private-key',
        'credential', 'credentials',
        'auth', 'authorization',
        'session', 'cookie',
        'ssh_key', 'sshkey',
        'aws_access_key', 'aws_secret',
        'database_url', 'db_password',
        'smtp_password', 'mail_password',
    ]

    # .env 文件模式
    ENV_FILE_PATTERNS = [
        '.env',
        '.env.local',
        '.env.development',
        '.env.production',
        '.env.test',
        '.env.staging',
        '.env.*',
    ]

    # 配置文件模式
    CONFIG_FILE_PATTERNS = [
        '*.env',
        'config.*',
        'settings.*',
        '*.config.*',
        '*.json',
        '*.yaml',
        '*.yml',
        '*.toml',
        '*.ini',
    ]

    # 环境变量模式
    ENV_VAR_PATTERNS = [
        # Shell 格式
        (r'^\s*([A-Z_][A-Z0-9_]*)\s*=\s*(.+)$', 'shell'),
        # Python os.environ
        (r"os\.environ(?:get)?\s*[\[\(]\s*['\"]([A-Z_][A-Z0-9_]*)['\"]", 'python'),
        # Node.js process.env
        (r"process\.env\.([A-Z_][A-Z0-9_]*)", 'nodejs'),
        # dotenv
        (r"dotenv\.([A-Z_][A-Z0-9_]*)", 'dotenv'),
    ]

    # 敏感值模式
    SENSITIVE_VALUE_PATTERNS = [
        (r'-----BEGIN\s+(?:RSA\s+)?PRIVATE KEY-----', 'private_key'),
        (r'sk-[a-zA-Z0-9]{20,}', 'openai_key'),
        (r'AKIA[0-9A-Z]{16}', 'aws_access_key'),
        (r'ghp_[a-zA-Z0-9]{36}', 'github_token'),
        (r'xox[baprs]-[a-zA-Z0-9-]+', 'slack_token'),
        (r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*', 'jwt_token'),
        (r'mongodb(\+srv)?://[^:]+:([^@]+)@', 'mongodb_uri'),
        (r'postgres(?:ql)?://[^:]+:([^@]+)@', 'postgres_uri'),
        (r'mysql://[^:]+:([^@]+)@', 'mysql_uri'),
        (r'redis://[^:]*:([^@]+)@', 'redis_uri'),
    ]

    def __init__(self, project_dir: str, scan_secrets: bool = True):
        self.project_dir = Path(project_dir).resolve()
        self.scan_secrets = scan_secrets
        self.env_vars: Dict[str, EnvVariable] = {}
        self.secrets_found: List[SecretFinding] = []
        self.env_files: List[str] = []

    def scan(self) -> Dict[str, Any]:
        """执行扫描"""
        logger.info(f"开始环境变量扫描: {self.project_dir}")

        self._scan_env_files()
        self._scan_source_files()

        if self.scan_secrets:
            self._scan_for_secrets()

        return self._generate_report()

    def _scan_env_files(self) -> None:
        """扫描 .env 文件"""
        for pattern in self.ENV_FILE_PATTERNS:
            for env_file in self.project_dir.glob(pattern):
                self._parse_env_file(env_file)
                self.env_files.append(str(env_file.relative_to(self.project_dir)))

    def _parse_env_file(self, file_path: Path) -> None:
        """解析 .env 文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            rel_path = str(file_path.relative_to(self.project_dir))

            for line_num, line in enumerate(lines, 1):
                line = line.strip()

                # 跳过注释和空行
                if not line or line.startswith('#'):
                    continue

                # 解析 KEY=VALUE
                match = re.match(r'^([A-Z_][A-Z0-9_]*)\s*=\s*(.*)$', line)
                if match:
                    name = match.group(1)
                    value = match.group(2).strip().strip('"').strip("'")

                    is_secret = self._is_secret_name(name)

                    self.env_vars[name] = EnvVariable(
                        name=name,
                        value='***' if is_secret else value,
                        source=rel_path,
                        line=line_num,
                        is_secret=is_secret,
                        is_set=bool(value),
                    )

        except Exception as e:
            logger.debug(f"解析 env 文件失败 {file_path}: {e}")

    def _scan_source_files(self) -> None:
        """扫描源代码中的环境变量引用"""
        source_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.rs', '.rb'}

        for root, dirs, files in os.walk(self.project_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                ext = Path(f).suffix.lower()
                if ext in source_extensions:
                    file_path = Path(root) / f
                    self._extract_env_from_source(file_path)

    def _extract_env_from_source(self, file_path: Path) -> None:
        """从源代码提取环境变量引用"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            rel_path = str(file_path.relative_to(self.project_dir))

            for pattern, source_type in self.ENV_VAR_PATTERNS:
                for match in re.finditer(pattern, content, re.MULTILINE):
                    name = match.group(1)

                    if name not in self.env_vars:
                        is_secret = self._is_secret_name(name)
                        self.env_vars[name] = EnvVariable(
                            name=name,
                            source=rel_path,
                            line=content[:match.start()].count('\n') + 1,
                            is_secret=is_secret,
                            is_set=False,
                        )

        except Exception as e:
            logger.debug(f"提取环境变量失败 {file_path}: {e}")

    def _scan_for_secrets(self) -> None:
        """扫描敏感信息"""
        for root, dirs, files in os.walk(self.project_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for f in files:
                ext = Path(f).suffix.lower()
                if ext in {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.go', '.json', '.yaml', '.yml', '.env'}:
                    file_path = Path(root) / f
                    self._find_secrets_in_file(file_path)

    def _find_secrets_in_file(self, file_path: Path) -> None:
        """在文件中查找敏感信息"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            rel_path = str(file_path.relative_to(self.project_dir))

            for line_num, line in enumerate(lines, 1):
                for pattern, secret_type in self.SENSITIVE_VALUE_PATTERNS:
                    if re.search(pattern, line):
                        # 脱敏
                        snippet = line.strip()[:50] + '...' if len(line.strip()) > 50 else line.strip()
                        snippet = re.sub(r'[a-zA-Z0-9]{10,}', '***REDACTED***', snippet)

                        self.secrets_found.append(SecretFinding(
                            type=secret_type,
                            file=rel_path,
                            line=line_num,
                            snippet=snippet,
                            severity='high',
                        ))

        except Exception as e:
            logger.debug(f"查找敏感信息失败 {file_path}: {e}")

    def _is_secret_name(self, name: str) -> bool:
        """检查变量名是否表示敏感信息"""
        name_lower = name.lower()
        return any(kw in name_lower for kw in self.SECRET_KEYWORDS)

    def _generate_report(self) -> Dict[str, Any]:
        """生成报告"""
        # 分类统计
        total_vars = len(self.env_vars)
        secret_vars = sum(1 for v in self.env_vars.values() if v.is_secret)
        set_vars = sum(1 for v in self.env_vars.values() if v.is_set)

        return {
            'summary': {
                'total_variables': total_vars,
                'secret_variables': secret_vars,
                'set_variables': set_vars,
                'env_files': self.env_files,
                'secrets_found': len(self.secrets_found),
            },
            'variables': [
                {
                    'name': v.name,
                    'source': v.source,
                    'line': v.line,
                    'is_secret': v.is_secret,
                    'is_set': v.is_set,
                }
                for v in sorted(self.env_vars.values(), key=lambda x: x.name)
            ],
            'secrets': [
                {
                    'type': s.type,
                    'file': s.file,
                    'line': s.line,
                    'severity': s.severity,
                }
                for s in self.secrets_found
            ],
            'recommendations': self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> List[str]:
        """生成安全建议"""
        recommendations = []

        # 检查是否有 .env 文件
        if self.env_files:
            recommendations.append("确保 .env 文件已添加到 .gitignore")

        # 检查未设置的变量
        unset_secrets = [v.name for v in self.env_vars.values() if v.is_secret and not v.is_set]
        if unset_secrets:
            recommendations.append(f"以下敏感变量未设置值: {', '.join(unset_secrets[:5])}")

        # 检查发现的敏感信息
        if self.secrets_found:
            recommendations.append(f"发现 {len(self.secrets_found)} 个潜在敏感信息泄露，请检查")

        # 检查是否需要 .env.example
        env_example = self.project_dir / '.env.example'
        if self.env_files and not env_example.exists():
            recommendations.append("建议创建 .env.example 文件作为模板")

        return recommendations


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: env_scanner.py <project_dir> [--no-secrets]")
        print("\nOptions:")
        print("  --no-secrets    Skip secret scanning")
        sys.exit(1)

    project_dir = sys.argv[1]
    scan_secrets = '--no-secrets' not in sys.argv

    scanner = EnvScanner(project_dir, scan_secrets=scan_secrets)
    result = scanner.scan()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()