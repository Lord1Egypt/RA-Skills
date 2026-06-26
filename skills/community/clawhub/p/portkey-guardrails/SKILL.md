---
name: portkey-guardrails
version: 1.0.0
description: "Portkey-inspired guardrails for OpenClaw: 5 configurable rules that block prompt injection, redact PII, flag off-scope responses, enforce agent budgets, and warn on context length. Runs as a workspace hook — no external service required. Implemented from reading Portkey's open-source LLM gateway and building the patterns natively."
metadata:
  version: 1.0.0
  openclaw:
    emoji: "🛡️"
    events:
      - "message:received"
      - "message:preprocessed"
      - "message:sending"
      - "message:sent"
    requires:
      bins:
        - "node"
        - "ollama"
      env: []
    network:
      outbound: false
    primaryEnv: ""
    security_notes: "Pattern strings such as 'Ignore all previous instructions' and 'base64' appear in G-01 and G-02 rule code as DETECTION TARGETS — this is a guardrail skill, and these are the phrases it intercepts. They are not injections. ollama is optional (semantic cache only) — all 5 guardrail rules run fully offline without it."
---
**Last used:** 2026-04-03
**Status:** Active (live in production)

---

# Portkey Guardrails

A workspace hook that brings Portkey-style guardrails into OpenClaw natively — no external service, no API key, no Portkey account.

## What this skill does

Five sequential guardrail rules run on every inbound and outbound message:

| Rule | Layer | Default | What it catches |
|---|---|---|---|
| G-01 Prompt Injection | Input | block | "Ignore all previous instructions", DAN mode, base64-encoded overrides |
| G-02 PII Leakage | Output | redact | Australian phone numbers, email addresses, credit card patterns, TFN |
| G-03 Off-Scope Filter | Output | flag | NSFW, competitor-disparaging, political content in agent responses |
| G-04 Budget Guard | Input | block | Blocks agent dispatch when agent is in `red` budget state |
| G-05 Context Length | Input | warn | Warns when estimated token count exceeds 90% of model context window |

Rules are sequential and fail-fast: the first non-passing rule stops the chain. All non-pass events are audit-logged.

## Background

This skill was built by studying [Portkey's open-source LLM gateway](https://github.com/Portkey-AI/gateway) and implementing the same patterns natively inside OpenClaw's hook system. We do not use the Portkey SDK or service — this is a "reference architecture" adoption: read the source, understand the patterns, build your own version that fits your stack.

## How to use

Install the skill, then enable the hook:

```bash
openclaw skills install portkey-guardrails
openclaw hooks enable portkey-guardrails
```

Restart the gateway to load the hook:

```bash
openclaw gateway restart
```

## Per-agent configuration

To customise guardrail behaviour per agent, add an `agent-config.yaml` to each agent directory under `agents/<name>/agent-config.yaml`. Example:

```yaml
version: "1"
agent: kit

guardrails:
  inherit_defaults: true
  overrides:
    - id: G-01
      severity: flag   # downgrade from block to flag for Kit
    - id: G-03
      enabled: false   # Kit can discuss any topic
```

## Audit log

All non-pass events are appended to:
```
agents/<agentId>/guardrails-audit.md
```

## Declarative config layer

The skill also ships a full declarative YAML config system for per-agent reliability settings (retries, fallbacks, timeouts, cache hints). See `rules/config-schema.yaml` for the full schema.

## Semantic cache (optional)

Phase 3 includes an embedding-based semantic cache using local Ollama (`nomic-embed-text`) + SQLite. Requires Ollama running locally with the `nomic-embed-text` model pulled. Cache degrades gracefully if Ollama is unavailable.

```bash
ollama pull nomic-embed-text
```

## Fail-open design

If the guardrails module fails to load for any reason, the hook exits cleanly without blocking dispatch. Your gateway keeps running.

## Files

```
portkey-guardrails/
├── SKILL.md                          # This file
├── CHANGELOG.md
├── hook/
│   ├── HOOK.md                       # Hook metadata
│   └── handler.ts                    # Hook implementation
├── rules/
│   ├── G-01-prompt-injection.ts
│   ├── G-02-pii-leakage.ts
│   ├── G-03-off-scope-filter.ts
│   ├── G-04-budget-guard.ts
│   ├── G-05-context-length.ts
│   └── config-schema.yaml
└── tests/
    └── cases.yaml
```

## Requirements

- Node.js 18+ (for `tsx` TypeScript execution)
- OpenClaw workspace hook system enabled
- Ollama (optional — only for semantic cache Phase 3)
