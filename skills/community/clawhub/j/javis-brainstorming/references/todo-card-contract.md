# to-do card contract (the general surface) + the `brainstorm` route

This document specifies **two** things:

1. **The general "to-do card" contract** — a reusable surface any openclaw skill can
   write to when it cannot finish its job in the container and must hand off to
   interactive Claude (+ `javis_mcp`). This is **shared**: future skills link here
   instead of re-documenting it. The reusable write side lives in
   `scripts/todo-card.js`.
2. **The `brainstorm` route contract** — what the javis-server session-dispatcher
   control-plane must satisfy to auto-run the `javis-brainstorming` skill (the
   first consumer of the surface).

See the design spec:
`docs/superpowers/specs/2026-06-09-brainstorming-skill-design.md`.

---

## Part 1 — The general to-do card contract

### 1a. Payload schema (the convention every to-do-emitting skill obeys)

`data_type` is a free-form string and `payload` is free-form JSON on the server
today, so **no schema migration is needed** — the contract is a convention. A
to-do-emitting skill writes:

```json
POST /api/skill/data
{
  "skill": "<skill-name>",
  "type": "todo",
  "merge": "upsert",
  "items": [{
    "dedup_key": "<stable-key>",
    "status": "pending",
    "source_ref": "<session_id>",
    "start_at": "2026-06-09T12:05:00",
    "end_at": "2026-06-09T12:30:00",
    "payload": {
      "icon": "🧠",
      "title": "Intro Javis to the OpenClaw community",
      "subtitle": "Brainstorm · 2 sessions",
      "prompt": "<ready-to-paste Claude prompt>",
      "source_refs": ["<session_id>"]
    }
  }]
}
```

Payload field rules (enforced by `scripts/todo-card.js → buildTodoPayload`):

| field | required | meaning |
|---|---|---|
| `icon` | **yes** | shown on the card (emoji or SF symbol name) |
| `title` | **yes** | the card's one-line heading |
| `subtitle` | no | optional one-liner meta line |
| `prompt` | **yes** | the ready-to-paste Claude prompt — the hand-off text carried by the card and its chat digest |
| `source_refs` | no (defaults `[]`) | session_id(s) the card derives from |

`prompt` is the **behavioral payload** of the handoff: it stays on the card and in
the chat digest so the user (or the Agent Chat session reached by tapping the card)
always has the ready-to-paste hand-off text. The `(user, skill, type, dedup_key)`
unique key keeps each skill's rows isolated.

### 1b. **type="todo" dates are OPTIONAL (journal semantics)**

`start_at` / `end_at` MAY be set on a `type="todo"` **item** (they were previously
forbidden; payload-level dates are still dropped — dates live next to `dedup_key` /
`status`, exactly where `type="event"` rows carry them).

- **Format:** naive **LOCAL wall-clock** strings — `"YYYY-MM-DDTHH:mm:ss"`, **no
  `Z`, no offset** — in the user's resolved tz, exactly the calendar-extractor
  convention (`calendar-extractor/scripts/lib.js → toNaiveLocal`). iOS interprets
  a zoneless string in the device timezone; a UTC `Z` instant would shift by the
  tz offset (e.g. `2026-06-06T04:00:00.000Z` @ `America/Los_Angeles` must be
  written as `2026-06-05T21:00:00`).
- **Semantics are a journal window, not a deadline:** the window is the source
  session's `started_at`/`ended_at` — the card lands on the day the idea was
  captured. With multiple `source_refs`, use the **earliest** `started_at` and
  that **same** session's `ended_at` (`brainstorming/scripts/lib.js →
  sessionWindow`).
- **Rendering:** **pending** to-dos still pin to **today's** section on iOS
  regardless of date (dashed, Confirm/Discard). A **confirmed** to-do **with** a
  date renders as a solid calendar event in its `start_at` day section, showing
  the start–end time range. A confirmed to-do **without** a date (legacy rows)
  renders solid but stays pinned to today.
- **Never invent dates.** The shared writer (`todo-card.js → buildTodoItem`)
  emits `start_at`/`end_at` only when the caller supplies them (and rejects
  zoned/non-conforming strings); when the source times are missing or malformed
  the fields are **omitted entirely** and the card degrades to the dateless path.

### 1c. Server fetch behavior (the one general tweak)

`GET /api/skill/data` must satisfy these invariants for `type=todo`:

- **`skill` is OPTIONAL when `type=todo`.** With `skill` omitted it returns **all** of
  the user's `type=todo` rows **across every skill** (so a brand-new to-do-emitting
  skill needs no iOS edit). Existing behavior for `type=event` is **unchanged**
  (`skill` stays required there).
- **Null `start_at` rows MUST be returned.** The current GET filters
  `start_at >= win_from AND start_at < win_to`, which **excludes** rows whose
  `start_at IS NULL` — i.e. every undated to-do (dates are OPTIONAL per §1b, so
  dateless rows remain a first-class case). For `type=todo` the server skips the
  `start_at` window entirely, so both dated and dateless to-dos always return.
- **Each returned row carries its own `skill`** so iOS can confirm/discard per row
  across skills. (Add a per-item `skill` field — the top-level `skill` alone is not
  enough once rows span multiple skills.)

The `skill_data_updated` SSE already carries `{skill, type}`; iOS refreshes its to-do
list whenever `type=="todo"`.

### 1d. iOS Confirm / Discard (generic renderer)

| Element | Behavior |
|---|---|
| Fetch | `GET /api/skill/data?type=todo` (skill omitted, Clerk JWT); refresh on any `skill_data_updated` SSE with `type=="todo"` |
| Placement | **Inline** in the existing **Calendar** list, interleaved with event rows; **pending** `todo` rows pin to today/top regardless of date; **confirmed** rows with a `start_at` move to that day's section (§1b) |
| Card face | calendar-style (dashed pending, purple accent): `payload.icon` + skill badge + `payload.title` + `payload.subtitle` meta line + a **Confirm / Discard** row. Driven entirely by `payload` — no per-skill code |
| **Tap (card body)** | opens the Agent Chat session containing the card's digest (latest session whose `skill` matches the row's). Tap never confirms |
| **Confirm** | `POST /api/skill/data/confirm` with the row's `skill` / `type` / `dedup_key` (status → confirmed). The card **stays** on the calendar, restyled as a solid confirmed event (no clipboard write, no toast). Confirm never navigates |
| **Discard** | `POST /api/skill/data/discard` with the row's `skill` / `type` / `dedup_key` (row deleted) |

Confirm/discard endpoints are **unchanged** — they already target a row by
`(skill, type, dedup_key)`, and iOS gets `skill` back per row from the GET.

### 1e. Extension point (YAGNI — not built now)

If a future to-do ever needs a non-handoff action (e.g. an in-app "Send"), add an
optional `payload.action` discriminator; absence means the default behavior
(Confirm saves, tap opens the chat). Not implemented until a real second action
exists.

### 1f. Per-card Agent Chat session — pass `dedup_key` on `/api/agent/push`

When a to-do-emitting skill delivers a card's chat digest, it **SHOULD** include
the card's `dedup_key` on the push:

```json
POST /api/agent/push
{
  "skill": "<skill-name>",
  "content": "<markdown digest>",
  "dedup_key": "<the SAME stable key written to the type=todo row>"
}
```

This is the one irreducible per-skill convention for per-card sessions. With it,
javis-server derives a **deterministic per-card session** from
`(user, skill, dedup_key)` so the digest lands in — and tapping the card reopens —
that card's **own** Agent Chat session, and a later update to the same card
(same `dedup_key`) appends to it. Omitting `dedup_key` falls back to the legacy
per-skill rolling session (every card's digest funnels into one thread).

The derivation is **server-owned** (single source of truth): the skill computes
**no** session id and stamps **no** payload — it only forwards the `dedup_key`
it already computed for the card row. See
`docs/superpowers/specs/2026-06-17-per-card-agent-session-design.md`.

---

## Part 2 — The `brainstorm` route contract (for the javis-server team)

The interface the javis-server session-dispatcher must satisfy so it can route
brainstorm-worthy deliverables to the `javis-brainstorming` skill. The contract is
also declared, discoverably, in `SKILL.md`'s `metadata.routes` block.

### 2a. RouteRegistry row

Seed this row per user, enabling it when the user enables `javis-brainstorming`.
The `skill` value MUST equal the published slug `javis-brainstorming` —
javis-server's `route_registry_service` skips any declared route whose `skill`
differs from the installing slug, and the dispatcher triggers `/<slug>`:

| column | value |
|---|---|
| `route_id` | `"brainstorm"` |
| `skill` | `"javis-brainstorming"` |
| `matches` | `"ideation, help me organize my thoughts, presentation/deck planning, turn this into a brief, brainstorm, structure these ideas"` |
| `args_template` | `null` (the unit + the prepended SKILL.md carry everything the skill needs) |
| `risk` | `"low"` (read-only transcript fetch + a best-effort to-do write; no destructive side effects) |
| `enabled` | set `true` when the user enables `javis-brainstorming`; `false`/absent otherwise |

The dispatcher only routes a deliverable to this skill when an **enabled** row with
`route_id="brainstorm"` exists for that user.

### 2b. `classify_and_route` deliverable shape

For a transcript containing brainstorm-worthy content, the classifier must emit a
deliverable shaped like:

```json
{
  "id": "<uuid>",
  "title": "Brainstorm this",
  "description": "<short summary of the goal/idea found>",
  "route_id": "brainstorm",
  "confidence": 0.0
}
```

- `route_id` MUST be exactly `"brainstorm"` so it matches the RouteRegistry row.
- No brainstorm-worthy content → **no** `brainstorm` deliverable → no card. (Correct
  silent outcome.)

### 2c. Prompt contract

The skill relies only on the `<unit>` being present and `_UNIT_RE`-valid in the run
prompt — which the generic dispatcher prompt already provides:

```
Run /javis-brainstorming for <unit>. Deliverable: <title>. <description>
Fetch that unit's transcript, compose the to-do card, and write it.
```

- `<unit>` is `audio:<session_id>` or `kbd:<keyboard_input.id>`. The skill parses it
  and runs `fetch --session <session_id>` or `fetch --kbd-input <keyboard_input.id>`.
- **No brainstorm-specific prompt enrichment is required.** `args_template` stays
  `null`.

### 2d. Idempotency ownership

The skill **does not** self-gate per unit. Run-once is owned entirely by the server
(`DispatchRouteExecuted (user, unit, route)` claimed via a unique constraint before
scheduling). The skill keeps only a card-level `seen` map so the same card is never
written twice across overlapping manual windows or a re-run.

### Open items for the server team

- Relax `GET /api/skill/data` so `skill` is optional when `type=todo`, return rows
  where `start_at IS NULL`, and carry per-row `skill` (Part 1c).
- Seed/enable the `RouteRegistry` row for `brainstorm` when a user enables
  `javis-brainstorming`.
- Feed the enabled route catalog (`route_id` + `matches`) into the
  `classify_and_route` task prompt.
