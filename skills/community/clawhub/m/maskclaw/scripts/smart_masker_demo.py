#!/usr/bin/env python3
"""
MaskClaw Smart Masker Demo
智能视觉打码演示脚本

Usage:
    python scripts/smart_masker_demo.py --image test.jpg --keywords "手机号,身份证,银行卡"
"""

import argparse
import base64
import json
import sys
import time
from pathlib import Path

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.smart_masker import VisualMasker


def demo_basic_masking():
    """基础打码演示"""
    print("=" * 60)
    print("MaskClaw Smart Masker - 基础打码演示")
    print("=" * 60)

    masker = VisualMasker()

    keywords = ["李一航", "手机号", "身份证"]

    print(f"\n📝 敏感关键词: {keywords}")
    print(f"📷 输入图片: sample_input.jpg")

    print("\n🔄 开始处理...")
    start_time = time.time()

    print("\n💡 提示: 请提供实际的图片文件进行测试")
    print(f"   运行: python scripts/smart_masker_demo.py --image your_image.jpg --keywords '手机号,身份证'")


def demo_api_usage():
    """API 使用演示"""
    print("\n" + "=" * 60)
    print("MaskClaw Smart Masker - API 使用示例")
    print("=" * 60)

    code_example = '''
from scripts.smart_masker import VisualMasker

# 1. 初始化
masker = VisualMasker()

# 2. 定义敏感关键词
keywords = ["手机号", "身份证", "银行卡", "密码"]

# 3. 处理图片
result = masker.process_image(
    image_path="test.jpg",
    sensitive_keywords=keywords,
    method="blur"  # blur/mosaic/block
)

# 4. 检查结果
if result["success"]:
    print(f"检测到 {result['regions_count']} 个敏感区域")
    for region in result["detected_regions"]:
        print(f"  - {region['text']} at {region['bbox']}")
    print(f"脱敏图片: {result['masked_image_path']}")
'''
    print(code_example)


def demo_ocr_results():
    """OCR 识别结果演示"""
    print("\n" + "=" * 60)
    print("MaskClaw Smart Masker - OCR 识别结果示例")
    print("=" * 60)

    sample_ocr_result = {
        "success": True,
        "masked_image_path": "temp/masked_20260325_143052.jpg",
        "detected_regions": [
            {
                "text": "13812345678",
                "bbox": [120, 340, 280, 370],
                "keyword_matched": "手机号",
                "confidence": 0.95
            },
            {
                "text": "110101199001011234",
                "bbox": [100, 400, 320, 430],
                "keyword_matched": "身份证",
                "confidence": 0.92
            }
        ],
        "regions_count": 2,
        "processing_time_ms": 45
    }

    print("\n📋 示例 OCR 识别结果:")
    print(json.dumps(sample_ocr_result, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser(description="MaskClaw Smart Masker Demo")
    parser.add_argument("--image", "-i", type=str, help="输入图片路径")
    parser.add_argument("--keywords", "-k", type=str, help="敏感关键词，用逗号分隔")
    parser.add_argument("--method", "-m", type=str, default="blur",
                        choices=["blur", "mosaic", "block"],
                        help="打码方式: blur(高斯模糊), mosaic(马赛克), block(色块)")

    args = parser.parse_args()

    if args.image and args.keywords:
        print(f"📷 输入图片: {args.image}")
        print(f"📝 敏感关键词: {args.keywords}")
        print(f"🎨 打码方式: {args.method}")
        print("\n⚠️ 需要实际图片文件才能运行演示")
    else:
        demo_basic_masking()
        demo_api_usage()
        demo_ocr_results()


if __name__ == "__main__":
    main()
