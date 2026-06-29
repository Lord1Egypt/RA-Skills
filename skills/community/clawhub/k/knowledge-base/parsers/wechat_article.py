#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章解析器
用法: （由 agent.py 直接调用 web_fetch，本文件提供解析函数）
"""

import re
import json
from datetime import datetime


def parse_wechat_html(html: str, url: str = "") -> dict:
    """
    解析微信公众号文章 HTML，提取标题/作者/正文/发布时间。
    由 agent.py 调用 web_fetch 获取 HTML 后，传入本函数解析。
    """
    result = {
        "title": "",
        "author": "",
        "content": "",
        "pub_time": "",
        "url": url,
    }

    # 提取标题
    m = re.search(r"<h1[^>]*class=\"rich_media_title\"[^>]*>(.*?)</h1>", html, re.DOTALL)
    if not m:
        m = re.search(r"<title>(.+?)</title>", html)
    if m:
        result["title"] = _clean(m.group(1))

    # 提取作者（公众号名）
    m = re.search(r"var\s+nickname\s*=\s*\"([^\"]+)\"", html)
    if not m:
        m = re.search(r"rich_media_meta_text[^\"]*>\s*([^<]+)<", html)
    if m:
        result["author"] = _clean(m.group(1))

    # 提取发布时间
    m = re.search(r"var\s+publish_time\s*=\s*\"([^\"]+)\"", html)
    if not m:
        m = re.search(r"rich_media_meta_text[^\"]*>\s*(\d{4}-\d{2}-\d{2})", html)
    if m:
        result["pub_time"] = _clean(m.group(1))

    # 提取正文（js_content 区域）
    m = re.search(r"<div\s+id=\"js_content\"[^>]*>(.*?)</div>\s*<script", html, re.DOTALL)
    if m:
        content_html = m.group(1)
        # 简单转 markdown：保留图片，去掉其他标签
        content = _html_to_markdown(content_html)
        result["content"] = content
    else:
        # 兜底：取 body 内文字
        m = re.search(r"<body[^>]*>(.*?)</body>", html, re.DOTALL)
        if m:
            result["content"] = _clean(m.group(1)[:2000])

    return result


def _clean(s: str) -> str:
    """去掉 HTML 标签和多余空白"""
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("&nbsp;", " ").replace("&amp;", "&")
    s = s.replace("&lt;", "<").replace("&gt;", ">")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _html_to_markdown(html: str) -> str:
    """把微信公众号正文 HTML 简易转成 markdown"""
    md = html
    # 图片
    md = re.sub(r'<img[^>]+data-src="([^"]+)"[^>]*>', r"![](\1)\n", md)
    md = re.sub(r'<img[^>]+src="([^"]+)"[^>]*>', r"![](\1)\n", md)
    # 标题
    md = re.sub(r"<h1[^>]*>(.*?)</h1>", r"# \1\n", md, flags=re.DOTALL)
    md = re.sub(r"<h2[^>]*>(.*?)</h2>", r"## \1\n", md, flags=re.DOTALL)
    md = re.sub(r"<h3[^>]*>(.*?)</h3>", r"### \1\n", md, flags=re.DOTALL)
    # 加粗
    md = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", md, flags=re.DOTALL)
    # 段落
    md = re.sub(r"<p[^>]*>(.*?)</p>", r"\1\n\n", md, flags=re.DOTALL)
    # 清理剩余标签
    md = re.sub(r"<[^>]+>", "", md)
    # 还原实体
    md = md.replace("&nbsp;", " ").replace("&amp;", "&")
    md = md.replace("&lt;", "<").replace("&gt;", ">")
    # 清理多余空行
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def make_markdown(article: dict) -> str:
    """把解析结果转成适合存腾讯文档的 markdown"""
    md = f"# {article['title']}\n\n"
    md += f"**公众号：** {article.get('author', '未知')}  \n"
    if article.get("pub_time"):
        md += f"**发布时间：** {article['pub_time']}  \n"
    md += f"**原文链接：** {article.get('url', '')}  \n\n"
    md += "---\n\n"
    md += article.get("content", "") + "\n"
    return md


# ── 独立测试 ──────────────────────────────────────────────────
def main():
    import sys, argparse
    parser = argparse.ArgumentParser(description="微信公众号文章解析（从 HTML 文件）")
    parser.add_argument("html_file", help="web_fetch 保存的 HTML 文件路径")
    parser.add_argument("--url", default="", help="原文链接")
    args = parser.parse_args()

    html = open(args.html_file, encoding="utf-8").read()
    article = parse_wechat_html(html, args.url)
    print(json.dumps(article, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
