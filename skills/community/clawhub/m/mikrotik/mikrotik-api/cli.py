#!/usr/bin/env python3
"""
MikroTik RouterOS API 命令行工具

用法:
    python cli.py <host> [command] [options]

示例:
    python cli.py 192.168.1.1 status           # 查看设备状态
    python cli.py 192.168.1.1 firewall         # 查看防火墙
    python cli.py 192.168.1.1 interfaces       # 查看接口
    python cli.py 192.168.1.1 cmd /ip/address/print  # 执行自定义命令
"""

import sys
import argparse

# 支持直接运行和包导入两种模式
try:
    from .client import MikroTikAPI
    from .commands import QuickCommands
except ImportError:
    from client import MikroTikAPI
    from commands import QuickCommands


def main():
    parser = argparse.ArgumentParser(description='MikroTik RouterOS API 命令行工具')
    parser.add_argument('host', help='RouterOS 设备 IP 地址')
    parser.add_argument('-u', '--username', default='admin', help='用户名 (默认：admin)')
    parser.add_argument('-p', '--password', default='', help='密码 (默认：空)')
    parser.add_argument('--port', type=int, default=8728, help='API 端口 (默认：8728)')
    parser.add_argument('command', nargs='?', default='status', 
                       choices=['status', 'firewall', 'interfaces', 'routes', 'cmd'],
                       help='要执行的命令')
    parser.add_argument('args', nargs='*', help='命令参数')
    
    args = parser.parse_args()
    
    # 连接设备
    api = MikroTikAPI(args.host, args.username, args.password, args.port)
    
    if not api.connect():
        print(f"❌ 无法连接到 {args.host}:{args.port}")
        sys.exit(1)
    
    if not api.login():
        print("❌ 登录失败")
        api.disconnect()
        sys.exit(1)
    
    quick = QuickCommands(api)
    
    try:
        if args.command == 'status':
            quick.print_status()
        
        elif args.command == 'firewall':
            print("=" * 60)
            print("🔥 防火墙规则")
            print("=" * 60)
            
            # 过滤规则
            print("\n📋 过滤规则:")
            rules = quick.firewall.get_filter_rules()
            if rules:
                for i, rule in enumerate(rules, 1):
                    chain = rule.get('chain', 'N/A')
                    action = rule.get('action', 'N/A')
                    disabled = rule.get('disabled', '') == 'true'
                    comment = rule.get('comment', '')
                    status = "⏸️" if disabled else "✅"
                    print(f"  {status} [{i}] {chain}: {action}" + 
                          (f" ({comment})" if comment else ""))
            else:
                print("  (无规则)")
            
            # NAT 规则
            print("\n🔄 NAT 规则:")
            rules = quick.firewall.get_nat_rules()
            if rules:
                for i, rule in enumerate(rules, 1):
                    chain = rule.get('chain', 'N/A')
                    action = rule.get('action', 'N/A')
                    to_addr = rule.get('to-addresses', '')
                    comment = rule.get('comment', '')
                    print(f"  [{i}] {chain}: {action}" + 
                          (f" → {to_addr}" if to_addr else "") +
                          (f" ({comment})" if comment else ""))
            else:
                print("  (无规则)")
            
            print("=" * 60)
        
        elif args.command == 'interfaces':
            print("=" * 60)
            print("🔌 网络接口")
            print("=" * 60)
            interfaces = quick.network.get_interfaces()
            for iface in interfaces:
                name = iface.get('name', 'unknown')
                running = iface.get('running', 'false') == 'true'
                mtu = iface.get('mtu', 'N/A')
                mac = iface.get('mac-address', 'N/A')
                status = "✅" if running else "❌"
                print(f"  {status} {name} (MTU: {mtu}, MAC: {mac})")
            print("=" * 60)
        
        elif args.command == 'routes':
            print("=" * 60)
            print("🛤️ 路由表")
            print("=" * 60)
            routes = quick.network.get_routes()
            for route in routes:
                dst = route.get('dst-address', 'N/A')
                gateway = route.get('gateway', 'N/A')
                distance = route.get('distance', '1')
                print(f"  {dst} via {gateway} (distance: {distance})")
            print("=" * 60)
        
        elif args.command == 'cmd':
            if not args.args:
                print("❌ 请指定命令路径，如：/system/resource/print")
                sys.exit(1)
            
            cmd = args.args[0]
            results = api.run_command(cmd)
            
            if results:
                for item in results:
                    for key, value in item.items():
                        print(f"  {key}: {value}")
                    print()
            else:
                print("(无结果)")
    
    finally:
        api.disconnect()


if __name__ == '__main__':
    main()
