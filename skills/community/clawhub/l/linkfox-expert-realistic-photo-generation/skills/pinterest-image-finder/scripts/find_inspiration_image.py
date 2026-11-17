#!/usr/bin/env python3
"""
Pinterest Image Finder - 搜索 Pinterest 灵感图并提取图片 URL

Usage:
  python find_inspiration_image.py '<JSON params>'
  python find_inspiration_image.py --stdin       # 从 stdin 读取 JSON

Params:
  keyword:      搜索关键词（必填）
  max_results:  最多返回结果数（默认 5）
"""

import json
import os
import re
import sys
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

API_PATH = "/tsearch/search"


def get_api_base():
    return (os.environ.get("LINKFOX_TOOL_GATEWAY") or "https://tool-gateway.linkfox.com").rstrip("/")


def get_api_key():
    key = os.environ.get("LINKFOX_AGENT_API_KEY") or os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(json.dumps({"status": "error", "message": "API Key 未配置"}), file=sys.stdout)
        sys.exit(1)
    return key


def search_pinterest(keyword):
    """调用 tsearch API 搜索 Pinterest"""
    api_url = get_api_base() + API_PATH
    api_key = get_api_key()
    search_query = f"site:pinterest.com {keyword}"
    data = json.dumps({"keyword": search_query}).encode("utf-8")
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
        "User-Agent": "LinkFox-Skill/2.0",
        "SESSION_ID": os.environ.get("SESSION_ID", ""),
        "MESSAGE_ID": os.environ.get("MESSAGE_ID", ""),
        "MODE_ID": os.environ.get("MODE_ID", ""),
        "APP_NAME": os.environ.get("APP_NAME", ""),
    }
    req = Request(api_url, data=data, headers=headers, method="POST")
    try:
        with urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result
    except (HTTPError, URLError, Exception) as e:
        print(json.dumps({"status": "error", "message": f"搜索请求失败: {str(e)}"}))
        sys.exit(1)


def extract_image_urls_from_content(content):
    """从搜索结果文本中正则提取图片 URL"""
    img_pattern = r'https?://[^\s"<>\'\\]+\.(?:jpg|jpeg|png|webp)(?:\?[^\s"<>\'\\]*)?'
    urls = re.findall(img_pattern, content, re.IGNORECASE)
    # 去重
    seen = set()
    unique = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            unique.append(u)
    return unique


def try_fetch_page_for_images(page_url, timeout=10):
    """尝试直接请求页面，从 HTML 中提取图片 URL"""
    try:
        req = Request(page_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urlopen(req, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="ignore")
            # 提取 i.pinimg.com 图片 URL
            pinimg_pattern = r'https://i\.pinimg\.com/[^\s"<>\'\\]+\.(?:jpg|jpeg|png|webp)'
            urls = re.findall(pinimg_pattern, html, re.IGNORECASE)
            # 也提取其他图片 URL
            if not urls:
                urls = extract_image_urls_from_content(html)
            # 去重
            seen = set()
            unique = []
            for u in urls:
                if u not in seen:
                    seen.add(u)
                    unique.append(u)
            return unique
    except Exception:
        return []


def resolve_session_dir():
    """按会话目录规则解析输出路径"""
    import datetime
    session_id = os.environ.get("SESSION_ID", "default")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    cwd = os.getcwd()
    session_dir = os.path.join(cwd, "linkfox", today, session_id, "data")
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


def save_result(result):
    """将完整结果落盘到会话目录"""
    import time
    session_dir = resolve_session_dir()
    filename = f"pinterest-image-finder-{int(time.time() * 1000000)}.json"
    filepath = os.path.join(session_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return filepath


def main():
    # 读取参数
    if "--stdin" in sys.argv:
        params = json.loads(sys.stdin.read())
    elif len(sys.argv) > 1 and sys.argv[1] != "--stdin":
        params = json.loads(sys.argv[1])
    else:
        params = json.loads(sys.stdin.read())

    keyword = params.get("keyword", "").strip()
    max_results = params.get("max_results", 5)

    if not keyword:
        print(json.dumps({"status": "error", "message": "keyword 参数必填"}))
        sys.exit(1)

    # Step 1: 搜索 Pinterest
    search_result = search_pinterest(keyword)
    search_list = search_result.get("searchList", [])

    if not search_list:
        result = {
            "status": "error",
            "message": "搜索无结果",
            "image_urls": [],
            "page_urls": [],
            "fallback": False,
        }
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)

    # Step 2: 从搜索结果内容中提取图片 URL
    all_image_urls = []
    page_urls = []
    for item in search_list[:max_results * 2]:
        url = item.get("url", "")
        content = item.get("content", "")
        if url:
            page_urls.append(url)
        # 从内容中提取图片 URL
        imgs = extract_image_urls_from_content(content)
        all_image_urls.extend(imgs)

    # 去重
    seen = set()
    unique_images = []
    for u in all_image_urls:
        if u not in seen:
            seen.add(u)
            unique_images.append(u)

    # Step 3: 如果搜索结果中没有图片 URL，尝试直接请求页面
    if not unique_images and page_urls:
        for page_url in page_urls[:3]:
            imgs = try_fetch_page_for_images(page_url)
            unique_images.extend(imgs)
            if len(unique_images) >= max_results:
                break

    # 去重
    seen = set()
    final_images = []
    for u in unique_images:
        if u not in seen:
            seen.add(u)
            final_images.append(u)

    # Step 4: 构建结果
    if final_images:
        result = {
            "status": "success",
            "image_urls": final_images[:max_results],
            "page_urls": page_urls[:max_results],
            "fallback": False,
            "search_keyword": keyword,
        }
    elif page_urls:
        result = {
            "status": "partial",
            "image_urls": [],
            "page_urls": page_urls[:max_results],
            "fallback": True,
            "search_keyword": keyword,
            "message": "未能自动提取图片 URL，请手动访问 page_urls 中的链接，选一张图上传",
        }
    else:
        result = {
            "status": "error",
            "image_urls": [],
            "page_urls": [],
            "fallback": True,
            "search_keyword": keyword,
            "message": "搜索无有效结果",
        }

    # 落盘
    saved_path = save_result(result)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
