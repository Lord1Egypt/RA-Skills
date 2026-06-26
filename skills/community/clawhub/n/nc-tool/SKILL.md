---
name: nc-tool
description: Read and write data across network connections using TCP or UDP. Use for network debugging, port scanning, and data transfer.
---
# NC - Netcat Network Utility

Read from and write to network connections using TCP or UDP. Versatile tool for network diagnostics, port testing, and simple data transfer.

## Usage
```bash
nc-tool [options] <host> <port>
```
## Features
- TCP and UDP connections
- Port scanning
- Listen mode for receiving connections
- Data transfer and piping
## Examples
```bash
nc-tool -v example.com 80
nc-tool -l -p 8080
nc-tool -z host 20-80
```