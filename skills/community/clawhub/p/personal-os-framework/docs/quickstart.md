# Quick Start Examples

## Example 1: First Day Setup

On your first day, create these files:

```
my-personal-os/
├── STATE.md
├── TODO.md
├── DECISIONS.md
├── PENDING-DECISIONS.md
└── HEARTBEAT-LOG.md
```

### STATE.md
```markdown
# Project State

## My Projects
| Project | Status | Next Action |
|---------|--------|------------|
| | | |

## Last Updated
2026-03-26
```

### DECISIONS.md
```markdown
# Decision Log

## Entries

```

## Example 2: Making a Decision

When you make an important choice:

**You say to your AI:**
> "I'm going to use Python for this project instead of JavaScript."

**AI writes to DECISIONS.md:**
```markdown
## Decision — 2026-03-26

### Use Python over JavaScript for the API

**Rationale:** 
- Better async/await support
- Team has more Python experience
- Libraries are more mature for our use case

**Alternatives considered:**
- JavaScript/TypeScript (rejected due to callback complexity)
- Go (rejected due to learning curve)

**Consequences:**
- Faster development expected
- May need to hire Python developers later

**Follow-up:**
- [ ] Set up Python project template
- [ ] Review team Python skills
```

## Example 3: Weekly Review

**AI generates review:**
```markdown
# Weekly Review — 2026-03-26

## What moved this week
- API project: decided on Python, started scaffolding
- Landing page: design completed, waiting on content

## What stalled
- Mobile app: blocked on design review
- Documentation: not started (wasn't priority)

## Stale items
- [ ] Mobile app wireframes (last updated: 2 weeks ago)
- [ ] API integration plan (last updated: 10 days ago)

## Next week priorities
1. Complete API scaffolding
2. Get mobile design review
3. Write first draft of documentation

## Decisions to log
- Python over JavaScript for API (done)
```

## Example 4: Routing a Note

**You capture a note:**
> "Saw an interesting article about AI agents"

**AI routes it:**
```markdown
# Knowledge Entry — 2026-03-26

## AI Agents Article Summary

**Source:** [link]

**Key Points:**
- Agents can plan and execute tasks autonomously
- Memory is a key challenge
- Tool use is expanding rapidly

**Why kept:** Relevant to our AI strategy

**Tags:** #AI #agents #research
```

## Example 5: Task Management

**You start working on a task:**
```markdown
# Task: API authentication
- [p] In Progress
- Started: 2026-03-26
- Waiting on: security review from team
- Follow-up: update docs after completion
```

**After 3 days with no progress:**
```markdown
# WARNING: Stale Task

- [w] API authentication
- Started: 2026-03-26
- Last updated: 2026-03-26 (3 days ago)
- Waiting on: security review (overdue)
- Action needed: follow up with team
```

## Example 6: AI Collaboration Flow

**Conversation:**
> **You:** I finished the user research for the new feature

**AI reads STATE.md, sees project status, then:**
```markdown
# Session Note — 2026-03-26

## What happened
User research completed for feature v2

## AI recorded to DECISIONS.md:
- Decision: Build feature v2 based on user research findings
- Key insight: Users want simpler onboarding
- Decision made by: [You]

## AI updated:
- STATE.md: project status
- TODO.md: added research findings to backlog
```

## How to Use These Examples

1. **Start simple** — Create the 5 core files first
2. **Log decisions** — When you make a choice, have AI record it
3. **Run weekly reviews** — AI generates, you fill in
4. **Route notes** — Everything goes somewhere
5. **Track tasks** — Keep status current

The AI does the recording. You do the work.
