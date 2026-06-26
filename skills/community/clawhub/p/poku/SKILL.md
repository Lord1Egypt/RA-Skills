---
name: poku
description: "Sends and receives phone calls and messages (like SMS, WhatsApp, Slack), and reserves dedicated phone numbers using the Poku API. Example use cases: calling a restaurant for a reservation, having a text conversation with a friend to arrange a meeting, accepting calls on a business number during off hours. Use this skill any time the user wants to do actions like call or message someone, or reserve a phone number, even if they never mention 'Poku'."
metadata: { "openclaw": { "homepage": "https://pokulabs.com", "requires": { "env": ["POKU_API_KEY"] }, "primaryEnv": "POKU_API_KEY" }, "api_base": "https://api.pokulabs.com" }
---

# Poku — Calls, Messages & Numbers

## Variables

- `POKU_API_KEY` *(required)* — Poku API key. If not set, see **Troubleshooting** below.
- `POKU_TRANSFER_NUMBER` *(optional)* — E.164 number to transfer calls to if the counterparty asks to speak with a human.

Never display any full command with a resolved API key in user-facing output. Mask the key if showing commands for debugging: `Bearer ***`.


## Skill Overview

Here's what you can do with Poku:

**Reserve a dedicated number** — Claim a phone number to send/receive calls and messages with.

**Make calls** — Call on your behalf, speak naturally, handle responses, and report back what happened. Calls use a female English voice by default; just ask if you'd like a male voice or different language.

**Send messages** — Send SMS messages from your dedicated number.

**Send WhatsApp messages** — Reach contacts on WhatsApp through a shared Poku WhatsApp number.

To receive inbound calls or texts, a webhook is required. 

---

## Phone Number Format

Always use **E.164 format**: `+` then country code then number.

- `+12223334444` ✓
- `(222) 333-4444` ✗
- `222-333-4444` ✗
- `2223334444` ✗

If a human gives you a US number without a country code, confirm with them that it should be US `+1`. If not, ask the user which country and country code this number is for.

---

## Outbound Call or Message 

If call, use `reference/CALLS.md`  
If message, use `reference/MESSAGES.md`

Always go through each step before placing a call, NEVER skip any steps.

---

## Troubleshooting

### OpenClaw: POKU_API_KEY not found

If the API key is missing, tell the user:

> "Your Poku API key isn't configured. Open `~/.openclaw/openclaw.json` and add the following block, then run `openclaw gateway restart`:"

```json
{
  "skills": {
    "entries": {
      "poku": {
        "enabled": true,
        "apiKey": "<your-poku-api-key>",
        "env": {
          "POKU_TRANSFER_NUMBER": "<your-transfer-number>"
        }
      }
    }
  }
}
```

Get your API key from [dashboard.pokulabs.com](https://dashboard.pokulabs.com).

After restarting, verify the skill loaded:
```bash
openclaw skills list --eligible
# poku should appear in the list
```

---

## Reference Files

| File | When to read |
|---|---|
| `references/CALLS.md` | When making an outbound call |
| `references/CALL-TEMPLATES.md` | When drafting a call prompt (Step 3) |
| `references/MESSAGES.md` | When sending a message (like SMS, WhatsApp, Slack, etc) |
| `references/MESSAGE-TEMPLATES.md` | When drafting a message prompt |
| `references/NUMBERS.md` | When reserving or managing phone numbers |
| `references/WEBHOOKS.md` | When setting up inbound calls/texts or advanced config |
| `references/API.md` | When you need full endpoint parameters |

## Learn More

- **Full API reference for LLMs:** [docs.pokulabs.com/llms.txt](https://docs.pokulabs.com/llms.txt)
- **Interactive docs:** [docs.pokulabs.com](https://docs.pokulabs.com)
- **Issues, feedback, feature requests:** email `hello@pokulabs.com`
