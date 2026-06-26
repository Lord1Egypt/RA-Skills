#!/usr/bin/env python3
"""Network Controller - Linux version."""
import subprocess, json, sys, os, argparse
from common import run_cmd

def list_adapters():
    """List all network adapters."""
    stdout, _, code = run_cmd(['ip', 'link'])
    return json.dumps({"adapters": stdout if code == 0 else "error"}, indent=2)

def get_adapter_info(name):
    """Get adapter details."""
    stdout, _, code = run_cmd(['ip', 'addr', 'show', name])
    return json.dumps({"info": stdout if code == 0 else "error"}, indent=2)

def enable_adapter(name):
    """Enable network adapter."""
    stdout, _, code = run_cmd(['ip', 'link', 'set', name, 'up'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def disable_adapter(name):
    """Disable network adapter (requires confirmation)."""
    stdout, _, code = run_cmd(['ip', 'link', 'set', name, 'down'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def scan_wifi():
    """Scan available WiFi networks."""
    stdout, _, code = run_cmd(['nmcli', 'device', 'wifi', 'list'])
    return json.dumps({"networks": stdout if code == 0 else "error"}, indent=2)

def get_wifi_status():
    """Get current WiFi connection status."""
    stdout, _, code = run_cmd(['nmcli', 'device', 'wifi', 'show'])
    return json.dumps({"status": stdout if code == 0 else "error"}, indent=2)

def connect_wifi(ssid, password):
    """Connect to WiFi network."""
    stdout, _, code = run_cmd(['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def disconnect_wifi():
    """Disconnect current WiFi."""
    stdout, _, code = run_cmd(['nmcli', 'device', 'disconnect', 'wlan0'])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_dns_ip():
    """Get all adapter IP configurations."""
    stdout, _, code = run_cmd(['ip', 'addr'])
    return json.dumps({"ip_config": stdout if code == 0 else "error"}, indent=2)

def get_dns():
    """Get DNS configuration."""
    stdout, _, code = run_cmd(['nmcli', 'device', 'show', '|', 'grep', 'DNS'])
    return json.dumps({"dns": stdout if code == 0 else "error"}, indent=2)

def get_adapter_dns(name):
    """Get DNS for specific adapter."""
    stdout, _, code = run_cmd(['nmcli', 'device', 'show', name, '|', 'grep', 'DNS'])
    return json.dumps({"dns": stdout if code == 0 else "error"}, indent=2)

def set_dns(adapter, servers):
    """Set DNS for adapter."""
    server_list = servers.split(',')
    stdout, _, code = run_cmd(['nmcli', 'connection', 'modify', adapter, 'ipv4.dns', servers])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def reset_dns(adapter):
    """Reset DNS to DHCP auto."""
    stdout, _, code = run_cmd(['nmcli', 'connection', 'modify', adapter, 'ipv4.dns', ''])
    return json.dumps({"success": code == 0, "message": stdout}, indent=2)

def get_proxy():
    """Get current proxy settings."""
    env = os.environ
    proxy_info = {
        "http_proxy": env.get('http_proxy'),
        "https_proxy": env.get('https_proxy'),
        "no_proxy": env.get('no_proxy')
    }
    return json.dumps({"proxy": proxy_info}, indent=2)

def set_proxy(address, port):
    """Set proxy (requires confirmation)."""
    os.environ['http_proxy'] = f'http://{address}:{port}'
    os.environ['https_proxy'] = f'http://{address}:{port}'
    return json.dumps({"success": True, "message": "Proxy set"}, indent=2)

def disable_proxy():
    """Disable proxy."""
    if 'http_proxy' in os.environ:
        del os.environ['http_proxy']
    if 'https_proxy' in os.environ:
        del os.environ['https_proxy']
    return json.dumps({"success": True, "message": "Proxy disabled"}, indent=2)

def ping_host(host, count=4):
    """Ping a host."""
    stdout, _, code = run_cmd(['ping', '-c', str(count), host])
    return json.dumps({"ping_result": stdout if code == 0 else "error"}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Network Controller')
    subparsers = parser.add_subparsers(dest='command')

    # adapter commands
    adapter_parser = subparsers.add_parser('adapter')
    adapter_subparsers = adapter_parser.add_subparsers(dest='adapter_cmd')
    adapter_subparsers.add_parser('list')
    adapter_info = adapter_subparsers.add_parser('info')
    adapter_info.add_argument('--name', required=True)
    adapter_enable = adapter_subparsers.add_parser('enable')
    adapter_enable.add_argument('--name', required=True)
    adapter_disable = adapter_subparsers.add_parser('disable')
    adapter_disable.add_argument('--name', required=True)

    # wifi commands
    wifi_parser = subparsers.add_parser('wifi')
    wifi_subparsers = wifi_parser.add_subparsers(dest='wifi_cmd')
    wifi_subparsers.add_parser('scan')
    wifi_subparsers.add_parser('status')
    wifi_connect = wifi_subparsers.add_parser('connect')
    wifi_connect.add_argument('--ssid', required=True)
    wifi_connect.add_argument('--password', required=True)
    wifi_subparsers.add_parser('disconnect')
    wifi_subparsers.add_parser('profiles')
    wifi_profile = wifi_subparsers.add_parser('profile-detail')
    wifi_profile.add_argument('--ssid', required=True)
    wifi_forget = wifi_subparsers.add_parser('forget')
    wifi_forget.add_argument('--ssid', required=True)

    # dns commands
    dns_parser = subparsers.add_parser('dns')
    dns_subparsers = dns_parser.add_subparsers(dest='dns_cmd')
    dns_subparsers.add_parser('get-ip')
    dns_subparsers.add_parser('get')
    dns_adapter = dns_subparsers.add_parser('adapter')
    dns_adapter.add_argument('--name', required=True)
    dns_set = dns_subparsers.add_parser('set')
    dns_set.add_argument('--adapter', required=True)
    dns_set.add_argument('--servers', required=True)
    dns_reset = dns_subparsers.add_parser('reset')
    dns_reset.add_argument('--adapter', required=True)

    # proxy commands
    proxy_parser = subparsers.add_parser('proxy')
    proxy_subparsers = proxy_parser.add_subparsers(dest='proxy_cmd')
    proxy_subparsers.add_parser('get')
    proxy_set = proxy_subparsers.add_parser('set')
    proxy_set.add_argument('--address', required=True)
    proxy_set.add_argument('--port', type=int, required=True)
    proxy_subparsers.add_parser('disable')

    # connectivity commands
    conn_parser = subparsers.add_parser('connectivity')
    conn_subparsers = conn_parser.add_subparsers(dest='conn_cmd')
    conn_ping = conn_subparsers.add_parser('ping')
    conn_ping.add_argument('--host', required=True)
    conn_ping.add_argument('--count', type=int, default=4)

    args = parser.parse_args()

    if args.command == 'adapter':
        if args.adapter_cmd == 'list':
            print(list_adapters())
        elif args.adapter_cmd == 'info':
            print(get_adapter_info(args.name))
        elif args.adapter_cmd == 'enable':
            print(enable_adapter(args.name))
        elif args.adapter_cmd == 'disable':
            print(disable_adapter(args.name))
    elif args.command == 'wifi':
        if args.wifi_cmd == 'scan':
            print(scan_wifi())
        elif args.wifi_cmd == 'status':
            print(get_wifi_status())
        elif args.wifi_cmd == 'connect':
            print(connect_wifi(args.ssid, args.password))
        elif args.wifi_cmd == 'disconnect':
            print(disconnect_wifi())
    elif args.command == 'dns':
        if args.dns_cmd == 'get-ip':
            print(get_dns_ip())
        elif args.dns_cmd == 'get':
            print(get_dns())
        elif args.dns_cmd == 'adapter':
            print(get_adapter_dns(args.name))
        elif args.dns_cmd == 'set':
            print(set_dns(args.adapter, args.servers))
        elif args.dns_cmd == 'reset':
            print(reset_dns(args.adapter))
    elif args.command == 'proxy':
        if args.proxy_cmd == 'get':
            print(get_proxy())
        elif args.proxy_cmd == 'set':
            print(set_proxy(args.address, args.port))
        elif args.proxy_cmd == 'disable':
            print(disable_proxy())
    elif args.command == 'connectivity' and args.conn_cmd == 'ping':
        print(ping_host(args.host, args.count))

if __name__ == '__main__':
    main()
