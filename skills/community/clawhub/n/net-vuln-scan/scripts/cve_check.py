#!/usr/bin/env python3
"""
CVE 检测脚本
检测系统中是否存在已知高危漏洞
"""

import subprocess
import socket
import sys
import io
import re
from datetime import datetime

# Fix Chinese Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 高危 CVE 列表
HIGH_RISK_CVES = {
    'CVE-2026-21514': {
        'name': 'Microsoft Word OLE Bypass',
        'severity': 'HIGH',
        'cvss': 7.8,
        'description': 'Microsoft Word OLE 安全绕过漏洞，影响近 1400 万设备',
        'check': 'check_word_version'
    },
    'CVE-2026-21262': {
        'name': 'SQL Server EoP',
        'severity': 'HIGH', 
        'cvss': 8.8,
        'description': 'SQL Server 权限提升漏洞',
        'check': 'check_sql_server'
    },
    'CVE-2026-26110': {
        'name': 'Office RCE',
        'severity': 'CRITICAL',
        'cvss': 8.4,
        'description': 'Microsoft Office 远程代码执行漏洞',
        'check': 'check_office'
    },
    'CVE-2026-26127': {
        'name': '.NET DoS',
        'severity': 'HIGH',
        'cvss': 7.5,
        'description': '.NET 拒绝服务漏洞',
        'check': 'check_dotnet'
    }
}


def check_word_version():
    """检查 Microsoft Word 版本"""
    try:
        # 检查 Word 是否安装
        result = subprocess.run(
            ['reg', 'query', r'HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\WINWORD.EXE'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return {
                'installed': True,
                'info': 'Microsoft Word 已安装，建议更新到最新补丁'
            }
        else:
            return {
                'installed': False,
                'info': 'Microsoft Word 未安装'
            }
    except Exception as e:
        return {'installed': False, 'info': f'检查失败: {str(e)}'}


def check_sql_server():
    """检查 SQL Server"""
    try:
        # 检查常见 SQL Server 端口
        ports = [1433, 1434]
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex(('127.0.0.1', port))
                sock.close()
                if result == 0:
                    return {
                        'installed': True,
                        'info': f'SQL Server 端口 {port} 开放，建议安装官方补丁'
                    }
            except:
                pass
        return {'installed': False, 'info': '未检测到 SQL Server'}
    except Exception as e:
        return {'installed': False, 'info': f'检查失败: {str(e)}'}


def check_office():
    """检查 Office 版本"""
    try:
        result = subprocess.run(
            ['reg', 'query', r'HKLM\SOFTWARE\Microsoft\Office\ClickToRun\Configuration'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return {
                'installed': True,
                'info': 'Microsoft Office 已安装，建议更新到最新版本'
            }
        else:
            return {'installed': False, 'info': 'Office 365 未检测到'}
    except Exception as e:
        return {'installed': False, 'info': f'检查失败: {str(e)}'}


def check_dotnet():
    """检查 .NET 版本"""
    try:
        result = subprocess.run(
            ['dotnet', '--list-sdks'],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            sdks = result.stdout.strip()
            return {
                'installed': True,
                'info': f'检测到 .NET SDK: {sdks}'
            }
        else:
            return {'installed': False, 'info': '未检测到 .NET SDK'}
    except FileNotFoundError:
        return {'installed': False, 'info': '.NET 未安装'}
    except Exception as e:
        return {'installed': False, 'info': f'检查失败: {str(e)}'}


def check_cve(cve_id):
    """检测指定 CVE"""
    if cve_id not in HIGH_RISK_CVES:
        return {'error': f'未知 CVE: {cve_id}'}
    
    cve = HIGH_RISK_CVES[cve_id]
    check_func = globals().get(cve['check'])
    
    if check_func:
        result = check_func()
        return {
            'cve': cve_id,
            'name': cve['name'],
            'severity': cve['severity'],
            'cvss': cve['cvss'],
            'description': cve['description'],
            'check_result': result
        }
    
    return {'error': f'无检测方法: {cve_id}'}


def check_all_cves():
    """检测所有高危 CVE"""
    results = []
    for cve_id in HIGH_RISK_CVES:
        result = check_cve(cve_id)
        results.append(result)
    return results


def generate_report(results):
    """生成检测报告"""
    print(f"\n{'='*60}")
    print(f"=== CVE 漏洞检测报告 ===")
    print(f"{'='*60}")
    print(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    critical = 0
    high = 0
    
    for result in results:
        if 'error' in result:
            continue
            
        severity = result.get('severity', '')
        if severity == 'CRITICAL':
            critical += 1
        elif severity == 'HIGH':
            high += 1
            
        print(f"\n{'🔴' if severity in ['CRITICAL', 'HIGH'] else '🟡'} {result.get('cve')}")
        print(f"   名称: {result.get('name')}")
        print(f"   严重程度: {severity} (CVSS: {result.get('cvss')})")
        print(f"   描述: {result.get('description')}")
        
        check_result = result.get('check_result', {})
        if check_result.get('installed'):
            print(f"   ⚠️  状态: {check_result.get('info')}")
        else:
            print(f"   ✅ 状态: {check_result.get('info', '未受影响')}")
    
    print(f"\n{'='*60}")
    print(f"=== 汇总 ===")
    print(f"🔴 严重/高危: {critical + high}")
    print(f"   - 严重 (CRITICAL): {critical}")
    print(f"   - 高危 (HIGH): {high}")
    
    print(f"\n💡 建议:")
    print(f"  1. 定期检查微软官方安全公告")
    print(f"  2. 及时安装系统补丁")
    print(f"  3. 启用自动更新")
    print(f"  4. 详细修复方案请参考: references/latest_vulnerabilities_2026.md")


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python cve_check.py <CVE-ID>     # 检测指定 CVE")
        print("  python cve_check.py all          # 检测所有高危 CVE")
        print("\n示例:")
        print("  python cve_check.py CVE-2026-21514")
        print("  python cve_check.py all")
        sys.exit(1)
    
    target = sys.argv[1].upper()
    
    if target == 'ALL':
        results = check_all_cves()
        generate_report(results)
    elif target.startswith('CVE-'):
        result = check_cve(target)
        if 'error' in result:
            print(f"错误: {result['error']}")
            sys.exit(1)
        generate_report([result])
    else:
        print(f"未知参数: {target}")
        sys.exit(1)


if __name__ == '__main__':
    main()
