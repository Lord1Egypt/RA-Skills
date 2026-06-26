---
name: pallio
description: Chat with Pallio AI knowledge-base personas. Ask questions against curated document collections with RAG-powered citations.
user-invocable: true
metadata:
  openclaw:
    emoji: "🧠"
    homepage: "https://pallioai.com"
    requires:
      env:
        - PALLIO_PERSONA_ID
    primaryEnv: PALLIO_PERSONA_ID
---

# Pallio AI — Knowledge Base Chat

You can chat with a Pallio AI persona — an AI assistant backed by a curated knowledge base of uploaded documents. The persona answers questions using RAG (Retrieval-Augmented Generation) with document citations.

## Setup

The user must set the `PALLIO_PERSONA_ID` environment variable to the ID of a public Pallio persona. Browse available personas at https://pallioai.com/community.

## How to Use

### Step 1: Initialize a Session

Before sending any messages, initialize a session to get an authentication token.

```bash
curl -s "https://pallioai.com/api/widget/init/$PALLIO_PERSONA_ID"
```

The response contains:
- `token` — Session token (valid for 2 hours). Store this for all subsequent messages.
- `persona.name` — The persona's display name.
- `persona.welcomeMessage` — An introductory message from the persona. Show this to the user.
- `persona.starterPrompts` — Suggested first questions. Offer these to the user.
- `persona.messageLimit` — Maximum free messages per session (typically 3).

### Step 2: Send Messages

Send the user's message with the session token. Maintain conversation history for context.

```bash
curl -s -X POST "https://pallioai.com/api/widget/chat" \
  -H "X-Widget-Token: $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What topics do you cover?",
    "history": []
  }'
```

The `history` array should contain all previous messages in the conversation:
```json
[
  { "role": "user", "content": "What topics do you cover?" },
  { "role": "assistant", "content": "I cover fire safety procedures..." },
  { "role": "user", "content": "Tell me more about ventilation." }
]
```

The response contains:
- `response` — The AI-generated answer. Display this to the user.
- `sources` — Array of `{ title, page }` objects. Display these as citations below the response.
- `messageNumber` — Which message this is (1, 2, 3...).
- `messagesRemaining` — How many free messages remain.
- `nudge` — If `"signup_soft"`, gently suggest signing up. If `"signup_required"`, the session is exhausted.
- `signupUrl` — URL for the user to create a full Pallio account.

### Step 3: Display Sources

When `sources` is present and non-empty, format citations below the response:

```
Sources:
- Document Name (p. 42)
- Another Document (p. 15)
```

### Step 4: Handle the Message Limit

Each session allows a limited number of free messages (typically 3).

- When `messagesRemaining` reaches 0 or `nudge` is `"signup_required"`, inform the user:
  "You've used all free messages for this session. Sign up for full access: {signupUrl}"
- To start a new session, call the init endpoint again (rate limited to 30/hour).

For **unlimited access**, the user can get a Pallio API key (Professional tier or higher) — see https://pallioai.com/settings.

## Error Handling

| Error Code | Meaning | Action |
|-----------|---------|--------|
| `SESSION_NOT_FOUND` | Token is invalid | Re-initialize the session |
| `SESSION_EXPIRED` | Token TTL exceeded (2 hours) | Re-initialize the session |
| `MESSAGE_LIMIT_REACHED` | Free messages exhausted | Show signup URL |
| `RATE_LIMITED` | Too many requests | Wait and retry (check `retryAfter` field) |
| `PERSONA_NOT_FOUND` | Invalid persona ID | Verify PALLIO_PERSONA_ID is correct |
| `WIDGET_DISABLED` | Persona owner disabled widget | Try a different persona |

## Important Notes

- Sessions expire after 2 hours. If you get `SESSION_EXPIRED`, initialize a new session.
- Rate limits: 30 session inits per IP per hour, 10 messages per IP per hour.
- The persona only answers from its uploaded knowledge base — it will not fabricate answers.
- This is the free widget endpoint. For full RAG pipeline access (hybrid search, more tokens, higher limits), use the Pallio Agent API with an API key.
