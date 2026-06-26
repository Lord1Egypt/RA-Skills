#!/usr/bin/env python3
"""
Omada SDN Controller Query Tool

Read-only queries against TP-Link Omada controllers via the Northbound API.

Environment variables required:
  OMADA_URL          - Base URL of the controller (e.g., https://omada.local:8043)
  OMADA_CLIENT_ID    - API client ID
  OMADA_CLIENT_SECRET - API client secret

Optional:
  OMADA_OMADAC_ID    - Controller ID (auto-detected if not set)
  OMADA_SITE         - Site name (defaults to first site)
  OMADA_VERIFY_SSL   - Set to "false" to disable SSL verification

Usage:
  python omada_query.py <command> [args]

Commands:
  sites                    List all sites
  devices                  List all devices (APs, switches, gateways)
  clients                  List connected clients
  vlans                    List VLANs/LAN networks
  dhcp-reservations        List DHCP reservations
  port-forwards            List port forwarding rules
  switch-ports <mac>       List ports for a specific switch
  wan-ports                List gateway WAN ports
  wan-status               Show WAN public IPs, DNS, latency, and health
  router-ports             Show all physical router ports and modes
  router-summary           Quick combined router/WAN/LAN summary
  summary                  Quick network health summary
"""

import os
import sys
import json
import urllib3
from typing import Optional

# Suppress SSL warnings if verification disabled
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


class OmadaClient:
    def __init__(self):
        self.base_url = os.environ.get("OMADA_URL", "").rstrip("/")
        self.client_id = os.environ.get("OMADA_CLIENT_ID", "")
        self.client_secret = os.environ.get("OMADA_CLIENT_SECRET", "")
        self.omadac_id = os.environ.get("OMADA_OMADAC_ID", "")
        self.site_name = os.environ.get("OMADA_SITE", "")
        self.verify_ssl = os.environ.get("OMADA_VERIFY_SSL", "true").lower() != "false"
        
        if not all([self.base_url, self.client_id, self.client_secret]):
            print("Error: Missing required environment variables:")
            print("  OMADA_URL, OMADA_CLIENT_ID, OMADA_CLIENT_SECRET")
            sys.exit(1)
        
        self.token: Optional[str] = None
        self.site_id: Optional[str] = None
    
    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop("headers", {})
        headers["Content-Type"] = "application/json"
        if self.token:
            headers["Authorization"] = f"AccessToken={self.token}"
        
        resp = requests.request(method, url, headers=headers, verify=self.verify_ssl, **kwargs)
        resp.raise_for_status()
        return resp.json()
    
    def get_controller_id(self):
        """Get the controller's omadacId from /api/info."""
        if self.omadac_id:
            return  # Already set via env var
        resp = requests.get(f"{self.base_url}/api/info", verify=self.verify_ssl)
        resp.raise_for_status()
        data = resp.json()
        self.omadac_id = data["result"]["omadacId"]
    
    def authenticate(self):
        """Get OAuth2 access token using client credentials."""
        # Build the request body as a proper dict
        body = {
            "omadacId": self.omadac_id,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        resp = requests.post(
            f"{self.base_url}/openapi/authorize/token",
            params={"grant_type": "client_credentials"},
            json=body,
            headers={"Content-Type": "application/json"},
            verify=self.verify_ssl
        )
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("errorCode") != 0:
            raise ValueError(f"Auth failed: {data.get('msg', 'Unknown error')}")
        
        self.token = data["result"]["accessToken"]
    
    def get_site_id(self):
        """Get site ID (by name or first available)."""
        data = self._request("GET", f"/openapi/v1/{self.omadac_id}/sites", params={"page": 1, "pageSize": 100})
        sites = data["result"]["data"]
        if not sites:
            raise ValueError("No sites found")
        
        if self.site_name:
            for site in sites:
                if site["name"].lower() == self.site_name.lower():
                    self.site_id = site["siteId"]
                    return
            print(f"Warning: Site '{self.site_name}' not found, using first site")
        
        self.site_id = sites[0]["siteId"]
    
    def setup(self):
        """Authenticate and get controller/site IDs."""
        self.get_controller_id()
        self.authenticate()
        self.get_site_id()
    
    def _api(self, endpoint: str, params: dict = None) -> dict:
        """Make API call to site-scoped endpoint."""
        default_params = {"page": 1, "pageSize": 200}
        if params:
            default_params.update(params)
        return self._request("GET", f"/openapi/v1/{self.omadac_id}/sites/{self.site_id}{endpoint}", params=default_params)
    
    # Query methods
    def list_sites(self) -> list:
        data = self._request("GET", f"/openapi/v1/{self.omadac_id}/sites")
        return data["result"]["data"]
    
    def list_devices(self) -> list:
        data = self._api("/devices")
        return data["result"]["data"]
    
    def list_clients(self) -> list:
        data = self._api("/clients")
        return data["result"]["data"]
    
    def list_vlans(self) -> list:
        data = self._api("/lan-networks")
        return data["result"]["data"]
    
    def list_dhcp_reservations(self) -> list:
        """Get DHCP reservations across all networks."""
        # Note: Reservations may be embedded in network DHCP settings
        # or available via a separate endpoint depending on controller version
        networks = self.list_vlans()
        reservations = []
        for net in networks:
            dhcp = net.get("dhcpSettingsVO", {})
            if dhcp.get("enable"):
                reservations.append({
                    "network_name": net.get("name", "Unknown"),
                    "network_id": net.get("id"),
                    "vlan": net.get("vlan"),
                    "dhcp_start": dhcp.get("ipaddrStart"),
                    "dhcp_end": dhcp.get("ipaddrEnd"),
                    "dns": dhcp.get("priDns"),
                    "lease_time": dhcp.get("leasetime")
                })
        return reservations
    
    def list_port_forwards(self) -> list:
        data = self._api("/nat/port-forwardings")
        return data["result"]["data"]
    
    def list_switch_ports(self, switch_mac: str) -> list:
        data = self._api(f"/switches/{switch_mac}/ports")
        return data["result"]["data"]
    
    def list_gateways(self) -> list:
        data = self._api("/devices")
        return [d for d in data["result"]["data"] if d.get("type") == "gateway"]
    
    def list_wan_ports(self) -> list:
        gateways = self.list_gateways()
        ports = []
        for gw in gateways:
            try:
                data = self._api(f"/gateways/{gw['mac']}/ports", params={})
                for port in data["result"]:
                    port["gateway_name"] = gw.get("name", gw["mac"])
                    ports.append(port)
            except Exception:
                pass
        return ports
    
    def get_gateway_info(self) -> dict:
        gateways = self.list_gateways()
        if not gateways:
            raise ValueError("No gateway found")
        gw = gateways[0]
        data = self._api(f"/gateways/{gw['mac']}", params={})
        return data["result"]
    
    def get_wan_status(self) -> list:
        gateways = self.list_gateways()
        if not gateways:
            return []
        gw = gateways[0]
        data = self._api(f"/gateways/{gw['mac']}/wan-status", params={})
        return data["result"]
    
    def get_router_ports(self) -> list:
        gateways = self.list_gateways()
        if not gateways:
            return []
        gw = gateways[0]
        data = self._api(f"/gateways/{gw['mac']}/ports", params={})
        return data["result"]
    
    def get_lan_status(self) -> list:
        gateways = self.list_gateways()
        if not gateways:
            return []
        gw = gateways[0]
        data = self._api(f"/gateways/{gw['mac']}/lan-status", params={})
        return data["result"]
    
    def get_internet_ports_config(self) -> dict:
        data = self._api("/internet/ports-config", params={})
        return data["result"]

def print_json(data):
    print(json.dumps(data, indent=2))


def print_table(data: list, columns: list):
    """Print data as a simple table."""
    if not data:
        print("No data found.")
        return
    
    # Calculate column widths
    widths = {col: len(col) for col in columns}
    for row in data:
        for col in columns:
            val = str(row.get(col, ""))
            widths[col] = max(widths[col], len(val))
    
    # Print header
    header = " | ".join(col.upper().ljust(widths[col]) for col in columns)
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in data:
        line = " | ".join(str(row.get(col, "")).ljust(widths[col]) for col in columns)
        print(line)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    client = OmadaClient()
    client.setup()
    
    if command == "sites":
        sites = client.list_sites()
        print_table(sites, ["name", "siteId", "region"])
    
    elif command == "devices":
        devices = client.list_devices()
        print_table(devices, ["name", "type", "mac", "ip", "status"])
    
    elif command == "clients":
        clients = client.list_clients()
        print_table(clients, ["name", "ip", "mac", "networkName", "connectType"])
    
    elif command == "vlans":
        vlans = client.list_vlans()
        print_table(vlans, ["name", "vlan", "gatewaySubnet"])
    
    elif command == "dhcp-reservations":
        reservations = client.list_dhcp_reservations()
        print_table(reservations, ["network_name", "mac", "ip", "description"])
    
    elif command == "port-forwards":
        rules = client.list_port_forwards()
        print_table(rules, ["name", "externalPort", "forwardIp", "forwardPort", "status"])
    
    elif command == "switch-ports":
        if len(sys.argv) < 3:
            print("Usage: omada_query.py switch-ports <switch_mac>")
            sys.exit(1)
        switch_mac = sys.argv[2]
        ports = client.list_switch_ports(switch_mac)
        print_table(ports, ["port", "name", "linkStatus", "linkSpeed", "poe"])
    
    elif command == "wan-ports":
        ports = client.list_wan_ports()
        print_table(ports, ["gateway_name", "port", "name", "type", "mode"])
    
    elif command == "wan-status":
        wans = client.get_wan_status()
        print_table(wans, ["name", "ip", "proto", "latency", "loss", "status"])
    
    elif command == "router-ports":
        ports = client.get_router_ports()
        print_table(ports, ["port", "name", "type", "mode", "physicalType"])
    
    elif command == "router-summary":
        print("=== Router Summary ===\n")
        gw = client.get_gateway_info()
        print(f"Gateway: {gw.get('showModel', 'Unknown')} @ {gw.get('ip', 'N/A')}")
        print(f"Firmware: {gw.get('firmwareVersion', 'N/A')}")
        print(f"Uptime: {gw.get('uptime', 'N/A')}")
        print()
        
        print("WANs:")
        for wan in client.get_wan_status():
            print(f"  - {wan.get('name')}: {wan.get('ip')} ({wan.get('proto')}, latency {wan.get('latency')} ms, loss {wan.get('loss')}%)")
        print()
        
        print("Router Ports:")
        for port in client.get_router_ports():
            print(f"  - Port {port.get('port')}: {port.get('name')} (type={port.get('type')}, mode={port.get('mode')})")
        print()
        
        print("LAN Interfaces:")
        for lan in client.get_lan_status():
            print(f"  - VLAN {lan.get('vlan')}: {lan.get('lanName')} @ {lan.get('ip')} ({lan.get('clientNum')} clients)")
    
    elif command == "summary":
        print("=== Network Summary ===\n")
        
        devices = client.list_devices()
        # status: 0=pending, 1=connected, 10=heartbeat missed, 11=isolated
        online = sum(1 for d in devices if d.get("status") == 1)
        print(f"Devices: {online}/{len(devices)} online")
        for d in devices:
            status = "[+]" if d.get("status") == 1 else "[-]"
            print(f"  {status} {d.get('name', d['mac'])} ({d.get('type', 'unknown')})")
        
        print()
        clients = client.list_clients()
        print(f"Clients: {len(clients)} connected")
        
        # VLANs and port forwards may not be available on all controllers
        try:
            vlans = client.list_vlans()
            print(f"\nVLANs: {len(vlans)}")
            for v in vlans:
                print(f"  - {v.get('name', 'Unnamed')} (VLAN {v.get('vlan', 'N/A')})")
        except Exception:
            print("\nVLANs: (not available)")
        
        try:
            forwards = client.list_port_forwards()
            enabled = sum(1 for f in forwards if f.get("enable"))
            enabled = sum(1 for f in forwards if f.get("status") == True)
            print(f"\nPort Forwards: {enabled}/{len(forwards)} enabled")
        except Exception:
            print("\nPort Forwards: (not available)")
    
    elif command == "json":
        # Raw JSON output for any subcommand
        if len(sys.argv) < 3:
            print("Usage: omada_query.py json <subcommand>")
            sys.exit(1)
        subcmd = sys.argv[2].lower()
        if subcmd == "devices":
            print_json(client.list_devices())
        elif subcmd == "clients":
            print_json(client.list_clients())
        elif subcmd == "vlans":
            print_json(client.list_vlans())
        elif subcmd == "port-forwards":
            print_json(client.list_port_forwards())
        else:
            print(f"Unknown subcommand: {subcmd}")
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
