# Working File Templates — Money

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/money/config.yaml` | Key by key, read-modify-write |
| Situation, money shape, payoff order, goals, allocation, net worth, due dates, box index | `~/Clawic/data/money/memory.md` | Rewritten in place; stays small |
| Every account held with an institution — current, savings, brokerage, pension, card, loan, mortgage | `~/Clawic/data/finances/accounts.md` (**shared**) | One row per account, every institution in one inventory |
| Recurring payments and their renewal dates | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per subscription |
| The monthly plan: categories, planned amounts, sinking funds | `~/Clawic/data/finances/budget.md` (**shared**) | Rewritten in place, one plan at a time |
| An adviser, accountant, broker, lender contact or executor | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person; named here by name only |
| The one-line money summary of something the user runs as a project | `~/Clawic/data/projects/<project-kebab>.md` (**shared**) | One line under `## Money` in an existing project file; the analysis stays in `artifacts/` |
| Things you produced that get re-read — payoff plan, investment policy, rent-versus-buy analysis, coverage map, claim log, estate checklist, income-shock playbook, tax-prep checklist | `~/Clawic/data/money/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| Decisions taken, with the amount, the reason and what was rejected | `~/Clawic/data/money/decisions/<year>.md` | Append-only, cut by year |
| **Anything durable this table does not name** | `~/Clawic/data/money/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| An account, rate, balance or credit limit was learned or changed | Its row in `finances/accounts.md` |
| A payoff order was agreed, or a balance crossed a milestone | `## Debt Plan` |
| The buffer target or its current level moved | `## Goals` (emergency fund is a goal like any other) |
| Income, core spending or savings rate was established or changed | `## Money Shape` |
| A budget was built or revised, a sinking fund added | `finances/budget.md` |
| A recurring payment was found, cancelled or repriced | `finances/subscriptions.md` |
| A target allocation or rebalancing band was set | `## Allocation` |
| A net-worth reading was taken | `## Net Worth` |
| A decision was taken — buy, rent, refinance, cover level, accept an offer, decline a product | `decisions/<year>.md`; the analysis behind it goes to `artifacts/` |
| A payoff plan, investment policy, coverage map, estate checklist, shock playbook or tax-prep list came out of the session | `artifacts/` |
| A named adviser, accountant, broker or executor entered the picture | `contacts/contacts.md`, referenced from here by name |
| A shock, a windfall, a job change, a household change | `## Situation`, plus `decisions/<year>.md` if money moved |
| A review ran, or a recurring check was scheduled | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, decision records and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/money/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move — `### X` inside `memory.md` becomes `## X` in the extracted file, same words — so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a payoff plan or a rent-versus-buy analysis is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. A statement, a policy schedule or a tax return pasted for analysis is exactly where secrets hide. Store the pointer in place of the value, in this shape: `<kind>:<locator>`.

`keychain:bank-login` · `1password:Personal/Broker` · `bitwarden:Cards/Visa` · `vault:finance/portal` · `env:BROKER_API_KEY` · `file:~/Documents/tax-2025.pdf` (the path, never the contents)

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `login: <keychain:bank-login>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: institution names, account nicknames and types, the last four digits, interest rates and APRs, credit limits, balances with their currency and date, employer and job title, ticker symbols and fund categories, insurer name and policy type, deductible and cover amounts, tax year, filing status, an adviser's name and fee structure.

**Secrets, strip them**: full account numbers, IBAN, sort code plus account number together, card PAN, expiry and CVV, PINs, online banking usernames and passwords, one-time-code seeds and recovery codes, brokerage or bank API keys, national insurance / social security / tax identification numbers, passport and ID numbers, full date of birth paired with mother's maiden name or any other knowledge-based answer, seed phrases and private keys, full policy and claim numbers, and any link that logs in without a password.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared accounts inventory](#shared-accounts-inventory) · [shared subscriptions](#shared-subscriptions) · [shared budget](#shared-budget) · [shared contacts](#shared-contacts) · [artifacts/](#artifacts) · [decisions/](#decisions) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/money/` if it does not exist.

```yaml
currency: EUR
country: ES
emergency_fund_months: 9
high_interest_rate_pct: 7
savings_rate_target_pct: 25
risk_posture: balanced
household: couple
review_day: 5
exclusions: [leverage, crypto]

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  budget_month_start: 25        # payday, not the 1st
  fiscal_year_end: "12-31"
advice_order: [retirement, mortgage_freedom, education]
institutions:
  broker: "the one already in use — name only, never a login"
output_format:
  show_math: true
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Money Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Net-worth snapshots (14 quarters) → `net-worth.md`; read before any "are we on track" question
- Payoff plan, cards + car loan → `artifacts/payoff-plan.md`; read whenever a debt payment or a windfall comes up
- Investment policy → `artifacts/investment-policy.md`; read before any allocation change or market-timing question
- Rent-versus-buy, Malasaña 2026 → `artifacts/decision-rent-vs-buy.md`; read if buying comes up again before 2028
- Coverage map → `artifacts/coverage-map.md`; read at the annual insurance review or after any life change
- Decisions 2026 → `decisions/2026.md`; read before revisiting a decision already taken this year

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Cashflow review | month, day 5 | 2026-07-05 | 2026-08-05 |
| Net-worth snapshot | quarter | 2026-06-30 | 2026-09-30 |
| Rebalance check (5pp bands) | quarter | 2026-06-30 | 2026-09-30 |
| Insurance + beneficiary review | year, October | 2025-10-12 | 2026-10-12 |
| Credit report pull | year, March | 2026-03-04 | 2027-03-04 |
| Subscription audit | year, January | 2026-01-08 | 2027-01-08 |

## Situation
Couple, two incomes, one dependant. Tax residency ES. One salaried, one freelance since 2025-09 (see `## Money Shape`).

## Money Shape
| Figure | Amount | As of |
|--------|--------|-------|
| Gross household income | 84,000 EUR/yr | 2026-07 |
| Core monthly spend | 2,450 EUR | 2026-07 |
| Total monthly spend | 3,100 EUR | 2026-07 |
| Savings rate | 21% of gross | 2026-07 |

## Debt Plan
### Order
| # | Debt | Rate | Balance | Monthly | Cleared by |
|---|------|------|---------|---------|------------|
| 1 | Visa | 21.9% | 3,400 EUR | 600 EUR | 2027-01 |
| 2 | Car loan | 6.4% | 8,900 EUR | 210 EUR | 2030-03 |
Method: avalanche. Mortgage at 2.1% is below `high_interest_rate_pct` — deliberately not prepaid.

### Progress
| Date | Event | Balance after |
|------|-------|---------------|
| 2026-06-30 | Visa rate reduced 24.9% → 21.9% after a retention call | 3,900 EUR |

## Goals
### Active
| Goal | Target | Current | Date | Monthly needed |
|------|--------|---------|------|----------------|
| Emergency fund (9 months core) | 22,050 EUR | 9,800 EUR | 2028-06 | 525 EUR |
| Deposit | 60,000 EUR | 12,000 EUR | 2030-01 | 1,100 EUR |

## Allocation
Target 70/30 equity/bonds, `risk_posture: balanced`. Rebalance at 5pp bands, checked quarterly. Last drift check 2026-06-30: 73/27, inside band.

## Net Worth
### Snapshots
| Date | Assets | Liabilities | Net | Note |
|------|--------|-------------|-----|------|
| 2026-03-31 | 96,400 EUR | 71,200 EUR | 25,200 EUR | — |
| 2026-06-30 | 101,900 EUR | 69,100 EUR | 32,800 EUR | bonus landed |

## Pain Points
2021: lost 4,000 EUR to a "guaranteed" FX scheme. Will not discuss anything with a return promise attached.

## How They Work
Wants the number and the order, not the theory. Show the arithmetic; one recommendation, not five options.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every recurring thing this skill schedules belongs here, and `review_day` sets the monthly one.
- **Every amount carries its currency and an `As of` date.** A balance with no date is unusable within a quarter, and a figure with no currency is unusable the moment a second currency appears.
- **`## Money Shape`**: core spend and total spend are different numbers and both are needed — the buffer is sized on core, the savings rate on total. Overwrite the rows; never append a second copy of the same figure.
- **`## Debt Plan`** holds the *strategy*: order, method, which debts are deliberately not being paid early, and why. The debts themselves are accounts and live in `finances/accounts.md` — one balance, one home.
- **`## Net Worth`**: one snapshot per reading date, never two for the same date. Assets and liabilities are totals; the account-level detail is already in `finances/accounts.md`.
- Headings marked `###` above are exactly the ones the extracted file gets, promoted one level, so a split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their situation |
| `complete` | Know their accounts, rates, goals and constraints |

## Shared accounts inventory

Lives at `~/Clawic/data/finances/accounts.md` and is shared with every other money skill — the user may have none of them installed, so the format travels with this skill.

```markdown
# Accounts

| Name | Institution | Type | Purpose | Rate | Balance | As of | Access reference |
|------|-------------|------|---------|------|---------|-------|------------------|
| Joint current | Banco X | current | bills and direct debits | 0% | 2,100 EUR | 2026-07-26 | keychain:bancox-joint |
| Buffer | Banco Y | savings | emergency fund | 2.4% AER | 9,800 EUR | 2026-07-26 | keychain:bancoy |
| Visa | Banco X | credit card | — | 21.9% APR | -3,400 EUR | 2026-07-26 | keychain:bancox-card |
| Mortgage | Banco Z | mortgage | home | 2.1% fixed to 2033 | -58,000 EUR | 2026-07-26 | file:~/Documents/mortgage.pdf |
```

- **Identity is `Name`.** Read the file before adding and look for that name. If it is already there, update the row in place — it is yours. Rows written by another skill are read-only: never rewrite one, only add what is missing.
- **Debts are accounts.** A card, a loan or a mortgage is a row here with a negative balance and its rate, so that the payoff order in `memory.md` and the inventory never disagree about a number.
- **Amounts carry their currency in the value** (`9,800 EUR`), because a second currency always shows up and someone will add the column.
- **`As of` is mandatory.** A balance with no reading date cannot be compared, and a stale one silently poisons a net-worth snapshot.
- **Closure is part of the inventory.** When an account is closed or a debt cleared, delete the row and note the date in `memory.md`. An inventory that only grows stops being an inventory.
- **Scale cut**: one row per account while there are ≤15. Past that, split by institution into `~/Clawic/data/finances/<institution-kebab>.md` with the same columns, and `accounts.md` becomes the index (`Name | Institution | Type | → file`). If you arrive and the folder already looks like that, follow it — never start a parallel `accounts.md`.
- **Foreign columns win.** If the file already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Access reference is a pointer only, never a number, login or password.

## Shared subscriptions

`~/Clawic/data/finances/subscriptions.md`. Identity is `Name`; update in place, delete the row when it is cancelled and note the date and the saving in `memory.md`.

```markdown
# Subscriptions

| Name | Provider | Amount | Cycle | Next charge | Paid from | Status | Cancel by |
|------|----------|--------|-------|-------------|-----------|--------|-----------|
| Cloud storage | Provider A | 9.99 EUR | monthly | 2026-08-03 | Visa | keep | — |
| Gym | Provider B | 480 EUR | yearly | 2026-11-01 | Joint current | review | 2026-10-01 |
```

Annual items carry `Cancel by` — the date the notice period starts, not the renewal date, because that is the date that can still be acted on. Amounts always with currency; convert nothing, compare at the review. **Foreign columns win**: if a `subscriptions` or tracker skill already wrote the file with other columns, match its header and add anything missing as a trailing note rather than rewriting it.

## Shared budget

`~/Clawic/data/finances/budget.md`. One plan at a time, rewritten in place, with the date it was set. **Read it before writing.** If the file already exists in another shape — another skill's categories, extra columns, a different period — keep that shape and edit the amounts inside it; "rewritten in place" means replacing the plan's numbers, never replacing someone else's schema. Only an absent file is created from the template below.

```markdown
# Budget — set 2026-07-05

| Category | Type | Planned | Typical actual | Note |
|----------|------|---------|----------------|------|
| Housing | fixed | 1,050 EUR | 1,050 EUR | — |
| Groceries | variable | 520 EUR | 575 EUR | consistently over |
| Car tax + service | sinking | 62 EUR | — | 745 EUR/yr ÷ 12 |

## Sinking Funds
| For | Annual cost | Monthly | Held in |
|-----|-------------|---------|---------|
| Car tax + service | 745 EUR | 62 EUR | Buffer |
```

Every known irregular cost has a sinking line, or it will arrive as an emergency and eat the buffer. `Type` is `fixed`, `variable` or `sinking` — the three behave differently under a cut and the distinction is the point of the file.

## Shared contacts

An adviser, accountant, broker, lender contact or executor is a person and belongs in `~/Clawic/data/contacts/contacts.md` (`name | role | preferred channel | context`), identified by email or handle, updated in place. Reference them here by name only — never copy the person's record into the money box, and never copy their fee arrangement into contacts: the fee is money data, the person is not.

- **Ending the relationship deletes the row**, with the date noted in `memory.md`; a former accountant left in the inventory gets contacted by the next skill that reads it. Rows written by another skill are read-only.
- **Scale cut**: one table in `contacts.md` while there are ≤15 people. Past that, one `~/Clawic/data/contacts/<name-kebab>.md` per person with the same fields, and `contacts.md` becomes the index. If the folder already looks like that on arrival, follow it.
- **Foreign columns win.** If the file exists with a different column set, match its columns and put anything missing in a trailing note. Never rewrite its header.

## Shared projects

If the user tracks a purchase or a plan as a project, the one-line summary also belongs in the shared `~/Clawic/data/projects/<project-kebab>.md`, with the analysis staying in `artifacts/` and referenced by name. The protocol travels with this skill, because the one that owns the box may not be installed:

- **Identity is the project name**, kebab-cased into the filename; one file per project from the first, never a table of several. Read the folder before writing and match an existing project rather than opening a second file for the same thing under another spelling.
- Write **one line** under a `## Money` heading — decision, amount with currency, date, and the artifact filename it came from. If that heading is already there, update the line in place; only its absence justifies a new one.
- **Someone else's structure wins.** If the file exists with other headings or a table, fit the line into what is there and never rewrite its layout or its header. Only the user framing this as a project justifies creating the file; short of that, write nothing there — the artifact is enough.
- When the project closes, delete the money line and note the closure date in `memory.md`. The artifact and the decisions row stay.

## artifacts/

One file per thing, at `~/Clawic/data/money/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **payoff plan**, **investment policy**, **decision analysis** (rent-versus-buy, an offer comparison, a big purchase), **coverage map**, **claim log** (one per open insurance claim, `claim-<kebab>.md`), **estate and beneficiary checklist**, **income-shock playbook**, **tax-prep checklist**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Payoff plan — cards and car loan
*Read whenever a debt payment, a rate change or a windfall comes up. Written 2026-07-26.*

Method: avalanche. Order, rate, monthly, projected clear date.
Total interest avoided versus minimums: 2,180 EUR.
Trigger to revisit: any rate change, any income change above 10%, or a windfall.
```

```markdown
# Investment policy
*Read before any allocation change, any "is now a bad time" question, and at the quarterly rebalance. 2026-07-26.*

Target: 70/30, rebalance at 5pp bands, quarterly check only.
Contribution: 525 EUR/month, automated on payday.
What would change this: horizon shortening under 7 years, or a stated posture change — never a market move.
Written rule for a drop: no change above a 20% fall; the plan already assumed it.
```

```markdown
# Decision — rent versus buy, 2026
*Read if buying comes up again before 2028. 2026-07-26.*

Decision: keep renting for now.
Numbers: round-trip transaction cost ~9% of price; break-even at 6.2 years; expected stay 3 years.
Rejected: buying with a 10% deposit — the break-even is longer than the horizon.
What would flip it: a stay longer than 7 years, or a deposit above 20% with the rate below 3%.
```

## decisions/

`~/Clawic/data/money/decisions/<year>.md`. Short rows; the long analysis lives in `artifacts/` and is named in the last column. This is what stops the same question being re-litigated every six months.

```markdown
# Decisions — 2026

| Date | Decision | Amount | Why | Rejected | Analysis |
|------|----------|--------|-----|----------|----------|
| 2026-06-30 | Bonus split: 70% to Visa, 30% to buffer | 4,200 EUR | 21.9% beats every alternative | Investing it | — |
| 2026-07-26 | Keep renting | — | Break-even 6.2y vs 3y horizon | Buying at 10% deposit | `artifacts/decision-rent-vs-buy.md` |
```

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`, promoted one level.

`net-worth.md` — `## Snapshots`, `## Composition`. The reason this file exists is the series: a single reading says nothing, twelve quarters say whether the plan works.

`goals.md` — `## Active`, `## Achieved`. Achieved goals are kept, with the date; deleting them erases the only evidence the system works.

`debt-plan.md` — `## Order`, `## Progress`. The progress log is why it splits: rate reductions and milestones accumulate and are exactly what makes the next retention call easy to win.
