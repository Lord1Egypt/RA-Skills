#!/usr/bin/env python3
"""
Search Pro - Content Extractor
内容提取脚本

Usage: python3 extract.py --url https://example.com

Security: 仅提取网页内容，不读取本地文件，不访问内网地址
"""

import argparse
import re
import socket
import sys
from urllib.parse import urlparse
from ipaddress import ip_address, ip_network

# 修复Windows GBK编码兼容问题
if sys.platform.startswith('win'):
    try:
        # Python 3.7+ 支持 reconfigure
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # 旧版本Python兼容
        import io
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

# 内网 IP 范围（RFC 1918 + 特殊地址）
PRIVATE_NETWORKS = [
    ip_network('10.0.0.0/8'),
    ip_network('172.16.0.0/12'),
    ip_network('192.168.0.0/16'),
    ip_network('127.0.0.0/8'),
    ip_network('0.0.0.0/8'),
    ip_network('169.254.0.0/16'),
]

def is_private_ip(ip_str: str) -> bool:
    """检查 IP 地址是否为私有/内网地址"""
    try:
        ip = ip_address(ip_str)
        # 检查是否为私有地址
        for network in PRIVATE_NETWORKS:
            if ip in network:
                return True
        return False
    except ValueError:
        return False

def resolve_and_check_hostname(hostname: str) -> bool:
    """解析主机名并检查是否为内网地址"""
    try:
        # 获取所有 IP 地址
        addr_info = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
        for info in addr_info:
            ip = info[4][0]
            if is_private_ip(ip):
                print(f"⚠️  警告：{hostname} 解析到内网 IP: {ip}")
                return True  # 是内网
        return False  # 不是内网
    except socket.gaierror:
        print(f"⚠️  警告：无法解析主机名 {hostname}")
        return True  # 无法解析，视为不安全

def validate_url(url: str) -> tuple:
    """
    验证 URL 是否安全
    
    Returns:
        (is_safe: bool, error_msg: str)
    """
    # 1. 解析 URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        return False, f"URL 解析失败：{e}"
    
    # 2. 检查协议
    if parsed.scheme not in ('http', 'https'):
        return False, f"不支持的协议：{parsed.scheme}（仅支持 http/https）"
    
    # 3. 检查主机名
    hostname = parsed.hostname
    if not hostname:
        return False, "无效的主机名"
    
    # 4. 检查常见内网主机名
    localhost_names = ['localhost', 'localhost.localdomain', 'internal', 'intranet']
    if hostname.lower() in localhost_names:
        return False, f"不允许访问内网主机：{hostname}"
    
    # 5. 检查是否为 IP 地址
    try:
        ip = ip_address(hostname)
        if is_private_ip(str(ip)):
            return False, f"不允许访问内网 IP: {hostname}"
    except ValueError:
        # 不是 IP 地址，是域名，需要解析检查
        pass
    
    # 6. 解析域名并检查（实际执行 DNS 查询）
    if resolve_and_check_hostname(hostname):
        return False, f"域名解析到内网地址：{hostname}"
    
    # 7. 检查内网域名模式
    if is_private_ip_hostname(hostname):
        return False, f"检测到内网域名：{hostname}"
    
    return True, ""

def is_private_ip_hostname(hostname: str) -> bool:
    """检查域名是否解析到内网 IP（简化版，不实际 DNS 查询）"""
    # 常见内网域名模式
    internal_patterns = [
        r'.*\.local$',
        r'.*\.internal$',
        r'.*\.intranet$',
        r'.*\.lan$',
        r'.*\.private$',
    ]
    
    for pattern in internal_patterns:
        if re.match(pattern, hostname, re.IGNORECASE):
            return True
    
    return False

def extract_from_url(url: str):
    """从 URL 提取内容"""
    print("📄 Search Pro - Content Extractor")
    print("=" * 50)
    print(f"🔗 提取 URL: {url}")
    
    # 安全验证
    is_safe, error_msg = validate_url(url)
    
    if not is_safe:
        print(f"❌ 错误：{error_msg}")
        print("\n安全限制:")
        print("  - 仅支持 http:// 和 https:// 协议")
        print("  - 不支持 file:// 或其他协议")
        print("  - 不访问内网地址（localhost, 127.x.x.x, 192.168.x.x 等）")
        print("  - 不访问 .local, .internal, .intranet 等内网域名")
        return False
    
    print("\n✅ URL 验证通过")
    print("\n提示：完整功能需要集成 web_fetch 或 requests + BeautifulSoup")
    print("示例代码：")
    print("  import requests")
    print("  from bs4 import BeautifulSoup")
    print("  response = requests.get(url)")
    print("  soup = BeautifulSoup(response.text, 'html.parser')")
    print("  print(soup.get_text())")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='内容提取工具')
    parser.add_argument('--url', help='要提取的网页 URL')
    
    args = parser.parse_args()
    
    if not args.url:
        print("用法：python3 extract.py --url <URL>")
        print("\n示例:")
        print("  python3 extract.py --url https://example.com")
        print("\n安全限制:")
        print("  - 仅支持 http:// 和 https:// 协议")
        print("  - 不支持 file:// 本地文件")
        print("  - 不访问内网地址")
        print("  - 不访问 .local, .internal 等内网域名")
        return
    
    success = extract_from_url(args.url)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
