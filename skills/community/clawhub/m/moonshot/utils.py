#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工具函数模块
"""

import os
import mimetypes
from typing import Optional, Tuple
from PIL import Image
import io


def validate_image_file(image_path: str) -> Tuple[bool, Optional[str]]:
    """
    验证图片文件

    Args:
        image_path: 图片文件路径

    Returns:
        (是否有效, 错误信息)
    """
    if not os.path.exists(image_path):
        return False, f"文件不存在: {image_path}"

    if not os.path.isfile(image_path):
        return False, f"路径不是文件: {image_path}"

    # 检查文件大小
    file_size = os.path.getsize(image_path)
    if file_size > 10 * 1024 * 1024:  # 10MB
        return False, f"文件过大: {file_size / 1024 / 1024:.2f}MB (最大 10MB)"

    # 检查文件类型
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type not in ['image/jpeg', 'image/png', 'image/webp', 'image/jpg']:
        return False, f"不支持的文件类型: {mime_type}"

    # 验证图片内容
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True, None
    except Exception as e:
        return False, f"无效的图片文件: {str(e)}"


def get_image_info(image_path: str) -> dict:
    """
    获取图片信息

    Args:
        image_path: 图片文件路径

    Returns:
        图片信息字典
    """
    try:
        with Image.open(image_path) as img:
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'file_size': os.path.getsize(image_path)
            }
    except Exception as e:
        return {'error': str(e)}


def resize_image(
    image_path: str,
    max_width: int = 1920,
    max_height: int = 1080,
    output_path: Optional[str] = None
) -> str:
    """
    调整图片大小

    Args:
        image_path: 图片文件路径
        max_width: 最大宽度
        max_height: 最大高度
        output_path: 输出路径（默认覆盖原文件）

    Returns:
        处理后的图片路径
    """
    try:
        with Image.open(image_path) as img:
            # 计算新尺寸
            img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

            # 保存图片
            output = output_path or image_path
            img.save(output, optimize=True, quality=95)

            return output
    except Exception as e:
        raise RuntimeError(f"图片处理失败: {str(e)}")


def convert_to_png(image_path: str, output_path: Optional[str] = None) -> str:
    """
    转换图片为 PNG 格式

    Args:
        image_path: 图片文件路径
        output_path: 输出路径

    Returns:
        转换后的图片路径
    """
    try:
        with Image.open(image_path) as img:
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')

            output = output_path or os.path.splitext(image_path)[0] + '.png'
            img.save(output, 'PNG')

            return output
    except Exception as e:
        raise RuntimeError(f"图片转换失败: {str(e)}")


def estimate_tokens(text: str) -> int:
    """
    估算文本的 token 数量

    Args:
        text: 输入文本

    Returns:
        估算的 token 数量
    """
    # 简单估算：中文约 1.5 字符/token，英文约 4 字符/token
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    english_chars = len(text) - chinese_chars

    tokens = int(chinese_chars / 1.5 + english_chars / 4)
    return tokens


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小

    Args:
        size_bytes: 字节数

    Returns:
        格式化后的大小字符串
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的文件名
    """
    # 移除或替换非法字符
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')

    # 移除前后空格
    filename = filename.strip()

    # 限制长度
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255 - len(ext)] + ext

    return filename


def create_output_directory(base_path: str, subdir: str = "output") -> str:
    """
    创建输出目录

    Args:
        base_path: 基础路径
        subdir: 子目录名称

    Returns:
        创建的目录路径
    """
    output_dir = os.path.join(base_path, subdir)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def parse_model_version(model_string: str) -> str:
    """
    解析模型版本字符串

    Args:
        model_string: 模型字符串

    Returns:
        标准化的模型名称
    """
    model_mapping = {
        '': '',
        '': '',
        '': '',
        '': '',
        '': '',
        '': ''
    }

    return model_mapping.get(model_string.lower(), model_string)


def batch_process_images(
    image_paths: list,
    process_func,
    desc: str = "处理中"
) -> list:
    """
    批量处理图片

    Args:
        image_paths: 图片路径列表
        process_func: 处理函数
        desc: 描述信息

    Returns:
        处理结果列表
    """
    from tqdm import tqdm

    results = []
    errors = []

    for image_path in tqdm(image_paths, desc=desc):
        try:
            result = process_func(image_path)
            results.append((image_path, result, None))
        except Exception as e:
            errors.append((image_path, str(e)))
            results.append((image_path, None, str(e)))

    return results


def generate_summary(results: list) -> dict:
    """
    生成批处理结果摘要

    Args:
        results: 处理结果列表

    Returns:
        摘要字典
    """
    total = len(results)
    success = sum(1 for _, _, error in results if error is None)
    failed = total - success

    return {
        'total': total,
        'success': success,
        'failed': failed,
        'success_rate': success / total if total > 0 else 0
    }


def load_prompt_template(template_name: str) -> Optional[str]:
    """
    加载提示词模板

    Args:
        template_name: 模板名称

    Returns:
        模板内容或 None
    """
    template_dir = os.path.join(os.path.dirname(__file__), 'prompts')
    template_path = os.path.join(template_dir, f"{template_name}.md")

    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()

    return None


def format_error_message(error: Exception, context: str = "") -> str:
    """
    格式化错误消息

    Args:
        error: 异常对象
        context: 上下文信息

    Returns:
        格式化的错误消息
    """
    error_type = type(error).__name__
    error_msg = str(error)

    if context:
        return f"[{error_type}] {context}: {error_msg}"
    else:
        return f"[{error_type}] {error_msg}"


if __name__ == '__main__':
    # 测试代码
    print("工具函数模块")
    print(f"Token 估算测试: {estimate_tokens('这是一个测试文本')}")
    print(f"文件大小格式化: {format_file_size(1024 * 1024 * 5)}")
    print(f"文件名清理: {sanitize_filename('test<>file?.txt')}")
