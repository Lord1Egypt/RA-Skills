# Report Number Audit — Reviewer Notes

> Package: `leafather-report-audit` · version 3.5.0 · License: MIT
> This file exists so a non-Chinese-speaking reviewer can judge the skill quickly.
> The skill itself (`SKILL.md`) is written in Chinese because its users are Chinese data analysts.

## What it does (one sentence)

Traces every number in a delivered data report back to the ledger entry, SQL, caliber and data
cutoff date that produced it — and blocks delivery when a number cannot be traced.

## Why it exists

A report usually ships as several files (md / html / pptx / client version). When a source number
is corrected, it is easy to update one file and forget the others. Nobody notices until the client
does. This skill turns "trust me" into "you can re-run it yourself".

## What it reads and writes

| | |
|---|---|
| **Reads** | a local ledger JSON (`report-ledger/1.0`), the report files you point it at, and optionally a local database (DuckDB / SQLite / any CLI that maps SQL→CSV) |
| **Writes** | `audit.md`, `audit.html`, `evidence.csv`, `manifest.json` — in the directory you specify |
| **Network** | **none.** No HTTP client, no telemetry, no update checks. `grep -ri "requests\|urllib\|http"` over `scripts/` returns nothing |
| **Credentials / env** | never read |
| **Files outside the given paths** | never touched |

## Safety posture (why the scary-looking checks are safe)

- **No `eval` / `exec`.** The ledger may contain an arithmetic expression written by a third party.
  Instead of `eval`, it is parsed with `ast` and evaluated by a recursive walker that only accepts
  numbers, `+ - * /`, parentheses and unary signs. Anything else is rejected — verified by
  7 legal / 9 malicious expressions.
- **No shell injection.** SQL is executed through the database driver's own API; subprocesses are
  always built as argument lists (`shell=False`).
- **HTML output is fully escaped.** Report text, context and SQL all pass through `html.escape()`.
  A ledger field containing `<script>alert(1)</script>` renders as text.
- **CSV output is formula-injection safe.** Cells beginning with `= + - @` get a leading `'`, so
  Excel will not execute them. Numeric columns are deliberately left unescaped.
- **No absolute paths in deliverables.** `manifest.json` stores file **names** plus SHA-256 prefixes;
  the reproduce command replaces absolute paths with `<path:filename>`, so the receipt can be shared.

## How to verify it yourself (30 seconds, no database needed)

```bash
cd leafather-report-audit
python3 scripts/rla_selftest.py
# → 7/7 通过   (7 of 7 cases pass; degrades to sqlite3 automatically when duckdb is absent)
```

The self-test builds a small fixture, then asserts that the skill **catches** four classes of
problems (tampered number, cross-file inconsistency, client-version leak, fabricated ledger entry),
that a correct report **passes**, that a multi-file mismatch is reported and highlighted, and that
all four deliverables are complete and the audit ID is stable.

If you want to see it on a real-looking case:

```bash
python3 examples/cross-file-build.py     # builds fixture + ledger + two deliverables (stdlib only)
python3 scripts/rla_audit.py --ledger rla-demo/ledger.json --files report_a.md report_b.html \
    --command "python3 scripts/cmd_sqlite.py --db rla-demo/demo.sqlite" --out rla-demo/audit.md
# → exit code 1 (blocked): one stale number caught, one cross-file mismatch flagged
```

## Known limitations (stated in the tool itself)

- It proves "the number in the report equals the number in the ledger" — **not** that the ledger's
  caliber was chosen correctly. A wrong definition, faithfully recomputed, will still pass.
- Numbers inside images are not scanned; they are reported as "not covered".
- Coverage rate is always disclosed; the tool refuses to declare "pass" when coverage is below the
  configured threshold (default 90%).

## License

MIT. No attribution required. No data leaves the machine.
