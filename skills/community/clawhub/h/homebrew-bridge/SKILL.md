---
name: homebrew-bridge
version: "0.6.1"
description: Expose Mac Homebrew tools like brew, gh, and other /opt/homebrew/bin CLIs on a Linux OpenClaw gateway by installing explicit same-LAN SSH wrappers with optional Wake-on-LAN and OpenClaw config auto-discovery.
metadata: {"openclaw":{"emoji":"🍺"}}
---

# Homebrew Bridge

Use this skill when the real value is giving a Linux OpenClaw gateway access to a Mac node's Homebrew toolchain.

This skill is for `/opt/homebrew/bin/<tool>` wrappers such as:

- `brew`
- `gh`
- other Homebrew-installed CLIs you want to expose from a Mac node

## Use This Skill For

- Linux gateways that should run Homebrew-backed tools through a Mac node
- wrapper-backed skills that depend on `brew`, `gh`, or another Homebrew CLI
- same-LAN Mac nodes that already hold the real Homebrew installs
- optional host auto-discovery from OpenClaw config when only one Mac owner is known

## Do Not Use This Skill For

- tools that are inherently Mac-owned apps or permissioned CLIs like `imsg` or `remindctl`
- Linux-native tools that should be installed on Linux directly
- WAN-routed Macs or generic remote shell access

## Requirements

- Linux gateway and owning Mac share the same trusted local network or VLAN
- Linux gateway can SSH to the owning Mac
- the requested tool exists at `/opt/homebrew/bin/<tool>` on that Mac
- the Mac stays awake during work windows or supports Wake-on-LAN

## Workflow

### 1. Render A Tool Ownership Map

Run:

```bash
scripts/render-tool-map.sh /home/node/.openclaw/openclaw.json
```

This prints the inferred or fallback Mac owner for Homebrew-backed tools.

### 2. Install The Homebrew Pack

Example:

```bash
scripts/install-homebrew-pack.sh \
  --target-dir /home/node/.openclaw/bin \
  --tool brew \
  --tool gh \
  --tool claude \
  --default-host mac-ops@mac-node.local \
  --wake-map mac-node.local=AA:BB:CC:DD:EE:FF \
  --wake-wait 20 \
  --wake-retries 2
```

Host resolution order:

- explicit `--map tool=user@host`
- `--default-host user@host`
- the single discovered `remoteHost` in the OpenClaw config, if there is exactly one
- no repeated host questions when the OpenClaw config already resolves the owner

### 3. Verify The Pack

Run:

```bash
scripts/verify-homebrew-pack.sh --target-dir /home/node/.openclaw/bin
```

## Design Contract

- Linux owns the stable wrapper paths
- the Mac owns the real `/opt/homebrew/bin` binaries
- public skills depend on wrapper paths, not Mac paths
- wrapper names stay explicit per tool

## Files

- `scripts/install-wrapper.sh`: create one SSH wrapper for a remote binary
- `scripts/install-homebrew-pack.sh`: install a batch of Homebrew-backed wrappers
- `scripts/verify-homebrew-pack.sh`: verify the installed wrappers
- `scripts/render-tool-map.sh`: print inferred or fallback tool-to-host maps
- `references/skill-readiness.md`: publishability rules for Homebrew-backed wrappers
