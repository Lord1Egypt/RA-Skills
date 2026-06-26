---
name: ironclaw-security-guard
homepage: https://github.com/wd041216-bit/openclaw-ironclaw-security-guard
description: Add lightweight defense-in-depth guardrails to OpenClaw with dangerous-command blocking, prompt-injection detection, secret redaction, and audit logging.
---

# IronClaw Security Guard

Use this skill when an OpenClaw runtime needs lightweight security guardrails rather than a full sandbox.

## What it is for

Use it when the user wants to:

- reduce risky shell execution
- protect sensitive paths and credentials
- detect prompt-injection patterns in untrusted content
- redact secrets before outgoing messages
- keep an audit trail of risky or blocked behavior

## What it covers

- shell-risk filtering
- protected path detection
- prompt-injection heuristics
- outbound secret redaction
- audit logging
- manual inspection through `ironclaw_security_scan`

## When to use it

- local-model deployments
- tool-heavy OpenClaw setups
- environments with chat, shell, web, and file tools enabled
- operator workflows that need safety checks without a heavyweight sandbox

## Non-goals

This skill does not:

- provide container isolation
- guarantee malware containment
- replace OS, network, or credential-hygiene controls

## Operating workflow

1. Check whether the plugin is enabled or running in `monitorOnly` mode.
2. Review configured allowlists, blocked command patterns, and protected path patterns.
3. Use `ironclaw_security_scan` first when content or tool parameters look suspicious.
4. Prefer the least-privileged path for shell, network, and messaging actions.
5. If the plugin blocks a call, inspect the audit log before overriding safeguards.

## Output expectations

Good use of this skill should usually produce:

- a concise risk explanation
- the matched finding category
- a safer alternative when one exists
- a note about whether the event should be audited or blocked

