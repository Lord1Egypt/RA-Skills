#!/usr/bin/env python3
"""
H5/小程序/链接可用性检测工具
检测：HTTP状态码、响应时间、SSL证书、跳转重定向、标题解析
Usage: python3 check_url.py <url> [--full]
       python3 check_url.py --batch urls.txt
"""
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime
from urllib.parse import urlparse

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


STATUS_COLORS = {
    "up": "✅",
    "warn": "⚠️",
    "down": "❌",
}


def check_url(url, timeout=10, follow_redirects=True, verify_ssl=True):
    """检查单个URL"""
    result = {
        "url": url,
        "status": "unknown",
        "http_code": None,
        "response_time_ms": None,
        "final_url": None,
        "title": None,
        "content_type": None,
        "error": None,
        "ssl": None,
        "recommendations": [],
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }

    try:
        start = time.time()
        resp = requests.get(
            url,
            headers=headers,
            timeout=timeout,
            allow_redirects=follow_redirects,
            verify=verify_ssl,
        )
        elapsed = (time.time() - start) * 1000
        result["response_time_ms"] = round(elapsed)
        result["http_code"] = resp.status_code
        result["final_url"] = resp.url
        result["content_type"] = resp.headers.get("Content-Type", "")

        # 解析标题
        if "text/html" in resp.headers.get("Content-Type", ""):
            try:
                import re
                title_match = re.search(r'<title[^>]*>([^<]+)</title>', resp.text, re.IGNORECASE)
                if title_match:
                    result["title"] = title_match.group(1).strip()
            except Exception:
                pass

        # 判断状态
        if resp.status_code == 200:
            if elapsed > 3000:
                result["status"] = "warn"
                result["recommendations"].append(f"响应时间过长（{round(elapsed)}ms > 3000ms）")
            elif "html" not in resp.headers.get("Content-Type", ""):
                result["status"] = "up"
            else:
                result["status"] = "up"
        elif resp.status_code in (301, 302, 303, 307, 308):
            result["status"] = "warn"
            result["recommendations"].append(f"存在重定向（HTTP {resp.status_code}）→ {resp.headers.get('Location','')}")
        elif resp.status_code in (400, 401, 403, 404):
            result["status"] = "warn"
            result["recommendations"].append(f"客户端错误（HTTP {resp.status_code}）")
        elif resp.status_code >= 500:
            result["status"] = "down"
            result["recommendations"].append(f"服务端错误（HTTP {resp.status_code}）")
        else:
            result["status"] = "warn"

    except requests.exceptions.SSLError as e:
        result["status"] = "down"
        result["error"] = f"SSL证书错误：{e}"
        result["recommendations"].append("检查SSL证书是否过期或配置错误")
    except requests.exceptions.Timeout:
        result["status"] = "down"
        result["error"] = f"请求超时（>{timeout}s）"
        result["recommendations"].append("检查服务器是否响应缓慢或网络问题")
    except requests.exceptions.ConnectionError as e:
        result["status"] = "down"
        result["error"] = f"连接失败：{str(e)[:100]}"
        result["recommendations"].append("检查域名解析和网络连通性")
    except Exception as e:
        result["status"] = "down"
        result["error"] = str(e)

    # SSL检查
    try:
        parsed = urlparse(url)
        if parsed.scheme == "https":
            import ssl
            import socket
            ctx = ssl.create_default_context()
            with socket.create_connection((parsed.netloc, 443), timeout=timeout) as sock:
                with ctx.wrap_socket(sock, server_hostname=parsed.netloc) as ssock:
                    cert = ssock.getpeercert()
                    result["ssl"] = {
                        "valid": True,
                        "subject": dict(x[0] for x in cert.get("subject", [])),
                        "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    }
    except Exception:
        pass

    return result


def print_result(r, verbose=False):
    """打印检测结果"""
    icon = STATUS_COLORS.get(r["status"], "❓")
    print(f"\n{icon} [{r['http_code'] or '---'}] {r['url']}")
    if r.get("final_url") and r["final_url"] != r["url"]:
        print(f"   → 重定向到: {r['final_url']}")
    if r.get("response_time_ms"):
        ms = r["response_time_ms"]
        flag = " ⚠️ 慢" if ms > 3000 else ""
        print(f"   响应时间: {ms} ms{flag}")
    if r.get("title"):
        print(f"   页面标题: {r['title']}")
    if r.get("error"):
        print(f"   ❗错误: {r['error']}")
    if verbose and r.get("recommendations"):
        print(f"   💡 建议:")
        for rec in r["recommendations"]:
            print(f"      - {rec}")
    if verbose and r.get("ssl"):
        print(f"   🔒 SSL: 有效  颁发给: {r['ssl'].get('subject', {}).get('commonName', 'N/A')}")


def print_summary(results):
    """打印汇总报告"""
    total = len(results)
    up = sum(1 for r in results if r["status"] == "up")
    warn = sum(1 for r in results if r["status"] == "warn")
    down = sum(1 for r in results if r["status"] == "down")
    avg_time = sum(r.get("response_time_ms", 0) or 0 for r in results) / total if total else 0

    print("\n" + "=" * 60)
    print("  📊 汇总报告")
    print("=" * 60)
    print(f"  总计     : {total} 个链接")
    print(f"  正常     : {up} ✅")
    print(f"  警告     : {warn} ⚠️")
    print(f"  不可用   : {down} ❌")
    print(f"  平均响应 : {avg_time:.0f} ms")
    print("=" * 60)

    if warn > 0:
        print("\n⚠️ 警告项：")
        for r in results:
            if r["status"] == "warn":
                print(f"  - [{r['http_code']}] {r['url']}")
                for rec in r.get("recommendations", []):
                    print(f"    → {rec}")

    if down > 0:
        print("\n❌ 不可用项：")
        for r in results:
            if r["status"] == "down":
                print(f"  - {r['url']}")
                print(f"    原因: {r.get('error', f'HTTP {r.get(\"http_code\")}')}")

    print()


def check_install():
    if not HAS_REQUESTS:
        print("⚠️ 缺少 requests 库，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "requests", "-q"], check=True)
        global HAS_REQUESTS
        HAS_REQUESTS = True


# 广州日报/融媒云常用链接预设
PRESET_URLS = {
    "新花城H5": [
        "https://huacheng.gz-cmc.com/",
        "https://huacheng.gz-cmc.com/pages/index.html",
    ],
    "大洋网": [
        "https://news.dayoo.com/",
        "https://www.dayoo.com/",
    ],
    "融媒云门户": [
        "http://app.bhntv.com.cn/",
    ],
}


def main():
    parser = argparse.ArgumentParser(description="H5/链接可用性检测工具")
    parser.add_argument("url", nargs="?", help="单个URL")
    parser.add_argument("--batch", help="批量文件路径（每行一个URL）")
    parser.add_argument("--full", action="store_true", help="详细输出模式")
    parser.add_argument("--timeout", type=int, default=10, help="超时秒数")
    parser.add_argument("--preset", help=f"使用预设链接组：{', '.join(PRESET_URLS.keys())}")
    parser.add_argument("--report", help="输出JSON报告文件路径")
    args = parser.parse_args()

    check_install()

    urls = []

    if args.preset:
        urls = PRESET_URLS.get(args.preset, [])
        print(f"📋 预设测试组：{args.preset}（{len(urls)} 个链接）")
    elif args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        print(f"📋 批量测试：{len(urls)} 个链接")
    elif args.url:
        urls = [args.url]
    else:
        print("用法: python3 check_url.py <url> [--full]")
        print("      python3 check_url.py --batch urls.txt")
        print("      python3 check_url.py --preset 新花城H5")
        print(f"\n可用预设: {', '.join(PRESET_URLS.keys())}")
        sys.exit(1)

    print(f"⏱  开始检测 {len(urls)} 个链接...\n")
    results = []
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 检测: {url[:70]}", end="   \r")
        r = check_url(url, timeout=args.timeout)
        results.append(r)

    print("\n\n" + "=" * 60)
    print("  🔍 检测结果")
    print("=" * 60)
    for r in results:
        print_result(r, verbose=args.full)

    print_summary(results)

    if args.report:
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "total": len(results),
                "results": results,
            }, f, ensure_ascii=False, indent=2)
        print(f"📄 报告已保存: {args.report}")


if __name__ == "__main__":
    main()
