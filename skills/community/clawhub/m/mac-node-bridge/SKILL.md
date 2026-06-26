---
name: mac-node-bridge
description: Bridge macOS-only tools into a Linux OpenClaw gateway via SSH wrappers and connected Mac nodes. Use when a Linux gateway needs to run imsg, remindctl, memo, things, peekaboo, brew-backed CLIs, or other node-local macOS binaries without patching OpenClaw core or pretending Linux can run macOS skills directly.
metadata: {"openclaw":{"emoji":"🔌"}}
---

# Mac Node Bridge

Use this skill when your gateway runs on Linux but the real tool lives on a Mac node.

This skill does not patch bundled OpenClaw skills. It creates explicit SSH wrappers and verification steps so a Linux gateway can call macOS binaries on connected nodes in a way that is publishable, repeatable, and auditable.

## Use This Skill For

- `imsg`, `remindctl`, `memo`, `things`, `peekaboo`, or other macOS-only CLIs
- Homebrew-installed business tools that only exist on a Mac node
- Linux gateway + one or more Mac nodes where you want a stable remote execution path
- ClawHub-ready skills that should target Macs cleanly instead of mutating bundled Linux assumptions

## Do Not Use This Skill For

- Linux-native CLIs that should simply be installed on the gateway
- UI-only pairing problems
- Cases where you do not have passwordless SSH from the gateway to the Mac node
- Forcing bundled OpenClaw macOS skills to show green on Linux by patching core files

## Requirements

- Linux gateway can SSH to the target Mac node without a password
- Remote binary exists on the Mac node and is executable
- The Mac node already has any required macOS privacy permissions granted
- You know which Mac should own the tool

## Path Rules

Use dynamic paths by default.

- Wrapper install dir defaults to `OPENCLAW_BIN_DIR`, then `XDG_DATA_HOME/openclaw/bin`, then `HOME/.openclaw/bin`
- Preset installs resolve remote binaries dynamically with `command -v`, remote `brew --prefix`, and common Homebrew prefixes
- Use `--target-dir` or `--remote-bin` only when you intentionally need to override the defaults

## Trust Model

This skill assumes:

- the Linux gateway is the orchestrator
- each Mac node is a separately trusted execution surface
- cross-host access must be narrow, explicit, and reversible

Plan around these rules:

- use strong, scoped credentials and per-node trust, not one broad shared secret
- require the Mac side to prove identity before the gateway accepts orchestration signals
- give each wrapper only the minimum action it needs
- log cross-host setup, verification, and deployment steps
- fail soft when a Mac is unavailable; do not crash the whole system

Read [references/security-model.md](references/security-model.md) before publishing or extending this skill.

## Workflow

### 1. Pick The Owning Mac

Default pattern:

- `M1`: always-on services like `imsg`
- `MacBook Pro`: heavier interactive or business tooling

If you are unsure, verify first:

```bash
scripts/verify-node-tool.sh --host agent1@mac-mini.local --tool imsg
scripts/verify-node-tool.sh --host agent2@macbook-pro.local --tool remindctl
```

If the tool lives outside the normal shell path or Homebrew defaults, pass an explicit path:

```bash
scripts/verify-node-tool.sh --host agent2@macbook-pro.local --bin /custom/path/remindctl
```

### 2. Install A Wrapper On The Gateway

For a known tool preset:

```bash
scripts/install-preset.sh \
  --tool imsg \
  --host agent1@mac-mini.local
```

Or install a generic wrapper:

```bash
scripts/install-wrapper.sh \
  --name remindctl-mbp \
  --host agent2@macbook-pro.local \
  --remote-bin /opt/homebrew/bin/remindctl
```

Override the wrapper directory only when you need a non-default layout:

```bash
scripts/install-preset.sh \
  --tool memo \
  --host agent1@mac-mini.local \
  --target-dir "$HOME/.local/bin"
```

### 3. Verify The Wrapper

```bash
"${OPENCLAW_BIN_DIR:-${XDG_DATA_HOME:-$HOME/.openclaw}/openclaw/bin}"/imsg chats --limit 1
"${OPENCLAW_BIN_DIR:-${XDG_DATA_HOME:-$HOME/.openclaw}/openclaw/bin}"/remindctl-mbp lists
```

If the wrapper works but a bundled OpenClaw skill still shows gray, that is expected on a Linux gateway. Use the wrapper-backed workflow or publish a wrapper-aware skill instead of patching OpenClaw core.

### 4. Publish Wrapper-Aware Skills

When building a new ClawHub skill on top of this bridge:

- call the wrapper through a configurable path contract, not a user-specific absolute home path
- document which node owns the tool
- keep secrets and tokens on the node or gateway config, not in the skill folder
- treat the wrapper as the stable contract

Read [references/publish-pattern.md](references/publish-pattern.md) before turning a one-off wrapper into a public skill.

## Security Rules

- Use a dedicated SSH key for gateway-to-node wrappers whenever possible
- Use non-root accounts on the Mac nodes
- Prefer one wrapper per tool per node instead of a single unrestricted shell bridge
- Never store API tokens, app secrets, or OAuth cookies in the skill folder
- Never patch bundled OpenClaw skill files just to make Linux appear to support macOS tools
- Keep wrapper names explicit, for example `imsg-m1` or `remindctl-mbp`, when multiple Macs may own similar tools
- Log who installed or rotated a wrapper and when
- Keep a rollback path: remove one wrapper, do not tear down the whole node
- If a tool needs more than read or one explicit action, define that permission boundary in the published skill
- If a wrapper depends on a Mac-only GUI permission, verify it explicitly and report a degraded-but-safe state instead of pretending success

## Common Presets

Supported presets in `scripts/install-preset.sh`:

- `imsg`
- `remindctl`
- `memo`
- `things`
- `peekaboo`
- `brew`
- `gh`

The preset installer resolves the remote binary dynamically. If resolution fails, pass `--remote-bin` explicitly.

## Examples

### Wire iMessage Through M1

```bash
scripts/install-preset.sh \
  --tool imsg \
  --host agent1@mac-mini.local
```

### Wire Reminders Through MacBook Pro

```bash
scripts/install-preset.sh \
  --tool remindctl \
  --host agent2@macbook-pro.local \
  --name remindctl-mbp
```

### Use A Custom Binary

```bash
scripts/install-wrapper.sh \
  --name my-mac-tool \
  --host agent2@macbook-pro.local \
  --remote-bin /custom/tools/my-mac-tool
```

## Files

- `scripts/install-wrapper.sh`: create one secure SSH wrapper for a remote binary
- `scripts/install-preset.sh`: install wrappers for common macOS tools with dynamic remote resolution
- `scripts/verify-node-tool.sh`: verify SSH and remote binary availability by path or tool name
- `references/publish-pattern.md`: how to build a publishable wrapper-aware skill on top
- `references/security-model.md`: trust boundaries, least privilege, audit trail, and rollback expectations
