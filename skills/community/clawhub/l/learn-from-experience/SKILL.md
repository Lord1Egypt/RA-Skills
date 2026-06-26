---
name: learn-from-experience
slug: learn-from-experience
version: 1.3.0
description: "Learn from experience: self-reflection + self-criticism + self-learning + self-organizing memory + cross-session sync. Agent evaluates its own work, catches mistakes, and improves permanently. Compiles confirmed learnings to global config for automatic cross-session persistence. Use when (1) a command, tool, API, or operation fails; (2) the user corrects you or rejects your work; (3) you realize your knowledge is outdated or incorrect; (4) you discover a better approach; (5) the user explicitly installs or references the skill for the current task."
changelog: "v1.3.0: Rebrand to learn-from-experience. Add cross-session memory sync protocol — compile confirmed preferences to agent global config for automatic loading in new sessions. Multi-agent compatibility: Claude Code, OpenClaw, Codex, CodeBuddy, opencode."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/learn-from-experience/"],"configPaths.optional":["./AGENTS.md","./SOUL.md","./HEARTBEAT.md"]}}
---

## When to Use

User corrects you or points out mistakes. You complete significant work and want to evaluate the outcome. You notice something in your own output that could be better. Knowledge should compound over time without manual maintenance.

## Supported Agent Products

This skill is agent-agnostic. It works with any product that loads a global config file on session start.

| Product | Skill Install Path | Global Config File | Global Config Path |
|---------|-------------------|--------------------|-------------------|
| Claude Code | `~/.claude/skills/learn-from-experience/` | `CLAUDE.md` | `~/.claude/CLAUDE.md` |
| OpenClaw | `~/.openclaw/skills/learn-from-experience/` | `AGENTS.md` | `~/.openclaw/AGENTS.md` |
| Codex | `~/.codex/skills/learn-from-experience/` | `AGENTS.md` | `~/.codex/AGENTS.md` |
| CodeBuddy | `~/.codebuddy/skills/learn-from-experience/` | `CODEBUDDY.md` | `~/.codebuddy/CODEBUDDY.md` |
| opencode | `~/.config/opencode/skills/learn-from-experience/` | `AGENTS.md` | `~/.config/opencode/AGENTS.md` |

The skill auto-detects which product is running by checking which config path exists. Memory data always lives in `~/learn-from-experience/` (shared across all products).

## Architecture

Memory lives in `~/learn-from-experience/` with tiered structure. If `~/learn-from-experience/` does not exist, run `setup.md`.
Workspace setup should add the standard steering to the workspace AGENTS, SOUL, and `HEARTBEAT.md` files, with recurring maintenance routed through `heartbeat-rules.md`.
Confirmed preferences are compiled to the agent's global config `### Patterns` section for cross-session persistence (see Sync Protocol below).

```
~/learn-from-experience/
├── memory.md          # HOT: <=100 lines, always loaded
├── index.md           # Topic index with line counts + sync status
├── heartbeat-state.md # Heartbeat state: last run, reviewed change, action notes
├── projects/          # Per-project learnings
├── domains/           # Domain-specific (code, writing, comms)
├── archive/           # COLD: decayed patterns
└── corrections.md     # Last 50 corrections log
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Heartbeat state template | `heartbeat-state.md` |
| Memory template | `memory-template.md` |
| Workspace heartbeat snippet | `HEARTBEAT.md` |
| Heartbeat rules | `heartbeat-rules.md` |
| Learning mechanics | `learning.md` |
| Security boundaries | `boundaries.md` |
| Scaling rules | `scaling.md` |
| Memory operations | `operations.md` |
| Self-reflection log | `reflections.md` |

## Requirements

- No credentials required
- No extra binaries required
- Agent must have a global config file that auto-loads on session start

## Learning Signals

Log automatically when you notice these patterns:

**Corrections** -> add to `corrections.md`, evaluate for `memory.md`:
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "I prefer X, not Y"
- "Remember that I always..."
- "I told you before..."
- "Stop doing X"
- "Why do you keep..."
- "bu dui, bu shi zhe yang de......"
- "shi ji shang, ying gai shi......"
- "ni gao cuo le......"
- "wo geng xi huan X, bu shi Y"
- "ji zhu wo yong yuan dou yao......"
- "wo zhi qian gen ni shuo guo......"
- "bie zai zuo X le"
- "ni wei shen me yi zhi......"

**Preference signals** -> add to `memory.md` if explicit:
- "I like when you..."
- "Always do X for me"
- "Never do Y"
- "My style is..."
- "For [project], use..."
- "ni zhe yang...de shi hou wo jue de hen hao"
- "yi ding yao bang wo zuo X"
- "yong yuan bu yao zuo Y"
- "wo de feng ge shi......"
- "zai [xiang mu] zhong yao yong......"

**Pattern candidates** -> track, promote after 3x:
- Same instruction repeated 3+ times
- Workflow that works well repeatedly
- User praises specific approach

**Ignore** (don't log):
- One-time instructions ("do X now")
- Context-specific ("in this file...")
- Hypotheticals ("what if...")

## Self-Reflection

After completing significant work, pause and evaluate:

1. **Did it meet expectations?** -- Compare outcome vs intent
2. **What could be better?** -- Identify improvements for next time
3. **Is this a pattern?** -- If yes, log to `corrections.md`

**When to self-reflect:**
- After completing a multi-step task
- After receiving feedback (positive or negative)
- After fixing a bug or mistake
- When you notice your output could be better

**Log format:**
```
CONTEXT: [type of task]
REFLECTION: [what I noticed]
LESSON: [what to do differently]
```

**Example:**
```
CONTEXT: Flutter UI build
REFLECTION: Spacing was wrong, had to redo
LESSON: Check visual spacing before showing to user
```

Self-reflection entries follow the same promotion rules: 3x applied successfully -> promote to HOT.

## Quick Queries

| User says | Action |
|-----------|--------|
| "What do you know about X?" | Search all tiers for X |
| "What have you learned?" | Show last 10 from `corrections.md` |
| "Show my patterns" | List `memory.md` (HOT) |
| "Show [project] patterns" | Load `projects/{name}.md` |
| "What's in warm storage?" | List files in `projects/` + `domains/` |
| "Memory stats" | Show counts per tier |
| "Forget X" | Remove from all tiers (confirm first) |
| "Export memory" | ZIP all files |
| "Sync memory" / "sync" | Run cross-session sync now |

## Memory Stats

On "memory stats" request, report:

```
Learn-from-Experience Memory

HOT (always loaded):
  memory.md: X entries

WARM (load on demand):
  projects/: X files
  domains/: X files

COLD (archived):
  archive/: X files

Cross-session sync:
  Last sync: YYYY-MM-DD
  Status: in_sync | stale

Recent activity (7 days):
  Corrections logged: X
  Promotions to HOT: X
  Demotions to WARM: X
```

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Learning from silence | Creates false rules | Wait for explicit correction or repeated evidence |
| Promoting too fast | Pollutes HOT memory | Keep new lessons tentative until repeated |
| Reading every namespace | Wastes context | Load only HOT plus the smallest matching files |
| Compaction by deletion | Loses trust and history | Merge, summarize, or demote instead |

## Core Rules

### 1. Learn from Corrections and Self-Reflection
- Log when user explicitly corrects you
- Log when you identify improvements in your own work
- Never infer from silence alone
- After 3 identical lessons -> ask to confirm as rule

### 2. Tiered Storage
| Tier | Location | Size Limit | Behavior |
|------|----------|------------|----------|
| HOT | memory.md | <=100 lines | Always loaded |
| WARM | projects/, domains/ | <=200 lines each | Load on context match |
| COLD | archive/ | Unlimited | Load on explicit query |

### 3. Automatic Promotion/Demotion
- Pattern used 3x in 7 days -> promote to HOT
- Pattern unused 30 days -> demote to WARM
- Pattern unused 90 days -> archive to COLD
- Never delete without asking

### 4. Namespace Isolation
- Project patterns stay in `projects/{name}.md`
- Global preferences in HOT tier (memory.md)
- Domain patterns (code, writing) in `domains/`
- Cross-namespace inheritance: global -> domain -> project

### 5. Conflict Resolution
When patterns contradict:
1. Most specific wins (project > domain > global)
2. Most recent wins (same level)
3. If ambiguous -> ask user

### 6. Compaction
When file exceeds limit:
1. Merge similar corrections into single rule
2. Archive unused patterns
3. Summarize verbose entries
4. Never lose confirmed preferences

### 7. Transparency
- Every action from memory -> cite source: "Using X (from projects/foo.md:12)"
- Weekly digest available: patterns learned, demoted, archived
- Full export on demand: all files as ZIP

### 8. Security Boundaries
See `boundaries.md` -- never store credentials, health data, third-party info.

### 9. Graceful Degradation
If context limit hit:
1. Load only memory.md (HOT)
2. Load relevant namespace on demand
3. Never fail silently -- tell user what's not loaded

## Cross-Session Sync Protocol

### Problem
Memory in `~/learn-from-experience/memory.md` is only loaded when the skill is activated.
The agent's global config file is automatically loaded every session.
Without sync, learnings from one session are invisible to the next.

### Solution
Compile confirmed preferences from `memory.md` into the global config's `### Patterns` section under `## Learnings`. This is a one-way compile: memory.md is the source of truth, global config is the read-only cache.

### When to Sync
- After recording a user correction to Confirmed Preferences
- After promote/demote/compact operations on memory.md
- User explicitly says "sync memory"
- Session end self-reflection if new confirmed rules were added this session

### Sync Rules
1. **Source**: Only `## Confirmed Preferences` entries from memory.md
2. **Format**: Each entry compiles to `- [tag] one-line description`
3. **Target**: `### Patterns` block under `## Learnings` in agent's global config
4. **Limit**: Max 30 lines; if exceeded, keep only HIGH priority + highest confidence entries
5. **Safety**: Only replace content between `### Patterns` header and the next `###` or `##` header. Never touch other global config content
6. **Timestamp**: Include sync timestamp in HTML comment after `### Patterns` header
7. **Stale detection**: On session start, check `~/learn-from-experience/index.md` sync status. If `stale`, auto-sync

### Sync Flow
```
1. Read ~/learn-from-experience/memory.md -> extract ## Confirmed Preferences
2. Compile each entry: "### title | confidence" -> "- [tag] description"
3. Detect agent product -> locate global config file
4. Read global config file
5. Find ### Patterns block (create if missing, under ## Learnings)
6. Replace block content (preserve everything else)
7. Update ~/learn-from-experience/index.md sync timestamp + status
```

### Agent Detection
To find the correct global config file:
```
Check in order (first existing path wins):
1. ~/.claude/CLAUDE.md              (Claude Code)
2. ~/.openclaw/AGENTS.md            (OpenClaw)
3. ~/.codex/AGENTS.md               (Codex)
4. ~/.codebuddy/CODEBUDDY.md        (CodeBuddy)
5. ~/.config/opencode/AGENTS.md     (opencode)
```
If multiple exist, sync to all of them (user may use multiple products).

## Session Lifecycle

```
Session Start:
  1. Global config auto-loads (built-in to agent product)
  2. Skill activates: read ~/learn-from-experience/memory.md (full HOT)
  3. Check index.md sync status -> if stale, auto-sync
  4. Detect project context -> load projects/{name}.md if needed

Session Work:
  5. Correction received -> write corrections.md + memory.md + sync global config
  6. New pattern discovered -> write memory.md (tentative) [no sync until confirmed]

Session End:
  7. If new confirmed rules this session -> sync global config
```

## Scope

This skill ONLY:
- Learns from user corrections and self-reflection
- Stores preferences in local files (`~/learn-from-experience/`)
- Syncs confirmed preferences to agent's global config `### Patterns` section
- Maintains heartbeat state in `~/learn-from-experience/heartbeat-state.md` when the workspace integrates heartbeat
- Reads its own memory files on activation

This skill NEVER:
- Accesses calendar, email, or contacts
- Makes network requests
- Reads files outside `~/learn-from-experience/` and the agent's global config file
- Infers preferences from silence or observation
- Deletes or blindly rewrites memory during heartbeat cleanup
- Modifies its own SKILL.md
- Touches global config content outside the `### Patterns` block

## Data Storage

Local state lives in `~/learn-from-experience/`:

- `memory.md` for HOT rules and confirmed preferences
- `corrections.md` for explicit corrections and reusable lessons
- `projects/` and `domains/` for scoped patterns
- `archive/` for decayed or inactive patterns
- `heartbeat-state.md` for recurring maintenance markers
- `index.md` for tier index + cross-session sync status

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `memory` -- Long-term memory patterns for agents
- `learning` -- Adaptive teaching and explanation
- `decide` -- Auto-learn decision patterns
- `escalate` -- Know when to ask vs act autonomously
