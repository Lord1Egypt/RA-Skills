---
name: learnloop
version: 1.0.0
author: jiajiaoy
homepage: https://clawhub.ai/skills/learnloop
description: "Continuous learning protocol for Claude — captures corrections, errors, and user preferences into native auto-memory so the next session remembers. Stop teaching Claude the same thing twice."
keywords:
  - continuous learning
  - persistent memory
  - auto-memory
  - learning loop
  - knowledge capture
  - self-improvement
  - memory protocol
  - Claude forgets
  - Claude repeats mistakes
  - AI forgets corrections
  - teach Claude twice
  - Claude has no memory
  - lost context
  - AI amnesia
  - AI agent
  - agentic
  - Claude Code
  - LLM memory
  - AI productivity
  - agentic memory
  - smarter Claude
  - make Claude better
  - Claude improvement
  - improve AI
  - agent improvement
  - 持续学习
  - 自动记忆
  - 智能记忆
  - 不再重复错误
  - AI记忆
  - ThinkStack
---

# LearnLoop

Claude forgets everything between sessions by default. LearnLoop closes that loop — every correction, every error, every preference is captured into Claude Code's native auto-memory and auto-loaded next time.

## The Core Problem

Without persistent learning, every session starts from zero:

- You correct Claude → it agrees → next session, same mistake
- You explain your role and preferences → gone tomorrow
- A command fails with a known fix → re-debugged from scratch
- An external tool has a gotcha → relearned on every encounter
- You discover a better approach → never reused

The result: smart in the moment, amnesic over time. Your time is spent re-teaching, not advancing.

## Why Native Memory

LearnLoop writes directly to Claude Code's auto-memory system at `~/.claude/projects/<project-id>/memory/`:

- **Auto-injected** — MEMORY.md is loaded into every new session, no manual recall needed
- **Typed** — entries are classified (user / feedback / project / reference) so retrieval is sharp
- **Linked** — memories cross-reference via `[[slug]]` for graph-style recall
- **Local** — nothing leaves your machine

No `.learnings/` folder to maintain, no separate file to read, no "did I check the log?" overhead.

## When to Activate

Trigger LearnLoop on any of these moments:

| Trigger | Save As | Example |
|---------|---------|---------|
| User corrects Claude ("No, that's wrong", "Actually...") | `feedback` | "Don't use `git add .` — too broad" |
| Command or tool fails unexpectedly | `project` or `feedback` | "`npm test` requires Node 20+ in this repo" |
| User shares role, expertise, or preference | `user` | "Senior backend dev, new to React" |
| External system referenced | `reference` | "Bugs tracked in Linear project INGEST" |
| Knowledge turned out to be outdated | `feedback` | "API moved from v1 to v2 in March" |
| Better approach discovered for recurring task | `feedback` | "Use `rg` not `grep` — 10x faster in this monorepo" |
| Project deadline or constraint mentioned | `project` | "Mobile freeze starts 2026-03-05" |

If you'd otherwise say "I'll keep that in mind for next time" — that's the trigger. You can't keep it in mind. Save it.

## The Protocol

### Step 1: Detect the Trigger
Watch for the seven moments above. The two strongest signals:

- **User uses corrective language**: "no", "actually", "wrong", "stop", "don't"
- **Validated success on a non-obvious choice**: user accepts an unusual approach without pushback ("yes exactly", "perfect")

Save from failure AND success. Saving only corrections produces a fearful agent; saving validated wins keeps you bold.

### Step 2: Classify the Memory Type

| Type | Use For |
|------|---------|
| `user` | Role, expertise, goals, communication preferences |
| `feedback` | Behavioral rules: do this, don't do that, why |
| `project` | Ongoing initiatives, deadlines, who/why context |
| `reference` | Pointers to external systems (Linear, Grafana, Slack channels) |

If unsure, ask: *does this guide my future behavior?* (feedback) *or describe a person?* (user) *or a workstream?* (project) *or point elsewhere?* (reference).

### Step 3: Write the Memory File

Path: `~/.claude/projects/<project-id>/memory/<short-kebab-slug>.md`

Frontmatter format:
```yaml
---
name: short-kebab-slug
description: one-line summary, specific enough to judge relevance later
metadata:
  type: feedback
---
```

Body structure for `feedback` and `project` types — lead with the rule/fact, then:
- **Why:** the reason (often a past incident or stated preference)
- **How to apply:** when this guidance kicks in

The **Why** is load-bearing. Without it, future-you can't judge edge cases — you'll either follow blindly or ignore stale rules.

### Step 4: Update MEMORY.md Index

`MEMORY.md` is the index loaded into every session. One line per entry, under ~150 chars:

```
- [Title](slug.md) — one-line hook on when it matters
```

Keep it under 200 lines. If MEMORY.md fills up, consolidate related entries into single files rather than truncating.

### Step 5: Verify Before Recalling

Memories age. Before acting on a recalled fact:

- Names a file path? Check it exists.
- Names a function or flag? `grep` for it.
- Summarizes repo state? Prefer `git log` over the snapshot.

If the memory conflicts with current reality, **update or delete the memory**. Don't act on stale memory.

## What NOT to Save

These belong in code, git, or scratch — not memory:

- Code patterns, architecture, file paths derivable from the project
- Git history or who-changed-what (use `git log` / `git blame`)
- Bug-fix recipes — the fix lives in the commit
- Anything already in CLAUDE.md
- Ephemeral task state (use TodoWrite or a plan instead)

Even when the user says "remember this PR list" — ask what was *surprising* about it. The surprise is the memory. The list is not.

## Anti-Patterns to Avoid

- **Save-everything spam** — memory becomes noise; future-you ignores it
- **Skipping the "Why"** — rule without reason becomes dogma or gets discarded
- **Duplicate entries** — check existing memories before writing a new one
- **Cargo-culting from one session** — confirmed-twice beats said-once for behavioral rules
- **Trusting stale memory** — always verify file/symbol/state before acting on a recalled claim

## Output Format

When you decide to save:

```
[LearnLoop] Saving as <type>: <one-line summary>
  → memory/<slug>.md
  → MEMORY.md updated
```

When you decide *not* to save:

```
[LearnLoop] Noted but not saved — <reason>
```

Be visible about the loop. Silent saves hide the mechanism; users should see what you remembered and what you didn't.

## Pairs Well With

LearnLoop is part of the **ThinkStack** — meta-skills that compound:

- `clarity-first` — understand the request before you act
- `thinkdeep` — reason through complex problems
- `honest-critic` — push back instead of validating
- `task-pilot` — execute structured plans
- `learnloop` — never lose what you learned

```bash
openclaw install learnloop
openclaw install honest-critic
openclaw install thinkdeep
openclaw install clarity-first
openclaw install task-pilot
```
