#!/usr/bin/env python3
"""
端口扫描脚本
检测目标主机的开放端口和风险服务
"""

import socket
import sys
import io
from datetime import datetime

# Fix Chinese Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 高风险端口列表
HIGH_RISK_PORTS = {
    21: ('FTP', '高', '建议关闭，使用 SFTP'),
    23: ('Telnet', '极高', '立即关闭，使用 SSH'),
    25: ('SMTP', '中', '限制中继'),
    135: ('RPC', '中', 'Windows 远程过程调用'),
    139: ('NetBIOS', '中', '文件共享'),
    445: ('SMB', '高', '勒索软件攻击风险'),
    1433: ('MSSQL', '高', '数据库建议本地访问'),
    3306: ('MySQL', '高', '数据库建议本地访问'),
    3389: ('RDP', '高', '建议仅内网访问'),
    5432: ('PostgreSQL', '高', '数据库建议本地访问'),
    5900: ('VNC', '高', '建议关闭'),
    6379: ('Redis', '极高', '建议本地访问+密码'),
    8080: ('HTTP-Proxy', '中', '建议使用 HTTPS'),
    27017: ('MongoDB', '高', '建议本地访问+密码'),
}

# 快速扫描端口列表（仅高危）
FAST_SCAN_PORTS = [21, 22, 23, 25, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 3306, 3389, 5432, 5900, 6379, 8080, 27017]


def scan_port(host, port, timeout=1):
    """扫描单个端口"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def get_service_name(port):
    """获取服务名称"""
    try:
        return socket.getservbyport(port)
    except:
        return 'Unknown'


def scan_host(host, ports=None, fast=True):
    """扫描主机端口"""
    if fast and ports is None:
        ports = FAST_SCAN_PORTS
    
    if ports is None:
        ports = range(1, 1025)
    
    open_ports = []
    
    print(f"\n=== 端口扫描 ===")
    print(f"目标: {host}")
    print(f"扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"扫描模式: {'快速扫描' if fast else '全面扫描'}")
    print(f"\n正在扫描...")
    
    for port in ports:
        if scan_port(host, port):
            service = get_service_name(port)
            risk_info = HIGH_RISK_PORTS.get(port, (service, '低', ''))
            
            open_ports.append({
                'port': port,
                'service': service,
                'risk_level': risk_info[1],
                'recommendation': risk_info[2],
                'risk_desc': risk_info[0]
            })
            
            # 实时输出
            if risk_info[1] in ['极高', '高']:
                print(f"  ⚠️  [{risk_info[1]}] {port}/tcp - {service}")
            else:
                print(f"  ✓ {port}/tcp - {service}")
    
    return open_ports


def generate_report(open_ports):
    """生成检测报告"""
    print(f"\n{'='*50}")
    print(f"=== 扫描结果汇总 ===")
    print(f"{'='*50}")
    
    if not open_ports:
        print("未发现开放端口")
        return
    
    # 按风险等级排序
    risk_order = {'极高': 0, '高': 1, '中': 2, '低': 3}
    open_ports.sort(key=lambda x: risk_order.get(x['risk_level'], 4))
    
    high_risk = [p for p in open_ports if p['risk_level'] in ['极高', '高']]
    medium_risk = [p for p in open_ports if p['risk_level'] == '中']
    low_risk = [p for p in open_ports if p['risk_level'] == '低']
    
    print(f"\n总开放端口数: {len(open_ports)}")
    print(f"🔴 高危: {len(high_risk)} | 🟡 中危: {len(medium_risk)} | 🟢 低危: {len(low_risk)}")
    
    if high_risk:
        print(f"\n🔴 高危端口（需立即处理）:")
        for p in high_risk:
            print(f"  - {p['port']}/tcp ({p['service']}): {p['recommendation']}")
    
    if medium_risk:
        print(f"\n🟡 中危端口（建议处理）:")
        for p in medium_risk:
            print(f"  - {p['port']}/tcp ({p['service']})")
    
    print(f"\n建议:")
    if high_risk:
        print("  1. 立即关闭高危端口")
        print("  2. 限制远程访问")
        print("  3. 使用防火墙规则")
    else:
        print("  1. 定期进行安全检测")
        print("  2. 保持系统更新")


def main():
    if len(sys.argv) < 2:
        print("用法: python port_scan.py <目标> [--fast] [--port <端口列表>]")
        print("示例: python port_scan.py 192.168.1.1 --fast")
        sys.exit(1)
    
    target = sys.argv[1]
    fast = '--fast' in sys.argv
    
    open_ports = scan_host(target, fast=fast)
    generate_report(open_ports)


if __name__ == '__main__':
    main()
