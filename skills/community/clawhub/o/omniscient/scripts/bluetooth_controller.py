#!/usr/bin/env python3
"""
Bluetooth Controller - Manage Bluetooth devices on Windows/macOS/Linux.

Capabilities:
  - Bluetooth adapter info
  - List paired/connected devices
  - BLE scan and service discovery (requires bleak)
  - Classic Bluetooth scan (Linux/macOS)
  - Connect/disconnect/unpair devices

Requirements: Windows 10/11 or macOS or Linux
Dependencies: bleak (for BLE features, auto-installed)
"""

import subprocess
import sys
import json
import os
import platform
import asyncio
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


# ========== Utilities ==========

def _is_windows():
    return platform.system() == "Windows"


def _run_cmd(cmd, timeout=30):
    """Execute a shell command with safety filtering.

    Security measures:
      - Command must be a string
      - Command length limited
      - Rejects backtick, $() substitution, ${} variable expansion
      - Input parameters (address etc.) should be pre-validated before calling

    Note: Pipe (|) and redirection (2>/dev/null) are allowed because this
    function is used for bluetoothctl/hcitool commands that require them.
    """
    if not isinstance(cmd, str):
        return "", "ERROR: Command must be a string", -1
    if len(cmd) > 10000:
        return "", "ERROR: Command exceeds maximum length", -1
    # Block dangerous shell injection patterns
    for blocked in ('`', '$(', '${'):
        if blocked in cmd:
            return "", f"ERROR: Command blocked - contains '{blocked}'", -1

    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=timeout
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "Command timed out", -1
    except Exception as e:
        return "", str(e), -1


def _validate_bt_address(address):
    """Validate Bluetooth address format: XX:XX:XX:XX:XX:XX (hex)."""
    if not address or not isinstance(address, str):
        return None
    address = address.strip()
    if not re.match(r'^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$', address):
        return None
    return address.upper()


def _check_bleak():
    """Check if bleak is available."""
    try:
        import bleak
        return True
    except ImportError:
        return False


def _ensure_bleak():
    """Ensure bleak is installed."""
    try:
        import bleak
        return bleak
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "bleak>=0.22.0,<1", "-q"])
        import bleak
        return bleak


# ========== Adapter Info ==========

def bt_info():
    """Get Bluetooth adapter information."""
    result = {
        "OS": f"{platform.system()} {platform.release()}",
        "Python": platform.python_version(),
    }

    if _is_windows():
        stdout, _, rc = _run_ps(
            "Get-PnpDevice -Class Bluetooth | Select-Object Status, FriendlyName, InstanceId | ConvertTo-Json",
            timeout=10
        )
        if stdout and stdout != '{}':
            try:
                result["Devices"] = json.loads(stdout)
            except Exception:
                result["DevicesRaw"] = stdout
        else:
            result["Info"] = "No Bluetooth adapter detected"

        stdout2, _, _ = _run_ps(
            "Get-Service bthserv | Select-Object Status, Name, DisplayName | ConvertTo-Json",
            timeout=5
        )
        if stdout2 and stdout2 != '{}':
            try:
                result["Service"] = json.loads(stdout2)
            except Exception:
                pass
    else:
        stdout, _, _ = _run_cmd("hciconfig -a 2>/dev/null || bluetoothctl show 2>/dev/null", 5)
        if stdout:
            result["AdapterInfo"] = stdout
        else:
            result["Info"] = "Bluetooth tools not installed or no permission"

    return json.dumps(result, indent=2, ensure_ascii=False)


# ========== Device Listing ==========

def bt_devices():
    """List currently connected Bluetooth devices."""
    if _is_windows():
        stdout, _, _ = _run_ps(
            "Get-PnpDevice -Class Bluetooth -Status OK | "
            "Where-Object { $_.FriendlyName -ne $null } | "
            "Select-Object FriendlyName | ConvertTo-Json",
            timeout=10
        )
        if stdout and stdout != '{}' and stdout != '[]':
            return stdout
        return json.dumps({"Info": "No connected Bluetooth devices found"})
    else:
        stdout, _, _ = _run_cmd("bluetoothctl devices Connected 2>/dev/null", 5)
        if stdout:
            lines = [l.strip() for l in stdout.split("\n") if l.strip()]
            return json.dumps({"ConnectedDevices": lines}, indent=2, ensure_ascii=False)
        return json.dumps({"Info": "No connected Bluetooth devices found"})


def bt_paired():
    """List paired Bluetooth devices."""
    if _is_windows():
        stdout, _, _ = _run_ps(
            "Get-PnpDevice -Class Bluetooth | "
            "Where-Object { $_.Status -eq 'OK' -or $_.Status -eq 'Error' } | "
            "Select-Object Status, FriendlyName | ConvertTo-Json",
            timeout=10
        )
        if stdout and stdout != '{}' and stdout != '[]':
            return stdout
        return json.dumps({"Info": "No paired devices found"})
    else:
        stdout, _, _ = _run_cmd("bluetoothctl devices 2>/dev/null", 5)
        if stdout:
            lines = [l.strip() for l in stdout.split("\n") if l.strip()]
            return json.dumps({"PairedDevices": lines}, indent=2, ensure_ascii=False)
        return json.dumps({"Info": "No paired devices or Bluetooth tools not installed"})


# ========== BLE Scan & Discovery ==========

def ble_scan(timeout=10):
    """Scan for BLE devices nearby."""
    bleak = _ensure_bleak()

    async def _scan():
        from bleak import BleakScanner
        devices = await BleakScanner.discover(timeout=timeout)
        if not devices:
            return json.dumps({"Info": "No BLE devices found"})
        results = []
        for i, d in enumerate(devices, 1):
            results.append({
                "Index": i,
                "Name": d.name or "(Unknown)",
                "Address": d.address,
                "RSSI": d.rssi,
            })
        return json.dumps({"Count": len(results), "Devices": results}, indent=2, ensure_ascii=False)

    return asyncio.run(_scan())


def ble_services(address, timeout=10):
    """Discover services of a BLE device."""
    safe_addr = _validate_bt_address(address)
    if safe_addr is None:
        return json.dumps({"Error": "Invalid Bluetooth address. Expected format: XX:XX:XX:XX:XX:XX"})
    address = safe_addr
    bleak = _ensure_bleak()

    async def _discover():
        from bleak import BleakClient
        try:
            async with BleakClient(address, timeout=timeout) as client:
                if not client.is_connected:
                    return json.dumps({"Error": "Connection failed"})
                result = {
                    "Address": client.address,
                    "Name": client.name or "Unknown",
                    "Connected": True,
                    "Services": [],
                }
                services = await client.get_services()
                for svc in services:
                    svc_info = {
                        "UUID": svc.uuid,
                        "Description": svc.description,
                    }
                    if svc.characteristics:
                        svc_info["Characteristics"] = [
                            {"UUID": c.uuid, "Properties": ", ".join(c.properties)}
                            for c in svc.characteristics
                        ]
                    result["Services"].append(svc_info)
                return json.dumps(result, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"Error": str(e)})

    return asyncio.run(_discover())


# ========== Classic Bluetooth ==========

def classic_scan(timeout=10):
    """Scan for classic Bluetooth devices."""
    if not _is_windows():
        stdout, _, _ = _run_cmd(
            f"hcitool scan 2>/dev/null || timeout {timeout} bluetoothctl scan on 2>/dev/null",
            timeout + 5
        )
        if stdout:
            lines = [l.strip() for l in stdout.split("\n") if l.strip()]
            return json.dumps({"Count": len(lines), "Devices": lines}, indent=2, ensure_ascii=False)
        return json.dumps({"Info": "No devices found or Bluetooth tools not installed"})
    else:
        return json.dumps({"Info": "Windows: Use BLE scan (list command) or Settings > Bluetooth > Add device"})


# ========== Connection Management ==========

def bt_connect(address):
    """Connect to a Bluetooth device."""
    safe_addr = _validate_bt_address(address)
    if safe_addr is None:
        return json.dumps({"Error": "Invalid Bluetooth address. Expected format: XX:XX:XX:XX:XX:XX"})
    address = safe_addr
    if _is_windows():
        stdout, stderr, _ = _run_cmd(
            f'powershell -Command "Connect-BluetoothDevice -Address \'{address}\' 2>$null; '
            f'Add-Device -BluetoothAddress \'{address}\' -Confirm:$false 2>$null"',
            15
        )
        msg = stdout or "Connection command sent, check system notifications"
        result = {"OK": msg}
        if stderr:
            result["Note"] = stderr
        return json.dumps(result, indent=2, ensure_ascii=False)
    elif platform.system() == "Linux":
        stdout, _, _ = _run_cmd(f'echo -e "connect {address}\\nquit" | bluetoothctl 2>/dev/null', 15)
        return json.dumps({"OK": stdout or "Connection command sent"}, indent=2, ensure_ascii=False)
    else:
        return json.dumps({"Info": "macOS: Use System Preferences > Bluetooth to connect manually"})


def bt_disconnect(address):
    """Disconnect a Bluetooth device."""
    safe_addr = _validate_bt_address(address)
    if safe_addr is None:
        return json.dumps({"Error": "Invalid Bluetooth address. Expected format: XX:XX:XX:XX:XX:XX"})
    address = safe_addr
    if _is_windows():
        stdout, _, _ = _run_cmd(
            f'powershell -Command "Disconnect-BluetoothDevice -Address \'{address}\' 2>$null"',
            10
        )
        return json.dumps({"OK": stdout or "Disconnect command sent"}, indent=2, ensure_ascii=False)
    elif platform.system() == "Linux":
        stdout, _, _ = _run_cmd(f'echo -e "disconnect {address}\\nquit" | bluetoothctl 2>/dev/null', 10)
        return json.dumps({"OK": stdout or "Disconnect command sent"}, indent=2, ensure_ascii=False)
    else:
        return json.dumps({"Info": "macOS: Use System Preferences > Bluetooth to disconnect manually"})


def bt_unpair(address):
    """Unpair a Bluetooth device."""
    safe_addr = _validate_bt_address(address)
    if safe_addr is None:
        return json.dumps({"Error": "Invalid Bluetooth address. Expected format: XX:XX:XX:XX:XX:XX"})
    address = safe_addr
    if _is_windows():
        stdout, _, _ = _run_cmd(
            f'powershell -Command "Remove-BluetoothDevice -Address \'{address}\' -Confirm:$false 2>$null"',
            10
        )
        return json.dumps({"OK": stdout or "Unpair command sent"}, indent=2, ensure_ascii=False)
    elif platform.system() == "Linux":
        stdout, _, _ = _run_cmd(f'echo -e "remove {address}\\nquit" | bluetoothctl 2>/dev/null', 10)
        return json.dumps({"OK": stdout or "Unpair command sent"}, indent=2, ensure_ascii=False)
    else:
        return json.dumps({"Info": "macOS: Use System Preferences > Bluetooth to unpair manually"})


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Bluetooth Controller")
    sub = parser.add_subparsers(dest="command")

    # info
    sub.add_parser("info", help="Bluetooth adapter info")

    # list
    p_list = sub.add_parser("list", help="BLE scan nearby devices")
    p_list.add_argument("--timeout", type=int, default=10, help="Scan timeout in seconds")

    # paired
    sub.add_parser("paired", help="List paired devices")

    # devices
    sub.add_parser("devices", help="List connected devices")

    # services
    p_svc = sub.add_parser("services", help="Discover BLE device services")
    p_svc.add_argument("address", help="Device Bluetooth address")
    p_svc.add_argument("--timeout", type=int, default=10, help="Discovery timeout in seconds")

    # scan-classic
    p_classic = sub.add_parser("scan-classic", help="Classic Bluetooth scan")
    p_classic.add_argument("--timeout", type=int, default=10, help="Scan timeout in seconds")

    # connect
    p_conn = sub.add_parser("connect", help="Connect to device")
    p_conn.add_argument("address", help="Device Bluetooth address")

    # disconnect
    p_disc = sub.add_parser("disconnect", help="Disconnect device")
    p_disc.add_argument("address", help="Device Bluetooth address")

    # unpair
    p_unpair = sub.add_parser("unpair", help="Unpair device")
    p_unpair.add_argument("address", help="Device Bluetooth address")

    args = parser.parse_args()

    if args.command == "info":
        print(bt_info())
    elif args.command == "list":
        print(ble_scan(args.timeout))
    elif args.command == "paired":
        print(bt_paired())
    elif args.command == "devices":
        print(bt_devices())
    elif args.command == "services":
        print(ble_services(args.address, args.timeout))
    elif args.command == "scan-classic":
        print(classic_scan(args.timeout))
    elif args.command == "connect":
        print(bt_connect(args.address))
    elif args.command == "disconnect":
        print(bt_disconnect(args.address))
    elif args.command == "unpair":
        print(bt_unpair(args.address))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
