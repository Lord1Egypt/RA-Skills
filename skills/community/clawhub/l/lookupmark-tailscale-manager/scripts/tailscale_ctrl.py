#!/usr/bin/env python3
"""Secure Tailscale network manager.

Whitelisted commands only. Blocks destructive/unauthorized operations.
Masks public IPs in FINAL output only (after JSON parsing).

Usage:
    tailscale_ctrl.py status          # Network overview
    tailscale_ctrl.py devices         # Connected devices
    tailscale_ctrl.py ip              # This device's Tailscale IPs
    tailscale_ctrl.py ping <host>     # Ping a tailnet device
    tailscale_ctrl.py netcheck        # Network diagnostics
    tailscale_ctrl.py serve-status    # Current serve/funnel config
    tailscale_ctrl.py whois <ip>      # Who is this IP
"""

import argparse
import json
import re
import subprocess
import sys

# Only these subcommands are allowed
READ_COMMANDS = {"status", "ip", "ping", "netcheck", "whois", "serve-status"}

# Public IP patterns (applied ONLY to final text output, never to raw JSON)
PUBLIC_IPV4_RE = re.compile(
    r'\b(?!(100\.|10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.|127\.|::1|fe80:))'
    r'(?:\d{1,3}\.){3}\d{1,3}\b'
)


def mask_public_ips(text: str) -> str:
    """Replace public IPs (v4 and v6) in text output. NOT applied to raw JSON."""
    text = PUBLIC_IPV4_RE.sub("[IP-MASKED]", text)
    # IPv6: mask addresses that aren't link-local, loopback, or Tailscale (fd7a:)
    # Handles full, abbreviated (e.g. ::1, fe80::1%eth0), and mixed formats
    text = re.sub(
        r'(?<![0-9a-fA-F:])(?!(?:fd7a|fe80|::1[:/%]?))(?:[0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}(?:%\w+)?',
        '[IP-MASKED]', text
    )
    return text


def run_tailscale_raw(args: list[str], timeout: int = 15) -> dict:
    """Execute a tailscale command and return raw stdout/stderr (NO masking)."""
    cmd = ["tailscale"] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out ({timeout}s)"}
    except FileNotFoundError:
        return {"error": "tailscale not found in PATH — install tailscale first"}
    except Exception as e:
        return {"error": str(e)}


def get_status():
    """Get tailnet status (raw text)."""
    return run_tailscale_raw(["status"])


def get_status_json():
    """Get detailed status as structured data. Parse JSON FIRST, then mask."""
    result = run_tailscale_raw(["status", "--json"])
    if "error" in result:
        return result
    try:
        data = json.loads(result["stdout"])
        # Extract key info — Tailscale IPs are safe to show (100.x.x.x)
        summary = {
            "self": {
                "name": data.get("Self", {}).get("DNSName", "?"),
                "online": data.get("Self", {}).get("Online", False),
                "tailscale_ips": data.get("Self", {}).get("TailscaleIPs", []),
            },
            "peers": [],
        }
        for peer_id, peer in data.get("Peer", {}).items():
            summary["peers"].append({
                "name": peer.get("DNSName", peer.get("HostName", "?")),
                "online": peer.get("Online", False),
                "ips": peer.get("TailscaleIPs", []),
                "os": peer.get("OS", "?"),
                "last_seen": peer.get("LastSeen", "?"),
            })
        return summary
    except json.JSONDecodeError:
        return {"raw": result["stdout"]}


def get_ip():
    """Get Tailscale IPs."""
    return run_tailscale_raw(["ip"])


def ping_host(host: str):
    """Ping a tailnet host."""
    return run_tailscale_raw(["ping", "-c", "3", host], timeout=20)


def netcheck():
    """Run network diagnostics."""
    return run_tailscale_raw(["netcheck"], timeout=30)


def serve_status():
    """Show current serve config."""
    return run_tailscale_raw(["serve", "status"])


def whois(ip_or_name: str):
    """Look up who an IP/name belongs to."""
    return run_tailscale_raw(["whois", ip_or_name])


def mask_output(data: dict) -> dict:
    """Apply IP masking to the FINAL output (text only, not structured data)."""
    if "stdout" in data:
        data["stdout"] = mask_public_ips(data["stdout"])
    if "stderr" in data:
        data["stderr"] = mask_public_ips(data["stderr"])
    return data


def format_output(data):
    """Format for human-readable output. Mask IPs only at display time."""
    if isinstance(data, dict):
        if "error" in data:
            return f"❌ {data['error']}"
        if "stdout" in data:
            text = mask_public_ips(data["stdout"])  # Mask only for display
            return text or data.get("stderr", "(empty)")
        if "self" in data:
            lines = []
            s = data["self"]
            lines.append(f"📍 This device: {s['name']} ({'online' if s['online'] else 'offline'})")
            lines.append(f"   IPs: {', '.join(s.get('tailscale_ips', []))}")
            if data.get("peers"):
                lines.append(f"\n👥 Peers ({len(data['peers'])}):")
                for p in data["peers"]:
                    status = "🟢" if p["online"] else "🔴"
                    lines.append(f"  {status} {p['name']} ({p.get('os', '?')}) — {', '.join(p.get('ips', []))}")
            return "\n".join(lines)
        return json.dumps(data, indent=2)
    return str(data)


def main():
    parser = argparse.ArgumentParser(description="Secure Tailscale manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status")
    sub.add_parser("devices")
    sub.add_parser("ip")
    sub.add_parser("netcheck")
    sub.add_parser("serve-status")

    p_ping = sub.add_parser("ping")
    p_ping.add_argument("host")

    p_whois = sub.add_parser("whois")
    p_whois.add_argument("target")

    parser.add_argument("--json", action="store_true", help="JSON output")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "status":
        data = get_status_json() if args.json else get_status()
    elif args.command == "devices":
        data = get_status_json()
    elif args.command == "ip":
        data = get_ip()
    elif args.command == "ping":
        data = ping_host(args.host)
    elif args.command == "netcheck":
        data = netcheck()
    elif args.command == "serve-status":
        data = serve_status()
    elif args.command == "whois":
        data = whois(args.target)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        # JSON output: apply IP masking to the full JSON string
        output = json.dumps(data, indent=2, default=str)
        print(mask_public_ips(output))
    else:
        print(format_output(data))


if __name__ == "__main__":
    main()
