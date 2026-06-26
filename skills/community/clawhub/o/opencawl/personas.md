# Personas & Voice Configuration

Personas define how OpenCawl sounds and behaves on calls. For most agents, using a persona slug is the simplest option.

---

## Built-in Personas

| Slug | Voice | Style | Best For |
|------|-------|-------|----------|
| `professional-friendly` | Emily | Calm, professional | B2B outreach, demos, enterprise |
| `direct-confident` | Thomas | Clear, authoritative | Executive outreach, follow-ups |
| `empathetic-support` | Serena | Soft, soothing | Support, onboarding, check-ins |
| `energetic-sales` | Freya | Gentle, upbeat | SMB sales, product promotions |
| `neutral-informational` | Adam | Deep, clear default | Appointment reminders, surveys |

Pass a persona slug in the `call` command's `persona` field. If omitted, your dashboard voice selection is used.

---

## Optional Voice Override

If your agent already knows a specific voice ID, you can pass `voice_id` directly in the `call` command. Otherwise, prefer `persona`.

## Examples

Pass the persona slug in any `call` command:

```json
{
  "to": "+15551234567",
  "goal": "Qualify the lead and book a demo",
  "persona": "professional-friendly"
}
```

Or use a direct voice override:

```json
{
  "to": "+15551234567",
  "goal": "Qualify the lead and book a demo",
  "voice_id": "rachel"
}
```

Priority: `persona` > `voice_id` > dashboard default.

If both `persona` and `voice_id` are provided, `persona` wins.
