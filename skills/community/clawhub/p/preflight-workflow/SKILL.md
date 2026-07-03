---
name: preflight-workflow
description: "Stop before you break — four mandatory checks before every operation: search, rollback, test, scope"
version: 1.0.0
platforms: [macos, linux, windows]
metadata:
  tags: [workflow, safety, preflight, rules, checklist, devops, automation]
  category: devops
  icon: 🛡️
  
clawhub:
  display_name: Preflight Workflow
  summary: "Force four checks before any operation. Stop guessing. Stop breaking things."
  categories: [devops, automation, productivity]
  languages: [en, zh]
---

# 🛡️ Preflight Workflow

A lightweight safety workflow that stops agents and humans from acting before they think. Four mandatory checks — if even one fails, stop and fix it first.

## When to Use

Every time you (or your agent) are about to:
- Run a system command
- Deploy or modify code
- Change configuration
- Execute an unfamiliar or risky operation

**Core rule:** No search = no action. No preflight = no execution.

## How It Works (for agents)

### Step 1: User describes what they want to do
If it's a new, unfamiliar, or risky operation → run the full four-question checklist.

### Step 2: Four mandatory questions

#### ✅ Q1: Have you searched first?
- Look for existing solutions, known pitfalls, or prior experience
- Don't answer from memory or intuition
- Check at least 2 independent sources

#### ✅ Q2: Is there a rollback plan?
- What state can you return to if it fails?
- Have you made a backup?
- Do you have clear rollback steps?

#### ✅ Q3: Has it been tested or validated?
- Has the approach been verified on a small scale?
- Are you relying on "let's try and see"?

#### ✅ Q4: Is the impact clear?
- What are you changing?
- Who/what will it affect?
- How long to recover if it goes wrong?

### Step 3: All pass → proceed. Any fail → stop.
Four ✅ required. **Not one less.**

### Step 4: After the operation
| Outcome | Action |
|---------|--------|
| ✅ Success | Log it (date + what + result) |
| ❌ Failure | Write to LEARNINGS.md (root cause + fix + prevention) |
| 💡 New insight | Update this SKILL.md |

## CLI Mode (no agent, just a shell script)

```bash
chmod +x preflight.sh
./preflight.sh "deploy new cron job"
```

Answers four yes/no questions interactively. All ✅ → "All passed, go ahead." Any ❌ → "Blocked: ... Fix it first."

## Common Pitfalls

- ❌ "I know this one" → No you don't. Search first.
- ❌ "This is too simple to check" → Small ops cause big outages.
- ❌ Trying repeatedly without documenting → Failure is a lesson. Write it down.
- ✅ Getting corrected? Accept → Fix → Remember. No excuses.

## Included Files

| File | Purpose |
|------|---------|
| `preflight.sh` | Interactive CLI checklist (4 yes/no questions) |
| `SKILL.md` | Loadable skill for any SKILL.md-compatible agent |
| `LEARNINGS.md` | Post-mortem template (root cause + fix + prevention) |
| `install.sh` | One-command install script |
| `README.md` | Quick start guide |

## Verification

Run the script and answer all four questions:
- All `y` → ✅ "All passed, proceed."
- Any `n` → ❌ "Blocked by: [reason]. Fix before proceeding."
