#!/usr/bin/env python3
"""
SSL/TLS 证书检测脚本
检测 HTTPS 服务的证书和配置问题
"""

import ssl
import socket
import sys
import io
from datetime import datetime
from urllib.parse import urlparse

# Fix Chinese Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def get_certificate(domain, port=443):
    """获取 SSL 证书信息"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                return {
                    'valid': True,
                    'cert': cert,
                    'cipher': cipher,
                    'protocol': version,
                    'subject': dict(x[0] for x in cert['subject']),
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'notBefore': cert['notBefore'],
                    'notAfter': cert['notAfter'],
                    'version': version
                }
    except Exception as e:
        return {'valid': False, 'error': str(e)}


def check_protocol_support(domain, port=443):
    """检测支持的协议版本"""
    protocols = {
        'SSLv3': ssl.PROTOCOL_SSLv23,
        'TLSv1.0': ssl.PROTOCOL_TLSv1,
        'TLSv1.1': ssl.PROTOCOL_TLSv1_1,
        'TLSv1.2': ssl.PROTOCOL_TLSv1_2,
        'TLSv1.3': ssl.PROTOCOL_TLSv1_3 if hasattr(ssl, 'PROTOCOL_TLSv1_3') else None
    }
    
    supported = []
    weak = []
    
    # 检测 TLS 1.3
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_3
        context.maximum_version = ssl.TLSVersion.TLSv1_3
        with socket.create_connection((domain, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                supported.append('TLSv1.3')
    except:
        pass
    
    # 检测 TLS 1.2
    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        with socket.create_connection((domain, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                supported.append('TLSv1.2')
    except:
        pass
    
    # 检测弱协议
    weak_protocols = ['SSLv3', 'TLSv1.0', 'TLSv1.1']
    for proto in weak_protocols:
        try:
            if proto == 'TLSv1.0':
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            elif proto == 'TLSv1.1':
                context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1)
            else:
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            
            context.minimum_version = ssl.TLSVersion.SSLv3
            with socket.create_connection((domain, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    weak.append(proto)
        except:
            pass
    
    return supported, weak


def check_security_headers(domain):
    """检测安全响应头（简化版）"""
    # 这是一个简化检测，实际需要完整的 HTTP 请求
    headers_to_check = [
        'Strict-Transport-Security',
        'Content-Security-Policy',
        'X-Frame-Options',
        'X-Content-Type-Options',
        'X-XSS-Protection'
    ]
    
    # 返回检测提示
    return {
        'note': '需要完整 HTTP 检测，请使用在线工具验证',
        'headers': headers_to_check
    }


def calculate_days_remaining(not_after):
    """计算证书剩余天数"""
    from datetime import datetime
    try:
        # 解析日期格式
        exp_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
        remaining = (exp_date - datetime.now()).days
        return remaining
    except:
        return None


def generate_report(domain, cert_info, protocols, weak_protocols):
    """生成检测报告"""
    print(f"\n{'='*60}")
    print(f"=== SSL/TLS 安全检测报告 ===")
    print(f"{'='*60}")
    print(f"域名: {domain}")
    print(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not cert_info.get('valid'):
        print(f"\n❌ 连接失败: {cert_info.get('error')}")
        print(f"\n可能原因:")
        print(f"  - 域名不存在或无法访问")
        print(f"  - 未启用 HTTPS")
        print(f"  - 防火墙阻止")
        return
    
    # 证书信息
    print(f"\n📜 证书信息:")
    subject = cert_info.get('subject', {})
    issuer = cert_info.get('issuer', {})
    print(f"  颁发给: {subject.get('commonName', 'N/A')}")
    print(f"  颁发者: {issuer.get('commonName', 'N/A')}")
    print(f"  生效时间: {cert_info.get('notBefore', 'N/A')}")
    print(f"  过期时间: {cert_info.get('notAfter', 'N/A')}")
    
    days_left = calculate_days_remaining(cert_info.get('notAfter', ''))
    if days_left is not None:
        if days_left < 0:
            print(f"  状态: ❌ 已过期 {abs(days_left)} 天")
        elif days_left < 30:
            print(f"  状态: ⚠️  即将过期（{days_left} 天）")
        else:
            print(f"  状态: ✅ 有效（剩余 {days_left} 天）")
    
    # 协议支持
    print(f"\n🔐 协议支持:")
    for proto in ['TLSv1.3', 'TLSv1.2']:
        if proto in protocols:
            print(f"  ✅ {proto} - 支持")
        else:
            print(f"  ❌ {proto} - 不支持")
    
    if weak_protocols:
        print(f"\n⚠️  警告 - 弱协议:")
        for proto in weak_protocols:
            print(f"  ❌ {proto} - 存在漏洞风险")
    
    # 加密套件
    cipher = cert_info.get('cipher')
    if cipher:
        print(f"\n🔒 加密套件:")
        print(f"  协议: {cipher[1]}")
        print(f"  加密算法: {cipher[0]}")
    
    # 安全头提示
    print(f"\n🛡️ 安全响应头:")
    print(f"  提示: {check_security_headers(domain)['note']}")
    for header in check_security_headers(domain)['headers']:
        print(f"  - {header}")
    
    # 风险评估
    print(f"\n{'='*60}")
    print(f"=== 风险评估 ===")
    risk_level = '🟢 低'
    issues = []
    
    if days_left is not None and days_left < 0:
        risk_level = '🔴 极高'
        issues.append('证书已过期')
    elif days_left is not None and days_left < 30:
        risk_level = '🟡 中危'
        issues.append('证书即将过期')
    
    if weak_protocols:
        risk_level = '🔴 高危'
        issues.append('支持弱协议')
    
    print(f"总体风险: {risk_level}")
    
    if issues:
        print(f"\n发现的问题:")
        for issue in issues:
            print(f"  - {issue}")
    
    # 建议
    print(f"\n💡 建议:")
    if days_left is not None and days_left < 30:
        print(f"  1. 立即续期证书")
        print(f"  2. 配置自动续期（Let's Encrypt）")
    
    if weak_protocols:
        print(f"  1. 禁用 SSLv3、TLS 1.0、1.1")
        print(f"  2. 仅启用 TLS 1.2+")
    
    print(f"  1. 启用 HSTS 强制 HTTPS")
    print(f"  2. 配置安全响应头")


def main():
    if len(sys.argv) < 2:
        print("用法: python ssl_check.py <域名> [--port <端口>]")
        print("示例: python ssl_check.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1].replace('https://', '').replace('http://', '').split('/')[0]
    port = 443
    
    if '--port' in sys.argv:
        try:
            port = int(sys.argv[sys.argv.index('--port') + 1])
        except:
            pass
    
    print(f"正在检测 {domain}...")
    
    cert_info = get_certificate(domain, port)
    protocols, weak_protocols = check_protocol_support(domain, port)
    
    generate_report(domain, cert_info, protocols, weak_protocols)


if __name__ == '__main__':
    main()
