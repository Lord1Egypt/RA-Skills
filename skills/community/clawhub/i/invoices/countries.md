# Countries — Retention, Mandates, And Filing Calendars

Jurisdiction-specific rules that change what the archive must hold and for how long. Selected by `country` in `config.yaml`; while it is unset, name the assumption before acting on it (Rule 9).

**Verified 2026-07.** Retention periods and filing deadlines are stable across years; **e-invoicing mandate dates are not** — they have moved repeatedly in every country that has announced one. Treat every date in the Mandates section as needing confirmation against the national tax authority before anyone builds a process on it, and re-check anything read here more than a quarter ago.

**Before applying anything from this file**, read `config.yaml` for `country`, `vat_regime`, and `retention_years`, and `## Filings` in `memory.md` for what has already been submitted and when.

**Contents:** [Retention](#retention) · [How Long Is Actually Long Enough](#how-long-is-actually-long-enough) · [E-Invoicing Mandates](#e-invoicing-mandates) · [Spain](#spain) · [Germany](#germany) · [France](#france) · [Italy](#italy) · [United Kingdom](#united-kingdom) · [United States](#united-states) · [Elsewhere](#elsewhere) · [Cross-Border](#cross-border)

## Retention

Clocks run from the **end of the tax or accounting year**, not the invoice date (`filing.md`).

| Country | Fiscal clock | Commercial / accounting clock | Practical floor |
|---|---|---|---|
| Spain | 4 years, the general prescription period | 6 years for books and supporting documents under commercial law | 6, and 10+ where capital-goods adjustment applies |
| Germany | Books and records 10 years; accounting vouchers were shortened to 8 years for periods from 2025 | Same regime | 10, because the shorter voucher rule does not cover everything |
| France | 6 years for tax documents | 10 years for accounting records and supporting documents | 10 |
| Italy | 5 years fiscal from the filing deadline | 10 years civil for accounting records | 10 |
| United Kingdom | 6 years from the end of the accounting period for VAT records | Company records 6 years | 6 |
| Netherlands | 7 years; 10 for records relating to immovable property | Same | 7, 10 for property |
| Portugal | 10 years | Same | 10 |
| Poland | 5 years from the end of the year the tax was due | Accounting 5 years | 5 |
| United States | IRS general 3 years; 6 if income is understated by more than 25%; 7 for bad-debt and worthless-securities claims; 4 for employment tax; unlimited where no return was filed or fraud is alleged | State rules vary | 7 |

## How Long Is Actually Long Enough

The default `retention_years` = 10 is not conservatism for its own sake; four independent clocks can run past the tax one:

1. **Commercial and accounting law**, which in most of Europe outruns the tax period.
2. **Capital goods**, where VAT on assets can be adjusted over several years and on property over a decade — the invoice for the asset must survive its whole adjustment window.
3. **Contractual and statutory limitation** on the underlying supply, measured in years, which decides whether an invoice can still be enforced or disputed.
4. **Anything under audit, dispute, or proceedings**, which suspends every other clock until it ends.

Storage costs nothing next to reconstructing a year nobody kept. Purging is proposed with counts and periods, never executed silently (`filing.md`).

## E-Invoicing Mandates

The pattern is the same everywhere and it is worth understanding once: **the obligation to *receive* structured invoices always lands before the obligation to *issue* them**, and it lands on everyone at the same time rather than being phased by size. Being unable to receive is the failure that actually bites a small business, because the supplier's invoice is legally delivered whether or not it can be opened.

Status as verified 2026-07, and every one of these dates has moved at least once:

| Country | Reception | Issuing | Channel |
|---|---|---|---|
| Italy | Long-established | Mandatory B2B since 2019, extended to flat-rate taxpayers in 2024 | The national exchange platform; the platform copy is the legal original |
| Germany | Mandatory for domestic B2B since January 2025 | Phased from 2027, by turnover | EN 16931 formats: XRechnung, ZUGFeRD/Factur-X |
| France | Mandatory for all businesses from September 2026 | Phased from September 2026 through 2027, largest first | Approved platforms; Factur-X is the common hybrid |
| Belgium | Mandatory B2B from January 2026 | Same date | Peppol network |
| Poland | Phased through 2026, largest first | Same phasing | The national platform |
| Spain | Reception obligations follow the anti-fraud software rules and the B2B regulation still being finalised | Not yet fully in force | National formats plus the anti-fraud software regime |
| EU-wide | Digital reporting requirements agreed under the VAT-in-the-digital-age package, applying around 2030 | Same | Structured formats and near-real-time reporting |

Consequences for this archive regardless of country:

- A supplier in a mandate country may deliver via a platform and never email anything. An invoice reported missing is checked on the channel before it is chased (`suppliers.md`).
- Where a platform is the legal channel, the platform copy is the original and an emailed PDF is a courtesy copy. When they disagree, the platform wins (`capture.md`).
- Structured formats remove OCR from the process entirely, which removes the largest single source of extraction error.

## Spain

- **Retention**: 4 years fiscal, 6 commercial; longer for capital goods.
- **Invoice validity** requires the elements in the invoicing regulation: sequential number, issue date, issuer's name and tax ID, issuer's address, description of the operation, taxable base, rate applied, tax amount, and total.
- **Simplified invoices** (the till-receipt form) are permitted below a value threshold, but they only allow VAT deduction when they additionally carry the recipient's tax ID and the tax amount stated separately. Requesting the full invoice at the point of sale is much easier than getting one later.
- **Rate bands**: a standard rate, a reduced rate, and a super-reduced rate, plus exempt categories including insurance, finance, health, and education.
- **Withholding on professional services**: invoices from certain professionals carry an income-tax withholding that reduces the amount payable without reducing the deductible base. Capture it as its own field, never as tax and never as a discount (`extraction.md`).
- **Equivalence surcharge** applies to certain retailers and rides alongside VAT without being VAT.
- **Periodic VAT return** is filed quarterly by default, in the twenty days following each quarter, with the fourth quarter falling in January; large taxpayers file monthly with near-real-time record submission.
- **Annual counterparty declaration**: operations with any single counterparty above a set annual threshold are declared once a year. The archive is what makes this answerable, and a supplier just under the threshold is exactly the case where a missing invoice changes the answer.
- **Anti-fraud software rules** govern invoice *issuing* systems; they matter here only because they change what suppliers send and when.

## Germany

- **Retention**: 10 years for books, inventories, and annual accounts; 8 years for accounting vouchers for periods from 2025. Keeping everything for 10 avoids classifying each document.
- **Principles for digital records** require that stored records be complete, unalterable, traceable, and readable for the whole period, with the process itself documented. A digital archive is fine; an undocumented one is the gap.
- **Reception of structured B2B invoices has been mandatory since January 2025.** A supplier may send XRechnung or ZUGFeRD/Factur-X and is not obliged to provide a readable PDF.
- **VAT ID vs tax number**: the domestic tax number is not the VAT identification number, and only the latter works for cross-border reverse charge (`validation.md`).
- **Small-amount invoices** below a threshold may omit the recipient's details and still allow deduction, which is the exception to the usual rule.

## France

- **Retention**: 6 years fiscal, 10 years commercial. Ten in practice.
- **Reception of e-invoices becomes mandatory for all businesses in September 2026**, issuing phased from the same date through 2027 by size. This is the largest near-term change for anyone invoicing or being invoiced in France.
- **Factur-X** is the hybrid format in common use: a PDF/A-3 carrying CII XML, identical in substance to ZUGFeRD.
- The mandate is accompanied by e-reporting obligations for transactions outside its scope, which is a supplier-side concern but changes what arrives.

## Italy

- **Retention**: 10 years civil, 5 fiscal. Ten.
- **B2B e-invoicing through the national exchange system has been mandatory since 2019**, extended to flat-rate taxpayers in 2024. FatturaPA XML is the only valid form for domestic B2B.
- **The copy delivered by the exchange system is the legal original.** A PDF the supplier emails is a convenience rendering, and its content is not what the authority holds.
- Digital preservation carries its own conformity requirements; a supplier or a service usually handles it, and the local archive is a second copy rather than the compliant one.

## United Kingdom

- **Retention**: 6 years from the end of the accounting period.
- **Digital record-keeping and digital links** are required for VAT: the chain from record to return must be digital, with no manual re-keying between steps. A CSV export that is retyped into a return breaks the link.
- **No EU-wide VAT-number validation applies** post-Brexit; UK numbers are checked against the domestic service.
- **Imports from the EU are now imports**, with customs documentation and, where elected, postponed VAT accounting. The customs document is still the deduction voucher (`vat.md`).

## United States

- **Retention**: 7 years covers the common cases; longer where no return was filed.
- **There is no VAT and no input-tax recovery.** Sales tax paid on purchases is generally a cost, not something reclaimable, and resale exemptions work through certificates rather than through the invoice.
- **Sales tax is state and local**, with rates varying by jurisdiction and sometimes within a single ZIP code. An invoice's tax line is not comparable to a VAT line and should not be coded as recoverable.
- **Vendor tax reporting**: payments to certain contractors and service providers are reported annually, which makes accurate supplier records and identification numbers a filing requirement rather than a convenience.

## Elsewhere

Where `country` is not covered above, the questions that determine everything else, in order:

1. Is there a value-added or goods-and-services tax with input recovery, or a sales tax that is a pure cost?
2. What are the fiscal and commercial retention clocks, and which is longer?
3. What makes an invoice valid for deduction — specifically, must it name the recipient and their tax identifier?
4. Is there an e-invoicing mandate, and does it bind reception, issuing, or both?
5. What is the filing cadence and the deadline after each period end?

Answer those five, record them in an artifact with the date and the source, and the rest of this skill applies unchanged.

## Cross-Border

- **Reverse charge** for intra-EU B2B services, with a valid VAT number on both sides (`vat.md`).
- **Imports** need the customs document, not the supplier invoice, for recovery.
- **Foreign VAT** charged by a supplier in another country is recovered through that state's refund procedure, subject to an annual deadline and minimum amounts, or avoided in the first place by giving the supplier a valid VAT number.
- **A supplier in a mandate country invoicing a customer outside it** usually falls back to PDF, which is why the mandates have not eliminated OCR for anyone with international suppliers.
- **Currency**: convert at the rate for the date the tax became chargeable, from a source used consistently (Rule 4).

**Write before you finish**: the country rules that apply to this user — retention, filing deadlines, the mandate status that affects their suppliers — go to `artifacts/rules-<country>.md` with the verification date, the source, and its `## Boxes` line, so the next session reads a dated fact rather than re-deriving one. Deadlines become dated rows in `## Due`, never the word "quarterly" — the deadline is not the period end (`memory-template.md`).
