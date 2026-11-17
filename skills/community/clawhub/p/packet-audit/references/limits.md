# Limits

The value of an audit is that its silences are trustworthy. These are the things Packet
Audit does not do, stated so a reader can tell "checked and agreed" from "not checked".

## Not OCR

Images (`.png`, `.jpg`, `.tif`, `.bmp`, `.webp`, `.heic`) are never read. An image-only PDF
is detected as having no text layer and reported, not processed. The finding is
`PA-R01` with the reason spelled out. A photographed passport therefore *always* shows up as
unreadable, and the packet cannot reach `READY` while it is a required document.

Workaround that stays inside the skill's honesty rules: put a text dump beside the file as
`<name>.pdf.txt` (or convert the document to `.docx`/`.txt`). The engine uses the sidecar and
records `extraction: sidecar` in the inventory, so the report shows that the text came from a
sidecar rather than from the file itself.

## PDF: text layer only

PDF text is read by the bundled `scripts/pdftext.py`: standard library only (objects and
object streams, Flate/ASCIIHex/ASCII85 filters, the page tree, `Tj`/`TJ` with per-font
`/ToUnicode` maps and `/Widths`-based word gaps). Findings cite `p1`, `p2`, and so on.
What it will not do:

- OCR an image-only or scanned PDF, or read text baked into a picture: reported as
  `pdf has no extractable text layer (scan or image-only)`.
- Decrypt an encrypted PDF: reported as `pdf is encrypted; its text cannot be read without
  the password`.
- Render or reflow: two-column pages can interleave, and words are reconstructed from
  positioning, so a word split by an unusual kerning jump may come back as two.

`pypdf`, when it is already installed, is tried only after the bundled reader fails.

## Not comprehension

Classification and field extraction are pattern-based. Consequences:

- A value expressed in prose ("she earns about four thousand a month") is not extracted and
  will raise `PA-F01`.
- A value inside a table image or a scanned table cell is not extracted.
- A label not covered by the profile's patterns (`Surname:` against a `Full name:` pattern)
  is not extracted. The fix is a profile change, not a retry.
- A field that appears twice in one document yields the first occurrence; the engine does not
  reconcile a document against itself.

## Not legal, tax, or eligibility advice

The audit compares documents to each other and to the profile's checklist. It does not know
whether a person qualifies for a visa, a tenancy, a benefit, or a payout, and it does not
interpret law. Profiles carry a `review_note` in every report because the authority's real
checklist changes and is authoritative.

## Not a fraud or forgery detector

Two documents agreeing does not make them genuine. The audit has no baseline for what a real
payslip, passport, or bank statement looks like, and it does not check metadata, fonts, or
issue patterns. It compares values.

## Not jurisdiction-aware

Profiles encode one country's common practice, and the two bundled US/EU profiles are starting
points. Validity windows, notarisation, apostille, translation, and certified-copy rules are
jurisdiction-specific and are not modelled beyond the explicit `validity` entries.

## Not a signature or completeness-of-execution check

The engine does not verify that a form was signed, witnessed, dated by hand, or initialled on
each page. It checks that documents exist, are readable, carry the fields the profile names,
and agree where they overlap.

## Not a substitute for the authority's checklist

The profile is a declared checklist. If the authority asks for something the profile does not
know about, the audit will call the packet `READY` correctly against the profile and wrongly
against the authority. Always compare the profile to the authority's current list before
submitting, and update the profile when it drifts.

## Determinism and repeatability

Given the same folder, profile, and `--decision-date`, the findings and the manifest are
identical; `--now` pins the timestamp so two runs can be diffed byte for byte. File order is
sorted, so the report does not depend on filesystem enumeration order.

## What it is good at

Cross-document agreement on a handful of high-consequence fields, presence of required
document types, and expiry windows — the three failures that get otherwise complete packets
rejected.
