#!/usr/bin/env python3
"""
PDF 水印处理工具
支持添加文本水印、图像水印和移除水印
支持中文字体
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
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import tempfile
import subprocess

class PDFWatermark:
    """PDF 水印处理类"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
        self.image_formats = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
        self.chinese_fonts = self._detect_chinese_fonts()
    
    def _detect_chinese_fonts(self):
        """检测系统中可用的中文字体"""
        chinese_fonts = {}
        
        # 常见中文字体路径
        common_font_paths = [
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 文泉驿正黑
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',  # 文泉驿微米黑
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Noto Sans CJK
            '/usr/share/fonts/truetype/arphic/uming.ttc',  # AR PL UMing
            '/usr/share/fonts/truetype/arphic/ukai.ttc',   # AR PL UKai
            '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Droid Sans Fallback
        ]
        
        # 通过fc-list查找中文字体
        try:
            result = subprocess.run(['fc-list', ':lang=zh'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if ':' in line:
                        font_path = line.split(':')[0].strip()
                        if os.path.exists(font_path):
                            font_name = os.path.basename(font_path)
                            chinese_fonts[font_name] = font_path
        except:
            pass
        
        # 检查常见字体路径
        for font_path in common_font_paths:
            if os.path.exists(font_path):
                font_name = os.path.basename(font_path)
                chinese_fonts[font_name] = font_path
        
        # 默认字体映射
        default_mapping = {
            'simsun': '宋体',
            'simhei': '黑体',
            'simkai': '楷体',
            'simfang': '仿宋',
            'wqy-zenhei': '文泉驿正黑',
            'wqy-microhei': '文泉驿微米黑',
            'notosanscjk': 'Noto Sans CJK',
            'uming': 'AR PL UMing',
            'ukai': 'AR PL UKai',
            'droidsansfallback': 'Droid Sans Fallback'
        }
        
        # 添加友好名称
        friendly_fonts = {}
        for font_name, font_path in chinese_fonts.items():
            for key, friendly_name in default_mapping.items():
                if key in font_name.lower():
                    friendly_fonts[friendly_name] = font_path
                    break
            else:
                friendly_fonts[font_name] = font_path
        
        return friendly_fonts
    
    def _register_chinese_font(self, font_name=None):
        """注册中文字体到reportlab"""
        if not font_name:
            # 使用第一个可用的中文字体
            if self.chinese_fonts:
                font_name = list(self.chinese_fonts.keys())[0]
                font_path = self.chinese_fonts[font_name]
            else:
                return "Helvetica"  # 回退到英文字体
        
        if font_name in self.chinese_fonts:
            try:
                # 注册字体
                pdfmetrics.registerFont(TTFont(font_name, self.chinese_fonts[font_name]))
                return font_name
            except Exception as e:
                print(f"警告: 无法注册字体 {font_name}: {e}")
                return "Helvetica"
        else:
            # 检查是否是系统默认字体
            if font_name in ["Helvetica", "Times-Roman", "Courier"]:
                return font_name
            else:
                return "Helvetica"
    
    def add_text_watermark(self, input_pdf, output_pdf, text, 
                          font_size=40, color=(0.5, 0.5, 0.5), 
                          alpha=0.3, rotation=45, position='center',
                          font_name=None):
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
            font_name: 字体名称，支持中文字体名称如'文泉驿正黑'、'黑体'等
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
                
                # 设置水印样式
                # 检测是否需要中文字体（检查文本是否包含中文字符）
                has_chinese = any('\u4e00' <= char <= '\u9fff' for char in text)
                
                if has_chinese or font_name:
                    # 使用中文字体
                    actual_font_name = self._register_chinese_font(font_name)
                    can.setFont(actual_font_name, font_size)
                    print(f"使用字体: {actual_font_name} (中文文本: {text})")
                else:
                    # 使用英文字体
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
    
    def add_image_watermark(self, input_pdf, output_pdf, image_path,
                           scale=0.2, alpha=0.3, position='center'):
        """
        添加图像水印到PDF
        
        参数:
            input_pdf: 输入PDF文件路径
            output_pdf: 输出PDF文件路径
            image_path: 图像文件路径
            scale: 图像缩放比例
            alpha: 透明度 (0-1)
            position: 位置 ('center', 'top-left', 'top-right', 'bottom-left', 'bottom-right')
        """
        try:
            # 检查图像文件
            if not os.path.exists(image_path):
                return False, f"图像文件不存在: {image_path}"
            
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
                
                # 读取并缩放图像
                img = ImageReader(image_path)
                img_width, img_height = img.getSize()
                
                # 计算缩放后的尺寸
                scaled_width = img_width * scale
                scaled_height = img_height * scale
                
                # 根据位置设置图像坐标
                if position == 'center':
                    x = (page_width - scaled_width) / 2
                    y = (page_height - scaled_height) / 2
                elif position == 'top-left':
                    x = 20
                    y = page_height - scaled_height - 20
                elif position == 'top-right':
                    x = page_width - scaled_width - 20
                    y = page_height - scaled_height - 20
                elif position == 'bottom-left':
                    x = 20
                    y = 20
                elif position == 'bottom-right':
                    x = page_width - scaled_width - 20
                    y = 20
                else:
                    x, y = 20, 20
                
                # 绘制图像（reportlab 不支持直接设置图像透明度，需要预处理）
                can.drawImage(image_path, x, y, width=scaled_width, height=scaled_height, 
                            mask='auto')
                
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
            
            return True, f"成功添加图像水印到 {output_pdf}"
            
        except Exception as e:
            return False, f"添加图像水印失败: {str(e)}"
    
    def remove_watermarks(self, input_pdf, output_pdf):
        """
        移除PDF中的水印（简单版本，通过提取文本和重新生成）
        注意：这是一个简化版本，复杂水印可能需要更高级的方法
        """
        try:
            # 这个功能比较复杂，需要OCR或高级分析
            # 这里提供一个简单的实现：复制原始PDF（实际上不处理水印）
            # 在实际应用中，可能需要使用专门的PDF处理库
            
            import shutil
            shutil.copy2(input_pdf, output_pdf)
            
            return True, f"已创建副本（水印移除功能需要更高级的实现）: {output_pdf}"
            
        except Exception as e:
            return False, f"移除水印失败: {str(e)}"
    
    def batch_process(self, input_dir, output_dir, watermark_text=None, 
                     watermark_image=None, **kwargs):
        """
        批量处理PDF文件
        
        参数:
            input_dir: 输入目录
            output_dir: 输出目录
            watermark_text: 水印文字（如果使用文本水印）
            watermark_image: 水印图像路径（如果使用图像水印）
        """
        try:
            input_path = Path(input_dir)
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            pdf_files = list(input_path.glob("*.pdf"))
            results = []
            
            for pdf_file in pdf_files:
                output_file = output_path / f"watermarked_{pdf_file.name}"
                
                if watermark_text:
                    success, message = self.add_text_watermark(
                        str(pdf_file), str(output_file), watermark_text, **kwargs
                    )
                elif watermark_image:
                    success, message = self.add_image_watermark(
                        str(pdf_file), str(output_file), watermark_image, **kwargs
                    )
                else:
                    success, message = False, "未指定水印类型"
                
                results.append({
                    'file': pdf_file.name,
                    'success': success,
                    'message': message
                })
            
            return True, results
            
        except Exception as e:
            return False, f"批量处理失败: {str(e)}"

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
    text_parser.add_argument('--font-name', help='字体名称 (如: 文泉驿正黑, 黑体, 楷体等)')
    
    # 添加图像水印命令
    image_parser = subparsers.add_parser('image', help='添加图像水印')
    image_parser.add_argument('input', help='输入PDF文件')
    image_parser.add_argument('output', help='输出PDF文件')
    image_parser.add_argument('--image', required=True, help='水印图像文件')
    image_parser.add_argument('--scale', type=float, default=0.2, help='图像缩放比例')
    image_parser.add_argument('--alpha', type=float, default=0.3, help='透明度 (0-1)')
    image_parser.add_argument('--position', default='center',
                           choices=['center', 'top-left', 'top-right', 'bottom-left', 'bottom-right'],
                           help='水印位置')
    
    # 批量处理命令
    batch_parser = subparsers.add_parser('batch', help='批量处理')
    batch_parser.add_argument('input_dir', help='输入目录')
    batch_parser.add_argument('output_dir', help='输出目录')
    batch_parser.add_argument('--text', help='水印文字')
    batch_parser.add_argument('--image', help='水印图像文件')
    batch_parser.add_argument('--font-size', type=int, default=40, help='字体大小')
    
    args = parser.parse_args()
    
    watermark = PDFWatermark()
    
    if args.command == 'text':
        # 解析颜色
        color = tuple(map(float, args.color.split(',')))
        success, message = watermark.add_text_watermark(
            args.input, args.output, args.text,
            font_size=args.font_size, color=color,
            alpha=args.alpha, rotation=args.rotation,
            position=args.position,
            font_name=args.font_name
        )
        print(message)
        
    elif args.command == 'image':
        success, message = watermark.add_image_watermark(
            args.input, args.output, args.image,
            scale=args.scale, alpha=args.alpha,
            position=args.position
        )
        print(message)
        
    elif args.command == 'batch':
        kwargs = {'font_size': args.font_size}
        if args.text:
            success, results = watermark.batch_process(
                args.input_dir, args.output_dir,
                watermark_text=args.text, **kwargs
            )
        elif args.image:
            success, results = watermark.batch_process(
                args.input_dir, args.output_dir,
                watermark_image=args.image, **kwargs
            )
        else:
            print("错误: 必须指定 --text 或 --image")
            sys.exit(1)
        
        if success:
            for result in results:
                status = "✅" if result['success'] else "❌"
                print(f"{status} {result['file']}: {result['message']}")
        else:
            print(f"批量处理失败: {results}")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()