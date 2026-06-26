#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体加载器 — Font Loader Module
================================

功能：
- 自动查找系统可用的中文字体
- 支持字体回退链（三级优先级）
- 跨平台支持（macOS / Linux / Windows）

字体优先级：
1. Bundle 字体（技能目录下fonts/）
2. 系统中文字体（黑体/苹方/微软雅黑）
3. 英文保底字体（DejaVu Sans）

用法：
    from font_loader import get_font, get_text_bbox, draw_centered_text
    
    font = get_font(size=20)  # 自动选择可用字体
"""

import os
import platform
from PIL import ImageFont

# ===================== 字体路径配置 =====================

# 获取技能目录路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)

# 第1级：Bundle 字体（打包在技能目录下）
BUNDLE_FONTS = [
    os.path.join(SKILL_ROOT, 'fonts', 'STHeiti Medium.ttc'),  # macOS 黑体
    os.path.join(SKILL_ROOT, 'fonts', 'SourceHanSansSC-Bold.otf'),  # 思源黑体
]

# 第2级：macOS 系统字体
MACOS_FONTS = [
    '/System/Library/Fonts/STHeiti.ttc',  # 华文黑体
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/PingFang.ttc',  # 苹方
    '/System/Library/Fonts/Hiragino Sans GB.ttc',  # 冬青黑体
    '/Library/Fonts/Heiti.ttc',
]

# 第2级：Linux 系统字体
LINUX_FONTS = [
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
    '/usr/share/fonts/truetype/arphic/uming.ttc',
    '/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc',
    '/usr/share/fonts/google-noto-cjk/NotoSansCJK-Bold.ttc',
]

# 第2级：Windows 系统字体
WINDOWS_FONTS = [
    'C:/Windows/Fonts/msyh.ttc',  # 微软雅黑
    'C:/Windows/Fonts/simhei.ttf',  # 黑体
    'C:/Windows/Fonts/SourceHanSansCN-Bold.otf',
]

# 第3级：英文保底
ENGLISH_FONTS = [
    'DejaVu Sans',
    'Arial',
    'Helvetica',
]

# ===================== 全局字体缓存 =====================

_font_cache = {}

# ===================== 字体查找函数 =====================

def find_chinese_font():
    """
    自动查找系统中可用的中文字体（三级回退）
    
    Returns:
        str: 可用的中文字体路径，如果都没找到返回 None
    """
    # 根据操作系统选择搜索路径
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        search_order = BUNDLE_FONTS + MACOS_FONTS
    elif system == 'Linux':
        search_order = BUNDLE_FONTS + LINUX_FONTS
    elif system == 'Windows':
        search_order = BUNDLE_FONTS + WINDOWS_FONTS
    else:
        search_order = BUNDLE_FONTS
    
    # 遍历查找
    for path in search_order:
        if path and os.path.exists(path):
            print(f"[font_loader] 找到中文字体: {path}")
            return path
    
    print("[font_loader] ⚠️ 未找到中文字体，将使用英文保底字体")
    return None


def get_font(size=20, bold=False):
    """
    获取字体对象（带缓存）
    
    Args:
        size: 字体大小
        bold: 是否使用粗体（如果 Bundle 字体有多个 weight）
    
    Returns:
        ImageFont.FreeTypeFont: PIL 字体对象
    """
    cache_key = f"{size}_{bold}"
    
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    # 尝试加载中文字体
    chinese_font_path = find_chinese_font()
    
    try:
        if chinese_font_path:
            font = ImageFont.truetype(chinese_font_path, size)
            _font_cache[cache_key] = font
            print(f"[font_loader] ✅ 字体加载成功: {size}px")
            return font
    except Exception as e:
        print(f"[font_loader] ⚠️ 中文字体加载失败: {e}")
    
    # 回退到英文默认字体
    try:
        font = ImageFont.load_default()
        _font_cache[cache_key] = font
        print(f"[font_loader] ⚠️ 使用系统默认字体（可能显示不正常）")
        return font
    except Exception as e:
        print(f"[font_loader] ❌ 默认字体加载失败: {e}")
        raise e


def get_text_bbox(text, font):
    """
    获取文字边界框
    
    Args:
        text: 文字内容
        font: ImageFont 对象
    
    Returns:
        tuple: (left, top, right, bottom)
    """
    try:
        return font.getbbox(text)
    except Exception:
        # 有些字体不支持 getbbox，使用替代方法
        width = int(len(text) * font.size * 0.6)  # 估算宽度
        height = font.size
        return (0, 0, width, height)


def draw_centered_text(draw, pos, text, font, fill):
    """
    在指定位置居中绘制文字
    
    Args:
        draw: ImageDraw 对象
        pos: 位置 (x, y) 中心点
        text: 文字内容
        font: ImageFont 对象
        fill: 填充颜色
    """
    bbox = get_text_bbox(text, font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = pos[0] - text_width // 2
    y = pos[1] - text_height // 2
    
    draw.text((x, y), text, fill=fill, font=font)


def draw_left_text(draw, pos, text, font, fill):
    """
    在指定位置左对齐绘制文字
    
    Args:
        draw: ImageDraw 对象
        pos: 位置 (x, y) 左上点
        text: 文字内容
        font: ImageFont 对象
        fill: 填充颜色
    """
    draw.text(pos, text, fill=fill, font=font)


def clear_cache():
    """清空字体缓存（用于测试或切换字体）"""
    global _font_cache
    _font_cache = {}
    print("[font_loader] 字体缓存已清空")


# ===================== 测试代码 =====================

if __name__ == '__main__':
    print("=== 字体加载器测试 ===")
    print(f"操作系统: {platform.system()}")
    print(f"技能根目录: {SKILL_ROOT}")
    
    # 检查 Bundle 字体
    print("\nBundle 字体检查:")
    for f in BUNDLE_FONTS:
        exists = "✅" if os.path.exists(f) else "❌"
        print(f"  {exists} {f}")
    
    # 测试获取字体
    font = get_font(size=24)
    print(f"\n✅ 字体加载成功")
    
    # 测试文字边界
    bbox = get_text_bbox('反应温度 80°C', font)
    print(f"   文字边界: {bbox}")
    
    # 测试绘制
    from PIL import Image
    img = Image.new('RGBA', (800, 100), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    draw_centered_text(d, (400, 50), '反应温度 80°C', font, (0, 0, 0, 255))
    img.save('/tmp/font_loader_test.png')
    print(f"   绘制测试成功: /tmp/font_loader_test.png")
