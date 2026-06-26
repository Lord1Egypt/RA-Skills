---
name: openphone
description: Manage business phone calls, SMS, and contacts via OpenPhone API. Use when asked to send a text message, list calls or messages, look up conversation history with a contact, get voicemail transcripts, list phone numbers, or check call recordings. Requires OPENPHONE_API_KEY env var.
---

# OpenPhone Skill

OpenPhone REST API base: `https://api.openphone.com/v1`

## Auth
```bash
curl -H "Authorization: $OPENPHONE_API_KEY" \
     -H "Content-Type: application/json" \
     https://api.openphone.com/v1/...
```

## Phone Numbers

### List Your Phone Numbers
```bash
curl "https://api.openphone.com/v1/phone-numbers" \
  -H "Authorization: $OPENPHONE_API_KEY"
# Save phoneNumberId for sending messages/calls
```

## Contacts

### Search Contacts
```bash
curl "https://api.openphone.com/v1/contacts?query=John+Smith" \
  -H "Authorization: $OPENPHONE_API_KEY"
```

### Create Contact
```bash
curl -X POST "https://api.openphone.com/v1/contacts" \
  -H "Authorization: $OPENPHONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Jane",
    "lastName": "Smith",
    "phoneNumbers": [{"number": "+15551234567"}],
    "emails": [{"address": "jane@acme.com"}],
    "company": "Acme Corp"
  }'
```

## Messages (SMS/MMS)

### Send SMS
```bash
curl -X POST "https://api.openphone.com/v1/messages" \
  -H "Authorization: $OPENPHONE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "<phoneNumberId>",
    "to": ["+15551234567"],
    "content": "Hi Jane, following up on our conversation earlier!"
  }'
```

### List Messages (Conversation History)
```bash
curl "https://api.openphone.com/v1/messages?phoneNumberId=<id>&participants[]=+15551234567&maxResults=20" \
  -H "Authorization: $OPENPHONE_API_KEY"
```

## Calls

### List Calls
```bash
curl "https://api.openphone.com/v1/calls?phoneNumberId=<id>&maxResults=20" \
  -H "Authorization: $OPENPHONE_API_KEY"
```

### Get Call Details (Recording + Transcript)
```bash
curl "https://api.openphone.com/v1/calls/<call_id>" \
  -H "Authorization: $OPENPHONE_API_KEY"
# Response includes: recordingUrl, transcript (if enabled), duration, direction
```

### List Voicemails
```bash
curl "https://api.openphone.com/v1/calls?type=voicemail&phoneNumberId=<id>" \
  -H "Authorization: $OPENPHONE_API_KEY"
```

## Call Directions
`incoming`, `outgoing`

## Message Status Values
`queued`, `sending`, `delivered`, `failed`, `received`

## Tips
- `phoneNumberId` starts with `PN` — always list phone numbers first
- Transcripts require call recording to be enabled in workspace settings
- Rate limit: 60 req/min; batch message sends in loops with brief delays
