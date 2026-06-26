#!/usr/bin/env python3
"""
从笔趣阁目录页获取所有章节的正确 URL 映射
"""

import re
import json
import logging
from pathlib import Path
import subprocess

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def fetch_html(url):
    """使用 curl 获取 HTML"""
    cmd = [
        "curl", "-s", "-L", "--max-time", "30",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        url,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
    return result.stdout if result.returncode == 0 else None


def parse_catalog(html, book_id):
    """解析目录页，提取章节映射"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, "html.parser")
    chapters = []
    
    # 查找所有章节链接
    for a in soup.find_all("a", href=re.compile(rf"/{book_id}/\d+")):
        href = a.get("href", "")
        title = a.get_text(strip=True)
        
        if not href or not title:
            continue
        
        # 解析章节号
        ch_match = re.search(r"第\s*(\d+)\s*章", title)
        if not ch_match:
            continue
        
        ch_num = int(ch_match.group(1))
        url_id = href.split("/")[-1].replace(".html", "")
        full_url = f"https://www.bqquge.com{href}"
        
        chapters.append({
            "number": ch_num,
            "url_id": url_id,
            "url": full_url,
            "title": title,
        })
    
    # 按章节号排序
    chapters.sort(key=lambda x: x["number"])
    
    return chapters


def main():
    book_id = "4"  # 没钱修什么仙的书 ID
    catalog_url = f"https://www.bqquge.com/{book_id}"  # 正确的目录页 URL
    
    logger.info(f"📚 获取目录页：{catalog_url}")
    html = fetch_html(catalog_url)
    
    if not html:
        logger.error("❌ 无法获取目录页")
        return
    
    logger.info("🔍 解析章节列表...")
    chapters = parse_catalog(html, book_id)
    
    if not chapters:
        logger.error("❌ 未找到任何章节")
        return
    
    logger.info(f"✅ 找到 {len(chapters)} 章")
    logger.info(f"📖 范围：第{chapters[0]['number']}章 - 第{chapters[-1]['number']}章")
    
    # 检查 URL ID 是否连续
    gaps = []
    for i in range(1, len(chapters)):
        if int(chapters[i]["url_id"]) - int(chapters[i-1]["url_id"]) > 1:
            gaps.append({
                "from_ch": chapters[i-1]["number"],
                "to_ch": chapters[i]["number"],
                "from_url": chapters[i-1]["url_id"],
                "to_url": chapters[i]["url_id"],
            })
    
    if gaps:
        logger.info(f"\n⚠️ 发现 {len(gaps)} 处 URL ID 跳跃:")
        for gap in gaps[:5]:
            logger.info(f"  第{gap['from_ch']}章 (URL {gap['from_url']}) → 第{gap['to_ch']}章 (URL {gap['to_url']})")
        if len(gaps) > 5:
            logger.info(f"  ... 还有 {len(gaps)-5} 处")
    
    # 保存映射
    output_file = Path.home() / ".openclaw" / "workspace" / "skills" / "novel-scraper" / "state" / f"book_{book_id}_catalog.json"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chapters, f, ensure_ascii=False, indent=2)
    
    logger.info(f"\n💾 已保存到：{output_file}")
    
    # 生成 URL 列表（从第 116 章开始）
    start_ch = 116
    filtered = [ch for ch in chapters if ch["number"] >= start_ch]
    
    if filtered:
        urls = ",".join([ch["url"] for ch in filtered])
        logger.info(f"\n📋 第{start_ch}章起的 URL 列表:")
        logger.info(f"  共{len(filtered)}章")
        logger.info(f"  URL: {urls[:200]}...")
        
        # 保存到文件
        url_file = output_file.with_suffix(".urls.txt")
        with open(url_file, "w", encoding="utf-8") as f:
            f.write(urls)
        logger.info(f"  完整列表已保存到：{url_file}")


if __name__ == "__main__":
    main()
