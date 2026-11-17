# Extraction — Reading The Document

What to pull out, how to grade it, and what to do when a field is missing or unreadable. Applies after format triage (`capture.md`): a structured payload is parsed, not extracted, and skips confidence grading entirely.

**Before extracting**, read `## Suppliers` in `~/Clawic/data/invoices/memory.md` (or `~/Clawic/data/invoices/supplier-book.md` if `## Boxes` points there) and `~/Clawic/data/invoices/categories.md` if `config.yaml` names one. A supplier already known brings its canonical name, its tax ID, its usual rate, and any parsing quirk recorded for it — extracting blind against a supplier you have twenty invoices from is wasted work and a new spelling in the ledger.

**Contents:** [Required Fields](#required-fields) · [Optional Fields](#optional-fields) · [The Tax Block](#the-tax-block) · [Line Items](#line-items) · [Dates](#dates) · [Currency](#currency) · [Confidence Grading](#confidence-grading) · [Field Recovery](#field-recovery) · [Categories](#categories) · [Structured Payload Mapping](#structured-payload-mapping)

## Required Fields

No ledger row is complete without these five. A document that cannot yield them is `status: pending`, not `filed`.

| Field | What it is | Failure mode |
|---|---|---|
| `supplier` | Legal name as printed | Trading name captured instead; resolve to canonical (`suppliers.md`) |
| `invoice_number` | The supplier's own reference | Order number, customer number, or payment reference captured instead — the invoice number is the one that increments |
| `date` | Issue date, not print date, not due date | Three dates on the page and the wrong one taken; see Dates |
| `total` | The amount payable | The subtotal taken as the total on invoices where tax appears below the fold |
| `currency` | ISO code | Assumed from the country; a German supplier can invoice in USD |

## Optional Fields

Pull when present; their absence is information, not an error.

| Field | Why it matters |
|---|---|
| `supplier_tax_id` | The identity key (Rule 3), and the precondition for VAT deduction in most regimes |
| `recipient_tax_id` | Whether the invoice is actually addressed to the user — an invoice naming someone else is not deductible by them |
| `subtotal` per rate band | The only way a per-rate VAT return adds up (`vat.md`) |
| `tax_rate` / `tax_amount` per band | Same; a single blended rate is a lost breakdown |
| `due_date` | Drives payment scheduling and the discount clock (`payments.md`) |
| `payment_terms` | "2/10 net 30" is the discount, not decoration |
| `line_items` | What was bought — deductibility often turns on it, and disputes always do |
| `iban` / account reference | Compared against the supplier's stored last four (Rule 5). Store only the **last four** |
| `payment_reference` | What the supplier matches the payment against; a wrong one produces a dunning notice for an invoice you paid |
| `purchase_order` | Enables 2-way and 3-way match (`approvals.md`) |
| `period_covered` | A service period differing from the issue date changes which tax period it belongs to |
| `customs_reference` | On import documents, the deduction hangs on it (`vat.md`) |

## The Tax Block

The single densest source of extraction error, because invoices print it four different ways.

- **Per band, always.** An invoice with 21% and 10% lines has two bases, two rates, two tax amounts. Collapsing them into one number destroys the return.
- **Tax-inclusive pricing** is common in retail: the line prices already contain tax and the block back-computes it. `base = total / (1 + rate)`. Worked: a 121.00 EUR total at 21% → base 100.00, tax 21.00. Taking 121.00 as the base and adding 21% is the classic 25.41 EUR error.
- **Zero is three different things**: `0%` zero-rated, `EX` exempt, `RC` reverse charge. They print almost identically and are declared differently. The invoice usually names it in a legend line ("reverse charge", "autoliquidación", "Steuerschuldnerschaft des Leistungsempfängers", "autoliquidazione"); capture the legend when the code is ambiguous.
- **Withholding** is not VAT and not a discount. Some jurisdictions have suppliers withhold income tax on the invoice (Spanish `IRPF` on professional services is the common case): the total payable drops but the deductible base does not. Capture it as its own field and never net it against tax.
- **Recargo de equivalencia**, surcharges, environmental levies, and tourist taxes ride alongside tax and are not tax. They belong in the base or in their own line, never in the tax column.
- Verify before accepting: `sum(bases) + sum(taxes) + surcharges − withholding = total`, tolerance ±0.02 per band (Rule 6).

## Line Items

Capture them when the invoice has fewer than about twenty and when any of these is true: the amount exceeds `approval_threshold`, the deductibility is partial or conditional, a purchase order exists, or the invoice is disputed. Otherwise the description line is enough — line items are not free to store and are almost never read back for a 9 EUR subscription.

Shape: `description · quantity · unit price · line total · rate band`. Where line totals do not sum to the subtotal, the difference is usually a discount line or shipping; find it rather than adjusting the subtotal.

## Dates

Three dates compete on most invoices and a fourth hides in the fine print.

| Date | What it drives | How it is mistaken |
|---|---|---|
| Issue date | Tax period, ledger year, FX rate (Rule 4) | Confused with the download or print date, which can be months later |
| Due date | Payment scheduling, discount window | Taken as the issue date on invoices where "date" means due |
| Service / supply period | Which period the cost belongs to when it differs from issue | Ignored entirely; a December invoice for November service is a real allocation question |
| Payment date | The `Paid` column, cash-basis reporting | Not on the invoice at all — it comes from the bank |

Format ambiguity: `03/04/2026` is March 4th or April 3rd depending on the issuing country. Resolve using the supplier's country, not the reader's locale, and when the day exceeds 12 use it to disambiguate the rest of that supplier's invoices permanently — record the finding as a parsing quirk in the supplier's artifact.

## Currency

- The issued currency is stored as issued (Rule 4). Conversion is a derived column, never a replacement.
- `€`, `$`, and `kr` are ambiguous symbols. `$` alone spans USD, CAD, AUD, and more; resolve from the supplier's country or an explicit ISO code on the document, and mark the field low confidence when neither is available.
- Decimal separators invert between locales: `1.234,56` and `1,234.56` are the same amount written by different countries. Anchor on the supplier's country, and sanity-check against the tax math — an amount that is off by a factor of a thousand fails Rule 6 immediately, which is the cheapest possible detector.

## Confidence Grading

Applies to OCR and text-layer extraction, never to structured payloads.

| Grade | Meaning | Consequence |
|---|---|---|
| `high` | Clear text, and the field passes its own validation (tax math, ID format, date plausible) | Files without review |
| `medium` | Read cleanly but unvalidated — no format to check it against | Files; the field is flagged in the row if it is one of the five required |
| `low` | Partial, ambiguous, or contradicted by another field | Blocks filing; goes to `## Open Items` as pending |

Any required field at `low` makes the whole document pending. One optional field at `low` does not — but a `low` on the total or the tax block always does, because both feed a number that gets reported.

## Field Recovery

When a field will not come out of the document:

| Missing | Recover from |
|---|---|
| Supplier tax ID | The supplier row from an earlier invoice; the public registry for their country; the supplier's own website footer |
| Invoice number | The payment reference, the portal listing, or the filename the supplier used — then confirm against the document |
| Rate band on a total-only invoice | Back-compute from base and tax if both are present; otherwise the supplier's standing rate from `## Suppliers`, marked `medium` |
| Recipient details | If the invoice does not name the user at all, it may not be theirs; stop and check before filing anything deductible |
| Everything, unreadable scan | Request a reissue while the supplier's own retention window is still open — portals expire long before tax retention does (`capture.md`) |

Never invent a field to make a row complete. An empty cell is readable; a plausible fabrication is not detectable later.

## Categories

Built-in list, used until `category_scheme` points at a mapping file.

| Category | Typical matches |
|---|---|
| hosting | infrastructure and cloud providers, domains, CDN |
| software | SaaS subscriptions, licences, developer tools |
| telecom | mobile, broadband, VoIP |
| utilities | electricity, gas, water, heating |
| office | supplies, furniture, coworking, rent |
| professional | legal, accounting, consulting, agencies |
| marketing | ads, sponsorships, design, content |
| travel | transport, accommodation, per-diem-adjacent costs |
| meals | restaurants and catering — conditional deductibility in most regimes |
| equipment | hardware and anything capitalizable rather than expensed |
| insurance | policies of any kind, commonly VAT-exempt |
| financial | bank fees, payment-processor fees, interest |
| tax | levies and duties invoiced directly |
| other | assigned only with a note saying why nothing fit |

Assign from the supplier first, the description second, keywords last — the supplier is stable and the description is marketing copy. A supplier that spans categories (a marketplace, a large retailer) is categorized per invoice, and that fact belongs in its supplier row so nobody re-derives it monthly.

**Write before you finish**: a newly seen supplier, a new alias for a known one, a corrected tax ID, or a parsing quirk worth remembering goes to `## Suppliers` in `memory.md` (or `~/Clawic/data/invoices/supplier-book.md` past the split); a quirk long enough to need explaining goes to `artifacts/supplier-<name>-parsing.md` with its `## Boxes` line. The extracted invoice itself becomes a ledger row at filing time, not here (`filing.md`).
