---
name: marrow
description: Persistent agent memory for OpenClaw. Surface past failures, log decisions, and compound intelligence across sessions. Use when an agent should enforce Marrow usage automatically on every turn instead of relying on memory or opt-in logging.
metadata: {"openclaw": {"requires": {"env": ["MARROW_API_KEY"]}, "primaryEnv": "MARROW_API_KEY", "emoji": "🧠", "homepage": "https://getmarrow.ai"}}
---

# Marrow

Use the existing `@getmarrow/mcp` tools directly. Do not invent wrappers, aliases, or local substitutes.

## Operating rule

Treat Marrow logging as mandatory. The point is simple: every logged action improves future decisions, and every skipped action throws away usable failure prevention.

## Required flow

1. **Session start:** call `marrow_orient({ autoWarn: true })` before any other tool. If `shouldPause=true`, stop and review the warnings before acting.
2. **Before every meaningful action:** call `marrow_auto({ action: "what you are about to do" })`. Meaningful actions include file writes, edits, deploys, config changes, API calls, security changes, installs, deletes, and external sends.
3. **After every meaningful action:** call `marrow_auto({ action: "what you did", outcome: "result", success: true|false })`. If the action already happened, one combined `marrow_auto` call is fine.
4. **For complex or multi-step work:** use `marrow_think` before acting and `marrow_commit` after acting so you get pattern intelligence, loop detection, and explicit outcomes.
5. **For quick one-shot work:** `marrow_run` is acceptable when you want orient, think, and commit handled in one call.
6. **Before unfamiliar or risky work:** ask `marrow_ask("plain English question")` for prior failures, working patterns, or recommended next steps.

## Redaction rules

- **NEVER log** secrets, API keys, tokens, passwords, OTPs, auth headers, PII, or sensitive file contents in any Marrow call. Log the action and outcome, not the payload.
- **Do NOT log Marrow tool calls themselves.** Calling `marrow_orient`, `marrow_auto`, `marrow_think`, `marrow_commit`, `marrow_run`, `marrow_ask`, or any `marrow_*` tool is infrastructure — not a loggable action.
- Strip credentials from outcomes before committing. Example: "deployed to CF" not "deployed to CF with token cfut_abc123".

## Non-negotiables

- Never skip Marrow because the task feels small.
- Prefer fewer, clearer logs over noisy fragments.
- Record failures honestly. Bad news is training data.
- Read `references/marrow-api.md` when you need the tool quick reference.
