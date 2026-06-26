# vCard Projection

Rules for `weave.project.vcard`. Confidence threshold: 0.7. Omit fields below threshold entirely.

## Field map

FN -- name (always include if present)
N -- name_family;name_given (include if both present)
EMAIL -- email
TEL -- phone (E.164 preferred)
ADR -- location_city + location_country only. Never street address.
ORG -- org
TITLE -- occupation
NOTE -- notes (confidence >= 0.7 only)
REV -- record_time (always include)

Never include: id, clay_id, google_resource_name, preferences, relationships, street address, zip, inferred fields.

## Output format

```
BEGIN:VCARD
VERSION:4.0
FN:{name}
N:{name_family};{name_given};;;
EMAIL;TYPE=WORK:{email}
TEL;TYPE=WORK:{phone}
ORG:{org}
TITLE:{occupation}
ADR;TYPE=WORK:;;{location_city};;;{location_country};
NOTE:{notes}
REV:{record_time}
END:VCARD
```

Omit any line where the value is missing or below threshold. One block per person. Separate blocks with a blank line.

All output is labeled DRAFT. No writeback without explicit user approval via `weave.writeback.contacts`.
