---
name: mjolnir-brain
description: "AI Agent 自进化记忆系统 (Mjolnir Brain)。提供分层记忆架构、Write-Through 即时写入、策略注册表(问题→解法+成功率追踪)、心跳自检、AI 真摘要提炼。核心功能纯本地运行，无网络依赖。备份和 cron 均为可选 opt-in。适用于需要持久记忆、自我学习和自动纠错能力的 AI Agent。"
---

# Mjolnir Brain — AI Agent Self-Evolving Memory System

> **Security model**: Core memory functions are local-only (read/write files in your workspace). No network access, no credentials, no external calls required. Optional backup scripts and cron jobs are strictly opt-in — see [docs/security.md](docs/security.md).

## Prerequisites

The core memory system (templates + strategies.json) requires **no binaries** — it's pure Markdown + JSON read by the agent.

**Optional scripts** (in `scripts/`) require:
- `bash` 4+ — script execution
- `git` — auto_commit.sh
- `grep` — memory_search.sh
- `tar`, `gzip` — memory_consolidate.sh (archiving)
- `curl` — workspace_backup.sh (only if WebDAV backup enabled)
- `ssh`, `scp` — workspace_backup.sh (only if SSH backup enabled)

You can use the core memory system without any of these scripts.

## Quick Setup

```bash
# Copy templates to workspace
cp -r templates/* $WORKSPACE/
cp strategies.json $WORKSPACE/
mkdir -p $WORKSPACE/memory

# Optional: copy automation scripts (review before using!)
cp -r scripts/ $WORKSPACE/scripts/
cp -r playbooks/ $WORKSPACE/
chmod +x $WORKSPACE/scripts/*.sh
```

## Core Components

### 1. Three-Layer Memory
- **Layer 1**: `memory/YYYY-MM-DD.md` — daily session logs (ephemeral)
- **Layer 2**: `MEMORY.md` (≤20KB) + `strategies.json` + `playbooks/` — curated knowledge
- **Layer 3**: `SOUL.md` + `AGENTS.md` + `TOOLS.md` — identity & rules (stable)

### 2. Write-Through Protocol
Write immediately, never defer. Enforced in AGENTS.md:
- Learn something → write to file instantly
- Command fails → check `strategies.json` → update success rate
- Sub-task completes → write findings to `memory/learnings-queue.md`

### 3. Strategy Registry (`strategies.json`)
Problem→solution mapping with success rate tracking:
```bash
# Look up solutions (requires grep)
scripts/strategy_lookup.sh "pip install"
# Update after attempt
scripts/strategy_update.sh pip_install_fail 0 success
```

### 4. Automated Maintenance (OPT-IN cron)

> ⚠️ **All cron jobs are optional.** The core memory system works without them. Review each script before enabling.

```cron
# 0 * * * *  scripts/auto_commit.sh           # hourly git commit (requires: git)
# 0 4 * * *  scripts/memory_consolidate.sh     # clean + archive (requires: tar, gzip)
# 0 4 * * *  scripts/workspace_backup.sh       # remote backup (requires: curl/ssh, credentials)
```

### 5. Search (requires: grep)
```bash
scripts/memory_search.sh "keyword"           # exact search
scripts/memory_search.sh -f "fuzzy term"     # fuzzy search
scripts/memory_search.sh -a "old topic"      # include archives
```

## Session Startup

At the start of each session, the agent reads local workspace files to restore memory context:
1. Read `SOUL.md` — personality definition
2. Read `USER.md` — user profile
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) — recent context
4. **Main session only**: Read `MEMORY.md` — long-term curated memory

> **Privacy safeguard**: `MEMORY.md` is loaded **only in private main sessions** (1:1 with the user). It is **never loaded** in group chats, shared channels, or multi-party contexts to prevent data leakage. All files are local to the workspace — no data is sent externally.

## File Reference
| File | Purpose | Load Context |
|------|---------|-------------|
| `SOUL.md` | Personality | Every session (local read) |
| `AGENTS.md` | Behavior rules + Write-Through | Every session (local read) |
| `USER.md` | User profile | Every session (local read) |
| `MEMORY.md` | Long-term curated memory (≤20KB) | **Main session only** (never in group/shared) |
| `IDENTITY.md` | Name, vibe, emoji | On reference |
| `TOOLS.md` | Environment config | On reference |
| `HEARTBEAT.md` | Periodic checks + idle queue | On heartbeat (opt-in) |
| `BOOTSTRAP.md` | First-run setup (delete after) | First session only |
| `strategies.json` | Problem→solution registry | On error |
| `playbooks/` | Parameterized runbooks | On repeated operation |

## Docs
- `docs/architecture.md` — System design and data flow
- `docs/self-learning.md` — Four learning mechanisms explained
- `docs/best-practices.md` — Tips and common pitfalls
- `docs/security.md` — Security model and privacy safeguards
