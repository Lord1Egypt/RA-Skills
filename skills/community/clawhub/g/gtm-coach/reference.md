# GTM Coach — reference

Companion to [SKILL.md](SKILL.md) and **[playbook.md](playbook.md)**. Keep `plan.json` small. Live pains/leads stay on the API. Strategy turns are a CMO board (stage + project type + channel index). Channel SOPs load only after the founder chooses to execute.

## plan.json (hot)

Copy [plan.example.json](plan.example.json). Allowed top-level keys:

| Key | Purpose |
| --- | --- |
| `version` | Plan schema version (`2`), not the Skill release version |
| `skill` | Installed Skill version and last update check. Auto-apply on newer remote; do not prompt |
| `current_week` | ISO week from `GET /status` (`2026-W38`) |
| `intake` | `blank` \| `industry` \| `idea` \| `shipped` — how much product exists |
| `product` | Pin: name, `project_type`, one_liner, icp, url, repo_confirmed |
| `strategy` | CMO board (see below). `confirmed` must be true before dumping pains/leads |
| `modules` | Exact project-type, primary-channel, and optional-campaign files loaded this week |
| `connection` | Bind state; never stores the secret token. `last_cta_id` + `offered_week` throttle upgrade CTAs |
| `focus` | One sentence for this week’s bet |
| `constraint` | First missing outcome shown on the board and dashboard (max 240 chars) |
| `this_week` | Theme + one active experiment + 3–7 micro-tasks |
| `open_decisions` | Pointers only: `{ id, source, ask, url? }` — max 20 |
| `filters` | `ignore_pain_tags`, `prefer_subreddits`, `skip_subreddits` |
| `last_outcomes` | Compact channel/result counts + optional `manual_note` |
| `partners` | `waiting` \| `open` \| `handed_off` |
| `milestones` | Fixed ids for dashboard + Build-in-Public triggers. See below |
| `scorecard` | Deterministic GTM readiness scores. Recompute from [dashboard.md](dashboard.md); never vibe a number |
| `share` | Signature opt-in + last BIP draft pointer. No tokens |

### `strategy` (required)

`product.project_type` uses the NicheReach project values: `MICRO_SAAS`, `SERVICE_FREELANCER`, `NEWSLETTER_MEDIA`, `DIGITAL_PRODUCT`, `COMMUNITY`, `CREATOR_ARTIST`, `BRAND`, `EDUCATION_COHORT`, or `PLATFORM_MARKETPLACE`. Apply the matching lens in `playbook.md`; do not assume every project ships code or converts through a trial.

| Field | Values |
| --- | --- |
| `confirmed` | `true` only after the founder agrees the board |
| `period` | `validate` \| `build` \| `cold_start` \| `launch` \| `promote` \| `monitor` |
| `build` | `not_started` \| `in_progress` \| `mvp` \| `shipped` |
| `evidence` | `none` \| `anecdote` \| `pains_scored` \| `waitlist` \| `paying` — same list as SKILL.md. `pains_scored` includes observed use. Retained/referring customers stay `paying` plus a `manual_note`. |
| `primary_channel` | `direct` \| `reddit` \| `indiehackers` \| `linkedin` \| `x` \| `short_video` \| `youtube` \| `newsletter` \| `seo` \| `producthunt` \| `hackernews` \| `webinar` \| `podcast` \| `partnerships` \| `paid` \| `other` \| `undecided` |
| `channels_this_quarter` | short list of channel ids |
| `launch_optional.producthunt` / `show_hn` | booleans — optional campaigns, not the weekly engine |
| `share_loop` | natural artifact/action or `none yet`; never force an invite |
| `paid_promotion` | `blocked` \| `validation_test` \| `eligible_to_test`; scale spend needs payment + value/retention |
| `seo_status` | `not_applicable` \| `audit_needed` \| `foundation_ready` \| `content_loop` |
| `note` | max 240 chars |

**Never store:** full `post_body`, long pain descriptions, tokens, partner pitches.

### `this_week.micro_tasks`

3–7 rows. Each: `{ id, title, status, done_at }`.

| Field | Values |
| --- | --- |
| `id` | Stable slug, e.g. `mt_1` |
| `title` | One founder action (max 120 chars) |
| `status` | `todo` \| `doing` \| `done` |
| `done_at` | ISO date when `done`, else `null` |

Completing a micro-task does **not** offer a BIP draft. Only [milestones](#milestones) do.

### `milestones`

Keep these five ids. Do not invent extras. Status is `todo` or `done`.

| id | Done when |
| --- | --- |
| `picture_confirmed` | `strategy.confirmed` becomes `true` |
| `channel_committed` | `strategy.primary_channel` is set and not `undecided` |
| `week_reviewed` | `this_week.active_experiment.decision` is `continue` \| `change` \| `stop` |
| `evidence_upgraded` | `strategy.evidence` moves to a strictly higher rung than `share.evidence_watermark` |
| `replies_10` | `last_outcomes.replies_posted_7d >= 10` (instrument count — not ICP proof) |

Evidence rungs, low → high: `none` < `anecdote` < `pains_scored` < `waitlist` < `paying`.

On `evidence_upgraded`: set `done`, `share_offered=false`, then `share.evidence_watermark` to the new evidence. A later upgrade may fire BIP again. `replies_10` fires once.

`share_offered` is `true` after the founder accepts **or** skips the BIP offer for that completion. Do not nag.

### `scorecard`

Recompute with the rubric in [dashboard.md](dashboard.md). Store the result; do not ask the model for a “feel” score.

| Field | Rule |
| --- | --- |
| `label` | `GTM forming` (<40) · `GTM in motion` (40–69) · `GTM ready` (70–84) · `GTM strong` (85+ **and** evidence is `waitlist` or `paying`). Never write **GTM Validated** |
| `total` | Weighted round of the five dimensions |
| `weights` | picture 20 · evidence 25 · channel 20 · weekly 20 · learning 15 |
| `dimensions.*` | Integers 0–100 from the rubric |

If total would be 85+ but evidence is below `waitlist`, keep the number and cap the **label** at `GTM ready`.

### `share`

| Field | Rule |
| --- | --- |
| `signature_enabled` | Default `false`. Set `true` only if the founder opts in on a BIP draft |
| `signature` | Exact: `Via gtm_coach by nichestarter.ai`. Do not list it as a numbered BIP post. The dashboard appends it when the founder copies or shares. |
| `evidence_watermark` | Last evidence rung that already triggered `evidence_upgraded` |
| `bip` | **Required** on every dashboard generate when `product.name` is set: `{ trigger, channel, posts }`. `posts` is 3 X drafts or 1 LinkedIn draft. Never `null` for a named product — the HTML hides the BIP card and share buttons if `posts` is empty. |
| `last_bip` | `{ trigger, channel, drafted_at, posted, path }`. `posted` is true only if the founder says they published. Path is `.gtm/share/bip-draft.md` |

Dashboard files (not secrets): `.gtm/dashboard.html`, `.gtm/share/scorecard.md`, `.gtm/share/bip-draft.md`. Local only. No hosted badge in this release.

Hosted `https://nichestarter.ai/badge/{id}` is **not built**. Do not invent that URL. Export Markdown/PNG from the local dashboard instead.

### Selective module protocol

**Board layer**

1. Persist the full `gtm-coach/` bundle into **this** agent’s skills folder if missing (see SKILL.md). Never store plan or tokens there.
2. On first write, copy [plan.example.json](plan.example.json). Load this reference only then, or when schema/API changed. Write `.gtm/` at the workspace root for the bound project (monorepos: do not nest inside `web/` unless that is the root). If `.gtm/plan.json` already exists, resume it—do not re-init. Any agent that opens the same folder can read it; each agent still needs its own skill install.
3. Resolve `strategy.period` through `stages/index.md` (use `status.picture` as a hypothesis). Store one exact path in `modules.stage` and load that SOP.
4. Resolve `product.project_type` through `project-types/index.md`; store one exact path in `modules.project_type` and load that SOP.
5. Score channels through `channels/index.md` only. Record the recommended id in `strategy.primary_channel`. Keep `modules.primary_channel` **null** until a dive.
6. Cite `outcomes.leads_pending` / `replies_posted_7d` as instrument counts on the board. Do not GET `/leads` until the founder confirms the board and chooses a community channel.

**Dive layer**

7. Load a channel SOP only after the founder chooses to execute or inspect that channel; then store its path in `modules.primary_channel`.
8. Set `modules.optional_campaign` only after the founder approves one additional campaign.
9. Do not load all stage/project/channel modules. After a dive, keep the CMO board (stage included) at the top of the turn.
10. When type/channel/stage changes, replace the path and record why in the weekly journal.

**Dashboard layer**

11. After RECORD, or when the founder asks for the dashboard / scorecard / BIP, load [dashboard.md](dashboard.md). Rewrite `.gtm/dashboard.html`. Do not load it for a normal strategy board.

When `current_week` from `/status` differs from `plan.json`, close the old week first.

### Skill release state

`GET /api/gtm/agent` → `skill_release` is the canonical update manifest.

| Field | Rule |
| --- | --- |
| `skill.installed_version` | Last complete Skill bundle the agent loaded |
| `skill.last_checked_at` | ISO timestamp of the latest successful manifest check |
| `skill.last_update_notice_version` | Last auto-apply notice version; do not repeat the one-line note every turn |
| `skill.deferred_until` | Legacy. Ignore. Auto-apply does not defer |

The top-level `version` remains the plan schema. Never overwrite it with a SemVer string.

`skill_release.update_policy` is `check_each_new_session_auto_apply`. Follow it.

Version behavior:

- PATCH/MINOR/MAJOR skill files: auto-apply at session start. No founder confirmation.
- Higher `plan_schema_version`: add missing `plan.json` fields from the example; keep existing strategy.
- Offline/check failure: continue the installed version and retry next new session. Never block coaching.

### Project bind and CTA state

| Field | Values / rule |
| --- | --- |
| `connection.status` | `unbound` \| `bound` |
| `connection.last_cta_id` | Last shown `status.cta.id` |
| `connection.offered_week` | ISO week; with `cta.once_per_week`, stay silent for the same id |
| `connection.project_id` / `project_name` | Set only after bound `/status` verifies the key |

Coaching requires a project token. Binding is free. Follow `status.cta` after the board. Store the token only in `.gtm/secrets.md`, never `plan.json`.

## inbox.json

Open items only. After a decision, delete the row and append a line to `journal/{week}.md`. Cap 20. See [inbox.example.json](inbox.example.json).

## journal/YYYY-Www.md

Append-only. Do not load more than the **current** and **previous** week into context. See [journal.example.md](journal.example.md).

## Decision protocol

### Pains (`source: starter`)

Ask: `build` | `later` | `not_us`

- `build` → add a micro-task (spec, copy, or ship). Remember `id` in `last_outcomes.pains_shipped` when they say it shipped.
- `later` → journal only; do not re-push for 2 weeks.
- `not_us` → add a tag or phrase to `filters.ignore_pain_tags`.

### Leads (`source: reach`)

Ask: `open in extension` | `save` | `skip`

Store `url` (the Reddit `post_url`) on the inbox row. When you show the lead, it must be a markdown link `[title](url)`.

- `open in extension` (legacy alias: `reply`) → **do not fetch the post and do not draft copy**. Send the founder to the URL with the **NicheReach Chrome extension** ([install](https://chromewebstore.google.com/detail/nichereach/meijkmdpgkfookehfglnkdcjgobheemp)). Inbox: `https://www.nichestarter.ai/reach`. Next session ask if they posted.
- `save` → journal; they can open `/reach`.
- `skip` → if the same subreddit is skipped 3 times, add to `filters.skip_subreddits`.

Do not list `r/sub 「title」` without a URL. Do not make pasting into reddit.com the default publish path. Do not scrape or open the thread in the agent to write a comment.

### Manual stats

If `/status.outcomes` cannot explain the week, ask **one** paste:

> Waitlist signups, revenue, or “I posted N replies and heard back from …” — one line is enough.

Put it in `last_outcomes.manual_note` (max 240 chars).

### Action experiment

Keep only one `this_week.active_experiment`:

| Field | Rule |
| --- | --- |
| `action` / `channel` | The chosen action and where it runs |
| `hypothesis` | One falsifiable sentence |
| `success_metric` / `target` | Closest useful outcome: qualified conversation, demo, activation, repeat use, referral, or payment |
| `baseline` | Number or `unknown`; never invent |
| `artifact_url` | Public URL when available; use `private` for email/DM/interview |
| `review_on` | Date or event trigger |
| `result` | Compact counts + qualitative lesson |
| `decision` | `pending` \| `continue` \| `change` \| `stop` |

When results arrive, judge signal quality before proposing more work. Impressions, likes, and followers alone are not proof; connect them to qualified responses or product behavior. Append the conclusion to the weekly journal.

## Copy templates

### Community replies

Do not write Reddit/Facebook comments here. Handoff: clickable `post_url` + NicheReach extension.

### X

- Offer a useful single post or a learn / ship / ask three-post set.
- One idea per post, founder’s voice, no invented metrics or fake controversy.
- Track qualified replies, site actions, and conversations; impressions are context.
- Milestone BIP drafts: follow [dashboard.md](dashboard.md). Copy/share appends `Via gtm_coach by nichestarter.ai` — do not list it as a numbered post.

### LinkedIn

- One evidence-led post from stored facts (problem, lesson, limitation, or question).
- BIP drafts for LinkedIn use the same milestone trigger as X. Founder publishes.

### Direct outreach

- Start with a real trigger and a specific pain/job question.
- Ask for a short conversation, demo, manual pilot, or paid pilot according to evidence.
- Personalize from facts; no bulk generic pitch.

### Show HN

- Title: `Show HN: {thing} — {honest outcome}` (no “game-changer”).  
- Body: what it is, who it is for, what is still rough, link.  
- Do not claim user counts you cannot see.

### Product Hunt (only if on the strategy board)

- Name + tagline: what it does for whom.
- First comment: who it is for, what is still rough, link.
- Same week: keep one normal primary-channel action. The launch spike fades.

## API catalog (shipped)

Base `https://www.nichestarter.ai`

Module routing:

- `/skills/gtm-coach/stages/index.md` → choose one current-stage SOP.
- `/skills/gtm-coach/project-types/index.md` → choose one of nine project SOPs.
- `/skills/gtm-coach/channels/index.md` → choose one primary-channel SOP.
- `/skills/gtm-coach/dashboard.md` → local dashboard, scorecard rubric, BIP drafts (after RECORD).
- Bound `/status.project_type_playbook_url` gives the exact project-type module.
- `/status.channel_playbook_url` gives the channel index because primary channel is founder/local-plan state.
- `skill_release.dashboard_url` and catalog `dashboard_playbook_url` point at the dashboard SOP.

| Method | Path | Auth | Role |
| --- | --- | --- | --- |
| GET | `/api/gtm/agent` | no | Canonical `skill_release` manifest + catalog/module URLs |
| GET | `/api/gtm/agent/status` | `nmagt_` to coach | Unbound: `bind_required`. Bound: project + `billing` + `entitlements` + `sample` + `cta` |
| GET | `/api/gtm/agent/brief` | `nmagt_` | Linked-topic pains. Unbound returns 401; no public-library teaser |
| GET | `/api/gtm/agent/opportunities` | `nmagt_` | Ranked Nichestarter opportunities for the bound project (Basic/Premium) |
| GET | `/api/gtm/agent/leads` | `nmagt_` | Pending NicheReach leads for this project |
| GET, POST | `/api/gtm/agent/topics` | `nmagt_` | List / create / link Nichestarter searches on this project |
| GET | `/api/public/weekly-report-preview` | no | Optional Monday pain evidence |
| GET | `/api/social/daily-brief` | no | Optional recent pain evidence |

Token: same NicheMatch bind key. Header `Authorization: Bearer` plus the `nmagt_` key, or `X-NicheMatch-Token`. Never echo a pasted key. **Required to coach.** Existing keys with `profile:write` work — no re-issue required.

`GET /status` includes `picture`, `billing`, `entitlements`, `sample`, `cta`, and `outcomes.kind: "instruments"`. Suggestions are not confirmation. Follow `status.cta`. `status.next` must not be treated as permission to fetch `/leads`.

For a bound project, brief mode is **project_topics** when Nichestarter searches are attached. With no linked topic it returns `mode: "topic_required"` and `items: []`; it never falls back to public-library keyword overlap. Verifying a project auto-provisions a first-project sample. `POST { "action": "create_from_project" }` on `/topics` uses the same provisioner. Extra custom topics still need Premium seats. If they cannot upgrade, continue coaching from the bound brief.

### Capability and CTA boundaries

| Need | Available now | If unavailable / human action |
| --- | --- | --- |
| Keep monitoring linked topics | `GET /status` checks `starter.mode`; `GET /brief` returns linked-topic pains | If `topic_required`, ask once; on yes attach/create at `https://www.nichestarter.ai/projects` |
| Ranked product opportunities | `GET /opportunities?limit=5` when Basic/Premium | If `upgrade_required`, note once; coach from brief + leads |
| Fetch potential customers | If `discover_enabled`, `GET /leads` returns pending Reach leads including `post_url` | If off, ask once; on yes send to `https://www.nichestarter.ai/reach`. The agent cannot start it |
| Draft and publish a reply | NicheReach Chrome extension reads the thread, drafts, and safety-checks | Founder opens `post_url` in the extension and clicks Post. Agent never fetches the post, never drafts, never posts |
| Fetch/handle partners | NicheMatch skill + same token, only while `match.marketplace.enabled` | Value Card/matching CTA: `https://www.nichestarter.ai/nichematch` |
| Persist GTM decisions | Local `.gtm` inbox/journal | Server decision endpoint is not built |
| Local GTM dashboard / scorecard / BIP draft | `.gtm/dashboard.html` + `.gtm/share/` from [dashboard.md](dashboard.md) | Hosted badge is not built. Founder publishes social posts |

Fetched rows are **decision inputs**, not the plan:

1. Filter by confirmed ICP, period, and ignored history.
2. Explain fit in one sentence.
3. Ask one bounded decision (`build/later/not_us`, `reply/save/skip`, or partner investigate/pass).
4. Convert an accepted pain into one weekly task. Convert an accepted Reddit/Facebook lead into an extension handoff, not a drafted comment.
5. Journal/suppress rejected or deferred items so they do not recur.

## APIs not built yet (coach still runs)

Ask the founder to paste data, or send them to the web app. Do not block the week.

1. **`POST /api/gtm/agent/decisions`** — persist build/later/reply/skip on the server (today: local journal only).  
2. **`POST /api/nichereach/agent/draft`** — not used by this Skill. Drafting lives in the NicheReach Chrome extension.
3. **Watch / push webhook** — notify when new leads or pains arrive (today: they re-open the chat, or `/loop` on `/status` if they asked).  
4. **Plan sync to `/dashboard`** — optional upload of `plan.json` (today: local `.gtm/dashboard.html` only).  
5. **Hosted GTM badge / snapshot** — `https://nichestarter.ai/badge/{id}` is not built. Export Markdown/PNG locally.  
6. **NicheMatch** — matching stays behind `NICHEMATCH_MARKETPLACE_LIVE`; not required for coaching.

## Gitignore

```
.gtm/
.nichematch/
```

Do **not** gitignore the agent skills folder. It has no secrets. Optional: commit project-level `gtm-coach/` under `.cursor/skills`, `.claude/skills`, `.agents/skills`, and/or `.codebuddy/skills` (or symlink one canonical copy) so teammates on that host get natural-language calling. `.gtm/` stays local and is readable by any agent that opens the same workspace.
