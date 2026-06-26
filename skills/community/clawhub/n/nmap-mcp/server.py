#!/usr/bin/env python3
"""
nmap-mcp — Network Scanning MCP Server
Wraps nmap with structured output, scope enforcement, and audit logging.

All MCP protocol output → stdout
All logs/debug → stderr
"""
from __future__ import annotations

import json
import logging
import os
import re
import socket
import subprocess
import sys
import ipaddress
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import nmap
import yaml

try:
    from fastmcp import FastMCP
except ImportError:
    print("ERROR: fastmcp not installed. Run: pip3 install --break-system-packages fastmcp", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CONFIG_PATH = Path(os.environ.get("NMAP_CONFIG", Path(__file__).parent / "config.yaml"))

def _load_config() -> dict:
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return yaml.safe_load(f) or {}
    return {}

CFG = _load_config()

ALLOWED_CIDRS: list[ipaddress.IPv4Network | ipaddress.IPv6Network] = [
    ipaddress.ip_network(c, strict=False)
    for c in CFG.get("allowed_cidrs", ["127.0.0.0/8"])
]
AUDIT_LOG = Path(CFG.get("audit_log", Path(__file__).parent / "audit.log"))
SCAN_DIR = Path(CFG.get("scan_dir", Path(__file__).parent / "scans"))
NMAP_BIN = CFG.get("nmap_bin", "/usr/bin/nmap")
TIMEOUTS = CFG.get("timeouts", {"quick": 120, "standard": 300, "deep": 600})

SCAN_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="nmap-mcp: %(message)s")
log = logging.getLogger("nmap-mcp")

def _audit(tool: str, target: str, args: dict, result: str, success: bool) -> None:
    """Append one line to the audit log."""
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "tool": tool,
        "target": target,
        "args": args,
        "success": success,
        "result_summary": result[:200],
    }
    try:
        with open(AUDIT_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        log.error("Audit log write failed: %s", e)

# ---------------------------------------------------------------------------
# Scope enforcement
# ---------------------------------------------------------------------------

def _in_scope(target: str) -> bool:
    """Return True if every address in target falls within an allowed CIDR."""
    if not ALLOWED_CIDRS:
        return True  # scope check disabled
    # Try as CIDR range first
    try:
        net = ipaddress.ip_network(target, strict=False)
        return any(net.subnet_of(allowed) or net == allowed for allowed in ALLOWED_CIDRS)
    except ValueError:
        pass
    # Try as plain IP
    try:
        addr = ipaddress.ip_address(target)
        return any(addr in allowed for allowed in ALLOWED_CIDRS)
    except ValueError:
        pass
    # Hostname — resolve to IPs and validate every resolved address.
    # Fail closed: if resolution fails or any IP is out of scope, reject.
    try:
        resolved = socket.getaddrinfo(target, None)
        addrs = {r[4][0] for r in resolved}
        if not addrs:
            log.warning("Scope check: hostname '%s' resolved to no addresses — rejecting", target)
            return False
        for raw in addrs:
            try:
                addr = ipaddress.ip_address(raw)
                if not any(addr in allowed for allowed in ALLOWED_CIDRS):
                    log.warning("Scope check: hostname '%s' resolves to out-of-scope IP %s", target, raw)
                    return False
            except ValueError:
                return False
        return True
    except socket.gaierror:
        log.warning("Scope check: hostname '%s' could not be resolved — rejecting", target)
        return False

def _require_scope(target: str, tool: str) -> None:
    """Validate target format and reject if out of scope."""
    _validate_target(target)
    if not _in_scope(target):
        _audit(tool, target, {}, "REJECTED: out of scope", False)
        raise ValueError(
            f"Target '{target}' is outside the allowed scan scope. "
            f"Allowed CIDRs: {[str(c) for c in ALLOWED_CIDRS]}"
        )

# ---------------------------------------------------------------------------
# Target validation
# ---------------------------------------------------------------------------

# Valid target patterns: IPv4, IPv4/CIDR, IPv6, simple hostname (no spaces or shell chars)
_TARGET_RE = re.compile(
    r'^('
    r'(\d{1,3}\.){3}\d{1,3}(/\d{1,2})?'        # IPv4 or IPv4/CIDR
    r'|[0-9a-fA-F:]+(/\d{1,3})?'               # IPv6 or IPv6/prefix
    r'|[a-zA-Z0-9]([a-zA-Z0-9\-\.]{0,253}[a-zA-Z0-9])?'  # hostname
    r')$'
)

def _validate_target(target: str) -> None:
    """Raise ValueError if target contains suspicious characters."""
    if not target or len(target) > 255:
        raise ValueError(f"Invalid target: must be 1-255 characters")
    if not _TARGET_RE.match(target):
        raise ValueError(
            f"Invalid target '{target}': must be an IP address, CIDR range, or hostname. "
            "No spaces or special characters allowed."
        )

# Nmap flags that take path arguments — never allow in custom_scan
_DANGEROUS_FLAGS = re.compile(
    r'(^|[\s])(--script(?!=-)|-oN|-oX|-oG|-oA|-oS|--datadir|'
    r'--servicedb|--versiondb|--resume|--stylesheet|--script-args)',
    re.IGNORECASE
)

# ---------------------------------------------------------------------------
# Scan execution helpers
# ---------------------------------------------------------------------------

def _run_nmap(args: list[str], timeout: int = 300) -> dict:
    """
    Run nmap with the given args. Returns:
      {"success": bool, "stdout": str, "stderr": str, "command": str}
    """
    cmd = [NMAP_BIN] + args
    log.info("Running: %s", " ".join(cmd))
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "success": r.returncode == 0,
            "stdout": r.stdout,
            "stderr": r.stderr,
            "command": " ".join(cmd),
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": f"Timed out after {timeout}s", "command": " ".join(cmd)}
    except FileNotFoundError:
        return {"success": False, "stdout": "", "stderr": f"nmap not found at {NMAP_BIN}", "command": " ".join(cmd)}

def _nmap_structured(target: str, extra_args: list[str], timeout: int = 300) -> dict:
    """
    Run nmap with -oX - to get XML output, parse it with python-nmap,
    return a structured dict.
    """
    nm = nmap.PortScanner()
    args_str = " ".join(extra_args)
    log.info("python-nmap scan: target=%s args=%s", target, args_str)
    try:
        nm.scan(hosts=target, arguments=args_str, timeout=timeout)
    except nmap.PortScannerError as e:
        return {"error": str(e), "hosts": {}}
    except Exception as e:
        return {"error": str(e), "hosts": {}}

    result: dict = {"command": nm.command_line(), "hosts": {}}
    for host in nm.all_hosts():
        h: dict = {
            "hostname": nm[host].hostname(),
            "state": nm[host].state(),
            "protocols": {},
            "os": [],
        }
        for proto in nm[host].all_protocols():
            h["protocols"][proto] = {}
            for port in sorted(nm[host][proto].keys()):
                pd = nm[host][proto][port]
                h["protocols"][proto][port] = {
                    "state": pd.get("state"),
                    "name": pd.get("name"),
                    "product": pd.get("product", ""),
                    "version": pd.get("version", ""),
                    "extrainfo": pd.get("extrainfo", ""),
                    "cpe": pd.get("cpe", ""),
                    "reason": pd.get("reason", ""),
                    "script": pd.get("script", {}),
                }
        # OS detection results
        if "osmatch" in nm[host]:
            for osm in nm[host]["osmatch"]:
                h["os"].append({
                    "name": osm.get("name"),
                    "accuracy": osm.get("accuracy"),
                    "osclass": [
                        {
                            "type": c.get("type"),
                            "vendor": c.get("vendor"),
                            "osfamily": c.get("osfamily"),
                            "osgen": c.get("osgen"),
                        }
                        for c in osm.get("osclass", [])
                    ],
                })
        result["hosts"][host] = h
    return result

def _save_scan(tool: str, target: str, result: dict) -> str:
    """Persist scan result to disk, return scan_id."""
    now = datetime.now(timezone.utc)
    scan_id = f"{now.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    record = {
        "scan_id": scan_id,
        "timestamp": now.isoformat(),
        "tool": tool,
        "target": target,
        "result": result,
    }
    path = SCAN_DIR / f"{scan_id}.json"
    with open(path, "w") as f:
        json.dump(record, f, indent=2)
    log.info("Scan saved: %s", path)
    return scan_id

# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP("nmap-mcp")

# --- Host Discovery ---------------------------------------------------------

@mcp.tool()
def nmap_ping_scan(target: str) -> str:
    """
    Discover live hosts via ICMP + TCP ping. No port scanning.
    Returns a list of hosts that are up with their hostnames.
    Use this first to find what's alive before deeper scanning.

    target: IP, hostname, or CIDR range (e.g. '192.168.1.0/24')
    """
    _require_scope(target, "nmap_ping_scan")
    result = _nmap_structured(target, ["-sn", "-T4"], timeout=TIMEOUTS["quick"])
    scan_id = _save_scan("nmap_ping_scan", target, result)

    hosts_up = [
        {"ip": ip, "hostname": data.get("hostname", ""), "state": data.get("state")}
        for ip, data in result.get("hosts", {}).items()
        if data.get("state") == "up"
    ]
    output = {"scan_id": scan_id, "target": target, "hosts_up": hosts_up, "count": len(hosts_up)}
    _audit("nmap_ping_scan", target, {}, f"{len(hosts_up)} hosts up", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_arp_discovery(target: str) -> str:
    """
    ARP-based host discovery — most reliable for local LAN segments.
    Only works when scanning subnets you're directly connected to.
    Returns IP, MAC address, and vendor for each live host.

    target: CIDR range or IP (e.g. '192.168.1.0/24')
    """
    _require_scope(target, "nmap_arp_discovery")
    # ARP discovery + privileged for raw socket access
    result = _nmap_structured(target, ["--privileged", "-sn", "-PR", "-T4"], timeout=TIMEOUTS["quick"])
    scan_id = _save_scan("nmap_arp_discovery", target, result)

    hosts = []
    for ip, data in result.get("hosts", {}).items():
        hosts.append({"ip": ip, "hostname": data.get("hostname", ""), "state": data.get("state")})

    output = {"scan_id": scan_id, "target": target, "hosts": hosts, "count": len(hosts)}
    _audit("nmap_arp_discovery", target, {}, f"{len(hosts)} hosts discovered", True)
    return json.dumps(output, indent=2)


# --- Port Scanning ----------------------------------------------------------

@mcp.tool()
def nmap_top_ports(target: str, count: int = 100) -> str:
    """
    Fast scan of the N most common ports using TCP connect (no root needed).
    Good first pass to find what's open before going deeper.

    target: IP, hostname, or CIDR range
    count: Number of top ports to scan (default 100, max 65535)
    """
    _require_scope(target, "nmap_top_ports")
    count = max(1, min(count, 65535))
    result = _nmap_structured(target, ["-sT", f"--top-ports={count}", "-T4", "--open"], timeout=TIMEOUTS["standard"])
    scan_id = _save_scan("nmap_top_ports", target, result)

    summary = _port_summary(result)
    output = {"scan_id": scan_id, "target": target, "top_ports_scanned": count, **summary}
    _audit("nmap_top_ports", target, {"count": count}, f"{summary['total_open']} open ports", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_syn_scan(target: str, ports: str = "1-1024") -> str:
    """
    SYN (half-open) scan — faster and stealthier than TCP connect.
    Requires cap_net_raw capability (already configured on this system).

    target: IP, hostname, or CIDR range
    ports: Port range, e.g. '22,80,443' or '1-65535' or 'common' (default '1-1024')
    """
    _require_scope(target, "nmap_syn_scan")
    port_arg = ports if ports != "common" else "--top-ports=1000"
    extra = ["--privileged", "-sS", "-T4", "--open"]
    if ports == "common":
        extra.append("--top-ports=1000")
    else:
        extra += ["-p", ports]

    result = _nmap_structured(target, extra, timeout=TIMEOUTS["standard"])
    scan_id = _save_scan("nmap_syn_scan", target, result)

    summary = _port_summary(result)
    output = {"scan_id": scan_id, "target": target, "ports_scanned": ports, **summary}
    _audit("nmap_syn_scan", target, {"ports": ports}, f"{summary['total_open']} open ports", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_tcp_scan(target: str, ports: str = "1-1024") -> str:
    """
    Full TCP connect scan — no special privileges needed.
    Slower than SYN but works everywhere and leaves full connection logs on target.

    target: IP, hostname, or CIDR range
    ports: Port range, e.g. '22,80,443' or '1-65535' (default '1-1024')
    """
    _require_scope(target, "nmap_tcp_scan")
    result = _nmap_structured(target, ["-sT", "-p", ports, "-T4", "--open"], timeout=TIMEOUTS["standard"])
    scan_id = _save_scan("nmap_tcp_scan", target, result)

    summary = _port_summary(result)
    output = {"scan_id": scan_id, "target": target, "ports_scanned": ports, **summary}
    _audit("nmap_tcp_scan", target, {"ports": ports}, f"{summary['total_open']} open ports", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_udp_scan(target: str, ports: str = "53,67,68,69,123,161,162,500,514,1900") -> str:
    """
    UDP port scan. Slow but finds services TCP scans miss (DNS, SNMP, TFTP, NTP, etc.).
    Requires cap_net_raw capability (already configured on this system).

    target: IP, hostname, or CIDR range
    ports: Port list or range (default: common UDP service ports)
    """
    _require_scope(target, "nmap_udp_scan")
    result = _nmap_structured(
        target,
        ["--privileged", "-sU", "-p", ports, "-T4"],
        timeout=TIMEOUTS["deep"]
    )
    scan_id = _save_scan("nmap_udp_scan", target, result)

    summary = _port_summary(result, proto="udp")
    output = {"scan_id": scan_id, "target": target, "ports_scanned": ports, **summary}
    _audit("nmap_udp_scan", target, {"ports": ports}, f"{summary['total_open']} open UDP ports", True)
    return json.dumps(output, indent=2)


# --- Service & OS Detection -------------------------------------------------

@mcp.tool()
def nmap_service_detection(target: str, ports: str = "common", intensity: int = 7) -> str:
    """
    Detect service names and versions on open ports (-sV).
    Returns per-port: service name, product, version, CPE identifier.

    target: IP, hostname, or CIDR range
    ports: Port range (default: top 1000 common ports)
    intensity: Version detection aggressiveness 0-9 (default 7)
    """
    _require_scope(target, "nmap_service_detection")
    intensity = max(0, min(9, intensity))
    port_args = ["--top-ports=1000"] if ports == "common" else ["-p", ports]
    extra = ["-sT", "-sV", f"--version-intensity={intensity}", "-T4"] + port_args

    result = _nmap_structured(target, extra, timeout=TIMEOUTS["standard"])
    scan_id = _save_scan("nmap_service_detection", target, result)

    summary = _port_summary(result)
    output = {"scan_id": scan_id, "target": target, "intensity": intensity, **summary}
    _audit("nmap_service_detection", target, {"ports": ports, "intensity": intensity}, f"{summary['total_open']} open", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_os_detection(target: str) -> str:
    """
    OS fingerprinting (-O). Identifies OS, version, and device type.
    Works best when the target has at least one open and one closed port.
    Requires cap_net_raw capability (already configured on this system).

    target: Single IP or hostname (OS detection doesn't work well on ranges)
    """
    _require_scope(target, "nmap_os_detection")
    result = _nmap_structured(
        target,
        ["--privileged", "-O", "--osscan-guess", "-T4"],
        timeout=TIMEOUTS["standard"]
    )
    scan_id = _save_scan("nmap_os_detection", target, result)

    os_results = {}
    for ip, data in result.get("hosts", {}).items():
        os_results[ip] = {
            "hostname": data.get("hostname", ""),
            "os_matches": data.get("os", []),
        }

    output = {"scan_id": scan_id, "target": target, "os_detection": os_results}
    _audit("nmap_os_detection", target, {}, f"{len(os_results)} hosts fingerprinted", True)
    return json.dumps(output, indent=2)


# --- NSE Scripts ------------------------------------------------------------

@mcp.tool()
def nmap_script_scan(target: str, scripts: str, ports: str = "common") -> str:
    """
    Run specific NSE (Nmap Scripting Engine) scripts against a target.
    Good for targeted checks: banner grabbing, SSL cert inspection, protocol probes.

    target: IP, hostname, or CIDR range
    scripts: Script name(s), e.g. 'http-title', 'ssl-cert,http-headers', 'banner'
    ports: Port range (default: top 1000 common ports)
    """
    _require_scope(target, "nmap_script_scan")
    port_args = ["--top-ports=1000"] if ports == "common" else ["-p", ports]
    extra = ["-sT", f"--script={scripts}", "-T4"] + port_args

    result = _nmap_structured(target, extra, timeout=TIMEOUTS["standard"])
    scan_id = _save_scan("nmap_script_scan", target, result)

    # Pull script output out of the structured result
    script_results = {}
    for ip, data in result.get("hosts", {}).items():
        script_results[ip] = {"hostname": data.get("hostname", ""), "scripts": {}}
        for proto, ports_data in data.get("protocols", {}).items():
            for port, pd in ports_data.items():
                if pd.get("script"):
                    script_results[ip]["scripts"][f"{port}/{proto}"] = pd["script"]

    output = {"scan_id": scan_id, "target": target, "scripts_run": scripts, "results": script_results}
    _audit("nmap_script_scan", target, {"scripts": scripts, "ports": ports}, "completed", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_vuln_scan(target: str, ports: str = "common") -> str:
    """
    Run the full 'vuln' NSE script category — checks for known CVEs and
    common misconfigurations (SMB vulns, weak SSL, default creds, etc.).
    This is slow. Use on specific targets, not wide ranges.

    target: IP or hostname (keep scope tight for vuln scans)
    ports: Port range (default: top 1000 common ports)
    """
    _require_scope(target, "nmap_vuln_scan")
    port_args = ["--top-ports=1000"] if ports == "common" else ["-p", ports]
    extra = ["-sT", "--script=vuln", "-T4"] + port_args

    result = _nmap_structured(target, extra, timeout=TIMEOUTS["deep"])
    scan_id = _save_scan("nmap_vuln_scan", target, result)

    # Extract vulnerability findings
    findings = {}
    for ip, data in result.get("hosts", {}).items():
        findings[ip] = {"hostname": data.get("hostname", ""), "vulnerabilities": {}}
        for proto, ports_data in data.get("protocols", {}).items():
            for port, pd in ports_data.items():
                if pd.get("script"):
                    findings[ip]["vulnerabilities"][f"{port}/{proto}"] = pd["script"]

    output = {"scan_id": scan_id, "target": target, "vulnerability_findings": findings}
    _audit("nmap_vuln_scan", target, {"ports": ports}, f"{len(findings)} hosts checked", True)
    return json.dumps(output, indent=2)


# --- Convenience ------------------------------------------------------------

@mcp.tool()
def nmap_full_recon(target: str, ports: str = "common") -> str:
    """
    Full reconnaissance sweep: SYN scan + service detection + OS fingerprinting
    + default NSE scripts. The all-in-one audit tool for a single host or small range.
    Takes a while — use nmap_top_ports or nmap_ping_scan first for wide ranges.

    target: IP, hostname, or small CIDR range (e.g. /28 or smaller)
    ports: Port range (default: top 1000 common ports)
    """
    _require_scope(target, "nmap_full_recon")
    port_args = ["--top-ports=1000"] if ports == "common" else ["-p", ports]
    extra = ["--privileged", "-sS", "-sV", "-O", "--script=default", "-T4"] + port_args

    result = _nmap_structured(target, extra, timeout=TIMEOUTS["deep"])
    scan_id = _save_scan("nmap_full_recon", target, result)

    summary = _port_summary(result)
    os_results = {
        ip: data.get("os", [])[:1]  # top OS match only
        for ip, data in result.get("hosts", {}).items()
    }
    output = {
        "scan_id": scan_id,
        "target": target,
        "ports_scanned": ports,
        "os_detection": os_results,
        **summary,
    }
    _audit("nmap_full_recon", target, {"ports": ports}, f"{summary['total_open']} open ports", True)
    return json.dumps(output, indent=2)


@mcp.tool()
def nmap_custom_scan(target: str, flags: str) -> str:
    """
    Run nmap with arbitrary flags. Still subject to scope enforcement and audit logging.
    For power users who need options not covered by the other tools.
    Do NOT include the target in flags — it's added automatically.

    target: IP, hostname, or CIDR range
    flags: Raw nmap flags, e.g. '-sS -p 443 --script ssl-enum-ciphers'
    """
    _require_scope(target, "nmap_custom_scan")

    # Reject shell metacharacters
    FORBIDDEN = [";", "&", "|", "`", "$", "(", ")", "<", ">", "\n", "\r", "\x00"]
    for ch in FORBIDDEN:
        if ch in flags:
            _audit("nmap_custom_scan", target, {"flags": flags}, f"REJECTED: forbidden char", False)
            raise ValueError(f"Forbidden character in flags. Use individual tool functions for complex scans.")

    # Block flags that write to paths or execute arbitrary code
    # (nmap output flags, --script with path, --datadir, etc.)
    if _DANGEROUS_FLAGS.search(flags):
        _audit("nmap_custom_scan", target, {"flags": flags}, "REJECTED: dangerous flag", False)
        raise ValueError(
            "Flags containing path-writing or code-execution options are not allowed "
            "(e.g. -oN, -oX, --script with path, --datadir). "
            "Use nmap_script_scan or nmap_vuln_scan for NSE scripts."
        )

    args = flags.split() + [target]
    raw = _run_nmap(args, timeout=TIMEOUTS["deep"])
    scan_id = _save_scan("nmap_custom_scan", target, {"raw_output": raw["stdout"], "command": raw["command"]})

    output = {
        "scan_id": scan_id,
        "target": target,
        "command": raw["command"],
        "success": raw["success"],
        "output": raw["stdout"],
    }
    if raw["stderr"]:
        output["stderr"] = raw["stderr"]

    _audit("nmap_custom_scan", target, {"flags": flags}, "completed" if raw["success"] else "failed", raw["success"])
    return json.dumps(output, indent=2)


# --- Scan History -----------------------------------------------------------

@mcp.tool()
def nmap_list_scans(limit: int = 20) -> str:
    """
    List recent saved scans with their IDs, timestamps, tool used, and target.
    Use the scan_id with nmap_get_scan to retrieve full results.

    limit: Max number of scans to return (default 20, newest first)
    """
    scans = sorted(SCAN_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    results = []
    for p in scans:
        try:
            with open(p) as f:
                d = json.load(f)
            results.append({
                "scan_id": d.get("scan_id"),
                "timestamp": d.get("timestamp"),
                "tool": d.get("tool"),
                "target": d.get("target"),
                "file": p.name,
            })
        except Exception:
            pass
    return json.dumps({"scans": results, "count": len(results)}, indent=2)


@mcp.tool()
def nmap_get_scan(scan_id: str) -> str:
    """
    Retrieve the full result of a previous scan by its ID.

    scan_id: The scan_id returned by any scan tool or nmap_list_scans
    """
    # Sanitize — scan_id should be alphanumeric + underscores only
    safe_id = "".join(c for c in scan_id if c.isalnum() or c == "_")
    path = SCAN_DIR / f"{safe_id}.json"
    if not path.exists():
        return json.dumps({"error": f"Scan '{scan_id}' not found"})
    with open(path) as f:
        return f.read()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _port_summary(result: dict, proto: str = "tcp") -> dict:
    """Extract a flat list of open ports across all hosts from a structured result."""
    all_open: list[dict] = []
    per_host: dict = {}

    for ip, data in result.get("hosts", {}).items():
        host_open = []
        protocols_data = data.get("protocols", {})
        # Only iterate the requested protocol — avoids double-counting
        if proto in protocols_data:
            for port_num, pd in protocols_data[proto].items():
                if pd.get("state") in ("open", "open|filtered"):
                    entry = {
                        "port": port_num,
                        "protocol": proto,
                        "state": pd["state"],
                        "service": pd.get("name", ""),
                        "version": f"{pd.get('product','')} {pd.get('version','')}".strip(),
                    }
                    host_open.append(entry)
                    all_open.append({"ip": ip, **entry})
        per_host[ip] = {
            "hostname": data.get("hostname", ""),
            "state": data.get("state"),
            "open_ports": host_open,
        }

    return {
        "total_open": len(all_open),
        "per_host": per_host,
        "all_open_ports": all_open,
    }


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    log.info("starting — allowed CIDRs: %s", [str(c) for c in ALLOWED_CIDRS])
    log.info("scan dir: %s", SCAN_DIR)
    log.info("audit log: %s", AUDIT_LOG)
    mcp.run()
