# Translation input and outputs

Use schema `mochi-translation-qa.v1`. See [the complete sample](../samples/review.json).

- `reportLanguage`: `zh-CN` or `en`, controlling report labels, not the translation target.
- `title`, `sourceLanguage`, `targetLanguage`: supplied task description and language names/codes.
- `sourceSegments`: 1–200 `{id,text}` entries; `targetSegments`: 0–200 entries using corresponding IDs. IDs use letters, numbers, `_` and `-`, at most 40 characters. Text is at most 12,000 characters per segment.
- `glossary`: optional 0–100 `{source,target,caseSensitive?}` entries. Terms are literal, with Latin word boundaries and Chinese substring matching. Plurals, inflections and alternative acceptable translations are not inferred. Agree suitable terms with the user rather than silently inventing a glossary.

Duplicate IDs, missing/empty targets, extra target IDs, omitted numeric spellings, changed source links and missing required terms create errors. Newly added numbers/links create review warnings. Number order is not checked; occurrences are compared. These are consistency checks, not grammar, legal, medical or semantic certification. URL extraction is heuristic and does not fetch destinations or prove links are safe/available.

Input must be a UTF-8 JSON object of at most 1 MiB. Original files are read only. The output parent must already exist and be a real directory. Outputs go into `mochi-translation-qa-UUID/`. Do not request an output filename or use a user-provided string as a path fragment.

`comparison.md` has literal source/target blocks and an issue checklist. `comparison.csv` is UTF-8 with BOM for common spreadsheet importers, RFC4180-style quoted cells and CRLF rows. Cells beginning with whitespace/control/format characters followed by `=`, `+`, `-` or `@` receive an apostrophe; quote/comma/newline content remains one cell. Keep the Markdown/input JSON as the exact text reference when the CSV prefix is visible in another reader.

`report.json` includes structured issue codes and `semanticAccuracyVerified:false`. `run.json` adds generation time and the source input's SHA-256. Exit 0 means only that this script found no blocking mechanical errors; the status remains `review_required`. Exit 2 retains blocked outputs for inspection. Exit 1 means execution/input failure; do not claim a complete report.

Offline self-test on Node 24+:

```text
node --test --test-isolation=none "{baseDir}/tests/check.test.mjs"
```

For a smoke test, use `samples/review.json` as `--input`. The package installs as `<workspace>/skills/mochi-translation-qa/SKILL.md`; inspect it first and run `openclaw skills check`. Format reference: https://docs.openclaw.ai/tools/skills (checked 2026-10-22).
