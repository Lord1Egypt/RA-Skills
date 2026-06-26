---
name: Token Efficiency
description: Avoid unnecessary context burn. Surgical file reads, batched commands, less narration. Every token read is a token taxed.
---

# Token Efficiency - Avoiding Unnecessary Context Burn

Every token read is a token taxed. Be surgical.

## Core Rules

- **grep/tail over full reads** — need one section? `grep -A 20 "## Section"`. Need the end? `tail -50`. Don't read 500 lines to find 5.
- **batch API calls** — one curl with multiple params > three separate curls. Combine endpoint checks into single scripts.
- **sub-agents for heavy research** — scraping a thread, summarizing 50 posts, reading a full repo? Spawn a sub-agent. Don't burn main context on bulk work.
- **don't re-read context** — if a file was already read this session, use what you have. Never read it again "just to be sure."
- **summarize before storing** — tool output going to a file? Strip it down first. Store the insight, not the raw dump.

## Anti-Patterns (Observed)

| Bad | Good |
|-----|------|
| Read full 3000-line comment thread | `grep -c ""` for count, tail for recent, grep for keywords |
| 4 separate curl calls to 4 endpoints | One script, four curls, one python parse pass |
| Narrate every grep and read step | Just do it, report the finding |
| Re-read SKILL.md to "refresh" mid-session | Trust what's already in context |
| Store raw JSON API response | Extract the 3 fields you care about, store those |

## When to Use Sub-Agents

- Research tasks > ~10 tool calls
- Bulk reading (threads, repos, feeds)
- Tasks that can run in parallel with main work
- Anything that would dominate your context window

## Quick Heuristics

- If you're about to read a file you've already read → stop
- If you're about to make the same API call twice → cache the result
- If narrating a step takes longer than doing it → just do it
- If a task feels heavy → sub-agent it
