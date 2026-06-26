"""
图像增强器 - Image Enhancer
"""

from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np


class ImageEnhancer:
    """图像增强器类"""
    
    def __init__(self):
        pass
    
    def upscale(self, input_path: str, output_path: str, scale: int = 2) -> str:
        """图像超分辨率（简化版使用 PIL 插值）"""
        img = Image.open(input_path)
        new_size = (img.width * scale, img.height * scale)
        upscaled = img.resize(new_size, Image.Resampling.LANCZOS)
        upscaled.save(output_path)
        return output_path
    
    def sharpen(self, input_path: str, output_path: str, factor: float = 2.0) -> str:
        """图像锐化"""
        img = Image.open(input_path)
        enhancer = ImageEnhance.Sharpness(img)
        sharpened = enhancer.enhance(factor)
        sharpened.save(output_path)
        return output_path
    
    def adjust_contrast(self, input_path: str, output_path: str, factor: float = 1.5) -> str:
        """调整对比度"""
        img = Image.open(input_path)
        enhancer = ImageEnhance.Contrast(img)
        adjusted = enhancer.enhance(factor)
        adjusted.save(output_path)
        return output_path
    
    def denoise(self, input_path: str, output_path: str) -> str:
        """图像去噪（使用 OpenCV）"""
        img = cv2.imread(input_path)
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
        cv2.imwrite(output_path, denoised)
        return output_path
