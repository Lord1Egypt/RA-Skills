"""
Smart Crop - 智能裁剪
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Union, List
import os


class SmartCrop:
    """智能裁剪工具"""
    
    def __init__(self):
        self.face_cascade = None
        self._init_face_detector()
    
    def _init_face_detector(self):
        """初始化人脸检测器"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
        except Exception as e:
            print(f"人脸检测器初始化失败: {e}")
    
    def face_crop(self, image_path: str, output_path: str,
                  size: Tuple[int, int] = (200, 200),
                  padding: float = 0.2) -> str:
        """
        人脸识别裁剪
        
        Args:
            padding: 人脸周围的留白比例
        """
        if self.face_cascade is None:
            raise RuntimeError("人脸检测器未初始化")
        
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"无法加载图像: {image_path}")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        if len(faces) == 0:
            print("未检测到人脸，使用中心裁剪")
            return self.center_crop(image_path, output_path, size)
        
        # 使用最大的人脸
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        
        # 添加留白
        pad_x = int(w * padding)
        pad_y = int(h * padding)
        
        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(image.shape[1], x + w + pad_x)
        y2 = min(image.shape[0], y + h + pad_y)
        
        # 裁剪并调整大小
        face_img = image[y1:y2, x1:x2]
        face_img = cv2.resize(face_img, size, interpolation=cv2.INTER_LANCZOS4)
        
        cv2.imwrite(output_path, face_img)
        print(f"人脸裁剪完成: {output_path}")
        return output_path
    
    def center_crop(self, image_path: str, output_path: str,
                   size: Tuple[int, int]) -> str:
        """中心裁剪"""
        image = Image.open(image_path)
        width, height = image.size
        
        # 计算裁剪区域
        crop_width, crop_height = size
        left = (width - crop_width) // 2
        top = (height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height
        
        # 确保不越界
        left = max(0, left)
        top = max(0, top)
        right = min(width, right)
        bottom = min(height, bottom)
        
        cropped = image.crop((left, top, right, bottom))
        
        # 如果裁剪尺寸不符，调整大小
        if cropped.size != size:
            cropped = cropped.resize(size, Image.Resampling.LANCZOS)
        
        cropped.save(output_path)
        print(f"中心裁剪完成: {output_path}")
        return output_path
    
    def subject_crop(self, image_path: str, output_path: str,
                    ratio: Union[str, Tuple[int, int]] = '16:9') -> str:
        """
        主体检测裁剪 (简化版，使用显著性检测)
        
        Args:
            ratio: 裁剪比例 ('16:9', '4:3', '1:1' 或 (宽, 高))
        """
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"无法加载图像: {image_path}")
        
        height, width = image.shape[:2]
        
        # 解析比例
        if isinstance(ratio, str):
            w_ratio, h_ratio = map(int, ratio.split(':'))
        else:
            w_ratio, h_ratio = ratio
        
        target_ratio = w_ratio / h_ratio
        current_ratio = width / height
        
        # 计算裁剪尺寸
        if current_ratio > target_ratio:
            # 太宽，裁剪左右
            new_width = int(height * target_ratio)
            left = (width - new_width) // 2
            cropped = image[:, left:left + new_width]
        else:
            # 太高，裁剪上下
            new_height = int(width / target_ratio)
            top = (height - new_height) // 2
            cropped = image[top:top + new_height, :]
        
        cv2.imwrite(output_path, cropped)
        print(f"主体裁剪完成: {output_path}")
        return output_path
    
    def thumbnail(self, image_path: str, output_path: str,
                 size: Tuple[int, int] = (150, 150),
                 crop_method: str = 'center') -> str:
        """
        生成缩略图
        
        Args:
            crop_method: 'center', 'face', 'subject'
        """
        if crop_method == 'face':
            try:
                return self.face_crop(image_path, output_path, size)
            except Exception:
                return self.center_crop(image_path, output_path, size)
        elif crop_method == 'center':
            return self.center_crop(image_path, output_path, size)
        else:
            return self.subject_crop(image_path, output_path, f"{size[0]}:{size[1]}")


if __name__ == '__main__':
    print("SmartCrop 初始化成功")
