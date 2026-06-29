---
name: javis-brainstorming
description: Turn a brainstorm-worthy voice/keyboard unit into a generic "to-do card" whose ready-to-paste prompt hands off to Claude's content-brainstorming skill (with javis_mcp pulling the source transcript). This skill does NO brainstorming itself — it composes a hand-off prompt and writes a type="todo" card stamped with the source session's start/end times (journal semantics). Use on demand when the user asks to "brainstorm this" / "整理成簡報" / "帮我腦力激盪", and fetch the last 24 hours of transcript data by default. The javis-server session dispatcher also AUTO-RUNS this skill (no approve-to-run card) when a completed unit matches the brainstorm route, passing a deliverable hint in the run prompt that the agent may use alongside the transcript; the card is written PENDING and a markdown digest of it is delivered to the Agent Chat via POST /api/agent/push (the chat shows [push:javis-brainstorming] + the card summary); the human gate is Confirm/Discard in the iOS Calendar tab (Confirm saves the card on the calendar as a solid event; tapping the card body opens its Agent Chat session). Triggers: 'brainstorm this', '整理成簡報', '帮我腦力激盪'.
keywords: brainstorm this, brainstorm, 整理成簡報, 帮我腦力激盪, content-brainstorming, todo card, brainstorming
metadata:
  openclaw:
    runtime:
      node: ">=18"
  routes:
    - route_id: brainstorm
      skill: javis-brainstorming
      matches: "ideation, help me organize my thoughts, presentation/deck planning, turn this into a brief, brainstorm, structure these ideas"
      args_template: null
      risk: low
---

# Brainstorming

> Turn a brainstorm-worthy voice/keyboard unit into a generic **to-do card** whose
> `prompt` hands off to Claude's `content-brainstorming` skill. The skill does **no**
> brainstorming itself — it detects a discernible goal/request in a transcript,
> **composes** a ready-to-paste Claude prompt, and writes a `type="todo"` card
> stamped with the source session's start/end times (journal semantics). iOS
> renders that card generically (calendar-style, **Confirm / Discard**) in the
> Calendar tab; **Confirm** saves it on the calendar as a solid event at its
> session time, and tapping the card body opens the Agent Chat session that holds
> its digest. Fetch the last 24 hours of transcript data by default.

## When to use

- "brainstorm this"
- "整理成簡報" (organize this into a presentation)
- "帮我腦力激盪" (help me brainstorm)
- A natural ask like "help me organize my thoughts on X" or "turn this into a deck".
- Automatically, when the javis-server session dispatcher **auto-runs** this skill after a completed unit matches the `brainstorm` route — no approve-to-run card (see "How this skill is invoked").

## Core commands

> **`<userId>` is optional.** Omit it and it defaults to `self`. Each HiJavis user
> runs in their own openclaw container, so `self` is correctly isolated; the gateway
> token (not the userId) authenticates every server call.

```bash
# Step 1 — fetch recent transcripts as JSON (the agent reads this and composes a card)
node scripts/brainstorming.js fetch [--hours N] [--limit N]

# Step 1 (dispatcher run) — fetch ONE completed unit (the auto-run dispatcher unit)
node scripts/brainstorming.js fetch --session <sessionId> [--hours N]   # audio unit
node scripts/brainstorming.js fetch --kbd-input <inputId> [--hours N]   # keyboard unit

# Step 2 — push: pipe the composed to-do-card JSON to stdin; dedups (seen) + writes type=todo pending + delivers the chat digest.
# Include the fetch payload's `sessions` and `tz` alongside the card so push can
# stamp the card's start_at/end_at from the source session's times.
echo '{"card": <todo-card-json>, "sessions": <fetch.sessions>, "tz": "<fetch.tz>"}' | node scripts/brainstorming.js push
```

## Workflow

A two-step pipeline mirroring `calendar-extractor`: the **script** does the I/O
(fetch transcripts, dedup, write the card), the **agent/LLM** does the reasoning
(decide there is a brainstorm-worthy unit, extract its goal/request, and compose the
hand-off prompt). Nothing is hardcoded — the agent reads the fetched transcript and
emits one to-do-card JSON object.

1. **Fetch** — `node scripts/brainstorming.js <userId> fetch` issues
   `GET http://javis-server:8000/api/transcripts/recent?since=…&limit=…` with the
   `OPENCLAW_GATEWAY_TOKEN` bearer and prints
   `{ "reference_time": LOCAL-wall-clock (zoneless, in tz), "reference_date": "YYYY-MM-DD", "reference_weekday": "Thursday", "reference_time_utc": ISO8601, "tz": IANA, "sessions": [ { session_id, started_at, ended_at, transcript, source } ] }`.
   If fetch fails, returns invalid JSON, or yields zero sessions, output nothing and
   do not push; report the failure only if the user asked for a diagnostic.

2. **Compose** — the agent reads that JSON and decides whether there is a discernible
   **goal** and **request**. If there is none, **emit no card** (silence is a valid
   detector outcome). If there is, produce **one** to-do-card JSON object:

   ```json
   {
     "title": "Intro Javis to the OpenClaw community",
     "goal": "introduce Javis to the OpenClaw community, for non-engineer users",
     "subtitle": "Brainstorm · 2 sessions",
     "request": [
       "an attention hook",
       "a step-by-step demo/onboarding flow",
       "an explanation for the open-source community",
       "concise skill examples & use cases"
     ],
     "key_points": ["…optional notes the agent pulled from the transcript…"],
     "source_refs": ["<session_id>", "<session_id>"]
   }
   ```

   `title`, `goal`, `request[]`, and `source_refs[]` are the bracketed fields. The
   `push` script **composes** the ready-to-paste `prompt` from them using the fixed
   template below (the agent may instead supply an explicit `prompt` field to override
   it; if absent, the template is used). `icon` defaults to `🧠`; `subtitle` defaults
   to `Brainstorm` / `Brainstorm · N sessions`.

3. **Push** — pipe `{"card": <card>, "sessions": <fetch.sessions>, "tz": "<fetch.tz>"}`
   into `node scripts/brainstorming.js <userId> push` (a bare card object still
   works — the card then just carries no dates). The script:
   - dedups against per-user local state (`data/users/<userId>.json` → `seen` map, 30-day TTL),
   - stamps the item's **optional** `start_at`/`end_at` journal window from the
     source session's `started_at`/`ended_at` (earliest session by `started_at`
     among the card's `source_refs`, that **same** session's `ended_at`),
     serialized as **naive LOCAL wall-clock** in the resolved tz — the
     calendar-extractor convention. Missing/malformed session times ⇒ the fields
     are omitted entirely (never invented),
   - validates + writes the **new** card to `POST /api/skill/data` with
     `type="todo"`, `merge="upsert"`, `status="pending"`, and
     `payload = { icon, title, subtitle?, prompt, source_refs[] }` (icon/title/prompt
     **required**) — see `references/todo-card-contract.md` for the general contract,
   - delivers a markdown digest of the card via `POST /api/agent/push`
     (calendar-extractor style), so the Agent Chat shows `[push:javis-brainstorming]`
     + the card summary (title, 🎯 goal, 📋 request items, 📡 session count,
     Confirm/Discard footer). The digest is non-fatal — the summary line reports
     `Chat digest: delivered.` or `Chat digest FAILED: <reason>`.

## The ready-to-paste prompt (the per-skill `payload.prompt`)

`push` composes this from the card's bracketed fields; the rest is literal. It
stays on the card payload and in the chat digest — the handoff path is the Agent
Chat session opened by tapping the card:

```
I want to <GOAL — e.g. introduce Javis to the OpenClaw community, for non-engineer users>.

Source: my Javis voice note(s), session_id(s): <id…>. Before we start, pull the full
transcript via the javis_mcp connector (get_transcript_tool / search_transcripts_tool).

Please produce:
- <REQUEST item 1 — e.g. an attention hook>
- <REQUEST item 2 — e.g. a step-by-step demo/onboarding flow>
- <REQUEST item 3 — e.g. an explanation for the open-source community>
- <REQUEST item 4 — e.g. concise skill examples & use cases>

Run the content-brainstorming flow: ask me clarifying questions one at a time,
inventory the source material, then produce a structured brief before drafting.
```

This closes the loop: the openclaw `javis-brainstorming` skill hands off to the Claude-side
`content-brainstorming` skill, with `javis_mcp` pulling the source transcript.

## How this skill is invoked

This skill has **two triggers** (dispatcher auto-run and manual).

1. **Dispatcher auto-run (automatic).** When a unit of input completes (an audio
   session ends or a keyboard input is saved), the javis-server **session dispatcher**
   classifies the transcript. If it finds brainstorm-worthy content (ideation,
   "help me organize", presentation/deck planning) and an enabled `brainstorm`
   route matches, the server claims run-once (`DispatchRouteExecuted (user, unit,
   route)`) and **AUTO-RUNS this skill directly — there is no approve-to-run proposal
   card**. It runs in the user's container with a prompt of the form
   `Run /javis-brainstorming for <unit>. Deliverable: …`, where the deliverable text is the
   dispatcher's classification carried as an **advisory HINT**. The agent parses
   `<unit>` (`audio:<session_id>` or `kbd:<keyboard_input.id>`), runs
   `fetch --session <id>` / `fetch --kbd-input <id>`, composes the card, and pushes it.
   **The human gate is not running the skill — it is Confirm/Discard on the produced
   to-do card.** **The skill does not self-gate** — the server owns run-once.
2. **Manual ("brainstorm this").** On demand, the agent runs the windowed `fetch`
   (last 24h by default) → composes → pushes. Repeating the ask re-runs composition on
   the window; the `seen` map still prevents writing the same card twice.

The route contract the javis-server team must satisfy is declared in this file's
`metadata.routes` block and documented in `references/todo-card-contract.md` (which
also carries the **general** to-do card contract shared by all to-do-emitting skills).

## Notes

- **Runtime dependencies** — the scripts use Node 18+ built-ins only (`fetch`, `fs`, `path`); no `npm install` is needed for the script runtime.
- **Does no brainstorming.** This skill detects + composes + writes a card. The actual
  brainstorming happens on Claude — tap the card to open its Agent Chat session
  (which carries the digest and `payload.prompt`) and continue into the interactive
  `content-brainstorming` flow.
- **The card is written PENDING, with a journal window.** The row mirrored to
  `/api/skill/data` carries `status: "pending"` plus optional `start_at`/`end_at`
  stamped from the source session's times; iOS renders pending cards dashed (purple
  accent), pinned to **today** regardless of date, with **Confirm · Discard**.
  **Confirm** marks the row confirmed and the card stays on the calendar as a solid
  event at its `start_at` day (undated legacy cards stay pinned to today);
  **Discard** deletes it. Tapping the card body opens its Agent Chat session — tap
  never confirms, Confirm never navigates. There is no approve-to-run proposal card.
- **Chat digest, not a thin nudge.** A novel card also delivers a markdown digest of
  itself via `POST /api/agent/push` (calendar-extractor style): the Agent Chat shows a
  `[push:javis-brainstorming]` bubble followed by the card summary. Delivery is
  non-fatal — the push summary line reports `Chat digest: delivered.` or
  `Chat digest FAILED: <reason>` so failures are diagnosable from the run log.
- **Backgrounded/killed iOS app**: `AGENT_PUSH` is WebSocket-only (no APNs), so a
  backgrounded or killed app misses the chat message — the pending card in the
  Calendar tab is the durable artifact.
- **Dedup is local-state-authoritative.** The container's gateway token can WRITE to
  `/api/skill/data` but cannot read it back (`GET /api/skill/data` requires a Clerk
  JWT), so novelty is decided by the local `seen` map (`{ "<dedup_key>": "<ts>" }` in
  `data/users/<userId>.json`, 30-day TTL-pruned); the server write is a best-effort
  mirror. The to-do `dedup_key` is `title|hash(goal)` — re-brainstorming the same unit
  toward a new goal is a genuinely new card.
- **Timezone**: there is **no prefs file**. tz resolves in order: the `tz` field on the
  push/fetch payload → the `TZ` environment variable → the system zone. The resolved
  tz is used twice: for the relative-date anchor (so the agent resolves "today"
  coherently) and to serialize the card's optional `start_at`/`end_at` as **naive
  LOCAL wall-clock** (`"YYYY-MM-DDTHH:mm:ss"`, no `Z`/offset — the
  calendar-extractor convention; iOS reads zoneless strings in the device tz).
- **The shared write side.** `scripts/todo-card.js` is the reusable Layer-1 helper:
  any future skill can `require` it to build + POST a `type="todo"` card without
  re-implementing the contract. `brainstorming.js` is its first consumer.
- **User IDs** only allow letters, digits, `-`, `_` (path-traversal guard in `data.js`).
