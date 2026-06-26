#!/usr/bin/env python3
"""
nexus-reader: 微信读书飙升榜每日推荐卡片生成器

两阶段架构：
  阶段1 - 抓数据：python reader.py --fetch-only
  阶段2 - 渲染卡片：python reader.py --card <json_path> [--png]

流程：
  1. --fetch-only    抓取飙升榜数据，输出 JSON 到 data/ 目录
  2. LLM 选书 + 创作内容（宜忌/金句/标题/推荐语），生成完整 card JSON
  3. --card <json>   读取 LLM 生成的 JSON，渲染 HTML 卡片
  4. --png           额外生成 PNG 图片
"""

import requests
from bs4 import BeautifulSoup
import json
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# ===== 配置 =====
SOURCE_URL = "https://weread.qq.com/web/category/rising"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "data")

# 农历月名（简化版，实际可用 lunarcalendar 库）
LUNAR_MONTHS = ["正月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "冬月", "腊月"]


# ============================================================
# 阶段1：抓取飙升榜数据
# ============================================================

def fetch_trending_books(force=False, cache_hours=1):
    """
    从微信读书飙升榜抓取书籍数据
    支持缓存机制：当天数据文件 < cache_hours 小时则跳过重新抓取
    """
    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.abspath(DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)

    cache_file = os.path.join(output_dir, f"weread_rising_{today}.json")

    # 检查缓存
    if not force and os.path.exists(cache_file):
        file_age_hours = (datetime.now().timestamp() - os.path.getmtime(cache_file)) / 3600
        if file_age_hours < cache_hours:
            with open(cache_file, "r", encoding="utf-8") as f:
                books = json.load(f)
            print(f"[缓存] 使用本地缓存数据 ({len(books)} 本书，{file_age_hours:.1f}小时前)")
            return books

    # 抓取页面
    print(f"[抓取] 正在获取微信读书飙升榜: {SOURCE_URL}")
    headers = {"User-Agent": USER_AGENT}

    try:
        resp = requests.get(SOURCE_URL, headers=headers, timeout=15)
        resp.encoding = "utf-8"
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[错误] 请求失败: {e}")
        # 尝试使用旧缓存
        if os.path.exists(cache_file):
            with open(cache_file, "r", encoding="utf-8") as f:
                books = json.load(f)
            print(f"[降级] 使用旧缓存数据 ({len(books)} 本书)")
            return books
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    books = []

    items = soup.find_all(class_="wr_bookList_item")
    print(f"[解析] 找到 {len(items)} 个书籍项")

    for item in items:
        try:
            # 排名
            index_elem = item.find(class_="wr_bookList_item_index")
            index = index_elem.get_text(strip=True) if index_elem else ""

            # 书名
            title_elem = item.find(class_="wr_bookList_item_title")
            title = title_elem.get_text(strip=True) if title_elem else ""

            # 作者
            author_elem = item.find(class_="wr_bookList_item_author")
            author = author_elem.get_text(strip=True) if author_elem else ""

            # 简介
            desc_elem = item.find(class_="wr_bookList_item_desc")
            desc = desc_elem.get_text(strip=True) if desc_elem else ""

            # 封面
            cover_img = item.find(class_="wr_bookCover_img")
            cover_url = ""
            if cover_img and cover_img.get("src"):
                cover_url = cover_img["src"]

            # 书籍链接
            link_elem = item.find(class_="wr_bookList_item_link")
            book_url = ""
            if link_elem and link_elem.get("href"):
                book_url = "https://weread.qq.com" + link_elem["href"]

            # 阅读人数
            reading_elem = item.find(class_="wr_bookList_item_reading_number")
            reading_count = reading_elem.get_text(strip=True) if reading_elem else ""

            # 推荐值
            rating_elem = item.find(class_="wr_bookList_item_reading_percent")
            rating = rating_elem.get_text(strip=True) if rating_elem else ""

            if title:
                books.append({
                    "index": index,
                    "title": title,
                    "author": author,
                    "desc": desc,
                    "cover_url": cover_url,
                    "book_url": book_url,
                    "reading_count": reading_count,
                    "rating": rating,
                    "date": today,
                })
        except Exception as e:
            print(f"[警告] 解析书籍项时出错: {e}")
            continue

    # 保存JSON缓存
    if books:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(books, f, ensure_ascii=False, indent=2)
        print(f"[保存] 数据已缓存: {cache_file}")

    return books


# ============================================================
# 阶段2：渲染卡片 HTML
# ============================================================

def render_card_html(card_data, template_path=None):
    """
    从 LLM 生成的 card JSON 渲染 HTML 卡片
    使用 template.html 模板，替换 {{key}} 占位符

    card_data 结构（由 LLM 生成）:
    {
      "date": "2026/05/04",
      "day": "04",
      "weekday": "星期日",
      "lunar_date": "农历 四月十八",
      "yi": "静心品读",
      "ji": "焦虑内耗",
      "title": "有一分热就去发光",        # 金句标题
      "book_title": "阿勒泰的角落",
      "book_author": "李娟",
      "book_desc": "...",                  # LLM 创作的推荐语
      "cover_url": "https://...",
      "book_url": "https://...",
      "rating": "88.4%",
      "reading_count": "1486"
    }
    """
    now = datetime.now()

    # 从 card_data 取值，带默认值
    date_str = card_data.get("date", now.strftime("%Y/%m"))
    day_str = card_data.get("day", now.strftime("%d"))
    weekday = card_data.get("weekday", ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][now.weekday()])
    lunar_date = card_data.get("lunar_date", "")
    yi = card_data.get("yi", "翻开书页")
    ji = card_data.get("ji", "虚度光阴")
    title = card_data.get("title", "每日一书")          # 金句标题
    book_title = card_data.get("book_title", "未知")
    book_author = card_data.get("book_author", "佚名")
    book_desc = card_data.get("book_desc", "")          # LLM 推荐语
    cover_url = card_data.get("cover_url", "")
    book_url = card_data.get("book_url", SOURCE_URL)
    rating = card_data.get("rating", "N/A")
    reading_count = card_data.get("reading_count", "0")

    # 推荐语截取（防过长）
    display_desc = book_desc[:300] + "..." if len(book_desc) > 300 else book_desc

    # 替换映射
    replacements = {
        "date": date_str,
        "day": day_str,
        "weekday": weekday,
        "lunar_date": lunar_date,
        "yi": yi,
        "ji": ji,
        "title": title,
        "book_title": book_title,
        "book_author": book_author,
        "book_desc": display_desc,
        "cover_url": cover_url,
        "book_url": book_url,
        "rating": rating,
        "reading_count": reading_count,
    }

    # 读取模板文件
    if template_path is None:
        template_path = os.path.join(SCRIPT_DIR, "template.html")
    if not os.path.exists(template_path):
        print(f"[错误] 模板文件不存在: {template_path}")
        return "<p>模板文件缺失</p>"

    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 替换所有 {{key}} 占位符
    for key, value in replacements.items():
        html = html.replace("{{" + key + "}}", str(value))

    return html


# ============================================================
# PNG 生成
# ============================================================

def html_to_png(html_path, png_path=None, width=480):
    """
    使用 Playwright 将 HTML 转为 PNG（截图方式）
    需要 playwright chromium 已安装：playwright install chromium
    """
    if png_path is None:
        png_path = html_path.replace(".html", ".png")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[错误] 需要安装 playwright: pip install playwright && playwright install chromium")
        return None

    abs_html = os.path.abspath(html_path)
    file_url = "file:///" + abs_html.replace("\\", "/")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": width, "height": 800})
            page.goto(file_url, wait_until="networkidle", timeout=15000)
            # 等待字体加载
            page.wait_for_timeout(2000)
            # 截图整个页面
            page.screenshot(path=png_path, full_page=True)
            browser.close()
        print(f"[PNG] 图片已生成: {png_path}")
        return png_path
    except Exception as e:
        print(f"[错误] PNG 生成失败: {e}")
        return None


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="nexus-reader: 微信读书飙升榜每日推荐卡片生成器",
        epilog="""
示例：
  # 阶段1：抓取飙升榜数据
  python reader.py --fetch-only

  # 阶段2：根据 JSON 渲染卡片
  python reader.py --card data/nexus-reader-20260504.json

  # 渲染卡片 + 生成 PNG
  python reader.py --card data/nexus-reader-20260504.json --png

  # 强制重新抓取
  python reader.py --fetch-only --force
        """
    )

    # 互斥的两种模式
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--fetch-only", action="store_true",
                       help="阶段1：只抓取飙升榜数据，输出 JSON")
    group.add_argument("--card", type=str, metavar="JSON_PATH",
                       help="阶段2：读取 LLM 生成的 card JSON，渲染 HTML 卡片")

    # 通用参数
    parser.add_argument("--output", type=str, default=None,
                        help="输出目录（默认 data/）")
    parser.add_argument("--force", action="store_true",
                        help="强制重新抓取（忽略缓存）")
    parser.add_argument("--cache-hours", type=float, default=1,
                        help="缓存有效时间（小时，默认1）")
    parser.add_argument("--png", action="store_true",
                        help="额外生成 PNG 图片（需 --card 模式）")

    args = parser.parse_args()

    output_dir = args.output or os.path.abspath(DEFAULT_OUTPUT_DIR)
    os.makedirs(output_dir, exist_ok=True)

    # ===== 阶段1：抓取数据 =====
    if args.fetch_only:
        books = fetch_trending_books(force=args.force, cache_hours=args.cache_hours)
        if not books:
            print("[错误] 未获取到书籍数据")
            sys.exit(1)

        # 输出简要信息
        print(f"\n{'='*50}")
        print(f"飙升榜 TOP {len(books)}")
        print(f"{'='*50}")
        for b in books:
            rating_str = f" (推荐值: {b.get('rating', 'N/A')})" if b.get('rating') else ""
            print(f"  {b['index']}. 《{b['title']}》- {b['author']}{rating_str}")

        # JSON 路径
        today = datetime.now().strftime("%Y-%m-%d")
        json_path = os.path.join(output_dir, f"weread_rising_{today}.json")
        print(f"\n[数据] JSON已保存: {json_path}")
        print(f"[提示] 请 LLM 选书并创作内容，生成 card JSON 后用 --card 渲染")
        return

    # ===== 阶段2：渲染卡片 =====
    if args.card:
        card_json_path = args.card
        if not os.path.exists(card_json_path):
            print(f"[错误] JSON 文件不存在: {card_json_path}")
            sys.exit(1)

        with open(card_json_path, "r", encoding="utf-8") as f:
            card_data = json.load(f)

        # 渲染 HTML
        html = render_card_html(card_data)
        today = datetime.now().strftime("%Y%m%d")
        # 如果 card JSON 里有 index 字段，文件名带上序号区分
        book_index = card_data.get("index", "")
        suffix = f"-{book_index}" if book_index else ""
        html_path = os.path.join(output_dir, f"nexus-reader-{today}{suffix}.html")
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"[卡片] HTML已生成: {html_path}")

        # 生成 PNG
        if args.png:
            png_path = os.path.join(output_dir, f"nexus-reader-{today}{suffix}.png")
            result = html_to_png(html_path, png_path, width=480)
            if result:
                print(f"[完成] 卡片已生成: {html_path} + {png_path}")
            else:
                print(f"[完成] HTML卡片已生成: {html_path} (PNG生成失败)")
        else:
            print(f"[完成] HTML卡片已生成: {html_path}")


if __name__ == "__main__":
    main()
