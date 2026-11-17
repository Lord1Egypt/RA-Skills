# Filing — The Archive That Survives An Audit

Where the document goes, what it is called, how it stays provably unaltered, how long it is kept, and what happens when it has to be produced years later.

**Before filing**, read `## Boxes` in `~/Clawic/data/invoices/memory.md` for the current ledger year and the archive layout in use, and `config.yaml` for `naming`, `retention_years`, and `country`. Filing into a layout that differs from the existing one fragments the archive permanently.

**Contents:** [The Filing Turn](#the-filing-turn) · [Naming](#naming) · [Layout](#layout) · [Byte Integrity](#byte-integrity) · [Retention](#retention) · [Backups And Restore](#backups-and-restore) · [Producing Documents On Demand](#producing-documents-on-demand) · [Purging](#purging) · [Personal Data](#personal-data)

## The Filing Turn

One turn, three writes, no partial state (Rule 9):

1. The original moves from `inbox/` into `archive/<year>/<month>/` under its filed name.
2. Its row is appended to `ledger/<year>.md`, with the archive path in the `File` column.
3. Anything learned about the supplier updates `## Suppliers`.

If the ledger year is new, its `## Boxes` line is written in the same turn. A file in the archive with no row is invisible; a row with no file is a claim with no evidence. Neither state is ever the end of a turn.

## Naming

Default pattern, overridden by `naming.pattern`:

```
<issue-date>_<supplier-slug>_<invoice-number>_<total><currency>.<ext>
2026-02-13_hetzner_INV-12345_89.50EUR.pdf
```

- **Date first, ISO format.** It is what makes any folder sortable by any tool, including a human scrolling.
- **Supplier slug is the canonical name**, lowercased, non-alphanumerics to hyphens. The alias never appears in a filename — that is the whole point of normalizing (`suppliers.md`).
- **Invoice number sanitized** to `[a-z0-9._-]`, case preserved where the supplier uses case meaningfully. Slashes in invoice numbers are common and must become hyphens.
- **Total with its currency, no symbol.** `89.50EUR` sorts and greps; `€89,50` does neither.
- Length: keep the whole name under about 100 characters so it survives being emailed, zipped, and opened on a system with a path limit. Truncate the supplier slug, never the number or the date.
- A credit note uses the same pattern with its own number and a negative total (`-118.00EUR`), so it sorts next to what it credits.

## Layout

```
archive/
├── 2025/
│   ├── 01/ … 12/
└── 2026/
    ├── 01/
    └── 02/
        └── 2026-02-13_hetzner_INV-12345_89.50EUR.pdf
```

- **Chronological, cut by issue month** (`naming.archive_cut` accepts `month`, `quarter`, `year`).
- **Never one folder per supplier as the primary tree.** Suppliers get renamed, merged, and misspelled; the tree fragments, and the question that actually gets asked — "what did Q2 cost" — becomes unanswerable without walking every folder. The supplier dimension is resolved through the ledger, which is cheap to filter and impossible to misspell.
- Cut by **issue** month even when payment falls in another month, so the archive and the accrual-basis report agree by construction (`period-close.md`).
- A hybrid Factur-X PDF is one file. A structured invoice delivered as XML plus a human-readable PDF is two files with the same base name, and the ledger points at the XML.
- Non-invoice documents that must be kept — a customs declaration, a signed contract that a recurring invoice references — live in `archive/<year>/<month>/` alongside, with a suffix naming what they are (`_customs`, `_contract`), and are referenced from the ledger row rather than getting their own.

## Byte Integrity

The archive's value is that it holds what the supplier sent, not a version of it (Rule 1).

- **Never re-save, re-compress, flatten, crop, rotate-and-save, or "optimize" a stored file.** Re-generating a PDF strips an embedded XML payload and invalidates a qualified electronic signature, and a Facturae or FatturaPA invoice without its signature is no longer the legal document.
- **Never redact.** If a document contains something the user does not want in an export, the export drops it — the archive keeps the original (`period-close.md`).
- **Corrections go in the ledger row**, with the reason. A wrong amount on a supplier's invoice is fixed by the supplier issuing a credit note or a corrected invoice, both of which arrive as new documents (`disputes.md`).
- **Record a content hash at filing time** when the user wants provable integrity: a `Hash` column in the ledger, computed once, never recomputed into the row. Its purpose is to detect later alteration — a hash stored in the same row it validates is weak, so a copy of the ledger in the backup is what gives it teeth.
- Set the archive read-only at the filesystem level if the user asks; it prevents the accidental "helpful" re-save more effectively than any rule.

## Retention

Retention runs from the **end of the tax year**, not the invoice date — a January invoice and a December invoice from the same year expire together. Default `retention_years` = 10, overridden upward by `country` rules and never downward without the user saying so explicitly.

Three clocks run at once and the longest wins:

1. **Tax.** How long the authority can review or reassess the period.
2. **Commercial and accounting.** Company law usually requires books and vouchers for longer than the tax clock. This is the one people forget when they purge at the tax period.
3. **Asset-specific.** Capital goods and property carry their own multi-year adjustment periods in VAT regimes, so the invoice for a building or a major asset outlives the ordinary rule by years.

Country figures and their sources: `countries.md`. Two rules that hold everywhere:

- **An open dispute, audit, or legal proceeding suspends every clock** on anything related to it. Nothing in scope is purged while a matter is live.
- **Readability is part of the obligation.** Keeping a file whose format nobody can open in year nine satisfies nothing. PDF/A is the archival format for exactly this reason; a proprietary format that arrived from a supplier is kept as received and, if it is exotic, accompanied by a PDF rendering with a `_render` suffix.

## Backups And Restore

An archive with one copy is not an archive.

- **Second copy, different medium or location.** The failure this protects against is not disk failure alone; it is a sync client deleting a folder everywhere at once.
- **The ledger travels with the archive.** A backup of PDFs without the index is a box of unsorted paper.
- **Test the restore, on a cadence** (`## Due`, default quarterly): pick one file at random from a year that is not the current one, restore it, and open it. Untested backups fail on the details — a permissions change, a broken sync, an encrypted volume whose passphrase nobody recorded. That passphrase, incidentally, is a `<kind:locator>` pointer and never a stored value.
- Record the restore test's date and what was restored in `## Due` and, if it failed, in `## Open Items`. A backup last verified two years ago is functionally unverified.

## Producing Documents On Demand

The day the archive earns its keep. What is asked for, in practice:

| Request | What to produce |
|---|---|
| "Invoice X from supplier Y" | The archive file, plus its ledger row for context |
| "Everything from this supplier in year N" | Ledger rows filtered, then the files; the row list usually settles it without opening one |
| "The whole quarter for the tax authority" | Files plus a CSV index, boundary stated (issue date), credit notes included as negative rows |
| "Proof this file has not been altered" | The hash recorded at filing time, and the backup copy that carries an independent version of the ledger |
| "The supporting invoice for this bank line" | Reverse lookup by amount and date across a ±5 day window; if nothing matches, that is the finding, not a search failure |

Anything produced for a third party is an export, not a copy of the archive, and it drops what the recipient does not need (`period-close.md`).

## Purging

Purging is proposed, never performed silently.

1. Compute the eligible set: everything whose retention clock has fully expired for `country` and `retention_years`, excluding anything under dispute, audit, or an asset-specific clock.
2. Report it as a count, a period range, and a total value — not a file list.
3. Delete only after explicit confirmation, and **write what was purged** to `## Filings` or an artifact: period, count, date, who confirmed. A gap in the archive with no record of why is indistinguishable from a loss.
4. The ledger rows stay. They are small, they are the only remaining evidence the invoice existed, and deleting them makes historical totals silently change.

## Personal Data

Invoices carry names, addresses, and occasionally more. Three consequences that are operational, not decorative:

- **Exports carry only what the recipient needs.** An accountant needs supplier, amounts, and tax data; an analysis spreadsheet needs neither addresses nor names of individuals.
- **Deletion requests do not override retention.** A legal obligation to keep an accounting document outranks a request to erase it; the answer is that the data is retained under that obligation and used for nothing else.
- **Sharing is confirmed before it happens**, with the recipient named. Nothing leaves the machine on inference.

**Write before you finish**: every filed document has its ledger row in the same turn; a new ledger year, a new archive location, or a first backup target gets its `## Boxes` line; a restore test writes its date to `## Due`; a purge writes its record to `## Filings` (`memory-template.md`).
