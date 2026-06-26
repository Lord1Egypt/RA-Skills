#!/usr/bin/env python3
"""Bluetooth Controller - cross-platform."""
import json, sys, os, argparse, asyncio

def get_adapter_info():
    """Get adapter information."""
    try:
        import subprocess
        stdout = subprocess.check_output(['bluetoothctl', 'info'], text=True)
        return json.dumps({"adapter": stdout}, indent=2)
    except:
        return json.dumps({"error": "Bluetooth not available"}, indent=2)

def list_paired():
    """List paired devices."""
    try:
        import subprocess
        stdout = subprocess.check_output(['bluetoothctl', 'paired-devices'], text=True)
        return json.dumps({"paired": stdout}, indent=2)
    except:
        return json.dumps({"error": "Bluetooth not available"}, indent=2)

async def scan_ble(timeout=10):
    """Scan BLE devices."""
    try:
        import bleak
        devices = []
        async with bleak.BleakScanner() as scanner:
            device = await scanner.discover(timeout=timeout)
            devices.append({"name": device.name, "address": device.address})
        return json.dumps({"devices": devices}, indent=2)
    except ImportError:
        return json.dumps({"error": "Install bleak"}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

async def discover_services(address):
    """Discover services for device."""
    try:
        import bleak
        async with bleak.BleakClient(address) as client:
            services = await client.get_services()
            return json.dumps({"services": str(services)}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

async def connect_device(address):
    """Connect to device."""
    try:
        import bleak
        async with bleak.BleakClient(address) as client:
            connected = await client.is_connected()
            return json.dumps({"connected": connected, "address": address}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, indent=2)

def main():
    parser = argparse.ArgumentParser(description='Bluetooth Controller')
    subparsers = parser.add_subparsers(dest='command')

    # info command
    subparsers.add_parser('info')

    # paired command
    subparsers.add_parser('paired')

    # scan command
    scan_parser = subparsers.add_parser('scan')
    scan_parser.add_argument('--timeout', type=int, default=10)

    # discover command
    discover_parser = subparsers.add_parser('discover')
    discover_parser.add_argument('--address', required=True)

    # connect command
    connect_parser = subparsers.add_parser('connect')
    connect_parser.add_argument('address')

    args = parser.parse_args()

    if args.command == 'info':
        print(get_adapter_info())
    elif args.command == 'paired':
        print(list_paired())
    elif args.command == 'scan':
        print(asyncio.run(scan_ble(args.timeout)))
    elif args.command == 'discover':
        print(asyncio.run(discover_services(args.address)))
    elif args.command == 'connect':
        print(asyncio.run(connect_device(args.address)))

if __name__ == '__main__':
    main()
