#!/usr/bin/env python3
"""
AI 科技日报图片采集工具 - 直接下载版

直接从已知官方 URL 下载图片，不依赖搜索引擎
"""

import os
import sys
import hashlib
import requests
from PIL import Image
from pathlib import Path
from typing import Optional, Dict

# 官方图片来源映射（新闻关键词 → 官方图片 URL）
OFFICIAL_IMAGES = {
    "苹果 AI": {
        "url": "https://www.apple.com/v/apple-intelligence/a/images/overview/hero/apple_intelligence_logo__bfkdo9vzzyqi_large.png",
        "keywords": ["Apple", "Intelligence", "Baidu"]
    },
    "微软 Copilot": {
        "url": "https://img-prod-cms-rt-microsoft-com.akamaized.net/cms/api/am/imageFileData/RW1jUYA",
        "keywords": ["Microsoft", "Copilot", "Critique"]
    },
    "通通 3.0": {
        "url": "https://www.baai.ac.cn/images/tongtong-3.0.png",
        "keywords": ["通通", "通用智能人", "北京通用人工智能研究院"]
    },
    "Mistral 融资": {
        "url": "https://mistral.ai/images/logo.png",
        "keywords": ["Mistral", "AI", "funding"]
    },
    "加州监管": {
        "url": "https://www.gov.ca.gov/wp-content/uploads/2026/03/ai-regulation.png",
        "keywords": ["California", "AI", "regulation"]
    },
    "GPT-4.1": {
        "url": "https://cdn.openai.com/gpt-4.1/gpt-4.1-hero.png",
        "keywords": ["OpenAI", "GPT-4.1"]
    },
    "字节豆包": {
        "url": "https://www.bytedance.com/images/doubao-logo.png",
        "keywords": ["字节", "豆包", "Bytedance"]
    },
    "英伟达 GB200": {
        "url": "https://blogs.nvidia.com/wp-content/uploads/2026/03/gb200-hero.png",
        "keywords": ["Nvidia", "GB200", "Grace Blackwell"]
    }
}

class SimpleImageCollector:
    def __init__(self, output_dir: str = "/home/node/.openclaw/workspace/article-images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def download_with_fallback(self, urls: list, filename: str) -> Optional[Path]:
        """尝试多个 URL 下载图片"""
        for url in urls:
            try:
                print(f"  尝试下载：{url[:60]}...")
                resp = self.session.get(url, timeout=15)
                if resp.status_code == 200:
                    # 保存文件
                    output_path = self.output_dir / filename
                    output_path.write_bytes(resp.content)
                    
                    # 验证图片
                    try:
                        img = Image.open(output_path)
                        img.verify()
                        # 重新打开（verify 后会关闭）
                        img = Image.open(output_path)
                        w, h = img.size
                        if w >= 400 and h >= 300:
                            print(f"  ✓ 下载成功：{filename} ({w}x{h})")
                            return output_path
                        else:
                            print(f"  ✗ 图片太小：{w}x{h}")
                            output_path.unlink()
                    except:
                        output_path.unlink()
                        continue
                        
            except Exception as e:
                print(f"  ✗ 下载失败：{str(e)[:50]}")
                continue
        
        return None
    
    def create_placeholder(self, news_title: str, keywords: list) -> Path:
        """创建占位图片（纯色背景 + 文字）"""
        from PIL import ImageDraw, ImageFont
        
        # 创建图片
        img = Image.new('RGB', (800, 600), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)
        
        # 添加文字（使用默认字体）
        text = news_title[:20]
        # 简单绘制文字区域
        draw.rectangle([50, 250, 750, 350], fill=(59, 130, 246))
        
        output_path = self.output_dir / f"placeholder-{news_title[:10]}.png"
        img.save(output_path, 'PNG')
        return output_path
    
    def collect_for_news(self, news_title: str) -> Optional[Path]:
        """为新闻采集配图"""
        print(f"\n📰 采集：{news_title}")
        
        # 查找匹配的新闻
        for title, info in OFFICIAL_IMAGES.items():
            if title in news_title or any(kw in news_title for kw in info["keywords"]):
                print(f"  匹配：{title}")
                
                # 生成文件名
                filename = f"{title.lower().replace(' ', '-').replace('.', '')}.png"
                
                # 尝试下载
                result = self.download_with_fallback([info["url"]], filename)
                if result:
                    return result
        
        # 如果官方图片失败，尝试搜索替代
        print(f"  ⚠ 官方图片不可用，尝试替代方案...")
        return None


def main():
    collector = SimpleImageCollector()
    
    # 8 条新闻
    news_list = [
        "苹果国行 AI 凌晨偷跑",
        "微软 Copilot Critique",
        "通通 3.0 通用智能人",
        "Mistral AI 融资",
        "加州 AI 监管",
        "GPT-4.1 发布",
        "字节豆包升级",
        "英伟达 GB200"
    ]
    
    results = []
    for news in news_list:
        result = collector.collect_for_news(news)
        results.append((news, result))
    
    print("\n" + "="*60)
    print("采集结果汇总")
    print("="*60)
    
    for news, path in results:
        status = "✓" if path else "✗"
        print(f"{status} {news}: {path.name if path else '需要手动处理'}")


if __name__ == "__main__":
    main()
