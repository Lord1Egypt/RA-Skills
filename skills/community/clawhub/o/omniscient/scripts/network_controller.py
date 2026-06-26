#!/usr/bin/env python3
"""
Network Controller - Windows network and WiFi management.

Capabilities:
  - Network adapters (list, enable, disable)
  - WiFi (scan, connect, disconnect, profiles, forget)
  - IP configuration (view)
  - DNS management (get, set, reset)
  - Network proxy (get, set, disable)
  - Connectivity test (ping)

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None
"""

import subprocess
import sys
import os
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== Safety ==========

def _require_confirmation(action_name):
    """Safety gate for destructive network operations."""
    confirmed = os.environ.get("SYSTEM_CONTROLLER_CONFIRM", "")
    if action_name not in confirmed.split(","):
        return (
            f"ERROR: {action_name} requires explicit confirmation. "
            f"Set environment variable SYSTEM_CONTROLLER_CONFIRM={action_name} "
            f"or SYSTEM_CONTROLLER_CONFIRM=all to proceed."
        )
    return None


def _validate_adapter_name(name):
    """Validate network adapter name - only allow alphanumeric, space, hyphen, parentheses."""
    if not name or not isinstance(name, str):
        return False
    if len(name) > 128:
        return False
    return bool(re.match(r'^[\w\s\-\(\)\.]+$', name))


# ========== Network Adapters ==========

def list_adapters():
    """List all network adapters with status and link speed."""
    script = r"""
Get-NetAdapter | Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress |
    ForEach-Object {
        [PSCustomObject]@{
            Name = $_.Name
            Description = $_.InterfaceDescription
            Status = $_.Status
            Speed = $_.LinkSpeed
            MAC = $_.MacAddress
        }
    } | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def enable_adapter(name):
    """Enable a network adapter by name."""
    if not _validate_adapter_name(name):
        return "ERROR: Invalid adapter name"
    escaped = name.replace("'", "''")
    script = f"""
try {{
    Enable-NetAdapter -Name '{escaped}' -Confirm:$false -ErrorAction Stop
    Write-Output "OK: Adapter '{escaped}' enabled"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def disable_adapter(name):
    """Disable a network adapter. Requires confirmation."""
    if not _validate_adapter_name(name):
        return "ERROR: Invalid adapter name"
    err = _require_confirmation("disable_network")
    if err:
        return err
    escaped = name.replace("'", "''")
    script = f"""
try {{
    $adapter = Get-NetAdapter -Name '{escaped}' -ErrorAction Stop
    if ($adapter.Status -eq 'Disabled') {{
        Write-Output "INFO: Adapter '{escaped}' is already disabled"
        return
    }}
    Disable-NetAdapter -Name '{escaped}' -Confirm:$false -ErrorAction Stop
    Write-Output "OK: Adapter '{escaped}' disabled"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def adapter_info(name):
    """Get detailed info for a specific network adapter."""
    if not _validate_adapter_name(name):
        return "ERROR: Invalid adapter name"
    escaped = name.replace("'", "''")
    script = f"""
try {{
    $adapter = Get-NetAdapter -Name '{escaped}' -ErrorAction Stop
    $ip = Get-NetIPConfiguration -InterfaceAlias '{escaped}' -ErrorAction SilentlyContinue
    [PSCustomObject]@{{
        Name = $adapter.Name
        Description = $adapter.InterfaceDescription
        Status = $adapter.Status
        LinkSpeed = $adapter.LinkSpeed
        MAC = $adapter.MacAddress
        MTU = $adapter.MtuSize
        IPv4 = if ($ip.IPv4Address) { $ip.IPv4Address.IPAddress -join ', ' } else {{ '' }}
        IPv6 = if ($ip.IPv6Address) { $ip.IPv6Address.IPAddress -join ', ' } else {{ '' }}
        DNS = if ($ip.DNSServer) { $ip.DNSServer.ServerAddresses -join ', ' } else {{ '' }}
    }} | ConvertTo-Json
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== WiFi ==========

def list_wifi():
    """Scan and list available WiFi networks with signal strength."""
    script = r"""
try {
    $result = netsh wlan show networks mode=bssid 2>&1
    $result | Out-String
} catch {
    Write-Output "ERROR: Could not scan WiFi networks."
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def wifi_status():
    """Get current WiFi connection status."""
    script = r"""
try {
    $result = netsh wlan show interfaces 2>&1
    $result | Out-String
} catch {
    Write-Output "ERROR: Could not get WiFi status."
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def connect_wifi(ssid, password=None):
    """Connect to a WiFi network. Requires confirmation."""
    if not ssid or not isinstance(ssid, str):
        return "ERROR: SSID is required"
    if len(ssid) > 32:
        return "ERROR: SSID too long (max 32 chars)"
    err = _require_confirmation("connect_wifi")
    if err:
        return err
    escaped_ssid = ssid.replace("'", "''")
    if password:
        escaped_pwd = password.replace("'", "''")
        script = f"""
try {{
    # Create profile with password
    $xml = @"
<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{escaped_ssid}</name>
    <SSIDConfig><SSID><name>{escaped_ssid}</name></SSID></SSIDConfig>
    <connectionType>ESS</connectionType>
    <MSM><security><authEncryption><authentication>WPA2PSK</authentication><encryption>AES</encryption></authEncryption>
    <sharedKey><keyType>passPhrase</keyType><protected>false</protected><keyMaterial>{escaped_pwd}</keyMaterial></sharedKey>
    </security></MSM>
</WLANProfile>
"@
    $profilePath = [System.IO.Path]::GetTempFileName()
    $xml | Out-File -FilePath $profilePath -Encoding Unicode
    netsh wlan add profile filename="$profilePath" 2>&1 | Out-Null
    Remove-Item $profilePath -Force -ErrorAction SilentlyContinue
    netsh wlan connect name="{escaped_ssid}" 2>&1 | ForEach-Object {{ Write-Output $_ }}
    Start-Sleep -Seconds 2
    $conn = netsh wlan show interfaces 2>&1
    if ($conn -match "{escaped_ssid}") {{
        Write-Output "OK: Connected to '{escaped_ssid}'"
    }} else {{
        Write-Output "INFO: Connection attempt sent to '{escaped_ssid}'. Check status with wifi-status."
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    else:
        script = f"""
try {{
    netsh wlan connect name="{escaped_ssid}" 2>&1 | ForEach-Object {{ Write-Output $_ }}
    Start-Sleep -Seconds 2
    $conn = netsh wlan show interfaces 2>&1
    if ($conn -match "{escaped_ssid}") {{
        Write-Output "OK: Connected to '{escaped_ssid}'"
    }} else {{
        Write-Output "INFO: Connection attempt sent to '{escaped_ssid}'. Check status with wifi-status."
    }}
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def disconnect_wifi():
    """Disconnect from current WiFi network."""
    script = r"""
try {
    netsh wlan disconnect 2>&1 | ForEach-Object { Write-Output $_ }
    Start-Sleep -Seconds 1
    Write-Output "OK: WiFi disconnected"
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def list_wifi_profiles():
    """List saved WiFi profiles."""
    script = r"""
try {
    netsh wlan show profiles 2>&1 | Out-String
} catch {
    Write-Output "ERROR: Could not list WiFi profiles."
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def wifi_profile_detail(ssid):
    """Show details of a saved WiFi profile (including password if available)."""
    if not ssid or not isinstance(ssid, str):
        return "ERROR: SSID is required"
    if len(ssid) > 32:
        return "ERROR: SSID too long (max 32 chars)"
    escaped_ssid = ssid.replace("'", "''")
    script = f"""
try {{
    netsh wlan show profile name="{escaped_ssid}" key=clear 2>&1 | Out-String
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def forget_wifi(ssid):
    """Remove a saved WiFi profile. Requires confirmation."""
    if not ssid or not isinstance(ssid, str):
        return "ERROR: SSID is required"
    if len(ssid) > 32:
        return "ERROR: SSID too long (max 32 chars)"
    err = _require_confirmation("forget_wifi")
    if err:
        return err
    escaped_ssid = ssid.replace("'", "''")
    script = f"""
try {{
    netsh wlan delete profile name="{escaped_ssid}" 2>&1 | ForEach-Object {{ Write-Output $_ }}
    Write-Output "OK: WiFi profile '{escaped_ssid}' removed"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== IP / DNS ==========

def get_ip_config():
    """Get IP configuration for all adapters."""
    script = r"""
Get-NetIPConfiguration | ForEach-Object {
    [PSCustomObject]@{
        Interface = $_.InterfaceAlias
        IPv4 = if ($_.IPv4Address) { $_.IPv4Address.IPAddress -join ', ' } else { '' }
        IPv6 = if ($_.IPv6Address) { $_.IPv6Address.IPAddress -join ', ' } else { '' }
        Gateway = if ($_.IPv4DefaultGateway) { $_.IPv4DefaultGateway.NextHop -join ', ' } else { '' }
        DNS = if ($_.DNSServer) { $_.DNSServer.ServerAddresses -join ', ' } else { '' }
    }
} | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def get_dns(adapter=None):
    """Get DNS servers for an adapter (or all if not specified)."""
    if adapter:
        if not _validate_adapter_name(adapter):
            return "ERROR: Invalid adapter name"
        escaped = adapter.replace("'", "''")
        script = f"""
Get-DnsClientServerAddress -InterfaceAlias '{escaped}' -AddressFamily IPv4 |
    Select-Object InterfaceAlias, ServerAddresses |
    ForEach-Object {{
        [PSCustomObject]@{{
            Interface = $_.InterfaceAlias
            DNS = $_.ServerAddresses -join ', '
        }}
    }} | ConvertTo-Json
"""
    else:
        script = r"""
Get-DnsClientServerAddress -AddressFamily IPv4 |
    Select-Object InterfaceAlias, ServerAddresses |
    ForEach-Object {
        [PSCustomObject]@{
            Interface = $_.InterfaceAlias
            DNS = $_.ServerAddresses -join ', '
        }
    } | ConvertTo-Json -Compress
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def set_dns(adapter, servers):
    """Set DNS servers for an adapter. Requires confirmation."""
    if not _validate_adapter_name(adapter):
        return "ERROR: Invalid adapter name"
    if not servers or not isinstance(servers, str):
        return "ERROR: DNS servers required (comma-separated IPs)"
    # Validate each IP is a valid IPv4 address
    for ip in servers.split(","):
        ip = ip.strip()
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            return f"ERROR: Invalid IPv4 address: '{ip}'"
        parts = ip.split(".")
        if any(int(p) > 255 for p in parts):
            return f"ERROR: Invalid IPv4 address: '{ip}'"

    err = _require_confirmation("set_dns")
    if err:
        return err
    escaped = adapter.replace("'", "''")
    # Escape for PS string interpolation
    safe_servers = servers.replace("'", "''")
    script = f"""
try {{
    $servers = '{safe_servers}' -split ',' | ForEach-Object {{ $_.Trim() }}
    Set-DnsClientServerAddress -InterfaceAlias '{escaped}' -ServerAddresses $servers -ErrorAction Stop
    Write-Output "OK: DNS set to $servers on '{escaped}'"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def reset_dns(adapter):
    """Reset DNS to DHCP (automatic)."""
    if not _validate_adapter_name(adapter):
        return "ERROR: Invalid adapter name"
    escaped = adapter.replace("'", "''")
    script = f"""
try {{
    Set-DnsClientServerAddress -InterfaceAlias '{escaped}' -ResetServerAddresses -ErrorAction Stop
    Write-Output "OK: DNS reset to automatic on '{escaped}'"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Proxy ==========

def get_proxy():
    """Get current system proxy settings."""
    script = r"""
try {
    $reg = Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings'
    [PSCustomObject]@{
        ProxyEnable = [bool]$reg.ProxyEnable
        ProxyServer = $reg.ProxyServer
        ProxyOverride = $reg.ProxyOverride
        AutoConfigURL = $reg.AutoConfigURL
    } | ConvertTo-Json
} catch {
    Write-Output "ERROR: Could not read proxy settings."
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def set_proxy(address, port):
    """Set system proxy. Requires confirmation."""
    if not address or not isinstance(address, str):
        return "ERROR: Proxy address is required"
    if not re.match(r'^[\w.\-]+$', address):
        return "ERROR: Invalid proxy address"
    try:
        port = int(port)
        if not (1 <= port <= 65535):
            return "ERROR: Port must be 1-65535"
    except (ValueError, TypeError):
        return "ERROR: Port must be a number"
    err = _require_confirmation("set_proxy")
    if err:
        return err
    escaped_addr = address.replace("'", "''")
    script = f"""
try {{
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyEnable -Value 1 -ErrorAction Stop
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyServer -Value '{escaped_addr}:{port}' -ErrorAction Stop
    Write-Output "OK: Proxy set to {escaped_addr}:{port}"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


def disable_proxy():
    """Disable system proxy."""
    script = r"""
try {
    Set-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyEnable -Value 0 -ErrorAction Stop
    Write-Output "OK: Proxy disabled"
} catch {
    Write-Output "ERROR: $($_.Exception.Message)"
}
"""
    stdout, _, _ = _run_ps(script)
    return stdout


# ========== Connectivity ==========

def ping(host, count=4):
    """Test network connectivity to a host."""
    if not host or not isinstance(host, str):
        return "ERROR: Host is required"
    if len(host) > 253:
        return "ERROR: Host too long"
    # Basic validation: hostname or IPv4
    if not re.match(r'^[\w.\-]+$', host):
        return "ERROR: Invalid hostname or IP address"
    try:
        count = int(count)
        if not (1 <= count <= 20):
            count = 4
    except (ValueError, TypeError):
        count = 4
    escaped = host.replace("'", "''")
    script = f"""
try {{
    $result = Test-Connection -ComputerName '{escaped}' -Count {count} -ErrorAction Stop
    $sent = $result.Count
    $received = @($result | Where-Object {{ $_.StatusCode -eq 0 }}).Count
    $avg = [math]::Round(($result | Measure-Object -Property ResponseTime -Average).Average, 1)
    Write-Output "Ping {escaped}: $received/$sent succeeded, avg ${avg}ms"
}} catch {{
    Write-Output "Ping {escaped}: failed - $($_.Exception.Message)"
}}
"""
    stdout, _, _ = _run_ps(script, timeout=30)
    return stdout


# ========== Main ==========

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Network Controller")
    sub = parser.add_subparsers(dest="category")

    # Adapters
    p_adp = sub.add_parser("adapter", help="Network adapter management")
    adp_sub = p_adp.add_subparsers(dest="action")
    adp_sub.add_parser("list", help="List all adapters")
    adp_info = adp_sub.add_parser("info", help="Adapter details")
    adp_info.add_argument("--name", type=str, required=True)
    adp_en = adp_sub.add_parser("enable", help="Enable adapter")
    adp_en.add_argument("--name", type=str, required=True)
    adp_dis = adp_sub.add_parser("disable", help="Disable adapter")
    adp_dis.add_argument("--name", type=str, required=True)

    # WiFi
    p_wifi = sub.add_parser("wifi", help="WiFi management")
    wifi_sub = p_wifi.add_subparsers(dest="action")
    wifi_sub.add_parser("scan", help="Scan WiFi networks")
    wifi_sub.add_parser("status", help="Current WiFi connection")
    wifi_conn = wifi_sub.add_parser("connect", help="Connect to WiFi")
    wifi_conn.add_argument("--ssid", type=str, required=True)
    wifi_conn.add_argument("--password", type=str, default=None)
    wifi_sub.add_parser("disconnect", help="Disconnect WiFi")
    wifi_sub.add_parser("profiles", help="List saved profiles")
    wifi_det = wifi_sub.add_parser("profile-detail", help="Profile details")
    wifi_det.add_argument("--ssid", type=str, required=True)
    wifi_forget = wifi_sub.add_parser("forget", help="Remove saved profile")
    wifi_forget.add_argument("--ssid", type=str, required=True)

    # DNS
    p_dns = sub.add_parser("dns", help="DNS management")
    dns_sub = p_dns.add_subparsers(dest="action")
    dns_sub.add_parser("get", help="Get DNS servers")
    dns_sub.add_parser("get-ip", help="Get IP configuration")
    dns_set = dns_sub.add_parser("set", help="Set DNS servers")
    dns_set.add_argument("--adapter", type=str, required=True)
    dns_set.add_argument("--servers", type=str, required=True, help="Comma-separated IPs")
    dns_get = dns_sub.add_parser("adapter", help="Get DNS for specific adapter")
    dns_get.add_argument("--name", type=str, required=True)
    dns_reset = dns_sub.add_parser("reset", help="Reset DNS to DHCP")
    dns_reset.add_argument("--adapter", type=str, required=True)

    # Proxy
    p_proxy = sub.add_parser("proxy", help="System proxy")
    proxy_sub = p_proxy.add_subparsers(dest="action")
    proxy_sub.add_parser("get", help="Get proxy settings")
    proxy_set = proxy_sub.add_parser("set", help="Set proxy")
    proxy_set.add_argument("--address", type=str, required=True)
    proxy_set.add_argument("--port", type=str, required=True)
    proxy_sub.add_parser("disable", help="Disable proxy")

    # Connectivity
    p_conn = sub.add_parser("connectivity", help="Network connectivity test")
    conn_sub = p_conn.add_subparsers(dest="action")
    conn_ping = conn_sub.add_parser("ping", help="Ping a host")
    conn_ping.add_argument("--host", type=str, required=True)
    conn_ping.add_argument("--count", type=int, default=4)

    args = parser.parse_args()

    if args.category == "adapter":
        if args.action == "list":
            print(list_adapters())
        elif args.action == "info":
            print(adapter_info(args.name))
        elif args.action == "enable":
            print(enable_adapter(args.name))
        elif args.action == "disable":
            print(disable_adapter(args.name))
        else:
            p_adp.print_help()
    elif args.category == "wifi":
        if args.action == "scan":
            print(list_wifi())
        elif args.action == "status":
            print(wifi_status())
        elif args.action == "connect":
            print(connect_wifi(args.ssid, args.password))
        elif args.action == "disconnect":
            print(disconnect_wifi())
        elif args.action == "profiles":
            print(list_wifi_profiles())
        elif args.action == "profile-detail":
            print(wifi_profile_detail(args.ssid))
        elif args.action == "forget":
            print(forget_wifi(args.ssid))
        else:
            p_wifi.print_help()
    elif args.category == "dns":
        if args.action == "get":
            print(get_dns())
        elif args.action == "get-ip":
            print(get_ip_config())
        elif args.action == "adapter":
            print(get_dns(args.name))
        elif args.action == "set":
            print(set_dns(args.adapter, args.servers))
        elif args.action == "reset":
            print(reset_dns(args.adapter))
        else:
            p_dns.print_help()
    elif args.category == "proxy":
        if args.action == "get":
            print(get_proxy())
        elif args.action == "set":
            print(set_proxy(args.address, args.port))
        elif args.action == "disable":
            print(disable_proxy())
        else:
            p_proxy.print_help()
    elif args.category == "connectivity":
        if args.action == "ping":
            print(ping(args.host, args.count))
        else:
            p_conn.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
