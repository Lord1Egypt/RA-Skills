# Source policy

This is the **only** source standard in `job-hunt`. It governs every live
retrieval in every mode. If the skill's own behaviour would violate a line here,
the line wins and the behaviour changes — a policy the skill violates on every
run teaches the reader to ignore all of it.

**Account risk is not zero.** Every yellow action below runs inside the user's own
logged-in browser session, on the user's own account, against a platform that did
not agree to it. The caps exist to keep the behaviour closer to note-taking than to
automation, not to make the risk disappear. The user can stop at any point, and
discover mode is never triggered as a side effect of another mode — starting it is
always an explicit act by the user.

## Green

Allowed by default, no disclosure needed:

- Job descriptions, links, PDFs, screenshots or CSV/JSON exports the **user** pasted.
- Official or public job APIs with a documented usage path.
- Public employer career pages reachable without a login and without a bypass.
- Search-engine results that point at public career pages.
- `opencli <site> --help -f yaml`, `opencli list`, `opencli doctor`,
  `opencli auth status` — introspection that touches no site.
- opencli read commands on adapters that have **no auth or login command**
  (`51job`, `indeed`: absent from `opencli auth status` entirely, and exposing no
  `login` command), within the caps below. This describes the adapter, not the
  website's access requirements; an actual login or verification wall still
  requires user recovery.

## Yellow

Allowed, capped, and disclosed. Say plainly that account risk is not zero.

- opencli read commands on a **logged-in** adapter (`boss`, `linkedin`) in a session
  the user is present for.
- **Pagination** within the round cap. `brief.yaml` must carry `max_rows_per_round`
  and `max_pages_per_site`, and these are **ceilings, not defaults**: at most 25
  rows per site per round and at most 2 pages per site. `check_shortlist.py`
  enforces both with `CAP_MISSING` (the brief left one out) and
  `CAP_ABOVE_CEILING` (the brief raised one) — the cap is a check, not a promise.
  Also never above the adapter's own documented `--limit` ceiling — indeed caps at
  25, 51job at 50, linkedin at 100, upwork at 50.
- **Detail-page fetch**, and only for rows whose provisional verdict is
  `strong_apply`, `worth_applying` or `stretch`. `likely_screen_out` and `blocked`
  rows stay card-level during initial triage and are labelled 未取详情. Before a
  complete report, exclude them or read them if they are retained. A user-named
  fetch or a read needed to complete a retained row goes in `shortlist.yaml` `detail_fetch_exceptions` with
  a reason. `check_shortlist.py` enforces this with `DETAIL_FETCH_OUT_OF_BAND` —
  the cap is a check, not a promise. A separate `brief.yaml.max_match_reviews`
  value from 1 to 5 caps how many fetched details can enter the CV-to-JD matching
  review; `check_candidate_match.py` enforces it. A named fetch does not turn that
  bounded review into an unbounded one. Full-description reading is separate:
  `detail_unmapped` retains a verified description without doing a CV mapping.
  A report target never overrides site caps, stop signals or user recovery.
- Small-volume capture for the user's own analysis, with source, timestamp and
  read-quality retained on every row.
- **Stop on any risk-control signal**, for that site, for that round. Do not retry.
  Do not change parameters and retry. Do not route around it. First pause and
  offer [user recovery](user-recovery.md); resume only after explicit user
  confirmation, in a new bounded round preserving the stopped journal.
  Offer partial results or directions if the user declines or cannot recover;
  do not silently end the task while waiting for a login/verification reply.

## Red

Never performed and never designed, whatever the user asks:

- Captcha, risk-control, fingerprint, proxy or stealth evasion of any kind.
- Multi-account rotation or cookie switching between identities.
- Background or unattended operation while the user is not present.
- Batch apply, batch greeting, auto-chat, auto-reply, or any automated contact with
  a recruiter or hiring manager.
- Running any opencli command whose published `access:` is `write` — including
  `login`. It is never run here. Ask the user to click Login/登录 on the page kept
  open in their daily browser; do not ask them to run a terminal command. Follow
  [user recovery](user-recovery.md) and wait for their explicit completion reply.
- Claiming a job is open without a fresh source signal.
- Presenting a fabricated, inferred or padded listing as retrieved. If the count
  falls short of the target, write the reason; never pad.

## What changed from the retired policy

`~/.codex/skills/job-search-coach/references/source-policy.md` is retired. Three of
its Red lines moved, and naming them honestly matters more than the move:

| Retired Red line | Now | Why |
|---|---|---|
| "Auto-scroll or page through large result sets" | Yellow, capped by `max_pages_per_site` | Two pages of a keyword search a human asked for is not a scrape; an uncapped crawl is. The cap is the difference, so the cap is enforced by a script. |
| "Automatically opening many detail pages" | Yellow, capped to the top three verdict levels | "Many" was never defined, so it could not be checked. "Only the rows the user might actually apply to" can be. |
| "Hidden/internal API calls on logged-in job boards" | Yellow | This is the uncomfortable one, said plainly: opencli's `strategy: cookie` read commands on `boss` and `linkedin` **are** requests to the site's own endpoints carrying the user's session. Calling that Red while building the skill on top of it would be a lie in a file whose only job is to be true. |

Unchanged: every Red line about defeating a control the platform put up on purpose,
and every Red line about writing.

## Required source metadata

These are not a separate schema — they are the `JobListingEvidence` fields that
`check_shortlist.py` already enforces on every row:

| Metadata | Field | Enforced by |
|---|---|---|
| source name | `source_site` | `NO_SOURCE_SITE` |
| traceable identifier | `source_id`, verbatim in `raw/<site>-*.json` | `SOURCE_ID_NOT_IN_RAW` |
| collection time | `retrieved_at` | `NO_RETRIEVED_AT` |
| extraction method | `extraction_method`: `adapter_search` \| `adapter_detail` \| `user_paste` \| `public_page` | `BAD_ENUM` |
| text quality | `quality`: `complete` \| `partial` \| `card_only` | `BAD_ENUM` |
| verification status | `verification`: `fresh_verified` \| `collected_unverified` \| `stale_possible` | `BAD_ENUM` |
| original URL | `url`, verbatim from an adapter response | `URL_NOT_FROM_ADAPTER` |

The retired policy's screenshot / visible-capture extraction methods are gone:
there is no OCR pipeline in this skill and there will not be one. A screenshot the
user pastes is `user_paste`, and if it cannot be read, the honest output is
`insufficient_evidence`, not a guess.

## Source tiers apply to ACTIONS, not to rows

A row does not carry a tier. The tier describes what was done to obtain it, and
that is already recorded: `journal.jsonl` holds the site, command and classification
of every invocation, and `check_no_write.py` resolves each one against opencli's own
`access:` metadata. A `source_tier` column on a row would be a self-assessment with
nothing checking it.

## Browser retrieval

`references/daily-browser.md` defines CDP-first daily-browser routing and shared
concurrency budgets; `references/browser-fallback.md` defines its capture path. Public page reads follow Green; logged-in reads and pagination follow
Yellow with the same caps. Browser snapshots use `browser_page` extraction and
`browser_call` records, with original URLs from the page rather than an adapter.
`check_no_write.py` verifies the fixed snapshot operation and capture hashes;
`check_shortlist.py` verifies browser row provenance and shared limits. Stop
signals apply to the site across tools. No arbitrary browser eval or write action
can be declared safe merely by labelling it a read.

## Removed sources

1point3acres (一亩三分地) is outside job-hunt scope. Do not query it, recommend it
as an interview source, or include it in a recovery queue. Historical captures
and regression fixtures remain evidence of past behavior, not active routing.
