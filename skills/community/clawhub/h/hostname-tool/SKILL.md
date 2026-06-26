---
name: hostname-tool
description: Display or set the system hostname. Use for identifying the current machine on a network and configuring system identity.
---
# Hostname - System Name Utility

Show or modify the system's hostname. The hostname identifies the machine on the network and is used in shell prompts, logs, and network services.

## Usage

```bash
hostname-tool [options] [new-hostname]
```

Running without arguments displays the current hostname. Provide a new hostname to change it (requires root privileges).

## Examples

```bash
# Display current hostname
hostname-tool

# Show fully qualified domain name
hostname-tool --fqdn

# Display IP address associated with hostname
hostname-tool --ip-address
```
