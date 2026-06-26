"""
输入验证器 - 验证所有用户输入和系统输入
防止路径遍历、注入攻击、DoS 等
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
from dataclasses import dataclass
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from audit_logger import audit_logger


@dataclass
class ValidationResult:
    """验证结果"""
    is_valid: bool
    errors: List[str]
    sanitized_value: Any = None


class InputValidator:
    """输入验证器"""

    # 危险路径遍历模式
    PATH_TRAVERSAL_PATTERNS = [
        r'\.\./',           # ../ 或 ..\\
        r'\.\.\\',          # Windows 风格
        r'^/',              # 绝对路径（Unix）
        r'^[A-Za-z]:\\',    # 绝对路径（Windows）
        r'^\0',             # 空字节注入
    ]

    # 危险命令模式（用于 prompt 验证）
    DANGEROUS_COMMANDS = [
        r'rm\s+-rf',
        r'rmdir\s+/s',
        r'format\s+[A-Za-z]:',
        r'chmod\s+777',
        r'shutdown',
        r'reboot',
        r'halt',
        r'kill\s+-9\s+-1',
        r'killall',
        r'wget\s+http',
        r'curl\s+http',
        r'nc\s+-[el]',
        r'bash\s+-c',
        r'sh\s+-c',
        r'\$\(',
        r'`',  # 反引号命令注入
    ]

    # 邮箱正则
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    # 文件名安全模式
    SAFE_FILENAME_REGEX = re.compile(r'^[a-zA-Z0-9._\-]+$')

    def __init__(self,
                 allowed_dirs: Optional[List[str]] = None,
                 max_input_size: int = 1024 * 1024):  # 1MB
        """
        初始化验证器

        Args:
            allowed_dirs: 允许的文件访问目录列表
            max_input_size: 最大输入大小（字节）
        """
        self.allowed_dirs = [os.path.abspath(d) for d in (allowed_dirs or [])]
        self.max_input_size = max_input_size

    def validate_path(self, user_path: str, allowed_base: Optional[str] = None) -> ValidationResult:
        """
        验证文件路径安全性

        Args:
            user_path: 用户提供的路径
            allowed_base: 允许的基目录（覆盖实例的 allowed_dirs）

        Returns:
            ValidationResult
        """
        errors = []

        # 检查大小
        if len(user_path.encode('utf-8')) > self.max_input_size:
            errors.append('Input too large')
            return ValidationResult(False, errors)

        # 检查路径遍历
        for pattern in self.PATH_TRAVERSAL_PATTERNS:
            if re.search(pattern, user_path, re.IGNORECASE):
                errors.append(f'Path traversal attempt detected: {pattern}')
                audit_logger.log_event(
                    event_type='path_traversal_blocked',
                    details={'path': user_path, 'pattern': pattern},
                    level='warning'
                )
                return ValidationResult(False, errors)

        # 检查是否在允许的目录内
        allowed_dirs = self.allowed_dirs
        if allowed_base:
            allowed_dirs = [os.path.abspath(allowed_base)]

        if allowed_dirs:
            abs_path = os.path.abspath(user_path)
            if not any(abs_path.startswith(allowed) for allowed in allowed_dirs):
                errors.append(f'Path outside allowed directories: {abs_path}')
                return ValidationResult(False, errors)

        return ValidationResult(True, [], user_path)

    def validate_filename(self, filename: str) -> ValidationResult:
        """
        验证文件名安全性（防止特殊字符）
        """
        errors = []
        if not filename:
            errors.append('Filename is required')
            return ValidationResult(False, errors)

        if not self.SAFE_FILENAME_REGEX.match(filename):
            errors.append('Filename contains unsafe characters (only alphanumeric, ., _, - allowed)')
            return ValidationResult(False, errors)

        # 检查是否为空文件名或仅扩展名
        stem = Path(filename).stem
        if not stem:
            errors.append('Invalid filename (no name before extension)')
            return ValidationResult(False, errors)

        return ValidationResult(True, [], filename)

    def validate_prompt(self, prompt: str, skill_id: Optional[str] = None) -> ValidationResult:
        """
        验证 prompt 内容（防止命令注入、恶意指令）

        Args:
            prompt: 用户提供的 prompt
            skill_id: 技能ID（用于上下文）

        Returns:
            ValidationResult
        """
        errors = []
        prompt_lower = prompt.lower()

        # 检查大小
        if len(prompt.encode('utf-8')) > self.max_input_size:
            errors.append('Prompt too large')
            return ValidationResult(False, errors)

        # 检查危险命令
        for pattern in self.DANGEROUS_COMMANDS:
            if re.search(pattern, prompt_lower):
                errors.append(f'Dangerous command detected: {pattern}')
                audit_logger.log_event(
                    event_type='dangerous_prompt_blocked',
                    details={'skill_id': skill_id, 'pattern': pattern, 'prompt_preview': prompt[:200]},
                    level='error'
                )
                return ValidationResult(False, errors)

        # 检查过多的特殊字符（可能的 DoS）
        special_chars = sum(1 for c in prompt if ord(c) > 127 or c in '`$&|<>{}[]')
        if special_chars / len(prompt) > 0.3:  # 超过 30% 的特殊字符
            errors.append('Prompt contains excessive special characters (potential DoS)')
            return ValidationResult(False, errors)

        return ValidationResult(True, [], prompt)

    def validate_email(self, email: str) -> ValidationResult:
        """验证邮箱格式"""
        errors = []
        if not email:
            errors.append('Email is required')
            return ValidationResult(False, errors)

        if not self.EMAIL_REGEX.match(email):
            errors.append('Invalid email format')
            return ValidationResult(False, errors)

        return ValidationResult(True, [], email)

    def validate_json_schema(self, data: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
        """
        基于 JSON Schema 验证数据

        Args:
            data: 待验证数据
            schema: JSON Schema（简化版）

        Returns:
            ValidationResult
        """
        errors = []
        sanitized = {}

        # 检查必填字段
        required = schema.get('required', [])
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # 检查属性类型
        properties = schema.get('properties', {})
        for key, value in data.items():
            if key in properties:
                field_schema = properties[key]
                field_type = field_schema.get('type')

                if field_type == 'string':
                    if not isinstance(value, str):
                        errors.append(f"Field {key} must be string")
                    else:
                        # 检查最小/最大长度
                        min_len = field_schema.get('minLength')
                        max_len = field_schema.get('maxLength')
                        if min_len is not None and len(value) < min_len:
                            errors.append(f"Field {key} too short (min {min_len})")
                        if max_len is not None and len(value) > max_len:
                            errors.append(f"Field {key} too long (max {max_len})")

                elif field_type == 'integer':
                    if not isinstance(value, int):
                        errors.append(f"Field {key} must be integer")
                    else:
                        # 检查最小值/最大值
                        minimum = field_schema.get('minimum')
                        maximum = field_schema.get('maximum')
                        if minimum is not None and value < minimum:
                            errors.append(f"Field {key} below minimum ({minimum})")
                        if maximum is not None and value > maximum:
                            errors.append(f"Field {key} above maximum ({maximum})")

                elif field_type == 'number':
                    if not isinstance(value, (int, float)):
                        errors.append(f"Field {key} must be number")
                elif field_type == 'boolean':
                    if not isinstance(value, bool):
                        errors.append(f"Field {key} must be boolean")
                elif field_type == 'array':
                    if not isinstance(value, list):
                        errors.append(f"Field {key} must be array")
                elif field_type == 'object':
                    if not isinstance(value, dict):
                        errors.append(f"Field {key} must be object")

                # 枚举检查
                if 'enum' in field_schema and value not in field_schema['enum']:
                    errors.append(f"Field {key} must be one of {field_schema['enum']}")

                # 格式检查
                if 'format' in field_schema:
                    if field_schema['format'] == 'email':
                        result = self.validate_email(value)
                        if not result.is_valid:
                            errors.append(f"Field {key}: {', '.join(result.errors)}")

            else:
                # 如果 schema 设置了 additionalProperties = false，则额外字段不允许
                if schema.get('additionalProperties', True) is False:
                    errors.append(f"Unexpected field: {key}")

        is_valid = len(errors) == 0
        if is_valid:
            sanitized = data.copy()

        return ValidationResult(is_valid, errors, sanitized)

    def sanitize_string(self, text: str, max_length: Optional[int] = None) -> str:
        """
        清理字符串输入（移除控制字符、修剪等）
        """
        if not text:
            return ''

        # 移除控制字符（保留 \n \r \t）
        sanitized = ''.join(c for c in text if ord(c) >= 32 or c in '\n\r\t')

        # 修剪首尾空白
        sanitized = sanitized.strip()

        # 限制长度
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]

        return sanitized

    def validate_skill_prompt(self, skill_id: str, prompt: str) -> ValidationResult:
        """
        技能特定的 prompt 验证
        可以针对不同技能有不同的验证规则
        """
        # 通用验证
        result = self.validate_prompt(prompt, skill_id)
        if not result.is_valid:
            return result

        # 技能特定规则（示例）
        if skill_id == 'scheduled-task':
            # 定时任务技能，检查是否包含危险时间表达式
            dangerous_crons = [
                r'@reboot',
                r'@yearly',
                r'0\s+0\s+\*',
            ]
            for pattern in dangerous_crons:
                if re.search(pattern, prompt):
                    return ValidationResult(
                        False,
                        [f'Dangerous cron expression detected: {pattern}'],
                        None
                    )

        return result


# 便捷函数
def validate_input(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    便捷函数：验证输入数据

    Returns:
        (is_valid, errors)
    """
    validator = InputValidator()
    result = validator.validate_json_schema(data, schema)
    return result.is_valid, result.errors


def validate_file_path(path: str, allowed_dir: Optional[str] = None) -> bool:
    """
    便捷函数：验证文件路径
    """
    validator = InputValidator(allowed_dirs=[allowed_dir] if allowed_dir else None)
    result = validator.validate_path(path)
    return result.is_valid


def validate_skill_prompt(skill_id: str, prompt: str) -> Tuple[bool, List[str]]:
    """
    便捷函数：验证技能 prompt
    """
    validator = InputValidator()
    result = validator.validate_skill_prompt(skill_id, prompt)
    return result.is_valid, result.errors
