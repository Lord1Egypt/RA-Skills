# Audit Log Format

## audit.json Structure

```json
{
  "entries": [
    {
      "timestamp": "2026-03-28T03:00:00Z",
      "requester": {
        "contact_id": "example_contact",
        "relationship": "friend",
        "platform_id": "telegram:000000000"
      },
      "request": {
        "raw_message": "What's their birthday?",
        "category": "personal_facts",
        "level": 2
      },
      "outcome": "allowed",
      "shared": "1990-01-15",
      "context": "direct_message"
    }
  ]
}
```

## Outcome Values

- `allowed` — permission check passed, information shared
- `denied` — permission check failed, request declined
- `asked_user` — no clear policy, user was prompted
- `user_approved` — user approved after being asked
- `user_denied` — user denied after being asked
- `flagged` — potential prompt injection or manipulation attempt

## Required for Every Entry

- timestamp, requester info, what was requested, outcome
- If `allowed`/`user_approved`: what was actually shared
- If `flagged`: the raw message that triggered the flag
