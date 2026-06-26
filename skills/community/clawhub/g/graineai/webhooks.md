# NoddyAI Webhook Payloads

Your `webhook_url` receives POST requests from NoddyAI when call events occur.

---

## Completed Call

Sent when a call finishes successfully.

```json
{
  "id": "exec-uuid-1234",
  "agent_id": "<AGENT_ID>",
  "organization_id": "<ORG_ID>",
  "phone_number": "+911234567890",
  "status": "completed",
  "conversation_time": 45.3,
  "duration_seconds": 62,
  "total_cost": 0.012,
  "recording_url": "https://storage.example.com/rec.mp3",
  "transcript": "Agent: Hello... Customer: Hi...",
  "extracted_data": {},
  "telephony_data": {
    "provider": "jambonz",
    "provider_call_id": "jambonz-call-sid",
    "hangup_detail": "normal_clearing"
  }
}
```

## No-Answer / Voicemail / Busy

> These events are processed **internally only**. Your `webhook_url` is NOT called for `no-answer`, `voicemail`, or `busy` outcomes.

```json
{
  "id": "exec-uuid-5678",
  "status": "no-answer",
  "phone_number": "+911234567890",
  "telephony_data": {
    "hangup_detail": "voicemail_detected"
  }
}
```

---

## `status` values

| Value | Meaning |
|-------|---------|
| `completed` | Call connected and finished normally |
| `failed` | Call connected but terminated with an error |
| `no-answer` | Recipient did not pick up |
| `busy` | Recipient line was busy |
