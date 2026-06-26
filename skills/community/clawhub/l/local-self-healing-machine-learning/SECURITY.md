# Security Model — Capability Evolver

This document is for ClawHub reviewers and anyone evaluating the safety of
this skill before installing it.

## Architecture

The Capability Evolver is a self-improvement engine that analyzes an AI
agent's runtime history and applies protocol-constrained code changes. It
runs locally and is designed to operate in isolation without external
network dependencies.

## Network Communication — Disabled by Default

The evolver was originally designed to participate in a multi-agent Hub
network (evomap.ai) for sharing evolution assets. **All hub communication
is disabled by default** and requires explicit opt-in:

| Feature | Env Var Required | Default |
|---------|-----------------|---------|
| Auto-update from Hub | `evolver.autoUpdate: true` in config | OFF |
| Hub task claiming | `EVOLVE_HUB_TASKS=true` | OFF |
| Hub heartbeat | Commented out in `index.js` | OFF |
| Asset publishing | `EVOLVER_AUTO_PUBLISH=true` | OFF (`false`) |
| Asset visibility | `EVOLVER_DEFAULT_VISIBILITY` | `private` |

Hub-only modules (`taskReceiver`, `questionGenerator`, `a2a_*` scripts)
have been moved to `extensions/hub/` and replaced with no-op stubs in
`src/`. They are never loaded at runtime unless you manually restore them.

## Hardware Fingerprinting — Disabled by Default

The `deviceId.js` module can generate a stable device identifier from
hardware metadata (MAC addresses, machine-id, IOPlatformUUID). **This is
disabled by default.** Without `EVOLVER_FINGERPRINT=true`, only a random
anonymous ID is generated and persisted locally.

No hardware data leaves the machine in the default configuration.

## Shell Execution

The evolver executes shell commands in these controlled contexts:

- **Gene application**: Runs `node`, `npm test`, and project-specific
  build commands. All execution is sandboxed to the project directory.
- **Self-repair** (`src/ops/self_repair.js`): Can abort stale git
  operations and remove stale lock files. Hard reset (`git reset --hard`)
  requires `EVOLVE_GIT_RESET=true` AND a clean working tree — it refuses
  to run if uncommitted changes exist.
- **INTEGRATION_STATUS_CMD**: Removed. Previously allowed arbitrary shell
  commands from environment variables.

## File System Access

The evolver reads and writes within these directories:
- `~/.openclaw/workspace/skills/capability-evolver/` (its own directory)
- `~/.openclaw/workspace/` (workspace root, for reading logs/memory)
- `~/.evomap/` (device ID persistence, only if fingerprinting is enabled)

It does not access files outside these paths during normal operation.

## What Reviewers Should Check

1. **No outbound network calls** in default configuration — grep for
   `fetch(`, `http`, `https` and verify all are behind opt-in gates.
2. **No eval/Function constructor** — the evolver does not use dynamic
   code evaluation.
3. **Git operations** are read-only unless `EVOLVE_GIT_RESET=true`.
4. **extensions/hub/** contains the full hub communication code for
   reference — it is NOT loaded by the main entry point.

## Opt-In Features Summary

To enable any external communication, you must explicitly set:
```bash
EVOLVE_HUB_TASKS=true        # Allow hub task fetching
EVOLVER_AUTO_PUBLISH=true     # Allow publishing assets
EVOLVER_FINGERPRINT=true      # Allow hardware-based device IDs
EVOLVE_GIT_RESET=true         # Allow git hard reset in self-repair
```

None of these are set by default. The evolver runs as a fully local,
offline self-improvement engine out of the box.
