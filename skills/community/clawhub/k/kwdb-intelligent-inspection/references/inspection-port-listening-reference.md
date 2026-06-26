# Port Listening Detection Reference

This document describes how to check KaiwuDB port reachability status.

## Critical Constraint (non-negotiable)

**Do not SSH into the target server to run inspection commands there.** Always use local tools on the machine where the inspection is being performed. Only use remote port probing tools (`nc`, `telnet`, `curl`, `wget`) to check if KaiwuDB ports are reachable on target servers.

## Default Ports

| Service | Default Port | Description |
|---------|-------------|-------------|
| SQL Port | `26257` | KaiwuDB SQL/API port |
| Admin Console | `8080` | Admin UI port |

## Supported Detection Methods

Use remote port probing tools to check if KaiwuDB ports are listening on target servers. Common tools:

- **All platforms**: `nc` (netcat), `telnet`
- **For HTTP ports**: `curl`, `wget`

## Tool Installation

If the required port detection tool is not available on the local system:

1. **Do NOT install tool automatically** — always request user permission first
2. Explain to the user which tool is missing and why it is needed
3. Ask for explicit confirmation before proceeding with installation
4. Only after user approval, proceed with installation using system package manager

Example prompt when tool is missing:
```
[TOOL_MISSING] The port probing tool 'nc' is not installed on this system.
Required for: Checking if KaiwuDB ports (26257, 8080) are reachable on target server.
Do you want me to install it? (y/n)
```

## Example Commands

### Using `nc` (netcat)
```bash
nc -zv <target_host> 26257 8080 -w 5
```

### Using `telnet`
```bash
echo "quit" | telnet <target_host> 26257
```

### Using `curl` (for HTTP ports)
```bash
curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 http://<target_host>:8080
```

### Using `wget` (for HTTP ports)
```bash
wget --spider --timeout=5 -q http://<target_host>:8080
```

## Expected Output

The inspection should verify:
1. Whether each port is reachable (open/closed)
2. Connection response time (if available)

## Output Format

Report the port reachability status:
```json
{
  "port": 26257,
  "reachable": true,
  "response_time_ms": 12
}
```
