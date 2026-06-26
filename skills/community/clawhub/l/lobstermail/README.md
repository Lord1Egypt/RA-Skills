# @lobstermail/claw

An [OpenClaw](https://openclaw.ai) skill that gives Claude the ability to create email inboxes, send and receive email, and safely consume message content — all autonomously, with no human setup required.

## Install

One-liner — downloads the skill from the edge proxy and saves it to your OpenClaw skills directory:

```bash
curl -sL https://api.lobstermail.ai/install | sh
```

Restart OpenClaw (or start a new session). The skill loads automatically.

### Local development

If you're working on the skill itself, you can symlink it instead:

```bash
mkdir -p ~/.openclaw/skills
ln -s "$(pwd)/packages/claw-skill" ~/.openclaw/skills/lobstermail
```

### Verify it loaded

```
/skills
```

You should see `lobstermail` in the list.

## What Claude can do with this skill

- **Create an email address on the fly** — Claude picks a meaningful name based on its identity (e.g. `sarah-shield@lobstermail.ai`) with automatic collision handling.
- **Receive emails** — poll an inbox, wait for a specific message, or filter by sender/subject.
- **Send emails** — compose and send from any provisioned inbox (requires Tier 1+).
- **Read content safely** — every email is scanned for prompt injection, spam, and phishing. `safeBodyForLLM()` wraps content in boundary markers so Claude can read untrusted mail without risk.

## Quick test

After the skill is loaded, try asking Claude:

> Create yourself an email inbox and tell me the address.

or

> Sign up for [some service] using a LobsterMail inbox and read the verification email.

Claude will `npm install lobstermail`, auto-provision an account (no API key needed), create a smart inbox, and start receiving real email at `@lobstermail.ai`.

## How it works

| Step                  | What happens                                                                            |
| --------------------- | --------------------------------------------------------------------------------------- |
| **1. SDK init**       | `LobsterMail.create()` auto-signs up, persists a token to `~/.lobstermail/token`        |
| **2. Inbox creation** | `createSmartInbox()` tries identity-based names, then numbered fallbacks, then random   |
| **3. Receive**        | `waitForEmail()` polls with exponential backoff until a matching message arrives        |
| **4. Safe read**      | `email.safeBodyForLLM()` returns content wrapped in boundary markers with risk metadata |

## Security

Every inbound email is scanned for:

- **Prompt injection** — boundary manipulation, system prompt overrides, role hijacking, data exfiltration attempts, obfuscated payloads
- **Spam & phishing** — keyword patterns, suspicious URLs, urgency language
- **SPF / DKIM / DMARC** — sender authentication results from SES

The SDK exposes `email.isInjectionRisk` (boolean) and a detailed `email.security` object so Claude can make informed decisions about untrusted content.

## Live E2E test

Run the real-life integration test to verify the full pipeline — signup, inbox creation, receiving a real email from Gmail, security scanning, and LLM-safe body formatting:

```bash
npx tsx packages/sdk/src/__tests__/live-e2e.ts
```

The script will create an inbox and print the address. Send an email to it from your Google Workspace account, press Enter, and watch it come through. No mocks, no simulation — real SES inbound.

## Skill file

The full skill definition lives in [`SKILL.md`](./SKILL.md). It teaches Claude:

- When and why to use LobsterMail
- How to pick good inbox names (identity-based vs. purpose-based vs. random)
- The `createSmartInbox` variation order and collision handling
- How to wait for emails with filters and timeouts
- How to safely pass email bodies to an LLM

## Links

- **SDK on npm**: [`lobstermail`](https://www.npmjs.com/package/lobstermail)
- **Domain**: `lobstermail.ai`
- **API docs**: OpenAPI 3.1 spec in `packages/docs`
