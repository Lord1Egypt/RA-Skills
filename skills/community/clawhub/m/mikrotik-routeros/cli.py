import sys
import argparse
from client import RouterOSApi
from commands import QuickCommands

"""
MikroTik RouterOS API CLI Tool
Author: Xiage
Translator/Maintainer: drodecker
"""

def main():
    parser = argparse.ArgumentParser(description='MikroTik RouterOS API CLI Tool')
    parser.add_argument('host', help='RouterOS device IP address')
    parser.add_argument('-u', '--username', default='admin', help='Username (default: admin)')
    parser.add_argument('-p', '--password', default='', help='Password (default: empty)')
    parser.add_argument('--port', type=int, default=8728, help='API port (default: 8728)')
    parser.add_argument('command', choices=['status', 'firewall', 'interfaces', 'routes', 'cmd'], 
                        help='Command to execute')
    parser.add_argument('args', nargs='*', help='Command arguments')

    args = parser.parse_args()

    # Connect to device
    with RouterOSApi(args.host, args.username, args.password, args.port) as api:
        if not api:
            print(f"❌ Could not connect to {args.host}:{args.port}")
            return

        quick = QuickCommands(api)
        
        if args.command == 'status':
            quick.print_status()
            
        elif args.command == 'firewall':
            print("🔥 Firewall Rules")
            
            # Filter rules
            print("\n📋 Filter Rules:")
            rules = quick.firewall.get_filter_rules()
            if rules:
                for i, r in enumerate(rules):
                    disabled = r.get('disabled') == 'true'
                    status = "⏸️" if disabled else "✅"
                    print(f"  {i}. {status} {r.get('chain')} {r.get('action')} {r.get('dst-address', '')}")
            else:
                print("  (No rules)")
                
            # NAT rules
            print("\n🔄 NAT Rules:")
            nat = quick.firewall.get_nat_rules()
            if nat:
                for i, r in enumerate(nat):
                    to_addr = r.get('to-addresses', '')
                    print(f"  {i}. {r.get('chain')} {r.get('action')} " +
                          (f" → {to_addr}" if to_addr else ""))
            else:
                print("  (No rules)")
                
        elif args.command == 'interfaces':
            print("🔌 Network Interfaces")
            interfaces = quick.network.get_interfaces()
            for i in interfaces:
                name = i.get('name', 'N/A')
                running = i.get('running') == 'true'
                status = "✅" if running else "❌"
                print(f"  {status} {name} ({i.get('type', 'N/A')}) - {i.get('mac-address', 'N/A')}")
                
        elif args.command == 'routes':
            print("🛤️ Routing Table")
            routes = quick.network.get_routes()
            for i, r in enumerate(routes):
                print(f"  {i}. {r.get('dst-address')} via {r.get('gateway')} ({r.get('distance')})")
                
        elif args.command == 'cmd':
            if not args.args:
                print("❌ Please specify command path, e.g., /system/resource/print")
                return
            
            res = api.run_command(args.args[0], args.args[1:])
            if res:
                for i, entry in enumerate(res):
                    print(f"\n[{i}]")
                    for k, v in entry.items():
                        print(f"  {k}: {v}")
            else:
                print("(No results)")

if __name__ == '__main__':
    main()
