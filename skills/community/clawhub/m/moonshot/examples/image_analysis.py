#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像分析示例
演示如何使用  进行图像分析
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import


def analyze_single_image():
    """分析单张图片"""
    print("=== 单张图片分析示例 ===\n")

    # 初始化客户端
    client = ()

    # 分析图片
    image_path = "path/to/your/image.jpg"

    try:
        result = client.analyze_image(
            image_path=image_path,
            prompt="""请详细分析这张图片，包括：
1. 图片中的主要物体和人物
2. 场景和环境描述
3. 构图和视觉风格
4. 色彩搭配和光线
5. 情感氛围和传达的信息
6. 适用场景和目标受众""",
            temperature=0.7
        )

        print("分析结果：")
        print(result.content)
        print(f"\n识别的物体: {result.objects}")
        print(f"场景类型: {result.scene}")
        print(f"情感倾向: {result.emotion}")
        print("\n建议:")
        for i, suggestion in enumerate(result.suggestions, 1):
            print(f"{i}. {suggestion}")

    except Exception as e:
        print(f"分析失败: {e}")


def analyze_with_different_models():
    """使用不同模型分析"""
    print("\n=== 不同模型对比示例 ===\n")

    client = ()
    image_path = "path/to/your/image.jpg"

    models = ['', '', '']

    for model in models:
        print(f"\n使用模型: {model}")
        print("-" * 50)

        try:
            result = client.analyze_image(
                image_path=image_path,
                prompt="简要描述这张图片",
                model=model
            )
            print(result.content)
        except Exception as e:
            print(f"错误: {e}")


def batch_analyze_images():
    """批量分析多张图片"""
    print("\n=== 批量图像分析示例 ===\n")

    client = ()
    image_paths = [
        "path/to/image1.jpg",
        "path/to/image2.jpg",
        "path/to/image3.jpg"
    ]

    for i, image_path in enumerate(image_paths, 1):
        print(f"\n分析图片 {i}: {os.path.basename(image_path)}")
        print("-" * 50)

        try:
            result = client.analyze_image(
                image_path=image_path,
                prompt="分析这张图片的主要内容和特点"
            )
            print(result.content)
        except Exception as e:
            print(f"错误: {e}")


def analyze_product_image():
    """产品图片分析"""
    print("\n=== 产品图片分析示例 ===\n")

    client = ()
    image_path = "path/to/product.jpg"

    result = client.analyze_image(
        image_path=image_path,
        prompt="""作为一个专业的产品分析师，请分析这张产品图片：

1. 产品外观和设计特点
2. 产品质量和材质感
3. 目标用户群体
4. 核心卖点和优势
5. 适用的营销场景
6. 潜在的改进建议

请给出专业、详细的分析报告。"""
    )

    print("产品分析报告:")
    print(result.content)


def analyze_social_media_image():
    """社交媒体图片分析"""
    print("\n=== 社交媒体图片分析示例 ===\n")

    client = ()
    image_path = "path/to/social_media.jpg"

    result = client.analyze_image(
        image_path=image_path,
        prompt="""从社交媒体运营的角度分析这张图片：

1. 视觉吸引力和传播潜力
2. 适合的平台和受众
3. 可能的话题和标签
4. 互动性和参与度预测
5. 优化建议

请给出实用的社交媒体运营建议。"""
    )

    print("社交媒体分析:")
    print(result.content)


def compare_images():
    """对比分析两张图片"""
    print("\n=== 图片对比分析示例 ===\n")

    client = ()
    image1 = "path/to/image1.jpg"
    image2 = "path/to/image2.jpg"

    # 先分析第一张
    print("分析第一张图片:")
    result1 = client.analyze_image(
        image_path=image1,
        prompt="详细描述这张图片的内容、风格和特点"
    )
    print(result1.content)

    # 再分析第二张
    print("\n分析第二张图片:")
    result2 = client.analyze_image(
        image_path=image2,
        prompt="详细描述这张图片的内容、风格和特点"
    )
    print(result2.content)

    # 综合对比
    print("\n综合对比:")
    conversation = client.create_conversation()
    comparison = conversation.chat(
        message=f"""基于以下两张图片的分析结果，请进行对比分析：

图片1分析: {result1.content}

图片2分析: {result2.content}

请从以下方面进行对比：
1. 内容差异
2. 风格特点
3. 优劣分析
4. 适用场景

请给出详细的对比分析报告。"""
    )
    print(comparison)


if __name__ == '__main__':
    print(" 大模型 - 图像分析示例\n")
    print("=" * 60)

    # 运行示例（根据需要选择）
    # analyze_single_image()
    # analyze_with_different_models()
    # batch_analyze_images()
    # analyze_product_image()
    # analyze_social_media_image()
    # compare_images()

    print("\n提示：请取消注释想要运行的示例函数，并修改图片路径。")
