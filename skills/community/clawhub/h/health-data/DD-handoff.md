# DD Handoff – health-data skill

- **Scope:** Parses Apple Health exports (export.zip or apple_health_export/export.xml) locally. No network calls; the script only heads into temporary files to read XML via `xmlstarlet`.
- **Data sensitivity:** The XML contains PII/PHI (biometric, sleep, heart-rate, location/activity); treat it like medical data. Remove the export (and any derivative JSON) after the analysis, and do not paste raw values into chat or public systems without explicit consent/justification.
- **Temporary storage:** When a zip is provided the script extracts `export.xml` into a `mktemp` file and removes it via a `trap` once the command finishes. There is no persistence beyond the process lifetime. For large exports, expect the temporary file to grow to the size of the XML.
- **Dependencies:** `xmlstarlet`, `jq`, and `unzip` are required. All outputs are read-only, but if any future extension writes reports or logs, re-validate that it never leaks data outside the local environment.
- **Recommendation for reviewers:** Validate that zipped exports remain on disk you control and are deleted after use. Avoid storing copies in shared folders (Dropbox, Google Drive) unless the user explicitly mandates it and appropriate privacy controls are in place.

## Privacy improvements
- `summary` and `export-json` now emit a runtime PHI warning banner to stderr so that every invocation clearly signals the presence of sensitive health data.
- `export-json` streams records per line (avoiding a full-document slurp), warns after 100,000 emitted records when `--limit` is omitted, and supports `--out <file>` to save the JSON to a file created with 600 permissions instead of piping to stdout.
