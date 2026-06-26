---
name: moltcare-open
description: Install and configure the MoltCare Agent Framework - a four-layer configuration system (SOUL/AGENTS/USER/MEMORY) with three-layer trigger architecture (Exact + Semantic + Agent Evaluation) and PUA problem-solving framework. Use when the user wants to set up or configure OpenClaw Agent with structured personality, intelligent memory triggers, proactive problem-solving, and multi-expert decision modes. Triggers on phrases like 'install moltcare', 'setup agent framework', 'configure openclaw personality', 'set up memory triggers', or when the user needs a complete Agent configuration system.
---

# MoltCare-Open Skill

> 🦞 **OpenClaw Skill** - v3.2.0 | Auto-published via GitHub Actions

Install and configure the MoltCare Agent Framework for OpenClaw.

## What is MoltCare?

MoltCare is a four-layer configuration framework that transforms OpenClaw Agent from passive execution to proactive problem-solving:

```
┌─────────────────────────────────────────┐
│  SOUL.md        ← Agent 灵魂（原则、人格） │
├─────────────────────────────────────────┤
│  AGENTS.md      ← 操作手册（流程、工具）   │
├─────────────────────────────────────────┤
│  USER.md        ← 用户画像（偏好、约束）   │
├─────────────────────────────────────────┤
│  MEMORY.md      ← 长期记忆（核心信息）     │
└─────────────────────────────────────────┘
```

## Core Features

### 1. Three-Layer Trigger Architecture (AGENTS.md v3.2)

| Layer | Trigger | Signal | Priority |
|-------|---------|--------|----------|
| **Layer 1** | Exact triggers | +2 | 🔴 Highest |
| **Layer 2** | Semantic triggers | +1 | 🟡 Medium |
| **Layer 3** | Agent self-evaluation | Auto | 🟢 Lowest |

**Layer 1 - Exact Triggers:**
- `多专家讨论:` → Multi-expert mode [🧠]
- `这很重要` → High priority memory [⭐]
- `记住这个` → Learning debt [💾]
- `我偏好` → User preference [👤]

**Layer 2 - Semantic Triggers:**
- "关键是..." / "核心在于..." → Key info [⭐]
- "别忘了..." / "要记住..." → Learning debt [💾]
- "我喜欢..." / "我讨厌..." → Preference [👤]
- "还不行" / "太慢了" → PUA activation [🔥]

**Layer 3 - Agent Evaluation:**
After task completion, self-evaluate 7 questions and auto-record if ≥2 criteria met.

### 2. PUA Problem-Solving Framework

**Three Iron Laws:**
1. **Exhaust all options** - Never say "cannot solve" until all tried
2. **Act first, ask later** - Use tools before asking user
3. **Take ownership** - End-to-end delivery

**Pressure Escalation (L1-L4):**
- L1: "Try again" / "Another approach"
- L2: "Why still not working" / 2 failures
- L3: "You can't do it" / 3+ failures + 7-item checklist
- L4: "Cannot solve" / 5+ failures →拼命模式

### 3. Multi-Expert Decision System

Automatically activate for:
- Architecture design
- Security/risk assessment
- Complex trade-offs

**Experts:** 🔍 Researcher → 🧠 Architect → 💻 Engineer → 👑 Captain

### 4. Task Layering & Cost Optimization

Intelligent task execution with minimal token consumption:

| Layer | Task Type | Execution | Token Cost |
|-------|-----------|-----------|------------|
| **L0** | Data collection, polling, formatting | Pure script | Zero |
| **L1** | Query, display, status checks | Pure script | Zero |
| **L2** | Anomaly detection, threshold checks | Script + conditional trigger | On-demand |
| **L3** | Analysis, decision-making, summarization | AI invocation | Normal |

**Principle**: Push computation to scripts; reserve AI for judgment.

**Benefits**:
- 90%+ reduction in token consumption for routine tasks
- Faster response times (no model latency)
- Predictable operational costs
- Scalable automation

### 5. Daily Token Optimization Audit

Automated daily review of tasks and workflows to identify optimization opportunities:

**What it checks**:
| Check Item | Purpose |
|------------|---------|
| **Repetitive AI tasks** | Identify tasks that could be scripted |
| **High-frequency queries** | Find patterns for caching/pre-computation |
| **Threshold-based decisions** | Detect rules that could be automated |
| **Data processing workflows** | Spot opportunities for batch/aggregate processing |

**Daily Checklist**:
```markdown
□ Review yesterday's token usage patterns
□ Identify tasks with >3 similar executions
□ Check for threshold-based decisions using AI
□ Look for data formatting/processing done by AI
□ Find opportunities for incremental updates
```

**Optimization Report Template**:
```markdown
## [Date] Token Optimization Report

### Findings
| Task | Current | Suggested | Savings |
|------|---------|-----------|---------|
| [Name] | AI every call | Script + cache | ~X% |

### Action Items
- [ ] [Task]: Convert to L0/L1/L2
- [ ] [Task]: Add caching layer
- [ ] [Task]: Implement incremental updates
```

**Auto-trigger**: Daily at configured time or manual via "检查token优化"

## Installation

### Step 1: Copy Templates (⚠️ Important: Copy to ROOT, not subfolders)

OpenClaw **automatically loads** these files from workspace root at session start:

**CORE (required):**
```
~/.openclaw/workspace/
├── AGENTS.md      ← Operation manual (auto-loaded)
├── SOUL.md        ← Agent principles (auto-loaded)
├── USER.md        ← User profile (auto-loaded)
└── MEMORY.md      ← Long-term memory (auto-loaded)
```

**OPTIONAL (loaded if exists):**
```
~/.openclaw/workspace/
├── IDENTITY.md    ← Agent identity (auto-loaded)
├── TOOLS.md       ← Environment tools (auto-loaded)
└── HEARTBEAT.md   ← Health check system (auto-loaded)
```

**MEMORY templates (read on-demand):**
```
~/.openclaw/workspace/memory/
├── learning-debt.md      (read via `read` tool)
├── constraints.md        (read via `read` tool)
├── preferences.md        (read via `read` tool)
└── token-audit-template.md  (read via `read` tool)
```

**❌ WRONG - Do NOT do this:**
```bash
# Wrong - creates subfolders
mkdir -p ~/.openclaw/workspace/core
mkdir -p ~/.openclaw/workspace/assets
cp assets/* ~/.openclaw/workspace/core/  # ❌ WRONG
```

**✅ CORRECT (or use install.sh):**
```bash
# Core templates → ROOT (auto-loaded by OpenClaw)
cp assets/AGENTS.md ~/.openclaw/workspace/
cp assets/SOUL.md ~/.openclaw/workspace/
cp assets/USER.md ~/.openclaw/workspace/
cp assets/MEMORY.md ~/.openclaw/workspace/

# Optional templates → ROOT (auto-loaded if exists)
cp assets/IDENTITY.md ~/.openclaw/workspace/
cp assets/TOOLS.md ~/.openclaw/workspace/
cp assets/HEARTBEAT.md ~/.openclaw/workspace/

# Memory templates → memory/ (read on-demand)
mkdir -p ~/.openclaw/workspace/memory
cp assets/learning-debt.md ~/.openclaw/workspace/memory/
cp assets/constraints.md ~/.openclaw/workspace/memory/
cp assets/preferences.md ~/.openclaw/workspace/memory/
cp assets/token-audit-template.md ~/.openclaw/workspace/memory/

# Note: BEST_PRACTICES.md stays in skill/assets/ (reference only, not auto-loaded)
```

### Step 2: Configure User Profile

Edit `~/.openclaw/workspace/USER.md` and fill in:
- Your name/role
- Communication preferences
- Technical level
- Constraints and boundaries

### Step 3: Initialize Memory System

Create today's memory file:

```bash
mkdir -p ~/.openclaw/workspace/memory
echo "# $(date +%Y-%m-%d) Memory Flush" > ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

### Step 4: Configure Weekly Token Audit (Auto-configured)

Token optimization audit is **automatically configured** during installation:

**Default Schedule**: Every Monday at 03:00 (cron)
```
0 3 * * 1 cd ~/.openclaw/workspace && echo '检查token优化' >> ~/.openclaw/workspace/.audit-trigger
```

**Trigger methods**:
1. **Automatic** - Runs every Monday 03:00 via cron
2. **Manual** - Say "检查token优化" anytime
3. **Custom period** - Say "检查本周token优化" or "检查本月token优化"

**To change schedule**, edit crontab:
```bash
crontab -e
# Change: 0 3 * * 1 (Monday 03:00)
# To daily: 0 3 * * * (daily 03:00)
# To disable: Comment out or remove the line
```

## File Reference

### CORE Configuration (Auto-loaded by OpenClaw)

**Must be in `~/.openclaw/workspace/` root.**

| File | Purpose | Key Content | Required |
|------|---------|-------------|----------|
| **AGENTS.md** | Operation manual | 3-layer triggers, multi-expert, PUA levels | ✅ Required |
| **SOUL.md** | Agent soul & principles | 7 principles, PUA framework, safety rules | ✅ Required |
| **USER.md** | User profile | Preferences, constraints, communication style | ✅ Required |
| **MEMORY.md** | Long-term memory | High-signal info (Signal 8-10) | ✅ Required |

### OPTIONAL Configuration (Auto-loaded if exists)

**Placed in `~/.openclaw/workspace/` root. Loaded only if file exists.**

| File | Purpose | Key Content |
|------|---------|-------------|
| **IDENTITY.md** | Agent identity | Display name, emoji, role definition |
| **TOOLS.md** | Environment tools | Local tool versions, API keys, commands |
| **HEARTBEAT.md** | Health check system | Quick status checks |
| **TOKEN_AUDIT.md** | Weekly audit config | Token optimization schedule, thresholds |
| **CONFIG_CHECKLIST.md** | Post-install verification | How to use all md files correctly |

### MEMORY Templates (Read on-demand)

**Placed in `~/.openclaw/workspace/memory/`. Read via `read` tool when needed.**

| File | Purpose |
|------|---------|
| **learning-debt.md** | Topics to learn (Signal 6+) |
| **constraints.md** | Absolute boundaries |
| **preferences.md** | Preference change log |
| **token-audit-template.md** | Daily token optimization review template |

### Reference Documentation (Not auto-loaded)

**Stay in `skill/assets/`. Read manually when needed.**

| File | Purpose |
|------|---------|
| **BEST_PRACTICES.md** | Efficiency guide - Task layering, token optimization |
| **README.md** | This documentation |

## Quick Start

After installation, test the framework:

1. **Test Layer 1 trigger:**
   ```
   用户: "这很重要，我偏好简洁的回答"
   Agent: [⭐] 已记录核心偏好: 简洁回答
   ```

2. **Test Layer 2 trigger:**
   ```
   用户: "关键是配置要正确，别忘了备份"
   Agent: [⭐] 记录关键信息: 配置要正确
          [💾] 添加到学习债务: 别忘了备份
   ```

3. **Test Multi-Expert mode:**
   ```
   用户: "多专家讨论: 如何设计一个高并发系统"
   Agent: [🧠 多专家模式]
          🔍 研究员: ...
          🧠 架构师: ...
          💻 工程师: ...
          👑 队长: ...
   ```

## Updating

To update the framework while preserving your configurations:

1. Backup your USER.md and MEMORY.md
2. Reinstall the skill
3. Merge your custom configurations back

## Resources

All templates are in `assets/` directory:
- Core templates: SOUL.md, AGENTS.md, USER.md, MEMORY.md, HEARTBEAT.md
- Memory templates: learning-debt.md, constraints.md, preferences.md

## Version

v3.2 - Task Layering & Cost Optimization
