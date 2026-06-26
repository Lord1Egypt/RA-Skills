---
name: large-codebase-workflow
description: Best practices for using Claude Code with large, multi-part codebases
homepage: https://canlah.ai
---

# Large Codebase Workflow Guide

## Core Principle

**Context is your scarcest resource.** Success = divide & conquer + parallel processing + persistent memory.

---

## Project Infrastructure Setup

```
project/
├── CLAUDE.md                 # Global instructions (<10k words)
├── .claudeignore             # Exclude node_modules, dist, etc.
├── .claude/
│   ├── rules/                # Modular rule files
│   │   ├── backend.md
│   │   ├── frontend.md
│   │   └── testing.md
│   ├── skills/               # Reusable workflows
│   ├── agents/               # Custom subagents
│   └── commands/             # Custom slash commands
```

### CLAUDE.md Rules
- Only include what Claude can't infer from code
- Monorepo: split 47k → 9k words = major performance gain
- Each rule: "Would removing this cause mistakes?" No → delete it

---

## Codemap Strategy: Reduce Session Startup Cost

**Problem:** Every new session, Claude explores codebase → wastes 50%+ context.
**Solution:** Pre-generate codemaps, Claude reads md files instead of exploring.

### Recommended Structure

```
.claude/
├── CLAUDE.md              # Concise instructions
└── codemaps/              # Pre-generated code maps
    ├── architecture.md    # Overall architecture
    ├── api-endpoints.md   # API listing
    ├── components.md      # Component relationships
    └── data-flow.md       # Data flow diagram
```

### Example: architecture.md

```markdown
# Architecture Overview

## Entry Points
- `src/index.ts` → App bootstrap
- `src/api/routes.ts` → All API routes

## Core Modules
| Module | Path | Purpose |
|--------|------|---------|
| Auth | `src/auth/` | JWT + session management |
| API | `src/api/` | REST endpoints |
| DB | `src/db/` | Prisma + migrations |

## Key Files (Read These First)
- `src/types/index.ts` → All shared types
- `src/config.ts` → Environment config
- `src/utils/` → Shared utilities

## Common Patterns
- All API handlers in `src/api/handlers/`
- Middleware chain: auth → validate → handler
- Error format: `{ error: string, code: number }`
```

### Auto-Generate Codemap (One-Time)

```bash
claude -p "Analyze this codebase and create a comprehensive codemap.
Output to .claude/codemaps/architecture.md. Include:
- Entry points
- Module responsibilities
- Key files to read first
- Data flow
- Common patterns"
```

### Reference in CLAUDE.md

```markdown
# CLAUDE.md

## Codebase Quick Start
Read these BEFORE exploring:
@.claude/codemaps/architecture.md
@.claude/codemaps/api-endpoints.md

## Commands
- `pnpm dev` - Start dev server
- `pnpm test` - Run tests
```

### Result
- New session: read 2-5k tokens (md files)
- Without codemap: explore 50k+ tokens
- **10x context savings**

### Keep Codemaps Updated

```bash
# After major refactors, regenerate
claude -p "Update .claude/codemaps/architecture.md based on current codebase structure"
```

---

## Session Strategy: One Goal Per Session

```bash
# Wrong: Multiple unrelated tasks in one session
# Right: Clear goal, then /clear between tasks

claude  # "Migrate auth middleware to v2"
/clear
claude  # "Add rate limiting to API"
```

### Key Commands
| Command | When to Use |
|---------|-------------|
| `/clear` | Between tasks (mandatory) |
| `/compact` | At 70% context capacity |
| `--continue` | Resume last session |
| `--resume` | Pick from history |

---

## Workflow: Explore → Plan → Code → Commit

### 1. EXPLORE (Plan Mode)
```
"read /src/auth and understand session handling"
```
- Read-only, no code changes

### 2. PLAN
```
"I want to add OAuth. What files need to change? Create a detailed plan."
```
- Output to SPEC.md or plan.md

### 3. IMPLEMENT (Normal Mode)
```
"implement the OAuth flow from your plan. write tests, run them, fix failures."
```
- Always provide verification: tests, screenshots, expected output

### 4. COMMIT
```
"commit with descriptive message and open a PR"
```

---

## Subagent Strategy (Key for Large Projects)

### Why Subagents
- Each has independent context window
- Won't pollute main session
- Can run 7 in parallel

### Usage Patterns
```bash
# Investigation
"use subagents to investigate how authentication handles token refresh"

# Parallel review
"use subagents to run security-scanner, style-checker, and test-coverage simultaneously"

# Verification
"use a subagent to review this code for edge cases"
```

### Built-in Subagent Types
| Agent | Purpose | Access |
|-------|---------|--------|
| Explore | Code search, understanding | Read-only |
| Plan | Architecture design | Read-only |
| security-reviewer | Security audit | Read, Grep, Glob |
| code-reviewer | Code review | Read, Grep, Glob |

---

## Parallel Development with Git Worktrees

```bash
# Create independent worktrees
git worktree add ../project-auth feature/auth
git worktree add ../project-api feature/api

# Run separate Claude sessions in each
# Session A: Refactor auth
# Session B: Build API
# Session C: Write tests
```

### Writer/Reviewer Pattern
- Session A writes code
- Session B reviews with clean context (avoids self-bias)

---

## Batch Processing & Automation

```bash
# Batch migrate files
for file in $(cat files.txt); do
  claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit:*)"
done

# CI integration
claude -p "Analyze this PR for security issues" --output-format json
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Symptom | Solution |
|--------------|---------|----------|
| Re-explore every session | 50% context gone on startup | Pre-generate codemaps |
| Kitchen sink session | N unrelated tasks in one session | `/clear` between tasks |
| Repeated corrections | 3+ corrections still wrong | `/clear` + better initial prompt |
| CLAUDE.md overload | Claude ignores your rules | Keep <10k words, use skills |
| Infinite exploration | "investigate" reads 100 files | Use subagent for exploration |
| Trust without verify | Code looks right but has bugs | Always provide tests/verification |
| Long session exhaustion | Context full, Claude "forgets" | Document & Clear method |

---

## Quick Reference

```bash
# Start new task
/clear

# Explore codebase (use subagent to save context)
"use subagents to investigate [X]"

# Complex task
Plan Mode → output plan.md → /clear → execute

# Context management
/compact "Focus on API changes"  # At 70%
/clear                           # Between tasks

# Resume previous session (preserve context)
claude --continue                # Resume last session
claude --resume                  # Pick from history

# Document & Clear (for long tasks)
"Output current progress to progress.md"
/clear
"Read progress.md and continue from where we left off"

# Parallel work
git worktree + multiple claude sessions

# Generate/update codemap
claude -p "Create codemap for this project → .claude/codemaps/"
```

## Context Budget Rule of Thumb

| Action | Token Cost | Recommendation |
|--------|------------|----------------|
| Read codemap | 2-5k | Always do first |
| Explore codebase | 30-50k+ | Use subagent instead |
| Read single file | 1-10k | OK if targeted |
| Full investigation | 50k+ | Document & Clear method |

---

## Sources
- [Anthropic Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Claude Code Docs](https://code.claude.com/docs/en/best-practices)
- [Subagents Guide](https://code.claude.com/docs/en/sub-agents)

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
