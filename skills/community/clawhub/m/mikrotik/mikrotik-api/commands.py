#!/usr/bin/env python3
"""
MikroTik RouterOS API - 常用命令封装
"""

from typing import List, Dict, Optional

# 支持直接运行和包导入两种模式
try:
    from .client import MikroTikAPI
except ImportError:
    from client import MikroTikAPI


class SystemCommands:
    """系统相关命令"""
    
    def __init__(self, api: MikroTikAPI):
        self.api = api
    
    def get_resource(self) -> Dict:
        """获取系统资源信息"""
        results = self.api.run_command('/system/resource/print')
        return results[0] if results else {}
    
    def get_identity(self) -> Dict:
        """获取设备标识"""
        results = self.api.run_command('/system/identity/print')
        return results[0] if results else {}
    
    def get_version(self) -> Dict:
        """获取系统版本"""
        results = self.api.run_command('/system/routerboard/print')
        return results[0] if results else {}
    
    def get_health(self) -> Dict:
        """获取健康状态（温度、电压等）"""
        results = self.api.run_command('/system/health/print')
        return results[0] if results else {}
    
    def get_uptime(self) -> str:
        """获取运行时间"""
        resource = self.get_resource()
        return resource.get('uptime', 'N/A')
    
    def get_users(self) -> List[Dict]:
        """获取系统用户列表"""
        return self.api.run_command('/user/print')
    
    def get_services(self) -> List[Dict]:
        """获取系统服务（API、SSH、WWW 等）"""
        return self.api.run_command('/ip/service/print')
    
    def get_scheduler(self) -> List[Dict]:
        """获取定时任务列表"""
        return self.api.run_command('/system/scheduler/print')
    
    def get_scripts(self) -> List[Dict]:
        """获取脚本列表"""
        return self.api.run_command('/system/script/print')
    
    def get_logging(self) -> List[Dict]:
        """获取日志配置"""
        return self.api.run_command('/system/logging/print')
    
    def get_scheduler(self) -> List[Dict]:
        """获取定时任务列表"""
        return self.api.run_command('/system/scheduler/print')
    
    def get_watchdog(self) -> Dict:
        """获取看门狗配置"""
        results = self.api.run_command('/system/watchdog/print')
        return results[0] if results else {}
    
    def get_recent_logs(self, count: int = 20) -> List[Dict]:
        """
        获取最近日志
        
        Args:
            count: 日志条数
        """
        return self.api.run_command('/log/print', [f'=.count={count}'])
    
    def reboot(self):
        """重启设备"""
        self.api.run_command('/system/reboot')
    
    def shutdown(self):
        """关闭设备"""
        self.api.run_command('/system/shutdown')


class FirewallCommands:
    """防火墙相关命令"""
    
    def __init__(self, api: MikroTikAPI):
        self.api = api
    
    def get_filter_rules(self) -> List[Dict]:
        """获取过滤规则"""
        return self.api.run_command('/ip/firewall/filter/print')
    
    def get_nat_rules(self) -> List[Dict]:
        """获取 NAT 规则"""
        return self.api.run_command('/ip/firewall/nat/print')
    
    def get_mangle_rules(self) -> List[Dict]:
        """获取 Mangle 规则"""
        return self.api.run_command('/ip/firewall/mangle/print')
    
    def get_address_lists(self) -> List[Dict]:
        """获取地址列表"""
        return self.api.run_command('/ip/firewall/address-list/print')
    
    def get_active_connections(self, count: int = 100) -> List[Dict]:
        """获取活动连接"""
        return self.api.run_command('/ip/firewall/active/print', 
                                    [f'=.proplist=src-address,dst-address,protocol,src-port,dst-port'])
    
    def get_connection_stats(self) -> Dict:
        """获取连接统计"""
        results = self.api.run_command('/ip/firewall/connection/print', ['=count-only='])
        return {'total': len(results)} if results else {}
    
    def get_raw_rules(self) -> List[Dict]:
        """获取 Raw 规则（预处理防火墙）"""
        return self.api.run_command('/ip/firewall/raw/print')
    
    def get_connection_tracking(self) -> Dict:
        """获取连接跟踪状态"""
        results = self.api.run_command('/ip/firewall/connection/print', ['=count-only='])
        return {'active_connections': len(results)} if results else {}


class NetworkCommands:
    """网络相关命令"""
    
    def __init__(self, api: MikroTikAPI):
        self.api = api
    
    def get_interfaces(self) -> List[Dict]:
        """获取网络接口列表"""
        return self.api.run_command('/interface/print')
    
    def get_ip_addresses(self) -> List[Dict]:
        """获取 IP 地址配置"""
        return self.api.run_command('/ip/address/print')
    
    def get_routes(self) -> List[Dict]:
        """获取路由表"""
        return self.api.run_command('/ip/route/print')
    
    def get_dns(self) -> List[Dict]:
        """获取 DNS 配置"""
        return self.api.run_command('/ip/dns/print')
    
    def get_dhcp_leases(self) -> List[Dict]:
        """获取 DHCP 租约"""
        return self.api.run_command('/ip/dhcp-server/lease/print')
    
    def get_dhcp_servers(self) -> List[Dict]:
        """获取 DHCP 服务器配置"""
        return self.api.run_command('/ip/dhcp-server/print')
    
    def get_arp(self) -> List[Dict]:
        """获取 ARP 表"""
        return self.api.run_command('/ip/arp/print')
    
    def get_neighbors(self) -> List[Dict]:
        """获取邻居发现"""
        return self.api.run_command('/ip/neighbor/print')
    
    def get_wireguard_peers(self) -> List[Dict]:
        """获取 WireGuard 对等体状态"""
        return self.api.run_command('/interface/wireguard/peer/print')
    
    def get_vlan_interfaces(self) -> List[Dict]:
        """获取 VLAN 接口列表"""
        return self.api.run_command('/interface/vlan/print')
    
    def get_bridge_ports(self) -> List[Dict]:
        """获取桥接端口列表"""
        return self.api.run_command('/interface/bridge/port/print')
    
    def get_traffic_stats(self, interface: str = '') -> List[Dict]:
        """
        获取接口流量统计
        
        Args:
            interface: 指定接口名，空则返回所有接口
        """
        if interface:
            return self.api.run_command('/interface/print', [f'=.where=name={interface}'])
        return self.api.run_command('/interface/print')
    
    def get_interface_stats(self, interface: str = '') -> List[Dict]:
        """
        获取接口详细统计（字节数、包数）
        
        Args:
            interface: 指定接口名，空则返回所有接口
        """
        # 获取所有接口统计，然后在 Python 层面过滤
        all_stats = self.api.run_command('/interface/print')
        
        if interface:
            # 过滤指定接口
            return [iface for iface in all_stats if iface.get('name') == interface]
        return all_stats
    
    def get_wireguard_status(self) -> List[Dict]:
        """获取 WireGuard 接口状态"""
        return self.api.run_command('/interface/wireguard/print')
    
    def get_bridge(self) -> List[Dict]:
        """获取桥接配置"""
        return self.api.run_command('/interface/bridge/print')
    
    def get_vlan(self) -> List[Dict]:
        """获取 VLAN 配置"""
        return self.api.run_command('/interface/vlan/print')
    
    def get_pppoe(self) -> List[Dict]:
        """获取 PPPoE 客户端配置"""
        return self.api.run_command('/interface/pppoe-client/print')
    
    def get_bonding(self) -> List[Dict]:
        """获取链路聚合（Bonding）配置"""
        return self.api.run_command('/interface/bonding/print')
    
    def get_simple_queues(self) -> List[Dict]:
        """获取简单队列（带宽限制）配置"""
        return self.api.run_command('/queue/simple/print')
    
    def get_queue_tree(self) -> List[Dict]:
        """获取队列树配置"""
        return self.api.run_command('/queue/tree/print')
    
    def get_queue_types(self) -> List[Dict]:
        """获取队列类型定义"""
        return self.api.run_command('/queue/type/print')


class RoutingCommands:
    """路由相关命令"""
    
    def __init__(self, api: MikroTikAPI):
        self.api = api
    
    def get_routes(self) -> List[Dict]:
        """获取路由表"""
        return self.api.run_command('/ip/route/print')
    
    def get_static_routes(self) -> List[Dict]:
        """获取静态路由"""
        return self.api.run_command('/ip/route/print', ['=.where=dynamic=false'])
    
    def get_dynamic_routes(self) -> List[Dict]:
        """获取动态路由"""
        return self.api.run_command('/ip/route/print', ['=.where=dynamic=true'])
    
    def get_ospf_instances(self) -> List[Dict]:
        """获取 OSPF 实例配置"""
        return self.api.run_command('/routing/ospf/instance/print')
    
    def get_ospf_areas(self) -> List[Dict]:
        """获取 OSPF 区域配置"""
        return self.api.run_command('/routing/ospf/area/print')
    
    def get_ospf_interfaces(self) -> List[Dict]:
        """获取 OSPF 接口配置"""
        return self.api.run_command('/routing/ospf/interface/print')
    
    def get_ospf_neighbors(self) -> List[Dict]:
        """获取 OSPF 邻居状态"""
        return self.api.run_command('/routing/ospf/neighbor/print')
    
    def get_ospf_lsdb(self) -> List[Dict]:
        """获取 OSPF 链路状态数据库"""
        return self.api.run_command('/routing/ospf/lsdb/print')
    
    def get_bgp_instances(self) -> List[Dict]:
        """获取 BGP 实例配置"""
        return self.api.run_command('/routing/bgp/instance/print')
    
    def get_bgp_peers(self) -> List[Dict]:
        """获取 BGP 对等体配置"""
        return self.api.run_command('/routing/bgp/peer/print')
    
    def get_bgp_sessions(self) -> List[Dict]:
        """获取 BGP 会话状态"""
        return self.api.run_command('/routing/bgp/session/print')
    
    def get_bgp_routes(self) -> List[Dict]:
        """获取 BGP 路由"""
        return self.api.run_command('/routing/bgp/advertised-route/print')
    
    def get_bgp_networks(self) -> List[Dict]:
        """获取 BGP 网络宣告"""
        return self.api.run_command('/routing/bgp/network/print')
    
    def get_mpls_interfaces(self) -> List[Dict]:
        """获取 MPLS 接口配置"""
        return self.api.run_command('/mpls/interface/print')
    
    def get_mpls_ldp_neighbors(self) -> List[Dict]:
        """获取 MPLS LDP 邻居"""
        return self.api.run_command('/mpls/ldp/neighbor/print')
    
    def get_ping(self, host: str, count: int = 5) -> List[Dict]:
        """
        执行 Ping 测试
        
        Args:
            host: 目标地址
            count: Ping 次数
        """
        return self.api.run_command('/ping', [f'=address={host}', f'=count={count}'])
    
    def get_traceroute(self, host: str) -> List[Dict]:
        """
        执行 Traceroute
        
        Args:
            host: 目标地址
        """
        return self.api.run_command('/tool/traceroute', [f'=address={host}'])
    
    def get_dns_cache(self) -> List[Dict]:
        """获取 DNS 缓存"""
        return self.api.run_command('/ip/dns/cache/print')
    
    def get_bandwidth_test(self, interface: str = '') -> List[Dict]:
        """
        带宽测试（需要两端支持）
        
        Args:
            interface: 指定接口
        """
        if interface:
            return self.api.run_command('/tool/bandwidth-test', [f'=interface={interface}'])
        return self.api.run_command('/tool/bandwidth-server/print')
    
    def get_poe(self) -> List[Dict]:
        """获取 PoE 状态"""
        return self.api.run_command('/interface/ethernet/poe/print')
    
    def get_usb(self) -> List[Dict]:
        """获取 USB 设备列表"""
        return self.api.run_command('/system/usb/print')
    
    def get_storage(self) -> List[Dict]:
        """获取存储设备信息"""
        return self.api.run_command('/disk/print')


class UserCommands:
    """用户和 PPP 相关命令"""
    
    def __init__(self, api: MikroTikAPI):
        self.api = api
    
    def get_ppp_users(self) -> List[Dict]:
        """获取 PPP 用户（PPPoE/PPTP/L2TP）"""
        return self.api.run_command('/ppp/secret/print')
    
    def get_ppp_active(self) -> List[Dict]:
        """获取活跃 PPP 连接"""
        return self.api.run_command('/ppp/active/print')
    
    def get_hotspot_users(self) -> List[Dict]:
        """获取 Hotspot 用户"""
        return self.api.run_command('/ip/hotspot/user/print')
    
    def get_hotspot_active(self) -> List[Dict]:
        """获取活跃 Hotspot 会话"""
        return self.api.run_command('/ip/hotspot/active/print')
    
    def get_user_groups(self) -> List[Dict]:
        """获取用户组"""
        return self.api.run_command('/user/group/print')


class QuickCommands:
    """快捷命令集合"""
    
    def __init__(self, api: MikroTikAPI):
        self.api = api
        self.system = SystemCommands(api)
        self.firewall = FirewallCommands(api)
        self.network = NetworkCommands(api)
        self.user = UserCommands(api)
        self.routing = RoutingCommands(api)
    
    def status(self) -> Dict:
        """获取设备完整状态"""
        return {
            'identity': self.system.get_identity(),
            'resource': self.system.get_resource(),
            'interfaces': self.network.get_interfaces(),
            'addresses': self.network.get_ip_addresses(),
            'routes': self.network.get_routes(),
        }
    
    def print_status(self):
        """打印设备状态（人类可读）"""
        identity = self.system.get_identity()
        resource = self.system.get_resource()
        
        print("=" * 60)
        print("📡 MikroTik RouterOS 设备状态")
        print("=" * 60)
        print(f"  设备名：{identity.get('name', 'N/A')}")
        print(f"  版本：{resource.get('version', 'N/A')}")
        print(f"  运行时间：{resource.get('uptime', 'N/A')}")
        print(f"  CPU: {resource.get('cpu', 'N/A')} @ {resource.get('cpu-frequency', 'N/A')}MHz")
        print(f"  CPU 负载：{resource.get('cpu-load', 'N/A')}%")
        print(f"  内存：{int(resource.get('free-memory', 0))/1024/1024:.1f}MB / "
              f"{int(resource.get('total-memory', 1))/1024/1024:.1f}MB")
        print(f"  存储：{int(resource.get('free-hdd-space', 0))/1024/1024:.1f}MB / "
              f"{int(resource.get('total-hdd-space', 1))/1024/1024:.1f}MB")
        print("=" * 60)
        
        # 接口状态
        print("\n🔌 网络接口:")
        interfaces = self.network.get_interfaces()
        for iface in interfaces:
            name = iface.get('name', 'unknown')
            running = iface.get('running', 'false') == 'true'
            status = "✅" if running else "❌"
            print(f"  {status} {name}")
        
        # IP 地址
        print("\n🌐 IP 地址:")
        addresses = self.network.get_ip_addresses()
        for addr in addresses:
            print(f"  - {addr.get('address', 'N/A')} on {addr.get('interface', 'N/A')}")
        
        # 默认路由
        print("\n🛤️ 默认路由:")
        routes = self.network.get_routes()
        for route in routes:
            if route.get('dst-address') == '0.0.0.0/0':
                print(f"  - 默认网关：{route.get('gateway', 'N/A')}")
        
        print("=" * 60)
