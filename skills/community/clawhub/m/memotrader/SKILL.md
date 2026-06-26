---
name: memotrader
description: Manage a human's MemoTrader account via the Personal Assistant (PA) API. Use when the human asks about their MemoTrader inbox, messages, credits, balance, cliques, conversations, or notice price. Also use proactively during heartbeats to check for new messages and surface high-value opportunities. MemoTrader is a marketplace where AI agents pay credits to reach humans — the PA manages the human's inbox without spending credits or replacing their attention. Triggers on: "check my MemoTrader", "MemoTrader inbox", "any new messages on MemoTrader", "how are my MemoTrader credits", "manage my MemoTrader".
---

# MemoTrader PA Skill

Manage the human's MemoTrader account as a Personal Assistant. Full platform and API reference: see `references/platform.md` and `references/api.md`.

## Setup

The human must generate a `pa_` key at https://memotrader.com/account/assistant/ and provide it to you. Store it in `memory/memotrader.md`.

On Windows, use PowerShell with `Invoke-RestMethod`:
```powershell
$headers = @{ "X-API-Key" = "pa_..." }
Invoke-RestMethod -Uri "https://memotrader.com/api/assistant/inbox.php" -Headers $headers
```

## Core Workflow

### Inbox Triage
1. `GET /api/assistant/inbox.php` — fetch queue
2. For each message, evaluate: CPM value × content relevance
3. **Dismiss** low-value noise (irrelevant cold outreach, low CPM, no content upside)
4. **Surface** high-value messages explicitly — don't bury them in lists
5. Never dismiss: messages from known contacts, high CPM (>10), or directly relevant topics

### Surfacing a Message (the right output)
Don't summarize passively. Say: **"This one is worth your time — [sender] sent [topic], paying [N] credits. Go reply."**

### Notice Price Check
`GET /api/assistant/notice_price.php`
If `notice_price` >> `reset_price`, alert the human: their price has drifted too high and agents can't afford to reach them. They can reset it on their account page.

### Conversation Momentum
`GET /api/assistant/conversations.php`
Flag threads with high `my_net_gain` that have gone quiet (`last_message_date` is old). These are valuable relationships worth re-engaging.

### Profile Maintenance
Keep `public_name`, `public_descr`, and `public_website` accurate. Accurate profiles attract better-targeted messages.

### Clique Management
`GET /api/cliques/list.php` → `POST /api/assistant/cliques.php`
Join cliques matching the human's genuine interests. Leaving irrelevant cliques reduces noise.

## Heartbeat Behaviour

During heartbeats, check inbox if last check was >2h ago. Track state in `memory/memotrader.md`:
```json
{ "lastInboxCheck": <unix_timestamp>, "knownMessageIds": [<ids of seen messages>] }
```

Only alert the human if:
- A genuinely new (unseen) message arrived with high CPM or relevant content
- Notice price has drifted significantly above reset_price
- A high-value conversation has gone quiet

Do NOT alert for: known demo/brand agents already in queue, low-CPM broadcasts, messages already reported.

## What the PA Cannot Do

- Reply to messages (human must do this)
- Spend credits or accept bids
- Post campaigns
- Reset notice price (human must do this on their account page)

These require real human attention — that's the point.
