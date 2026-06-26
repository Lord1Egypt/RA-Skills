#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配图生成器 - 生成水墨中国风配图
支持通过 AI 工具（image_gen 或即梦 API）生成配图
"""

import os
import json
import random
from datetime import datetime


class ImageGenerator:
    """配图生成器"""

    def __init__(self, output_dir=None):
        """
        初始化配图生成器

        Args:
            output_dir: 图片输出目录（默认使用临时目录）
        """
        # 设置输出目录
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "generated-images")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # 水墨中国风配图主题
        self.image_themes = [
            "水墨竹子，宣纸底色，红色印章，中国风",
            "水墨山水，宣纸底色，淡雅意境，红色印章",
            "水墨梅兰竹菊，宣纸底色，古典雅致，红色印章",
            "水墨松鹤延年，宣纸底色，禅意，红色印章",
            "水墨荷花，宣纸底色，清雅，红色印章"
        ]

        # 配图风格
        self.style_keywords = [
            "水墨画风格",
            "传统中国画",
            "文人画风格",
            "国画风格",
            "古典水墨"
        ]

    def generate_prompt(self, theme=None):
        """
        生成配图提示词

        Args:
            theme: 配图主题（可选，随机选择）

        Returns:
            str: 配图提示词
        """
        if theme is None:
            theme = random.choice(self.image_themes)

        # 基础提示词
        base_prompt = f"{theme}，极简留白，高清，细节丰富"

        # 添加风格关键词
        style_keyword = random.choice(self.style_keywords)
        prompt = f"{base_prompt}，{style_keyword}"

        return prompt

    def generate_image_prompt_for_topic(self, article_topic):
        """
        根据文章话题生成配图提示词

        Args:
            article_topic: 文章话题

        Returns:
            str: 配图提示词
        """
        if any(keyword in article_topic for keyword in ["35岁", "失业", "裁员"]):
            theme = "水墨松柏，象征坚韧，宣纸底色，红色印章，中国风"
        elif any(keyword in article_topic for keyword in ["钱", "房", "车贷"]):
            theme = "水墨山水，象征生活起伏，宣纸底色，红色印章，中国风"
        elif any(keyword in article_topic for keyword in ["焦虑", "压力"]):
            theme = "水墨竹子，象征清高坚韧，宣纸底色，红色印章，中国风"
        else:
            theme = random.choice(self.image_themes)

        return self.generate_prompt(theme)

    def save_placeholder_image(self, filename=None):
        """
        创建占位图片（用于测试或AI配图服务不可用时）

        Args:
            filename: 图片文件名（可选）

        Returns:
            str: 图片文件路径
        """
        if filename is None:
            filename = f"placeholder_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

        filepath = os.path.join(self.output_dir, filename)

        try:
            from PIL import Image
            img = Image.new('RGB', (1024, 1024), color='#F5F5DC')  # 米黄色宣纸底色
            img.save(filepath, 'PNG')
            print(f"[配图生成器] 占位图片已保存: {filepath}")
            return filepath
        except ImportError:
            # 如果没有PIL，创建一个最小的PNG文件
            with open(filepath, 'wb') as f:
                f.write(b'\x89PNG\r\n\x1a\n')
            print(f"[配图生成器] 占位图片已保存: {filepath}")
            return filepath
        except Exception as e:
            print(f"[配图生成器] 创建占位图片失败: {e}")
            return None


def main():
    """测试配图生成器"""
    generator = ImageGenerator()

    # 测试生成提示词
    prompt = generator.generate_prompt()
    print(f"配图提示词: {prompt}")

    prompt2 = generator.generate_image_prompt_for_topic("35岁被裁员")
    print(f"话题配图提示词: {prompt2}")

    # 测试保存占位图
    path = generator.save_placeholder_image()
    print(f"占位图片: {path}")


if __name__ == "__main__":
    main()
