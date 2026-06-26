#!/usr/bin/env python3
"""
PDF处理工具集
支持：合并、拆分、提取页面、旋转、压缩、转换等操作
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from PyPDF2 import PdfReader, PdfWriter, Transformation
    from PyPDF2.errors import PdfReadError
except ImportError:
    print("请安装 PyPDF2: pip install PyPDF2")
    sys.exit(1)

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from PIL import Image
except ImportError:
    Image = None

try:
    import reportlab
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ImportError:
    reportlab = None


class PDFTools:
    """PDF处理工具类"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def _validate_pdf(self, file_path: str) -> bool:
        """验证PDF文件是否有效"""
        if not os.path.exists(file_path):
            print(f"错误: 文件不存在 - {file_path}")
            return False
        if not file_path.lower().endswith('.pdf'):
            print(f"错误: 不是PDF文件 - {file_path}")
            return False
        return True
    
    def _get_reader(self, file_path: str) -> Optional[PdfReader]:
        """获取PDF阅读器"""
        try:
            return PdfReader(file_path)
        except Exception as e:
            print(f"错误: 无法读取PDF - {e}")
            return None
    
    def info(self, file_path: str) -> dict:
        """获取PDF信息"""
        if not self._validate_pdf(file_path):
            return {}
        
        reader = self._get_reader(file_path)
        if not reader:
            return {}
        
        info = {
            "文件": file_path,
            "页数": len(reader.pages),
            "文件大小": f"{os.path.getsize(file_path) / 1024:.2f} KB"
        }
        
        if reader.metadata:
            info["作者"] = reader.metadata.get('/Author', 'N/A')
            info["标题"] = reader.metadata.get('/Title', 'N/A')
            info["创建者"] = reader.metadata.get('/Creator', 'N/A')
            info["创建日期"] = reader.metadata.get('/CreationDate', 'N/A')
        
        return info
    
    def merge(self, input_files: List[str], output_file: str) -> bool:
        """合并多个PDF文件"""
        writer = PdfWriter()
        
        for file_path in input_files:
            if not self._validate_pdf(file_path):
                continue
            
            reader = self._get_reader(file_path)
            if reader:
                for page in reader.pages:
                    writer.add_page(page)
                print(f"已添加: {file_path} ({len(reader.pages)} 页)")
        
        try:
            with open(output_file, 'wb') as f:
                writer.write(f)
            print(f"合并完成: {output_file}")
            return True
        except Exception as e:
            print(f"错误: 合并失败 - {e}")
            return False
    
    def split(self, input_file: str, ranges: List[str], output_dir: str) -> bool:
        """按页面范围拆分PDF"""
        if not self._validate_pdf(input_file):
            return False
        
        reader = self._get_reader(input_file)
        if not reader:
            return False
        
        total_pages = len(reader.pages)
        os.makedirs(output_dir, exist_ok=True)
        
        base_name = Path(input_file).stem
        
        for i, page_range in enumerate(ranges):
            writer = PdfWriter()
            
            try:
                if '-' in page_range:
                    start, end = map(int, page_range.split('-'))
                    start = max(1, start)
                    end = min(total_pages, end)
                    for p in range(start - 1, end):
                        writer.add_page(reader.pages[p])
                else:
                    page_num = int(page_range)
                    page_num = max(1, min(total_pages, page_num))
                    writer.add_page(reader.pages[page_num - 1])
                
                output_file = os.path.join(output_dir, f"{base_name}_part{i+1}.pdf")
                with open(output_file, 'wb') as f:
                    writer.write(f)
                print(f"已拆分: {output_file}")
            except Exception as e:
                print(f"错误: 拆分页面 {page_range} 失败 - {e}")
        
        return True
    
    def extract_pages(self, input_file: str, pages: List[int], output_file: str) -> bool:
        """提取指定页面"""
        if not self._validate_pdf(input_file):
            return False
        
        reader = self._get_reader(input_file)
        if not reader:
            return False
        
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        for p in pages:
            if 1 <= p <= total_pages:
                writer.add_page(reader.pages[p - 1])
        
        try:
            with open(output_file, 'wb') as f:
                writer.write(f)
            print(f"页面提取完成: {output_file}")
            return True
        except Exception as e:
            print(f"错误: 提取失败 - {e}")
            return False
    
    def rotate(self, input_file: str, output_file: str, degrees: int = 90) -> bool:
        """旋转PDF页面"""
        if not self._validate_pdf(input_file):
            return False
        
        reader = self._get_reader(input_file)
        if not reader:
            return False
        
        writer = PdfWriter()
        
        for page in reader.pages:
            page.rotate(degrees)
            writer.add_page(page)
        
        try:
            with open(output_file, 'wb') as f:
                writer.write(f)
            print(f"旋转完成 ({degrees}°): {output_file}")
            return True
        except Exception as e:
            print(f"错误: 旋转失败 - {e}")
            return False
    
    def compress(self, input_file: str, output_file: str) -> bool:
        """压缩PDF"""
        if not self._validate_pdf(input_file):
            return False
        
        reader = self._get_reader(input_file)
        if not reader:
            return False
        
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.compress_content_streams()
        
        try:
            with open(output_file, 'wb') as f:
                writer.write(f)
            original_size = os.path.getsize(input_file)
            new_size = os.path.getsize(output_file)
            ratio = (1 - new_size / original_size) * 100
            print(f"压缩完成: {output_file}")
            print(f"原始大小: {original_size / 1024:.2f} KB -> 新大小: {new_size / 1024:.2f} KB (减少 {ratio:.1f}%)")
            return True
        except Exception as e:
            print(f"错误: 压缩失败 - {e}")
            return False
    
    def to_images(self, input_file: str, output_dir: str, dpi: int = 150) -> bool:
        """将PDF转换为图片"""
        if pdfplumber is None:
            print("错误: 请安装 pdfplumber 进行PDF转图片: pip install pdfplumber pypdfium2")
            return False
        
        if not self._validate_pdf(input_file):
            return False
        
        try:
            import pdfplumber.utils
        except:
            pass
        
        try:
            import pypdfium2 as pdfium
        except ImportError:
            print("错误: 请安装 pypdfium2: pip install pypdfium2")
            return False
        
        os.makedirs(output_dir, exist_ok=True)
        
        pdf = pdfium.PdfDocument(input_file)
        base_name = Path(input_file).stem
        
        for i in range(len(pdf)):
            page = pdf[i]
            pil_image = page.render(
                scale=dpi/72,
                rotation=0,
            )
            output_path = os.path.join(output_dir, f"{base_name}_page{i+1:03d}.png")
            pil_image.save(output_path)
            print(f"已转换: {output_path}")
        
        print(f"转换完成，共 {len(pdf)} 页")
        return True
    
    def from_images(self, image_files: List[str], output_file: str) -> bool:
        """将图片转换为PDF"""
        if Image is None:
            print("错误: 请安装 Pillow: pip install Pillow")
            return False
        
        if not image_files:
            print("错误: 未提供图片文件")
            return False
        
        images = []
        for img_path in image_files:
            if not os.path.exists(img_path):
                print(f"警告: 文件不存在 - {img_path}")
                continue
            try:
                img = Image.open(img_path)
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                images.append(img)
            except Exception as e:
                print(f"错误: 无法读取图片 {img_path} - {e}")
        
        if not images:
            print("错误: 没有有效的图片文件")
            return False
        
        if len(images) == 1:
            images[0].save(output_file, 'PDF', resolution=100.0)
        else:
            images[0].save(output_file, 'PDF', save_all=True, append_images=images[1:])
        
        print(f"转换完成: {output_file}")
        return True
    
    def encrypt(self, input_file: str, output_file: str, password: str) -> bool:
        """加密PDF"""
        if not self._validate_pdf(input_file):
            return False
        
        reader = self._get_reader(input_file)
        if not reader:
            return False
        
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        
        writer.encrypt(password)
        
        try:
            with open(output_file, 'wb') as f:
                writer.write(f)
            print(f"加密完成: {output_file}")
            return True
        except Exception as e:
            print(f"错误: 加密失败 - {e}")
            return False
    
    def decrypt(self, input_file: str, output_file: str, password: str) -> bool:
        """解密PDF"""
        if not self._validate_pdf(input_file):
            return False
        
        try:
            reader = PdfReader(input_file)
            if not reader.is_encrypted:
                print("文件未加密")
                return False
            
            reader.decrypt(password)
            
            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)
            
            with open(output_file, 'wb') as f:
                writer.write(f)
            print(f"解密完成: {output_file}")
            return True
        except Exception as e:
            print(f"错误: 解密失败 - 密码可能不正确")
            return False


def interactive_mode():
    """交互模式"""
    tools = PDFTools()
    
    print("=" * 50)
    print("PDF 处理工具")
    print("=" * 50)
    print("1. 查看PDF信息")
    print("2. 合并PDF")
    print("3. 拆分PDF")
    print("4. 提取页面")
    print("5. 旋转页面")
    print("6. 压缩PDF")
    print("7. PDF转图片")
    print("8. 图片转PDF")
    print("9. 加密PDF")
    print("10. 解密PDF")
    print("0. 退出")
    print("=" * 50)
    
    choice = input("请选择操作 (0-10): ").strip()
    
    if choice == "1":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        info = tools.info(file_path)
        for k, v in info.items():
            print(f"{k}: {v}")
    
    elif choice == "2":
        files = input("输入PDF文件路径（逗号分隔）: ").split(',')
        files = [f.strip().strip('"') for f in files if f.strip()]
        output = input("输出文件路径: ").strip().strip('"')
        tools.merge(files, output)
    
    elif choice == "3":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        ranges = input("输入页面范围（逗号分隔，如 1-3,5,7-10）: ").split(',')
        ranges = [r.strip() for r in ranges]
        output_dir = input("输出目录: ").strip().strip('"')
        tools.split(file_path, ranges, output_dir)
    
    elif choice == "4":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        pages = input("输入页码（逗号分隔，如 1,3,5）: ").split(',')
        pages = [int(p.strip()) for p in pages if p.strip().isdigit()]
        output = input("输出文件路径: ").strip().strip('"')
        tools.extract_pages(file_path, pages, output)
    
    elif choice == "5":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        degrees = int(input("输入旋转角度 (90/180/270): ").strip())
        output = input("输出文件路径: ").strip().strip('"')
        tools.rotate(file_path, output, degrees)
    
    elif choice == "6":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        output = input("输出文件路径: ").strip().strip('"')
        tools.compress(file_path, output)
    
    elif choice == "7":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        output_dir = input("输出目录: ").strip().strip('"')
        dpi = int(input("输入DPI (默认150): ").strip() or "150")
        tools.to_images(file_path, output_dir, dpi)
    
    elif choice == "8":
        files = input("输入图片文件路径（逗号分隔）: ").split(',')
        files = [f.strip().strip('"') for f in files if f.strip()]
        output = input("输出PDF文件路径: ").strip().strip('"')
        tools.from_images(files, output)
    
    elif choice == "9":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        password = input("输入密码: ").strip()
        output = input("输出文件路径: ").strip().strip('"')
        tools.encrypt(file_path, output, password)
    
    elif choice == "10":
        file_path = input("输入PDF文件路径: ").strip().strip('"')
        password = input("输入密码: ").strip()
        output = input("输出文件路径: ").strip().strip('"')
        tools.decrypt(file_path, output, password)


def main():
    parser = argparse.ArgumentParser(description='PDF处理工具')
    parser.add_argument('command', nargs='?', help='命令: info, merge, split, extract, rotate, compress, to-images, from-images, encrypt, decrypt')
    parser.add_argument('args', nargs='*', help='命令参数')
    
    args = parser.parse_args()
    
    if not args.command:
        interactive_mode()
        return
    
    tools = PDFTools()
    command = args.command.lower()
    
    if command == 'info':
        if len(args.args) < 1:
            print("用法: pdf-tools info <file.pdf>")
        else:
            info = tools.info(args.args[0])
            for k, v in info.items():
                print(f"{k}: {v}")
    
    elif command == 'merge':
        if len(args.args) < 2:
            print("用法: pdf-tools merge <output.pdf> <file1.pdf> <file2.pdf> ...")
        else:
            tools.merge(args.args[1:], args.args[0])
    
    elif command == 'split':
        if len(args.args) < 3:
            print("用法: pdf-tools split <file.pdf> <output_dir> <range1> <range2> ...")
        else:
            tools.split(args.args[0], args.args[2:], args.args[1])
    
    elif command == 'extract':
        if len(args.args) < 3:
            print("用法: pdf-tools extract <file.pdf> <output.pdf> <page1> <page2> ...")
        else:
            pages = [int(p) for p in args.args[2:]]
            tools.extract_pages(args.args[0], pages, args.args[1])
    
    elif command == 'rotate':
        if len(args.args) < 3:
            print("用法: pdf-tools rotate <file.pdf> <output.pdf> [degrees]")
        else:
            degrees = int(args.args[2]) if len(args.args) > 2 else 90
            tools.rotate(args.args[0], args.args[1], degrees)
    
    elif command == 'compress':
        if len(args.args) < 2:
            print("用法: pdf-tools compress <file.pdf> <output.pdf>")
        else:
            tools.compress(args.args[0], args.args[1])
    
    elif command == 'to-images':
        if len(args.args) < 2:
            print("用法: pdf-tools to-images <file.pdf> <output_dir> [dpi]")
        else:
            dpi = int(args.args[2]) if len(args.args) > 2 else 150
            tools.to_images(args.args[0], args.args[1], dpi)
    
    elif command == 'from-images':
        if len(args.args) < 2:
            print("用法: pdf-tools from-images <output.pdf> <image1.jpg> <image2.png> ...")
        else:
            tools.from_images(args.args[1:], args.args[0])
    
    elif command == 'encrypt':
        if len(args.args) < 3:
            print("用法: pdf-tools encrypt <file.pdf> <output.pdf> <password>")
        else:
            tools.encrypt(args.args[0], args.args[1], args.args[2])
    
    elif command == 'decrypt':
        if len(args.args) < 3:
            print("用法: pdf-tools decrypt <file.pdf> <output.pdf> <password>")
        else:
            tools.decrypt(args.args[0], args.args[1], args.args[2])
    
    else:
        print(f"未知命令: {command}")
        print("可用命令: info, merge, split, extract, rotate, compress, to-images, from-images, encrypt, decrypt")


if __name__ == '__main__':
    main()
