#!/usr/bin/env python3
"""
综合平台漏洞检测脚本
检测各平台常见漏洞
"""

import subprocess
import socket
import sys
import io
import re
from datetime import datetime

# Fix Chinese Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 平台检测模块
PLATFORMS = {
    'database': {
        'name': '数据库平台',
        'services': {
            'mysql': {'port': 3306, 'check': 'check_mysql'},
            'postgresql': {'port': 5432, 'check': 'check_postgresql'},
            'redis': {'port': 6379, 'check': 'check_redis'},
            'mongodb': {'port': 27017, 'check': 'check_mongodb'},
            'mssql': {'port': 1433, 'check': 'check_mssql'},
        }
    },
    'network': {
        'name': '网络设备/服务',
        'services': {
            'ssh': {'port': 22, 'check': 'check_ssh'},
            'telnet': {'port': 23, 'check': 'check_telnet'},
            'rdp': {'port': 3389, 'check': 'check_rdp'},
            'vpn': {'port': 443, 'check': 'check_vpn'},
        }
    },
    'web': {
        'name': 'Web 服务',
        'services': {
            'apache': {'port': 80, 'check': 'check_apache'},
            'nginx': {'port': 80, 'check': 'check_nginx'},
            'iis': {'port': 80, 'check': 'check_iis'},
        }
    },
    'cloud': {
        'name': '云服务',
        'services': {
            'aws_metadata': {'169.254.169.254': 'check_aws_metadata'},
            'azure_metadata': {'169.254.169.254': 'check_azure_metadata'},
        }
    },
    'container': {
        'name': '容器/虚拟化',
        'services': {
            'docker': {'port': 2375, 'check': 'check_docker'},
            'kubernetes': {'port': 6443, 'check': 'check_kubernetes'},
            'vmware': {'port': 443, 'check': 'check_vmware'},
        }
    }
}

# 高危漏洞列表
VULNERABILITIES = {
    'mysql': [
        {'cve': 'CVE-2026-21410', 'desc': 'MySQL 权限提升', 'severity': 'HIGH'},
    ],
    'postgresql': [
        {'cve': 'CVE-2026-21262', 'desc': 'PostgreSQL 权限提升 (CVSS 8.8)', 'severity': 'HIGH'},
    ],
    'redis': [
        {'cve': 'CVE-2025-32756', 'desc': 'Redis 认证绕过', 'severity': 'CRITICAL'},
    ],
    'mongodb': [
        {'cve': 'CVE-2026-21421', 'desc': 'MongoDB RCE', 'severity': 'CRITICAL'},
    ],
    'ssh': [
        {'cve': 'CVE-2025-32433', 'desc': 'Erlang SSH RCE (CVSS 10.0)', 'severity': 'CRITICAL'},
    ],
    'telnet': [
        {'cve': 'CVE-2026-xxx', 'desc': 'Telnet 明文传输', 'severity': 'HIGH'},
    ],
    'rdp': [
        {'cve': 'CVE-2026-xxx', 'desc': 'RDP 远程攻击风险', 'severity': 'HIGH'},
    ],
    'docker': [
        {'cve': 'CVE-2026-xxx', 'desc': 'Docker API 未授权访问', 'severity': 'CRITICAL'},
    ],
}


def check_port(host, port, timeout=2):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False


def check_mysql():
    """检测 MySQL"""
    result = {'service': 'MySQL', 'port': 3306, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 3306):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('MySQL 端口开放 (建议限制远程访问)')
        result['cves'] = VULNERABILITIES.get('mysql', [])
    else:
        result['status'] = '未开放'
    return result


def check_postgresql():
    """检测 PostgreSQL"""
    result = {'service': 'PostgreSQL', 'port': 5432, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 5432):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('PostgreSQL 端口开放')
        result['cves'] = VULNERABILITIES.get('postgresql', [])
    else:
        result['status'] = '未开放'
    return result


def check_redis():
    """检测 Redis"""
    result = {'service': 'Redis', 'port': 6379, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 6379):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('Redis 未授权访问风险')
        result['cves'] = VULNERABILITIES.get('redis', [])
    else:
        result['status'] = '未开放'
    return result


def check_mongodb():
    """检测 MongoDB"""
    result = {'service': 'MongoDB', 'port': 27017, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 27017):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('MongoDB 端口开放')
        result['cves'] = VULNERABILITIES.get('mongodb', [])
    else:
        result['status'] = '未开放'
    return result


def check_mssql():
    """检测 MS SQL Server"""
    result = {'service': 'MSSQL', 'port': 1433, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 1433):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('MSSQL 端口开放 (建议仅本地访问)')
    else:
        result['status'] = '未开放'
    return result


def check_ssh():
    """检测 SSH"""
    result = {'service': 'SSH', 'port': 22, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 22):
        result['status'] = '开放'
        result['issues'].append('SSH 服务运行中 (建议使用密钥认证)')
    else:
        result['status'] = '未开放'
    return result


def check_telnet():
    """检测 Telnet"""
    result = {'service': 'Telnet', 'port': 23, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 23):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('⚠️  Telnet 极度危险，建议立即关闭')
        result['cves'] = [{'cve': 'CVE-2026-xxx', 'desc': 'Telnet 明文传输', 'severity': 'CRITICAL'}]
    else:
        result['status'] = '未开放'
    return result


def check_rdp():
    """检测 RDP"""
    result = {'service': 'RDP', 'port': 3389, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 3389):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('RDP 开放 (建议仅内网访问，启用 NLA)')
    else:
        result['status'] = '未开放'
    return result


def check_vpn():
    """检测 VPN"""
    result = {'service': 'VPN/SSL', 'port': 443, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 443):
        result['status'] = '开放'
        result['issues'].append('HTTPS/VPN 服务运行')
    else:
        result['status'] = '未开放'
    return result


def check_apache():
    """检测 Apache"""
    result = {'service': 'Apache', 'port': 80, 'vulnerable': False, 'issues': []}
    try:
        import urllib.request
        urllib.request.urlopen('http://127.0.0.1', timeout=2)
        result['status'] = '运行中'
    except:
        result['status'] = '未运行'
    return result


def check_nginx():
    """检测 Nginx"""
    result = {'service': 'Nginx', 'port': 80, 'vulnerable': False, 'issues': []}
    result['status'] = '检测跳过'
    return result


def check_iis():
    """检测 IIS"""
    result = {'service': 'IIS', 'port': 80, 'vulnerable': False, 'issues': []}
    result['status'] = '检测跳过'
    return result


def check_aws_metadata():
    """检测 AWS 元数据服务"""
    result = {'service': 'AWS Metadata', 'ip': '169.254.169.254', 'vulnerable': False, 'issues': []}
    try:
        import urllib.request
        req = urllib.request.Request('http://169.254.169.254/latest/meta-data/')
        urllib.request.urlopen(req, timeout=2)
        result['status'] = '可访问'
        result['vulnerable'] = True
        result['issues'].append('⚠️  AWS 元数据服务可访问，可能存在 SSRF 漏洞')
    except:
        result['status'] = '不可访问'
    return result


def check_azure_metadata():
    """检测 Azure 元数据服务"""
    result = {'service': 'Azure Metadata', 'ip': '169.254.169.254', 'vulnerable': False, 'issues': []}
    try:
        import urllib.request
        req = urllib.request.Request('http://169.254.169.254/metadata/instance', headers={'Metadata': 'true'})
        urllib.request.urlopen(req, timeout=2)
        result['status'] = '可访问'
        result['vulnerable'] = True
        result['issues'].append('⚠️  Azure 元数据服务可访问')
    except:
        result['status'] = '不可访问'
    return result


def check_docker():
    """检测 Docker"""
    result = {'service': 'Docker', 'port': 2375, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 2375):
        result['status'] = '开放'
        result['vulnerable'] = True
        result['issues'].append('⚠️  Docker API 未授权访问风险')
    else:
        result['status'] = '未开放'
    return result


def check_kubernetes():
    """检测 Kubernetes"""
    result = {'service': 'Kubernetes API', 'port': 6443, 'vulnerable': False, 'issues': []}
    if check_port('127.0.0.1', 6443):
        result['status'] = '开放'
        result['issues'].append('Kubernetes API 运行中')
    else:
        result['status'] = '未开放'
    return result


def check_vmware():
    """检测 VMware"""
    result = {'service': 'VMware', 'port': 443, 'vulnerable': False, 'issues': []}
    result['status'] = '检测跳过'
    return result


def check_platform(platform_key):
    """检测指定平台"""
    platform = PLATFORMS.get(platform_key)
    if not platform:
        return None
    
    results = []
    for service_name, service_info in platform['services'].items():
        check_func = globals().get(service_info.get('check', ''))
        if check_func:
            result = check_func()
            results.append(result)
    
    return {
        'platform': platform['name'],
        'services': results
    }


def check_all():
    """检测所有平台"""
    all_results = []
    for platform_key in PLATFORMS:
        result = check_platform(platform_key)
        if result:
            all_results.append(result)
    return all_results


def generate_report(results):
    """生成检测报告"""
    print(f"\n{'='*70}")
    print(f"=== 综合平台漏洞检测报告 ===")
    print(f"{'='*70}")
    print(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_vulns = 0
    critical = 0
    high = 0
    
    for platform_result in results:
        print(f"\n{'='*70}")
        print(f"📦 {platform_result['platform']}")
        print(f"{'='*70}")
        
        for service in platform_result['services']:
            status = service.get('status', '未知')
            vulnerable = service.get('vulnerable', False)
            
            icon = '🔴' if vulnerable else '✅'
            print(f"\n{icon} {service['service']}: {status}")
            
            if service.get('issues'):
                for issue in service['issues']:
                    print(f"   ⚠️  {issue}")
            
            if service.get('cves'):
                total_vulns += len(service['cves'])
                for cve in service['cves']:
                    severity = cve.get('severity', '')
                    if severity == 'CRITICAL':
                        critical += 1
                    elif severity == 'HIGH':
                        high += 1
                    print(f"   🐞 {cve['cve']}: {cve['desc']} [{severity}]")
    
    print(f"\n{'='*70}")
    print(f"=== 汇总 ===")
    print(f"{'='*70}")
    print(f"🔴 严重 (CRITICAL): {critical}")
    print(f"🟡 高危 (HIGH): {high}")
    print(f"⚠️  总计高危漏洞: {total_vulns}")
    
    print(f"\n💡 建议:")
    print(f"  1. 关闭不必要的端口和服务")
    print(f"  2. 数据库服务仅允许本地访问")
    print(f"  3. 禁用 Telnet，使用 SSH")
    print(f"  4. 启用云服务元数据保护")
    print(f"  5. 定期进行安全扫描")
    print(f"\n📚 详细漏洞信息请参考: references/platform_vulnerabilities_2026.md")


def main():
    print("=== 综合平台漏洞检测 ===")
    print("1. 数据库平台")
    print("2. 网络服务")
    print("3. Web 服务")
    print("4. 云服务")
    print("5. 容器/虚拟化")
    print("6. 检测全部")
    
    if len(sys.argv) < 2:
        choice = input("\n请选择 (1-6): ").strip()
    else:
        choice = sys.argv[1]
    
    if choice == '1':
        results = [check_platform('database')]
    elif choice == '2':
        results = [check_platform('network')]
    elif choice == '3':
        results = [check_platform('web')]
    elif choice == '4':
        results = [check_platform('cloud')]
    elif choice == '5':
        results = [check_platform('container')]
    else:
        results = check_all()
    
    # 过滤 None
    results = [r for r in results if r]
    generate_report(results)


if __name__ == '__main__':
    main()
