---
name: liu-longterm-memory
version: 1.0.3
description: "Ultimate AI agent memory system for Cursor, Claude, ChatGPT & Copilot. WAL protocol + vector search + git-notes + cloud backup. Never lose context again. Vibe-coding ready."
author: NextFrontierBuilds
keywords: [memory, ai-agent, ai-coding, long-term-memory, vector-search, lancedb, git-notes, wal, persistent-context, claude, claude-code, gpt, chatgpt, cursor, copilot, github-copilot, openclaw, moltbot, vibe-coding, agentic, ai-tools, developer-tools, devtools, typescript, llm, automation]
metadata:
  openclaw:
    emoji: "🧠"
---

# Elite Longterm Memory 🧠

**The ultimate memory system for AI agents.** Combines 6 layers into one bulletproof architecture.

Never lose context. Never forget decisions. Never repeat mistakes.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ELITE LONGTERM MEMORY                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   HOT RAM   │  │  WARM STORE │  │  COLD STORE │             │
│  │             │  │             │  │             │             │
│  │ SESSION-    │  │  LanceDB    │  │  Git-Notes  │             │
│  │ STATE.md    │  │  Vectors    │  │  Knowledge  │             │
│  │             │  │             │  │  Graph      │             │
│  │ (survives   │  │ (semantic   │  │ (permanent  │             │
│  │  compaction)│  │  search)    │  │  decisions) │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │  MEMORY.md  │  ← Curated long-term           │
│                  │  + daily/   │    (human-readable)            │
│                  └─────────────┘                                │
│                          │                                      │
│                          ▼                                      │
│                  ┌─────────────┐                                │
│                  │   Backup    │  ← zip / Git remote (optional) │
│                  │ zip / Gitee │                                │
│                  └─────────────┘                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## The 6 Memory Layers

### Layer 1: HOT RAM (SESSION-STATE.md)
**From: bulletproof-memory**

Active working memory that survives compaction. Write-Ahead Log protocol.

```markdown
# SESSION-STATE.md — Active Working Memory

## Current Task
[What we're working on RIGHT NOW]

## Key Context
- User preference: ...
- Decision made: ...
- Blocker: ...

## Pending Actions
- [ ] ...
```

**Rule:** Write BEFORE responding. Triggered by user input, not agent memory.

### Layer 2: WARM STORE (LanceDB Vectors)
**From: lancedb-memory**

Semantic search across all memories. Auto-recall injects relevant context.

```bash
# Auto-recall (happens automatically)
memory_recall query="project status" limit=5

# Manual store
memory_store text="User prefers dark mode" category="preference" importance=0.9
```

### Layer 3: COLD STORE (Git-Notes Knowledge Graph)
**From: git-notes-memory**

Structured decisions, learnings, and context. Branch-aware.

```bash
# Store a decision (SILENT - never announce)
python3 memory.py -p $DIR remember '{"type":"decision","content":"Use React for frontend"}' -t tech -i h

# Retrieve context
python3 memory.py -p $DIR get "frontend"
```

### Layer 4: CURATED ARCHIVE (MEMORY.md + daily/)
**From: OpenClaw native**

Human-readable long-term memory. Daily logs + distilled wisdom.

```
workspace/
├── MEMORY.md              # Curated long-term (the good stuff)
└── memory/
    ├── 2026-01-30.md      # Daily log
    ├── 2026-01-29.md
    └── topics/            # Topic-specific files
```

### Layer 5: BACKUP (zip / Git Remote) — Optional

Cross-device sync and disaster recovery. Use the CLI commands:

#### zip Backup (简单快速)

```bash
npx liu-longterm-memory backup
# → Creates memory-backup-20260404-153022.zip

npx liu-longterm-memory restore memory-backup-20260404-153022.zip
# → Restores from backup
```

#### Git Remote Backup (推荐，支持版本历史)

```bash
npx liu-longterm-memory backup --git
# → Commits and pushes memory files to your Git remote

# Tip: Use Gitee for domestic users (国内推荐)
# git remote add origin https://gitee.com/your-username/my-memory
```

Benefits:
- **Version history**: Track how decisions evolved over time
- **Cross-device sync**: Pull on any machine
- **Free**: GitHub and Gitee both offer free private repos
- **国内直连**: Gitee 无需代理

### Layer 6: AUTO-EXTRACTION (LLM-Powered)

Automatic fact extraction from conversations using LLM. Two modes:

#### Mode A: Agent-Driven Extraction (零依赖，默认)

No external service needed. The agent follows these rules to auto-extract facts:

| Detected Pattern | Auto-Action |
|-----------------|-------------|
| User states a **preference** | Write to `MEMORY.md ## Preferences` + `memory_store` (importance=0.9) |
| User makes a **decision** | Write to `MEMORY.md ## Decisions Log` + Git-Notes |
| User gives a **deadline/date** | Write to `SESSION-STATE.md ## Key Context` |
| User mentions a **tech stack** | Write to `MEMORY.md ## Projects` |
| User **corrects** the agent | Update `SESSION-STATE.md` + `memory/lessons.md` |
| Session ends | Distill key facts into `memory/YYYY-MM-DD.md` |

#### Mode B: LLM Batch Extraction (智谱免费模型，推荐)

Use ZhipuAI's free GLM-4-Flash model to batch-extract facts from conversation history. Zero cost.

Call the GLM-4-Flash chat completions endpoint with a system prompt:

> "Extract structured facts from the conversation. Return JSON array: [{type, content, importance}]. Types: preference, decision, fact, deadline, correction."

Then write each extracted fact to the appropriate memory layer.

- **Free**: GLM-4-Flash 完全免费，在 https://bigmodel.cn/ 注册获取密钥
- **Automatic**: Extracts preferences, decisions, facts, deadlines
- **国内直连**: No proxy needed
- **80% token reduction** vs raw conversation history

## Quick Setup

### 1. Create SESSION-STATE.md (Hot RAM)

```bash
cat > SESSION-STATE.md << 'EOF'
# SESSION-STATE.md — Active Working Memory

This file is the agent's "RAM" — survives compaction, restarts, distractions.

## Current Task
[None]

## Key Context
[None yet]

## Pending Actions
- [ ] None

## Recent Decisions
[None yet]

---
*Last updated: [timestamp]*
EOF
```

### 2. Enable LanceDB (Warm Store) — Optional

> **No API key required for core memory.** Layers 1/3/4 (SESSION-STATE.md, Git-Notes, MEMORY.md) work without any key. LanceDB vector search is an **optional enhancement**.

Choose your embedding provider in your config file (`~/.openclaw/openclaw.json` or `~/.clawdbot/clawdbot.json`):

#### Option A: ZhipuAI (国内推荐，免费额度充足)

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai-compatible",
    "baseURL": "https://open.bigmodel.cn/api/paas/v4",
    "model": "embedding-3",
    "apiKeyEnv": "ZHIPUAI_API_KEY",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  },
  "plugins": {
    "entries": {
      "memory-lancedb": {
        "enabled": true,
        "config": {
          "autoCapture": false,
          "autoRecall": true,
          "captureCategories": ["preference", "decision", "fact"],
          "minImportance": 0.7
        }
      }
    }
  }
}
```

Register at https://bigmodel.cn/ to get your free key, then set the `ZHIPUAI_API_KEY` environment variable.

#### Option B: Local Ollama (完全免费，离线可用)

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai-compatible",
    "baseURL": "http://localhost:11434/v1",
    "model": "nomic-embed-text",
    "apiKeyEnv": "",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  }
}
```

```bash
# Install and pull embedding model
ollama pull nomic-embed-text
```

#### Option C: Any OpenAI-Compatible API (通用方案)

Works with OpenAI, DeepSeek, Moonshot, 通义千问, or any service with an OpenAI-compatible `/v1/embeddings` endpoint.

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai-compatible",
    "baseURL": "https://api.openai.com/v1",
    "model": "text-embedding-3-small",
    "apiKeyEnv": "OPENAI_API_KEY",
    "sources": ["memory"],
    "minScore": 0.3,
    "maxResults": 10
  }
}
```

Set the environment variable matching your `apiKeyEnv` config (e.g. `OPENAI_API_KEY`, `DEEPSEEK_API_KEY`, or `DASHSCOPE_API_KEY`).

#### Option D: Disabled (纯文件记忆，无需任何 Key)

```json
{
  "memorySearch": {
    "enabled": false
  }
}
```

Memory still works via SESSION-STATE.md, MEMORY.md, Git-Notes, and daily logs — just without vector semantic search.

### 3. Initialize Git-Notes (Cold Store)

```bash
cd ~/clawd
git init  # if not already
python3 skills/git-notes-memory/memory.py -p . sync --start
```

### 4. Verify MEMORY.md Structure

```bash
# Ensure you have:
# - MEMORY.md in workspace root
# - memory/ folder for daily logs
mkdir -p memory
```

### 5. (Optional) Setup Backup

```bash
# Option 1: zip backup (one command)
npx liu-longterm-memory backup

# Option 2: Git remote backup (推荐，支持版本历史)
npx liu-longterm-memory backup --git

# Restore from backup
npx liu-longterm-memory restore memory-backup-20260404.zip
```

## Agent Instructions

### On Session Start
1. Read SESSION-STATE.md — this is your hot context
2. Run `memory_search` for relevant prior context
3. Check memory/YYYY-MM-DD.md for recent activity

### During Conversation (Auto-Extraction)
For every user message, scan for extractable facts and act **BEFORE responding** (WAL):

1. **Preference detected?** → Write to `SESSION-STATE.md` + append to `MEMORY.md ## Preferences` + `memory_store` (importance=0.9)
2. **Decision made?** → Write to `SESSION-STATE.md` + append to `MEMORY.md ## Decisions Log` + Git-Notes (SILENTLY)
3. **Deadline/date given?** → Write to `SESSION-STATE.md ## Key Context`
4. **Tech stack mentioned?** → Append to `MEMORY.md ## Projects`
5. **Correction received?** → Update `SESSION-STATE.md` + log to `memory/lessons.md`
6. **Other concrete detail?** → Write to `SESSION-STATE.md ## Key Context`
7. **Backup requested?** (user says "备份" / "backup" / "save memory") → Run `npx liu-longterm-memory backup` (zip) or `npx liu-longterm-memory backup --git` (Git)

### On Session End
1. Update SESSION-STATE.md with final state
2. Distill session facts into MEMORY.md (if worth keeping long-term)
3. Create/update daily log in memory/YYYY-MM-DD.md with:
   - Tasks completed
   - Decisions made
   - Lessons learned
   - Action items for next session
4. (Optional) If significant changes were made, suggest: `npx liu-longterm-memory backup`

### Memory Hygiene (Weekly)
1. Review SESSION-STATE.md — archive completed tasks
2. Check LanceDB for junk: `memory_recall query="*" limit=50`
3. Clear irrelevant vectors: `memory_forget id=<id>`
4. Consolidate daily logs into MEMORY.md
5. Run backup: `npx liu-longterm-memory backup` or `npx liu-longterm-memory backup --git`

## The WAL Protocol (Critical)

**Write-Ahead Log:** Write state BEFORE responding, not after.

| Trigger | Action |
|---------|--------|
| User states preference | Write to SESSION-STATE.md → then respond |
| User makes decision | Write to SESSION-STATE.md → then respond |
| User gives deadline | Write to SESSION-STATE.md → then respond |
| User corrects you | Write to SESSION-STATE.md → then respond |

**Why?** If you respond first and crash/compact before saving, context is lost. WAL ensures durability.

## Example Workflow

```
User: "Let's use Tailwind for this project, not vanilla CSS"

Agent (internal):
1. Write to SESSION-STATE.md: "Decision: Use Tailwind, not vanilla CSS"
2. Store in Git-Notes: decision about CSS framework
3. memory_store: "User prefers Tailwind over vanilla CSS" importance=0.9
4. THEN respond: "Got it — Tailwind it is..."
```

## Supported Embedding Providers

Any service with an OpenAI-compatible `/v1/embeddings` endpoint works. Tested providers:

| Provider | baseURL | Model | Free Tier |
|----------|---------|-------|-----------|
| **ZhipuAI 智谱** | `https://open.bigmodel.cn/api/paas/v4` | `embedding-3` | 2500 万 tokens 免费 |
| **Ollama (local)** | `http://localhost:11434/v1` | `nomic-embed-text` | 完全免费离线 |
| **OpenAI** | `https://api.openai.com/v1` | `text-embedding-3-small` | Paid |
| **DeepSeek** | `https://api.deepseek.com/v1` | `deepseek-embedding` | Free tier available |
| **通义千问** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `text-embedding-v3` | Free tier available |

## Maintenance Commands

```bash
# Check memory health
npx liu-longterm-memory status

# Create zip backup
npx liu-longterm-memory backup

# Git backup (commit + push)
npx liu-longterm-memory backup --git

# Restore from backup
npx liu-longterm-memory restore memory-backup-20260404.zip

# Audit vector memory
memory_recall query="*" limit=50

# Clear all vectors (nuclear option)
rm -rf ~/.openclaw/memory/lancedb/   # or ~/.clawdbot/memory/lancedb/
openclaw gateway restart

# Export Git-Notes
python3 memory.py -p . export --format json > memories.json

# Check disk usage
du -sh ~/.openclaw/memory/       # or ~/.clawdbot/memory/
wc -l MEMORY.md
ls -la memory/
```

## Why Memory Fails

Understanding the root causes helps you fix them:

| Failure Mode | Cause | Fix |
|--------------|-------|-----|
| Forgets everything | `memory_search` disabled | Enable memorySearch + configure embedding provider (see Setup) |
| Files not loaded | Agent skips reading memory | Add to AGENTS.md rules |
| Facts not captured | No auto-extraction | Ensure Agent follows Auto-Extraction rules (Layer 6) |
| Sub-agents isolated | Don't inherit context | Pass context in task prompt |
| Repeats mistakes | Lessons not logged | Write to memory/lessons.md |

## Solutions (Ranked by Effort)

### 1. Quick Win: Enable memory_search

Enable semantic search with any OpenAI-compatible embedding provider:

```bash
openclaw configure --section web
```

This enables vector search over MEMORY.md + memory/*.md files. See the **Enable LanceDB** section above for provider configuration (ZhipuAI, Ollama, OpenAI, etc.).

### 2. LLM-Powered Auto-Extraction (Recommended)

Use the built-in auto-extraction rules (Layer 6) + optional LLM batch extraction with ZhipuAI's free GLM-4-Flash model. The agent scans each message for preferences, decisions, deadlines, and corrections, then writes them to the appropriate memory layer before responding. See **Layer 6** for setup details.

### 3. Better File Structure (No Dependencies)

```
memory/
├── projects/
│   ├── strykr.md
│   └── taska.md
├── people/
│   └── contacts.md
├── decisions/
│   └── 2026-01.md
├── lessons/
│   └── mistakes.md
└── preferences.md
```

Keep MEMORY.md as a summary (<5KB), link to detailed files.

## Immediate Fixes Checklist

| Problem | Fix |
|---------|-----|
| Forgets preferences | Add `## Preferences` section to MEMORY.md |
| Repeats mistakes | Log every mistake to `memory/lessons.md` |
| Sub-agents lack context | Include key context in spawn task prompt |
| Forgets recent work | Strict daily file discipline |
| Memory search not working | Check your configured env var is set |

## Troubleshooting

**Agent keeps forgetting mid-conversation:**
→ SESSION-STATE.md not being updated. Check WAL protocol.

**Irrelevant memories injected:**
→ Disable autoCapture, increase minImportance threshold.

**Memory too large, slow recall:**
→ Run hygiene: clear old vectors, archive daily logs.

**Git-Notes not persisting:**
→ Run `git notes push` to sync with remote.

**memory_search returns nothing:**
→ Verify your configured env var is set (check `apiKeyEnv` in config)
→ Verify memorySearch enabled in openclaw.json (or clawdbot.json)
→ Verify baseURL and model are correct for your provider

---

## 🇨🇳 国内用户指南

### 安装加速

```bash
# 使用 npmmirror 镜像加速安装
npx --registry https://registry.npmmirror.com liu-longterm-memory init

# 或全局设置镜像
npm config set registry https://registry.npmmirror.com
```

### 服务可用性

| 服务 | 国内可用性 | 说明 |
|------|-----------|------|
| **核心记忆** (SESSION-STATE.md, MEMORY.md, daily logs) | ✅ 完全可用 | 纯本地文件，无网络依赖 |
| **LanceDB + 智谱AI** | ✅ 完全可用 | 智谱国内直连，免费额度充足 |
| **LanceDB + Ollama** | ✅ 完全可用 | 本地运行，无需网络 |
| **LanceDB + DeepSeek** | ✅ 完全可用 | DeepSeek API 国内直连 |
| **Git-Notes** | ✅ 完全可用 | 本地 git 操作 |
| **LLM 事实提取 (GLM-4-Flash)** | ✅ 完全可用 | 智谱免费模型，国内直连 |
| **Backup (zip / Gitee)** | ✅ 完全可用 | zip 本地备份 或 Gitee 远程同步 |
| **ClawdHub** | ✅ 有国内镜像 | 使用 `mirror-cn.clawhub.com` |

### 推荐配置（国内最佳实践）

1. 使用**智谱AI**或**Ollama**作为 embedding provider（见 Setup 章节）
2. 使用**内置 Auto-Extraction** + **GLM-4-Flash**（免费，国内直连）
3. 使用 **zip** 或 **Gitee** 远程仓库备份记忆文件
4. 通过国内镜像安装 npm 包

---

## Links

- bulletproof-memory: https://clawdhub.com/skills/bulletproof-memory
- lancedb-memory: https://clawdhub.com/skills/lancedb-memory
- git-notes-memory: https://clawdhub.com/skills/git-notes-memory
- memory-hygiene: https://clawdhub.com/skills/memory-hygiene
- ClawdHub 国内镜像: https://mirror-cn.clawhub.com

---

*Built by [@NextXFrontier](https://x.com/NextXFrontier) — Part of the Next Frontier AI toolkit*
