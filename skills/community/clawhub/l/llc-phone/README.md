# llc-phone

**OpenClaw skill package** for low-latency inbound and outbound AI phone calls
via the OpenAI Realtime API and Twilio.

Covers the full stack for both directions: pre-warm / pre-accept warm, AI
IVR, receptionist flows, CSR with database-backed tools, VAD tuning, prompt
caching, and field-tested implementation caveats.

Research note: this package mixes official vendor docs with thoroughly sourced
practitioner research. Treat vendor docs as authoritative, and treat
operational latency or behavior claims here as well-sourced guidance to
validate in your own environment.

## Local install

```bash
cp -r llc-phone ~/.openclaw/skills/
```

After installing, start a new OpenClaw session — skills are snapshotted at
session start.

## Required environment variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key with Realtime API access |
| `TWILIO_ACCOUNT_SID` | Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Twilio Auth Token |
| `TWILIO_PHONE_NUMBER` | Outbound/default caller ID (E.164, e.g. `+12025551234`) |

Set these in `~/.openclaw/openclaw.json` — see `docs/09-openclaw-config.md`.

## Maintainer

- Creator: Chris M. / Promethean Dynamic
- Website: https://promethean-dynamic.com
- License: MIT-0
- Repository: https://github.com/cygnostik/llc-phone

## Optional config

| Key | Default | Description |
|---|---|---|
| `voice` | `"cedar"` | Realtime voice for outbound/default inbound |
| `model` | `"gpt-realtime-1.5"` | Default flagship Realtime model string |
| `prewarm_timeout_ms` | `10000` | Pre-warm / pre-accept fallback timeout (ms) |
| `eagerness` | `"high"` | Semantic VAD eagerness for first turn |
| `prompt_cache_key` | `"llc-outbound-v1"` | Prompt cache key for outbound |
| `edge_location` | `""` | Twilio edge (e.g. `umatilla`, `ashburn`) |
| `IVR_DID` | — | Inbound DID that routes to AI IVR mode |
| `RECEPTIONIST_DID` | — | Inbound DID that routes to receptionist mode |
| `CSR_DID` | — | Inbound DID that routes to CSR with DB mode |

## What this skill knows

**Outbound**
- Pre-warm pattern: <100ms to first audio after pickup; 10s fallback to cold connect
- Greeting buffer architecture, session state map, orphaned session cleanup
- Async tool calling during live conversation (CRM, calendar, notes)

**Inbound**
- Pre-accept warm: OpenAI session opens during Twilio webhook BEFORE TwiML response
- AI IVR: natural language routing, cold transfer, warm conference-bridge transfer
- Receptionist: greet, qualify, check availability, take messages, route
- CSR with DB: caller lookup by phone, appointments, notes, escalation

**Both directions**
- `gpt-realtime-1.5` vs `gpt-realtime-mini` vs legacy realtime model trade-offs
- Full `session.update` reference with recommended outbound + inbound defaults
- Semantic VAD, eagerness tuning, mid-session VAD switching
- Prompt caching via `prompt_cache_key` — structure for maximum cache hits
- Known bugs, regressions, and watch-later items with workarounds

## Docs

```
docs/
  01-overview.md            Model selection notes and current evaluation stance
  02-session-config.md      session.update reference + recommended config
  03-prewarm-outbound.md    Outbound pre-warm: buffer, fallback, edge cases
  04-inbound-modes.md       Inbound: AI IVR, receptionist, CSR with DB
  05-async-tools.md         Async tool calling for inbound and outbound
  06-latency-tuning.md      All latency levers after pre-warm / pre-accept
  07-twilio-integration.md  Twilio audio, edge colocation, AMD
  08-known-issues.md        Operational notes and watch-later items
  09-openclaw-config.md     openclaw.json config reference
```

## Version history

| Version | Notes |
|---|---|
| 3.0.3 | Sanitized SKILL.md and README — removed deployment-specific paths and host references. Technical content unchanged. |
| 3.0.2 | Prior release (see GitHub history) |
