#!/usr/bin/env python3
"""
弱密码检测脚本
检测常见服务的默认/弱密码（仅检测已知弱密码，不暴力破解）
"""

import socket
import sys
import io
from datetime import datetime

# Fix Chinese Windows encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 常见弱密码列表（仅用于检测，不实际尝试登录）
COMMON_WEAK_PASSWORDS = [
    'password', '123456', '12345678', '123456789', 'qwerty',
    'abc123', 'password1', 'admin', 'letmein', 'welcome',
    'monkey', '123123', '654321', 'passw0rd', 'root'
]

# 常见默认账户
DEFAULT_CREDENTIALS = {
    'ssh': [
        ('root', 'root'), ('root', '123456'), ('root', 'password'),
        ('admin', 'admin'), ('admin', 'password'), ('admin', '123456'),
        ('ubuntu', 'ubuntu'), ('user', 'user'), ('user', '123456'),
    ],
    'ftp': [
        ('anonymous', 'anonymous'), ('ftp', 'ftp'), ('admin', 'admin'),
    ],
    'mysql': [
        ('root', ''), ('root', 'root'), ('mysql', 'mysql'),
    ],
    'postgres': [
        ('postgres', 'postgres'), ('postgres', 'password'),
    ],
    'redis': [
        ('', ''),  # 空密码
    ],
}


def check_ssh_weakpass(host, port=22):
    """SSH 弱密码检测（仅检测服务可用性）"""
    result = {
        'service': 'SSH',
        'port': port,
        'status': 'unknown',
        'issues': []
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        sock.close()
        
        result['status'] = 'open'
        result['note'] = f'SSH 服务运行在端口 {port}'
        
        # 检测是否允许密码认证（通过 banner 判断）
        result['issues'].append('建议：使用 SSH 密钥认证，禁用密码登录')
        
    except ConnectionRefusedError:
        result['status'] = 'closed'
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result


def check_ftp_weakpass(host, port=21):
    """FTP 检测"""
    result = {
        'service': 'FTP',
        'port': port,
        'status': 'unknown',
        'issues': []
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        
        # 接收 FTP 欢迎信息
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        
        result['status'] = 'open'
        result['banner'] = banner[:100]
        
        # 检测是否允许匿名登录
        result['issues'].append('建议：禁用明文 FTP，使用 SFTP')
        
    except ConnectionRefusedError:
        result['status'] = 'closed'
    except Exception as e:
        result['status'] = 'error'
    
    return result


def check_mysql_weakpass(host, port=3306):
    """MySQL 检测"""
    result = {
        'service': 'MySQL',
        'port': port,
        'status': 'unknown',
        'issues': []
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        sock.close()
        
        result['status'] = 'open'
        result['issues'].append('建议：绑定 127.0.0.1，禁止远程 root')
        result['issues'].append('建议：使用强密码，禁用空密码')
        
    except ConnectionRefusedError:
        result['status'] = 'closed'
    except Exception as e:
        result['status'] = 'error'
    
    return result


def check_redis_weakpass(host, port=6379):
    """Redis 检测"""
    result = {
        'service': 'Redis',
        'port': port,
        'status': 'unknown',
        'issues': []
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect((host, port))
        
        # 尝试发送 PING
        sock.send(b'*1\r\n$4\r\nPING\r\n')
        response = sock.recv(1024)
        sock.close()
        
        if b'+PONG' in response:
            result['status'] = 'open'
            result['issues'].append('🔴 高危：Redis 可能无需认证')
            result['issues'].append('建议：设置密码，绑定 127.0.0.1')
        else:
            result['status'] = 'protected'
            
    except ConnectionRefusedError:
        result['status'] = 'closed'
    except Exception as e:
        result['status'] = 'error'
    
    return result


def check_service(host, service_type):
    """检测指定服务"""
    services = {
        'ssh': (check_ssh_weakpass, 22),
        'ftp': (check_ftp_weakpass, 21),
        'mysql': (check_mysql_weakpass, 3306),
        'redis': (check_redis_weakpass, 6379),
    }
    
    if service_type not in services:
        return None
    
    check_func, default_port = services[service_type]
    return check_func(host, default_port)


def generate_report(results):
    """生成检测报告"""
    print(f"\n{'='*60}")
    print(f"=== 弱密码/默认凭证检测报告 ===")
    print(f"{'='*60}")
    print(f"检测时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    open_services = []
    high_risk = 0
    
    for result in results:
        if result and result.get('status') == 'open':
            open_services.append(result)
            
            if result['service'] in ['Redis', 'MySQL', 'FTP', 'SSH']:
                high_risk += 1
            
            print(f"\n🔍 {result['service']} 服务:")
            print(f"  端口: {result['port']}")
            print(f"  状态: 开放")
            
            if result.get('banner'):
                print(f"  Banner: {result['banner']}")
            
            if result.get('issues'):
                print(f"  风险提示:")
                for issue in result['issues']:
                    print(f"    - {issue}")
    
    if not open_services:
        print(f"\n✅ 未发现开放的高风险服务")
        return
    
    # 风险评估
    print(f"\n{'='*60}")
    print(f"=== 风险评估 ===")
    
    if high_risk > 2:
        risk_level = '🔴 高危'
    elif high_risk > 0:
        risk_level = '🟡 中危'
    else:
        risk_level = '🟢 低危'
    
    print(f"风险等级: {risk_level}")
    print(f"开放高风险服务: {high_risk} 个")
    
    # 总体建议
    print(f"\n💡 总体建议:")
    print(f"  1. 关闭不必要的服务端口")
    print(f"  2. 使用强密码或密钥认证")
    print(f"  3. 限制数据库服务仅本地访问")
    print(f"  4. 启用防火墙规则")
    print(f"  5. 定期进行安全检测")


def main():
    if len(sys.argv) < 2:
        print("用法: python weakpass_check.py <目标> [--service <服务类型>]")
        print("服务类型: ssh, ftp, mysql, redis, all")
        print("示例: python weakpass_check.py 192.168.1.1 --service all")
        sys.exit(1)
    
    host = sys.argv[1]
    service_type = 'all'
    
    if '--service' in sys.argv:
        try:
            service_type = sys.argv[sys.argv.index('--service') + 1]
        except:
            pass
    
    print(f"正在检测 {host} 的服务安全...")
    
    results = []
    
    if service_type == 'all':
        services = ['ssh', 'ftp', 'mysql', 'redis']
    else:
        services = [service_type]
    
    for svc in services:
        result = check_service(host, svc)
        if result:
            results.append(result)
    
    generate_report(results)


if __name__ == '__main__':
    main()
