"""
输出清理器 - 从日志和输出中移除敏感信息
防止密码、密钥、token 等敏感数据泄露到审计日志或错误报告中
"""

import re
from typing import Dict, Any, Optional


class OutputSanitizer:
    """敏感信息脱敏器"""

    # 敏感信息正则模式（按优先级排序）
    PATTERNS = [
        # API Keys
        (re.compile(r'(sk_live_|sk_test_|Bearer\s+)[A-Za-z0-9\-_]{20,}', re.IGNORECASE), '***API_KEY***'),
        (re.compile(r'api[_-]?key\s*[:=]\s*[\'"]?[A-Za-z0-9\-_]{20,}[\'"]?', re.IGNORECASE), '***API_KEY***'),
        (re.compile(r'(ghp_|github_pat_)[A-Za-z0-9\-_]{22,}', re.IGNORECASE), '***GITHUB_TOKEN***'),

        # AWS Keys
        (re.compile(r'(AKIA|A3T|AGPA|AIDA|AIPA|AKIA|ANPA|ANVA|AROA|ASIA)[A-Z0-9]{16,}', re.IGNORECASE), '***AWS_KEY***'),

        # Slack Tokens
        (re.compile(r'(xox[baprs]-)[0-9]{12}-[0-9]{12}-[0-9A-Za-z]{32}', re.IGNORECASE), '***SLACK_TOKEN***'),

        # Passwords
        (re.compile(r'(password|passwd|pwd)\s*[:=]\s*[\'"]?[^\'"\s]{4,}[\'"]?', re.IGNORECASE), '***PASSWORD***'),
        (re.compile(r'(secret|secret_key)\s*[:=]\s*[\'"]?[^\'"\s]{4,}[\'"]?', re.IGNORECASE), '***SECRET***'),

        # JWT Tokens
        (re.compile(r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', re.IGNORECASE), '***JWT_TOKEN***'),

        # Database Connection Strings
        (re.compile(r'(mongodb|mysql|postgresql|redis)://[^\s]+', re.IGNORECASE), '***DB_CONNECTION***'),

        # Email/Password combinations
        (re.compile(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}\s*[:=]\s*[\'"]?[^\'"\s]{4,}', re.IGNORECASE), '***EMAIL_PASS***'),

        # Hardcoded IPs (optional - keep if not sensitive)
        # (re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'), '***IP_ADDRESS***'),
    ]

    # 文件路径匿名化
    PATH_PATTERN = re.compile(r'([A-Za-z]:\\Users\\[A-Za-z0-9_\\-]+|[~/]+[\w/\\\.-]+)', re.IGNORECASE)

    @classmethod
    def sanitize(cls, text: str, preserve_length: bool = False) -> str:
        """
        清理文本中的敏感信息

        Args:
            text: 原始文本
            preserve_length: 是否保持脱敏后字符串长度（避免日志格式错乱）

        Returns:
            str: 脱敏后的文本
        """
        if not text:
            return text

        sanitized = text

        # 应用所有模式
        for pattern, replacement in cls.PATTERNS:
            if preserve_length:
                # 保持长度
                sanitized = pattern.sub(
                    lambda m: replacement * (len(m.group(0)) // len(replacement) + 1),
                    sanitized
                )
            else:
                sanitized = pattern.sub(replacement, sanitized)

        # 文件路径匿名化
        sanitized = cls.PATH_PATTERN.sub('***PATH***', sanitized)

        return sanitized

    @classmethod
    def sanitize_dict(cls, data: Dict[str, Any], preserve_length: bool = False) -> Dict[str, Any]:
        """
        递归清理字典中的敏感信息
        """
        sanitized = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized[key] = cls.sanitize(value, preserve_length)
            elif isinstance(value, dict):
                sanitized[key] = cls.sanitize_dict(value, preserve_length)
            elif isinstance(value, list):
                sanitized[key] = [
                    cls.sanitize_dict(item, preserve_length) if isinstance(item, dict) else
                    cls.sanitize(str(item), preserve_length) if isinstance(item, str) else
                    item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized

    @classmethod
    def contains_sensitive_data(cls, text: str) -> bool:
        """检查文本是否包含敏感信息"""
        for pattern, _ in cls.PATTERNS:
            if pattern.search(text):
                return True
        return False

    @classmethod
    def redact_sensitive_lines(cls, text: str, max_lines: int = 10) -> str:
        """
        脱敏敏感行，并限制返回的最大行数
        用于错误报告等场景
        """
        lines = text.split('\n')
        sanitized_lines = [cls.sanitize(line) for line in lines]

        if len(sanitized_lines) > max_lines:
            half = max_lines // 2
            sanitized_lines = (
                sanitized_lines[:half] +
                [f"... ({len(sanitized_lines) - max_lines} lines omitted) ..."] +
                sanitized_lines[-half:]
            )

        return '\n'.join(sanitized_lines)
