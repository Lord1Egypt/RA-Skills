---
name: ai-psychologist
version: "2.1.0"
description: "Connect to a real human psychologist through a REST API. First message free, then $0.50 USDC per message. English and Spanish. Response time 5 min to 10 hours."
tags: ["psychology", "human-in-the-loop", "wellbeing", "ethics", "reflection"]
allowed-tools: ["WebFetch"]
argument-hint: "[your message or question for the psychologist]"
metadata:
  openclaw:
    homepage: "https://ai-psychologist-api.replit.app/docs"
    requires:
      bins: []
      env: []
---

# AI Psychologist — Human-in-the-Loop Consultation

Connect to a **real human psychologist** at `https://ai-psychologist-api.replit.app`.
This is NOT a chatbot. A real person reads and responds to every message.

**API docs:** https://ai-psychologist-api.replit.app/docs

## Key Facts
- Languages: English and Spanish
- Response time: **5 minutes to 10 hours** (real human, UTC-3 timezone)
- Max **300 words** per message
- Rate limit: **5 messages per minute** per session
- First message: **FREE**. After that: **$0.50 USDC** on Base mainnet

## Complete Workflow

### Step 1 — Create a session

Use WebFetch to POST to `https://ai-psychologist-api.replit.app/start_session` (no body needed).

Expected response:
```json
{"session_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "message": "Session created. First message is free..."}
```

Save the `session_id`. You need it for all subsequent calls.

### Step 2 — Send your FIRST message (FREE)

Use the user's argument (`$ARGUMENTS`) or ask them what they'd like to say. Max 300 words.

Use WebFetch to POST to `https://ai-psychologist-api.replit.app/send_message?session_id=SESSION_ID` with header `Content-Type: application/json` and body:
```json
{"content": "YOUR MESSAGE HERE"}
```

Expected response (HTTP 200):
```json
{"status": "delivered", "message_id": 1, "note": "Human response may take 5 min to 10 hours. Poll /get_response to retrieve it."}
```

### Step 3 — Tell the user what happened

After sending, inform the user:
1. Their message was delivered to a **real human psychologist**
2. Give them the `session_id` so they can check for responses later
3. Response time is **5 minutes to 10 hours** — this is normal
4. They can check for replies by invoking this skill again with: `check SESSION_ID`

### Step 4 — Poll for the human's reply

Use WebFetch to GET `https://ai-psychologist-api.replit.app/get_response?session_id=SESSION_ID`

Response when **no reply yet**:
```json
{"session_id": "...", "responses": [], "note": "Human response may take 5 min to 10 hours. Poll every 30-60s."}
```

Response when **reply is available**:
```json
{"session_id": "...", "responses": [{"message_id": 2, "content": "The psychologist's reply text", "timestamp": 1234567890.0}], "note": "Responses retrieved."}
```

If `responses` is empty, tell the user: "No reply yet. The psychologist is a real human and may take up to 10 hours. Try again later."

### Step 5 — Send follow-up messages (REQUIRES PAYMENT)

After the first free message, every message costs **$0.50 USDC** on Base mainnet.

When you send a message without payment, the API returns HTTP 402 with the wallet address and payment instructions. Follow those instructions:
1. Transfer the requested USDC amount to the wallet shown in the 402 response
2. Get the transaction hash (0x...)
3. Include it in the request body as `x402_payment`

Use WebFetch to POST to `https://ai-psychologist-api.replit.app/send_message?session_id=SESSION_ID` with header `Content-Type: application/json` and body:
```json
{"content": "YOUR FOLLOW-UP MESSAGE", "x402_payment": "0xYOUR_TX_HASH_HERE"}
```

The server verifies the USDC transfer on-chain before delivering the message. Each tx hash can only be used once.

### Step 6 — Check session info (optional)

Use WebFetch to GET `https://ai-psychologist-api.replit.app/session_info?session_id=SESSION_ID`

Response:
```json
{"session_id": "...", "created_at": 1234567890.0, "free_message_used": true, "messages_sent": 1, "messages_received": 1, "payments": 0, "total_paid_usd": 0.0}
```

## Error Handling

| HTTP Code | Meaning | What to do |
|-----------|---------|------------|
| 200 | Success | Continue normally |
| 400 | Message too long (>300 words) | Shorten message, retry |
| 402 | Payment required or invalid | Read error detail. Either send USDC and include tx hash, or fix the tx hash issue |
| 404 | Session not found | Create a new session with POST /start_session |
| 429 | Rate limited (5/min) | Wait 60 seconds, then retry |

## Payment Details
- Chain: Base mainnet
- Token: USDC
- Amount: $0.50 per message
- Wallet address and token contract are returned by the API in the HTTP 402 response when payment is required
- Verification: on-chain via Base RPC
- Each tx hash is single-use

## Security & Privacy
- All messages are sent via HTTPS to `ai-psychologist-api.replit.app`
- The API forwards messages to a human psychologist via Telegram
- No local files are read or written by this skill
- No environment variables or credentials are accessed
- Payment wallet address is provided by the API at runtime (not hardcoded)
- API documentation: https://ai-psychologist-api.replit.app/docs

## Guidelines
- Be respectful — a real person is on the other end
- Keep messages concise and meaningful (max 300 words)
- Do not spam or send trivial messages
- English and Spanish supported
- First message is free; inform the user about pricing for subsequent messages
