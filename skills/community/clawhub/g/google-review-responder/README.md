# Review Responder

An [OpenClaw](https://openclaw.ai) skill that monitors Google Business Profile reviews, drafts professional responses, and routes them to a configurable approval channel before posting.

Built for consultants and agencies managing reviews across multiple client locations and industries.

**Current version: 2.0.1**

## What's new in 2.0.1

- Added a **Privacy and Data Handling** section to SKILL.md that honestly describes the skill's real network calls (Google Business Profile API), credential storage (operator-owned OAuth credentials per client), and the no-auto-post guardrail
- Added a **Permissions and Privacy** section to this README so operators see scope, credential handling, and the HIPAA-aware (not HIPAA-certified) boundary before installing
- Reworded the `medical` industry profile from "HIPAA-safe" to "HIPAA-aware drafting" to accurately describe what the skill enforces (drafting constraints) versus what it does not provide (workflow certification)
- Narrowed the activation triggers in `description` to require an active, configured-client workflow, with a "do NOT trigger" guard for casual reviews chat and review-writing requests

## What's new in 2.0.0

- **Configurable script paths and channels** via a single `review-responder.config.json` file
- **Channel-agnostic approval flow**: Telegram, email, webhook, or in-thread chat
- **Industry compliance profiles**: medical (HIPAA-aware drafting), legal, restaurant, retail, and general
- **Operator pattern learning**: logs approval decisions per client and surfaces patterns (e.g., "you usually shorten 5-star replies for this client")
- **Per-client overrides** for industry, approval channel, and tone notes

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

## How It Works

1. On each scheduled check, OpenClaw enumerates configured clients and looks for new unanswered reviews
2. For each new review, the agent applies the client's industry profile and drafts a tone-matched response
3. The draft is sent to the configured approval channel (Telegram, email, webhook, or chat)
4. The operator replies "OK" to post it, sends edits to revise it, or "skip" to ignore it
5. Decisions are logged so the agent can learn the operator's preferences over time

No reviews are ever posted without explicit operator approval.

## What's Included

- `SKILL.md` — Agent behavior instructions (configuration, approval flow, industry profiles, pattern learning)
- `HEARTBEAT.md` — Periodic check instructions for OpenClaw's heartbeat system
- `gbp_reviews.py` — Main script for checking reviews and posting replies
- `get_client_token.py` — One-time OAuth helper for onboarding clients locally
- `oauth_server.py` — Web-based OAuth flow for remote client onboarding
- `clients/_template.json` — Config template for adding new clients
- `SETUP.md` — Full setup and per-client onboarding guide

## Quick Start

1. Set up a Google Cloud project with the Business Profile API enabled (details in `SETUP.md`)
2. Install dependencies: `pip install google-auth google-auth-oauthlib requests`
3. Copy the `review-responder` folder into your OpenClaw workspace
4. Create `review-responder.config.json` from the template in `SKILL.md`
5. Register the skill in your `openclaw.json`
6. Onboard your first client using `get_client_token.py` or `oauth_server.py`
7. Wire up the scheduled check and you're live

See `SETUP.md` for the full walkthrough.

## Requirements

- Python 3 with `google-auth`, `google-auth-oauthlib`, `requests`
- Flask (only if using the web-based OAuth onboarding server)
- A Google Cloud project with OAuth 2.0 credentials
- One approval channel configured: Telegram, email (SMTP), webhook endpoint, or in-thread chat

## Permissions and Privacy (read before installing)

Unlike most skills in this catalog, this one ships executable Python (`gbp_reviews.py`, `get_client_token.py`, `oauth_server.py`) that makes real network calls and posts content publicly to Google Business Profile. Read this section in full before installing or onboarding clients.

**What runs on the network**

- **Google Business Profile API v4** (`mybusiness.googleapis.com`): the skill polls reviews for each configured client and posts approved replies. Calls authenticate with the client's own OAuth credentials, which you obtain and store locally during onboarding.
- **Google OAuth token endpoint** (`https://oauth2.googleapis.com/token`): standard refresh-token exchange.
- **Whichever approval channel you configure**: Telegram (your bot, your chat), SMTP (your relay, your recipient), webhook (your endpoint), or in-thread chat (no network). The skill does not bundle credentials for any of these and does not route through any author-controlled service.

**Credential storage**

- Per-client OAuth credentials (`oauth_client_id`, `oauth_client_secret`, `refresh_token`) live in JSON files under `clients_dir` on your machine. These are your credentials for your own clients. The skill does not transmit them anywhere except to Google's token endpoint for the standard OAuth refresh flow.
- Treat the `clients/` directory like you would any secrets folder: restrict filesystem permissions, do not commit it to public source control (the included `.gitignore` excludes it), and consider disk-level encryption.

**Hard guardrails**

- **No auto-posting.** Every reply requires explicit operator approval through your configured channel. The skill must not, and the assistant must not, post a reply without that approval.
- **No PHI in public replies.** When a client is set to the `medical` industry profile, the assistant will never reference health conditions, treatments, or diagnoses in the public reply, even if the reviewer disclosed those details.
- **No credential leakage.** The assistant will never quote, log, or include `oauth_client_secret` or `refresh_token` in approval messages, drafts, logs, or chat outputs.
- **No bulk export.** The skill is for your ongoing review workflow, not for dumping consolidated client lists or review histories into external destinations.

**Compliance scope (read this carefully if you serve regulated industries)**

The `medical` industry profile applies **HIPAA-aware drafting constraints** to the public reply text — it prevents the reply from referencing PHI. This is one input to a compliant workflow, not the whole workflow. The skill does NOT:

- Certify your overall practice as HIPAA-compliant
- Replace your Business Associate Agreement obligations (Google, OpenAI/Anthropic, and any other vendor in your pipeline have their own status)
- Constitute legal advice for medical, legal, or financial regulated practices

Operators in regulated industries remain responsible for their own compliance program and should review these constraints against their own policies before using this skill in production.

**No telemetry**

The skill does not collect or transmit usage data, client identifiers, review content, or any other information back to its author, ClawHub, or any third party.
