---
name: HomeNetworkSecurityAgent
description: Audits local network infrastructure, identifies active hosts, and scans the gateway/public IP for exposed ports and vulnerabilities.
version: 1.0.0
author: assix
keywords:
  - security
  - networking
  - nmap
  - vulnerability-scanner
  - agent
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - nmap
        - ip
---

# HomeNetworkSecurityAgent

This agent performs internal and external security audits of your home network environment. It utilizes `nmap` to discover devices and footprint exposed services.

## Setup
Ensure `nmap` is installed on the host system:
```bash
sudo apt install nmap
```

## User Instructions
- "Scan my local network and tell me what devices are online."
- "Find my public IP and gateway, then check if my gateway management ports (like 8443, 443) or DNS resolvers (like port 53) are exposed to the outside."
- "Run a deep vulnerability scan on my router to see if it needs a firmware update."

## Tools

### `get_network_topology`
Retrieves the default gateway IP and the external public IP address of the network.
- **Inputs:** None
- **Call:** `python3 scanner.py --tool get_network_topology`

### `discover_lan_hosts`
Performs a ping sweep on the local subnet to identify all connected physical and IoT devices.
- **Inputs:** `gateway_ip` (string)
- **Call:** `python3 scanner.py --tool discover_lan_hosts --target {{gateway_ip}}`

### `scan_ports_and_vulns`
Runs a service detection scan against a target IP (local or public) to list open ports and identify potential misconfigurations.
- **Inputs:** `ip_address` (string), `scan_type` (string: "fast" or "deep")
- **Call:** `python3 scanner.py --tool scan_ports_and_vulns --target {{ip_address}} --type {{scan_type}}`
