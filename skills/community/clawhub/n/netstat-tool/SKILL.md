---
name: netstat-tool
description: Display network connections, routing tables, and interface statistics. Use for network diagnostics and monitoring.
---
# Netstat - Network Statistics Viewer

Show active network connections, listening ports, routing tables, and network interface statistics. Essential for network troubleshooting.

## Usage
```bash
netstat-tool [options]
```
## Options
- `-t`: TCP connections only
- `-u`: UDP connections only
- `-l`: Show listening sockets only
- `-n`: Show numeric addresses
- `-p`: Show process using connection
## Examples
```bash
netstat-tool -tlnp
netstat-tool -rn
netstat-tool -i
```