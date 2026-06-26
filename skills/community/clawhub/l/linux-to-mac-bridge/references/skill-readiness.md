# Skill Readiness

Use this file when building public skills that should stay ready on a Linux gateway while using Mac-backed tools.

This pattern is meant for the same trusted local network, not arbitrary internet-routed Macs.

## The Problem

Bundled macOS-only skills often stay gray on a Linux gateway because the Linux host does not actually have the macOS binary.

Trying to patch OpenClaw core to change that is brittle.

## The Publishable Pattern

Instead:

- install a Linux-side wrapper path
- point the wrapper at the owning Mac node over SSH
- make the public skill depend on the wrapper path
- assume the gateway can reach the Mac over the local LAN or VLAN

Then the published skill can truthfully say:

- Linux gateway requirement: wrapper exists
- Mac node requirement: real binary exists and permissions are granted
- Network requirement: gateway and owning Mac are on the same local network and reachable over SSH
- Node readiness requirement: Mac stays awake or has Wake-on-LAN enabled
- Recovery behavior: wrapper can send Wake-on-LAN and retry when the node is asleep, if a wake map was configured at install time

## Good Example

Skill requirement:

- `/home/node/.openclaw/bin/imsg`

Implementation:

- wrapper on Linux
- `/opt/homebrew/bin/imsg` on the owning Mac
- owning Mac reachable over the same local network
- owning Mac configured to stay awake during work windows or support Wake-on-LAN for recovery
- optional Wake-on-LAN metadata embedded into the Linux wrapper

## Bad Example

- patching bundled skill metadata to claim Linux natively supports `imsg`
- depending on `/opt/homebrew/bin/imsg` directly from a Linux skill
- treating an off-LAN or sleeping Mac as if it were a stable always-on tool host
