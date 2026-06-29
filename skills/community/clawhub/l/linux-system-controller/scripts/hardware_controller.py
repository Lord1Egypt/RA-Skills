#!/usr/bin/env python3
"""
Hardware Controller - Control Linux system hardware settings.

Capabilities:
  - Volume control (get/set/mute/unmute)
  - Screen brightness (get/set)
  - Power management (sleep, hibernate, shutdown, restart, lock)
  - Network adapters (list, enable, disable, WiFi scan, network info)
  - USB devices (list)

Requirements: Linux with standard tools (amixer, xbacklight/brillo, systemctl, ip, lsusb)
Dependencies: None
"""

import subprocess
import json
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


def run_command(cmd, timeout=30):
    """Execute shell command with proper encoding."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace"
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "ERROR: Command timed out", -1
    except Exception as e:
        return "", f"ERROR: {e}", -1


# ============ Volume Control ============

def volume_get():
    """Get current volume level."""
    stdout, stderr, code = run_command("amixer get Master")
    if code != 0:
        return {"error": f"Failed to get volume: {stderr}"}

    # Parse amixer output
    import re
    match = re.search(r'\[(\d+)%\]', stdout)
    if match:
        volume = int(match.group(1))
        muted = '[off]' in stdout
        return {"volume": volume, "muted": muted}
    return {"error": "Failed to parse volume"}


def volume_set(level):
    """Set volume level (0-100)."""
    if not 0 <= level <= 100:
        return {"error": "Volume must be between 0 and 100"}

    cmd = f"amixer set Master {level}%"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "volume": level}
    return {"error": f"Failed to set volume: {stderr}"}


def volume_mute():
    """Mute volume."""
    cmd = "amixer set Master mute"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "muted": True}
    return {"error": f"Failed to mute volume: {stderr}"}


def volume_unmute():
    """Unmute volume."""
    cmd = "amixer set Master unmute"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "muted": False}
    return {"error": f"Failed to unmute volume: {stderr}"}


# ============ Screen Brightness ============

def brightness_get():
    """Get current screen brightness level."""
    stdout, stderr, code = run_command("xbacklight -get")
    if code == 0:
        brightness = float(stdout)
        return {"brightness": round(brightness, 2)}
    return {"error": f"Failed to get brightness: {stderr}"}


def brightness_set(level):
    """Set screen brightness level (0-100)."""
    if not 0 <= level <= 100:
        return {"error": "Brightness must be between 0 and 100"}

    cmd = f"xbacklight -set {level}"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "brightness": level}
    return {"error": f"Failed to set brightness: {stderr}"}


# ============ Power Management ============

def power_lock():
    """Lock the screen."""
    cmd = "xdg-screensaver lock"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True}
    # Fallback: use dm-tool
    cmd2 = "dm-tool lock"
    stdout, stderr, code = run_command(cmd2)
    if code == 0:
        return {"success": True}
    return {"error": "Failed to lock screen"}


def power_sleep():
    """Put system to sleep."""
    cmd = "systemctl suspend"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True}
    return {"error": f"Failed to suspend: {stderr}"}


def power_hibernate():
    """Hibernate the system."""
    cmd = "systemctl hibernate"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True}
    return {"error": f"Failed to hibernate: {stderr}"}


def power_shutdown():
    """Shutdown the system."""
    cmd = "shutdown -h now"
    return {"success": True, "message": "System is shutting down"}


def power_restart():
    """Restart the system."""
    cmd = "shutdown -r now"
    return {"success": True, "message": "System is restarting"}


# ============ Network ============

def network_list_adapters():
    """List all network adapters."""
    cmd = "ip -o link show | awk '{print $2, $9}' | sed 's/:$//'"
    stdout, stderr, code = run_command(cmd)
    if code != 0:
        return {"error": f"Failed to list adapters: {stderr}"}

    adapters = []
    for line in stdout.split('\n'):
        if not line.strip():
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            adapters.append({
                "name": parts[0],
                "status": parts[1]
            })
    return {"adapters": adapters}


def network_enable(adapter):
    """Enable a network adapter."""
    cmd = f"ip link set {adapter} up"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "adapter": adapter}
    return {"error": f"Failed to enable {adapter}: {stderr}"}


def network_disable(adapter):
    """Disable a network adapter."""
    cmd = f"ip link set {adapter} down"
    stdout, stderr, code = run_command(cmd)
    if code == 0:
        return {"success": True, "adapter": adapter}
    return {"error": f"Failed to disable {adapter}: {stderr}"}


def network_wifi_scan():
    """Scan for WiFi networks."""
    cmd = "nmcli device wifi list"
    stdout, stderr, code = run_command(cmd)
    if code != 0:
        return {"error": f"Failed to scan WiFi: {stderr}"}

    networks = []
    lines = stdout.split('\n')[1:]  # Skip header
    for line in lines:
        if not line.strip():
            continue
        parts = line.split()
        if len(parts) >= 8:
            networks.append({
                "ssid": parts[1],
                "mode": parts[2],
                "channel": parts[3],
                "rate": parts[4],
                "signal": parts[5],
                "bars": parts[6],
                "security": parts[7]
            })
    return {"networks": networks}


def network_info():
    """Get network information."""
    # IP addresses
    cmd = "ip addr show | grep 'inet ' | grep -v '127.0.0.1'"
    ip_stdout, _, _ = run_command(cmd)

    # Default gateway
    cmd2 = "ip route | grep default"
    gateway_stdout, _, _ = run_command(cmd2)

    return {
        "ip_addresses": ip_stdout.split('\n') if ip_stdout else [],
        "gateway": gateway_stdout if gateway_stdout else None
    }


# ============ USB ============

def usb_list():
    """List all USB devices."""
    cmd = "lsusb"
    stdout, stderr, code = run_command(cmd)
    if code != 0:
        return {"error": f"Failed to list USB devices: {stderr}"}

    devices = []
    for line in stdout.split('\n'):
        if not line.strip():
            continue
        # Parse: Bus 001 Device 002: ID 1234:5678 Manufacturer Name
        import re
        match = re.match(r'Bus (\d+) Device (\d+): ID ([\da-f]+):([\da-f]+) (.+)', line)
        if match:
            devices.append({
                "bus": int(match.group(1)),
                "device": int(match.group(2)),
                "vendor_id": match.group(3),
                "product_id": match.group(4),
                "name": match.group(5).strip()
            })
    return {"devices": devices}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Hardware Controller for Linux")
    subparsers = parser.add_subparsers(dest='category', help='Category to control')

    # Volume
    volume_parser = subparsers.add_parser('volume', help='Volume control')
    volume_subparsers = volume_parser.add_subparsers(dest='action', help='Volume action')
    volume_subparsers.add_parser('get', help='Get volume')
    volume_subparsers.add_parser('mute', help='Mute volume')
    volume_subparsers.add_parser('unmute', help='Unmute volume')
    volume_set_parser = volume_subparsers.add_parser('set', help='Set volume')
    volume_set_parser.add_argument('--level', type=int, required=True, help='Volume level (0-100)')

    # Screen
    screen_parser = subparsers.add_parser('screen', help='Screen control')
    screen_subparsers = screen_parser.add_subparsers(dest='action', help='Screen action')
    brightness_parser = screen_subparsers.add_parser('brightness', help='Brightness control')
    brightness_subparsers = brightness_parser.add_subparsers(dest='subaction', help='Brightness action')
    brightness_subparsers.add_parser('get', help='Get brightness')
    brightness_set_parser = brightness_subparsers.add_parser('set', help='Set brightness')
    brightness_set_parser.add_argument('--level', type=int, required=True, help='Brightness level (0-100)')

    # Power
    power_parser = subparsers.add_parser('power', help='Power management')
    power_subparsers = power_parser.add_subparsers(dest='action', help='Power action')
    power_subparsers.add_parser('lock', help='Lock screen')
    power_subparsers.add_parser('sleep', help='Suspend')
    power_subparsers.add_parser('hibernate', help='Hibernate')
    power_subparsers.add_parser('shutdown', help='Shutdown')
    power_subparsers.add_parser('restart', help='Restart')

    # Network
    network_parser = subparsers.add_parser('network', help='Network control')
    network_subparsers = network_parser.add_subparsers(dest='action', help='Network action')
    network_subparsers.add_parser('list', help='List adapters')
    network_subparsers.add_parser('wifi', help='Scan WiFi')
    network_subparsers.add_parser('info', help='Network info')
    network_enable_parser = network_subparsers.add_parser('enable', help='Enable adapter')
    network_enable_parser.add_argument('--adapter', required=True, help='Adapter name')
    network_disable_parser = network_subparsers.add_parser('disable', help='Disable adapter')
    network_disable_parser.add_argument('--adapter', required=True, help='Adapter name')

    # USB
    usb_parser = subparsers.add_parser('usb', help='USB control')
    usb_subparsers = usb_parser.add_subparsers(dest='action', help='USB action')
    usb_subparsers.add_parser('list', help='List USB devices')

    args = parser.parse_args()

    if not args.category:
        parser.print_help()
        sys.exit(1)

    result = {}

    # Volume
    if args.category == 'volume':
        if args.action == 'get':
            result = volume_get()
        elif args.action == 'set':
            result = volume_set(args.level)
        elif args.action == 'mute':
            result = volume_mute()
        elif args.action == 'unmute':
            result = volume_unmute()

    # Screen
    elif args.category == 'screen':
        if args.action == 'brightness':
            if args.subaction == 'get':
                result = brightness_get()
            elif args.subaction == 'set':
                result = brightness_set(args.level)

    # Power
    elif args.category == 'power':
        if args.action == 'lock':
            result = power_lock()
        elif args.action == 'sleep':
            result = power_sleep()
        elif args.action == 'hibernate':
            result = power_hibernate()
        elif args.action == 'shutdown':
            result = power_shutdown()
        elif args.action == 'restart':
            result = power_restart()

    # Network
    elif args.category == 'network':
        if args.action == 'list':
            result = network_list_adapters()
        elif args.action == 'enable':
            result = network_enable(args.adapter)
        elif args.action == 'disable':
            result = network_disable(args.adapter)
        elif args.action == 'wifi':
            result = network_wifi_scan()
        elif args.action == 'info':
            result = network_info()

    # USB
    elif args.category == 'usb':
        if args.action == 'list':
            result = usb_list()

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
