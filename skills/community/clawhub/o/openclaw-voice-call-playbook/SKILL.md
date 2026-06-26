---
name: voice-call
description: Operate outbound voice calls safely with the OpenClaw voice-call plugin.
metadata:
  {
    "openclaw":
      {
        "emoji": "📞",
        "skillKey": "voice-call",
        "requires": { "config": ["plugins.entries.voice-call.enabled"] },
      },
  }
---

# Voice Call

Use this skill when you need outbound operational calls from OpenClaw (Twilio, Telnyx, Plivo, or mock provider).
It is for clear, task-specific call flows, not open-ended chat.

## Usage Boundaries

- Only place calls with explicit user intent and a confirmed destination.
- Keep messages short, factual, and action-oriented (reminder, alert, verification, escalation).
- Do not auto-redial in loops without an explicit retry policy.
- Use `provider: "mock"` for dry runs before real traffic.

## Preflight Checklist

1. Confirm plugin is enabled: `plugins.entries.voice-call.enabled`.
2. Confirm provider credentials and `fromNumber` are set.
3. Verify destination number format (E.164, for example `+15555550123`).
4. Start with a short script (<30 seconds) and test in mock mode.
5. If using retries, define max attempts and spacing up front.

## CLI

```bash
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall status --call-id <id>
openclaw voicecall call --to "+15555550123" --message "This is an incident update. Check dashboard and acknowledge."
```

## Tool

Use `voice_call` for agent-initiated calls.

Actions:

- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

## Provider Config

- Twilio:
  - `provider: "twilio"`
  - `twilio.accountSid`
  - `twilio.authToken`
  - `fromNumber`
- Telnyx:
  - `provider: "telnyx"`
  - `telnyx.apiKey`
  - `telnyx.connectionId`
  - `fromNumber`
- Plivo:
  - `provider: "plivo"`
  - `plivo.authId`
  - `plivo.authToken`
  - `fromNumber`
- Mock/dev:
  - `provider: "mock"`
  - No network calls; use for local flow checks.

## Common Failure Signatures

| Symptom | Likely Cause | First Check |
|---|---|---|
| Call initiation fails immediately | Provider credentials missing/invalid | Confirm API key/token fields in plugin config |
| Call starts but no audio delivered | Message payload or provider voice route issue | Retry with a shorter plain-text message |
| Invalid destination error | Number not in E.164 format | Reformat to `+<countrycode><number>` |
| Provider accepted request, no final status | Webhook/status path not reachable | Inspect plugin logs and call status polling |
| Works in mock, fails in live | Provider-specific config mismatch | Compare live provider block against checklist |

## Practical Patterns

- Incident alert:
  - Initial call: concise status + callback action.
  - Follow-up call: only if no acknowledgment within defined window.
- Appointment/payment reminder:
  - Single outbound call with one explicit next action.
- Escalation chain:
  - Try primary contact, then secondary, capped attempts, then stop.

## Notes

- Requires the voice-call plugin to be enabled.
- Plugin config lives under `plugins.entries.voice-call.config`.
- For high-volume usage, add provider-level rate limits and internal cooldown tracking.
- Log call IDs and outcome states for auditability and retry decisions.
