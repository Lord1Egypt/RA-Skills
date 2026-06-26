# NoddyAI API Skill

Call the NoddyAI platform API (graine.ai) to manage voice agents, place calls, handle telephony, and retrieve call records.

## Security, credentials, and user consent (read first)

**No secrets ship in this skill.** This package is **documentation only** (markdown files). It does **not** contain API keys, tokens, passwords, or `org_id` values. Operators must supply credentials via the **host** (OpenClaw secrets, environment variables, or your workspace's approved credential store - see host documentation). The model must use `Authorization: Bearer` only with a key **the user or runtime already configured**, never invent or embed credentials in skill text.

**Declare required configuration to the user.** Before any API call, ensure a Graine/NoddyAI API key (prefix `gat_`) and an `organization-` id are available from configuration; if missing, ask the user to add them - do not proceed with placeholder secrets.

**Confirm before high-impact actions.** Obtain explicit user confirmation before: placing **outbound** or **batch** calls, **transferring** live calls, **revoking** API tokens, **deleting** agents, or **changing inbound webhook URLs**. Summarize the exact numbers, agent IDs, or URLs affected.

**What “save IDs” means.** Retain `call_sid`, agent IDs, and similar values **only in the current task/session** so follow-up calls (e.g. GET call status) work. Do not send credentials or tokens to third parties; do not store identifiers beyond what the user expects for the active workflow.

**Webhooks.** `webhook_url` and inbound webhook fields send events to URLs **the user provides**. They must verify those endpoints are under their control before PATCH/POST that set webhooks.

## ClawHub / OpenClaw notes

- This skill describes **HTTP calls** to `https://api.graine.ai`. It does **not** require a local `openclaw run` command (many CLI versions have no `run` - use `openclaw --help`).
- **Test locally** with `curl` or any HTTP client; see `README.md` for CLI troubleshooting and ClawHub publish tips (slug conflicts, network status codes).

## Setup

**Credential source (not in repo):** API key and org id come from **user/host configuration** only.

All requests require:
- **Base URL**: `https://api.graine.ai` (fixed; no other base URLs for this skill)
- **Auth header**: `Authorization: Bearer <API_KEY>` - key prefix `gat_`, supplied by the user or secret store
- **org_id**: organization ID (format `organization-XXXX`), supplied by the user or secret store

Refer to `endpoints.md` for the full endpoint reference and `examples.md` for ready-to-use request bodies.

## How to use this skill

When the user asks you to interact with NoddyAI, identify which operation they need from the list below and construct the HTTP request using the details in `endpoints.md`.

### Operations available

| # | Operation | Method | Path |
|---|-----------|--------|------|
| 1 | Validate API token | GET | `/api/v1/api-tokens/validate-token` |
| 2 | List API tokens | GET | `/api/v1/api-tokens/list-tokens` |
| 3 | Revoke API token | DELETE | `/api/v1/api-tokens/revoke-token/{token}` |
| 4 | Create voice agent | POST | `/api/v1/agents` |
| 5 | Get agent (runtime format) | GET | `/api/v1/agents/{agent_id}` |
| 6 | List agents | GET | `/api/v1/agents` |
| 7 | Update agent voice/synthesizer | PATCH | `/api/v1/agents/{agent_id}` |
| 8 | Update agent system prompt | PATCH | `/api/v1/agents/{agent_id}` |
| 9 | Add API tool/skill to agent | PATCH | `/api/v1/agents/{agent_id}` |
| 10 | Delete agent | DELETE | `/api/v1/agents/{agent_id}` |
| 11 | Make outbound call | POST | `/api/v1/telephony/call` |
| 12 | Get call status | GET | `/api/v1/telephony/call/{call_sid}` |
| 13 | Transfer call (human handoff) | POST | `/api/v1/telephony/transfer` |
| 14 | Create inbound agent | POST | `/api/v1/telephony/inbound-agents` |
| 15 | Update inbound webhook URLs | PATCH | `/api/v1/telephony/inbound-agents/webhooks` |
| 16 | Submit batch call | POST | `/api/v1/batch/calls` |
| 17 | Upload CSV batch | POST | `/api/v1/batch/upload` |
| 18 | List call records | GET | `/api/v1/calls` |
| 19 | Get single call record | GET | `/api/v1/calls/{call_sid}` |

## Response behavior

- Always show the HTTP status and response body to the user (redact full Bearer tokens if echoing headers).
- For `call_sid` values returned from telephony, keep them in **this conversation** for follow-up status checks only.
- For agent IDs from create operations, keep them in **this conversation** for follow-up PATCH/DELETE only.
- Webhook payload shapes are in `webhooks.md` - use when the user builds or debugs **their own** webhook servers.
