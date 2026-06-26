#!/usr/bin/env python3
"""
快代理 - 测试代理连接

Usage:
    python test_proxy.py --proxy "http://ip:port"
    python test_proxy.py --proxy "http://user:pass@ip:port"
"""

import argparse
import sys
import requests
import time


def test_proxy(proxy: str, test_url: str = "https://httpbin.org/ip", timeout: int = 10):
    """
    测试代理连接

    Args:
        proxy: 代理地址 (格式: http://[user:pass@]ip:port)
        test_url: 测试URL
        timeout: 超时时间(秒)
    """
    proxies = {"http": proxy, "https": proxy}

    print(f"测试代理: {proxy}")
    print(f"目标URL: {test_url}")
    print("-" * 50)

    try:
        start_time = time.time()
        resp = requests.get(test_url, proxies=proxies, timeout=timeout)
        elapsed = time.time() - start_time

        print(f"✓ 连接成功")
        print(f"✓ 响应时间: {elapsed:.2f}s")
        print(f"✓ 出口IP: {resp.json().get('origin', 'unknown')}")
        print(f"✓ 状态码: {resp.status_code}")
        return True

    except requests.exceptions.ProxyError as e:
        print(f"✗ 代理错误: {e}")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ 连接超时 (>{timeout}s)")
        return False
    except requests.RequestException as e:
        print(f"✗ 请求失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="测试代理连接")
    parser.add_argument("--proxy", required=True, help="代理地址")
    parser.add_argument("--url", default="https://httpbin.org/ip", help="测试URL")
    parser.add_argument("--timeout", type=int, default=10, help="超时时间(秒)")

    args = parser.parse_args()

    success = test_proxy(proxy=args.proxy, test_url=args.url, timeout=args.timeout)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
