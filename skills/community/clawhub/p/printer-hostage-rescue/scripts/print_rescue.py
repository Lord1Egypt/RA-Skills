#!/usr/bin/env python3
"""print_rescue.py — printer failure-class diagnosis, spooler clearing, and
driverless-IPP discovery/test. Stdlib only.

Subcommands:
  diagnose --symptom "text"       classify failure + fix path
  spooler [--fix]                 show/clear wedged print queues (CUPS/local)
  discover [--subnet 192.168.1.0/24]
                                  scan for printers: TCP 631/9100/80/443,
                                  mDNS browse, driverless-IPP test page
  economics --pages 80            inkjet vs laser page-cost comparison
"""
import argparse
import socket
import struct
import subprocess
import sys

CLASSES = [
    ("ink-low-block", ["ink low", "ink empty", "low ink", "cartridge empty",
                        "replace cartridge", "ink depleted", "toner low"],
     "Chip estimate, not measurement. Override ink monitoring (Settings→Supplies), "
     "judge by print quality. Keep one spare; don't panic-replace on the chip."),
    ("non-genuine", ["non-genuine", "non-original", "counterfeit", "used cartridge",
                      "cartridge error 0x", "unsupported cartridge", "ink cannot be"],
     "Cartridge DRM. Check firmware version against blocking updates; use "
     "accept-and-warn menu; EU/UK consumer-law lever; vendor downgrade path."),
    ("contact", ["cartridge error", "blinking", "led error", "no cartridge",
                  "not detected"],
     "Electrical contact failure. Reseat, isopropyl on contacts, remove shipping "
     "tape, isolate by swapping carts. Clean the printer-side contacts too."),
    ("region", ["region", "regional", "wrong region", "installed wrong"],
     "Regionalization DRM after moving countries. Free vendor reset with proof of "
     "local cartridge purchase; support chat flow per vendor."),
    ("spooler", ["stuck", "queue", "printing forever", "not responding",
                  "offline", "pending", "documents in queue"],
     "Wedged spooler (half of 'dead' printers). Cancel all jobs, restart spooler "
     "service; test from a second device before blaming hardware. Run: spooler --fix"),
    ("blank", ["blank pages", "blank", "faded", "stripes", "white lines",
                "missing color", "nozzle"],
     "Clogged nozzles / air in head. Max 2-3 cleaning cycles, then 8h pause; nozzle "
     "check between cycles; persistent single-color absence = cart valve or head."),
    ("network", ["wifi", "wi-fi", "cannot find", "not found", "airprint",
                  "discovery", "cannot connect", "ip changed"],
     "mDNS/discovery broken or AP isolation. Set DHCP reservation; use IP-based "
     "driverless IPP (port 631); skip vendor drivers entirely. Run: discover"),
    ("driver", ["driver", "install", "cd", "setup", "windows 11", "no printer"],
     "Skip vendor software: IPP Everywhere/AirPrint/Mopria is built into Win10+, "
     "macOS, Linux CUPS, iOS, Android. Add queue as ipp://<ip>/ipp/print."),
    ("subscription", ["instant ink", "subscription", "card declined", "billing",
                       "enrollment"],
     "Subscription hostage (cartridges are leased). Cancel via vendor flow so the "
     "printer exits grace cleanly; then use retail cartridges."),
    ("jam", ["jam", "paper jam", "jammed", "paper error", "misfeed"],
     "Ghost jam: fragment deep in path or knocked sensor flag. Rear door, duplexer "
     "reseat, cardstock strip through the path, flashlight on actuator flags."),
    ("quality", ["ghosting", "smudge", "repeat", "streak", "spots", "gray background"],
     "Drum/fuser wear or toner spill (laser). Measure repeat distance: drum ~75mm, "
     "fuser larger. Replace DRUM unit not toner for ghosting."),
]


def cmd_diagnose(args):
    s = args.symptom.lower()
    scored = []
    for name, keys, fix in CLASSES:
        score = sum(1 for k in keys if k in s)
        if score:
            scored.append((score, name, fix))
    if not scored:
        print("No direct class match. Classes:")
        for name, keys, _ in CLASSES:
            print(f"  {name:<14} e.g. {keys[0]!r}")
        return
    scored.sort(reverse=True)
    for sc, name, fix in scored[:3]:
        print(f"[{name}] (match {sc})\n  {fix}\n")


def cmd_spooler(args):
    import shutil
    if shutil.which("lpstat"):
        r = subprocess.run(["lpstat", "-W", "all", "-o"], capture_output=True, text=True)
        jobs = [l for l in (r.stdout or "").splitlines() if l.strip()]
        print(f"CUPS jobs: {len(jobs)}")
        for j in jobs[:10]:
            print("  " + j)
        if args.fix and jobs:
            subprocess.run(["cancel", "-a"], capture_output=True)
            print("→ cancel -a sent; remaining:")
            r2 = subprocess.run(["lpstat", "-o"], capture_output=True, text=True)
            print(r2.stdout or "  (none — queue clear)")
    else:
        print("No CUPS lpstat. Windows: net stop spooler && del /Q "
              "%SYSTEMROOT%\\System32\\spool\\PRINTERS\\*.* && net start spooler")
        print("macOS: cancel -a - ; sudo launchctl kickstart -k system/org.cups.cupsd")


def probe(ip, port, timeout=0.6):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except OSError:
        return False


def mdns_browse():
    """Parse printers from Avahi output if present (no C extension needed)."""
    import shutil
    if not shutil.which("avahi-browse"):
        return []
    r = subprocess.run(["avahi-browse", "-rt", "_ipp._tcp"], capture_output=True,
                       text=True, timeout=8)
    found = []
    for line in (r.stdout or "").splitlines():
        if line.startswith("="):
            parts = [p.strip() for p in line.split(";")]
            if len(parts) >= 8:
                found.append((parts[3], parts[7]))  # name, ip
    return found


def ipp_test_page(ip):
    """IPP Get-Printer-Attributes wrapped in HTTP POST (IPP standard transport).
    No external deps — hand-rolled HTTP/1.1 request over TCP 631."""
    ipp = b"\x02\x00"            # IPP 2.0
    ipp += b"\x00\x0b"           # operation: Get-Printer-Attributes
    ipp += b"\x00\x00\x00\x01"   # request-id 1 (4 bytes)
    ipp += b"\x01"               # operation-attributes-tag
    ipp += b"\x47" + b"\x00\x12" + b"attributes-charset"
    ipp += b"\x00\x05" + b"utf-8"
    ipp += b"\x48" + b"\x00\x1b" + b"attributes-natural-language"
    ipp += b"\x00\x02" + b"en"
    ipp += b"\x45" + b"\x00\x0b" + b"printer-uri"
    uri = f"ipp://{ip}/ipp/print".encode()
    ipp += struct.pack(">H", len(uri)) + uri
    ipp += b"\x03"               # end-of-attributes-tag
    req = (f"POST /ipp/print HTTP/1.1\r\nHost: {ip}:631\r\n"
           "Content-Type: application/ipp\r\n"
           f"Content-Length: {len(ipp)}\r\nConnection: close\r\n\r\n").encode() + ipp
    try:
        with socket.create_connection((ip, 631), timeout=6) as s:
            s.settimeout(6)
            s.sendall(req)
            chunks = b""
            while len(chunks) < 65536:
                d = s.recv(4096)
                if not d:
                    break
                chunks += d
        head, _, body = chunks.partition(b"\r\n\r\n")
        status_line = head.split(b"\r\n", 1)[0].decode("latin1", "replace")
        if body[:1] in (b"\x01", b"\x02"):
            ver = f"{body[0]}.{body[1]}"
            ipp_status = (body[2] << 8) | body[3] if len(body) >= 4 else -1
            return f"IPP ALIVE: HTTP '{status_line}', IPP {ver}, status 0x{ipp_status:04x}, {len(body)}B body"
        return f"port 631 responded: '{status_line}' (body {len(body)}B, not IPP)"
    except OSError as e:
        return f"IPP probe failed: {e}"


def cmd_discover(args):
    subnet = args.subnet or "192.168.1.0/24"
    base = subnet.rsplit(".", 1)[0]
    print(f"Scanning {base}.1-254 ports 631/9100/80 …")
    hits = []
    import concurrent.futures as cf
    def check(i):
        ip = f"{base}.{i}"
        open_ports = [p for p in (631, 9100, 80, 443) if probe(ip, p)]
        return (ip, open_ports) if open_ports else None
    with cf.ThreadPoolExecutor(max_workers=64) as ex:
        for res in ex.map(check, range(1, 255)):
            if res:
                hits.append(res)
                ip, ports = res
                tags = []
                if 631 in ports:
                    tags.append("IPP/driverless-likely")
                if 9100 in ports:
                    tags.append("raw-JetDirect")
                if 80 in ports or 443 in ports:
                    tags.append("web-admin")
                print(f"  {ip:<16} {ports}  {' + '.join(tags)}")
    if not hits:
        print("  none found — check subnet or printer is on the network")
    for ip, ports in hits:
        if 631 in ports:
            print(f"{ip}: {ipp_test_page(ip)}")
    try:
        for name, ip in mdns_browse():
            print(f"mDNS: {name} @ {ip}")
    except Exception:
        pass
    if hits:
        ipp_hits = [ip for ip, ports in hits if 631 in ports]
        ip = ipp_hits[0] if ipp_hits else hits[0][0]
        print(f"\nAdd driverless queue for {ip}:")
        print(f"  Linux/mac: lpadmin -p rescue -E -v ipp://{ip}/ipp/print -m everywhere")
        print(f"  Windows:   Settings→Printers→Add→ '{ip}' appears via IPP")
        print(f"  Test:      lp -d rescue /etc/hostname  (or any small text file)")


def cmd_economics(args):
    pages = args.pages
    months = 12
    ink_cost = pages * months * 0.16      # inkjet color blended, incl cleaning waste
    laser_cost = 130 + pages * months * 0.03
    print(f"At {pages} pages/mo:")
    print(f"  inkjet:   ${ink_cost:,.0f}/yr (consumables only, ~$0.16/page)")
    print(f"  mono laser: ${laser_cost:,.0f}/yr first year incl. $130 device (~$0.03/page)")
    crossover = 130 / (0.16 - 0.03) / 12
    print(f"  inkjet is cheaper only under {crossover:.0f} pages/mo")


def main():
    p = argparse.ArgumentParser(description="Printer hostage rescue toolkit.")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("diagnose"); d.add_argument("--symptom", required=True)
    s = sub.add_parser("spooler"); s.add_argument("--fix", action="store_true")
    c = sub.add_parser("discover"); c.add_argument("--subnet")
    e = sub.add_parser("economics"); e.add_argument("--pages", type=int, default=80)
    a = p.parse_args()
    {"diagnose": cmd_diagnose, "spooler": cmd_spooler,
     "discover": cmd_discover, "economics": cmd_economics}[a.cmd](a)


if __name__ == "__main__":
    main()
