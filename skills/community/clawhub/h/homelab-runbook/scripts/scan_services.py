#!/usr/bin/env python3
"""Scan running system services and output JSON. Supports macOS (launchd) and Linux (systemd)."""

import json
import os
import re
import subprocess
import sys


def detect_os():
    import platform
    return platform.system()  # 'Darwin' or 'Linux'


def scan_macos():
    """Use launchctl list to get running services."""
    try:
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip(), "services": []}

        services = []
        lines = result.stdout.strip().splitlines()
        # Header: PID  Status  Label
        for line in lines[1:]:
            parts = line.split(None, 2)
            if len(parts) < 3:
                continue
            pid_str, status_str, label = parts
            pid = None if pid_str == "-" else pid_str
            # Only include services with a running PID (not "-")
            if pid is not None:
                try:
                    services.append({
                        "name": label.strip(),
                        "pid": int(pid),
                        "exit_code": int(status_str) if status_str.lstrip("-").isdigit() else status_str,
                        "status": "running" if pid else "stopped",
                    })
                except (ValueError, TypeError):
                    services.append({
                        "name": label.strip(),
                        "pid": pid,
                        "exit_code": status_str,
                        "status": "running",
                    })
        return {"os": "macOS", "services": services}
    except FileNotFoundError:
        return {"error": "launchctl not found", "services": []}
    except subprocess.TimeoutExpired:
        return {"error": "launchctl timed out", "services": []}
    except Exception as e:
        return {"error": str(e), "services": []}


def scan_linux():
    """Use systemctl to list running services."""
    try:
        result = subprocess.run(
            [
                "systemctl",
                "list-units",
                "--type=service",
                "--state=running",
                "--no-pager",
                "--no-legend",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip(), "services": []}

        services = []
        for line in result.stdout.strip().splitlines():
            parts = line.split(None, 4)
            if not parts:
                continue
            name = parts[0].removesuffix(".service") if parts[0].endswith(".service") else parts[0]
            load = parts[1] if len(parts) > 1 else ""
            active = parts[2] if len(parts) > 2 else ""
            sub = parts[3] if len(parts) > 3 else ""
            desc = parts[4].strip() if len(parts) > 4 else ""
            services.append({
                "name": name,
                "load": load,
                "active": active,
                "sub": sub,
                "description": desc,
                "status": "running" if sub == "running" else sub,
            })
        return {"os": "Linux", "services": services}
    except FileNotFoundError:
        return {"error": "systemctl not found", "services": []}
    except subprocess.TimeoutExpired:
        return {"error": "systemctl timed out", "services": []}
    except Exception as e:
        return {"error": str(e), "services": []}


def scan_services():
    os_name = detect_os()
    if os_name == "Darwin":
        return scan_macos()
    elif os_name == "Linux":
        return scan_linux()
    else:
        return {"error": f"Unsupported OS: {os_name}", "services": []}


if __name__ == "__main__":
    data = scan_services()
    print(json.dumps(data, indent=2))
