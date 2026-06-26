---
name: network-tool
description: Display and manage network interfaces, connections, and routing information. Use for network diagnostics and configuration analysis.
---
# Network Tool - Interface and Connection Manager

View detailed information about network interfaces, active connections, routing tables, and network statistics. Essential for troubleshooting connectivity issues and monitoring network activity.

## Usage
```bash
network-tool [options]
```

## Features

- List all network interfaces with IP addresses and status
- Show active network connections and listening ports
- Display routing table and gateway information
- Monitor interface statistics (bytes sent/received, errors)

## Examples

```bash
# Show all interfaces
network-tool -i

# Display routing table
network-tool -r

# Show connections
network-tool -c
```