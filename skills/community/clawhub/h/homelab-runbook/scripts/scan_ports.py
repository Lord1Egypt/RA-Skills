#!/usr/bin/env python3
"""Scan open TCP listening ports and identify processes. Supports macOS and Linux."""

import json
import os
import platform
import re
import subprocess
import sys


LSOF_PATHS = ["/usr/sbin/lsof", "/usr/bin/lsof", "lsof"]


def _find_lsof():
    for path in LSOF_PATHS:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    return "lsof"  # Let subprocess raise FileNotFoundError if missing


def scan_macos():
    """Use lsof to find listening TCP ports."""
    lsof = _find_lsof()
    try:
        result = subprocess.run(
            [lsof, "-iTCP", "-sTCP:LISTEN", "-n", "-P"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode not in (0, 1):  # lsof returns 1 when no results
            stderr = result.stderr.strip()
            if stderr:
                return {"error": stderr, "ports": []}

        ports = []
        seen = set()
        lines = result.stdout.strip().splitlines()
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) < 9:
                continue
            process = parts[0]
            pid_str = parts[1]
            name_field = parts[8]  # e.g. "*:8080" or "127.0.0.1:5432"

            # Parse address:port
            if ":" not in name_field:
                continue
            addr, port_str = name_field.rsplit(":", 1)
            if not port_str.isdigit():
                continue
            port = int(port_str)

            key = (port, process)
            if key in seen:
                continue
            seen.add(key)

            try:
                pid = int(pid_str)
            except ValueError:
                pid = None

            ports.append({
                "port": port,
                "address": addr,
                "process": process,
                "pid": pid,
                "proto": "tcp",
            })

        ports.sort(key=lambda x: x["port"])
        return {"os": "macOS", "ports": ports}

    except PermissionError:
        return {"error": "Permission denied running lsof. Try with sudo.", "ports": []}
    except FileNotFoundError:
        return {"error": "lsof not found", "ports": []}
    except subprocess.TimeoutExpired:
        return {"error": "lsof timed out", "ports": []}
    except Exception as e:
        return {"error": str(e), "ports": []}


def scan_linux():
    """Use ss to find listening TCP ports."""
    try:
        result = subprocess.run(
            ["ss", "-tlnp"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            # Fallback to netstat
            return scan_linux_netstat()

        ports = []
        seen = set()
        lines = result.stdout.strip().splitlines()
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) < 4:
                continue
            # State Recv-Q Send-Q Local-Address:Port Peer-Address:Port Process
            local = parts[3]
            if ":" not in local:
                continue
            addr, port_str = local.rsplit(":", 1)
            if not port_str.isdigit():
                continue
            port = int(port_str)

            process = ""
            pid = None
            # Process info in last field: users:(("nginx",pid=1234,fd=6))
            if len(parts) >= 6:
                proc_field = parts[5]
                pid_match = re.search(r'pid=(\d+)', proc_field)
                name_match = re.search(r'"([^"]+)"', proc_field)
                if pid_match:
                    pid = int(pid_match.group(1))
                if name_match:
                    process = name_match.group(1)

            key = (port, process)
            if key in seen:
                continue
            seen.add(key)

            ports.append({
                "port": port,
                "address": addr,
                "process": process,
                "pid": pid,
                "proto": "tcp",
            })

        ports.sort(key=lambda x: x["port"])
        return {"os": "Linux", "ports": ports}

    except FileNotFoundError:
        return scan_linux_netstat()
    except subprocess.TimeoutExpired:
        return {"error": "ss timed out", "ports": []}
    except Exception as e:
        return {"error": str(e), "ports": []}


def scan_linux_netstat():
    """Fallback using netstat if ss is not available."""
    try:
        result = subprocess.run(
            ["netstat", "-tlnp"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return {"error": "Neither ss nor netstat available", "ports": []}

        ports = []
        for line in result.stdout.strip().splitlines():
            if not line.startswith("tcp"):
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            local = parts[3]
            if ":" not in local:
                continue
            addr, port_str = local.rsplit(":", 1)
            if not port_str.isdigit():
                continue
            port = int(port_str)
            process = parts[6] if len(parts) > 6 else ""
            pid = None
            if "/" in process:
                pid_str, process = process.split("/", 1)
                try:
                    pid = int(pid_str)
                except ValueError:
                    pass
            ports.append({
                "port": port,
                "address": addr,
                "process": process,
                "pid": pid,
                "proto": "tcp",
            })
        ports.sort(key=lambda x: x["port"])
        return {"os": "Linux", "ports": ports}
    except Exception as e:
        return {"error": str(e), "ports": []}


def scan_ports():
    os_name = platform.system()
    if os_name == "Darwin":
        return scan_macos()
    elif os_name == "Linux":
        return scan_linux()
    else:
        return {"error": f"Unsupported OS: {os_name}", "ports": []}


if __name__ == "__main__":
    data = scan_ports()
    print(json.dumps(data, indent=2))
