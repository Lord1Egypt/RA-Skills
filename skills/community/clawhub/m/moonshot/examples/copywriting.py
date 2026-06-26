#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文案创作示例
演示如何使用  进行智能���案创作
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from client import, CopywritingStyle, PlatformType


def generate_product_copywriting():
    """产品文案创作"""
    print("=== 产品文案创作示例 ===\n")

    client = ()
    image_path = "path/to/product.jpg"

    try:
        result = client.generate_copywriting(
            image_path=image_path,
            prompt="创作一段吸引人的产品文案，突出产品的创新性和实用性",
            style=CopywritingStyle.CREATIVE,
            platform=PlatformType.WECHAT,
            length="medium"
        )

        print(f"标题: {result.title}")
        print(f"平台: {result.platform}")
        print(f"字数: {result.word_count}")
        print(f"标签: {', '.join(result.tags)}")
        print("\n文案内容:")
        print(result.content)

    except Exception as e:
        print(f"创作失败: {e}")


def generate_social_media_content():
    """社交媒体内容创作"""
    print("\n=== 社交媒体内容创作示例 ===\n")

    client = ()

    platforms = [
        (PlatformType.WECHAT, "微信朋友圈"),
        (PlatformType.WEIBO, "微博"),
        (PlatformType.XIAOHONGSHU, "小红书"),
        (PlatformType.DOUYIN, "抖音")
    ]

    for platform, platform_name in platforms:
        print(f"\n--- {platform_name}文案 ---")

        try:
            result = client.generate_copywriting(
                prompt="分享一个生活中的小确幸",
                style=CopywritingStyle.CASUAL,
                platform=platform,
                length="short"
            )

            print(result.content)

        except Exception as e:
            print(f"错误: {e}")


def generate_marketing_copywriting():
    """营销文案创作"""
    print("\n=== 营销文案创作示例 ===\n")

    client = ()
    image_path = "path/to/product.jpg"

    styles = [
        CopywritingStyle.PROFESSIONAL,
        CopywritingStyle.CREATIVE,
        CopywritingStyle.INSPIRING
    ]

    for style in styles:
        print(f"\n--- {style.value.upper()} 风格 ---")

        try:
            result = client.generate_copywriting(
                image_path=image_path,
                prompt="创作一段营销文案",
                style=style,
                platform=PlatformType.WECHAT,
                length="medium"
            )

            print(result.content)

        except Exception as e:
            print(f"错误: {e}")


def generate_brand_story():
    """品牌故事创作"""
    print("\n=== 品牌故事创作示例 ===\n")

    client = ()

    try:
        result = client.generate_copywriting(
            prompt="""创作一个品牌故事：

品牌名称：时光印记
品牌定位：高端手工皮具
核心价值观：匠心传承、时光永恒、品质至上
目标受众：追求品质生活的都市精英

请创作一个感人至深的品牌故事，体现品牌的价值观和历史传承。""",
            style=CopywritingStyle.INSPIRING,
            platform=PlatformType.WECHAT,
            length="long"
        )

        print(f"标题: {result.title}")
        print("\n品牌故事:")
        print(result.content)

    except Exception as e:
        print(f"创作失败: {e}")


def generate_ad_variations():
    """广告变体创作"""
    print("\n=== 广告变体创作示例 ===\n")

    client = ()
    image_path = "path/to/product.jpg"

    angles = [
        "突出产品的性价比",
        "强调产品的品质感",
        "聚焦产品的创新科技",
        "营造情感共鸣"
    ]

    for i, angle in enumerate(angles, 1):
        print(f"\n--- 变体 {i}: {angle} ---")

        try:
            result = client.generate_copywriting(
                image_path=image_path,
                prompt=f"创作广告文案，{angle}",
                style=CopywritingStyle.CREATIVE,
                platform=PlatformType.WEIBO,
                length="short"
            )

            print(result.content)

        except Exception as e:
            print(f"错误: {e}")


def generate_seo_copywriting():
    """SEO 优化文案创作"""
    print("\n=== SEO 优化文案创作示例 ===\n")

    client = ()

    try:
        result = client.generate_copywriting(
            prompt="""创作一篇 SEO 优化的产品介绍文章：

关键词：智能手表、健康监测、长续航
产品特点：7天续航、全天候健康监测、防水设计、运动模式
目标：提高搜索引擎排名，吸引潜在购买者

请创作一篇自然融入关键词的高质量文章。""",
            style=CopywritingStyle.PROFESSIONAL,
            platform=PlatformType.WECHAT,
            length="long"
        )

        print(f"标题: {result.title}")
        print("\n文章内容:")
        print(result.content)

    except Exception as e:
        print(f"创作失败: {e}")


def generate_event_promotion():
    """活动推广文案创作"""
    print("\n=== 活动推广文案创作示例 ===\n")

    client = ()

    try:
        result = client.generate_copywriting(
            prompt="""创作一个限时优惠活动的推广文案：

活动主题：夏季清仓大促
优惠内容：全场5折起，满300减50
活动时间：本周五至周日
目标：吸引用户下单，提高转化率

请创作一段有吸引力的活动推广文案，营造紧迫感。""",
            style=CopywritingStyle.CREATIVE,
            platform=PlatformType.WEIBO,
            length="medium"
        )

        print(f"标题: {result.title}")
        print("\n推广文案:")
        print(result.content)

    except Exception as e:
        print(f"创作失败: {e}")


def generate_user_review_copywriting():
    """用户评价文案创作"""
    print("\n=== 用户评价文案创作示例 ===\n")

    client = ()

    try:
        result = client.generate_copywriting(
            prompt="""创作一个真实的用户评价文案：

产品：无线蓝牙耳机
使用场景：通勤、运动、办公
用户感受：音质清晰、佩戴舒适、续航持久
推荐指数：⭐⭐⭐⭐⭐

请以真实用户的口吻，创作一段有说服力的评价文案。""",
            style=CopywritingStyle.CASUAL,
            platform=PlatformType.XIAOHONGSHU,
            length="medium"
        )

        print(f"标题: {result.title}")
        print("\n用户评价:")
        print(result.content)

    except Exception as e:
        print(f"创作失败: {e}")


def generate_series_copywriting():
    """系列文案创作"""
    print("\n=== 系列文案创作示例 ===\n")

    client = ()

    themes = [
        "产品发布预热",
        "产品功能亮点",
        "用户使用场景",
        "购买引导"
    ]

    for i, theme in enumerate(themes, 1):
        print(f"\n--- 第 {i} 篇: {theme} ---")

        try:
            result = client.generate_copywriting(
                prompt=f"创作一篇{theme}的文案",
                style=CopywritingStyle.PROFESSIONAL,
                platform=PlatformType.WECHAT,
                length="medium"
            )

            print(result.content)

        except Exception as e:
            print(f"错误: {e}")


def interactive_copywriting_creation():
    """交互式文案创作"""
    print("\n=== 交互式文案创作示例 ===\n")

    client = ()
    conversation = client.create_conversation()

    print("开始交互式文案创作...")

    # 第一步：了解需求
    print("\n[步骤 1] 了解产品/服务")
    response1 = conversation.chat(
        message="我想为一款智能手表创作营销文案。这款手表具有健康监测、运动追踪、消息提醒等功能，目标用户是25-35岁的都市白领。请给出文案创作建议。"
    )
    print(response1)

    # 第二步：选择风格
    print("\n[步骤 2] 确定风格")
    response2 = conversation.chat(
        message="很好。我希望文案风格是专业而轻松的，适合在微信朋友圈发布。请创作一段文案。"
    )
    print(response2)

    # 第三步：优化调整
    print("\n[步骤 3] 优化调整")
    response3 = conversation.chat(
        message="文案不错，但能否再突出一下'提升工作效率'这个卖点？"
    )
    print(response3)

    # 第四步：生成变体
    print("\n[步骤 4] 生成变体")
    response4 = conversation.chat(
        message "很好！请基于这个文案，再创作2个不同角度的变体。"
    )
    print(response4)


if __name__ == '__main__':
    print(" 大模型 - 文案创作示例\n")
    print("=" * 60)

    # 运行示例（根据需要选择）
    # generate_product_copywriting()
    # generate_social_media_content()
    # generate_marketing_copywriting()
    # generate_brand_story()
    # generate_ad_variations()
    # generate_seo_copywriting()
    # generate_event_promotion()
    # generate_user_review_copywriting()
    # generate_series_copywriting()
    # interactive_copywriting_creation()

    print("\n提示：请取消注释想要运行的示例函数，并修改图片路径。")
