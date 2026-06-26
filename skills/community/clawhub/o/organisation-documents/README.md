# organisation-documents

> Claude skill for **French accounting firms** (`cabinets comptables`). Receives accounting documents (invoices, bank statements), identifies the client of the firm by reading bank statements, and classifies each PDF into a per-client / year / month folder tree. Deterministic script-driven — never guesses.

## What it does

For each invocation, the skill runs **one command** :

```bash
python3 scripts/main.py <inbox_dir> <clients_root>
```

That script:

1. **Deduplicates** files by SHA-256 (already-classified docs are skipped, listed in `_index.json`).
2. **Extracts** each PDF with `scripts/extract.py` (`pdftotext -layout` + deterministic regexes — no LLM-eyeballing).
3. **Phase 1 — bank statements first.** The account holder shown on the statement header **is** the client of the firm (unambiguous). For each statement, create/complete the `clients.json` entry and file the statement into `<slug>/<AAAA>/<MM>/bank-statements/`.
4. **Phase 2 — invoices.** Compare emitter and recipient (extracted from the PDF) against `clients.json`. One side matches a known client → that's the firm's client ; emitter ≈ client → `invoices/out/`, recipient ≈ client → `invoices/in/`.
5. **Phase 3 — others** : files that are neither invoices nor bank statements → `_non-attribue/`.
6. Writes `clients/clients.json`, `clients/_index.json`, `clients/_report.json`, and prints a short summary.

The agent's job is then only to **read `_report.json` and relay it to the accountant in plain French** — including any onboarding question when the client of a new invoice is ambiguous.

## Onboarding for ambiguous senders (the "Corse Plomberie" case)

An invoice always carries two companies. When neither is yet in `clients.json` and no bank statement covers them, the script does not guess :

1. **Step 1** — the document lands in `clients/_a-identifier/` and a question is added to `_report.json → questions` :
   > « Document : facture `TUYO-2024-087` (348,50 € TTC). Émetteur « TUYO SARL », destinataire « Corse Plomberie ». Lequel est votre client ? »
2. **Step 2** — when the accountant answers « it's Corse Plomberie », the agent adds the mapping to `clients.json` (`contacts[].email = <sender>`) and re-runs the script on `_a-identifier/`. The piece gets filed correctly, in the right direction (in/out). **The question is never asked again** for that sender.

## Output tree

```
clients/
├── clients.json                    ← clients of the firm (auto-derived from bank statements + accountant confirmations)
├── _index.json                     ← sha256 → classified path (dedup)
├── _report.json                    ← last-run report (questions, incomplete, classified, ignored)
├── _a-identifier/                  ← pieces awaiting accountant disambiguation
├── _incomplet/                     ← extraction-incomplete pieces (date or TTC missing)
├── _non-attribue/                  ← non-accounting documents
└── <slug>/
    └── <AAAA>/<MM>/
        ├── bank-statements/<AAAA-MM>_<bank>.pdf
        └── invoices/
            ├── in/<AAAA-MM-JJ>_<N°Facture>_<Counterparty>_<MontantTTC>.pdf
            └── out/<AAAA-MM-JJ>_<N°Facture>_<Counterparty>_<MontantTTC>.pdf
```

Invoice numbers in filenames are extracted from PDF content (e.g. `N° F1-2026-0003`) — not guessed. If absent in the PDF, the script writes `SANS-NUM` and flags the piece for review. **No invented values, ever.**

## Why script-driven

Earlier versions let the agent classify documents by reading PDFs and inventing field values. Result : invoice numbers like `"N"`, `"des"`, `"um-rix"`, total amounts of `0.00`, and downstream reconciliation collapse. The current SKILL.md forbids LLM-eyeballed classification and mandates `scripts/main.py`. The extraction logic lives entirely in `scripts/extract.py` (`pdftotext -layout` + named-group regexes for `N°`, `TOTAL TTC`, `SIRET`, transaction lines, etc.).

## Prerequisite

The script calls `pdftotext` (package `poppler-utils`). Install it once on the runtime :

```bash
apt install poppler-utils   # Debian/Ubuntu
brew install poppler        # macOS
```

## Companion skill

- [`rapprochement-bancaire`](https://github.com/developers-trendex/rapprochement-bancaire) — reconciles bank transactions with the invoices classified here. Consumes the same `clients/<slug>/...` tree.

## Files

| File                              | Purpose                                                                |
| --------------------------------- | ---------------------------------------------------------------------- |
| `SKILL.md`                        | Skill definition (French) — the "when and how to relay" layer          |
| `scripts/main.py`                 | Entrypoint — classification, `clients.json` bootstrap, report          |
| `scripts/extract.py`              | Deterministic extractor (only place that touches `pdftotext`)          |
| `references/structure-cible.md`   | Reference — path/naming conventions, enums                             |
| `references/contrat-io.md`        | Reference — JSON I/O contract                                          |
| `references/validation-fr.md`     | Reference — French legal validation rules                              |
| `references/roadmap.md`           | Roadmap                                                                |
| `data/`                           | Sample data for tests                                                  |

## License

Internal — OpenClaw private use.
