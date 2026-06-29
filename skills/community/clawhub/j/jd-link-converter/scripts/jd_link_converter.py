#!/usr/bin/env python3
"""
京东链接转换工具 - 将京东移动端分享短链接/长链接转换为PC端链接

支持输入格式:
  1. 京东短链接: https://3.cn/xxxxxxx 或 https://u.jd.com/xxxxxxx
  2. 移动端商品链接: https://item.m.jd.com/product/{id}.html?...
  3. 移动端商品链接(无product): https://item.m.jd.com/{id}.html?...
  4. PC端商品链接(含多余参数): https://item.jd.com/{id}.html?...

输出:
  PC端纯净商品链接: https://item.jd.com/{id}.html
"""

import re
import sys
import json
import urllib.request
import urllib.error


def resolve_short_url(url: str, max_redirects: int = 8) -> str:
    """
    解析京东短链接，手动跟踪重定向获取实际URL。
    支持 3.cn 和 u.jd.com 短链接。

    3.cn 短链接需要模拟京东 App 的 User-Agent 才能正确跳转到商品页，
    否则会被重定向到京东首页。

    Args:
        url: 短链接URL
        max_redirects: 最大重定向次数

    Returns:
        最终重定向后的URL
    """
    # 京东 App 分享链接的 User-Agent，确保 3.cn 能正确跳转
    mobile_ua = "jdapp;iPhone;13.2.0;16.2;network/wifi;Mozilla/5.0 (iPhone; CPU iPhone OS 16_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1"

    current_url = url
    for _ in range(max_redirects):
        try:
            req = urllib.request.Request(
                current_url,
                method="GET",
                headers={
                    "User-Agent": mobile_ua,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9",
                },
            )
            # 不自动跟随重定向，手动处理以捕获每一跳
            class NoRedirect(urllib.request.HTTPRedirectHandler):
                def redirect_request(self, req, fp, code, msg, headers, newurl):
                    return None

            opener = urllib.request.build_opener(NoRedirect, urllib.request.HTTPHandler)
            try:
                resp = opener.open(req, timeout=10)
                final_url = resp.url
                resp.close()
                # 如果已到达商品页，直接返回
                if "item.m.jd.com" in final_url or "item.jd.com" in final_url:
                    return final_url
                current_url = final_url
            except urllib.error.HTTPError as e:
                if e.code in (301, 302, 303, 307, 308):
                    location = e.headers.get("Location", "")
                    if location:
                        # 处理相对路径
                        if location.startswith("/"):
                            from urllib.parse import urljoin
                            location = urljoin(current_url, location)
                        if "item.m.jd.com" in location or "item.jd.com" in location:
                            return location
                        current_url = location
                        continue
                # 非重定向错误，尝试用PC UA重试
                break
        except Exception:
            break

    # 回退: 用PC浏览器UA重试一次
    try:
        req = urllib.request.Request(
            url,
            method="GET",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            },
        )
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.url
    except Exception:
        return current_url


def extract_product_id(url: str) -> str | None:
    """
    从URL中提取京东商品ID。

    支持格式:
      - https://item.m.jd.com/product/100198170140.html
      - https://item.m.jd.com/100198170140.html
      - https://item.jd.com/100198170140.html
      - https://item.jd.com/100198170140.html?xxx=yyy
      - 纯数字ID

    Args:
        url: 商品URL

    Returns:
        商品ID字符串，未找到返回None
    """
    # 匹配 item.m.jd.com/product/{id}.html 或 item.jd.com/{id}.html
    patterns = [
        r"item\.m\.jd\.com/product/(\d+)\.html",
        r"item\.m\.jd\.com/(\d+)\.html",
        r"item\.jd\.com/(\d+)\.html",
        r"item\.jd\.com/(\d+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # 尝试纯数字（可能是直接传入的ID）
    if re.fullmatch(r"\d{6,}", url.strip()):
        return url.strip()

    return None


def convert_jd_link(input_url: str) -> dict:
    """
    将京东链接（短链接/移动端链接/PC端链接）转换为PC端纯净链接。

    Args:
        input_url: 输入的京东链接

    Returns:
        转换结果字典，包含:
          - original: 原始输入
          - resolved: 短链接解析后的实际URL（若输入为短链接）
          - product_id: 商品ID
          - pc_url: PC端纯净链接
          - error: 错误信息（如有）
    """
    result = {
        "original": input_url,
        "resolved": None,
        "product_id": None,
        "pc_url": None,
        "error": None,
    }

    url = input_url.strip()

    # Step 1: 判断是否为短链接，需要先解析
    is_short = bool(re.match(r"https?://(3\.cn|u\.jd\.com)/", url))

    if is_short:
        resolved = resolve_short_url(url)
        result["resolved"] = resolved
        url = resolved

    # Step 2: 提取商品ID
    product_id = extract_product_id(url)

    if not product_id:
        result["error"] = f"无法从URL中提取商品ID: {url}"
        return result

    result["product_id"] = product_id

    # Step 3: 生成PC端纯净链接
    result["pc_url"] = f"https://item.jd.com/{product_id}.html"

    return result


def batch_convert(input_urls: list[str]) -> list[dict]:
    """
    批量转换京东链接。

    Args:
        input_urls: 输入URL列表

    Returns:
        转换结果列表
    """
    return [convert_jd_link(url) for url in input_urls]


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: jd_link_converter.py <url1> [url2] [url3] ...")
        print("       echo '<url>' | jd_link_converter.py")
        print()
        print("支持的URL格式:")
        print("  - 京东短链接: https://3.cn/xxxxxxx")
        print("  - 京东短链接: https://u.jd.com/xxxxxxx")
        print("  - 移动端链接: https://item.m.jd.com/product/{id}.html?...")
        print("  - PC端链接:   https://item.jd.com/{id}.html?...")
        sys.exit(1)

    urls = sys.argv[1:]

    # 支持管道输入
    if not urls and not sys.stdin.isatty():
        urls = [line.strip() for line in sys.stdin if line.strip()]

    results = batch_convert(urls)

    # 输出JSON结果
    print(json.dumps(results, ensure_ascii=False, indent=2))

    # 同时输出简洁版
    print("\n--- 简洁结果 ---")
    for r in results:
        if r["pc_url"]:
            print(f"{r['original']}")
            print(f"  -> {r['pc_url']}")
        else:
            print(f"{r['original']}")
            print(f"  -> 错误: {r['error']}")


if __name__ == "__main__":
    main()
