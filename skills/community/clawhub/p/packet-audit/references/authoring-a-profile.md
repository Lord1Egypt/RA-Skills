# Authoring a profile

A profile is a JSON file in `profiles/`. It declares what a packet of a given kind must
contain, which fields must agree, and how long credentials must stay valid. The engine is
generic; the profile is the only thing that knows about visas or insurance.

## Schema

```json
{
  "id": "professional-licence",
  "title": "Professional licence application",
  "date_order": "mdy",
  "money_tolerance": 0.0,
  "review_note": "Shown in every report. Say what this profile does not know.",
  "classify": [ { "type": "photo_id", "ext": [".pdf"], "content": ["passport number"] } ],
  "fields": { "full_name": { "label": "Full name", "normalizer": "name", "patterns": [ { "regex": "..." } ] } },
  "document_fields": { "photo_id": ["full_name"] },
  "required": [ { "type": "photo_id", "label": "photo ID", "alternates": [] } ],
  "validity": [ { "doc_type": "photo_id", "field": "id_expiry", "min_days_after_decision": 30, "severity": "error", "reason": "why" } ],
  "consistency": [ { "field": "full_name", "primary": "photo_id", "severity": "error" } ]
}
```

All keys are required, even when empty (`"validity": []`). Validation runs at load time and
refuses an unknown field, an unknown document type, an unparsable regex, or a normalizer that
does not exist — a profile cannot half-work.

### id, title, review_note

`id` is lowercase words joined by hyphens and must match the file name. `review_note` is
copied into the report under the profile block: use it to say which requirements this profile
approximates and what the user must confirm with the authority.

### date_order

`mdy` or `dmy`. This resolves ambiguous dates like `03/04/2026` deterministically. When the
first component cannot be a month, the parser flips it; when both components could be a
month, `date_order` decides. Never leave this to guesswork.

### classify

Ordered list; the first rule that matches wins. A rule matches when:

- `ext` is present and the extension is in the list, **and**
- if `filename` is present, at least one pattern matches the relative path, **and**
- if `content` is present, at least one pattern matches the extracted text.

A rule with both `filename` and `content` requires both, which is precise but brittle; a rule
with only `content` is robust to any file name. A common shape is: precise content rules
first, filename-only fallbacks after them, `unknown` implicitly last.

### fields

Each field has a `label` (shown in reports), a `normalizer`, and one or more `patterns`. The
first match in a document wins, so order patterns from most to least specific. Patterns are
compiled with `re.I | re.M`, and `^` therefore anchors to a line.

Normalizers decide how two values are compared:

- `name` — strips accents, titles, punctuation; sorts tokens, so word order does not matter.
- `address` — lowercases, drops punctuation, expands a small synonym set (`street` to `st`),
  then compares street number, postal code, and token overlap.
- `date` — parses to ISO using `date_order`; unparsable values become `null` and raise `PA-X02`.
- `money` — strips currency and separators; compared with `money_tolerance`.
- `text` — casefold and whitespace collapse; differences are `PA-C02` variants, not conflicts.

Use `group` inside a pattern only when the value is not the first capture group.

### document_fields

```json
"document_fields": { "payslip": ["full_name", "employer", "monthly_income"] }
```

Every field listed must be found in every document of that type, or `PA-F01` fires. Keep
this list to values the document type reliably prints; if a bank statement sometimes omits
the address, do not require it there.

### required

```json
"required": [ { "type": "payslip", "label": "proof of income", "alternates": ["bank_statement"] } ]
```

`type` is the primary expectation; `alternates` are accepted substitutes. The label is what
the report shows when nothing matched.

### validity

```json
"validity": [ { "doc_type": "passport", "field": "passport_expiry", "min_days_after_decision": 90, "severity": "error", "reason": "three months beyond departure" } ]
```

`doc_type` must also be in `required`. The field must be an expiry-like field with the `date`
normalizer. `reason` is printed with the finding, which is what makes the finding actionable.

### consistency

```json
"consistency": [ { "field": "full_name", "primary": "photo_id", "severity": "error" } ]
```

`primary` names the document type whose value is treated as correct. Without it, the first
document in path order wins, which is arbitrary — always set it. `severity` defaults to
`error`; set `warning` for fields where a wording difference is tolerable (employer names are
a good example).

## Worked example: add a licensing packet

1. Copy `profiles/rental-us.json` to `profiles/professional-licence.json`.
2. Change `id` to `professional-licence` and `title`.
3. Rewrite `classify` for the document types the board asks for: photo ID, degree
   certificate, transcript, reference letters, application form, fee receipt.
4. Keep the fields that appear across documents (`full_name`, `date_of_birth`, `address`);
   add board-specific ones (licence number, exam date) with their labels.
5. Set `required` to the board's list, with alternates where the board accepts substitutes.
6. Set `validity` for the ID, and leave the degree alone.
7. Set `consistency` with a `primary` for every field — the application form is usually the
   right primary for address, the ID for name and date of birth.
8. Validate:

```bash
python3 scripts/packet_audit.py --profile professional-licence --folder ./sample --decision-date 2027-06-01
```

A profile that loads is not a profile that is right: build one clean packet and one packet
with a seeded error, and confirm the clean one produces no findings.

## Pitfalls that have already bitten

- **A field pattern that matches its own label.** `name` alone will match `Name of bank:` in a
  statement. Anchor patterns with `^` and require the separator.
- **`primary` naming a type that is optional.** An absent primary is fine and silent, but a
  primary that is *present* and does not yield the field raises `PA-C03`, so make sure its
  field labels are covered by the patterns.
- **Money with thousands separators and no decimals.** `4,200` and `4.200` are different
  numbers in different locales; `money_tolerance` does not fix that, `date_order`-style
  locale declaration would. Keep the packets you audit in one locale.
- **Duplicates.** Two identical files are compared once, so a repeated payslip cannot
  manufacture a phantom conflict. `PA-D01` still reports the duplicate.
- **Images.** A photographed ID always raises `PA-R01`. If a profile's required document is
  routinely a photo, the profile should say so in `review_note` rather than pretend the
  audit checked it.
