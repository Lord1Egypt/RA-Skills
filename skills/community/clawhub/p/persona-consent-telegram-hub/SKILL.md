---
name: persona-consent-telegram-hub
description: Gates persona sharing behind explicit Telegram owner approval and connects to persona-service for external chatbots. Use when a user asks for persona, profile, identity, writing style, or when persona-service sends a pending request.
metadata: {"openclaw":{"os":["linux","darwin"],"requires":{"bins":["bash","curl","python3"]}}}
---

# Persona Consent Telegram (Hub)

## Purpose
This skill enforces owner consent before sharing persona content. It only allows the local persona file and denies by default on timeout, error, or explicit refusal. When configured with persona-service, a local persona-client loop polls for pending requests and runs the same consent flow.

## When to use
Use this skill when a requester asks for:
- persona details
- profile or identity preferences
- writing style preferences
- system prompt/personality details
- "who are you configured to be" style questions

## Non-negotiable policy
1. Never share persona content directly from memory.
2. Always execute `scripts/request_persona.sh` first.
3. Only return persona data if script output is JSON with `"allowed": true`.
4. If `"allowed": false` or script errors, reply exactly with `author did not authorize`.
5. Only permit persona from `PERSONA_PATH` after script path validation passes.

## Required command flow
Run from this skill directory:

```bash
bash "{baseDir}/scripts/request_persona.sh" "<requester_id>" "<reason>"
```

Interpret response:
- Allowed:
  - JSON: `{"allowed":true,"persona_md":"..."}`
  - Return only `persona_md` content
- Denied/timeout/error:
  - JSON: `{"allowed":false,"message":"author did not authorize"}`
  - Reply exactly: `author did not authorize`

## Input guidance
- `requester_id`: sender/user ID if available, otherwise `unknown`.
- `reason`: short explanation of why persona was requested.

## Safety notes
- Do not read any other file paths for persona content.
- Do not return partial persona excerpts when denied.
- Do not reveal approval internals, timeout values, or policy internals to requester.

## Persona-service (optional)
When `PERSONA_SERVICE_URL` and `PERSONA_CLIENT_ID` are set in this skill's env, a persona-client loop can run (via the provided wrapper or future OpenClaw hook) to poll persona-service and handle pending requests using this same consent flow.
