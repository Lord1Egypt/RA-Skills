---
name: openclaw-guide
description: >
  Guide for OpenClaw setup, config, commands, routing, and troubleshooting.
  Use when the user asks how OpenClaw works, how to configure it, why a channel or agent
  is misbehaving, or how to diagnose gateway/channel/session issues. Prefer local docs first,
  then inspect the specific config subtree before suggesting changes. Not for designing or auditing skills themselves.
---

# OpenClaw Guide

Use this skill for **OpenClaw-specific guidance**, not general coding or generic Linux/macOS support.

## Scope

Good fits:
- OpenClaw config questions
- gateway restarts / health / logs
- channel routing issues (Telegram, Discord, iMessage, etc.)
- session / agent / cron behavior questions
- “why is OpenClaw doing X?” troubleshooting

Do **not** use this skill for:
- general shell/debug work unrelated to OpenClaw
- building new features unless the request is specifically about OpenClaw behavior
- security review of third-party code (use a review/audit flow instead)

## Default workflow

1. **Clarify the lane**
   Identify whether the request is about:
   - docs / usage
   - config / schema
   - runtime health
   - channel routing
   - skill structure
   - cron behavior

2. **Check local docs first**
   Prefer local docs before web docs:
   - `/Users/donzurbrick/.openclaw/workspace/docs`
   - `/Users/donzurbrick/.openclaw/workspace/AGENTS.md`
   - `/Users/donzurbrick/.openclaw/workspace/TOOLS.md`
   - `/Users/donzurbrick/.openclaw/workspace/MEMORY.md`

3. **Inspect only the relevant config subtree**
   Before answering config-field questions or making config changes, inspect the targeted schema subtree.
   Examples:
   - `channels.telegram`
   - `agents.defaults`
   - `gateway.auth`
   - `commands`

4. **Prefer the smallest explanation or change**
   - answer with the specific field/path involved
   - avoid dumping unrelated config
   - prefer a minimal patch over a broad rewrite

5. **Verify after mutation**
   If a restart or config change happens:
   - run the pre-restart validator if relevant
   - verify after restart
   - report pass/fail/warn cleanly

## Troubleshooting sequence

For runtime issues, use this order:
1. Determine whether the issue is **ingress**, **routing**, **authorization**, **model/provider**, or **delivery**
2. Check the most specific evidence source available
3. Avoid guessing from stale sessions when live config/logs can answer it
4. Separate:
   - what is verified
   - what is inferred
   - what still needs a test

## Skill structure rule

When asked to extend OpenClaw behavior, prefer:
1. existing tools
2. a skill with supporting files
3. retrieval/progressive disclosure
4. a specialist sub-agent
5. a new first-class tool

Do not recommend a new primitive unless the Tool Addition Gate is satisfied.

## Supporting references

Read these only if relevant:
- `references/triage-checklist.md` — quick diagnostic flow for common OpenClaw failures
- `references/skill-design-notes.md` — how to decide between skill vs tool vs subagent

## Output style

- Lead with the diagnosis or answer
- Name the exact config path / command / failure mode
- Distinguish verified facts from best guesses
- Keep it tight unless the issue is architectural
