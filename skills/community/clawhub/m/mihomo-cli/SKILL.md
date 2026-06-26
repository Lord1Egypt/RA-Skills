---
name: mihomo-cli
description: Inspect and operate a local Mihomo/Clash.Meta/Clash Verge/ClashMac instance through its REST API. Use when the user asks to check proxy status, list nodes, read delay/latency history, switch proxy groups, inspect active connections, flush DNS/FakeIP cache, restart Mihomo, or discover where Mihomo is installed/running on the machine.
---

Use the bundled script for repeatable Mihomo operations instead of re-discovering paths and API auth each time.

## Quick start

Run:

```bash
scripts/mihomo-cli.sh status
```

The script auto-detects common Mihomo installs by checking:
- `~/Library/Application Support/clashmac/work/config.yaml`
- `~/.config/mihomo/config.yaml`
- `~/.config/clash/config.yaml`

It extracts:
- `external-controller`
- `secret`

## Common commands

```bash
scripts/mihomo-cli.sh status
scripts/mihomo-cli.sh proxies
scripts/mihomo-cli.sh groups
scripts/mihomo-cli.sh test
scripts/mihomo-cli.sh test "🇭🇰 E0 香港核心"
scripts/mihomo-cli.sh connections
scripts/mihomo-cli.sh flush dns
scripts/mihomo-cli.sh flush fakeip
scripts/mihomo-cli.sh restart
scripts/mihomo-cli.sh config
```

## When switching a group

1. List groups first:

```bash
scripts/mihomo-cli.sh groups
```

2. Switch the selector/group to a target proxy:

```bash
scripts/mihomo-cli.sh switch GLOBAL "🇭🇰 E0 香港核心"
```

Use exact group and proxy names.

## For latency / node quality questions

Default to:

```bash
scripts/mihomo-cli.sh proxies
```

This shows the latest recorded delay from Mihomo's history.

If the user wants a live test for one node, run:

```bash
scripts/mihomo-cli.sh test "<proxy-name>"
```

Treat `0ms` with caution: it may indicate missing/failed measurement rather than a truly perfect route.

## For deeper API work

Read `references/api.md` when you need raw endpoint details, request shapes, or want to call an endpoint not wrapped by the helper script.

## Practical notes

- Prefer read-only commands first (`status`, `proxies`, `groups`, `connections`) before mutating state.
- Before `switch` or `restart`, be sure that changing the active route is actually what the user wants.
- If API requests return `Unauthorized`, re-check `secret` from the detected config.
- If the script cannot find config automatically, inspect running processes for `mihomo`, `clash`, `verge`, or `clashmac`, then locate the active config path from process args.
- On macOS with ClashMac, the real core may run as `mihomo` under `~/Library/Application Support/clashmac/core/` while the GUI runs as `ClashMac.app`.

## Useful fallback detection

When auto-detect fails, use:

```bash
ps aux | grep -iE "clash|mihomo|verge" | grep -v grep
```

Then inspect the config path from the process command line.
