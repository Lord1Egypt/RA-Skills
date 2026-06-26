#!/usr/bin/env python3
"""
微信公众号文章转 Markdown 工具
v1.3 - 完善页面滚动懒加载、图片下载和本地替换
"""

import argparse
import hashlib
import mimetypes
import os
import re
import sys
import time
import traceback
from datetime import datetime
from urllib.parse import urlparse, unquote

try:
    from playwright.sync_api import sync_playwright
    from bs4 import BeautifulSoup
    import frontmatter
    import markdownify
    import requests
    from requests import Session
except ImportError:
    print("错误：缺少依赖库")
    print("请运行：pip install playwright beautifulsoup4 python-frontmatter markdownify requests")
    print("然后运行：playwright install chromium")
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description="抓取微信公众号文章并转换为 Markdown"
    )
    parser.add_argument("url", help="微信公众号文章链接")
    parser.add_argument("-o", "--output", help="输出文件路径")
    parser.add_argument("--output-dir", help="输出目录（自动生成文件名）")
    parser.add_argument("--headed", action="store_true", help="使用可视浏览器（默认无头模式）")
    parser.add_argument("--wait", action="store_true", help="等待用户确认后抓取（仅在 --headed 模式有效）")
    parser.add_argument("--timeout", type=int, default=30000, help="页面加载超时时间（毫秒）")
    parser.add_argument("--download-images", action="store_true", help="下载图片到本地 images/ 目录")
    args = parser.parse_args()

    if args.wait and not args.headed:
        print("⚠️  警告：--wait 选项需要配合 --headed 使用")
        print("   自动切换到可视浏览器模式...")
        args.headed = True

    return args


def generate_slug(title):
    """从标题生成 slug"""
    slug = re.sub(r'[^\w\u4e00-\u9fff]+', '-', title)
    slug = slug.strip('-')
    words = slug.split('-')[:6]
    return '-'.join(words)


def get_output_path(url, title, output_dir=None):
    """生成输出文件路径"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = generate_slug(title)

    if output_dir:
        base_dir = output_dir
    else:
        base_dir = "./wechat-articles"

    date_dir = os.path.join(base_dir, date_str)
    os.makedirs(date_dir, exist_ok=True)

    md_path = os.path.join(date_dir, f"{slug}.md")

    counter = 1
    while os.path.exists(md_path):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        md_path = os.path.join(date_dir, f"{slug}-{timestamp}.md")
        counter += 1
        if counter > 10:
            break

    return md_path


# ---------------------------------------------------------------------------
# 微信图片专项处理
# ---------------------------------------------------------------------------

def _is_svg_placeholder(src):
    """判断 src 是否是微信常见的 1x1 SVG 占位图"""
    if not src:
        return True
    return src.startswith("data:image/svg+xml")


def _normalize_image_url(url):
    """标准化图片 URL，去掉空白和片段。"""
    if not url:
        return None

    normalized = str(url).strip()
    if not normalized:
        return None

    if normalized.startswith("//"):
        normalized = f"https:{normalized}"

    if normalized.startswith("http"):
        return normalized.split("#", 1)[0]

    return None


def _pick_real_image_url(img_tag):
    """
    按可靠性优先级从 img 标签中提取真实图片 URL。
    微信公众号页面的懒加载机制会把真实 URL 放在 data-* 属性里，
    src 则塞入一个 1x1 SVG 占位图。

    优先级：
      1. data-src          — 微信最常见的懒加载字段
      2. data-original     — 部分历史模板使用
      3. data-actualsrc    — 极少数旧版编辑器
      4. data-croporisrc   — 裁剪后的原图
      5. src               — 兜底，如果不是占位图则可用
    """
    candidates = [
        img_tag.get("data-src"),
        img_tag.get("data-original"),
        img_tag.get("data-actualsrc"),
        img_tag.get("data-croporisrc"),
        img_tag.get("data-cover"),
    ]
    for url in candidates:
        normalized = _normalize_image_url(url)
        if normalized:
            return normalized

    # 兜底：src 本身不是占位图时才采用
    src = img_tag.get("src", "")
    normalized_src = _normalize_image_url(src)
    if normalized_src and not _is_svg_placeholder(src):
        return normalized_src

    return None


def _is_tiny_or_decorative(img_tag):
    """判断图片是否是装饰性小图或占位图，不应该被下载。"""
    try:
        # 检查 data-w 和 data-ratio 来判断尺寸
        data_w = img_tag.get("data-w")
        data_ratio = img_tag.get("data-ratio")
        if data_w and data_ratio:
            w = float(data_w)
            h = w * float(data_ratio)
            if w < 50 and h < 50:  # 小于 50x50 的图片跳过
                return True
        
        # 检查 src 是否是 data:image/svg+xml 或极小
        src = img_tag.get("src", "")
        if _is_svg_placeholder(src):
            return True
        if src.startswith("data:image/") and len(src) < 200:  # 极小的 base64 图片跳过
            return True
    except (ValueError, TypeError):
        pass
    
    return False


def fix_wechat_images(content_soup):
    """
    遍历内容区 DOM，将所有 img 的 src 替换为真实图片地址。
    必须在调用 markdownify 之前执行，否则 markdownify 会吃到占位图。
    返回被修复的图片数量。
    """
    fixed = 0
    removed = 0
    skipped = 0
    for img in content_soup.find_all("img"):
        real_url = _pick_real_image_url(img)
        if real_url:
            old_src = img.get("src", "")
            if old_src != real_url:
                img["src"] = real_url
                fixed += 1
            if str(img.get("title", "")).strip().lower() in {"null", "none"}:
                del img["title"]
            if img.get("data-src"):
                img["data-src"] = real_url
            if img.get("data-original"):
                img["data-original"] = real_url
            if img.get("data-actualsrc"):
                img["data-actualsrc"] = real_url
            if img.get("srcset"):
                del img["srcset"]
        else:
            # 既没有 data-src 也没有有效 src，移除这个无用 img 标签
            img.decompose()
            removed += 1
    return fixed, removed


# ---------------------------------------------------------------------------
# 图片下载
# ---------------------------------------------------------------------------

def _url_to_filename(url, index):
    """从 URL 生成一个稳定、可读的文件名"""
    url = _normalize_image_url(url) or url
    # 取 URL hash 的前 8 位作为唯一标识
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

    # 尝试从 URL 猜测扩展名
    ext = ".jpg"  # 默认
    if "wx_fmt=" in url:
        fmt = url.split("wx_fmt=")[1].split("&")[0].split("#")[0]
        fmt_map = {"jpeg": ".jpg", "jpg": ".jpg", "png": ".png",
                   "gif": ".gif", "webp": ".webp", "svg": ".svg"}
        ext = fmt_map.get(fmt, f".{fmt}")
    else:
        path = urlparse(url).path
        if "." in os.path.basename(path):
            ext = os.path.splitext(path)[1][:5]  # 限制长度

    return f"img_{index:02d}_{url_hash}{ext}"


def _pick_extension_from_response(img_url, response):
    """优先根据响应头补全图片扩展名。"""
    content_type = (response.headers.get("Content-Type") or "").split(";", 1)[0].strip()
    if content_type.startswith("image/"):
        ext = mimetypes.guess_extension(content_type)
        if ext == ".jpe":
            return ".jpg"
        if ext:
            return ext

    return os.path.splitext(_url_to_filename(img_url, 0))[1] or ".jpg"


def _parse_markdown_image(match):
    """解析 markdownify 生成的图片语法，兼容可选 title。"""
    alt_text = match.group(1)
    img_url = (match.group(2) or "").strip()
    if img_url.startswith("<") and img_url.endswith(">"):
        img_url = img_url[1:-1].strip()
    return alt_text, img_url


def _build_image_session(referer_url=None, cookies=None):
    """为微信图片下载构建带请求头和 Cookie 的 Session。"""
    session = Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/122.0.0.0 Safari/537.36",
        "Referer": referer_url or "https://mp.weixin.qq.com/",
        "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    })
    for cookie in cookies or []:
        name = cookie.get("name")
        value = cookie.get("value")
        domain = cookie.get("domain") or None
        path = cookie.get("path") or "/"
        if name and value is not None:
            session.cookies.set(name, value, domain=domain, path=path)
    return session


def download_images(markdown_text, md_path, referer_url=None, cookies=None):
    """
    下载 Markdown 中所有图片到 images/ 目录，并将链接替换为相对路径。
    单张下载失败不会中断整个流程，仅打印警告并保留原 URL。
    返回 (替换后的 markdown, 成功数, 失败数)。
    """
    images_dir = os.path.join(os.path.dirname(md_path), "images")
    os.makedirs(images_dir, exist_ok=True)

    # 匹配 Markdown 图片语法 ![alt](url)
    img_pattern = re.compile(r'!\[([^\]]*)\]\((\S+?)(?:\s+"[^"]*")?\)')
    matches = list(img_pattern.finditer(markdown_text))

    if not matches:
        return markdown_text, 0, 0

    success = 0
    failed = 0
    skipped = 0
    replacements = []

    session = _build_image_session(referer_url=referer_url, cookies=cookies)

    for i, m in enumerate(matches):
        alt_text, img_url = _parse_markdown_image(m)
        img_url = _normalize_image_url(img_url)

        # 跳过已经是本地路径的
        if not img_url:
            continue
            
        # 过滤明显不是文章图片的 URL（比如微信图标、装饰性小图）
        if "mmbiz.qpic.cn" not in img_url and "res.wx.qq.com" in img_url:
            print(f"  ⏭️  图片 {i}: 微信资源图片，跳过")
            skipped += 1
            continue

        filename = _url_to_filename(img_url, i)
        local_path = os.path.join(images_dir, filename)
        relative_path = f"images/{filename}"

        try:
            resp = session.get(img_url, timeout=30)
            resp.raise_for_status()

            content_type = (resp.headers.get("Content-Type") or "").lower()
            if content_type and not content_type.startswith("image/"):
                raise ValueError(f"返回内容不是图片：{content_type}")

            # 检查返回的内容是否像图片（至少 200 字节）
            if len(resp.content) < 200:
                print(f"  ⏭️  图片 {i} 内容太小（{len(resp.content)} 字节），可能是占位图，跳过")
                skipped += 1
                continue

            real_ext = _pick_extension_from_response(img_url, resp)
            if not local_path.endswith(real_ext):
                local_path = os.path.join(
                    images_dir,
                    f"{os.path.splitext(filename)[0]}{real_ext}"
                )
                relative_path = f"images/{os.path.basename(local_path)}"

            with open(local_path, "wb") as f:
                f.write(resp.content)

            replacements.append((m.group(0), f"![{alt_text}]({relative_path})"))
            success += 1
            print(f"  ✅ 图片 {i} 下载成功: {os.path.basename(local_path)}")
        except Exception as e:
            print(f"  ⚠️  下载图片 {i} 失败，保留原链接: {e}")
            failed += 1

    # 应用替换
    result = markdown_text
    for old, new in replacements:
        result = result.replace(old, new, 1)

    if skipped > 0:
        print(f"  ⏭️  共跳过 {skipped} 张装饰性/占位图")

    return result, success, failed


# ---------------------------------------------------------------------------
# 内容提取与转换
# ---------------------------------------------------------------------------

def extract_wechat_content(html):
    """从 HTML 中提取微信公众号文章内容"""
    soup = BeautifulSoup(html, "html.parser")

    # 提取标题
    title = ""
    title_elem = (soup.find("h1", class_="rich_media_title")
                  or soup.find("h1", id="activity-name"))
    if title_elem:
        title = title_elem.get_text(strip=True)

    # 提取作者
    author = ""
    author_elem = (soup.find("a", class_="rich_media_meta rich_media_meta_text")
                   or soup.find("span", class_="rich_media_meta rich_media_meta_text"))
    if author_elem:
        author = author_elem.get_text(strip=True)

    # 提取发布时间
    published_at = ""
    time_elem = (soup.find("em", id="publish_time")
                 or soup.find("span", class_="rich_media_meta rich_media_meta_text"))
    if time_elem:
        published_at = time_elem.get_text(strip=True)

    # 提取正文内容
    content_elem = (soup.find("div", class_="rich_media_content")
                    or soup.find("div", id="js_content"))

    content_html = ""
    img_fixed = 0
    img_removed = 0
    if content_elem:
        # *** 核心修复：在转 Markdown 之前先修复图片链接 ***
        img_fixed, img_removed = fix_wechat_images(content_elem)
        content_html = str(content_elem)

    return {
        "title": title,
        "author": author,
        "published_at": published_at,
        "content_html": content_html,
        "img_fixed": img_fixed,
        "img_removed": img_removed,
    }


def html_to_markdown(html):
    """HTML 转 Markdown（使用 markdownify）"""
    soup = BeautifulSoup(html, "html.parser")
    for elem in soup(["script", "style"]):
        elem.decompose()

    md = markdownify.markdownify(str(soup))
    return md.strip()


def main():
    args = parse_args()

    print("=" * 60)
    print("微信公众号文章转 Markdown 工具 v1.3")
    print("=" * 60)

    parsed_url = urlparse(args.url)
    if "mp.weixin.qq.com" not in parsed_url.netloc:
        print("⚠️  警告：这看起来不是微信公众号文章链接")
        print("   建议使用 mp.weixin.qq.com 域名的链接")

    with sync_playwright() as p:
        print("\n🚀 启动浏览器...")

        browser = p.chromium.launch(headless=not args.headed)
        page = browser.new_page()

        try:
            print(f"📡 访问页面：{args.url}")
            page.goto(args.url, timeout=args.timeout)

            if args.wait:
                print("\n⏳ 等待模式：请在浏览器中确认页面加载完成")
                print("   完成后按 Enter 继续...")
                input()

            print("\n🔍 等待页面稳定...")
            page.wait_for_load_state("networkidle", timeout=args.timeout)

            print("\n📜 滚动页面触发懒加载图片...")
            # 微信公众号文章通常有懒加载图片，滚动可以触发加载
            scroll_height = page.evaluate("document.body.scrollHeight")
            viewport_height = page.viewport_size["height"]
            current_scroll = 0
            step = viewport_height // 2  # 每次滚动半屏
            
            while current_scroll < scroll_height:
                page.evaluate(f"window.scrollTo(0, {current_scroll})")
                time.sleep(0.3)  # 等待图片加载
                current_scroll += step
                # 重新获取滚动高度（可能因为内容加载而变长）
                scroll_height = page.evaluate("document.body.scrollHeight")
            
            # 回到顶部
            page.evaluate("window.scrollTo(0, 0)")
            time.sleep(0.5)  # 等待稳定

            html = page.content()

            # 提取内容（内部会修复图片链接）
            print("📝 提取文章内容...")
            content = extract_wechat_content(html)

            if not content["title"]:
                content["title"] = "微信文章"
                print("⚠️  未能提取到标题，使用默认标题")

            print(f"   标题：{content['title']}")
            print(f"   作者：{content['author']}")
            print(f"   发布时间：{content['published_at']}")
            print(f"   🖼️  图片修复：{content['img_fixed']} 张替换为真实地址，"
                  f"{content['img_removed']} 张无效图片已移除")

            # 转换为 Markdown
            print("🔄 转换为 Markdown...")
            markdown_content = html_to_markdown(content["content_html"])

            # 构建 front matter
            post = frontmatter.Post(markdown_content)
            post.metadata["url"] = args.url
            post.metadata["title"] = content["title"]
            post.metadata["author"] = content["author"]
            post.metadata["published_at"] = content["published_at"]
            post.metadata["captured_at"] = datetime.now().isoformat()

            # 确定输出路径
            if args.output:
                md_path = args.output
            else:
                md_path = get_output_path(args.url, content["title"], args.output_dir)

            html_path = md_path.replace(".md", "-captured.html")

            os.makedirs(os.path.dirname(md_path), exist_ok=True)

            # 下载图片（如果启用）
            if args.download_images:
                print("📥 下载图片到本地...")
                md_text = frontmatter.dumps(post)
                md_text, dl_ok, dl_fail = download_images(
                    md_text,
                    md_path,
                    referer_url=args.url,
                    cookies=page.context.cookies(),
                )
                print(f"   ✅ 成功下载 {dl_ok} 张，❌ 失败 {dl_fail} 张")

                # 直接写替换后的文本
                print(f"💾 保存 Markdown：{md_path}")
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(md_text)
            else:
                print(f"💾 保存 Markdown：{md_path}")
                with open(md_path, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))

            print(f"💾 保存 HTML 快照：{html_path}")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html)

            print("\n✅ 完成！")
            print(f"   Markdown：{md_path}")
            print(f"   HTML 快照：{html_path}")
            if args.download_images:
                images_dir = os.path.join(os.path.dirname(md_path), "images")
                print(f"   图片目录：{images_dir}")

        except Exception as e:
            print(f"\n❌ 错误：{e}")
            traceback.print_exc()
            return 1

        finally:
            browser.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
