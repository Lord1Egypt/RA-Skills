# OpenClaw Security Modes

## Conservative Mode (Production)

### Use Cases
- Production environments
- Enterprise deployments  
- Sensitive data handling
- Compliance requirements

### Configuration Settings

#### Gateway
- `bind`: "loopback" (only localhost access)
- `auth.mode`: "token" (mandatory token authentication)
- `auth.token`: 64+ character random token
- `tailscale.mode`: "off" (no remote access)

#### Tools
- `profile`: "messaging" (minimal permissions)
- `fs.workspaceOnly`: true (workspace isolation)

#### Session
- `dmScope`: "paired" (explicit pairing required)
- `pairingStrategy`: "manual"

#### Security Score Target: 95+

### Risk Profile
- **Network Exposure**: Minimal
- **Authentication**: Strong
- **Permissions**: Least privilege
- **Attack Surface**: Smallest possible

## Balanced Mode (Development) ⭐ Recommended

### Use Cases
- Personal development
- Small team collaboration
- Development/test environments
- General purpose usage

### Configuration Settings

#### Gateway
- `bind`: "loopback" (localhost only)
- `auth.mode`: "token" (token authentication)
- `auth.token`: 32+ character random token
- `tailscale.mode`: "auto" (remote access via Tailscale)

#### Tools
- `profile`: "coding" (development tools enabled)
- `fs.workspaceOnly`: true (workspace isolation)

#### Session
- `dmScope`: "per-channel-peer" (channel-based sessions)
- `pairingStrategy`: "auto"

#### Security Score Target: 75-90

### Risk Profile
- **Network Exposure**: Controlled (Tailscale only)
- **Authentication**: Strong
- **Permissions**: Reasonable for development
- **Attack Surface**: Moderate, balanced with usability

## Aggressive Mode (Testing)

### Use Cases
- Isolated test environments
- Local development only
- Trusted networks
- Temporary testing

### Configuration Settings

#### Gateway
- `bind`: "lan" (local network access)
- `auth.mode`: "none" (no authentication)
- `tailscale.mode`: "auto"

#### Tools
- `profile`: "full" (all permissions enabled)
- `fs.workspaceOnly`: false (full filesystem access)

#### Session
- `dmScope`: "any" (anyone can start sessions)
- `pairingStrategy`: "auto"

#### Security Score Target: 40-60

### Risk Profile
- **Network Exposure**: High (local network)
- **Authentication**: None
- **Permissions**: Full system access
- **Attack Surface**: Large

### ⚠️ Warning
This mode should ONLY be used in completely isolated test environments. Never use in production or on networks with untrusted devices.

## Mode Selection Guide

### Choose Conservative Mode When:
- Running in production
- Handling sensitive data
- Subject to compliance requirements
- Security is the top priority

### Choose Balanced Mode When:
- Developing applications
- Working in small teams
- Need reasonable security with good usability
- Most common use case

### Choose Aggressive Mode When:
- Testing in isolated environments
- Temporary development setup
- Network is completely trusted
- Maximum functionality needed for testing

## Migration Between Modes

### Conservative → Balanced
- Change `tools.profile` from "messaging" to "coding"
- Change `session.dmScope` from "paired" to "per-channel-peer"
- Enable Tailscale if needed

### Balanced → Conservative  
- Change `tools.profile` from "coding" to "messaging"
- Change `session.dmScope` from "per-channel-peer" to "paired"
- Disable Tailscale

### Any Mode → Aggressive
- Set `gateway.auth.mode` to "none"
- Set `tools.profile` to "full"
- Set `tools.fs.workspaceOnly` to false
- Set `session.dmScope` to "any"

### Aggressive → Any Other Mode
- **Always** enable authentication first
- **Always** restrict tool permissions
- **Always** limit session scope
- **Always** backup configuration before changes