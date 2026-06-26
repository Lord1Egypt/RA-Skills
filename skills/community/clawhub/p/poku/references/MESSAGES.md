# SMS, WhatsApp & Slack — Messaging Flow

> **Always use the specific sub-endpoint for each message type.**
> There is no generic `/messages` endpoint.
> - SMS → `POST /messages/sms`
> - WhatsApp → `POST /messages/whatsapp`
> - Slack → `POST /messages/slack`
> - Saved channel → `POST /messages/<CHANNEL_ID>`

---

## Step A: Resolve the Phone Number (SMS & WhatsApp only)

Convert to E.164 format:
- Strip formatting, prepend country code (`+1` for US/Canada)
- If given a contact name, ask the user for the number — do not guess
- If given a business name, use the search tool, then confirm with the user

For Slack, you need a **Slack user, member, or channel ID** (e.g. `U12345678`) — not a phone number.

---

## Step B: Draft and Confirm the Message

Use a matching template from the **Message Templates** section below. Fill in every `[placeholder]` — never leave one blank.

Show the draft clearly before sending:

> **Draft:**
> "[message body]"
>
> Sending to [number or ID] via [SMS / WhatsApp / Slack] — good to go?

Do not send until the user confirms.

---

## Step C: Send the Message

### Send an SMS

```bash
curl -s -X POST https://api.pokulabs.com/messages/sms \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "<message body>",
    "to": "<E.164 number>",
    "waitTime": 60,
    "followUpTime": 6000
  }'
```

`waitTime` (1–600s): hold the request open waiting for a reply.
`followUpTime` (1–60000s): keep listening after `waitTime` closes; replies delivered via webhook.

Both are optional — omit them if no reply is expected.

---

### Send a WhatsApp Message

**Option 1 — Free-form from Poku's WhatsApp account:**

```bash
curl -s -X POST https://api.pokulabs.com/messages/whatsapp \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "<message body>",
    "to": "<E.164 number>"
  }'
```

**Option 2 — From your own WhatsApp number using a Meta-approved template:**

```bash
curl -s -X POST https://api.pokulabs.com/messages/whatsapp \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "template": {
      "id": "<template UUID from Meta Business>",
      "variables": {
        "name": "<value>",
        "time": "<value>"
      }
    },
    "to": "<E.164 number>",
    "from": "<your WhatsApp-enabled E.164 number>"
  }'
```

---

### Send a Slack Message

Prerequisite: you must have joined the Poku Slack workspace or added the Poku bot to your own workspace.

```bash
curl -s -X POST https://api.pokulabs.com/messages/slack \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "<message body>",
    "to": "<Slack user/member/channel ID>",
    "from": "<Slack workspace ID — omit to send from Poku workspace>"
  }'
```

---

### Send via a Saved Channel. Must configure a channel card on the Poku dashboard and retrieve a channel_ID first.

```bash
curl -s -X POST https://api.pokulabs.com/messages/<CHANNEL_ID> \
  -H "Authorization: Bearer $POKU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "<message body>",
    "waitTime": 60
  }'
```

Use `medium` to override the channel type (`"sms"`, `"whatsapp"`, or `"slack"`). Use `to` and `from` to override recipient/sender.

---

## Message Templates

Use the closest match and adapt as needed. Fill every `[placeholder]`.

---

### Scheduling

```
Hi, I'm reaching out on behalf of [user name] to coordinate [activity] for you both. Let me know a few times that you're available [timeframe]!
```

---

### Follow-Up After a Call

```
Hi, this is [user name] following up on our recent conversation about [topic]. [One sentence summary of next step or ask.] Feel free to reply here or call back at your convenience.
```

---

### General / Other

```
Hi, this is a message on behalf of [user name]. [State the purpose in one or two plain sentences.] [Optional: include a call to action — reply, call back, confirm, etc.] Thank you.
```
