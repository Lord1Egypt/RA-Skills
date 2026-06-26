#!/usr/bin/env python3
"""
简单测试 - 使用视觉 AI 识别图片内容
"""

import sys
sys.path.insert(0, '/root/.openclaw/workspace')

# 读取图片
image_path = '/root/.openclaw/media/inbound/2c718a15-d264-4100-af87-7b6e814a9201.jpg'

print("📷 读取图片:", image_path)
print("图片已加载，现在需要视觉 AI 来识别内容...")
print()
print("由于 PaddleOCR 与当前 CPU 不兼容，建议使用以下方案:")
print("1. 使用 GPT-4V / Claude Vision 等视觉 AI")
print("2. 使用 Google Cloud Vision API")
print("3. 使用 Azure Computer Vision")
print()
print("测试图片路径:", image_path)
