# Instrumentation — Definitions, Events, and Numbers You Can Defend

Most growth arguments are definition arguments in disguise. This file makes a number reproducible: what it counts, over what window, from which event, stitched to which identity. Written against `analytics_stack`; the shapes below are tool-independent.

**Contents:** [Definition Before Metric](#definition-before-metric) · [The Tracking Plan](#the-tracking-plan) · [Naming](#naming) · [Client, Server, or Both](#client-server-or-both) · [Identity Stitching](#identity-stitching) · [The North Star and Its Tree](#the-north-star-and-its-tree) · [Data Hygiene Checks](#data-hygiene-checks) · [Privacy and Consent](#privacy-and-consent) · [Dashboards People Actually Read](#dashboards-people-actually-read) · [Traps](#traps)

**Before quoting or building any metric**, read `## Metric Definitions` in `~/Clawic/data/growth/memory.md` and open `artifacts/metric-definitions.md` if `## Boxes` lists it. Re-deriving a definition that already exists is how two versions of "active user" end up in the same deck.

## Definition Before Metric

Every metric needs five fields written down. Missing any one of them makes two honest people compute different numbers:

| Field | Example | Failure if unset |
|---|---|---|
| Event or source | `subscription_started` from the billing webhook | Client-side signups counted before payment clears |
| Denominator | Unique visitors, deduplicated by anonymous id | Sessions counted as people; rate falls when engagement rises |
| Window | 7 days from first touch | Comparisons between a 7-day and a 30-day version of the same rate |
| Cohort anchor | Date of first touch, fixed forever | History rewrites itself as users convert |
| Exclusions | Internal users, bots, test accounts, refunded orders | Small businesses inflate their own numbers by 5-20% with staff traffic |

Write these once, in `artifacts/metric-definitions.md`, and reference them rather than restating. A metric changed later gets a **new name**, not a redefinition — silently redefining breaks every historical comparison and nobody notices for a quarter.

## The Tracking Plan

A spreadsheet-shaped document, one row per event, agreed before code:

| Event | When it fires | Properties | Source | Owner | In which metric |
|---|---|---|---|---|---|
| `signup_completed` | Account row created | `plan`, `source`, `referrer_id`, `invite_id` | server | backend | Signup rate, cohort anchor |
| `project_created` | First save persists | `template`, `seconds_since_signup` | server | backend | Activation (aha), `activation.md` |
| `paywall_viewed` | Modal rendered | `trigger`, `limit_hit`, `plan_shown` | client | web | Paywall conversion, `monetization.md` |
| `subscription_started` | Billing webhook confirms | `plan`, `mrr`, `currency`, `trial` | server | billing | Paid conversion, MRR |

Rules that keep it usable:

- **Fewer events, more properties.** `button_clicked` with a `name` property beats forty named click events; the property is filterable, the event name is not.
- **Instrument the *state change*, not the UI.** `project_created` survives three redesigns; `clicked_new_project_button_v2` does not.
- **Ship the event in the same pull request as the feature** (SKILL.md Rule 9). Retroactive events cannot backfill, and the first cohort is the one you needed.
- **Every event names the metric it feeds.** An event feeding nothing is cost: storage, plan noise, and a false sense of coverage.

## Naming

Pick one convention and enforce it mechanically; the convention matters less than its uniformity.

- `object_action`, snake_case, past tense: `invite_sent`, `subscription_cancelled`. Sorting the event list then groups by object, which is how anyone actually browses it.
- Properties are snake_case nouns with units in the name: `revenue_usd`, `duration_seconds`, `seconds_since_signup`. A number without a unit in its name gets summed with a different unit within a year.
- Reserve a prefix for internal/QA traffic and exclude it in the tool's default view, not in each query.
- Campaign and UTM taxonomy: lowercase, no spaces, `utm_source` = platform, `utm_medium` = channel type, `utm_campaign` = campaign slug that matches the row in `## Channels`. Mixed case creates two rows for the same campaign in every report.

## Client, Server, or Both

| Event type | Where | Why |
|---|---|---|
| Money — subscription, order, refund, chargeback | Server, from the billing system | Ad blockers, closed tabs, and network drops make client-side revenue undercount, and it is the number nobody may get wrong |
| State changes — signup, item created, invite sent | Server | Reliable, and independent of the front end |
| Intent and UI — page view, modal shown, scroll, hover | Client | The server never sees them |
| Attribution parameters | Client at capture, persisted server-side on signup | The click id must survive the session that captured it |

Client-side loss to blockers and tracking prevention is real and varies with audience — a developer-tool audience blocks far more than a consumer one. Never compute a rate whose numerator is server-side and denominator client-side without saying so: the ratio will read high and nobody will find out why.

## Identity Stitching

Three ids, one chain:

1. **Anonymous id** — set on first visit, persisted. Cross-domain and cross-device it does not survive; browser storage caps mean it can expire in days on some browsers.
2. **User id** — assigned at signup. On signup, alias the anonymous id to it so pre-signup touches attach to the person.
3. **Account/org id** — for B2B, every event carries it; per-user metrics are meaningless when the buyer, the admin, and the user are three people (`b2b.md`).

Failure to alias is the single most common reason a funnel loses its top: signups appear with no acquisition source and get bucketed as "direct".

## The North Star and Its Tree

The north star measures **value delivered**, not money collected, and moves ahead of revenue.

| Model | Reasonable north star | Not this |
|---|---|---|
| SaaS collaboration | Weekly active teams with ≥3 members editing | Signups |
| Marketplace | Completed transactions | Listings |
| Media | Weekly hours of content consumed by returning readers | Pageviews |
| Ecommerce | Repeat purchases per active customer per quarter | Sessions |
| Dev tool | Weekly projects deployed | GitHub stars |

Its tree has one level: three input metrics that multiply to it, each with one owner. Below that is the team's own backlog, not the company scoreboard. Test the candidate before adopting it: does it rise only when a user got value, can each team move it, and does it lead revenue by at least one reporting period? If it fails any of the three, it is a dashboard tile, not a north star.

## Data Hygiene Checks

Run at the `reporting_cadence`; each has produced a fake crisis or a fake win.

- **Volume anomaly**: any event ±30% week over week with no release — usually a broken tag, not a market shift.
- **Duplicate events**: same user, same event, sub-second apart. A double-fired signup inflates the top of the funnel and deflates every rate below it.
- **Null property rate**: a property whose null rate crosses ~5% has an unshipped path or a rename.
- **Bot and internal traffic**: excluded by rule, verified quarterly; office IPs and staging domains drift.
- **Timezone**: one timezone for everything, stated on the dashboard. Mixed UTC and local timezones make Monday spikes appear.
- **Attribution nulls**: the share of signups with no source; rising nulls means the alias step broke.

## Privacy and Consent

Under `privacy_regime` = gdpr or both: consent precedes non-essential tracking, and consent-mode implementations mean part of the funnel is modelled, not measured — label modelled numbers as such in any comparison. Personal data is minimised by design: hash or drop emails in analytics properties, keep the join key in the warehouse the user controls.

Retention of raw event data is a decision with a cost; pick a window and state it. And never write a user-level export into `~/Clawic/data/` — the aggregate is the memory, the rows belong in the user's own systems (SKILL.md Data).

## Dashboards People Actually Read

One screen, in this order: north star with its trend, the equation's stages with current versus prior period, the channel table, active experiments. Everything else is a link. Two disciplines keep it alive: every tile carries its definition on hover or in a footnote, and any tile nobody has looked at in a quarter gets deleted — an unread tile is not free, it is the thing people scroll past on the way to the number they trust.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Redefining a metric in place | Every historical comparison silently breaks | New name, new definition, both documented with the change date |
| Tracking everything "so we have it later" | Plan noise, cost, and nobody knows which event is authoritative | Events that feed a named metric; delete the rest |
| Counting revenue client-side | Blocked scripts and abandoned tabs undercount money | Billing webhook, server-side |
| Sessions used as the denominator for a person-level rate | Engagement improvements make conversion look worse | Unique users, deduplicated by the stitched id |
| Comparing month-to-date to a closed month | Always reads as collapse mid-month | Like windows, both with as-of dates |
| One dashboard per team, each with its own "active user" | Meetings become metric archaeology | One definition file, referenced everywhere |

**After agreeing any definition, shipping a tracking plan, or fixing a measurement bug**, write it back in the same turn: the definition row into `## Metric Definitions` in `~/Clawic/data/growth/memory.md`, the full plan into `~/Clawic/data/growth/artifacts/tracking-plan.md`, and the definitions document into `artifacts/metric-definitions.md`, each with its `## Boxes` line and its read condition (`memory-template.md`). If a metric was found to be wrong, record the period it was wrong for next to it — otherwise the corrected number gets compared against the bad history forever.
