#!/usr/bin/env python3
"""Scan running Docker containers and output JSON."""

import json
import os
import re
import subprocess
import sys


def docker_available():
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def parse_ports(ports_str):
    """Parse Docker ports string into a list of port mappings."""
    if not ports_str:
        return []
    return [p.strip() for p in ports_str.split(",") if p.strip()]


def scan_docker():
    if not docker_available():
        return {"error": "Docker not installed or not running", "containers": []}

    # Try --format json (Docker 20.10+)
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0 and result.stdout.strip():
            containers = []
            for line in result.stdout.strip().splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    raw = json.loads(line)
                    containers.append({
                        "name": raw.get("Names", ""),
                        "image": raw.get("Image", ""),
                        "status": raw.get("Status", ""),
                        "ports": parse_ports(raw.get("Ports", "")),
                        "mounts": [m.strip() for m in raw.get("Mounts", "").split(",") if m.strip()],
                        "created": raw.get("CreatedAt", ""),
                        "id": raw.get("ID", raw.get("Id", "")),
                    })
                except json.JSONDecodeError:
                    continue
            return {"containers": containers}
    except subprocess.TimeoutExpired:
        return {"error": "Docker command timed out", "containers": []}

    # Fallback: plain docker ps
    try:
        result = subprocess.run(
            ["docker", "ps", "--no-trunc"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return {"error": result.stderr.strip(), "containers": []}

        lines = result.stdout.strip().splitlines()
        if len(lines) < 2:
            return {"containers": []}  # No containers

        # Parse header to find column positions
        header = lines[0]
        col_names = re.split(r"  +", header.strip())
        containers = []
        for line in lines[1:]:
            parts = re.split(r"  +", line.strip())
            if len(parts) >= 6:
                containers.append({
                    "id": parts[0] if len(parts) > 0 else "",
                    "image": parts[1] if len(parts) > 1 else "",
                    "status": parts[4] if len(parts) > 4 else "",
                    "ports": parse_ports(parts[5] if len(parts) > 5 else ""),
                    "name": parts[-1] if parts else "",
                    "mounts": [],
                    "created": "",
                })
        return {"containers": containers}
    except subprocess.TimeoutExpired:
        return {"error": "Docker command timed out", "containers": []}
    except Exception as e:
        return {"error": str(e), "containers": []}


if __name__ == "__main__":
    data = scan_docker()
    print(json.dumps(data, indent=2))
