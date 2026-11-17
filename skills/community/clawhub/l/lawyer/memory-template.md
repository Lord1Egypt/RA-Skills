# Working File Templates — Lawyer

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/lawyer/config.yaml` | Key by key, read-modify-write |
| Legal context, contracts, positions, matters, deadlines, pain points, box index | `~/Clawic/data/lawyer/memory.md` | Rewritten in place; stays small |
| Agreements: one row per executed contract | `## Contracts` in `memory.md` up to 15; `~/Clawic/data/lawyer/contracts.md` from there | One row per agreement |
| Matters: disputes, investigations, transactions, regulator contacts | `## Matters` in `memory.md` up to 15; `~/Clawic/data/lawyer/matters.md` from there | One row per matter, open and closed |
| Standing clause positions and what was conceded to whom | `## Positions` in `memory.md`; `~/Clawic/data/lawyer/positions.md` from 15 | One row per clause per counterparty |
| Filings, registrations and renewals actually made | `~/Clawic/data/lawyer/filings/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — clause language that was accepted, templates, policies, memos, chronologies, notices served, demand letters, settlement terms, diligence answers, the cap table | `~/Clawic/data/lawyer/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| People: counterparties, outside counsel, opposing counsel, registered agents | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, every skill's contacts in one place |
| A transaction or matter the user runs as a project | `~/Clawic/data/projects/<project>.md` (**shared**) | One file per project |
| Recurring contract costs, subscriptions, legal spend | `~/Clawic/data/finances/subscriptions.md` and `budget.md` (**shared**) | One row per subscription or budget line, with currency |
| **Anything durable this table does not name** | `~/Clawic/data/lawyer/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |
| Third-party personal data: evidence files, employee records, customer data | Nowhere here | Note that it exists, its categories and its controller — never its contents |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| An agreement was signed, amended, renewed or terminated | Its row in `## Contracts`, plus every date it creates in `## Due` |
| A notice, renewal, cure, limitation or filing date was computed | `## Due`, with its alarm date |
| A position was taken or conceded in a negotiation | `## Positions` |
| Clause language was finally accepted | `artifacts/clause-<topic>.md` |
| A dispute, investigation, regulator contact or transaction opened, moved or closed | `## Matters` |
| A filing, registration, grant or renewal was made | `filings/<year>.md` |
| Shares, options or convertibles were issued, granted, transferred, exercised or cancelled | `artifacts/cap-table.md`, the same day it was approved |
| An entity, jurisdiction, regime, headcount or counsel relationship became a fact | `## Legal Context` |
| A policy, template, memo, chronology or diligence answer set was produced | `artifacts/` |
| A notice was actually served | `artifacts/notice-<counterparty>-<subject>.md` with the proof of delivery |
| A counterparty, lawyer or opposing counsel was named | Their row in the shared `contacts.md` |
| A recurring contract cost or a legal bill landed | The shared `finances/subscriptions.md` or `finances/budget.md`, with currency |
| Something bit the user once and must not bite twice | `## Pain Points` |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except artifacts, filings and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. **Who**: the agent about to append. **When**: before appending, count the entries already in the section.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/lawyer/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, promoted one level: `### Active` inside `## Contracts` becomes `## Active` in `contracts.md`. The split is a copy-paste, never a rewrite.
4. **Precedence**: never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a memo, a policy or a chronology is born as its own file whatever its size, because it is read whole and only when its subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Legal documents are unusually dense in secrets: payment schedules carry bank details, data-room invitations carry tokens, runbooks carry logins, signature blocks carry national identifiers. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`env:ESIGN_API_KEY` · `keychain:companies-registry` · `1password:Legal/DataRoom/acme` · `bitwarden:Legal/Court-portal` · `vault:legal/registry` · `profile:filing-agent` · `file:~/Documents/legal/executed/msa-acme.pdf`

When the user pastes a contract, a runbook or an export to save, replace each secret value before writing and leave the pointer visible: `Account: <1password:Finance/Bank/operating>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: registered company names, company and VAT registration numbers, registered addresses, trademark and patent application and registration numbers and classes, case and docket numbers, matter references, court and registry names, contract titles and dates, clause text, cap and fee amounts with currency, insurance policy numbers and limits, counsel and firm names, filing receipt numbers. **Secrets, strip them**: passwords and portal logins for registries, courts, e-signature tools and data rooms; API keys and webhook tokens; data-room or document share links that carry an access token; bank account, IBAN, routing and card numbers in payment schedules; national identity numbers (SSN, NI, passport, tax id of an individual); full dates of birth of third parties; scans or images of identity documents; private keys, escrow release codes and one-time codes.

Third-party personal data is not a secret in this scheme and is still not stored here: record that the dataset exists, its categories and who controls it.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared contacts](#shared-contacts) · [shared projects](#shared-projects) · [shared finances](#shared-finances) · [artifacts/](#artifacts) · [filings/](#filings) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/lawyer/` if it does not exist.

```yaml
home_jurisdiction: england-and-wales
default_side: vendor
risk_posture: balanced
entity_type: ltd
liability_cap_basis: fees-12mo
signature_authority_usd: 25000
notice_lead_days: 45
compliance_regimes: [gdpr, soc2]
counsel_relationship: on-demand
document_format: markdown

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
conventions:
  contract_filename: "<counterparty>-<type>-<yyyy-mm-dd>"
  defined_terms: initial-capitals
jurisdiction:
  contract_language: en
  forum_default: london
risk:
  walk_aways: [uncapped-liability, personal-guarantee]
  min_cyber_cover: "2000000 GBP"
escalation:
  always_counsel: [employment-termination, regulator-contact]
  approver_above_threshold: "the user"
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Lawyer Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Contracts (22 agreements) → `contracts.md`; read before any review, renewal or "what did we sign" question
- Matters (open and closed) → `matters.md`; read before any dispute, claim or regulator question
- Filings 2026 → `filings/2026.md`; read before filing anything, to avoid a duplicate application
- Accepted liability-cap language → `artifacts/clause-liability-cap.md`; read when drafting or redlining a cap
- Diligence answer set → `artifacts/diligence-answers.md`; read the moment a buyer, investor or enterprise customer sends a request list
- Cap table (14 holdings, 9 grants) → `artifacts/cap-table.md`; read before any equity, dilution, leaver or diligence question
- Acme dispute chronology → `artifacts/chronology-acme.md`; read whenever Acme or the 2025 delivery failure comes up

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Acme MSA — non-renewal notice window opens | once, 2026-09-15 | — | 2026-09-15 |
| Confirmation statement | year | 2026-03-04 | 2027-03-04 |
| Trademark UK00003xxxxxx renewal | 10 years | 2019-06-11 | 2029-06-11 |
| Contract renewal sweep | quarter | 2026-07-01 | 2026-10-01 |
| Policy and privacy review | year | 2026-02-10 | 2027-02-10 |

## Legal Context
Acme Widgets Ltd (12345678, England and Wales), single entity, 9 employees UK + 2 contractors ES.
Regimes: UK GDPR, EU GDPR (EU customers), SOC 2 Type II in progress. Registered agent: none, own address.
Counsel: Smith & Co (commercial), on-demand — see contacts.

## Contracts
### Active
| Counterparty | Type | Side | Value | Effective | Term | Renews | Notice by | Law | Cap | Executed copy |
|---|---|---|---|---|---|---|---|---|---|---|
| Acme Corp | MSA + order form | vendor | 60,000 GBP/yr | 2025-01-15 | 12m auto | 2027-01-15 | 2026-10-15 | E&W | 12m fees | file:~/Documents/legal/executed/acme-msa.pdf |
| Northwind | DPA | processor | — | 2025-11-02 | with MSA | — | — | E&W | per MSA | file:~/Documents/legal/executed/northwind-dpa.pdf |

### Expired
| Counterparty | Type | Ended | Why | Survives |
|---|---|---|---|---|
| Contoso | pilot | 2025-08-30 | not converted | confidentiality to 2028-08-30 |

## Positions
| Clause | Our position | Conceded to | When | Note |
|---|---|---|---|---|
| Liability cap | 12m fees + 3× supercap for data | Acme | 2025-01 | matched to 2M GBP cyber limit |
| IP in deliverables | customer owns deliverables, we keep background | — | — | never conceded background IP |

## Matters
### Open
| Matter | Counterparty | Stage | At stake | Forum | Next step | By | Spend |
|---|---|---|---|---|---|---|---|
| Late delivery claim | Acme | demand sent | 45,000 GBP | E&W courts | response due | 2026-08-09 | 1,200 GBP |

### Closed
| Matter | Counterparty | Outcome | Closed | Total cost |
|---|---|---|---|---|
| Trademark opposition | Globex | withdrawn after letter | 2025-12-04 | 900 GBP |

## Pain Points
2025: an auto-renewal on a 24,000 GBP tool renewed unnoticed — notice window had closed 11 weeks earlier. Every contract gets a `## Due` alarm at signature since.

## How They Work
Wants the exposure number first and the reasoning second. Will not pay for counsel below ~5,000 GBP at stake.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every date this skill computes belongs here, including one-off deadlines, and the alarm date is what is stored, not the raw deadline (SKILL.md Rule 3).
- **`## Contracts`**: one row per agreement, never a second row for the same one — a renewal or amendment updates the row in place and moves the dates. `Value` and `Cap` always carry their currency. `Executed copy` is a `file:` pointer to where the signed document lives, never its contents.
- **`## Matters`**: money at stake and spend to date both carry currency. A matter moves from `### Open` to `### Closed` with its outcome; it is never deleted, because the limitation period on a closed matter can outlast the memory of it.
- **`## Positions`**: what was conceded and to whom. This is the file that stops the same concession being re-given, and stops a position being offered to customer B that contradicts what customer A was told.
- These headings are exactly the ones `contracts.md`, `matters.md` and `positions.md` get when their sections outgrow this file, promoted one level, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their entities, contracts and posture |
| `complete` | Know their legal setup and standing positions well |

## Shared contacts

Lives at `~/Clawic/data/contacts/contacts.md` and is shared with every other skill that tracks people — the user may not have any of them installed, so the format travels with this skill.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|------|-----|------|-------------------|---------|--------------|------|
| Jane Smith | jane@smithco.legal | outside counsel (commercial) | email | Smith & Co, 320 GBP/hr, on-demand | 2026-07-20 | — |
| Tom Reyes | t.reyes@acme.com | counterparty — Acme, contracts | email | approves up to 50k; escalates above | 2026-07-11 | — |
```

- **Identity is the `Key` column**: lowercase email, falling back to a handle, falling back to `<kebab-name>` plus a stable disambiguator. It is a column of the row, never implicit and never delegated to a per-person file. `Preferred channel` is the type of channel, not the address, so it cannot serve as a key.
- **Read the file before adding.** If the key is already there, update the row in place — never append a second row for the same person. Rows written by other skills are theirs: add missing information, never rewrite their entry.
- **Retirement is part of the inventory.** When a relationship ends, delete the row and note the date in `memory.md`. A contact list that only grows stops being one.
- **Rates and amounts carry their currency in the value** (`320 GBP/hr`), because rows from other skills and other countries sit beside them.
- **Scale cut**: one row per person while there are ≤15, or until one person no longer fits in a row. Past that, one file per person at `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it — do not start a parallel `contacts.md`.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Never store an individual's national identity number, date of birth or identity document here. Contract rows reference a person **by name only**; the person record is never duplicated into the lawyer box.

## Shared projects

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, from the first one. Use it when the user runs a transaction or a matter as a project — a fundraise, an acquisition, an enterprise deal, a compliance programme.

```markdown
# Series A

status: in progress
objective: raise 2M GBP
decisions:
- 2026-06-02 — Delaware flip rejected; UK Ltd retained (see lawyer/artifacts/memo-delaware-flip.md)
milestones:
- data room open 2026-07-01
- disclosure letter due 2026-08-15
```

- **Identity is the project name** (the file slug). Read the folder before creating a file; if the project exists, update it in place.
- **Baseline never deleted**: a finished project gets `status: done | cancelled — <date>` inside the file, because it is the record of what was delivered. Past ~20 closed projects, move them to `projects/archive/<project>.md` without renaming.
- **Foreign columns and fields win**: if the file already exists with another structure, follow it and append.
- Legal documents stay in `~/Clawic/data/lawyer/artifacts/` and are referenced from here by filename. Never duplicate a memo into the project file.

## Shared finances

Lives at `~/Clawic/data/finances/`. This skill writes two things: recurring contract costs, and legal spend.

```markdown
# Subscriptions

| Name | Provider | Cost | Cycle | Renews | Cancel by | Contract |
|------|----------|------|-------|--------|-----------|----------|
| CRM seats | Northwind | 480 GBP | month | 2027-02-01 | 2026-11-03 | Northwind MSA (lawyer/contracts.md) |
```

- **Identity is the subscription or account name.** Read before adding; if it exists, update the row in place. Rows from other skills are theirs.
- **`subscriptions.md` is not split**: it stays a single table and stays small because cancelling deletes the row. When a contract is terminated (`obligations.md`), the row goes — not a status change.
- **Amounts carry their currency in the value** (`480 GBP`), and estimated amounts carry their estimation date.
- Legal spend goes to `~/Clawic/data/finances/budget.md` as a line with the matter name, the amount with currency and the period. The matter detail stays in `## Matters`; only the money crosses over.
- **Foreign columns win.** Match the header that is already there.

## artifacts/

One file per thing, at `~/Clawic/data/lawyer/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **clause language that was accepted** (`clause-<topic>.md`), **template** (`template-<type>.md`), **policy** (`policy-<name>.md`), **memo or decision with its reasoning** (`memo-<topic>.md`), **dispute chronology** (`chronology-<counterparty>.md`), **record of a notice served** (`notice-<counterparty>-<subject>.md`), **settlement terms** (`settlement-<counterparty>.md`), **diligence answer set** (`diligence-answers.md`, `diligence-security.md`), **litigation hold notice** (`hold-<matter>.md`), **compliance register** (`compliance-register.md`), **cap table** (`cap-table.md`). Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Clause — liability cap, accepted language
*Read when drafting or redlining a limitation of liability. Accepted by Acme 2026-01-15.*

Accepted wording: ...the exact text...
Rejected: their 100%-of-fees-paid-to-date cap; our unlimited data carve-out.
Why this landed: matched to the 2,000,000 GBP cyber limit — insurance made it arithmetic.
```

```markdown
# Memo — why we kept the UK Ltd and rejected a Delaware flip
*Read before any question about entity, investors or where to incorporate. 2026-06-02.*

Decision: ...one sentence...
Rejected: Delaware C-corp flip — cost, and no US investor in the round.
Trigger to revisit: a US-led round, or US employees above 5.
```

```markdown
# Cap table — Acme Widgets Ltd
*Read before any equity, dilution, leaver or diligence question. Reconciled to the register 2026-07-14.*

Source of truth: this file. (If it lives elsewhere, say where — `file:~/Documents/legal/cap-table.xlsx` — and keep the summary here.)

| Holder | Security | Class | Number | Price paid | Issued | Vesting | Cliff | Expiry | Evidence |
|---|---|---|---|---|---|---|---|---|---|
| Jane Doe | ordinary shares | A | 400,000 | 0.0001 GBP | 2024-02-01 | 4y from 2024-02-01 | 1y | — | board consent 2024-02-01 |
| Tom Reyes | option (EMI) | — | 30,000 | 0.85 GBP strike | 2025-06-30 | 4y from 2025-06-01 | 1y | 2035-06-30 | grant notice EMI-2026-04 |

Options by state: granted 90,000 · vested 22,500 · exercised 0 · cancelled 5,000 · pool remaining 55,000.
```

```markdown
# Notice — Acme MSA non-renewal
*Read if the Acme renewal is ever disputed. Served 2026-10-02.*

Method: email to notices@acme.example + courier to the registered address (both required by cl. 18.2).
Recipient: General Counsel, per cl. 18.2 as amended 2025-06.
Deemed received: 2026-10-06 (2 business days, courier).
Proof: courier tracking reference and email delivery receipt held with the contract file.
```

If the user tracks the underlying work as a project, the decision summary also belongs in the shared `~/Clawic/data/projects/<project>.md`, with the document staying here and referenced by name.

## filings/

Append-only, cut by year. The point is to never file the same thing twice and to always know what is on record.

```markdown
# Filings — 2026

| Date | What | Authority | Reference | Territory | Cost | Next action |
|------|------|-----------|-----------|-----------|------|-------------|
| 2026-03-04 | Confirmation statement | Companies House | 12345678 | UK | 34 GBP | 2027-03-04 |
| 2026-05-19 | Trademark application, classes 9 and 42 | UKIPO | UK00003xxxxxx | UK | 370 GBP | examination reply window |
| 2026-06-30 | 83(b) equivalent — EMI grant notification | HMRC | EMI-2026-04 | UK | — | — |
```

Every row with a future consequence also gets a `## Due` line in `memory.md`, in the same turn.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`, promoted one level.

`contracts.md` — `## Active`, `## Expired`, same columns. This is the file `obligations.md` and `review.md` read first, so its `## Boxes` read condition names both: "read before any review, renewal or 'what did we sign' question".

`matters.md` — `## Open`, `## Closed`, same columns. A closed matter is kept, not deleted: limitation periods outlast memories.

`positions.md` — the standing clause positions table. The reason this file exists is that a position conceded to one counterparty will be found by the next one's diligence; without it, the same concession is re-given and then contradicted.
