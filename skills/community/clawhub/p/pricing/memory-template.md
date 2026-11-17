# Working File Templates — Pricing

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md`, `price-book.md` and everything the index points at is what you **observed** or produced. An observation never overwrites a declaration.

**Contents:** [Where each thing goes](#where-each-thing-goes) · [When to write](#when-to-write) · [Start flat, split](#start-flat-split-only-when-it-hurts) · [Secrets](#secrets) · [config.yaml](#configyaml) · [memory.md](#memorymd) · [price-book.md](#price-bookmd) · [artifacts/](#artifacts) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [split-out files](#split-out-files)

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/pricing/config.yaml` | Key by key, read-modify-write |
| What they sell, cost inputs, competitors, price history, tests, deals, research runs, due dates, box index | `~/Clawic/data/pricing/memory.md` | Rewritten in place; stays small |
| **The current price book** — plans, value metric, what each tier gates, effective date | `~/Clawic/data/pricing/price-book.md` | Its own file from the first product; one block per plan or SKU |
| Competitor prices, each with the date it was observed | `## Competitors` in `memory.md`; `~/Clawic/data/pricing/competitors.md` once it outgrows the section | One row per competitor plan |
| Price changes shipped, and grandfathered cohorts with their expiry | `## Price History` in `memory.md`; `~/Clawic/data/pricing/price-history.md` once it outgrows the section | One row per change |
| Price tests: what was tested, on whom, what it decided | `## Experiments` in `memory.md`; `~/Clawic/data/pricing/experiments.md` once it outgrows the section | One row per test |
| Non-standard deals: discount, term, floor, what was traded, who approved | `## Deals` in `memory.md`; `~/Clawic/data/pricing/deals.md` once it outgrows the section | One row per deal; the customer itself goes to `contacts/` |
| Willingness-to-pay runs: method, n, date, resulting range | `## Research` in `memory.md`; `~/Clawic/data/pricing/wtp-studies.md` once it outgrows the section | One row per study; the full write-up goes to `artifacts/` |
| Things you produced that get re-read whole — discount policy, price-change plan, packaging or value-metric decision with what was rejected, value-quantification model, WTP study write-up, a rate card sent to a client, a pricing page that converted, a competitor teardown, a jurisdiction compliance check or a competition-law incident with its date and source (`artifacts/compliance-<market>.md`) | `~/Clawic/data/pricing/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Customers, prospects, and interviewees named anywhere above | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill writing into one file |
| A repricing run as a piece of work: goal, status, milestones, decisions | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project, from the first |
| **Anything durable this table does not name** | `~/Clawic/data/pricing/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, a project, a subscription, an invoice? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a policy, a plan, a decision with its reasoning, a model, a report? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A price was set, changed, or repackaged | The plan block in `price-book.md`, and a row in `## Price History` |
| A cohort was grandfathered | `## Price History`, with the expiry date, and a `## Due` row for that date |
| A discount was granted outside `discount_floor_pct` | `## Deals` — depth, term, what was traded back, who approved |
| A competitor's price was observed | `## Competitors`, with the date seen and where it was seen |
| A willingness-to-pay study ran | `## Research` for the row; `artifacts/` for the curves, the questions, and the write-up |
| A price test started, ended, or was abandoned | `## Experiments`, including tests that were stopped and why |
| Churn or revenue was read 30/60/90 days after a change | The same `## Price History` row, in its outcome column |
| A value-metric, packaging, or grandfathering decision was made | `artifacts/`, with what was rejected and the condition that would revisit it |
| A cost, margin, or fee input took work to establish | `## Cost Inputs` |
| Unbilled work was given away — extra scope, an unpaid round, a favour | `## Deals`, with the days or amount it cost and `Traded for: nothing` |
| A jurisdiction rule was verified, or a Legal Tripwire fired | `artifacts/compliance-<market>.md` — the date, the source, and for a tripwire the message, who was present, and that counsel was told |
| A customer, prospect, or interviewee was named | `~/Clawic/data/contacts/contacts.md` (shared), referenced from here by name only |
| The repricing is being tracked as a project | `~/Clawic/data/projects/<project>.md` (shared) |
| A review, sweep, audit, or checkpoint was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except `price-book.md`, artifacts, and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/pricing/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

`price-book.md` and artifacts are the exception: the price book is read on almost every activation and a decision is read whole when its subject comes up, so both are born as their own file whatever their size.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A pasted contract, billing export, admin screenshot, or coupon list is the densest source there is: strip each value **before** writing and leave its pointer in place, in this shape: `<kind>:<locator>`.

`env:STRIPE_SECRET_KEY` · `keychain:paddle-admin` · `1password:Work/Billing/live` · `bitwarden:Finance/Chargebee` · `vault:secret/billing/api` · `ssm:/prod/billing/webhook-secret` · `file:~/.config/billing/credentials`

In a text, the pointer goes where the value was: `webhook_secret: <env:STRIPE_WEBHOOK_SECRET>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: list prices and discount percentages, plan and SKU names, currencies, contract terms and end dates, renewal and notice dates, margins and unit costs, MRR/ARR figures, take rates, competitor prices, customer and company names, VAT and company registration numbers, public promo codes, the last four digits of a card.

**Secrets, strip them**: payment-processor API keys and webhook signing secrets, billing-platform admin passwords and session tokens, unpublished coupon or promo codes that grant a discount to whoever holds them, full card numbers and full bank account or IBAN details, customer payment tokens, tax-portal logins, and any credential inside a pasted export.

Confidential is not the same as secret: a competitor's contract price obtained under NDA is data, and it gets stored with its source restriction noted in the row (`source: under NDA — not for external use`) rather than deleted.

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/pricing/` if it does not exist.

```yaml
business_model: saas-subscription
currency: EUR
target_gross_margin_pct: 82
discount_floor_pct: 15
annual_discount_pct: 17
grandfather_policy: fixed-term
price_endings: charm
tax_display: inclusive
price_review_cadence: half

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  billing_platform: paddle        # merchant of record — it owns VAT collection
  survey_tool: typeform
conventions:
  tier_names: [Starter, Team, Business, Enterprise]
  seat_word: editor
platform:
  markets: [EU, UK, US]
  ppp_bands: true
risk_posture:
  live_price_tests: geo-only
  floor_is_absolute: true
cadence:
  competitor_sweep: quarter
  discount_audit: quarter
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Pricing Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Current price book (4 plans) → `price-book.md`; read before quoting, discounting or changing any price
- Discount policy and approval ladder → `artifacts/discount-policy.md`; read before approving anything past 15%
- Seat-to-usage decision, with what was rejected → `artifacts/decision-value-metric.md`; read before repackaging
- 2026 Team-tier raise plan → `artifacts/plan-team-raise-2026.md`; read while the migration is still running
- Van Westendorp study, Sept 2026 → `artifacts/wtp-study-2026-09.md`; read before any change to Starter or Team
- Competitor plans (11) → `competitors.md`; read before a positioning claim or a match request

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Full price review | half | 2026-03-02 | 2026-09-02 |
| Competitor sweep | quarter | 2026-07-01 | 2026-10-01 |
| Discount audit (realized vs policy) | quarter | 2026-07-05 | 2026-10-05 |
| Team raise: 90-day churn read | once, 2026-11-01 | — | 2026-11-01 |
| Legacy Starter cohort expires | once, 2027-01-01 | — | 2027-01-01 |

## Offering
B2B SaaS, self-serve plus a sales-led top tier. Value metric: editors. Sells in EUR to EU/UK, USD to US.

## Cost Inputs
| Input | Value | As of | Source |
|-------|-------|-------|--------|
| Variable cost per editor per month | 3.10 EUR | 2026-06 | infra + support allocation |
| Payment fees, blended | 2.6% + 0.25 EUR | 2026-06 | Paddle statement |
| Target gross margin | 82% | 2026-01 | declared, see config.yaml |

## Competitors
| Competitor | Plan | Price | Metric | Observed | Where |
|---|---|---|---|---|---|
| Acme | Team | 29 USD/user/mo | seat | 2026-07-01 | public pricing page |
| Borealis | Growth | 490 USD/mo flat | flat, 20 seats incl. | 2026-07-01 | public pricing page |

## Price History
| Date | What changed | From | To | Cohorts | Grandfather until | Outcome at 30/60/90d |
|---|---|---|---|---|---|---|
| 2026-08-01 | Team list price | 39 EUR | 45 EUR | new logos only | n/a | churn +0.2pp, ARPU +13% at 90d |
| 2026-09-15 | Team, existing customers | 39 EUR | 45 EUR | monthly cohort, 45-day notice | 2027-01-01 | pending |

## Experiments
| Started | Ended | What was tested | Split | Read on | Result | Decision |
|---|---|---|---|---|---|---|
| 2026-05-04 | 2026-06-15 | Starter 15 vs 19 EUR | new traffic, EU only | RPV + 90d churn | RPV +11% at 19, churn flat | adopted 19 |

## Deals
| Date | Customer | List | Agreed | Discount | Traded for | Term | Approved by |
|---|---|---|---|---|---|---|---|
| 2026-06-20 | Northwind (see contacts) | 12,000 EUR/yr | 9,600 EUR/yr | 20% | 2-year term, prepaid, logo rights | 24 mo | founder |

## Research
| Date | Method | n | Segment | Result | Write-up |
|---|---|---|---|---|---|
| 2026-09-10 | Van Westendorp | 214 | EU, 10-50 employees | acceptable range 34-58 EUR, OPP 44 | `artifacts/wtp-study-2026-09.md` |

## Pain Points
2025: raised Starter 60% overnight with no notice; visible backlash and 9% churn in that cohort. Notice period is now non-negotiable.

## How They Work
Wants the number and the break-even, not the framework. Will not discount below 15% under any argument.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. One-off dates belong here too: a grandfather expiry and a 90-day churn read are the two that get forgotten most.
- **`## Cost Inputs`**: `As of` is mandatory. Margin maths run against a stale unit cost is the quiet way a floor stops being a floor.
- **`## Competitors`**: `Observed` is the date you saw it, and prices without one are unusable within a quarter. Record the metric alongside the price — 29 per seat and 490 flat are not comparable until seats are named.
- **`## Price History`**: one row per change, and the outcome column gets filled in later, not left blank forever. `Grandfather until` is a date or `n/a`; the word "indefinitely" belongs nowhere in this column (SKILL.md Rule 7).
- **`## Experiments`**: record abandoned tests too — the reason a test was stopped is the finding most likely to be repeated.
- **`## Deals`**: `Traded for` is the column that makes the discount policy real; a row with an empty one is a price cut being recorded as a negotiation. Unbilled scope given away lands here too, with `Traded for: nothing` — that is what makes the annual total visible (`services.md`).
- **All amounts carry their currency in the value** (`45 EUR`), because rows from other markets sit next to them.
- These headings are exactly the ones `competitors.md`, `price-history.md`, `experiments.md`, `deals.md` and `wtp-studies.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning what they sell and to whom |
| `complete` | Know the offering, the cost base, and the buyer well |

## price-book.md

The answer to "what do we charge", read before quoting, discounting, or changing anything. Created the first time a price exists; one block per plan or SKU.

```markdown
# Price Book
*Effective 2026-09-15. Currency EUR, prices shown incl. VAT for consumers, excl. VAT for business.*

Value metric: **editors** (users who can create or edit). Viewers are free and uncounted.

## Starter — 19 EUR / editor / month
Annual: 190 EUR / editor / year (2 months free, 16.7%)
Includes: 3 editors max, 5 GB, community support
Fences: no SSO, no audit log, 30-day history

## Team — 45 EUR / editor / month
Annual: 450 EUR / editor / year
Includes: unlimited editors, 100 GB, email support, 1-year history
Fences: no SSO, no SLA

## Business — 79 EUR / editor / month
Includes: SSO/SAML, audit log, 99.9% SLA, priority support

## Enterprise — quoted
Floor: 25,000 EUR / year. Uplift clause 5%/yr. Approval past 15% discount: founder.

## Legacy
- Starter 15 EUR (pre-2026-06 cohort) — grandfathered until 2027-01-01
```

- Every plan states its value metric, what is included, and the fence that separates it from the tier above.
- The header line carries currency, tax treatment, and effective date (SKILL.md Rule 6). A price book with no effective date cannot be compared to the invoice a customer is holding.
- Legacy plans live at the bottom with their expiry, and disappear from the file on the day the last cohort migrates — the removal is recorded in `## Price History`.
- Floors and approval thresholds live here too, so the number and the limit on the number are never in separate files.

## artifacts/

One file per thing, at `~/Clawic/data/pricing/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a discount policy**, **a price-change plan**, **a packaging or value-metric decision**, **a willingness-to-pay study write-up**, **a value-quantification model**, **a rate card sent to a client**, **a competitor teardown**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Decision — editors, not seats or usage
*Read before any repackaging, and before quoting a customer with many read-only users. 2026-07-26.*

Decision: charge per editor; viewers free and uncounted.
Why: value tracks people who produce, and buyers can count editors without our dashboard (SKILL.md Rule 1).
Rejected: total seats — killed the largest accounts, where 80% of users only read.
Rejected: API calls — value did not track calls, and the bill was unforecastable for the buyer.
Revisit when: read-only usage starts carrying its own infrastructure cost, or a competitor prices on outcomes.
```

```markdown
# Plan — Team raise, 39 → 45 EUR
*Read while the migration is running. Written 2026-08-20.*

Break-even (SKILL.md Rule 2): +15.4% price at 82% margin tolerates 15.8% volume loss.
Churn budget: 8% of the monthly cohort. Stop and reverse above that.
Sequence: new logos 2026-08-01 → renewals 2026-09-15 → monthly cohort on 45 days' notice.
Grandfathered: pre-2026-06 Starter cohort until 2027-01-01 (in `## Due`).
Comms: what changed, why, the date, and what stays the same. No countdown, no apology.
Checkpoints: churn and ARPU at 30/60/90 days, written into the `## Price History` row.
```

If the user tracks this work as a project, the one-line decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the full artifact staying here and referenced by name.

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that knows people — the user may have none of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Ana Ruiz | ana.ruiz@northwind.example | procurement lead, Northwind | email | 24-month deal at 20% off, prepaid | 2026-06-20 | — |
```

- **Identity is the `Key` column**: lowercase email, else the handle, else `<kebab-name>` plus a stable disambiguator. It is a real column in the row, never implicit and never delegated to a per-person file. `Preferred channel` is the *type* of channel, not the address, so it can never serve as the key.
- **Read the file before adding.** If the key is already present, update that row in place; only its absence justifies a new row. Never rewrite or delete a row this skill did not write.
- **Retirement**: when a relationship ends, delete the row and note the date in `## Deals` here. An index that only grows stops being an index.
- **Scale cut**: rows while there are ≤15 people, or until one no longer fits on its line. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If the folder already looks like that when you arrive, follow it — never start a parallel `contacts.md`.
- **Foreign columns win.** If the file already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Pricing keeps the deal in its own `## Deals` row and references the person by name only. Never duplicate the person here.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project from the first, shared with every skill that tracks work.

```markdown
# Project — 2026 repricing

status: active
Goal: move Team from 39 to 45 EUR without exceeding 8% cohort churn.
Milestones: new logos (done 2026-08-01) · renewals (2026-09-15) · monthly cohort (2026-09-15, 45 days' notice)
Decisions: per-editor metric kept (`pricing/artifacts/decision-value-metric.md`)
People: Ana Ruiz (see contacts)
```

- Identity is the project name, which is the filename. Read before creating: a repricing already tracked by another skill gets updated, not duplicated.
- Closing is `status: done | cancelled — <date>` inside the file, never deletion: the file is the record of what was shipped. Past roughly 20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- Amounts carry their currency. Long artifacts stay in `pricing/artifacts/` and are referenced here by path, never pasted in.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`competitors.md` — `## Competitors`, plus a `## Positioning Notes` heading once claims start depending on the table. This is the file that stops the same competitor page being re-read every month with no record of what changed.

`price-history.md` — `## Price History`, plus `## Grandfathered Cohorts` (cohort, plan, price held, expiry, count). The outcome columns are the reason this file exists: without them, the third raise is argued with the same assumptions as the first.

`experiments.md` — `## Experiments`, plus `## Abandoned` for tests stopped before a read, with the reason.

`deals.md` — `## Deals`, plus `## Floor Exceptions` for anything below the price-book floor, with who approved it and under what argument.

`wtp-studies.md` — `## Research`, one `## <method>` heading per method once more than one is in use. Rows point at the full write-up in `artifacts/`; raw responses are never pasted here.
