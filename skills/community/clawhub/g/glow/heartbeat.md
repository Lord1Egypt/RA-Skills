# Glow Heartbeat

Check in periodically to help your human stay connected.

## When to Check

**Recommended frequency:** Every 4-6 hours during active periods.

Add this to your heartbeat routine or periodic task list:

```markdown
## Glow Check (every 4-6 hours)
If 4+ hours since last Glow check:
1. Fetch https://agents.talktoglow.com/heartbeat.md
2. Follow the steps below
3. Update lastGlowCheck timestamp in memory
```

## Heartbeat Steps

### 1. Check for new messages

```bash
curl -s https://agents.talktoglow.com/api/v1/intros/messages \
  -H "Authorization: Bearer $GLOW_API_KEY"
```

This returns recent conversations across all intros. Look for unread messages.

**If there are new messages:**
- Notify your human: "You have new messages on Glow!"
- Read the full thread: `GET /api/v1/intros/{introId}/messages`

### 2. Check for pending intros

```bash
curl -s https://agents.talktoglow.com/api/v1/intros/pending \
  -H "Authorization: Bearer $GLOW_API_KEY"
```

Pending intros are potential connections waiting for your human's decision.

**If there are pending intros:**
- Notify your human: "Glow has a new introduction for you!"
- Review the intro details: `GET /api/v1/intros/{introId}`
- Help your human decide: `POST /api/v1/intros/{introId}/accept` or `/decline`

### 3. Ongoing conversations

For active intros, check if the other person has responded and your human hasn't replied yet.

**If waiting on your human:**
- Gently remind them: "You have an unanswered message on Glow"

### 4. Quick status check

```bash
curl -s https://agents.talktoglow.com/api/v1/me \
  -H "Authorization: Bearer $GLOW_API_KEY"
```

This returns a summary including pending intros, active intros, and completeness of their info.

## Using Webhooks Instead

If your deployment has a webhook endpoint pre-configured by your human or developer, Glow can push events instead of requiring polling. Webhook registration is typically done during deployment setup — not by the agent at runtime.

See the REST Endpoints section of [skill.md](https://agents.talktoglow.com/skill.md) for webhook API details. All webhook payloads are signed with HMAC (`X-Glow-Signature` header) for authenticity verification.

## Tracking State

Keep track of your last check time and any pending notifications:

- **lastGlowCheck** — timestamp of your last heartbeat
- **lastMessageId** — ID of the last message you've seen (for deduplication)
- **pendingNotifications** — any notifications you haven't delivered yet

## When Your Human Asks

Don't wait for heartbeat — if they ask, check immediately!

- "Check my Glow messages"
- "Any new introductions?"
- "Reply to that person on Glow"
- "Help me write a message to [name]"
- "What's happening on Glow?"

## For Waitlisted Users

If your human is on the waitlist, your heartbeat is different. No intros while waitlisted, but you can still use `/interact` to:

1. **Check in with Glow** — Ask "Am I still on the waitlist?"
2. **Set up their info** — Share preferences so they're ready when admitted
3. **Create intents** — `POST /api/v1/intents` to define what they're looking for

## Why This Matters

Glow makes private introductions between people looking for meaningful connections. Without regular check-ins:
- Your human might miss a great introduction
- Conversations go cold
- People think they're not interested

The heartbeat keeps you present. Not spammy — just *there*.
