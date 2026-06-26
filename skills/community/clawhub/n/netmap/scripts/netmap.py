#!/usr/bin/env python3
"""
netmap - Home/office network device scanner
Maps all devices on your local network: IP, hostname, MAC, vendor, first/last seen.

Commands:
  scan          Scan network and update device database
  list          Show all known devices
  find <query>  Search by IP, hostname, MAC, or vendor
  new           Show devices seen in the last N minutes (default 60)
  gone          Show devices that disappeared recently
  watch         Continuous scan mode (Ctrl+C to stop)
  export        Export device list as JSON
"""

import sys
import os
import json
import subprocess
import re
import socket
import struct
import time
import argparse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

DB_FILE = Path.home() / '.config' / 'netmap' / 'devices.json'
VENDOR_CACHE_FILE = Path.home() / '.config' / 'netmap' / 'vendor_cache.json'
DB_FILE.parent.mkdir(parents=True, exist_ok=True)

NMAP_PATH = subprocess.run(['which', 'nmap'], capture_output=True, text=True).stdout.strip() or 'nmap'


def load_vendor_cache():
    if VENDOR_CACHE_FILE.exists():
        try:
            return json.loads(VENDOR_CACHE_FILE.read_text())
        except Exception:
            pass
    return {}


def save_vendor_cache(cache):
    VENDOR_CACHE_FILE.write_text(json.dumps(cache, indent=2))


def lookup_vendor(mac):
    """Look up vendor for a MAC address, with local caching."""
    if not mac:
        return None
    prefix = mac[:8].upper()  # First 3 octets
    cache = load_vendor_cache()
    if prefix in cache:
        return cache[prefix]
    try:
        resp = urllib.request.urlopen(
            f'https://api.macvendors.com/{mac}', timeout=3
        )
        vendor = resp.read().decode('utf-8').strip()
        if vendor and 'Not Found' not in vendor:
            cache[prefix] = vendor
            save_vendor_cache(cache)
            return vendor
    except Exception:
        pass
    cache[prefix] = None
    save_vendor_cache(cache)
    return None


def load_db():
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text())
        except Exception:
            pass
    return {'devices': {}, 'last_scan': None}


def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2, default=str))


def get_local_subnet():
    """Auto-detect the local network subnet (e.g. 192.168.0.0/24)."""
    try:
        # Get default gateway interface IP
        result = subprocess.run(
            ['python3', '-c',
             'import socket; s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM); '
             's.connect(("8.8.8.8",80)); print(s.getsockname()[0]); s.close()'],
            capture_output=True, text=True
        )
        ip = result.stdout.strip()
        if ip:
            parts = ip.split('.')
            return f"{parts[0]}.{parts[1]}.{parts[2]}.0/24"
    except Exception:
        pass
    return '192.168.0.0/24'


def get_arp_table():
    """Get MAC addresses from ARP cache without sudo (macOS/Linux)."""
    macs = {}
    try:
        result = subprocess.run(['/usr/sbin/arp', '-a'], capture_output=True, text=True, timeout=5)
        out = result.stdout
    except Exception:
        try:
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=5)
            out = result.stdout
        except Exception:
            return macs
    for line in out.splitlines():
        # Format: ? (192.168.1.1) at cc:40:d0:15:53:d4 on en1 ...
        m = re.search(r'\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-f:]{17})', line, re.I)
        if m:
            ip, mac = m.group(1), m.group(2).upper()
            if mac != 'FF:FF:FF:FF:FF:FF':
                macs[ip] = mac
    return macs


def run_nmap(subnet, fast=True):
    """Run nmap host discovery."""
    print(f"  Scanning {subnet} (this may take 30-60s)...")
    cmd = [
        NMAP_PATH,
        '-sn',           # Ping scan — discovers live hosts
        '-oX', '-',      # XML output to stdout
        '--host-timeout', '15s',
        subnet
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def run_nmap_ports(ip):
    """Quick port scan to fingerprint device type."""
    try:
        result = subprocess.run(
            [NMAP_PATH, '-F', '--open', '-oX', '-', '--host-timeout', '10s', ip],
            capture_output=True, text=True, timeout=20
        )
        return result.stdout
    except Exception:
        return ''


def guess_device_type(open_ports, hostname, vendor):
    """Guess device type from open ports and hostname."""
    ports = set(open_ports)
    hostname_lower = (hostname or '').lower()
    vendor_lower = (vendor or '').lower()

    hints = []
    if 80 in ports or 443 in ports:
        hints.append('web interface')
    if 9100 in ports or 631 in ports:
        hints.append('printer')
    if 22 in ports:
        hints.append('SSH')
    if 5353 in ports:
        hints.append('mDNS')
    if 62078 in ports:
        hints.append('iPhone/iPad')
    if 7000 in ports or 7100 in ports:
        hints.append('AirPlay')
    if 8080 in ports or 8443 in ports:
        hints.append('NAS/server')

    if 'canon' in vendor_lower or 'canon' in hostname_lower:
        return 'Canon printer'
    if 'apple' in vendor_lower:
        return 'Apple device'
    if 'samsung' in vendor_lower:
        return 'Samsung device'
    if 'amazon' in vendor_lower or 'echo' in hostname_lower:
        return 'Amazon device'
    if 'ring' in hostname_lower:
        return 'Ring device'
    if 'roku' in hostname_lower or 'roku' in vendor_lower:
        return 'Roku'
    if 'router' in hostname_lower or '.1' == (hostname_lower or '').split('.')[-1]:
        return 'Router/gateway'

    if hints:
        return ', '.join(hints)
    return None


def parse_nmap_xml(xml_output):
    """Parse nmap XML into list of device dicts."""
    import xml.etree.ElementTree as ET
    devices = []
    try:
        root = ET.fromstring(xml_output)
    except ET.ParseError:
        return devices

    for host in root.findall('host'):
        state_el = host.find('status')
        if state_el is None or state_el.get('state') != 'up':
            continue

        device = {'ip': None, 'mac': None, 'hostname': None, 'vendor': None}

        for addr in host.findall('address'):
            addrtype = addr.get('addrtype')
            if addrtype == 'ipv4':
                device['ip'] = addr.get('addr')
            elif addrtype == 'mac':
                device['mac'] = addr.get('addr', '').upper()
                device['vendor'] = addr.get('vendor') or None

        hostnames = host.find('hostnames')
        if hostnames is not None:
            for hn in hostnames.findall('hostname'):
                if hn.get('type') in ('PTR', 'user'):
                    device['hostname'] = hn.get('name')
                    break

        if device['ip']:
            devices.append(device)

    return devices


def reverse_dns(ip):
    """Try reverse DNS lookup."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def scan(subnet=None, quiet=False, deep=False):
    """Scan network and update device database."""
    if subnet is None:
        subnet = get_local_subnet()

    if not quiet:
        print(f"🔍 netmap scan{'  (deep mode)' if deep else ''}")
        print(f"  Network: {subnet}")

    db = load_db()
    now = datetime.now().isoformat()
    xml = run_nmap(subnet)
    found = parse_nmap_xml(xml)

    # Enrich with ARP table (MAC addresses without sudo)
    arp_table = get_arp_table()
    for device in found:
        if device['ip'] and not device.get('mac') and device['ip'] in arp_table:
            device['mac'] = arp_table[device['ip']]
        # Vendor lookup if we have MAC but no vendor (check cache first, fast)
        if device.get('mac') and not device.get('vendor'):
            v = lookup_vendor(device['mac'])
            if v:
                device['vendor'] = v

    # Deep scan: fingerprint each device via port scan
    if deep and found:
        print(f"  Fingerprinting {len(found)} devices...")
        import xml.etree.ElementTree as ET
        for device in found:
            port_xml = run_nmap_ports(device['ip'])
            open_ports = []
            try:
                root = ET.fromstring(port_xml)
                for port in root.findall('.//port'):
                    state = port.find('state')
                    if state is not None and state.get('state') == 'open':
                        open_ports.append(int(port.get('portid', 0)))
            except Exception:
                pass
            device['device_type'] = guess_device_type(
                open_ports, device.get('hostname'), device.get('vendor')
            )
            device['open_ports'] = open_ports

    if not found and not quiet:
        print("  ⚠️  No devices found. Try running with sudo for full ARP scan.")

    # Mark all current devices as potentially gone
    for mac, dev in db['devices'].items():
        dev['_seen_this_scan'] = False

    new_count = 0
    updated_count = 0

    for device in found:
        # Try reverse DNS if no hostname
        if not device['hostname'] and device['ip']:
            device['hostname'] = reverse_dns(device['ip'])

        key = device['mac'] or device['ip']  # Use MAC as key, fall back to IP
        if key:
            if key not in db['devices']:
                db['devices'][key] = {
                    'ip': device['ip'],
                    'mac': device['mac'],
                    'hostname': device['hostname'],
                    'vendor': device['vendor'],
                    'device_type': device.get('device_type'),
                    'open_ports': device.get('open_ports', []),
                    'first_seen': now,
                    'last_seen': now,
                    'label': None,  # User-set friendly name
                }
                new_count += 1
            else:
                existing = db['devices'][key]
                existing['ip'] = device['ip']
                existing['last_seen'] = now
                if device['hostname']:
                    existing['hostname'] = device['hostname']
                if device['vendor'] and not existing.get('vendor'):
                    existing['vendor'] = device['vendor']
                if device.get('device_type'):
                    existing['device_type'] = device['device_type']
                if device.get('open_ports'):
                    existing['open_ports'] = device['open_ports']
                updated_count += 1
            db['devices'][key]['_seen_this_scan'] = True

    # Backfill vendor for existing devices that have MAC but no vendor
    for key, dev in db['devices'].items():
        if dev.get('mac') and not dev.get('vendor'):
            v = lookup_vendor(dev['mac'])
            if v:
                dev['vendor'] = v

    db['last_scan'] = now
    save_db(db)

    if not quiet:
        total = len([d for d in db['devices'].values() if d.get('_seen_this_scan')])
        print(f"\n✅ Scan complete — {total} devices online, {new_count} new")
        if new_count > 0:
            print("\n🆕 New devices:")
            for dev in db['devices'].values():
                if dev.get('_seen_this_scan') and dev['first_seen'] == now:
                    _print_device(dev)

    return db


def _print_device(dev, show_times=False):
    """Print a single device row."""
    label = dev.get('label')
    hostname = dev.get('hostname') or ''
    vendor = dev.get('vendor') or ''
    mac = dev.get('mac') or ''
    ip = dev.get('ip') or ''
    device_type = dev.get('device_type') or ''

    name = label or hostname or '(unknown)'
    extra = []
    if vendor:
        extra.append(vendor)
    if device_type:
        extra.append(f'[{device_type}]')
    if mac and not vendor:
        extra.append(mac)
    elif mac and vendor:
        extra.append(mac)
    extra_str = '  '.join(extra)

    line = f"  {ip:<18} {name:<35} {extra_str}"
    print(line)

    if show_times:
        first = dev.get('first_seen', '')[:16].replace('T', ' ')
        last = dev.get('last_seen', '')[:16].replace('T', ' ')
        print(f"    {'':18} first: {first}  last: {last}")


def list_devices(show_times=False, online_only=False):
    """List all known devices."""
    db = load_db()
    if not db['devices']:
        print("No devices in database. Run: netmap.py scan")
        return

    last_scan = db.get('last_scan', 'never')[:16].replace('T', ' ') if db.get('last_scan') else 'never'
    print(f"📡 Network devices  (last scan: {last_scan})\n")
    print(f"  {'IP':<18} {'Name/Hostname':<35} Vendor / MAC")
    print(f"  {'-'*18} {'-'*35} {'-'*30}")

    devices = list(db['devices'].values())
    devices.sort(key=lambda d: [int(x) for x in (d.get('ip') or '0.0.0.0').split('.')] if d.get('ip') else [0,0,0,0])

    for dev in devices:
        if online_only and not dev.get('_seen_this_scan'):
            continue
        _print_device(dev, show_times=show_times)


def find_device(query):
    """Search for a device by IP, hostname, MAC, vendor, or label."""
    db = load_db()
    query_lower = query.lower()
    results = []

    for dev in db['devices'].values():
        fields = [
            dev.get('ip') or '',
            dev.get('hostname') or '',
            dev.get('mac') or '',
            dev.get('vendor') or '',
            dev.get('label') or '',
            dev.get('device_type') or '',
        ]
        if any(query_lower in f.lower() for f in fields):
            results.append(dev)

    if not results:
        print(f"No devices matching '{query}'")
        return

    print(f"🔎 Results for '{query}':\n")
    for dev in results:
        _print_device(dev, show_times=True)


def show_new(minutes=60):
    """Show devices first seen within the last N minutes."""
    db = load_db()
    cutoff = (datetime.now() - timedelta(minutes=minutes)).isoformat()
    new_devs = [d for d in db['devices'].values() if d.get('first_seen', '') >= cutoff]

    if not new_devs:
        print(f"No new devices in the last {minutes} minutes.")
        return

    print(f"🆕 New devices (last {minutes} min):\n")
    for dev in new_devs:
        _print_device(dev, show_times=True)


def label_device(ip_or_mac, name):
    """Set a friendly label for a device."""
    db = load_db()
    for key, dev in db['devices'].items():
        if dev.get('ip') == ip_or_mac or (dev.get('mac') or '').upper() == ip_or_mac.upper():
            dev['label'] = name
            save_db(db)
            print(f"✅ Labeled {ip_or_mac} as '{name}'")
            return
    print(f"Device not found: {ip_or_mac}")


def export_json():
    """Export device database as clean JSON."""
    db = load_db()
    clean = []
    for dev in db['devices'].values():
        d = {k: v for k, v in dev.items() if not k.startswith('_')}
        clean.append(d)
    print(json.dumps({'devices': clean, 'last_scan': db.get('last_scan')}, indent=2))


def watch(interval=120, subnet=None):
    """Continuous scan mode."""
    print(f"👁  Watch mode — scanning every {interval}s (Ctrl+C to stop)\n")
    while True:
        scan(subnet=subnet, quiet=False)
        print(f"\n  Next scan in {interval}s...")
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description='netmap — network device scanner')
    subparsers = parser.add_subparsers(dest='command')

    scan_p = subparsers.add_parser('scan')
    scan_p.add_argument('--subnet', help='Override subnet (e.g. 10.0.0.0/24)')
    scan_p.add_argument('--deep', action='store_true', help='Port scan each device to fingerprint type (slower)')
    subparsers.add_parser('list').add_argument('--times', action='store_true', help='Show first/last seen times')

    find_p = subparsers.add_parser('find')
    find_p.add_argument('query', help='Search term (IP, hostname, MAC, vendor)')

    new_p = subparsers.add_parser('new')
    new_p.add_argument('--minutes', type=int, default=60)

    label_p = subparsers.add_parser('label')
    label_p.add_argument('device', help='IP or MAC address')
    label_p.add_argument('name', help='Friendly label')

    subparsers.add_parser('export')

    watch_p = subparsers.add_parser('watch')
    watch_p.add_argument('--interval', type=int, default=120)
    watch_p.add_argument('--subnet')

    args = parser.parse_args()

    if args.command == 'scan':
        scan(subnet=getattr(args, 'subnet', None), deep=getattr(args, 'deep', False))
    elif args.command == 'list':
        list_devices(show_times=getattr(args, 'times', False))
    elif args.command == 'find':
        find_device(args.query)
    elif args.command == 'new':
        show_new(minutes=args.minutes)
    elif args.command == 'label':
        label_device(args.device, args.name)
    elif args.command == 'export':
        export_json()
    elif args.command == 'watch':
        watch(interval=args.interval, subnet=getattr(args, 'subnet', None))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
