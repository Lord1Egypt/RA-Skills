#!/usr/bin/env python3
"""
PDF 水印添加工具 - 智能版
根据页面长宽比自动调整水印角度和位置
"""

import sys
import os
import math
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO


# 注册中文字体
CHINESE_FONTS = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/simhei.ttf",
    "C:/Windows/Fonts/simsun.ttc",
    "C:/Windows/Fonts/msyh.ttc",
]


def register_chinese_font():
    """注册中文字体"""
    for font_path in CHINESE_FONTS:
        if os.path.exists(font_path):
            try:
                font_name = os.path.basename(font_path).split('.')[0]
                pdfmetrics.registerFont(TTFont(font_name, font_path))
                return font_name
            except:
                continue
    return "Helvetica"


def calculate_smart_angle(width, height):
    """
    根据页面长宽比智能计算水印角度
    
    竖版页面 (height > width): 斜向30-45度
    横版页面 (width > height): 根据宽高比调整
    正方形: 水平或45度
    """
    aspect_ratio = width / height
    
    if aspect_ratio < 0.8:  # 明显竖版 (如 A4 竖版 0.707)
        return 30  # 较平缓的斜角
    elif aspect_ratio > 1.3:  # 明显横版
        return 25  # 更平缓，适合宽屏
    else:
        return 35  # 接近正方形，中等角度


def calculate_font_size(width, height, base_size=42):
    """
    根据页面尺寸智能调整字体大小
    确保水印不会太大或太小
    """
    # 使用对角线的比例来调整字体
    diagonal = math.sqrt(width**2 + height**2)
    # A4 纸对角线约 842 点
    reference_diagonal = 842
    scale_factor = diagonal / reference_diagonal
    
    # 限制缩放范围
    adjusted_size = int(base_size * scale_factor)
    return max(28, min(60, adjusted_size))  # 限制在 28-60 之间


def create_watermark(text, font_name, page_width, page_height, 
                     angle=None, opacity=0.25, font_size=None, 
                     color=(100, 100, 100), multi_line=False):
    """
    创建智能水印
    
    参数:
        angle: 如果为None则自动计算
        font_size: 如果为None则自动计算
        multi_line: 是否多行显示（长文本自动换行）
    """
    # 自动计算角度
    if angle is None:
        angle = calculate_smart_angle(page_width, page_height)
    
    # 自动计算字体大小
    if font_size is None:
        font_size = calculate_font_size(page_width, page_height)
    
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))
    
    # 设置颜色
    c.setStrokeColorRGB(*[c/255 for c in color], alpha=opacity)
    c.setFillColorRGB(*[c/255 for c in color], alpha=opacity)
    c.setFont(font_name, font_size)
    
    # 计算页面中心
    center_x = page_width / 2
    center_y = page_height / 2
    
    # 保存状态并绘制
    c.saveState()
    c.translate(center_x, center_y)
    c.rotate(angle)
    
    # 绘制文字
    if multi_line and '\n' in text:
        lines = text.split('\n')
        line_height = font_size * 1.3
        total_height = len(lines) * line_height
        start_y = total_height / 2 - line_height / 2
        
        for i, line in enumerate(lines):
            y = start_y - i * line_height
            c.drawCentredString(0, y, line)
    else:
        c.drawCentredString(0, 0, text)
    
    c.restoreState()
    c.save()
    packet.seek(0)
    
    return packet


def add_watermark_to_pdf(input_path, output_path, watermark_text, 
                         angle=None, opacity=0.25, font_size=None):
    """
    智能添加水印到 PDF
    
    参数:
        angle: None=自动, 或指定角度
        font_size: None=自动, 或指定大小
    """
    font_name = register_chinese_font()
    reader = PdfReader(input_path)
    writer = PdfWriter()
    
    print(f"📄 正在处理 {len(reader.pages)} 页...")
    
    for page_num, page in enumerate(reader.pages):
        # 获取页面尺寸
        page_box = page.mediabox
        page_width = float(page_box.width)
        page_height = float(page_box.height)
        
        # 检测页面方向
        aspect = page_width / page_height
        orientation = "竖版" if aspect < 0.9 else ("横版" if aspect > 1.1 else "方版")
        
        # 创建水印
        watermark_buffer = create_watermark(
            watermark_text, font_name, page_width, page_height,
            angle, opacity, font_size
        )
        
        watermark_reader = PdfReader(watermark_buffer)
        watermark_page = watermark_reader.pages[0]
        
        # 合并
        page.merge_page(watermark_page)
        writer.add_page(page)
        
        # 第一页显示信息
        if page_num == 0:
            actual_angle = angle if angle else calculate_smart_angle(page_width, page_height)
            actual_size = font_size if font_size else calculate_font_size(page_width, page_height)
            print(f"  📐 页面尺寸: {page_width:.0f} x {page_height:.0f} ({orientation})")
            print(f"  📝 水印角度: {actual_angle}°, 字体: {actual_size}px")
        
        if (page_num + 1) % 10 == 0 or page_num == len(reader.pages) - 1:
            print(f"  进度: {page_num + 1}/{len(reader.pages)} 页")
    
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"✅ 完成！输出: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("智能 PDF 水印工具")
        print("用法: python add_pdf_watermark.py <输入PDF> <水印文字> [输出PDF] [角度] [透明度] [字体大小]")
        print("")
        print("参数说明:")
        print("  角度: 默认自动根据页面长宽比计算")
        print("  透明度: 0.0-1.0, 默认 0.25")
        print("  字体大小: 默认自动根据页面尺寸计算")
        print("")
        print("示例:")
        print("  全自动: python add_pdf_watermark.py doc.pdf '机密' doc_watermarked.pdf")
        print("  自定义: python add_pdf_watermark.py doc.pdf '机密' doc.pdf 30 0.3 40")
        sys.exit(1)
    
    input_file = sys.argv[1]
    watermark_text = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else input_file.replace('.pdf', '_watermarked.pdf')
    
    # 解析参数，支持 "auto" 表示自动
    angle_arg = sys.argv[4] if len(sys.argv) > 4 else "auto"
    angle = None if angle_arg.lower() == "auto" else int(angle_arg)
    
    opacity = float(sys.argv[5]) if len(sys.argv) > 5 else 0.25
    
    size_arg = sys.argv[6] if len(sys.argv) > 6 else "auto"
    font_size = None if size_arg.lower() == "auto" else int(size_arg)
    
    if not os.path.exists(input_file):
        print(f"❌ 错误: 文件不存在 - {input_file}")
        sys.exit(1)
    
    add_watermark_to_pdf(input_file, output_file, watermark_text, angle, opacity, font_size)
