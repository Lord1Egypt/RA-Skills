#!/usr/bin/env python3
"""
图片文字识别工具
用法: python3 /home/ubuntu/.openclaw/skills/img-ocr/ocr.py <图片路径>
"""
import sys
import pytesseract
from PIL import Image

if len(sys.argv) < 2:
    print("用法: python3 ocr.py <图片路径>")
    sys.exit(1)

path = sys.argv[1]
try:
    img = Image.open(path)
    # 中文+英文识别
    text = pytesseract.image_to_string(img, lang='chi_sim+eng')
    print("识别结果:")
    print(text)
except FileNotFoundError:
    print(f"文件不存在: {path}")
except Exception as e:
    print(f"错误: {e}")
