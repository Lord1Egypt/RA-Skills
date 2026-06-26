# Python MikroTik RouterOS API Client

A simple, lightweight Python client for the MikroTik RouterOS API.

## Features

- Lightweight and dependency-free (standard library only)
- Supports both cleartext (8728) and SSL (8729) connections
- Command-line interface for quick debugging
- Comprehensive command wrappers for common tasks
- Network scanner for discovering devices

## Usage

### Library

```python
from mikrotik_api.client import RouterOSApi

# Connect to device
with RouterOSApi("192.168.88.1", "admin", "password") as api:
    # Run command
    results = api.run_command("/system/resource/print")
    print(results)
```

### CLI

```bash
# Specify username and password
python cli.py 192.168.88.1 status -u admin -p yourpassword

# Use environment variables
export MIKROTIK_USER=admin
export MIKROTIK_PASS=yourpassword
python cli.py 192.168.88.1 status
```

## Features

### Core Client (`client.py`)
- Connection management
- Word encoding/decoding
- Error handling
- SSL support

### Command Wrappers (`commands.py`)
- `SystemCommands`: Resources, health, identity, backup, logs
- `InterfaceCommands`: Lists, addresses, routes, bridge, vlan, wireguard
- `FirewallCommands`: Filter, NAT, Mangle, address-lists
- `UserPPPCommands`: System users, PPP secrets, hotspot users
- `IPCommands`: ARP, DNS, DHCP leases, neighbors

### CLI Tool (`cli.py`)
- Interactive or single-shot command execution
- Formatted output

### Scanner (`scanner.py`)
- Discover MikroTik devices on the local network
- No configuration required

## Protocol Support

MikroTik RouterOS API uses a custom sentence-based protocol over TCP. This client implements:
1. **Connection**: TCP socket (port 8728/8729)
2. **Authentication**: Supports empty passwords and MD5 challenge-response
3. **Sentences**: Commands and attributes encoded as length-prefixed words
4. **Responses**: `!re` (reply), `!trap` (error), `!done` (finished)

## License

MIT
