---
name: job-application
description: Creates tailored job-application materials from structured profile and job data, including a focused CV, cover letter, plain-text application, and optional local PDF rendering. Use for drafting or rendering an application; do not use for submitting it without explicit authorization.
license: MIT-0
metadata:
  openclaw:
    requires:
      bins: [pdflatex, pdfinfo, pdftotext]
      anyBins: [python3, python, py]
    envVars:
      - name: JOB_APPLICATION_PROFILE_DIR
        required: false
        description: Persistent profile directory outside the installed skill; bundled fictional data is used when unset.
      - name: JOB_APPLICATION_OUTPUT_DIR
        required: false
        description: Persistent application output root outside the installed skill; defaults to the private data root's applications directory.
      - name: JOB_APPLICATION_DATA_DIR
        required: false
        description: Private per-user data root; defaults to the platform data directory under openclaw/job-application.
---

# Job application

Create truthful, role-specific application documents from the bundled structured profile or a profile supplied by the user.

## Privacy and authorization

- Treat all profile and application data as private.
- Never invent qualifications, employment, education, or contact details.
- The bundled profile is fictional demonstration data and may be replaced by the user.
- Do not submit, email, upload, or message an application without explicit authorization for that specific destination.

## Persistent data and inputs

- Profile data: `$JOB_APPLICATION_PROFILE_DIR/*.json` when configured, otherwise the fictional demonstration data in `assets/profile/*.json`
- Application output: `$JOB_APPLICATION_OUTPUT_DIR` when configured, otherwise `$JOB_APPLICATION_DATA_DIR/applications` (or the platform data directory's equivalent)
- Job data: a `job.json` shaped like `examples/job.json`
- Templates: `assets/templates/`

Keep real profiles, photographs, signatures, generated documents, and application history outside the installed skill directory. ClawHub updates may replace that directory. Resolve bundled resources relative to this skill directory, but honor the persistent-data environment variables. Do not assume a username, home directory, workspace layout, messaging channel, or recipient ID. For ClawHub, export the whitelist-only staging directory described in `PUBLISHING.md`, then run the publish dry-run against that staging directory.

## Workflow

1. Create the application folder with `python3 scripts/prepare_application.py --slug <yyyy-mm-company-role>`. For a derived application, add `--base-application <absolute/base-directory>`; its readable, valid `cv_selection.json` is checked before a new directory is created. Use the printed absolute path for all following files. Never overwrite an existing application directory unless the user explicitly requests reuse.
2. Save normalized job details as `job.json`.
3. Run `scripts/generate_cv_selection.py --job <job.json> --output <cv_selection.json>`. Use `--limits <limits.json>` for reviewed CV limits, and optionally `--base <base/cv_selection.json> --mode adaptive|strict` for a derived application. Review its deterministic suggestion and adjust only with facts supported by the profile.
4. Create one `application_content.json` with `schema_version: 2`, `job`, `cover_letter`, and `plain_text` as in `examples/application_content.json`. Keep claims grounded in selected profile records. The legacy `cover_letter.json` and `indeed_text.json` adapters are transitional; use `scripts/convert_application_content.py` to migrate them.
   The cover-letter template renders `job.company` as its own first recipient line. Therefore `cover_letter.recipient` must name only the contact or team, and `cover_letter.company_address` must contain only address/location lines, never the company name again.
5. Generate source documents:

   ```bash
   python3 scripts/generate_cv.py --selection <cv_selection.json> --output <CV.tex>
   python3 scripts/generate_cover_letter.py --content <application_content.json> --output <cover_letter.tex> --profile-dir <profile-directory>
   python3 scripts/generate_plain_text.py --content <application_content.json> --output <indeed_text.txt>
   ```

6. If `pdflatex` is available and PDFs are requested, run the cross-platform renderer:

   ```bash
   python3 scripts/render_application.py <application-dir>
   ```

   Rendering runs `validate_application.py` by default; Poppler's `pdfinfo` and `pdftotext` are required. The visible `--skip-validation` switch is for debugging only. Use `validate_application.py <application-dir> --strict-fill` to make an underfilled CV fail. For an external profile, pass the same `--profile-dir` to the cover-letter generator and renderer (or configure `JOB_APPLICATION_PROFILE_DIR`). The generator refuses an external letter that would silently use the bundled fictional profile, and the validator checks the letterhead against the selected profile.
   On Windows, `py -3` can be used instead of `python3`. Linux and macOS users may alternatively use the `scripts/render_application.sh` wrapper.
7. Return the generated paths and validation result. Deliver files externally only after destination-specific approval.
   - If the user explicitly asks to receive the documents in the current chat and the channel supports attachments, send the validated `CV.pdf`, `cover_letter.pdf`, and (when useful) `indeed_text.txt` as native downloadable document attachments in that conversation.
   - Do not present local filesystem paths or `file://` links as downloadable chat links. They are references for the local host only and are not usable by most chat clients.
   - Never attach source JSON, profile data, signature assets, credentials, or intermediate files. Attach only the final requested deliverables after validation has passed.
   - Treat every chat attachment as destination-specific external delivery. A request such as “send the documents here” authorizes only that current conversation, never an application submission or delivery to a recruiter.

Installation requirements and platform-specific commands are documented in `README.md`. Generated sample PDFs using only fictional data are in `examples/generated/`.

## Content policy

- Default to a one-page CV.
- Default CV limits are five skills, three experience entries, two education entries, one project, three languages, and two achievement sentences per experience. They may be intentionally changed only in the reviewed selection limits; the generator enforces them.
- Prefer evidence relevant to the posting over generic claims.
- Keep each experience entry to the reviewed `achievement_sentences_per_experience` limit (two by default) and make every sentence concise.
- Preserve optional project attribution fields (`organization`, `context`, and `context_label`) so generated CVs can distinguish employer projects from work performed through the candidate's own company.
- Include the profile's available address or location by default, including a street address when supplied. Omit date of birth and a signature image by default. Include a signature image only when the user requests it through `cover_letter.signature_image`. Include a profile photograph only when the user requests one or the supplied profile explicitly declares `profile_picture`; the bundled photo is fictional demonstration material.
- Match the job's language unless the user requests another language.

JSON contains content, Python performs deterministic transformation, and LaTeX handles layout. Do not hand-edit generated LaTeX when the source JSON can be corrected instead.
