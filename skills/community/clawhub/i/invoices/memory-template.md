# Working File Templates — Invoices

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md`, the ledger, and everything they index are what you **observed** or filed. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/invoices/config.yaml` | Key by key, read-modify-write |
| Business context, open items, filings, supplier notes, due dates, box index | `~/Clawic/data/invoices/memory.md` | Rewritten in place; stays small |
| One row per invoice ever filed — the searchable index | `~/Clawic/data/invoices/ledger/<year>.md` | Append-only, cut by year; born with the first invoice |
| The original documents, exactly as received | `~/Clawic/data/invoices/archive/<year>/<month>/` | One file per invoice, never edited (Rule 1) |
| Documents that arrived but are not filed yet | `~/Clawic/data/invoices/inbox/` | Emptied by filing; a file older than the sweep cadence is a `## Due` item |
| Suppliers: canonical name, aliases, tax ID, cadence, terms, bank last-four | `## Suppliers` in `memory.md`; `~/Clawic/data/invoices/supplier-book.md` past the split | One row per supplier |
| A recurring charge the user is committed to | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per service, every source in one place |
| A named human at a supplier — billing contact, account manager | `~/Clawic/data/contacts/contacts.md` (**shared**) | One row per person, keyed by the `Key` column; a file per person past 15 |
| A cost that will be rebilled to a client project | `~/Clawic/data/projects/<project>.md` (**shared**) | One line per rebillable cost; the invoice stays in the ledger and is referenced by number |
| Chart-of-accounts or category mapping the user or their accountant requires | `~/Clawic/data/invoices/categories.md` | Declared mapping; `config.yaml` points at it by path |
| Tax periods actually filed, with their totals | `## Filings` in `memory.md`; `~/Clawic/data/invoices/filing-history.md` past the split | One row per period |
| Things you produced that get re-read — accountant handoff procedures, VAT treatment decisions, dispute files, fraud-attempt write-ups, backlog import plans, supplier parsing quirks | `~/Clawic/data/invoices/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/invoices/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind, including anything the user pastes | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| An invoice was filed | Its row in `ledger/<year>.md`, in the same turn the file lands in `archive/` (Rule 9) |
| A duplicate was detected and rejected | A `status: duplicate-of <number>` row in the ledger — never a silent discard, or the same file returns next month |
| An invoice was paid, partially paid, or a credit note applied | The `Paid` and `Status` columns of its ledger row, in place; a partial amount, a discount taken, a write-off, or an FX difference in its `Notes` column |
| An approval, a refusal, a split coding, a match discrepancy, or an unusual intake route | The `Notes` column of that invoice's ledger row — the only free-text field a row has, and the reason it exists |
| A supplier appeared, was renamed, merged, or normalized | `## Suppliers`, with the alias added — never a second row |
| A supplier's bank details changed, and how it was verified | The supplier row (`Bank last4`, `Verified`) **and** `artifacts/` if it was a fraud attempt |
| A recurring charge was recognised as a standing commitment | Its row in `~/Clawic/data/finances/subscriptions.md` |
| A named person at a supplier was identified | Their row in `~/Clawic/data/contacts/contacts.md` |
| A cost is to be rebilled to a client project | One line in `~/Clawic/data/projects/<project>.md`, referencing the invoice number only |
| An expected invoice did not arrive, or was chased | `## Open Items`, with the date chased |
| A dispute was opened, escalated, or resolved | `## Open Items` for the state, `artifacts/dispute-<supplier>-<number>.md` for the chronology |
| A tax period was closed and filed | `## Filings`, with the totals actually submitted |
| A VAT treatment was decided for an odd purchase, or an accountant stated how they want things | `artifacts/` |
| A backlog import ran | `## Boxes` for any new ledger year, and `artifacts/` for the plan and what was skipped |
| The user declared a preference | Its key in `config.yaml` |
| Recurring work was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except the ledger, the archive, the shared boxes, and artifacts begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings, and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/invoices/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Three exceptions, all of them born as their own box because of how they are read:

- **The ledger** is a log: it grows without end and is read by year, so it never lives inside `memory.md`. Its first row creates `ledger/<year>.md`.
- **Artifacts** are read whole and only when their subject comes up: a dispute file or a treatment decision is its own file at any size.
- **The archive and the inbox** hold original documents, not text you read. Their `## Boxes` lines exist so nobody forgets they are there, not so they get opened routinely — the ledger row answers the question, the file is only opened when the ledger cannot.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:supplier-portal` · `1password:Work/Telecom/portal` · `bitwarden:Personal/Bank` · `env:OCR_API_KEY` · `file:~/.config/accounting/token` · `vault:kv/billing/portal`

In a document the pointer goes exactly where the value was: `portal_password: <keychain:acme-billing>`. When the user pastes a portal note, an email thread, or a `.env` to be saved, replace each secret value **before** writing and say in one line that you did it.

**The archived original is the single exception, and it is not an exception to this rule.** An invoice PDF is stored exactly as received and is never edited (Rule 1), so whatever the supplier printed on it stays on it. The prohibition governs everything *you* write: ledger rows, memory, supplier rows, artifacts, exports, and pasted text. If an email body carrying an invoice also carries a password, the attachment is archived and the body is not.

In this domain — **not secrets, keep them**: supplier legal name and trading names, VAT and tax IDs (theirs and the user's — they are printed on every invoice and are publicly checkable), invoice and credit-note numbers, purchase-order numbers, dates, amounts, currencies, tax rates, categories, payment status, payment method, the **last four** digits of an account or card, the supplier's public billing email and portal URL, customs declaration references. **Secrets, strip them**: supplier-portal and accounting-software logins and passwords, mailbox and IMAP/app passwords, OCR or accounting API keys and tokens, online-banking credentials and one-time codes, full card numbers, CVVs and expiry dates, full IBANs or account numbers of the **user's own** accounts, SEPA mandate signing credentials, and the passphrase of any e-signature or tax-filing certificate.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [ledger/](#ledger) · [archive/ and inbox/](#archive-and-inbox) · [shared subscriptions box](#shared-subscriptions-box) · [shared contacts box](#shared-contacts-box) · [shared projects box](#shared-projects-box) · [categories.md](#categoriesmd) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/invoices/` if it does not exist.

```yaml
country: ES
vat_regime: standard
vat_period: quarterly
base_currency: EUR
retention_years: 10
duplicate_action: flag
anomaly_pct: 50
approval_threshold: 1000 EUR
accounting_target: csv
category_scheme: ~/Clawic/data/invoices/categories.md

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
intake:
  drop_folder: ~/Downloads/invoices
  accept_photos: true
naming:
  pattern: "<date>_<supplier>_<number>_<total><currency>"
  archive_cut: month
reporting:
  boundary: issue-date      # never mix with payment-date totals
  accountant_columns: [date, supplier, tax_id, number, base, rate, tax, total, category]
retention:
  second_copy: external-drive
  paper_after_scan: keep-one-year
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Invoices Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Invoice ledger 2026 (214 rows) → `ledger/2026.md`; read before any question about an invoice, supplier, or period total
- Invoice ledger 2025 (317 rows) → `ledger/2025.md`; read for anything before this year
- Originals as received → `archive/<year>/<month>/`; open a file only when the ledger row cannot answer
- Unfiled documents (2) → `inbox/`; check at the start of any filing session
- Category mapping the accountant requires → `categories.md`; read before assigning any category
- Accountant handoff procedure → `artifacts/accountant-handoff.md`; read before any export or year-end pack
- Reverse-charge treatment for US SaaS → `artifacts/treatment-us-saas.md`; read when a non-EU supplier invoices without VAT
- Bank-change attempt, Acme, 2026-05 → `artifacts/fraud-acme-2026-05.md`; read if Acme's payment details change again

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Inbox sweep | week | 2026-07-20 | 2026-07-27 |
| Missing recurring invoices | month, day 5 | 2026-07-05 | 2026-08-05 |
| VAT return | quarter | 2026-07-14 | 2026-10-20 |
| Annual pack for accountant | year, January | 2026-01-22 | 2027-01-22 |
| Retention review | year | 2026-02-01 | 2027-02-01 |
| Archive restore test | quarter | 2026-06-30 | 2026-09-30 |

## Context
Sole trader, ES, standard VAT, quarterly 303 filed by an external accountant. Fiscal year = calendar year.

## Suppliers
| Supplier | Tax ID | Aliases | Category | Cadence | Terms | Bank last4 | Verified | Notes |
|---|---|---|---|---|---|---|---|---|
| Hetzner | DE812871812 | Hetzner Online GmbH, HETZNER ONLINE GMBH | hosting | monthly, day 1 | prepaid | 4471 | 2025-11-02 | portal https://accounts.hetzner.com; indexation every January |
| Acme Legal | B12345678 | Acme Abogados SL | professional | irregular | net 30 | 8820 | 2026-05-14 | verified by phone on the number in the 2024 engagement letter |

## Open Items
| What | Supplier | Amount | Since | State |
|---|---|---|---|---|
| Invoice never arrived for June | Telecom | ~45 EUR | 2026-07-05 | chased 2026-07-12 |
| Overbilled two seats | Acme SaaS | 118 EUR | 2026-06-30 | credit note requested |

## Filings
| Period | Filed | Deductible base | VAT reclaimed | Notes |
|---|---|---|---|---|
| 2026-Q1 | 2026-04-18 | 12,450 EUR | 2,315 EUR | one invoice arrived late, carried to Q2 |
| 2026-Q2 | 2026-07-14 | 9,980 EUR | 1,842 EUR | includes the Q1 late invoice |

## How They Work
Wants the archive path with every answer. Never wants an invoice marked paid on their behalf.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file or folder that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the box is created. Never delete a line without deleting what it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Filing deadlines come from `country` (`countries.md`) and are entered here as dates, not as "quarterly", because the deadline is not the period end.
- **`## Open Items`**: only things that are still open. A resolved row is deleted, not annotated — the ledger already holds the history, and a list of resolved items is how this section silently becomes the thirtieth entry that triggers a split.
- **`## Suppliers`**: one row per supplier, keyed by tax ID. Aliases accumulate in their column; a new spelling is never a new row. `Bank last4` plus `Verified` is what Rule 5 compares against — it is the whole reason this table exists rather than being derived from the ledger. `Notes` is the supplier's free-text field: parsing quirks, portal URL, indexation month, notice period, instalment plan, how a bank detail was verified, a pointer to a dispute artifact.
- **`## Filings`**: the numbers actually submitted, not the numbers currently computable. A recomputed total that disagrees with a filed one is a finding, and it only stays a finding if the filed number was written down.
- These headings are exactly the ones `supplier-book.md` and `filing-history.md` get when their sections outgrow this file, so the split stays a copy-paste. The example above is a pre-split file: `## Suppliers` is still inline, so no `## Boxes` line points at it. The moment it is extracted, the section is deleted here and the line appears there — never both.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning their suppliers, regime, and how they want things filed |
| `complete` | Archive is current, suppliers normalized, filings on cadence |

## ledger/

One row per invoice, one file per year, at `~/Clawic/data/invoices/ledger/<year>.md`. Cut by the **issue year**, so a period total never spans two files by accident. This is the index that answers questions; the archive is only opened when it cannot.

```markdown
# Invoice Ledger — 2026

| Date | Supplier | Tax ID | Number | Base | Rate | Tax | Total | Cur | FX | Category | Status | Paid | File | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-02-13 | Hetzner | DE812871812 | INV-12345 | 75.21 | 19% | 14.29 | 89.50 | EUR | — | hosting | filed | 2026-02-15 | `archive/2026/02/2026-02-13_hetzner_INV-12345_89.50EUR.pdf` | — |
| 2026-03-02 | Figma | — | 4471-9920 | 144.00 | RC | 0.00 | 144.00 | USD | 0.9213 ECB 2026-03-02 | software | filed | 2026-03-02 | `archive/2026/03/2026-03-02_figma_4471-9920_144.00USD.pdf` | downloaded from the portal, never emailed; rebilled to acme-redesign |
| 2026-03-11 | Acme SaaS | B12345678 | A-2026-118 | 97.52 | 21% | 20.48 | 118.00 | EUR | — | software | disputed | — | `archive/2026/03/2026-03-11_acme-saas_A-2026-118_118.00EUR.pdf` | 2 seats billed, 1 in use; credit requested 2026-06-30 |
```

- **One row per rate band** when an invoice mixes rates: same date, supplier and number, one row per band, and the `Total` column carries the full invoice total only on the first of them, `—` on the rest. Splitting the base is the only way a per-rate VAT return adds up; repeating the total is how it double-counts.
- **`FX`** is filled only when the invoice currency differs from `base_currency`: `<rate> <source> <date>`, the date being the invoice date (Rule 4). An empty FX column on a foreign-currency row is an unfinished row.
- **`Rate`** carries `RC` for reverse charge, `EX` for exempt, `0%` for zero-rated — three different things that a bare `0` would flatten, and the return needs them apart (`vat.md`).
- **`Status`**: `filed` · `pending` (arrived, not yet complete) · `disputed` · `duplicate-of <number>` · `credited-by <number>` · `non-deductible`. A rejected duplicate keeps a row: a discarded file with no trace comes back next month and gets filed for real.
- **`Paid`** is the payment date, not a flag. Empty means unpaid; a date makes the payment-boundary report possible (`period-close.md`).
- **`Notes`** is the row's only free-text field, and every durable fact about the invoice that no other column holds goes here — nowhere else. What lands in it: a discount taken and its amount, a partial payment and the balance left, a write-off, an FX gain or loss against the payment-date rate, a split coding across projects or accounts with the amounts, `approved by <name>, <date>, against <PO or contract reference>`, a refusal and its reason, a match discrepancy, the business purpose of a purchase whose deductibility depends on it, and an unusual intake route. One fact per clause, separated by `;`, oldest first, appended never overwritten. Anything longer than a line is an artifact and the cell carries its filename.
- Never rewrite a past year's ledger to a new column set. Add the column to the current year going forward and leave history as filed — a retroactively "improved" ledger no longer matches what was reported.

Credit notes get their own row, with a negative `Base`, `Tax`, and `Total`, `Status: credit-note for <number>`, and the original row updated to `credited-by <its number>`. Never edit the original amounts.

## archive/ and inbox/

```
~/Clawic/data/invoices/
├── inbox/                       # arrived, not filed yet
└── archive/
    └── 2026/
        └── 02/
            └── 2026-02-13_hetzner_INV-12345_89.50EUR.pdf
```

- Filename pattern: `<issue-date>_<supplier-slug>_<number>_<total><currency>.<ext>`, sanitized to `[a-z0-9._-]`. The `naming.pattern` key overrides it; the date stays first whatever the pattern, because that is what makes the folder sortable.
- Cut by issue **month** by default (`naming.archive_cut`), so a month folder stays browsable by a human without any tooling.
- The bytes are never modified (Rule 1). A hybrid Factur-X or ZUGFeRD PDF is stored as the single file it arrived as; a structured invoice that arrived as XML plus a human-readable PDF is stored as both, same base name, and the ledger `File` column points at the XML.
- Collision on the same name means the same invoice arrived twice: it is a duplicate check (Rule 3), never a `-2` suffix.
- Record a content hash at filing time if the user wants provable integrity — a column in the ledger, not a second file. It is what makes the digital-only choice defensible (`filing.md`).
- If files exist at an older location (`~/invoices/` or `~/Clawic/data/invoices/` under a different layout), move them into this structure and index every one in the ledger as you go — a moved file with no row is a lost file.

## Shared subscriptions box

Lives at `~/Clawic/data/finances/subscriptions.md`, shared with the money, subscription, and infrastructure skills — the user may have none of them installed, so the format travels with this skill. A recurring invoice becomes a row here the second time the same supplier bills the same thing.

```markdown
# Subscriptions

| Service | Category | Amount | Cycle | Next charge | Paid with | Notes |
|---|---|---|---|---|---|---|
| Hetzner (infra-main) | infrastructure | 41 EUR | monthly | 2026-08-01 | card ••4471 | invoices filed under Hetzner in the invoices ledger |
```

- **Identity is `Service`**, including the account name in parentheses when one provider bills two accounts separately. Read the file before adding; if the row is there, update it in place — never a second row.
- **Amounts carry their currency inside the value** (`41 EUR`, not `€41`), because rows from other providers arrive in other currencies and someone will add the column up. An estimated amount carries the date of the estimate in `Notes`.
- **Update after each invoice** that changes the amount or the cycle; a price rise is exactly the event this box exists to make visible.
- **Cancellation is part of the inventory**: when the service ends, delete the row and note the date in `## Open Items` or `## Suppliers`. A list that only grows stops being a list.
- **Foreign columns win.** If the file already exists with a different header, match it and put anything extra in the last column. Never rewrite its header, and never touch a row this skill did not create.
- **No scale cut**: `subscriptions.md` stays one table however many rows it holds. It stays readable because cancellation deletes the row, not because it is ever split — a commitments list spread across files is one nobody can sum in a single read, which was its only job. If you arrive and another skill has split it anyway, follow what is there and never fold it back.
- Never a full card number here, never a portal password — the last four and a `<kind:locator>` pointer at most.

## Shared contacts box

Lives at `~/Clawic/data/contacts/contacts.md`, shared with every skill that touches people. Only a **named human** goes here — the supplier company itself stays in `## Suppliers`, and duplicating the company in both is how two skills start contradicting each other.

```markdown
# Contacts

| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Marta Ruiz | marta.ruiz@acmelegal.es | Billing, Acme Legal | email | issues the corrected invoices; copy on any dispute; number from the 2024 engagement letter | 2026-06-30 | — |
```

- **Identity is the `Key` column**, and it is written into the row, never left implicit: lowercased email, falling back to a handle, falling back to `<kebab-name>` plus a stable disambiguator. `Preferred channel` is the *kind* of channel, not the address, so it can never serve as the key. Read the file before adding; if the key is there, update that row in place and **extend** `Context` rather than replacing it — another skill wrote what is already in it.
- Delete a row only when the person is no longer a contact at all, not when one engagement ends.
- **Foreign columns win**: match the header that exists, put anything extra in the last column, and never touch a row this skill did not write.
- **Scale cut**: one table while there are ≤15 people; past that — or the moment one person no longer fits in a row — a `~/Clawic/data/contacts/<name>.md` per person with the same fields as headings, and `contacts.md` stays as the index with the `File` column pointing at each one. Count before adding the row that would cross it. If you arrive and the folder already looks like that, follow it and never fold it back into one table.
- No phone numbers used for out-of-band verification get treated as casual data — record where the number came from in the `Context` column of this file, because Rule 5 depends on knowing that it predates the suspicious invoice.

## Shared projects box

Lives at `~/Clawic/data/projects/<project>.md`, one file per project, shared with every skill that tracks work. Used only when a cost will be rebilled or attributed to a client project.

```markdown
## Rebillable costs
| Date | What | Amount | Invoice | Rebilled |
|---|---|---|---|---|
| 2026-03-02 | Figma seat for the Acme redesign | 144.00 USD | 4471-9920 | not yet |
```

- **Identity is the filename**, one `.md` per project from the first, named after the project as a slug. Read it before appending; create it only when no file for that project exists under any spelling — a second file for the same project is the same failure as a second contacts row.
- The invoice itself stays in the ledger; this box carries **only the reference** (`Invoice` = the invoice number). Never copy the full invoice record here.
- Append under a `## Rebillable costs` heading, creating it if the file exists without one. Never restructure a project file written by another skill.
- **A finished project's file is never deleted** — it is the record of what was delivered and what it cost. Closure is a `status:` line inside the file, written by whoever closes it; this skill only ever appends costs.
- Mark `Rebilled` when it appears on an outgoing invoice; that is the column that stops a cost being billed twice or never.

## categories.md

The mapping between what an invoice looks like and the account the user's bookkeeping expects. Written only when the user or their accountant states it — until then, the built-in list in `extraction.md` applies and this file does not exist.

```markdown
# Category Mapping

| Category | Account | Deductible | Matches |
|---|---|---|---|
| hosting | 629 | full | Hetzner, AWS, DigitalOcean, Cloudflare |
| software | 629 | full | Figma, Notion, GitHub, JetBrains |
| meals | 629 | conditional — business purpose recorded | restaurants, catering |
| vehicle-fuel | 628 | 50% presumption, mixed use | fuel stations |
| entertainment | 627 | none | client gifts, events |
```

`config.yaml` points at this file by path (`category_scheme`); the mapping is a declaration, so it lives here and never in `memory.md`.

## artifacts/

One file per thing, at `~/Clawic/data/invoices/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **accountant handoff procedure**, **VAT treatment decision**, **dispute file**, **fraud-attempt write-up**, **backlog import plan**, **supplier parsing quirks**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Accountant handoff — what Marta needs and in what shape
*Read before any export or year-end pack. Written 2026-01-22.*

Format: one CSV per quarter, columns in this order: ...
Wants credit notes as negative rows in the same file, not a separate one.
Rejects anything without a supplier tax ID — those go in a separate "pending" sheet.
Deadline: her office needs the quarter by day 10, filing is day 20.
```

```markdown
# VAT treatment — US SaaS invoiced without VAT
*Read when a non-EU supplier invoices without VAT. Decided 2026-03-02, with the accountant.*

Treatment: reverse charge. Both the output and the input entry are declared; net effect zero while fully deductible.
Ledger convention: `Rate` = `RC`, `Tax` = 0.00, base in the issued currency with the FX cell filled.
Why it is not "no VAT, nothing to declare": the pair is still owed and a missing pair is a filing error.
Applies to: Figma, Notion, GitHub. Re-check if the supplier starts charging local VAT — then it is an ordinary invoice.
```

```markdown
# Dispute — Acme SaaS A-2026-118, two seats overbilled
*Read if Acme SaaS billing is questioned again. Opened 2026-06-30.*

Chronology, what was requested, what they answered, what closed it, and the credit-note number.
```

A dispute file is written from the first message, not once it escalates: the useful part is the chronology, and a chronology reconstructed later is missing exactly the dates that matter.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`supplier-book.md` — `## Suppliers`, the same columns. Once extracted, it is what gets read before filing any invoice, and its `## Boxes` line says so. The name is deliberately not `suppliers.md`: that is the name of a guide in this skill, and a data box that collides with a guide gets opened by the wrong reader.

`filing-history.md` — `## Filings`, the same columns, and named apart from the `filing.md` guide for the same reason. The reason it exists as a file is comparison across years: a quarter's deductible base that moves 40% without an explanation is the finding, and it is only visible with several years side by side.
