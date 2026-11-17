# Capture — Getting Documents In

Everything upstream of extraction: what arrived, whether it is even an invoice, which format it is, and how a backlog gets absorbed without stalling.

**Before capturing anything**, read `## Boxes` in `~/Clawic/data/invoices/memory.md` and check `inbox/` — a document already sitting there from a previous session is the same document the user is about to hand you again.

**Contents:** [Sources](#sources) · [Is It Even An Invoice](#is-it-even-an-invoice) · [Format Triage](#format-triage) · [The E-Invoice Formats](#the-e-invoice-formats) · [Photos And Scans](#photos-and-scans) · [Email Intake](#email-intake) · [Portal Downloads](#portal-downloads) · [Absorbing A Backlog](#absorbing-a-backlog)

## Sources

| Source | What arrives | First move |
|---|---|---|
| Email attachment | PDF, sometimes XML, sometimes both | Keep the attachment, not the email body; the body is where passwords and phishing live |
| Email body only | An HTML "invoice" with no attachment | Not a document. Request the PDF/XML, or download it from the portal; file as `pending` meanwhile |
| Photo of paper | Image, variable quality | Photos section below; a bad photo costs more than a re-shoot |
| Scanner | Image PDF, sometimes multi-invoice | Split into one file per invoice before anything else |
| Supplier portal | PDF or XML download | Portal section below; record the URL in the supplier row, never the login |
| Structured e-invoice channel (Peppol, SdI, national platform) | XML, already validated | Highest-fidelity source there is; parse and file |
| Handed over as a folder | Years of loose files | Backlog section below |

## Is It Even An Invoice

Filing a non-invoice as an invoice double-counts the moment the real one arrives. The distinctions that matter:

| Document | Tell | Destination |
|---|---|---|
| Invoice | Numbered, dated, names the recipient, states tax | Ledger, normal path |
| Simplified invoice / till receipt | No recipient named, often no recipient tax ID | Deductible for income tax in most regimes, usually **not** for VAT unless it carries the recipient's tax ID and the tax amount. Request a full invoice (`vat.md`) |
| Proforma | Says "proforma", no fiscal number, often "not a valid invoice for tax" | Not a cost. One row in `## Open Items` as expected, deleted when the real invoice is filed |
| Quote / order confirmation | Prices, no invoice number, forward-looking | Not a cost, not a ledger row |
| Statement of account | Lists several invoices and a balance | Not a cost. Useful for finding invoices you never received (`suppliers.md`) |
| Payment confirmation / receipt of payment | References an invoice, proves the money moved | Fills the `Paid` column of an existing row; never its own row (Rule 7) |
| Credit note | Negative amounts, references the original | Its own row, negative, `credit-note for <number>` (`disputes.md`) |
| Dunning notice / reminder | Repeats an invoice already issued | Not a new cost. Check whether the original is in the ledger — if not, that is the finding |
| Anything else | — | Ask what it is once, then file it where the user says; if durable, `artifacts/` |

Recognition tokens across languages, because suppliers do not translate for you: invoice · factura · facture · rechnung · fattura · fatura · faktura · nota fiscal · 請求書. Credit note: nota de crédito · avoir · gutschrift · nota di credito. A proforma is called proforma nearly everywhere, which is the one piece of luck in this table.

## Format Triage

Run in order; stop at the first that applies (SKILL.md Rule 2).

1. **File is XML** → parse it directly. Fields are declared, not inferred; no confidence grading applies.
2. **File is a PDF with an embedded file attachment** → it is a hybrid. Extract the attached XML and parse that; the visible page is a rendering, and where the two disagree, the XML is the invoice.
3. **PDF has a text layer** → extract text and parse against labels and tax IDs, never against pixel positions. Layouts change between two invoices from the same supplier.
4. **PDF is an image, or the file is an image** → OCR, then grade every field (`extraction.md`).
5. **File is a ZIP** → suppliers ship a month of invoices in one archive; expand and treat each as a separate document.

A PDF that renders as an invoice but yields no text at all is a scan, no matter how crisp it looks.

## The E-Invoice Formats

| Format | Shape | Where | Notes that change handling |
|---|---|---|---|
| Factur-X / ZUGFeRD | PDF/A-3 with embedded CII XML | FR, DE, increasingly EU-wide | Indistinguishable from a normal PDF until you check attachments. Same standard under two national names |
| XRechnung | Pure XML (UBL or CII), EN 16931 | DE, mandatory for public sector, B2B reception since 2025 | No visual layer at all; a human needs a viewer, so keep a rendered copy alongside if the user wants to eyeball it |
| FatturaPA | XML routed through the SdI exchange system | IT | Digitally signed and delivered by the platform; the copy from the SdI is the legal original, a supplier-emailed PDF is not |
| Facturae | Signed XML (XAdES) | ES | The signature is what makes it valid — re-saving or converting destroys it (Rule 1) |
| Peppol BIS Billing 3.0 | UBL XML over the Peppol network | EU-wide, national mandates | Network delivery means an invoice can exist without ever touching email; check the channel before declaring one missing |
| UBL 2.1 / UN/CEFACT CII | The two syntaxes EN 16931 permits | — | EN 16931 is the semantic standard; UBL and CII are the two ways to write it |
| Plain PDF | No structured data | Everywhere | Still legal in most B2B contexts today; mandates are closing this (`countries.md`) |

A PDF emailed by a supplier in a country where the platform is the legal channel is a courtesy copy. When the two disagree, the platform copy wins.

## Photos And Scans

- One invoice per file. A photo containing two receipts becomes two files before extraction, or the ledger gets one row for two costs.
- Reject and re-shoot rather than OCR badly: a cut-off total line, a fold across the tax block, or glare over the invoice number costs more in corrections than a second photo. The specific fields worth checking before accepting a photo: number, date, tax ID, per-rate tax block, total.
- Thermal receipts fade to blank in months. Anything on thermal paper is captured the day it arrives, not at period end.
- Multi-page invoices: the totals page alone is not the invoice. Keep every page in one file — a detached page is what a supplier disputes later.
- A rotated or skewed scan is fine for OCR; a compressed-to-oblivion one is not. Never re-compress to "save space" (Rule 1).

## Email Intake

Only when the user has set up their own mail access and asks for it in the session — this skill does not connect to a mailbox on its own.

- Candidate signals, in descending reliability: an attachment whose content is an invoice · a sender already in `## Suppliers` · a subject carrying an invoice token in any of the languages above · an amount and a due date in the body.
- The attachment is captured, the body is not (`memory-template.md`, Secrets). If the body carries the only copy of a portal password, that password is not stored.
- Never trust the display name of a sender; compare the actual domain against the supplier's known domain, character by character. This is the same check Rule 5 exists for.
- Mark the source in the ledger row's `Notes` column when an invoice arrived by an unusual route (`arrived from billing@ instead of the portal`) — it is the first thing you want when the same supplier's next invoice looks off.

## Portal Downloads

- Store the portal URL in the supplier row; store the credentials nowhere (`<keychain:...>` pointer at most).
- Portals commonly hold invoices the supplier never emailed. When a recurring invoice is reported missing, the portal is the first place to look, before chasing (`suppliers.md`).
- Download the structured format when the portal offers a choice — the XML and the PDF are the same invoice, and the XML files without OCR.
- Portals retain for a limited window, often 12-24 months, while retention obligations run for years. That asymmetry is the whole argument for a local archive.

## Absorbing A Backlog

A folder of years of PDFs is a throughput problem, not an extraction problem. Extracting everything at full fidelity stalls in the first hundred files and then never resumes.

1. **Sort newest first.** Recent invoices affect open tax periods and unpaid balances; the oldest ones are already past every deadline they could have affected.
2. **Full extraction inside open tax periods only** — periods not yet filed, plus any period still within amendment range. Everything older gets the light pass: date, supplier, total, currency, archive path, and a ledger row marked `status: filed, extraction: light`.
3. **Batch by supplier, not by date.** Twenty invoices from the same supplier share a layout; extraction accuracy climbs and per-file time drops after the first two.
4. **File as you go.** A batch extracted but not filed is a second backlog. Archive plus ledger row in the same turn, every time (Rule 9).
5. **Deduplicate at the end, not during.** The same invoice appears in a downloads folder and an email export; run the Rule 3 identity check across the finished ledger year rather than on every insert.
6. **Record what was skipped.** Unreadable files, documents that are not invoices, and anything ambiguous go in the import artifact by name — an undocumented gap is indistinguishable from a missing invoice a year later.

Light-pass rows are honest, not provisional: they say what is known and do not pretend to a tax breakdown nobody derived. Upgrade one only when a question actually needs it.

**Write before you finish**: every captured document either has a ledger row in `ledger/<year>.md` or is still sitting in `inbox/` with an `## Open Items` line saying why. A backlog import writes its plan and its skip list to `artifacts/<name>-import.md`, and any new ledger year gets its `## Boxes` line in the same turn (`memory-template.md`).
