---
name: macos-bridge
version: 0.6.2
description: Bridge Mac-owned tools like imsg, remindctl, memo, things, and peekaboo onto a Linux OpenClaw gateway by installing explicit same-LAN SSH wrappers with optional Wake-on-LAN, enabled-channel auto-discovery, and OpenClaw config fallback.
metadata: {"openclaw":{"emoji":"🍎"}}
---

# macOS Bridge

Use this skill when a Linux OpenClaw gateway should expose Mac-owned tools as stable Linux-side commands.

This skill is for tools that are inherently macOS-backed:

- `imsg`
- `remindctl`
- `memo`
- `things`
- `peekaboo`

It does not try to make Linux pretend those binaries are native. It installs explicit Linux-side wrappers that call the owning Mac over SSH.

If the matching feature is disabled in `openclaw.json`, do not force the bridge.

If the feature is enabled and Linux already has a working local binary, that is also acceptable. Use this skill when the enabled feature needs the Mac-owned implementation.

## Use This Skill For

- same-LAN Linux gateway to Mac node setups
- Mac-owned tools with macOS permissions or data access
- wrapper-backed public skills that should stay truthful on Linux
- enabled-channel auto-selection from `channels.*.enabled`
- `remoteHost` auto-discovery from an existing OpenClaw config
- optional Wake-on-LAN recovery when a Mac sleeps

## Do Not Use This Skill For

- Homebrew-centric Linux augmentation where the main goal is exposing `/opt/homebrew/bin` tools in general
- Linux-native tools that should be installed locally
- patching OpenClaw internals so macOS-only tools show as green on Linux
- WAN-routed or untrusted remote Macs

## Requirements

- Linux gateway and Mac nodes share the same trusted local network or VLAN
- Linux gateway can SSH to the owning Mac node
- remote binaries exist and already have the needed macOS permissions
- Macs stay awake for work windows or support Wake-on-LAN if you expect remote resume

## Workflow

### 1. Render A Tool Ownership Map

Run:

```bash
scripts/render-tool-map.sh /home/node/.openclaw/openclaw.json
```

If the OpenClaw config already contains enabled macOS-backed channels, this prints an auto-discovered map for enabled tools first.

### 2. Install The macOS Pack

Example:

```bash
scripts/install-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --openclaw-config /home/node/.openclaw/openclaw.json \
  --default-host agent2@192.168.88.12 \
  --wake-map mac-node.local=AA:BB:CC:DD:EE:FF \
  --wake-wait 20 \
  --wake-retries 2
```

When no `--tool` or `--map` arguments are provided, the installer now auto-selects only the supported tools whose channels are enabled in the OpenClaw config.

The installer resolves hosts in this order:

- explicit `--map tool=user@host`
- matching `remoteHost` in the OpenClaw config
- `--default-host user@host`
- the single discovered Mac host if only one unique `remoteHost` exists
- no repeated host questions when the OpenClaw config already resolves the owner

### 3. Verify The Pack

Run:

```bash
scripts/verify-macos-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --openclaw-config /home/node/.openclaw/openclaw.json
```

When `--openclaw-config` is provided, verification only checks enabled macOS-backed features instead of treating every supported tool as required.

## Design Contract

- Linux holds the wrapper paths
- macOS holds the real binaries and OS permissions
- published skills depend on wrapper paths, not remote binary paths
- tool ownership stays explicit and auditable

## Files

- `scripts/install-wrapper.sh`: create one SSH wrapper for a remote binary
- `scripts/install-macos-pack.sh`: install a batch of macOS-owned tool wrappers with auto-discovery and optional Wake-on-LAN
- `scripts/verify-macos-pack.sh`: verify the installed wrapper pack
- `scripts/render-tool-map.sh`: print auto-discovered or fallback ownership maps
- `references/skill-readiness.md`: publishability rules for wrapper-backed skills
