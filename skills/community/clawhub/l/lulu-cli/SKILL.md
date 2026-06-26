---
name: lulu-cli
description: >
  Manage LuLu macOS firewall rules from the command line. Use when connections
  are blocked, domains need allowing/blocking, or firewall rules need reviewing.
  Prevents data exfiltration while allowing essential services. Triggers include
  "connection blocked", "allow domain", "firewall rules", "check blocks",
  "lulu", "unblock".
allowed-tools: Bash(lulu-cli:*), Bash(sudo lulu-cli:*)
metadata:
  openclaw:
    os: ["darwin"]
    requires:
      bins: ["lulu-cli"]
    install:
      - id: brew
        kind: brew
        formula: "woop/tap/lulu-cli"
        bins: ["lulu-cli"]
        label: "Install lulu-cli (brew)"
---

# LuLu Firewall CLI

CLI for managing [LuLu](https://objective-see.org/products/lulu.html) macOS firewall rules. LuLu is a free, open-source macOS firewall that blocks unknown outgoing connections.

**Requires:** macOS 13+, LuLu installed, `sudo` for write operations.

## When to Use This Skill

- A network request fails and you suspect it's being blocked by the firewall
- You need to allow a new domain or service through the firewall
- You want to audit what's currently allowed or blocked
- You need to clean up stale or unnecessary rules
- You're setting up a new machine and need to configure firewall rules

## How LuLu Works

LuLu runs as a macOS system extension. When configured in **passive mode** with new connections defaulting to block, any unrecognized outbound connection is silently blocked and logged as a passive rule.

- Rules live in `/Library/Objective-See/LuLu/rules.plist` (NSKeyedArchiver binary format, owned by root)
- The CLI reads/writes this file directly using the same serialization format as LuLu
- The system extension only reads rules at startup, so `reload` (kill + auto-restart) is needed after changes
- New blocks from passive mode appear immediately in `recent` without needing a reload

## Core Workflow

Most usage follows this pattern:

1. **Diagnose** -- check what's being blocked
2. **Fix** -- add allow rules for legitimate domains
3. **Apply** -- reload the extension

```bash
# 1. Check recent blocks
lulu-cli recent 10

# 2. Allow the blocked domain
sudo lulu-cli add --key '*' --path '*' --action allow --addr api.example.com --port 443

# 3. Apply
sudo lulu-cli reload
```

## Commands

### list [filter]

List all firewall rules. Optionally filter by keyword (matches key or binary path).

```bash
lulu-cli list              # all rules
lulu-cli list curl         # rules for curl
lulu-cli list node         # rules for node
lulu-cli list '*'          # global/wildcard rules only
```

No sudo required.

### recent [N]

Show the N most recent block rules, sorted by creation date (newest first). Default: 20.

```bash
lulu-cli recent            # last 20 blocks
lulu-cli recent 5          # last 5 blocks
```

No sudo required. This is the first command to run when diagnosing connection failures.

### add

Add a new firewall rule. Requires sudo.

**Flags:**
- `--key KEY` -- signing identity (e.g. `com.apple.curl`) or `*` for global
- `--path PATH` -- binary path or `*` for global
- `--action allow|block` -- rule action
- `--addr ADDR` -- domain, IP, or regex pattern (default: `*`)
- `--port PORT` -- port number or `*` for any (default: `*`)
- `--regex` -- treat `--addr` as a regex pattern

```bash
# Allow a domain globally (all apps)
sudo lulu-cli add --key '*' --path '*' --action allow --addr example.com --port 443

# Allow a domain and all subdomains (regex)
sudo lulu-cli add --key '*' --path '*' --action allow \
  --addr '^(.+\.)?example\.com$' --port '*' --regex

# Allow for a specific app only
sudo lulu-cli add --key "/usr/bin/curl" --path /usr/bin/curl \
  --action allow --addr example.com --port 443

# Block a domain
sudo lulu-cli add --key '*' --path '*' --action block --addr malicious.com --port '*'
```

### delete

Delete rule(s) by key. Requires sudo.

**Flags:**
- `--key KEY` -- required
- `--uuid UUID` -- specific rule UUID. If omitted, deletes ALL rules for the key.

```bash
# Delete a specific rule by UUID
sudo lulu-cli delete --key "com.apple.curl" --uuid "A1B2C3D4-..."

# Delete ALL rules for a key
sudo lulu-cli delete --key "com.apple.curl"
```

### delete-match

Delete rules matching specific criteria. Requires sudo.

**Flags:**
- `--key KEY` -- required
- `--action allow|block` -- optional filter
- `--addr ADDR` -- optional filter
- `--port PORT` -- optional filter

```bash
# Delete all block rules on port 53 for curl
sudo lulu-cli delete-match --key "com.apple.curl" --action block --port 53
```

### enable / disable

Toggle a rule's enabled state. Requires sudo.

**Flags:**
- `--key KEY` -- required
- `--uuid UUID` -- required

```bash
sudo lulu-cli enable --key '*' --uuid A1B2C3D4-...
sudo lulu-cli disable --key '*' --uuid A1B2C3D4-...
```

### reload

Restart the LuLu system extension to apply rule changes. Requires sudo.

```bash
sudo lulu-cli reload
```

Kills the extension process. macOS auto-restarts registered system extensions within ~8 seconds. There is a brief gap in filtering during the restart.

**Always run `reload` after add, delete, enable, or disable.**

### help

Show usage information.

```bash
lulu-cli help
```

## Key Concepts

- **key**: Signing identity (e.g. `com.apple.curl`) or binary path for unsigned apps. Use `*` for global rules that apply to all apps.
- **action**: `allow` or `block`
- **addr**: Domain name, IP address, regex pattern, or `*` (any)
- **port**: Port number or `*` (any)
- **type**: `default` (system), `apple`, `user` (manually created), `passive` (auto-created from blocked connections)
- **Global rules**: key=`*` and path=`*` apply to all applications

## Rule Policy: Allow-All vs Domain Allowlist

Not all processes should get unrestricted internet access. When using LuLu as a security boundary for AI agents:

**Allow-all (`addr=* port=*`)** -- Only for processes the agent cannot invoke:
- Apple system daemons (apsd, mDNSResponder, trustd, ocspd, etc.)
- User-only apps (Raycast, Zed, LuLu, Bitwarden CLI)
- Network infrastructure (Tailscale, ssh)

**Domain allowlist only** -- Any process an agent could use to reach the internet:
- `node` (Claude Code, OpenClaw runtime)
- `python` / `uv` (agent scripts)
- `curl` (command-line HTTP)
- `git` / `gh` (could push to arbitrary remotes)
- Browser helpers (agent browser automation)

When in doubt, leave a process restricted to the domain allowlist. It's easy to add an allow-all later; harder to notice data leaking through an over-permissive rule.

## Troubleshooting

If a connection is failing:

1. Run `lulu-cli recent` to see if it was blocked
2. If yes, add an allow rule for the domain + port (usually 443 for HTTPS)
3. Run `sudo lulu-cli reload` to apply
4. Retry the connection

If the domain doesn't appear in `recent`, the problem is not the firewall.
