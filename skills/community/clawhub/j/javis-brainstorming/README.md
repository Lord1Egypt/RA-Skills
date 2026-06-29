# Brainstorming

> ⚠️ **Requires the HiJavis iPhone app.** This skill runs inside HiJavis — install the app first, then it's ready to use.
> 📲 https://apps.apple.com/us/app/hijavis/id6745134765

Brainstorming catches the half-formed ideas hiding in your conversations and gets them ready for a real working session with Claude. HiJavis listens, spots when you're trying to think something through, and drops a ready-to-go card right in your Calendar tab — on the day the idea was captured. Tap the card to jump into its chat and keep shaping the idea; tap Confirm to keep it on your calendar.

## Picture this

- You're walking and talking out loud: "I should really introduce Javis to the open-source crowd... maybe a demo, maybe an explainer." Later, a card is waiting: tap it to open the chat behind it and start shaping the idea into a real plan, or tap Confirm to keep it on your calendar.
- You finish a brain-dump voice note about a presentation you want to give. Instead of a wall of text, you get a tidy hand-off that already knows your goal and what you asked for.
- An idea strikes mid-errand. By the time you're home, it's queued up as a brainstorm card — nothing lost.

If any of those sound like you, this one's for you.

## What it does

HiJavis listens to your conversations and voice notes. Brainstorming reads back through your recent recordings, notices when you're working through an idea — a goal plus a few things you want help producing — and turns it into a single **to-do card** in your Calendar tab. At the same moment, a tidy summary of the card lands right in your chat — title, goal, what you asked for — so you see what was captured without leaving the conversation.

The card carries a ready-to-paste prompt. It does **not** brainstorm for you in the app — instead, it hands you off to Claude's full brainstorming flow with all your context already filled in.

## How to use it

### Just ask

Open your HiJavis chat and ask. Any of these works:

- "brainstorm this"
- "整理成簡報"
- "帮我腦力激盪"
- Or a natural ask like "help me organize my thoughts on this" or "turn this into a deck."

HiJavis scans your recent recordings and, if it finds something worth brainstorming, places a card in your Calendar tab and posts a summary of it in your chat.

### Then tap or confirm

The card shows up dashed (pending) at the top of today's calendar items. **Tap the card** to open the chat session that holds its summary and tailored prompt — that's where the guided brainstorming continues: Claude asks you one question at a time, pulls your original voice note, and builds a structured brief before drafting. Tap **Confirm** and the card stays on your calendar as a solid entry at the time the idea was captured. Not interested? Tap **Discard** and it's gone.

## What makes it handy

- **It does the setup for you.** The prompt already states your goal, lists what you asked for, and tells Claude to pull your original transcript. You just paste and go.
- **It hands off to the real thing.** No cramped in-app Q&A — the actual brainstorming happens in Claude's full flow.
- **It never repeats itself.** It remembers the cards it already made, so the same idea won't clutter your list twice.
- **It works in English and Chinese.**

## Good to know

- Brainstorming **does no brainstorming itself** — it detects a brainstorm-worthy moment, composes a hand-off prompt, and writes a card. The thinking happens on Claude, in the chat you reach by tapping the card.
- Cards arrive **pending**, pinned to today. Confirm keeps the card on your calendar (as a solid entry on the day the idea was captured); Discard removes it. That's the only gate — there's no extra approval step.
- The chat summary is delivered live: if the app is in the background or closed at that moment, you may miss the chat message — but the pending card in the Calendar tab is always there waiting.
- For cards to arrive promptly, keep the HiJavis app open and running. Asking on the spot works anytime.

## For developers

This skill is the first consumer of the **general "to-do card" surface**: any openclaw skill that needs to hand a job off to interactive Claude can write a `type="todo"` row with the same small payload `{ icon, title, subtitle?, prompt, source_refs }`, plus an optional item-level `start_at`/`end_at` journal window (naive local wall-clock, calendar-extractor convention). The reusable write side lives in `scripts/todo-card.js`; the full contract (payload schema, optional dates, server fetch behavior, iOS tap/Confirm/Discard) is in `references/todo-card-contract.md`.

- `scripts/brainstorming.js` — `fetch` / `push` CLI (transcript fetch, card compose-and-write, dedup, Agent Chat digest push via `POST /api/agent/push`).
- `scripts/todo-card.js` — shared, dependency-free helper to validate + build + POST a `type="todo"` card.
- `scripts/lib.js` — pure helpers (tz resolution, the relative-date anchor, the `sessionWindow` journal window, dedup key, prompt-template assembly, the `formatDigest` Agent Chat markdown, TTL pruning).
- `scripts/data.js` — per-user local `seen` state with a path-traversal guard.

Node 18+ built-ins only (`fetch`, `fs`, `path`) — no dependencies, no `npm install`. Run the tests with `node --test`.
