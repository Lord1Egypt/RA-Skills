---
name: Kimi
slug: kimi
version: 1.0.0
homepage: https://clawic.com/skills/kimi
description: Build and debug Kimi API workflows for chat, coding, reasoning, and tool-calling with live model checks, retries, and safe routing.
changelog: Initial release with Kimi workflow routing, OpenAI-compatible request patterns, migration guidance, and operational safety checks.
metadata: {"clawdbot":{"emoji":"🌙","requires":{"bins":["curl","jq"],"env":["MOONSHOT_API_KEY"]},"os":["linux","darwin","win32"],"configPaths":["~/kimi/"]}}
---

## When to Use

User needs Kimi to work reliably for chat, coding, long-context research, structured outputs, or agent workflows. Agent handles live model verification, request shaping, migration from other OpenAI-compatible providers, and failure recovery before the workflow is trusted.

## Architecture

Memory lives in `~/kimi/`. If `~/kimi/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/kimi/
├── memory.md         # Status, activation rules, and stable defaults
├── routes.md         # Preferred route per workload
├── approvals.md      # Sensitive-send boundaries and redaction preferences
├── experiments.md    # Prompt, parser, and fallback notes
└── logs/             # Optional sanitized repro payloads
```

## Quick Reference

Use the smallest file that resolves the blocker.

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| Minimal request patterns | `api-patterns.md` |
| Workload routing choices | `routing-matrix.md` |
| OpenAI-compatible migration | `migration-playbook.md` |
| Trust and redaction workflows | `safety-workflows.md` |
| Fast diagnosis and recovery | `troubleshooting.md` |

## Requirements

- `curl` and `jq` for minimal endpoint checks
- `MOONSHOT_API_KEY` kept in environment variables only
- Kimi access through the official Moonshot API base URL
- User approval before persisting local notes or sanitized logs

## Core Rules

### 1. Verify Auth and Live Models Before Naming Any Route
- Start with `https://api.moonshot.ai/v1/models` and copy live model IDs from the response.
- Never trust remembered Kimi model names, screenshots, or stale blog examples when a workflow is failing now.

### 2. Lock the Job to One Workload Before Tuning Prompts
- Classify the request as one of: fast chat, coding agent, long-context research, deterministic JSON, or migration debugging.
- Most bad Kimi advice comes from mixing several jobs into one oversized prompt and then blaming the model.

### 3. Treat Structured Output as a Separate Reliability Path
- If output feeds tools, code execution, or downstream writes, use strict schemas or a second normalization pass.
- Do not ask one response to do open-ended reasoning and perfect machine-readable output at the same time.

### 4. Keep Sensitive Data Out Unless the User Explicitly Approves It
- Redact secrets, customer identifiers, internal hostnames, and raw tokens before sending prompts externally.
- If the user wants repeatable Kimi workflows, save the redaction rule and approval boundary in `~/kimi/approvals.md` after confirming the first write.

### 5. Route by Deadline and Cost, Not Brand Habit
- Use the smallest Kimi route that can finish the current job reliably.
- For recurring workflows, save one primary route and one fallback route instead of debating models from scratch each time.

### 6. Separate Provider Migration Problems From Model Problems
- When moving from OpenAI-compatible code to Kimi, isolate the variable: base URL, auth env var, model ID, parser, or retry policy.
- Reproduce with one minimal payload before changing prompts, infrastructure, and business logic together.

### 7. Ask Before Creating Persistent State
- Work statelessly by default.
- Only create `~/kimi/` notes, approvals, or debug logs after the user wants continuity across Kimi tasks.

## Common Traps

- Hardcoding a remembered model ID -> fetch `/models` and use the live ID instead.
- Treating Kimi as one generic route -> split coding, reasoning, JSON, and migration work.
- Sending raw internal logs to the API -> redact first and preview what leaves the machine.
- Combining creative reasoning with strict JSON output -> use a second deterministic pass.
- Blaming the model for every failure -> verify auth, base URL, retries, and parser behavior first.

## External Endpoints

Use only the official Moonshot API surface required for the current task.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://api.moonshot.ai/v1/models | Auth header only | Discover live Kimi models |
| https://api.moonshot.ai/v1/chat/completions | Prompt messages and options | Kimi chat, reasoning, coding, and structured-output requests |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Prompt content sent to the Moonshot API when the user asks for Kimi inference
- Optional sanitized excerpts of code, logs, or documents sent for analysis after approval

**Data that stays local:**
- Activation preferences, route defaults, and approval boundaries in `~/kimi/` after user approval
- Optional sanitized repro payloads and troubleshooting notes saved for recurring workflows

**This skill does NOT:**
- Store `MOONSHOT_API_KEY` in markdown or project files
- Send data to undeclared endpoints
- Persist raw secrets or sensitive prompts without explicit user approval
- Modify its own skill files

## Scope

This skill ONLY:
- designs and debugs Kimi API workflows
- routes Kimi usage across coding, reasoning, research, and deterministic-output jobs
- hardens retries, validation, and migration from other OpenAI-compatible providers
- stores lightweight local notes only after user approval

This skill NEVER:
- invent live model availability without checking
- persist secrets in `~/kimi/`
- execute destructive downstream automation from unvalidated output
- treat cost-sensitive or sensitive-send boundaries as implicit

## Trust

Using this skill sends prompt data to Moonshot's Kimi API.
Only install if you trust Moonshot with that data, or keep sensitive preprocessing local and sanitized.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `api` — debug auth, payloads, retries, and OpenAI-compatible request shapes
- `models` — compare model families and cost tiers before locking Kimi into production
- `coding` — tighten coding-agent behavior after the Kimi route itself is stable
- `backend` — connect Kimi workflows to services, jobs, and API boundaries
- `fastapi` — expose Kimi-backed endpoints with request validation and safer deployment defaults

## Feedback

- If useful: `clawhub star kimi`
- Stay updated: `clawhub sync`
