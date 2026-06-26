# File Workflows

`privacy-protector` supports text-like files plus `.docx` and `.pdf`.

## Output naming

Default file output path:

- `<name>.redacted.<ext>`

Collision-safe suffixes are added when needed.

## Map linkage

For file workflows, redact writes a sidecar map reference:

- `<output-stem>.map.json`

Embedded markers are only used for:

- `.txt` via hash-comment
- `.md` / `.markdown` via HTML comment

All other file types rely on sidecar map linkage only.

Restore flows still accept legacy `modeio-redact-map-id` markers so older redacted files remain reversible after the public rename to `privacy-protector`.

## Assurance policy

Text-like files:

- `best_effort`
- coverage mismatch still enforced for output projections

Structured rich files:

- `.docx` and `.pdf` use `verified`
- coverage mismatch and residual findings fail closed

## Format boundaries

- `.pdf` anonymization is anonymize-only
- `.pdf` de-anonymization is intentionally unsupported
- non-text API-backed anonymization requires mapping entries so redact can safely project changes back to the source format
