#!/usr/bin/env python3
"""
MikroTik RouterOS Skill - 命令处理器
"""

import sys
import os
import re

# 添加 API 库路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mikrotik-api'))

from client import MikroTikAPI
from commands import QuickCommands


def get_device_config(device_name=None):
    """
    获取设备配置（从 TOOLS.md 或环境变量）
    
    优先级：环境变量 > TOOLS.md > 默认值
    
    支持空密码和有密码两种情况
    """
    devices = {}
    
    # 1. 首先尝试从环境变量读取（最高优先级）
    env_host = os.environ.get('MIKROTIK_HOST')
    env_user = os.environ.get('MIKROTIK_USER', 'admin')
    env_pass = os.environ.get('MIKROTIK_PASS', '')  # 空密码是允许的
    
    if env_host:
        devices['default'] = {
            'host': env_host,
            'username': env_user,
            'password': env_pass  # 支持空字符串
        }
    
    # 2. 从 TOOLS.md 读取配置
    tools_md_path = os.path.expanduser('~/.openclaw/workspace/TOOLS.md')
    if os.path.exists(tools_md_path):
        try:
            with open(tools_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析 MikroTik 设备配置
            # 格式：- **名称**：IP, 用户名，密码 (可选)
            # 示例：- **office**: 192.168.1.1, admin, 空密码
            # 示例：- **home**：192.168.88.1, admin, mypassword123
            mikrotik_section = re.search(r'###\s*MikroTik 设备.*?\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
            if mikrotik_section:
                section_text = mikrotik_section.group(1)
                
                # 提取每个设备配置
                device_pattern = r'-\s*\*\*([^*]+)\*\*[:：]\s*([^,\n]+),\s*([^,\n]+),\s*(.+?)\s*$'
                matches = re.findall(device_pattern, section_text, re.MULTILINE)
                
                for name, host, username, password in matches:
                    device_key = name.strip().lower()
                    # 处理"空密码"的情况
                    pwd = password.strip()
                    if pwd.lower() in ['空密码', '无密码', 'none', 'null', '']:
                        pwd = ''
                    
                    devices[device_key] = {
                        'host': host.strip(),
                        'username': username.strip(),
                        'password': pwd
                    }
        except Exception as e:
            print(f"⚠️ 读取 TOOLS.md 失败：{e}")
    
    # 3. 返回请求的设备配置
    if device_name:
        # 优先返回环境变量配置的 default
        if device_name.lower() in ['default', '默认'] and 'default' in devices:
            return devices['default']
        return devices.get(device_name.lower())
    
    # 没有指定设备时，返回第一个可用的
    if 'default' in devices:
        return devices['default']
    if devices:
        return list(devices.values())[0]
    
    return None


def backup_config(api, quick):
    """备份路由器配置"""
    try:
        # 创建备份文件
        backup_cmd = '/system/backup/save name=backup-' + quick.api._send_word('/system/clock/print')[0].split('=')[1]
        result = api.run_cmd(backup_cmd)
        
        # 列出备份文件
        files = api.run_cmd('/file/print where name~"backup"')
        
        lines = [
            "💾 MikroTik 配置备份",
            "=" * 60,
        ]
        
        if files:
            for f in files:
                lines.append(f"  ✅ {f.get('name', 'N/A')} ({f.get('size', 'N/A')} bytes)")
        
        lines.append("=" * 60)
        lines.append("💡 提示：备份文件可通过 Files 菜单下载，或使用 /export 命令导出配置")
        
        return "\n".join(lines)
    except Exception as e:
        return f"❌ 备份失败：{e}"


def cleanup_storage(api, quick):
    """清理路由器存储空间"""
    try:
        # 获取文件列表
        files = api.run_cmd('/file/print')
        
        # 找出可删除的文件（日志、备份等）
        deletable = []
        for f in files:
            name = f.get('name', '')
            if any(x in name.lower() for x in ['.log', 'backup-', 'debug']):
                deletable.append(f)
        
        lines = [
            "🧹 存储空间清理建议",
            "=" * 60,
        ]
        
        if deletable:
            lines.append("可删除的文件:")
            for f in deletable[:10]:  # 最多显示 10 个
                lines.append(f"  - {f.get('name', 'N/A')} ({f.get('size', '0')} bytes)")
            
            if len(deletable) > 10:
                lines.append(f"  ... 还有 {len(deletable) - 10} 个文件")
            
            lines.append("")
            lines.append("💡 执行清理命令:")
            lines.append("  在 mikrotik 上执行：/file remove [find name~\"backup\"]")
        else:
            lines.append("✅ 无需清理，存储空间充足")
        
        # 显示存储使用情况
        resource = quick.system.get_resource()
        free_mem = resource.get('free-memory', 'N/A')
        lines.append("")
        lines.append(f"当前可用内存：{free_mem}")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    except Exception as e:
        return f"❌ 清理检查失败：{e}"


def configure_api_access(api, quick):
    """配置 API 访问限制"""
    try:
        # 获取当前 API 服务配置
        api_services = api.run_cmd('/ip/service/print where name="api"')
        api_ssl_services = api.run_cmd('/ip/service/print where name="api-ssl"')
        
        lines = [
            "🔐 API 访问配置",
            "=" * 60,
        ]
        
        if api_services:
            svc = api_services[0]
            lines.append(f"API 服务：{'✅ 启用' if not svc.get('disabled', True) else '❌ 禁用'}")
            lines.append(f"  端口：{svc.get('port', '8728')}")
            lines.append(f"  地址：{svc.get('address', '0.0.0.0/0')}")
        
        if api_ssl_services:
            svc = api_ssl_services[0]
            lines.append(f"API-SSL 服务：{'✅ 启用' if not svc.get('disabled', True) else '❌ 禁用'}")
            lines.append(f"  端口：{svc.get('port', '8729')}")
            lines.append(f"  地址：{svc.get('address', '0.0.0.0/0')}")
        
        lines.append("")
        lines.append("💡 安全建议:")
        lines.append("  1. 限制 API 访问地址：/ip/service set api address=10.254.252.0/24")
        lines.append("  2. 禁用不必要的服务：/ip/service disable api-ssl")
        lines.append("  3. 使用强密码")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    except Exception as e:
        return f"❌ 查询失败：{e}"


def format_status(api, quick):
    """格式化设备状态"""
    identity = quick.system.get_identity()
    resource = quick.system.get_resource()
    
    # 获取 RouterBOARD 信息（正确解读固件字段）
    routerboard = quick.system.get_version()
    
    lines = [
        "📡 MikroTik RouterOS 设备状态",
        "=" * 60,
        f"  设备名：{identity.get('name', 'N/A')}",
        f"  RouterOS: {resource.get('version', 'N/A')}",
        f"  型号：{routerboard.get('model', 'N/A')} ({routerboard.get('board-name', 'N/A')})",
        f"  运行时间：{resource.get('uptime', 'N/A')}",
        f"  CPU: {resource.get('cpu', 'N/A')} @ {resource.get('cpu-frequency', 'N/A')}MHz",
        f"  CPU 负载：{resource.get('cpu-load', 'N/A')}%",
        f"  内存：{int(resource.get('free-memory', 0))/1024/1024:.1f}MB / "
        f"{int(resource.get('total-memory', 1))/1024/1024:.1f}MB",
        f"  存储：{int(resource.get('free-hdd-space', 0))/1024/1024:.1f}MB / "
        f"{int(resource.get('total-hdd-space', 1))/1024/1024:.1f}MB",
        "=" * 60,
    ]
    
    # 显示固件信息（正确解读字段）
    if routerboard and routerboard.get('routerboard') == 'true':
        lines.append(f"\n🔧 RouterBOARD 信息:")
        lines.append(f"  序列号：{routerboard.get('serial-number', 'N/A')}")
        # upgrade-firmware 是当前实际使用的固件版本
        firmware = routerboard.get('upgrade-firmware', routerboard.get('current-firmware', 'N/A'))
        lines.append(f"  固件版本：{firmware}")
    
    # 接口状态
    lines.append("\n🔌 网络接口:")
    interfaces = quick.network.get_interfaces()
    for iface in interfaces:
        name = iface.get('name', 'unknown')
        running = iface.get('running', 'false') == 'true'
        status = "✅" if running else "❌"
        lines.append(f"  {status} {name}")
    
    # IP 地址
    lines.append("\n🌐 IP 地址:")
    addresses = quick.network.get_ip_addresses()
    for addr in addresses:
        lines.append(f"  - {addr.get('address', 'N/A')} on {addr.get('interface', 'N/A')}")
    
    # 默认路由
    lines.append("\n🛤️ 默认路由:")
    routes = quick.network.get_routes()
    for route in routes:
        if route.get('dst-address') == '0.0.0.0/0':
            lines.append(f"  - 默认网关：{route.get('gateway', 'N/A')}")
    
    return "\n".join(lines)


def format_firewall(api, quick):
    """格式化防火墙信息"""
    lines = [
        "🔥 MikroTik 防火墙配置",
        "=" * 60,
    ]
    
    # 过滤规则
    lines.append("\n📋 过滤规则:")
    rules = quick.firewall.get_filter_rules()
    if rules:
        for i, rule in enumerate(rules, 1):
            chain = rule.get('chain', 'N/A')
            action = rule.get('action', 'N/A')
            disabled = rule.get('disabled', '') == 'true'
            comment = rule.get('comment', '')
            status = "⏸️" if disabled else "✅"
            lines.append(f"  {status} [{i}] {chain}: {action}" + (f" ({comment})" if comment else ""))
    else:
        lines.append("  (无规则)")
    
    # NAT 规则
    lines.append("\n🔄 NAT 规则:")
    rules = quick.firewall.get_nat_rules()
    if rules:
        for i, rule in enumerate(rules, 1):
            chain = rule.get('chain', 'N/A')
            action = rule.get('action', 'N/A')
            to_addr = rule.get('to-addresses', '')
            comment = rule.get('comment', '')
            line = f"  [{i}] {chain}: {action}"
            if to_addr:
                line += f" → {to_addr}"
            if comment:
                line += f" ({comment})"
            lines.append(line)
    else:
        lines.append("  (无规则)")
    
    # 活动连接
    lines.append("\n🔗 活动连接数：检查中...")
    
    return "\n".join(lines)


def format_interfaces(api, quick):
    """格式化接口信息"""
    lines = [
        "🔌 网络接口",
        "=" * 60,
    ]
    
    interfaces = quick.network.get_interfaces()
    for iface in interfaces:
        name = iface.get('name', 'unknown')
        running = iface.get('running', 'false') == 'true'
        mtu = iface.get('mtu', 'N/A')
        mac = iface.get('mac-address', 'N/A')
        status = "✅" if running else "❌"
        lines.append(f"  {status} {name} (MTU: {mtu}, MAC: {mac})")
    
    return "\n".join(lines)


def format_dhcp(api, quick):
    """格式化 DHCP 信息"""
    lines = [
        "📋 DHCP 配置",
        "=" * 60,
    ]
    
    # DHCP 服务器
    lines.append("\n🖥️ DHCP 服务器:")
    servers = quick.network.get_dhcp_servers()
    for srv in servers:
        name = srv.get('name', 'N/A')
        iface = srv.get('interface', 'N/A')
        lines.append(f"  - {name} on {iface}")
    
    # DHCP 租约
    lines.append("\n📝 DHCP 租约:")
    leases = quick.network.get_dhcp_leases()
    if leases:
        for i, lease in enumerate(leases[:20], 1):  # 最多显示 20 条
            ip = lease.get('address', 'N/A')
            mac = lease.get('mac-address', 'N/A')
            host = lease.get('host-name', 'N/A')
            status = lease.get('status', 'N/A')
            lines.append(f"  {i}. {ip} - {mac}" + (f" ({host})" if host else "") + f" [{status}]")
        if len(leases) > 20:
            lines.append(f"  ... 还有 {len(leases) - 20} 条租约")
    else:
        lines.append("  (无租约)")
    
    return "\n".join(lines)


def format_clients(api, quick):
    """格式化无线客户端列表 (CAPsMAN)"""
    lines = [
        "📶 无线客户端 (CAPsMAN)",
        "=" * 60,
    ]
    
    # 获取 CAPsMAN 注册表
    reg = api.run_command('/caps-man/registration-table/print')
    
    if reg:
        lines.append(f"\n✅ 已连接 {len(reg)} 个无线客户端:\n")
        for i, client in enumerate(reg, 1):
            mac = client.get('mac-address', 'N/A')
            ssid = client.get('ssid', 'N/A')
            iface = client.get('interface', 'N/A')
            signal = client.get('rx-signal', 'N/A')
            tx_rate = client.get('tx-rate', 'N/A')
            rx_rate = client.get('rx-rate', 'N/A')
            uptime = client.get('uptime', 'N/A')
            last_ip = client.get('last-ip', 'N/A')
            packets_tx = client.get('packets', 'N/A')
            bytes_tx = client.get('bytes', 'N/A')
            
            # 解析流量统计
            traffic_info = ""
            if packets_tx != 'N/A' and ',' in str(packets_tx):
                pkt = str(packets_tx).split(',')
                bytes_list = str(bytes_tx).split(',') if ',' in str(bytes_tx) else ['N/A', 'N/A']
                # 内联字节格式化
                def fmt_b(b):
                    if not b.isdigit():
                        return 'N/A'
                    b = int(b)
                    if b >= 1024**3:
                        return f"{b/1024**3:.1f}GB"
                    elif b >= 1024**2:
                        return f"{b/1024**2:.1f}MB"
                    elif b >= 1024:
                        return f"{b/1024:.1f}KB"
                    else:
                        return f"{b}B"
                tx_b = fmt_b(bytes_list[0])
                rx_b = fmt_b(bytes_list[1]) if len(bytes_list) > 1 else 'N/A'
                traffic_info = f"\n       流量：TX {tx_b} / RX {rx_b}"
            
            # 信号强度评级
            signal_rating = ""
            try:
                sig = int(signal.replace(' dBm', '').replace('-', '')) if signal != 'N/A' else 0
                if sig <= 35:
                    signal_rating = "⭐⭐⭐⭐⭐"
                elif sig <= 45:
                    signal_rating = "⭐⭐⭐⭐"
                elif sig <= 55:
                    signal_rating = "⭐⭐⭐"
                elif sig <= 65:
                    signal_rating = "⭐⭐"
                else:
                    signal_rating = "⭐"
            except:
                pass
            
            lines.append(f"  【客户端 {i}】")
            lines.append(f"    MAC: {mac}")
            lines.append(f"    SSID: {ssid} | 接口：{iface}")
            lines.append(f"    信号：{signal} {signal_rating}")
            lines.append(f"    速率：TX {tx_rate} | RX {rx_rate}")
            lines.append(f"    连接时间：{uptime}")
            lines.append(f"    IP 地址：{last_ip}{traffic_info}")
            lines.append("")
    else:
        lines.append("\n❌ 当前没有无线客户端连接")
        lines.append("\n💡 提示：")
        lines.append("  1. 确认 CAPsMAN 已启用 (/caps-man/manager)")
        lines.append("  2. 确认 AP 已注册为 CAP (/interface/wireless/cap)")
        lines.append("  3. 检查无线配置模板 (/caps-man/configuration)")
    
    return "\n".join(lines)


def format_arp(api, quick):
    """格式化 ARP 表"""
    lines = [
        "📋 ARP 表",
        "=" * 60,
    ]
    
    arp_entries = quick.network.get_arp()
    if arp_entries:
        lines.append(f"\n共 {len(arp_entries)} 条记录:\n")
        for i, entry in enumerate(arp_entries[:30], 1):  # 最多显示 30 条
            ip = entry.get('address', 'N/A')
            mac = entry.get('mac-address', 'N/A')
            iface = entry.get('interface', 'N/A')
            lines.append(f"  {i}. {ip} → {mac} ({iface})")
        if len(arp_entries) > 30:
            lines.append(f"  ... 还有 {len(arp_entries) - 30} 条记录")
    else:
        lines.append("  (无记录)")
    
    return "\n".join(lines)


def format_wireguard(api, quick):
    """格式化 WireGuard 信息"""
    lines = [
        "🔐 WireGuard 配置",
        "=" * 60,
    ]
    
    peers = quick.network.get_wireguard_peers()
    if peers:
        lines.append(f"\n共 {len(peers)} 个对等体:\n")
        for i, peer in enumerate(peers, 1):
            name = peer.get('name', 'N/A')
            pubkey = peer.get('public-key', 'N/A')[:20] + '...' if peer.get('public-key') else 'N/A'
            endpoint = peer.get('endpoint', 'N/A')
            allowed = peer.get('allowed-address', 'N/A')
            lines.append(f"  {i}. {name}")
            lines.append(f"     公钥：{pubkey}")
            lines.append(f"     端点：{endpoint}")
            lines.append(f"     允许：{allowed}")
    else:
        lines.append("  (无 WireGuard 对等体)")
    
    return "\n".join(lines)


def format_users(api, quick):
    """格式化用户信息"""
    lines = [
        "👤 用户配置",
        "=" * 60,
    ]
    
    # 系统用户
    lines.append("\n🔐 系统用户:")
    users = quick.system.get_users()
    for user in users:
        name = user.get('name', 'N/A')
        group = user.get('group', 'N/A')
        disabled = user.get('disabled', '') == 'true'
        status = "⏸️" if disabled else "✅"
        lines.append(f"  {status} {name} ({group})")
    
    # PPP 用户
    ppp_users = quick.user.get_ppp_users()
    if ppp_users:
        lines.append(f"\n📞 PPP 用户 ({len(ppp_users)}):")
        for user in ppp_users[:10]:
            name = user.get('name', 'N/A')
            service = user.get('service', 'N/A')
            lines.append(f"  - {name} ({service})")
        if len(ppp_users) > 10:
            lines.append(f"  ... 还有 {len(ppp_users) - 10} 个用户")
    
    return "\n".join(lines)


def format_logs(api, quick):
    """格式化日志信息"""
    lines = [
        "📝 系统日志 (最近 20 条)",
        "=" * 60,
    ]
    
    logs = quick.system.get_recent_logs(20)
    if logs:
        for log in logs:
            time = log.get('time', 'N/A')
            topics = log.get('topics', 'N/A')
            message = log.get('message', 'N/A')
            lines.append(f"  [{time}] {topics}: {message}")
    else:
        lines.append("  (无日志)")
    
    return "\n".join(lines)


def format_services(api, quick):
    """格式化系统服务"""
    lines = [
        "🔧 系统服务",
        "=" * 60,
    ]
    
    services = quick.system.get_services()
    for svc in services:
        name = svc.get('name', 'N/A')
        port = svc.get('port', 'N/A')
        disabled = svc.get('disabled', '') == 'true'
        status = "⏸️" if disabled else "✅"
        lines.append(f"  {status} {name} (端口：{port})")
    
    return "\n".join(lines)


def format_traffic(api, quick):
    """格式化接口流量统计"""
    lines = [
        "📈 接口流量统计",
        "=" * 60,
    ]
    
    stats = quick.network.get_interface_stats()
    
    if not stats:
        lines.append("  (无数据)")
        return "\n".join(lines)
    
    # 表头
    lines.append("")
    lines.append(f"  {'接口':<20} {'接收 ↓':<15} {'发送 ↑':<15} {'包数':<12} {'错误/丢弃'}")
    lines.append("  " + "-" * 70)
    
    for iface in stats:
        name = iface.get('name', 'unknown')[:18]
        rx_bytes = int(iface.get('rx-byte', 0))
        tx_bytes = int(iface.get('tx-byte', 0))
        rx_packets = int(iface.get('rx-packet', 0))
        tx_packets = int(iface.get('tx-packet', 0))
        rx_errors = int(iface.get('rx-error', 0))
        tx_errors = int(iface.get('tx-error', 0))
        rx_drops = int(iface.get('rx-drop', 0))
        tx_drops = int(iface.get('tx-drop', 0))
        
        # 格式化流量（转换为 MB/GB）
        def format_bytes(b):
            if b >= 1024**3:
                return f"{b/1024**3:.1f}GB"
            elif b >= 1024**2:
                return f"{b/1024**2:.1f}MB"
            elif b >= 1024:
                return f"{b/1024:.1f}KB"
            else:
                return f"{b}B"
        
        rx_str = format_bytes(rx_bytes)
        tx_str = format_bytes(tx_bytes)
        packets_str = f"{rx_packets + tx_packets:,}"
        errors_str = f"{rx_errors + tx_errors}/{rx_drops + tx_drops}"
        
        lines.append(f"  {name:<20} {rx_str:>14} {tx_str:>14} {packets_str:>12} {errors_str}")
    
    lines.append("  " + "-" * 70)
    lines.append(f"\n总计：{len(stats)} 个接口")
    
    return "\n".join(lines)


def format_interface_detail(api, quick, interface_name: str = ''):
    """格式化接口详细信息"""
    lines = [
        f"🔌 接口详情" + (f": {interface_name}" if interface_name else ""),
        "=" * 60,
    ]
    
    if interface_name:
        stats = quick.network.get_interface_stats(interface_name)
    else:
        stats = quick.network.get_interface_stats()
    
    if not stats:
        lines.append(f"  ❌ 未找到接口：{interface_name}" if interface_name else "  (无数据)")
        return "\n".join(lines)
    
    for iface in stats:
        name = iface.get('name', 'unknown')
        iface_type = iface.get('type', 'N/A')
        running = iface.get('running', 'false') == 'true'
        mtu = iface.get('mtu', 'N/A')
        mac = iface.get('mac-address', 'N/A')
        rx_bytes = int(iface.get('rx-byte', 0))
        tx_bytes = int(iface.get('tx-byte', 0))
        
        lines.append(f"\n📌 {name}")
        lines.append(f"  类型：{iface_type}")
        lines.append(f"  状态：{'✅ 运行中' if running else '❌ 已关闭'}")
        lines.append(f"  MTU: {mtu}")
        lines.append(f"  MAC: {mac}")
        lines.append(f"  接收：{rx_bytes / 1024 / 1024:.2f} MB ({int(iface.get('rx-packet', 0)):,} 包)")
        lines.append(f"  发送：{tx_bytes / 1024 / 1024:.2f} MB ({int(iface.get('tx-packet', 0)):,} 包)")
        
        # VLAN 信息
        if iface_type == 'vlan':
            vlan_id = iface.get('vlan-id', 'N/A')
            interface = iface.get('interface', 'N/A')
            lines.append(f"  VLAN ID: {vlan_id} (on {interface})")
        
        # Bridge 信息
        if iface_type == 'bridge':
            lines.append(f"  桥接模式")
        
        # WireGuard 信息
        if iface_type == 'wireguard':
            lines.append(f"  WireGuard VPN 接口")
    
    return "\n".join(lines)


def format_vlan(api, quick):
    """格式化 VLAN 配置"""
    lines = [
        "🏷️ VLAN 配置",
        "=" * 60,
    ]
    
    vlans = quick.network.get_vlan()
    if vlans:
        for vlan in vlans:
            name = vlan.get('name', 'N/A')
            vlan_id = vlan.get('vlan-id', 'N/A')
            interface = vlan.get('interface', 'N/A')
            running = vlan.get('running', 'false') == 'true'
            status = "✅" if running else "❌"
            lines.append(f"  {status} {name} (ID: {vlan_id}, on {interface})")
    else:
        lines.append("  (无 VLAN 配置)")
    
    return "\n".join(lines)


def format_bridge(api, quick):
    """格式化桥接配置"""
    lines = [
        "🌉 桥接配置",
        "=" * 60,
    ]
    
    bridges = quick.network.get_bridge()
    if bridges:
        for bridge in bridges:
            name = bridge.get('name', 'N/A')
            running = bridge.get('running', 'false') == 'true'
            status = "✅" if running else "❌"
            lines.append(f"  {status} {name}")
        
        # 桥接端口
        lines.append("\n🔌 桥接端口:")
        ports = quick.network.get_bridge_ports()
        for port in ports[:20]:  # 最多显示 20 个
            bridge_name = port.get('bridge', 'N/A')
            interface = port.get('interface', 'N/A')
            hw = port.get('hw', 'false') == 'true'
            lines.append(f"  - {interface} → {bridge_name}" + (" (硬件转发)" if hw else ""))
        if len(ports) > 20:
            lines.append(f"  ... 还有 {len(ports) - 20} 个端口")
    else:
        lines.append("  (无桥接配置)")
    
    return "\n".join(lines)


def format_health(api, quick):
    """格式化系统健康信息"""
    lines = [
        "🌡️ 系统健康",
        "=" * 60,
    ]
    
    # 系统资源
    resource = quick.system.get_resource()
    lines.append(f"\n💻 系统资源:")
    lines.append(f"  CPU 负载：{resource.get('cpu-load', 'N/A')}%")
    
    # 内存
    free_mem = int(resource.get('free-memory', 0)) / 1024 / 1024
    total_mem = int(resource.get('total-memory', 1)) / 1024 / 1024
    used_mem = total_mem - free_mem
    mem_percent = (used_mem / total_mem * 100) if total_mem > 0 else 0
    lines.append(f"  内存使用：{used_mem:.1f}MB / {total_mem:.1f}MB ({mem_percent:.1f}%)")
    
    # 存储
    free_hdd = int(resource.get('free-hdd-space', 0)) / 1024 / 1024
    total_hdd = int(resource.get('total-hdd-space', 1)) / 1024 / 1024
    used_hdd = total_hdd - free_hdd
    hdd_percent = (used_hdd / total_hdd * 100) if total_hdd > 0 else 0
    lines.append(f"  存储使用：{used_hdd:.1f}MB / {total_hdd:.1f}MB ({hdd_percent:.1f}%)")
    
    # 硬件健康状态（温度、电压、风扇）
    health = quick.system.get_health()
    if health:
        lines.append(f"\n🔧 硬件状态:")
        
        # 温度
        temperature = health.get('temperature', '')
        if temperature:
            temp_value = temperature.replace('°C', '').strip()
            try:
                temp_num = float(temp_value)
                if temp_num > 70:
                    temp_icon = "🔥"
                elif temp_num > 50:
                    temp_icon = "⚠️"
                else:
                    temp_icon = "✅"
                lines.append(f"  {temp_icon} 温度：{temperature}")
            except:
                lines.append(f"  🌡️ 温度：{temperature}")
        
        # 电压
        voltage = health.get('voltage', '')
        if voltage:
            lines.append(f"  ⚡ 电压：{voltage}")
        
        # 风扇状态
        psu1_state = health.get('psu1-state', '')
        psu2_state = health.get('psu2-state', '')
        fan1_state = health.get('fan1-state', '')
        fan2_state = health.get('fan2-state', '')
        
        if psu1_state:
            psu1_icon = "✅" if psu1_state == 'ok' else "❌"
            lines.append(f"  {psu1_icon} 电源 1: {psu1_state}")
        if psu2_state:
            psu2_icon = "✅" if psu2_state == 'ok' else "❌"
            lines.append(f"  {psu2_icon} 电源 2: {psu2_state}")
        if fan1_state:
            fan1_icon = "✅" if fan1_state == 'ok' else "❌"
            lines.append(f"  {fan1_icon} 风扇 1: {fan1_state}")
        if fan2_state:
            fan2_icon = "✅" if fan2_state == 'ok' else "❌"
            lines.append(f"  {fan2_icon} 风扇 2: {fan2_state}")
        
        # 其他健康指标
        for key, value in health.items():
            if key not in ['temperature', 'voltage', 'psu1-state', 'psu2-state', 'fan1-state', 'fan2-state']:
                if 'temperature' in key.lower() or 'voltage' in key.lower() or 'fan' in key.lower():
                    lines.append(f"  🔧 {key}: {value}")
    else:
        lines.append(f"\n🔧 硬件状态：不支持或未配置")
    
    # 运行时间
    uptime = resource.get('uptime', 'N/A')
    lines.append(f"\n⏱️ 运行时间：{uptime}")
    
    # 看门狗状态
    watchdog = quick.system.get_watchdog()
    if watchdog:
        lines.append(f"\n🐕 看门狗:")
        enabled = watchdog.get('watchdog-timer', '') != 'no'
        lines.append(f"  状态：{'✅ 已启用' if enabled else '❌ 已禁用'}")
        if watchdog.get('watchdog-timer', '') != 'no':
            lines.append(f"  超时：{watchdog.get('watchdog-timer', 'N/A')}")
    
    return "\n".join(lines)


def format_scheduler(api, quick):
    """格式化计划任务"""
    lines = [
        "📅 计划任务",
        "=" * 60,
    ]
    
    schedulers = quick.system.get_scheduler()
    if schedulers:
        lines.append(f"\n共 {len(schedulers)} 个任务:\n")
        for i, sched in enumerate(schedulers[:20], 1):
            name = sched.get('name', 'N/A')
            interval = sched.get('interval', 'N/A')
            on_event = sched.get('on-event', 'N/A')
            disabled = sched.get('disabled', '') == 'true'
            status = "⏸️" if disabled else "✅"
            lines.append(f"  {status} [{i}] {name}")
            lines.append(f"      间隔：{interval}")
            lines.append(f"      执行：{on_event}")
        if len(schedulers) > 20:
            lines.append(f"  ... 还有 {len(schedulers) - 20} 个任务")
    else:
        lines.append("  (无计划任务)")
    
    return "\n".join(lines)


def format_neighbors(api, quick):
    """格式化邻居设备发现"""
    lines = [
        "📡 邻居设备",
        "=" * 60,
    ]
    
    neighbors = quick.network.get_neighbors()
    if neighbors:
        lines.append(f"\n共 {len(neighbors)} 个邻居设备:\n")
        for i, nbr in enumerate(neighbors[:20], 1):
            identity = nbr.get('identity', 'N/A')
            platform = nbr.get('platform', 'N/A')
            address = nbr.get('address', 'N/A')
            interface = nbr.get('interface', 'N/A')
            mac = nbr.get('mac-address', 'N/A')
            lines.append(f"  [{i}] {identity}")
            lines.append(f"      型号：{platform}")
            lines.append(f"      地址：{address}")
            lines.append(f"      接口：{interface}")
            if mac != 'N/A':
                lines.append(f"      MAC: {mac}")
        if len(neighbors) > 20:
            lines.append(f"  ... 还有 {len(neighbors) - 20} 个设备")
    else:
        lines.append("  (未发现邻居设备)")
    
    return "\n".join(lines)


def format_scan(api, quick):
    """格式化网络扫描结果（从 LattePanda 本地独立扫描，不依赖 API）"""
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mikrotik-api'))
    from scanner import MikroTikScanner
    
    lines = [
        "📡 网络扫描",
        "=" * 60,
    ]
    
    print("🔍 从 LattePanda 本地扫描（不依赖已知设备）...\n")
    
    # 使用独立扫描器
    scanner = MikroTikScanner(timeout=2.0)
    devices = scanner.scan()
    
    # 获取 LattePanda 本机 IP（用于排除，不扫描自己）
    self_ips = []
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True, timeout=5)
        self_ips = result.stdout.strip().split()
    except:
        pass
    
    # 排除 LattePanda 本机 IP
    if self_ips:
        original_count = len(devices)
        devices = [dev for dev in devices if dev.get('ip') not in self_ips]
        if original_count > len(devices):
            print(f"\nℹ️ 排除 {original_count - len(devices)} 个本机 IP")
            # 更新 scanner 的设备列表
            scanner.discovered_devices = devices
    
    # 如果已连接 API，尝试获取型号信息（可选增强）
    try:
        if api and api.connected and devices:
            print("\n🔍 从 API 获取设备型号（可选）...")
            neighbors = quick.network.get_neighbors()
            neighbor_map = {}
            for nbr in neighbors:
                mac = nbr.get('mac-address', '').upper()
                if mac:
                    board = nbr.get('board', '')
                    neighbor_map[mac] = {
                        'model': board if board else nbr.get('platform', ''),
                        'version': nbr.get('version', '')
                    }
            
            # 更新设备信息
            for dev in devices:
                mac = dev.get('mac', '')
                if mac in neighbor_map:
                    info = neighbor_map[mac]
                    dev['model'] = info.get('model', '')
                    dev['version'] = info.get('version', '')
                    if dev['model']:
                        print(f"  ✅ {dev['ip']}: {dev['model']}")
    except Exception as e:
        # API 不可用时，只显示 Unknown
        pass
    
    # 格式化结果
    print()
    lines.append(scanner.format_results())
    
    if not scanner.discovered_devices:
        lines.append("\n💡 提示:")
        lines.append("  - 确保 MikroTik 设备启用了 MAC Telnet/Winbox 发现")
        lines.append("  - 命令：/tool mac-server winbox set enabled=yes")
        lines.append("  - 检查防火墙是否允许 UDP 5678 端口")
        lines.append("  - 确认 LattePanda 和 MikroTik 设备在同一网段")
    
    return "\n".join(lines)


def format_connections(api, quick):
    """格式化活动连接统计"""
    lines = [
        "🔗 活动连接",
        "=" * 60,
    ]
    
    # 连接统计
    stats = quick.firewall.get_connection_stats()
    lines.append(f"\n📊 连接统计:")
    lines.append(f"  活跃连接数：{stats.get('total', 'N/A')}")
    
    # 活动连接（前 20 条）
    connections = quick.firewall.get_active_connections(20)
    if connections:
        lines.append(f"\n🔥 TOP 连接:")
        for i, conn in enumerate(connections[:20], 1):
            src = conn.get('src-address', 'N/A')
            dst = conn.get('dst-address', 'N/A')
            proto = conn.get('protocol', 'N/A')
            sport = conn.get('src-port', 'N/A')
            dport = conn.get('dst-port', 'N/A')
            lines.append(f"  {i}. {src}:{sport} → {dst}:{dport} ({proto})")
        if len(connections) == 20:
            lines.append(f"  ... 还有更多连接")
    
    return "\n".join(lines)


def format_routing(api, quick):
    """格式化路由配置"""
    lines = [
        "🌐 路由配置",
        "=" * 60,
    ]
    
    # 路由表统计
    routes = quick.routing.get_routes()
    static_routes = [r for r in routes if r.get('dynamic', '') != 'true']
    dynamic_routes = [r for r in routes if r.get('dynamic', '') == 'true']
    
    lines.append(f"\n📊 路由表统计:")
    lines.append(f"  总路由数：{len(routes)}")
    lines.append(f"  静态路由：{len(static_routes)}")
    lines.append(f"  动态路由：{len(dynamic_routes)}")
    
    # 显示静态路由
    lines.append(f"\n🛤️ 静态路由:")
    if static_routes:
        for i, route in enumerate(static_routes[:15], 1):
            dst = route.get('dst-address', 'N/A')
            gateway = route.get('gateway', 'N/A')
            distance = route.get('distance', '1')
            disabled = route.get('disabled', '') == 'true'
            status = "⏸️" if disabled else "✅"
            lines.append(f"  {status} [{i}] {dst} via {gateway} (dist: {distance})")
        if len(static_routes) > 15:
            lines.append(f"  ... 还有 {len(static_routes) - 15} 条")
    else:
        lines.append("  (无静态路由)")
    
    # OSPF 状态
    ospf_instances = quick.routing.get_ospf_instances()
    if ospf_instances:
        lines.append(f"\n🔵 OSPF 配置 ({len(ospf_instances)} 实例):")
        for inst in ospf_instances:
            name = inst.get('name', 'default')
            router_id = inst.get('router-id', 'N/A')
            lines.append(f"  - {name} (Router ID: {router_id})")
        
        # OSPF 邻居
        ospf_neighbors = quick.routing.get_ospf_neighbors()
        if ospf_neighbors:
            lines.append(f"\n🔵 OSPF 邻居 ({len(ospf_neighbors)}):")
            for nbr in ospf_neighbors[:10]:
                # 尝试多个字段名（不同 RouterOS 版本字段名可能不同）
                addr = nbr.get('neighbor-address') or nbr.get('address') or nbr.get('router-id') or 'N/A'
                state = nbr.get('state', 'N/A')
                interface = nbr.get('interface', 'N/A')
                state_icon = "✅" if state == 'Full' else "⏳"
                lines.append(f"  {state_icon} {addr} - {state} ({interface})")
            if len(ospf_neighbors) > 10:
                lines.append(f"  ... 还有 {len(ospf_neighbors) - 10} 个邻居")
    else:
        lines.append("\n🔵 OSPF: 未配置")
    
    # BGP 状态
    bgp_instances = quick.routing.get_bgp_instances()
    if bgp_instances:
        lines.append(f"\n🟠 BGP 配置 ({len(bgp_instances)} 实例):")
        for inst in bgp_instances:
            name = inst.get('name', 'default')
            as_num = inst.get('as', 'N/A')
            router_id = inst.get('router-id', 'N/A')
            lines.append(f"  - {name} (AS: {as_num}, Router ID: {router_id})")
        
        # BGP 对等体
        bgp_peers = quick.routing.get_bgp_peers()
        if bgp_peers:
            lines.append(f"\n🟠 BGP 对等体 ({len(bgp_peers)}):")
            for peer in bgp_peers[:10]:
                name = peer.get('name', 'N/A')
                remote_addr = peer.get('remote-address', 'N/A')
                remote_as = peer.get('remote-as', 'N/A')
                disabled = peer.get('disabled', '') == 'true'
                status = "⏸️" if disabled else "✅"
                lines.append(f"  {status} {name} - {remote_addr} (AS{remote_as})")
            if len(bgp_peers) > 10:
                lines.append(f"  ... 还有 {len(bgp_peers) - 10} 个对等体")
    else:
        lines.append("\n🟠 BGP: 未配置")
    
    return "\n".join(lines)


def format_queues(api, quick):
    """格式化队列/带宽限制配置"""
    lines = [
        "📊 队列/带宽限制",
        "=" * 60,
    ]
    
    # 简单队列
    lines.append("\n🎯 简单队列:")
    queues = quick.network.get_simple_queues()
    if queues:
        for i, queue in enumerate(queues, 1):
            name = queue.get('name', 'N/A')
            target = queue.get('target', 'N/A')
            max_limit = queue.get('max-limit', '0/0')
            limit_at = queue.get('limit-at', '0/0')
            disabled = queue.get('disabled', '') == 'true'
            status = "⏸️" if disabled else "✅"
            
            # 格式化带宽（转换为 Mbps）
            def format_bw(bw_str):
                try:
                    down, up = bw_str.split('/')
                    down_bps = int(down) if down.isdigit() else 0
                    up_bps = int(up) if up.isdigit() else 0
                    down_mbps = down_bps / 1000 / 1000
                    up_mbps = up_bps / 1000 / 1000
                    if down_mbps >= 1000:
                        down_str = f"{down_mbps/1000:.1f}G"
                    else:
                        down_str = f"{down_mbps:.0f}M"
                    if up_mbps >= 1000:
                        up_str = f"{up_mbps/1000:.1f}G"
                    else:
                        up_str = f"{up_mbps:.0f}M"
                    return f"{down_str}/{up_str}"
                except:
                    return bw_str
            
            bw_display = format_bw(max_limit)
            lines.append(f"  {status} [{i}] {name}")
            lines.append(f"      目标：{target}")
            lines.append(f"      限制：{bw_display} (下载/上传)")
            if limit_at != '0/0':
                lines.append(f"      保证：{format_bw(limit_at)}")
    else:
        lines.append("  (无简单队列)")
    
    # 队列树
    queue_tree = quick.network.get_queue_tree()
    if queue_tree:
        lines.append(f"\n🌳 队列树 ({len(queue_tree)} 条):")
        for i, qt in enumerate(queue_tree[:10], 1):
            name = qt.get('name', 'N/A')
            parent = qt.get('parent', 'N/A')
            packet_marks = qt.get('packet-marks', 'N/A')
            max_limit = qt.get('max-limit', '0')
            disabled = qt.get('disabled', '') == 'true'
            status = "⏸️" if disabled else "✅"
            lines.append(f"  {status} [{i}] {name} (parent: {parent})")
        if len(queue_tree) > 10:
            lines.append(f"  ... 还有 {len(queue_tree) - 10} 条")
    
    # 队列类型
    queue_types = quick.network.get_queue_types()
    if queue_types:
        lines.append(f"\n📦 队列类型 ({len(queue_types)}):")
        for qt in queue_types[:5]:
            name = qt.get('name', 'N/A')
            kind = qt.get('kind', 'N/A')
            lines.append(f"  - {name} ({kind})")
        if len(queue_types) > 5:
            lines.append(f"  ... 还有 {len(queue_types) - 5} 种")
    
    return "\n".join(lines)


def execute_command(device, command):
    """
    执行 MikroTik 命令
    
    支持空密码和有密码两种情况
    """
    config = get_device_config(device)
    
    if not config:
        # 提供友好的错误提示
        error_msg = "❌ 未找到设备配置\n\n"
        error_msg += "请在 TOOLS.md 中添加 MikroTik 设备配置:\n"
        error_msg += "```markdown\n"
        error_msg += "### MikroTik 设备\n"
        error_msg += "- **office**: 192.168.1.1, admin, 空密码\n"
        error_msg += "- **home**：192.168.88.1, admin, yourpassword\n"
        error_msg += "```\n"
        error_msg += "\n或使用环境变量:\n"
        error_msg += "- `MIKROTIK_HOST`: 设备 IP\n"
        error_msg += "- `MIKROTIK_USER`: 用户名 (可选，默认 admin)\n"
        error_msg += "- `MIKROTIK_PASS`: 密码 (可选，支持空密码)"
        return error_msg
    
    try:
        # 显示连接信息（调试用，生产环境可移除）
        pwd_display = "(空密码)" if config['password'] == '' else "(已配置密码)"
        print(f"🔌 连接设备：{config['host']} [{config['username']}] {pwd_display}")
        
        api = MikroTikAPI(
            config['host'], 
            config['username'], 
            config['password'],
            timeout=10  # 增加超时时间
        )
        
        if not api.connect():
            return f"❌ 无法连接到 {config['host']}\n\n请检查:\n1. 设备 IP 是否正确\n2. 网络是否可达\n3. API 服务是否启用（默认端口 8728）"
        
        if not api.login():
            pwd_hint = "空密码" if config['password'] == '' else "密码可能错误"
            return f"❌ 登录失败 ({pwd_hint})\n\n请检查:\n1. 用户名/密码是否正确\n2. 用户是否有 API 访问权限"
        
        quick = QuickCommands(api)
        
        # 根据命令类型返回不同格式
        if 'status' in command.lower() or '状态' in command:
            result = format_status(api, quick)
        elif '备份' in command or 'backup' in command.lower():
            result = backup_config(api, quick)
        elif '清理' in command or 'cleanup' in command.lower() or '存储' in command:
            result = cleanup_storage(api, quick)
        elif 'api' in command.lower() and ('配置' in command or 'access' in command.lower()):
            result = configure_api_access(api, quick)
        elif 'firewall' in command.lower() or '防火墙' in command:
            result = format_firewall(api, quick)
        elif 'interface' in command.lower() or '接口' in command:
            # 检查是否要查看详细信息
            if 'detail' in command.lower() or '详细' in command:
                # 提取接口名
                import re
                match = re.search(r'(ether\d+|bridge|vlan\d+|wireguard\w+|cap\d+|lo)', command)
                iface_name = match.group(1) if match else ''
                result = format_interface_detail(api, quick, iface_name)
            else:
                result = format_interfaces(api, quick)
        elif 'traffic' in command.lower() or '流量' in command:
            result = format_traffic(api, quick)
        elif 'dhcp' in command.lower():
            result = format_dhcp(api, quick)
        elif 'arp' in command.lower():
            result = format_arp(api, quick)
        elif 'client' in command.lower() or '客户端' in command or '无线' in command or 'wifi' in command or 'wi-fi' in command:
            result = format_clients(api, quick)
        elif 'wireguard' in command.lower() or 'wg' in command.lower():
            result = format_wireguard(api, quick)
        elif 'user' in command.lower() or '用户' in command:
            result = format_users(api, quick)
        elif 'log' in command.lower() or '日志' in command:
            result = format_logs(api, quick)
        elif 'service' in command.lower() or '服务' in command:
            result = format_services(api, quick)
        elif 'vlan' in command.lower():
            result = format_vlan(api, quick)
        elif 'bridge' in command.lower() or '桥接' in command:
            result = format_bridge(api, quick)
        elif 'queue' in command.lower() or '队列' in command or '带宽' in command or '限速' in command:
            result = format_queues(api, quick)
        elif 'route' in command.lower() or 'routing' in command.lower() or '路由' in command.lower() or 'ospf' in command.lower() or 'bgp' in command.lower():
            result = format_routing(api, quick)
        elif 'health' in command.lower() or '温度' in command.lower() or '电压' in command.lower() or '风扇' in command.lower() or '硬件' in command.lower():
            result = format_health(api, quick)
        elif 'scheduler' in command.lower() or '计划' in command.lower() or '定时' in command.lower() or '任务' in command.lower():
            result = format_scheduler(api, quick)
        elif 'neighbor' in command.lower() or '邻居' in command.lower() or '设备发现' in command.lower():
            result = format_neighbors(api, quick)
        elif 'connection' in command.lower() or '连接' in command.lower() or '活动连接' in command.lower():
            result = format_connections(api, quick)
        elif 'ping' in command.lower():
            # 提取目标地址
            import re
            match = re.search(r'(\d+\.\d+\.\d+\.\d+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', command)
            target = match.group(1) if match else '8.8.8.8'
            results = api.run_command('/ping', [f'=address={target}', '=count=5'])
            if results:
                result = f"🏓 Ping {target}:\n"
                for r in results:
                    if 'sent' in r:
                        result += f"  发送：{r.get('sent')}, 接收：{r.get('received')}, 丢失：{r.get('lost')}"
                    elif 'status' in r:
                        result += f"  状态：{r.get('status')}"
            else:
                result = "(无结果)"
        elif 'scan' in command.lower() or '扫描' in command.lower():
            # 扫描功能独立工作，不依赖设备配置
            result = format_scan(api, quick)
        else:
            # 执行自定义命令
            results = api.run_command(command)
            if results:
                result = "命令执行结果:\n"
                for item in results:
                    for key, value in item.items():
                        result += f"  {key}: {value}\n"
            else:
                result = "(无结果)"
        
        api.disconnect()
        return result
    
    except ConnectionRefusedError:
        return f"❌ 连接被拒绝：{config['host']}\n\n可能原因:\n1. API 服务未启用\n2. 防火墙阻止了 8728 端口\n3. 设备离线"
    except TimeoutError:
        return f"❌ 连接超时：{config['host']}\n\n请检查网络连通性"
    except Exception as e:
        return f"❌ 错误：{type(e).__name__}: {e}"


def handle_message(message):
    """处理用户消息"""
    original_message = message
    message = message.lower().strip()
    
    # 解析命令
    if 'mikrotik' in message or 'routeros' in message or '路由器' in message:
        # 提取设备名称（支持中文和英文）
        device = None
        
        # 尝试从 TOOLS.md 中匹配已配置的设备名称
        tools_md_path = os.path.expanduser('~/.openclaw/workspace/TOOLS.md')
        if os.path.exists(tools_md_path):
            try:
                with open(tools_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取所有已配置的设备名称
                mikrotik_section = re.search(r'###\s*MikroTik 设备.*?\n(.*?)(?=\n###|\Z)', content, re.DOTALL | re.IGNORECASE)
                if mikrotik_section:
                    section_text = mikrotik_section.group(1)
                    device_names = re.findall(r'\*\*([^*]+)\*\*', section_text)
                    
                    # 检查消息中是否包含已配置的设备名称
                    for name in device_names:
                        if name.strip().lower() in message or name.strip() in original_message:
                            device = name.strip().lower()
                            break
            except:
                pass
        
        # 扫描命令独立处理，不依赖设备配置
        if '扫描' in message or 'scan' in message:
            return format_scan(None, None)
        
        # 如果没有匹配到设备名称，使用默认值
        if not device:
            device = 'default'  # 使用默认设备
        
        # 检查命令类型
        if '状态' in message or 'status' in message:
            return execute_command(device, 'status')
        elif '防火墙' in message or 'firewall' in message:
            return execute_command(device, 'firewall')
        elif '接口' in message or 'interface' in message:
            return execute_command(device, 'interfaces')
        elif '客户端' in message or '无线' in message or 'wifi' in message or 'wi-fi' in message:
            return execute_command(device, 'clients')
        elif '执行' in message or '命令' in message:
            # 提取命令路径
            if '/ip/' in message or '/system/' in message:
                cmd_start = message.find('/')
                command = message[cmd_start:].split()[0]
                return execute_command(device, command)
    
    return None  # 不是本 skill 处理的命令


if __name__ == '__main__':
    # 测试
    if len(sys.argv) > 1:
        device = sys.argv[1] if len(sys.argv) > 1 else 'office'
        command = sys.argv[2] if len(sys.argv) > 2 else 'status'
        print(execute_command(device, command))
    else:
        print("用法：python handler.py [设备] [命令]")
        print("示例：python handler.py office status")
