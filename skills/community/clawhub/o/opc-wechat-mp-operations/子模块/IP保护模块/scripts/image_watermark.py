#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片水印脚本 - 为图片添加半透明水印

使用方法:
    python image_watermark.py --input image.jpg --output image_marked.jpg --text "老胡说"
    python image_watermark.py --input ./images/ --output ./output/ --text "老胡说" --opacity 0.5
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ 错误：需要安装 Pillow 库")
    print("请运行: pip install Pillow")
    sys.exit(1)


# 默认配置
DEFAULT_CONFIG = {
    "text": "老胡说",
    "position": "bottom_right",
    "opacity": 0.5,
    "font_size": 24,
    "padding": 20,
    "font_family": "Microsoft YaHei",
    "text_color": (255, 255, 255),
    "bg_color": (0, 0, 0, 128),
    "border_radius": 8,
    "add_background": True,
}


def get_font(font_size, font_family=None):
    """获取字体对象"""
    # 尝试加载指定字体，失败则使用默认字体
    if font_family:
        try:
            return ImageFont.truetype(font_family, font_size)
        except:
            pass
    
    # 常见中文字体路径
    font_paths = [
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "C:/Windows/Fonts/msyh.ttc",
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                return ImageFont.truetype(font_path, font_size)
            except:
                continue
    
    # 最后使用默认字体
    return ImageFont.load_default()


def calculate_position(img_width, img_height, text_width, text_height, padding, position):
    """计算水印位置"""
    positions = {
        "top_left": (padding, padding),
        "top_right": (img_width - text_width - padding, padding),
        "bottom_left": (padding, img_height - text_height - padding),
        "bottom_right": (img_width - text_width - padding, img_height - text_height - padding),
        "center": ((img_width - text_width) // 2, (img_height - text_height) // 2),
    }
    
    return positions.get(position, positions["bottom_right"])


def create_rounded_rectangle(draw, xy, radius, fill):
    """创建圆角矩形"""
    x1, y1, x2, y2 = xy
    
    # 绘制主体矩形
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    
    # 绘制四个圆角
    draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
    draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)


def add_image_watermark(image_path, output_path, config=None):
    """
    为单张图片添加水印
    
    Args:
        image_path: 输入图片路径
        output_path: 输出图片路径
        config: 配置字典
    
    Returns:
        bool: 是否成功
    """
    if config is None:
        config = DEFAULT_CONFIG
    
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 转换为 RGBA 模式
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 创建可绘制的图层
        overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)
        
        # 获取配置
        text = config.get("text", DEFAULT_CONFIG["text"])
        position = config.get("position", DEFAULT_CONFIG["position"])
        opacity = config.get("opacity", DEFAULT_CONFIG["opacity"])
        font_size = config.get("font_size", DEFAULT_CONFIG["font_size"])
        padding = config.get("padding", DEFAULT_CONFIG["padding"])
        font_family = config.get("font_family", DEFAULT_CONFIG["font_family"])
        add_bg = config.get("add_background", DEFAULT_CONFIG["add_background"])
        border_radius = config.get("border_radius", DEFAULT_CONFIG["border_radius"])
        
        # 根据图片尺寸调整字体大小
        img_width, img_height = img.size
        if img_width < 800:
            font_size = min(font_size, 16)
        elif img_width < 1200:
            font_size = min(font_size, 24)
        elif img_width < 2000:
            font_size = min(font_size, 32)
        else:
            font_size = min(font_size, 40)
        
        # 获取字体
        font = get_font(font_size, font_family)
        
        # 计算文字尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 计算水印位置
        x, y = calculate_position(img_width, img_height, text_width, text_height, padding, position)
        
        # 绘制背景和文字
        if add_bg:
            # 圆角矩形背景
            bg_padding = 12
            bg_xy = (
                x - bg_padding,
                y - bg_padding,
                x + text_width + bg_padding,
                y + text_height + bg_padding
            )
            
            # 半透明背景
            bg_color = (0, 0, 0, int(255 * opacity * 0.6))
            create_rounded_rectangle(draw, bg_xy, border_radius, bg_color)
        
        # 绘制文字
        text_color = (255, 255, 255, int(255 * opacity))
        draw.text((x, y), text, font=font, fill=text_color)
        
        # 合并图层
        watermarked = Image.alpha_composite(img, overlay)
        
        # 转换为 RGB 模式保存（去除Alpha通道）
        if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
            watermarked = watermarked.convert('RGB')
        
        # 保存
        watermarked.save(output_path, quality=95)
        
        return True
        
    except Exception as e:
        print(f"❌ 处理失败 {image_path}: {e}")
        return False


def process_file(input_path, output_path, config):
    """处理单个文件"""
    success = add_image_watermark(input_path, output_path, config)
    if success:
        print(f"✅ {input_path} → {output_path}")


def batch_process(input_dir, output_dir, config):
    """批量处理目录下的所有图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图片格式
    extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.webp']
    
    count = 0
    for filename in os.listdir(input_dir):
        ext = os.path.splitext(filename)[1].lower()
        if ext in extensions:
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            process_file(input_path, output_path, config)
            count += 1
    
    print(f"\n处理完成：{count} 张图片")


def main():
    parser = argparse.ArgumentParser(description='为图片添加水印')
    parser.add_argument('--input', '-i', required=True, help='输入图片或目录路径')
    parser.add_argument('--output', '-o', required=True, help='输出图片或目录路径')
    parser.add_argument('--text', '-t', default='老胡说', help='水印文字')
    parser.add_argument('--position', '-p', default='bottom_right', 
                        choices=['top_left', 'top_right', 'bottom_left', 'bottom_right', 'center'],
                        help='水印位置')
    parser.add_argument('--opacity', '-o', type=float, default=0.5, help='透明度 (0.0-1.0)')
    parser.add_argument('--font-size', '-s', type=int, default=24, help='字体大小')
    parser.add_argument('--padding', type=int, default=20, help='边距')
    parser.add_argument('--no-bg', action='store_true', help='不添加背景')
    
    args = parser.parse_args()
    
    # 构建配置
    config = {
        "text": args.text,
        "position": args.position,
        "opacity": args.opacity,
        "font_size": args.font_size,
        "padding": args.padding,
        "add_background": not args.no_bg,
    }
    
    # 判断输入是文件还是目录
    if os.path.isfile(args.input):
        add_image_watermark(args.input, args.output, config)
    elif os.path.isdir(args.input):
        batch_process(args.input, args.output, config)
    else:
        print(f"❌ 错误：找不到文件或目录 {args.input}")


if __name__ == '__main__':
    main()
