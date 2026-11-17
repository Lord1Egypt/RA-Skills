#!/usr/bin/env python3
"""Home router security audit for civilians: hardening checklist with
brand-family pointers, stdlib-only local device inventory (ARP + ping
sweep), admin-page dictionary, and a baseline record.

Read-only on your network: it never changes router settings.

Examples:
  python3 router_audit.py --checklist --brand asus
  python3 router_audit.py --inventory
  python3 router_audit.py --inventory --subnet 192.168.1.0/24 --pings 8
  python3 router_audit.py --dict
  python3 router_audit.py --baseline --model "RT-AX3000" --fw "3.0.0.4.388"
"""
import argparse
import json
import os
import platform
import re
import subprocess
import sys
from datetime import datetime

CHECKLIST = [
    ("Firmware", "Update FIRST (updates can reset settings). Vendor support page or admin UI 'Firmware Update'."),
    ("Admin password", "The ROUTER's login, not Wi-Fi. Unique + password manager. Factory admin/admin is the #1 real-world hole."),
    ("Wi-Fi encryption", "WPA3 if all devices support it; WPA2/WPA3 transitional meanwhile; WPA2-AES floor. Never WEP, never TKIP/mixed."),
    ("WPS", "OFF. Push-button pairing with a crackable PIN protocol, default-on, rarely missed."),
    ("Remote management", "OFF (a.k.a. 'Web Access from WAN' / 'Remote Admin'). If you use the vendor cloud app, harden THAT account instead (password + MFA)."),
    ("UPnP", "OFF. Any LAN malware can otherwise open inbound ports on your perimeter. Forward specific ports manually when needed."),
    ("Guest network", "ON for IoT + visitors, 'allow access to local network' OFF. Puts the weakest devices on their own island."),
    ("DNS", "Note what the router hands out; consider malware-filtering resolvers (Quad9 9.9.9.9, Cloudflare 1.1.1.1) over ISP default."),
    ("Admin over Wi-Fi", "If the router can restrict admin access to wired clients, enable it."),
    ("Services", "Telnet OFF always; SSH off unless you use it; 'DNS rebind protection' ON."),
]

BRANDS = {
    "asus": ("router.asus.com or 192.168.50.1", [
        "Wireless > General: encryption + WPS toggle",
        "Administration > System: admin password, 'Enable Web Access from WAN' = No",
        "WAN > Virtual Server: manual port forwards (replaces UPnP)",
        "Network Map > Clients: built-in inventory",
        "AiCloud / remote apps: disable unless used, then lock the ASUS account",
    ]),
    "tp-link": ("tplinkwifi.net / tplogin.cn or 192.168.0.1", [
        "Wireless > Wireless Security: WPA2/WPA3 + WPS disable",
        "System Tools > Password: admin password",
        "Security > Remote Management: disable",
        "Forwarding > UPnP: disable; use Virtual Servers for forwards",
        "TP-Link cloud/app: if bound, lock the TP-Link ID account",
    ]),
    "netgear": ("routerlogin.net or 192.168.1.1", [
        "Wireless Settings: WPA2/WPA3",
        "Advanced Wireless Settings: WPS = disabled",
        "Advanced > Remote Management: off",
        "Advanced > Setup > WAN Setup: disable 'Respond to Ping on Internet Port'",
        "NETGEAR armor/app: skip upsells; firmware at Router Update",
    ]),
    "dlink": ("192.168.0.1", [
        "Wireless > Wireless Security",
        "System > Admin password",
        "Tools > Admin: remote management off",
        "Advanced > Firewall: keep on",
    ]),
    "eero": ("app-managed", [
        "Settings > Advanced: WPA3 toggle",
        "No admin password page - the AMAZON account is the admin: strong password + MFA there",
        "Guest network via app; eero 'Band Steering' etc. are performance, not security",
    ]),
    "google-nest": ("app-managed (Google Home)", [
        "Wi-Fi settings: WPA3 transition toggle",
        "Admin = your Google account: password + 2FA there",
        "Guest network in app; disable 'cloud services' you don't use",
    ]),
    "other": ("see the router's label or manual (common: 192.168.0.1 / 192.168.1.1)", [
        "Find: wireless/security page, administration/system page, WAN/remote page",
        "The checklist order still applies; wording drifts by vendor",
    ]),
}

DICTIONARY = [
    ("WPS", "Wi-Fi Protected Setup - push-button/PIN pairing. PIN mode is crackable on many models. Turn OFF."),
    ("UPnP / NAT-PMP", "Lets LAN devices open inbound ports automatically = malware's best friend. OFF; forward manually."),
    ("Remote management / Web Access from WAN", "Admin page reachable from the internet. OFF unless you truly administer remotely."),
    ("DNS rebind protection", "Blocks DNS answers that name your router's internal IP. Keep ON."),
    ("Telnet / SSH", "Command-line access to the router. Telnet: always OFF. SSH: off unless you use it."),
    ("IGMP snooping", "Multicast optimization for TV boxes. Not security; leave default."),
    ("mDNS / Bonjour", "Local device discovery (printers, Chromecast). Fine on LAN; never forward to WAN."),
    ("MAC filtering", "Allow-list of device hardware IDs. Spoofable in seconds - inventory aid, not a lock."),
    ("Hidden SSID", "Doesn't hide from attackers (probe requests leak it); complicates your own devices. Skip."),
    ("DMZ host", "Forwards ALL inbound ports to one machine. Almost never justified; use specific forwards."),
    ("Guest network isolation", "Guests/IoT can reach the internet but not your laptops. The point of guest networks."),
    ("WPA2/WPA3 transitional (mixed)", "Accepts both during upgrade. Fine as a phase; end at WPA3-only if hardware allows."),
    ("SPI / NAT firewall", "Stateful packet inspection - the basic inbound blocker. Keep ON."),
    ("Ping from WAN / Respond to ICMP", "Makes your router visible to internet scanners. Disable."),
]

AUDIT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "router_baseline.json")


def cmd_checklist(args):
    print("=" * 66)
    print("HOME ROUTER HARDENING PASS - do these in order")
    print("=" * 66)
    for i, (item, how) in enumerate(CHECKLIST, 1):
        print(f"\n {i:2d}. {item.upper()}")
        for s in how.split(". "):
            s = s.strip()
            print(f"     {s}." if not s.endswith(".") else f"     {s}")
    url, hints = BRANDS.get(args.brand or "other", BRANDS["other"])
    print("\n" + "=" * 66)
    print(f"BRAND POINTERS - {args.brand or 'other'}: admin at {url}")
    print("=" * 66)
    for h in hints:
        print(f"  - {h}")
    print("\nAfter each change: rejoin Wi-Fi/wire and confirm the setting stuck,")
    print("then confirm your devices still work before the next change.")


def local_subnet():
    """Best-effort local subnet guess from the host's IP config."""
    # 1. pure-stdlib: UDP connect trick (no packets sent, just routing table)
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            if not ip.startswith("127."):
                return ip.rsplit(".", 1)[0]
        finally:
            s.close()
    except Exception:
        pass
    # 2. hostname -I style via gethostname resolution
    try:
        import socket
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if not ip.startswith("127."):
                return ip.rsplit(".", 1)[0]
    except Exception:
        pass
    # 3. platform commands
    if platform.system() == "Windows":
        out = subprocess.run(["ipconfig"], capture_output=True, text=True).stdout
        m = re.search(r"IPv4[^\d]+(\d+\.\d+\.\d+)\.\d+", out)
        return m.group(1) if m else "192.168.1"
    for cmd in (["ip", "-4", "route", "get", "8.8.8.8"], ["ifconfig"]):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True).stdout or ""
            m = re.search(r"src (\d+\.\d+\.\d+\.\d+)", out)
            if m:
                return m.group(1).rsplit(".", 1)[0]
            m = re.search(r"inet (\d+\.\d+\.\d+\.\d+)", out)
            if m and not m.group(1).startswith("127."):
                return m.group(1).rsplit(".", 1)[0]
        except Exception:
            continue
    return "192.168.1"


def arp_table():
    """Return list of (ip, mac) from the system ARP table, cross-platform."""
    rows = []
    # Linux: /proc/net/arp is always there, no external command needed
    if os.path.exists("/proc/net/arp"):
        with open("/proc/net/arp") as f:
            for line in f.readlines()[1:]:
                parts = line.split()
                if len(parts) >= 4 and parts[2].lower() == "0x2":
                    rows.append((parts[0], parts[3].lower()))
        if rows:
            return rows
    if platform.system() == "Windows":
        out = subprocess.run(["arp", "-a"], capture_output=True, text=True).stdout
        for line in out.splitlines():
            m = re.match(r"\s*(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})", line)
            if m:
                rows.append((m.group(1), m.group(2).replace("-", ":").lower()))
    else:
        try:
            out = subprocess.run(["arp", "-an"], capture_output=True, text=True).stdout
            for line in out.splitlines():
                m = re.search(r"\((\d+\.\d+\.\d+\.\d+)\) at ([0-9a-f:]{17})", line)
                if m:
                    rows.append((m.group(1), m.group(2).lower()))
        except Exception:
            pass
    return rows


def ping(host, count=1, timeout_s=1):
    flag = "-n" if platform.system() == "Windows" else "-c"
    to = "-w" if platform.system() == "Windows" else "-W"
    to_ms = str(int(timeout_s * 1000)) if platform.system() == "Windows" else str(int(timeout_s))
    try:
        r = subprocess.run(
            ["ping", flag, str(count), to, to_ms, host],
            capture_output=True, text=True, timeout=timeout_s + 2,
        )
        return r.returncode == 0
    except Exception:
        return False


def resolve_name(ip):
    try:
        out = subprocess.run(
            ["ping", "-a" if platform.system() == "Windows" else "-c", "1",
             ip] if platform.system() == "Windows" else ["getent", "hosts", ip],
            capture_output=True, text=True, timeout=2,
        )
        if platform.system() == "Windows":
            m = re.search(r"Pinging (\S+)\[", out.stdout)
            if m:
                return m.group(1)
        else:
            for tok in (out.stdout or "").split():
                if not re.match(r"^\d+\.\d+\.\d+\.\d+$", tok) and "." in tok:
                    return tok.split()[0]
    except Exception:
        pass
    return ""


def cmd_inventory(args):
    subnet = args.subnet.rsplit(".", 1)[0] if args.subnet else local_subnet()
    if "/" in subnet:
        subnet = subnet.split("/")[0].rsplit(".", 1)[0]
    print("=" * 66)
    print(f"LOCAL DEVICE INVENTORY - subnet {subnet}.0/24 (read-only)")
    print("=" * 66)
    print("Reading ARP table...")
    devices = dict(arp_table())
    print(f"{len([ip for ip in devices if ip.startswith(subnet)])} cached entries on this subnet.")
    if args.ping_sweep:
        print(f"Ping-sweeping {args.pings} addresses to populate ARP (may take ~{args.pings * 1}s)...")
        for i in range(1, args.pings + 1):
            ping(f"{subnet}.{i}")
        # also common static ranges
        for i in (100, 101, 200, 250, 254):
            ping(f"{subnet}.{i}")
        devices = dict(arp_table())
    known = [ip for ip, _ in devices.items() if ip.startswith(subnet)]
    print(f"\n{'IP':16s} {'MAC':19s} NAME")
    print("-" * 66)
    for ip in sorted(known, key=lambda s: tuple(map(int, s.split(".")))):
        mac = devices[ip]
        name = resolve_name(ip) or "-"
        print(f"{ip:16s} {mac:19s} {name}")
    print("-" * 66)
    print(f"{len(known)} devices responded on {subnet}.0/24")
    print("""
Verdicts:
  KNOWN      - matches your mental list of phones/laptops/TVs/printers
  CHECK      - unnamed or dormant: identify it (unplug candidates one by one)
  INVESTIGATE- active device you cannot account for:
               change Wi-Fi password, check router admin clients page,
               review WPS/guest settings. Unknown clients are the visible
               symptom of freeloaders OR compromise.
TIP: many IoT devices have generic names; their MAC vendor prefix
     (first 3 octets) identifies the maker - search it online.""")


def cmd_dict(_args):
    print("ROUTER-SPEAK DICTIONARY (what the admin page actually means)")
    print("=" * 66)
    for term, meaning in DICTIONARY:
        print(f"\n  {term}")
        print(f"    {meaning}")


def cmd_baseline(args):
    data = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "model": args.model or "?",
        "firmware": args.fw or "?",
        "settings_changed": CHECKLIST and [c[0] for c in CHECKLIST],
        "notes": args.notes or "",
    }
    with open(AUDIT_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")
    print(f"Baseline saved to {AUDIT_FILE}:")
    print(json.dumps(data, indent=2))
    print("\nNext audit: compare firmware version + confirm every item still set.")


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("--checklist", action="store_true", help="hardening checklist (main output)")
    ap.add_argument("--brand", choices=BRANDS, help="brand-family admin-page pointers")
    ap.add_argument("--inventory", action="store_true", help="local subnet device inventory")
    ap.add_argument("--subnet", help="e.g. 192.168.1.0/24 (default: auto-detect)")
    ap.add_argument("--ping-sweep", action="store_true", help="populate ARP with a ping sweep (slower, fuller)")
    ap.add_argument("--pings", type=int, default=25, help="addresses to sweep (default 25)")
    ap.add_argument("--dict", action="store_true", help="admin-page dictionary")
    ap.add_argument("--baseline", action="store_true", help="record model/firmware baseline")
    ap.add_argument("--model"), ap.add_argument("--fw"), ap.add_argument("--notes")
    args = ap.parse_args()
    if not any([args.checklist, args.inventory, args.dict, args.baseline]):
        args.checklist = True
    if args.checklist:
        cmd_checklist(args)
    if args.inventory:
        cmd_inventory(args)
    if args.dict:
        cmd_dict(args)
    if args.baseline:
        cmd_baseline(args)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
