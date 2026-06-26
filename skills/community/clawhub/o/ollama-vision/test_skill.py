#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Ollama Vision 技能
"""

import sys
import os

# 添加技能目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyze_image import analyze_image, check_ollama, check_model


def test_environment():
    """测试环境"""
    print("=" * 50)
    print("测试 1: 环境检查")
    print("=" * 50)
    
    if check_ollama():
        print("✅ Ollama 运行正常")
    else:
        print("❌ Ollama 未运行")
        return False
    
    if check_model("qwen3-vl:4b"):
        print("✅ qwen3-vl:4b 模型已安装")
    else:
        print("❌ qwen3-vl:4b 模型未安装")
        return False
    
    return True


def test_analysis(image_path):
    """测试图片分析"""
    print("\n" + "=" * 50)
    print("测试 2: 图片分析")
    print("=" * 50)
    print(f"图片路径: {image_path}")
    print(f"分析模式: describe")
    print("-" * 50)
    
    result = analyze_image(image_path, mode="describe")
    print("\n分析结果:")
    print(result)
    return True


if __name__ == "__main__":
    # 测试环境
    if not test_environment():
        print("\n环境检查失败，请修复后再试")
        sys.exit(1)
    
    # 查找测试图片
    test_paths = [
        os.path.expandvars(r"%USERPROFILE%\.openclaw\media\inbound"),
    ]
    
    test_image = None
    for path in test_paths:
        if os.path.exists(path):
            files = os.listdir(path)
            image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                test_image = os.path.join(path, image_files[0])
                break
    
    if test_image:
        test_analysis(test_image)
    else:
        print("\n未找到测试图片")
        print("请发送一张图片到任意频道，或指定图片路径:")
        print(f"  python test_skill.py <图片路径>")
