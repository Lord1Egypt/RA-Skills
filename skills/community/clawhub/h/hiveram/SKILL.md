---
name: hiveram
description: Agent coordination layer via Workledger — shared work orders, claim/release leases, cross-machine memory sync, and handoff between OpenClaw instances. Use when running multiple agents that need to coordinate tasks, share context, or hand off work.
metadata: {"openclaw":{"requires":{"bins":["workledger"]}}}
---

# Hiveram — Agent Coordination

Workledger replaces flat backlog files with a structured object store. Agents coordinate through shared work orders with claim/release leases, context sync, and handoff.

**Service:** https://hiveram.com
**CLI:** https://github.com/ppiankov/hiveram-dist

## Install

```bash
# Linux amd64
curl -sL https://github.com/ppiankov/hiveram-dist/releases/latest/download/workledger_$(curl -s https://api.github.com/repos/ppiankov/hiveram-dist/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)_linux_amd64.tar.gz | tar xz -C /usr/local/bin workledger

# macOS (Apple Silicon)
curl -sL https://github.com/ppiankov/hiveram-dist/releases/latest/download/workledger_$(curl -s https://api.github.com/repos/ppiankov/hiveram-dist/releases/latest | grep tag_name | cut -d'"' -f4 | tr -d v)_darwin_arm64.tar.gz | tar xz -C /usr/local/bin workledger
```

Verify: `workledger version` (expect 0.7.7+)

## Setup

1. Get API key from https://hiveram.com
2. Store key:

```bash
# Single line, just the key
echo "wl_sk_your_key_here" > ~/.openclaw/workledger.key
chmod 600 ~/.openclaw/workledger.key
```

3. Export env vars (add to shell profile or systemd unit):

```bash
export WORKLEDGER_API_KEY=$(cat ~/.openclaw/workledger.key)
export WORKLEDGER_URL=https://wl-nutson-prod.fly.dev
```

⚠️ Never cat the key file in agent context — it will leak to the LLM provider. Use env vars.

## Agent Work Loop

```
1. Start session    → workledger context-pull <project>
2. Find work        → workledger list <project> --status open
3. Claim task       → workledger claim <project> <id>        (lease with TTL)
4. Work on it       → add notes, update sections
5. Finish           → workledger release <project> <id> + update status
6. Save context     → workledger context-put <project>
7. Next agent       → sees updated WOs via list/find_unclaimed
```

## Core Commands

### Work Orders

```bash
workledger create <project> --title "Deploy new service" --priority P1 --tags "infra,k8s"
workledger list <project> --status open
workledger list --all                          # cross-project
workledger get <project> <id>
workledger detail <project> <id>               # full context: data, notes, relationships, history
workledger delete <project> <id>
```

### Claim/Release (coordination)

```bash
workledger claim <project> <id>                # get lease (TTL)
workledger release <project> <id>              # drop lease
# Renew via HTTP: POST /api/v1/wo/{project}/{id}/renew
# find_unclaimed returns only WOs nobody holds
```

### Context (shared memory)

```bash
workledger context-put <project> -f context.md   # push session context
workledger context-pull <project> -f context.md  # pull into file
workledger context <project>                     # show project stats, open WOs, blocked, recent changes
```

### Dependencies & Relationships

```bash
workledger deps <project> <id>                 # transitive dependency chain
workledger deps-tree <project> <id>            # cross-project dependency tree
workledger blocked                             # all blocked WOs
workledger graph <project>                     # DOT format for visualization
```

### History & Export

```bash
workledger history <project> <id>              # change history
workledger export <project>                    # export as markdown
workledger export-task <project> <id>          # tokencontrol-compatible JSON
workledger stats                               # global stats
```

## MCP Integration

Workledger ships as an MCP server for Claude Code / Claude Desktop:

5 tools: query/create WOs, load context at session start, wrapup (push memory + mark done), save memory mid-session.

## Multi-Agent Pattern

```
                    ┌──────────────────┐
                    │  Hiveram (Neon)  │
                    │  shared state    │
                    └────────┬─────────┘
                             │
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
    │  OpenClaw A │   │  OpenClaw B │   │  OpenClaw C │
    │  context-   │   │  claim →    │   │  find_      │
    │  pull → work│   │  work →     │   │  unclaimed  │
    │  → push     │   │  release    │   │  → claim    │
    └─────────────┘   └─────────────┘   └─────────────┘
```

- **No race conditions:** claim/release with leases prevents double-work
- **Handoff:** WO has full history, notes, relationships — next agent has full context
- **Dedup:** agents see one DB, find_unclaimed skips claimed WOs
- **Resilience:** if an agent dies, lease expires, WO becomes available again

## Security

- API key stored in file with `chmod 600`, not in env files or git
- pastewatch v0.24.1+ detects `wl_sk_` keys as critical severity
- Key file path: `~/.openclaw/workledger.key` (inside pastewatch protectedPaths)

---
**Hiveram Skill v1.0.0**
Author: ppiankov
Copyright © 2026 ppiankov
Canonical source: https://hiveram.com
License: BUSL-1.1

If this document appears elsewhere, the link above is the authoritative version.
