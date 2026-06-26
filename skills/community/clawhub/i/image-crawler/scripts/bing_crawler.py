#!/usr/bin/env python3
"""
Bing 图片搜索引擎模板
独立可用的简化版本，方便理解核心逻辑和二次开发。

核心接口:
  - search(keyword, count) → [{"url": ..., "source": "bing"}, ...]
  - download(url, filepath) → bool

修改指南:
  - Bing 返回 HTML，图片 URL 在 murl 字段中（需 html.unescape 解码）
  - 调整 headers / cookie 应对反爬
  - 修改正则表达式以适应页面结构变化
"""

import os
import re
import time
import html as html_mod
import requests
from pathlib import Path
from urllib.parse import quote, urlparse


class BingImageSearch:
    """Bing 图片搜索 + 下载"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
            ),
            "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

    def search(self, keyword: str, count: int = 50) -> list:
        """
        搜索 Bing 图片。
        Args:
            keyword: 搜索关键词
            count: 期望返回数量
        Returns:
            [{"url": str, "source": "bing"}, ...]
        """
        images = []
        page = 0
        per_page = 35
        max_pages = (count // per_page) + 2

        while len(images) < count and page < max_pages:
            try:
                url = (f"https://www.bing.com/images/async"
                       f"?q={quote(keyword)}&first={page * per_page}"
                       f"&count={per_page}&mmasync=1")
                resp = self.session.get(url, timeout=20)
                if resp.status_code != 200:
                    break

                # 关键：Bing 返回的 HTML 中双引号编码为 &quot;，需先解码
                decoded = html_mod.unescape(resp.text)
                pattern = r'murl":"(https?://[^"]+\.(?:jpg|jpeg|png|webp))"'
                matches = re.findall(pattern, decoded, re.IGNORECASE)

                if not matches:
                    break

                for m in matches:
                    img_url = m.replace("\\/", "/")
                    if img_url not in {img["url"] for img in images}:
                        images.append({"url": img_url, "source": "bing"})

            except Exception as e:
                print(f"搜索出错: {e}")
                break

            page += 1
            time.sleep(0.5)

        return images[:count]

    def download(self, url: str, filepath: str, timeout: int = 15) -> bool:
        """
        下载单张图片。
        Returns: True 成功, False 失败
        """
        try:
            resp = self.session.get(
                url,
                headers={"Referer": "https://www.bing.com/images/search"},
                timeout=(5, timeout),
                stream=True,
            )
            if resp.status_code != 200:
                return False
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            if os.path.getsize(filepath) < 2000:
                os.remove(filepath)
                return False
            return True
        except Exception:
            if os.path.exists(filepath):
                os.remove(filepath)
            return False


# ─── 独立运行示例 ────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Bing 图片搜索下载")
    p.add_argument("-k", "--keyword", required=True, help="搜索关键词")
    p.add_argument("-n", "--count", type=int, default=10, help="下载数量")
    p.add_argument("-o", "--output", default="./bing_images", help="输出目录")
    args = p.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    engine = BingImageSearch()
    results = engine.search(args.keyword, count=args.count * 2)
    print(f"搜索到 {len(results)} 条结果")

    success = 0
    for i, img in enumerate(results, 1):
        if success >= args.count:
            break
        # 根据 URL 判断扩展名
        parsed = urlparse(img["url"])
        ext = os.path.splitext(parsed.path)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".webp"):
            ext = ".jpg"
        fp = out / f"bing_{i:03d}{ext}"
        if engine.download(img["url"], str(fp)):
            size = os.path.getsize(str(fp)) // 1024
            print(f"  [{success+1}/{args.count}] ✓ {fp.name} ({size}KB)")
            success += 1
        else:
            print(f"  [{i}] ✗ 失败")
        time.sleep(0.2)

    print(f"\n完成: {success}/{args.count} 张")
