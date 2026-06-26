"""
MikroTik RouterOS API - Common Command Wrappers
Author: Xiage
Translator/Maintainer: drodecker
"""

class SystemCommands:
    """System related commands"""
    def __init__(self, api):
        self.api = api

    def get_resource(self):
        """Get system resource information"""
        return self.api.run_command('/system/resource/print')

    def get_identity(self):
        """Get device identity"""
        return self.api.run_command('/system/identity/print')

    def get_version(self):
        """Get system version"""
        return self.api.run_command('/system/package/update/print')

    def get_health(self):
        """Get health status (temperature, voltage, etc.)"""
        return self.api.run_command('/system/health/print')

    def get_uptime(self):
        """Get system uptime"""
        res = self.get_resource()
        return res[0].get('uptime') if res else 'N/A'

    def get_users(self):
        """Get system user list"""
        return self.api.run_command('/user/print')

    def get_services(self):
        """Get system services (API, SSH, WWW, etc.)"""
        return self.api.run_command('/ip/service/print')

    def get_scheduler(self):
        """Get scheduled tasks list"""
        return self.api.run_command('/system/scheduler/print')

    def get_scripts(self):
        """Get scripts list"""
        return self.api.run_command('/system/script/print')

    def get_logging(self):
        """Get logging configuration"""
        return self.api.run_command('/system/logging/print')

    def get_watchdog(self):
        """Get watchdog configuration"""
        return self.api.run_command('/system/watchdog/print')

    def get_logs(self, count=20):
        """
        Get recent logs
        Args:
            count: Number of logs
        """
        return self.api.run_command('/log/print')[-count:]

    def reboot(self):
        """Reboot device"""
        return self.api.run_command('/system/reboot')

    def shutdown(self):
        """Shutdown device"""
        return self.api.run_command('/system/shutdown')


class FirewallCommands:
    """Firewall related commands"""
    def __init__(self, api):
        self.api = api

    def get_filter_rules(self):
        """Get filter rules"""
        return self.api.run_command('/ip/firewall/filter/print')

    def get_nat_rules(self):
        """Get NAT rules"""
        return self.api.run_command('/ip/firewall/nat/print')

    def get_mangle_rules(self):
        """Get Mangle rules"""
        return self.api.run_command('/ip/firewall/mangle/print')

    def get_address_lists(self):
        """Get address lists"""
        return self.api.run_command('/ip/firewall/address-list/print')

    def get_active_connections(self):
        """Get active connections"""
        return self.api.run_command('/ip/firewall/connection/print')

    def get_connection_stats(self):
        """Get connection statistics"""
        return self.api.run_command('/ip/firewall/connection/tracking/print')

    def get_raw_rules(self):
        """Get Raw rules (pre-processing firewall)"""
        return self.api.run_command('/ip/firewall/raw/print')

    def get_tracking_status(self):
        """Get connection tracking status"""
        return self.api.run_command('/ip/firewall/connection/tracking/print')


class NetworkCommands:
    """Network related commands"""
    def __init__(self, api):
        self.api = api

    def get_interfaces(self):
        """Get network interface list"""
        return self.api.run_command('/interface/print')

    def get_ip_addresses(self):
        """Get IP address configuration"""
        return self.api.run_command('/ip/address/print')

    def get_routes(self):
        """Get routing table"""
        return self.api.run_command('/ip/route/print')

    def get_dns(self):
        """Get DNS configuration"""
        return self.api.run_command('/ip/dns/print')

    def get_dhcp_leases(self):
        """Get DHCP leases"""
        return self.api.run_command('/ip/dhcp-server/lease/print')

    def get_dhcp_servers(self):
        """Get DHCP server configuration"""
        return self.api.run_command('/ip/dhcp-server/print')

    def get_arp(self):
        """Get ARP table"""
        return self.api.run_command('/ip/arp/print')

    def get_neighbors(self):
        """Get neighbor discovery"""
        return self.api.run_command('/ip/neighbor/print')

    def get_wireguard_peers(self):
        """Get WireGuard peers status"""
        return self.api.run_command('/interface/wireguard/peers/print')

    def get_vlan_interfaces(self):
        """Get VLAN interface list"""
        return self.api.run_command('/interface/vlan/print')

    def get_bridge_ports(self):
        """Get bridge ports list"""
        return self.api.run_command('/interface/bridge/port/print')

    def get_traffic_stats(self, interface=''):
        """
        Get interface traffic statistics
        Args:
            interface: Interface name, empty for all
        """
        args = [f'=interface={interface}'] if interface else []
        return self.api.run_command('/interface/monitor-traffic', args + ['=once='])

    def get_interface_stats(self, interface=''):
        """
        Get detailed interface statistics (bytes, packets)
        Args:
            interface: Interface name, empty for all
        """
        res = self.api.run_command('/interface/print', ['=stats='])
        if interface:
            # Filter specified interface
            return [i for i in res if i.get('name') == interface]
        return res

    def get_wireguard_interfaces(self):
        """Get WireGuard interface status"""
        return self.api.run_command('/interface/wireguard/print')

    def get_bridge_config(self):
        """Get bridge configuration"""
        return self.api.run_command('/interface/bridge/print')

    def get_vlan_config(self):
        """Get VLAN configuration"""
        return self.api.run_command('/interface/vlan/print')

    def get_pppoe_clients(self):
        """Get PPPoE client configuration"""
        return self.api.run_command('/interface/pppoe-client/print')

    def get_bonding(self):
        """Get bonding configuration"""
        return self.api.run_command('/interface/bonding/print')

    def get_queues(self):
        """Get simple queue (bandwidth limit) configuration"""
        return self.api.run_command('/queue/simple/print')

    def get_queue_tree(self):
        """Get queue tree configuration"""
        return self.api.run_command('/queue/tree/print')

    def get_queue_types(self):
        """Get queue type definitions"""
        return self.api.run_command('/queue/type/print')


class RoutingCommands:
    """Routing related commands"""
    def __init__(self, api):
        self.api = api

    def get_routes(self):
        """Get routing table"""
        return self.api.run_command('/ip/route/print')

    def get_static_routes(self):
        """Get static routes"""
        return self.api.run_command('/ip/route/print', ['?static=yes'])

    def get_dynamic_routes(self):
        """Get dynamic routes"""
        return self.api.run_command('/ip/route/print', ['?dynamic=yes'])

    def get_ospf_instance(self):
        """Get OSPF instance configuration"""
        return self.api.run_command('/routing/ospf/instance/print')

    def get_ospf_area(self):
        """Get OSPF area configuration"""
        return self.api.run_command('/routing/ospf/area/print')

    def get_ospf_interface(self):
        """Get OSPF interface configuration"""
        return self.api.run_command('/routing/ospf/interface/print')

    def get_ospf_neighbor(self):
        """Get OSPF neighbor status"""
        return self.api.run_command('/routing/ospf/neighbor/print')

    def get_ospf_lsa(self):
        """Get OSPF LSA database"""
        return self.api.run_command('/routing/ospf/lsa/print')

    def get_bgp_instance(self):
        """Get BGP instance configuration"""
        return self.api.run_command('/routing/bgp/instance/print')

    def get_bgp_peer(self):
        """Get BGP peer configuration"""
        return self.api.run_command('/routing/bgp/peer/print')

    def get_bgp_session(self):
        """Get BGP session status"""
        return self.api.run_command('/routing/bgp/session/print')

    def get_bgp_route(self):
        """Get BGP routes"""
        return self.api.run_command('/routing/bgp/route/print')

    def get_bgp_advertisements(self):
        """Get BGP advertisements"""
        return self.api.run_command('/routing/bgp/adverts/print')

    def get_mpls_interface(self):
        """Get MPLS interface configuration"""
        return self.api.run_command('/mpls/interface/print')

    def get_mpls_ldp_neighbor(self):
        """Get MPLS LDP neighbor"""
        return self.api.run_command('/mpls/ldp/neighbor/print')

    def ping(self, host, count=4):
        """
        Execute Ping test
        Args:
            host: Target address
            count: Number of pings
        """
        return self.api.run_command('/tool/ping', [f'=address={host}', f'=count={count}'])

    def traceroute(self, host):
        """
        Execute Traceroute
        Args:
            host: Target address
        """
        return self.api.run_command('/tool/traceroute', [f'=address={host}'])

    def get_dns_cache(self):
        """Get DNS cache"""
        return self.api.run_command('/ip/dns/cache/print')

    def bandwidth_test(self, interface=''):
        """
        Bandwidth test (requires support on both ends)
        Args:
            interface: Specified interface
        """
        # Note: Bandwidth test is usually interactive, this is just a wrapper
        return self.api.run_command('/tool/bandwidth-test', [f'=interface={interface}'])

    def get_poe_status(self):
        """Get PoE status"""
        return self.api.run_command('/interface/ethernet/poe/print')

    def get_usb(self):
        """Get USB device list"""
        return self.api.run_command('/system/usb/print')

    def get_disk(self):
        """Get storage device information"""
        return self.api.run_command('/disk/print')


class UserPPPCommands:
    """User and PPP related commands"""
    def __init__(self, api):
        self.api = api

    def get_ppp_users(self):
        """Get PPP users (PPPoE/PPTP/L2TP)"""
        return self.api.run_command('/ppp/secret/print')

    def get_active_ppp(self):
        """Get active PPP connections"""
        return self.api.run_command('/ppp/active/print')

    def get_hotspot_users(self):
        """Get Hotspot users"""
        return self.api.run_command('/ip/hotspot/user/print')

    def get_active_hotspot(self):
        """Get active Hotspot sessions"""
        return self.api.run_command('/ip/hotspot/active/print')

    def get_user_groups(self):
        """Get user groups"""
        return self.api.run_command('/user/group/print')


class QuickCommands:
    """Quick commands collection"""
    def __init__(self, api):
        self.api = api
        self.system = SystemCommands(api)
        self.firewall = FirewallCommands(api)
        self.network = NetworkCommands(api)
        self.routing = RoutingCommands(api)
        self.user_ppp = UserPPPCommands(api)

    def get_full_status(self):
        """Get full device status"""
        return {
            'resource': self.system.get_resource(),
            'identity': self.system.get_identity(),
            'interfaces': self.network.get_interfaces(),
            'addresses': self.network.get_ip_addresses()
        }

    def print_status(self):
        """Print device status (human readable)"""
        res = self.system.get_resource()
        identity = self.system.get_identity()
        
        if not res or not identity:
            print("❌ Failed to get device status")
            return
            
        res = res[0]
        identity = identity[0]
        
        print("📡 MikroTik RouterOS Device Status")
        print(f"  Device Name: {identity.get('name', 'N/A')}")
        print(f"  Version: {res.get('version', 'N/A')}")
        print(f"  Uptime: {res.get('uptime', 'N/A')}")
        print(f"  CPU Load: {res.get('cpu-load', 'N/A')}%")
        print(f"  Memory: {int(res.get('free-memory', 0))/1024/1024:.1f}MB / "
              f"{int(res.get('total-memory', 0))/1024/1024:.1f}MB")
        print(f"  Storage: {int(res.get('free-hdd-space', 0))/1024/1024:.1f}MB / "
              f"{int(res.get('total-hdd-space', 0))/1024/1024:.1f}MB")
        
        # Interface status
        print("\n🔌 Network Interfaces:")
        interfaces = self.network.get_interfaces()
        for i in interfaces[:10]:  # Show first 10
            name = i.get('name', 'N/A')
            running = i.get('running') == 'true'
            status = "✅" if running else "❌"
            print(f"  {status} {name} ({i.get('type', 'N/A')})")
            
        # IP Addresses
        print("\n🌐 IP Addresses:")
        addresses = self.network.get_ip_addresses()
        for a in addresses:
            print(f"  - {a.get('address', 'N/A')} ({a.get('interface', 'N/A')})")
            
        # Default Route
        print("\n🛤️ Default Route:")
        routes = self.network.get_routes()
        for route in routes:
            if route.get('dst-address') == '0.0.0.0/0':
                print(f"  - Default Gateway: {route.get('gateway', 'N/A')}")
