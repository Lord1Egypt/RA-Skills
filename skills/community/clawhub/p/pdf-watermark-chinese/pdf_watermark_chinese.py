#!/usr/bin/env python3
"""
PDF 水印处理工具 - 中文增强版
支持添加文本水印、图像水印和移除水印
"""

import os
import sys
import argparse
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
import io
import tempfile

class PDFWatermark:
    """PDF 水印处理类"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.image_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    
    def add_text_watermark(self, input_pdf, output_pdf, text, 
                          font_size=40, color=(0.5, 0.5, 0.5), 
                          alpha=0.3, rotation=45, position='center'):
        """
        添加文本水印到PDF
        
        参数:
            input_pdf: 输入PDF文件路径
            output_pdf: 输出PDF文件路径
            text: 水印文字
            font_size: 字体大小
            color: RGB颜色元组 (0-1)
            alpha: 透明度 (0-1)
            rotation: 旋转角度
            position: 位置 ('center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'diagonal')
        """
        try:
            reader = PdfReader(input_pdf)
            writer = PdfWriter()
            
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                
                # 获取页面尺寸
                page_width = float(page.mediabox.width)
                page_height = float(page.mediabox.height)
                
                # 创建水印
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(page_width, page_height))
                
                # 检测是否需要中文字体
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
                
                if has_chinese:
                    # 使用UTF-8编码和reportlab的中文字体支持
                    # 尝试使用系统字体，如果失败则回退到Helvetica
                    try:
                        # 注册中文字体（如果可用）
                        from reportlab.pdfbase import pdfmetrics
                        from reportlab.pdfbase.ttfonts import TTFont
                        
                        # 尝试使用常见的中文字体文件
                        font_files = [
                            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
                            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
                        ]
                        
                        registered = False
                        for font_file in font_files:
                            if os.path.exists(font_file):
                                try:
                                    # 使用fontconfig来获取字体名
                                    font_name = "ChineseFont"
                                    pdfmetrics.registerFont(TTFont(font_name, font_file))
                                    can.setFont(font_name, font_size)
                                    registered = True
                                    print(f"✓ 使用中文字体: {font_file}")
                                    break
                                except Exception as e:
                                    print(f"✗ 无法加载字体 {font_file}: {e}")
                        
                        if not registered:
                            # 回退到Helvetica
                            can.setFont("Helvetica", font_size)
                            print("✓ 回退到Helvetica字体")
                    except Exception:
                        can.setFont("Helvetica", font_size)
                        print("✓ 回退到Helvetica字体")
                else:
                    can.setFont("Helvetica", font_size)
                
                can.setFillColorRGB(color[0], color[1], color[2], alpha=alpha)
                can.rotate(rotation)
                
                # 根据位置设置水印坐标
                if position == 'center':
                    x, y = page_width/2 - 100, page_height/2
                elif position == 'top-left':
                    x, y = 50, page_height - 100
                elif position == 'top-right':
                    x, y = page_width - 300, page_height - 100
                elif position == 'bottom-left':
                    x, y = 50, 100
                elif position == 'bottom-right':
                    x, y = page_width - 300, 100
                else:  # diagonal - 平铺
                    # 平铺水印
                    for i in range(0, int(page_width), 300):
                        for j in range(0, int(page_height), 200):
                            can.drawString(i, j, text)
                    x, y = 0, 0  # 不需要单独绘制
                
                if position != 'diagonal':
                    can.drawString(x, y, text)
                
                can.save()
                
                # 合并水印
                packet.seek(0)
                watermark = PdfReader(packet)
                watermark_page = watermark.pages[0]
                page.merge_page(watermark_page)
                writer.add_page(page)
            
            # 保存输出文件
            with open(output_pdf, "wb") as output_file:
                writer.write(output_file)
            
            return True, f"成功添加文本水印到 {output_pdf}"
            
        except Exception as e:
            return False, f"添加文本水印失败: {str(e)}"

def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description='PDF 水印处理工具')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 添加文本水印命令
    text_parser = subparsers.add_parser('text', help='添加文本水印')
    text_parser.add_argument('input', help='输入PDF文件')
    text_parser.add_argument('output', help='输出PDF文件')
    text_parser.add_argument('--text', required=True, help='水印文字')
    text_parser.add_argument('--font-size', type=int, default=40, help='字体大小')
    text_parser.add_argument('--color', default='0.5,0.5,0.5', help='RGB颜色 (0-1), 格式: r,g,b')
    text_parser.add_argument('--alpha', type=float, default=0.3, help='透明度 (0-1)')
    text_parser.add_argument('--rotation', type=int, default=45, help='旋转角度')
    text_parser.add_argument('--position', default='center', 
                           choices=['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right', 'diagonal'],
                           help='水印位置')
    
    args = parser.parse_args()
    
    watermark = PDFWatermark()
    
    if args.command == 'text':
        # 解析颜色
        color = tuple(map(float, args.color.split(',')))
        success, message = watermark.add_text_watermark(
            args.input, args.output, args.text,
            font_size=args.font_size, color=color,
            alpha=args.alpha, rotation=args.rotation,
            position=args.position
        )
        print(message)
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()