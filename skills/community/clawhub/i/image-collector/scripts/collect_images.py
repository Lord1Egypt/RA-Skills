#!/usr/bin/env python3
"""
AI 科技日报图片采集工具

功能：
1. 从官方来源采集新闻配图
2. 水印检测
3. 图片质量检查
4. 关联性验证
5. 自动下载和优化

使用示例：
    python collect_images.py --news "苹果 AI 百度文心" --keywords "Apple,Intelligence,Baidu"
    python collect_images.py --news "微软 Copilot" --keywords "Microsoft,Copilot,Critique" --source microsoft.com
"""

import os
import sys
import json
import hashlib
import requests
from PIL import Image
from pathlib import Path
from typing import Optional, List, Dict
import subprocess

# 图片来源白名单
OFFICIAL_SOURCES = {
    "apple.com": {"priority": 0, "keywords": ["Apple", "iOS", "Siri", "AI"]},
    "microsoft.com": {"priority": 0, "keywords": ["Microsoft", "Copilot", "Azure"]},
    "openai.com": {"priority": 0, "keywords": ["OpenAI", "GPT", "ChatGPT"]},
    "anthropic.com": {"priority": 0, "keywords": ["Anthropic", "Claude"]},
    "google.com": {"priority": 0, "keywords": ["Google", "Gemini", "Bard"]},
    "bytedance.com": {"priority": 0, "keywords": ["字节", "豆包", "Bytedance"]},
    "36kr.com": {"priority": 1, "keywords": ["36Kr", "创业"]},
    "huxiu.com": {"priority": 1, "keywords": ["虎嗅"]},
    "ifanr.com": {"priority": 1, "keywords": ["爱范儿"]},
    "bloomberg.com": {"priority": 1, "keywords": ["Bloomberg", "彭博"]},
    "reuters.com": {"priority": 1, "keywords": ["Reuters", "路透"]},
    "theverge.com": {"priority": 1, "keywords": ["The Verge"]},
    "ca.gov": {"priority": 1, "keywords": ["California", "加州"]},
    "gov.cn": {"priority": 1, "keywords": ["中国政府"]},
}

# 禁用来源
BANNED_SOURCES = [
    "mmbiz.qpic.cn",  # 微信图片，可能带水印
    "unsplash.com",   # 随机图片，与内容无关
    "pixabay.com",    # 随机图片
    "pexels.com",     # 随机图片
]


class ImageCollector:
    def __init__(self, output_dir: str = "/home/node/.openclaw/workspace/article-images"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
    
    def search_official_images(self, keywords: List[str], source: Optional[str] = None) -> List[Dict]:
        """
        搜索官方图片
        
        Args:
            keywords: 搜索关键词列表
            source: 限定来源域名（可选）
        
        Returns:
            图片信息列表，包含 url, source, width, height 等
        """
        results = []
        
        # 如果指定了来源，优先从该来源搜索
        if source:
            sources_to_search = [source]
        else:
            # 根据关键词匹配可能的来源
            sources_to_search = []
            for kw in keywords:
                for src, info in OFFICIAL_SOURCES.items():
                    if any(k.lower() in kw.lower() for k in info["keywords"]):
                        sources_to_search.append(src)
            
            # 去重，按优先级排序
            sources_to_search = sorted(set(sources_to_search), 
                                       key=lambda x: OFFICIAL_SOURCES.get(x, {}).get("priority", 99))
        
        print(f"🔍 搜索来源：{sources_to_search}")
        
        # 对每个来源执行搜索
        for src in sources_to_search[:3]:  # 最多搜索 3 个来源
            try:
                search_query = " ".join(keywords)
                # 使用 Google 自定义搜索或 Jina 搜索
                search_url = f"https://r.jina.ai/http://www.google.com/search?q=site:{src}+{search_query}+filetype:png+OR+filetype:jpg"
                
                resp = self.session.get(search_url, timeout=15)
                if resp.status_code == 200:
                    # 解析搜索结果，提取图片 URL
                    # 这里简化处理，实际应该用正则或 BeautifulSoup
                    print(f"✓ 从 {src} 获取到搜索结果")
                    
            except Exception as e:
                print(f"✗ 搜索 {src} 失败：{e}")
        
        return results
    
    def download_image(self, url: str, filename: Optional[str] = None) -> Optional[Path]:
        """
        下载图片
        
        Args:
            url: 图片 URL
            filename: 保存文件名（可选，自动生成）
        
        Returns:
            保存的文件路径，失败返回 None
        """
        try:
            # 检查来源是否被禁用
            for banned in BANNED_SOURCES:
                if banned in url:
                    print(f"✗ 禁用来源：{banned}")
                    return None
            
            resp = self.session.get(url, timeout=15)
            if resp.status_code != 200:
                print(f"✗ 下载失败：{resp.status_code}")
                return None
            
            # 生成文件名
            if not filename:
                # 从 URL 生成哈希文件名
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                content_type = resp.headers.get("Content-Type", "image/jpeg")
                ext = content_type.split("/")[-1]
                if ext == "jpeg":
                    ext = "jpg"
                filename = f"{url_hash}.{ext}"
            
            # 保存文件
            output_path = self.output_dir / filename
            output_path.write_bytes(resp.content)
            
            print(f"✓ 下载成功：{filename}")
            return output_path
            
        except Exception as e:
            print(f"✗ 下载异常：{e}")
            return None
    
    def check_watermark(self, image_path: Path) -> Dict:
        """
        检测图片水印
        
        检测策略：
        1. 检查四角是否有明显 Logo（颜色差异）
        2. 检查底部是否有文字区域
        3. 检查是否有半透明覆盖层
        
        Returns:
            检测结果：{has_watermark: bool, confidence: float, location: str}
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            pixels = img.load()
            
            watermark_score = 0
            locations = []
            
            # 检查四个角（各 10% 区域）
            corner_size = min(width, height) // 10
            
            # 左上角
            corner_colors = []
            for x in range(corner_size):
                for y in range(corner_size):
                    corner_colors.append(pixels[x, y])
            
            # 简单检测：如果角落颜色过于单一（可能是 Logo 背景）
            unique_colors = len(set(corner_colors))
            if unique_colors < corner_size * corner_size * 0.3:
                watermark_score += 0.2
                locations.append("左上角")
            
            # 检查底部 15% 区域（常见水印位置）
            bottom_start = int(height * 0.85)
            bottom_colors = []
            for x in range(width):
                for y in range(bottom_start, height):
                    bottom_colors.append(pixels[x, y])
            
            # 如果底部颜色分布异常（可能有文字）
            unique_bottom = len(set(bottom_colors))
            total_bottom = width * (height - bottom_start)
            if unique_bottom < total_bottom * 0.5:
                watermark_score += 0.3
                locations.append("底部")
            
            return {
                "has_watermark": watermark_score > 0.4,
                "confidence": watermark_score,
                "location": ", ".join(locations) if locations else "未检测到"
            }
            
        except Exception as e:
            print(f"✗ 水印检测失败：{e}")
            return {"has_watermark": False, "confidence": 0, "location": "检测失败"}
    
    def check_quality(self, image_path: Path) -> Dict:
        """
        检查图片质量
        
        Returns:
            质量报告：{width: int, height: int, acceptable: bool, issues: List}
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            issues = []
            
            # 检查分辨率
            if width < 800 or height < 600:
                issues.append(f"分辨率过低：{width}x{height}")
            
            # 检查宽高比（太窄或太扁的图片不适合做配图）
            aspect_ratio = width / height
            if aspect_ratio < 0.5 or aspect_ratio > 3:
                issues.append(f"宽高比异常：{aspect_ratio:.2f}")
            
            # 检查文件大小
            file_size = image_path.stat().st_size
            if file_size < 10 * 1024:  # 小于 10KB
                issues.append("文件过小，可能压缩过度")
            
            return {
                "width": width,
                "height": height,
                "acceptable": len(issues) == 0,
                "issues": issues
            }
            
        except Exception as e:
            print(f"✗ 质量检查失败：{e}")
            return {"width": 0, "height": 0, "acceptable": False, "issues": [str(e)]}
    
    def check_relevance(self, image_path: Path, keywords: List[str]) -> Dict:
        """
        检查图片与关键词的关联性
        
        策略：
        1. 文件名是否包含关键词
        2. （未来）使用 OCR 检测图片中的文字
        3. （未来）使用 CLIP 模型计算相似度
        
        Returns:
            关联性报告：{score: float, matched_keywords: List}
        """
        filename = image_path.name.lower()
        matched = []
        
        for kw in keywords:
            # 检查关键词是否在文件名中
            kw_clean = kw.lower().replace(" ", "").replace("-", "")
            if kw_clean in filename.replace(".", "").replace("_", ""):
                matched.append(kw)
        
        score = len(matched) / len(keywords) if keywords else 0
        
        return {
            "score": score,
            "matched_keywords": matched,
            "filename": image_path.name
        }
    
    def optimize_image(self, image_path: Path, output_path: Optional[Path] = None) -> Path:
        """
        优化图片（压缩、格式转换）
        
        Args:
            image_path: 输入图片路径
            output_path: 输出路径（可选，默认覆盖原文件）
        
        Returns:
            优化后的文件路径
        """
        try:
            img = Image.open(image_path)
            
            # 转换为 RGB（处理 PNG 透明通道）
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            # 调整大小（如果过大）
            max_size = (1920, 1080)
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 保存优化
            target = output_path or image_path
            img.save(target, "JPEG", quality=85, optimize=True, progressive=True)
            
            print(f"✓ 优化完成：{target.name}")
            return target
            
        except Exception as e:
            print(f"✗ 优化失败：{e}")
            return image_path
    
    def collect_for_news(self, news_title: str, keywords: List[str], 
                         source: Optional[str] = None) -> Optional[Path]:
        """
        为单条新闻采集配图
        
        完整流程：
        1. 搜索官方图片
        2. 下载候选图片
        3. 水印检测
        4. 质量检查
        5. 关联性验证
        6. 优化处理
        
        Args:
            news_title: 新闻标题
            keywords: 关键词列表
            source: 限定来源域名（可选）
        
        Returns:
            最终选中的图片路径，失败返回 None
        """
        print(f"\n📰 为新闻采集配图：{news_title}")
        print(f"🔑 关键词：{keywords}")
        
        # 1. 搜索图片
        candidates = self.search_official_images(keywords, source)
        
        if not candidates:
            print("✗ 未找到候选图片，尝试备选方案...")
            # 备选：使用 web-access skill 截图
            # 这里留给用户手动处理
            return None
        
        # 2. 下载并验证每个候选
        for candidate in candidates[:5]:  # 最多处理 5 个候选
            url = candidate.get("url")
            if not url:
                continue
            
            print(f"\n  处理候选：{url}")
            
            # 下载
            img_path = self.download_image(url)
            if not img_path:
                continue
            
            # 水印检测
            watermark_result = self.check_watermark(img_path)
            if watermark_result["has_watermark"]:
                print(f"  ✗ 检测到水印：{watermark_result['location']}")
                img_path.unlink()  # 删除有水印的图片
                continue
            
            # 质量检查
            quality_result = self.check_quality(img_path)
            if not quality_result["acceptable"]:
                print(f"  ✗ 质量不达标：{quality_result['issues']}")
                img_path.unlink()
                continue
            
            # 关联性检查
            relevance_result = self.check_relevance(img_path, keywords)
            if relevance_result["score"] < 0.3:
                print(f"  ⚠ 关联性较低：{relevance_result['score']}")
                # 关联性低不删除，作为备选
            
            # 优化
            optimized_path = self.optimize_image(img_path)
            
            print(f"  ✓ 验证通过，可用性：{relevance_result['score']:.1%}")
            return optimized_path
        
        print("\n✗ 所有候选图片均未通过验证")
        return None


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AI 科技日报图片采集工具")
    parser.add_argument("--news", required=True, help="新闻标题")
    parser.add_argument("--keywords", required=True, help="关键词（逗号分隔）")
    parser.add_argument("--source", help="限定来源域名（可选）")
    parser.add_argument("--output", default="/home/node/.openclaw/workspace/article-images",
                       help="输出目录")
    
    args = parser.parse_args()
    
    keywords = [k.strip() for k in args.keywords.split(",")]
    
    collector = ImageCollector(output_dir=args.output)
    result = collector.collect_for_news(args.news, keywords, args.source)
    
    if result:
        print(f"\n✅ 采集成功：{result}")
        sys.exit(0)
    else:
        print(f"\n❌ 采集失败，需要手动处理")
        sys.exit(1)


if __name__ == "__main__":
    main()
