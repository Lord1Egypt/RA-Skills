# Working File Templates — Growth

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/growth/config.yaml` | Key by key, read-modify-write |
| Business context, constraint, metric definitions, funnel, markets, retention, channels, loops, pricing, backlog, targets, pain points, due dates, box index | `~/Clawic/data/growth/memory.md` | Rewritten in place; stays small |
| Funnel stage rates over time | `## Funnel` in `memory.md`; `~/Clawic/data/growth/funnel-history.md` once it outgrows the section | One row per stage per period |
| Cohort retention curves | `## Retention` in `memory.md`; `~/Clawic/data/growth/retention-curves.md` once it outgrows the section | One row per cohort |
| Channels with CAC, payback, spend and kill numbers | `## Channels` in `memory.md`; `~/Clawic/data/growth/channels.md` once it outgrows the section | One row per channel, killed ones kept |
| Marketplace markets — liquidity per market | `## Markets` in `memory.md`; `~/Clawic/data/growth/markets.md` once it outgrows the section | One row per market. Never in `## Funnel`: that section holds one row per **stage**, and mixing the two makes the split undecidable |
| Experiment ideas awaiting a slot | `## Backlog` in `memory.md`; `~/Clawic/data/growth/backlog.md` once it outgrows the section | One row per idea |
| Experiments that ran, with their readouts | `~/Clawic/data/growth/experiments/<year>.md` | Append-only, cut by year — never a section of `memory.md` |
| Things you produced that get re-read — tracking plan, metric definitions, growth model, activation spec, loop design, referral program, lifecycle map, pricing change, stall review, win/loss synthesis, channel post-mortem, market-launch playbook, SKAN value scheme, contribution model | `~/Clawic/data/growth/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Paid budgets, growth-tool subscriptions, revenue commitments | `~/Clawic/data/finances/` (**shared**) | `budget.md`, `subscriptions.md`; amounts carry their currency |
| A launch or growth initiative with an owner and an end | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, from the first |
| People — agencies, freelancers, partners, creators, interviewed customers, champions | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, keyed by email |
| **Anything durable this table does not name** | `~/Clawic/data/growth/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, money, a device? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a procedure, a model, a decision with its reasoning, a spec? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A funnel stage was measured | Its row in `## Funnel`, with denominator, window and as-of date |
| A market's liquidity was read, or a market launched | Its row in `## Markets`, with the as-of date; the constrained side also goes to `## Business` |
| A constraint was named or expired | `## Constraint` |
| A cohort was refreshed or a curve read | `## Retention` |
| A channel was started, scaled, or killed | Its row in `## Channels`, with CAC, payback, spend and the kill number |
| A budget was committed | Shared `~/Clawic/data/finances/budget.md`, with currency and period |
| An experiment ended | A readout in `experiments/<year>.md`; the idea leaves `## Backlog` |
| An idea was proposed and scored | `## Backlog` |
| A loop was identified, timed, or falsified | `## Loops` |
| A lifecycle program shipped or changed | `artifacts/lifecycle-map.md` — the map is an artifact from the first state, never a section of `memory.md` |
| A metric, aha action, PQL, or natural frequency was defined | `## Metric Definitions` |
| Prices, plans, limits, or contribution per order changed | `## Pricing` |
| A target, forecast or falsifier was set | `## Targets` |
| A failure's cause was found, or the same failure appeared twice | `## Pain Points`; the second occurrence earns an artifact |
| A tracking plan, model, spec, program design, or review came out of the session | `artifacts/` |
| A person or agency became involved | Shared `contacts.md` |
| An initiative got an owner and an end date | Shared `projects/<project>.md` |
| A recurring review or refresh was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, experiment records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. **Who**: the agent about to add the entry that crosses the line — not a later cleanup.
2. **When**: count the section's entries **before** appending. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — split first, then append.
3. **What happens to the original**: in the same turn, create the file in `~/Clawic/data/growth/`, move the whole section into it, **delete the section from `memory.md`** leaving only its `## Boxes` line, and add the new entry to the new file.
4. **Precedence**: never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

**Isomorphism**: the extracted file keeps exactly the headings the section had — a `###` sub-heading becomes a `##` heading in the new file, same name, same order, nothing renamed and nothing merged. That is what makes the split a copy-paste instead of a rewrite that loses rows.

Artifacts are the exception: a model, a spec, a program design or a review is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted tracking snippet, ad-platform export, ESP configuration, `.env` or webhook setup is the densest source of secrets in this domain: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:SEGMENT_WRITE_KEY` · `env:ESP_API_KEY` · `keychain:meta-ads` · `1password:Work/Analytics/amplitude` · `bitwarden:Growth/Klaviyo` · `vault:secret/growth/ga4` · `ssm:/prod/stripe/key` · `file:~/.config/ga/credentials.json`

In a text, the pointer goes where the value was: `write_key: <env:SEGMENT_WRITE_KEY>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: GA4 property and measurement ids, ad account ids, campaign, ad set and creative names, UTM values, experiment and variant keys, audience and segment names, plan names and public prices, app store ids and bundle ids, domain and subdomain names, list and flow names, public referral codes, and every aggregate metric. **Secrets, strip them**: analytics write keys and server-side API secrets, ad-platform access and refresh tokens, ESP and SMS API keys, payment-processor secret keys, webhook signing secrets, CRM and warehouse credentials, connection strings, and personal access tokens sitting inside a pasted config.

One more rule that is not about credentials: **raw user-level exports** — rows carrying emails, names, addresses or phone numbers — never go into `~/Clawic/data/`. Keep the aggregate (the rate, the cohort, the count), drop the rows, and say so in one line.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [experiments/](#experiments) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [shared finances](#shared-finances) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/growth/` if it does not exist.

```yaml
business_model: saas
motion: hybrid
stage: growth
north_star: weekly active teams with 3+ members editing
target_cac_payback_months: 9
monthly_paid_budget: 12000
analytics_stack: posthog
experiment_confidence: 95
reporting_cadence: weekly
privacy_regime: gdpr

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  event_naming: object_action_snake_case
  utm_taxonomy: "source=platform, medium=channel-type, campaign=slug"
  cohort_anchor: first_touch
risk_posture:
  banned_tactics: [incentivized installs, purchased lists]
  discount_cap_pct_of_new_revenue: 10
output_format: memo-with-numbers
cadence:
  cohort_refresh: monthly
  channel_audit: quarterly
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Growth Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Channels incl. killed (17) → `channels.md`; read before proposing or scaling any channel
- Cohort curves (22 cohorts) → `retention-curves.md`; read before any retention or payback claim
- Experiments 2026 (41) → `experiments/2026.md`; read before designing a test, always
- Tracking plan → `artifacts/tracking-plan.md`; read before adding an event or quoting a rate
- Metric definitions → `artifacts/metric-definitions.md`; read before quoting any rate
- Q3 growth model → `artifacts/growth-model-2026-q3.md`; read before any target or budget question
- Activation spec → `artifacts/activation-spec.md`; read before changing onboarding
- Referral program v2 → `artifacts/referral-program.md`; read before touching incentives or attribution
- Lifecycle map (8 states) → `artifacts/lifecycle-map.md`; read before adding or changing any message

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Growth review (funnel + channels) | week, Monday | 2026-07-20 | 2026-07-27 |
| Cohort refresh | month | 2026-07-01 | 2026-08-01 |
| Channel audit incl. marginal CAC | quarter | 2026-04-10 | 2026-07-10 |
| Re-derive aha action | 2 quarters | 2026-03-02 | 2026-09-02 |
| Re-forecast against model | month | 2026-07-05 | 2026-08-05 |

## Business
saas, hybrid motion, stage growth. ICP: 10-50 person product teams. ACV 6.2k USD.
North star: weekly active teams with 3+ members editing (declared, see config.yaml).

## Constraint
Activation (22% → 30% achievable, ~950 USD MRR/month). Named 2026-07-14 off the 22.0% reading of
that date; the seeded-project ship has since moved the 30d rolling rate to 23.4%. Re-check 2026-10-14.

## Metric Definitions
| Metric | Definition | Window | Cohort anchor | Excludes |
|---|---|---|---|---|
| Signup rate | signups ÷ unique visitors | 7d | first touch | internal, bots |
| Activated | ≥1 project created AND ≥1 teammate invited | 7d from signup | first touch | internal |
| Natural frequency | median gap between value actions = 4 days → weekly reporting | — | — | — |
| PQL | ≥3 active users from one domain in 7d | 7d rolling | account | trials from free-mail domains |

## Funnel
| Stage | Metric | Current | As of | Prior | Source |
|---|---|---|---|---|---|
| Visitors | unique, 30d | 121,400 | 2026-07-25 | 118,900 | posthog |
| Signup | 3.1% | 3.1% | 2026-07-25 | 3.3% | posthog |
| Activated | 23.4% | 23.4% | 2026-07-25 | 22.0% | posthog |
| Paid | 6.5% | 6.5% | 2026-07-25 | 6.6% | billing |

## Retention
| Cohort | Size | P1 | P2 | P3 | P4 | P6 | P8 | P12 |
|---|---|---|---|---|---|---|---|---|
| 2026-04 | 1,240 | 52% | 41% | 37% | 35% | 34% | 34% | — |
| 2026-05 | 1,610 | 55% | 44% | 39% | 37% | 36% | — | — |
Flattens ~34% by P6. Weekly periods (natural frequency 4 days).

## Channels
| Channel | Status | Spend/mo | CAC | Payback | New/mo | Kill number | As of |
|---|---|---|---|---|---|---|---|
| Non-brand search | scaling | 9,000 USD | 168 USD | 7.1 mo | 54 | CAC > 240 USD | 2026-07-25 |
| Content/SEO | scaling | 4,200 USD loaded | 71 USD | 3.0 mo | 59 | — | 2026-07-25 |
| Paid social | testing | 2,500 USD | 310 USD | 13.1 mo | 8 | CAC > 240 after 30 conv or 6 wks | 2026-07-25 |
| Cold outbound | killed 2026-05 | — | 890 USD | — | — | killed on number | 2026-05-30 |

## Loops
Collaborative invite. activated user → invites collaborator → collaborator signs up → creates own doc.
k = 0.38 on activated users (2026-07-12). Cycle 9 days median. Bottleneck: invite acceptance 31%.

## Pricing
Free (3 projects) · Team 29 USD/seat/mo · Business 59 USD/seat/mo. Value metric: seats.
Paywall trigger: 4th project. Last change 2026-02, grandfathered pre-2026 accounts.

## Backlog
| Idea | Stage it targets | I | C | E | Notes |
|---|---|---|---|---|---|
| Seed sample project on signup | activation | 8 | 7 | 8 | shipped 2026-07-14, see experiments/2026.md |
| Invite prompt at first export | loop | 7 | 6 | 9 | needs event first |

## Targets
Q3: activation 22% → 28% (input target). Falsifier: no movement by 2026-08-20 → re-plan.
Top sensitivity input: paid CAC; break-even at 240 USD. Model: artifacts/growth-model-2026-q3.md.

## Pain Points
2026-03: two dashboards disagreed on "active" for six weeks; a quarter of decisions were argued not decided.
2026-05: cold outbound burned 14k USD before a kill number existed.

## How They Work
Solo founder plus one marketer. Wants the number and the decision, not the framework.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here.
- **`## Funnel`**: one row per **stage**, never per market or per segment. Every rate carries its denominator, window and as-of date (SKILL.md Rule 3). Re-measuring a stage **overwrites** its row; the previous value moves to `Prior`. Never two rows for the same stage — history belongs in `funnel-history.md` after the split.
- **`## Markets`** (marketplaces only, omitted otherwise): one row per market, columns `Market | Liquidity supply→demand | Liquidity demand→supply | Fill rate | Time to first transaction | Constrained side | Launched | As of`. Splits to `markets.md` with those exact columns.
- **`## Channels`**: killed channels stay, with the CAC that killed them and the date. A channel table that only shows survivors invites the same mistake next year. Amounts carry their currency.
- **`## Retention`**: one row per cohort, anchored on first touch, never re-anchored. State the period unit and the natural frequency under the table.
- **`## Constraint`**: one constraint at a time, with the date it was named and the date it expires. An expired constraint is re-derived, not assumed.
- These headings are exactly the ones the split-out files get, so the split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their business and their numbers |
| `complete` | Know the model, the constraint, and the channel portfolio well |

## experiments/

Append-only, one file per year, created with the first readout. Never a section of `memory.md`: a log grows without end and would force a split every quarter.

```markdown
# Experiments — 2026

## 2026-06-08 → 2026-07-13 · onboarding: seed sample project for new signups
Hypothesis: because 61% of churned users never created a project, seeding one will
            raise 7-day activation from 22% to ≥26%.
Design: 50/50, new signups only, primary = activated_7d, fixed horizon, guardrails
        = M1 retention, support volume. n = 16 × 0.22 × 0.78 ÷ 0.04² = 1,716 →
        1,800/arm planned; 29 days of intake at ~124 signups/day, plus 7 days for
        the last cohort's activation window.
Result: 22.1% → 25.4% (+3.3pp, +15% rel). SRM clean. Guardrails flat.
Decision: shipped 100% on 2026-07-14. Next: seed by use case.

## 2026-06-02 → 2026-06-16 · paid social: broad vs interest targeting
Result: no difference (CAC 305 vs 312, n below plan). Underpowered — recorded as
        inconclusive, not as "no effect".
Decision: not re-run until the surface has volume.
```

Losses and inconclusive results are the reason this file exists. Mark an underpowered test **inconclusive**, never "no effect" — the two lead to opposite decisions next year.

## artifacts/

One file per thing, at `~/Clawic/data/growth/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **tracking plan**, **metric definitions**, **growth model**, **activation spec**, **loop design**, **referral program**, **lifecycle map**, **pricing change**, **stall review**, **win/loss synthesis**, **channel post-mortem**, **market-launch playbook**, **contribution model**, **SKAN conversion values**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Metric definitions
*Read before quoting any rate. Updated 2026-07-26.*

Signup rate — signups ÷ unique visitors, 7d, cohort anchored on first touch,
excludes internal domains and known bots. Source: posthog. Owner: growth.
...one block per metric, plus the date any definition changed and the period
it was wrong for...
```

```markdown
# Growth model — 2026 Q3
*Read before any target, forecast or budget question. Built 2026-07-05.*

Inputs (with sources and as-of dates): ...
Scenarios: base / downside (CAC +30%, conversion −10%) / upside (SEO compounding)
Top sensitivity: paid CAC. Break-even 240 USD. Re-plan trigger written to ## Targets.
Rejected: doubling paid spend — payback fails the 2× test at 26k USD/mo.
```

If the work is tracked as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the detail staying here and referenced by name. Never duplicate the project record.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that touches people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Ana Ruiz | ana@northloop.io | agency — paid social | email | runs Meta account, 15% of spend | 2026-07-22 | — |
```

- **Identity is `Key`**: lowercase email, falling back to a handle, falling back to `<kebab-name>` plus a stable disambiguator. It is a **column of the row**, never implicit and never delegated to a per-person file. `Preferred channel` is the type of channel, not the address, so it cannot serve as a key.
- **Read the file before adding.** If the key is already there, update the row in place — never append a second row for the same person. Rows written by other skills are not yours: add missing detail, never rewrite their columns.
- **Retirement**: when a relationship ends, delete the row and note the date in `## Pain Points` or `## Channels` of `memory.md`, whichever it belonged to. A contact list that only grows stops being usable.
- **Scale cut**: one row per person while there are ≤15, or until one person no longer fits in a row. Past that, `~/Clawic/data/contacts/<name>.md` per person with the same fields, and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- No credentials, no private phone numbers pasted from a signature, no notes the person would be surprised to read.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every planning skill.

```markdown
# Q3 activation push
status: active — 2026-07-14
owner: growth
goal: activation 22% → 28% by 2026-09-30
decisions: seed sample project (shipped); use-case branching (next)
links: growth artifacts/activation-spec.md
```

- **Identity is the file name** (the project slug). Read the folder before creating: a project with a near-identical name is the same project under a different phrasing, and it gets updated, not duplicated.
- **Retirement**: `status: done | cancelled — <date>` inside the file; never delete it — it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Growth detail (the model, the spec) stays in `~/Clawic/data/growth/artifacts/` and is referenced by name here. Never duplicate it.

## Shared finances

Lives at `~/Clawic/data/finances/`, shared with every money skill.

```markdown
# Budget

| Item | Amount | Period | Owner | Notes |
|------|--------|--------|-------|-------|
| Paid social test | 2500 USD | month, 2026-07 to 2026-09 | growth | kill number CAC > 240 USD |
| Non-brand search | 9000 USD | month, ongoing | growth | scaling while payback ≤ 9 mo |
```

- **Identity is the item name** within its period. Read before adding; if the item exists for that period, update the row in place.
- **Amounts carry their currency inside the value** (`2500 USD`, not `$2500`) and estimates carry their estimation date — the file is shared with skills using other currencies and someone will add the column up.
- **Retirement**: when a budget line ends, delete the row and record the final spend and outcome in `## Channels` of the growth `memory.md`.
- Growth-tool costs (analytics, ESP, experiment platform) are rows in `subscriptions.md`, not `budget.md`: one row per subscription, kept small because cancelling deletes the row.
- **Foreign columns win**, same rule as contacts. Never rewrite a header another skill wrote.
- References to payment accounts are pointers only, never card numbers or credentials.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`channels.md` — the channel table plus `## Killed`, which is the reason the file exists: without it, a channel gets retried every eighteen months by whoever is new.

`retention-curves.md` — the cohort table plus `## Notes` for the natural frequency, the period unit, and any definition change with the date it took effect.

`funnel-history.md` — one section per stage, each a period-by-period table, so a trend can be read without re-querying. Keeps the stage names exactly as they appear in `## Funnel`.

`backlog.md` — the scored idea table plus `## Shelved`, with the reason and the condition that would revive each idea.

`markets.md` — the `## Markets` table with its exact columns (`Market | Liquidity supply→demand | Liquidity demand→supply | Fill rate | Time to first transaction | Constrained side | Launched | As of`), for marketplaces once there are more than a handful.
