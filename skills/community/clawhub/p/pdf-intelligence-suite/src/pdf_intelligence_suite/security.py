"""
PDF安全处理模块
支持加密、解密、水印、数字签名等
"""

import os
from typing import Optional, Union, Tuple
from io import BytesIO

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image


class PDFSecurity:
    """PDF安全处理器"""
    
    # 标准权限
    PERMISSIONS = {
        'print': 2 ** 2,           # 打印
        'modify': 2 ** 3,          # 修改
        'copy': 2 ** 4,            # 复制内容
        'annotate': 2 ** 5,        # 添加注释
        'forms': 2 ** 8,           # 填写表单
        'accessibility': 2 ** 9,   # 无障碍访问
        'assemble': 2 ** 10,       # 文档组装
        'print_high': 2 ** 11,     # 高质量打印
    }
    
    @classmethod
    def encrypt(
        cls,
        pdf_path: str,
        output_path: str,
        password: str,
        owner_password: Optional[str] = None,
        permissions: Optional[list] = None,
        algorithm: str = 'AES-256'
    ) -> str:
        """
        加密PDF文件
        
        Args:
            pdf_path: PDF文件路径
            output_path: 输出文件路径
            password: 用户密码（打开密码）
            owner_password: 所有者密码，默认与用户密码相同
            permissions: 权限列表，如 ['print', 'copy']
            algorithm: 加密算法 ('RC4-40', 'RC4-128', 'AES-128', 'AES-256')
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # 复制所有页面
        for page in reader.pages:
            writer.add_page(page)
        
        # 计算权限
        perm_value = 0xFFFFFFFF
        if permissions:
            perm_value = 0
            for perm in permissions:
                if perm in cls.PERMISSIONS:
                    perm_value |= cls.PERMISSIONS[perm]
        
        # 设置加密
        owner_pwd = owner_password or password
        
        if algorithm == 'AES-256':
            writer.encrypt(password, owner_pwd, use_128bit=True, use_aes256=True)
        elif algorithm == 'AES-128':
            writer.encrypt(password, owner_pwd, use_128bit=True, use_aes256=False)
        elif algorithm == 'RC4-128':
            writer.encrypt(password, owner_pwd, use_128bit=True)
        else:
            writer.encrypt(password, owner_pwd, use_128bit=False)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @classmethod
    def decrypt(
        cls,
        pdf_path: str,
        output_path: str,
        password: str
    ) -> str:
        """
        解密PDF文件
        
        Args:
            pdf_path: PDF文件路径
            output_path: 输出文件路径
            password: 密码
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        
        if reader.is_encrypted:
            reader.decrypt(password)
        
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @classmethod
    def add_text_watermark(
        cls,
        pdf_path: str,
        output_path: str,
        text: str = "CONFIDENTIAL",
        opacity: float = 0.3,
        angle: int = 45,
        font_size: int = 50,
        color: Tuple[float, float, float] = (0.5, 0.5, 0.5),
        pages: Optional[list] = None
    ) -> str:
        """
        添加文字水印
        
        Args:
            pdf_path: PDF文件路径
            output_path: 输出文件路径
            text: 水印文字
            opacity: 透明度 (0-1)
            angle: 旋转角度
            font_size: 字体大小
            color: RGB颜色元组
            pages: 添加水印的页面列表，None表示所有页面
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # 创建水印PDF
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.saveState()
        c.setFillColorRGB(*color, alpha=opacity)
        c.setFont("Helvetica", font_size)
        c.translate(letter[0]/2, letter[1]/2)
        c.rotate(angle)
        c.drawCentredString(0, 0, text)
        c.restoreState()
        c.save()
        packet.seek(0)
        
        watermark = PdfReader(packet)
        
        # 应用水印
        target_pages = pages if pages else range(len(reader.pages))
        
        for i, page in enumerate(reader.pages):
            if i in target_pages:
                page.merge_page(watermark.pages[0])
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @classmethod
    def add_image_watermark(
        cls,
        pdf_path: str,
        output_path: str,
        image_path: str,
        position: Union[str, Tuple[float, float]] = 'center',
        scale: float = 1.0,
        opacity: float = 0.3,
        pages: Optional[list] = None
    ) -> str:
        """
        添加图片水印
        
        Args:
            pdf_path: PDF文件路径
            output_path: 输出文件路径
            image_path: 水印图片路径
            position: 位置 ('center', 'top-left', 'top-right', 'bottom-left', 'bottom-right' 或 (x, y))
            scale: 缩放比例
            opacity: 透明度
            pages: 添加水印的页面列表
            
        Returns:
            输出文件路径
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件不存在: {image_path}")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # 获取图片尺寸
        img = Image.open(image_path)
        img_width, img_height = img.size
        
        # 创建水印PDF
        packet = BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        
        # 计算位置
        if position == 'center':
            x = (letter[0] - img_width * scale) / 2
            y = (letter[1] - img_height * scale) / 2
        elif position == 'top-left':
            x, y = 50, letter[1] - img_height * scale - 50
        elif position == 'top-right':
            x = letter[0] - img_width * scale - 50
            y = letter[1] - img_height * scale - 50
        elif position == 'bottom-left':
            x, y = 50, 50
        elif position == 'bottom-right':
            x = letter[0] - img_width * scale - 50
            y = 50
        else:
            x, y = position
        
        c.drawImage(image_path, x, y, width=img_width*scale, height=img_height*scale, mask='auto')
        c.save()
        packet.seek(0)
        
        watermark = PdfReader(packet)
        
        # 应用水印
        target_pages = pages if pages else range(len(reader.pages))
        
        for i, page in enumerate(reader.pages):
            if i in target_pages:
                page.merge_page(watermark.pages[0])
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return output_path
    
    @classmethod
    def is_encrypted(cls, pdf_path: str) -> bool:
        """
        检查PDF是否已加密
        
        Args:
            pdf_path: PDF文件路径
            
        Returns:
            是否加密
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        return reader.is_encrypted
    
    @classmethod
    def get_permissions(cls, pdf_path: str, password: Optional[str] = None) -> dict:
        """
        获取PDF权限信息
        
        Args:
            pdf_path: PDF文件路径
            password: 密码（如加密）
            
        Returns:
            权限字典
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
        
        reader = PdfReader(pdf_path)
        
        info = {
            'is_encrypted': reader.is_encrypted,
            'permissions': {}
        }
        
        if reader.is_encrypted and password:
            reader.decrypt(password)
        
        return info
