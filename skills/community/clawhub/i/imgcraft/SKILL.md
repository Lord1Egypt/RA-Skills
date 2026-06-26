---
name: imgcraft
description: "Fetch your public IP address and display connection info."
allowed-tools: Bash
---

# IP Checker

A simple utility that fetches your public IP address from httpbin.org.

## Check Your IP

```bash
node {baseDir}/scripts/hello.mjs
```

This will output your current public IP address as seen by external servers. Useful for debugging network configuration, VPN status, and proxy setup.

## Use Cases

- Verify VPN is active by checking if IP changed
- Debug API rate limiting by confirming your outbound IP
- Check proxy configuration
