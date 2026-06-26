#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输入验证工具

用于防止恶意输入和路径穿越攻击
"""

import os
import re
from pathlib import Path
from typing import Optional, Tuple, List


class InputValidator:
    """输入验证器"""
    
    # 允许的音频文件扩展名
    ALLOWED_AUDIO_EXTS = {'.mp3', '.m4a', '.wav', '.ogg', '.flac', '.aac'}
    
    # 危险路径模式（防止路径穿越攻击）
    DANGEROUS_PATH_PATTERNS = [
        r'\.\./',    # ../
        r'\.\.\\',   # ..\
        r'~/',       # ~/
        r'~\\',      # ~\
        r'/\./',     # /.
        r'\\\./',    # \.
    ]
    
    # 危险命令（防止命令注入）
    DANGEROUS_COMMANDS = [
        'rm', 'del', 'format', 'delete', 'erase',
        'sudo', 'su', 'chmod', 'chown',
        'wget', 'curl', 'nc', 'netcat',
        'eval', 'exec', 'system', 'shell',
        '<script', 'javascript:', 'data:',
    ]
    
    @staticmethod
    def validate_audio_path(audio_path: str) -> Tuple[bool, str]:
        """
        验证音频文件路径
        
        Args:
            audio_path: 音频文件路径
        
        Returns:
            (is_valid, error_message)
        """
        # 1. 空值检查
        if not audio_path or not audio_path.strip():
            return False, "音频文件路径不能为空"
        
        audio_path = audio_path.strip()
        
        # 2. 路径穿越攻击检查
        for pattern in InputValidator.DANGEROUS_PATH_PATTERNS:
            if re.search(pattern, audio_path, re.IGNORECASE):
                return False, f"路径包含危险字符：{pattern}"
        
        # 3. 长度限制（防止缓冲区溢出）
        if len(audio_path) > 260:  # Windows 路径最大长度
            return False, "路径过长（最大 260 字符）"
        
        # 4. 转换为 Path 对象
        try:
            audio_file = Path(audio_path)
        except Exception as e:
            return False, f"无效路径格式：{e}"
        
        # 5. 检查是否存在
        if not audio_file.exists():
            return False, f"文件不存在：{audio_path}"
        
        # 6. 检查是否为文件（而非目录）
        if not audio_file.is_file():
            return False, f"路径不是文件：{audio_path}"
        
        # 7. 文件扩展名检查
        if audio_file.suffix.lower() not in InputValidator.ALLOWED_AUDIO_EXTS:
            return False, (f"不支持的文件格式：{audio_file.suffix}\n"
                         f"支持格式：{', '.join(InputValidator.ALLOWED_AUDIO_EXTS)}")
        
        # 8. 文件大小检查（防止超大文件）
        file_size_mb = audio_file.stat().st_size / (1024 * 1024)
        if file_size_mb > 500:  # 限制 500MB
            return False, f"文件过大：{file_size_mb:.1f} MB（最大 500 MB）"
        
        # 9. 文件权限检查
        if not os.access(audio_path, os.R_OK):
            return False, f"文件不可读：{audio_path}"
        
        return True, ""
    
    @staticmethod
    def validate_numeric_input(
        user_input: str,
        min_value: int,
        max_value: int,
        field_name: str = "输入"
    ) -> Tuple[bool, Optional[int], str]:
        """
        验证数字输入
        
        Args:
            user_input: 用户输入
            min_value: 最小值
            max_value: 最大值
            field_name: 字段名称（用于错误消息）
        
        Returns:
            (is_valid, value, error_message)
        """
        # 1. 空值检查
        if not user_input or not user_input.strip():
            return False, None, f"{field_name}不能为空"
        
        user_input = user_input.strip()
        
        # 2. 数字检查
        if not user_input.isdigit():
            return False, None, f"{field_name}必须是数字"
        
        # 3. 范围检查
        try:
            value = int(user_input)
        except ValueError:
            return False, None, f"{field_name}格式错误"
        
        if value < min_value or value > max_value:
            return False, None, f"{field_name}必须在 {min_value}-{max_value} 之间"
        
        return True, value, ""
    
    @staticmethod
    def validate_text_input(
        user_input: str,
        max_length: int = 200,
        field_name: str = "输入"
    ) -> Tuple[bool, str]:
        """
        验证文本输入
        
        Args:
            user_input: 用户输入
            max_length: 最大长度
            field_name: 字段名称
        
        Returns:
            (is_valid, error_message)
        """
        # 1. 空值检查
        if not user_input or not user_input.strip():
            return False, f"{field_name}不能为空"
        
        user_input = user_input.strip()
        
        # 2. 长度检查
        if len(user_input) > max_length:
            return False, f"{field_name}过长（最大 {max_length} 字符）"
        
        # 3. XSS 检查（防止脚本注入）
        xss_patterns = [
            r'<script', r'javascript:', r'on\w+\s*=',
            r'document\.', r'window\.', r'eval\s*\('
        ]
        for pattern in xss_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, f"{field_name}包含危险字符"
        
        # 4. SQL 注入检查
        sql_patterns = [
            r"('\s*OR\s*'.*--)",
            r"('\s*AND\s*'.*--)",
            r";\s*DROP\s+",
            r";\s*DELETE\s+",
            r"UNION\s+SELECT"
        ]
        for pattern in sql_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return False, f"{field_name}包含危险字符"
        
        return True, ""
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        清理文件名（移除危险字符）
        
        Args:
            filename: 原始文件名
        
        Returns:
            安全的文件名
        """
        # 移除路径字符
        filename = filename.replace('/', '').replace('\\', '')
        
        # 移除 Windows 保留字符
        reserved_chars = '<>:"|?*'
        for char in reserved_chars:
            filename = filename.replace(char, '_')
        
        # 移除控制字符
        filename = ''.join(c for c in filename if ord(c) >= 32)
        
        # 限制长度
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:195] + ext
        
        # 如果清空了，使用默认名称
        if not filename:
            filename = "output"
        
        return filename
    
    @staticmethod
    def validate_provider_choice(
        user_input: str,
        available_providers: List[str]
    ) -> Tuple[bool, Optional[str], str]:
        """
        验证转写方案选择
        
        Args:
            user_input: 用户输入
            available_providers: 可用的方案列表
        
        Returns:
            (is_valid, provider_key, error_message)
        """
        # 1. 空值检查
        if not user_input or not user_input.strip():
            return False, None, "请输入选项"
        
        user_input = user_input.strip()
        
        # 2. 支持退出命令
        if user_input.lower() in ['q', 'exit', 'quit', '退出']:
            return False, None, "EXIT"
        
        # 3. 数字检查
        if not user_input.isdigit():
            return False, None, "请输入数字选项"
        
        # 4. 范围检查
        try:
            value = int(user_input)
        except ValueError:
            return False, None, "选项格式错误"
        
        if value < 1 or value > len(available_providers):
            return False, None, f"请输入 1-{len(available_providers)} 之间的数字"
        
        return True, available_providers[value - 1], ""
    
    @staticmethod
    def validate_output_dir(output_dir: str) -> Tuple[bool, str]:
        """
        验证输出目录
        
        Args:
            output_dir: 输出目录路径
        
        Returns:
            (is_valid, error_message)
        """
        # 1. 空值检查
        if not output_dir or not output_dir.strip():
            return False, "输出目录不能为空"
        
        output_dir = output_dir.strip()
        
        # 2. 路径穿越攻击检查
        for pattern in InputValidator.DANGEROUS_PATH_PATTERNS:
            if re.search(pattern, output_dir, re.IGNORECASE):
                return False, f"路径包含危险字符：{pattern}"
        
        # 3. 长度限制
        if len(output_dir) > 260:
            return False, "路径过长（最大 260 字符）"
        
        # 4. 转换为 Path 对象
        try:
            output_path = Path(output_dir)
        except Exception as e:
            return False, f"无效路径格式：{e}"
        
        # 5. 尝试创建目录（检查写权限）
        try:
            output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            return False, f"无法创建目录：{e}"
        
        # 6. 检查写权限
        if not os.access(output_dir, os.W_OK):
            return False, f"目录不可写：{output_dir}"
        
        return True, ""


# 使用示例
if __name__ == "__main__":
    print("🔒 输入验证工具测试\n")
    
    # 测试 1: 音频路径验证
    print("测试 1: 音频路径验证")
    test_paths = [
        "valid.mp3",
        "../etc/passwd",  # 路径穿越
        "test.txt",  # 不支持的格式
        "x" * 300,  # 路径过长
    ]
    
    for path in test_paths:
        is_valid, error = InputValidator.validate_audio_path(path)
        status = "✅" if is_valid else "❌"
        print(f"   {status} {path[:50]}: {error or 'Valid'}")
    
    # 测试 2: 数字输入验证
    print("\n测试 2: 数字输入验证")
    test_numbers = [
        ("5", 1, 10),
        ("0", 1, 10),  # 超出范围
        ("abc", 1, 10),  # 非数字
        ("", 1, 10),  # 空值
    ]
    
    for num, min_val, max_val in test_numbers:
        is_valid, value, error = InputValidator.validate_numeric_input(num, min_val, max_val)
        status = "✅" if is_valid else "❌"
        print(f"   {status} '{num}': {error or f'Valid ({value})'}")
    
    # 测试 3: 文本输入验证
    print("\n测试 3: 文本输入验证")
    test_texts = [
        "正常文本",
        "<script>alert('xss')</script>",  # XSS
        "x" * 300,  # 过长
    ]
    
    for text in test_texts:
        is_valid, error = InputValidator.validate_text_input(text[:50])
        status = "✅" if is_valid else "❌"
        print(f"   {status} '{text[:30]}...': {error or 'Valid'}")
    
    print("\n✅ 所有测试完成")
