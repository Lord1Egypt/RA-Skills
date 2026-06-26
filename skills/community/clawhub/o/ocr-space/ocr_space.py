#!/usr/bin/env python3
"""
OCR.space API 封装脚本
调用免费 OCR API 识别图片中的文字

使用方法:
    python3 ocr_space.py <图片路径> [语言代码]

语言代码 (默认 chs):
    - chs: 中文简体
    - cht: 中文繁体
    - eng: 英语
    - jpn: 日语
    - kor: 韩语
    - fre: 法语
    - ger: 德语
    完整列表见: https://ocr.space/ocrapi

示例:
    python3 ocr_space.py /path/to/image.jpg
    python3 ocr_space.py /path/to/image.png eng
"""

import sys
import os
import requests
import json
import base64

API_URL = "https://api.ocr.space/parse/image"
API_KEY = "helloworld"  # 免费测试 key


def resize_image_if_needed(image_path, max_size_kb=5120):  # 5MB
    """
    如果图片太大，自动压缩
    
    参数:
        image_path: 图片路径
        max_size_kb: 最大文件大小 (KB)
    
    返回:
        压缩后的图片路径
    """
    import io
    from PIL import Image
    
    file_size = os.path.getsize(image_path) / 1024  # KB
    if file_size <= max_size_kb:
        return image_path
    
    print(f"图片过大 ({file_size:.1f}KB)，正在压缩...")
    
    img = Image.open(image_path)
    
    # 转换为 RGB 模式（JPEG 不支持 RGBA）
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    # 逐步降低质量直到文件大小合适
    quality = 85
    while quality > 20:
        output = io.BytesIO()
        img.save(output, format='JPEG', quality=quality)
        size_kb = len(output.getvalue()) / 1024
        
        if size_kb <= max_size_kb:
            # 保存压缩后的图片
            compressed_path = image_path.replace('.jpg', '_compressed.jpg').replace('.png', '_compressed.jpg')
            if not compressed_path.endswith('.jpg'):
                compressed_path += '.jpg'
            
            with open(compressed_path, 'wb') as f:
                f.write(output.getvalue())
            
            print(f"压缩完成: {size_kb:.1f}KB (质量: {quality})")
            return compressed_path
        
        quality -= 10
    
    return image_path


def ocr_image(image_path, language="chs", is_file=True):
    """
    调用 OCR.space API 识别图片
    
    参数:
        image_path: 图片路径或 base64 字符串
        language: 语言代码 (默认 chs 中文简体)
        is_file: True=文件路径, False=base64 字符串
    
    返回:
        识别到的文本，失败返回 None
    """
    import io
    
    data = {
        "language": language,
        "isOverlayRequired": "false",
        "detectOrientation": "true",
        "scale": "true",
        "OCREngine": "2",  # 使用 Engine 2，支持语言自动检测
    }
    
    headers = {"apikey": API_KEY}
    
    try:
        if is_file:
            if not os.path.exists(image_path):
                print(f"错误: 文件不存在: {image_path}")
                return None
            
            # 检查文件大小，必要时压缩
            original_path = image_path
            image_path = resize_image_if_needed(image_path)
            
            with open(image_path, 'rb') as f:
                files = {"file": f}
                response = requests.post(API_URL, files=files, data=data, headers=headers, timeout=30)
            
            # 删除临时压缩文件
            if image_path != original_path and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                except:
                    pass
        else:
            # base64 编码
            files = {"file": base64.b64decode(image_path)}
            response = requests.post(API_URL, files=files, data=data, headers=headers, timeout=30)
        
        result = response.json()
        
        if result.get("ParsedResults"):
            text = result["ParsedResults"][0].get("ParsedText", "")
            return text.strip()
        else:
            error = result.get("ErrorMessage", ["未知错误"])[0]
            print(f"OCR 错误: {error}")
            return None
            
    except requests.exceptions.Timeout:
        print("错误: 请求超时")
        return None
    except Exception as e:
        print(f"错误: {str(e)}")
        return None


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    image_path = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else "chs"
    
    print(f"正在识别图片: {image_path}")
    print(f"语言: {language}")
    
    result = ocr_image(image_path, language)
    
    if result:
        print("\n--- 识别结果 ---")
        print(result)
        print("--- 结束 ---\n")
    else:
        print("识别失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
