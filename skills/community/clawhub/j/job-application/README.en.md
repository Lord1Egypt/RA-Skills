# Job Application Skill for OpenClaw

[Deutsche Dokumentation](README.md)

The skill creates a truthful, tailored one-page CV, cover letter, and plain-text
application from structured profile data. Bundled data is fictional. It never
sends or publishes an application.

## Requirements

- Python 3.10+
- `pdflatex` for PDFs
- The LaTeX `fontawesome5` package for CV contact icons
- Poppler (`pdfinfo`, `pdftotext`) for mandatory PDF quality validation
- optional Bash wrapper on Linux/macOS

Keep real profiles, photos, signatures, and output outside the installed skill directory:

```text
JOB_APPLICATION_DATA_DIR=/path/to/private/job-application-data
JOB_APPLICATION_PROFILE_DIR=/path/to/private/profile
JOB_APPLICATION_OUTPUT_DIR=/path/to/applications
```

When `JOB_APPLICATION_OUTPUT_DIR` is unset, applications are created under
`$JOB_APPLICATION_DATA_DIR/applications`; when the data root is unset, the
platform user-data directory `openclaw/job-application` is used. Without
`JOB_APPLICATION_PROFILE_DIR`, only the bundled fictional profile is used. See
`PUBLISHING.md` and run a ClawHub publish dry-run before publishing.
When the installed skill lives inside a larger Git repository, use the
whitelist-only staging export documented there rather than publishing the
installed directory directly.

For real applications, use the same external profile directory for both the CV
and cover letter. Either configure `JOB_APPLICATION_PROFILE_DIR` or pass it
explicitly:

```text
python3 scripts/generate_cover_letter.py --content application_content.json --output cover_letter.tex --profile-dir /path/to/private/profile
python3 scripts/render_application.py <application-directory> --profile-dir /path/to/private/profile
```

The cover-letter generator refuses to silently fall back to the fictional
bundled profile for an external application. The PDF validator also checks the
cover-letter header for the selected profile's name, email, phone, and address.

## Reproduce the public example

This command uses only the bundled fictional profile data, including the
fictional signature asset, and writes its output outside the installed skill:

```text
python3 scripts/render_example.py --output /tmp/job-application-example
```

It generates `CV.pdf`, `cover_letter.pdf`, and `indeed_text.txt`, then runs the
mandatory PDF validation. PDF timestamps may differ between runs; the content,
template, and validation result are reproducible.

## V2 workflow

```text
python3 scripts/prepare_application.py --slug 2026-10-example-demo
python3 scripts/generate_cv_selection.py --job job.json --output cv_selection.json
python3 scripts/generate_cv.py --selection cv_selection.json --output CV.tex
python3 scripts/generate_cover_letter.py --content application_content.json --output cover_letter.tex
python3 scripts/generate_plain_text.py --content application_content.json --output indeed_text.txt
python3 scripts/render_application.py <application-directory>
```

`render_application.py` runs `validate_application.py` by default. It requires
readable CV and cover-letter PDFs, exactly one CV page, no unresolved
placeholders, valid input schemas, in-page text bounds, and useful CV vertical
fill. `--skip-validation` is a visible debug-only escape hatch.

Use `--strict-fill` to make an underfilled CV fail. `--min-vertical-fill` and
`--max-vertical-fill` default to `0.52` and `0.98`.

## Chat delivery

Generated files initially exist only on the local host. A local filesystem path
is not a downloadable link in Telegram, Slack, or most other chat clients. If
the user explicitly requests the documents in the current chat, the handling
agent must attach the already validated `CV.pdf`, `cover_letter.pdf`, and, when
useful, `indeed_text.txt` as native document attachments.

Only the requested final deliverables may be attached. Never send profile JSON,
source files, signature assets, or other private intermediate material. Chat
delivery does not authorize application submission or forwarding documents to a
recruiter.

## Selection, derivation, and migration

V2 `cv_selection.json` records configurable `limits`; defaults preserve the v1
limits. Pass `--limits limits.json` to `generate_cv_selection.py`. The CV
generator rejects unknown IDs, negative limits, duplicates, and selections that
exceed their limits before LaTeX is rendered.

To derive a new application without changing the base:

```text
python3 scripts/prepare_application.py --slug 2026-10-company-role --base-application /absolute/base
python3 scripts/generate_cv_selection.py --job job.json --base /absolute/base/cv_selection.json --mode adaptive --output cv_selection.json
```

`adaptive` prioritizes the new job and keeps base decisions as fallback;
`strict` keeps the base selection. The resulting selection stores local-only
`derived_from` provenance, which is never rendered.

Both cover letter and plain-text generators use one V2
`application_content.json`. Legacy `cover_letter.json` and `indeed_text.json`
remain readable during the documented transition. Convert them with:

```text
python3 scripts/convert_application_content.py --cover-letter cover_letter.json --indeed-text indeed_text.json --job job.json --profile /path/to/master_profile.json --output application_content.json
```

## Tests

```text
python3 -m pytest
```

Tests use fictional data only and cover successful validation plus all documented
failure classes.
