---
name: opencawl
description: Add phone calling to your agent through OpenCawl. Use this skill to place calls, check outcomes, end active calls, and review voicemails.
homepage: https://opencawl.com
metadata: {"openclaw": {"emoji": "📞", "requires": {"env": ["OPENCAWL_API_KEY"]}, "primaryEnv": "OPENCAWL_API_KEY"}}
---

# OpenCawl

OpenCawl adds phone calling to your agent. Use it to place outbound calls, check results, end active calls, and review voicemails.

**Security:** This skill requires `OPENCAWL_API_KEY` and sends HTTPS requests to OpenCawl. Optional callbacks or inbound automations are only used if you explicitly configure them in OpenCawl.

## Setup

1. Create an OpenCawl account and API key at https://opencawl.com
2. Install the skill with `openclaw skills install opencawl`
3. Set `OPENCAWL_API_KEY` using your agent's normal environment-variable or config setup
4. Run `/opencawl setup` to confirm the skill is connected

This skill does not require editing any specific local config file.

---

## Best Use Cases

- Place a phone call for the user
- Check whether a call succeeded, failed, or went to voicemail
- End an in-progress call
- Review recent calls or voicemails

---

## Commands

### `call` — Make an outbound call

Place an outbound call. Returns a `call_id` immediately. The call runs asynchronously; use `status` to track the result.

**Parameters:**
- `to` (required): E.164 phone number, e.g. `+15551234567`
- `goal` (required): What the call should accomplish in plain language
- `context` (optional): Background the agent should know — lead source, prior interactions, objections to expect
- `persona` (optional): Voice/personality profile slug (e.g. `professional-friendly`, `direct-confident`)
- `max_duration_seconds` (optional): Hard cap on call length in seconds (default: 300, max: 1800)

Advanced options such as direct voice overrides and completion callbacks are documented in `api.md`.

**Example:**
```json
{
  "skill": "opencawl",
  "command": "call",
  "to": "+15551234567",
  "goal": "Schedule a 30-minute Workmate demo. Get their name, email, and two availability windows. If they push back, mention we have a 14-day free trial.",
  "context": "Inbound lead from the enterprise landing page. Requested info 2 days ago. Has not replied to follow-up email.",
  "persona": "professional-friendly"
}
```

**Returns:** `call_id`, `status: "ringing"`

---

### `status` — Check call outcome

Poll the status and result of any call.

**Parameters:**
- `call_id` (required): The call ID returned by `call`

**Returns:**
```json
{
  "call_id": "abc123def456",
  "direction": "outbound",
  "status": "completed",
  "outcome": "success",
  "to_number": "+15551234567",
  "goal": "Schedule a 30-minute Workmate demo",
  "persona": "professional-friendly",
  "summary": "Spoke with Jamie Chen. Scheduled demo for Thursday 2pm ET. Email: jamie@acme.com.",
  "extracted": {
    "name": "Jamie Chen",
    "email": "jamie@acme.com",
    "availability": ["Thursday 2pm ET", "Friday 10am ET"]
  },
  "duration_seconds": 187,
  "transcript": "...",
  "recording_url": "https://api.twilio.com/...",
  "created_at": "2026-03-28T14:00:00Z",
  "completed_at": "2026-03-28T14:03:07Z"
}
```

Possible `status` values: `initiated`, `queued`, `ringing`, `in_progress`, `completed`, `failed`, `no_answer`, `voicemail`, `busy`

---

### `calls` — List recent calls

List calls with optional filtering.

**Parameters:**
- `status` (optional): Filter by status
- `from` (optional): ISO date range start
- `to` (optional): ISO date range end
- `limit` (optional): Max results (default: 20, max: 100)
- `cursor` (optional): Pagination cursor from previous response

---

### `hangup` — End a call

Terminate an in-progress call.

**Parameters:**
- `call_id` (required): Call to end
- `reason` (optional): Logged reason (e.g. `"goal_achieved"`, `"no_answer_threshold"`)

---

### `voicemail` — Check voicemail inbox

List and read voicemails left on your OpenCawl number.

**Parameters:**
- `limit` (optional): Max results (default: 10)
- `unread_only` (optional): `true` to filter to unheard messages

---

### `credits` — Check balance

**Returns:** Credit balance, plan name, estimated minutes remaining, next reset date

---

### `setup` — First-time initialization

Reports your current phone number, credits, and calling configuration. Run once after installing the skill.

```
/opencawl setup
```

---

## Personas

Personas define how OpenCawl sounds and behaves on calls.

| Slug | Voice | Best For |
|------|-------|----------|
| `professional-friendly` | Emily | B2B outreach, demos, enterprise |
| `direct-confident` | Thomas | Executive outreach, follow-ups |
| `empathetic-support` | Serena | Support, onboarding, check-ins |
| `energetic-sales` | Freya | SMB sales, product promotions |
| `neutral-informational` | Adam | Appointment reminders, surveys |

Pass the persona slug in the `call` command. If omitted, OpenCawl uses your current default voice configuration.

See `personas.md` for optional voice overrides and plan-specific voice features.

---

## Optional Advanced Usage

Inbound calling, completion callbacks, and task routing are available, but they are not required for normal outbound calling.

Only configure those features if your agent or app exposes a public HTTPS endpoint that you control.

## Reference Files

- `api.md` — Full API reference and advanced request fields
- `inbound.md` — Optional inbound automation and task-routing setup
- `personas.md` — Persona reference and optional voice overrides
