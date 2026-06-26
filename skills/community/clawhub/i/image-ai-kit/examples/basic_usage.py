"""
Image AI Kit - 基本使用示例
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from image_processor import ImageProcessor
from ocr_engine import OCREngine
from smart_crop import SmartCrop


def demo_image_processing():
    """演示图像处理"""
    print("=" * 50)
    print("图像处理示例")
    print("=" * 50)
    
    print("\n基本操作:")
    print("""
    from scripts.image_processor import ImageProcessor
    
    # 加载图像
    img = ImageProcessor('photo.jpg')
    
    # 调整大小
    img.resize(width=800, height=600)
    
    # 裁剪
    img.crop(x=100, y=100, width=300, height=300)
    
    # 旋转
    img.rotate(90)
    
    # 调整亮度/对比度
    img.adjust_brightness(1.2)
    img.adjust_contrast(1.1)
    
    # 保存
    img.save('output.png')
    """)


def demo_ocr():
    """演示OCR识别"""
    print("\n" + "=" * 50)
    print("OCR文字识别示例")
    print("=" * 50)
    
    print("\n支持的语言:")
    print("  - chi_sim: 简体中文")
    print("  - chi_tra: 繁体中文")
    print("  - eng: 英文")
    print("  - jpn: 日文")
    print("  - chi_sim+eng: 中英文混合")
    
    print("\n示例代码:")
    print("""
    from scripts.ocr_engine import OCREngine
    
    # 初始化OCR引擎 (中文+英文)
    ocr = OCREngine(lang='chi_sim+eng')
    
    # 识别文字
    text = ocr.extract_text('document.jpg')
    print(text)
    
    # 提取带位置的文字
    boxes = ocr.extract_boxes('document.jpg')
    for box in boxes:
        print(f"{box['text']} at ({box['x']}, {box['y']})")
    """)


def demo_smart_crop():
    """演示智能裁剪"""
    print("\n" + "=" * 50)
    print("智能裁剪示例")
    print("=" * 50)
    
    print("\n裁剪模式:")
    print("  - face_crop: 人脸识别裁剪")
    print("  - center_crop: 中心裁剪")
    print("  - subject_crop: 主体检测裁剪")
    
    print("\n示例代码:")
    print("""
    from scripts.smart_crop import SmartCrop
    
    cropper = SmartCrop()
    
    # 人脸识别裁剪 (头像)
    cropper.face_crop('photo.jpg', 'avatar.jpg', size=(200, 200))
    
    # 中心裁剪
    cropper.center_crop('photo.jpg', 'center.jpg', size=(800, 600))
    
    # 按比例裁剪 (16:9)
    cropper.subject_crop('photo.jpg', 'wide.jpg', ratio='16:9')
    """)


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print(" Image AI Kit - AI图像工具包示例 ")
    print("=" * 60)
    
    demo_image_processing()
    demo_ocr()
    demo_smart_crop()
    
    print("\n" + "=" * 60)
    print("所有示例已完成！")
    print("=" * 60)
