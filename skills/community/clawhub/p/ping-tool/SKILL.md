---
name: ping-tool
description: Test network connectivity to remote hosts by sending ICMP echo requests. Use for network diagnostics and latency measurement.
---

# Network Connectivity Tester

Send ICMP echo request packets to network hosts and measure response times. Essential tool for diagnosing network connectivity issues.

## Usage

```bash
ping-tool [options] <hostname>
```

## Options

- `-c N`: Send N packets then stop
- `-i N`: Wait N seconds between packets
- `-s N`: Set packet size
- `-t N`: Set timeout in seconds

## Examples

```bash
# Ping 4 times
ping-tool -c 4 google.com

# Continuous ping
ping-tool 8.8.8.8

# With interval
ping-tool -i 2 -c 10 example.com
```