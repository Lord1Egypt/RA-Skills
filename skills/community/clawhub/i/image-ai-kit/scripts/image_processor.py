"""
Image Processor - 图像处理器
"""

from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from typing import Optional, Tuple, Union, List
import os


class ImageProcessor:
    """图像处理器"""
    
    def __init__(self, image_path: Optional[str] = None):
        self.image_path = image_path
        self.image = None
        
        if image_path and os.path.exists(image_path):
            self.load(image_path)
    
    def load(self, image_path: str) -> 'ImageProcessor':
        """加载图像"""
        self.image_path = image_path
        self.image = Image.open(image_path)
        return self
    
    def resize(self, width: Optional[int] = None,
              height: Optional[int] = None,
              maintain_ratio: bool = True) -> 'ImageProcessor':
        """调整图像大小"""
        if maintain_ratio and (width or height):
            self.image.thumbnail((width or self.image.width,
                                 height or self.image.height),
                                Image.Resampling.LANCZOS)
        elif width and height:
            self.image = self.image.resize((width, height),
                                          Image.Resampling.LANCZOS)
        return self
    
    def crop(self, x: int, y: int, width: int, height: int) -> 'ImageProcessor':
        """裁剪图像"""
        self.image = self.image.crop((x, y, x + width, y + height))
        return self
    
    def crop_center(self, width: int, height: int) -> 'ImageProcessor':
        """中心裁剪"""
        img_w, img_h = self.image.size
        left = (img_w - width) // 2
        top = (img_h - height) // 2
        self.image = self.image.crop((left, top, left + width, top + height))
        return self
    
    def rotate(self, angle: float, expand: bool = True) -> 'ImageProcessor':
        """旋转图像"""
        self.image = self.image.rotate(angle, expand=expand)
        return self
    
    def flip_horizontal(self) -> 'ImageProcessor':
        """水平翻转"""
        self.image = self.image.transpose(Image.FlipLeftRight)
        return self
    
    def flip_vertical(self) -> 'ImageProcessor':
        """垂直翻转"""
        self.image = self.image.transpose(Image.FlipTopBottom)
        return self
    
    def convert(self, mode: str) -> 'ImageProcessor':
        """转换模式 (RGB, RGBA, L, etc.)"""
        self.image = self.image.convert(mode)
        return self
    
    def adjust_brightness(self, factor: float) -> 'ImageProcessor':
        """调整亮度 (0.0-2.0)"""
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def adjust_contrast(self, factor: float) -> 'ImageProcessor':
        """调整对比度 (0.0-2.0)"""
        enhancer = ImageEnhance.Contrast(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def adjust_saturation(self, factor: float) -> 'ImageProcessor':
        """调整饱和度 (0.0-2.0)"""
        enhancer = ImageEnhance.Color(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def adjust_sharpness(self, factor: float) -> 'ImageProcessor':
        """调整锐度 (0.0-2.0)"""
        enhancer = ImageEnhance.Sharpness(self.image)
        self.image = enhancer.enhance(factor)
        return self
    
    def blur(self, radius: float = 2.0) -> 'ImageProcessor':
        """模糊处理"""
        self.image = self.image.filter(ImageFilter.GaussianBlur(radius))
        return self
    
    def sharpen(self) -> 'ImageProcessor':
        """锐化"""
        self.image = self.image.filter(ImageFilter.SHARPEN)
        return self
    
    def edge_enhance(self) -> 'ImageProcessor':
        """边缘增强"""
        self.image = self.image.filter(ImageFilter.EDGE_ENHANCE)
        return self
    
    def grayscale(self) -> 'ImageProcessor':
        """转为灰度"""
        self.image = ImageOps.grayscale(self.image)
        return self
    
    def invert(self) -> 'ImageProcessor':
        """颜色反转"""
        self.image = ImageOps.invert(self.image.convert('RGB'))
        return self
    
    def auto_contrast(self) -> 'ImageProcessor':
        """自动对比度"""
        self.image = ImageOps.autocontrast(self.image)
        return self
    
    def equalize(self) -> 'ImageProcessor':
        """直方图均衡化"""
        self.image = ImageOps.equalize(self.image)
        return self
    
    def compress(self, quality: int = 85) -> 'ImageProcessor':
        """压缩质量"""
        self.quality = quality
        return self
    
    def save(self, output_path: str, format: Optional[str] = None,
            quality: int = 95, **kwargs) -> str:
        """
        保存图像
        
        Args:
            output_path: 输出路径
            format: 格式 (JPEG, PNG, WEBP, GIF)
            quality: 质量 (1-95)
        """
        save_kwargs = {}
        
        if format is None:
            format = os.path.splitext(output_path)[1][1:].upper()
            if format == 'JPG':
                format = 'JPEG'
        
        if format == 'JPEG':
            save_kwargs['quality'] = quality
            save_kwargs['optimize'] = True
            # JPEG 不支持透明度
            if self.image.mode == 'RGBA':
                self.image = self.image.convert('RGB')
        elif format == 'PNG':
            save_kwargs['optimize'] = True
        elif format == 'WEBP':
            save_kwargs['quality'] = quality
        
        self.image.save(output_path, format=format, **save_kwargs)
        print(f"图像已保存: {output_path}")
        return output_path
    
    def get_size(self) -> Tuple[int, int]:
        """获取图像尺寸"""
        return self.image.size if self.image else (0, 0)
    
    def get_mode(self) -> str:
        """获取颜色模式"""
        return self.image.mode if self.image else ''
    
    def get_info(self) -> dict:
        """获取图像信息"""
        if not self.image:
            return {}
        
        return {
            'size': self.get_size(),
            'mode': self.get_mode(),
            'format': self.image.format if hasattr(self.image, 'format') else None
        }


if __name__ == '__main__':
    print("ImageProcessor 初始化成功")
