# gmail-wiki-ingest — server endpoint contract

The wire shapes of the three candidate calls this skill makes — `fetch`,
`content` and `submit` — and the rules the server applies to what it is handed.
(The fourth call, `report`'s `POST /api/agent/push`, is an existing generic
endpoint that needed no change for this skill; its contract is the daily-report
design spec's, not this file's.) It is the contract only — the implementation is
javis-server's — the generic candidate core plus the gmail adapter, reached over
gateway-token HTTP from `scripts/gmail-wiki-ingest.js` and routed through
`app/routers/skill_candidates.py`. An earlier revision made these openclaw
client tools; that transport is unreachable from a cron turn (see
`trigger-contract.md`). The payloads did not change with the transport — only
the caller and the `skill` field, which the script pins and the server validates
against its registered adapters.

Design specs:
`javis.is/docs/superpowers/specs/2026-08-28-gmail-wiki-ingest-skill-migration-design.md`
(§PR 2) for `fetch`/`submit`, and
`javis.is/docs/superpowers/specs/2026-09-06-gmail-ingest-foundation-and-skill-split-design.md`
(§4.2, §6) for `content` and the knowledge model. Verification plan:
`…-e2e-test-plan.md` — note that its TC6 asserts the *old* content boundary (a
body nonce absent everywhere in the container) and is inverted by `content`; the
property that replaced it is TC6's staged-batch form, asserted in-process by
javis-server's `tests/api/test_skill_candidates_content.py`.

## Transport

Ordinary HTTP to javis-server, authenticated by the container's
`OPENCLAW_GATEWAY_TOKEN` bearer — the same shape `POST /skill/data` and
`/transcripts/recent` already use for calendar-extractor. The script makes the
call; javis-server runs the work in its own process against its own database
session.

**What the token does and does not carry.** It identifies the **user**, not the
skill: one token per container, shared by every skill installed in it. So the
`skill` field travels in the request body, and two things follow that the skill
depends on:

1. **The user cannot be redirected.** `user_id` comes from the token and is
   never read from the body. A run can only ever touch its own user's mail,
   ledger and wiki.
2. **The skill CAN be named, and is validated rather than trusted.** The server
   404s any slug no registered adapter claims. This is weaker than the client-
   tool transport it replaced, where the skill was injected server-side and was
   unnameable — a property a shared per-container token cannot reproduce. The
   residual exposure is one user's own skills, never another user's data.
   Restoring the stronger guarantee needs a per-skill credential, which does not
   exist today.

`gmail_search` and `gmail_get_message` remain removed from this skill's
server-initiated turns, at advertisement and at execution. A cron turn has no
client tools at all, so on the daily run the question does not arise.

That deny-gate is **more** load-bearing since `content` landed, not less. The two
tools are unbounded reads over the whole mailbox; `content` can only answer for
threads this run's own `fetch` staged. Leaving them advertised alongside
`content` would make the staged-batch bound decorative.

## `fetch` → `POST /api/skill/candidates/fetch`

**Arguments** — `{"limit": <int>}`, optional, default 25. **No paging, by
design**: the source side is already bounded (Gmail is walked at most
`_MAX_THREAD_PAGES` pages behind the watermark), and a 25-item batch has been
sufficient in practice. A run is one fetch.

**Result**

| field | shape | notes |
|---|---|---|
| `status` | string | `ok` on a normal pass. Anything else: stop. |
| `items` | array | the candidates to judge; possibly empty |
| `context` | object | `{"knowledge_model": {version, built_at, truncated, fields, nodes}}` — see below. Servers predating the knowledge model send `{"wiki_index": [{page_type, slug, title}, …]}` instead; the skill reads whichever is present. |
| `recent_decisions` | array | ≤ 20 of `{title, actor, category, decision}` |
| `filtered` | object | counters for what never reached `items` |
| `error` | string | present only on the failure rows in the error table |

**`context.knowledge_model`**

| field | shape | notes |
|---|---|---|
| `version` | string | content hash of `nodes`, `km1:`-prefixed. Stable across builds over an unchanged wiki, so a caller may cache on it. |
| `built_at` | string | ISO-8601 Z. Provenance only — deliberately not part of `version`. |
| `truncated` | bool | true when the node cap bit and older pages are not citable this run |
| `fields` | array | the position names for every row in `nodes`, currently `["page_type", "slug", "title", "degree"]` |
| `nodes` | array | one **positional array** per citable page, in `fields` order |

**`nodes` rows are arrays, not objects.** `["concept", "Agent-Builder", "", 41]`
is one node. The `fields` header states the order once rather than repeating
four key names per page: measured as a list of objects the index was ~190KB /
~48k tokens and was effectively the whole envelope. Read positions off `fields`;
do not hard-code the order.

`title` is `""` whenever it merely de-slugifies its own slug — `Agent-Builder`
titled "Agent Builder" ships blank, which is 37% of a real wiki. The blank is a
payload saving at the serialization boundary, not a page without a title, and
nothing should ever cite a title in the first place.

`degree` is inbound link count from `wiki_links`, counted across the whole wiki
rather than within the requested page types, so it means the same thing to
every caller.

**`items[]`**

| field | notes |
|---|---|
| `thread_id` | the `item_key` to echo back, verbatim |
| `subject` | header |
| `from` | header, display-name form |
| `date` | header |
| `rfc822_msgid` | header, carried through to the review card |
| `message_count` | messages in the thread |
| `trusted` | server-computed from the ledger; context, never a score multiplier |

**No `body`, and no `snippet` — in `fetch`.** The batch is metadata, and it stays
metadata: shipping a snippet with every item would put a body excerpt for every
thread in the container whether or not the agent had any use for it. Bodies come
from `content`, one explicit call, for a shortlist the agent named, bounded to
what this `fetch` already offered. That is the difference between the two calls
and the reason they are two calls.

**`filtered`** counts what the server dropped before judging: machine mail
(`List-Unsubscribe`, a bulk `Precedence`, or a machine local-part), threads
already distilled, and threads already decided. The counters exist so a
discard's *cause* is knowable after the fact — a thread that vanished at the
machine-mail filter and one that lost the LOW band must stay distinguishable.

**`recent_decisions`** is filtered server-side to `source='user'` rows, and that
filter lives **inside** the query, before the LIMIT. Filtering after the LIMIT
would let a run of machine-written rows starve the window, and the model would
end up learning from its own verdicts.

## `content` → `POST /api/skill/candidates/content`

**Arguments** — `{"item_keys": ["<thread_id>", …]}`, at most `CONTENT_BATCH_MAX`
(12 by default, server-side; the script trims to the same number before posting).

**No `skill` field, and that is the endpoint.** `fetch` and `submit` name the
skill in the body because a gateway token identifies the user and not the skill.
`content` names nothing: the server resolves the batch from the run that invoked
it, so the call has no argument that could point it anywhere else.

**Result**

```jsonc
{ "status": "ok",
  "items": [ { "item_key": "<thread_id>", "text": "<the thread, as text>" } ],
  "unavailable": [ { "item_key": "…", "reason": "not_in_batch" | "fetch_failed" } ] }
```

**The security property, and it is the whole point of the endpoint.** An
`item_key` is honoured **only if it is in the batch this run's `fetch` staged**.
A key outside that set answers `not_in_batch` and reads nothing — not the
thread, not its headers, nothing. So the skill cannot use this endpoint to read
arbitrary mail; it can only deepen its view of threads the server had already
chosen to offer it. It is bound to the *offered* set specifically, which on a
truncated walk is narrower than the set of threads the server itself walked.

**Bodies are returned and never persisted.** `gmail_ingested_threads` and
`wiki_pages` remain the only places thread content is durably written, and both
still sit behind a confirm. The script writes counters to `data/last-run.json`
and never a line of text.

**Failure is per-item.** One thread the server cannot read answers
`fetch_failed`; the rest of the request still returns.

**Any `fetch_failed` holds the watermark**, and the rule belongs to whoever
*reports* the failure rather than to whoever was supposed to perform the read —
because several of the routes to `fetch_failed` never reach a reader at all: the
user turned ingest off between `fetch` and `content`, the skill's adapter has no
content implementation, the whole call raised. A hold that lived with the reader
covered only the route it knew about, and the others promoted the cursor over
threads whose bodies were asked for and never arrived: judged on a subject line,
then retired forever, with no counter recording that the closer look never
happened. Re-scanning is always safe; skipping never is.

`not_in_batch` deliberately does **not** hold. That key was never offered, so no
thread is at risk of being stepped over, and holding on it would let a caller
stall its own cursor indefinitely by naming ids that do not exist.

Account-level failures (`auth_missing`, `needs_reconnect`) are not per-item: they
come back as an error envelope, exactly as they do from `fetch`, with the same
effect on the scope row — and they hold the watermark too, since not one body
arrived.

**No staged batch** — the `fetch` never landed, or too long has passed —
answers `{"status": "error", "error": "no_staged_batch"}`. Nothing is read, the
run judges on metadata, and no state is written.

## `submit` → `POST /api/skill/candidates/submit`

**Arguments**

```jsonc
{ "verdicts": [
  { "item_key": "<thread_id from this batch>",
    "category": "correspondence" | "transactional" | "marketing" | "announcement",
    "score": 0.0,
    "refs": [ { "page_type": "concept", "slug": "Agent-Builder" } ],
    "reason": "one sentence",
    "occurred_at": "2026-09-04T17:22:00Z" }
] }
```

`refs` is the generic name for what gmail's ledger column still calls
`related_to`; the column keeps its name because renaming it would buy nothing.
For a skill with nothing to cite, `refs` is `[]` and validation is a
pass-through.

**`occurred_at` is optional, and it is the instant the item is *about* rather
than the instant it was judged.** The server writes it to the candidate row's
time anchor, so the card files itself under that day on the user's timeline
instead of under today. It must be ISO-8601 **with a zone** — the trailing `Z`
in the example, or any explicit offset. A zoneless string is not read in the
container's local time, it is refused: the container's clock is not the user's
and never was, and guessing which was meant is how a date lands hours away from
the thing it records.

The server polices the value it accepts, and both of its rules land in the same
place. A date in the future is **replaced** with the thread's own date, because
an email records correspondence that happened and the days ahead belong to the
calendar; a date that is absent, zoneless or unparseable falls back to exactly
that same thread date. So the field can only ever move a card backwards onto a
truer day, never forwards, and getting it wrong costs the card's placement and
never the verdict — the judgment about the *mail* stands either way.

Those two rules are the *only* ones, and the gap they leave is midnight. A
date-only source written out as `2026-08-01T00:00:00Z` satisfies both — it
parses, it carries a zone, it is in the past — so it is accepted verbatim,
stored verbatim, and only turns into a day when the reader's device resolves it
against the reader's own clock, where it is the evening of July 31 for everyone
west of UTC. No counter moves and no value is dropped; the card simply sits one
day early, and only for some readers. Nothing on the wire can distinguish that
from a genuine instant that happens to fall on midnight UTC, which is why the
fix lives in the judgment and not in validation: send a bare calendar date as
midday. Which date to send, and in what form, is `rubric.md` §5's, not this
file's.

**Validation, all server-side**

| rule | on violation |
|---|---|
| `score` clamped to 0–1 | clamped, not rejected |
| `item_key` must be from this batch | verdict → `rejected` |
| `category` must match the enum | verdict → `rejected` |
| each ref must exist in the live index | that ref stripped, counted in `unvalidated` |
| slugs normalized (`concept/Foo` → `Foo`) before the check | silently fixed |
| `occurred_at` must parse as ISO-8601 **with a zone** | dropped, and the thread's own date is used |
| `occurred_at` must not be in the future | replaced with the thread's own date |

The normalize-then-drop shape is not fussiness: a judge asked to cite slugs
guesses at the `page_type/` prefix — 21% invalid refs in one probe run, 3% in the
next. Normalizing catches the prefix case; dropping the rest keeps dangling
references out of the review queue and out of the ledger that trains the next
run.

**Result** — `{high, middle, low, unvalidated, dropped, gated, uncovered, acted: [...],
rejected: [...], promoted}`.

**`gated` and `dropped` are different numbers, and only one of them partitions
the batch.** `gated` is the adapter's category gate alone — the items refused
before any band ran, on a rule about what kind of thing they are — so
`high + middle + low + gated` accounts for every judged item. `dropped` is the
server's older "judged, and kept nothing" counter: it covers the gate **and**
the LOW band, so it overlaps `low` entirely and a batch of correctly labelled,
low-scoring mail comes back with `low == dropped` and `gated == 0`. The digest
renders `gated`; `dropped` stays on the wire because it is what the submit log
line carries.

## The cursor / watermark contract

`fetch` writes `GmailIngestScope.pending_cursor_epoch` — the max internalDate
over every thread the walk **scanned**, not just the ones it offered. It is
promoted to `cursor_epoch` in exactly two places:

1. **On `submit`**, when the pass raised nothing *and* accounted for every item
   the fetch offered.
2. **Inside `fetch` itself**, when the pass offered nothing at all and nothing
   raised — the empty-batch rule means no `submit` is coming, and without this
   a mailbox of pure newsletters would re-walk a widening window every day
   forever.

"Accounted for" means the item came out of `submit` with an outcome: HIGH,
MIDDLE, LOW, or the category gate's hard drop. It does **not** include an item
that was omitted from `verdicts` or one whose verdict was rejected — both leave
the thread with no review row and no ledger row, so a promoted watermark would
step past a thread nothing anywhere records having seen. `uncovered` in the
result is the count, and a non-zero `uncovered` always means `promoted: false`.

- Agent dies mid-turn → nothing promoted, next `fetch` overwrites the pending
  value and re-offers the same threads.
- Agent never calls `submit` → same.
- Agent submits half the batch → same, for the whole batch.
- A malformed `arguments` blob decodes to `{}` and arrives as `verdicts: []`.
  Without the coverage rule that reads as a clean pass and promotes the entire
  batch away; with it, nothing moves.
- A promoted cursor that skipped a thread is **unrecoverable and silent**, which
  is why the rule is one-directional: **re-scanning is always safe; skipping
  never is.** The E2E plan calls this its highest-severity case (TC9).

The cost of holding is bounded and visible: an agent that mangles the same
verdict every run pins the cursor and the listing window widens, which shows up
as `uncovered=` on every `skill candidates: submit` log line. The cost of
promoting wrongly is a thread nobody will ever see again.

Idempotency sits underneath all of it: `gmail_ingested_threads.message_ids` is
compared as a set — equal set skips, superset re-distils — so a double-fired
run or a re-submitted thread is a no-op, not a duplicate page.

## Errors

| Condition | Server behavior | Skill behavior |
|---|---|---|
| `GoogleAuthMissing` | `fetch` → `{error: "auth_missing"}`; the scope is disabled and its status set | report, stop |
| `GmailScopeMissing` | `{error: "needs_reconnect"}`; the scope stays **enabled** so the GET endpoint can prompt re-consent | report, stop |
| Scope off (discovery switched off, or Google disconnected) | `fetch` → `{error: "disabled"}`, nothing staged or written; also returned by a `fetch` or `submit` that was in flight when the switch-off landed, with that call's writes rolled back | stop silently — no `report` |
| One thread's metadata fails | skipped and counted; the batch continues | judge the rest |
| One thread's body read fails inside `content` | that key answers `unavailable: fetch_failed`; counted as `raised`, so the cursor holds | judge that item on metadata |
| `content` key outside the staged batch | answers `unavailable: not_in_batch`; nothing is read | judge on metadata, or drop an item that was never offered |
| `content` with no staged batch | `{"error": "no_staged_batch"}`; nothing read, nothing written | judge the whole batch on metadata and say so in the digest |
| Google access lost during `content` | same as `fetch`: scope disabled on `auth_missing`, held on `needs_reconnect` | judge on metadata, submit, report, tell the user to reconnect |
| Malformed verdict | dropped into `rejected`, counted in `uncovered`, and the watermark is held for the whole batch; the rest of the batch still lands | do not re-submit — the next run re-offers it |
| Distillation fails inside `submit` | the row stays confirmed-but-undistilled; `_confirmed_but_never_distilled` retries next cycle | nothing to do |
| Cron missed while the container was stopped | `runMissedJobs` fires it once on the next start | nothing to do |

## What is NOT in this contract

- No endpoint to POST to, no bearer token, no `javis-server:8000` URL.
- No band, no threshold, no trust count in either direction. The agent proposes;
  the server disposes.
- No rubric. What to score, what to cite and which threads earn a body read are
  `rubric.md`'s, and are meant to change without touching any of this.
- No user-facing enable switch. That is `gmail_ingest_scopes.enabled`, written
  by iOS. Tying it to a file inside an ephemeral container would be a worse
  contract than the row that already exists.
