# Ebook File Check reference

## Load condition

Read this reference before running the specification check or comparison, diagnosing returned findings, or selecting the local evidence path.

## What it measures

Ebook File Check runs the official EPUBCheck engine against exact EPUB bytes.

`powmcp-epub-check:ebook_check` validates one EPUB against the EPUB 2/3 specification with pinned EPUBCheck 5.3.0 in a no-network sandbox.

Its granularity includes the automated pass state, detected EPUB version, counts for fatal, error, warning, and usage messages, and findings grouped most-severe-first.

A finding can include the EPUBCheck rule ID, internal file path, line, and column.

The result also includes a structural inventory covering spine items, media types, and remote-resource state, plus the SHA-256 of the checked bytes and truncation metadata.

`powmcp-epub-check:ebook_compare` validates two builds sequentially with the same pinned engine and limits. It reports regressions, fixed findings, per-build hashes, EPUB versions, pass states, severity counts, and a ranking based on pass state and blocking findings.

A declared-title mismatch is evidence that the inputs may not be two builds of one publication. Report that flag before interpreting changed findings as regressions.

## Input decisions

### One-build check

Choose exactly one source kind. Use `url` for a direct public HTTP(S) URL to EPUB bytes. Do not use a local path, ChatGPT file ID, cloud-drive share, archive page, viewer page, or authenticated URL that requires login.

Use `file` for one EPUB attached in the conversation. The attachment limit is 25 MB. Do not also send `url`.

Do not ask a user to publish an attached file.

Use `maxMessages` to control the maximum findings returned, most severe first. Its allowed range is 1 to 500 and its default is 200.

Tell the user before the call that it can take up to 110 seconds under the call deadline.

### Two-build comparison

Choose exactly one source kind and exactly two distinct builds. Use `urls` for two direct public HTTP(S) EPUB URLs, baseline first and revised second.

Use `files` for two attached EPUB files, baseline first and revised second. Do not also send `urls`.

Use `maxMessages` to control findings collected per build. Its allowed range is 1 to 300 and its default is 150.

Tell the user before the call that the sequential comparison can take up to 110 seconds under one shared deadline.

## Output to quote

For `powmcp-epub-check:ebook_check`, quote:

- Input identity or returned SHA-256.
- Automated pass state.
- Detected EPUB version or undetected state.
- Fatal, error, warning, and usage counts.
- Rule ID, message, path, line, and column as returned.
- Spine items, media types, and remote-resource state.
- Truncation metadata.

For `powmcp-epub-check:ebook_compare`, quote:

- Baseline and revised SHA-256 values.
- Each build’s EPUB version, pass state, and severity counts.
- Regressions and fixed findings as returned.
- Blocking counts.
- Declared-title mismatch when reported.
- The reported winner or the absence of a winner.

Do not re-derive, round, or embellish figures. Do not infer a defect from a rule ID beyond the returned message.

## Pass and fail scope

A pass establishes that the submitted bytes satisfied the pinned automated EPUBCheck profile with no blocking finding.

Warnings and usage messages can remain after a pass.

A fail identifies blocking specification findings in the submitted bytes. Repair the cited locations and rerun on the remediated artifact.

An undetected EPUB version or truncated findings makes diagnosis incomplete.

A comparison ranking describes automated conformance only. When both builds tie on pass state and blocking count, the tool names no winner.

Absence from the findings is not endorsement.

## Structurally unassessable work

The checker does not render the publication, so it cannot establish appearance or reading behavior in Thorium, Apple Books, Kobo, or other reading systems.

It does not assess accessibility, WCAG, or accessibility metadata. Use Ebook Accessibility Check for that separate job: https://powmcp.com/apps/epub-accessibility-check/

It does not assess editorial quality.

It does not predict store acceptance or assess retailer-specific cover files, trade metadata, DRM choices, watermarking, or extra ingestion rules.

These areas remain unassessable because this evidence step runs the EPUB specification checker rather than a reading system, accessibility checker, editorial review, or retailer ingestion process.

## Failure handling

The packet provides failure messages rather than numeric failure codes.

If both one-build source kinds are supplied, tell the user verbatim: “Ebook check failed: provide either an EPUB URL or an attached EPUB file, not both”

If the comparison source choice is invalid, tell the user verbatim: “Ebook compare failed: provide either two EPUB URLs or two attached EPUB files, not both”

If the comparison does not contain two valid sources, tell the user verbatim: “Ebook compare failed: provide two public EPUB URLs or attach two EPUB build files”

When an invalid-arguments response names a field, correct that field and call again. It is not evidence that the tool is missing.

Do not expose URL query strings, attachment download-URL tokens, or credentials while reporting a source failure.

## Non-PowMCP path

Fetch or retain the same retailer-bound bytes and run the official EPUBCheck CLI or GUI locally. Record the local validator version and an exact-file hash, inspect each returned rule ID and location, repair the package, and rerun.

This path covers automated EPUB specification checking, but it diverges from the pinned PowMCP environment, structured response, and in-session PowMCP evidence. Reading-system, accessibility, editorial, and retailer-specific work remain separate.

## Source of truth

- EPUBCheck conformance role: https://www.w3.org/publishing/epubcheck
- Official EPUBCheck implementation: https://github.com/w3c/epubcheck
- Ebook File Check app: https://powmcp.com/apps/epub-check/
