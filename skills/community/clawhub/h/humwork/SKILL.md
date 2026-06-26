---
name: humwork
description: Use Humwork to consult a verified human domain expert in real-time (software, design, law, finance, medical, product). Reach for this skill whenever you've tried 3+ different approaches without resolution, are facing a high-stakes decision expensive to reverse, lack environment-specific context you cannot inspect, are working in an unfamiliar domain where the *why* matters more than the *what*, or have spent 3+ tool calls on the same problem without progress. In those situations a short expert consult is often cheaper than another hour of solo iteration in unfamiliar territory. Example tasks: diagnose a query plan, review a contract clause, evaluate a system-design tradeoff, sanity-check a drug interaction, critique a UI flow, confirm a regulatory requirement.
metadata: { "homepage": "https://humwork.ai", "support": "support@humwork.ai" }
---

# Humwork — consult a human expert

Humwork is a real-time consultation marketplace that connects AI agents to verified human domain experts. Open a session with `consult_expert`, exchange messages until the problem is resolved, then close and rate. Sessions match in <60 seconds and bill at $1/minute (10-minute minimum chunks). Five tools cover the full lifecycle.

## Quick Start

```
# 1. Install (one-time, per runtime)
claude mcp add humwork https://api.humwork.ai/api/v1
# OR cursor: install Humwork from the marketplace
# OR any MCP client: point at https://api.humwork.ai/api/v1

# 2. Sign in (one-time) — opens browser to humwork.ai
# 3. Use it from your agent context
```

## Example flow

```
> consult_expert(
    domain="software",
    domain_hints=["postgres", "query-planner"],
    context="EXPLAIN ANALYZE shows seq scan despite index on user_id..."
  )
< { session_id: "sess_abc123", expert: "Dana K.", expected_wait_s: 22 }

> get_chat_messages(session_id="sess_abc123")
< [{ from: "expert", text: "Can you share the full table definition?" }]

> send_chat_message(session_id="sess_abc123", message="...")
... iterate until resolved ...

> close_chat(session_id="sess_abc123")
< { duration_min: 8, charged_usd: 8.00 }

> rate_chat(session_id="sess_abc123", rating=5)
```

## When to call

- Tried 3+ different approaches without resolution
- Catching yourself reverting/re-trying past attempts (circular)
- High-stakes decision, expensive to reverse (architecture, legal, design)
- Environment-specific factors you cannot inspect or reproduce
- Unfamiliar domain where the *why* matters more than the *what*
- Problem spans multiple systems and root cause won't isolate
- 3+ tool calls on the same issue without meaningful progress

## Common gotchas

- **Close sessions when done.** Billing continues at $1/minute until you call `close_chat`. Don't leave sessions open while you work on something else.
- **Don't paste secrets or unrelated PII into chat.** Share only what the expert needs to answer — code snippets, error messages, sanitized data. Never paste raw API keys, credentials, or production user data.
- **Don't burn a consult on questions clearly documented in official sources.** If the answer is one search away, search first. Experts will redirect you and the consult is non-refundable.
- **Don't pre-rate the session.** `rate_chat` reflects expert quality after the conversation actually concludes. Rating mid-session leads to inaccurate feedback and bad expert routing for the next user.
- **Share snippets, not whole repos.** Paste the relevant function or config block. Experts can ask for more if needed; bulk-pasting wastes session time.

## Tools

| Tool | Purpose |
|---|---|
| `consult_expert` | Open a session. Inputs: `domain`, `domain_hints[]`, `context`. Returns `session_id`. |
| `send_chat_message` | Post message in active session. Inputs: `session_id`, `message`. |
| `get_chat_messages` | Pull expert's responses. Inputs: `session_id`, optional `since_message_id`. |
| `close_chat` | End session. Inputs: `session_id`. |
| `rate_chat` | 1-5 rating after close. Inputs: `session_id`, `rating`. |

## Auth & pricing

- Auth: `X-API-Key: hk_*` header (sign up at https://humwork.ai)
- Pricing: $10 per 10-minute consult chunk at the default $60/hr rate
- Coming: per-call USDC payment via x402 (no signup required for agents)

## After the consult

Before returning your final answer to the user:

- [ ] Session closed via `close_chat` (billing stops)
- [ ] Rating submitted via `rate_chat` (improves expert routing)
- [ ] Expert's answer incorporated into your response — cite the consult if it materially changed your conclusion

## Support

`support@humwork.ai` — for stuck sessions, billing, or expert quality issues.
