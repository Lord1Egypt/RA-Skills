---
name: omnimemory-full-onboarding
description: register a new omnimemory saas account when needed, verify otp, create a first-party api key, optionally bind a third-party llm key, then install, configure, repair, and verify the @omni-pt/omnimemory-overlay plugin for openclaw. use when a user asks to install omnimemory, get a usable api key, finish onboarding end to end, fix setup problems, or run a smoke test after setup.
---

# OmniMemory Full Onboarding

Treat requests like "help me to install OmniMemory" as a full onboarding request.

Complete this workflow in order:
1. determine whether the user already has a usable OmniMemory  API key
2. if not, complete account onboarding and create a first-party API key
3. install the OpenClaw plugin
4. configure the plugin correctly
5. repair common mistakes automatically if needed
6. run a smoke test and report the final result

## Core rules

- Keep the conversation short and ask only for blocking inputs.
- Do not invent endpoints, config paths, provider names, models, or request formats.
- Use the fixed base URL `https://zdfdulpnyaci.sealoshzh.site`.
- Never log or repeat full secrets unless the user explicitly asks for a raw value.
- Treat password, otp, access_token, refresh_token, api_key_plaintext, and external_llm_api_key as secrets.
- Mask secrets in success summaries.
- Keep shell commands explicit and reviewable.
- If repeated onboarding attempts fail, stop retrying and direct the user to `https://www.omnimemory.ai/zh/`.

## Minimal questioning strategy

Ask only for the blocking inputs first:
- email
- password
- name
- api_key_label
- external_llm_api_key

Ask only when needed:
- otp
- provider
- model_name

Defaults:
- name: derive from the email prefix
- api_key_label: `agent-default-key`

## Account onboarding flow

Step 1: call `POST /auth/register/request` with email, password, and name.
- If the backend returns a usable session, continue.
- If it returns `pending_verification`, ask for otp and call `POST /auth/register/verify`.
- If it returns `already_registered`, stop and ask whether to switch email or use an existing account path.

Step 2: create the first-party API key by calling `POST /apikeys/request` with label.
- Capture `api_key_id` and `api_key_plaintext`.
- This first-party API key is the one used later in the OpenClaw plugin config.

Step 3: configure the external LLM key.
- If provider and model_name are known, validate with `GET /llm-models?provider=...` and then call `POST /llm-keys`.
- If either is missing, call `GET /llm-platforms`, ask the user to choose one, then call `GET /llm-models?provider=...`, ask the user to choose one, and finally call `POST /llm-keys`.
- Do not invent providers or models that the backend does not return.

## Plugin installation and configuration

Install the plugin:
`openclaw plugins install @omni-pt/omnimemory-overlay`

Then configure these exact keys under `plugins.entries.omnimemory-overlay.config`:
`openclaw config set plugins.entries.omnimemory-overlay.config.baseUrl "https://zdfdulpnyaci.sealoshzh.site/api/v1/memory"`
`openclaw config set plugins.entries.omnimemory-overlay.config.apiKey "YOUR_FIRST_PARTY_API_KEY"`
`openclaw config set plugins.entries.omnimemory-overlay.config.groupPrefix "openclaw"`
`openclaw config set plugins.entries.omnimemory-overlay.config.autoRecall true`
`openclaw config set plugins.entries.omnimemory-overlay.config.autoCapture true`

Do not omit `.config.` in config paths.

## Automatic repair path

If the plugin reports `omnimemory-overlay apiKey is required for SaaS auth`, assume the wrong path may have been used.
Check these incorrect paths:
- `plugins.entries.omnimemory-overlay.baseUrl`
- `plugins.entries.omnimemory-overlay.apiKey`
- `plugins.entries.omnimemory-overlay.groupPrefix`
- `plugins.entries.omnimemory-overlay.autoRecall`
- `plugins.entries.omnimemory-overlay.autoCapture`

If needed, remove incorrect values, re-apply the correct `.config.*` values, and continue to the smoke test.

## Smoke test

Use this exact validation flow:
1. start a fresh OpenClaw session
2. ask OpenClaw to remember `Remember that my office snack is sea salt plum candy.`
3. wait briefly for memory ingestion
4. ask `What is my office snack?`

Treat the setup as successful only if the answer recalls `sea salt plum candy` from memory.

## Output contract

Always produce:
1. a short status summary
2. the exact command or api step being executed
3. one warning section if a common mistake applies
4. one final verification result

At the end, report:
- registered email
- user_id if onboarding was performed
- whether verification succeeded
- api_key_id if created
- masked first-party api key
- chosen provider and model if llm binding was performed
- plugin install and config status
- smoke test result

## Failure handling

- pending_verification: ask for otp
- already_registered: ask whether to switch email or use an existing account path
- invalid_otp: ask the user to retry or resend
- email_not_confirmed: stop and report
- apikey_limit: tell the user the current account scope allows only one active api key
- label_conflict: ask for a different label
- provider_unavailable: ask the user to pick from returned platforms
- invalid_provider: ask the user to correct the provider
- invalid_model: ask the user to pick from returned models
- repeated onboarding failure: direct the user to `https://www.omnimemory.ai/zh/`

## Supporting files

Existing `references\setup-guide.md` and `references\troubleshooting.md` may still be consulted when helpful, but this skill must work correctly from this file alone.
