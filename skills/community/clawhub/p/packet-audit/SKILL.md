---
name: packet-audit
description: "Use when documents must be submitted to an authority and pass first time — visa, rental, mortgage, benefits, insurance, grant, licensing — to check the folder for missing, expired, or mutually inconsistent documents with page-level citations. Offline, deterministic, no model calls. Not legal advice, not an eligibility decision, not OCR."
metadata: {"version": "1.1.1", "license": "MIT-0", "offline": true, "entrypoints": ["scripts/packet_audit.py", "scripts/self_check.py"]}
---

# Packet Audit

A submission packet fails on the details nobody cross-checks: the address on the bank
statement is last year's, the passport expires two weeks before the decision date, the
name on the payslip has an `e` where the passport has an `a`. Packet Audit walks a folder
of documents, extracts the fields that must agree, and reports every disagreement,
missing document, and expired credential with the file and page it came from.

It produces evidence, not prose: a findings list, a document inventory with SHA-256 per
file, and a JSON manifest of the exact packet that was checked.

## When to use

- A set of documents is about to be submitted and acceptance matters: visa or residence
  application, rental application, mortgage or refinance file, benefits claim, insurance
  claim, grant or tender response, professional licensing.
- A previous submission was rejected and the user needs to know which document caused it.
- Someone is assembling a packet for another person (family member, client, employee)
  and needs a second pair of eyes that cites sources.
- A records folder has accumulated duplicates, scans, and stale credentials and needs a
  defensible inventory before it goes anywhere.

## When not to use

- Deciding whether someone qualifies. This skill checks documents against each other and
  against a declared checklist; it never decides eligibility.
- Legal, tax, or immigration advice. It cites what the packet says, not what the law allows.
- Reading photographed or scanned pages. Images and image-only PDFs are reported as
  unreadable; this skill does not perform OCR and will not guess at a value.
- Writing the application, the cover letter, or the appeal. Use a drafting skill for that,
  then run this one over the result.
- Auditing a single document against itself (numbering, cross-references, terminology) —
  that is an editorial check, not a packet check.

## Quickstart

```bash
npx --yes clawhub@0.23.3 install deepseekoracle/packet-audit@1.1.1
```

```bash
python3 scripts/packet_audit.py --list-profiles
python3 scripts/packet_audit.py --folder ./my-packet --profile rental-us --decision-date 2027-06-01
python3 scripts/packet_audit.py --folder ./my-packet --profile schengen-visa --decision-date 2027-06-01 --json
```

The audit writes three files into `--out` (default `<folder>/.packet-audit`):
`packet-report.md`, `packet-report.json`, `packet-manifest.json`.

Exit codes: `0` clean, `1` warnings only, `2` blocking findings, `3` bad input. A CI job or
an agent can gate on the exit code without parsing prose.

## Bundled profiles

| Profile | Packet | Blocking rules |
|---|---|---|
| `rental-us` | US rental application | photo ID present and valid 30 days past the decision date, proof of income, completed form, name/address/income agree |
| `schengen-visa` | Schengen short-stay visa | passport valid 90 days past the decision date, insurance cover live, accommodation, funds, itinerary, name/DOB agree |
| `insurance-claim-property` | Property insurance claim | policy schedule, claim form, invoice or proof of ownership, damage photographs, policy number and loss date agree |

Profiles are data, not code: a new packet type is a new JSON file, and the engine does not
change. See `references/authoring-a-profile.md`.

## Finding codes

| Code | Severity | Meaning |
|---|---|---|
| `PA-E01` | error | A required document type is absent from the packet |
| `PA-X01` | error | A document expires before the profile's validity window closes |
| `PA-C01` | error | A field disagrees across two documents |
| `PA-C02` | warning | A field differs only in spelling or wording |
| `PA-C03` | warning | The authoritative document is in the packet but does not show the field, so agreement is checked against a fallback |
| `PA-F01` | warning | A required field was not found in a document that should carry it |
| `PA-X02` | warning | An expiry date could not be parsed |
| `PA-R01` | warning | A file could not be read (image, scan, or no PDF text layer) |
| `PA-D01` | info | Two files are byte-identical |
| `PA-U01` | info | A file matched no document type and was not checked |

`references/finding-codes.md` carries the full detail, including what each finding looks
like in the report and how to act on it.

## Outputs

- `packet-report.md` — verdict, findings table, document inventory, extracted values, next actions.
- `packet-report.json` — the same content with a stable schema (`packet-audit/report/1`),
  including the profile id and its SHA-256 so a result can be reproduced.
- `packet-manifest.json` — path, size, SHA-256, classified type, and readability per file.

## Permissions

- **Filesystem, read:** the folder passed to `--folder`, recursively.
- **Filesystem, write:** only `--out` (default `<folder>/.packet-audit`).
- **Network:** none. No upload, no telemetry, no model call, no package install at runtime.
- **Subprocess:** none.
- **Environment:** none required, and no third-party import is needed to read a PDF: the
  bundled `scripts/pdftext.py` is standard library only. `pypdf` is used only as a fallback
  when it is already importable; the skill never installs or fetches anything.

## Limits and non-claims

Text comes from `.txt`, `.md`, `.csv`, `.json`, `.docx` and `.pdf` with the standard library
(a sibling `<name>.pdf.txt` text dump is used when one exists). A PDF needs a text layer:
encrypted files and scans are reported with that reason, never guessed at. Classification and field extraction are
pattern-based heuristics, not comprehension: a document that hides a value inside prose or
inside a table image will come back as `PA-F01`, not as a wrong value. Confirm the
authority's own checklist before submitting — the bundled profiles are starting points, and
`references/limits.md` lists the rest of what this deliberately does not do.

## References

- `references/finding-codes.md` — every code, its severity, and the action it implies.
- `references/authoring-a-profile.md` — profile schema, worked example, validation rules.
- `references/limits.md` — what the audit cannot see, and why it says so instead of guessing.

## Self-check

```bash
python3 scripts/self_check.py
python3 -m unittest discover -s tests
```

The self-check runs one named rule per known release hazard (version agreement, profile
validity, no network imports, no absolute paths, pinned installs, compilation, CLI smoke,
no HTML comments, test presence, declared scope) and exits non-zero if any rule fails.
