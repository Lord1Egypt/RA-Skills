# Finding codes

Every finding carries a stable code, a severity, a one-line detail, and the documents it
was derived from. Severity drives the verdict and the exit code:

| Severity | Effect on verdict | Exit code |
|---|---|---|
| `error` | `NOT READY` | 2 |
| `warning` | `READY WITH WARNINGS` | 1 |
| `info` | no effect | 0 when nothing else fires |

## PA-E01 — required document missing

The profile's `required` list names a document type that no file in the folder matched.
Alternates count: a profile that accepts a payslip *or* a bank statement stays quiet when
either is present.

Act: add the document, or correct the profile if the authority accepts something else.
The detail names the expected type and the accepted alternates.

## PA-X01 — document expires too soon

A document's expiry date is before `decision date + min_days_after_decision`. The Schengen
passport rule (90 days) and the rental photo-ID rule (30 days) both land here.

Act: renew the document, or move the decision date if the date entered was wrong. The
detail prints both dates so the gap is visible.

## PA-X02 — expiry date could not be parsed

The field was found but the value is not a date the engine understands (for example
`expires: end of 2027`). The finding is a warning, not a pass: an unparsed expiry is never
treated as valid.

Act: read that line of the document and decide manually; if the format is common, extend the
field pattern in the profile.

## PA-C01 — field disagrees across documents

The same field has different values in two documents that both carry it. Comparison is
normalised first, so `448 Cedar Street` and `448 Cedar St` agree, and `Jordan Alvarez` and
`jordan alvarez` agree.

The detail says which part disagreed:

- name: token overlap below 60 percent, reported as a percentage.
- address: street number differs, or postal code differs, or token overlap below 60 percent.
- date: the two ISO dates.
- amount: both amounts, to two decimals.

Act: fix the document that is wrong. The report lists both files with their locators, so the
user can see which side to correct.

## PA-C02 — field differs in wording

Token overlap is at least 60 percent, so it is very likely the same value written differently
(`J. Alvarez` against `Jordan Alvarez`, or an address with a missing `Apt 3B`). Reported as a
warning because it is usually acceptable and occasionally is not.

Act: normalise wording if the authority is strict about exact matches.

## PA-C03 — authoritative document shows no value

A `consistency` rule names a `primary` document type (the passport, the policy, the payslip),
that document is in the packet, and it did not yield the field. Agreement is still checked,
against the first document that carries the value, but the reference is weaker than the
profile intends.

A primary type that is simply absent does not raise this: if it is required, `PA-E01` already
says so; if it is optional, its absence is not a problem.

Act: check that document's label for the field (`Surname:` against a `Full name:` pattern is
the usual cause), or add the label variant to the profile.

## PA-F01 — required field not found

A document of a type listed in `document_fields` did not yield one of the fields it should
carry. Common causes: the value is inside a table image, the label differs from every pattern
(`Surname:` instead of `Full name:`), or the file is the wrong document.

Act: confirm the document actually shows the value; if it does, add the label variant to the
profile's pattern list.

## PA-R01 — document could not be read

The file exists but no text was extracted. Reasons the engine reports verbatim:

- `image: needs OCR, which this skill does not perform`
- `pdf is encrypted; its text cannot be read without the password`
- `pdf has no extractable text layer (scan or image-only)`
- `not a PDF file (no %PDF header)`
- `pdf structure could not be parsed (no objects found)`
- `unsupported file type`

The audit does not guess. An unreadable required document is a warning, and the verdict
cannot be `READY` while one exists.

Act: convert to a text-bearing file, add a sibling `<name>.pdf.txt` text dump, or read that
document manually. Do not treat the audit as having checked it.

## PA-D01 — duplicate file

Two files have the same SHA-256. Harmless in most packets, worth knowing when the folder has
been assembled by several people. Duplicates are excluded from cross-document comparison so
one repeated file cannot produce a pair of identical conflicts.

## PA-U01 — file not classified

The file matched no document type in the profile. It is listed in the inventory and left
alone. If it is a required document under a name the profile does not know, either rename it
or extend the profile's classify rules.

## Reading the verdict

`READY` means: every required type was present, every required field was found, every
validity window held, and every cross-checked field agreed. It does not mean the authority
will accept the packet — it means the packet is internally consistent and complete against
the declared checklist.
