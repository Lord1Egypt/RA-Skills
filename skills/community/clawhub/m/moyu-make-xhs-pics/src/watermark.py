"""
水印处理模块
"""

import random
from pathlib import Path
from typing import Optional

# 安装 Pillow: pip install Pillow
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow not installed, watermark will not be added")

# 水印文字
WATERMARK_TEXT = "AI 生成"

# 字体路径
FONT_PATHS = [
    "/System/Library/Fonts/STHeiti Medium.ttc",  # 黑体
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Helvetica.ttc",
]


def get_font(size: int):
    """获取字体"""
    for font_path in FONT_PATHS:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    return ImageFont.load_default()


def add_watermark(
    image_path: str,
    text: str = WATERMARK_TEXT,
    position: Optional[str] = None
) -> str:
    """
    添加水印
    
    Args:
        image_path: 图片路径
        text: 水印文字
        position: 位置 ("left_bottom", "right_bottom", None=随机)
    
    Returns:
        处理后的图片路径
    """
    if not HAS_PIL:
        return image_path
    
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        width, height = img.size
        font_size = max(16, width // 30)
        font = get_font(font_size)
        
        # 获取文字尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 计算位置
        padding = 20
        
        if position is None:
            position = random.choice(["left_bottom", "right_bottom"])
        
        if position == "left_bottom":
            x = padding
            y = height - text_height - padding
        else:  # right_bottom
            x = width - text_width - padding
            y = height - text_height - padding
        
        # 绘制文字（带阴影效果）
        shadow_color = (0, 0, 0)
        text_color = (255, 255, 255)
        
        # 阴影
        draw.text((x + 2, y + 2), text, fill=shadow_color, font=font)
        # 文字
        draw.text((x, y), text, fill=text_color, font=font)
        
        # 保存
        img.save(image_path)
        return image_path
        
    except Exception as e:
        print(f"添加水印失败: {e}")
        return image_path
