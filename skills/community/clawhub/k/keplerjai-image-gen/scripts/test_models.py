#!/usr/bin/env python3
"""
Test script for ThinkZone AI image models
"""

import subprocess
import sys
import os

# 设置环境变量
os.environ["THINKZONE_API_KEY"] = "amags_48e72e862e5d8f43d333df566c6ae65cc9401be4c902285d2f6565d092ba5a97"
os.environ["THINKZONE_BASE_URL"] = "https://open.thinkzoneai.com"

# 测试的模型列表
IMAGE_MODELS = [
    "seedream-5-0-260128",
    "seedream-4-5-251128",
    "seedream-4-0-241215",
    "seedream-3-0-240820",
    "seedream-lite-240601",
]


def test_image_model(model):
    """Test image generation with specified model."""
    print(f"\n{'='*60}")
    print(f"🎨 Testing Image Model: {model}")
    print(f"{'='*60}")

    cmd = [
        sys.executable,
        "scripts/gen_image.py",
        "--prompt", f"测试图片生成 - {model}",
        "--model", model,
        "--size", "2K",
        "--max-images", "1",
        "--no-watermark",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if result.returncode == 0:
            print(f"✅ {model} - SUCCESS")
            return True
        else:
            print(f"❌ {model} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"⏰ {model} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {model} - ERROR: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Starting ThinkZone AI Model Tests")
    print(f"📍 Working directory: {os.getcwd()}")

    results = {"passed": 0, "failed": 0}

    print("\n\n" + "🎨 IMAGE MODELS ".ljust(60, "="))
    for model in IMAGE_MODELS:
        if test_image_model(model):
            results["passed"] += 1
        else:
            results["failed"] += 1

    print("\n\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"🎨 Image Models: {results['passed']} passed, {results['failed']} failed")

    if results["failed"] > 0:
        sys.exit(1)
    else:
        print("\n✅ All tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
