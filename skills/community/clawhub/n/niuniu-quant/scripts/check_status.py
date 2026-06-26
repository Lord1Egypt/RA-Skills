#!/usr/bin/env python3
"""
牛牛量化系统 - 快速状态检查脚本
用法：python3 scripts/check_status.py
"""

import subprocess
import json
import sys

def check_port(port):
    """检查端口是否被监听"""
    try:
        result = subprocess.run(
            ['ss', '-tlnp'],
            capture_output=True,
            text=True
        )
        return str(port) in result.stdout
    except:
        return False

def test_api(port, endpoint):
    """测试 API 端点"""
    try:
        result = subprocess.run(
            ['curl', '-s', '-m', '2', f'http://localhost:{port}{endpoint}'],
            capture_output=True,
            text=True,
            timeout=3
        )
        data = json.loads(result.stdout)
        return True, data
    except:
        return False, None

def main():
    print("=" * 60)
    print("🐮 牛牛量化系统 - 状态检查")
    print("=" * 60)
    print()
    
    services = [
        (3000, '用户后端', '/api/admin/stats'),
        (3001, '选股池数据', '/api/pool'),
        (3002, '回测 API', '/api/strategies'),
        (3003, '实时股价', '/api/price/000001'),
        (5000, '选股池 Web', '/api/pool'),
        (8080, '前端代理', '/api/admin/stats'),
    ]
    
    running = 0
    for port, name, endpoint in services:
        is_running = check_port(port)
        status = "✅" if is_running else "❌"
        print(f"{status} {port} 端口：{name}")
        if is_running:
            running += 1
    
    print()
    print(f"服务状态：{running}/{len(services)} 运行中")
    print()
    
    if running == len(services):
        print("✅ 所有服务正常运行！")
        print()
        print("🌐 访问地址:")
        print("  http://localhost:8080/")
        print("  http://101.42.104.24:8080/")
    else:
        print("⚠️  部分服务未运行，请执行:")
        print("  牛牛量化站点")
    
    print()
    print("=" * 60)
    return 0 if running == len(services) else 1

if __name__ == '__main__':
    sys.exit(main())
