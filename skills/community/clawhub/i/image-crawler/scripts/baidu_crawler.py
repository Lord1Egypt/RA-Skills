#!/usr/bin/env python3
"""
百度图片搜索引擎模板
独立可用的简化版本，方便理解核心逻辑和二次开发。

核心接口:
  - search(keyword, start, count) → [{"url": ..., "title": ...}, ...]
  - download(url, filepath) → bool

修改指南:
  - 调整 headers 应对反爬
  - 修改 search() 的参数来改变搜索行为
  - 修改 download() 中的 content-type 检查来支持更多格式
"""

import os
import json
import time
import requests
from pathlib import Path


class BaiduImageSearch:
    """百度图片搜索 + 下载"""

    API_URL = "https://image.baidu.com/search/acjson"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            ),
            "Accept": "application/json, text/javascript, */*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Referer": "https://image.baidu.com/",
        })

    def search(self, keyword: str, start: int = 0, count: int = 30) -> list:
        """
        搜索百度图片。
        Args:
            keyword: 搜索关键词
            start: 起始偏移量（分页用，每页 count 条）
            count: 每页返回数量（最大 30）
        Returns:
            [{"url": str, "title": str, "width": int, "height": int}, ...]
        """
        images = []
        try:
            resp = self.session.get(self.API_URL, params={
                "tn": "resultjson_com", "ipn": "rj",
                "ct": "201326592", "fp": "result",
                "queryWord": keyword, "word": keyword,
                "cl": "2", "lm": "-1",
                "ie": "utf-8", "oe": "utf-8",
                "st": "-1", "ic": "0", "face": "0",
                "istype": "2", "nc": "1",
                "pn": start, "rn": count,
            }, timeout=15)

            if resp.status_code == 200:
                for item in resp.json().get("data", []):
                    url = item.get("thumbURL") or item.get("objURL")
                    if url and url.startswith("http"):
                        images.append({
                            "url": url,
                            "title": item.get("fromPageTitle", "")[:50],
                            "width": item.get("width", 0),
                            "height": item.get("height", 0),
                        })
        except Exception as e:
            print(f"搜索出错: {e}")
        return images

    def search_all(self, keyword: str, total: int = 100) -> list:
        """多页搜索，自动翻页直到收集够 total 条"""
        all_images = []
        page = 0
        per_page = 30
        while len(all_images) < total and page < 35:
            batch = self.search(keyword, start=page * per_page, count=per_page)
            if not batch:
                break
            all_images.extend(batch)
            page += 1
            time.sleep(0.3)
        return all_images[:total]

    def download(self, url: str, filepath: str, timeout: int = 15) -> bool:
        """
        下载单张图片。
        Returns: True 成功, False 失败
        """
        try:
            resp = self.session.get(url, timeout=(5, timeout), stream=True)
            if resp.status_code != 200:
                return False
            ct = resp.headers.get("content-type", "")
            if "image" not in ct and "octet" not in ct:
                return False
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    if chunk:
                        f.write(chunk)
            # 过滤过小的文件（可能是占位图）
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

    p = argparse.ArgumentParser(description="百度图片搜索下载")
    p.add_argument("-k", "--keyword", required=True, help="搜索关键词")
    p.add_argument("-n", "--count", type=int, default=10, help="下载数量")
    p.add_argument("-o", "--output", default="./baidu_images", help="输出目录")
    args = p.parse_args()

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    engine = BaiduImageSearch()
    results = engine.search_all(args.keyword, total=args.count * 2)
    print(f"搜索到 {len(results)} 条结果")

    success = 0
    for i, img in enumerate(results, 1):
        if success >= args.count:
            break
        fp = out / f"baidu_{i:04d}.jpg"
        if engine.download(img["url"], str(fp)):
            size = os.path.getsize(str(fp)) // 1024
            print(f"  [{success+1}/{args.count}] ✓ {fp.name} ({size}KB)")
            success += 1
        else:
            print(f"  [{i}] ✗ 失败")
        time.sleep(0.15)

    print(f"\n完成: {success}/{args.count} 张")
