# packet-audit

Checks a folder of submission documents for the three failures that get complete packets
rejected: a required document that is not there, a credential that expires before the
decision date, and a field that disagrees between two documents.

```bash
python3 scripts/packet_audit.py --folder ./my-packet --profile rental-us --decision-date 2027-06-01
```

```
verdict: NOT READY
errors: 4  warnings: 1  notes: 1
  [error  ] PA-C01  Values disagree across documents: Current address: street number 512 vs 448.
  [error  ] PA-C01  Values disagree across documents: Full name: different names (token overlap 33%).
  [error  ] PA-C01  Values disagree across documents: Monthly income: 4,000.00 vs 4,200.00.
  [error  ] PA-X01  Document expires too soon: id.txt expires 2026-12-01; the packet needs it
                    valid until at least 2027-07-01 (agents reject IDs that expire inside the
                    application window).
  [warning] PA-R01  Document could not be read: photo.jpg: image: needs OCR, which this skill
                    does not perform.
  [info   ] PA-D01  Duplicate file: application.txt is byte-identical to application copy.txt.
report: ./my-packet/.packet-audit/packet-report.md
```

Every finding names the files it came from and, for PDFs, the page. The audit also writes a
JSON report with a stable schema and a manifest of SHA-256 hashes for the exact packet that
was checked.

## Why

Existing packet tooling stops at "here is a checklist" or "here is a draft letter". The step
that actually fails — proving the documents agree with each other — is left to the human at
the counter. An agent with the right rules can do it exhaustively in one pass; this skill is
those rules, made deterministic.

## Design

- **Profiles are data.** `profiles/*.json` declares document types, required fields, validity
  windows, and which document is authoritative for each cross-check. Adding a packet type
  does not touch the engine.
- **Offline.** No network imports, no subprocess, no model calls, no package installs at
  runtime, and no third-party package is needed to read a PDF. `pypdf` is used only as a
  fallback when it is already present.
- **Honest about the unreadable.** Images and image-only PDFs are reported, never guessed at.
  A text dump beside the file (`<name>.pdf.txt`) is used and disclosed as a sidecar.
- **Deterministic.** Sorted traversal, `--now` for a pinned timestamp, normalized comparison
  so `448 Cedar Street` and `448 Cedar St` agree.

## Install

```bash
npx --yes clawhub@0.23.3 install deepseekoracle/packet-audit@1.1.1
```

## Use

```bash
python3 scripts/packet_audit.py --list-profiles
python3 scripts/packet_audit.py --folder ./packet --profile schengen-visa --decision-date 2027-06-01
python3 scripts/packet_audit.py --folder ./packet --profile rental-us --json > audit.json
```

Exit codes: `0` clean, `1` warnings, `2` blocking findings, `3` bad input.

## Test

```bash
python3 -m unittest discover -s tests
python3 scripts/self_check.py
```

The suite builds every fixture in a temporary folder — clean packet, seeded mismatches,
missing documents, `.docx` and sidecar extraction, profile validation, and CLI behaviour —
so the tests cannot drift from the documents they check.

## Limits

No OCR, no legal or eligibility advice, no forgery detection, and no PDF text without a
real text layer (a scan is reported, not read). `references/limits.md` lists the rest, and each bundled profile carries
a `review_note` telling the user what to confirm with the authority.

## License

MIT-0.
