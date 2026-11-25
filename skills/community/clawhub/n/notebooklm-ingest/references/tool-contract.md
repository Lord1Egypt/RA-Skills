# notebooklm-ingest — server endpoint contract

The wire shapes of the two calls this skill makes, and the rules javis-server
applies to what it is handed. It is the contract only — the implementation is
javis-server's.

Design spec:
`javis.is/docs/superpowers/specs/2026-10-29-notebooklm-connector-design.md`
(§Ownership, R2–R5, R17, R18, R19). Research:
`…-notebooklm-connector-research.md` (F64–F69 are the content gates and the
provenance defect).

> **THE SHAPE BELOW IS THIS BUNDLE'S EXPECTATION OF AN ENDPOINT JAVIS-SERVER
> OWNS**, and it is now read off the endpoint javis-server shipped rather than
> guessed at. The spec left "the push endpoint's exact request shape and error
> vocabulary" to the builder; the builder chose `POST /api/skill/wiki/sources`,
> named for what it is rather than for NotebookLM. The E2E runbook's tool box
> still curls the earlier guess, `POST /api/skill/sources/push`, which no
> router serves — the curl line is stale, not the code.
>
> Every value below has one definition and this file cites it:
>
> | what | javis-server file |
> |---|---|
> | the path | `app/routers/skill_wiki_sources.py` (`@router.post`), prefixed `/api` in `app/main.py` |
> | the request fields | `WikiSourcePushRequest`, same file |
> | the response envelope | `_envelope` in `app/services/skill_wiki_sources.py` |
> | the refusal codes | `REFUSAL_NEXT_STEPS`, same file |
> | the locator rules | `wiki_source_gates.locator_for` / `check_namespace` |
>
> The two halves disagreed once, in four places at once, with both test suites
> green — each asserted its own invented shape. `test/contract.test.js` now
> reads those javis-server files directly whenever a checkout sits beside this
> one, so the pair is checked and not just each half.

## Transport

Ordinary HTTP to javis-server, authenticated by the container's
`OPENCLAW_GATEWAY_TOKEN` bearer — the same shape `POST /skill/data`,
`/transcripts/recent` and `gmail-wiki-ingest`'s three candidate calls already
use. The script makes the call; javis-server runs the work in its own process
against its own database session.

**What the token does and does not carry.** It identifies the **user**, not the
skill: one token per container, shared by every skill installed in it. Two
things follow:

1. **The user cannot be redirected.** `user_id` comes from the token and is
   never read from the body. A run can only ever touch its own user's sources
   and wiki.
2. **The skill is named in the body and validated rather than trusted.** The
   server rejects a slug no registered adapter claims. The residual exposure is
   one user's own skills, never another user's data. Restoring the stronger
   guarantee needs a per-skill credential, which does not exist today.

**There are exactly two endpoints and both are writes.** That is R19 and it is
the whole point of the endpoint: a compromised skill cannot use this route to
read the wiki, another source, or another user's data. `scripts/server.js`
exports no GET and no read helper, and `test/server.test.js` asserts the
absence rather than documenting it.

## `push` → `POST /api/skill/wiki/sources`

**Request.** Every field here is one `WikiSourcePushRequest` declares. Pydantic
drops unknown keys without a word, so a field this bundle invents is not a
contract, it is a silence — which is exactly what `skill`, `path` and
`notebook` were.

| field | shape | notes |
|---|---|---|
| `source_type` | string | `notebooklm`. **R17**: the server records which kind of source the row is and names its wiki page after that kind — `SLUG_PREFIXES` in `app/services/obsidian_ingest.py` keys on this string, so the source page is `notebooklm-note-<id>` and never `obsidian-note-<id>`. `obsidian` is refused by name: those rows are the user's vault. |
| `source_id` | string | The NotebookLM note id, **verbatim**. Already a lowercase uuid (F65), which is exactly what `check_source_id` wants, so there is no mapping table. Uppercase is refused, not normalised — two spellings would be two rows. |
| `op` | string | `upsert` (the default) or `delete`. |
| `title` | string | The note title. May be empty: 4 of the 6 notebooks in the research account have one, and `clean_title` falls back to the locator's stem. |
| `text` | string | The **normalised** note text. See "normalise then hash" below. |
| `body_hash` | string | 64 lowercase hex: sha256 over the UTF-8 bytes of `text` exactly as sent. |
| `notebook_id` | string | Optional. One segment of the locator the server builds. **It must match `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`** (`check_namespace`), which a notebook TITLE usually does not — a space or a CJK character would be a hard `invalid_request`. `notebookId()` slugifies, and omits the field when nothing usable survives: a locator without the notebook segment is worse, no ingest at all is worse still. |
| `dry_run` | boolean | Always sent, `false` on a real push. `true` reports what it can and writes nothing (R3). A flag on the one endpoint rather than a second route, so there is exactly one way content enters. |
| `upstream_error` | string | Optional. The skill reporting that it could not reach NotebookLM at all. Answered `upstream_unavailable` / 502 with the re-authorise action. Sent by `reportUpstream`, never on a normal push. |
| `response_headers` | object | Optional. The header NAMES the container saw from Google, for **R16**. The server records the FIRST `Sec-Session-*` ever reported for this account (`wiki_logs`, op `source_canary`) — a fact about the account, which only it can hold. Values are never read and never sent. |

**There is no `path` field, by design.** `locator_for` derives the stored
locator from the kind, the id and `notebook_id` — "nothing a skill sends can
shape a stored path". `buildPath` still exists and is still checked against
`check_locator`'s rules, but what it produces is the path the DIGEST and the
LEDGER show the user, not a wire field.

**Response.** One envelope, the same keys on every path — stored, unchanged,
dry run, refused — so a caller never branches on presence (`_envelope`).

| field | shape | notes |
|---|---|---|
| `status` | string | `pending` (202, queued for the poller), `unchanged`, `dry_run`, `deleted`, `deleting`, or `refused`. There is no `ok`. |
| `source_type`, `source_id` | string | the row the push landed on |
| `source_slug` | string | `notebooklm-note-<id>` — the source page's slug (R17) |
| `page` | object | `{page_type, slug, action}` where `action` is `create` or `update`: the SOURCE page this push writes. |
| `feeds` | array | `[{page_type, slug, action}]` — the pages the ledger already says this source contributes to. |
| `would_change` | string | `new` / `update` / `unchanged` / `delete` |
| `budget` | object | `{units_per_hour, units_remaining, window_seconds, shared_with}` — **R9**'s budget line, rendered into the digest footer verbatim. Honest about the sharing: one rolling-hour budget covers every kind of ingest, so an Obsidian vault and a NotebookLM push can starve each other. |
| `notice` | string\|null | On a dry run, what the preview cannot name (see R3 below). |
| `canary` | object | `{flagged, first, headers}` — **R16**. |
| `error`, `error_description`, `next_step` | string\|null | `null` on a 2xx; on a refusal, the code, the reason and the one action (**R4**, **R5**). |

**R20's page list is `page` + `feeds`**, in that order, each keeping the
server's `create` / `update` marker. There is no `pages` key and there never
was; there is no `url` either, because the envelope names pages by slug and
hands back no content (R19) — so a page renders unlinked unless javis-server
starts sending one. `sanitizeUrl`'s allowlist (`javis://` or `https://`, URL
characters only) stands ready for that day and drops anything else.

**R3 is narrowed, and the narrowing is in the answer.** A dry run names the
source page, whether it is new, the refusal it would get, and the pages this
source already feeds. It cannot name the concept pages the ingest will write:
that is an LLM extraction the poller runs minutes later, and this route is
contractually forbidden from distilling. The server says so in `notice` and the
digest prints it, rather than implying the list is complete.

**The content gates, all server-side and all mirrored client-side.** These are
`javis_mcp/obsidian_sources.py`'s existing rules, which a real NotebookLM note
passes unmodified (F64: 9 of 13 gates pass, 4 refuse exactly as designed, 0
unexpected):

| rule | server | this bundle |
|---|---|---|
| `body_hash` is 64 hex | `_HEX64` | `normalize.hash` only ever emits that |
| text has no NUL | `_storable` | `checkText` → `text_has_nul` |
| text has no lone surrogate | `_storable` | `checkText` → `text_not_utf8` |
| text ≤ 262144 bytes of UTF-8, **checked before the hash compare** | `MAX_TEXT_BYTES`, `_TooLarge` first | `checkText` → `text_too_large`, and no hash is computed |
| `sha256(text) == body_hash` | `_check_text_and_hash` | `prepare()` guarantees it |
| the locator is relative, `.md`, no bad segment, not under `Javis-wiki` | `check_locator` (over the locator the SERVER builds) | `buildPath`, over the DISPLAY path |
| source id is a lowercase uuid | `check_source_id` | `UUID_RE` → `source_id_invalid` |
| `notebook_id` is one safe locator segment | `check_namespace` | `notebookId()` slugifies, or omits the field |

**Normalise then hash, and why it is the client's problem.**
`_check_text_and_hash`'s own docstring says the server must not rewrite the text
because "rewriting the text here would make every hash mismatch". F67 confirmed
it empirically: normalising the note and keeping the earlier hash produced
`body_hash does not match the text`. So the order is the contract —
`normalize(raw)` then `hash(text)`, never the reverse — and
`test/normalize.test.js` pins the inversion as a failing case.

**Refusals.** Each is one machine-readable code with one reason and one next
action (R4, R5); `SKILL.md`'s Errors table is the full list, and
`test/skill-md.test.js` fails if the table and the code drift apart.

The vocabulary is javis-server's, code for code with `REFUSAL_NEXT_STEPS`:

| code | status | what it means |
|---|---|---|
| `invalid_request` | 400 | a field is missing or malformed, or `sha256(text as sent) != body_hash` |
| `unsupported_source_type` | 400 | the kind is not one this endpoint accepts (`obsidian` never is) |
| `payload_too_large` | 413 | the note is over 256 KiB, or the body over 2 MiB |
| `quota_exceeded` | 507 | the account already stores as many sources as it may |
| `conflict` | 409 | the id belongs to another kind, or was deleted and is never reused |
| `budget_exhausted` | 429 | the rolling hour's wiki-ingest units are spent |
| `upstream_unavailable` | 502 | the answer to `upstream_error` |
| `internal_error` | 500 | the source could not be stored |

**The server's `next_step` wins over this bundle's row.** It was computed
against the actual request and names the field; the local row is the fallback
for a code that arrives without one. Dropping it for "report the code and stop"
would be R5 failing at the one point it exists for. The status decides when
there is no code at all, so a 401 from an ingress and a 413 from a body-size
guard both still land on a row the table has, and an unknown code is reported
under its own name and exits non-zero rather than being dressed up as a known
one — or, worse, as a success.

## `report` → `POST /api/agent/push`

An existing generic endpoint that needed no change for this skill. Body is
`{skill, content}` — markdown, rendered by the script from run state.

**No `session_id` and no `dedup_key`, deliberately.** With neither set the
server resolves `session_source="history"`, which joins the newest existing
`notebooklm-ingest` session, so a daily message appends to yesterday's thread
rather than opening a new branch of the chat tree every morning. Same choice
`gmail-wiki-ingest` makes, for the same reason.

This is the **only** output path a scheduled run has: an `openclaw cron` turn is
started by openclaw's own timer, so javis-server never builds a `body.tools` for
it and `chat_emit_*` is simply absent. See `trigger-contract.md`.

## What is NOT here

- **No `notebooklm_*` MCP tools.** An earlier revision of the design had
  javis-server orchestrate the reads through them. That is superseded: it would
  have pulled a 161k-line dependency on ~65 undocumented Google RPC ids into
  javis-server's tree and made every Google breakage a server deploy.
- **No read endpoint of any kind**, which is R19.
- **No javisweb route.** javisweb has no ingest route at all and neither
  Obsidian nor Gmail ingest has one; results surface as cards on the user's
  timeline.
- **`wiki_ingest_external_tool`** remains over MCP, behind OAuth on javis-mcp,
  and takes text from any origin with no Google access. It is the path that
  survives a Google breakage and it is deliberately independent of this skill.
