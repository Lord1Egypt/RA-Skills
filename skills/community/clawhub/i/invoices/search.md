# Search — Finding Things In The Archive

The ledger answers questions; the archive holds documents. Opening PDFs to answer a question the ledger can answer is the slow, wrong path — and it is the path an archive without a good index forces on you forever.

**Before answering anything**, read the ledger years the question spans (`ledger/<year>.md`), plus `## Suppliers` when a supplier is named — the name in the question is almost never the canonical one.

**Contents:** [What The Ledger Can Answer](#what-the-ledger-can-answer) · [Resolving The Question](#resolving-the-question) · [Query Patterns](#query-patterns) · [Multilingual And Fuzzy Input](#multilingual-and-fuzzy-input) · [When The Answer Is Nothing](#when-the-answer-is-nothing) · [Answer Shape](#answer-shape) · [Reverse Lookups](#reverse-lookups)

## What The Ledger Can Answer

Without opening a single document: supplier, tax ID, invoice number, dates, base, rate, tax, total, currency, FX rate, category, status, payment date, archive path.

Only the document itself can answer: what was actually bought line by line, the payment reference, the bank details as printed, the terms text, anything in an attachment. When a question needs one of those, open the one file the ledger points at — never a folder scan.

The practical consequence: a question like "what did we spend on hosting in 2025" is a filter over one file, and "which invoice covers the second seat we added in March" needs one PDF opened. Knowing which is which before starting is most of the speed.

## Resolving The Question

Four dimensions, in this order, because each one narrows more than the next:

1. **Time** — a period, a year, "last quarter", "since we started with them". Convert to explicit dates and say which dates were used.
2. **Supplier** — resolve through canonical name and aliases (`suppliers.md`). A user asking for "Amazon" may mean the marketplace, the cloud provider, or an advertising account, each a different supplier row.
3. **Amount or state** — over/under a threshold, unpaid, disputed, non-deductible.
4. **Category or content** — the weakest filter, because categories are assigned and descriptions are marketing copy.

State the resolution when it was ambiguous: "Hetzner, matching also 'Hetzner Online GmbH', 2025-01-01 to 2025-12-31, issue date."

## Query Patterns

| Asked | Filter | Trap |
|---|---|---|
| Everything from a supplier | Canonical name plus aliases | Filtering on the string in the question misses three spellings |
| A period total | Date range on the stated boundary | An unstated boundary makes the number unreproducible (`period-close.md`) |
| What is unpaid | Empty `Paid`, excluding disputed and duplicate rows | Including disputed rows inflates payables and someone pays them |
| Above or below an amount | `Total`, in the issued currency unless conversion is requested | Comparing mixed currencies as bare numbers |
| By category | `Category` column | Categories are assigned, so the answer is only as good as the coding; say so when it matters |
| One specific invoice | Supplier plus number, the identity key | Searching by amount finds the twelve identical subscription invoices |
| "The big one from last year" | Sort by total descending within the year and offer the top few | Guessing which one they meant |
| What changed versus last year | Same period, both years, per supplier | Comparing a closed year against a partial one without saying so |
| Everything for the accountant | The whole period, plus the exceptions list | An export is not a search result (`period-close.md`) |
| Anything else | Filter what is filterable, then say which part of the question the ledger cannot answer and what would have to be opened | Silently answering a narrower question than the one asked |

## Multilingual And Fuzzy Input

Users ask in whatever language they think in, and the archive holds documents in several.

- **Supplier names are matched loosely**: case-insensitive, accent-insensitive, ignoring legal suffixes (`GmbH`, `SL`, `Ltd`, `SAS`, `BV`, `Inc`). `hetzner online gmbh` and `Hetzner` are the same query.
- **Month and period names in any language** resolve to date ranges: a request for "enero", "janvier", or "January" is `01-01` to `01-31` of the year in context.
- **Amount formats invert**: `1.500` may be one thousand five hundred or one and a half. Resolve from the user's locale, and when the parse is ambiguous, say which reading was used rather than picking silently.
- **Category words are not categories.** A request about "software" is a category filter; a request about "the Figma thing" is a supplier lookup. Try the supplier interpretation first — it is exact when it hits.

## When The Answer Is Nothing

An empty result is a finding, and which finding depends on why:

| Reason | What to say |
|---|---|
| Supplier not in the ledger at all | Name it: there are no invoices from that supplier, and check whether they are known under another name |
| Supplier exists, period empty | The invoice may be missing rather than absent — check the cadence (`suppliers.md`) |
| Documents in `inbox/` unfiled | Say how many, because the answer is incomplete until they are filed |
| Period predates the archive | State the earliest date the ledger covers; an answer about 2019 from an archive starting in 2022 is not zero, it is unknown |
| Filter too narrow | Show the nearest matches rather than an empty table |

Never present "no results" as "no such cost". The distinction between *absent* and *not recorded* is the whole reliability of the archive.

## Answer Shape

- **Rows, then total, then boundary.** The total is what was asked; the boundary is what makes it trustworthy.
- **Include the archive path** when a specific invoice is the answer — the next thing wanted is the file.
- **Currency per row, never mixed into one sum** without saying the conversion was applied and at which rate.
- **Count as well as amount.** "2,847.50 EUR across 23 invoices" catches an error that "2,847.50 EUR" hides.
- **Name the exclusions.** Disputed, duplicate, and pending rows left out of a total are stated once, not buried.
- Long results get summarized by supplier or month first, with the detail available — a 200-row dump answers nothing.

## Reverse Lookups

Coming from the other direction, which is where the value hides:

- **From a bank line to an invoice**: match amount exactly, date within ±5 days for transfers and ±30 for cards. No match is the interesting outcome — it is an invoice never collected (`period-close.md`).
- **From a dunning notice to the ledger**: search the invoice number first, then the amount and supplier. Not present at all means the invoice never arrived, which is a different problem from a payment that did not match (`payments.md`).
- **From a card statement to the archive**: one statement line often corresponds to a monthly invoice issued days later. Match by supplier and period, never by exact date.
- **From a contract to its invoices**: the contract lives in the archive alongside (`filing.md`); its invoices are found by supplier and date range, and the gap between what the contract says should be billed and what was billed is worth checking once a year.

**Write before you finish**: a search rarely produces durable data, and inventing some is worse than none. Two exceptions: a supplier name resolved to a new alias goes to `## Suppliers`, and a gap the search revealed — a period with no invoice from a cadence supplier, a bank line with no invoice — goes to `## Open Items` in `memory.md`. A finding nobody records is a finding that gets rediscovered every quarter (`memory-template.md`).
