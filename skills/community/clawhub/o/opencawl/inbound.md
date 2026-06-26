# Inbound Call Handling

Inbound calling is optional. You do not need any inbound setup to place outbound calls.

Inbound calls support two modes configured in OpenCawl:

| Mode | How it works |
|------|-------------|
| `autonomous` (default) | Preferred mode. ElevenLabs handles the live call loop with OpenCawl-provided per-user overrides. |
| `voicemail_only` | Caller goes straight to voicemail. Transcription available if enabled. |

---

## Basic Setup

1. Open the OpenCawl dashboard and choose your inbound mode, greeting, prompt, and voicemail settings.
2. If you want inbound calls to trigger actions in your own agent or app, add a public HTTPS callback endpoint in the dashboard.
3. If that callback requires bearer authentication, set `gateway_token` so OpenCawl can send `Authorization: Bearer <gateway_token>`.

---

## Live Call Pattern

Each inbound autonomous call follows this loop:

```
1. Caller speaks
2. OpenCawl applies the user's voice, prompt, and greeting settings
3. OpenCawl and its telephony providers run the live conversation
4. If real work is needed, OpenCawl can dispatch a task to the configured callback endpoint
5. The agent or app completes the task and reports the result back to OpenCawl
6. After hangup, OpenCawl stores the transcript and call outcome
```

---

## Callback Safety

Only configure `gateway_webhook` if you trust the receiving endpoint with call-related task data. If you set `gateway_token`, OpenCawl sends it as bearer auth to that endpoint.

---

## Prompt Guidance

Keep the user-level inbound prompt short and durable. Good default shape:

```text
You are OpenCawl for this user.
Be concise and natural on the phone.
Confirm the requested task before acting.
Use the OpenCawl task tools for external actions.
Do not claim success until a tool or downstream system confirms it.
```

For exact request and response shapes, see `api.md`.
