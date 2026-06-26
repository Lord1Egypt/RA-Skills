---
name: linux-to-mac-bridge
version: "1.2.1"
description: Legacy combined bridge skill for Linux-to-Mac wrapper installs. Prefer the newer split skills `macos-bridge` for Mac-owned CLIs and `homebrew-bridge` for Homebrew-backed tools.
metadata: {"openclaw":{"emoji":"🌉"}}
---

# Linux to Mac Bridge

This is now the legacy combined skill.

Prefer:

- `macos-bridge` for `imsg`, `remindctl`, `memo`, `things`, `peekaboo`
- `homebrew-bridge` for `brew`, `gh`, and other `/opt/homebrew/bin` tools

Use this skill when a Linux gateway should expose Mac-backed tools as stable Linux-side commands.

This is the publishable answer to the “gray macOS skill on Linux gateway” problem:

- do not patch bundled skills
- do not pretend Linux can run macOS binaries
- install explicit wrappers on the Linux gateway
- make public skills depend on those wrapper paths instead
- assume the Linux gateway and Mac nodes are on the same trusted local network

## Use This Skill For

- `imsg`, `remindctl`, `memo`, `things`, `peekaboo`
- Homebrew business tools that live on a connected Mac node
- wrapper-backed skills that should show as ready on a Linux gateway
- capability reports and stable tool ownership mapping
- same-LAN Linux gateway to Mac node setups
- Mac nodes that are kept awake or have Wake-on-LAN enabled

## Do Not Use This Skill For

- Linux-native tools that should just be installed locally
- random internet-routed Mac hosts or untrusted WAN hops
- arbitrary remote shell access
- patching OpenClaw internals so bundled macOS skills lie about support

## Requirements

- Linux gateway and Mac nodes share the same trusted local network or VLAN
- Linux gateway can SSH to the owning Mac nodes
- remote binaries exist and have the needed macOS permissions
- you know which Mac owns each tool
- Mac nodes should stay awake for agent work, or at minimum have Wake-on-LAN enabled if you expect them to be resumed remotely

## Local Network Contract

This skill is designed for a homelab or office-local topology:

- Linux gateway on the same LAN as the Macs
- stable RFC1918 or otherwise local addresses for the Mac nodes
- low-latency SSH between gateway and nodes
- no requirement for public internet routing to the Macs

Default assumption:

- if the gateway cannot reach the Mac over the local network, the wrapper-backed workflow is not healthy

Wake-on-LAN note:

- the wrapper install scripts can embed Wake-on-LAN metadata and retry logic
- if a Mac may sleep, configure a wake map so the Linux-side wrapper can send a magic packet and retry SSH automatically

## Design Contract

- Linux gateway holds the wrappers
- Mac nodes hold the real binaries and OS-level permissions
- public skills depend on the wrapper path, not the remote path
- tool ownership stays explicit and auditable
- the bridge is optimized for same-LAN node reachability, not public-host reachability

## Workflow

### 1. Render A Tool Ownership Map

Run:

```bash
scripts/render-tool-map.sh
```

If `~/.openclaw/openclaw.json` already contains Mac-backed `remoteHost` entries, this will auto-render a gateway-local ownership map from that config first. In that case, do not ask again for IP address or SSH username unless the discovered mapping is missing or clearly wrong.

Otherwise it gives you a repeatable starter map such as:

- `imsg -> mac-ops@mac-messages.local`
- `remindctl -> mac-ops@mac-messages.local`
- `gh -> mac-ops@mac-tools.local`

### 2. Install The macOS Pack

Example:

```bash
scripts/install-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --tool imsg \
  --tool remindctl \
  --tool memo \
  --tool gh \
  --openclaw-config /home/node/.openclaw/openclaw.json \
  --wake-map mac-messages.local=AA:BB:CC:DD:EE:FF \
  --wake-map mac-tools.local=11:22:33:44:55:66 \
  --wake-wait 20 \
  --wake-retries 2
```

The installer will now:

- use explicit `--map tool=user@host` entries when you provide them
- otherwise try to infer the tool host from `remoteHost` values in the OpenClaw config
- fall back to a single discovered Mac host for unmapped tools when only one unique `remoteHost` is known
- let you force a shared owner with `--default-host user@host`
- avoid manual host questions when it can already resolve the owner from the OpenClaw config

This creates wrapper paths on Linux such as:

- `/home/node/.openclaw/bin/imsg`
- `/home/node/.openclaw/bin/remindctl`
- `/home/node/.openclaw/bin/memo`
- `/home/node/.openclaw/bin/gh`

When a wake map is configured, the generated wrapper will:

- attempt SSH normally first
- send a Wake-on-LAN magic packet if the first attempt fails
- wait the configured number of seconds
- retry the remote command

### 3. Verify The Pack

Run:

```bash
scripts/verify-macos-pack.sh --target-dir /home/node/.openclaw/bin
```

This verifies the wrapper executables exist and can be resolved from the gateway side.

It also shows whether Wake-on-LAN is embedded in each installed wrapper.

### 4. Build Public Skills On Top

When publishing a community skill:

- require the Linux wrapper path, not the macOS binary path
- document which Mac is expected to own the tool
- treat the wrapper as the stable API surface

Read [references/skill-readiness.md](references/skill-readiness.md).

## Security Rules

- one wrapper per tool
- one explicit owning Mac per tool
- no generic remote shell bridge
- no secrets stored in the skill folder
- no core patching to force a green badge

## Files

- `scripts/install-wrapper.sh`: create one SSH wrapper for a remote binary
- `scripts/install-macos-pack.sh`: install a batch of common Mac-backed tool wrappers with optional auto-discovery from OpenClaw config and Wake-on-LAN maps
- `scripts/verify-macos-pack.sh`: verify the wrapper pack on the Linux gateway and show Wake-on-LAN status
- `scripts/render-tool-map.sh`: print the auto-discovered or recommended tool ownership map plus Wake-on-LAN map examples
- `references/skill-readiness.md`: how to make public skills stay ready on Linux without patching core
