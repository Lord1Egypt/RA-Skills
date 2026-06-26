# Prompt Refinement Patterns

## By Task Type

### Code Tasks
When refining prompts for code work, prioritize:
- **Scope**: Which files/modules/functions are in play
- **Verification**: How to confirm the change works (tests, manual check, build)
- **Deliverables**: What exactly should be produced (diff, new file, refactored module)
- **Non-goals**: What should NOT be touched

**Example — Before:**
> 帮我优化登录性能

**Example — After:**
> Goal: Reduce login API response time from current ~2s to <500ms
> Context: Backend is Express + PostgreSQL, login endpoint at /api/auth/login
> Constraints: Don't change the database schema or auth flow logic
> Execution: Profile the endpoint, identify top 3 bottlenecks, fix them
> Verification: Run load test before/after, compare p95 latency
> Acceptance: p95 < 500ms under 100 concurrent users

### Content Tasks
When refining prompts for writing/content, prioritize:
- **Audience**: Who reads this
- **Tone**: Formal, casual, technical, friendly
- **Length**: Word count or section count
- **Structure**: Required sections, format constraints

**Example — Before:**
> 帮我写个项目介绍

**Example — After:**
> Goal: Write a project introduction for our open-source CLI tool
> Audience: Developers who use Claude Code
> Tone: Technical but approachable, no marketing fluff
> Length: 200-300 words
> Structure: What it does → Why it exists → How to install → Quick example

### General Tasks
When refining prompts for general/ambiguous work:
- **Goal**: What does "done" look like
- **Context**: What do you already know / have
- **Boundaries**: What's out of scope
- **Output format**: How should the result be delivered

## Common Vague Phrases → Actionable Rewrites

| Vague | Actionable |
|-------|-----------|
| "优化一下" | Specify: optimize what metric, by how much, under what constraints |
| "搞快点" | Specify: target latency/throughput, current baseline, acceptable tradeoffs |
| "弄好一点" | Specify: what's wrong now, what "better" means concretely |
| "帮我改改" | Specify: what to change, what to preserve, how to verify |
| "看看有没有问题" | Specify: review scope, what kinds of issues matter, severity threshold |
